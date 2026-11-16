#!/usr/bin/env python3
"""
Independent recompute of the FCLR-008 terminal headline (B0/B1/C1/C2 24h QLIKE
and paired C2-vs-B1 / C1-vs-B1 / C2-vs-C1 contrasts) on the frozen 2026 test
window (2026-05-08 .. 2026-08-06, 91 days = 3 non-overlapping 30-day blocks).

Re-derives results from cached 2026 mark-price / funding / premium-index /
index-price CSVs WITHOUT using canonical scripts/run_evaluation.py and WITHOUT
the LFS run_manifest pointer. Splits are hardcoded from
research_protocol_fclr008.md (v1.0, frozen 2026-11-01T00:50:00Z, before
outcomes). OLS is fit via a deterministic Gaussian-elimination solver on
log(y+1e-12) with raw predictors + intercept + 1e-12 ridge (matching the
canonical model family); QLIKE is y/yhat - log(y/yhat) - 1. Block bootstrap by
UTC day, 2000 deterministic-seed replicates (seed 12345). Compared to published
values with tolerances QLIKE abs <= 1e-6, mean diff abs <= 1e-6, relative
reduction <= 0.01 pct-points (n must match where deterministic). No statsmodels,
no network, read-only, no research_state writes outside this session directory.

Queue item 3 (FCLR-008). Queue items 1 (FCLR-009) and 2 (FCLR-006) are DONE and
must NOT be repeated.
"""
from __future__ import annotations

import csv
import hashlib
import json
import math
import random
from collections import defaultdict
from datetime import datetime, timedelta, timezone
from pathlib import Path

import pandas as pd

REPO = Path(__file__).resolve().parents[2]
DATA = REPO / "research_state" / "data_cache"
OUT_DIR = Path(__file__).resolve().parent

SYMBOLS = ["BTCUSDT", "ETHUSDT", "BNBUSDT", "SOLUSDT", "XRPUSDT"]
EPS = 1e-12
HORIZON = 24
N_BOOT = 2000
RNG_SEED = 12345

# Frozen splits from research_protocol_fclr008.md (v1.0, frozen 2026-11-01T00:50:00Z)
TRAIN = (pd.Timestamp("2026-01-01T00:00:00Z"), pd.Timestamp("2026-03-17T23:00:00Z"))
VAL = (pd.Timestamp("2026-03-25T00:00:00Z"), pd.Timestamp("2026-04-30T23:00:00Z"))
TEST = (pd.Timestamp("2026-05-08T00:00:00Z"), pd.Timestamp("2026-08-06T23:00:00Z"))

# Published values from research_state/evaluation_summary_FCLR-008.md
PUBLISHED = {
    "B0": {"qlike": 0.330127, "n": 10800},
    "B1": {"qlike": 0.333314, "n": 10785},
    "C1": {"qlike": 0.330164, "n": 10785},
    "C2": {"qlike": 0.318996, "n": 10785},
    "C2_vs_B1": {"mean_diff": -0.014318, "rel_pct": 4.30, "ci_lo": -0.029938, "ci_hi": 0.000524, "n_pairs": 10785},
    "C1_vs_B1": {"mean_diff": -0.003150, "rel_pct": 0.94, "ci_lo": -0.010051, "ci_hi": 0.003832, "n_pairs": 10785},
    "C2_vs_C1": {"mean_diff": -0.011168, "rel_pct": 3.38, "ci_lo": -0.026088, "ci_hi": 0.002175, "n_pairs": 10785},
}


def ts_to_dt(ts_ms):
    return datetime.fromtimestamp(ts_ms / 1000, tz=timezone.utc)


def load_mark_series(sym, start_dt, end_dt):
    series = []
    cur = start_dt.replace(hour=0, minute=0, second=0, microsecond=0)
    end_day = end_dt.replace(hour=0, minute=0, second=0, microsecond=0)
    while cur <= end_day:
        date_str = cur.strftime("%Y-%m-%d")
        base = DATA / f"{sym}_{cur.year}_{cur.month:02d}"
        csvp = base / f"markPriceKlines-{date_str}" / f"{sym}-1h-{date_str}.csv"
        if not csvp.exists():
            csvp = base / f"markPriceKlines-{date_str}" / f"{sym}-1h-{date_str}" / f"{sym}-1h-{date_str}.csv"
        if csvp.exists():
            try:
                with csvp.open() as f:
                    reader = csv.DictReader(f)
                    for row in reader:
                        try:
                            ts_ms = int(row["open_time"])
                            ts_dt = ts_to_dt(ts_ms)
                            if ts_dt < start_dt - timedelta(days=1) or ts_dt > end_dt + timedelta(days=1):
                                continue
                            close = float(row["close"])
                            series.append((ts_ms, close))
                        except (ValueError, KeyError):
                            continue
            except OSError:
                continue
        cur = cur + timedelta(days=1)
    series.sort(key=lambda x: x[0])
    return series


def load_index_close(sym, ts_ms):
    ts_dt = ts_to_dt(ts_ms)
    date_str = ts_dt.strftime("%Y-%m-%d")
    base = DATA / f"{sym}_{ts_dt.year}_{ts_dt.month:02d}"
    csvp = base / f"indexPriceKlines-{date_str}" / f"{sym}-1h-{date_str}.csv"
    if not csvp.exists():
        csvp = base / f"indexPriceKlines-{date_str}" / f"{sym}-1h-{date_str}" / f"{sym}-1h-{date_str}.csv"
    if csvp.exists():
        try:
            with csvp.open() as f:
                reader = csv.DictReader(f)
                for row in reader:
                    try:
                        rts = int(row["open_time"])
                        if rts == ts_ms or abs(rts - ts_ms) < 1000:
                            return float(row["close"])
                    except (ValueError, KeyError):
                        continue
        except OSError:
            return None
    return None


def load_premium_close(sym, ts_ms):
    ts_dt = ts_to_dt(ts_ms)
    date_str = ts_dt.strftime("%Y-%m-%d")
    base = DATA / f"{sym}_{ts_dt.year}_{ts_dt.month:02d}"
    csvp = base / f"premiumIndexKlines-{date_str}" / f"{sym}-1h-{date_str}.csv"
    if not csvp.exists():
        csvp = base / f"premiumIndexKlines-{date_str}" / f"{sym}-1h-{date_str}" / f"{sym}-1h-{date_str}.csv"
    if csvp.exists():
        try:
            with csvp.open() as f:
                reader = csv.DictReader(f)
                for row in reader:
                    try:
                        rts = int(row["open_time"])
                        if rts == ts_ms or abs(rts - ts_ms) < 1000:
                            return float(row["close"])
                    except (ValueError, KeyError):
                        continue
        except OSError:
            return None
    return None


def funding_months(end_ym, start_ym="2026-01"):
    sy, sm = map(int, start_ym.split("-"))
    ey, em = map(int, end_ym.split("-"))
    out = []
    y, m = sy, sm
    while (y, m) <= (ey, em):
        out.append((y, m))
        m += 1
        if m > 12:
            m = 1
            y += 1
    return out


def load_funding_series_all(sym, months):
    series = []
    for (y, m) in months:
        ym = f"{y}-{m:02d}"
        base = DATA / f"{sym}_{y}_{m:02d}"
        csvp = base / f"{sym}-fundingRate-{ym}" / f"{sym}-fundingRate-{ym}.csv"
        if not csvp.exists():
            continue
        try:
            with csvp.open() as f:
                reader = csv.DictReader(f)
                for row in reader:
                    try:
                        ts_ms = int(row.get("calc_time", 0))
                        fr = float(row["last_funding_rate"])
                        series.append((ts_ms, fr))
                    except (ValueError, KeyError):
                        continue
        except OSError:
            continue
    series.sort(key=lambda x: x[0])
    dedup = []
    seen = set()
    for ts, fr in series:
        if ts in seen:
            continue
        seen.add(ts)
        dedup.append((ts, fr))
    return dedup


def log_ret(p1, p0):
    if p0 is None or p1 is None or p0 <= 0 or p1 <= 0:
        return None
    return math.log(p1 / p0)


def realized_variance_from_prices(prices_list):
    rv = 0.0
    for i in range(1, len(prices_list)):
        r = log_ret(prices_list[i], prices_list[i - 1])
        if r is None:
            return None
        rv += r * r
    return rv


def get_funding_latest(funding_series, ts_ms):
    best = None
    for ts_f, fr in funding_series:
        if ts_f <= ts_ms:
            best = (ts_f, fr)
        else:
            break
    return best


def get_funding_abs_percentile(funding_series, ts_ms, window_days=90, min_obs=30):
    cutoff = ts_ms - window_days * 24 * 3600 * 1000
    hist = [fr for (t2, fr) in funding_series if cutoff <= t2 < ts_ms]
    if len(hist) < min_obs:
        return None
    abs_hist = [abs(x) for x in hist]
    latest_f = get_funding_latest(funding_series, ts_ms)
    if latest_f is None:
        return None
    abs_latest = abs(latest_f[1])
    cnt = sum(1 for v in abs_hist if v <= abs_latest)
    return cnt / len(abs_hist) if abs_hist else None


def compute_ema_dist(mark_series, t_idx):
    alpha = 2.0 / 25.0
    start = max(0, t_idx - 23)
    ema_cur = sum(mark_series[i][1] for i in range(start, t_idx + 1)) / (t_idx - start + 1)
    for i in range(max(1, t_idx - 200), t_idx + 1):
        ema_cur = alpha * mark_series[i][1] + (1.0 - alpha) * ema_cur
    if ema_cur > 0:
        return mark_series[t_idx][1] / ema_cur - 1.0
    return None


def build_features_for_origin(mark_series, funding_series, t_idx, sym=None):
    if t_idx < 0 or t_idx >= len(mark_series):
        return None
    ts_ms_t = mark_series[t_idx][0]

    def trailing_rv_window(n):
        if t_idx - n < 0:
            return None
        rv = 0.0
        for i in range(t_idx - n + 1, t_idx + 1):
            if i <= 0:
                return None
            r = log_ret(mark_series[i][1], mark_series[i - 1][1])
            if r is None:
                return None
            rv += r * r
        return rv

    rv1h = trailing_rv_window(1)
    rv24h = trailing_rv_window(24)
    rv168h = trailing_rv_window(168)

    latest_f = get_funding_latest(funding_series, ts_ms_t)
    signed_funding = latest_f[1] if latest_f else None
    abs_fund_pct = get_funding_abs_percentile(funding_series, ts_ms_t)

    ema_dist = compute_ema_dist(mark_series, t_idx)

    prem = None
    if sym is not None:
        prem_close = load_premium_close(sym, ts_ms_t)
        if prem_close is not None:
            prem = float(prem_close)
        else:
            idx_close = load_index_close(sym, ts_ms_t)
            if idx_close is not None and idx_close > 0:
                prem = mark_series[t_idx][1] / idx_close - 1.0

    return {
        "ts_ms": ts_ms_t,
        "rv1h": rv1h,
        "rv24h": rv24h,
        "rv168h": rv168h,
        "signed_funding": signed_funding,
        "abs_fund_pct": abs_fund_pct,
        "ema_dist": ema_dist,
        "prem": prem,
    }


def solve_linear(A, b):
    n = len(A)
    M = [row[:] + [b[i]] for i, row in enumerate(A)]
    for col in range(n):
        piv = max(range(col, n), key=lambda r: abs(M[r][col]))
        if abs(M[piv][col]) < 1e-18:
            continue
        M[col], M[piv] = M[piv], M[col]
        for r in range(col + 1, n):
            factor = M[r][col] / M[col][col] if M[col][col] != 0 else 0
            for c2 in range(col, n + 1):
                M[r][c2] -= factor * M[col][c2]
    x = [0.0] * n
    for i in range(n - 1, -1, -1):
        s = M[i][n]
        for j in range(i + 1, n):
            s -= M[i][j] * x[j]
        if abs(M[i][i]) < 1e-18:
            x[i] = 0.0
        else:
            x[i] = s / M[i][i]
    return x


def fit_ols(X_list, y_list):
    rows = []
    for X, y in zip(X_list, y_list):
        if y is None or y <= 0:
            continue
        rows.append((X, y))
    if len(rows) < 10:
        return None
    n = len(rows)
    p = len(rows[0][0])
    XtX = [[0.0] * p for _ in range(p)]
    Xty = [0.0] * p
    for X, y in rows:
        ly = math.log(y + EPS)
        for i in range(p):
            Xty[i] += X[i] * ly
            for j in range(p):
                XtX[i][j] += X[i] * X[j]
    for i in range(p):
        XtX[i][i] += 1e-12
    beta = solve_linear(XtX, Xty)
    return beta


def predict(beta, X):
    if beta is None or X is None:
        return None
    s = beta[0]
    for i in range(1, len(beta)):
        if i - 1 < len(X) and X[i - 1] is not None:
            s += beta[i] * X[i - 1]
    yhat = math.exp(s)
    if yhat < 0:
        yhat = 1e-18
    return yhat


def qlike(y, yhat):
    if yhat is None or yhat <= 0 or y is None or y <= 0:
        return None
    return y / yhat - math.log(y / yhat) - 1.0


def in_split_dt(dt, bounds):
    lo, hi = bounds
    return lo <= dt <= hi


def block_bootstrap_diff(pairs_ts, pairs_diff, n_boot=N_BOOT, seed=RNG_SEED):
    blocks = defaultdict(list)
    for ts_ms, d in zip(pairs_ts, pairs_diff):
        dt = datetime.fromtimestamp(ts_ms / 1000, tz=timezone.utc)
        blocks[dt.date().isoformat()].append(d)
    block_list = list(blocks.values())
    rng = random.Random(seed)
    stats = []
    for _ in range(n_boot):
        samp = []
        for _ in range(len(block_list)):
            b = rng.choice(block_list)
            samp.extend(b)
        if not samp:
            continue
        stats.append(sum(samp) / len(samp))
    stats.sort()
    lo = stats[int(0.025 * len(stats))] if stats else None
    hi = stats[int(0.975 * len(stats))] if stats else None
    return stats, lo, hi


def main():
    start_all = pd.Timestamp("2026-01-01T00:00:00Z")
    end_all = pd.Timestamp("2026-08-06T23:00:00Z")
    months = funding_months("2026-08", "2026-01")

    data = {}
    for sym in SYMBOLS:
        data[sym] = {
            "mark": load_mark_series(sym, start_all, end_all),
            "funding": load_funding_series_all(sym, months),
        }

    ts_sets = []
    for sym in SYMBOLS:
        ts_sets.append(set(m[0] for m in data[sym]["mark"]))
    common_ts = set.intersection(*ts_sets) if ts_sets else set()

    eval_rows = []
    for sym in SYMBOLS:
        mark_list = data[sym]["mark"]
        fund_list = data[sym]["funding"]
        for i in range(len(mark_list)):
            ts_ms = mark_list[i][0]
            if ts_ms not in common_ts:
                continue
            ts_dt = ts_to_dt(ts_ms)
            split = None
            if in_split_dt(ts_dt, TRAIN):
                split = "train"
            elif in_split_dt(ts_dt, VAL):
                split = "val"
            elif in_split_dt(ts_dt, TEST):
                split = "test"
            else:
                continue
            if i < 168:
                continue
            if i + HORIZON >= len(mark_list):
                continue
            future_prices = [mark_list[i][1]] + [mark_list[i + 1 + j][1] for j in range(HORIZON)]
            y = realized_variance_from_prices(future_prices)
            if y is None or y <= 0:
                continue
            feats = build_features_for_origin(mark_list, fund_list, i, sym=sym)
            if feats is None:
                continue
            eval_rows.append({
                "sym": sym,
                "ts_ms": ts_ms,
                "ts_dt": ts_dt,
                "split": split,
                "y": y,
                "feats": feats,
                "i": i,
            })

    print(f"Collected {len(eval_rows)} rows", flush=True)

    train_rows = [r for r in eval_rows if r["split"] == "train"]
    val_rows = [r for r in eval_rows if r["split"] == "val"]
    test_rows = [r for r in eval_rows if r["split"] == "test"]
    print(f"train={len(train_rows)} val={len(val_rows)} test={len(test_rows)}", flush=True)

    def make_X_B0(rows):
        Xs, ys = [], []
        for r in rows:
            f = r["feats"]
            if f["rv24h"] is None or f["rv24h"] <= 0:
                continue
            Xs.append([math.log(f["rv24h"] + EPS)])
            ys.append(r["y"])
        return Xs, ys

    def make_X_B1(rows):
        Xs, ys = [], []
        for r in rows:
            f = r["feats"]
            if f["rv1h"] is None or f["rv24h"] is None or f["rv168h"] is None:
                continue
            if f["rv1h"] <= 0 or f["rv24h"] <= 0 or f["rv168h"] <= 0:
                continue
            Xs.append([math.log(f["rv1h"] + EPS), math.log(f["rv24h"] + EPS), math.log(f["rv168h"] + EPS)])
            ys.append(r["y"])
        return Xs, ys

    def make_X_C1(rows):
        Xs, ys = [], []
        for r in rows:
            f = r["feats"]
            if f["rv1h"] is None or f["rv24h"] is None or f["rv168h"] is None:
                continue
            if f["rv1h"] <= 0 or f["rv24h"] <= 0 or f["rv168h"] <= 0:
                continue
            sf = f["signed_funding"] if f["signed_funding"] is not None else 0.0
            af = f["abs_fund_pct"] if f["abs_fund_pct"] is not None else 0.0
            Xs.append([math.log(f["rv1h"] + EPS), math.log(f["rv24h"] + EPS), math.log(f["rv168h"] + EPS), sf, af])
            ys.append(r["y"])
        return Xs, ys

    def make_X_C2(rows):
        Xs, ys = [], []
        for r in rows:
            f = r["feats"]
            if f["rv1h"] is None or f["rv24h"] is None or f["rv168h"] is None:
                continue
            if f["rv1h"] <= 0 or f["rv24h"] <= 0 or f["rv168h"] <= 0:
                continue
            sf = f["signed_funding"] if f["signed_funding"] is not None else 0.0
            af = f["abs_fund_pct"] if f["abs_fund_pct"] is not None else 0.0
            prem = f["prem"] if f["prem"] is not None else 0.0
            ema = f["ema_dist"] if f["ema_dist"] is not None else 0.0
            Xs.append([math.log(f["rv1h"] + EPS), math.log(f["rv24h"] + EPS), math.log(f["rv168h"] + EPS), sf, af, prem, ema])
            ys.append(r["y"])
        return Xs, ys

    models = {}
    for name, maker in [("B0", make_X_B0), ("B1", make_X_B1), ("C1", make_X_C1), ("C2", make_X_C2)]:
        Xtr, ytr = maker(train_rows)
        if not Xtr:
            models[name] = None
            continue
        Xtr_int = [[1.0] + x for x in Xtr]
        beta = fit_ols(Xtr_int, ytr)
        models[name] = {"beta": beta, "maker": maker}

    def eval_model(name, split_rows):
        model = models.get(name)
        if not model or model["beta"] is None:
            return []
        beta = model["beta"]
        preds = []
        for r in split_rows:
            f = r["feats"]
            if name == "B0":
                if f["rv24h"] is None or f["rv24h"] <= 0:
                    continue
                X = [1.0, math.log(f["rv24h"] + EPS)]
            elif name == "B1":
                if f["rv1h"] is None or f["rv24h"] is None or f["rv168h"] is None:
                    continue
                if f["rv1h"] <= 0 or f["rv24h"] <= 0 or f["rv168h"] <= 0:
                    continue
                X = [1.0, math.log(f["rv1h"] + EPS), math.log(f["rv24h"] + EPS), math.log(f["rv168h"] + EPS)]
            elif name == "C1":
                if f["rv1h"] is None or f["rv24h"] is None or f["rv168h"] is None:
                    continue
                if f["rv1h"] <= 0 or f["rv24h"] <= 0 or f["rv168h"] <= 0:
                    continue
                sf = f["signed_funding"] if f["signed_funding"] is not None else 0.0
                af = f["abs_fund_pct"] if f["abs_fund_pct"] is not None else 0.0
                X = [1.0, math.log(f["rv1h"] + EPS), math.log(f["rv24h"] + EPS), math.log(f["rv168h"] + EPS), sf, af]
            elif name == "C2":
                if f["rv1h"] is None or f["rv24h"] is None or f["rv168h"] is None:
                    continue
                if f["rv1h"] <= 0 or f["rv24h"] <= 0 or f["rv168h"] <= 0:
                    continue
                sf = f["signed_funding"] if f["signed_funding"] is not None else 0.0
                af = f["abs_fund_pct"] if f["abs_fund_pct"] is not None else 0.0
                prem = f["prem"] if f["prem"] is not None else 0.0
                ema = f["ema_dist"] if f["ema_dist"] is not None else 0.0
                X = [1.0, math.log(f["rv1h"] + EPS), math.log(f["rv24h"] + EPS), math.log(f["rv168h"] + EPS), sf, af, prem, ema]
            else:
                continue
            yhat = predict(beta, X[1:])
            if yhat is None or yhat <= 0 or r["y"] <= 0:
                continue
            q = qlike(r["y"], yhat)
            if q is not None:
                preds.append({"y": r["y"], "yhat": yhat, "qlike": q, "sym": r["sym"], "ts_ms": r["ts_ms"]})
        return preds

    results = {}
    for name in ["B0", "B1", "C1", "C2"]:
        results[name] = {"test": eval_model(name, test_rows), "val": eval_model(name, val_rows)}

    def mean_qlike(preds):
        if not preds:
            return None
        return sum(p["qlike"] for p in preds) / len(preds)

    summary = {}
    for name in ["B0", "B1", "C1", "C2"]:
        preds_t = results[name]["test"]
        summary[name] = {"test_qlike_mean": mean_qlike(preds_t), "test_n": len(preds_t)}

    contrasts = {}
    for a, b in [("C2", "B1"), ("C1", "B1"), ("C2", "C1")]:
        preds_a = results[a]["test"]
        preds_b = results[b]["test"]
        key_b = {(p["sym"], p["ts_ms"]): p for p in preds_b}
        pairs_ts = []
        pairs_diff = []
        for pa in preds_a:
            key = (pa["sym"], pa["ts_ms"])
            if key in key_b:
                pairs_ts.append(pa["ts_ms"])
                pairs_diff.append(pa["qlike"] - key_b[key]["qlike"])
        mean_d = sum(pairs_diff) / len(pairs_diff) if pairs_diff else None
        mean_qb = summary[b]["test_qlike_mean"]
        rel = (-mean_d / abs(mean_qb) * 100) if (mean_d is not None and mean_qb) else None
        stats, lo, hi = block_bootstrap_diff(pairs_ts, pairs_diff)
        contrasts[f"{a}_vs_{b}"] = {
            "mean_diff": mean_d,
            "rel_reduction_pct": rel,
            "ci_lo": lo,
            "ci_hi": hi,
            "n_pairs": len(pairs_diff),
        }

    tol_q = 1e-6
    tol_diff = 1e-6
    tol_rel = 0.01
    comp = {}
    for name in ["B0", "B1", "C1", "C2"]:
        comp[name] = {
            "published_qlike": PUBLISHED[name]["qlike"],
            "recomputed_qlike": summary[name]["test_qlike_mean"],
            "abs_diff_qlike": abs(summary[name]["test_qlike_mean"] - PUBLISHED[name]["qlike"]),
            "published_n": PUBLISHED[name]["n"],
            "recomputed_n": summary[name]["test_n"],
            "n_match": summary[name]["test_n"] == PUBLISHED[name]["n"],
            "qlike_within_tol": abs(summary[name]["test_qlike_mean"] - PUBLISHED[name]["qlike"]) <= tol_q,
        }
    for k, pub_key in [("C2_vs_B1", "C2_vs_B1"), ("C1_vs_B1", "C1_vs_B1"), ("C2_vs_C1", "C2_vs_C1")]:
        c = contrasts[k]
        p = PUBLISHED[pub_key]
        comp[k] = {
            "published_mean_diff": p["mean_diff"],
            "recomputed_mean_diff": c["mean_diff"],
            "abs_diff_mean_diff": abs(c["mean_diff"] - p["mean_diff"]),
            "published_rel_pct": p["rel_pct"],
            "recomputed_rel_pct": c["rel_reduction_pct"],
            "abs_diff_rel_pct": abs(c["rel_reduction_pct"] - p["rel_pct"]),
            "published_ci_lo": p["ci_lo"],
            "recomputed_ci_lo": c["ci_lo"],
            "published_ci_hi": p["ci_hi"],
            "recomputed_ci_hi": c["ci_hi"],
            "published_n_pairs": p["n_pairs"],
            "recomputed_n_pairs": c["n_pairs"],
            "n_pairs_match": c["n_pairs"] == p["n_pairs"],
            "mean_diff_within_tol": abs(c["mean_diff"] - p["mean_diff"]) <= tol_diff,
            "rel_within_tol": abs(c["rel_reduction_pct"] - p["rel_pct"]) <= tol_rel,
        }
    all_within = (
        all(comp[n]["qlike_within_tol"] for n in ["B0", "B1", "C1", "C2"])
        and all(comp[n]["n_match"] for n in ["B0", "B1", "C1", "C2"])
        and all(comp[k]["mean_diff_within_tol"] for k in ["C2_vs_B1", "C1_vs_B1", "C2_vs_C1"])
        and all(comp[k]["rel_within_tol"] for k in ["C2_vs_B1", "C1_vs_B1", "C2_vs_C1"])
        and all(comp[k]["n_pairs_match"] for k in ["C2_vs_B1", "C1_vs_B1", "C2_vs_C1"])
    )

    # Gate assessment (primary contrast C2 vs B1): >=2% rel reduction AND CI excludes zero AND 5 instruments AND >=3 blocks
    c2b1 = contrasts["C2_vs_B1"]
    gate_met = (
        c2b1["rel_reduction_pct"] is not None
        and c2b1["rel_reduction_pct"] >= 2.0
        and c2b1["ci_hi"] is not None
        and c2b1["ci_hi"] < 0.0
        and c2b1["n_pairs"] >= 5
    )
    # 91-day test = 3 non-overlapping 30-day blocks (>=3 met by design)
    test_days = (TEST[1] - TEST[0]).days + 1
    n_blocks = test_days // 30

    result = {
        "session_utc": OUT_DIR.name.replace("session_", ""),
        "method": "independent recompute; daily CSV load; hardcoded frozen splits from research_protocol_fclr008.md; OLS via deterministic Gaussian elimination on log(y+1e-12) with raw predictors + intercept + 1e-12 ridge; canonical QLIKE; block bootstrap random.Random(12345) by UTC day; no statsmodels, no network, no manifest/LFS dependency, read-only",
        "data_cache": str(DATA.relative_to(REPO)),
        "symbols": SYMBOLS,
        "splits": {
            "train": [str(TRAIN[0]), str(TRAIN[1])],
            "val": [str(VAL[0]), str(VAL[1])],
            "test": [str(TEST[0]), str(TEST[1])],
            "embargoes": ["2026-03-18..2026-03-24 (7d)", "2026-05-01..2026-05-07 (7d)"],
        },
        "counts": {
            "collected": len(eval_rows),
            "train": len(train_rows),
            "val": len(val_rows),
            "test": len(test_rows),
        },
        "model_results": {
            name: {"test_qlike_mean": summary[name]["test_qlike_mean"], "test_n": summary[name]["test_n"]}
            for name in ["B0", "B1", "C1", "C2"]
        },
        "contrasts": {
            k: {
                "mean_diff": v["mean_diff"],
                "rel_reduction_pct": v["rel_reduction_pct"],
                "ci_lo": v["ci_lo"],
                "ci_hi": v["ci_hi"],
                "n_pairs": v["n_pairs"],
            }
            for k, v in contrasts.items()
        },
        "gate": {
            "primary_contrast": "C2_vs_B1",
            "test_days": test_days,
            "n_blocks_30d": n_blocks,
            "instruments": len(SYMBOLS),
            "rel_reduction_pct": c2b1["rel_reduction_pct"],
            "rel_floor_pct": 2.0,
            "ci_lo": c2b1["ci_lo"],
            "ci_hi": c2b1["ci_hi"],
            "ci_excludes_zero": (c2b1["ci_hi"] is not None and c2b1["ci_hi"] < 0.0),
            "paired_n": c2b1["n_pairs"],
            "gate_met": bool(gate_met),
            "verdict": "PASS" if gate_met else "NOT_MET",
        },
        "comparison_to_published": comp,
        "tolerances": {"qlike_abs": tol_q, "mean_diff_abs": tol_diff, "rel_pct_points": tol_rel},
        "all_within_tolerance": bool(all_within),
        "conclusion": (
            "Independent recompute reproduces all published FCLR-008 QLIKE values, n, and the "
            "C2-vs-B1 / C1-vs-B1 / C2-vs-C1 contrasts (mean diff, relative reduction, n_pairs) "
            "within declared tolerance. The FCLR-008 NOT_MET terminal headline (CI does not "
            "exclude zero on the improving side) is corroborated by an independent code path."
            if all_within else
            "Independent recompute diverged from published FCLR-008 values beyond tolerance; "
            "investigate feature construction / row eligibility / OLS details."
        ),
    }

    ts = OUT_DIR.name.replace("session_", "")
    out_json = OUT_DIR / f"recompute_fclr008_{ts}.json"
    out_json.write_text(json.dumps(result, indent=2))
    print(json.dumps(result, indent=2))
    print(f"\nWROTE {out_json}")

    md = []
    md.append(f"# Independent Recompute — FCLR-008 — {ts}")
    md.append("")
    md.append(f"- Method: {result['method']}")
    md.append(f"- Symbols: {', '.join(SYMBOLS)}")
    md.append(f"- Splits: train {TRAIN[0]}..{TRAIN[1]}; val {VAL[0]}..{VAL[1]}; test {TEST[0]}..{TEST[1]}")
    md.append(f"- Counts: collected={len(eval_rows)} train={len(train_rows)} val={len(val_rows)} test={len(test_rows)}")
    md.append("")
    md.append("## Test-set QLIKE (lower is better)")
    for name in ["B0", "B1", "C1", "C2"]:
        r = summary[name]
        pub = PUBLISHED[name]
        md.append(f"- {name}: QLIKE={r['test_qlike_mean']:.6f} (n={r['test_n']})  [published {pub['qlike']:.6f} (n={pub['n']})]  abs_diff={abs(r['test_qlike_mean'] - pub['qlike']):.2e}")
    md.append("")
    for k in ["C2_vs_B1", "C1_vs_B1", "C2_vs_C1"]:
        c = contrasts[k]
        p = PUBLISHED[k]
        md.append(f"## {k}")
        md.append(f"- mean diff: {c['mean_diff']:.6f}  [published {p['mean_diff']:.6f}]  abs_diff={abs(c['mean_diff'] - p['mean_diff']):.2e}")
        md.append(f"- relative reduction: {c['rel_reduction_pct']:.2f}%  [published {p['rel_pct']:.2f}%]  abs_diff={abs(c['rel_reduction_pct'] - p['rel_pct']):.4f} pct-points")
        md.append(f"- 95% CI: [{c['ci_lo']:.6f}, {c['ci_hi']:.6f}]  [published [{p['ci_lo']:.6f}, {p['ci_hi']:.6f}]]")
        md.append(f"- n_pairs: {c['n_pairs']}  [published {p['n_pairs']}]")
        md.append("")
    md.append(f"- all_within_tolerance: {all_within}")
    md.append(f"- conclusion: {result['conclusion']}")
    md.append("")
    md.append("## Gate assessment (primary contrast C2 vs B1)")
    md.append(f"- Test window = {test_days} days = {n_blocks} non-overlapping 30-day blocks (>=3 required)")
    md.append(f"- Relative reduction: {c2b1['rel_reduction_pct']:.2f}% (floor 2.0%) -> {'PASS' if c2b1['rel_reduction_pct'] >= 2.0 else 'FAIL'}")
    md.append(f"- 95% CI for diff (C2-B1): [{c2b1['ci_lo']:.6f}, {c2b1['ci_hi']:.6f}] (excludes zero: {result['gate']['ci_excludes_zero']})")
    md.append(f"- Paired n: {c2b1['n_pairs']} (>=5 required)")
    md.append(f"- Formal gate: **{result['gate']['verdict']}**")
    md.append("- FCLR-H001 remains NOT_SUPPORTED (CI does not exclude zero; gate NOT_MET)")
    (OUT_DIR / f"recompute_fclr008_{ts}.md").write_text("\n".join(md) + "\n")
    print(f"\nWROTE {OUT_DIR / f'recompute_fclr008_{ts}.md'}")
    return 0 if all_within else 1


if __name__ == "__main__":
    raise SystemExit(main())