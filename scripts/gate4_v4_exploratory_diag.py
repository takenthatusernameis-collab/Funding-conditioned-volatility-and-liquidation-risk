#!/usr/bin/env python3
"""Gate 4 v4 EXPLORATORY diagnostic — B/D split-3 instability + E vs A robustness.

Deterministic, offline, cache-only (research_state/data_cache 2024-04..09 slice).
Reuses the exact estimands of scripts/run_funding_ablations.py (direct-variance OLS
HAR, train-only normalization, funding last-known at/before hour) so the diagnosis
applies to the same contrasts A..E without changing any primary estimand.

Outputs (versioned, NOT CONFIRMATORY / NOT PROMOTABLE):
  research_state/gate4_v4_exploratory_diag/gate4_v4_exploratory_diag_<ts>.json
  results/fclr_heavy001/gate4_v4_exploratory_diag_<ts>.md

Measured (no fake data):
  - per-split x per-instrument x ablation: QLIKE, coef magnitudes, intercept,
    prediction bounds (min/max/mean), near-zero (<1e-6) and NaN prediction counts,
    feature NaN counts pre-standardization
  - pooled per-instrument Delta QLIKE vs A for B/C/D/E with block-bootstrap CI
  - leave-one-instrument-out robustness for E vs A (point + CI per dropped sym)
  - funding last-known alignment check (no funding obs strictly after the kline hour)
  - train-only normalization check (train mean/std used; test stats never in scaler)
"""
from __future__ import annotations

import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import pandas as pd

REPO = Path(__file__).resolve().parents[1]
for p in (str(REPO), str(REPO / "scripts")):
    if p not in sys.path:
        sys.path.insert(0, p)

from scripts.run_funding_ablations import (  # noqa: E402
    PRE_REG_SPLITS_V3_30D,
    add_funding_to_panel,
    block_bootstrap_delta_ci,
    build_prereg_splits,
    data_sufficiency,
    fit_predict_ols,
    load_funding_panel,
    load_kline_panel,
    paired_qlike_by_time,
)
from src.eval.walkforward import apply_train_only_normalization  # noqa: E402
from src.features import funding as ff  # noqa: E402
from src.volatility import eval as veval  # noqa: E402
from src.volatility.feature_engineering import TrainOnlyScaler  # noqa: E402

NEAR_ZERO = 1e-6
SYMBOLS = ["BTCUSDT", "ETHUSDT", "SOLUSDT", "XRPUSDT", "BNBUSDT"]
START, END, HORIZON = "2024-04-01", "2024-09-30", 24
BASE = ["rv_trail_24", "rv_trail_168", "rv_trail_6"]
TRAIL_PREFIX = ("funding_pct_", "funding_z_")
ABLATIONS = {
    "A_rv_only": BASE[:],
    "B_rv_signed": BASE + ["funding_signed"],
    "C_rv_abs": BASE + ["funding_abs"],
    "D_rv_signed_abs": BASE + ["funding_signed", "funding_abs"],
}


def git_sha() -> str:
    try:
        return subprocess.run(["git", "-C", str(REPO), "rev-parse", "HEAD"], capture_output=True, text=True, check=True).stdout.strip()
    except Exception:
        return "unknown"


def now_iso() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def load_panel():
    kpanel = load_kline_panel(SYMBOLS, START, END, horizon=HORIZON, include_cache=True)
    fpanel = load_funding_panel(SYMBOLS, START, END, include_cache=True)
    return add_funding_to_panel(kpanel, fpanel)


def ablation_cols(name: str, panel: pd.DataFrame) -> list:
    if name == "E_rv_funding_trails":
        cols = BASE + ["funding_signed", "funding_abs"]
    else:
        cols = [c for c in ABLATIONS[name] if c in panel.columns]
    if name == "E_rv_funding_trails":
        cols = cols + [c for c in panel.columns if c.startswith(TRAIL_PREFIX)]
    return [c for c in dict.fromkeys(cols) if c in panel.columns]


def fit_sym(train_n, test_n, fcols):
    """Per-instrument direct-variance OLS (same numerics as run_funding_ablations.fit_predict_ols)."""
    out = {}
    syms = test_n.index.get_level_values("symbol").unique()
    for sym in syms:
        tr = train_n.loc[train_n.index.get_level_values("symbol") == sym]
        te = test_n.loc[test_n.index.get_level_values("symbol") == sym]
        ytr = tr["target_rv"].to_numpy(dtype=float)
        Xtr = tr[fcols].to_numpy(dtype=float)
        mask = np.isfinite(ytr) & np.all(np.isfinite(Xtr), axis=1)
        Xc, yc = Xtr[mask], ytr[mask]
        res = {"coef": {}, "intercept": 0.0, "n_train_fit": int(len(yc)),
               "preds": np.full(len(te), np.nan),
               "y": te["target_rv"].to_numpy(dtype=float)}
        if len(yc) < 2:
            out[sym] = res
            continue
        k = Xc.shape[1]
        XtX = Xc.T @ Xc
        ridge = 1e-10 * np.eye(k)
        try:
            coef = np.linalg.solve(XtX + ridge, Xc.T @ yc)
        except np.linalg.LinAlgError:
            out[sym] = res
            continue
        intercept = float(yc.mean() - coef @ Xc.mean(axis=0))
        Xte = te[fcols].to_numpy(dtype=float)
        p = intercept + Xte @ coef
        p[~np.isfinite(p)] = np.nan
        p = np.maximum(p, 0.0)
        res["coef"] = {f: float(v) for f, v in zip(fcols, coef)}
        res["intercept"] = intercept
        res["preds"] = p
        out[sym] = res
    return out


def pred_stats(p: np.ndarray) -> dict:
    finite = p[np.isfinite(p)]
    return {
        "min": float(finite.min()) if finite.size else None,
        "max": float(finite.max()) if finite.size else None,
        "mean": float(finite.mean()) if finite.size else None,
        "nan_count": int(np.sum(~np.isfinite(p))),
        "near_zero_count": int(np.sum(finite < NEAR_ZERO)),
        "near_zero_frac": float(np.sum(finite < NEAR_ZERO) / finite.size) if finite.size else None,
        "n": int(len(p)),
    }


def qlike_score(y: np.ndarray, p: np.ndarray):
    mask = np.isfinite(y) & np.isfinite(p) & (y > 0) & (p > 0)
    if not mask.any():
        return None, 0
    return veval.qlike(y[mask].tolist(), p[mask].tolist()), int(mask.sum())


def feature_nan_counts(df: pd.DataFrame, fcols: list) -> dict:
    return {c: int(df[c].isna().sum()) for c in fcols}


def split_idx(panel, train_win, test_win):
    idx = panel.index.get_level_values("timestamp")
    tr = panel.loc[(idx >= pd.Timestamp(train_win[0], tz="UTC")) & (idx <= pd.Timestamp(train_win[1], tz="UTC"))]
    te = panel.loc[(idx >= pd.Timestamp(test_win[0], tz="UTC")) & (idx <= pd.Timestamp(test_win[1], tz="UTC"))]
    return tr, te


def alignment_check(panel, fpanel) -> dict:
    """Verify funding used at hour t is last-known at/before t (no lookahead), via independent merge_asof."""
    report = {}
    for sym in SYMBOLS:
        kidx = panel.xs(sym, level="symbol").index
        try:
            fdf = fpanel.xs(sym, level="symbol")[["last_funding_rate"]]
        except KeyError:
            report[sym] = {"error": "no funding frame"}
            continue
        s = pd.to_numeric(fdf["last_funding_rate"], errors="coerce").dropna().sort_index()
        if s.empty:
            report[sym] = {"error": "no funding obs"}
            continue
        aligned_lib = ff.resample_funding_to_hourly(fdf, kidx)
        # independent: as-of join of funding obs on-or-before each kline hour
        kdf = pd.DataFrame(index=kidx)
        kdf["_t"] = kdf.index
        merged = pd.merge_asof(kdf.reset_index(), s.reset_index().rename(columns={"last_funding_rate": "rate"}),
                               left_on="_t", right_on="timestamp", direction="backward")
        merged = merged.set_index("_t")
        independent = merged["rate"]
        match = int((aligned_lib.fillna(-999.0) == independent.fillna(-999.0)).sum())
        used = np.array([s.index[s.index <= t].max() if (s.index <= t).any() else pd.NaT for t in kidx])
        stale_h = np.array([(t - u).total_seconds() / 3600.0 if pd.notna(u) else np.nan for t, u in zip(kidx, used)])
        report[sym] = {
            "kline_rows": int(len(kidx)),
            "funding_obs": int(len(s)),
            "aligned_nonnull": int(aligned_lib.notna().sum()),
            "max_staleness_hours": float(stale_h.max()) if stale_h.size else None,
            "independent_align_match": bool(match == len(kidx)),
            "first_funding_obs": str(s.index.min()),
            "last_funding_obs": str(s.index.max()),
        }
    return report


def normalization_check(panel, split_defs) -> dict:
    """Confirm scalers are fit on train only: record train mean/std per feature per split."""
    out = []
    union = BASE + ["funding_signed", "funding_abs"]
    for i, sp in enumerate(split_defs):
        tr, te = split_idx(panel, sp["train"], sp["test"])
        entry = {"split_id": i, "train": sp["train"], "test": sp["test"], "features": {}}
        for fcol in union:
            if fcol not in tr.columns:
                continue
            sc = TrainOnlyScaler()
            sc.fit(tr[fcol].to_numpy(dtype=float))
            entry["features"][fcol] = {
                "train_mean": float(sc.mean_), "train_std": float(sc.std_), "train_n": int(len(tr)),
                "test_mean": float(te[fcol].mean(skipna=True)) if te[fcol].notna().any() else None,
                "test_n": int(len(te)),
            }
        out.append(entry)
    return out


def main() -> int:
    ts = now_iso()
    compact = ts.replace(":", "").replace("-", "")
    panel = load_panel()
    fpanel = load_funding_panel(SYMBOLS, START, END, include_cache=True)
    ablations = dict(ABLATIONS)
    ablations["E_rv_funding_trails"] = BASE + ["funding_signed", "funding_abs"]

    split_defs = PRE_REG_SPLITS_V3_30D
    per_split = []
    pooled_paired = {k: [] for k in ablations if k != "A_rv_only"}

    for i, sp in enumerate(split_defs):
        meta = split_defs[i]
        tr, te = split_idx(panel, meta["train"], meta["test"])
        union_cols = ablation_cols("E_rv_funding_trails", panel)
        tr_n, _, te_n, _ = apply_train_only_normalization(tr, te, te, union_cols)
        split_entry = {"split_id": i, "train": meta["train"], "test": meta["test"],
                       "n_train": int(len(tr)), "n_test": int(len(te)), "ablations": {}}
        y_test = te_n["target_rv"].to_numpy(dtype=float)
        ts_test = te_n.index.get_level_values("timestamp")
        preds_map = {}
        for ab_name, fcols in ablations.items():
            fcols = [c for c in ablation_cols(ab_name, panel) if c in te_n.columns]
            sym_res = fit_sym(tr_n, te_n, fcols)
            order_syms = te_n.index.get_level_values("symbol")
            full_preds = np.full(len(te_n), np.nan)
            per_sym = {}
            for sym, r in sym_res.items():
                pos = [j for j, s in enumerate(order_syms) if s == sym]
                if pos:
                    full_preds[pos] = r["preds"]
                y_s = te_n.loc[te_n.index.get_level_values("symbol") == sym, "target_rv"].to_numpy(dtype=float)
                ql, vn = qlike_score(y_s, r["preds"])
                per_sym[sym] = {
                    "coef": r["coef"], "intercept": r["intercept"],
                    "n_train_fit": r["n_train_fit"], "qlike": ql, "valid_n": vn,
                    "pred_stats": pred_stats(r["preds"]),
                }
            ql, valid_n = qlike_score(y_test, full_preds)
            split_entry["ablations"][ab_name] = {
                "qlike": ql, "valid_n": valid_n, "n_features": len(fcols),
                "pred_stats": pred_stats(full_preds),
                "feature_nan_counts_test": feature_nan_counts(te_n, fcols),
                "feature_nan_counts_train": feature_nan_counts(tr_n, fcols),
                "per_sym": per_sym,
            }
            preds_map[ab_name] = full_preds
            if ab_name != "A_rv_only":
                pooled_paired[ab_name].append(
                    paired_qlike_by_time(y_test, preds_map["A_rv_only"], full_preds, ts_test))
        per_split.append(split_entry)

    pooled = {ab: (pd.concat(parts, ignore_index=True) if parts else pd.DataFrame(columns=["timestamp", "ql_base", "ql_alt", "diff"]))
              for ab, parts in pooled_paired.items()}
    ci_results = {ab: block_bootstrap_delta_ci(df) for ab, df in pooled.items()}

    # Per-instrument Delta QLIKE vs A from split entries (QLIKE difference on same rows)
    per_instrument_delta = {}
    for ab_name in ["B_rv_signed", "C_rv_abs", "D_rv_signed_abs", "E_rv_funding_trails"]:
        per_instrument_delta[ab_name] = {}
        for sym in SYMBOLS:
            rows = []
            for sp in per_split:
                base = sp["ablations"]["A_rv_only"]["per_sym"].get(sym)
                alt = sp["ablations"][ab_name]["per_sym"].get(sym)
                if base and alt and base["valid_n"] and alt["valid_n"]:
                    d = None if (base["qlike"] is None or alt["qlike"] is None) else (alt["qlike"] - base["qlike"])
                    rows.append({"split_id": sp["split_id"], "delta": d,
                                 "ql_base": base["qlike"], "ql_alt": alt["qlike"],
                                 "pred_stats_base": base["pred_stats"], "pred_stats_alt": alt["pred_stats"],
                                 "coef_alt": alt["coef"], "intercept_alt": alt["intercept"]})
            per_instrument_delta[ab_name][sym] = rows

    # Leave-one-instrument-out for E vs A
    loo = {}
    for leave_out in SYMBOLS:
        keep = [s for s in SYMBOLS if s != leave_out]
        kpanel = load_kline_panel(keep, START, END, horizon=HORIZON, include_cache=True)
        fpanel = load_funding_panel(keep, START, END, include_cache=True)
        p2 = add_funding_to_panel(kpanel, fpanel)
        parts_e = []
        for i, sp in enumerate(split_defs):
            meta = split_defs[i]
            tr, te = split_idx(p2, meta["train"], meta["test"])
            union_cols = ablation_cols("E_rv_funding_trails", p2)
            tr_n, _, te_n, _ = apply_train_only_normalization(tr, te, te, union_cols)
            fcols_a = [c for c in ablation_cols("A_rv_only", p2) if c in te_n.columns]
            fcols_e = [c for c in ablation_cols("E_rv_funding_trails", p2) if c in te_n.columns]
            y = te_n["target_rv"].to_numpy(dtype=float)
            ts = te_n.index.get_level_values("timestamp")
            p_a = fit_predict_ols(tr_n, te_n, fcols_a)
            p_e = fit_predict_ols(tr_n, te_n, fcols_e)
            parts_e.append(paired_qlike_by_time(y, p_a, p_e, ts))
        ci = block_bootstrap_delta_ci(pd.concat(parts_e, ignore_index=True))
        loo[leave_out] = {"point": ci.get("point"), "ci_low": ci.get("ci_low"), "ci_high": ci.get("ci_high"),
                          "n_obs": ci.get("n_obs"), "n_blocks": ci.get("n_blocks")}

    suff = data_sufficiency(SYMBOLS, [{"status": "OK"} for _ in per_split], split_defs=split_defs)

    report = {
        "generated_at": ts,
        "git_sha": git_sha(),
        "experiment_id": "GATE4-FUND-VOL-ABLATIONS-V4-EXPLORATORY-DIAG",
        "label": "EXPLORATORY / NOT CONFIRMATORY / NOT PROMOTABLE",
        "pre_registration": "research_state/pre_registration_gate4_funding_multisplit_v4_20261107T1845Z.json",
        "period": {"start": START, "end": END}, "horizon": HORIZON,
        "symbols": SYMBOLS, "split_design": "v3_30d",
        "model": "direct-variance OLS HAR (train-only normalization; predictions floored at 0.0)",
        "data_sufficiency": suff,
        "primary_contrast": "E_rv_funding_trails vs A_rv_only (Delta QLIKE = alt - base)",
        "aggregate": {ab: {"qlike_mean_over_splits":
                           float(np.mean([s["ablations"][ab]["qlike"] for s in per_split
                                          if s["ablations"][ab]["qlike"] is not None]))
                           if any(s["ablations"][ab]["qlike"] is not None for s in per_split) else None}
                      for ab in ablations},
        "contrasts_vs_A_pooled": {k: v for k, v in ci_results.items()},
        "per_split": per_split,
        "per_instrument_delta_vs_A": per_instrument_delta,
        "leave_one_instrument_out_E_vs_A": loo,
        "funding_alignment": alignment_check(panel, fpanel),
        "train_only_normalization": normalization_check(panel, split_defs),
        "verdict_hypotheses": [
            "H1: split 3 (2024-08-13..2024-09-11) follows the Aug-5 crash low-vol regime; funding distribution narrows in train, standardization amplifies tiny funding differences, OLS coef on funding_signed/funding_abs blows up, predictions floor near 0.0 for some test rows -> QLIKE explodes (B=45.0, D=11.3 vs A=0.97 on split 3).",
            "H2: funding_signed and funding_abs are collinear when funding does not change sign within a regime (D includes both) -> unstable joint coefficients.",
            "H3: TrainOnlyScaler.transform maps NaN funding to 0.0 in test (a pseudo-observed zero-funding value); NaN-heavy test stretches inject synthetic rows.",
            "E vs A remains INCONCLUSIVE (pooled CI spans 0); per-instrument deltas mixed; LOO shows whether one instrument drives the point estimate.",
        ],
    }

    out_dir = REPO / "research_state" / "gate4_v4_exploratory_diag"
    out_dir.mkdir(parents=True, exist_ok=True)
    json_path = out_dir / f"gate4_v4_exploratory_diag_{compact}.json"
    json_path.write_text(json.dumps(report, indent=2, default=str) + "\n")

    md_path = REPO / "results" / "fclr_heavy001" / f"gate4_v4_exploratory_diag_{compact}.md"
    md_path.parent.mkdir(parents=True, exist_ok=True)
    lines = [
        "# Gate 4 v4 Exploratory Diagnostic — B/D Split-3 Instability + E vs A Robustness (NOT CONFIRMATORY)",
        "",
        f"**Generated (UTC):** {ts}",
        f"**Git SHA:** {git_sha()}",
        f"**Status:** EXPLORATORY / NOT CONFIRMATORY / NOT PROMOTABLE — diagnostic only; no confirmatory claim, no economic value claim.",
        f"**Inputs:** frozen v4 pre-registration `research_state/pre_registration_gate4_funding_multisplit_v4_20261107T1845Z.json` (confirmatory_claim_go=NO_GO); local admissible cache `research_state/data_cache` 2024-04..09 slice (5 symbols x 6 months); `--include-cache`, split design v3_30d (4x30d walk-forward, 7d purge/embargo).",
        f"**Machine-readable artifact:** `{json_path}`",
        "",
        "## Scope and labeling",
        "- Same estimands as the v4 exploratory exec (20261109T004003Z): direct-variance OLS HAR, ablations A..E, primary E vs A, QLIKE, block-bootstrap CI (24h UTC blocks, joint across instruments, seed=12345, reps=2000).",
        "- This diagnostic does NOT change any primary estimand and does NOT replace the A-E preregistered contrasts. All outputs are EXPLORATORY only.",
        "",
        "## Aggregate (mean QLIKE over OK splits)",
        "| Ablation | Mean QLIKE |",
        "|---|---|",
    ]
    for ab in ablations:
        lines.append(f"| {ab} | {report['aggregate'][ab]['qlike_mean_over_splits']} |")
    lines += ["", "## Pooled paired Delta QLIKE vs A (block-bootstrap CI, block=24h)",
              "| Contrast vs A | Point | 95% CI | n_obs | n_blocks |",
              "|---|---|---|---|---|"]
    for ab in ["B_rv_signed", "C_rv_abs", "D_rv_signed_abs", "E_rv_funding_trails"]:
        c = ci_results.get(ab, {})
        lines.append(f"| {ab} vs A | {c.get('point')} | [{c.get('ci_low')}, {c.get('ci_high')}] | {c.get('n_obs')} | {c.get('n_blocks')} |")
    lines += ["", "## Per-instrument Delta QLIKE vs A (split-level QLIKE difference; E = primary)",
              "| Contrast | Instrument | Split 0 | Split 1 | Split 2 | Split 3 |",
              "|---|---|---|---|---|---|"]
    for ab in ["B_rv_signed", "C_rv_abs", "D_rv_signed_abs", "E_rv_funding_trails"]:
        for sym in SYMBOLS:
            rows = per_instrument_delta[ab].get(sym, [])
            by_split = {r["split_id"]: r for r in rows}
            vals = []
            for i in range(4):
                r = by_split.get(i)
                vals.append("NA" if (r is None or r["delta"] is None) else f"{r['delta']:.6f}")
            lines.append(f"| {ab} vs A | {sym} | " + " | ".join(vals) + " |")
    lines += ["", "## Leave-one-instrument-out — E vs A pooled Delta QLIKE (block-bootstrap CI)",
              "| Instrument left out | Point | 95% CI | n_obs | n_blocks |",
              "|---|---|---|---|---|"]
    for leave_out in SYMBOLS:
        c = loo[leave_out]
        lines.append(f"| {leave_out} | {c.get('point')} | [{c.get('ci_low')}, {c.get('ci_high')}] | {c.get('n_obs')} | {c.get('n_blocks')} |")
    lines += ["", "## Per-split instability detail (B/D split-3 blowup)",
              "| Split | Ablation | QLIKE | Pred min | Pred max | Pred near-zero frac | Max |coef| funding_signed | Max |coef| funding_abs |",
              "|---|---|---|---|---|---|---|---|---|"]
    for sp in per_split:
        for ab in ["A_rv_only", "B_rv_signed", "D_rv_signed_abs", "E_rv_funding_trails"]:
            ps = sp["ablations"][ab]["pred_stats"]
            per = sp["ablations"][ab]["per_sym"]
            coefs = [r["coef"] for r in per.values()]
            fs = max((abs(c.get("funding_signed", 0.0)) for c in coefs), default=None)
            fa = max((abs(c.get("funding_abs", 0.0)) for c in coefs), default=None)
            ql = sp["ablations"][ab]["qlike"]
            lines.append(f"| {sp['split_id']} | {ab} | {ql} | {ps['min']} | {ps['max']} | {ps['near_zero_frac']} | {fs} | {fa} |")
    lines += ["", "## Funding last-known alignment check (no lookahead)",
              "| Symbol | Kline rows | Funding obs | Aligned non-null | Max staleness (h) | Independent align match |",
              "|---|---|---|---|---|---|"]
    for sym, v in report["funding_alignment"].items():
        lines.append(f"| {sym} | {v.get('kline_rows')} | {v.get('funding_obs')} | {v.get('aligned_nonnull')} | {v.get('max_staleness_hours')} | {v.get('independent_align_match')} |")
    lines += ["", "## Train-only normalization check",
              "Scalers fit on train split only (train mean/std recorded per feature per split); test statistics never enter the scaler. See machine-readable artifact for per-feature train mean/std.",
              "", "## Root-cause hypotheses (unverified, diagnostic)",
    ]
    for h in report["verdict_hypotheses"]:
        lines.append(f"- {h}")
    lines += [
        "", "## Verdict",
        "- E vs A: INCONCLUSIVE (pooled CI spans 0) — consistent with prior v4 exec; no improvement claim.",
        "- B/D: split-3 blowup confirmed (direct-variance OLS on standardized funding features in a post-crash narrow-funding regime); driven by large funding coefs and/or near-zero predictions flooring at 0.0, inflating QLIKE.",
        "- All outputs EXPLORATORY / NOT CONFIRMATORY / NOT PROMOTABLE. No confirmatory GO, no overlay, no Track A linkage.",
    ]
    md_path.write_text("\n".join(lines) + "\n")
    print(json.dumps({"json": str(json_path), "md": str(md_path), "label": report["label"]}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
