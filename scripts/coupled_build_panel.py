#!/usr/bin/env python3
"""Build the FCLR-COUPLED-001 hourly panel from ironflow Hyperliquid liquidation census.

Vectorized pandas construction. Caches to research_state/.cache/fclr_coupled_panel.parquet
so the experiment is restartable without re-reading 2.17M raw rows.

FCLR-NEXT-112: routed through guarded_execute contract. No direct parquet/outcome
reads on blocked branches. The actual ironflow parquet load is an explicit
outcome_loader invoked ONLY after guarded_execute returns READY_FROZEN.
FCLR-NEXT-115 (G1): build() machine-refuses without an explicit outcome_loader;
no direct parquet read exists outside the guarded contract.

Labels only. Features are computed later from label history (decision-time, causal).
Cross-track firewall: Hyperliquid native perps ONLY. No Binance data.
"""
from __future__ import annotations

import json
import os
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from typing import Callable, Dict, Optional

import numpy as np
import pandas as pd

# Guarded-read refusal (machine-refuse; no implicit parquet read).
class GuardedReadRefused(RuntimeError):
    pass

REPO = Path(__file__).resolve().parents[1]
IRONFLOW = REPO / "research_state" / "data_cache" / "ironflow_events"
CACHE = REPO / "research_state" / ".cache" / "fclr_coupled_panel.parquet"
MANIFEST = REPO / "research_state" / "run_manifest.json"

# FCLR-NEXT-124 G1: canonical cache write-scope allowlist for coupled_build_panel.
# READY-path writes may only target the specific cache parquet artifact
# RESEARCH_STATE/.cache/fclr_coupled_panel.parquet (no dir-wide research_state/
# repo-root/wildcards, no Hyperliquid canonical output mutation). Fail-closed
# before any cache write on READY path violations; blocked NO-READY path must
# not invoke cache writes.
_COUPLED_CACHE_ALLOWED_ARTIFACT = (REPO / "research_state" / ".cache" / "fclr_coupled_panel.parquet").resolve()
_COUPLED_DENIED_CANONICAL_MARKERS = (
    "experiment" + "_" + "frontier.json",
    "run" + "_" + "manifest.json",
    "cross" + "_" + "track" + "_" + "decision_log.md",
    "evaluation_summary_FCLR010.md",
)


def _guard_coupled_cache_write_target(target: Path, *, repo: Path = REPO) -> dict:
    """Machine-enforced write-scope allowlist for coupled panel cache artifacts.

    Returns {pass, failures, reason_code, allowed_artifact, target, network, writes_real_research_state}.
    Deterministic; no IO, no network. Validates target is exactly the allowed
    cache parquet artifact (not dir-wide, not repo root, not wildcard, not a
    Hyperliquid canonical output, not escaping repo).
    """
    failures: list[str] = []
    repo_r = Path(repo).resolve()
    rs_r = (repo_r / "research_state").resolve()
    try:
        t = Path(target).resolve()
    except Exception:
        failures.append("target_unresolvable")
        t = Path(str(target))
    allowed = _COUPLED_CACHE_ALLOWED_ARTIFACT
    if str(t) != str(allowed):
        failures.append("target_not_allowed_cache_artifact")
    if not str(t).startswith(str(repo_r)):
        failures.append("target_escapes_repo")
    if any(ch in str(target) for ch in "*?["):
        failures.append("wildcard_not_allowed")
    if str(t) == str(rs_r) or str(t) == str(repo_r):
        failures.append("dir_wide_or_repo_root_not_allowed")
    for m in _COUPLED_DENIED_CANONICAL_MARKERS:
        if m in str(t):
            failures.append(f"denied_canonical_target:{m}")
    # target must be the specific .cache parquet (not an arbitrary research_state path)
    if str(t).startswith(str(rs_r)) and str(t) != str(allowed):
        # allow only the exact cache artifact
        if not failures or failures == ["target_not_allowed_cache_artifact"]:
            failures.append("research_state_non_cache_artifact_not_allowed")
    return {
        "pass": not failures,
        "failures": failures,
        "reason_code": "OK" if not failures else "COUPLED_CACHE_WRITE_SCOPE_VIOLATION",
        "allowed_artifact": str(allowed),
        "target": str(t),
        "script": "coupled_build_panel",
        "network": False,
        "writes_real_research_state": False,
    }


def _load_run_manifest_lfs_aware() -> dict:
    """Read run_manifest.json, transparently smudging Git LFS pointers (no network)."""
    raw = Path(MANIFEST).read_bytes()
    if raw.startswith(b"version https://git-lfs.github.com/spec/v1"):
        r = subprocess.run(["git", "lfs", "smudge", "--"], input=raw, capture_output=True)
        if r.returncode == 0 and r.stdout:
            raw = r.stdout
    return json.loads(raw)


_M = _load_run_manifest_lfs_aware()
_S = _M["split_boundaries_fclr010"]
# FCLR-010 (Track A) manifest carries train/validation/test blocks, NOT a data_window
# key (data_window is a FCLR-009/Track C field). Derive the panel window from the
# frozen FCLR-010 split boundaries: train.start .. test.end.
WIN_START = pd.Timestamp(_S["train"]["start"])
WIN_END = pd.Timestamp(_S["test"]["end"])


def _load_coupled_outcomes(data_path: Path, context: Optional[Dict] = None) -> Dict:
    """Explicit outcome/parquet loader for coupled panel build.

    Invoked ONLY after guarded_execute returns READY_FROZEN. Blocked branches
    never reach this function; no pyarrow/pandas parquet import on blocked paths.
    FCLR-NEXT-124 G1: fail-closed cache write-scope guard before any READY-path write.
    """
    import pyarrow.parquet as pq

    force = (context or {}).get("force", False)
    if CACHE.exists() and not force:
        return {"panel_cached": True, "cache": str(CACHE)}

    files = sorted(f for f in os.listdir(data_path) if f.endswith(".parquet"))
    frames = []
    for fname in files:
        t = pq.read_table(
            data_path / fname,
            columns=["timestamp", "market", "position_side", "notional_usd"],
        )
        df = t.to_pandas()
        m = df["market"].astype(str).str.endswith("-PERP") & ~df["market"].astype(str).str.contains(":")
        df = df.loc[m].copy()
        df["hour"] = df["timestamp"].dt.floor("h")
        df["notional_usd"] = df["notional_usd"].fillna(0.0).astype(np.float64)
        df["is_long"] = (df["position_side"].astype(str) == "long").astype(np.int64)
        df["is_short"] = (df["position_side"].astype(str) == "short").astype(np.int64)
        df["side_count"] = np.ones(len(df), dtype=np.int64)
        frames.append(df[["hour", "market", "side_count", "is_long", "is_short", "notional_usd"]])

    raw = pd.concat(frames, ignore_index=True)
    raw = raw[(raw["hour"] >= WIN_START) & (raw["hour"] <= WIN_END)]

    g = (
        raw.groupby(["market", "hour"], as_index=False)
        .agg(
            cnt=("side_count", "sum"),
            long_cnt=("is_long", "sum"),
            short_cnt=("is_short", "sum"),
            usd=("notional_usd", "sum"),
        )
    )
    symbols = sorted(g["market"].unique().tolist())
    hours = pd.date_range(WIN_START, WIN_END, freq="h", inclusive="left")
    idx = pd.MultiIndex.from_product([symbols, hours], names=["market", "hour"])
    panel = idx.to_frame(index=False)
    panel = panel.merge(g, on=["market", "hour"], how="left")
    for c in ["cnt", "long_cnt", "short_cnt", "usd"]:
        panel[c] = panel[c].fillna(0.0 if c == "usd" else 0).astype(np.int64 if c != "usd" else np.float64)
    panel["y_occ"] = (panel["cnt"] > 0).astype(np.int64)
    panel["y_int"] = np.log1p(panel["usd"])
    panel = panel.sort_values(["market", "hour"]).reset_index(drop=True)
    # FCLR-NEXT-124 G1: fail closed before any READY-path cache write.
    wg = _guard_coupled_cache_write_target(CACHE)
    if not wg.get("pass"):
        raise GuardedReadRefused(
            f"coupled_build_panel cache write refused: {wg.get('reason_code')} failures={wg.get('failures')}"
        )
    CACHE.parent.mkdir(parents=True, exist_ok=True)
    panel.to_parquet(CACHE, index=False)
    return {"panel_cached": False, "rows": len(panel), "symbols": panel["market"].nunique(), "hours": panel["hour"].nunique(), "cache": str(CACHE)}


def build(force: bool = False, outcome_loader: Optional[Callable] = None) -> pd.DataFrame:
    """Build coupled panel.

    FCLR-NEXT-115 (G1): machine-refuses unless an explicit outcome_loader is
    supplied (the guarded READY_FROZEN contract). No direct parquet read exists
    outside the guarded contract — even when a cache file is present.
    """
    if outcome_loader is None:
        raise GuardedReadRefused(
            "coupled_build_panel.build refused: explicit outcome_loader required "
            "(guarded READY_FROZEN contract). No direct parquet read outside guarded contract."
        )
    loaded = outcome_loader(CACHE, {"force": force})
    if loaded.get("panel_cached"):
        return pd.read_parquet(CACHE)
    return pd.read_parquet(CACHE)


def main():
    from scripts.fclr010_guarded_entry import guarded_execute, refusal_payload

    guard = guarded_execute(
        data_path=IRONFLOW,
        pre_reg_path=None,
        repo_root=REPO,
        source_manifest=None,
        admissible_manifest=None,
        admissible_manifest_path=None,
        outcome_loader=_load_coupled_outcomes,
        loader_context={"force": True},
        allow_default_loader=False,
    )
    if guard.get("status") != "READY_FROZEN":
        payload = refusal_payload(
            reason="coupled_build_panel refused: no guarded READY_FROZEN contract (admissible seam + prereg + manifest/data gates). Direct parquet reads bypassed.",
            reason_code="PREREG_OR_MANIFEST_BLOCK_AFTER_DRIFT_PASS",
            script="coupled_build_panel",
            guard=guard,
        )
        payload.setdefault("network", False)
        payload.setdefault("writes_real_research_state", False)
        payload.setdefault("canonical_outputs_mutated", False)
        print(json.dumps(payload, indent=2, sort_keys=True))
        print(f"=== COUPLED_BUILD_PANEL BLOCKED {datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')} ===", flush=True)
        return 1

    loaded = guard.get("outcomes_loaded")
    p = build(force=True, outcome_loader=_load_coupled_outcomes)
    print(f"Panel: {p.shape}  symbols={p['market'].nunique()}  hours={p['hour'].nunique()}")
    print("occurrence rate:", p['y_occ'].mean().round(6))
    print(p.head())
    return 0


if __name__ == "__main__":
    import sys
    sys.exit(main())