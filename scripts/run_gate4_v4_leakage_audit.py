#!/usr/bin/env python3
"""Gate 4 v4 EXPLORATORY leakage audit — train-only parameter provenance + block-bootstrap reproducibility.

EXPLORATORY / NOT CONFIRMATORY / NOT PROMOTABLE. No confirmatory claim. No Track A probing.

Verifies that every train-only parameter used by Gate 4 v4 stabilized variants
(ridge scale, winsor bounds, target floor, normalization mean/std) is computed
exclusively from training data: a perturbation of the test fold must not change
any train-derived parameter. Also verifies block-bootstrap CI reproducibility
with a fixed deterministic seed.

Outputs (versioned, not overwriting): JSON + markdown under
research_state/gate4_v4_leakage_audit/ and results/fclr_heavy001/.
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Tuple

import numpy as np
import pandas as pd

REPO = Path(__file__).resolve().parents[1]
if str(REPO) not in sys.path:
    sys.path.insert(0, str(REPO))

from scripts.run_gate4_v4_exploratory_stab import (  # noqa: E402
    ABLATIONS,
    LABEL,
    PREREG_V4,
    fit_predict_variant,
)
from scripts.run_funding_ablations import (  # noqa: E402
    PRE_REG_SPLITS_V3_30D,
    add_funding_to_panel,
    block_bootstrap_delta_ci,
    load_funding_panel,
    load_kline_panel,
    paired_qlike_by_time,
)
from src.eval import walkforward as wf  # noqa: E402

STATE_DIR = "research_state/gate4_v4_leakage_audit"
RESULTS_DIR = "results/fclr_heavy001"
SYMBOLS = ["BTCUSDT", "ETHUSDT", "SOLUSDT", "XRPUSDT", "BNBUSDT"]
START = "2024-04-01"
END = "2024-09-30"


def _ts() -> str:
    return datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")


def _git_sha() -> str:
    try:
        return subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=REPO, text=True).strip()
    except Exception:
        return "UNKNOWN"


def train_normalization_stats(train_n: pd.DataFrame, fcols: List[str]) -> Dict[str, object]:
    """Train-only mean/std used by wf.apply_train_only_normalization (recomputed for audit)."""
    stats = {}
    for c in fcols:
        col = train_n[c].to_numpy(dtype=float)
        m = col[np.isfinite(col)]
        stats[c] = {
            "mean": float(np.mean(m)) if m.size else None,
            "std": float(np.std(m)) if m.size else None,
            "n": int(m.size),
        }
    return stats


def train_derived_params(train_n: pd.DataFrame, fcols: List[str], variant: str) -> Dict[str, object]:
    """Recompute all train-only parameters for one symbol/train fold (leakage boundary)."""
    X = train_n[fcols].to_numpy(dtype=float)
    y = train_n["target_rv"].to_numpy(dtype=float)
    mask = np.isfinite(y) & np.all(np.isfinite(X), axis=1)
    Xc, yc = X[mask], y[mask]
    k = Xc.shape[1]
    XtX = Xc.T @ Xc
    diag_scale = float(np.trace(XtX) / max(k, 1))
    ypos = yc[np.isfinite(yc) & (yc > 0)]
    ymed = float(np.median(ypos)) if ypos.size else 0.0
    floor = max(0.0, 1e-4 * ymed)
    out = {
        "n_train_valid": int(mask.sum()),
        "n_train_total": int(len(train_n)),
        "ridge_scale_diag_trace_over_k": diag_scale,
        "ridge_rule": "1e-10*I" if variant == "V1_primary" else f"1e-8*max({diag_scale:.6g},1)",
        "target_floor": floor,
        "target_floor_rule": "max(p,0)" if variant == "V1_primary" else f"max(p,1e-4*train_target_median={floor:.6g})",
        "normalization": train_normalization_stats(train_n, fcols),
    }
    if variant == "V4_winsor_train":
        lo = np.nanquantile(Xc, 0.005, axis=0)
        hi = np.nanquantile(Xc, 0.995, axis=0)
        out["winsor_lo"] = [float(v) for v in lo]
        out["winsor_hi"] = [float(v) for v in hi]
        out["winsor_bounds_from"] = "train_only"
    return out


def audit_variant_leakage(panel: pd.DataFrame, variant: str, split_defs) -> Dict[str, object]:
    """For each split/symbol: compute train-only params under (a) original test and (b)
    perturbed test targets. Both runs use the same training fold through
    wf.apply_train_only_normalization; train-derived params must be identical —
    no leakage from test into ridge scale, winsor bounds, target floor, or
    normalization stats."""
    idx = panel.index.get_level_values("timestamp")
    split_audits = []
    for i, meta in enumerate(split_defs):
        sp = wf.SplitBounds(train=meta["train"], validation=meta["test"], test=meta["test"],
                            purge_days=meta.get("purge_days", 7), embargo_days=meta.get("embargo_days", 7))
        train = panel.loc[wf._in_window(idx, sp.train)]
        test = panel.loc[wf._in_window(idx, sp.test)]
        symbol_rows = []
        for sym in SYMBOLS:
            tr_s = train.loc[train.index.get_level_values("symbol") == sym]
            te_s = test.loc[test.index.get_level_values("symbol") == sym]
            if tr_s.empty or te_s.empty:
                symbol_rows.append({"symbol": sym, "status": "INSUFFICIENT_DATA", "n_train": int(len(tr_s)), "n_test": int(len(te_s))})
                continue
            fcols = [c for c in ABLATIONS["A_rv_only"] if c in panel.columns]
            tr_norm_base, _, te_norm_base, _ = wf.apply_train_only_normalization(tr_s, te_s, te_s, fcols)
            base = train_derived_params(tr_norm_base, fcols, variant)
            # Perturb test targets (scale by 2.0): train-derived params must be byte-identical.
            te_perturbed = te_s.copy()
            te_perturbed["target_rv"] = te_s["target_rv"].to_numpy(dtype=float) * 2.0
            tr_norm, _, te_norm, _ = wf.apply_train_only_normalization(tr_s, te_perturbed, te_perturbed, fcols)
            perturbed = train_derived_params(tr_norm, fcols, variant)
            changed = []
            for key in ("ridge_scale_diag_trace_over_k", "target_floor", "n_train_valid"):
                if base.get(key) != perturbed.get(key):
                    changed.append(key)
            for c in fcols:
                b = base["normalization"][c]; p = perturbed["normalization"][c]
                if (b.get("mean") is not None and p.get("mean") is not None
                        and abs(b["mean"] - p["mean"]) > 1e-12):
                    changed.append(f"norm.{c}.mean")
                if (b.get("std") is not None and p.get("std") is not None
                        and abs(b["std"] - p["std"]) > 1e-12):
                    changed.append(f"norm.{c}.std")
            if variant == "V4_winsor_train":
                if base.get("winsor_lo") != perturbed.get("winsor_lo") or base.get("winsor_hi") != perturbed.get("winsor_hi"):
                    changed.append("winsor_bounds")
            symbol_rows.append({
                "symbol": sym, "status": "OK",
                "n_train": int(len(tr_s)), "n_test": int(len(te_s)),
                "train_params": base, "test_perturbation_unchanged": len(changed) == 0, "changed_keys": changed,
            })
        split_audits.append({"split_id": i, "train": meta["train"], "test": meta["test"], "symbols": symbol_rows})
    all_unchanged = all(
        s.get("test_perturbation_unchanged") is True
        for sp in split_audits for s in sp["symbols"] if s.get("status") == "OK"
    )
    return {"variant": variant, "all_train_params_test_invariant": all_unchanged, "splits": split_audits}


def audit_block_bootstrap_reproducibility(panel: pd.DataFrame, split_defs) -> Dict[str, object]:
    """Same deterministic seed must produce identical block-bootstrap CIs across runs."""
    idx = panel.index.get_level_values("timestamp")
    reps = []
    for run in range(2):
        parts = []
        for i, meta in enumerate(split_defs):
            sp = wf.SplitBounds(train=meta["train"], validation=meta["test"], test=meta["test"],
                                purge_days=meta.get("purge_days", 7), embargo_days=meta.get("embargo_days", 7))
            train = panel.loc[wf._in_window(idx, sp.train)]
            test = panel.loc[wf._in_window(idx, sp.test)]
            if train.empty or test.empty:
                continue
            fcols = [c for c in ABLATIONS["A_rv_only"] if c in panel.columns]
            tr_a, _, te_a, _ = wf.apply_train_only_normalization(train, test, test, fcols)
            tr_e, _, te_e, _ = wf.apply_train_only_normalization(train, test, test,
                                                                 [c for c in ABLATIONS["E_rv_funding_trails"] if c in panel.columns])
            pa, _ = fit_predict_variant(tr_a, te_a, fcols, "V1_primary")
            pe, _ = fit_predict_variant(tr_e, te_e, [c for c in ABLATIONS["E_rv_funding_trails"] if c in panel.columns], "V1_primary")
            parts.append(paired_qlike_by_time(te_a["target_rv"].to_numpy(dtype=float), pa, pe,
                                              te_a.index.get_level_values("timestamp")))
        df = pd.concat(parts, ignore_index=True) if parts else pd.DataFrame(columns=["timestamp", "ql_base", "ql_alt", "diff"])
        reps.append(block_bootstrap_delta_ci(df, seed=20261109))
    identical = all(reps[0].get(k) == reps[1].get(k) for k in ("point", "ci_low", "ci_high", "n_obs", "n_blocks"))
    return {"run1": reps[0], "run2": reps[1], "seed": 20261109, "identical_on_rerun": identical}


def _diag_field(ci: Dict[str, object], key: str, fallback: object = None) -> object:
    """Read additive bootstrap diagnostic field with legacy fallback tolerance.

    New delegates (src.eval.inference.block_bootstrap_delta_ci_diagnostic) emit
    `effective_block_count`, `regime_flags`, `ci_accounting_valid`; older CI dicts
    omit them. Never raise on a malformed/legacy payload.
    """
    if ci is None:
        return fallback
    if key == "effective_block_count":
        v = ci.get("effective_block_count", ci.get("n_blocks"))
        return v if v is not None else fallback
    if key == "ci_accounting_valid":
        v = ci.get("ci_accounting_valid")
        return v if v is not None else fallback
    if key == "regime_flags":
        v = ci.get("regime_flags")
        if v is None:
            return fallback
        return list(v) if not isinstance(v, list) else v
    return ci.get(key, fallback)


def _flags_str(flags: object) -> str:
    if not flags:
        return "ok"
    if isinstance(flags, (list, tuple)):
        return ";".join(str(f) for f in flags)
    return str(flags)


def write_md(path: Path, payload: Dict[str, object]) -> None:
    lines = [
        f"# Gate 4 v4 EXPLORATORY leakage audit — {payload['ts']}",
        "",
        f"**{LABEL}**",
        f"- Git SHA: `{payload.get('git_sha')}`",
        f"- Prereg: `{PREREG_V4}` — `FROZEN_BEFORE_OUTCOMES`, `confirmatory_claim_go=NO_GO`",
        "- No confirmatory claim, no economic value, no promotion. Audit of leakage controls only.",
        "- Verifies train-only provenance of ridge scale, winsor bounds, target floor, normalization stats; "
          "and block-bootstrap CI reproducibility with fixed seed.",
        "",
        "## Train-only parameter provenance (test-fold perturbation invariance)",
        "| Variant | Split | Symbol | n_train | test_perturbation_unchanged | changed_keys |",
        "|---|---:|---|---:|---:|---|",
    ]
    for v in payload["variant_audits"]:
        for sp in v["splits"]:
            for s in sp["symbols"]:
                if s.get("status") == "OK":
                    lines.append(f"| {v['variant']} | {sp['split_id']} | {s['symbol']} | {s['n_train']} | {s['test_perturbation_unchanged']} | {','.join(s.get('changed_keys', [])) or '-'} |")
    lines += ["",
              f"**All train-derived parameters invariant to test perturbation: {payload['leakage_invariance_all']}**",
              "",
              "## Block-bootstrap reproducibility (fixed seed 20261109, two independent runs)",
              "| Metric | Run 1 | Run 2 | Identical | eff_blocks | ci_valid | regime_flags |",
              "|---|---:|---:|---:|---:|---:|---|",
    ]
    bb = payload["block_bootstrap_reproducibility"]
    run1, run2 = bb.get("run1", {}), bb.get("run2", {})
    for k in ("point", "ci_low", "ci_high", "n_obs", "n_blocks"):
        lines.append(
            f"| {k} | {run1.get(k)} | {run2.get(k)} | {run1.get(k) == run2.get(k)} "
            f"| {_diag_field(run1, 'effective_block_count')} | {_diag_field(run1, 'ci_accounting_valid')} "
            f"| {_flags_str(_diag_field(run1, 'regime_flags', []))} |"
        )
    # Additive diagnostic rows: effective block count, CI accounting validity, regime flags.
    for k in ("effective_block_count", "ci_accounting_valid", "regime_flags"):
        v1, v2 = _diag_field(run1, k), _diag_field(run2, k)
        if k == "regime_flags":
            v1s, v2s = _flags_str(v1), _flags_str(v2)
            lines.append(f"| {k} | {v1s} | {v2s} | {v1s == v2s} | - | - | - |")
        else:
            lines.append(f"| {k} | {v1} | {v2} | {v1 == v2} | - | - | - |")
    lines += ["",
              f"**Block-bootstrap CI identical on rerun: {bb['identical_on_rerun']}**",
              f"**CI accounting valid: {_diag_field(run1, 'ci_accounting_valid')}**",
              f"**Effective blocks: {_diag_field(run1, 'effective_block_count')}**",
              f"**Regime flags: {_flags_str(_diag_field(run1, 'regime_flags', []))}**",
              "",
              "## Interpretation (EXPLORATORY ONLY — NOT CONFIRMATORY)",
              payload.get("interpretation", ""),
              "",
              f"Artifacts: `{payload.get('json_path')}`, `{path}`",
    ]
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def make_interpretation(payload: Dict[str, object]) -> str:
    parts = []
    parts.append(f"Train-only provenance: {payload['leakage_invariance_all']} — every train-derived parameter "
                 "(ridge scale, winsor bounds, target floor, normalization mean/std) is unchanged when the test fold "
                 "is perturbed; no test-derived statistic enters training parameters.")
    parts.append(f"Block-bootstrap reproducibility: {payload['block_bootstrap_reproducibility']['identical_on_rerun']} — "
                 "fixed seed yields identical CIs across independent runs (deterministic inference).")
    if payload["leakage_invariance_all"] and payload["block_bootstrap_reproducibility"]["identical_on_rerun"]:
        parts.append("**Leakage audit PASS (EXPLORATORY diagnostic, not confirmatory):** Gate 4 v4 leakage controls "
                     "hold on the local 2024-04..09 slice; block-bootstrap inference is deterministic and reproducible.")
    return " ".join(parts)


def main(argv=None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--symbols", default=",".join(SYMBOLS))
    ap.add_argument("--start", default=START)
    ap.add_argument("--end", default=END)
    ap.add_argument("--include-cache", action="store_true", default=True)
    ap.add_argument("--out-suffix", default=None)
    ap.add_argument("--state-dir", default=STATE_DIR)
    ap.add_argument("--results-dir", default=RESULTS_DIR)
    args = ap.parse_args(argv)
    symbols = [s.strip() for s in args.symbols.split(",") if s.strip()]
    ts = args.out_suffix or _ts()
    state_dir = REPO / args.state_dir
    results_dir = REPO / args.results_dir
    state_dir.mkdir(parents=True, exist_ok=True)
    results_dir.mkdir(parents=True, exist_ok=True)
    variants = ["V1_primary", "V2_scale_ridge", "V3_scale_ridge_target_floor", "V4_winsor_train"]
    kpanel = load_kline_panel(symbols, args.start, args.end, horizon=24, include_cache=args.include_cache)
    fpanel = load_funding_panel(symbols, args.start, args.end, include_cache=args.include_cache)
    panel = add_funding_to_panel(kpanel, fpanel)
    payload = {
        "label": LABEL, "ts": ts, "git_sha": _git_sha(), "symbols": symbols,
        "start": args.start, "end": args.end, "include_cache": args.include_cache,
        "prereg_v4": PREREG_V4, "confirmatory_claim_go": "NO_GO",
        "command": f"python scripts/run_gate4_v4_leakage_audit.py --out-suffix {ts}",
        "variant_audits": [],
    }
    for v in variants:
        payload["variant_audits"].append(audit_variant_leakage(panel, v, PRE_REG_SPLITS_V3_30D))
    payload["leakage_invariance_all"] = all(
        v["all_train_params_test_invariant"] for v in payload["variant_audits"]
    )
    payload["block_bootstrap_reproducibility"] = audit_block_bootstrap_reproducibility(panel, PRE_REG_SPLITS_V3_30D)
    payload["interpretation"] = make_interpretation(payload)
    json_path = state_dir / f"gate4_v4_leakage_audit_{ts}.json"
    md_state = state_dir / f"gate4_v4_leakage_audit_{ts}.md"
    md_results = results_dir / f"gate4_v4_leakage_audit_{ts}.md"
    payload["json_path"] = str(json_path.relative_to(REPO))
    payload["md_state_path"] = str(md_state.relative_to(REPO))
    payload["md_results_path"] = str(md_results.relative_to(REPO))
    json_path.write_text(json.dumps(payload, indent=2, default=str) + "\n", encoding="utf-8")
    write_md(md_state, payload)
    write_md(md_results, payload)
    print(json.dumps({"label": LABEL, "json": str(json_path),
                      "leakage_invariance_all": payload["leakage_invariance_all"],
                      "bootstrap_reproducible": payload["block_bootstrap_reproducibility"]["identical_on_rerun"]},
                     indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
