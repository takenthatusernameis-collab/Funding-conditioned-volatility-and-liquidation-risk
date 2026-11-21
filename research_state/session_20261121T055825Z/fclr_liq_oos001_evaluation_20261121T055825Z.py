#!/usr/bin/env python3
"""
FCLR-LIQ-OOS-FORECAST-001 Step 2: OUT-OF-SAMPLE LIQUIDATION-RISK FORECAST EVALUATION.

Executes the FROZEN pre-outcomes protocol
(research_state/session_20261121T055825Z/fclr_liq_oos001_protocol_freeze_20261121T055825Z.json)
on the verified frozen combined liquidation panel.

  estimand : out-of-sample forecast of next-24h OBSERVED notional-weighted
             liquidation intensity (sum notional_usd per coin per 24h bucket)
  contrast : C2 (funding-conditioned) vs B1 (RV-only)
    B1  = [log(rv24h)]
    C2  = [log(rv24h), fundingRate, abs_fund_pct, premium, ema_dist]
  grain    : coin-day; features = last value within the current 24h bucket
             (causal, pre-target); target = next-24h sum(notional_usd)
  walk     : chronological expanding walk-forward train/validation/test blocks
             (no random split, no threshold-shopping, no holdout tuning)
             Train 2025-03-22..2025-12-31 ; Val 2026-01-01..2026-03-31
             Test blocks: 2026-04-01..2026-05-31, 2026-06-01..2026-08-31,
                          2026-09-01..2026-10-31 ; purge 1 day
  metrics  : QLIKE (continuous intensity), Brier + LogLoss (binary event
             intensity > train-median, logistic probability)
  inference: block bootstrap across the 3 test blocks (>=2000 reps, seed 20261121),
             Holm step-down over the joint 3-metric family, 95% CI
  gate     : per metric -> CI entirely < 0 (C2 strictly better) AND Holm adj_p < 0.05
             AND relative reduction (mean_B1-mean_C2)/mean_B1 >= 2.0% materiality floor
  verdict  : SUPPORTED only if ALL three metrics clear every gate; else honest
             NOT_SUPPORTED. No threshold-shopping or floor relaxation after outcomes.

Reads ONLY the panel + frozen protocol (pre-outcome). Writes only timestamped
fclr_liq_oos001_evaluation_20261121T055825Z.{py,json,md} under the session dir.
Never mutates sealed artifacts or .github/workflows. No network.
"""
from __future__ import annotations

import hashlib
import json
import math
import random
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import pandas as pd

REPO = Path(__file__).resolve().parents[2]
RS = REPO / "research_state"
SESSION = "20261121T055825Z"
OUT_DIR = RS / f"session_{SESSION}"
PANEL_LIQ = RS / "fclr_liq_combined_panel_20261115T181405Z.parquet"
PANEL_LIQ_SHA256 = "81a100d5d0625832bebabaabea13b786e15319577721cfe8507da5b779ec7f14"
PANEL_FCLR001 = RS / "fclr011_recompute_panel_20261115T234700Z.parquet"
PANEL_FCLR001_SHA256 = "41962f823e59de5989c7d854cb3180cad61a4cbc2f5f230133c41b321342c1f4"
PROTOCOL_PATH = OUT_DIR / f"fclr_liq_oos001_protocol_freeze_{SESSION}.json"
OUT_JSON = OUT_DIR / f"fclr_liq_oos001_evaluation_{SESSION}.json"
OUT_MD = OUT_DIR / f"fclr_liq_oos001_evaluation_{SESSION}.md"
SEED = 20261121
N_BOOT = 2000
ALPHA = 0.05
MATERIALITY_FLOOR = 0.02
EPS = 1e-12
COINS = ["BTC", "ETH", "BNB", "SOL", "XRP"]


def sha256_file(p: Path) -> str:
    h = hashlib.sha256()
    with p.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def qlike(y: float, yhat: float):
    if y is None or yhat is None or y <= 0 or yhat <= 0:
        return None
    if not (math.isfinite(y) and math.isfinite(yhat)):
        return None
    ratio = y / yhat
    return ratio - math.log(ratio) - 1.0


def _solve_linear(A, b):
    n = len(A)
    M = [row[:] + [b[i]] for i, row in enumerate(A)]
    for col in range(n):
        piv = max(range(col, n), key=lambda r: abs(M[r][col]))
        if abs(M[piv][col]) < 1e-18:
            continue
        M[col], M[piv] = M[piv], M[col]
        for r in range(col + 1, n):
            factor = M[r][col] / M[col][col] if M[col][col] != 0 else 0.0
            for c2 in range(col, n + 1):
                M[r][c2] -= factor * M[col][c2]
    x = [0.0] * n
    for i in range(n - 1, -1, -1):
        s = M[i][n]
        for j in range(i + 1, n):
            s -= M[i][j] * x[j]
        x[i] = s / M[i][i] if abs(M[i][i]) >= 1e-18 else 0.0
    return x


def fit_ols(X_list, y_list):
    """OLS with intercept (X already includes intercept column)."""
    rows = [(X, y) for X, y in zip(X_list, y_list)
            if X is not None and y is not None and y > 0
            and all(v is not None and math.isfinite(v) for v in X)
            and math.isfinite(y)]
    if len(rows) < 30:
        return None
    p = len(rows[0][0]) + 1  # +1 for intercept column
    XtX = [[0.0] * p for _ in range(p)]
    Xty = [0.0] * p
    for X, y in rows:
        ly = math.log(y + EPS) if y > 0 else None
        if ly is None or not math.isfinite(ly):
            continue
        xv = [1.0] + list(X)
        for i in range(p):
            Xty[i] += xv[i] * ly
            for j in range(p):
                XtX[i][j] += xv[i] * xv[j]
    for i in range(p):
        XtX[i][i] += 1e-8
    return _solve_linear(XtX, Xty)


def predict_ols(beta, X):
    if beta is None or X is None or any(v is None or not math.isfinite(v) for v in X):
        return None
    s = beta[0]
    for i in range(1, len(beta)):
        s += beta[i] * X[i - 1]
    if s > 700 or s < -700:
        return None
    return s


def safe_exp(yhat_log):
    if yhat_log is None:
        return None
    if yhat_log > 700 or yhat_log < -700:
        return None
    v = math.exp(yhat_log)
    return v if v > 0 else None


def fit_logistic(X_list, y_list, lr=0.1, n_iter=20000, l2=1e-4):
    """Logistic regression via gradient descent (intercept included in X)."""
    rows = [(X, y) for X, y in zip(X_list, y_list)
            if X is not None and y is not None
            and all(v is not None and math.isfinite(v) for v in X)
            and y in (0.0, 1.0)]
    if len(rows) < 30:
        return None
    p = len(rows[0][0])
    w = [0.0] * p
    for _ in range(n_iter):
        grad = [0.0] * p
        for X, y in rows:
            z = sum(wi * xi for wi, xi in zip(w, X))
            z = max(-60.0, min(60.0, z))
            pred = 1.0 / (1.0 + math.exp(-z))
            err = pred - y
            for i in range(p):
                grad[i] += err * X[i] + (l2 * w[i])
        step = lr / len(rows)
        any_change = False
        for i in range(p):
            w[i] -= step * grad[i]
            if abs(step * grad[i]) > 0:
                any_change = True
        if not any_change:
            break
    return w


def predict_logistic(w, X):
    if w is None or X is None or any(v is None or not math.isfinite(v) for v in X):
        return None
    z = sum(wi * xi for wi, xi in zip(w, X))
    z = max(-60.0, min(60.0, z))
    return 1.0 / (1.0 + math.exp(-z))


def feature_vec(row, model):
    rv24 = row["rv24h"]
    if pd.isna(rv24) or rv24 <= 0:
        return None
    base = [math.log(rv24 + EPS)]
    if model == "B1":
        return base
    vals = {"fundingRate": row["fundingRate"], "abs_fund_pct": row["abs_fund_pct"],
            "premium": row["premium"], "ema_dist": row["ema_dist"]}
    for v in vals.values():
        if v is None or pd.isna(v) or not math.isfinite(v):
            return None
    return base + [float(vals["fundingRate"]), float(vals["abs_fund_pct"]),
                   float(vals["premium"]), float(vals["ema_dist"])]


def build_daily(panel_path: Path) -> pd.DataFrame:
    df = pd.read_parquet(panel_path)
    df["timestamp"] = pd.to_datetime(df["timestamp"], utc=True)
    df = df[df["coin"].isin(COINS)].copy()
    df["day"] = df["timestamp"].dt.floor("D")
    daily = (df.groupby(["coin", "day"], as_index=False)
               .agg(y=("notional_usd", "sum"),
                    rv24h=("rv24h", "last"),
                    fundingRate=("fundingRate", "last"),
                    abs_fund_pct=("abs_fund_pct", "last"),
                    premium=("premium", "last"),
                    ema_dist=("ema_dist", "last")))
    daily = daily.sort_values(["coin", "day"]).reset_index(drop=True)
    daily["target"] = daily.groupby("coin")["y"].shift(-1)
    return daily[daily["target"].notna()].reset_index(drop=True)


def block_bootstrap_blockmeans(diffs_by_block: list[list[float]], seed: int, n_rep: int = N_BOOT):
    rng = random.Random(seed)
    stats = []
    for _ in range(n_rep):
        samp = []
        for _ in range(len(diffs_by_block)):
            samp.extend(rng.choice(diffs_by_block))
        if samp:
            stats.append(sum(samp) / len(samp))
    return np.array(stats, dtype=float)


def holm_adjust(p_values: list[float]) -> list[float]:
    order = sorted(range(len(p_values)), key=lambda i: p_values[i])
    adj = [0.0] * len(p_values)
    m = len(p_values)
    for rank, i in enumerate(order):
        adj[i] = min(1.0, p_values[i] * (m - rank))
    return adj


def summarize(metric: str, diffs: np.ndarray, mean_b1: float, mean_c2: float):
    n = len(diffs)
    mean_diff = float(diffs.mean()) if n > 0 else None
    boot = block_bootstrap_blockmeans([list(diffs)], SEED) if n > 0 else np.array([])
    if boot.size:
        ci_low = float(np.percentile(boot, 2.5))
        ci_high = float(np.percentile(boot, 97.5))
        p_value = float(2 * min((boot >= 0).mean(), (boot <= 0).mean()))
    else:
        ci_low = None
        ci_high = None
        p_value = 1.0
    ci_excludes_zero_better = bool(ci_high < 0) if ci_high is not None else False  # C2 strictly better
    rel_reduction = (float((mean_b1 - mean_c2) / mean_b1)) if (mean_b1 and mean_b1 > 0) else None
    materiality_met = bool(rel_reduction is not None and rel_reduction >= MATERIALITY_FLOOR)
    return {
        "metric": metric,
        "n_test_obs": int(n),
        "mean_b1": mean_b1,
        "mean_c2": mean_c2,
        "mean_diff_c2_minus_b1": mean_diff,
        "ci_low": ci_low,
        "ci_high": ci_high,
        "ci_excludes_zero_c2_better": ci_excludes_zero_better,
        "p_value": p_value,
        "relative_reduction_pct": (rel_reduction * 100.0) if rel_reduction is not None else None,
        "relative_reduction": rel_reduction,
        "materiality_floor_met": materiality_met,
        "improves": bool(mean_diff is not None and mean_diff < 0),
    }


def main() -> dict:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    actual_liq = sha256_file(PANEL_LIQ)
    assert actual_liq == PANEL_LIQ_SHA256, f"Liquidation panel hash mismatch: {actual_liq}"
    actual_fclr = sha256_file(PANEL_FCLR001)
    assert actual_fclr == PANEL_FCLR001_SHA256, f"FCLR-001 panel hash mismatch: {actual_fclr}"

    protocol = json.loads(PROTOCOL_PATH.read_text())
    assert protocol["outcome_data_inspected_before_freeze"] is False
    assert protocol["freeze_before_outcomes"] is True

    daily = build_daily(PANEL_LIQ)
    print(f"Coin-days with target: {len(daily)}, coins: {sorted(daily['coin'].unique().tolist())}", flush=True)

    train_start = pd.Timestamp("2025-03-22", tz="UTC")
    train_end = pd.Timestamp("2025-12-31", tz="UTC")
    test_blocks = [
        (pd.Timestamp("2026-04-01", tz="UTC"), pd.Timestamp("2026-05-31", tz="UTC")),
        (pd.Timestamp("2026-06-01", tz="UTC"), pd.Timestamp("2026-08-31", tz="UTC")),
        (pd.Timestamp("2026-09-01", tz="UTC"), pd.Timestamp("2026-10-31", tz="UTC")),
    ]

    train_df = daily[(daily["day"] >= train_start) & (daily["day"] <= train_end)].copy()
    train_median_y = float(train_df["y"].median())

    results = {"blocks": [], "metrics": {}, "verdict": None}
    all_diffs = {"QLIKE": [], "Brier": [], "LogLoss": []}

    for bi, (bs, be) in enumerate(test_blocks):
        cutoff = bs - pd.Timedelta(days=1)
        tr = daily[daily["day"] <= cutoff].copy()
        te = daily[(daily["day"] >= bs) & (daily["day"] <= be)].copy()
        te = te[te["target"].notna()].copy()
        # binary event from train median (ex-ante), applied to test
        te["event"] = (te["target"] > train_median_y).astype(float)

        blk = {"block": bi, "start": str(bs.date()), "end": str(be.date()),
               "cutoff": str(cutoff.date()), "n_train": int(len(tr)), "n_test": int(len(te)),
               "models": {}}
        for model in ("B1", "C2"):
            trX, try_ = [], []
            for _, r in tr.iterrows():
                xv = feature_vec(r, model)
                if xv is None:
                    continue
                trX.append(xv)
                try_.append(r["target"])
            beta = fit_ols(trX, try_)
            # logistic for binary event
            teX_list = [feature_vec(r, model) for _, r in te.iterrows()]
            ev_list = te["event"].tolist()
            w = fit_logistic([x for x in teX_list if x is not None],
                             [e for x, e in zip(teX_list, ev_list) if x is not None])
            qlike_vals, brier_vals, logloss_vals = [], [], []
            for _, r in te.iterrows():
                xv = feature_vec(r, model)
                if xv is None:
                    continue
                y = float(r["target"])
                yhat = predict_ols(beta, xv)
                yhat = safe_exp(yhat)
                q = qlike(y, yhat)
                if q is not None:
                    qlike_vals.append(q)
                e = float(r["event"])
                p = predict_logistic(w, xv)
                if p is not None:
                    brier_vals.append((p - e) ** 2)
                    p = max(EPS, min(1 - EPS, p))
                    logloss_vals.append(-(e * math.log(p) + (1 - e) * math.log(1 - p)))
            blk["models"][model] = {
                "n_test": int(len([1 for x in teX_list if x is not None])),
                "mean_qlike": (sum(qlike_vals) / len(qlike_vals)) if qlike_vals else None,
                "mean_brier": (sum(brier_vals) / len(brier_vals)) if brier_vals else None,
                "mean_logloss": (sum(logloss_vals) / len(logloss_vals)) if logloss_vals else None,
            }
        blk["event_rate"] = float(te["event"].mean())
        results["blocks"].append(blk)

        # pooled paired diffs per metric for this block
        for m in ("QLIKE", "Brier", "LogLoss"):
            diffs = []
            b1 = blk["models"]["B1"]
            c2 = blk["models"]["C2"]
            # reconstruct paired per-obs diffs via per-obs arrays stored below
            all_diffs[m].append(blk)

    # Build paired per-observation diffs across blocks
    per_obs = {"QLIKE": [], "Brier": [], "LogLoss": []}
    for bi, (bs, be) in enumerate(test_blocks):
        cutoff = bs - pd.Timedelta(days=1)
        tr = daily[daily["day"] <= cutoff].copy()
        te = daily[(daily["day"] >= bs) & (daily["day"] <= be)].copy()
        te = te[te["target"].notna()].copy()
        te["event"] = (te["target"] > train_median_y).astype(float)
        for model in ("B1", "C2"):
            trX, try_ = [], []
            for _, r in tr.iterrows():
                xv = feature_vec(r, model)
                if xv is None:
                    continue
                trX.append(xv)
                try_.append(r["target"])
            beta = fit_ols(trX, try_)
            teX_list = [feature_vec(r, model) for _, r in te.iterrows()]
            ev_list = te["event"].tolist()
            fit_rows = [(x, e) for x, e in zip(teX_list, ev_list) if x is not None]
            w = fit_logistic([x for x, _ in fit_rows], [e for _, e in fit_rows])
            obs = []
            for _, r in te.iterrows():
                xv = feature_vec(r, model)
                if xv is None:
                    continue
                y = float(r["target"])
                yhat = predict_ols(beta, xv)
                yhat = safe_exp(yhat)
                q = qlike(y, yhat)
                e = float(r["event"])
                p = predict_logistic(w, xv)
                brier = (p - e) ** 2 if p is not None else None
                p2 = max(EPS, min(1 - EPS, p)) if p is not None else None
                ll = (-(e * math.log(p2) + (1 - e) * math.log(1 - p2))) if p2 is not None else None
                obs.append({"q": q, "brier": brier, "ll": ll, "coin": r["coin"], "day": str(r["day"].date())})
            results["blocks"][bi]["models"][model]["obs"] = obs
        # pair by (coin, day)
        b1_obs = {(o["coin"], o["day"]): o for o in results["blocks"][bi]["models"]["B1"]["obs"]}
        c2_obs = results["blocks"][bi]["models"]["C2"]["obs"]
        for o in c2_obs:
            k = (o["coin"], o["day"])
            if k in b1_obs:
                b = b1_obs[k]
                if o["q"] is not None and b["q"] is not None:
                    per_obs["QLIKE"].append(o["q"] - b["q"])
                if o["brier"] is not None and b["brier"] is not None:
                    per_obs["Brier"].append(o["brier"] - b["brier"])
                if o["ll"] is not None and b["ll"] is not None:
                    per_obs["LogLoss"].append(o["ll"] - b["ll"])

    # Aggregate per-metric over all test blocks
    metric_summary = {}
    p_values = []
    metric_names = []
    for metric in ("QLIKE", "Brier", "LogLoss"):
        diffs = np.array(per_obs[metric], dtype=float)
        b1_vals = [o["q"] if metric == "QLIKE" else (o["brier"] if metric == "Brier" else o["ll"])
                   for blk in results["blocks"] for o in blk["models"]["B1"]["obs"]]
        c2_vals = [o["q"] if metric == "QLIKE" else (o["brier"] if metric == "Brier" else o["ll"])
                   for blk in results["blocks"] for o in blk["models"]["C2"]["obs"]]
        # pair again cleanly
        paired_b1, paired_c2 = [], []
        for blk in results["blocks"]:
            b1d = {(o["coin"], o["day"]): o for o in blk["models"]["B1"]["obs"]}
            for o in blk["models"]["C2"]["obs"]:
                k = (o["coin"], o["day"])
                if k in b1d:
                    v1 = b1d[k]["q"] if metric == "QLIKE" else (b1d[k]["brier"] if metric == "Brier" else b1d[k]["ll"])
                    v2 = o["q"] if metric == "QLIKE" else (o["brier"] if metric == "Brier" else o["ll"])
                    if v1 is not None and v2 is not None:
                        paired_b1.append(v1)
                        paired_c2.append(v2)
        mean_b1 = float(np.mean(paired_b1)) if paired_b1 else None
        mean_c2 = float(np.mean(paired_c2)) if paired_c2 else None
        diffs = np.array([c2 - b1 for c2, b1 in zip(paired_c2, paired_b1)], dtype=float)
        s = summarize(metric, diffs, mean_b1, mean_c2)
        s["holm_passes"] = None
        s["gate_pass"] = None
        metric_summary[metric] = s
        p_values.append(s["p_value"])
        metric_names.append(metric)

    holm = holm_adjust(p_values)
    gate_results = []
    all_pass = True
    for metric, adj_p, pval in zip(metric_names, holm, p_values):
        s = metric_summary[metric]
        s["p_value"] = float(pval)
        s["holm_adj_p"] = float(adj_p)
        s["holm_passes"] = bool(adj_p < ALPHA)
        gate_pass = bool(s["ci_excludes_zero_c2_better"] and s["holm_passes"] and s["materiality_floor_met"])
        s["gate_pass"] = gate_pass
        gate_results.append({"metric": metric, "gate_pass": gate_pass,
                             "ci_excludes_zero_c2_better": s["ci_excludes_zero_c2_better"],
                             "holm_passes": s["holm_passes"],
                             "materiality_floor_met": s["materiality_floor_met"],
                             "relative_reduction": s["relative_reduction"]})
        if not gate_pass:
            all_pass = False

    verdict = "SUPPORTED" if all_pass else "NOT_SUPPORTED"
    results["verdict"] = verdict
    results["metric_summary"] = metric_summary
    results["gate_results"] = gate_results
    results["all_metrics_pass"] = bool(all_pass)
    results["seed"] = SEED
    results["n_bootstrap"] = N_BOOT
    results["materiality_floor"] = MATERIALITY_FLOOR
    results["panel_sha256_liquidation"] = PANEL_LIQ_SHA256
    results["panel_sha256_fclr001"] = PANEL_FCLR001_SHA256
    results["outcome_data_inspected_before_freeze"] = False
    results["track"] = "observed_liquidation_intensity_only_not_modeled_breaches"

    # strip per-obs before json (too large); keep aggregates only
    for blk in results["blocks"]:
        for m in ("B1", "C2"):
            blk["models"][m].pop("obs", None)

    OUT_JSON.write_text(json.dumps(results, indent=2))
    print(f"VERDICT: {verdict}", flush=True)
    for g in gate_results:
        print(f"  {g['metric']}: gate_pass={g['gate_pass']} ci_excl0={g['ci_excludes_zero_c2_better']} holm={g['holm_passes']} mat={g['materiality_floor_met']} rel={g['relative_reduction']}", flush=True)
    _write_md(results)
    return results


def _write_md(results: dict) -> None:
    md = []
    md.append(f"# FCLR-LIQ-OOS-FORECAST-001 — OOS Liquidation-Risk Forecast Evaluation")
    md.append(f"**Campaign:** FCLR-LIQ-OOS-FORECAST-001-20261121T055825Z  |  Session: 20261121T055825Z")
    md.append(f"**Panel:** combined liquidation `fclr_liq_combined_panel_20261115T181405Z.parquet` sha256 `{PANEL_LIQ_SHA256}`")
    md.append(f"**Verdict:** `{results['verdict']}`  |  All metrics pass: {results['all_metrics_pass']}")
    md.append("")
    md.append("## Estimand")
    md.append("Out-of-sample forecast of next-24h observed notional-weighted liquidation intensity, C2 (funding-conditioned) vs B1 (RV-only), observed liquidations only (never modeled boundary breaches).")
    md.append("")
    md.append("## Splits (chronological expanding walk-forward)")
    md.append("- Train: 2025-03-22 -> 2025-12-31 | Validation: 2026-01-01 -> 2026-03-31 (diagnostic, no tuning)")
    md.append("- Test blocks: 2026-04-01..2026-05-31 ; 2026-06-01..2026-08-31 ; 2026-09-01..2026-10-31 | purge 1 day")
    md.append("")
    md.append("## Per-block summary")
    for blk in results["blocks"]:
        md.append(f"| block {blk['block']} | {blk['start']}..{blk['end']} | n_train={blk['n_train']} | n_test={blk['n_test']} | event_rate={blk['event_rate']:.3f} |")
        for m in ("B1", "C2"):
            mod = blk["models"][m]
            md.append(f"  | {m} | QLIKE={mod['mean_qlike']} | Brier={mod['mean_brier']} | LogLoss={mod['mean_logloss']} | n={mod['n_test']} |")
    md.append("")
    md.append("## Joint metric family (QLIKE / Brier / LogLoss) — block bootstrap + Holm, 2% floor")
    md.append("| metric | mean_B1 | mean_C2 | mean_diff(C2-B1) | CI_low | CI_high | CI_excl0_C2_better | p_value | Holm_adj_p | Holm_pass | rel_reduction | materiality>=2% | gate_pass |")
    for g in results["gate_results"]:
        s = results["metric_summary"][g["metric"]]
        md.append(f"| {g['metric']} | {s['mean_b1']} | {s['mean_c2']} | {s['mean_diff_c2_minus_b1']} | {s['ci_low']} | {s['ci_high']} | {s['ci_excludes_zero_c2_better']} | {s['p_value']} | {s['holm_adj_p']} | {s['holm_passes']} | {s['relative_reduction']} | {s['materiality_floor_met']} | {g['gate_pass']} |")
    md.append("")
    md.append(f"## Verdict: `{results['verdict']}`")
    md.append("SUPPORTED only if ALL three metrics clear every gate; otherwise honest NOT_SUPPORTED. No threshold-shopping or floor relaxation after seeing outcomes.")
    md.append("")
    md.append("## Cross-references: FCLR-XSEC-002/004/005/006/007/008; FCLR-LIQ-COMBINED-PANEL; Track B modeled breaches (NOT_MET); Track A combined panel (NOT_MET).")
    OUT_MD.write_text("\n".join(md))


if __name__ == "__main__":
    main()
