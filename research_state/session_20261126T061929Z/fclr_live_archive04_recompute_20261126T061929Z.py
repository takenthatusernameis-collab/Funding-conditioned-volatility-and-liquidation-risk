#!/usr/bin/env python3
"""FCLR-LIVE-ARCHIVE-04 INDEPENDENT stdlib recompute (separate code path).

Re-parses the raw Binance archive zips, rebuilds the next-24h realized-variance
quantile panel with an independent implementation, refits B1 and C2 with a
DIFFERENT MM/IRLS linear solver (plain Gauss-Jordan, no pivoting; different
iteration budget), and recomputes test-set average / per-quantile pinball loss,
empirical coverage and the relative average-pinball reduction. Compares against
fclr_live_archive04_eval_<UTC>.json and asserts all_checks_match.

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

SESSION = "20261126T061929Z"
EXPERIMENT = "FCLR-LIVE-ARCHIVE-04"
HERE = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.join(HERE, "..", "session_20261126T042519Z", "raw")
SYMBOLS = ["1INCHUSDT", "AAVEUSDT", "ADAUSDT", "ALGOUSDT", "ALPHAUSDT"]
MONTHS = [f"{y}-{m:02d}" for y in (2021, 2022, 2023, 2024) for m in range(1, 13)]
EMBARGO_H = 168
TAUS = [0.10, 0.25, 0.50, 0.75, 0.90]
EPS = 1e-7
QR_ITERS = 150
QR_TOL = 1e-11


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


def qfit(X, y, tau):
    # independent MM/IRLS quantile fit: plain Gauss-Jordan solver, monotone
    # step-halving on the actual check-loss objective, tighter tol.
    n = len(X)
    p = len(X[0])
    beta = [0.0] * p
    ys = sorted(y)
    beta[0] = ys[min(int(tau * (n - 1)), n - 1)]

    def obj(b):
        return sum(pinb(y[i] - sum(b[a] * X[i][a] for a in range(p)), tau)
                   for i in range(n))

    fcur = obj(beta)
    for _ in range(QR_ITERS):
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
        bn = solve_gj(XtW, XtWz)
        step = 1.0
        accepted = False
        cand = beta
        fc = fcur
        for _h in range(50):
            cand = [beta[a] + step * (bn[a] - beta[a]) for a in range(p)]
            fc = obj(cand)
            if fc <= fcur + 1e-15:
                accepted = True
                break
            step *= 0.5
        if not accepted:
            break
        delta = max(abs(cand[a] - beta[a]) for a in range(p))
        beta = cand
        fcur = fc
        if delta < QR_TOL:
            break
    return beta


def pinb(u, tau):
    return u * (tau - 1.0) if u < 0 else u * tau


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
                          "f": [f24, pct, prem, mdist], "y": y})
    panel.sort(key=lambda x: x["t"])
    uniq = sorted({x["t"] for x in panel})
    nu = len(uniq)
    b1 = uniq[int(0.6 * nu)] - EMBARGO_H * 3600
    b2 = uniq[int(0.8 * nu)] - EMBARGO_H * 3600
    train = [x for x in panel if x["t"] < b1]
    test = [x for x in panel if x["t"] >= b2]

    def feat(x, model):
        return x["b"] if model == "B1" else x["b"] + x["f"]

    def fit(model):
        X = [feat(x, model) for x in train]
        mu = [sum(col) / len(col) for col in zip(*X)]
        sd = [statistics.pstdev([row[k] for row in X]) or 1.0 for k in range(len(X[0]))]
        Xs = [[1.0] + [(row[k] - mu[k]) / sd[k] for k in range(len(row))] for row in X]
        y_raw = [x["y"] for x in train]
        ymean = sum(y_raw) / len(y_raw)
        ystd = statistics.pstdev(y_raw) or 1.0
        y = [(v - ymean) / ystd for v in y_raw]
        betas = {tau: qfit(Xs, y, tau) for tau in TAUS}
        return {"mu": mu, "sd": sd, "betas": betas, "model": model,
                "ymean": ymean, "ystd": ystd}

    models = {m: fit(m) for m in ("B1", "C2")}
    ys = [x["y"] for x in test]

    def preds(m):
        mm = models[m]
        out = {tau: [] for tau in TAUS}
        for x in test:
            row = feat(x, m)
            xs = [1.0] + [(row[k] - mm["mu"][k]) / mm["sd"][k] for k in range(len(row))]
            for tau in TAUS:
                out[tau].append(mm["ymean"] + mm["ystd"] *
                                sum(b * xi for b, xi in zip(mm["betas"][tau], xs)))
        return out

    P = {m: preds(m) for m in ("B1", "C2")}
    res = {}
    for m in ("B1", "C2"):
        per_tau = {}
        cover = {}
        for tau in TAUS:
            pl = P[m][tau]
            per_tau[tau] = sum(pinb(yy - p, tau) for p, yy in zip(pl, ys)) / max(len(ys), 1)
            cover[tau] = sum(1 for p, yy in zip(pl, ys) if yy <= p) / max(len(ys), 1)
        avg = sum(per_tau.values()) / len(TAUS)
        res[m] = {"avg_pinball": avg, "per_tau_pinball": per_tau, "empirical_coverage": cover}

    rel = (res["B1"]["avg_pinball"] - res["C2"]["avg_pinball"]) / max(res["B1"]["avg_pinball"], 1e-12)
    sufficient = len(test) >= 500 and nu >= 500
    improved = rel >= 0.02
    verdict = "INCONCLUSIVE" if not sufficient else ("PROMOTED" if improved else "NOT_SUPPORTED")

    ev = json.load(open(os.path.join(HERE, f"fclr_live_archive04_eval_{SESSION}.json")))
    checks = {
        "avg_pinball_B1_match": abs(res["B1"]["avg_pinball"] - ev["metrics"]["B1"]["avg_pinball"]) < 1e-6,
        "avg_pinball_C2_match": abs(res["C2"]["avg_pinball"] - ev["metrics"]["C2"]["avg_pinball"]) < 1e-6,
        "rel_reduction_match": abs(rel - ev["relative_avg_pinball_reduction_C2_vs_B1"]) < 5e-3,
        "n_test_match": len(test) == ev["n_test"],
        "verdict_reproduced": verdict == ev["verdict"],
    }
    out = {
        "experiment_id": EXPERIMENT,
        "session_id": SESSION,
        "artifact_id": f"fclr_live_archive04_recompute_{SESSION}",
        "method": "independent stdlib recompute (separate parser + plain Gauss-Jordan MM/IRLS solver)",
        "n_test": len(test),
        "n_unique_timestamps": nu,
        "recomputed": res,
        "relative_reduction_C2_vs_B1": rel,
        "eval": {m: ev["metrics"][m] for m in ("B1", "C2")},
        "eval_rel": ev["relative_avg_pinball_reduction_C2_vs_B1"],
        "abs_diffs": {
            "avg_pinball_B1": abs(res["B1"]["avg_pinball"] - ev["metrics"]["B1"]["avg_pinball"]),
            "avg_pinball_C2": abs(res["C2"]["avg_pinball"] - ev["metrics"]["C2"]["avg_pinball"]),
            "rel": abs(rel - ev["relative_avg_pinball_reduction_C2_vs_B1"]),
        },
        "checks": checks,
        "all_checks_match": all(checks.values()),
        "stdlib_only": True,
        "network": False,
        "read_only_cache": True,
        "verdict_reproduced": verdict,
        "eval_verdict": ev["verdict"],
    }
    with open(os.path.join(HERE, f"fclr_live_archive04_recompute_{SESSION}.json"), "w") as f:
        json.dump(out, f, indent=2)
    print(json.dumps({"all_checks_match": out["all_checks_match"],
                      "rel_pinball": rel, "verdict": verdict, "checks": checks}, indent=1))


if __name__ == "__main__":
    main()