#!/usr/bin/env python3
"""FCLR-LIVE-ARCHIVE-07 INDEPENDENT stdlib recompute (separate code path).

This does NOT import the eval script. It independently:
  * re-parses the read-only Binance archive cache (markPriceKlines only, any
    depth, dedup by open_time, close>0) to rebuild the all-five common support S;
  * rebuilds the next-24h mean log-realized-variance target and the B1/C2
    feature panels from scratch;
  * refits B1 and C2 with a DIFFERENT solver (train-only standardization +
    Cholesky normal-equation solve, ridge-stabilised) instead of the eval's
    pivoted Gauss-Jordan;
  * recomputes the standard non-negative QLIKE, the relative C2-vs-B1
    reduction, and the verdict, then asserts all_checks_match against
    fclr_live_archive07_eval_<UTC>.json.

Stdlib only. Read-only cache. No network.
"""
from __future__ import annotations

import bisect
import datetime as dt
import glob
import io
import json
import math
import os
import zipfile

SESSION = "20261127T065600Z"
EXPERIMENT = "FCLR-LIVE-ARCHIVE-07"
HERE = os.path.dirname(os.path.abspath(__file__))
CACHE = os.path.join(HERE, "..", "data_cache")
SYMBOLS = ["BNBUSDT", "BTCUSDT", "ETHUSDT", "SOLUSDT", "XRPUSDT"]
MONTHS = [f"{y}_{m:02d}" for y in (2024, 2025, 2026) for m in range(1, 13)
          if (y == 2024 and m >= 4) or y == 2025 or (y == 2026 and m <= 10)]
EMBARGO_H = 168
EPS = 1e-9
FLOOR = 0.02
RIDGE = 1e-6


def _lines(path: str):
    if path.endswith(".zip"):
        with open(path, "rb") as f:
            z = zipfile.ZipFile(io.BytesIO(f.read()))
            return z.read(z.namelist()[0]).decode("utf-8", "ignore").splitlines()
    with open(path, "r", encoding="utf-8", errors="ignore") as f:
        return f.read().splitlines()


def _is_mark(path: str) -> bool:
    return any(part.startswith("markPriceKlines-") for part in path.split(os.sep))


def _is_index(path: str) -> bool:
    return any(part.startswith("indexPriceKlines-") for part in path.split(os.sep))


def _load_klines(sym: str, want) -> dict:
    """Independent loader for mark or index 1h klines: any-depth, dedup by
    open_time, drop close<=0, open_time converted ms->s."""
    out: dict[int, float] = {}
    for month in MONTHS:
        base = os.path.join(CACHE, f"{sym}_{month}")
        if not os.path.isdir(base):
            continue
        for path in glob.glob(os.path.join(base, "**", "*"), recursive=True):
            if not os.path.isfile(path) or path.endswith(".sha256"):
                continue
            if not want(path):
                continue
            if not (path.endswith(".csv") or path.endswith(".zip")):
                continue
            for ln in _lines(path)[1:]:
                parts = ln.split(",")
                if len(parts) < 5:
                    continue
                try:
                    ot = int(parts[0]) // 1000
                    cl = float(parts[4])
                except ValueError:
                    continue
                if cl <= 0.0:
                    continue
                out[ot] = cl
    return out


def load_mark(sym: str) -> dict:
    return _load_klines(sym, _is_mark)


def load_index(sym: str) -> dict:
    return _load_klines(sym, _is_index)


def load_funding(sym: str):
    """Mirror eval: one funding file per month at the month-dir root
    (.zip or .csv), rate in column 2, open_time ms->s."""
    ft, fv = [], []
    for month in MONTHS:
        base = os.path.join(CACHE, f"{sym}_{month}")
        if not os.path.isdir(base):
            continue
        stem = f"{sym}-fundingRate-{month.replace('_', '-')}"
        path = None
        for ext in (".zip", ".csv"):
            cand = os.path.join(base, stem + ext)
            if os.path.exists(cand):
                path = cand
                break
        if path is None:
            continue
        for ln in _lines(path)[1:]:
            p = ln.split(",")
            if len(p) < 3:
                continue
            try:
                ft.append(int(p[0]) // 1000)
                fv.append(float(p[2]))
            except ValueError:
                continue
    order = sorted(range(len(ft)), key=lambda i: ft[i])
    return [ft[i] for i in order], [fv[i] for i in order]


def build(sym: str, mark: dict, index: dict, common: set):
    ts = sorted(t for t in mark if t in common)
    n = len(ts)
    close = mark
    r = [0.0] * n
    for i in range(1, n):
        if ts[i] - ts[i - 1] == 3600 and close[ts[i]] > 0 and close[ts[i - 1]] > 0:
            r[i] = math.log(close[ts[i]] / close[ts[i - 1]])
    rv1 = [v * v for v in r]
    rpos = [v * v if v > 0 else 0.0 for v in r]
    rneg = [v * v if v < 0 else 0.0 for v in r]

    def roll(vals, w):
        acc = [0.0] * (n + 1)
        for i in range(n):
            acc[i + 1] = acc[i] + vals[i]
        o = [None] * n
        for i in range(w - 1, n):
            o[i] = acc[i + 1] - acc[i + 1 - w]
        return o

    rv24 = roll(rv1, 24)
    rv168 = roll(rv1, 168)
    rp24 = roll(rpos, 24)
    rm24 = roll(rneg, 24)
    rp168 = roll(rpos, 168)
    rm168 = roll(rneg, 168)
    accp = [0.0] * (n + 1)
    accn = [0.0] * (n + 1)
    for i in range(n):
        accp[i + 1] = accp[i] + rpos[i]
        accn[i + 1] = accn[i] + rneg[i]
    next_rv = [None] * n
    for i in range(n - 24):
        next_rv[i] = (accp[i + 25] - accp[i + 1]) + (accn[i + 25] - accn[i + 1])

    ft, fv = load_funding(sym)
    ema = {}
    alpha = 2.0 / (24 + 1)
    e = None
    for t in ts:
        m = mark.get(t)
        if m is None:
            continue
        e = m if e is None else alpha * m + (1 - alpha) * e
        ema[t] = e
    rows = []
    for i in range(168, n - 24):
        if None in (rv24[i], rv168[i], rp24[i], rm24[i], rp168[i], rm168[i], next_rv[i]):
            continue
        t = ts[i]
        y = math.log(max(next_rv[i], 0.0) + EPS)
        j = bisect.bisect_right(ft, t) - 1 if ft else -1
        if j < 0:
            continue
        cur = fv[j]
        lo = bisect.bisect_right(ft, t - 24 * 3600)
        fund24 = sum(fv[lo:j + 1]) if j >= lo else 0.0
        lo90 = bisect.bisect_right(ft, t - 90 * 86400)
        win = [abs(x) for x in fv[lo90:j + 1]]
        pct = (sum(1 for x in win if x <= abs(cur)) / len(win)) if win else 0.5
        mk = mark.get(t)
        ix = index.get(t)
        prem = (mk - ix) / ix if (mk is not None and ix not in (None, 0)) else 0.0
        em = ema.get(t)
        mdist = (mk - em) / em if (mk is not None and em not in (None, 0)) else 0.0
        rows.append((t, y, rv1[i], rv24[i], rv168[i], rp24[i], rm24[i],
                     rp168[i], rm168[i], fund24, pct, prem, mdist))
    return rows


def feat(row, model):
    (_, y, rv1, rv24, rv168, rp24, rm24, rp168, rm168, fund24, pct,
     prem, mdist) = row
    b = [math.log(max(v, 1e-12)) for v in (rv1, rv24, rv168, rp24, rm24, rp168, rm168)]
    return b if model == "B1" else b + [fund24, pct, prem, mdist]


def cholesky_solve(A, b):
    """Solve SPD system A x = b via Cholesky (independent of eval's GE)."""
    p = len(A)
    L = [[0.0] * p for _ in range(p)]
    for i in range(p):
        for j in range(i + 1):
            s = A[i][j] - sum(L[i][k] * L[j][k] for k in range(j))
            if i == j:
                L[i][j] = math.sqrt(s if s > 1e-12 else 1e-12)
            else:
                L[i][j] = s / L[j][j]
    y = [0.0] * p
    for i in range(p):
        y[i] = (b[i] - sum(L[i][k] * y[k] for k in range(i))) / L[i][i]
    x = [0.0] * p
    for i in range(p - 1, -1, -1):
        x[i] = (y[i] - sum(L[k][i] * x[k] for k in range(i + 1, p))) / L[i][i]
    return x


def fit(rows, model):
    """Train-only standardization + ridge Cholesky OLS."""
    X = [[1.0] + feat(r, model) for r in rows]
    y = [r[1] for r in rows]
    p = len(X[0])
    mu = [sum(X[i][j] for i in range(len(X))) / len(X) for j in range(1, p)]
    sd = []
    for j in range(1, p):
        v = sum((X[i][j] - mu[j - 1]) ** 2 for i in range(len(X))) / len(X)
        sd.append(math.sqrt(v) if v > 1e-18 else 1.0)
    Z = []
    for i in range(len(X)):
        row = [1.0]
        for j in range(1, p):
            row.append((X[i][j] - mu[j - 1]) / sd[j - 1])
        Z.append(row)
    XtX = [[0.0] * p for _ in range(p)]
    Xty = [0.0] * p
    for i in range(len(Z)):
        zi, yi = Z[i], y[i]
        for a in range(p):
            Xty[a] += zi[a] * yi
            for bb in range(p):
                XtX[a][bb] += zi[a] * zi[bb]
    for a in range(1, p):
        XtX[a][a] += RIDGE
    beta = cholesky_solve(XtX, Xty)
    return {"model": model, "beta": beta, "mu": mu, "sd": sd}


def predict(m, r):
    x = feat(r, m["model"])
    z = [1.0] + [(x[j] - m["mu"][j]) / m["sd"][j] for j in range(len(x))]
    return sum(b * zi for b, zi in zip(m["beta"], z))


def qlike(y, p):
    return sum(math.exp(y[i] - p[i]) - (y[i] - p[i]) - 1.0 for i in range(len(y))) / len(y)


def main():
    raw = {s: load_mark(s) for s in SYMBOLS}
    idx = {s: load_index(s) for s in SYMBOLS}
    common = set(raw[SYMBOLS[0]])
    for s in SYMBOLS[1:]:
        common &= set(raw[s])
    n_common = len(common)
    panel = []
    for s in SYMBOLS:
        panel.extend(build(s, raw[s], idx[s], common))
    panel.sort(key=lambda r: r[0])
    uniq = sorted({r[0] for r in panel})
    nu = len(uniq)
    cut1 = uniq[int(0.6 * nu)] - EMBARGO_H * 3600
    cut2 = uniq[int(0.8 * nu)] - EMBARGO_H * 3600
    train = [r for r in panel if r[0] < cut1]
    test = [r for r in panel if r[0] >= cut2]
    b1 = fit(train, "B1")
    b2 = fit(train, "C2")
    ys = [r[1] for r in test]
    p1 = [predict(b1, r) for r in test]
    p2 = [predict(b2, r) for r in test]
    q1 = qlike(ys, p1)
    q2 = qlike(ys, p2)
    rel = (q1 - q2) / q1 if q1 > 0 else 0.0
    verdict = "NOT_SUPPORTED" if not (rel >= FLOOR) else "PROMOTED"

    with open(os.path.join(HERE, f"fclr_live_archive07_eval_{SESSION}.json")) as f:
        ev = json.load(f)
    checks = {
        "n_common_match": n_common == ev["common_support"]["n_common"],
        "n_test_match": len(test) == ev["n_test"],
        "n_unique_timestamps_match": nu == ev["n_unique_timestamps"],
        "qlike_B1_match": abs(q1 - ev["metrics"]["B1"]["qlike"]) < 1e-6,
        "qlike_C2_match": abs(q2 - ev["metrics"]["C2"]["qlike"]) < 1e-6,
        "rel_qlike_match": abs(rel - ev["relative_qlike_reduction_C2_vs_B1"]) < 1e-6,
        "verdict_match": verdict == ev["verdict"],
    }
    all_match = all(checks.values())
    out = {
        "experiment_id": EXPERIMENT,
        "session_id": SESSION,
        "artifact_id": f"fclr_live_archive07_recompute_{SESSION}",
        "generated_at": dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "method": "independent stdlib recompute: own cache reader, own panel build, train-only standardization + Cholesky ridge OLS",
        "n_common": n_common,
        "n_test": len(test),
        "n_unique_timestamps": nu,
        "qlike_B1": q1,
        "qlike_C2": q2,
        "relative_qlike_reduction_C2_vs_B1": rel,
        "verdict": verdict,
        "checks": checks,
        "all_checks_match": all_match,
        "stdlib_only": True,
        "network": False,
        "read_only_cache": True,
    }
    with open(os.path.join(HERE, f"fclr_live_archive07_recompute_{SESSION}.json"), "w") as f:
        json.dump(out, f, indent=2)
    print(json.dumps({k: out[k] for k in ("n_common", "n_test", "qlike_B1",
                                          "qlike_C2", "verdict", "all_checks_match")}, indent=2))
    if not all_match:
        print("CHECKS:", checks)
        raise SystemExit("RECOMPUTE MISMATCH")


if __name__ == "__main__":
    main()