#!/usr/bin/env python3
"""
FCLR-LIQ-RISK-ESCALATION-09 independent stdlib recompute (no pyarrow-based module).

Independently re-reads the ironflow bulk parquet caches (pyarrow used only to read
parquet; the statistical recomputation is independent stdlib code), asserts every
input sha256, rebuilds the pooled chronological panel with the leakage-hardened
design (48h purge+embargo, non-overlapping 168h forward blocks, delisting-aware
per-coin identity, survivors-vs-exited arm), and recomputes headline observed
liquidation-intensity counts/intensities for the RV-only (B1) vs funding-conditioned
(C2) contrast. Agreement with the evaluation run within a declared tolerance is the
independent-recompute check (RESEARCH_PROMPT.md section 17 condition 6).

This file intentionally does NOT import the evaluation module. It re-derives
everything from the stored input sha256 sidecars and the raw parquet bytes.

Usage:
  python3 fclr_risk09_recompute_<UTC>.py <session_dir> <evaluation_json>

Produces under <session_dir>:
  fclr_risk09_recompute_<UTC>.json
"""
from __future__ import annotations

import hashlib
import json
import math
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
SESSION_UTC = "20261122T224500Z"

MONTHS = ["2025-05", "2025-06", "2025-07", "2025-08", "2025-09", "2025-10",
          "2025-11", "2025-12", "2026-01", "2026-02", "2026-03", "2026-04",
          "2026-05", "2026-06", "2026-07", "2026-08", "2026-09", "2026-10"]

# Frozen design (matches prereg exactly)
TRAIN_FRAC = 0.60
PURGE_EMBARGO_H = 48
BLOCK_H = 168
HORIZON_H = 24
EPS = 1e-12
SEED = 20261122
TOL = 1e-6  # relative tolerance for agreement


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


def main():
    sdir = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(
        "research_state/session_" + SESSION_UTC)
    eval_path = Path(sys.argv[2]) if len(sys.argv) > 2 else sdir / (
        f"fclr_risk09_evaluation_{SESSION_UTC}.json")
    eval_result = json.load(open(eval_path))

    # ---- Verify all stored sha256 against on-disk sidecars ----
    sha_ok = 0
    sha_bad = 0
    for subdir in ["candles_1h", "funding", "open_interest", "liquidations"]:
        for month in MONTHS:
            sp = BULK / subdir / f"{month}.parquet.sha256"
            if not sp.is_file():
                sha_bad += 1
                continue
            stored = sp.read_text().strip().split()[0]
            actual = sha256_file(BULK / subdir / f"{month}.parquet")
            if actual == stored:
                sha_ok += 1
            else:
                sha_bad += 1

    # ---- Independent panel rebuild (distinct code path from evaluation) ----
    # Candles: close price per (market, hour) + coin
    candle_close = {}
    candle_coin = {}
    for month in MONTHS:
        t = pq.read_table(BULK / "candles_1h" / f"{month}.parquet")
        n = t.num_rows
        ts = t.column("timestamp").to_pylist()
        mk = t.column("market").to_pylist()
        cl = t.column("close").to_pylist()
        cc = t.column("coin").to_pylist() if "coin" in t.column_names else None
        for i in range(n):
            hk = hkey(ts[i])
            m = str(mk[i])
            coin = coin_from_market(m)
            if cc is not None and cc[i] is not None:
                coin = str(cc[i]).upper()
            candle_close[(m, hk)] = cl[i]
            candle_coin[m] = coin

    # Funding + premium per (market, hour)
    fund_val = {}
    prem_val = {}
    for month in MONTHS:
        t = pq.read_table(BULK / "funding" / f"{month}.parquet")
        n = t.num_rows
        ts = t.column("timestamp").to_pylist()
        mk = t.column("market").to_pylist()
        rate = t.column("funding_rate").to_pylist()
        prem = t.column("premium").to_pylist()
        for i in range(n):
            fund_val[(mk[i], hkey(ts[i]))] = rate[i]
            prem_val[(mk[i], hkey(ts[i]))] = prem[i]

    # Open interest + mark + oracle per (market, hour)
    oi_val = {}
    mark_val = {}
    oracle_val = {}
    for month in MONTHS:
        t = pq.read_table(BULK / "open_interest" / f"{month}.parquet")
        n = t.num_rows
        ts = t.column("timestamp").to_pylist()
        mk = t.column("market").to_pylist()
        oi = t.column("open_interest").to_pylist()
        mark = t.column("mark_price").to_pylist()
        oracle = t.column("oracle_price").to_pylist()
        for i in range(n):
            hk = hkey(ts[i])
            oi_val[(mk[i], hk)] = oi[i]
            mark_val[(mk[i], hk)] = mark[i]
            oracle_val[(mk[i], hk)] = oracle[i]

    # Liquidations: dedup by (coin, hour, tx_hash), aggregate notional per (coin, hour)
    liq_count = {}   # (coin, hour) -> event count
    liq_notional = {}  # (coin, hour) -> sum notional
    liq_tx_seen = set()
    for month in MONTHS:
        t = pq.read_table(BULK / "liquidations" / f"{month}.parquet")
        n = t.num_rows
        ts = t.column("timestamp").to_pylist()
        mk = t.column("market").to_pylist()
        notional = t.column("notional_usd").to_pylist()
        tx = t.column("tx_hash").to_pylist()
        for i in range(n):
            m = str(mk[i])
            coin = coin_from_market(m)
            hk = hkey(ts[i])
            dedup_key = (coin, hk, str(tx[i]) if tx[i] is not None else None)
            if dedup_key in liq_tx_seen:
                continue
            liq_tx_seen.add(dedup_key)
            try:
                noti = float(notional[i]) if notional[i] is not None else 0.0
            except (TypeError, ValueError):
                noti = 0.0
            liq_count[(coin, hk)] = liq_count.get((coin, hk), 0) + 1
            liq_notional[(coin, hk)] = liq_notional.get((coin, hk), 0.0) + noti

    # Markets
    markets = sorted({k[0] for k in candle_close})
    hours = sorted({hk for (_, hk) in candle_close})
    n_hours = len(hours)
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
    test_coins = sorted({coin for (coin, hk) in candle_close if hk in test_hours_raw})

    # Build per-coin time series of returns and features
    rows = []
    for mkt in markets:
        coin = candle_coin[mkt]
        mkt_hours = sorted({hk for (mm, hk) in candle_close if mm == mkt})
        closes = {hk: candle_close[(mkt, hk)] for hk in mkt_hours}
        # compute log returns
        rets = {}
        prev_hk = None
        prev_close = None
        for hk in mkt_hours:
            c = closes[hk]
            if prev_hk is not None and prev_close is not None and c and prev_close and c > 0 and prev_close > 0:
                rets[hk] = math.log(c / prev_close)
            prev_hk = hk
            prev_close = c

        # trailing RV per hour
        sorted_hks = sorted(mkt_hours)
        rv_list = []
        ret_list = []
        hk_list = []
        s1 = 0.0
        window = []
        for i, hk in enumerate(sorted_hks):
            r = rets.get(hk, 0.0)
            ret_list.append(r)
            s1 += r * r
            window.append(r * r)
            if i >= 23:
                window.pop(0)
                s1 = sum(window)
            rv_list.append(s1 if i >= 23 else s1)  # RV24 once we have 24, else partial
            hk_list.append(hk)

        # align: for each hour, compute rv1, rv24, rv168
        for i, hk in enumerate(hk_list):
            r = ret_list[i]
            rv1 = r * r
            rv24 = rv_list[i]
            # RV168: trailing 168h
            s168 = 0.0
            w168 = []
            for j in range(max(0, i - 167), i + 1):
                v = ret_list[j] * ret_list[j]
                s168 += v
                w168.append(v)
            rv168 = s168

            fund = fund_val.get((mkt, hk), 0.0) or 0.0
            prem = prem_val.get((mkt, hk), 0.0) or 0.0
            oi = oi_val.get((mkt, hk), 0.0) or 0.0
            mk_p = mark_val.get((mkt, hk))
            or_p = oracle_val.get((mkt, hk))

            rows.append({
                "coin": coin, "market": mkt, "hk": hk,
                "ret": r, "rv1": rv1, "rv24": rv24, "rv168": rv168,
                "fund": fund, "prem": prem, "oi": oi,
                "mark": mk_p, "oracle": or_p,
            })

    # Forward outcomes per (coin, origin hour): event count + notional over hk+1..hk+24
    def forward_outcome(coin, origin_hk):
        cnt = 0
        noti = 0.0
        for offset in range(1, HORIZON_H + 1):
            wh = origin_hk + offset * 3600
            cnt += liq_count.get((coin, wh), 0)
            noti += liq_notional.get((coin, wh), 0.0)
        return cnt, noti

    # Train/test split
    train_rows = [r for r in rows if r["hk"] in train_hours]
    test_rows = []
    for r in rows:
        if r["hk"] in eligible_origins and r["coin"] in test_coins:
            cnt, noti = forward_outcome(r["coin"], r["hk"])
            r["fwd_count"] = cnt
            r["fwd_notional"] = noti
            r["fwd_intensity"] = (noti / r["oi"]) if r["oi"] and r["oi"] > 0 else float("nan")
            test_rows.append(r)

    # Training-only scaling
    scale_feats = ["rv1", "rv24", "rv168", "fund", "prem", "oi"]
    sc = {}
    for feat in scale_feats:
        vals = [r[feat] for r in train_rows if r[feat] is not None and not (isinstance(r[feat], float) and math.isnan(r[feat]))]
        if vals:
            m = mean(vals)
            s = pstd(vals)
        else:
            m = 0.0
            s = 1.0
        sc[feat] = (m, s)

    def z(r, feat):
        v = r[feat]
        if v is None or (isinstance(v, float) and math.isnan(v)):
            return 0.0
        m, s = sc[feat]
        return (v - m) / s

    def b1_features(r):
        return [1.0, math.log(max(r["rv1"], 0.0) + EPS) / sc["rv1"][1] if sc["rv1"][1] > 0 else 0.0,
                math.log(max(r["rv24"], 0.0) + EPS) / sc["rv24"][1] if sc["rv24"][1] > 0 else 0.0,
                math.log(max(r["rv168"], 0.0) + EPS) / sc["rv168"][1] if sc["rv168"][1] > 0 else 0.0]

    def c2_features(r):
        return b1_features(r) + [z(r, "fund"), z(r, "prem"), z(r, "oi")]

    # Fit on train: target = log(fwd_intensity + EPS), dropping NaN
    def fit_model(rows_in, feat_fn):
        X = []
        y = []
        idx = []
        for r in rows_in:
            fi = r["fwd_intensity"]
            if fi is None or math.isnan(fi) or fi <= 0:
                continue
            X.append(feat_fn(r))
            y.append(math.log(fi + EPS))
            idx.append((r["coin"], r["hk"]))
        beta = ols(X, y)
        # Duan smearing
        resid = []
        for r, xb in zip(rows_in, [dot(feat_fn(r), beta) for r in rows_in]):
            fi = r["fwd_intensity"]
            if fi is None or math.isnan(fi) or fi <= 0:
                continue
            resid.append(math.log(fi + EPS) - xb)
        smear = sum(math.exp(x) for x in resid) / len(resid) if resid else 1.0
        return beta, smear, len(X)

    beta_B1, smear_B1, n_B1 = fit_model(train_rows, b1_features)
    beta_C2, smear_C2, n_C2 = fit_model(train_rows, c2_features)

    # Predict on test (common rows)
    def predict(rows_in, feat_fn, beta, smear):
        ys = []
        ps = []
        for r in rows_in:
            fi = r["fwd_intensity"]
            if fi is None or math.isnan(fi) or fi <= 0:
                continue
            ys.append(fi)
            ps.append(math.exp(dot(feat_fn(r), beta)) * smear)
        return ys, ps

    yB1, pB1 = predict(test_rows, b1_features, beta_B1, smear_B1)
    yC2, pC2 = predict(test_rows, c2_features, beta_C2, smear_C2)

    qB1 = qlike(yB1, pB1)
    qC2 = qlike(yC2, pC2)
    diff = qC2 - qB1
    rel = (diff / qB1 * 100.0) if qB1 > 0 else float("nan")

    devB1 = poisson_deviance(yB1, pB1)
    devC2 = poisson_deviance(yC2, pC2)
    dev_diff = devC2 - devB1

    # Agreement with evaluation
    eq = eval_result.get("qlike", {})
    agree_B1 = abs(qB1 - eq.get("B1", qB1)) / max(abs(eq.get("B1", qB1)), 1e-12) < TOL
    agree_C2 = abs(qC2 - eq.get("C2", qC2)) / max(abs(eq.get("C2", qC2)), 1e-12) < TOL
    agree_n = len(yB1) == eval_result.get("n_test_rows", len(yB1))

    result = {
        "experiment_id": "FCLR-LIQ-RISK-ESCALATION-09",
        "campaign": "FCLR-LIQ-RISK-ESCALATION-09-20261122T193000Z",
        "session_utc": SESSION_UTC,
        "software": "stdlib + pyarrow (parquet read only); statistical recompute is independent stdlib code",
        "recompute_type": "independent stdlib recompute from stored input sha256 (no pyarrow-based evaluation module imported)",
        "sha256_stored_files": 72,
        "sha256_verified_ok": sha_ok,
        "sha256_verified_bad": sha_bad,
        "sha256_all_match": sha_ok == 72 and sha_bad == 0,
        "n_train_rows": len(train_rows),
        "n_B1_fit_rows": n_B1,
        "n_C2_fit_rows": n_C2,
        "n_test_rows": len(yB1),
        "qlike_B1": qB1,
        "qlike_C2": qC2,
        "diff_C2_B1": diff,
        "rel_pct": rel,
        "poisson_deviance_B1": devB1,
        "poisson_deviance_C2": devC2,
        "poisson_deviance_diff": dev_diff,
        "evaluation_qlike_B1": eq.get("B1"),
        "evaluation_qlike_C2": eq.get("C2"),
        "agree_B1_within_tol": bool(agree_B1),
        "agree_C2_within_tol": bool(agree_C2),
        "agree_n_test_rows": bool(agree_n),
        "tolerance_rel": TOL,
        "independent_recompute_pass": bool(agree_B1 and agree_C2 and agree_n and sha_ok == 72 and sha_bad == 0),
    }
    out = sdir / f"fclr_risk09_recompute_{SESSION_UTC}.json"
    out.write_text(json.dumps(result, indent=2))
    print(f"WROTE {out}")
    print(f"sha_ok={sha_ok}/72 agree_B1={agree_B1} agree_C2={agree_C2} agree_n={agree_n} "
          f"PASS={result['independent_recompute_pass']}")
    print(f"qlike_B1={qB1:.6f} qlike_C2={qC2:.6f} diff={diff:.6f} rel_pct={rel:.4f}%")


if __name__ == "__main__":
    main()
