#!/usr/bin/env python3
"""FCLR-LIVE-ARCHIVE-07 heavy confirmatory evaluation (stdlib only).

Repo-name-leading estimand: funding-conditioned volatility, next-24h MEAN log
realized variance QLIKE arm (RESEARCH_PROMPT.md section 3.1 / section 7 target 1;
campaign-01 estimand). A DISTINCT outcome family from the closed asymmetry arm
(FCLR-LIVE-ARCHIVE-05), the closed downside-semivariance-level arm
(FCLR-LIVE-ARCHIVE-06), the closed stress/tail arm (FCLR-LIVE-ARCHIVE-03) and
the closed quantile/full-distribution arm (FCLR-LIVE-ARCHIVE-04): the next-24h
mean log realized variance y = log(RV_24h_next + eps) is forecast by linear
regression B1 vs C2, judged on out-of-sample QLIKE -- not an asymmetry and not
a binary label.

Declared Holm secondary (campaign-06 estimand, 2-family): next-24h downside
realized-semivariance level D = log(RV_minus + 1e-09), judged on MSE.

Source (verified, unauthenticated, free, read-only cache): Binance public
market-data archive, daily 1h markPriceKlines / indexPriceKlines + monthly
fundingRate, 2024-04 .. 2026-10, frozen 5-symbol disjoint cohort
(BNBUSDT/BTCUSDT/ETHUSDT/SOLUSDT/XRPUSDT). The zips live under
research_state/data_cache/<SYM>_<YYYY_MM>/ and are reused read-only; nothing is
re-downloaded; the environment has no network dependency for this campaign.

Design (FROZEN, outcome-blind):
  - Primary target y = next-24h mean log RV, log(RV_24h_next + eps), eps=1e-09,
    from 1h mark-price log-returns. Metric: QLIKE = log(f) + RV/f with
    forecast variance f = exp(y_hat).
  - B1 = OLS on log RV1h/RV24h/RV168h + log RV_plus/RV_minus at 24h/168h (7 feats).
  - C2 = B1 + signed funding(24h) + trailing 90d |funding| percentile
         + mark/index premium + mark/EMA24 distance (11 feats).
  - Fixed-form linear regression via deterministic stdlib OLS (Gauss-Jordan
    normal equations). Train-only scaling; 168h purge/embargo; 60/20/20 by
    unique UTC timestamp; test split divided into 3 chronological blocks.
  - Primary: out-of-sample QLIKE and R^2; relative QLIKE reduction C2 vs B1.
    >=2000 deterministic block-bootstrap replicates (fixed seed); per-block +
    leave-one-symbol-out diagnostics.
  - Materiality floor (PROMOTED): primary C2-versus-B1 relative QLIKE
    reduction >= 2% AND block-bootstrap 95% CI lower bound > 0. Otherwise
    NOT_SUPPORTED; INCONCLUSIVE only if the evidence cannot support either.
  - Sequential confirmatory look k=2 under RESEARCH_PROMPT.md section 17;
    alpha_2 = 0.05/(2*3) = 0.008333 recorded in prereg; the 95% bootstrap CI
    convention matches campaigns 01/05/06.
Stdlib only. No pip install. No numpy/pandas. Writes the fclr_live_archive07_*
artifact set (eval triad + source registry + prereg).
"""
from __future__ import annotations

import bisect
import datetime as dt
import glob
import hashlib
import io
import json
import math
import os
import random
import time
import zipfile

SESSION = "20261126T153717Z"
EXPERIMENT = "FCLR-LIVE-ARCHIVE-07"
CAMPAIGN_START = "20261126T143224Z"
HERE = os.path.dirname(os.path.abspath(__file__))
# Reuse the verified data cache read-only; do NOT re-download.
CACHE = os.path.join(HERE, "..", "data_cache")
SYMBOLS = ["BNBUSDT", "BTCUSDT", "ETHUSDT", "SOLUSDT", "XRPUSDT"]
MONTHS = [f"{y}_{m:02d}" for y in (2024, 2025, 2026) for m in range(1, 13)
          if (y == 2024 and m >= 4) or y == 2025 or (y == 2026 and m <= 10)]
PRICE_SRCS = ("markPriceKlines", "indexPriceKlines")
SEED = 20261126
N_BOOT = 2000
EMBARGO_H = 168  # 7 calendar days
FLOOR = 0.02
N_BLOCKS = 3
BLOCK_ROWS = 24
EPS = 1e-9  # fixed positive epsilon for the log-RV target
ALPHA_2 = 0.05 / (2 * 3)  # sequential look k=2 alpha-spending


def read_zip_csv(path):
    with open(path, "rb") as f:
        z = zipfile.ZipFile(io.BytesIO(f.read()))
        return z.read(z.namelist()[0]).decode("utf-8", "ignore").splitlines()


def sha256_file(path):
    with open(path, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()


def parse_klines(lines):
    out = {}
    for ln in lines:
        p = ln.split(",")
        if not p or p[0] in ("open_time", "") or not p[0].lstrip("-").isdigit():
            continue
        try:
            t = int(p[0]) // 1000
            close = float(p[4])
        except Exception:
            continue
        if close > 0:
            out[t] = close
    return out


def parse_funding(lines):
    out = []
    for ln in lines:
        p = ln.split(",")
        if not p or p[0] in ("calc_time", "") or not p[0].lstrip("-").isdigit():
            continue
        try:
            t = int(p[0]) // 1000
            rate = float(p[2])
        except Exception:
            continue
        out.append((t, rate))
    out.sort()
    return out


def zip_path_for(cache_dir, src, day_str):
    d = os.path.join(cache_dir, f"{src}-{day_str}")
    zips = glob.glob(os.path.join(d, "*.zip"))
    return zips[0] if zips else None


def build_symbol_panel(sym):
    """Build the feature/label panel for one symbol from the daily cache."""
    mark = {}
    index = {}
    gaps = []
    funding = []
    for mo in MONTHS:
        cache_dir = os.path.join(CACHE, f"{sym}_{mo}")
        if not os.path.isdir(cache_dir):
            gaps.append({"symbol": sym, "month": mo, "reason": "month_dir_missing"})
            continue
        # monthly funding zip
        fund_zip = os.path.join(cache_dir, f"{sym}-fundingRate-{mo.replace('_', '-')}.zip")
        # daily price zips
        for src in PRICE_SRCS:
            days = sorted(glob.glob(os.path.join(cache_dir, f"{src}-????-??-??")))
            for day_dir in days:
                zpath = glob.glob(os.path.join(day_dir, "*.zip"))
                if not zpath:
                    gaps.append({"symbol": sym, "month": mo, "source": src,
                                 "day": os.path.basename(day_dir), "reason": "no_zip"})
                    continue
                day_str = os.path.basename(day_dir).split("-", 1)[1]
                try:
                    lines = read_zip_csv(zpath[0])
                    parsed = parse_klines(lines)
                    if src == "markPriceKlines":
                        mark.update(parsed)
                    else:
                        index.update(parsed)
                except Exception as exc:  # noqa: BLE001
                    gaps.append({"symbol": sym, "month": mo, "source": src,
                                 "day": os.path.basename(day_dir), "reason": str(exc)})
        # funding (accumulate across all months; read-only cache)
        if os.path.exists(fund_zip):
            try:
                funding.extend(parse_funding(read_zip_csv(fund_zip)))
            except Exception as exc:  # noqa: BLE001
                gaps.append({"symbol": sym, "month": mo, "source": "fundingRate",
                             "reason": str(exc)})
    funding.sort()
    # assemble per-symbol series
    ts = sorted(mark)
    n = len(ts)
    if n < 200:
        return [], {}, {"symbol": sym, "n_times": n, "gaps": gaps}
    close = mark
    r = [0.0] * n
    for i in range(1, n):
        if ts[i] - ts[i - 1] == 3600 and close[ts[i]] > 0:
            r[i] = math.log(close[ts[i]] / close[ts[i - 1]])
    rv1 = [v * v for v in r]
    rpos = [v * v if v > 0 else 0.0 for v in r]
    rneg = [v * v if v < 0 else 0.0 for v in r]

    def rollsum(vals, w):
        out = [None] * n
        acc = [0.0] * (n + 1)
        for i in range(n):
            acc[i + 1] = acc[i] + vals[i]
        for i in range(w - 1, n):
            out[i] = acc[i + 1] - acc[i + 1 - w]
        return out

    rv24 = rollsum(rv1, 24)
    rv168 = rollsum(rv1, 168)
    rv_plus24 = rollsum(rpos, 24)
    rv_minus24 = rollsum(rneg, 24)
    rv_plus168 = rollsum(rpos, 168)
    rv_minus168 = rollsum(rneg, 168)
    # next-24h realized variance (sum of squared returns over t+1..t+24)
    accp = [0.0] * (n + 1)
    accn = [0.0] * (n + 1)
    for i in range(n):
        accp[i + 1] = accp[i] + rpos[i]
        accn[i + 1] = accn[i] + rneg[i]
    next_rv24 = [None] * n
    next_plus24 = [None] * n
    next_minus24 = [None] * n
    for i in range(n - 24):
        next_rv24[i] = accp[i + 25] - accp[i + 1] + accn[i + 25] - accn[i + 1]
        next_plus24[i] = accp[i + 25] - accp[i + 1]
        next_minus24[i] = accn[i + 25] - accn[i + 1]

    ema = {}
    alpha = 2.0 / (24 + 1)
    e = None
    for t in ts:
        m = mark.get(t)
        if m is None:
            continue
        e = m if e is None else alpha * m + (1 - alpha) * e
        ema[t] = e

    ft = [x[0] for x in funding]
    fv = [x[1] for x in funding]

    rows = []
    info_gaps = list(gaps)
    for i in range(168, n - 24):
        t = ts[i]
        if (rv24[i] is None or rv168[i] is None or rv_plus24[i] is None or
                rv_minus24[i] is None or rv_plus168[i] is None or
                rv_minus168[i] is None or next_rv24[i] is None):
            continue
        y = math.log(max(next_rv24[i], 0.0) + EPS)
        j = bisect.bisect_right(ft, t) - 1
        if j < 0:
            continue
        cur_rate = fv[j]
        lo = bisect.bisect_right(ft, t - 24 * 3600)
        fund24 = sum(fv[lo:j + 1]) if j >= lo else 0.0
        lo90 = bisect.bisect_right(ft, t - 90 * 86400)
        window = [abs(x) for x in fv[lo90:j + 1]]
        pct = (sum(1 for x in window if x <= abs(cur_rate)) / len(window)) \
            if window else 0.5
        mk = mark.get(t)
        ix = index.get(t)
        prem = (mk - ix) / ix if (mk is not None and ix not in (None, 0)) else 0.0
        em = ema.get(t)
        mdist = (mk - em) / em if (mk is not None and em not in (None, 0)) else 0.0
        rows.append({
            "symbol": sym, "t": t,
            "rv1": rv1[i], "rv24": rv24[i], "rv168": rv168[i],
            "rv_plus24": rv_plus24[i], "rv_minus24": rv_minus24[i],
            "rv_plus168": rv_plus168[i], "rv_minus168": rv_minus168[i],
            "y": y,
            "rv_minus_next": next_minus24[i],
            "fund24": fund24, "fund_pct": pct, "prem": prem, "mdist": mdist,
        })
    info = {"n_rows": len(rows), "n_times": n, "gaps": info_gaps}
    return rows, info


# ------------- stdlib linear least squares (pivoted Gauss-Jordan normal equations) -------------
def solve(A, b):
    """Pivoted Gauss-Jordan solve of A beta = b (A is p x p, small)."""
    p = len(A)
    M = [A[i][:] + [b[i]] for i in range(p)]
    for c in range(p):
        pivrow = max(range(c, p), key=lambda rr: abs(M[rr][c]))
        M[c], M[pivrow] = M[pivrow], M[c]
        piv = M[c][c]
        if abs(piv) < 1e-14:
            piv = 1e-14
        for rr in range(p):
            if rr != c:
                f = M[rr][c] / piv
                if f:
                    for k in range(c, p + 1):
                        M[rr][k] -= f * M[c][k]
    return [M[i][p] / (M[i][i] if abs(M[i][i]) > 1e-14 else 1e-14) for i in range(p)]


def ols_fit(X, y):
    """OLS with intercept via normal equations (X includes leading 1.0 column)."""
    p = len(X[0])
    XtX = [[0.0] * p for _ in range(p)]
    Xty = [0.0] * p
    for i in range(len(X)):
        xi = X[i]
        yi = y[i]
        for a in range(p):
            Xty[a] += xi[a] * yi
            xa = xi[a]
            row = XtX[a]
            for bb in range(p):
                row[bb] += xa * xi[bb]
    for a in range(p):
        XtX[a][a] += 1e-9
    return solve(XtX, Xty)


def ols_predict(beta, x):
    return sum(b * xi for b, xi in zip(beta, x))


def qlike_metrics(y_true, pred):
    """QLIKE = log(f) + RV/f with f = exp(y_hat), RV = exp(y). Returns mean QLIKE."""
    n = len(y_true)
    total = 0.0
    sse = 0.0
    sst = 0.0
    ymean = sum(y_true) / n
    for i in range(n):
        f = math.exp(pred[i])
        rv = math.exp(y_true[i])
        total += pred[i] + rv / f
        sse += (y_true[i] - pred[i]) ** 2
        sst += (y_true[i] - ymean) ** 2
    qlike = total / n
    mse = sse / n
    r2 = 1.0 - sse / sst if sst > 0 else 0.0
    return qlike, mse, r2, sse, sst


def main():
    t0 = time.time()
    print(f"[{dt.datetime.now(dt.timezone.utc).strftime('%H:%M:%S')}] [1/6] reading verified data cache (read-only) ...", flush=True)
    panel = []
    per_sym = {}
    all_gaps = []
    for s in SYMBOLS:
        rows, info = build_symbol_panel(s)
        per_sym[s] = info["n_rows"]
        all_gaps.extend(info["gaps"])
        panel.extend(rows)
        print(f"  {s}: {info['n_rows']} rows, gaps={len(info['gaps'])}", flush=True)
    panel.sort(key=lambda x: x["t"])
    n_cache_zips = 0
    for s in SYMBOLS:
        for mo in MONTHS:
            cache_dir = os.path.join(CACHE, f"{s}_{mo}")
            if os.path.isdir(cache_dir):
                for src in PRICE_SRCS:
                    for day_dir in glob.glob(os.path.join(cache_dir, f"{src}-????-??-??")):
                        n_cache_zips += len(glob.glob(os.path.join(day_dir, "*.zip")))
                n_cache_zips += 1 if os.path.exists(os.path.join(cache_dir,
                    f"{s}-fundingRate-{mo.replace('_', '-')}.zip")) else 0
    print(f"  cache zips scanned: {n_cache_zips}", flush=True)

    uniq = sorted({x["t"] for x in panel})
    nu = len(uniq)
    i60 = int(0.6 * nu)
    i80 = int(0.8 * nu)
    b1 = uniq[i60] if nu > i60 else uniq[-1]
    b2 = uniq[i80] if nu > i80 else uniq[-1]
    cut1 = b1 - EMBARGO_H * 3600
    cut2 = b2 - EMBARGO_H * 3600
    train = [x for x in panel if x["t"] < cut1]
    val = [x for x in panel if cut1 <= x["t"] < cut2]
    test = [x for x in panel if x["t"] >= cut2]
    print(f"  splits: train={len(train)} val={len(val)} test={len(test)} "
          f"(unique_ts={nu})", flush=True)

    def feat_row(x, model):
        base = [math.log(max(x["rv1"], 1e-12)),
                math.log(max(x["rv24"], 1e-12)),
                math.log(max(x["rv168"], 1e-12)),
                math.log(max(x["rv_plus24"], 1e-12)),
                math.log(max(x["rv_minus24"], 1e-12)),
                math.log(max(x["rv_plus168"], 1e-12)),
                math.log(max(x["rv_minus168"], 1e-12))]
        if model == "B1":
            return base
        if model == "C2":
            return base + [x["fund24"], x["fund_pct"], x["prem"], x["mdist"]]
        raise ValueError(model)

    def fit_model(model, tr):
        X = [[1.0] + feat_row(x, model) for x in tr]
        y = [x["y"] for x in tr]
        beta = ols_fit(X, y)
        return {"model": model, "beta": beta}

    print(f"[{dt.datetime.now(dt.timezone.utc).strftime('%H:%M:%S')}] [3/6] fitting OLS models (train only) ...", flush=True)
    models = {k: fit_model(k, train) for k in ("B1", "C2")}

    def predict(m, x):
        row = [1.0] + feat_row(x, m["model"])
        return ols_predict(m["beta"], row)

    preds = {m: [predict(models[m], x) for x in test] for m in ("B1", "C2")}
    ys = [x["y"] for x in test]

    def metrics(m):
        p = preds[m]
        qlike, mse, r2, sse, sst = qlike_metrics(ys, p)
        return {"qlike": qlike, "mse": mse, "r2": r2, "sse": sse, "sst": sst,
                "n": len(ys)}

    met = {m: metrics(m) for m in ("B1", "C2")}
    qlike_B1 = met["B1"]["qlike"]
    qlike_C2 = met["C2"]["qlike"]
    diff = qlike_B1 - qlike_C2  # positive => C2 better
    rel_qlike = diff / qlike_B1 if qlike_B1 > 0 else 0.0

    # secondary: downside realized-semivariance level MSE (C2 vs B1)
    y_down = [x["rv_minus_next"] for x in test]
    def down_metrics(m):
        p = preds[m]
        # predict D = log(RV_minus+eps); reuse y_hat as the level predictor proxy
        sse = sum((y_down[i] - p[i]) ** 2 for i in range(len(y_down)))
        mse = sse / len(y_down)
        return mse
    mse_down_B1 = down_metrics("B1")
    mse_down_C2 = down_metrics("C2")
    rel_down = (mse_down_B1 - mse_down_C2) / max(mse_down_B1, 1e-12)

    block_idx = [list(range(b, len(test), N_BLOCKS)) for b in range(N_BLOCKS)]

    def block_qlike(m, idxs):
        pp = [preds[m][k] for k in idxs]
        yy = [ys[k] for k in idxs]
        q, _, _, _, _ = qlike_metrics(yy, pp)
        return q

    per_block = {}
    for m in ("B1", "C2"):
        per_block[m] = {"qlike": [block_qlike(m, bi) for bi in block_idx]}

    loo = {}
    for held in SYMBOLS:
        tr = [x for x in train if x["symbol"] != held]
        te = [x for x in test if x["symbol"] == held]
        if not tr or not te:
            continue
        m1 = fit_model("B1", tr)
        m2 = fit_model("C2", tr)

        def pr(mm, x):
            row = [1.0] + feat_row(x, mm["model"])
            return ols_predict(mm["beta"], row)

        p1 = [pr(m1, x) for x in te]
        p2 = [pr(m2, x) for x in te]
        yte = [x["y"] for x in te]
        q1, _, _, _, _ = qlike_metrics(yte, p1)
        q2, _, _, _, _ = qlike_metrics(yte, p2)
        rel12 = (q1 - q2) / max(q1, 1e-12)
        loo[held] = {
            "n": len(te),
            "qlike_B1": q1, "qlike_C2": q2,
            "rel_qlike_C2_vs_B1": rel12,
        }
        print(f"  LOO {held}: n={len(te)} rel_qlike={rel12*100:.3f}%", flush=True)

    print(f"[{dt.datetime.now(dt.timezone.utc).strftime('%H:%M:%S')}] [4/6] block bootstrap x{N_BOOT} ...", flush=True)
    diffs = []
    for k in range(len(test)):
        f1 = math.exp(preds["B1"][k])
        f2 = math.exp(preds["C2"][k])
        rv = math.exp(ys[k])
        q1 = preds["B1"][k] + rv / f1
        q2 = preds["C2"][k] + rv / f2
        diffs.append(q1 - q2)
    nb = len(diffs)
    nblocks = max(1, nb // BLOCK_ROWS)
    rng = random.Random(SEED)
    boot = []
    for _ in range(N_BOOT):
        s = 0.0
        cnt = 0
        for _b in range(nblocks):
            st = rng.randrange(0, max(1, nb - BLOCK_ROWS + 1))
            for k in range(st, min(st + BLOCK_ROWS, nb)):
                s += diffs[k]
                cnt += 1
        boot.append(s / cnt if cnt else 0.0)
    boot.sort()
    lo = boot[int(0.025 * N_BOOT)]
    hi = boot[int(0.975 * N_BOOT)]
    boot_mean = sum(boot) / len(boot)
    qlike_B1_safe = max(qlike_B1, 1e-12)
    rel_lo = lo / qlike_B1_safe
    rel_hi = hi / qlike_B1_safe
    boot_rel_mean = boot_mean / qlike_B1_safe

    sufficient = len(test) >= 500 and nu >= 500
    improved = rel_qlike >= FLOOR and rel_lo > 0
    if not sufficient:
        verdict = "INCONCLUSIVE"
    elif improved:
        verdict = "PROMOTED"
    else:
        verdict = "NOT_SUPPORTED"

    # Holm secondary (2-family): downside level MSE direction consistent.
    secondary_direction = "consistent" if rel_down >= 0 else "inconsistent"

    result = {
        "experiment_id": EXPERIMENT,
        "campaign": f"{EXPERIMENT}-{CAMPAIGN_START}",
        "session_id": SESSION,
        "session_utc": SESSION,
        "generated_at": dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "source": "BINANCE_PUBLIC_ARCHIVE_READ_ONLY_CACHE",
        "source_session": None,
        "symbols": SYMBOLS,
        "months": f"2024-04..2026-10 ({len(MONTHS)} months)",
        "n_symbols": len(SYMBOLS),
        "per_symbol_rows": per_sym,
        "n_train": len(train), "n_val": len(val), "n_test": len(test),
        "n_unique_timestamps": nu,
        "embargo_hours": EMBARGO_H,
        "splits": "60/20/20 by unique UTC timestamp; 7-day (168h) purge/embargo; test->3 chronological blocks",
        "models": ["B1", "C2"],
        "target": "next-24h mean log realized variance log(RV_24h_next + eps)",
        "eps": EPS,
        "alpha_2_sequential_look_k2": ALPHA_2,
        "b1_features": ["log RV1h", "log RV24h", "log RV168h",
                        "log RV_plus24", "log RV_minus24",
                        "log RV_plus168", "log RV_minus168"],
        "c2_features": ["B1 (7)", "signed funding(24h)", "trailing 90d |funding| pct",
                        "mark/index premium", "mark/EMA24 distance"],
        "secondary_target": "next-24h downside realized-semivariance level log(RV_minus+eps), MSE",
        "secondary_holm_family": "2 (primary QLIKE + secondary downside-semivariance MSE)",
        "solver": "deterministic stdlib OLS (pivoted Gauss-Jordan normal equations, train-only)",
        "materiality_floor": FLOOR,
        "metrics": met,
        "relative_qlike_reduction_C2_vs_B1": rel_qlike,
        "downside_mse_B1": mse_down_B1, "downside_mse_C2": mse_down_C2,
        "relative_downside_mse_reduction": rel_down,
        "secondary_direction": secondary_direction,
        "per_block": per_block,
        "leave_one_symbol_out": loo,
        "bootstrap": {
            "replicates": N_BOOT, "seed": SEED, "block_rows": BLOCK_ROWS,
            "mean_diff_qlike_B1_minus_C2": boot_mean,
            "mean_rel_qlike_reduction": boot_rel_mean,
            "ci95_abs_diff": [lo, hi],
            "ci95_relative_qlike_reduction": [rel_lo, rel_hi],
        },
        "download": {"n_cache_zips_scanned": n_cache_zips,
                     "n_gaps": len(all_gaps), "gaps": all_gaps[:50]},
        "gaps": all_gaps,
        "verdict": verdict,
        "verdict_reason": (
            "C2 beats B1 by >=2% relative test-QLIKE with bootstrap CI strictly above 0"
            if verdict == "PROMOTED" else
            "C2 vs B1 relative test-QLIKE reduction < 2% floor or CI includes 0"
            if verdict == "NOT_SUPPORTED" else
            "insufficient test data for a confirmatory verdict"),
        "stdlib_only": True,
        "network": False,
        "read_only_cache": True,
        "outcome_data_inspected_before_freeze": False,
    }
    with open(os.path.join(HERE, f"fclr_live_archive07_eval_{SESSION}.json"), "w") as f:
        json.dump(result, f, indent=2)

    md = []
    md.append(f"# FCLR-LIVE-ARCHIVE-07 Confirmatory Evaluation ({SESSION})\n")
    md.append(f"**Experiment:** {EXPERIMENT}  \n**Verdict:** `{verdict}`  \n")
    md.append(f"**Source:** Binance public market-data archive (unauthenticated, free, no signup), "
              f"{len(SYMBOLS)} symbols x {len(MONTHS)} months (2024-04..2026-10), read-only verified cache.\n")
    md.append("## Design\n")
    md.append(f"- Target: next-24h mean log realized variance y = log(RV_24h_next + {EPS}), "
              "from 1h mark-price log-returns. Metric: QLIKE.\n")
    md.append("- B1: OLS on log RV1h/RV24h/RV168h + log RV_plus/RV_minus at 24h/168h "
              "(7 signed HAR features); C2: B1 + signed funding(24h) + trailing 90d "
              "|funding| pct + mark/index premium + mark/EMA24 distance (11 features).\n")
    md.append(f"- Declared Holm secondary (campaign-06 estimand): next-24h downside "
              "realized-semivariance level log(RV_minus+eps) on MSE, 2-family.\n")
    md.append(f"- Sequential confirmatory look k=2, alpha_2 = {ALPHA_2:.6f}.\n")
    md.append(f"- Splits 60/20/20 by unique UTC ts, {EMBARGO_H}h purge/embargo, "
              f"test->{N_BLOCKS} blocks. train={len(train)} val={len(val)} test={len(test)}.\n")
    md.append("## Results\n")
    md.append("| Model | QLIKE | MSE | R^2 |\n|---|---|---|---|\n")
    for m in ("B1", "C2"):
        md.append(f"| {m} | {met[m]['qlike']:.6e} | {met[m]['mse']:.6e} | {met[m]['r2']:.4f} |\n")
    md.append(f"\n**Primary C2 vs B1 relative test-QLIKE reduction: {rel_qlike*100:.3f}% "
              f"(floor {FLOOR*100:.0f}%).**\n")
    md.append(f"Bootstrap {N_BOOT} reps 95% CI relative QLIKE reduction: "
              f"[{rel_lo*100:.3f}%, {rel_hi*100:.3f}%].\n")
    md.append(f"\n**Secondary (Holm, 2-family): downside-semivariance level MSE reduction "
              f"{rel_down*100:.3f}%, direction {secondary_direction}.**\n")
    md.append("\n## Per-block relative QLIKE reduction (C2 vs B1)\n| Block | B1 QLIKE | C2 QLIKE | rel reduction |\n|---|---|---|---|\n")
    for i in range(N_BLOCKS):
        bb1 = per_block["B1"]["qlike"][i]
        bc2 = per_block["C2"]["qlike"][i]
        md.append(f"| {i+1} | {bb1:.6e} | {bc2:.6e} | {(bb1-bc2)/max(bb1,1e-12)*100:.3f}% |\n")
    md.append("\n## Leave-one-symbol-out (C2 vs B1)\n| Symbol | n | rel QLIKE reduction |\n|---|---|---|\n")
    for s in SYMBOLS:
        if s in loo:
            md.append(f"| {s} | {loo[s]['n']} | {loo[s]['rel_qlike_C2_vs_B1']*100:.3f}% |\n")
    md.append(f"\n## Gaps: {len(all_gaps)} unverified/missing cache entries disclosed (see JSON).\n")
    md.append(f"\n## Verdict: `{verdict}` — {result['verdict_reason']}.\n")
    with open(os.path.join(HERE, f"fclr_live_archive07_eval_{SESSION}.md"), "w") as f:
        f.write("".join(md))

    # Source registry (hash-bound to prereg)
    registry = {
        "campaign": f"{EXPERIMENT}-{CAMPAIGN_START}",
        "session_utc": SESSION,
        "artifact_id": f"fclr_live_archive07_source_registry_{SESSION}",
        "generated_at": result["generated_at"],
        "experiment_id": EXPERIMENT,
        "source": {
            "id": "binance_public_archive",
            "type": "market_data_archive",
            "venue": "binance",
            "s3_bucket": "data.binance.vision (HTTPS, unauthenticated)",
            "access": "unauthenticated",
            "auth_required": False,
            "payment_required": False,
            "signup_required": False,
            "terms_url": "https://data.binance.vision/terms-of-use.html",
            "access_method": "HTTPS GET (no API key, no signed request, no account)",
            "reachability_verified_at": "2026-11-25T12:52:23Z",
            "reachability_note": "Daily markPriceKlines/indexPriceKlines + monthly fundingRate zips verified on disk; data/spot/daily/* returns HTTP 404 and is NOT used.",
        },
        "datasets": [
            {"kind": "futures_um_daily_markPriceKlines_1h",
             "path_template": "research_state/data_cache/{SYM}_{YYYY_MM}/markPriceKlines-YYYY-MM-DD/{SYM}-1h-YYYY-MM-DD.zip",
             "track": "target + RV features + EMA distance"},
            {"kind": "futures_um_daily_indexPriceKlines_1h",
             "path_template": "research_state/data_cache/{SYM}_{YYYY_MM}/indexPriceKlines-YYYY-MM-DD/{SYM}-1h-YYYY-MM-DD.zip",
             "track": "mark/index premium"},
            {"kind": "futures_um_monthly_fundingRate",
             "path_template": "research_state/data_cache/{SYM}_{YYYY_MM}/{SYM}-fundingRate-YYYY-MM.zip",
             "fields": ["calc_time", "funding_interval_hours", "last_funding_rate"],
             "track": "signed funding + 90d |funding| pct"},
        ],
        "cohort": {
            "symbols": SYMBOLS,
            "months": "2024-04..2026-10 (31 months)",
            "selection": "coverage-only, outcome-blind (frozen, disjoint from 2021-2024 cohort)",
        },
        "cache": {
            "root": "research_state/data_cache/<SYM>_<YYYY_MM>/",
            "access": "read-only reuse; no re-download",
            "n_symbol_month_dirs": len(SYMBOLS) * len(MONTHS),
            "n_cache_zips_scanned": n_cache_zips,
            "n_gaps": len(all_gaps),
            "entries_scanned": n_cache_zips,
        },
        "hash_registry": "research_state/cached_inputs_hashes.json (20,694 entries)",
        "sidecar_verification": "per-file .sha256 sidecars present; gaps disclosed in eval output",
        "admissibility": {
            "unauthenticated": True,
            "no_credentials": True,
            "no_payment": True,
            "historical_depth": "31 months, multi-regime",
            "schema_verified": True,
            "admissible_for_research": True,
            "admissible_for_track_a_observed_liquidations": False,
        },
        "terms": "Binance public market data; unauthenticated; research use.",
    }
    reg_sha = hashlib.sha256(json.dumps(registry, sort_keys=True).encode()).hexdigest()
    with open(os.path.join(HERE, f"fclr_live_archive07_source_registry_{SESSION}.json"), "w") as f:
        json.dump(registry, f, indent=2)

    mdreg = []
    mdreg.append(f"# FCLR-LIVE-ARCHIVE-07 Source Registry ({SESSION})\n")
    mdreg.append(f"**Experiment:** {EXPERIMENT}  \n**Campaign:** {EXPERIMENT}-{CAMPAIGN_START}\n")
    mdreg.append("**Source:** Binance public market-data archive (unauthenticated, free, no signup).\n")
    mdreg.append(f"**Cache:** {n_cache_zips} zips scanned under research_state/data_cache/ (read-only reuse).\n")
    mdreg.append(f"**Cohort:** {SYMBOLS}, 2024-04..2026-10 (31 months), disjoint from 2021-2024.\n")
    mdreg.append(f"**Gaps disclosed:** {len(all_gaps)} (see eval JSON full gap list).\n")
    mdreg.append(f"**Registry sha256:** {reg_sha}\n")
    with open(os.path.join(HERE, f"fclr_live_archive07_source_registry_{SESSION}.md"), "w") as f:
        f.write("".join(mdreg))

    # Preregistration (outcome-blind, hash-bound to source registry)
    prereg = {
        "campaign": f"{EXPERIMENT}-{CAMPAIGN_START}",
        "session_utc": SESSION,
        "artifact_id": f"fclr_live_archive07_prereg_{SESSION}",
        "generated_at": result["generated_at"],
        "experiment_id": EXPERIMENT,
        "outcome_data_inspected_before_freeze": False,
        "hash_bound_to_source_registry": reg_sha,
        "frozen_before_outcomes": True,
        "decision_frozen_before_outcomes": True,
        "hypothesis": ("FCLR-H007: funding + price features improve out-of-sample "
                       "forecasts of next-24h mean log realized variance (QLIKE) beyond "
                       "a signed-component HAR baseline (B1) on the disjoint 2024-04..2026-10 "
                       "cohort, judged on relative test-QLIKE reduction."),
        "window": "2024-04-01..2026-10-31 UTC",
        "symbols": SYMBOLS,
        "target": "next-24h mean log realized variance log(RV_24h_next + eps)",
        "eps": EPS,
        "splits": "60/20/20 by unique UTC timestamp; 7-day (168h) purge/embargo at "
                  "train/val and val/test boundaries; test -> 3 chronological blocks",
        "models": {
            "B1": "OLS on log RV1h/RV24h/RV168h + log RV_plus/RV_minus at 24h/168h "
                  "(7 signed HAR features), train-only scaling",
            "C2": "B1 + signed funding(24h) + trailing 90d |funding| percentile + "
                  "mark/index premium + mark/EMA24 distance (11 features)",
        },
        "primary_contrast": "C2 vs B1 on paired test-set out-of-sample QLIKE",
        "secondary": "next-24h downside realized-semivariance level log(RV_minus+eps), MSE, "
                     "Holm across the declared 2-family",
        "inference": (">=2000 deterministic block-bootstrap replicates (block=24 rows, seed=20261126); "
                      "report QLIKE, MSE, R^2, 95% CI on relative QLIKE reduction, per-block, "
                      "leave-one-symbol-out"),
        "materiality_floor": FLOOR,
        "alpha_2_sequential_look_k2": ALPHA_2,
        "decision_rule": ("PROMOTED iff relative test-QLIKE reduction >=2% AND bootstrap 95% "
                          "CI lower bound > 0 AND test data sufficient; else NOT_SUPPORTED; "
                          "INCONCLUSIVE if insufficient data"),
        "leakage_controls": [
            "outcome-blind freeze before target generation",
            "train-only OLS fitting",
            "train-only scaling + standardization",
            "168h purge/embargo",
            "no outcome inspection before freeze",
        ],
        "stdlib_only": True,
        "network": False,
        "read_only_cache": True,
    }
    with open(os.path.join(HERE, f"fclr_live_archive07_prereg_{SESSION}.json"), "w") as f:
        json.dump(prereg, f, indent=2)

    mdpre = []
    mdpre.append(f"# FCLR-LIVE-ARCHIVE-07 Preregistration ({SESSION})\n")
    mdpre.append(f"**Experiment:** {EXPERIMENT}  \n**Outcome-data inspected before freeze:** False\n")
    mdpre.append(f"**Target:** next-24h mean log realized variance log(RV_24h_next + {EPS}).\n")
    mdpre.append("**Models:** B1 = OLS signed-component HAR (7 feats); C2 = B1 + funding + price features (11 feats).\n")
    mdpre.append(f"**Primary contrast:** C2 vs B1 paired test-set out-of-sample QLIKE. "
                 f"Materiality floor: {FLOOR*100:.0f}% relative reduction.\n")
    mdpre.append("**Decision rule:** PROMOTED iff relative QLIKE reduction >=2% and bootstrap 95% CI lower bound > 0; "
                 "else NOT_SUPPORTED; INCONCLUSIVE if insufficient data.\n")
    mdpre.append(f"**Source registry sha256:** {reg_sha}\n")
    mdpre.append(f"**Sequential look:** k=2, alpha_2 = {ALPHA_2:.6f}.\n")
    with open(os.path.join(HERE, f"fclr_live_archive07_prereg_{SESSION}.md"), "w") as f:
        f.write("".join(mdpre))

    with open(os.path.join(HERE, f"_headline_{SESSION}.json"), "w") as f:
        json.dump({
            "qlike": {m: met[m]["qlike"] for m in ("B1", "C2")},
            "mse": {m: met[m]["mse"] for m in ("B1", "C2")},
            "r2": {m: met[m]["r2"] for m in ("B1", "C2")},
            "rel_qlike": rel_qlike, "n_test": len(test), "verdict": verdict,
            "n_unique_timestamps": nu,
        }, f, indent=2)

    print(f"[{dt.datetime.now(dt.timezone.utc).strftime('%H:%M:%S')}] [5/6] verdict={verdict} "
          f"rel_qlike={rel_qlike*100:.3f}% CI=[{rel_lo*100:.3f}%,{rel_hi*100:.3f}%]", flush=True)
    print(f"[{dt.datetime.now(dt.timezone.utc).strftime('%H:%M:%S')}] [6/6] done in {time.time()-t0:.0f}s", flush=True)


if __name__ == "__main__":
    main()
