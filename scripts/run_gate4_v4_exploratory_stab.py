#!/usr/bin/env python3
"""Gate 4 v4 EXPLORATORY stabilized comparison (2024-04..09, local cache).

EXPLORATORY / NOT CONFIRMATORY / NOT PROMOTABLE. Sealed-anchor conflict applies
(v4 prereg confirmatory_claim_go=NO_GO). exploratory_smoke_authorized_after_freeze=true.

This script evaluates PRINCIPLED, leakage-safe EXPLORATORY modeling variants to
diagnose B/D split-3 instability and E sensitivity observed in
gate4_v4_exploratory_exec_20261109T004003Z/diag_20261109T021456Z. It does NOT
replace prereg A-E contrasts, does NOT change confirmatory estimands, and MUST
NOT be used to claim confirmatory GO, economic value, or promotion.

Variants (all EXPLORATORY, fixed deterministic rules):
- V1_primary: direct-variance OLS, ridge=1e-10*I, floor-at-zero after predict,
  QLIKE masks p<=0 (matches run_funding_ablations.fit_predict_ols).
- V2_scale_ridge: ridge = 1e-8 * max(trace(X'X)/k, 1.0) * I (scale-aware),
  floor-at-zero; QLIKE masks p<=0.
- V3_scale_ridge_target_floor: V2 ridge + train-only target-scale floor
  floor=max(0, 1e-4 * median(train_target_rv where >0)) applied to predictions;
  floor is computed from TRAIN only per instrument/split. QLIKE still requires p>0.
- V4_winsor_train: V3 + train-only winsorization of standardized feature matrix
  at [q0.5,q99.5] bounds learned from TRAIN standardized features only; bounds
  applied to train and test (leakage-safe transform using train bounds).

Outputs (versioned, not overwriting exec/diag): JSON + markdown under
research_state/gate4_v4_exploratory_stab/ and results/fclr_heavy001/.
"""
from __future__ import annotations

import argparse
import json
import subprocess
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
    fit_predict_ols as fit_predict_ols_primary,
    load_funding_panel,
    load_kline_panel,
    metrics,
    paired_qlike_by_time,
)
from src.eval import walkforward as wf  # noqa: E402

LABEL = "EXPLORATORY / NOT CONFIRMATORY / NOT PROMOTABLE"
PREREG_V4 = "research_state/pre_registration_gate4_funding_multisplit_v4_20261107T1845Z.json"
ABLATIONS = {
    "A_rv_only": ["rv_trail_24", "rv_trail_168", "rv_trail_6"],
    "B_rv_signed": ["rv_trail_24", "rv_trail_168", "rv_trail_6", "funding_signed"],
    "C_rv_abs": ["rv_trail_24", "rv_trail_168", "rv_trail_6", "funding_abs"],
    "D_rv_signed_abs": ["rv_trail_24", "rv_trail_168", "rv_trail_6", "funding_signed", "funding_abs"],
    "E_rv_funding_trails": ["rv_trail_24", "rv_trail_168", "rv_trail_6", "funding_signed", "funding_abs", "funding_pct_24", "funding_pct_72", "funding_pct_168", "funding_z_24", "funding_z_72", "funding_z_168"],
}


def _ts() -> str:
    return datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")


def _git_sha() -> str:
    try:
        return subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=REPO, text=True).strip()
    except Exception:
        return "UNKNOWN"


def train_only_winsor(Xtr: np.ndarray, Xte: np.ndarray, lo_q: float = 0.005, hi_q: float = 0.995) -> Tuple[np.ndarray, np.ndarray, Dict[str, object]]:
    """Leakage-safe: bounds from train standardized features only."""
    lo = np.nanquantile(Xtr, lo_q, axis=0)
    hi = np.nanquantile(Xtr, hi_q, axis=0)
    return np.clip(Xtr, lo, hi), np.clip(Xte, lo, hi), {"lo_q": lo_q, "hi_q": hi_q, "bounds_from": "train_only"}


def fit_predict_variant(train_n: pd.DataFrame, test_n: pd.DataFrame, fcols: List[str], variant: str) -> Tuple[np.ndarray, List[Dict[str, object]]]:
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
        Xte = grp[fcols].to_numpy(dtype=float)
        if variant == "V4_winsor_train":
            Xc_fit, Xte_fit, wmeta = train_only_winsor(Xc, Xte)
        else:
            Xc_fit, Xte_fit, wmeta = Xc, Xte, None
        k = Xc_fit.shape[1]
        XtX = Xc_fit.T @ Xc_fit
        diag_scale = float(np.trace(XtX) / max(k, 1))
        if variant == "V1_primary":
            ridge = 1e-10 * np.eye(k)
            ridge_rule = "1e-10*I"
        else:
            ridge_val = 1e-8 * max(diag_scale, 1.0)
            ridge = ridge_val * np.eye(k)
            ridge_rule = f"1e-8*max(trace(XtX)/k={diag_scale:.6g},1)"
        try:
            coef = np.linalg.solve(XtX + ridge, Xc_fit.T @ yc)
        except np.linalg.LinAlgError:
            diags.append({"symbol": sym, "status": "LINALG_FAIL", "n_train_valid": int(mask.sum())})
            continue
        intercept = float(yc.mean() - coef @ Xc_fit.mean(axis=0))
        raw = intercept + Xte_fit @ coef
        raw_ok = raw[np.isfinite(raw)]
        p = raw.copy()
        p[~np.isfinite(p)] = np.nan
        target_floor = 0.0
        floor_rule = "max(p,0)"
        if variant in ("V3_scale_ridge_target_floor", "V4_winsor_train"):
            ypos = yc[np.isfinite(yc) & (yc > 0)]
            ymed = float(np.median(ypos)) if ypos.size else 0.0
            target_floor = max(0.0, 1e-4 * ymed)
            floor_rule = f"max(p,1e-4*train_target_median={target_floor:.6g}) (train-only)"
            p = np.maximum(p, target_floor)
        else:
            p = np.maximum(p, 0.0)
        preds[test_n.index.get_indexer(grp.index)] = p
        yte = grp["target_rv"].to_numpy(dtype=float)
        m = metrics(yte, p)
        ql_mask = np.isfinite(yte) & np.isfinite(p) & (yte > 0) & (p > 0)
        ql_mean = None
        if ql_mask.any():
            r = yte[ql_mask] / p[ql_mask]
            ql_mean = float(np.mean(r - np.log(r) - 1.0))
        diags.append({
            "symbol": sym, "status": "OK", "n_train_valid": int(mask.sum()), "n_test": int(len(grp)),
            "variant": variant, "ridge_rule": ridge_rule, "floor_rule": floor_rule,
            "coef_l2": float(np.linalg.norm(coef)), "coef_max_abs": float(np.max(np.abs(coef))),
            "raw_pred": {"min": float(np.nanmin(raw_ok)) if raw_ok.size else None, "max": float(np.nanmax(raw_ok)) if raw_ok.size else None,
                         "n_neg_raw": int(np.sum(raw_ok < 0)) if raw_ok.size else 0, "n_finite": int(raw_ok.size)},
            "post_floor": {"min": float(np.nanmin(p[np.isfinite(p)])) if np.isfinite(p).any() else None,
                           "n_le_zero": int(np.sum(np.isfinite(p) & (p <= 0))), "n_near_zero_lt_1e6": int(np.sum(np.isfinite(p) & (p > 0) & (p < 1e-6)))},
            "metrics": m, "qlike_mean_on_valid": ql_mean, "winsor": wmeta,
        })
    return preds, diags


def run_one_variant(panel: pd.DataFrame, variant: str, ablations: Dict[str, List[str]], split_defs) -> Dict[str, object]:
    idx = panel.index.get_level_values("timestamp")
    split_rows = []
    pooled = {k: [] for k in ablations if k != "A_rv_only"}
    for i, meta in enumerate(split_defs):
        sp = wf.SplitBounds(train=meta["train"], validation=meta["test"], test=meta["test"], purge_days=meta.get("purge_days", 7), embargo_days=meta.get("embargo_days", 7))
        train = panel.loc[wf._in_window(idx, sp.train)]
        test = panel.loc[wf._in_window(idx, sp.test)]
        row = {"split_id": i, "train": meta["train"], "test": meta["test"], "n_train": int(len(train)), "n_test": int(len(test)), "ablations": {}}
        preds_map = {}
        y_test = ts_test = None
        for ab_name, fcols in ablations.items():
            fcols = [c for c in fcols if c in panel.columns]
            train_n, _, test_n, _ = wf.apply_train_only_normalization(train, test, test, fcols)
            p, diags = fit_predict_variant(train_n, test_n, fcols, variant)
            y = test_n["target_rv"].to_numpy(dtype=float)
            row["ablations"][ab_name] = {"metrics": metrics(y, p), "n_features": len(fcols), "per_symbol": diags}
            preds_map[ab_name] = p
            y_test = y
            ts_test = test_n.index.get_level_values("timestamp")
        if y_test is not None and "A_rv_only" in preds_map:
            for ab_name in pooled:
                if ab_name in preds_map:
                    pooled[ab_name].append(paired_qlike_by_time(y_test, preds_map["A_rv_only"], preds_map[ab_name], ts_test))
        split_rows.append(row)
    contrasts = {}
    for k, parts in pooled.items():
        df = pd.concat(parts, ignore_index=True) if parts else pd.DataFrame(columns=["timestamp", "ql_base", "ql_alt", "diff"])
        contrasts[k] = block_bootstrap_delta_ci(df)
    return {"variant": variant, "label": LABEL, "contrasts_vs_A": contrasts, "split_results": split_rows}


def run_loo(panel: pd.DataFrame, variant: str, base_ab: str, alt_ab: str, symbols: List[str], split_defs) -> Dict[str, object]:
    idx = panel.index.get_level_values("timestamp")
    a_cols = [c for c in ABLATIONS[base_ab] if c in panel.columns]
    e_cols = [c for c in ABLATIONS[alt_ab] if c in panel.columns]
    out = {}
    for name, keep in [("all", symbols)] + [(f"drop_{s}", [x for x in symbols if x != s]) for s in symbols]:
        pooled = []
        for i, meta in enumerate(split_defs):
            sp = wf.SplitBounds(train=meta["train"], validation=meta["test"], test=meta["test"], purge_days=meta.get("purge_days", 7), embargo_days=meta.get("embargo_days", 7))
            train = panel.loc[wf._in_window(idx, sp.train)].loc[lambda d: d.index.get_level_values("symbol").isin(keep)]
            test = panel.loc[wf._in_window(idx, sp.test)].loc[lambda d: d.index.get_level_values("symbol").isin(keep)]
            if train.empty or test.empty:
                continue
            tr_a, _, te_a, _ = wf.apply_train_only_normalization(train, test, test, a_cols)
            tr_e, _, te_e, _ = wf.apply_train_only_normalization(train, test, test, e_cols)
            pa, _ = fit_predict_variant(tr_a, te_a, a_cols, variant)
            pe, _ = fit_predict_variant(tr_e, te_e, e_cols, variant)
            pooled.append(paired_qlike_by_time(te_a["target_rv"].to_numpy(float), pa, pe, te_a.index.get_level_values("timestamp")))
        df = pd.concat(pooled, ignore_index=True) if pooled else pd.DataFrame(columns=["timestamp", "ql_base", "ql_alt", "diff"])
        out[name] = block_bootstrap_delta_ci(df)
        out[name]["instruments"] = keep
    return out


def write_md(path: Path, payload: Dict[str, object]) -> None:
    lines = [
        f"# Gate 4 v4 EXPLORATORY stabilized comparison — {payload['ts']}",
        "",
        f"**{LABEL}**",
        f"- Git SHA: `{payload.get('git_sha')}`",
        f"- Prereg: `{PREREG_V4}` — `FROZEN_BEFORE_OUTCOMES`, `confirmatory_claim_go=NO_GO`, `exploratory_smoke_authorized_after_freeze=true`",
        "- Does NOT replace prereg A-E contrasts or change confirmatory estimands. No confirmatory GO / economic value / promotion.",
        "- Leakage controls preserved: chronological multi-split, purge/embargo as prereg v3_30d, train-only normalization (`wf.apply_train_only_normalization`), train-only ridge scale/winsor/floor parameters, block bootstrap by UTC time blocks.",
        "",
        "## Variants (EXPLORATORY, fixed rules)",
        "- V1_primary: ridge=1e-10*I, floor 0 (matches primary fit).",
        "- V2_scale_ridge: ridge=1e-8*max(trace(X'X)/k,1)*I, floor 0.",
        "- V3_scale_ridge_target_floor: V2 + train-only floor max(0,1e-4*train_target_median) per instrument/split.",
        "- V4_winsor_train: V3 + train-only standardized-feature winsor q0.5/q99.5 (train bounds applied to train/test).",
        "",
        "## Pooled ΔQLIKE vs A (alt-base; negative better for alt), 95% block bootstrap CI",
        "| Variant | Contrast | Point | CI low | CI high | n_obs | n_blocks | eff_blocks | ci_valid | regime_flags | Verdict (EXPLORATORY) |",
        "|---|---|---:|---:|---:|---:|---:|---:|:---:|---|---|",
    ]
    for vname, vres in payload["variants"].items():
        for c, ci in vres["contrasts_vs_A"].items():
            pt = ci.get("point"); lo = ci.get("ci_low"); hi = ci.get("ci_high")
            verdict = "inconclusive (CI spans 0)" if (lo is not None and hi is not None and lo <= 0 <= hi) else ("alt worse (CI>0)" if (lo is not None and lo > 0) else ("alt better (CI<0)" if (hi is not None and hi < 0) else "unknown"))
            eff = ci.get("effective_block_count", ci.get("n_blocks"))
            flags = ",".join(ci.get("regime_flags") or []) or "ok"
            acc = ci.get("ci_accounting_valid")
            lines.append(f"| {vname} | {c} | {pt} | {lo} | {hi} | {ci.get('n_obs')} | {ci.get('n_blocks')} | {eff} | {acc} | {flags} | {verdict} |")
    lines += ["", "## E vs A instrument LOO (V3, EXPLORATORY)", "| LOO | Point | CI low | CI high | n_obs | eff_blocks | ci_valid | regime_flags |", "|---|---:|---:|---:|---:|---:|:---:|---|"]
    for k, ci in payload.get("loo_e_vs_a_v3", {}).items():
        flags = ",".join(ci.get("regime_flags") or []) or "ok"
        lines.append(f"| {k} | {ci.get('point')} | {ci.get('ci_low')} | {ci.get('ci_high')} | {ci.get('n_obs')} | {ci.get('effective_block_count', ci.get('n_blocks'))} | {ci.get('ci_accounting_valid')} | {flags} |")
    lines += ["", "## Split-3 B/D/E diagnostics (V1 vs V3, selected)", ""]
    for vname in ["V1_primary", "V3_scale_ridge_target_floor"]:
        vres = payload["variants"][vname]
        s3 = next((s for s in vres["split_results"] if s["split_id"] == 3), None)
        if not s3:
            continue
        lines.append(f"### {vname} split 3")
        for ab in ["A_rv_only", "B_rv_signed", "D_rv_signed_abs", "E_rv_funding_trails"]:
            m = s3["ablations"].get(ab, {}).get("metrics", {})
            lines.append(f"- {ab}: qlike={m.get('qlike')} valid_n={m.get('valid_n')} n={m.get('n')}")
            for d in s3["ablations"].get(ab, {}).get("per_symbol", []):
                if d.get("status") == "OK":
                    lines.append(f"  - {d['symbol']}: ql={d['metrics'].get('qlike')} raw_neg={d['raw_pred']['n_neg_raw']}/{d['raw_pred']['n_finite']} coef_max={d.get('coef_max_abs')} floor={d.get('floor_rule')}")
    lines += ["", "## Interpretation (EXPLORATORY ONLY — NOT CONFIRMATORY)", payload.get("interpretation", ""), "", f"Artifacts: `{payload.get('json_path')}`, `{path}`"]
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def make_interpretation(payload: Dict[str, object]) -> str:
    v1e = payload["variants"]["V1_primary"]["contrasts_vs_A"]["E_rv_funding_trails"]
    v3e = payload["variants"]["V3_scale_ridge_target_floor"]["contrasts_vs_A"]["E_rv_funding_trails"]
    def spans0(ci): return ci.get("ci_low") is not None and ci.get("ci_high") is not None and ci["ci_low"] <= 0 <= ci["ci_high"]
    parts = [f"V1 E vs A point={v1e.get('point')} CI=[{v1e.get('ci_low')},{v1e.get('ci_high')}] ({'inconclusive' if spans0(v1e) else 'not spanning 0'}).",
             f"V3 (scale-aware ridge + train-only target-scale floor) E vs A point={v3e.get('point')} CI=[{v3e.get('ci_low')},{v3e.get('ci_high')}] ({'inconclusive' if spans0(v3e) else 'not spanning 0'})."]
    loo = payload.get("loo_e_vs_a_v3", {})
    allp = loo.get("all", {}).get("point")
    no_improve = all((v.get("ci_low") is None or v.get("ci_low") > 0 or spans0(v)) for k, v in loo.items())
    parts.append(f"V3 E vs A LOO (EXPLORATORY): all={allp}; no LOO shows a CI entirely below 0={no_improve}.")
    v3b = payload["variants"]["V3_scale_ridge_target_floor"]["contrasts_vs_A"]["B_rv_signed"]
    parts.append(f"V3 B vs A point={v3b.get('point')} CI=[{v3b.get('ci_low')},{v3b.get('ci_high')}].")
    # check split 3 blowups reduced?
    s3v1 = next(s for s in payload["variants"]["V1_primary"]["split_results"] if s["split_id"] == 3)
    s3v3 = next(s for s in payload["variants"]["V3_scale_ridge_target_floor"]["split_results"] if s["split_id"] == 3)
    b1 = s3v1["ablations"]["B_rv_signed"]["metrics"].get("qlike")
    b3 = s3v3["ablations"]["B_rv_signed"]["metrics"].get("qlike")
    parts.append(f"Split 3 B QLIKE V1={b1} -> V3={b3} (EXPLORATORY diagnostic).")
    if spans0(v3e) and no_improve:
        parts.append("**EXPLORATORY NO-GO signal (not confirmatory):** principled stabilized comparison does not show credible out-of-sample improvement for funding ablations on this local 2024-04..09 slice; E remains inconclusive/sensitive and no LOO demonstrates improvement. No promotion, no sealed-anchor reuse, no confirmatory claim.")
    return " ".join(parts)


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--symbols", default="BTCUSDT,ETHUSDT,SOLUSDT,XRPUSDT,BNBUSDT")
    ap.add_argument("--start", default="2024-04-01")
    ap.add_argument("--end", default="2024-09-30")
    ap.add_argument("--include-cache", action="store_true", default=True)
    ap.add_argument("--variants", default="V1_primary,V2_scale_ridge,V3_scale_ridge_target_floor,V4_winsor_train")
    ap.add_argument("--out-suffix", default=None)
    ap.add_argument("--state-dir", default="research_state/gate4_v4_exploratory_stab")
    ap.add_argument("--results-dir", default="results/fclr_heavy001")
    args = ap.parse_args(argv)
    symbols = [s.strip() for s in args.symbols.split(",") if s.strip()]
    variants = [v.strip() for v in args.variants.split(",") if v.strip()]
    ts = args.out_suffix or _ts()
    state_dir = REPO / args.state_dir
    results_dir = REPO / args.results_dir
    state_dir.mkdir(parents=True, exist_ok=True)
    results_dir.mkdir(parents=True, exist_ok=True)
    kpanel = load_kline_panel(symbols, args.start, args.end, horizon=24, include_cache=args.include_cache)
    fpanel = load_funding_panel(symbols, args.start, args.end, include_cache=args.include_cache)
    panel = add_funding_to_panel(kpanel, fpanel)
    payload = {
        "label": LABEL, "ts": ts, "git_sha": _git_sha(), "symbols": symbols,
        "start": args.start, "end": args.end, "include_cache": args.include_cache,
        "prereg_v4": PREREG_V4, "confirmatory_claim_go": "NO_GO",
        "exploratory_smoke_authorized_after_freeze": True,
        "prior_exec": "research_state/gate4_v4_exploratory_exec/run_manifest_funding_v4_exploratory_exec_20261109T004003Z.json",
        "prior_diag": "research_state/gate4_v4_exploratory_diag/gate4_v4_exploratory_diag_20261109T021456Z.json",
        "variants": {}, "commands": {
            "run": f"python scripts/run_gate4_v4_exploratory_stab.py --out-suffix {ts}",
        },
    }
    for v in variants:
        payload["variants"][v] = run_one_variant(panel, v, ABLATIONS, PRE_REG_SPLITS_V3_30D)
    payload["loo_e_vs_a_v3"] = run_loo(panel, "V3_scale_ridge_target_floor", "A_rv_only", "E_rv_funding_trails", symbols, PRE_REG_SPLITS_V3_30D)
    payload["interpretation"] = make_interpretation(payload)
    json_path = state_dir / f"gate4_v4_exploratory_stab_{ts}.json"
    md_state = state_dir / f"gate4_v4_exploratory_stab_{ts}.md"
    md_results = results_dir / f"gate4_v4_exploratory_stab_{ts}.md"
    payload["json_path"] = str(json_path.relative_to(REPO))
    payload["md_state_path"] = str(md_state.relative_to(REPO))
    payload["md_results_path"] = str(md_results.relative_to(REPO))
    json_path.write_text(json.dumps(payload, indent=2, default=str) + "\n", encoding="utf-8")
    write_md(md_state, payload)
    write_md(md_results, payload)
    print(json.dumps({"label": LABEL, "json": str(json_path), "interpretation": payload["interpretation"]}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
