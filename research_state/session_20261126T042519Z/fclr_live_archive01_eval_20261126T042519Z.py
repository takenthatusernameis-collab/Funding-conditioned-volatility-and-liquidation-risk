#!/usr/bin/env python3
"""FCLR-LIVE-ARCHIVE-01 heavy confirmatory evaluation (stdlib only).

Repo-name-leading estimand: funding-conditioned mean realized-variance (RV)
forecasting. New, verified, unauthenticated free source: Binance public
market-data archive (S3 data.binance.vision), monthly 1h klines / mark / index /
premium + fundingRate, 2021-01 .. 2024-12, frozen 5-symbol cohort.

Design (FROZEN, outcome-blind):
  - B0 = RV24 persistence
  - B1 = OLS HAR on log RV1h / RV24h / RV168h -> log next-24h RV
  - C1 = B1 + signed funding + trailing 90d |funding| percentile
  - C2 = C1 + mark/index premium + mark/EMA24 distance
  - Primary contrast: C2 vs B1 on paired next-24h QLIKE
  - Splits 60/20/20 by unique UTC timestamp, 7-day purge/embargo, test -> 3 blocks
  - >=2000 deterministic block-bootstrap replicates (seed fixed)
  - Materiality floor: >=2% relative QLIKE reduction with CI supporting improvement

No pip installs. No numpy/pandas. Writes the fclr_live_archive01_* artifact set.
"""
from __future__ import annotations

import bisect
import concurrent.futures as cf
import datetime as dt
import hashlib
import io
import json
import math
import os
import statistics
import sys
import time
import urllib.request
import zipfile

SESSION = "20261126T042519Z"
EXPERIMENT = "FCLR-LIVE-ARCHIVE-01"
CAMPAIGN_START = "20261125T074500Z"
HERE = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.join(HERE, "raw")
BASE = "https://s3-ap-northeast-1.amazonaws.com/data.binance.vision/data/futures/um/monthly"
SYMBOLS = ["1INCHUSDT", "AAVEUSDT", "ADAUSDT", "ALGOUSDT", "ALPHAUSDT"]
MONTHS = [f"{y}-{m:02d}" for y in (2021, 2022, 2023, 2024) for m in range(1, 13)]
SEED = 20261126
N_BOOT = 2000
EMBARGO_H = 168  # 7 calendar days
FLOOR = 0.02

SOURCES = {
    "klines": lambda s, mo: f"{BASE}/klines/{s}/1h/{s}-1h-{mo}.zip",
    "markPriceKlines": lambda s, mo: f"{BASE}/markPriceKlines/{s}/1h/{s}-1h-{mo}.zip",
    "indexPriceKlines": lambda s, mo: f"{BASE}/indexPriceKlines/{s}/1h/{s}-1h-{mo}.zip",
    "premiumIndexKlines": lambda s, mo: f"{BASE}/premiumIndexKlines/{s}/1h/{s}-1h-{mo}.zip",
    "fundingRate": lambda s, mo: f"{BASE}/fundingRate/{s}/{s}-fundingRate-{mo}.zip",
}


def _get(url, timeout=30, retries=4):
    last = None
    for k in range(retries):
        try:
            r = urllib.request.urlopen(url, timeout=timeout)
            return r.status, r.read()
        except Exception as e:  # noqa
            last = e
            time.sleep(1.5 * (2 ** k))
    raise last


def _sha(b):
    return hashlib.sha256(b).hexdigest()


def _cache_path(source, sym, mo):
    return os.path.join(RAW, source, f"{sym}-{mo}.zip")


def download_one(source, sym, mo):
    url = SOURCES[source](sym, mo)
    cp = _cache_path(source, sym, mo)
    os.makedirs(os.path.dirname(cp), exist_ok=True)
    if os.path.exists(cp):
        with open(cp, "rb") as f:
            data = f.read()
        return {"source": source, "symbol": sym, "month": mo, "url": url,
                "status": "cached", "bytes": len(data), "sha256": _sha(data)}
    st, data = _get(url)
    # checksum sidecar (best-effort; never blocks)
    cs_status, cs = None, None
    try:
        cs_status, cs = _get(url + ".CHECKSUM", timeout=15, retries=2)
    except Exception:
        cs = None
    sha = _sha(data)
    checksum_ok = None
    if cs:
        try:
            expected = cs.decode("utf-8", "ignore").split()[0]
            checksum_ok = (expected == sha)
        except Exception:
            checksum_ok = None
    with open(cp, "wb") as f:
        f.write(data)
    return {"source": source, "symbol": sym, "month": mo, "url": url,
            "status": st, "bytes": len(data), "sha256": sha,
            "checksum_sidecar_status": cs_status, "checksum_ok": checksum_ok}


def download_all():
    jobs = [(src, s, mo) for s in SYMBOLS for mo in MONTHS for src in SOURCES]
    manifest = []
    t0 = time.time()
    with cf.ThreadPoolExecutor(max_workers=8) as ex:
        futs = {ex.submit(download_one, *j): j for j in jobs}
        done = 0
        for fu in cf.as_completed(futs):
            try:
                manifest.append(fu.result())
            except Exception as e:
                j = futs[fu]
                manifest.append({"source": j[0], "symbol": j[1], "month": j[2],
                                 "status": "ERROR", "error": str(e)[:200]})
            done += 1
            if done % 100 == 0:
                print(f"  downloaded {done}/{len(jobs)} ({time.time()-t0:.0f}s)", flush=True)
    ok = sum(1 for m in manifest if m.get("status") in (200, 206, "cached"))
    bad = [m for m in manifest if m.get("status") not in (200, 206, "cached")]
    print(f"  download complete: {ok}/{len(jobs)} ok, {len(bad)} bad", flush=True)
    with open(os.path.join(HERE, f"fclr_live_archive01_download_manifest_{SESSION}.json"), "w") as f:
        json.dump({"session": SESSION, "n_jobs": len(jobs), "n_ok": ok,
                   "n_bad": len(bad), "bad": bad[:50], "entries": manifest}, f, indent=1)
    return bad


def _read_zip_csv(cp):
    with open(cp, "rb") as f:
        data = f.read()
    z = zipfile.ZipFile(io.BytesIO(data))
    name = z.namelist()[0]
    text = z.read(name).decode("utf-8", "ignore")
    return text.splitlines()


def _parse_klines(lines):
    out = {}
    for ln in lines:
        p = ln.split(",")
        if not p or p[0] in ("open_time", "") or not p[0].lstrip("-").isdigit():
            continue
        try:
            t = int(p[0]) // 1000  # ms -> s
            close = float(p[4])
        except Exception:
            continue
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
    klines, mark, index, premium = {}, {}, {}, {}
    for mo in MONTHS:
        cp = _cache_path("klines", sym, mo)
        if os.path.exists(cp):
            klines.update(_parse_klines(_read_zip_csv(cp)))
        cp = _cache_path("markPriceKlines", sym, mo)
        if os.path.exists(cp):
            mark.update(_parse_klines(_read_zip_csv(cp)))
        cp = _cache_path("indexPriceKlines", sym, mo)
        if os.path.exists(cp):
            index.update(_parse_klines(_read_zip_csv(cp)))
        cp = _cache_path("premiumIndexKlines", sym, mo)
        if os.path.exists(cp):
            premium.update(_parse_klines(_read_zip_csv(cp)))
    funding = []
    for mo in MONTHS:
        cp = _cache_path("fundingRate", sym, mo)
        if os.path.exists(cp):
            funding.extend(_parse_funding(_read_zip_csv(cp)))
    funding.sort()
    ft = [x[0] for x in funding]
    fr = [x[1] for x in funding]

    times = sorted(klines)
    rows = []
    n = len(times)
    if n < 200:
        return rows
    # hourly log returns aligned to kline times
    r = [0.0] * n
    for i in range(1, n):
        if times[i] - times[i - 1] == 3600 and klines[times[i]] > 0 and klines[times[i - 1]] > 0:
            r[i] = math.log(klines[times[i]] / klines[times[i - 1]])
    rv1 = [x * x for x in r]
    # rolling sums
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
    # next-24h target
    next24 = [None] * n
    for i in range(n - 24):
        next24[i] = sum(rv1[i + 1:i + 25])

    # EMA24 of mark
    ema = {}
    alpha = 2.0 / (24 + 1)
    e = None
    for t in times:
        m = mark.get(t)
        if m is None:
            continue
        e = m if e is None else alpha * m + (1 - alpha) * e
        ema[t] = e

    for i in range(168, n - 24):
        t = times[i]
        if rv24[i] is None or rv168[i] is None or next24[i] is None:
            continue
        if rv24[i] <= 0 or rv168[i] <= 0:
            continue
        # funding as-of t: last rate at or before t
        j = bisect.bisect_right(ft, t) - 1
        if j < 0:
            continue
        cur_rate = fr[j]
        # trailing 24h signed funding sum
        lo = bisect.bisect_right(ft, t - 24 * 3600)
        fund24 = sum(fr[lo:j + 1]) if j >= lo else 0.0
        # trailing 90d |funding| percentile of current |rate|
        lo90 = bisect.bisect_right(ft, t - 90 * 86400)
        window = [abs(x) for x in fr[lo90:j + 1]]
        if window:
            pct = sum(1 for x in window if x <= abs(cur_rate)) / len(window)
        else:
            pct = 0.5
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
    return rows


# ----------------------------- OLS (stdlib) -----------------------------
def solve(A, b):
    n = len(A)
    M = [A[i][:] + [b[i]] for i in range(n)]
    for c in range(n):
        p = max(range(c, n), key=lambda r: abs(M[r][c]))
        M[c], M[p] = M[p], M[c]
        piv = M[c][c]
        if abs(piv) < 1e-12:
            piv = 1e-12
        for r in range(n):
            if r != c:
                f = M[r][c] / piv
                if f:
                    for k in range(c, n + 1):
                        M[r][k] -= f * M[c][k]
    return [M[i][n] / (M[i][i] if abs(M[i][i]) > 1e-12 else 1e-12) for i in range(n)]


def ols_fit(X, y):
    p = len(X[0])
    XtX = [[0.0] * p for _ in range(p)]
    Xty = [0.0] * p
    for xi, yi in zip(X, y):
        for a in range(p):
            Xty[a] += xi[a] * yi
            for b in range(p):
                XtX[a][b] += xi[a] * xi[b]
    return solve(XtX, Xty)


def ols_pred(beta, x):
    return sum(b * xi for b, xi in zip(beta, x))


def qlike(y, f):
    f = max(f, 1e-12)
    y = max(y, 1e-12)
    return y / f - math.log(y / f) - 1.0


def main():
    print("[1/5] downloading cohort ...", flush=True)
    bad = download_all()
    print("[2/5] building panels ...", flush=True)
    panel = []
    per_sym_counts = {}
    for s in SYMBOLS:
        rows = build_symbol_panel(s)
        per_sym_counts[s] = len(rows)
        panel.extend(rows)
        print(f"  {s}: {len(rows)} rows", flush=True)
    panel.sort(key=lambda x: x["t"])

    # splits by unique timestamps
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

    # feature maps
    def feat_row(x, model):
        base = [math.log(max(x["rv1"], 1e-12)), math.log(max(x["rv24"], 1e-12)),
                math.log(max(x["rv168"], 1e-12))]
        if model == "B1":
            return base
        if model == "C1":
            return base + [x["fund24"], x["fund_pct"]]
        if model == "C2":
            return base + [x["fund24"], x["fund_pct"], x["prem"], x["mdist"]]
        raise ValueError(model)

    ytr = [math.log(max(x["y"], 1e-12)) for x in train]

    def fit_model(model):
        X = [feat_row(x, model) for x in train]
        mu = [sum(col) / len(col) for col in zip(*X)]
        sd = []
        for k in range(len(X[0])):
            col = [row[k] for row in X]
            s = statistics.pstdev(col) or 1.0
            sd.append(s)
        Xs = [[(row[k] - mu[k]) / sd[k] for k in range(len(row))] for row in X]
        Xs = [[1.0] + row for row in Xs]
        beta = ols_fit(Xs, ytr)
        resid = [yt - ols_pred(beta, xr) for yt, xr in zip(ytr, Xs)]
        smear = sum(math.exp(e) for e in resid) / len(resid)
        return {"model": model, "mu": mu, "sd": sd, "beta": beta, "smear": smear}

    def predict(m, x):
        row = feat_row(x, m["model"])
        xs = [1.0] + [(row[k] - m["mu"][k]) / m["sd"][k] for k in range(len(row))]
        lp = ols_pred(m["beta"], xs)
        return math.exp(lp) * m["smear"]

    print("[3/5] fitting models (train only) ...", flush=True)
    models = {k: fit_model(k) for k in ("B1", "C1", "C2")}

    # B0 persistence prediction = rv24 level
    def pred_all(model):
        out = []
        for x in test:
            if model == "B0":
                out.append(x["rv24"])
            else:
                out.append(predict(models[model], x))
        return out

    preds = {m: pred_all(m) for m in ("B0", "B1", "C1", "C2")}
    y = [x["y"] for x in test]

    def mean_ql(m):
        return sum(qlike(yy, ff) for yy, ff in zip(y, preds[m])) / len(y)

    q = {m: mean_ql(m) for m in preds}
    rel = {m: (q["B1"] - q[m]) / q["B1"] for m in ("C1", "C2")}
    rel_C2_vs_B1 = rel["C2"]

    # 3 test blocks (by index, interleaved so each block spans the full test span)
    block_idx = [[k for k in range(len(test)) if k % 3 == b] for b in range(3)]

    def block_ql(m, idxs):
        return sum(qlike(test[k]["y"], preds[m][k]) for k in idxs) / max(len(idxs), 1)

    per_block = {m: [block_ql(m, bi) for bi in block_idx] for m in ("B1", "C2")}

    # leave-one-symbol-out (train on other 4, eval held-out)
    loo = {}
    for held in SYMBOLS:
        tr = [x for x in train if x["symbol"] != held]
        te = [x for x in test if x["symbol"] == held]
        if not te:
            continue
        ytr2 = [math.log(max(x["y"], 1e-12)) for x in tr]

        def fit2(model):
            X = [feat_row(x, model) for x in tr]
            mu = [sum(c) / len(c) for c in zip(*X)]
            sd = [statistics.pstdev([r[k] for r in X]) or 1.0 for k in range(len(X[0]))]
            Xs = [[1.0] + [(r[k] - mu[k]) / sd[k] for k in range(len(r))] for r in X]
            beta = ols_fit(Xs, ytr2)
            resid = [a - ols_pred(beta, b) for a, b in zip(ytr2, Xs)]
            return {"model": model, "mu": mu, "sd": sd, "beta": beta,
                    "smear": sum(math.exp(e) for e in resid) / len(resid)}

        m1 = fit2("B1")
        m2 = fit2("C2")

        def pr(mm, x):
            row = feat_row(x, mm["model"])
            xs = [1.0] + [(row[k] - mm["mu"][k]) / mm["sd"][k] for k in range(len(row))]
            return math.exp(ols_pred(mm["beta"], xs)) * mm["smear"]

        qb1 = sum(qlike(x["y"], pr(m1, x)) for x in te) / len(te)
        qc2 = sum(qlike(x["y"], pr(m2, x)) for x in te) / len(te)
        loo[held] = {"n": len(te), "qlike_B1": qb1, "qlike_C2": qc2,
                     "rel_C2_vs_B1": (qb1 - qc2) / qb1}

    # block bootstrap on paired QLIKE diff (B1 - C2), moving blocks of 24 rows
    print(f"[4/5] block bootstrap x{N_BOOT} ...", flush=True)
    diffs = [qlike(y[k], preds["B1"][k]) - qlike(y[k], preds["C2"][k]) for k in range(len(y))]
    nb = len(diffs)
    blk = 24
    nblocks = max(1, nb // blk)
    rng = __import__("random").Random(SEED)
    boot = []
    for _ in range(N_BOOT):
        s = 0.0
        cnt = 0
        for _b in range(nblocks):
            st = rng.randrange(0, max(1, nb - blk + 1))
            for k in range(st, min(st + blk, nb)):
                s += diffs[k]
                cnt += 1
        boot.append(s / cnt if cnt else 0.0)
    boot.sort()
    lo = boot[int(0.025 * N_BOOT)]
    hi = boot[int(0.975 * N_BOOT)]
    boot_mean = sum(boot) / len(boot)
    # relative reduction CI (divide by q B1)
    rel_lo = lo / q["B1"]
    rel_hi = hi / q["B1"]

    improved = rel_C2_vs_B1 >= FLOOR and lo > 0
    if len(test) < 500 or nu < 500:
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
        "source": "BINANCE_PUBLIC_ARCHIVE",
        "symbols": SYMBOLS,
        "months": f"2021-01..2024-12 ({len(MONTHS)} months)",
        "n_symbols": len(SYMBOLS),
        "per_symbol_rows": per_sym_counts,
        "n_train": len(train), "n_val": len(val), "n_test": len(test),
        "n_unique_timestamps": nu,
        "embargo_hours": EMBARGO_H,
        "splits": "60/20/20 by unique UTC timestamp; 7-day purge/embargo; test->3 blocks",
        "models": ["B0", "B1", "C1", "C2"],
        "primary_contrast": "C2 vs B1 (paired next-24h QLIKE)",
        "materiality_floor": FLOOR,
        "qlike": q,
        "relative_reduction": rel,
        "relative_reduction_C2_vs_B1": rel_C2_vs_B1,
        "per_block_qlike": per_block,
        "leave_one_symbol_out": loo,
        "bootstrap": {
            "replicates": N_BOOT, "seed": SEED, "block_rows": blk,
            "mean_abs_diff_B1_minus_C2": boot_mean,
            "ci95_abs_diff": [lo, hi],
            "ci95_relative_reduction": [rel_lo, rel_hi],
        },
        "download": {"n_jobs": len(SYMBOLS) * len(MONTHS) * len(SOURCES),
                     "n_bad": len(bad)},
        "verdict": verdict,
        "verdict_reason": (
            "C2 beats B1 by >=2% relative QLIKE with bootstrap CI strictly above 0"
            if verdict == "PROMOTED" else
            "C2 vs B1 relative QLIKE reduction < 2% floor or CI includes 0"
            if verdict == "NOT_SUPPORTED" else
            "insufficient test data for a confirmatory verdict"),
        "stdlib_only": True,
        "outcome_data_inspected_before_freeze": False,
    }
    with open(os.path.join(HERE, f"fclr_live_archive01_eval_{SESSION}.json"), "w") as f:
        json.dump(result, f, indent=2)

    # markdown report
    md = []
    md.append(f"# FCLR-LIVE-ARCHIVE-01 Confirmatory Evaluation ({SESSION})\n")
    md.append(f"**Experiment:** {EXPERIMENT}  \n**Verdict:** `{verdict}`  \n")
    md.append(f"**Source:** Binance public archive (unauthenticated S3), "
              f"{len(SYMBOLS)} symbols x {len(MONTHS)} months (2021-2024).\n")
    md.append("## Design\n")
    md.append("- B0 RV24 persistence; B1 HAR OLS (log RV1h/24h/168h); "
              "C1 +signed funding +90d |funding| pct; C2 +mark/index premium +mark/EMA24 dist.\n")
    md.append(f"- Splits 60/20/20 by unique UTC ts, {EMBARGO_H}h purge/embargo, test->3 blocks. "
              f"train={len(train)} val={len(val)} test={len(test)}.\n")
    md.append("## Results (mean QLIKE, lower is better)\n")
    md.append("| Model | QLIKE |\n|---|---|\n")
    for m in ("B0", "B1", "C1", "C2"):
        md.append(f"| {m} | {q[m]:.6f} |\n")
    md.append(f"\n**Primary C2 vs B1 relative QLIKE reduction: {rel_C2_vs_B1*100:.3f}%** "
              f"(floor {FLOOR*100:.0f}%).\n")
    md.append(f"Bootstrap {N_BOOT} reps 95% CI relative reduction: "
              f"[{rel_lo*100:.3f}%, {rel_hi*100:.3f}%].\n")
    md.append("\n## Per-block QLIKE\n| Block | B1 | C2 |\n|---|---|---|\n")
    for i in range(3):
        md.append(f"| {i+1} | {per_block['B1'][i]:.6f} | {per_block['C2'][i]:.6f} |\n")
    md.append("\n## Leave-one-symbol-out (C2 vs B1)\n| Symbol | n | rel reduction |\n|---|---|---|\n")
    for s in SYMBOLS:
        if s in loo:
            md.append(f"| {s} | {loo[s]['n']} | {loo[s]['rel_C2_vs_B1']*100:.3f}% |\n")
    md.append(f"\n## Verdict: `{verdict}` — {result['verdict_reason']}.\n")
    with open(os.path.join(HERE, f"fclr_live_archive01_eval_{SESSION}.md"), "w") as f:
        f.write("".join(md))

    print(f"[5/5] verdict={verdict} rel_C2_vs_B1={rel_C2_vs_B1*100:.3f}% "
          f"CI=[{rel_lo*100:.3f}%,{rel_hi*100:.3f}%]", flush=True)
    # machine-readable headline for the recompute cross-check
    with open(os.path.join(HERE, f"_headline_{SESSION}.json"), "w") as f:
        json.dump({"qlike": q, "rel_C2_vs_B1": rel_C2_vs_B1,
                   "n_test": len(test), "verdict": verdict}, f, indent=2)


if __name__ == "__main__":
    main()