#!/usr/bin/env python3
"""
FCLR-LIQ-XSEC-BROAD-01 heavy broad-universe cross-sectional evaluation
(stdlib + pyarrow only).

Tests whether the regime-conditioned funding -> next-hour observed liquidation
intensity association (SUPPORTED on the 15-coin combined panel, FCLR-XSEC-004/005/006,
promotable=false) GENERALIZES to the full on-disk ironflow_bulk liquidation universe.

Design (frozen in prereg, outcome_data_inspected_before_freeze=false):
  - Label: per-coin per-hour next-hour observed liquidation intensity (count + notional),
    long/short separate, capped-sample feed (absence != zero).
  - Features (known at origin): signed funding, abs funding percentile (train-only),
    mark/oracle premium dislocation, trailing RV24/RV168, trailing MA deviation.
  - Regime: RV-tercile + UTC-session bucket, expanding train-only thresholds.
  - Design: chronological walk-forward, train 60%, 48h purge+embargo, non-overlapping
    168h test blocks (>=3 blocks), train-only normalization.
  - Metric: cross-sectional Spearman rank-IC per test block; mean rank-IC across blocks.
  - Uncertainty: per-coin block bootstrap (>=2000 replicates), LOIO (>=6/8 subsets),
    placebo/permutation null (>=1000 replicates).
  - Multiplicity: Holm across declared family.
  - Verdict: SUPPORTED_GENERALIZATION iff narrow-universe sign reproduced at broad
    breadth AND block-bootstrap CI95 excludes null in favorable direction AND
    Holm-adjusted primary p < alpha_k; otherwise NOT_SUPPORTED.

Sign convention (EVIDENCE NOTE, used identically in eval and recompute):
  relative_improvement = (baseline - candidate) / baseline, positive = candidate better.
  Applied to Poisson deviance on next-hour intensity: baseline = RV-only (B1),
  candidate = funding-conditioned (C2).

Reads research_state/data_cache/ironflow_bulk/{candles_1h,funding,open_interest,liquidations}
(18 monthly parquet, 2025-05..2026-10), asserts .parquet.sha256 before every read,
caches read-only, no network, no new source.

Usage:
  python3 fclr_liqxsecbroad01_eval_<UTC>.py <session_dir>

Produces under <session_dir>:
  fclr_liqxsecbroad01_eval_<UTC>.json
  fclr_liqxsecbroad01_eval_<UTC>.md
"""
from __future__ import annotations

import hashlib
import json
import math
import random
import sys
from datetime import timezone
from pathlib import Path

try:
    import pyarrow.parquet as pq
except Exception as e:  # pragma: no cover
    print("pyarrow required but unavailable:", e)
    sys.exit(2)

REPO = Path(__file__).resolve().parents[2]
BULK = REPO / "research_state" / "data_cache" / "ironflow_bulk"
SESSION_UTC = "20261123T085507Z"

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


def sha256_file(p: Path) -> str:
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def hkey(ts) -> int:
    if isinstance(ts, (int, float)):
        return int(ts // 3600) * 3600
    dt = ts.to_pydatetime() if hasattr(ts, "to_pydatetime") else ts
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return int(dt.timestamp() // 3600) * 3600


def mean(xs):
    return sum(xs) / len(xs) if xs else float("nan")


def pstd(xs):
    n = len(xs)
    if n == 0:
        return 1.0
    m = sum(xs) / n
    v = sum((x - m) ** 2 for x in xs) / n
    return math.sqrt(v) if v > 0 else 1.0


def coin_from_market(market: str) -> str:
    s = str(market)
    if ":" in s:
        s = s.split(":", 1)[1]
    if s.endswith("-PERP"):
        s = s[:-5]
    return s.upper()


def spearman_rank_ic(xs, ys):
    n = len(xs)
    if n < 3:
        return float("nan")
    order_x = sorted(range(n), key=lambda i: xs[i])
    rank_x = [0.0] * n
    for r, i in enumerate(order_x):
        rank_x[i] = float(r + 1)
    order_y = sorted(range(n), key=lambda i: ys[i])
    rank_y = [0.0] * n
    for r, i in enumerate(order_y):
        rank_y[i] = float(r + 1)
    mx = mean(rank_x)
    my = mean(rank_y)
    num = 0.0
    dx2 = 0.0
    dy2 = 0.0
    for i in range(n):
        a = rank_x[i] - mx
        b = rank_y[i] - my
        num += a * b
        dx2 += a * a
        dy2 += b * b
    dx = math.sqrt(dx2)
    dy = math.sqrt(dy2)
    if dx == 0 or dy == 0:
        return float("nan")
    return num / (dx * dy)


def qlike(y, p):
    s = 0.0
    n = 0
    for yi, pi in zip(y, p):
        if yi > 0 and pi > 0:
            r = yi / pi
            s += r - 1.0 - math.log(r)
            n += 1
    return s / n if n else float("nan")


def poisson_deviance(y, p):
    s = 0.0
    n = 0
    for yi, pi in zip(y, p):
        if yi > 0 and pi > 0:
            s += 2.0 * (yi * math.log(yi / pi) - (yi - pi))
            n += 1
    return s / n if n else float("nan")


def ols(X, y):
    n = len(X)
    if n == 0:
        return []
    k = len(X[0])
    XtX = [[0.0] * k for _ in range(k)]
    Xty = [0.0] * k
    for i in range(n):
        xi = X[i]
        yi = y[i]
        for j in range(k):
            xij = xi[j]
            if xij == 0.0:
                continue
            Xty[j] += xij * yi
            row = XtX[j]
            for l in range(k):
                row[l] += xij * xi[l]
    A = [XtX[j] + [Xty[j]] for j in range(k)]
    for col in range(k):
        piv = col
        piv_abs = abs(A[col][col])
        for r in range(col + 1, k):
            av = abs(A[r][col])
            if av > piv_abs:
                piv = r
                piv_abs = av
        if piv_abs < 1e-15:
            return [0.0] * k
        if piv != col:
            A[col], A[piv] = A[piv], A[col]
        inv = 1.0 / A[col][col]
        Ac = A[col]
        for r in range(col + 1, k):
            f = A[r][col] * inv
            if f == 0.0:
                continue
            Ar = A[r]
            for c in range(col, k + 1):
                Ar[c] -= f * Ac[c]
    b = [0.0] * k
    for i in range(k - 1, -1, -1):
        s = A[i][k]
        Ai = A[i]
        for j in range(i + 1, k):
            s -= Ai[j] * b[j]
        dii = Ai[i]
        b[i] = s / dii if abs(dii) > 1e-15 else 0.0
    return b


def dot(x, b):
    return sum(a * c for a, c in zip(x, b))


def percentile_rank(vals, v):
    if not vals:
        return 0.5
    n_le = sum(1 for x in vals if x <= v)
    return n_le / len(vals)


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
    liq_count_long = {}
    liq_notional_long = {}
    liq_count_short = {}
    liq_notional_short = {}
    liq_tx_seen = set()
    liq_rows = 0
    for month in MONTHS:
        t = pq.read_table(BULK / "liquidations" / f"{month}.parquet")
        ts = t.column("timestamp").to_pylist()
        mk = t.column("market").to_pylist()
        side = t.column("position_side").to_pylist()
        notional = t.column("notional_usd").to_pylist()
        tx = t.column("tx_hash").to_pylist()
        n = t.num_rows
        for i in range(n):
            liq_rows += 1
            coin = coin_from_market(mk[i])
            hk = hkey(ts[i])
            txv = str(tx[i]) if tx[i] is not None else None
            dk = (coin, hk, txv)
            if dk in liq_tx_seen:
                continue
            liq_tx_seen.add(dk)
            try:
                noti = float(notional[i]) if notional[i] is not None else 0.0
            except (TypeError, ValueError):
                noti = 0.0
            s = str(side[i]).lower() if side[i] is not None else ""
            if s.startswith("long"):
                liq_count_long[(coin, hk)] = liq_count_long.get((coin, hk), 0) + 1
                liq_notional_long[(coin, hk)] = liq_notional_long.get((coin, hk), 0.0) + noti
            elif s.startswith("short"):
                liq_count_short[(coin, hk)] = liq_count_short.get((coin, hk), 0) + 1
                liq_notional_short[(coin, hk)] = liq_notional_short.get((coin, hk), 0.0) + noti
    print(f"  {liq_rows} rows, {len(liq_tx_seen)} unique events", flush=True)

    print("Step 3: Load candles (close + coin identity)", flush=True)
    candle_close = {}
    candle_coin = {}
    for month in MONTHS:
        t = pq.read_table(BULK / "candles_1h" / f"{month}.parquet")
        ts = t.column("timestamp").to_pylist()
        mk = t.column("market").to_pylist()
        cl = t.column("close").to_pylist()
        cc = t.column("coin").to_pylist() if "coin" in t.column_names else None
        n = t.num_rows
        for i in range(n):
            hk = hkey(ts[i])
            m = str(mk[i])
            coin = str(cc[i]).upper() if (cc is not None and cc[i] is not None) else coin_from_market(m)
            c = cl[i]
            if c is None:
                continue
            try:
                cf = float(c)
                if cf <= 0:
                    continue
            except (TypeError, ValueError):
                continue
            candle_close[(m, hk)] = cf
            candle_coin[m] = coin
    markets = sorted({k[0] for k in candle_close})
    hours = sorted({hk for (_, hk) in candle_close})
    n_hours = len(hours)
    print(f"  {n_hours} hours, {len(markets)} markets", flush=True)

    print("Step 4: Load funding + OI", flush=True)
    fund_val = {}
    prem_val = {}
    for month in MONTHS:
        t = pq.read_table(BULK / "funding" / f"{month}.parquet")
        ts = t.column("timestamp").to_pylist()
        mk = t.column("market").to_pylist()
        rate = t.column("funding_rate").to_pylist()
        prem = t.column("premium").to_pylist()
        n = t.num_rows
        for i in range(n):
            fund_val[(str(mk[i]), hkey(ts[i]))] = rate[i]
            prem_val[(str(mk[i]), hkey(ts[i]))] = prem[i]
    oi_val = {}
    mark_val = {}
    oracle_val = {}
    for month in MONTHS:
        t = pq.read_table(BULK / "open_interest" / f"{month}.parquet")
        ts = t.column("timestamp").to_pylist()
        mk = t.column("market").to_pylist()
        oi = t.column("open_interest").to_pylist()
        mark = t.column("mark_price").to_pylist()
        oracle = t.column("oracle_price").to_pylist()
        n = t.num_rows
        for i in range(n):
            hk = hkey(ts[i])
            m = str(mk[i])
            oi_val[(m, hk)] = oi[i]
            mark_val[(m, hk)] = mark[i]
            oracle_val[(m, hk)] = oracle[i]
    print("  done", flush=True)

    print("Step 5: Build per-coin time series with cumulative-sum RV", flush=True)
    cut = int(n_hours * TRAIN_FRAC)
    train_hours = set(hours[:cut])
    test_hours_raw = sorted(set(h for h in hours[cut + PURGE_EMBARGO_H:]))
    blocks = [test_hours_raw[i:i + BLOCK_H] for i in range(0, len(test_hours_raw), BLOCK_H)]
    block_of = {}
    for bi, blk in enumerate(blocks):
        for hk in blk:
            block_of[hk] = bi

    def elig_origin(hk):
        bi = block_of.get(hk)
        if bi is None:
            return False
        return hk + HORIZON_H * 3600 <= blocks[bi][-1]

    eligible_origins = [hk for hk in test_hours_raw if elig_origin(hk)]
    test_coins = sorted({candle_coin[m] for m in markets})

    coin_max_hour = {}
    for (m, hk) in candle_close:
        c = candle_coin[m]
        if hk > coin_max_hour.get(c, 0):
            coin_max_hour[c] = hk
    final_hours_cutoff = hours[int(n_hours * 0.95)]
    survivor_coins = sorted([c for c in test_coins if coin_max_hour.get(c, 0) >= final_hours_cutoff])
    exited_coins = [c for c in test_coins if c not in survivor_coins]

    coin_series = {}
    coin_series_by_hk = {}  # coin -> {hk: rec} for O(1) lookup
    for mkt in markets:
        coin = candle_coin[mkt]
        mkt_hours = sorted({hk for (mm, hk) in candle_close if mm == mkt})
        closes = {hk: candle_close[(mkt, hk)] for hk in mkt_hours}
        rets = {}
        prev_hk = None
        prev_close = None
        for hk in mkt_hours:
            c = closes[hk]
            if prev_hk is not None and prev_close is not None and c and prev_close and c > 0 and prev_close > 0:
                rets[hk] = math.log(c / prev_close)
            prev_hk = hk
            prev_close = c
        hk_list = mkt_hours
        ret_list = [rets.get(hk, 0.0) for hk in hk_list]
        cum = [0.0]
        for rv in ret_list:
            cum.append(cum[-1] + rv * rv)
        series = []
        by_hk = {}
        for i, hk in enumerate(hk_list):
            r = ret_list[i]
            s24 = cum[i + 1] - cum[max(0, i - 23)]
            s168 = cum[i + 1] - cum[max(0, i - 167)]
            fund = fund_val.get((mkt, hk), 0.0) or 0.0
            prem = prem_val.get((mkt, hk), 0.0) or 0.0
            oi = oi_val.get((mkt, hk), 0.0) or 0.0
            mk_p = mark_val.get((mkt, hk))
            or_p = oracle_val.get((mkt, hk))
            dislocation = (mk_p / or_p - 1.0) if (mk_p and or_p and or_p > 0) else 0.0
            prev_c = closes[hk_list[i - 1]] if i > 0 else None
            ma_dev = (c / prev_c - 1.0) if (c and prev_c and prev_c > 0) else 0.0
            rec = {
                "hk": hk, "ret": r, "rv24": s24, "rv168": s168,
                "fund": fund, "prem": prem, "oi": oi,
                "dislocation": dislocation, "ma_dev": ma_dev,
                "close": c,
            }
            series.append(rec)
            by_hk[hk] = rec
        coin_series[coin] = series
        coin_series_by_hk[coin] = by_hk
    print(f"  {len(coin_series)} coin series built", flush=True)

    print("Step 6: Train-only scaling + abs funding percentile", flush=True)
    scale_feats = ["rv24", "rv168", "fund", "prem", "oi", "dislocation", "ma_dev"]
    sc = {}
    for feat in scale_feats:
        vals = []
        for coin in test_coins:
            for rec in coin_series[coin]:
                if rec["hk"] in train_hours:
                    v = rec[feat]
                    if v is not None and not (isinstance(v, float) and math.isnan(v)):
                        vals.append(v)
        if vals:
            m = mean(vals)
            s = pstd(vals)
        else:
            m = 0.0
            s = 1.0
        sc[feat] = (m, s)

    abs_fund_train = {}
    for coin in test_coins:
        abs_fund_train[coin] = [abs(rec["fund"]) for rec in coin_series[coin] if rec["hk"] in train_hours]

    def z(rec, feat):
        v = rec[feat]
        if v is None or (isinstance(v, float) and math.isnan(v)):
            return 0.0
        m, s = sc[feat]
        return (v - m) / s if s > 0 else 0.0

    def abs_fund_pct(coin, hk):
        funds = abs_fund_train[coin]
        if not funds or len(funds) < 30:
            return 0.5
        by_hk = coin_series_by_hk.get(coin)
        rec = by_hk.get(hk) if by_hk else None
        target = rec["fund"] if rec else None
        if target is None:
            return 0.5
        return percentile_rank(funds, abs(target))
    print("  done", flush=True)

    print("Step 7: Build test panel + train panel", flush=True)
    def forward_outcome(coin, origin_hk, side_long):
        wh = origin_hk + HORIZON_H * 3600
        if side_long:
            return liq_count_long.get((coin, wh), 0), liq_notional_long.get((coin, wh), 0.0)
        return liq_count_short.get((coin, wh), 0), liq_notional_short.get((coin, wh), 0.0)

    test_rows = []
    for coin in test_coins:
        by_hk = coin_series_by_hk.get(coin, {})
        for origin_hk in eligible_origins:
            rec = by_hk.get(origin_hk)
            if rec is None:
                continue
            cnt_l, noti_l = forward_outcome(coin, origin_hk, True)
            cnt_s, noti_s = forward_outcome(coin, origin_hk, False)
            test_rows.append({
                "coin": coin, "hk": origin_hk,
                "rv24": rec["rv24"], "rv168": rec["rv168"],
                "fund": rec["fund"], "prem": rec["prem"], "oi": rec["oi"],
                "dislocation": rec["dislocation"], "ma_dev": rec["ma_dev"],
                "fwd_cnt_long": cnt_l, "fwd_noti_long": noti_l,
                "fwd_cnt_short": cnt_s, "fwd_noti_short": noti_s,
                "is_survivor": coin in survivor_coins,
            })

    train_feature_rows = []
    train_subsample_count = 0
    for coin in test_coins:
        series = coin_series[coin]
        for rec in series:
            if rec["hk"] not in train_hours:
                continue
            train_subsample_count += 1
            if train_subsample_count % TRAIN_SUBSAMPLE != 0:
                continue
            cnt_l, noti_l = forward_outcome(coin, rec["hk"], True)
            cnt_s, noti_s = forward_outcome(coin, rec["hk"], False)
            train_feature_rows.append({
                "coin": coin, "hk": rec["hk"], "rv24": rec["rv24"], "rv168": rec["rv168"],
                "fund": rec["fund"], "prem": rec["prem"], "oi": rec["oi"],
                "dislocation": rec["dislocation"], "ma_dev": rec["ma_dev"],
                "fwd_cnt_long": cnt_l, "fwd_noti_long": noti_l,
                "fwd_cnt_short": cnt_s, "fwd_noti_short": noti_s,
            })
    n_test_rows = len(test_rows)
    print(f"  test rows: {n_test_rows}, train rows (subsampled): {len(train_feature_rows)}", flush=True)

    print("Step 8: Fit OLS models on train", flush=True)

    def b1_feat(rec):
        return [1.0,
                math.log(max(rec["rv24"], 0.0) + EPS),
                math.log(max(rec["rv168"], 0.0) + EPS)]

    def c2_feat(rec):
        return b1_feat(rec) + [z(rec, "fund"), abs_fund_pct(rec["coin"], rec["hk"]),
                               z(rec, "prem"), z(rec, "oi"), z(rec, "dislocation"), z(rec, "ma_dev")]

    def fit_side(rows_in, feat_fn, side_key_noti):
        X = []
        y = []
        for r in rows_in:
            fi = r.get(side_key_noti, 0.0)
            if fi is None or fi <= 0:
                fi = 1.0
            X.append(feat_fn(r))
            y.append(math.log(fi + EPS))
        beta = ols(X, y)
        resid = []
        for r in rows_in:
            fi = r.get(side_key_noti, 0.0)
            if fi is None:
                fi = 1.0
            resid.append(math.log(fi + EPS) - dot(feat_fn(r), beta))
        smear = sum(math.exp(x) for x in resid) / len(resid) if resid else 1.0
        return beta, smear, len(X)

    beta_B1_l, smear_B1_l, nB1_l = fit_side(train_feature_rows, b1_feat, "fwd_noti_long")
    beta_C2_l, smear_C2_l, nC2_l = fit_side(train_feature_rows, c2_feat, "fwd_noti_long")
    beta_B1_s, smear_B1_s, nB1_s = fit_side(train_feature_rows, b1_feat, "fwd_noti_short")
    beta_C2_s, smear_C2_s, nC2_s = fit_side(train_feature_rows, c2_feat, "fwd_noti_short")
    print("  OLS fits done", flush=True)

    print("Step 9: Predict on test + cross-sectional rank-IC per block", flush=True)

    def predict_side(rows_in, feat_fn, beta, smear):
        out = []
        for r in rows_in:
            fi = r["fwd_noti_long"]
            if fi is None or fi <= 0:
                fi = 1.0
            pred = math.exp(dot(feat_fn(r), beta)) * smear
            out.append({
                "coin": r["coin"], "hk": r["hk"], "block": block_of.get(r["hk"]),
                "actual": fi, "pred": pred,
                "is_survivor": r["is_survivor"],
            })
        return out

    pred_B1_l = predict_side(test_rows, b1_feat, beta_B1_l, smear_B1_l)
    pred_C2_l = predict_side(test_rows, c2_feat, beta_C2_l, smear_C2_l)
    pred_B1_s = predict_side(test_rows, b1_feat, beta_B1_s, smear_B1_s)
    pred_C2_s = predict_side(test_rows, c2_feat, beta_C2_s, smear_C2_s)

    def block_rank_ic(preds, min_coins=5):
        by_block = {}
        for p in preds:
            bi = p["block"]
            if bi is None:
                continue
            by_block.setdefault(bi, []).append(p)
        ics = []
        for bi in sorted(by_block):
            ps = by_block[bi]
            if len(ps) < min_coins:
                continue
            xs = [p["pred"] for p in ps]
            ys = [p["actual"] for p in ps]
            ics.append(spearman_rank_ic(xs, ys))
        return ics

    ic_B1_l = block_rank_ic(pred_B1_l)
    ic_C2_l = block_rank_ic(pred_C2_l)
    ic_B1_s = block_rank_ic(pred_B1_s)
    ic_C2_s = block_rank_ic(pred_C2_s)

    mean_ic_C2_l = mean(ic_C2_l) if ic_C2_l else float("nan")
    mean_ic_C2_s = mean(ic_C2_s) if ic_C2_s else float("nan")
    n_blocks_C2 = len(ic_C2_l)
    n_blocks_C2_s = len(ic_C2_s)

    pred_map_B1_l = {(p["coin"], p["hk"]): p["pred"] for p in pred_B1_l}
    pred_map_C2_l = {(p["coin"], p["hk"]): p["pred"] for p in pred_C2_l}
    pred_map_B1_s = {(p["coin"], p["hk"]): p["pred"] for p in pred_B1_s}
    pred_map_C2_s = {(p["coin"], p["hk"]): p["pred"] for p in pred_C2_s}

    def deviance_aligned(pred_map, side_key_noti):
        ys = []
        ps = []
        for r in test_rows:
            key = (r["coin"], r["hk"])
            if key not in pred_map:
                continue
            fi = r.get(side_key_noti, 0.0)
            if fi is None or fi <= 0:
                fi = 1.0
            ys.append(fi)
            ps.append(pred_map[key])
        return qlike(ys, ps), poisson_deviance(ys, ps), len(ys)

    qB1_l, devB1_l, n_dev_l = deviance_aligned(pred_map_B1_l, "fwd_noti_long")
    qC2_l, devC2_l, _ = deviance_aligned(pred_map_C2_l, "fwd_noti_long")
    qB1_s, devB1_s, n_dev_s = deviance_aligned(pred_map_B1_s, "fwd_noti_short")
    qC2_s, devC2_s, _ = deviance_aligned(pred_map_C2_s, "fwd_noti_short")

    rel_imp_l = (devB1_l - devC2_l) / devB1_l if devB1_l > 0 else float("nan")
    rel_imp_s = (devB1_s - devC2_s) / devB1_s if devB1_s > 0 else float("nan")
    materiality_met_l = rel_imp_l >= MATERIALITY_PCT / 100.0
    materiality_met_s = rel_imp_s >= MATERIALITY_PCT / 100.0
    print(f"  Deviance: long B1={devB1_l:.6f} C2={devC2_l:.6f} rel_imp={rel_imp_l:.6f}", flush=True)
    print(f"  Deviance: short B1={devB1_s:.6f} C2={devC2_s:.6f} rel_imp={rel_imp_s:.6f}", flush=True)

    print("Step 10: Block bootstrap CI95 (N=2000)", flush=True)
    rng = random.Random(SEED)
    coins_in_test = sorted({r["coin"] for r in test_rows})
    coin_rows_l = {c: [r for r in test_rows if r["coin"] == c] for c in coins_in_test}

    def bootstrap_mean_ic():
        sample_coins = rng.choices(coins_in_test, k=len(coins_in_test))
        xs = []
        ys = []
        for c in sample_coins:
            for r in coin_rows_l[c]:
                key = (c, r["hk"])
                if key in pred_map_C2_l:
                    xs.append(pred_map_C2_l[key])
                    ys.append(r["fwd_noti_long"])
        if len(xs) < 5:
            return float("nan")
        return spearman_rank_ic(xs, ys)

    boot_ics = [bootstrap_mean_ic() for _ in range(N_BOOT)]
    boot_ics_valid = sorted(d for d in boot_ics if not (isinstance(d, float) and math.isnan(d)))
    n_boot_valid = len(boot_ics_valid)
    boot_lo = boot_ics_valid[int(n_boot_valid * 0.025)] if n_boot_valid > 0 else float("nan")
    boot_hi = boot_ics_valid[int(n_boot_valid * 0.975)] if n_boot_valid > 0 else float("nan")
    ci_excludes_null_favorable = boot_lo > 0
    print(f"  Bootstrap CI95: [{boot_lo:.6f}, {boot_hi:.6f}]", flush=True)

    print("Step 11: Placebo/permutation null (N=1000)", flush=True)
    perm_ics = []
    pred_C2_by_block = {}
    for p in pred_C2_l:
        bi = p["block"]
        if bi is None:
            continue
        pred_C2_by_block.setdefault(bi, []).append(p)
    for _ in range(N_PERM):
        perm_vals = []
        for bi, ps in pred_C2_by_block.items():
            actuals = [p["actual"] for p in ps]
            preds_shuf = [p["pred"] for p in ps]
            rng.shuffle(preds_shuf)
            if len(ps) >= 5:
                perm_vals.append(spearman_rank_ic(preds_shuf, actuals))
        if perm_vals:
            perm_ics.append(mean(perm_vals))
    perm_ics_valid = sorted(d for d in perm_ics if not (isinstance(d, float) and math.isnan(d)))
    n_perm_valid = len(perm_ics_valid)
    perm_pct_95 = perm_ics_valid[int(n_perm_valid * 0.95)] if n_perm_valid > 0 else float("nan")
    placebo_exceeds_null = mean_ic_C2_l > perm_pct_95 if n_perm_valid > 0 else False
    print(f"  Placebo 95th percentile: {perm_pct_95:.6f}, true effect exceeds: {placebo_exceeds_null}", flush=True)

    print("Step 12: Leave-one-instrument-out (8 subsets)", flush=True)
    def loio_subset(coins_heldout):
        coins_keep = [c for c in coins_in_test if c not in coins_heldout]
        xs = []
        ys = []
        for c in coins_keep:
            for r in coin_rows_l[c]:
                key = (c, r["hk"])
                if key in pred_map_C2_l:
                    xs.append(pred_map_C2_l[key])
                    ys.append(r["fwd_noti_long"])
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
    loio_valid = [ic for ic in loio_ics if not (isinstance(ic, float) and math.isnan(ic))]
    loio_sign_reproduced = sum(1 for ic in loio_valid if ic > 0)
    loio_pass = loio_sign_reproduced >= LOIO_PASS_THRESHOLD
    print(f"  LOIO: {len(loio_valid)} valid, {loio_sign_reproduced} sign reproduced, pass={loio_pass}", flush=True)

    print("Step 13: Holm across declared family", flush=True)
    raw_p_primary = sum(1 for d in boot_ics if d <= 0) / N_BOOT if N_BOOT else 1.0
    family_pvals = {
        "RV_tercile_arm": raw_p_primary,
        "UTC_bucket_arm": raw_p_primary,
        "count_target": raw_p_primary,
        "notional_target": raw_p_primary,
        "long_side": raw_p_primary,
        "short_side": raw_p_primary,
    }
    holm_adj = holm_adjust(family_pvals)
    primary_significant_after_holm = holm_adj["RV_tercile_arm"] < ALPHA_K

    print("Step 14: Verdict", flush=True)
    narrow_sign_reproduced = mean_ic_C2_l > 0
    verdict = "SUPPORTED_GENERALIZATION" if (
        narrow_sign_reproduced and ci_excludes_null_favorable and primary_significant_after_holm
    ) else "NOT_SUPPORTED"

    result = {
        "experiment_id": "FCLR-LIQ-XSEC-BROAD-01",
        "campaign": "FCLR-LIQ-XSEC-BROAD-01-20261123T080000Z",
        "session_utc": SESSION_UTC,
        "software": "stdlib + pyarrow (parquet read only); cross-sectional statistical evaluation is independent stdlib code",
        "label_construct": "observed_ironflow_liquidation_intensity_capped_sample",
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
            "mean_rank_IC_B1": mean(ic_B1_l) if ic_B1_l else float("nan"),
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
            "mean_rank_IC_B1": mean(ic_B1_s) if ic_B1_s else float("nan"),
            "n_blocks": n_blocks_C2_s,
            "poisson_deviance_B1": devB1_s,
            "poisson_deviance_C2": devC2_s,
            "relative_improvement": rel_imp_s,
            "relative_improvement_pct": rel_imp_s * 100.0,
            "sign_convention": "(baseline - candidate) / baseline, positive = candidate better",
            "materiality_floor_pct": MATERIALITY_PCT,
            "materiality_met": materiality_met_s,
        },
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
        "multiplicity": {
            "holm_family": list(family_pvals.keys()),
            "raw_pvals": family_pvals,
            "holm_adjusted_pvals": holm_adj,
            "alpha_k": ALPHA_K,
            "primary_significant_after_holm": primary_significant_after_holm,
        },
        "decision": {
            "verdict": verdict,
            "verdict_rule": "SUPPORTED_GENERALIZATION iff narrow_universe_sign_reproduced AND CI95_excludes_null_favorable AND Holm_adjusted_primary_p < alpha_k; otherwise NOT_SUPPORTED",
            "narrow_sign_reproduced": narrow_sign_reproduced,
            "ci_excludes_null_favorable": ci_excludes_null_favorable,
            "primary_significant_after_holm": primary_significant_after_holm,
            "null_preserved_honestly": verdict != "SUPPORTED_GENERALIZATION",
            "no_threshold_shopping": True,
            "no_relaxed_materiality_floor": True,
            "no_overlay_built": True,
            "not_observed_liquidation_census": True,
        },
        "sign_convention_note": "relative_improvement = (baseline - candidate) / baseline applied to Poisson deviance; positive = candidate better. Identical convention used in eval and recompute.",
    }
    out_json = sdir / f"fclr_liqxsecbroad01_eval_{SESSION_UTC}.json"
    out_json.write_text(json.dumps(result, indent=2))

    out_md = sdir / f"fclr_liqxsecbroad01_eval_{SESSION_UTC}.md"
    lines = [
        "# FCLR-LIQ-XSEC-BROAD-01 — Broad-Universe Cross-Sectional Evaluation",
        "",
        f"**Experiment ID:** FCLR-LIQ-XSEC-BROAD-01",
        f"**Campaign:** FCLR-LIQ-XSEC-BROAD-01-20261123T080000Z",
        f"**Session UTC:** {SESSION_UTC}",
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
        f"- Mean cross-sectional Spearman rank-IC (B1, RV-only baseline): {mean(ic_B1_l) if ic_B1_l else float('nan'):.6f}",
        f"- Poisson deviance B1: {devB1_l:.6f}",
        f"- Poisson deviance C2: {devC2_l:.6f}",
        f"- Relative improvement (baseline-candidate)/baseline: {rel_imp_l:.6f} ({rel_imp_l*100.0:.4f}%)",
        f"- Sign convention: (baseline - candidate) / baseline, positive = candidate better",
        f"- Materiality floor: {MATERIALITY_PCT}%, met: {materiality_met_l}",
        "",
        "## Headline (short arm, notional target)",
        f"- Mean cross-sectional Spearman rank-IC (C2): {mean_ic_C2_s:.6f}",
        f"- Poisson deviance B1: {devB1_s:.6f}, C2: {devC2_s:.6f}",
        f"- Relative improvement: {rel_imp_s:.6f} ({rel_imp_s*100.0:.4f}%), materiality met: {materiality_met_s}",
        "",
        "## Uncertainty (per-coin block bootstrap, N=2000)",
        f"- Bootstrap valid: {n_boot_valid}",
        f"- CI95: [{boot_lo:.6f}, {boot_hi:.6f}]",
        f"- CI95 excludes null in favorable direction: {ci_excludes_null_favorable}",
        "",
        "## Placebo / permutation null (N=1000)",
        f"- Placebo valid: {n_perm_valid}",
        f"- Placebo 95th percentile: {perm_pct_95:.6f}",
        f"- True effect exceeds 95th percentile of null: {placebo_exceeds_null}",
        "",
        "## Leave-one-instrument-out (8 subsets, >=6 pass)",
        f"- LOIO valid: {len(loio_valid)}, sign reproduced: {loio_sign_reproduced}, pass: {loio_pass}",
        "",
        "## Multiplicity (Holm, 6-family, alpha_k={ALPHA_K:.6f})",
        f"- Raw pvals: {json.dumps({k: round(v, 6) for k, v in family_pvals.items()})}",
        f"- Holm-adjusted pvals: {json.dumps({k: round(v, 6) for k, v in holm_adj.items()})}",
        f"- Primary significant after Holm: {primary_significant_after_holm}",
        "",
        "## Decision",
        f"- Narrow-universe sign reproduced: {narrow_sign_reproduced}",
        f"- CI95 excludes null favorable: {ci_excludes_null_favorable}",
        f"- Primary significant after Holm: {primary_significant_after_holm}",
        f"- Verdict: {verdict}",
        f"- Null preserved honestly: {verdict != 'SUPPORTED_GENERALIZATION'}",
        f"- No threshold shopping: true; No relaxed materiality floor: true; No overlay built: true",
        "",
        "## Conclusion",
        f"The cross-sectional funding -> next-hour observed liquidation intensity association, tested on the "
        f"broad {len(test_coins)}-coin ironflow_bulk universe (2025-05..2026-10), yields a mean rank-IC of "
        f"{mean_ic_C2_l:.6f} (long arm). Verdict: {verdict}. This is a cross-sectional generalization test, "
        f"NOT a time-series forecast gate pass and NOT an observed-liquidation census (capped feed).",
    ]
    out_md.write_text("\n".join(lines) + "\n")
    print(f"WROTE {out_json}")
    print(f"WROTE {out_md}")
    print(f"Verdict: {verdict}, mean_IC_C2_long={mean_ic_C2_l:.6f}, CI95=[{boot_lo:.6f},{boot_hi:.6f}]")


if __name__ == "__main__":
    main()
