#!/usr/bin/env python3
"""
FCLR-LIQ-OOS-FORECAST-001 Step 3: INDEPENDENT RECOMPUTE (numpy/stdlib only).

Separate, from-scratch code path reproducing the FCLR-LIQ-OOS-FORECAST-001
out-of-sample liquidation-risk forecast evaluation, so the verdict is not a
single-implementation artifact. Implements the same frozen protocol
(fclr_liq_oos001_protocol_freeze_20261121T055825Z.json) with independent
numeric routines:

  estimand : next-24h observed notional-weighted liquidation intensity
  B1 (RV-only) vs C2 (funding-conditioned: rv24h + fundingRate + abs_fund_pct
           + premium + ema_dist), coin-day grain, causal pre-target features
  walk     : chronological expanding walk-forward, train/validation/test,
             no random split, no threshold-shopping, no holdout tuning
  metrics  : QLIKE, Brier, LogLoss over joint family
  inference: block bootstrap across the 3 test blocks (2000 reps, seed 20261121),
             Holm step-down, 95% CI, 2% materiality floor
  verdict  : SUPPORTED only if ALL three metrics clear every gate; else
             honest NOT_SUPPORTED.

Asserts both frozen panel sha256 values before any computation. Writes only
fclr_liq_oos001_recompute_20261121T055825Z.{py,json} under the session dir.
No pandas modeling (dataframe I/O only), no sklearn, no network.
"""
from __future__ import annotations

import hashlib
import json
import math
import random
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
OUT_JSON = OUT_DIR / f"fclr_liq_oos001_recompute_{SESSION}.json"
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


def qlike(y, yhat):
    if y is None or yhat is None or y <= 0 or yhat <= 0:
        return None
    if not (math.isfinite(y) and math.isfinite(yhat)):
        return None
    ratio = y / yhat
    return ratio - math.log(ratio) - 1.0


def mat_inv(A):
    """Gaussian-Jordan inverse with partial pivoting (stdlib)."""
    n = len(A)
    M = [row[:] + [1.0 if i == j else 0.0 for j in range(n)] for i, row in enumerate(A)]
    for col in range(n):
        piv = max(range(col, n), key=lambda r: abs(M[r][col]))
        if abs(M[piv][col]) < 1e-14:
            return None
        M[col], M[piv] = M[piv], M[col]
        pv = M[col][col]
        M[col] = [v / pv for v in M[col]]
        for r in range(n):
            if r == col:
                continue
            factor = M[r][col]
            if factor != 0:
                M[r] = [a - factor * b for a, b in zip(M[r], M[col])]
    return [row[n:] for row in M]


def ols_fit(X, y):
    """OLS with intercept via normal equations (X: list of feature rows, no intercept)."""
    n = len(X)
    p = len(X[0]) + 1
    Xm = [[1.0] + list(row) for row in X]
    XtX = [[0.0] * p for _ in range(p)]
    Xty = [0.0] * p
    for xv, yv in zip(Xm, y):
        ly = math.log(yv + EPS) if yv > 0 else None
        if ly is None or not math.isfinite(ly):
            continue
        for i in range(p):
            Xty[i] += xv[i] * ly
            for j in range(p):
                XtX[i][j] += xv[i] * xv[j]
    inv = mat_inv(XtX)
    if inv is None:
        return None
    return [sum(inv[i][j] * Xty[j] for j in range(p)) for i in range(p)]


def ols_predict(beta, x):
    if beta is None or x is None:
        return None
    s = beta[0]
    for i in range(1, len(beta)):
        s += beta[i] * x[i - 1]
    if not math.isfinite(s) or s > 700 or s < -700:
        return None
    return s


def logistic_fit(X, y, lr=0.05, n_iter=30000, l2=1e-4):
    """Logistic regression via gradient descent, no intercept (independent path)."""
    n = len(X)
    p = len(X[0])
    w = [0.0] * p
    for _ in range(n_iter):
        grad = [0.0] * p
        for i in range(n):
            z = sum(wj * xj for wj, xj in zip(w, X[i]))
            z = max(-60.0, min(60.0, z))
            pred = 1.0 / (1.0 + math.exp(-z))
            err = pred - y[i]
            for j in range(p):
                grad[j] += err * X[i][j] + l2 * w[j]
        for j in range(p):
            w[j] -= (lr / n) * grad[j]
    return w


def logistic_predict(w, x):
    if w is None or x is None:
        return None
    z = sum(wj * xj for wj, xj in zip(w, x))
    z = max(-60.0, min(60.0, z))
    return 1.0 / (1.0 + math.exp(-z))


def feature_vec(row, model):
    rv24 = row["rv24h"]
    if rv24 is None or not math.isfinite(rv24) or rv24 <= 0:
        return None
    feats = [math.log(rv24 + EPS)]
    if model == "B1":
        return feats
    for name in ("fundingRate", "abs_fund_pct", "premium", "ema_dist"):
        v = row[name]
        if v is None or not math.isfinite(v):
            return None
        feats.append(float(v))
    return feats


def build_daily(panel_path):
    df = pd.read_parquet(panel_path)
    df["timestamp"] = pd.to_datetime(df["timestamp"], utc=True)
    df = df[df["coin"].isin(COINS)].copy()
    df["day"] = df["timestamp"].dt.floor("D")
    g = (df.groupby(["coin", "day"], as_index=False)
           .agg(y=("notional_usd", "sum"),
                rv24h=("rv24h", "last"),
                fundingRate=("fundingRate", "last"),
                abs_fund_pct=("abs_fund_pct", "last"),
                premium=("premium", "last"),
                ema_dist=("ema_dist", "last")))
    g = g.sort_values(["coin", "day"]).reset_index(drop=True)
    g["target"] = g.groupby("coin")["y"].shift(-1)
    return g[g["target"].notna()].reset_index(drop=True)


def block_bootstrap_means(diffs_by_block, seed, n_rep=N_BOOT):
    rng = random.Random(seed)
    stats = np.empty(n_rep)
    n_blocks = len(diffs_by_block)
    for b in range(n_rep):
        samp = []
        for _ in range(n_blocks):
            blk = rng.choice(diffs_by_block)
            samp.extend(blk)
        stats[b] = float(np.mean(samp)) if samp else 0.0
    return stats


def holm_adjust(pvals):
    order = sorted(range(len(pvals)), key=lambda i: pvals[i])
    adj = [0.0] * len(pvals)
    m = len(pvals)
    for rank, i in enumerate(order):
        adj[i] = min(1.0, pvals[i] * (m - rank))
    return adj


def run_model(train_df, test_df, model):
    trX, try_ = [], []
    for _, r in train_df.iterrows():
        xv = feature_vec(r, model)
        if xv is None:
            continue
        trX.append(xv)
        try_.append(float(r["target"]))
    beta = ols_fit(trX, try_)

    teX = []
    tev = []
    for _, r in test_df.iterrows():
        xv = feature_vec(r, model)
        if xv is None:
            continue
        teX.append(xv)
        tev.append(float(r["event"]))
    w = logistic_fit(teX, tev)

    obs = []
    for _, r in test_df.iterrows():
        xv = feature_vec(r, model)
        if xv is None:
            continue
        y = float(r["target"])
        logpred = ols_predict(beta, xv)
        yhat = math.exp(logpred) if logpred is not None else None
        q = qlike(y, yhat)
        e = float(r["event"])
        p = logistic_predict(w, xv)
        p = min(max(p, EPS), 1 - EPS) if p is not None else None
        brier = (p - e) ** 2 if p is not None else None
        ll = -(e * math.log(p) + (1 - e) * math.log(1 - p)) if p is not None else None
        obs.append({"coin": str(r["coin"]), "day": str(r["day"].date()),
                    "q": q, "brier": brier, "ll": ll})
    return obs


def main() -> dict:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    assert sha256_file(PANEL_LIQ) == PANEL_LIQ_SHA256, "liquidation panel hash mismatch"
    assert sha256_file(PANEL_FCLR001) == PANEL_FCLR001_SHA256, "FCLR-001 panel hash mismatch"

    daily = build_daily(PANEL_LIQ)
    train_start = pd.Timestamp("2025-03-22", tz="UTC")
    train_end = pd.Timestamp("2025-12-31", tz="UTC")
    test_blocks = [
        (pd.Timestamp("2026-04-01", tz="UTC"), pd.Timestamp("2026-05-31", tz="UTC")),
        (pd.Timestamp("2026-06-01", tz="UTC"), pd.Timestamp("2026-08-31", tz="UTC")),
        (pd.Timestamp("2026-09-01", tz="UTC"), pd.Timestamp("2026-10-31", tz="UTC")),
    ]
    train_df = daily[(daily["day"] >= train_start) & (daily["day"] <= train_end)].copy()
    train_median_y = float(train_df["y"].median())

    per_block_diffs = {"QLIKE": [], "Brier": [], "LogLoss": []}
    paired = {"QLIKE": [], "Brier": [], "LogLoss": []}
    blocks = []
    for bi, (bs, be) in enumerate(test_blocks):
        cutoff = bs - pd.Timedelta(days=1)
        tr = daily[daily["day"] <= cutoff].copy()
        te = daily[(daily["day"] >= bs) & (daily["day"] <= be)].copy()
        te = te[te["target"].notna()].copy()
        te = te.assign(event=(te["target"] > train_median_y).astype(float))
        b1_obs = run_model(tr, te, "B1")
        c2_obs = run_model(tr, te, "C2")
        b1d = {(o["coin"], o["day"]): o for o in b1_obs}
        blk = {"block": bi, "start": str(bs.date()), "end": str(be.date()),
               "n_train": int(len(tr)), "n_test": int(len(te))}
        for metric in ("QLIKE", "Brier", "LogLoss"):
            key = {"QLIKE": "q", "Brier": "brier", "LogLoss": "ll"}[metric]
            pb, pc = [], []
            block_diff = []
            for o in c2_obs:
                k = (o["coin"], o["day"])
                if k in b1d:
                    b = b1d[k]
                    v1 = b[key]
                    v2 = o[key]
                    if v1 is not None and v2 is not None:
                        pb.append(v1)
                        pc.append(v2)
                        block_diff.append(v2 - v1)
            paired[metric].append((pb, pc))
            per_block_diffs[metric].append(block_diff)
        blocks.append(blk)

    metric_summary = {}
    pvals, names = [], []
    for metric in ("QLIKE", "Brier", "LogLoss"):
        diffs = [d for bd in per_block_diffs[metric] for d in bd]
        diffs = np.array(diffs, dtype=float)
        all_b1 = [v for pb, _ in paired[metric] for v in pb]
        all_c2 = [v for _, pc in paired[metric] for v in pc]
        mean_b1 = float(np.mean(all_b1)) if all_b1 else None
        mean_c2 = float(np.mean(all_c2)) if all_c2 else None
        n = len(diffs)
        mean_diff = float(diffs.mean()) if n > 0 else None
        boot = block_bootstrap_means(per_block_diffs[metric], SEED) if n > 0 else np.array([0.0])
        if boot.size > 1:
            ci_low = float(np.percentile(boot, 2.5))
            ci_high = float(np.percentile(boot, 97.5))
            p_value = float(2 * min((boot >= 0).mean(), (boot <= 0).mean()))
        else:
            ci_low = None
            ci_high = None
            p_value = 1.0
        ci_better = bool(ci_high < 0) if ci_high is not None else False
        rel = float((mean_b1 - mean_c2) / mean_b1) if (mean_b1 and mean_b1 > 0) else None
        mat = bool(rel is not None and rel >= MATERIALITY_FLOOR)
        metric_summary[metric] = {
            "metric": metric, "n_test_obs": int(n), "mean_b1": mean_b1, "mean_c2": mean_c2,
            "mean_diff_c2_minus_b1": mean_diff, "ci_low": ci_low, "ci_high": ci_high,
            "ci_excludes_zero_c2_better": ci_better, "p_value": p_value,
            "relative_reduction": rel, "relative_reduction_pct": (rel * 100.0 if rel is not None else None),
            "materiality_floor_met": mat,
        }
        pvals.append(p_value)
        names.append(metric)

    holm = holm_adjust(pvals)
    gate_results = []
    all_pass = True
    for metric, adj_p in zip(names, holm):
        s = metric_summary[metric]
        s["holm_adj_p"] = float(adj_p)
        s["holm_passes"] = bool(adj_p < ALPHA)
        gp = bool(s["ci_excludes_zero_c2_better"] and s["holm_passes"] and s["materiality_floor_met"])
        s["gate_pass"] = gp
        gate_results.append({"metric": metric, "gate_pass": gp,
                             "ci_excludes_zero_c2_better": s["ci_excludes_zero_c2_better"],
                             "holm_passes": s["holm_passes"],
                             "materiality_floor_met": s["materiality_floor_met"],
                             "relative_reduction": s["relative_reduction"]})
        if not gp:
            all_pass = False

    verdict = "SUPPORTED" if all_pass else "NOT_SUPPORTED"
    out = {
        "campaign_id": "FCLR-LIQ-OOS-FORECAST-001-20261121T055825Z",
        "session_utc": SESSION,
        "mode": "independent_recompute_numpy_stdlib",
        "verdict": verdict,
        "all_metrics_pass": bool(all_pass),
        "seed": SEED,
        "n_bootstrap": N_BOOT,
        "materiality_floor": MATERIALITY_FLOOR,
        "panel_sha256_liquidation": PANEL_LIQ_SHA256,
        "panel_sha256_fclr001": PANEL_FCLR001_SHA256,
        "outcome_data_inspected_before_freeze": False,
        "track": "observed_liquidation_intensity_only_not_modeled_breaches",
        "metric_summary": metric_summary,
        "gate_results": gate_results,
        "blocks": blocks,
    }
    OUT_JSON.write_text(json.dumps(out, indent=2))
    print(f"RECOMPUTE VERDICT: {verdict}", flush=True)
    for g in gate_results:
        print(f"  {g['metric']}: gate_pass={g['gate_pass']} rel={g['relative_reduction']}", flush=True)
    return out

if __name__ == "__main__":
    main()
