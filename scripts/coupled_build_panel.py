#!/usr/bin/env python3
"""Build the FCLR-COUPLED-001 hourly panel from ironflow Hyperliquid liquidation census.

Vectorized pandas construction. Caches to research_state/.cache/fclr_coupled_panel.parquet
so the experiment is restartable without re-reading 2.17M raw rows.

FCLR-NEXT-112: routed through guarded_execute contract. No direct parquet/outcome
reads on blocked branches. The actual ironflow parquet load is an explicit
outcome_loader invoked ONLY after guarded_execute returns READY_FROZEN.

Labels only. Features are computed later from label history (decision-time, causal).
Cross-track firewall: Hyperliquid native perps ONLY. No Binance data.
"""
from __future__ import annotations

import json
import os
from datetime import datetime, timezone
from pathlib import Path
from typing import Callable, Dict, Optional

import numpy as np
import pandas as pd

REPO = Path(__file__).resolve().parents[1]
IRONFLOW = REPO / "research_state" / "data_cache" / "ironflow_events"
CACHE = REPO / "research_state" / ".cache" / "fclr_coupled_panel.parquet"
MANIFEST = REPO / "research_state" / "run_manifest.json"

with open(MANIFEST) as _f:
    _M = json.load(_f)
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
    CACHE.parent.mkdir(parents=True, exist_ok=True)
    panel.to_parquet(CACHE, index=False)
    return {"panel_cached": False, "rows": len(panel), "symbols": panel["market"].nunique(), "hours": panel["hour"].nunique(), "cache": str(CACHE)}


def build(force: bool = False, outcome_loader: Optional[Callable] = None) -> pd.DataFrame:
    """Build coupled panel.

    If outcome_loader is supplied (guarded READY_FROZEN path), it is used to
    load/construct the panel data. Otherwise reads from cache only (no direct
    parquet reads on non-guarded paths).
    """
    if outcome_loader is not None:
        loaded = outcome_loader(CACHE, {"force": force})
        if loaded.get("panel_cached"):
            return pd.read_parquet(CACHE)
        return pd.read_parquet(CACHE)
    if CACHE.exists():
        return pd.read_parquet(CACHE)
    raise RuntimeError("coupled_build_panel: no cached panel and no explicit outcome_loader; refused outside guarded contract")


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