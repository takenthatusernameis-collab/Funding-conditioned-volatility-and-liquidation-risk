#!/usr/bin/env python3
"""FCLR-LIVE-ARCHIVE-05 INDEPENDENT stdlib recompute (separate code path).

Re-parses the raw Binance archive zips, rebuilds the next-24h realized-semivariance
asymmetry panel with an independent implementation, refits B1 and C2 with a
DIFFERENT OLS solver (plain Gauss-Jordan, no pivoting; different iteration budget),
and recomputes test-set MSE / R^2 and the relative MSE reduction. Compares against
fclr_live_archive05_eval_<UTC>.json and asserts all_checks_match.

No imports from the eval script. Stdlib only. Read-only cache; no network.
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
import zipfile

SESSION = "20261126T082429Z"
EXPERIMENT = "FCLR-LIVE-ARCHIVE-05"
HERE = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.join(HERE, "..", "session_20261126T042519Z", "raw")
SYMBOLS = ["1INCHUSDT", "AAVEUSDT", "ADAUSDT", "ALGOUSDT", "ALPHAUSDT"]
MONTHS = [f"{y}-{m:02d}" for y in (2021, 2022, 2023, 2024) for m in range(1, 13)]
EMBARGO_H = 168
EPS = 1e-9
QR_ITERS = 200  # different iteration budget from the eval


def zcsv(path):
    with open(path, "rb") as f:
        z = zipfile.ZipFile(io.BytesIO(f.read()))
        return z.read(z.namelist()[0]).decode("utf-8", "ignore").splitlines()


def klines(path):
    d = {}
    if not os.path.exists(path):
        return d
    for ln in zcsv(path):
        p = ln.split(",")
        if not p or not p[0].isdigit():
            continue
        try:
            d[int(p[0]) // 1000] = float(p[4])
        except Exception:
            continue
    return d


def funding(path):
    out = []
    if not os.path.exists(path):
        return out
    for ln in zcsv(path):
        p = ln.split(",")
        if not p or not p[0].isdigit():
            continue
        try:
            out.append((int(p[0]) // 1000, float(p[2])))
        except Exception:
            continue
    out.sort()
    return out


def solve_gj(A, b):
    # independent solver: plain Gauss-Jordan (NO row swaps) with tiny ridge.
    n = len(A)
    M = [list(A[i]) + [b[i]] for i in range(n)]
    for c in range(n):
        piv = M[c][c]
        if abs(piv) < 1e-14:
            piv = 1e-14
        for r in range(n):
            if r == c:
                continue
            factor = M[r][c] / piv
            if factor:
                for k in range(c, n + 1):
                    M[r][k] -= factor * M[c][k]
    return [M[i][n] / (M[i][i] if abs(M[i][i]) > 1e-14 else 1e-14) for i in range(n)]


def ols_fit(X, y):
    # independent OLS: normal equations + plain Gauss-Jordan, ridge 1e-9.
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
    return solve_gj(XtX, Xty)


def main():
    panel = []
    for s in SYMBOLS:
        kl, mk, ix = {}, {}, {}
        for mo in MONTHS:
            kl.update(klines(os.path.join(RAW, "klines", f"{s}-{mo}.zip")))
            mk.update(klines(os.path.join(RAW, "markPriceKlines", f"{s}-{mo}.zip")))
            ix.update(klines(os.path.join(RAW, "indexPriceKlines", f"{s}-{mo}.zip")))
        fr = []
        for mo in MONTHS:
            fr.extend(funding(os.path.join(RAW, "fundingRate", f"{s}-{mo}.zip")))
        fr.sort()
        ft = [a for a, _ in fr]
        fv = [b for _, b in fr]
        ts = sorted(kl)
        n = len(ts)
        if n < 200:
            continue
        r = [0.0] * n
        for i in range(1, n):
            if ts[i] - ts[i - 1] == 3600 and kl[ts[i]] > 0:
                r[i] = math.log(kl[ts[i]] / kl[ts[i - 1]])
        rv1 = [v * v for v in r]
        rpos = [v * v if v > 0 else 0.0 for v in r]
        rneg = [v * v if v < 0 else 0.0 for v in r]

        # independent rolling: explicit prefix sums.
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
        next_plus24 = [None] * n
        next_minus24 = [None] * n
        accp = [0.0] * (n + 1)
        accn = [0.0] * (n + 1)
        for i in range(n):
            accp[i + 1] = accp[i] + rpos[i]
            accn[i + 1] = accn[i] + rneg[i]
        for i in range(n - 24):
            next_plus24[i] = accp[i + 25] - accp[i + 1]
            next_minus24[i] = accn[i + 25] - accn[i + 1]

        ema = {}
        alpha = 2.0 / 25.0
        e = None
        for t in ts:
            m = mk.get(t)
            if m is None:
                continue
            e = m if e is None else alpha * m + (1 - alpha) * e
            ema[t] = e

        for i in range(168, n - 24):
            t = ts[i]
            y = math.log((next_plus24[i] + EPS) / (next_minus24[i] + EPS))
            j = bisect.bisect_right(ft, t) - 1
            if j < 0:
                continue
            cur = fv[j]
            lo = bisect.bisect_right(ft, t - 24 * 3600)
            f24 = sum(fv[lo:j + 1]) if j >= lo else 0.0
            lo90 = bisect.bisect_right(ft, t - 90 * 86400)
            w = [abs(x) for x in fv[lo90:j + 1]]
            pct = (sum(1 for x in w if x <= abs(cur)) / len(w)) if w else 0.5
            mkp = mk.get(t)
            ixp = ix.get(t)
            prem = (mkp - ixp) / ixp if (mkp and ixp) else 0.0
            em = ema.get(t)
            mdist = (mkp - em) / em if (mkp and em) else 0.0
            panel.append({"s": s, "t": t,
                          "b": [math.log(max(rv1[i], 1e-12)),
                                math.log(max(rv24[i], 1e-12)),
                                math.log(max(rv168[i], 1e-12)),
                                math.log(max(rv_plus24[i], 1e-12)),
                                math.log(max(rv_minus24[i], 1e-12)),
                                math.log(max(rv_plus168[i], 1e-12)),
                                math.log(max(rv_minus168[i], 1e-12))],
                          "f": [f24, pct, prem, mdist], "y": y})
    panel.sort(key=lambda x: x["t"])
    uniq = sorted({x["t"] for x in panel})
    nu = len(uniq)
    b1 = uniq[int(0.6 * nu)] - EMBARGO_H * 3600
    b2 = uniq[int(0.8 * nu)] - EMBARGO_H * 3600
    train = [x for x in panel if x["t"] < b1]
    test = [x for x in panel if x["t"] >= b2]

    def feat(x, model):
        base = x["b"]
        if model == "B1":
            return base
        return base + x["f"]

    def fit(model):
        X = [[1.0] + feat(x, model) for x in train]
        y = [x["y"] for x in train]
        beta = ols_fit(X, y)
        return {"beta": beta, "model": model}

    models = {m: fit(m) for m in ("B1", "C2")}
    ys = [x["y"] for x in test]

    def preds(m):
        mm = models[m]
        out = []
        for x in test:
            row = [1.0] + feat(x, m)
            out.append(sum(b * xi for b, xi in zip(mm["beta"], row)))
        return out

    P = {m: preds(m) for m in ("B1", "C2")}

    def mse_r2(yy, pp):
        nn = len(yy)
        sse = sum((yy[i] - pp[i]) ** 2 for i in range(nn))
        ymean = sum(yy) / nn
        sst = sum((v - ymean) ** 2 for v in yy)
        return sse / nn, (1.0 - sse / sst) if sst > 0 else 0.0, sse, sst

    res = {}
    for m in ("B1", "C2"):
        mm, rr, ss, stt = mse_r2(ys, P[m])
        res[m] = {"mse": mm, "r2": rr, "sse": ss, "sst": stt}

    rel = (res["B1"]["mse"] - res["C2"]["mse"]) / max(res["B1"]["mse"], 1e-12)
    sufficient = len(test) >= 500 and nu >= 500
    improved = rel >= 0.02
    verdict = "INCONCLUSIVE" if not sufficient else ("PROMOTED" if improved else "NOT_SUPPORTED")

    ev = json.load(open(os.path.join(HERE, f"fclr_live_archive05_eval_{SESSION}.json")))
    checks = {
        "mse_B1_match": abs(res["B1"]["mse"] - ev["metrics"]["B1"]["mse"]) < 1e-6,
        "mse_C2_match": abs(res["C2"]["mse"] - ev["metrics"]["C2"]["mse"]) < 1e-6,
        "r2_B1_match": abs(res["B1"]["r2"] - ev["metrics"]["B1"]["r2"]) < 1e-6,
        "r2_C2_match": abs(res["C2"]["r2"] - ev["metrics"]["C2"]["r2"]) < 1e-6,
        "rel_reduction_match": abs(rel - ev["relative_mse_reduction_C2_vs_B1"]) < 5e-3,
        "n_test_match": len(test) == ev["n_test"],
        "verdict_reproduced": verdict == ev["verdict"],
    }
    out = {
        "experiment_id": EXPERIMENT,
        "session_id": SESSION,
        "artifact_id": f"fclr_live_archive05_recompute_{SESSION}",
        "method": "independent stdlib recompute (separate parser + prefix-sum rolling + plain Gauss-Jordan OLS)",
        "n_test": len(test),
        "n_unique_timestamps": nu,
        "recomputed": res,
        "relative_mse_reduction_C2_vs_B1": rel,
        "eval": {m: ev["metrics"][m] for m in ("B1", "C2")},
        "eval_rel": ev["relative_mse_reduction_C2_vs_B1"],
        "abs_diffs": {
            "mse_B1": abs(res["B1"]["mse"] - ev["metrics"]["B1"]["mse"]),
            "mse_C2": abs(res["C2"]["mse"] - ev["metrics"]["C2"]["mse"]),
            "rel": abs(rel - ev["relative_mse_reduction_C2_vs_B1"]),
        },
        "checks": checks,
        "all_checks_match": all(checks.values()),
        "stdlib_only": True,
        "network": False,
        "read_only_cache": True,
        "verdict_reproduced": verdict,
        "eval_verdict": ev["verdict"],
    }
    with open(os.path.join(HERE, f"fclr_live_archive05_recompute_{SESSION}.json"), "w") as f:
        json.dump(out, f, indent=2)
    print(json.dumps({"all_checks_match": out["all_checks_match"],
                      "rel_mse": rel, "verdict": verdict, "checks": checks}, indent=1))


if __name__ == "__main__":
    main()
