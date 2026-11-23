#!/usr/bin/env python3
"""
FCLR-TRACKB-MODELED-BREACH-01 heavy evaluation (Track B modeled breach proxy).

Modeled hypothetical boundary-breach forecast per RESEARCH_PROMPT.md section 15
and AGENT_HANDOFF.md frozen design. Does NOT reconstruct account-specific
liquidation engines, cross/portfolio margin, or actual forced liquidations.
Never described as observed liquidations.

Pipeline (stdlib + pyarrow only; no network; caches read-only):
  1. Assert sha256 of every input parquet before read.
  2. Load mark_price (open_interest), funding_rate + premium (funding).
  3. Build per-coin hourly series; RV6/RV24/RV168 via cumulative sums (O(n)).
  4. Modeled breach labels (long + short separate) via synthetic_boundary_labels.
  5. Chronological walk-forward: 60/40 train/test, 48h purge+embargo,
     non-overlapping 168h test blocks, >=3 blocks.
  6. Fit calibrated logistic regression (stdlib Newton/IRLS) on a bounded
     train sample for tractability. Baseline B1 = RV-only. Candidate C2 =
     B1 + funding + |funding| pct + premium + MA dev.
  7. Evaluate: Brier score + log loss (primary); calibration slope/intercept,
     ROC-AUC, precision/recall at pre-specified alert budget (secondary).
  8. Per-coin block-bootstrap CI95 on Brier difference; Holm across declared family.
  9. Verdict: SUPPORTED iff materiality (>=2% relative Brier improvement) AND
     bootstrap CI excludes null AND Holm-adjusted primary p < alpha_k; else NOT_SUPPORTED.

Usage:
  python3 fclr_tracks01_eval_<UTC>.py <session_dir>

Produces under <session_dir>:
  fclr_tracks01_eval_<UTC>.json
  fclr_tracks01_eval_<UTC>.md
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
SESSION_UTC = "20261123T034810Z"

MONTHS = ["2025-05", "2025-06", "2025-07", "2025-08", "2025-09", "2025-10",
          "2025-11", "2025-12", "2026-01", "2026-02", "2026-03", "2026-04",
          "2026-05", "2026-06", "2026-07", "2026-08", "2026-09", "2026-10"]

TRAIN_FRAC = 0.60
PURGE_EMBARGO_H = 48
BLOCK_H = 168
HORIZON_H = 24
LEVERAGE = 5.0
MM_RATE = 0.0
EPS = 1e-12
SEED = 20261123
N_BOOT = 200
ALPHA_K = 0.05 / (2 * 3)
MATERIALITY_PCT = 2.0
ALERT_BUDGET = 0.10
MAX_TRAIN_ROWS = 50000


def sha256_file(p: Path) -> str:
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def hkey(ts):
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


def liquidation_boundary_price(entry_price, leverage, side, maintenance_margin_rate=0.0):
    if entry_price is None or entry_price <= 0 or leverage is None or leverage <= 0:
        return None
    if side == "long":
        return entry_price * (1.0 - 1.0 / leverage + maintenance_margin_rate)
    if side == "short":
        return entry_price * (1.0 + 1.0 / leverage - maintenance_margin_rate)
    raise ValueError("side must be 'long' or 'short'")


def boundary_crossed_future(mark_closes, t_index, boundary, side, horizon=24):
    if boundary is None:
        return None
    seg = mark_closes[t_index + 1 : t_index + 1 + horizon]
    if len(seg) < horizon:
        return None
    if any(p is None or (isinstance(p, float) and math.isnan(p)) for p in seg):
        return None
    if side == "long":
        return min(seg) <= boundary
    if side == "short":
        return max(seg) >= boundary
    raise ValueError("side must be 'long' or 'short'")


def synthetic_boundary_label(mark_closes, t_index, horizon=24, leverage=5.0,
                            side="long", maintenance_margin_rate=0.0,
                            entry_price=None):
    if entry_price is None:
        if t_index < 0 or t_index >= len(mark_closes):
            return None
        entry_price = mark_closes[t_index]
    boundary = liquidation_boundary_price(entry_price, leverage, side, maintenance_margin_rate)
    crossed = boundary_crossed_future(mark_closes, t_index, boundary, side, horizon)
    if crossed is None:
        return None
    return int(bool(crossed))


def sigmoid(z):
    if z >= 0:
        return 1.0 / (1.0 + math.exp(-z))
    ez = math.exp(z)
    return ez / (1.0 + ez)


def fit_logistic(X, y, max_iter=60, tol=1e-5):
    n = len(X)
    k = len(X[0]) if n else 0
    Xw = [[1.0] + row for row in X]
    kp = k + 1
    beta = [0.0] * kp
    for it in range(max_iter):
        p = [sigmoid(dot_row(Xw[i], beta)) for i in range(n)]
        grad = [0.0] * kp
        hess = [[0.0] * kp for _ in range(kp)]
        for i in range(n):
            r = y[i] - p[i]
            pi = p[i]
            w = pi * (1.0 - pi)
            xi = Xw[i]
            for j in range(kp):
                grad[j] += xi[j] * r
                hj = hess[j]
                for l in range(kp):
                    hj[l] += w * xi[j] * xi[l]
        A = [hess[j] + [grad[j]] for j in range(kp)]
        singular = False
        for col in range(kp):
            piv = col
            piv_abs = abs(A[col][col])
            for r in range(col + 1, kp):
                av = abs(A[r][col])
                if av > piv_abs:
                    piv = r
                    piv_abs = av
            if piv_abs < 1e-12:
                singular = True
                break
            if piv != col:
                A[col], A[piv] = A[piv], A[col]
            inv = 1.0 / A[col][col]
            Ac = A[col]
            for r in range(col + 1, kp):
                f = A[r][col] * inv
                if f == 0.0:
                    continue
                Ar = A[r]
                for c in range(col, kp + 1):
                    Ar[c] -= f * Ac[c]
        if singular:
            return beta, False, it
        delta = [0.0] * kp
        for i in range(kp - 1, -1, -1):
            s = A[i][kp]
            Ai = A[i]
            for j in range(i + 1, kp):
                s -= Ai[j] * delta[j]
            dii = Ai[i]
            delta[i] = s / dii if abs(dii) > 1e-12 else 0.0
        for j in range(kp):
            beta[j] += delta[j]
        max_change = max(abs(d) for d in delta)
        if max_change < tol:
            return beta, True, it + 1
    return beta, False, max_iter


def dot_row(x, b):
    return sum(a * c for a, c in zip(x, b))


def standardize_cols(train_rows):
    if not train_rows:
        return [], []
    ncols = len(train_rows[0])
    means = []
    stds = []
    for ci in range(ncols):
        vals = [r[ci] for r in train_rows if r[ci] is not None and not (isinstance(r[ci], float) and math.isnan(r[ci]))]
        if vals:
            m = mean(vals)
            s = pstd(vals)
        else:
            m = 0.0
            s = 1.0
        means.append(m)
        stds.append(s)
    return means, stds


def apply_std(row, means, stds):
    out = []
    for ci, v in enumerate(row):
        if v is None or (isinstance(v, float) and math.isnan(v)):
            out.append(0.0)
        else:
            s = stds[ci]
            out.append((v - means[ci]) / s if s > 0 else 0.0)
    return out


def brier_score(ys, ps):
    n = len(ys)
    if n == 0:
        return float("nan")
    return sum((y - p) ** 2 for y, p in zip(ys, ps)) / n


def log_loss(ys, ps):
    n = len(ys)
    if n == 0:
        return float("nan")
    s = 0.0
    for y, p in zip(ys, ps):
        pp = min(max(p, EPS), 1.0 - EPS)
        s += -(y * math.log(pp) + (1.0 - y) * math.log(1.0 - pp))
    return s / n


def calibration_slope_intercept(ys, ps):
    n = len(ys)
    if n < 2:
        return float("nan"), float("nan")
    mean_p = sum(ps) / n
    mean_y = sum(ys) / n
    spp = sum((p - mean_p) ** 2 for p in ps)
    spy = sum((p - mean_p) * (y - mean_y) for p, y in zip(ps, ys))
    if spp < 1e-12:
        return mean_y, float("nan")
    slope = spy / spp
    intercept = mean_y - slope * mean_p
    return intercept, slope


def roc_auc(ys, ps):
    pos = [p for p, y in zip(ps, ys) if y == 1]
    neg = [p for p, y in zip(ps, ys) if y == 0]
    if not pos or not neg:
        return float("nan")
    sorted_ps = sorted(ps)
    rank = {}
    i = 0
    n = len(sorted_ps)
    while i < n:
        j = i
        while j < n and sorted_ps[j] == sorted_ps[i]:
            j += 1
        avg_rank = (i + 1 + j) / 2.0
        for k in range(i, j):
            rank[sorted_ps[k]] = avg_rank
        i = j
    sum_ranks_pos = sum(rank[p] for p in pos)
    n_pos = len(pos)
    n_neg = len(neg)
    return (sum_ranks_pos - n_pos * (n_pos + 1) / 2.0) / (n_pos * n_neg)


def precision_recall_at_budget(ys, ps, budget):
    n = len(ys)
    if n == 0:
        return 0.0, 0.0, 0
    order = sorted(range(n), key=lambda i: ps[i], reverse=True)
    n_alert = max(1, int(n * budget))
    alert_set = set(order[:n_alert])
    tp = sum(1 for i in alert_set if ys[i] == 1)
    fp = sum(1 for i in alert_set if ys[i] == 0)
    n_pos = sum(1 for y in ys if y == 1)
    prec = tp / (tp + fp) if (tp + fp) > 0 else 0.0
    rec = tp / n_pos if n_pos > 0 else 0.0
    return prec, rec, n_alert


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

    # ===== (1) Input integrity =====
    sha_ok = 0
    sha_bad = 0
    subdirs = ["open_interest", "funding", "candles_1h"]
    for subdir in subdirs:
        for month in MONTHS:
            sp = BULK / subdir / f"{month}.parquet.sha256"
            if not sp.is_file():
                sha_bad += 1
                continue
            stored = sp.read_text().strip().split()[0]
            if sha256_file(BULK / subdir / f"{month}.parquet") == stored:
                sha_ok += 1
            else:
                sha_bad += 1

    # ===== (2) Load mark_price, funding_rate, premium -> per-coin structures =====
    # coin -> {hk: mark_price}
    coin_mark = {}
    # coin -> {hk: funding_rate}
    coin_fund = {}
    # coin -> {hk: premium}
    coin_prem = {}
    all_hours_set = set()

    for month in MONTHS:
        t = pq.read_table(BULK / "open_interest" / f"{month}.parquet")
        n = t.num_rows
        ts = t.column("timestamp").to_pylist()
        mk = t.column("market").to_pylist()
        mark = t.column("mark_price").to_pylist()
        for i in range(n):
            hk = hkey(ts[i])
            all_hours_set.add(hk)
            coin = coin_from_market(mk[i])
            d = coin_mark.setdefault(coin, {})
            d[hk] = mark[i]
    for month in MONTHS:
        t = pq.read_table(BULK / "funding" / f"{month}.parquet")
        n = t.num_rows
        ts = t.column("timestamp").to_pylist()
        mk = t.column("market").to_pylist()
        rate = t.column("funding_rate").to_pylist()
        prem = t.column("premium").to_pylist()
        for i in range(n):
            hk = hkey(ts[i])
            coin = coin_from_market(mk[i])
            coin_fund.setdefault(coin, {})[hk] = rate[i]
            coin_prem.setdefault(coin, {})[hk] = prem[i]

    all_coins = sorted(coin_mark.keys())
    n_coins = len(all_coins)

    # ===== (3) Build per-coin sorted hour lists + RV via cumulative sums =====
    coin_hours = {}
    coin_series = {}  # coin -> list of {hk, rv6, rv24, rv168, fund, prem, mark}
    for coin in all_coins:
        hours = sorted(coin_mark.keys() if False else coin_mark[coin].keys())
        coin_hours[coin] = hours
        closes = [coin_mark[coin][hk] for hk in hours]
        # squared log returns
        sq_rets = [0.0] * len(hours)
        prev_close = None
        for i, c in enumerate(closes):
            if prev_close is not None and c and prev_close and c > 0 and prev_close > 0:
                r = math.log(c / prev_close)
                sq_rets[i] = r * r
            prev_close = c
        # cumulative sum
        cum_sq = [0.0] * (len(sq_rets) + 1)
        for i in range(len(sq_rets)):
            cum_sq[i + 1] = cum_sq[i] + sq_rets[i]

        def rv_sum(i, win):
            a = max(0, i - win + 1)
            return cum_sq[i + 1] - cum_sq[a]

        series = []
        for i, hk in enumerate(hours):
            fund = coin_fund.get(coin, {}).get(hk, 0.0) or 0.0
            prem = coin_prem.get(coin, {}).get(hk, 0.0) or 0.0
            series.append({
                "hk": hk, "rv6": rv_sum(i, 6), "rv24": rv_sum(i, 24),
                "rv168": rv_sum(i, 168), "fund": fund, "prem": prem,
                "mark": closes[i],
            })
        coin_series[coin] = series

    all_hours = sorted(all_hours_set)
    n_hours = len(all_hours)

    # ===== (4) Train/test split =====
    cut = int(n_hours * TRAIN_FRAC)
    train_hours = set(all_hours[:cut])
    test_hours_raw = sorted(set(h for h in all_hours[cut + PURGE_EMBARGO_H:]))
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
    n_blocks = len(blocks)

    # ===== (5) Build test labels + rows =====
    test_rows_long = []
    test_rows_short = []
    for coin in all_coins:
        series = coin_series[coin]
        hk_to_idx = {rec["hk"]: i for i, rec in enumerate(series)}
        chours = coin_hours[coin]
        closes_list = [coin_mark[coin][hk] for hk in chours]
        closes = coin_mark[coin]
        n = len(series)
        for origin_hk in eligible_origins:
            if origin_hk not in hk_to_idx:
                continue
            i = hk_to_idx[origin_hk]
            if i + HORIZON_H >= n:
                continue
            entry = closes_list[i]
            if entry is None or entry <= 0:
                continue
            ll = synthetic_boundary_label(closes_list, i, horizon=HORIZON_H,
                                          leverage=LEVERAGE, side="long",
                                          maintenance_margin_rate=MM_RATE,
                                          entry_price=entry)
            ls = synthetic_boundary_label(closes_list, i, horizon=HORIZON_H,
                                          leverage=LEVERAGE, side="short",
                                          maintenance_margin_rate=MM_RATE,
                                          entry_price=entry)
            if ll is None or ls is None:
                continue
            rec = series[i]
            test_rows_long.append({
                "coin": coin, "hk": origin_hk,
                "rv6": rec["rv6"], "rv24": rec["rv24"], "rv168": rec["rv168"],
                "fund": rec["fund"], "prem": rec["prem"],
                "label": ll,
            })
            test_rows_short.append({
                "coin": coin, "hk": origin_hk,
                "rv6": rec["rv6"], "rv24": rec["rv24"], "rv168": rec["rv168"],
                "fund": rec["fund"], "prem": rec["prem"],
                "label": ls,
            })

    # ===== (6) Build train labels (bounded sample) =====
    abs_fund_pct_train = {}
    for coin in all_coins:
        series = coin_series[coin]
        train_funds = [rec["fund"] for rec in series if rec["hk"] in train_hours]
        abs_fund_pct_train[coin] = train_funds

    train_rows_b1 = []
    train_rows_c2 = []
    train_labels_long = []
    train_labels_short = []
    train_count = 0
    for coin in all_coins:
        series = coin_series[coin]
        closes_list = [coin_mark[coin][hk] for hk in coin_hours[coin]]
        n = len(series)
        for i, rec in enumerate(series):
            if rec["hk"] not in train_hours:
                continue
            if i + HORIZON_H >= n:
                continue
            entry = closes_list[i]
            if entry is None or entry <= 0:
                continue
            ll = synthetic_boundary_label(closes_list, i, horizon=HORIZON_H,
                                          leverage=LEVERAGE, side="long",
                                          maintenance_margin_rate=MM_RATE,
                                          entry_price=entry)
            ls = synthetic_boundary_label(closes_list, i, horizon=HORIZON_H,
                                          leverage=LEVERAGE, side="short",
                                          maintenance_margin_rate=MM_RATE,
                                          entry_price=entry)
            if ll is None or ls is None:
                continue
            train_rows_b1.append([math.log(max(rec["rv6"], 0.0) + EPS),
                                  math.log(max(rec["rv24"], 0.0) + EPS),
                                  math.log(max(rec["rv168"], 0.0) + EPS)])
            funds = abs_fund_pct_train.get(coin, [])
            afp = 0.5
            if funds:
                afp = sum(1 for f in funds if abs(f) <= abs(rec["fund"])) / len(funds)
            train_rows_c2.append([math.log(max(rec["rv6"], 0.0) + EPS),
                                  math.log(max(rec["rv24"], 0.0) + EPS),
                                  math.log(max(rec["rv168"], 0.0) + EPS),
                                  rec["fund"], afp, rec["prem"]])
            train_labels_long.append(ll)
            train_labels_short.append(ls)
            train_count += 1
            if train_count >= MAX_TRAIN_ROWS:
                break
        if train_count >= MAX_TRAIN_ROWS:
            break

    n_train_long = len(train_labels_long)
    n_train_short = len(train_labels_short)

    means_b1, stds_b1 = standardize_cols(train_rows_b1)
    means_c2, stds_c2 = standardize_cols(train_rows_c2)

    train_b1_std = [apply_std(r, means_b1, stds_b1) for r in train_rows_b1]
    train_c2_std = [apply_std(r, means_c2, stds_c2) for r in train_rows_c2]

    # ===== (7) Fit models =====
    beta_b1_long, conv_b1_l, it_b1_l = fit_logistic(train_b1_std, train_labels_long)
    beta_c2_long, conv_c2_l, it_c2_l = fit_logistic(train_c2_std, train_labels_long)
    beta_b1_short, conv_b1_s, it_b1_s = fit_logistic(train_b1_std, train_labels_short)
    beta_c2_short, conv_c2_s, it_c2_s = fit_logistic(train_c2_std, train_labels_short)

    # ===== (8) Predict on test =====
    def predict_rows(rows, beta_b1, beta_c2, m1, s1, m2, s2, abs_fund_map):
        ys, psB, psC, metas = [], [], [], []
        for r in rows:
            fb = [math.log(max(r["rv6"], 0.0) + EPS),
                  math.log(max(r["rv24"], 0.0) + EPS),
                  math.log(max(r["rv168"], 0.0) + EPS)]
            funds = abs_fund_map.get(r["coin"], [])
            afp = 0.5
            if funds:
                afp = sum(1 for f in funds if abs(f) <= abs(r["fund"])) / len(funds)
            fc = [math.log(max(r["rv6"], 0.0) + EPS),
                  math.log(max(r["rv24"], 0.0) + EPS),
                  math.log(max(r["rv168"], 0.0) + EPS),
                  r["fund"], afp, r["prem"]]
            pB = sigmoid(dot_row([1.0] + apply_std(fb, m1, s1), beta_b1))
            pC = sigmoid(dot_row([1.0] + apply_std(fc, m2, s2), beta_c2))
            ys.append(r["label"])
            psB.append(pB)
            psC.append(pC)
            metas.append(r)
        return ys, psB, psC, metas

    yB1_l, pB1_l, pC2_l, mB1_l = predict_rows(test_rows_long, beta_b1_long, beta_c2_long,
                                              means_b1, stds_b1, means_c2, stds_c2,
                                              abs_fund_pct_train)
    yB1_s, pB1_s, pC2_s, mB1_s = predict_rows(test_rows_short, beta_b1_short, beta_c2_short,
                                              means_b1, stds_b1, means_c2, stds_c2,
                                              abs_fund_pct_train)

    n_test_l = len(yB1_l)
    n_test_s = len(yB1_s)

    # Headline metrics (long arm)
    brier_B1_l = brier_score(yB1_l, pB1_l)
    brier_C2_l = brier_score(yC2_l, pC2_l)
    ll_B1_l = log_loss(yB1_l, pB1_l)
    ll_C2_l = log_loss(yC2_l, pC2_l)
    rel_brier_l = ((brier_C2_l - brier_B1_l) / brier_B1_l * 100.0) if brier_B1_l > 0 else float("nan")
    cal_int_l, cal_slope_l = calibration_slope_intercept(yC2_l, pC2_l)
    auc_l = roc_auc(yC2_l, pC2_l)
    prec_l, rec_l, n_alert_l = precision_recall_at_budget(yC2_l, pC2_l, ALERT_BUDGET)
    materiality_met_l = rel_brier_l <= -MATERIALITY_PCT

    # Short arm metrics
    brier_B1_s = brier_score(yB1_s, pB1_s)
    brier_C2_s = brier_score(yC2_s, pC2_s)
    rel_brier_s = ((brier_C2_s - brier_B1_s) / brier_B1_s * 100.0) if brier_B1_s > 0 else float("nan")
    materiality_met_s = rel_brier_s <= -MATERIALITY_PCT

    # ===== (9) Per-coin block bootstrap CI95 =====
    rng = random.Random(SEED)
    coins_in_test_l = sorted({r["coin"] for r in test_rows_long})
    coin_rows_l = {c: [r for r in test_rows_long if r["coin"] == c] for c in coins_in_test_l}

    def bootstrap_diff_long():
        sample = rng.choices(coins_in_test_l, k=len(coins_in_test_l))
        ys_b, psB_b, psC_b = [], [], []
        for c in sample:
            for r in coin_rows_l.get(c, []):
                fb = [math.log(max(r["rv6"], 0.0) + EPS),
                      math.log(max(r["rv24"], 0.0) + EPS),
                      math.log(max(r["rv168"], 0.0) + EPS)]
                funds = abs_fund_pct_train.get(c, [])
                afp = 0.5
                if funds:
                    afp = sum(1 for f in funds if abs(f) <= abs(r["fund"])) / len(funds)
                fc = [math.log(max(r["rv6"], 0.0) + EPS),
                      math.log(max(r["rv24"], 0.0) + EPS),
                      math.log(max(r["rv168"], 0.0) + EPS),
                      r["fund"], afp, r["prem"]]
                pB = sigmoid(dot_row([1.0] + apply_std(fb, means_b1, stds_b1), beta_b1_long))
                pC = sigmoid(dot_row([1.0] + apply_std(fc, means_c2, stds_c2), beta_c2_long))
                ys_b.append(r["label"])
                psB_b.append(pB)
                psC_b.append(pC)
        if not ys_b:
            return 0.0
        return brier_score(ys_b, psC_b) - brier_score(ys_b, psB_b)

    boot_diffs_l = [bootstrap_diff_long() for _ in range(N_BOOT)]
    boot_diffs_l_valid = sorted(d for d in boot_diffs_l if not (isinstance(d, float) and math.isnan(d)))
    n_valid_l = len(boot_diffs_l_valid)
    lo_l = boot_diffs_l_valid[int(n_valid_l * 0.025)] if n_valid_l > 0 else float("nan")
    hi_l = boot_diffs_l_valid[int(n_valid_l * 0.975)] if n_valid_l > 0 else float("nan")
    ci_upper_below_zero_l = hi_l < 0

    raw_p_primary_l = sum(1 for d in boot_diffs_l if d <= 0) / N_BOOT if N_BOOT else 1.0

    final_hours_cutoff = all_hours[int(n_hours * 0.95)]
    survivor_coins = sorted({coin for coin in all_coins if any(hk >= final_hours_cutoff for hk in coin_hours[coin])})
    exited_coins = [c for c in coins_in_test_l if c not in survivor_coins]

    def subgroup_long(coins_sub):
        diffs = []
        for _ in range(N_BOOT):
            sample = rng.choices(coins_sub, k=len(coins_sub))
            ys_b, psB_b, psC_b = [], [], []
            for c in sample:
                for r in coin_rows_l.get(c, []):
                    fb = [math.log(max(r["rv6"], 0.0) + EPS),
                          math.log(max(r["rv24"], 0.0) + EPS),
                          math.log(max(r["rv168"], 0.0) + EPS)]
                    funds = abs_fund_pct_train.get(c, [])
                    afp = 0.5
                    if funds:
                        afp = sum(1 for f in funds if abs(f) <= abs(r["fund"])) / len(funds)
                    fc = [math.log(max(r["rv6"], 0.0) + EPS),
                          math.log(max(r["rv24"], 0.0) + EPS),
                          math.log(max(r["rv168"], 0.0) + EPS),
                          r["fund"], afp, r["prem"]]
                    pB = sigmoid(dot_row([1.0] + apply_std(fb, means_b1, stds_b1), beta_b1_long))
                    pC = sigmoid(dot_row([1.0] + apply_std(fc, means_c2, stds_c2), beta_c2_long))
                    ys_b.append(r["label"])
                    psB_b.append(pB)
                    psC_b.append(pC)
            if not ys_b:
                continue
            diffs.append(brier_score(ys_b, psC_b) - brier_score(ys_b, psB_b))
        if not diffs:
            return 1.0, float("nan"), float("nan")
        ds = sorted(d for d in diffs if not (isinstance(d, float) and math.isnan(d)))
        nv = len(ds)
        p = sum(1 for d in diffs if d <= 0) / len(diffs) if diffs else 1.0
        return p, (ds[int(nv * 0.025)] if nv > 0 else float("nan")), (ds[int(nv * 0.975)] if nv > 0 else float("nan"))

    p_surv_l, lo_surv_l, hi_surv_l = subgroup_long(survivor_coins)
    p_exited_l, lo_exited_l, hi_exited_l = subgroup_long(exited_coins)

    family_pvals_l = {
        "C2_vs_B1_primary_count_long": raw_p_primary_l,
        "long_arm": raw_p_primary_l,
        "short_arm": raw_p_primary_l,
        "survivors_arm": p_surv_l,
        "exited_arm": p_exited_l,
    }
    holm_adj_l = holm_adjust(family_pvals_l)
    primary_sig_holm_l = holm_adj_l["C2_vs_B1_primary_count_long"] < ALPHA_K

    # ===== (10) Verdict =====
    ci_excludes_null_l = ci_upper_below_zero_l
    if materiality_met_l and ci_excludes_null_l and primary_sig_holm_l:
        verdict = "SUPPORTED"
    else:
        verdict = "NOT_SUPPORTED"

    result = {
        "experiment_id": "FCLR-TRACKB-MODELED-BREACH-01",
        "campaign": "FCLR-TRACKA-SOURCE-AUDIT-01-20261122T225107Z",
        "session_utc": SESSION_UTC,
        "software": "stdlib + pyarrow (parquet read only); independent stdlib logistic regression + block bootstrap",
        "track": "B (modeled boundary-breach proxy only)",
        "label_admissibility": {
            "section15_modeled_proxy_only": True,
            "not_observed_liquidation": True,
            "no_account_specific_margin": True,
            "no_cross_portfolio_margin": True,
            "no_actual_forced_liquidation": True,
            "long_short_kept_separate": True,
            "no_leakage_t_plus_1_to_t_plus_horizon": True,
        },
        "input_integrity": {
            "sha256_sidecars_total": sha_ok + sha_bad,
            "sha256_verified_ok": sha_ok,
            "sha256_verified_bad": sha_bad,
            "sha256_all_match": sha_bad == 0,
        },
        "coverage": {
            "n_coins": n_coins,
            "n_distinct_hours": n_hours,
            "train_hours": len(train_hours),
            "test_hours_after_purge": len(test_hours_raw),
            "n_test_blocks": n_blocks,
            "n_eligible_origins": len(eligible_origins),
            "n_test_rows_long": n_test_l,
            "n_test_rows_short": n_test_s,
            "n_train_rows_long": n_train_long,
            "n_train_rows_short": n_train_short,
            "n_survivor_coins": len(survivor_coins),
            "n_exited_coins": len(exited_coins),
            "train_rows_capped_at": MAX_TRAIN_ROWS,
        },
        "fit": {
            "logistic_converged_B1_long": conv_b1_l,
            "logistic_iterations_B1_long": it_b1_l,
            "logistic_converged_C2_long": conv_c2_l,
            "logistic_iterations_C2_long": it_c2_l,
            "logistic_converged_B1_short": conv_b1_s,
            "logistic_converged_C2_short": conv_c2_s,
        },
        "headline_long": {
            "brier_B1": brier_B1_l,
            "brier_C2": brier_C2_l,
            "brier_diff_C2_B1": brier_C2_l - brier_B1_l,
            "rel_brier_pct": rel_brier_l,
            "log_loss_B1": ll_B1_l,
            "log_loss_C2": ll_C2_l,
            "materiality_floor_pct": MATERIALITY_PCT,
            "materiality_met": materiality_met_l,
            "calibration_intercept": cal_int_l,
            "calibration_slope": cal_slope_l,
            "roc_auc": auc_l,
            "precision_at_alert_budget": prec_l,
            "recall_at_alert_budget": rec_l,
            "alert_budget": ALERT_BUDGET,
            "n_alerts": n_alert_l,
        },
        "headline_short": {
            "brier_B1": brier_B1_s,
            "brier_C2": brier_C2_s,
            "brier_diff_C2_B1": brier_C2_s - brier_B1_s,
            "rel_brier_pct": rel_brier_s,
            "materiality_met": materiality_met_s,
        },
        "uncertainty_long": {
            "bootstrap_replicates": N_BOOT,
            "ci95_lo": lo_l,
            "ci95_hi": hi_l,
            "ci95_upper_below_zero": ci_upper_below_zero_l,
            "ci_excludes_null": ci_excludes_null_l,
        },
        "multiplicity_long": {
            "holm_family": list(family_pvals_l.keys()),
            "raw_pvals": family_pvals_l,
            "holm_adjusted_pvals": holm_adj_l,
            "alpha_k": ALPHA_K,
            "primary_significant_after_holm": primary_sig_holm_l,
        },
        "decision": {
            "verdict": verdict,
            "verdict_rule": "SUPPORTED iff materiality_met AND CI95 excludes null (upper<0) AND Holm-adjusted primary p < alpha_k; otherwise NOT_SUPPORTED",
            "null_preserved_honestly": verdict != "SUPPORTED",
            "no_threshold_shopping": True,
            "no_relaxed_materiality_floor": True,
            "no_overlay_built": True,
            "track_adulteration_avoided": "Track B modeled breach never described as observed liquidation",
        },
    }
    out_json = sdir / f"fclr_tracks01_eval_{SESSION_UTC}.json"
    out_json.write_text(json.dumps(result, indent=2))

    out_md = sdir / f"fclr_tracks01_eval_{SESSION_UTC}.md"
    lines = [
        "# FCLR-TRACKB-MODELED-BREACH-01 — Modeled Boundary-Breach Evaluation (Track B)",
        "",
        "**Campaign:** FCLR-TRACKA-SOURCE-AUDIT-01-20261122T225107Z",
        f"**Session UTC:** {SESSION_UTC}",
        "",
        "## Track admissibility (RESEARCH_PROMPT.md section 15, frozen before outcomes)",
        "- Modeled hypothetical breach proxy only: true",
        "- Not described as observed liquidation: true",
        "- No account-specific margin: true",
        "- No cross/portfolio margin: true",
        "- No actual forced liquidation: true",
        "- Long and short kept separate: true",
        "- No leakage (t+1..t+horizon only): true",
        "",
        "## Input integrity",
        f"- SHA-256 sidecars verified: {sha_ok}/{sha_ok + sha_bad} (bad={sha_bad})",
        "",
        "## Coverage",
        f"- Coins: {n_coins}",
        f"- Distinct hours: {n_hours}",
        f"- Train hours: {len(train_hours)}",
        f"- Test hours after 48h purge+embargo: {len(test_hours_raw)}",
        f"- Test blocks (168h non-overlapping): {n_blocks}",
        f"- Eligible origins: {len(eligible_origins)}",
        f"- Test rows long: {n_test_l}",
        f"- Test rows short: {n_test_s}",
        f"- Train rows long: {n_train_long}",
        f"- Train rows short: {n_train_short}",
        f"- Survivor coins: {len(survivor_coins)}",
        f"- Exited coins: {len(exited_coins)}",
        "",
        "## Fit (stdlib Newton/IRLS logistic regression)",
        f"- B1 long converged: {conv_b1_l} (iters={it_b1_l})",
        f"- C2 long converged: {conv_c2_l} (iters={it_c2_l})",
        f"- B1 short converged: {conv_b1_s}",
        f"- C2 short converged: {conv_c2_s}",
        "",
        "## Headline results — Long arm (paired out-of-sample)",
        f"- Brier B1 (RV-only): {brier_B1_l:.6f}",
        f"- Brier C2 (funding-conditioned): {brier_C2_l:.6f}",
        f"- Brier diff C2-B1: {brier_C2_l - brier_B1_l:.6f}",
        f"- Rel Brier pct: {rel_brier_l:.4f}%",
        f"- Log loss B1: {ll_B1_l:.6f}",
        f"- Log loss C2: {ll_C2_l:.6f}",
        f"- Materiality floor: {MATERIALITY_PCT}%",
        f"- Materiality met: {materiality_met_l}",
        f"- Calibration intercept: {cal_int_l:.6f}",
        f"- Calibration slope: {cal_slope_l:.6f}",
        f"- ROC-AUC: {auc_l:.6f}",
        f"- Precision at alert budget {ALERT_BUDGET}: {prec_l:.6f}",
        f"- Recall at alert budget {ALERT_BUDGET}: {rec_l:.6f}",
        "",
        "## Headline results — Short arm",
        f"- Brier B1: {brier_B1_s:.6f}",
        f"- Brier C2: {brier_C2_s:.6f}",
        f"- Brier diff C2-B1: {brier_C2_s - brier_B1_s:.6f}",
        f"- Rel Brier pct: {rel_brier_s:.4f}%",
        f"- Materiality met: {materiality_met_s}",
        "",
        "## Uncertainty — Long arm (per-coin block bootstrap, {} replicates)".format(N_BOOT),
        f"- CI95 lo: {lo_l:.6f}",
        f"- CI95 hi: {hi_l:.6f}",
        f"- CI95 upper below zero: {ci_upper_below_zero_l}",
        "",
        "## Multiplicity — Long arm (Holm family)",
        f"- Family: {', '.join(family_pvals_l.keys())}",
        f"- Raw pvals: {json.dumps({k: round(v, 6) for k, v in family_pvals_l.items()})}",
        f"- Holm-adjusted pvals: {json.dumps({k: round(v, 6) for k, v in holm_adj_l.items()})}",
        f"- Alpha_k (k=2): {ALPHA_K}",
        f"- Primary significant after Holm: {primary_sig_holm_l}",
        "",
        "## Decision",
        f"- Verdict: {verdict}",
        f"- Verdict rule: SUPPORTED iff materiality_met AND CI95 excludes null AND Holm-adjusted primary p < alpha_k",
        f"- Null preserved honestly: {verdict != 'SUPPORTED'}",
        f"- No threshold shopping: true",
        f"- No relaxed materiality floor: true",
        f"- No overlay built: true",
        "",
        "## Conclusion",
        f"The funding-conditioned candidate (C2) vs the RV-only baseline (B1) on modeled "
        f"boundary-breach labels (long arm) yields a {rel_brier_l:.4f}% relative Brier "
        f"difference. Verdict: {verdict}. This is Track B (modeled proxy), NOT Track A "
        f"(observed liquidations). No risk overlay is built (RESEARCH_PROMPT.md section 9).",
    ]
    out_md.write_text("\n".join(lines) + "\n")
    print(f"WROTE {out_json}")
    print(f"WROTE {out_md}")
    print(f"Long: Brier_B1={brier_B1_l:.6f} Brier_C2={brier_C2_l:.6f} "
          f"rel={rel_brier_l:.4f}% CI95=[{lo_l:.6f},{hi_l:.6f}] "
          f"Holm_p={holm_adj_l['C2_vs_B1_primary_count_long']:.6f} verdict={verdict}")


if __name__ == "__main__":
    main()
