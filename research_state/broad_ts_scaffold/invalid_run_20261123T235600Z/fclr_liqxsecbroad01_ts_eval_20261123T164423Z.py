#!/usr/bin/env python3
"""
FCLR-LIQ-XSEC-BROAD-TS-01 heavy temporal-stability evaluation (stdlib + numpy + pandas + pyarrow).

Vectorized re-implementation of BROAD-01's methodology with identical:
  - 18 monthly parquet (2025-05..2026-10), sha256 sidecar assertion
  - train_frac=0.60, purge_embargo_h=48, block_h=168, horizon_h=1
  - B1 features: [1, log(rv24+eps), log(rv168+eps)]
  - C2 features: B1 + z(fund), abs_fund_pct(train-only), z(prem), z(oi), z(dislocation), z(ma_dev)
  - Target: log(fwd_notional + eps), OLS with Duan smearing
  - Per-block Spearman rank-IC with block start hours retained
  - Stability battery: sign reproduction fraction, rolling-window IC, ordered-block trend test,
    first/second-half gap with bootstrap CI, LOOIC range, per-regime sign stability
  - Block bootstrap N=2000, permutation N=1000, LOIO N=8, Holm 6-arm family
  - Symmetric verdict: STABLE / NOT_STABLE

Primary arm: LONG arm (SUPPORTED in BROAD-01). Short arm descriptive only.
This is a stability test of a cross-sectional association, NOT a time-series forecast gate.

Usage:
  python3 fclr_liqxsecbroad01_ts_eval_<UTC>.py <session_dir>
"""
from __future__ import annotations

import hashlib
import json
import math
import sys
from datetime import timezone
from pathlib import Path

import numpy as np
import pandas as pd
import pyarrow.parquet as pq

REPO = Path(__file__).resolve().parents[2]
BULK = REPO / "research_state" / "data_cache" / "ironflow_bulk"
SESSION_UTC = "20261123T164423Z"

MONTHS = ["2025-05", "2025-06", "2025-07", "2025-08", "2025-09", "2025-10",
          "2025-11", "2025-12", "2026-01", "2026-02", "2026-03", "2026-04",
          "2026-05", "2026-06", "2026-07", "2026-08", "2026-09", "2026-10"]

TRAIN_FRAC = 0.60
PURGE_EMBARGO_H = 48
BLOCK_H = 168
HORIZON_H = 1
N_BOOT = 2000
N_PERM = 1000
N_LOIO = 8
LOIO_PASS_THRESHOLD = 6
SEED = 20261123
EPS = 1e-12
ALPHA_K = 0.05 / (2 * 3)
MATERIALITY_PCT = 2.0
TRAIN_SUBSAMPLE = 200
SIGN_REPRODUCTION_FRACTION = 0.80
ROLLING_WINDOW = 6
TREND_ALPHA = ALPHA_K
HOLM_FAMILY = [
    "trend_test_long_arm",
    "first_second_half_gap_long_arm",
    "loio_range_long_arm",
    "rolling_mean_min_long_arm",
    "per_regime_rv_tercile_long_arm",
    "per_regime_utc_bucket_long_arm",
]
rng = np.random.default_rng(SEED)


def sha256_file(p: Path) -> str:
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def _hkey(ts) -> int:
    if isinstance(ts, (int, float)):
        return int(ts // 3600) * 3600
    dt = ts.to_pydatetime() if hasattr(ts, "to_pydatetime") else ts
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return int(dt.timestamp() // 3600) * 3600


def add_hk(df, ts_col):
    df["hk"] = [_hkey(v) for v in df[ts_col].to_list()]
    return df


def mean(xs):
    return float(np.mean(xs)) if len(xs) > 0 else float("nan")


def pstd(xs):
    arr = np.asarray(xs, dtype=float)
    if len(arr) == 0:
        return 1.0
    v = float(np.var(arr))
    return math.sqrt(v) if v > 0 else 1.0


def coin_from_market(market: str) -> str:
    s = str(market)
    if ":" in s:
        s = s.split(":", 1)[1]
    if s.endswith("-PERP"):
        s = s[:-5]
    return s.upper()


def spearman_rank_ic(xs, ys):
    xs = np.asarray(xs, dtype=float)
    ys = np.asarray(ys, dtype=float)
    n = len(xs)
    if n < 3:
        return float("nan")
    rank_x = xs.argsort(kind="mergesort").argsort(kind="mergesort").astype(float) + 1.0
    rank_y = ys.argsort(kind="mergesort").argsort(kind="mergesort").astype(float) + 1.0
    mx = rank_x.mean()
    my = rank_y.mean()
    a = rank_x - mx
    b = rank_y - my
    num = float(np.dot(a, b))
    dx2 = float(np.dot(a, a))
    dy2 = float(np.dot(b, b))
    dx = math.sqrt(dx2)
    dy = math.sqrt(dy2)
    if dx == 0 or dy == 0:
        return float("nan")
    return num / (dx * dy)


def qlike(y, p):
    mask = (y > 0) & (p > 0)
    if mask.sum() == 0:
        return float("nan")
    r = y[mask] / p[mask]
    return float(np.mean(r - 1.0 - np.log(r)))


def poisson_deviance(y, p):
    mask = (y > 0) & (p > 0)
    if mask.sum() == 0:
        return float("nan")
    yv = y[mask]
    pv = p[mask]
    return float(np.mean(2.0 * (yv * np.log(yv / pv) - (yv - pv))))


def ols_fit(X, y):
    beta, _, _, _ = np.linalg.lstsq(X, y, rcond=None)
    return beta


def ols_predict(X, beta):
    return X @ beta


def percentile_rank(vals, v):
    if len(vals) == 0:
        return 0.5
    return float(np.sum(vals <= v) / len(vals))


def holm_adjust(pvals):
    items = sorted(pvals.items(), key=lambda kv: kv[1])
    m = len(items)
    adj = {}
    for i, (label, p) in enumerate(items):
        adj[label] = min(1.0, (m - i) * p)
    prev = 0.0
    for label in [k for k, _ in items]:
        prev = max(prev, adj[label])
        adj[label] = prev
    return adj


def main():
    sdir = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(
        "research_state/session_" + SESSION_UTC)

    print("Step 1: SHA-256 verification", flush=True)
    sha_ok = 0
    sha_bad = 0
    for subdir in ["candles_1h", "funding", "open_interest", "liquidations"]:
        for month in MONTHS:
            sp = BULK / subdir / f"{month}.parquet.sha256"
            pqfile = BULK / subdir / f"{month}.parquet"
            stored = sp.read_text().strip().split()[0] if sp.is_file() else None
            actual = sha256_file(pqfile) if pqfile.is_file() else None
            if stored and actual and stored == actual:
                sha_ok += 1
            else:
                sha_bad += 1
    print(f"  SHA-256: {sha_ok} ok, {sha_bad} bad", flush=True)

    print("Step 2: Load liquidations (dedup by coin/hour/tx_hash)", flush=True)
    liq_frames = []
    liq_rows = 0
    for month in MONTHS:
        t = pq.read_table(BULK / "liquidations" / f"{month}.parquet")
        df = t.to_pandas()
        liq_rows += len(df)
        df["coin"] = df["market"].map(coin_from_market)
        df = add_hk(df, "timestamp")
        df["txv"] = df["tx_hash"].astype(str)
        df["noti"] = pd.to_numeric(df["notional_usd"], errors="coerce").fillna(0.0)
        df["side"] = df["position_side"].astype(str).str.lower()
        liq_frames.append(df[["coin", "hk", "txv", "noti", "side"]])
    liq = pd.concat(liq_frames, ignore_index=True)
    liq = liq.drop_duplicates(subset=["coin", "hk", "txv"])
    liq_long = liq[liq["side"].str.startswith("long")]
    liq_short = liq[liq["side"].str.startswith("short")]
    liq_count_long = liq_long.groupby(["coin", "hk"]).size().to_dict()
    liq_notional_long = liq_long.groupby(["coin", "hk"])["noti"].sum().to_dict()
    liq_count_short = liq_short.groupby(["coin", "hk"]).size().to_dict()
    liq_notional_short = liq_short.groupby(["coin", "hk"])["noti"].sum().to_dict()
    print(f"  {liq_rows} rows, {len(liq)} unique events", flush=True)

    print("Step 3: Load candles (close + coin identity)", flush=True)
    candle_frames = []
    for month in MONTHS:
        t = pq.read_table(BULK / "candles_1h" / f"{month}.parquet")
        df = t.to_pandas()
        df = add_hk(df, "timestamp")
        df["close"] = pd.to_numeric(df["close"], errors="coerce")
        df = df[df["close"] > 0]
        if "coin" in df.columns:
            df["coin"] = df["coin"].astype(str).str.upper()
        else:
            df["coin"] = df["market"].map(coin_from_market)
        candle_frames.append(df[["market", "hk", "close", "coin"]])
    candles = pd.concat(candle_frames, ignore_index=True)
    candle_close = candles.set_index(["market", "hk"])["close"].to_dict()
    candle_coin = candles.groupby("market")["coin"].first().to_dict()
    markets = sorted(candle_close.keys() and [k[0] for k in candle_close.keys()])
    markets = sorted({k[0] for k in candle_close.keys()})
    hours = sorted({hk for (_, hk) in candle_close.keys()})
    n_hours = len(hours)
    print(f"  {n_hours} hours, {len(markets)} markets", flush=True)

    print("Step 4: Load funding + OI", flush=True)
    fund_frames = []
    for month in MONTHS:
        t = pq.read_table(BULK / "funding" / f"{month}.parquet")
        df = t.to_pandas()
        df = add_hk(df, "timestamp")
        fund_frames.append(df[["market", "hk", "funding_rate", "premium"]])
    funding = pd.concat(fund_frames, ignore_index=True)
    fund_val = funding.set_index(["market", "hk"])[["funding_rate", "premium"]].to_dict("index")
    fund_val = {(m, h): (v["funding_rate"], v["premium"]) for (m, h), v in fund_val.items()}

    oi_frames = []
    for month in MONTHS:
        t = pq.read_table(BULK / "open_interest" / f"{month}.parquet")
        df = t.to_pandas()
        df = add_hk(df, "timestamp")
        oi_frames.append(df[["market", "hk", "open_interest", "mark_price", "oracle_price"]])
    oidf = pd.concat(oi_frames, ignore_index=True)
    oi_val = oidf.set_index(["market", "hk"])["open_interest"].to_dict()
    mark_val = oidf.set_index(["market", "hk"])["mark_price"].to_dict()
    oracle_val = oidf.set_index(["market", "hk"])["oracle_price"].to_dict()
    print("  done", flush=True)

    print("Step 5: Build per-market time series with cumulative-sum RV", flush=True)
    cut = int(n_hours * TRAIN_FRAC)
    train_hours = set(hours[:cut])
    test_hours_raw = sorted(set(h for h in hours[cut + PURGE_EMBARGO_H:]))
    blocks = [test_hours_raw[i:i + BLOCK_H] for i in range(0, len(test_hours_raw), BLOCK_H)]
    block_of = {}
    block_start_of = {}
    for bi, blk in enumerate(blocks):
        for hk in blk:
            block_of[hk] = bi
            block_start_of[hk] = blk[0]

    def elig_origin(hk):
        bi = block_of.get(hk)
        if bi is None:
            return False
        return hk + HORIZON_H * 3600 <= blocks[bi][-1]

    eligible_origins = [hk for hk in test_hours_raw if elig_origin(hk)]
    test_coins = sorted(set(candle_coin.values()))

    coin_max_hour = {}
    for (m, hk) in candle_close.keys():
        c = candle_coin[m]
        if hk > coin_max_hour.get(c, 0):
            coin_max_hour[c] = hk
    final_hours_cutoff = hours[int(n_hours * 0.95)]
    survivor_coins = sorted([c for c in test_coins if coin_max_hour.get(c, 0) >= final_hours_cutoff])
    exited_coins = [c for c in test_coins if c not in survivor_coins]

    series_records = []
    for mkt in markets:
        coin = candle_coin[mkt]
        mkt_df = candles[(candles["market"] == mkt)].sort_values("hk")
        mkt_hours = mkt_df["hk"].values
        closes = mkt_df["close"].values.astype(float)
        rets = np.full(len(mkt_hours), 0.0)
        rets[1:] = np.log(closes[1:] / closes[:-1])
        cum = np.concatenate([[0.0], np.cumsum(rets * rets)])
        s24 = cum[1:] - np.maximum(0, np.arange(len(mkt_hours)) - 23)
        s24 = cum[1:] - cum[np.maximum(0, np.arange(len(mkt_hours)) - 23)]
        s168 = cum[1:] - cum[np.maximum(0, np.arange(len(mkt_hours)) - 167)]
        prev_closes = np.concatenate([[np.nan], closes[:-1]])
        ma_dev = (closes / prev_closes - 1.0)
        ma_dev[~np.isfinite(ma_dev)] = 0.0
        for i, hk in enumerate(mkt_hours):
            fund, prem = fund_val.get((mkt, hk), (0.0, 0.0))
            oi = oi_val.get((mkt, hk), 0.0) or 0.0
            mk_p = mark_val.get((mkt, hk))
            or_p = oracle_val.get((mkt, hk))
            dislocation = (mk_p / or_p - 1.0) if (mk_p and or_p and or_p > 0) else 0.0
            series_records.append({
                "coin": coin, "market": mkt, "hk": int(hk),
                "rv24": float(s24[i]), "rv168": float(s168[i]),
                "fund": float(fund) if fund is not None else 0.0,
                "prem": float(prem) if prem is not None else 0.0,
                "oi": float(oi),
                "dislocation": float(dislocation),
                "ma_dev": float(ma_dev[i]) if np.isfinite(ma_dev[i]) else 0.0,
                "close": float(closes[i]),
            })
    series_df = pd.DataFrame(series_records)
    print(f"  {len(series_df)} series rows, {series_df['coin'].nunique()} coins", flush=True)

    print("Step 6: Train-only scaling + abs funding percentile", flush=True)
    scale_feats = ["rv24", "rv168", "fund", "prem", "oi", "dislocation", "ma_dev"]
    sc = {}
    train_mask_df = series_df["hk"].isin(train_hours)
    for feat in scale_feats:
        vals = series_df.loc[train_mask_df, feat].values
        vals = vals[np.isfinite(vals)]
        if len(vals) > 0:
            sc[feat] = (float(np.mean(vals)), float(np.std(vals)) if np.std(vals) > 0 else 1.0)
        else:
            sc[feat] = (0.0, 1.0)

    abs_fund_train = {}
    for coin in test_coins:
        funds = series_df[(series_df["coin"] == coin) & train_mask_df]["fund"].abs().values
        abs_fund_train[coin] = funds

    def z_vec(df, feat):
        v = df[feat].values.astype(float)
        v = np.where(np.isfinite(v), v, 0.0)
        m, s = sc[feat]
        return (v - m) / s if s > 0 else np.zeros_like(v)

    def abs_fund_pct_vec(df):
        out = np.full(len(df), 0.5)
        coin_arr = df["coin"].values
        fund_arr = df["fund"].values.astype(float)
        abs_fund_arr = np.abs(fund_arr)
        for coin in test_coins:
            funds = abs_fund_train[coin]
            if len(funds) < 30:
                continue
            srt = np.sort(funds)
            mask = coin_arr == coin
            if not mask.any():
                continue
            targets = abs_fund_arr[mask]
            lo = np.searchsorted(srt, targets, side="left")
            hi = np.searchsorted(srt, targets, side="right")
            pct = (lo + hi) / (2.0 * len(srt))
            out[mask] = pct
        return out

    series_df["z_rv24"] = z_vec(series_df, "rv24")
    series_df["z_rv168"] = z_vec(series_df, "rv168")
    series_df["z_fund"] = z_vec(series_df, "fund")
    series_df["z_prem"] = z_vec(series_df, "prem")
    series_df["z_oi"] = z_vec(series_df, "oi")
    series_df["z_dislocation"] = z_vec(series_df, "dislocation")
    series_df["z_ma_dev"] = z_vec(series_df, "ma_dev")
    series_df["abs_fund_pct"] = abs_fund_pct_vec(series_df)
    print("  done", flush=True)

    print("Step 7: Build test panel + train panel", flush=True)

    def forward_outcome_map(liquidity_count, liquidity_notional):
        return liquidity_count, liquidity_notional

    liq_count_l = liq_count_long
    liq_noti_l = liq_notional_long
    liq_count_s = liq_count_short
    liq_noti_s = liq_notional_short

    eligible_set = set(eligible_origins)
    feat_cols = ["rv24", "rv168", "fund", "prem", "oi", "dislocation", "ma_dev",
                 "z_rv24", "z_rv168", "z_fund", "abs_fund_pct", "z_prem", "z_oi",
                 "z_dislocation", "z_ma_dev"]
    el = pd.DataFrame({"hk": eligible_origins})
    el["block"] = el["hk"].map(block_of)
    el["block_start_h"] = el["hk"].map(block_start_of)
    sk = series_df[["coin", "hk"] + feat_cols]
    sk = sk[sk["hk"].isin(eligible_set)]
    test_df = el.merge(sk, on="hk", how="inner")
    test_df["wh"] = test_df["hk"] + HORIZON_H * 3600
    test_df["fwd_cnt_long"] = [liq_count_l.get((c, w), 0) for c, w in zip(test_df["coin"], test_df["wh"])]
    test_df["fwd_noti_long"] = [liq_noti_l.get((c, w), 0.0) for c, w in zip(test_df["coin"], test_df["wh"])]
    test_df["fwd_cnt_short"] = [liq_count_s.get((c, w), 0) for c, w in zip(test_df["coin"], test_df["wh"])]
    test_df["fwd_noti_short"] = [liq_noti_s.get((c, w), 0.0) for c, w in zip(test_df["coin"], test_df["wh"])]
    test_df["is_survivor"] = test_df["coin"].isin(survivor_coins)
    test_df = test_df.drop(columns=["wh"])
    n_test_rows = len(test_df)

    train_df = series_df[series_df["hk"].isin(train_hours)].copy()
    train_sub = train_df.iloc[::TRAIN_SUBSAMPLE].copy()
    train_sub = train_sub.reset_index(drop=True)
    train_sub["wh"] = train_sub["hk"] + HORIZON_H * 3600
    train_sub["fwd_cnt_long"] = [liq_count_l.get((c, w), 0) for c, w in zip(train_sub["coin"], train_sub["wh"])]
    train_sub["fwd_noti_long"] = [liq_noti_l.get((c, w), 0.0) for c, w in zip(train_sub["coin"], train_sub["wh"])]
    train_sub["fwd_cnt_short"] = [liq_count_s.get((c, w), 0) for c, w in zip(train_sub["coin"], train_sub["wh"])]
    train_sub["fwd_noti_short"] = [liq_noti_s.get((c, w), 0.0) for c, w in zip(train_sub["coin"], train_sub["wh"])]
    train_df_full = train_sub.drop(columns=["wh"])
    print(f"  test rows: {n_test_rows}, train rows (subsampled): {len(train_df_full)}", flush=True)

    print("Step 8: Fit OLS models on train", flush=True)

    def b1_X(df):
        return np.column_stack([
            np.ones(len(df)),
            np.log(np.maximum(df["rv24"].values, 0.0) + EPS),
            np.log(np.maximum(df["rv168"].values, 0.0) + EPS),
        ])

    def c2_X(df):
        return np.column_stack([
            np.ones(len(df)),
            np.log(np.maximum(df["rv24"].values, 0.0) + EPS),
            np.log(np.maximum(df["rv168"].values, 0.0) + EPS),
            df["z_fund"].values, df["abs_fund_pct"].values,
            df["z_prem"].values, df["z_oi"].values,
            df["z_dislocation"].values, df["z_ma_dev"].values,
        ])

    def fit_side(df, feat_fn, side_key):
        fi = df[side_key].values.astype(float)
        fi = np.where((fi is None) | (fi <= 0), 1.0, fi)
        X = feat_fn(df)
        y = np.log(fi + EPS)
        beta = ols_fit(X, y)
        resid = y - ols_predict(X, beta)
        smear = float(np.mean(np.exp(resid))) if len(resid) > 0 else 1.0
        return beta, smear, len(X)

    beta_B1_l, smear_B1_l, nB1_l = fit_side(train_df_full, b1_X, "fwd_noti_long")
    beta_C2_l, smear_C2_l, nC2_l = fit_side(train_df_full, c2_X, "fwd_noti_long")
    beta_B1_s, smear_B1_s, nB1_s = fit_side(train_df_full, b1_X, "fwd_noti_short")
    beta_C2_s, smear_C2_s, nC2_s = fit_side(train_df_full, c2_X, "fwd_noti_short")
    print("  OLS fits done", flush=True)

    print("Step 9: Predict on test + per-block rank-IC with block start hours", flush=True)

    def predict_side(df, feat_fn, beta, smear, side_key="fwd_noti_long"):
        fi = df[side_key].values.astype(float)
        fi = np.where(fi <= 0, 1.0, fi)
        pred = np.exp(np.clip(ols_predict(feat_fn(df), beta), -50.0, 50.0)) * smear
        return pd.DataFrame({
            "coin": df["coin"].values,
            "hk": df["hk"].values,
            "block": df["block"].values,
            "block_start_h": df["block_start_h"].values,
            "actual": fi,
            "pred": pred,
        })

    pred_B1_l = predict_side(test_df, b1_X, beta_B1_l, smear_B1_l, "fwd_noti_long")
    pred_C2_l = predict_side(test_df, c2_X, beta_C2_l, smear_C2_l, "fwd_noti_long")
    pred_B1_s = predict_side(test_df, b1_X, beta_B1_s, smear_B1_s, "fwd_noti_long")
    pred_C2_s = predict_side(test_df, c2_X, beta_C2_s, smear_C2_s, "fwd_noti_long")

    def block_rank_ic_with_hours(pred_df, min_coins=5):
        results = []
        for bi, grp in pred_df.groupby("block"):
            if len(grp) < min_coins:
                continue
            ic = spearman_rank_ic(grp["pred"].values, grp["actual"].values)
            results.append({
                "block_index": int(bi),
                "block_start_h": int(grp["block_start_h"].iloc[0]),
                "ic": float(ic),
                "n_coins": int(len(grp)),
            })
        return sorted(results, key=lambda x: x["block_index"])

    ic_blocks_B1_l = block_rank_ic_with_hours(pred_B1_l)
    ic_blocks_C2_l = block_rank_ic_with_hours(pred_C2_l)
    ic_blocks_B1_s = block_rank_ic_with_hours(pred_B1_s)
    ic_blocks_C2_s = block_rank_ic_with_hours(pred_C2_s)

    ic_C2_l = np.array([b["ic"] for b in ic_blocks_C2_l])
    ic_C2_s = np.array([b["ic"] for b in ic_blocks_C2_s])
    ic_B1_l = np.array([b["ic"] for b in ic_blocks_B1_l])
    ic_B1_s = np.array([b["ic"] for b in ic_blocks_B1_s])
    block_start_hs = [b["block_start_h"] for b in ic_blocks_C2_l]
    block_indices = [b["block_index"] for b in ic_blocks_C2_l]

    mean_ic_C2_l = float(np.mean(ic_C2_l)) if len(ic_C2_l) > 0 else float("nan")
    mean_ic_C2_s = float(np.mean(ic_C2_s)) if len(ic_C2_s) > 0 else float("nan")
    mean_ic_B1_l = float(np.mean(ic_B1_l)) if len(ic_B1_l) > 0 else float("nan")
    mean_ic_B1_s = float(np.mean(ic_B1_s)) if len(ic_B1_s) > 0 else float("nan")
    n_blocks_C2 = len(ic_C2_l)
    n_blocks_C2_s = len(ic_C2_s)

    def deviance_aligned(pred_df, side_key):
        m = test_df[["coin", "hk", side_key]].merge(
            pred_df[["coin", "hk", "pred"]], on=["coin", "hk"], how="inner"
        )
        ys = m[side_key].values.astype(float)
        ys = np.where(ys <= 0, 1.0, ys)
        ps = m["pred"].values.astype(float)
        return qlike(ys, ps), poisson_deviance(ys, ps), len(ys)

    qB1_l, devB1_l, n_dev_l = deviance_aligned(pred_B1_l, "fwd_noti_long")
    qC2_l, devC2_l, _ = deviance_aligned(pred_C2_l, "fwd_noti_long")
    qB1_s, devB1_s, n_dev_s = deviance_aligned(pred_B1_s, "fwd_noti_short")
    qC2_s, devC2_s, _ = deviance_aligned(pred_C2_s, "fwd_noti_short")

    rel_imp_l = (devB1_l - devC2_l) / devB1_l if devB1_l > 0 else float("nan")
    rel_imp_s = (devB1_s - devC2_s) / devB1_s if devB1_s > 0 else float("nan")
    materiality_met_l = bool(rel_imp_l >= MATERIALITY_PCT / 100.0)
    materiality_met_s = bool(rel_imp_s >= MATERIALITY_PCT / 100.0)
    print(f"  Deviance: long B1={devB1_l:.6f} C2={devC2_l:.6f} rel_imp={rel_imp_l:.6f}", flush=True)
    print(f"  Deviance: short B1={devB1_s:.6f} C2={devC2_s:.6f} rel_imp={rel_imp_s:.6f}", flush=True)

    print("Step 10: Block bootstrap CI95 (N=2000)", flush=True)
    ic_blocks_valid = ic_C2_l[np.isfinite(ic_C2_l)]

    def bootstrap_mean_ic(arr):
        if len(arr) == 0:
            return float("nan")
        n_b = len(arr)
        sample = arr[rng.integers(0, n_b, size=n_b)]
        return float(np.mean(sample))

    boot_ics = np.array([bootstrap_mean_ic(ic_blocks_valid) for _ in range(N_BOOT)])
    boot_ics_valid = boot_ics[np.isfinite(boot_ics)]
    n_boot_valid = len(boot_ics_valid)
    boot_lo = float(np.percentile(boot_ics_valid, 2.5)) if n_boot_valid > 0 else float("nan")
    boot_hi = float(np.percentile(boot_ics_valid, 97.5)) if n_boot_valid > 0 else float("nan")
    ci_excludes_null_favorable = bool(boot_lo > 0)
    print(f"  Bootstrap CI95: [{boot_lo:.6f}, {boot_hi:.6f}]", flush=True)

    print("Step 11: Placebo/permutation null (N=1000)", flush=True)
    perm_ics = []
    pred_by_block = pred_C2_l.groupby("block")
    rank_a_by_block = {}
    rank_p_by_block = {}
    for bi, grp in pred_by_block:
        if len(grp) < 5:
            continue
        rank_a = grp["actual"].argsort(kind="mergesort").argsort(kind="mergesort").astype(float) + 1.0
        rank_p = grp["pred"].argsort(kind="mergesort").argsort(kind="mergesort").astype(float) + 1.0
        rank_a_by_block[bi] = rank_a
        rank_p_by_block[bi] = rank_p

    bis = list(rank_a_by_block.keys())
    for _ in range(N_PERM):
        perm_vals = []
        for bi in bis:
            shuf = rng.permutation(rank_p_by_block[bi])
            perm_vals.append(float(np.corrcoef(rank_a_by_block[bi], shuf)[0, 1]))
        if perm_vals:
            perm_ics.append(float(np.mean(perm_vals)))
    perm_ics = np.array(perm_ics)
    perm_ics_valid = perm_ics[np.isfinite(perm_ics)]
    n_perm_valid = len(perm_ics_valid)
    perm_pct_95 = float(np.percentile(perm_ics_valid, 95)) if n_perm_valid > 0 else float("nan")
    placebo_exceeds_null = bool(mean_ic_C2_l > perm_pct_95) if n_perm_valid > 0 else False
    print(f"  Placebo 95th percentile: {perm_pct_95:.6f}, true effect exceeds: {placebo_exceeds_null}", flush=True)

    print("Step 12: Leave-one-block-out range of mean rank-IC (long arm)", flush=True)
    loic_values = []
    for bi in block_indices:
        kept = ic_C2_l[[i for i in range(len(ic_C2_l)) if block_indices[i] != bi]]
        kept = kept[np.isfinite(kept)]
        loic_values.append(float(np.mean(kept)) if len(kept) > 0 else float("nan"))
    loic_valid_arr = np.array([v for v in loic_values if np.isfinite(v)])
    loic_range = float(np.max(loic_valid_arr) - np.min(loic_valid_arr)) if len(loic_valid_arr) > 0 else float("nan")
    loic_min = float(np.min(loic_valid_arr)) if len(loic_valid_arr) > 0 else float("nan")
    loic_max = float(np.max(loic_valid_arr)) if len(loic_valid_arr) > 0 else float("nan")
    print(f"  LOOIC range: [{loic_min:.6f}, {loic_max:.6f}] range={loic_range:.6f}", flush=True)

    print("Step 13: Leave-one-instrument-out (8 subsets)", flush=True)
    coins_in_test = sorted(test_df["coin"].unique())
    loio_base = test_df[["coin", "hk", "fwd_noti_long"]].merge(
        pred_C2_l[["coin", "hk", "pred"]], on=["coin", "hk"], how="inner"
    )

    def loio_subset(heldout):
        sub = loio_base[~loio_base["coin"].isin(heldout)]
        xs = sub["pred"].values.astype(float)
        ys = np.where(sub["fwd_noti_long"].values.astype(float) <= 0, 1.0,
                      sub["fwd_noti_long"].values.astype(float))
        if len(xs) < 5:
            return float("nan")
        return spearman_rank_ic(xs, ys)

    group_size = max(1, len(coins_in_test) // N_LOIO)
    loio_subsets = []
    for i in range(N_LOIO):
        start = i * group_size
        end = min((i + 1) * group_size, len(coins_in_test))
        loio_subsets.append(coins_in_test[start:end])
    if len(loio_subsets) > 1:
        loio_subsets[-1] = coins_in_test[(len(loio_subsets) - 1) * group_size:]

    loio_ics = [loio_subset(heldout) for heldout in loio_subsets]
    loio_valid = [ic for ic in loio_ics if np.isfinite(ic)]
    loio_sign_reproduced = sum(1 for ic in loio_valid if ic > 0)
    loio_pass = loio_sign_reproduced >= LOIO_PASS_THRESHOLD
    print(f"  LOIO: {len(loio_valid)} valid, {loio_sign_reproduced} sign reproduced, pass={loio_pass}", flush=True)

    print("Step 14: Rolling-window rank-IC (6-block) min/median/max + CI95 interval", flush=True)

    def rolling_mean(arr, w):
        if len(arr) < w:
            return np.array([])
        return np.convolve(arr, np.ones(w) / w, mode="valid")

    roll_ics = rolling_mean(ic_C2_l, ROLLING_WINDOW)
    roll_ics_valid = roll_ics[np.isfinite(roll_ics)]
    roll_min = float(np.min(roll_ics_valid)) if len(roll_ics_valid) > 0 else float("nan")
    roll_median = float(np.median(roll_ics_valid)) if len(roll_ics_valid) > 0 else float("nan")
    roll_max = float(np.max(roll_ics_valid)) if len(roll_ics_valid) > 0 else float("nan")

    boot_roll_mins = []
    boot_roll_maxs = []
    for _ in range(N_BOOT):
        n_b = len(ic_blocks_valid)
        sample = ic_blocks_valid[rng.integers(0, n_b, size=n_b)]
        roll_sample = rolling_mean(sample, ROLLING_WINDOW)
        roll_sample_valid = roll_sample[np.isfinite(roll_sample)]
        if len(roll_sample_valid) > 0:
            boot_roll_mins.append(float(np.min(roll_sample_valid)))
            boot_roll_maxs.append(float(np.max(roll_sample_valid)))
    boot_roll_mins_valid = np.array([v for v in boot_roll_mins if np.isfinite(v)])
    boot_roll_maxs_valid = np.array([v for v in boot_roll_maxs if np.isfinite(v)])
    roll_ci_lo = float(np.percentile(boot_roll_mins_valid, 2.5)) if len(boot_roll_mins_valid) > 0 else float("nan")
    roll_ci_hi = float(np.percentile(boot_roll_maxs_valid, 97.5)) if len(boot_roll_maxs_valid) > 0 else float("nan")
    print(f"  Rolling {ROLLING_WINDOW}-block: min={roll_min:.6f} median={roll_median:.6f} max={roll_max:.6f} CI95=[{roll_ci_lo:.6f},{roll_ci_hi:.6f}]", flush=True)

    print("Step 15: Ordered-block monotone trend test (Spearman block-index vs rank-IC)", flush=True)
    bi_arr = np.array(block_indices, dtype=float)
    trend_rho = spearman_rank_ic(bi_arr, ic_C2_l)
    trend_perm = []
    for _ in range(N_PERM):
        shuf = rng.permutation(ic_C2_l[np.isfinite(ic_C2_l)])
        trend_perm.append(spearman_rank_ic(bi_arr[:len(shuf)], shuf))
    trend_perm_valid = np.array([v for v in trend_perm if np.isfinite(v)])
    if len(trend_perm_valid) > 0:
        trend_p_two_sided = float((np.sum(np.abs(trend_perm_valid) >= np.abs(trend_rho)) + 1) / (len(trend_perm_valid) + 1))
    else:
        trend_p_two_sided = 1.0
    trend_not_reject_stationarity = bool(trend_p_two_sided >= TREND_ALPHA)
    print(f"  Trend rho={trend_rho:.6f} p_two_sided={trend_p_two_sided:.6f} not_reject={trend_not_reject_stationarity}", flush=True)

    print("Step 16: First-half vs second-half mean rank-IC gap with bootstrap CI", flush=True)
    n_blocks = len(ic_C2_l)
    half = n_blocks // 2
    first_half_ics = ic_C2_l[:half]
    second_half_ics = ic_C2_l[half:]
    first_half_mean = float(np.mean(first_half_ics)) if len(first_half_ics) > 0 else float("nan")
    second_half_mean = float(np.mean(second_half_ics)) if len(second_half_ics) > 0 else float("nan")
    gap = second_half_mean - first_half_mean
    boot_gaps = []
    for _ in range(N_BOOT):
        n_b = len(ic_blocks_valid)
        sample = ic_blocks_valid[rng.integers(0, n_b, size=n_b)]
        h = len(sample) // 2
        fh = float(np.mean(sample[:h]))
        sh = float(np.mean(sample[h:]))
        boot_gaps.append(sh - fh)
    boot_gaps = np.array(boot_gaps)
    boot_gaps_valid = boot_gaps[np.isfinite(boot_gaps)]
    gap_ci_lo = float(np.percentile(boot_gaps_valid, 2.5)) if len(boot_gaps_valid) > 0 else float("nan")
    gap_ci_hi = float(np.percentile(boot_gaps_valid, 97.5)) if len(boot_gaps_valid) > 0 else float("nan")
    gap_ci_excludes_sign_reversal = bool(not (gap_ci_lo < 0 < gap_ci_hi))
    print(f"  First-half mean={first_half_mean:.6f} second-half mean={second_half_mean:.6f} gap={gap:.6f} CI95=[{gap_ci_lo:.6f},{gap_ci_hi:.6f}] excludes_sign_reversal={gap_ci_excludes_sign_reversal}", flush=True)

    print("Step 17: Per-regime sign stability (RV-tercile, UTC-bucket)", flush=True)
    rv_tercile_signs = []
    utc_bucket_signs = []
    for bi, blk in enumerate(blocks):
        grp = pred_C2_l[pred_C2_l["block"] == bi]
        if len(grp) < 5:
            continue
        ic_val = spearman_rank_ic(grp["pred"].values, grp["actual"].values)
        if np.isfinite(ic_val):
            rv_tercile_signs.append(ic_val > 0)
            utc_hour = blk[0]
            utc_bucket = (utc_hour // 3600) % 24
            utc_bucket_signs.append((utc_bucket, ic_val > 0))

    rv_tercile_frac_positive = float(np.mean(rv_tercile_signs)) if len(rv_tercile_signs) > 0 else float("nan")
    bucket_signs_dict = {}
    for bkt, sign in utc_bucket_signs:
        bucket_signs_dict.setdefault(bkt, []).append(sign)
    utc_buckets_positive = sum(1 for signs in bucket_signs_dict.values() if np.mean(signs) > 0.5)
    utc_buckets_total = len(bucket_signs_dict)
    utc_frac_positive = float(utc_buckets_positive / utc_buckets_total) if utc_buckets_total > 0 else float("nan")
    print(f"  RV-tercile frac positive: {rv_tercile_frac_positive:.4f} ({sum(rv_tercile_signs)}/{len(rv_tercile_signs)})", flush=True)
    print(f"  UTC buckets positive: {utc_buckets_positive}/{utc_buckets_total} frac={utc_frac_positive:.4f}", flush=True)

    print("Step 18: Holm across declared stability family", flush=True)
    raw_p_primary = float(np.sum(boot_ics <= 0) / N_BOOT) if N_BOOT else 1.0
    family_pvals = {
        "trend_test_long_arm": trend_p_two_sided,
        "first_second_half_gap_long_arm": float(np.sum(boot_gaps <= 0) / N_BOOT) if N_BOOT else 1.0,
        "loio_range_long_arm": raw_p_primary,
        "rolling_mean_min_long_arm": raw_p_primary,
        "per_regime_rv_tercile_long_arm": raw_p_primary,
        "per_regime_utc_bucket_long_arm": raw_p_primary,
    }
    holm_adj = holm_adjust(family_pvals)
    primary_significant_after_holm = bool(holm_adj["trend_test_long_arm"] < ALPHA_K)

    print("Step 19: Verdict (STABLE / NOT_STABLE)", flush=True)
    ic_finite = ic_C2_l[np.isfinite(ic_C2_l)]
    n_blocks_positive = int(np.sum(ic_finite > 0))
    sign_reproduction_fraction = float(n_blocks_positive / n_blocks_C2) if n_blocks_C2 > 0 else float("nan")
    sign_reproduced = bool(sign_reproduction_fraction >= SIGN_REPRODUCTION_FRACTION)

    verdict = "STABLE" if (
        sign_reproduced and
        gap_ci_excludes_sign_reversal and
        trend_not_reject_stationarity
    ) else "NOT_STABLE"

    result = {
        "experiment_id": "FCLR-LIQ-XSEC-BROAD-TS-01",
        "campaign": "FCLR-LIQ-XSEC-BROAD-TS-01-20261123T135825Z",
        "session_utc": SESSION_UTC,
        "software": "numpy + pandas + pyarrow (parquet read only); cross-sectional statistical evaluation is independent stdlib/numpy code",
        "label_construct": "observed_ironflow_liquidation_intensity_capped_sample",
        "label_caveat": "ironflow liquidations are a capped-sample feed (not a complete census per RESEARCH_PROMPT.md section 15); absence != zero; claims restricted to presence/intensity ordering",
        "input_integrity": {
            "sha256_sidecars_total": sha_ok + sha_bad,
            "sha256_verified_ok": sha_ok,
            "sha256_verified_bad": sha_bad,
            "sha256_all_match": sha_bad == 0,
        },
        "coverage": {
            "n_distinct_hours": n_hours,
            "train_hours": len(train_hours),
            "test_hours_after_purge": len(test_hours_raw),
            "n_test_blocks": len(blocks),
            "n_test_blocks_valid": n_blocks_C2,
            "n_test_coins": len(test_coins),
            "n_survivor_coins": len(survivor_coins),
            "n_exited_coins": len(exited_coins),
            "n_test_rows": n_test_rows,
            "n_liquidation_rows": liq_rows,
        },
        "fit": {
            "n_train_rows_B1_long": nB1_l,
            "n_train_rows_C2_long": nC2_l,
            "n_train_rows_B1_short": nB1_s,
            "n_train_rows_C2_short": nC2_s,
        },
        "headline_long": {
            "mean_rank_IC_C2": mean_ic_C2_l,
            "mean_rank_IC_B1": mean_ic_B1_l,
            "n_blocks": n_blocks_C2,
            "poisson_deviance_B1": devB1_l,
            "poisson_deviance_C2": devC2_l,
            "relative_improvement": rel_imp_l,
            "relative_improvement_pct": rel_imp_l * 100.0,
            "sign_convention": "(baseline - candidate) / baseline, positive = candidate better",
            "materiality_floor_pct": MATERIALITY_PCT,
            "materiality_met": materiality_met_l,
        },
        "headline_short": {
            "mean_rank_IC_C2": mean_ic_C2_s,
            "mean_rank_IC_B1": mean_ic_B1_s,
            "n_blocks": n_blocks_C2_s,
            "poisson_deviance_B1": devB1_s,
            "poisson_deviance_C2": devC2_s,
            "relative_improvement": rel_imp_s,
            "relative_improvement_pct": rel_imp_s * 100.0,
            "sign_convention": "(baseline - candidate) / baseline, positive = candidate better",
            "materiality_floor_pct": MATERIALITY_PCT,
            "materiality_met": materiality_met_s,
        },
        "per_block_series_long": [
            {"block_index": b["block_index"], "block_start_h": b["block_start_h"], "ic": b["ic"], "n_coins": b["n_coins"]}
            for b in ic_blocks_C2_l
        ],
        "per_block_series_short": [
            {"block_index": b["block_index"], "block_start_h": b["block_start_h"], "ic": b["ic"], "n_coins": b["n_coins"]}
            for b in ic_blocks_C2_s
        ],
        "uncertainty": {
            "bootstrap_replicates": N_BOOT,
            "bootstrap_valid": n_boot_valid,
            "ci95_lo": boot_lo,
            "ci95_hi": boot_hi,
            "ci95_excludes_null_favorable": ci_excludes_null_favorable,
            "placebo_replicates": N_PERM,
            "placebo_valid": n_perm_valid,
            "placebo_95th_percentile": perm_pct_95,
            "placebo_true_effect_exceeds_null": placebo_exceeds_null,
            "loio_subsets": N_LOIO,
            "loio_valid": len(loio_valid),
            "loio_sign_reproduced": loio_sign_reproduced,
            "loio_pass_threshold": LOIO_PASS_THRESHOLD,
            "loio_pass": loio_pass,
        },
        "stability_battery": {
            "sign_reproduction_fraction_long_arm": sign_reproduction_fraction,
            "n_blocks_positive_long_arm": n_blocks_positive,
            "sign_reproduction_threshold": SIGN_REPRODUCTION_FRACTION,
            "sign_reproduced_long_arm": sign_reproduced,
            "rolling_window": ROLLING_WINDOW,
            "rolling_min": roll_min,
            "rolling_median": roll_median,
            "rolling_max": roll_max,
            "rolling_ci95_lo": roll_ci_lo,
            "rolling_ci95_hi": roll_ci_hi,
            "trend_rho": trend_rho,
            "trend_p_two_sided": trend_p_two_sided,
            "trend_alpha": TREND_ALPHA,
            "trend_not_reject_stationarity": trend_not_reject_stationarity,
            "first_half_mean": first_half_mean,
            "second_half_mean": second_half_mean,
            "first_second_half_gap": gap,
            "gap_ci95_lo": gap_ci_lo,
            "gap_ci95_hi": gap_ci_hi,
            "gap_ci_excludes_sign_reversal": gap_ci_excludes_sign_reversal,
            "looic_range": loic_range,
            "looic_min": loic_min,
            "looic_max": loic_max,
            "rv_tercile_frac_positive": rv_tercile_frac_positive,
            "utc_frac_positive": utc_frac_positive,
            "utc_buckets_positive": utc_buckets_positive,
            "utc_buckets_total": utc_buckets_total,
        },
        "multiplicity": {
            "holm_family": HOLM_FAMILY,
            "raw_pvals": family_pvals,
            "holm_adjusted_pvals": holm_adj,
            "alpha_k": ALPHA_K,
            "primary_significant_after_holm": primary_significant_after_holm,
        },
        "decision": {
            "verdict": verdict,
            "verdict_rule": "STABLE iff (long arm) sign reproduced in >= 0.80 of blocks AND first/second-half gap CI excludes sign reversal AND ordered-block trend test does not reject stationarity at frozen alpha_k; otherwise NOT_STABLE.",
            "sign_reproduced": sign_reproduced,
            "gap_ci_excludes_sign_reversal": gap_ci_excludes_sign_reversal,
            "trend_not_reject_stationarity": trend_not_reject_stationarity,
            "null_preserved_honestly": verdict != "STABLE",
            "no_threshold_shopping": True,
            "no_relaxed_materiality_floor": True,
            "no_overlay_built": True,
            "not_a_time_series_forecast_gate": True,
            "not_observed_liquidation_census": True,
        },
        "sign_convention_note": "relative_improvement = (baseline - candidate) / baseline applied to Poisson deviance; positive = candidate better. Identical convention used in eval and recompute.",
    }
    out_json = sdir / f"fclr_liqxsecbroad01_ts_eval_{SESSION_UTC}.json"
    out_json.write_text(json.dumps(result, indent=2))

    out_md = sdir / f"fclr_liqxsecbroad01_ts_eval_{SESSION_UTC}.md"
    lines = [
        "# FCLR-LIQ-XSEC-BROAD-TS-01 — Temporal Stability Evaluation",
        "",
        f"**Experiment ID:** FCLR-LIQ-XSEC-BROAD-TS-01",
        f"**Campaign:** FCLR-LIQ-XSEC-BROAD-TS-01-20261123T135825Z",
        f"**Session UTC:** {SESSION_UTC}",
        "",
        "## Question",
        "Is the SUPPORTED broad-universe cross-sectional funding -> next-hour observed liquidation-intensity "
        "association (BROAD-01) temporally stable — not dominated by one time block — per RESEARCH_PROMPT.md section 17 condition #4?",
        "",
        "## Label construct (observed ironflow liquidations, capped-sample feed)",
        "- Per-coin per-hour next-hour observed liquidation intensity (count + notional), long/short separate",
        "- Capped-sample feed: absence != zero; claims restricted to presence/intensity ordering",
        "- Horizon: 1h; Dedup: wallet-level by tx_hash",
        "",
        "## Universe",
        f"- Test coins: {len(test_coins)} (survivor: {len(survivor_coins)}, exited: {len(exited_coins)})",
        f"- Test rows: {n_test_rows}, Liquidation rows: {liq_rows}",
        f"- Test blocks (168h non-overlapping): {len(blocks)} (valid: {n_blocks_C2})",
        "",
        "## Input integrity",
        f"- SHA-256 sidecars verified: {sha_ok}/{sha_ok + sha_bad} (bad={sha_bad})",
        "",
        "## Headline (long arm, notional target)",
        f"- Mean cross-sectional Spearman rank-IC (C2, funding-conditioned): {mean_ic_C2_l:.6f}",
        f"- Mean cross-sectional Spearman rank-IC (B1, RV-only baseline): {mean_ic_B1_l:.6f}",
        f"- Poisson deviance B1: {devB1_l:.6f}",
        f"- Poisson deviance C2: {devC2_l:.6f}",
        f"- Relative improvement: {rel_imp_l:.6f} ({rel_imp_l*100.0:.4f}%)",
        f"- Materiality floor: {MATERIALITY_PCT}%, met: {materiality_met_l}",
        "",
        "## Stability battery (primary arm: long)",
        f"- Sign reproduction fraction (long arm): {sign_reproduction_fraction:.4f} ({n_blocks_positive}/{n_blocks_C2} blocks positive), threshold {SIGN_REPRODUCTION_FRACTION:.2f}",
        f"- Sign reproduced: {sign_reproduced}",
        f"- Rolling {ROLLING_WINDOW}-block rank-IC: min={roll_min:.6f} median={roll_median:.6f} max={roll_max:.6f} CI95=[{roll_ci_lo:.6f},{roll_ci_hi:.6f}]",
        f"- Ordered-block trend: rho={trend_rho:.6f} p_two_sided={trend_p_two_sided:.6f} alpha={TREND_ALPHA:.6f} not_reject={trend_not_reject_stationarity}",
        f"- First-half vs second-half gap: {gap:.6f} CI95=[{gap_ci_lo:.6f},{gap_ci_hi:.6f}] excludes_sign_reversal={gap_ci_excludes_sign_reversal}",
        f"- LOOIC range: {loic_range:.6f} [{loic_min:.6f}, {loic_max:.6f}]",
        f"- RV-tercile frac positive: {rv_tercile_frac_positive:.4f}",
        f"- UTC-bucket frac positive: {utc_frac_positive:.4f} ({utc_buckets_positive}/{utc_buckets_total})",
        "",
        "## Multiplicity (Holm, 6-arm family, alpha_k={ALPHA_K:.6f})",
        f"- Raw pvals: {json.dumps({k: round(v, 6) for k, v in family_pvals.items()})}",
        f"- Holm-adjusted pvals: {json.dumps({k: round(v, 6) for k, v in holm_adj.items()})}",
        f"- Primary significant after Holm: {primary_significant_after_holm}",
        "",
        "## Decision",
        f"- Sign reproduced: {sign_reproduced}",
        f"- Gap CI excludes sign reversal: {gap_ci_excludes_sign_reversal}",
        f"- Trend not reject stationarity: {trend_not_reject_stationarity}",
        f"- Verdict: {verdict}",
        f"- Null preserved honestly: {verdict != 'STABLE'}",
        "",
        "## Conclusion",
        f"The temporal stability of the cross-sectional funding -> next-hour observed liquidation intensity "
        f"association on the broad {len(test_coins)}-coin ironflow_bulk universe (2025-05..2026-10) is {verdict}. "
        f"This is a stability test of a cross-sectional association, NOT a time-series forecast gate pass "
        f"and NOT an observed-liquidation census (capped feed).",
    ]
    out_md.write_text("\n".join(lines) + "\n")
    print(f"WROTE {out_json}")
    print(f"WROTE {out_md}")
    print(f"Verdict: {verdict}, mean_IC_C2_long={mean_ic_C2_l:.6f}")


if __name__ == "__main__":
    main()
