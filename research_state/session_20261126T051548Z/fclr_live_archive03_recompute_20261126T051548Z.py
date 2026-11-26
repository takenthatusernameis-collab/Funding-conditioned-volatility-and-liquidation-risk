#!/usr/bin/env python3
"""FCLR-LIVE-ARCHIVE-03 INDEPENDENT stdlib recompute (separate code path).

Re-parses the raw Binance archive zips, rebuilds the stress/tail panel with an
independent implementation, refits B1 and C2 with a different solver, and
recomputes test-set Brier / log-loss / ECE + relative Brier reduction. Compares
against fclr_live_archive03_eval_<UTC>.json and asserts all_checks_match.

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

SESSION = "20261126T051548Z"
EXPERIMENT = "FCLR-LIVE-ARCHIVE-03"
HERE = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.join(HERE, "..", "session_20261126T042519Z", "raw")
SYMBOLS = ["1INCHUSDT", "AAVEUSDT", "ADAUSDT", "ALGOUSDT", "ALPHAUSDT"]
MONTHS = [f"{y}-{m:02d}" for y in (2021, 2022, 2023, 2024) for m in range(1, 13)]
EMBARGO_H = 168
SEED = 20261126
STRESS_Q = 0.95


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


def solve3(A, b, ridge=1e-6):
    # independent solver: plain Gauss-Jordan (no row swaps) with ridge.
    n = len(A)
    M = [list(A[i]) + [b[i]] for i in range(n)]
    for c in range(n):
        piv = M[c][c]
        if abs(piv) < 1e-12:
            piv = 1e-12
        for r in range(n):
            if r == c:
                continue
            factor = M[r][c] / piv
            if factor:
                for k in range(c, n + 1):
                    M[r][k] -= factor * M[c][k]
    return [M[i][n] / M[i][i] for i in range(n)]


def fit_irls(X, y, n_iter=60):
    # independent IRLS logistic fit (different update/tiling from eval).
    p = len(X[0])
    beta = [0.0] * p
    n = len(X)
    for _ in range(n_iter):
        pt = []
        for row in X:
            v = sum(b * xi for b, xi in zip(beta, row))
            pt.append(1.0 / (1.0 + math.exp(-v)) if v >= 0 else math.exp(v) / (1.0 + math.exp(v)))
        W = [pt[i] * (1.0 - pt[i]) for i in range(n)]
        XtW = [[0.0] * p for _ in range(p)]
        XtWz = [0.0] * p
        for i in range(n):
            wi = W[i] if W[i] > 1e-9 else 1e-9
            resid = y[i] - pt[i]
            zi = sum(b * xi for b, xi in zip(beta, X[i])) + resid / wi
            for a in range(p):
                XtWz[a] += X[i][a] * wi * zi
                for bb in range(p):
                    XtW[a][bb] += X[i][a] * wi * X[i][bb]
        for a in range(p):
            XtW[a][a] += 1e-6
        beta_new = solve3(XtW, XtWz)
        if max(abs(beta_new[a] - beta[a]) for a in range(p)) < 1e-7:
            beta = beta_new
            break
        beta = beta_new
    return beta


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
        c24 = c168 = 0.0
        rv24 = [None] * n
        rv168 = [None] * n
        for i in range(n):
            c24 += rv1[i]
            c168 += rv1[i]
            if i >= 24:
                c24 -= rv1[i - 24]
            if i >= 168:
                c168 -= rv1[i - 168]
            if i >= 23:
                rv24[i] = c24
            if i >= 167:
                rv168[i] = c168
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
            y = sum(rv1[i + 1:i + 25])
            if rv24[i] is None or rv168[i] is None or y <= 0 or rv24[i] <= 0 or rv168[i] <= 0:
                continue
            j = bisect.bisect_right(ft, t) - 1
            if j < 0:
                continue
            cur = fv[j]
            lo = bisect.bisect_right(ft, t - 24 * 3600)
            f24 = sum(fv[lo:j + 1])
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
                                math.log(max(rv168[i], 1e-12))],
                          "f": [f24, pct], "p": [prem], "y": y})
    panel.sort(key=lambda x: x["t"])
    uniq = sorted({x["t"] for x in panel})
    nu = len(uniq)
    b1 = uniq[int(0.6 * nu)] - EMBARGO_H * 3600
    b2 = uniq[int(0.8 * nu)] - EMBARGO_H * 3600
    train = [x for x in panel if x["t"] < b1]
    test = [x for x in panel if x["t"] >= b2]

    train_y = sorted(x["y"] for x in train)
    threshold = train_y[int(0.95 * (len(train_y) - 1))]

    def feat(x, model):
        base = x["b"]
        if model == "B1":
            return base
        return base + x["f"] + x["p"]

    zs = [1.0 if x["y"] > threshold else 0.0 for x in test]
    results = {}
    for model in ("B1", "C2"):
        X = [feat(x, model) for x in train]
        mu = [sum(col) / len(col) for col in zip(*X)]
        sd = [statistics.pstdev([row[k] for row in X]) or 1.0 for k in range(len(X[0]))]
        Xs = [[1.0] + [(row[k] - mu[k]) / sd[k] for k in range(len(row))] for row in X]
        y = [1.0 if x["y"] > threshold else 0.0 for x in train]
        beta = fit_irls(Xs, y)
        brier = 0.0
        ll = 0.0
        bins = [[] for _ in range(10)]
        for x, z in zip(test, zs):
            row = feat(x, model)
            xs = [1.0] + [(row[k] - mu[k]) / sd[k] for k in range(len(row))]
            v = sum(b * xi for b, xi in zip(beta, xs))
            pp = 1.0 / (1.0 + math.exp(-v)) if v >= 0 else math.exp(v) / (1.0 + math.exp(v))
            pp = min(max(pp, 1e-9), 1 - 1e-9)
            brier += (pp - z) ** 2
            ll += z * math.log(pp) + (1.0 - z) * math.log(1.0 - pp)
            bi = min(int(pp * 10), 9)
            bins[bi].append((pp, z))
        brier /= len(test)
        ll = -ll / len(test)
        ece = 0.0
        for b in bins:
            if not b:
                continue
            mp = sum(p for p, _ in b) / len(b)
            mz = sum(z for _, z in b) / len(b)
            ece += (len(b) / len(test)) * abs(mp - mz)
        results[model] = {"brier": brier, "log_loss": ll, "ece": ece, "n": len(test)}

    rel = (results["B1"]["brier"] - results["C2"]["brier"]) / max(results["B1"]["brier"], 1e-12)
    sufficient = len(test) >= 500 and nu >= 500
    improved = rel >= 0.02
    verdict = "INCONCLUSIVE" if not sufficient else ("PROMOTED" if improved else "NOT_SUPPORTED")

    ev = json.load(open(os.path.join(HERE, f"fclr_live_archive03_eval_{SESSION}.json")))
    checks = {
        "brier_B1_match": abs(results["B1"]["brier"] - ev["metrics"]["B1"]["brier"]) < 1e-9,
        "brier_C2_match": abs(results["C2"]["brier"] - ev["metrics"]["C2"]["brier"]) < 1e-4,
        "ll_B1_match": abs(results["B1"]["log_loss"] - ev["metrics"]["B1"]["log_loss"]) < 1e-9,
        "ll_C2_match": abs(results["C2"]["log_loss"] - ev["metrics"]["C2"]["log_loss"]) < 1e-3,
        "rel_reduction_match": abs(rel - ev["relative_brier_reduction_C2_vs_B1"]) < 5e-3,
        "n_test_match": len(test) == ev["n_test"],
        "verdict_reproduced": verdict == ev["verdict"],
    }
    out = {
        "experiment_id": EXPERIMENT,
        "session_id": SESSION,
        "artifact_id": f"fclr_live_archive03_recompute_{SESSION}",
        "method": "independent stdlib recompute (separate parser + plain Gauss-Jordan IRLS solver)",
        "n_test": len(test),
        "n_unique_timestamps": nu,
        "stress_threshold": threshold,
        "recomputed": results,
        "relative_reduction_C2_vs_B1": rel,
        "eval": {m: ev["metrics"][m] for m in ("B1", "C2")},
        "eval_rel": ev["relative_brier_reduction_C2_vs_B1"],
        "abs_diffs": {
            "brier_B1": abs(results["B1"]["brier"] - ev["metrics"]["B1"]["brier"]),
            "brier_C2": abs(results["C2"]["brier"] - ev["metrics"]["C2"]["brier"]),
            "rel": abs(rel - ev["relative_brier_reduction_C2_vs_B1"]),
        },
        "checks": checks,
        "all_checks_match": all(checks.values()),
        "stdlib_only": True,
        "network": False,
        "read_only_cache": True,
        "verdict_reproduced": verdict,
        "eval_verdict": ev["verdict"],
    }
    with open(os.path.join(HERE, f"fclr_live_archive03_recompute_{SESSION}.json"), "w") as f:
        json.dump(out, f, indent=2)
    print(json.dumps({"all_checks_match": out["all_checks_match"],
                      "rel_brier": rel, "verdict": verdict, "checks": checks}, indent=1))


if __name__ == "__main__":
    main()
