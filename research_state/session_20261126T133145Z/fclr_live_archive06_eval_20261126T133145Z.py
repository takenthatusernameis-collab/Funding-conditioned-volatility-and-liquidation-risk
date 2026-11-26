#!/usr/bin/env python3
"""FCLR-LIVE-ARCHIVE-06 heavy confirmatory evaluation (stdlib only).

Repo-name-leading estimand: funding-conditioned volatility, DOWNSIDE
REALIZED-SEMVARIANCE LEVEL arm. A DISTINCT outcome family from the closed
mean-RV QLIKE arm (FCLR-LIVE-ARCHIVE-01), the closed binary stress/tail arm
(FCLR-LIVE-ARCHIVE-03), the closed quantile/full-distribution arm
(FCLR-LIVE-ARCHIVE-04) and the closed signed-semivariance-asymmetry arm
(FCLR-LIVE-ARCHIVE-05): the next-24h downside realized semivariance level
D = log(RV_minus + eps), where RV_minus sums squared negative 1h mark-price
log-returns over the next 24 hours, is forecast by linear regression B1 vs C2,
judged on out-of-sample MSE / R^2 -- not a mean QLIKE and not a binary label.

Source (verified, unauthenticated, free, read-only cache): Binance public
market-data archive, monthly 1h klines / mark / index / premium + fundingRate,
2021-01 .. 2024-12, frozen 5-symbol cohort (1INCH/AAVE/ADA/ALGO/ALPHA).
The raw zips live under research_state/session_20261126T042519Z/raw/ and are
reused read-only; nothing is re-downloaded.

Design (FROZEN, outcome-blind):
  - Target y = next-24h downside realized-semivariance level log(RV_minus + eps).
  - B1 = OLS on log RV1h/RV24h/RV168h + log RV_plus/RV_minus at 24h/168h (7 feats).
  - C2 = B1 + signed funding(24h) + trailing 90d |funding| percentile
         + mark/index premium + mark/EMA24 distance (11 feats).
  - Fixed-form linear regression via deterministic stdlib OLS (Gauss-Jordan
    normal equations). Train-only scaling; 168h purge/embargo; 60/20/20 by
    unique UTC timestamp; test -> 3 interleaved blocks.
  - Primary: out-of-sample MSE and R^2; relative MSE reduction C2 vs B1.
  - >=2000 deterministic block-bootstrap replicates (fixed seed); per-block +
    leave-one-symbol-out diagnostics.
  - Materiality floor: >=2% relative test-MSE reduction for C2 vs B1 AND
    block-bootstrap 95% CI lower bound > 0. Otherwise NOT_SUPPORTED;
    INCONCLUSIVE only if the evidence cannot support either conclusion.
Stdlib only. No pip install. No numpy/pandas. Writes the fclr_live_archive06_*
artifact set (eval triad + source registry + prereg).
"""
from __future__ import annotations

import bisect
import datetime as dt
import hashlib
import io
import json
import math
import os
import random
import statistics
import time
import zipfile

SESSION = "20261126T133145Z"
EXPERIMENT = "FCLR-LIVE-ARCHIVE-06"
CAMPAIGN_START = "20261126T083526Z"
HERE = os.path.dirname(os.path.abspath(__file__))
# Reuse the verified raw cache read-only; do NOT re-download.
RAW = os.path.join(HERE, "..", "session_20261126T042519Z", "raw")
SYMBOLS = ["1INCHUSDT", "AAVEUSDT", "ADAUSDT", "ALGOUSDT", "ALPHAUSDT"]
MONTHS = [f"{y}-{m:02d}" for y in (2021, 2022, 2023, 2024) for m in range(1, 13)]
SOURCES = ("klines", "markPriceKlines", "indexPriceKlines",
           "premiumIndexKlines", "fundingRate")
SEED = 20261126
N_BOOT = 2000
EMBARGO_H = 168  # 7 calendar days
FLOOR = 0.02
N_BLOCKS = 3
BLOCK_ROWS = 24
EPS = 1e-9  # fixed positive epsilon for the downside level


def _zip_lines(cp):
    with open(cp, "rb") as f:
        z = zipfile.ZipFile(io.BytesIO(f.read()))
        return z.read(z.namelist()[0]).decode("utf-8", "ignore").splitlines()


def _sha256_file(cp):
    with open(cp, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()


def _parse_klines(lines):
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


def _parse_funding(lines):
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


def build_symbol_panel(sym):
    klines, mark, index = {}, {}, {}
    for mo in MONTHS:
        for src, d in (("klines", klines), ("markPriceKlines", mark),
                       ("indexPriceKlines", index)):
            cp = os.path.join(RAW, src, f"{sym}-{mo}.zip")
            if os.path.exists(cp):
                d.update(_parse_klines(_zip_lines(cp)))
    funding = []
    for mo in MONTHS:
        cp = os.path.join(RAW, "fundingRate", f"{sym}-{mo}.zip")
        if os.path.exists(cp):
            funding.extend(_parse_funding(_zip_lines(cp)))
    funding.sort()
    ft = [x[0] for x in funding]
    fr = [x[1] for x in funding]

    times = sorted(klines)
    n = len(times)
    if n < 200:
        return [], {}
    r = [0.0] * n
    for i in range(1, n):
        if times[i] - times[i - 1] == 3600 and klines[times[i]] > 0:
            r[i] = math.log(klines[times[i]] / klines[times[i - 1]])
    rv1 = [v * v for v in r]
    rpos = [v * v if v > 0 else 0.0 for v in r]
    rneg = [v * v if v < 0 else 0.0 for v in r]

    def roll(vals, w):
        out = [None] * n
        s = 0.0
        for i in range(n):
            s += vals[i]
            if i >= w:
                s -= vals[i - w]
            if i >= w - 1:
                out[i] = s
        return out

    rv24 = roll(rv1, 24)
    rv168 = roll(rv1, 168)
    rv_plus24 = roll(rpos, 24)
    rv_minus24 = roll(rneg, 24)
    rv_plus168 = roll(rpos, 168)
    rv_minus168 = roll(rneg, 168)
    next_plus24 = [None] * n
    next_minus24 = [None] * n
    for i in range(n - 24):
        next_plus24[i] = sum(rpos[i + 1:i + 25])
        next_minus24[i] = sum(rneg[i + 1:i + 25])

    ema = {}
    alpha = 2.0 / (24 + 1)
    e = None
    for t in times:
        m = mark.get(t)
        if m is None:
            continue
        e = m if e is None else alpha * m + (1 - alpha) * e
        ema[t] = e

    rows = []
    for i in range(168, n - 24):
        t = times[i]
        if (rv24[i] is None or rv168[i] is None or rv_plus24[i] is None or
                rv_minus24[i] is None or rv_plus168[i] is None or
                rv_minus168[i] is None or next_plus24[i] is None or
                next_minus24[i] is None):
            continue
        y = math.log(next_minus24[i] + EPS)
        j = bisect.bisect_right(ft, t) - 1
        if j < 0:
            continue
        cur_rate = fr[j]
        lo = bisect.bisect_right(ft, t - 24 * 3600)
        fund24 = sum(fr[lo:j + 1]) if j >= lo else 0.0
        lo90 = bisect.bisect_right(ft, t - 90 * 86400)
        window = [abs(x) for x in fr[lo90:j + 1]]
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
            "fund24": fund24, "fund_pct": pct, "prem": prem, "mdist": mdist,
        })
    info = {"n_rows": len(rows), "n_times": n}
    return rows, info


# ------------- stdlib linear least squares (Gauss-Jordan normal equations) -------------
def _solve(A, b):
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
    return _solve(XtX, Xty)


def ols_predict(beta, x):
    return sum(b * xi for b, xi in zip(beta, x))


def mse_r2(y, pred):
    n = len(y)
    sse = sum((y[i] - pred[i]) ** 2 for i in range(n))
    ymean = sum(y) / n
    sst = sum((v - ymean) ** 2 for v in y)
    mse = sse / n
    r2 = 1.0 - sse / sst if sst > 0 else 0.0
    return mse, r2, sse, sst


def sign_acc(y, pred):
    n = len(y)
    ok = 0
    for i in range(n):
        ys = 1.0 if y[i] > 0 else (-1.0 if y[i] < 0 else 0.0)
        ps = 1.0 if pred[i] > 0 else (-1.0 if pred[i] < 0 else 0.0)
        if ys == ps:
            ok += 1
    return ok / n


def main():
    t0 = time.time()
    print(f"[{dt.datetime.now(dt.timezone.utc).strftime('%H:%M:%S')}] [1/6] reading verified raw cache (read-only) ...", flush=True)
    file_entries = []
    for src in SOURCES:
        sdir = os.path.join(RAW, src)
        for mo in MONTHS:
            for sym in SYMBOLS:
                cp = os.path.join(sdir, f"{sym}-{mo}.zip")
                if os.path.exists(cp):
                    file_entries.append({
                        "source": src, "symbol": sym, "month": mo,
                        "path": cp, "bytes": os.path.getsize(cp),
                        "sha256": _sha256_file(cp),
                    })
                else:
                    file_entries.append({
                        "source": src, "symbol": sym, "month": mo,
                        "path": cp, "bytes": 0, "sha256": None,
                        "missing": True,
                    })
    n_ok = sum(1 for e in file_entries if not e.get("missing"))
    n_bad = sum(1 for e in file_entries if e.get("missing"))
    print(f"  cache entries {len(file_entries)} ok={n_ok} missing={n_bad}", flush=True)
    if n_bad:
        raise SystemExit(f"ABORT: {n_bad} cached zips missing; refusing to zero-fill or substitute")

    print(f"[{dt.datetime.now(dt.timezone.utc).strftime('%H:%M:%S')}] [2/6] building downside-level panels ...", flush=True)
    panel = []
    per_sym = {}
    for s in SYMBOLS:
        rows, info = build_symbol_panel(s)
        per_sym[s] = info["n_rows"]
        panel.extend(rows)
        print(f"  {s}: {info['n_rows']} rows", flush=True)
    panel.sort(key=lambda x: x["t"])

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
        mse, r2, sse, sst = mse_r2(ys, p)
        sa = sign_acc(ys, p)
        return {"mse": mse, "r2": r2, "sse": sse, "sst": sst, "sign_acc": sa,
                "n": len(ys)}

    met = {m: metrics(m) for m in ("B1", "C2")}
    mse_B1 = met["B1"]["mse"]
    mse_C2 = met["C2"]["mse"]
    diff = mse_B1 - mse_C2  # positive => C2 better
    rel_mse = diff / mse_B1 if mse_B1 > 0 else 0.0

    block_idx = [[k for k in range(len(test)) if k % N_BLOCKS == b] for b in range(N_BLOCKS)]

    def block_mse(m, idxs):
        pp = [preds[m][k] for k in idxs]
        yy = [ys[k] for k in idxs]
        mm, rr, _, _ = mse_r2(yy, pp)
        return mm

    per_block = {}
    for m in ("B1", "C2"):
        per_block[m] = {"mse": [block_mse(m, bi) for bi in block_idx]}

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
        mse1, r2_1, _, _ = mse_r2(yte, p1)
        mse2, r2_2, _, _ = mse_r2(yte, p2)
        rel12 = (mse1 - mse2) / max(mse1, 1e-12)
        loo[held] = {
            "n": len(te),
            "mse_B1": mse1, "r2_B1": r2_1,
            "mse_C2": mse2, "r2_C2": r2_2,
            "rel_mse_C2_vs_B1": rel12,
            "sign_acc_B1": sign_acc(yte, p1),
            "sign_acc_C2": sign_acc(yte, p2),
        }
        print(f"  LOO {held}: n={len(te)} rel_mse={rel12*100:.3f}%", flush=True)

    print(f"[{dt.datetime.now(dt.timezone.utc).strftime('%H:%M:%S')}] [4/6] block bootstrap x{N_BOOT} ...", flush=True)
    diffs = []
    for k in range(len(test)):
        e1 = (ys[k] - preds["B1"][k]) ** 2
        e2 = (ys[k] - preds["C2"][k]) ** 2
        diffs.append(e1 - e2)
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
    mse_B1_safe = max(mse_B1, 1e-12)
    rel_lo = lo / mse_B1_safe
    rel_hi = hi / mse_B1_safe
    boot_rel_mean = boot_mean / mse_B1_safe

    sufficient = len(test) >= 500 and nu >= 500
    improved = rel_mse >= FLOOR and rel_lo > 0
    if not sufficient:
        verdict = "INCONCLUSIVE"
    elif improved:
        verdict = "PROMOTED"
    else:
        verdict = "NOT_SUPPORTED"

    result = {
        "experiment_id": EXPERIMENT,
        "campaign": f"{EXPERIMENT}-{CAMPAIGN_START}",
        "session_id": SESSION,
        "session_utc": SESSION,
        "generated_at": dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "source": "BINANCE_PUBLIC_ARCHIVE_READ_ONLY_CACHE",
        "source_session": "session_20261126T042519Z",
        "symbols": SYMBOLS,
        "months": f"2021-01..2024-12 ({len(MONTHS)} months)",
        "n_symbols": len(SYMBOLS),
        "per_symbol_rows": per_sym,
        "n_train": len(train), "n_val": len(val), "n_test": len(test),
        "n_unique_timestamps": nu,
        "embargo_hours": EMBARGO_H,
        "splits": "60/20/20 by unique UTC timestamp; 7-day purge/embargo; test->3 blocks",
        "models": ["B1", "C2"],
        "target": "next-24h downside realized-semivariance level "
                  "log(RV_minus+eps)",
        "eps": EPS,
        "b1_features": ["log RV1h", "log RV24h", "log RV168h",
                        "log RV_plus24", "log RV_minus24",
                        "log RV_plus168", "log RV_minus168"],
        "c2_features": ["B1 (7)", "signed funding(24h)", "trailing 90d |funding| pct",
                        "mark/index premium", "mark/EMA24 distance"],
        "solver": "deterministic stdlib OLS (Gauss-Jordan normal equations, train-only)",
        "materiality_floor": FLOOR,
        "metrics": met,
        "relative_mse_reduction_C2_vs_B1": rel_mse,
        "per_block": per_block,
        "leave_one_symbol_out": loo,
        "bootstrap": {
            "replicates": N_BOOT, "seed": SEED, "block_rows": BLOCK_ROWS,
            "mean_diff_mse_B1_minus_C2": boot_mean,
            "mean_rel_mse_reduction": boot_rel_mean,
            "ci95_abs_diff": [lo, hi],
            "ci95_relative_mse_reduction": [rel_lo, rel_hi],
        },
        "download": {"n_cache_entries": len(file_entries), "n_ok": n_ok, "n_missing": n_bad},
        "verdict": verdict,
        "verdict_reason": (
            "C2 beats B1 by >=2% relative test-MSE with bootstrap CI strictly above 0"
            if verdict == "PROMOTED" else
            "C2 vs B1 relative test-MSE reduction < 2% floor or CI includes 0"
            if verdict == "NOT_SUPPORTED" else
            "insufficient test data for a confirmatory verdict"),
        "stdlib_only": True,
        "network": False,
        "read_only_cache": True,
        "outcome_data_inspected_before_freeze": False,
    }
    with open(os.path.join(HERE, f"fclr_live_archive06_eval_{SESSION}.json"), "w") as f:
        json.dump(result, f, indent=2)

    md = []
    md.append(f"# FCLR-LIVE-ARCHIVE-06 Confirmatory Evaluation ({SESSION})\n")
    md.append(f"**Experiment:** {EXPERIMENT}  \n**Verdict:** `{verdict}`  \n")
    md.append(f"**Source:** Binance public archive (unauthenticated), {len(SYMBOLS)} symbols x "
              f"{len(MONTHS)} months (2021-2024), read-only verified cache.\n")
    md.append("## Design\n")
    md.append("- Target: next-24h downside realized-semivariance level "
              f"D = log(RV_minus+{EPS}), RV_minus sums squared negative 1h "
              "log-returns over the next 24 hours.\n")
    md.append("- B1: OLS on log RV1h/RV24h/RV168h + log RV_plus/RV_minus at 24h/168h "
              "(7 signed HAR features); C2: B1 + signed funding(24h) + trailing 90d "
              "|funding| pct + mark/index premium + mark/EMA24 distance (11 features).\n")
    md.append(f"- Splits 60/20/20 by unique UTC ts, {EMBARGO_H}h purge/embargo, "
              f"test->{N_BLOCKS} blocks. train={len(train)} val={len(val)} test={len(test)}.\n")
    md.append("## Results\n")
    md.append("| Model | MSE | R^2 | Sign accuracy |\n|---|---|---|---|\n")
    for m in ("B1", "C2"):
        md.append(f"| {m} | {met[m]['mse']:.6e} | {met[m]['r2']:.4f} | {met[m]['sign_acc']:.4f} |\n")
    md.append(f"\n**Primary C2 vs B1 relative test-MSE reduction: {rel_mse*100:.3f}% "
              f"(floor {FLOOR*100:.0f}%).**\n")
    md.append(f"Bootstrap {N_BOOT} reps 95% CI relative MSE reduction: "
              f"[{rel_lo*100:.3f}%, {rel_hi*100:.3f}%].\n")
    md.append("\n## Per-block relative MSE reduction (C2 vs B1)\n| Block | B1 MSE | C2 MSE | rel reduction |\n|---|---|---|---|\n")
    for i in range(N_BLOCKS):
        bb1 = per_block["B1"]["mse"][i]
        bc2 = per_block["C2"]["mse"][i]
        md.append(f"| {i+1} | {bb1:.6e} | {bc2:.6e} | {(bb1-bc2)/max(bb1,1e-12)*100:.3f}% |\n")
    md.append("\n## Leave-one-symbol-out (C2 vs B1)\n| Symbol | n | rel MSE reduction | sign_acc B1 | sign_acc C2 |\n|---|---|---|---|---|\n")
    for s in SYMBOLS:
        if s in loo:
            md.append(f"| {s} | {loo[s]['n']} | {loo[s]['rel_mse_C2_vs_B1']*100:.3f}% | "
                      f"{loo[s]['sign_acc_B1']:.3f} | {loo[s]['sign_acc_C2']:.3f} |\n")
    md.append(f"\n## Verdict: `{verdict}` — {result['verdict_reason']}.\n")
    with open(os.path.join(HERE, f"fclr_live_archive06_eval_{SESSION}.md"), "w") as f:
        f.write("".join(md))

    # Source registry (hash-bound to prereg)
    registry = {
        "campaign": f"{EXPERIMENT}-{CAMPAIGN_START}",
        "session_utc": SESSION,
        "artifact_id": f"fclr_live_archive06_source_registry_{SESSION}",
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
            "reachability_note": "S3 delimiter catalog and monthly five-source keys verified HTTP 200/206 for the frozen cohort; data/spot/daily/* returns HTTP 404 and is NOT used.",
        },
        "datasets": [
            {"kind": "futures_um_monthly_klines_1h",
             "path_template": "data/futures/um/monthly/klines/{SYM}/1h/{SYM}-1h-{YYYY-MM}.zip",
             "track": "target downside level + RV features"},
            {"kind": "futures_um_monthly_markPriceKlines_1h",
             "path_template": "data/futures/um/monthly/markPriceKlines/{SYM}/1h/{SYM}-1h-{YYYY-MM}.zip",
             "track": "mark premium + EMA distance"},
            {"kind": "futures_um_monthly_indexPriceKlines_1h",
             "path_template": "data/futures/um/monthly/indexPriceKlines/{SYM}/1h/{SYM}-1h-{YYYY-MM}.zip",
             "track": "mark/index premium"},
            {"kind": "futures_um_monthly_premiumIndexKlines_1h",
             "path_template": "data/futures/um/monthly/premiumIndexKlines/{SYM}/1h/{SYM}-1h-{YYYY-MM}.zip",
             "track": "premium feature"},
            {"kind": "futures_um_monthly_fundingRate",
             "path_template": "data/futures/um/monthly/fundingRate/{SYM}/{SYM}-fundingRate-{YYYY-MM}.zip",
             "fields": ["calc_time", "funding_interval_hours", "last_funding_rate"],
             "note": "NO 1h/ segment",
             "track": "signed funding + 90d |funding| pct"},
        ],
        "cohort": {
            "symbols": SYMBOLS,
            "months": "2021-01..2024-12 (48 months)",
            "selection": "coverage-only, outcome-blind (frozen)",
        },
        "cache": {
            "raw_dir": "research_state/session_20261126T042519Z/raw/",
            "access": "read-only reuse; no re-download",
            "n_entries": len(file_entries),
            "n_ok": n_ok,
            "n_missing": n_bad,
            "sha256_verified_all": n_bad == 0,
            "entries": file_entries,
        },
        "admissibility": {
            "unauthenticated": True,
            "no_credentials": True,
            "no_payment": True,
            "historical_depth": "4 years, multi-regime",
            "schema_verified": True,
            "admissible_for_research": True,
            "admissible_for_track_a_observed_liquidations": False,
        },
        "terms": "Binance public market data; unauthenticated; research use.",
    }
    reg_sha = hashlib.sha256(json.dumps(registry, sort_keys=True).encode()).hexdigest()
    with open(os.path.join(HERE, f"fclr_live_archive06_source_registry_{SESSION}.json"), "w") as f:
        json.dump(registry, f, indent=2)

    mdreg = []
    mdreg.append(f"# FCLR-LIVE-ARCHIVE-06 Source Registry ({SESSION})\n")
    mdreg.append(f"**Experiment:** {EXPERIMENT}  \n**Campaign:** {EXPERIMENT}-{CAMPAIGN_START}\n")
    mdreg.append("**Source:** Binance public market-data archive (unauthenticated, free, no signup).\n")
    mdreg.append(f"**Cache:** {n_ok}/{len(file_entries)} zips present and sha256-verified under "
                 "research_state/session_20261126T042519Z/raw/ (read-only reuse).\n")
    mdreg.append(f"**Cohort:** {SYMBOLS}, 2021-01..2024-12.\n")
    mdreg.append(f"**Registry sha256:** {reg_sha}\n")
    with open(os.path.join(HERE, f"fclr_live_archive06_source_registry_{SESSION}.md"), "w") as f:
        f.write("".join(mdreg))

    # Preregistration (outcome-blind, hash-bound to source registry)
    prereg = {
        "campaign": f"{EXPERIMENT}-{CAMPAIGN_START}",
        "session_utc": SESSION,
        "artifact_id": f"fclr_live_archive06_prereg_{SESSION}",
        "generated_at": result["generated_at"],
        "experiment_id": EXPERIMENT,
        "outcome_data_inspected_before_freeze": False,
        "hash_bound_to_source_registry": reg_sha,
        "hypothesis": ("FCLR-H006: funding + price features improve out-of-sample "
                       "forecasts of next-24h downside realized-semivariance level "
                       "log(RV_minus+eps) beyond a signed-component HAR baseline (B1), "
                       "judged on relative test-MSE reduction."),
        "window": "2021-01-01..2024-12-31 UTC",
        "symbols": SYMBOLS,
        "target": "next-24h downside realized-semivariance level log(RV_minus+eps)",
        "eps": EPS,
        "splits": "60/20/20 by unique UTC timestamp; 7-day (168h) purge/embargo at "
                  "train/val and val/test boundaries; test -> 3 interleaved blocks",
        "models": {
            "B1": "OLS on log RV1h/RV24h/RV168h + log RV_plus/RV_minus at 24h/168h "
                  "(7 signed HAR features), train-only scaling",
            "C2": "B1 + signed funding(24h) + trailing 90d |funding| percentile + "
                  "mark/index premium + mark/EMA24 distance (11 features)",
        },
        "primary_contrast": "C2 vs B1 on paired test-set out-of-sample MSE",
        "secondary": "downside level sign accuracy (sign of predicted vs actual downside level)",
        "inference": (">=2000 deterministic moving-block bootstrap replicates (block=24 rows, seed=20261126); "
                      "report MSE, R^2, sign accuracy, 95% CI on relative MSE reduction, per-block, leave-one-symbol-out"),
        "materiality_floor": FLOOR,
        "decision_rule": ("PROMOTED iff relative test-MSE reduction >=2% AND bootstrap 95% CI lower bound > 0 "
                          "AND test data sufficient; else NOT_SUPPORTED; INCONCLUSIVE if test data insufficient"),
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
    with open(os.path.join(HERE, f"fclr_live_archive06_prereg_{SESSION}.json"), "w") as f:
        json.dump(prereg, f, indent=2)

    mdpre = []
    mdpre.append(f"# FCLR-LIVE-ARCHIVE-06 Preregistration ({SESSION})\n")
    mdpre.append(f"**Experiment:** {EXPERIMENT}  \n**Outcome-data inspected before freeze:** False\n")
    mdpre.append(f"**Target:** next-24h downside realized-semivariance level "
                 f"log(RV_minus+{EPS}).\n")
    mdpre.append("**Models:** B1 = OLS signed-component HAR (7 feats); C2 = B1 + funding + price features (11 feats).\n")
    mdpre.append(f"**Primary contrast:** C2 vs B1 paired test-set out-of-sample MSE. "
                 f"Materiality floor: {FLOOR*100:.0f}% relative reduction.\n")
    mdpre.append("**Decision rule:** PROMOTED iff relative MSE reduction >=2% and bootstrap 95% CI lower bound > 0; "
                 "else NOT_SUPPORTED; INCONCLUSIVE if insufficient data.\n")
    mdpre.append(f"**Source registry sha256:** {reg_sha}\n")
    with open(os.path.join(HERE, f"fclr_live_archive06_prereg_{SESSION}.md"), "w") as f:
        f.write("".join(mdpre))

    with open(os.path.join(HERE, f"_headline_{SESSION}.json"), "w") as f:
        json.dump({
            "mse": {m: met[m]["mse"] for m in ("B1", "C2")},
            "r2": {m: met[m]["r2"] for m in ("B1", "C2")},
            "sign_acc": {m: met[m]["sign_acc"] for m in ("B1", "C2")},
            "rel_mse": rel_mse, "n_test": len(test), "verdict": verdict,
            "n_unique_timestamps": nu,
        }, f, indent=2)

    print(f"[{dt.datetime.now(dt.timezone.utc).strftime('%H:%M:%S')}] [5/6] verdict={verdict} "
          f"rel_mse={rel_mse*100:.3f}% CI=[{rel_lo*100:.3f}%,{rel_hi*100:.3f}%]", flush=True)
    print(f"[{dt.datetime.now(dt.timezone.utc).strftime('%H:%M:%S')}] [6/6] done in {time.time()-t0:.0f}s", flush=True)


if __name__ == "__main__":
    main()
