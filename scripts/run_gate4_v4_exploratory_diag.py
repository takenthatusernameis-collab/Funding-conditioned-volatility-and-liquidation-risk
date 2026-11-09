#!/usr/bin/env python3
"""Gate 4 v4 EXPLORATORY diagnostic/robustness for 20261109T004003Z exec.

EXPLORATORY / NOT CONFIRMATORY / NOT PROMOTABLE. Sealed-anchor conflict applies
(v4 prereg confirmatory_claim_go=NO_GO). Uses local 2024-04..09 cache only.
Does NOT modify prereg A-E contrast definitions or replace the frozen exec.

Outputs (versioned): JSON diagnostics, per-split/instrument tables, LOO for E vs A,
coefficient/prediction/bounds diagnostics explaining B/D split-3 instability.
"""
from __future__ import annotations

import argparse
import json
import math
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Optional, Tuple

import numpy as np
import pandas as pd

REPO = Path(__file__).resolve().parents[1]
if str(REPO) not in sys.path:
    sys.path.insert(0, str(REPO))

from scripts.run_funding_ablations import (  # noqa: E402
    PRE_REG_SPLITS_V3_30D,
    add_funding_to_panel,
    block_bootstrap_delta_ci,
    fit_predict_ols,
    load_funding_panel,
    load_kline_panel,
    metrics,
    paired_qlike_by_time,
)
from src.eval import walkforward as wf  # noqa: E402


def _ts() -> str:
    return datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")


def fit_predict_ols_with_coef(train_n: pd.DataFrame, test_n: pd.DataFrame, fcols: List[str], ridge: float = 1e-10):
    """Return (preds, per_symbol_diag). EXPLORATORY diagnostic fit; mirrors fit_predict_ols."""
    preds = np.full(len(test_n), np.nan)
    diags = []
    for sym, grp in test_n.groupby(level="symbol", sort=False):
        tr = train_n.loc[train_n.index.get_level_values("symbol") == sym]
        ytr = tr["target_rv"].to_numpy(dtype=float)
        Xtr = tr[fcols].to_numpy(dtype=float)
        mask = np.isfinite(ytr) & np.all(np.isfinite(Xtr), axis=1)
        Xc, yc = Xtr[mask], ytr[mask]
        if len(yc) < 2:
            diags.append({"symbol": sym, "status": "INSUFFICIENT_TRAIN", "n_train_valid": int(mask.sum())})
            continue
        k = Xc.shape[1]
        XtX = Xc.T @ Xc
        try:
            coef = np.linalg.solve(XtX + ridge * np.eye(k), Xc.T @ yc)
        except np.linalg.LinAlgError:
            diags.append({"symbol": sym, "status": "LINALG_FAIL", "n_train_valid": int(mask.sum())})
            continue
        intercept = float(yc.mean() - coef @ Xc.mean(axis=0))
        Xte = grp[fcols].to_numpy(dtype=float)
        raw = intercept + Xte @ coef
        raw_ok = raw[np.isfinite(raw)]
        p = raw.copy()
        p[~np.isfinite(p)] = np.nan
        p_floored = np.maximum(p, 0.0)
        preds[test_n.index.get_indexer(grp.index)] = p_floored
        yte = grp["target_rv"].to_numpy(dtype=float)
        m = metrics(yte, p_floored)
        # QLIKE contributions (valid only) for per-instrument delta
        ql_mask = np.isfinite(yte) & np.isfinite(p_floored) & (yte > 0) & (p_floored > 0)
        ql_contrib = None
        if ql_mask.any():
            r = yte[ql_mask] / p_floored[ql_mask]
            ql_contrib = (r - np.log(r) - 1.0).tolist()
        diags.append({
            "symbol": sym,
            "status": "OK",
            "n_train_valid": int(mask.sum()),
            "n_test": int(len(grp)),
            "coef": {c: float(v) for c, v in zip(fcols, coef)},
            "intercept": intercept,
            "coef_l2": float(np.linalg.norm(coef)),
            "coef_max_abs": float(np.max(np.abs(coef))) if len(coef) else 0.0,
            "raw_pred": {
                "min": float(np.nanmin(raw_ok)) if raw_ok.size else None,
                "p01": float(np.nanquantile(raw_ok, 0.01)) if raw_ok.size else None,
                "p05": float(np.nanquantile(raw_ok, 0.05)) if raw_ok.size else None,
                "median": float(np.nanmedian(raw_ok)) if raw_ok.size else None,
                "max": float(np.nanmax(raw_ok)) if raw_ok.size else None,
                "n_neg_raw": int(np.sum(raw_ok < 0)) if raw_ok.size else 0,
                "n_finite": int(raw_ok.size),
            },
            "floored_pred": {
                "min": float(np.nanmin(p_floored[np.isfinite(p_floored)])) if np.isfinite(p_floored).any() else None,
                "n_zero_or_neg_floored": int(np.sum(np.isfinite(p_floored) & (p_floored <= 0))),
                "n_near_zero_lt_1e6": int(np.sum(np.isfinite(p_floored) & (p_floored > 0) & (p_floored < 1e-6))),
            },
            "metrics": m,
            "qlike_contrib_mean": float(np.mean(ql_contrib)) if ql_contrib else None,
            "qlike_contrib_n": len(ql_contrib) if ql_contrib else 0,
        })
    return preds, diags


def stabilized_predict(train_n: pd.DataFrame, test_n: pd.DataFrame, fcols: List[str], ridge_mult: float = 1000.0, pred_floor: float = 1e-8):
    """EXPLORATORY stabilized variant (comparison only; does NOT replace prereg A-E).
    Stronger ridge + small positive floor to avoid p<=0 QLIKE exclusion/extreme ratios.
    NOT CONFIRMATORY / NOT PROMOTABLE.
    """
    # compute base ridge scale from train covariance diag for comparability
    preds = np.full(len(test_n), np.nan)
    for sym, grp in test_n.groupby(level="symbol", sort=False):
        tr = train_n.loc[train_n.index.get_level_values("symbol") == sym]
        ytr = tr["target_rv"].to_numpy(dtype=float)
        Xtr = tr[fcols].to_numpy(dtype=float)
        mask = np.isfinite(ytr) & np.all(np.isfinite(Xtr), axis=1)
        Xc, yc = Xtr[mask], ytr[mask]
        if len(yc) < 2:
            continue
        k = Xc.shape[1]
        XtX = Xc.T @ Xc
        diag_scale = float(np.trace(XtX) / max(k, 1)) if k else 1.0
        ridge = (1e-10 * ridge_mult) * max(diag_scale, 1e-12)
        try:
            coef = np.linalg.solve(XtX + ridge * np.eye(k), Xc.T @ yc)
        except np.linalg.LinAlgError:
            continue
        intercept = float(yc.mean() - coef @ Xc.mean(axis=0))
        Xte = grp[fcols].to_numpy(dtype=float)
        p = intercept + Xte @ coef
        p[~np.isfinite(p)] = np.nan
        p = np.maximum(p, pred_floor)
        preds[test_n.index.get_indexer(grp.index)] = p
    return preds


def run_diag(panel: pd.DataFrame, ablations: Dict[str, List[str]], split_defs, symbols: List[str]):
    idx = panel.index.get_level_values("timestamp")
    split_results = []
    per_inst_delta = {k: [] for k in ablations if k != "A_rv_only"}
    pooled_paired = {k: [] for k in ablations if k != "A_rv_only"}
    pooled_stab = {k: [] for k in ablations if k != "A_rv_only"}
    for i, meta in enumerate(split_defs):
        sp = wf.SplitBounds(train=meta["train"], validation=meta["test"], test=meta["test"], purge_days=meta.get("purge_days", 7), embargo_days=meta.get("embargo_days", 7))
        train = panel.loc[wf._in_window(idx, sp.train)]
        test = panel.loc[wf._in_window(idx, sp.test)]
        row = {"split_id": i, "train": meta["train"], "test": meta["test"], "n_train": int(len(train)), "n_test": int(len(test)), "ablations": {}}
        preds_map = {}
        y_test = ts_test = None
        for ab_name, fcols in ablations.items():
            fcols = [c for c in fcols if c in panel.columns]
            try:
                train_n, _, test_n, _ = wf.apply_train_only_normalization(train, test, test, fcols)
                p, diags = fit_predict_ols_with_coef(train_n, test_n, fcols)
                y = test_n["target_rv"].to_numpy(dtype=float)
                m = metrics(y, p)
                row["ablations"][ab_name] = {"metrics": m, "n_features": len(fcols), "per_symbol": diags}
                preds_map[ab_name] = (p, test_n)
                y_test = y
                ts_test = test_n.index.get_level_values("timestamp")
                # per-instrument delta vs A computed later
            except Exception as e:
                row["ablations"][ab_name] = {"err": str(e)}
        # paired/per-instrument
        if y_test is not None and "A_rv_only" in preds_map:
            p_a, tn_a = preds_map["A_rv_only"]
            for ab_name in [k for k in ablations if k != "A_rv_only"]:
                if ab_name in preds_map:
                    p_b, tn_b = preds_map[ab_name]
                    dfp = paired_qlike_by_time(y_test, p_a, p_b, ts_test)
                    pooled_paired[ab_name].append(dfp)
                    # instrument LOO components: per-symbol contributions from diagnostic path
                    inst = {}
                    for d in row["ablations"][ab_name].get("per_symbol", []):
                        da = next((x for x in row["ablations"]["A_rv_only"].get("per_symbol", []) if x.get("symbol") == d.get("symbol")), None)
                        if da and d.get("qlike_contrib_mean") is not None and da.get("qlike_contrib_mean") is not None:
                            inst[d["symbol"]] = {"delta_qlike_mean": d["qlike_contrib_mean"] - da["qlike_contrib_mean"], "n": min(d.get("qlike_contrib_n", 0), da.get("qlike_contrib_n", 0)), "status": d.get("status"), "coef_max_abs": d.get("coef_max_abs"), "raw_neg": d.get("raw_pred", {}).get("n_neg_raw"), "raw_n": d.get("raw_pred", {}).get("n_finite")}
                    per_inst_delta[ab_name].append({"split_id": i, "per_instrument": inst})
                    # stabilized comparison (EXPLORATORY only)
                    fcols = [c for c in ablations[ab_name] if c in panel.columns]
                    train_n, _, test_n, _ = wf.apply_train_only_normalization(train, test, test, fcols)
                    p_stab = stabilized_predict(train_n, test_n, fcols)
                    pooled_stab[ab_name].append(paired_qlike_by_time(y_test, p_a, p_stab, ts_test))
                else:
                    pooled_paired[ab_name].append(pd.DataFrame(columns=["timestamp", "ql_base", "ql_alt", "diff"]))
                    pooled_stab[ab_name].append(pd.DataFrame(columns=["timestamp", "ql_base", "ql_alt", "diff"]))
        split_results.append(row)
    # aggregate CIs
    def agg_ci(pool):
        out = {}
        for k, parts in pool.items():
            df = pd.concat(parts, ignore_index=True) if parts else pd.DataFrame(columns=["timestamp", "ql_base", "ql_alt", "diff"])
            out[k] = block_bootstrap_delta_ci(df)
        return out
    # instrument LOO for E vs A (drop one instrument from pooled paired observations via split symbol diags approximation: recompute from per-split paired by joining? simpler: build per-instrument paired in diag pass)
    # Better: compute LOO by excluding symbol in a second pass
    loo = compute_loo(panel, ablations, split_defs, symbols)
    return {
        "label": "EXPLORATORY / NOT CONFIRMATORY / NOT PROMOTABLE",
        "split_results": split_results,
        "per_instrument_delta_vs_A": per_inst_delta,
        "pooled_contrasts_vs_A_primary_fit": agg_ci(pooled_paired),
        "pooled_contrasts_vs_A_stabilized_exploratory": agg_ci(pooled_stab),
        "stabilized_variant_note": "EXPLORATORY comparison only (stronger ridge + pred_floor=1e-8); does NOT replace prereg A-E contrasts or change confirmatory estimands.",
        "instrument_loo_E_vs_A_exploratory": loo,
    }


def compute_loo(panel: pd.DataFrame, ablations: Dict[str, List[str]], split_defs, symbols: List[str]):
    """Instrument leave-one-out for E vs A only (prereg-scoped exploratory robustness)."""
    idx = panel.index.get_level_values("timestamp")
    results = {}
    keep_sets = [("all", symbols)] + [(f"drop_{s}", [x for x in symbols if x != s]) for s in symbols]
    e_cols = [c for c in ablations["E_rv_funding_trails"] if c in panel.columns]
    a_cols = [c for c in ablations["A_rv_only"] if c in panel.columns]
    for name, keep in keep_sets:
        pooled = []
        for i, meta in enumerate(split_defs):
            sp = wf.SplitBounds(train=meta["train"], validation=meta["test"], test=meta["test"], purge_days=meta.get("purge_days", 7), embargo_days=meta.get("embargo_days", 7))
            train = panel.loc[wf._in_window(idx, sp.train)]
            test = panel.loc[wf._in_window(idx, sp.test)]
            # filter instruments
            train = train.loc[train.index.get_level_values("symbol").isin(keep)]
            test = test.loc[test.index.get_level_values("symbol").isin(keep)]
            if train.empty or test.empty:
                continue
            tr_a, _, te_a, _ = wf.apply_train_only_normalization(train, test, test, a_cols)
            tr_e, _, te_e, _ = wf.apply_train_only_normalization(train, test, test, e_cols)
            pa = fit_predict_ols(tr_a, te_a, a_cols)
            pe = fit_predict_ols(tr_e, te_e, e_cols)
            y = te_a["target_rv"].to_numpy(dtype=float)
            ts = te_a.index.get_level_values("timestamp")
            pooled.append(paired_qlike_by_time(y, pa, pe, ts))
        df = pd.concat(pooled, ignore_index=True) if pooled else pd.DataFrame(columns=["timestamp", "ql_base", "ql_alt", "diff"])
        results[name] = block_bootstrap_delta_ci(df)
        results[name]["instruments"] = keep
    return results


def alignment_checks() -> Dict[str, object]:
    # deterministic, no data needed beyond code-level evidence capture
    return {
        "train_only_normalization": "wf.apply_train_only_normalization used per split before fit (scripts/run_funding_ablations.py run_multisplit); scaler fit on train only.",
        "funding_last_known_alignment": "src.features.funding.resample_funding_to_hourly uses reindex(method='ffill') on sorted funding aligned to kline index => last known at/before hour; no backward fill.",
        "trailing_stats_past_only": "ff.trailing_funding_pct/zscore use rolling/past windows over already-aligned series; no future leakage by construction.",
        "prediction_floor_primary": "fit_predict_ols floors predictions at 0.0 after OLS; paired QLIKE masks require p>0 and y>0 so floored-to-zero are excluded but near-zero positives can inflate QLIKE (y/p).",
        "e_vs_a_note": "E adds funding_signed, funding_abs, funding_pct_*, funding_z_*; LOO and stabilized comparison reported as EXPLORATORY only.",
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--symbols", default="BTCUSDT,ETHUSDT,SOLUSDT,XRPUSDT,BNBUSDT")
    ap.add_argument("--start", default="2024-04-01")
    ap.add_argument("--end", default="2024-09-30")
    ap.add_argument("--include-cache", action="store_true", default=True)
    ap.add_argument("--out-dir", default="research_state/gate4_v4_exploratory_diag")
    ap.add_argument("--out-suffix", default=None)
    ap.add_argument("--git-sha", default=None)
    args = ap.parse_args()
    symbols = [s.strip() for s in args.symbols.split(",") if s.strip()]
    ts = args.out_suffix or _ts()
    out_dir = REPO / args.out_dir
    out_dir.mkdir(parents=True, exist_ok=True)
    ablations = {
        "A_rv_only": ["rv_trail_24", "rv_trail_168", "rv_trail_6"],
        "B_rv_signed": ["rv_trail_24", "rv_trail_168", "rv_trail_6", "funding_signed"],
        "C_rv_abs": ["rv_trail_24", "rv_trail_168", "rv_trail_6", "funding_abs"],
        "D_rv_signed_abs": ["rv_trail_24", "rv_trail_168", "rv_trail_6", "funding_signed", "funding_abs"],
        "E_rv_funding_trails": ["rv_trail_24", "rv_trail_168", "rv_trail_6", "funding_signed", "funding_abs", "funding_pct_24", "funding_pct_72", "funding_pct_168", "funding_z_24", "funding_z_72", "funding_z_168"],
    }
    kpanel = load_kline_panel(symbols, args.start, args.end, horizon=24, include_cache=args.include_cache)
    fpanel = load_funding_panel(symbols, args.start, args.end, include_cache=args.include_cache)
    panel = add_funding_to_panel(kpanel, fpanel)
    diag = run_diag(panel, ablations, PRE_REG_SPLITS_V3_30D, symbols)
    diag["meta"] = {
        "ts": ts,
        "symbols": symbols,
        "start": args.start,
        "end": args.end,
        "include_cache": args.include_cache,
        "git_sha": args.git_sha,
        "prereg_v4": "research_state/pre_registration_gate4_funding_multisplit_v4_20261107T1845Z.json",
        "prior_exec": "research_state/gate4_v4_exploratory_exec/run_manifest_funding_v4_exploratory_exec_20261109T004003Z.json",
        "confirmatory_claim_go": "NO_GO",
    }
    diag["alignment_checks"] = alignment_checks()
    out = out_dir / f"gate4_v4_exploratory_diag_{ts}.json"
    out.write_text(json.dumps(diag, indent=2, default=str) + "\n", encoding="utf-8")
    print(f"WROTE {out}")
    # concise stdout
    e = diag["pooled_contrasts_vs_A_primary_fit"].get("E_rv_funding_trails", {})
    print(f"E_vs_A primary point={e.get('point')} ci=[{e.get('ci_low')},{e.get('ci_high')}] n={e.get('n_obs')}")
    loo = diag["instrument_loo_E_vs_A_exploratory"]
    print("LOO E_vs_A:", {k: v.get("point") for k, v in loo.items()})
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
