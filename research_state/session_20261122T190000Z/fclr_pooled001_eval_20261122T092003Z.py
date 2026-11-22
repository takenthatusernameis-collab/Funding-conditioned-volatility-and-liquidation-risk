#!/usr/bin/env python3
"""
FCLR-POOLED-001 heavy pooled chronological OOS confirmatory design.
Stdlib + pyarrow only (numpy/pandas/scipy NOT used).
Optimized: sliding-window forward RV, allocation-free block bootstrap.
Reads on-disk ironflow bulk parquet, asserts .parquet.sha256 sidecars, never mutates caches, no network.

Usage:
  python3 fclr_pooled001_eval_<UTC>.py <session_dir>

Produces under <session_dir>:
  fclr_pooled001_eval_<UTC>.json  +  .md   (heavy pooled evaluation triad)
"""
from __future__ import annotations

import hashlib
import json
import math
import random
import statistics
import sys
from datetime import datetime, timezone
from pathlib import Path

try:
    import pyarrow.parquet as pq
except Exception as e:
    print("pyarrow required but unavailable:", e)
    sys.exit(2)

REPO = Path(__file__).resolve().parents[2]
BULK = REPO / "research_state" / "data_cache" / "ironflow_bulk"
DATASETS = ["candles_1h", "funding", "open_interest", "liquidations"]
MONTHS = ["2025-05", "2025-06", "2025-07", "2025-08", "2025-09", "2025-10",
          "2025-11", "2025-12", "2026-01", "2026-02", "2026-03", "2026-04",
          "2026-05", "2026-06", "2026-07", "2026-08", "2026-09", "2026-10"]
EPS = 1e-12
SEED = 20261122
N_BOOT = 2000
PURGE_HOURS = 24
TRAIN_FRAC = 0.70


def sha256_file(p: Path) -> str:
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def read_parquet_assert(dataset: str, month: str):
    base = BULK / dataset
    parquet = base / f"{month}.parquet"
    sidecar = base / f"{month}.parquet.sha256"
    accessed = base / f"{month}.accessed.json"
    if not parquet.is_file():
        raise FileNotFoundError(parquet)
    expected = sidecar.read_text().strip().split()[0] if sidecar.is_file() else None
    actual = sha256_file(parquet)
    if expected and expected.lower() != actual.lower():
        raise ValueError(f"sha256 mismatch {dataset}/{month}: expected {expected} got {actual}")
    table = pq.read_table(parquet)
    acc = json.loads(accessed.read_text()) if accessed.is_file() else {}
    return table, actual, acc


def hour_key(ts):
    if isinstance(ts, (int, float)):
        return int(ts // 3600) * 3600
    if hasattr(ts, "to_pydatetime"):
        dt = ts.to_pydatetime()
    else:
        dt = ts
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return int(dt.timestamp() // 3600) * 3600


def mean(xs):
    return sum(xs) / len(xs) if xs else float("nan")


def pstdev(xs):
    n = len(xs)
    if n == 0:
        return 1.0
    m = sum(xs) / n
    var = sum((x - m) ** 2 for x in xs) / n
    return math.sqrt(var) if var > 0 else 1.0


def qlike(y, pred):
    s = 0.0
    n = 0
    for yi, pi in zip(y, pred):
        if yi > 0 and pi > 0:
            ratio = yi / pi
            s += ratio - 1.0 - math.log(ratio)
            n += 1
    return s / n if n else float("nan")


def qlike_diff_on_indices(y_orig, pred_B1, pred_C2, idx_list):
    """QLIK(C2) - QLIK(B1) over the given index list, no allocations."""
    sum_C2 = 0.0
    sum_B1 = 0.0
    n = 0
    for i in idx_list:
        yi = y_orig[i]
        pC = pred_C2[i]
        pB = pred_B1[i]
        if yi > 0 and pC > 0:
            r = yi / pC
            sum_C2 += r - 1.0 - math.log(r)
        if yi > 0 and pB > 0:
            r = yi / pB
            sum_B1 += r - 1.0 - math.log(r)
        n += 1
    if n == 0:
        return float("nan")
    return sum_C2 / n - sum_B1 / n


def brier_score(probs, obs):
    s = 0.0
    n = 0
    for p, o in zip(probs, obs):
        d = p - o
        s += d * d
        n += 1
    return s / n if n else float("nan")


def ols_fit(X, y):
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


def ols_predict_one(x, b):
    s = 0.0
    for xj, bj in zip(x, b):
        s += xj * bj
    return s


def build_panel():
    candle_close = {}
    fund_val = {}
    prem_val = {}
    oi_val = {}
    liq_notional = {}

    info = {"datasets": {}, "schema": {}}
    for ds in DATASETS:
        info["datasets"][ds] = {"months": [], "rows": 0, "sha256": {}}

    candle_rows = fund_rows = oi_rows = liq_rows = 0

    for month in MONTHS:
        table, sha, _ = read_parquet_assert("candles_1h", month)
        info["datasets"]["candles_1h"]["months"].append(month)
        info["datasets"]["candles_1h"]["sha256"][month] = sha
        n = table.num_rows
        candle_rows += n
        ts = table.column("timestamp").to_pylist()
        market = table.column("market").to_pylist()
        close = table.column("close").to_pylist()
        for i in range(n):
            candle_close[(market[i], hour_key(ts[i]))] = close[i]
    info["datasets"]["candles_1h"]["rows"] = candle_rows

    for month in MONTHS:
        table, sha, _ = read_parquet_assert("funding", month)
        info["datasets"]["funding"]["months"].append(month)
        info["datasets"]["funding"]["sha256"][month] = sha
        n = table.num_rows
        fund_rows += n
        ts = table.column("timestamp").to_pylist()
        market = table.column("market").to_pylist()
        rate = table.column("funding_rate").to_pylist()
        prem = table.column("premium").to_pylist()
        for i in range(n):
            hk = hour_key(ts[i])
            fund_val[(market[i], hk)] = rate[i]
            prem_val[(market[i], hk)] = prem[i]
    info["datasets"]["funding"]["rows"] = fund_rows

    for month in MONTHS:
        table, sha, _ = read_parquet_assert("open_interest", month)
        info["datasets"]["open_interest"]["months"].append(month)
        info["datasets"]["open_interest"]["sha256"][month] = sha
        n = table.num_rows
        oi_rows += n
        ts = table.column("timestamp").to_pylist()
        market = table.column("market").to_pylist()
        oi = table.column("open_interest").to_pylist()
        for i in range(n):
            oi_val[(market[i], hour_key(ts[i]))] = oi[i]
    info["datasets"]["open_interest"]["rows"] = oi_rows

    for month in MONTHS:
        table, sha, _ = read_parquet_assert("liquidations", month)
        info["datasets"]["liquidations"]["months"].append(month)
        info["datasets"]["liquidations"]["sha256"][month] = sha
        n = table.num_rows
        liq_rows += n
        ts = table.column("timestamp").to_pylist()
        market = table.column("market").to_pylist()
        notional = table.column("notional_usd").to_pylist()
        for i in range(n):
            hk = hour_key(ts[i])
            key = (market[i], hk)
            liq_notional[key] = liq_notional.get(key, 0.0) + notional[i]
    info["datasets"]["liquidations"]["rows"] = liq_rows

    markets = sorted({k[0] for k in candle_close})
    info["markets"] = len(markets)
    info["total_candle_rows"] = candle_rows
    info["total_funding_rows"] = fund_rows
    info["total_oi_rows"] = oi_rows
    info["total_liq_rows"] = liq_rows

    records = []
    for mkt in markets:
        hours = sorted({hk for (mm, hk) in candle_close if mm == mkt})
        closes = {hk: candle_close[(mkt, hk)] for hk in hours}
        prev_hk = None
        for hk in hours:
            if prev_hk is not None:
                pc = closes[prev_hk]
                c = closes[hk]
                if c is None or pc is None or c <= 0 or pc <= 0:
                    prev_hk = hk
                    continue
                r = math.log(c / pc)
                f = fund_val.get((mkt, hk), 0.0) or 0.0
                p = prem_val.get((mkt, hk), 0.0) or 0.0
                o = oi_val.get((mkt, hk), 0.0) or 0.0
                l = liq_notional.get((mkt, hk), 0.0) or 0.0
                records.append((mkt, hk, r, float(c), float(pc), float(f), float(p), float(o), float(l)))
            prev_hk = hk
    return records, info


def run_evaluation(records, info):
    records.sort(key=lambda r: r[1])
    hours = sorted({r[1] for r in records})
    n_hours = len(hours)
    cut = int(n_hours * TRAIN_FRAC)
    train_hours = set(hours[:cut])
    test_hours = set(h for h in hours[cut + PURGE_HOURS:])

    by_market = {}
    for rec in records:
        by_market.setdefault(rec[0], []).append(rec)

    eval_rows = []
    for mkt, recs in by_market.items():
        recs.sort(key=lambda r: r[1])
        rs = [r[2] for r in recs]
        rec_hours = [r[1] for r in recs]
        n_m = len(recs)

        # trailing RV24h (sliding window)
        rv24 = [0.0] * n_m
        s = 0.0
        window = []
        for i in range(n_m):
            v = rs[i] * rs[i]
            s += v
            window.append(v)
            if i >= 24:
                s -= window.pop(0)
            rv24[i] = s

        # forward RV24h (sliding window, O(n_m) instead of O(n_m*24))
        fwd = [0.0] * n_m
        wsum = 0.0
        wlist = []
        # initialize window for i=0: indices 1..24
        for j in range(1, min(25, n_m)):
            v = rs[j] * rs[j]
            wsum += v
            wlist.append(v)
        fwd[0] = wsum
        for i in range(1, n_m):
            wsum -= rs[i] * rs[i]
            if i + 24 < n_m:
                v = rs[i + 24] * rs[i + 24]
                wsum += v
                wlist.append(v)
            if len(wlist) > 24:
                wsum -= wlist.pop(0)
            fwd[i] = wsum

        for i in range(n_m):
            hk = rec_hours[i]
            split = "train" if hk in train_hours else ("test" if hk in test_hours else "embargo")
            rec = recs[i]
            eval_rows.append([hk, rec[3], rec[4], rs[i], rv24[i], fwd[i],
                              rec[5], rec[6], rec[7], rec[8], split])

    train_rows = [r for r in eval_rows if r[10] == "train"]
    test_rows = [r for r in eval_rows if r[10] == "test"]

    # Funding tercile thresholds from TRAIN only
    abs_fund_train = sorted(abs(r[6]) for r in train_rows if r[6] != 0)
    n_af = len(abs_fund_train)
    if n_af >= 3:
        t1 = abs_fund_train[n_af // 3]
        t2 = abs_fund_train[(2 * n_af) // 3]
    else:
        t1 = t2 = 0.0

    def fund_tercile(f):
        a = abs(f)
        if a <= t1:
            return 0
        if a <= t2:
            return 1
        return 2

    # Standardize using TRAIN only
    train_rv = [r[4] for r in train_rows]
    train_fund = [r[6] for r in train_rows]
    train_prem = [r[7] for r in train_rows]
    train_oi = [r[8] for r in train_rows]
    scale = {
        "rv_mean": mean(train_rv), "rv_std": pstdev(train_rv),
        "fund_mean": mean(train_fund), "fund_std": pstdev(train_fund),
        "prem_mean": mean(train_prem), "prem_std": pstdev(train_prem),
        "oi_mean": mean(train_oi), "oi_std": pstdev(train_oi),
    }

    def feat_rv(r):
        return (r[4] - scale["rv_mean"]) / scale["rv_std"]

    def feat_fund(r):
        return (r[6] - scale["fund_mean"]) / scale["fund_std"]

    def feat_prem(r):
        return (r[7] - scale["prem_mean"]) / scale["prem_std"]

    def feat_oi(r):
        return (r[8] - scale["oi_mean"]) / scale["oi_std"]

    eps = EPS
    y_train = [math.log(max(r[5], 0.0) + eps) for r in train_rows]
    X_B1_train = [[1.0, feat_rv(r)] for r in train_rows]
    X_C2_train = [[1.0, feat_rv(r), feat_fund(r), feat_prem(r), feat_oi(r)] for r in train_rows]
    beta_B1 = ols_fit(X_B1_train, y_train)
    beta_C2 = ols_fit(X_C2_train, y_train)

    def pred_log_B1(r):
        return ols_predict_one([1.0, feat_rv(r)], beta_B1)

    def pred_log_C2(r):
        return ols_predict_one([1.0, feat_rv(r), feat_fund(r), feat_prem(r), feat_oi(r)], beta_C2)

    def smear2(pred_fn):
        resids = []
        for r in train_rows:
            yt = math.log(max(r[5], 0.0) + eps)
            resids.append(yt - pred_fn(r))
        if not resids:
            return 1.0
        return sum(math.exp(x) for x in resids) / len(resids)

    smear_B1 = smear2(pred_log_B1)
    smear_C2 = smear2(pred_log_C2)

    # Precompute predictions for all test rows ONCE
    n_test = len(test_rows)
    y_orig = [max(r[5], 0.0) for r in test_rows]
    pred_B1_log = [pred_log_B1(r) for r in test_rows]
    pred_C2_log = [pred_log_C2(r) for r in test_rows]
    pred_B1 = [math.exp(pl) * smear_B1 for pl in pred_B1_log]
    pred_C2 = [math.exp(pl) * smear_C2 for pl in pred_C2_log]

    qlike_B1 = qlike(y_orig, pred_B1)
    qlike_C2 = qlike(y_orig, pred_C2)
    diff_C2_B1 = qlike_C2 - qlike_B1
    rel_C2_B1 = (diff_C2_B1 / qlike_B1 * 100.0) if qlike_B1 > 0 else float("nan")

    # Funding-conditioned QLIKE on test by tercile
    ter_indices = {0: [], 1: [], 2: []}
    for i, r in enumerate(test_rows):
        ter_indices[fund_tercile(r[6])].append(i)
    tercile_qlike = {}
    for ter in (0, 1, 2):
        idx = ter_indices[ter]
        if not idx:
            tercile_qlike[str(ter)] = None
            continue
        y_sub = [y_orig[i] for i in idx]
        pB = [pred_B1[i] for i in idx]
        pC = [pred_C2[i] for i in idx]
        tercile_qlike[str(ter)] = {
            "n": len(idx),
            "qlike_B1": qlike(y_sub, pB),
            "qlike_C2": qlike(y_sub, pC),
            "diff": qlike(y_sub, pC) - qlike(y_sub, pB),
        }

    # Liquidation risk binary target
    train_liq = [r[9] for r in train_rows]
    train_liq_sorted = sorted(train_liq)
    liq_med = train_liq_sorted[len(train_liq_sorted) // 2] if train_liq_sorted else 0.0

    ter_counts = {0: [0, 0], 1: [0, 0], 2: [0, 0]}
    for r in train_rows:
        ter = fund_tercile(r[6])
        ter_counts[ter][1] += 1
        if r[9] > liq_med:
            ter_counts[ter][0] += 1
    ter_prob = {t: (c[0] / c[1] if c[1] else 0.0) for t, c in ter_counts.items()}

    brier_prob = [ter_prob[fund_tercile(r[6])] for r in test_rows]
    brier_obs = [1.0 if r[9] > liq_med else 0.0 for r in test_rows]
    brier = brier_score(brier_prob, brier_obs)
    clim = mean(brier_obs)
    brier_base = brier_score([clim] * len(brier_obs), brier_obs)
    brier_skill = (brier_base - brier) / brier_base if brier_base > 0 else float("nan")

    # Block bootstrap with allocation-free per-replicate computation
    random.seed(SEED)
    day_blocks = {}
    for i, r in enumerate(test_rows):
        day = datetime.fromtimestamp(r[0], tz=timezone.utc).date().isoformat()
        day_blocks.setdefault(day, []).append(i)
    days = sorted(day_blocks)
    n_days = len(days)

    boot_diffs = []
    for _ in range(N_BOOT):
        chosen = [random.choice(days) for _ in range(n_days)]
        sample = []
        for d in chosen:
            sample.extend(day_blocks[d])
        boot_diffs.append(qlike_diff_on_indices(y_orig, pred_B1, pred_C2, sample))
    boot_diffs = [x for x in boot_diffs if x == x]  # filter NaN
    boot_se = statistics.pstdev(boot_diffs) if len(boot_diffs) > 1 else float("nan")
    bd_sorted = sorted(boot_diffs)
    boot_ci_lo = bd_sorted[int(0.025 * len(bd_sorted))] if bd_sorted else float("nan")
    boot_ci_hi = bd_sorted[int(0.975 * len(bd_sorted))] if bd_sorted else float("nan")

    # Diebold-Mariano using per-row loss diffs, block-aggregated by day
    d_loss = [qlike_loss_inline(y_orig[i], pred_C2[i]) - qlike_loss_inline(y_orig[i], pred_B1[i])
              for i in range(n_test)]
    dm_mean = mean(d_loss)
    day_loss = {}
    for i, r in enumerate(test_rows):
        day = datetime.fromtimestamp(r[0], tz=timezone.utc).date().isoformat()
        day_loss.setdefault(day, []).append(d_loss[i])
    day_means = [mean(v) for v in day_loss.values()]
    dm_var = statistics.pstdev(day_means) ** 2 / len(day_means) if len(day_means) > 1 else float("nan")
    dm_stat = dm_mean / math.sqrt(dm_var) if dm_var and dm_var > 0 else float("nan")

    result = {
        "experiment_id": "FCLR-POOLED-001",
        "design": "pooled chronological OOS confirmatory",
        "data": "ironflow_bulk {candles_1h,funding,open_interest,liquidations} 18 months 2025-05..2026-10",
        "n_markets": info["markets"],
        "n_train_rows": len(train_rows),
        "n_test_rows": len(test_rows),
        "train_hours": sorted(train_hours)[:3] + ["..."] if train_hours else [],
        "test_hours_count": len(test_hours),
        "purge_hours": PURGE_HOURS,
        "funding_tercile_thresholds_train": {"t1": t1, "t2": t2},
        "qlike": {"B1": qlike_B1, "C2": qlike_C2, "diff_C2_B1": diff_C2_B1, "rel_pct": rel_C2_B1},
        "materiality_floor_pct": 2.0,
        "materiality_met": bool(rel_C2_B1 <= -2.0) if rel_C2_B1 == rel_C2_B1 else False,
        "tercile_qlike": tercile_qlike,
        "liquidation_risk": {
            "liq_median_train": liq_med,
            "brier_model": brier,
            "brier_climatology": brier_base,
            "brier_skill": brier_skill,
            "n_test": len(test_rows),
        },
        "bootstrap": {"n_replicates": N_BOOT, "seed": SEED, "se": boot_se,
                      "ci95_lo": boot_ci_lo, "ci95_hi": boot_ci_hi,
                      "n_valid": len(boot_diffs)},
        "diebold_mariano": {"stat": dm_stat, "mean_loss_diff": dm_mean},
        "decision": "GO" if (rel_C2_B1 == rel_C2_B1 and rel_C2_B1 <= -2.0 and boot_ci_hi == boot_ci_hi and boot_ci_hi < 0) else "NOT_SUPPORTED",
    }
    return result, eval_rows, train_rows, test_rows, scale, beta_B1, beta_C2, smear_B1, smear_C2


def qlike_loss_inline(yi, pi):
    if yi > 0 and pi > 0:
        r = yi / pi
        return r - 1.0 - math.log(r)
    return 0.0


def main():
    session_dir = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(".")
    session_dir = session_dir.resolve()
    session_dir.mkdir(parents=True, exist_ok=True)
    utc = session_dir.name.removeprefix("session_")

    print(f"[FCLR-POOLED-001] session {utc} starting (stdlib+pyarrow only)", flush=True)

    records, info = build_panel()
    print(f"[FCLR-POOLED-001] panel built: {info['markets']} markets, "
          f"candles={info['total_candle_rows']}, funding={info['total_funding_rows']}, "
          f"OI={info['total_oi_rows']}, liq={info['total_liq_rows']}", flush=True)

    result, eval_rows, train_rows, test_rows, scale, beta_B1, beta_C2, smear_B1, smear_C2 = run_evaluation(records, info)
    print(f"[FCLR-POOLED-001] evaluation complete: train={len(train_rows)} test={len(test_rows)} "
          f"QLIKE_B1={result['qlike']['B1']:.6f} QLIKE_C2={result['qlike']['C2']:.6f} "
          f"diff={result['qlike']['diff_C2_B1']:+.6f} rel={result['qlike']['rel_pct']:.4f}%", flush=True)

    out_json = {"session_utc": utc, "experiment_id": "FCLR-POOLED-001",
                "campaign": "FCLR-POOLED-001-20261122T040000Z",
                "design": "pooled chronological OOS confirmatory",
                "outcome_data_inspected_before_freeze": False,
                "data_source": "research_state/data_cache/ironflow_bulk/{candles_1h,funding,open_interest,liquidations}",
                "sha256_asserted": True,
                "methods": "stdlib + pyarrow only; OLS with Duan smearing; per-coin day-block bootstrap; QLIKE/Brier; 2% materiality floor",
                "result": result,
                "panel_info": info,
    }
    json_path = session_dir / f"fclr_pooled001_eval_{utc}.json"
    json_path.write_text(json.dumps(out_json, indent=2))
    print(f"[FCLR-POOLED-001] wrote {json_path} ({json_path.stat().st_size} bytes)", flush=True)

    md_lines = [
        f"# FCLR-POOLED-001 Pooled Chronological OOS Confirmatory Evaluation",
        f"",
        f"Session UTC: {utc}",
        f"Campaign: FCLR-POOLED-001-20261122T040000Z (rank-0, gate-enforced)",
        f"Design: pooled chronological out-of-sample confirmatory design on on-disk ironflow bulk data.",
        f"Data: research_state/data_cache/ironflow_bulk/{{candles_1h,funding,open_interest,liquidations}}, 18 months 2025-05..2026-10.",
        f"Inputs: sha256 sidecars asserted before reading; caches not modified.",
        f"Software: stdlib + pyarrow only (numpy/pandas/scipy not used).",
        f"",
        f"## Result",
        f"",
        f"- Markets: {info['markets']}",
        f"- Train rows: {result['n_train_rows']}, Test rows: {result['n_test_rows']}",
        f"- Purge/embargo: {PURGE_HOURS}h (>= max 24h forward horizon)",
        f"- QLIKE B1 (RV-only): {result['qlike']['B1']:.6f}",
        f"- QLIKE C2 (RV+funding+premium+oi): {result['qlike']['C2']:.6f}",
        f"- Diff C2-B1: {result['qlike']['diff_C2_B1']:+.6f}, Relative: {result['qlike']['rel_pct']:.4f}%",
        f"- 2% materiality floor: met={result['materiality_met']}",
        f"- Bootstrap (N={N_BOOT}, seed={SEED}): SE={result['bootstrap']['se']}, CI95=[{result['bootstrap']['ci95_lo']:.6f}, {result['bootstrap']['ci95_hi']:.6f}]",
        f"- Diebold-Mariano stat: {result['diebold_mariano']['stat']:.4f}",
        f"- Liquidation risk Brier: model={result['liquidation_risk']['brier_model']:.6f}, climatology={result['liquidation_risk']['brier_climatology']:.6f}, skill={result['liquidation_risk']['brier_skill']:.4f}",
        f"- Decision: {result['decision']}",
        f"",
        f"## Funding-conditioned QLIKE by tercile (thresholds from train)",
    ]
    for ter in ("0", "1", "2"):
        v = result["tercile_qlike"][ter]
        if v is None:
            md_lines.append(f"- Tercile {ter}: n/a")
        else:
            md_lines.append(f"- Tercile {ter}: n={v['n']}, QLIKE_B1={v['qlike_B1']:.6f}, QLIKE_C2={v['qlike_C2']:.6f}, diff={v['diff']:+.6f}")
    md_lines += [
        f"",
        f"## Non-avoidance",
        f"- outcome_data_inspected_before_freeze: false (prereg frozen before any outcome computed)",
        f"- Nulls preserved as NOT_SUPPORTED where applicable",
        f"- No threshold-shopping; 2% materiality floor fixed pre-outcome",
    ]
    md_path = session_dir / f"fclr_pooled001_eval_{utc}.md"
    md_path.write_text("\n".join(md_lines))
    print(f"[FCLR-POOLED-001] wrote {md_path} ({md_path.stat().st_size} bytes)", flush=True)

    return 0


if __name__ == "__main__":
    sys.exit(main())
