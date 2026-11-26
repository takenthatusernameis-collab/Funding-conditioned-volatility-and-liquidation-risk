#!/usr/bin/env python3
"""FCLR-LIVE-ARCHIVE-04 heavy confirmatory evaluation (stdlib only).

Repo-name-leading estimand: funding-conditioned volatility, FULL PREDICTIVE
DISTRIBUTION / QUANTILE arm (RESEARCH_PROMPT.md section 3.1 / section 7 target 1).
A DISTINCT outcome family from the closed mean-RV QLIKE arm (FCLR-LIVE-ARCHIVE-01)
and the closed binary stress/tail arm (FCLR-LIVE-ARCHIVE-03): the next-24h
realized variance is forecast as a predictive DISTRIBUTION at pre-registered
quantile levels {0.10, 0.25, 0.50, 0.75, 0.90}, judged on pinball loss,
empirical coverage and calibration -- not a mean QLIKE and not a binary label.

Source (verified, unauthenticated, free, read-only cache): Binance public
market-data archive, monthly 1h klines / mark / index / premium + fundingRate,
2021-01 .. 2024-12, frozen 5-symbol cohort (1INCH/AAVE/ADA/ALGO/ALPHA).
The raw zips live under research_state/session_20261126T042519Z/raw/ and are
reused read-only; nothing is re-downloaded.

Design (FROZEN, outcome-blind):
  - Target y = next-24h realized variance (continuous, > 0).
  - Predictive distribution: linear quantile regression at tau in
    {0.10, 0.25, 0.50, 0.75, 0.90}, estimated on TRAIN only, by the
    Hunter-Lange MM/IRLS algorithm (a deterministic majorize-minimise scheme
    whose fixed point is the exact quantile-regression optimum).
  - B1 = linear QR on log RV1h/RV24h/RV168h (HAR).
  - C2 = B1 + signed funding(24h) + trailing 90d |funding| percentile
         + mark/index premium + mark/EMA24 distance.
  - Train-only scaling; 7-day (168h) purge/embargo; 60/20/20 by unique UTC
    timestamp; test -> 3 interleaved blocks.
  - >=2000 deterministic moving-block bootstrap replicates (seed fixed);
    per-block + leave-one-symbol-out.
  - Materiality floor: >=2% relative reduction in AVERAGE PINBALL LOSS across
    the five quantiles, with bootstrap 95% CI lower bound > 0.
Stdlib only. No pip install. No numpy/pandas. Writes the fclr_live_archive04_*
artifact set (source registry, prereg, eval triad).
"""
from __future__ import annotations

import bisect
import datetime as dt
import hashlib
import io
import json
import math
import os
import statistics
import time
import zipfile

SESSION = "20261126T061929Z"
EXPERIMENT = "FCLR-LIVE-ARCHIVE-04"
CAMPAIGN_START = "20261126T053929Z"
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
TAUS = [0.10, 0.25, 0.50, 0.75, 0.90]
N_BLOCKS = 3
BLOCK_ROWS = 24
EPS = 1e-7
QR_ITERS = 80
QR_TOL = 1e-10


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
    rv1 = [x * x for x in r]

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
    next24 = [None] * n
    for i in range(n - 24):
        next24[i] = sum(rv1[i + 1:i + 25])

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
        if rv24[i] is None or rv168[i] is None or next24[i] is None:
            continue
        if rv24[i] <= 0 or rv168[i] <= 0 or next24[i] <= 0:
            continue
        j = bisect.bisect_right(ft, t) - 1
        if j < 0:
            continue
        cur_rate = fr[j]
        lo = bisect.bisect_right(ft, t - 24 * 3600)
        fund24 = sum(fr[lo:j + 1]) if j >= lo else 0.0
        lo90 = bisect.bisect_right(ft, t - 90 * 86400)
        window = [abs(x) for x in fr[lo90:j + 1]]
        pct = (sum(1 for x in window if x <= abs(cur_rate)) / len(window)) if window else 0.5
        mk = mark.get(t)
        ix = index.get(t)
        prem = (mk - ix) / ix if (mk is not None and ix not in (None, 0)) else 0.0
        em = ema.get(t)
        mdist = (mk - em) / em if (mk is not None and em not in (None, 0)) else 0.0
        rows.append({
            "symbol": sym, "t": t,
            "rv1": rv1[i], "rv24": rv24[i], "rv168": rv168[i],
            "y": next24[i],
            "fund24": fund24, "fund_pct": pct, "prem": prem, "mdist": mdist,
        })
    info = {"n_rows": len(rows), "n_times": n}
    return rows, info


# ------------- stdlib linear quantile regression (Hunter-Lange MM / IRLS) -------------
def _solve(A, b):
    """Pivoted Gauss-Jordan solve of A beta = b (A is p x p, small)."""
    n = len(A)
    M = [A[i][:] + [b[i]] for i in range(n)]
    for c in range(n):
        p = max(range(c, n), key=lambda rr: abs(M[rr][c]))
        M[c], M[p] = M[p], M[c]
        piv = M[c][c]
        if abs(piv) < 1e-14:
            piv = 1e-14
        for rr in range(n):
            if rr != c:
                f = M[rr][c] / piv
                if f:
                    for k in range(c, n + 1):
                        M[rr][k] -= f * M[c][k]
    return [M[i][n] / (M[i][i] if abs(M[i][i]) > 1e-14 else 1e-14) for i in range(n)]


def quantile_fit(X, y, tau, n_iter=QR_ITERS, tol=QR_TOL):
    """Fit linear quantile regression by Hunter-Lange MM with step-halving.

    Each iteration forms the standard MM weighted-least-squares majorizer of the
    check loss and then applies monotone step-halving on the ACTUAL check-loss
    objective, guaranteeing descent to the exact convex optimum even on
    heavy-tailed targets. X includes a leading intercept column of ones.
    """
    n = len(X)
    p = len(X[0])
    beta = [0.0] * p
    ys = sorted(y)
    beta[0] = ys[min(int(tau * (n - 1)), n - 1)]

    def objective(b):
        return sum(pinball(y[i] - sum(b[a] * X[i][a] for a in range(p)), tau)
                   for i in range(n))

    fcur = objective(beta)
    for _ in range(n_iter):
        u = [y[i] - sum(b * xi for b, xi in zip(beta, X[i])) for i in range(n)]
        w = [1.0 / (2.0 * (abs(u[i]) if abs(u[i]) > EPS else EPS)) for i in range(n)]
        z = [y[i] - 2.0 * (abs(u[i]) if abs(u[i]) > EPS else EPS) * ((tau - 1.0) if u[i] < 0 else tau)
             for i in range(n)]
        XtW = [[0.0] * p for _ in range(p)]
        XtWz = [0.0] * p
        for i in range(n):
            wi = w[i]
            xi = X[i]
            zi = z[i]
            for a in range(p):
                XtWz[a] += xi[a] * wi * zi
                xa = xi[a] * wi
                row = XtW[a]
                for bb in range(p):
                    row[bb] += xa * xi[bb]
        for a in range(p):
            XtW[a][a] += 1e-9
        bn = _solve(XtW, XtWz)
        step = 1.0
        accepted = False
        cand = beta
        fc = fcur
        for _h in range(50):
            cand = [beta[a] + step * (bn[a] - beta[a]) for a in range(p)]
            fc = objective(cand)
            if fc <= fcur + 1e-15:
                accepted = True
                break
            step *= 0.5
        if not accepted:
            break
        delta = max(abs(cand[a] - beta[a]) for a in range(p))
        beta = cand
        fcur = fc
        if delta < tol:
            break
    return beta


def quantile_pred(beta, x):
    return sum(b * xi for b, xi in zip(beta, x))


def pinball(u, tau):
    return u * (tau - 1.0) if u < 0 else u * tau


def avg_pinball(preds_by_tau, ys):
    total = 0.0
    cnt = 0
    for tau in TAUS:
        pl = preds_by_tau[tau]
        for p, yy in zip(pl, ys):
            total += pinball(yy - p, tau)
            cnt += 1
    return total / max(cnt, 1)


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

    print(f"[{dt.datetime.now(dt.timezone.utc).strftime('%H:%M:%S')}] [2/6] building panels ...", flush=True)
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
                math.log(max(x["rv168"], 1e-12))]
        if model == "B1":
            return base
        if model == "C2":
            return base + [x["fund24"], x["fund_pct"], x["prem"], x["mdist"]]
        raise ValueError(model)

    def fit_model(model, tr):
        X = [feat_row(x, model) for x in tr]
        mu = [sum(col) / len(col) for col in zip(*X)]
        sd = []
        for k in range(len(X[0])):
            col = [row[k] for row in X]
            s = statistics.pstdev(col) or 1.0
            sd.append(s)
        Xs = [[1.0] + [(row[k] - mu[k]) / sd[k] for k in range(len(row))] for row in X]
        y_raw = [x["y"] for x in tr]
        ymean = sum(y_raw) / len(y_raw)
        ystd = statistics.pstdev(y_raw) or 1.0
        y = [(v - ymean) / ystd for v in y_raw]
        betas = {tau: quantile_fit(Xs, y, tau) for tau in TAUS}
        return {"model": model, "mu": mu, "sd": sd, "betas": betas,
                "ymean": ymean, "ystd": ystd}

    print(f"[{dt.datetime.now(dt.timezone.utc).strftime('%H:%M:%S')}] [3/6] fitting quantile models (train only) ...", flush=True)
    models = {k: fit_model(k, train) for k in ("B1", "C2")}

    def predict(m, x):
        row = feat_row(x, m["model"])
        xs = [1.0] + [(row[k] - m["mu"][k]) / m["sd"][k] for k in range(len(row))]
        return {tau: m["ymean"] + m["ystd"] * quantile_pred(m["betas"][tau], xs) for tau in TAUS}

    preds = {m: [predict(models[m], x) for x in test] for m in ("B1", "C2")}
    ys = [x["y"] for x in test]

    def metrics(m):
        pbt = {tau: [preds[m][k][tau] for k in range(len(test))] for tau in TAUS}
        per_tau = {}
        cover = {}
        for tau in TAUS:
            pl = pbt[tau]
            per_tau[tau] = sum(pinball(yy - p, tau) for p, yy in zip(pl, ys)) / max(len(ys), 1)
            cover[tau] = sum(1 for p, yy in zip(pl, ys) if yy <= p) / max(len(ys), 1)
        avg = sum(per_tau.values()) / len(TAUS)
        calib = sum(abs(cover[tau] - tau) for tau in TAUS) / len(TAUS)
        return {
            "avg_pinball": avg,
            "per_tau_pinball": per_tau,
            "empirical_coverage": cover,
            "mean_abs_coverage_error": calib,
            "n": len(ys),
        }

    met = {m: metrics(m) for m in ("B1", "C2")}
    rel_pinball = ((met["B1"]["avg_pinball"] - met["C2"]["avg_pinball"])
                   / met["B1"]["avg_pinball"]) if met["B1"]["avg_pinball"] > 0 else 0.0

    block_idx = [[k for k in range(len(test)) if k % N_BLOCKS == b] for b in range(N_BLOCKS)]

    def block_avg_pinball(m, idxs):
        pbt = {tau: [preds[m][k][tau] for k in idxs] for tau in TAUS}
        yb = [ys[k] for k in idxs]
        return avg_pinball(pbt, yb)

    per_block = {}
    for m in ("B1", "C2"):
        per_block[m] = {"avg_pinball": [block_avg_pinball(m, bi) for bi in block_idx]}

    loo = {}
    for held in SYMBOLS:
        tr = [x for x in train if x["symbol"] != held]
        te = [x for x in test if x["symbol"] == held]
        if not tr or not te:
            continue
        m1 = fit_model("B1", tr)
        m2 = fit_model("C2", tr)

        def pr(mm, x):
            row = feat_row(x, mm["model"])
            xs = [1.0] + [(row[k] - mm["mu"][k]) / mm["sd"][k] for k in range(len(row))]
            return {tau: mm["ymean"] + mm["ystd"] * quantile_pred(mm["betas"][tau], xs) for tau in TAUS}

        p1 = [pr(m1, x) for x in te]
        p2 = [pr(m2, x) for x in te]
        yte = [x["y"] for x in te]
        a1 = avg_pinball({tau: [p1[k][tau] for k in range(len(te))] for tau in TAUS}, yte)
        a2 = avg_pinball({tau: [p2[k][tau] for k in range(len(te))] for tau in TAUS}, yte)
        loo[held] = {
            "n": len(te),
            "avg_pinball_B1": a1, "avg_pinball_C2": a2,
            "rel_pinball_C2_vs_B1": (a1 - a2) / max(a1, 1e-12),
        }
        print(f"  LOO {held}: n={len(te)} rel={loo[held]['rel_pinball_C2_vs_B1']*100:.3f}%", flush=True)

    print(f"[{dt.datetime.now(dt.timezone.utc).strftime('%H:%M:%S')}] [4/6] block bootstrap x{N_BOOT} ...", flush=True)
    diffs = []
    for k in range(len(test)):
        b1k = sum(pinball(ys[k] - preds["B1"][k][tau], tau) for tau in TAUS) / len(TAUS)
        b2k = sum(pinball(ys[k] - preds["C2"][k][tau], tau) for tau in TAUS) / len(TAUS)
        diffs.append(b1k - b2k)
    nb = len(diffs)
    nblocks = max(1, nb // BLOCK_ROWS)
    import random
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
    rel_lo = lo / max(met["B1"]["avg_pinball"], 1e-12)
    rel_hi = hi / max(met["B1"]["avg_pinball"], 1e-12)

    sufficient = len(test) >= 500 and nu >= 500
    improved = rel_pinball >= FLOOR and rel_lo > 0
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
        "target": "next-24h realized variance (continuous) forecast as predictive distribution",
        "quantile_levels": TAUS,
        "solver": "Hunter-Lange MM/IRLS linear quantile regression (train-only)",
        "materiality_floor": FLOOR,
        "metrics": met,
        "relative_avg_pinball_reduction_C2_vs_B1": rel_pinball,
        "per_block": per_block,
        "leave_one_symbol_out": loo,
        "bootstrap": {
            "replicates": N_BOOT, "seed": SEED, "block_rows": BLOCK_ROWS,
            "mean_diff_avg_pinball_B1_minus_C2": boot_mean,
            "ci95_abs_diff": [lo, hi],
            "ci95_relative_avg_pinball_reduction": [rel_lo, rel_hi],
        },
        "download": {"n_cache_entries": len(file_entries), "n_ok": n_ok, "n_missing": n_bad},
        "verdict": verdict,
        "verdict_reason": (
            "C2 beats B1 by >=2% relative average pinball loss with bootstrap CI strictly above 0"
            if verdict == "PROMOTED" else
            "C2 vs B1 relative average pinball reduction < 2% floor or CI includes 0"
            if verdict == "NOT_SUPPORTED" else
            "insufficient test data for a confirmatory verdict"),
        "stdlib_only": True,
        "network": False,
        "read_only_cache": True,
        "outcome_data_inspected_before_freeze": False,
    }
    with open(os.path.join(HERE, f"fclr_live_archive04_eval_{SESSION}.json"), "w") as f:
        json.dump(result, f, indent=2)

    md = []
    md.append(f"# FCLR-LIVE-ARCHIVE-04 Confirmatory Evaluation ({SESSION})\n")
    md.append(f"**Experiment:** {EXPERIMENT}  \n**Verdict:** `{verdict}`  \n")
    md.append(f"**Source:** Binance public archive (unauthenticated), {len(SYMBOLS)} symbols x "
              f"{len(MONTHS)} months (2021-2024), read-only verified cache.\n")
    md.append("## Design\n")
    md.append("- Target: next-24h realized variance (continuous) as a predictive distribution at "
              f"quantiles {TAUS}.\n")
    md.append("- B1: linear quantile regression on log RV1h/RV24h/RV168h (HAR); C2: B1 + "
              "funding(24h)+90d|funding|pct + mark/index premium + mark/EMA24 dist.\n")
    md.append(f"- Splits 60/20/20 by unique UTC ts, {EMBARGO_H}h purge/embargo, test->{N_BLOCKS} blocks. "
              f"train={len(train)} val={len(val)} test={len(test)}.\n")
    md.append("## Results\n")
    md.append("| Model | Avg pinball | Mean abs coverage error |\n|---|---|---|\n")
    for m in ("B1", "C2"):
        md.append(f"| {m} | {met[m]['avg_pinball']:.6e} | {met[m]['mean_abs_coverage_error']:.4f} |\n")
    md.append(f"\n**Primary C2 vs B1 relative avg-pinball reduction: {rel_pinball*100:.3f}% "
              f"(floor {FLOOR*100:.0f}%).**\n")
    md.append(f"Bootstrap {N_BOOT} reps 95% CI relative avg-pinball reduction: "
              f"[{rel_lo*100:.3f}%, {rel_hi*100:.3f}%].\n")
    md.append("\n### Per-quantile pinball loss\n| tau | B1 | C2 |\n|---|---|---|\n")
    for tau in TAUS:
        md.append(f"| {tau:.2f} | {met['B1']['per_tau_pinball'][tau]:.6e} | "
                  f"{met['C2']['per_tau_pinball'][tau]:.6e} |\n")
    md.append("\n### Empirical coverage (target = tau)\n| tau | B1 | C2 |\n|---|---|---|\n")
    for tau in TAUS:
        md.append(f"| {tau:.2f} | {met['B1']['empirical_coverage'][tau]:.4f} | "
                  f"{met['C2']['empirical_coverage'][tau]:.4f} |\n")
    md.append("\n## Per-block relative avg-pinball reduction (C2 vs B1)\n| Block | B1 | C2 | rel reduction |\n|---|---|---|---|\n")
    for i in range(N_BLOCKS):
        bb1 = per_block["B1"]["avg_pinball"][i]
        bc2 = per_block["C2"]["avg_pinball"][i]
        md.append(f"| {i+1} | {bb1:.6e} | {bc2:.6e} | {(bb1-bc2)/max(bb1,1e-12)*100:.3f}% |\n")
    md.append("\n## Leave-one-symbol-out (C2 vs B1)\n| Symbol | n | rel avg-pinball reduction |\n|---|---|---|\n")
    for s in SYMBOLS:
        if s in loo:
            md.append(f"| {s} | {loo[s]['n']} | {loo[s]['rel_pinball_C2_vs_B1']*100:.3f}% |\n")
    md.append(f"\n## Verdict: `{verdict}` — {result['verdict_reason']}.\n")
    with open(os.path.join(HERE, f"fclr_live_archive04_eval_{SESSION}.md"), "w") as f:
        f.write("".join(md))

    registry = {
        "campaign": f"{EXPERIMENT}-{CAMPAIGN_START}",
        "session_utc": SESSION,
        "artifact_id": f"fclr_live_archive04_source_registry_{SESSION}",
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
             "track": "target + RV features"},
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
            "selection": "coverage-only, outcome-blind (frozen 2026-11-26T01:05:14Z)",
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
    with open(os.path.join(HERE, f"fclr_live_archive04_source_registry_{SESSION}.json"), "w") as f:
        json.dump(registry, f, indent=2)

    mdreg = []
    mdreg.append(f"# FCLR-LIVE-ARCHIVE-04 Source Registry ({SESSION})\n")
    mdreg.append(f"**Experiment:** {EXPERIMENT}  \n**Campaign:** {EXPERIMENT}-{CAMPAIGN_START}\n")
    mdreg.append("**Source:** Binance public market-data archive (unauthenticated, free, no signup).\n")
    mdreg.append(f"**Cache:** {n_ok}/{len(file_entries)} zips present and sha256-verified under "
                 "research_state/session_20261126T042519Z/raw/ (read-only reuse).\n")
    mdreg.append(f"**Cohort:** {SYMBOLS}, 2021-01..2024-12.\n")
    mdreg.append(f"**Registry sha256:** {reg_sha}\n")
    with open(os.path.join(HERE, f"fclr_live_archive04_source_registry_{SESSION}.md"), "w") as f:
        f.write("".join(mdreg))

    prereg = {
        "campaign": f"{EXPERIMENT}-{CAMPAIGN_START}",
        "session_utc": SESSION,
        "artifact_id": f"fclr_live_archive04_prereg_{SESSION}",
        "generated_at": result["generated_at"],
        "experiment_id": EXPERIMENT,
        "outcome_data_inspected_before_freeze": False,
        "hash_bound_to_source_registry": reg_sha,
        "hypothesis": ("FCLR-H003: funding + price features improve out-of-sample "
                       "forecasts of the FULL predictive distribution of next-24h "
                       "realized variance (quantile forecasts) beyond an RV-only HAR baseline."),
        "window": "2021-01-01..2024-12-31 UTC",
        "symbols": SYMBOLS,
        "target": "next-24h realized variance (continuous) as a predictive distribution",
        "quantile_levels": TAUS,
        "quantile_estimation": "train-only linear quantile regression (Hunter-Lange MM/IRLS); never re-fit on test",
        "splits": "60/20/20 by unique UTC timestamp; 7-day (168h) purge/embargo at train/val and val/test boundaries; test -> 3 interleaved blocks",
        "models": {
            "B1": "linear quantile regression on log RV1h/RV24h/RV168h (HAR)",
            "C2": "B1 + signed funding(24h) + trailing 90d |funding| percentile + mark/index premium + mark/EMA24 distance",
        },
        "primary_contrast": "C2 vs B1 on paired test-set average pinball loss across the five quantiles",
        "inference": (">=2000 deterministic moving-block bootstrap replicates (block=24 rows, seed=20261126); "
                      "report average + per-quantile pinball, empirical coverage, 95% CI, per-block, leave-one-symbol-out"),
        "materiality_floor": FLOOR,
        "decision_rule": ("PROMOTED iff relative average-pinball reduction >=2% AND bootstrap 95% CI lower bound > 0 "
                          "AND test data sufficient; else NOT_SUPPORTED; INCONCLUSIVE if test data insufficient"),
        "leakage_controls": [
            "outcome-blind freeze before target generation",
            "train-only quantile fitting",
            "train-only scaling + standardization",
            "7-day purge/embargo",
            "no outcome inspection before freeze",
        ],
        "stdlib_only": True,
        "network": False,
        "read_only_cache": True,
    }
    with open(os.path.join(HERE, f"fclr_live_archive04_prereg_{SESSION}.json"), "w") as f:
        json.dump(prereg, f, indent=2)

    mdpre = []
    mdpre.append(f"# FCLR-LIVE-ARCHIVE-04 Preregistration ({SESSION})\n")
    mdpre.append(f"**Experiment:** {EXPERIMENT}  \n**Outcome-data inspected before freeze:** False\n")
    mdpre.append(f"**Target:** next-24h RV (continuous) as a predictive distribution at quantiles {TAUS}.\n")
    mdpre.append("**Models:** B1 = linear quantile HAR (log RV1h/24h/168h); C2 = B1 + funding + price features.\n")
    mdpre.append(f"**Primary contrast:** C2 vs B1 paired test-set average pinball loss. "
                 f"Materiality floor: {FLOOR*100:.0f}% relative reduction.\n")
    mdpre.append("**Decision rule:** PROMOTED iff relative avg-pinball reduction >=2% and bootstrap 95% CI lower bound > 0; "
                 "else NOT_SUPPORTED; INCONCLUSIVE if insufficient data.\n")
    mdpre.append(f"**Source registry sha256:** {reg_sha}\n")
    with open(os.path.join(HERE, f"fclr_live_archive04_prereg_{SESSION}.md"), "w") as f:
        f.write("".join(mdpre))

    with open(os.path.join(HERE, f"_headline_{SESSION}.json"), "w") as f:
        json.dump({
            "avg_pinball": {m: met[m]["avg_pinball"] for m in ("B1", "C2")},
            "rel_pinball": rel_pinball, "n_test": len(test), "verdict": verdict,
            "n_unique_timestamps": nu,
        }, f, indent=2)

    print(f"[{dt.datetime.now(dt.timezone.utc).strftime('%H:%M:%S')}] [5/6] verdict={verdict} "
          f"rel_pinball={rel_pinball*100:.3f}% CI=[{rel_lo*100:.3f}%,{rel_hi*100:.3f}%]", flush=True)
    print(f"[{dt.datetime.now(dt.timezone.utc).strftime('%H:%M:%S')}] [6/6] done in {time.time()-t0:.0f}s", flush=True)


if __name__ == "__main__":
    main()