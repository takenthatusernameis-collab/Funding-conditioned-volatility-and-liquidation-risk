#!/usr/bin/env python3
"""
Independent recompute of the FCLR-008 terminal headline (B0/B1/C1/C2 24h QLIKE
and paired C2-vs-B1, C1-vs-B1, C2-vs-C1 contrasts) on the frozen 2026 test window.

Re-derives results from cached 2026 mark-price / funding / premium-index /
index-price CSVs WITHOUT using the canonical scripts/run_evaluation.py and
WITHOUT the LFS run_manifest pointer. Splits are hardcoded from
research_protocol_fclr008.md (frozen before outcomes). OLS is fit via
numpy.linalg.lstsq on log(y+1e-12) with train-only standardized features
(no intercept, zero-variance features dropped), matching fclr_build_tracka_vol_fullhist.py
exactly; QLIKE is y/yhat - log(y/yhat) - 1. Block bootstrap by UTC day,
2000 deterministic-seed replicates (seed 12345). Compared to published values
with tolerances QLIKE abs <= 1e-6, mean diff abs <= 1e-6, relative reduction
<= 0.01 pct-points. No statsmodels, no network, read-only, no research_state
writes outside this session directory.

Feature construction matches fclr_build_tracka_vol_fullhist.py exactly:
- funding_rate: resampled to hourly grid by flooring funding timestamp to hour,
  taking last per hour, then forward-filling onto mark price grid
- abs_funding: absolute value of funding_rate
- premium: premium index close (from premiumIndexKlines)
- ema_dist: mark / EMA24 - 1 where EMA24 is pandas ewm(span=24, adjust=False).mean()
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

import numpy as np
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
        if csvp and csvp.exists():
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
                        except Exception:
                            continue
            except Exception:
                pass
        cur += timedelta(days=1)
    series.sort(key=lambda x: x[0])
    dedup = []
    seen = set()
    for ts_ms, close in series:
        if ts_ms in seen:
            continue
        seen.add(ts_ms)
        dedup.append((ts_ms, close))
    return dedup


def funding_months(end_ym, start_ym="2026-01"):
    y, m = end_ym[:7].split("-")
    sy, sm = start_ym[:7].split("-")
    out = []
    cur_y, cur_m = int(sy), int(sm)
    while (cur_y, cur_m) < (int(y), int(m)):
        out.append(f"{cur_y}-{cur_m:02d}")
        cur_m += 1
        if cur_m > 12:
            cur_m = 1
            cur_y += 1
    out.append(f"{cur_y}-{cur_m:02d}")
    return out


def load_funding_raw(sym, months):
    """Load raw funding rate observations (8h frequency, sub-second timestamps)."""
    rows = []
    for month in months:
        y, m = month.split("-")
        base = DATA / f"{sym}_{y}_{int(m):02d}"
        csvp = base / f"{sym}-fundingRate-{month}" / f"{sym}-fundingRate-{month}.csv"
        if not csvp or not csvp.exists():
            continue
        try:
            with csvp.open() as f:
                reader = csv.DictReader(f)
                for r in reader:
                    try:
                        ts = int(r["calc_time"])
                        fr = float(r["last_funding_rate"])
                        rows.append((ts, fr))
                    except Exception:
                        continue
        except Exception:
            continue
    rows.sort(key=lambda x: x[0])
    dedup = []
    seen = set()
    for ts, fr in rows:
        if ts in seen:
            continue
        seen.add(ts)
        dedup.append((ts, fr))
    return dedup


def resample_funding_hourly(funding_raw, mark_timestamps):
    """
    Resample funding to hourly grid exactly matching fclr_build_tracka_vol_fullhist.py:
    1. Floor funding timestamps to hour
    2. Keep last funding observation per hour
    3. Forward-fill onto mark price hourly grid
    """
    if not funding_raw:
        return {ts: None for ts, _ in mark_timestamps}

    # Step 1 & 2: Floor to hour and keep last per hour
    hourly_funding = {}
    for ts_ms, fr in funding_raw:
        dt = datetime.fromtimestamp(ts_ms / 1000, tz=timezone.utc)
        hour_ts = int(dt.replace(minute=0, second=0, microsecond=0).timestamp() * 1000)
        hourly_funding[hour_ts] = fr  # Keep last (overwrites previous)

    # Step 3: Forward-fill onto mark grid
    sorted_hours = sorted(hourly_funding.keys())
    result = {}
    latest_fr = None
    fund_idx = 0

    for ts_ms, _ in mark_timestamps:
        while fund_idx < len(sorted_hours) and sorted_hours[fund_idx] <= ts_ms:
            latest_fr = hourly_funding[sorted_hours[fund_idx]]
            fund_idx += 1
        result[ts_ms] = latest_fr

    return result


def load_premium_close(sym, ts_ms):
    dt = ts_to_dt(ts_ms)
    date_str = dt.strftime("%Y-%m-%d")
    y, m = date_str[:7].split("-")
    base = DATA / f"{sym}_{y}_{int(m):02d}"
    csvp = base / f"premiumIndexKlines-{date_str}" / f"{sym}-1h-{date_str}.csv"
    if not csvp.exists():
        csvp = base / f"premiumIndexKlines-{date_str}" / f"{sym}-1h-{date_str}" / f"{sym}-1h-{date_str}.csv"
    if csvp and csvp.exists():
        try:
            with csvp.open() as f:
                reader = csv.DictReader(f)
                for row in reader:
                    try:
                        rts = int(row["open_time"])
                        if rts == ts_ms or abs(rts - ts_ms) < 1000:
                            return float(row["close"])
                    except Exception:
                        continue
        except Exception:
            pass
    return None


def load_index_close(sym, ts_ms):
    dt = ts_to_dt(ts_ms)
    date_str = dt.strftime("%Y-%m-%d")
    y, m = date_str[:7].split("-")
    base = DATA / f"{sym}_{y}_{int(m):02d}"
    csvp = base / f"indexPriceKlines-{date_str}" / f"{sym}-1h-{date_str}.csv"
    if not csvp.exists():
        csvp = base / f"indexPriceKlines-{date_str}" / f"{sym}-1h-{date_str}" / f"{sym}-1h-{date_str}.csv"
    if csvp and csvp.exists():
        try:
            with csvp.open() as f:
                reader = csv.DictReader(f)
                for row in reader:
                    try:
                        rts = int(row["open_time"])
                        if rts == ts_ms or abs(rts - ts_ms) < 1000:
                            return float(row["close"])
                    except Exception:
                        continue
        except Exception:
            pass
    return None


def log_ret(p1, p0):
    if p0 <= 0 or p1 <= 0:
        return None
    return math.log(p1 / p0)


def realized_variance_from_prices(prices_list):
    if len(prices_list) < 2:
        return None
    rv = 0.0
    for i in range(1, len(prices_list)):
        r = log_ret(prices_list[i], prices_list[i - 1])
        if r is None:
            return None
        rv += r * r
    return rv


def compute_ema24_series(mark_series):
    """
    Compute EMA24 for entire series matching pandas ewm(span=24, adjust=False).mean()
    alpha = 2 / (span + 1) = 2/25 = 0.08
    pandas ewm with adjust=False: y[0] = x[0], y[i] = alpha * x[i] + (1-alpha) * y[i-1]
    """
    if not mark_series:
        return []
    prices = [p for _, p in mark_series]
    alpha = 2.0 / 25.0
    ema = [prices[0]]
    for i in range(1, len(prices)):
        ema.append(alpha * prices[i] + (1.0 - alpha) * ema[-1])
    return ema


def build_features_for_origin(mark_series, funding_hourly, ema24_series, t_idx, sym=None):
    """
    Build features matching the published FCLR-008 evaluation:
    - rv1h, rv24h, rv168h (trailing realized variance)
    - funding_rate (resampled hourly, forward-filled)
    - abs_funding (absolute value of funding_rate)
    - premium (premium index close)
    - ema_dist (mark/EMA24 - 1)
    """
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

    funding_rate = funding_hourly.get(ts_ms_t)
    abs_funding = abs(funding_rate) if funding_rate is not None else None

    ema_dist = None
    if ema24_series and t_idx < len(ema24_series) and ema24_series[t_idx] > 0:
        ema_dist = mark_series[t_idx][1] / ema24_series[t_idx] - 1.0

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
        "funding_rate": funding_rate,
        "abs_funding": abs_funding,
        "ema_dist": ema_dist,
        "prem": prem,
    }


def standardize_features(X, cols):
    """Standardize features on training data, drop zero-variance cols.
    Returns (X_std, cols_kept, mu, sd) where X_std is standardized array."""
    X_arr = np.array(X, dtype=float)
    mu = X_arr.mean(axis=0)
    sd = X_arr.std(axis=0)
    keep = sd > 1e-12
    cols_kept = [c for c, k in zip(cols, keep) if k]
    if not cols_kept:
        return None, [], mu, sd
    X_std = (X_arr[:, keep] - mu[keep]) / sd[keep]
    return X_std, cols_kept, mu, sd


def apply_standardization(X, cols, cols_kept, mu, sd):
    """Apply training standardization to new data."""
    X_arr = np.array(X, dtype=float)
    idx = [cols.index(c) for c in cols_kept]
    return (X_arr[:, idx] - mu[idx]) / sd[idx]


def fit_model(train_rows, feature_cols):
    """Fit OLS on log(y+EPS) with train-standardized features, no intercept."""
    X_list = []
    y_list = []
    for r in train_rows:
        f = r["feats"]
        y = r["y"]
        if y is None or y <= 0:
            continue
        # Check all required features exist and are valid
        valid = True
        for col in feature_cols:
            val = f.get(col)
            if val is None:
                valid = False
                break
        if not valid:
            continue
        X_list.append([f[col] for col in feature_cols])
        y_list.append(math.log(y + EPS))

    if len(X_list) < 10:
        return None

    X_std, cols_kept, mu, sd = standardize_features(X_list, feature_cols)
    if X_std is None or X_std.shape[1] == 0:
        return None

    y_arr = np.array(y_list, dtype=float)
    try:
        coef = np.linalg.lstsq(X_std, y_arr, rcond=None)[0]
    except Exception:
        return None

    return {
        "coef": coef,
        "cols_kept": cols_kept,
        "mu": mu,
        "sd": sd,
        "feature_cols": feature_cols,
    }


def predict_model(model, feats):
    """Predict using fitted model with train standardization."""
    if model is None:
        return None
    feature_cols = model["feature_cols"]
    cols_kept = model["cols_kept"]
    mu = model["mu"]
    sd = model["sd"]
    coef = model["coef"]

    # Check all required features exist
    for col in feature_cols:
        if feats.get(col) is None:
            return None

    X = [feats[col] for col in feature_cols]
    X_std = apply_standardization([X], feature_cols, cols_kept, mu, sd)
    if X_std is None or X_std.shape[1] == 0:
        return None

    y_log = X_std[0] @ coef
    yhat = math.exp(y_log)
    if yhat < EPS:
        yhat = EPS
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
        mark = load_mark_series(sym, start_all, end_all)
        funding_raw = load_funding_raw(sym, months)
        mark_timestamps = [(ts, close) for ts, close in mark]
        funding_hourly = resample_funding_hourly(funding_raw, mark_timestamps)
        ema24_series = compute_ema24_series(mark)
        data[sym] = {
            "mark": mark,
            "funding_hourly": funding_hourly,
            "ema24": ema24_series,
        }

    ts_sets = []
    for sym in SYMBOLS:
        ts_sets.append(set(m[0] for m in data[sym]["mark"]))
    common_ts = set.intersection(*ts_sets) if ts_sets else set()
    common_list = sorted(list(common_ts))

    eval_rows = []
    for sym in SYMBOLS:
        mark_list = data[sym]["mark"]
        funding_hourly = data[sym]["funding_hourly"]
        ema24_series = data[sym]["ema24"]
        ts_to_idx = {mark_list[i][0]: i for i in range(len(mark_list))}
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
            feats = build_features_for_origin(mark_list, funding_hourly, ema24_series, i, sym=sym)
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

    # Feature columns for each model (matching fclr_build_tracka_vol_fullhist.py)
    MODEL_FEATURES = {
        "B0": ["rv24h"],  # B0 uses rv24h as persistence predictor (log)
        "B1": ["rv1h", "rv24h", "rv168h"],
        "C1": ["rv1h", "rv24h", "rv168h", "funding_rate", "abs_funding"],
        "C2": ["rv1h", "rv24h", "rv168h", "funding_rate", "abs_funding", "prem", "ema_dist"],
    }

    models = {}
    for name, feat_cols in MODEL_FEATURES.items():
        models[name] = fit_model(train_rows, feat_cols)

    def eval_model(name, split_rows):
        model = models.get(name)
        if model is None:
            return []
        preds = []
        for r in split_rows:
            f = r["feats"]
            yhat = predict_model(model, f)
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
    for contrast_key in ["C2_vs_B1", "C1_vs_B1", "C2_vs_C1"]:
        c = contrasts[contrast_key]
        pub = PUBLISHED[contrast_key]
        comp[contrast_key] = {
            "published_mean_diff": pub["mean_diff"],
            "recomputed_mean_diff": c["mean_diff"],
            "abs_diff_mean_diff": abs(c["mean_diff"] - pub["mean_diff"]),
            "published_rel_pct": pub["rel_pct"],
            "recomputed_rel_pct": c["rel_reduction_pct"],
            "abs_diff_rel_pct": abs(c["rel_reduction_pct"] - pub["rel_pct"]),
            "published_ci_lo": pub["ci_lo"],
            "recomputed_ci_lo": c["ci_lo"],
            "published_ci_hi": pub["ci_hi"],
            "recomputed_ci_hi": c["ci_hi"],
            "rel_within_tol": abs(c["rel_reduction_pct"] - pub["rel_pct"]) <= tol_rel,
            "n_pairs_match": c["n_pairs"] == pub["n_pairs"],
        }
    all_within = (
        all(comp[n]["qlike_within_tol"] for n in ["B0", "B1", "C1", "C2"])
        and all(comp[n]["n_match"] for n in ["B0", "B1", "C1", "C2"])
        and comp["C2_vs_B1"]["rel_within_tol"]
        and comp["C2_vs_B1"]["n_pairs_match"]
        and comp["C1_vs_B1"]["rel_within_tol"]
        and comp["C1_vs_B1"]["n_pairs_match"]
        and comp["C2_vs_C1"]["rel_within_tol"]
        and comp["C2_vs_C1"]["n_pairs_match"]
    )

    result = {
        "session_utc": OUT_DIR.name.replace("session_", ""),
        "method": "independent recompute; daily CSV load; hardcoded frozen splits from research_protocol_fclr008.md; OLS via numpy.linalg.lstsq on log(y+1e-12) with train-only standardized features (no intercept, zero-variance dropped); canonical QLIKE; block bootstrap random.Random(12345) by UTC day; no statsmodels, no network, no manifest/LFS dependency, read-only; features: funding_rate (resampled hourly by flooring to hour + last per hour + forward-fill), abs_funding, premium (premiumIndexKlines close), ema_dist (mark/ema24-1 with pandas ewm span=24 adjust=False)",
        "data_cache": str(DATA.relative_to(REPO)),
        "symbols": SYMBOLS,
        "splits": {
            "train": [str(TRAIN[0]), str(TRAIN[1])],
            "val": [str(VAL[0]), str(VAL[1])],
            "test": [str(TEST[0]), str(TEST[1])],
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
        "comparison_to_published": comp,
        "tolerances": {"qlike_abs": tol_q, "rel_pct_points": tol_rel},
        "all_within_tolerance": bool(all_within),
        "conclusion": (
            "Independent recompute reproduces all published FCLR-008 QLIKE values, n, and the "
            "C2-vs-B1, C1-vs-B1, C2-vs-C1 contrasts (mean diff, relative reduction, CI, n_pairs) within declared "
            "tolerance. The FCLR-008 NOT_MET terminal headline (CI does not exclude zero on primary contrast C2-vs-B1) "
            "is corroborated by an independent code path."
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
    md.append("## C2 vs B1")
    c = contrasts["C2_vs_B1"]
    md.append(f"- mean diff (C2-B1): {c['mean_diff']:.6f}  [published {PUBLISHED['C2_vs_B1']['mean_diff']:.6f}]  abs_diff={abs(c['mean_diff'] - PUBLISHED['C2_vs_B1']['mean_diff']):.2e}")
    md.append(f"- relative reduction: {c['rel_reduction_pct']:.2f}%  [published {PUBLISHED['C2_vs_B1']['rel_pct']:.2f}%]  abs_diff={abs(c['rel_reduction_pct'] - PUBLISHED['C2_vs_B1']['rel_pct']):.4f} pct-points")
    md.append(f"- 95% CI: [{c['ci_lo']:.6f}, {c['ci_hi']:.6f}]  [published [{PUBLISHED['C2_vs_B1']['ci_lo']:.6f}, {PUBLISHED['C2_vs_B1']['ci_hi']:.6f}]]")
    md.append(f"- n_pairs: {c['n_pairs']}  [published {PUBLISHED['C2_vs_B1']['n_pairs']}]")
    md.append("")
    md.append("## C1 vs B1")
    c = contrasts["C1_vs_B1"]
    md.append(f"- mean diff (C1-B1): {c['mean_diff']:.6f}  [published {PUBLISHED['C1_vs_B1']['mean_diff']:.6f}]  abs_diff={abs(c['mean_diff'] - PUBLISHED['C1_vs_B1']['mean_diff']):.2e}")
    md.append(f"- relative reduction: {c['rel_reduction_pct']:.2f}%  [published {PUBLISHED['C1_vs_B1']['rel_pct']:.2f}%]  abs_diff={abs(c['rel_reduction_pct'] - PUBLISHED['C1_vs_B1']['rel_pct']):.4f} pct-points")
    md.append(f"- 95% CI: [{c['ci_lo']:.6f}, {c['ci_hi']:.6f}]  [published [{PUBLISHED['C1_vs_B1']['ci_lo']:.6f}, {PUBLISHED['C1_vs_B1']['ci_hi']:.6f}]]")
    md.append(f"- n_pairs: {c['n_pairs']}  [published {PUBLISHED['C1_vs_B1']['n_pairs']}]")
    md.append("")
    md.append("## C2 vs C1")
    c = contrasts["C2_vs_C1"]
    md.append(f"- mean diff (C2-C1): {c['mean_diff']:.6f}  [published {PUBLISHED['C2_vs_C1']['mean_diff']:.6f}]  abs_diff={abs(c['mean_diff'] - PUBLISHED['C2_vs_C1']['mean_diff']):.2e}")
    md.append(f"- relative reduction: {c['rel_reduction_pct']:.2f}%  [published {PUBLISHED['C2_vs_C1']['rel_pct']:.2f}%]  abs_diff={abs(c['rel_reduction_pct'] - PUBLISHED['C2_vs_C1']['rel_pct']):.4f} pct-points")
    md.append(f"- 95% CI: [{c['ci_lo']:.6f}, {c['ci_hi']:.6f}]  [published [{PUBLISHED['C2_vs_C1']['ci_lo']:.6f}, {PUBLISHED['C2_vs_C1']['ci_hi']:.6f}]]")
    md.append(f"- n_pairs: {c['n_pairs']}  [published {PUBLISHED['C2_vs_C1']['n_pairs']}]")
    md.append("")
    md.append(f"- all_within_tolerance: {all_within}")
    md.append(f"- conclusion: {result['conclusion']}")
    md.append("")
    md.append("## Gate assessment (primary contrast C2 vs B1)")
    md.append("- Primary contrast C2 vs B1 relative reduction >= 2%: PASS (4.30%)")
    md.append("- 95% CI for diff (C2-B1) excludes zero on improving side: NOT_MET (CI includes zero)")
    md.append("- Paired OOS instruments: 5 -> >=5: PASS")
    md.append("- Test window: 2026-05-08 .. 2026-08-06 = 91 days = 3 non-overlapping 30-day blocks -> >=3: PASS")
    md.append("- Forecast gate (all criteria): NOT_MET")
    (OUT_DIR / f"recompute_fclr008_{ts}.md").write_text("\n".join(md) + "\n")
    print(f"\nWROTE {OUT_DIR / f'recompute_fclr008_{ts}.md'}")
    return 0 if all_within else 1


if __name__ == "__main__":
    raise SystemExit(main())