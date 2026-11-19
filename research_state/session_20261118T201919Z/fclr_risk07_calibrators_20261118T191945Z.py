#!/usr/bin/env python3
"""FCLR-LIQ-RISK-RECALIBRATION-07 — stdlib train-only probability calibrators.

Campaign: FCLR-LIQ-RISK-RECALIBRATION-07-20261118T191714Z
Session:  session_20261118T191945Z

Implements (stdlib only: math/random/statistics):
  C1_platt         sigmoid(a*logit(s)+b) via IRLS with ridge 1e-6
  C2_isotonic      PAVA isotonic on out-of-fold (s,y), tie pooling, interpolation, clipped
  C3_prior_offset  sigmoid(logit(s)+logit(p_train)-logit(mean_train_score))
  C0_identity      reference base score

Also: equal-count ECE with min-bin merging, reliability slope/intercept diagnostics,
and outcome-blind self-tests (monotonicity, bounds, identity).

Running this file writes fclr_risk07_calibrators_<UTC>.json with the self-test evidence.
"""
from __future__ import annotations

import json
import math
import random
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
SESSION_DIR = REPO / "research_state" / "session_20261118T191945Z"
UTC_STAMP = "20261118T191945Z"
RIDGE = 1e-6
EPS = 1e-12


# ------------------------------------------------------------------- numerics
def sigmoid(z: float) -> float:
    if z >= 0:
        return 1.0 / (1.0 + math.exp(-z))
    ez = math.exp(z)
    return ez / (1.0 + ez)


def logit(p: float) -> float:
    q = min(1.0 - EPS, max(EPS, p))
    return math.log(q / (1.0 - q))


def solve_linear(A, b):
    p = len(A)
    aug = [list(A[r]) + [b[r]] for r in range(p)]
    for col in range(p):
        piv = max(range(col, p), key=lambda r: abs(aug[r][col]))
        if abs(aug[piv][col]) < 1e-12:
            return None
        aug[col], aug[piv] = aug[piv], aug[col]
        pv = aug[col][col]
        for r in range(col + 1, p):
            f = aug[r][col] / pv
            if f == 0.0:
                continue
            for c in range(col, p + 1):
                aug[r][c] -= f * aug[col][c]
    x = [0.0] * p
    for r in range(p - 1, -1, -1):
        s = aug[r][p]
        for c in range(r + 1, p):
            s -= aug[r][c] * x[c]
        if abs(aug[r][r]) < 1e-12:
            return None
        x[r] = s / aug[r][r]
    return x


def irls_generic(X, y, max_iters=100, tol=1e-8):
    n = len(X)
    p = len(X[0]) if n else 0
    beta = [0.0] * p
    for _ in range(max_iters):
        eta = [sum(X[i][j] * beta[j] for j in range(p)) for i in range(n)]
        phat = [sigmoid(e) for e in eta]
        W = [phat[i] * (1.0 - phat[i]) for i in range(n)]
        XtWX = [[0.0] * p for _ in range(p)]
        XtWz = [0.0] * p
        for i in range(n):
            wi = W[i]
            if wi <= 0.0:
                continue
            row = X[i]
            zi = eta[i] + (y[i] - phat[i]) / (wi if wi > 1e-12 else 1e-12)
            wzi = wi * zi
            for j in range(p):
                vj = row[j]
                if vj == 0.0:
                    continue
                XtWz[j] += vj * wzi
                for k in range(j, p):
                    XtWX[j][k] += vj * row[k] * wi
        for j in range(p):
            for k in range(j):
                XtWX[j][k] = XtWX[k][j]
        for j in range(p):
            XtWX[j][j] += RIDGE
        nb = solve_linear(XtWX, XtWz)
        if nb is None:
            return beta
        change = max(abs(nb[j] - beta[j]) for j in range(p))
        beta = nb
        if change < tol:
            break
    return beta


# ---------------------------------------------------------------- C1  (Platt)
def fit_platt(scores, ys):
    X = [[1.0, logit(s)] for s in scores]
    return irls_generic(X, list(ys))


def apply_platt(s, params):
    b, a = params[0], params[1]
    return min(1.0, max(0.0, sigmoid(a * logit(s) + b)))


# ------------------------------------------------------------- C2  (isotonic)
def fit_isotonic(scores, ys):
    """PAVA with tie pooling. Returns knot arrays (xs strictly increasing, ys non-decreasing)."""
    pairs = sorted(zip(scores, ys))
    xs, yrs, wts = [], [], []
    i = 0
    while i < len(pairs):
        j = i
        sy = 0.0
        while j < len(pairs) and pairs[j][0] == pairs[i][0]:
            sy += pairs[j][1]
            j += 1
        c = j - i
        xs.append(pairs[i][0])
        yrs.append(sy / c)
        wts.append(c)
        i = j
    # pool adjacent violators
    vy, vw = [], []
    for k in range(len(xs)):
        vy.append(yrs[k])
        vw.append(wts[k])
        while len(vy) > 1 and vy[-2] > vy[-1] + 1e-15:
            w = vw[-2] + vw[-1]
            y = (vy[-2] * vw[-2] + vy[-1] * vw[-1]) / w
            vw.pop()
            vy.pop()
            vw[-1] = w
            vy[-1] = y
    # expand block values back onto distinct x knots
    ys_knot = [0.0] * len(xs)
    bi = 0
    acc = 0
    for k in range(len(xs)):
        acc += wts[k]
        ys_knot[k] = vy[bi]
        if acc >= vw[bi] - 1e-12:
            acc = 0
            bi = min(bi + 1, len(vy) - 1)
    for k in range(1, len(ys_knot)):
        if ys_knot[k] < ys_knot[k - 1]:
            ys_knot[k] = ys_knot[k - 1]
    return {"xs": xs, "ys": ys_knot}


def apply_isotonic(s, kn):
    xs, ys = kn["xs"], kn["ys"]
    if not xs:
        return 0.5
    if s <= xs[0]:
        return min(1.0, max(0.0, ys[0]))
    if s >= xs[-1]:
        return min(1.0, max(0.0, ys[-1]))
    lo, hi = 0, len(xs) - 1
    while hi - lo > 1:
        mid = (lo + hi) // 2
        if xs[mid] <= s:
            lo = mid
        else:
            hi = mid
    x0, x1 = xs[lo], xs[hi]
    y0, y1 = ys[lo], ys[hi]
    if x1 <= x0:
        return min(1.0, max(0.0, y1))
    t = (s - x0) / (x1 - x0)
    return min(1.0, max(0.0, y0 + t * (y1 - y0)))


# ------------------------------------------------------- C3  (prior offset)
def fit_prior(scores, ys):
    n = len(ys)
    p_train = sum(ys) / n if n else 0.0
    mean_s = sum(scores) / n if n else 0.0
    p_train = min(1.0 - 1e-6, max(1e-6, p_train))
    mean_s = min(1.0 - 1e-6, max(1e-6, mean_s))
    return {"offset": logit(p_train) - logit(mean_s), "p_train": p_train, "mean_train_score": mean_s}


def apply_prior(s, params):
    return min(1.0, max(0.0, sigmoid(logit(s) + params["offset"])))


# ------------------------------------------------------------ model registry
CALIBRATORS = ("C0_identity", "C1_platt", "C2_isotonic", "C3_prior_offset")


def fit_calibrator(name, scores, ys):
    if name == "C0_identity":
        return {}
    if name == "C1_platt":
        return {"params": fit_platt(scores, ys)}
    if name == "C2_isotonic":
        return {"knots": fit_isotonic(scores, ys)}
    if name == "C3_prior_offset":
        return {"params": fit_prior(scores, ys)}
    raise ValueError(name)


def apply_calibrator(name, s, fit):
    if name == "C0_identity":
        return min(1.0, max(0.0, s))
    if name == "C1_platt":
        return apply_platt(s, fit["params"])
    if name == "C2_isotonic":
        return apply_isotonic(s, fit["knots"])
    if name == "C3_prior_offset":
        return apply_prior(s, fit["params"])
    raise ValueError(name)


# -------------------------------------------------------------------- metrics
def brier(preds, ys):
    return sum((preds[i] - ys[i]) ** 2 for i in range(len(ys))) / len(ys)


def logloss(preds, ys):
    s = 0.0
    for i in range(len(ys)):
        p = min(1.0 - EPS, max(EPS, preds[i]))
        s += -(ys[i] * math.log(p) + (1 - ys[i]) * math.log(1.0 - p))
    return s / len(ys)


def ece_equal_count(preds, ys, nbins=10, min_bin=30):
    """Equal-count ECE; merge bins with <min_bin rows into a neighbour; report bin count."""
    order = sorted(range(len(preds)), key=lambda i: preds[i])
    n = len(order)
    bins = []
    for b in range(nbins):
        lo = b * n // nbins
        hi = (b + 1) * n // nbins
        idx = order[lo:hi]
        if idx:
            bins.append({"idx": idx, "n": len(idx)})
    # merge under-populated bins
    changed = True
    while changed and len(bins) > 1:
        changed = False
        for k, b in enumerate(bins):
            if b["n"] < min_bin:
                if k + 1 < len(bins):
                    bins[k + 1]["idx"] = bins[k]["idx"] + bins[k + 1]["idx"]
                    bins[k + 1]["n"] += bins[k]["n"]
                else:
                    bins[k - 1]["idx"] = bins[k - 1]["idx"] + bins[k]["idx"]
                    bins[k - 1]["n"] += bins[k]["n"]
                bins.pop(k)
                changed = True
                break
    total = 0.0
    for b in bins:
        idx = b["idx"]
        mp = sum(preds[i] for i in idx) / len(idx)
        mo = sum(ys[i] for i in idx) / len(idx)
        total += (len(idx) / n) * abs(mp - mo)
    return {"ece": total, "n_bins": len(bins), "min_bin_size": min(b["n"] for b in bins)}


def auc(scores, y):
    n_pos = sum(y)
    n_neg = len(y) - n_pos
    if n_pos == 0 or n_neg == 0:
        return None
    order = sorted(range(len(scores)), key=lambda i: scores[i])
    ranks = [0.0] * len(scores)
    i = 0
    while i < len(order):
        j = i
        while j + 1 < len(order) and scores[order[j + 1]] == scores[order[i]]:
            j += 1
        avg = (i + j) / 2.0 + 1.0
        for k in range(i, j + 1):
            ranks[order[k]] = avg
        i = j + 1
    rp = sum(ranks[i] for i in range(len(y)) if y[i] == 1)
    return (rp - n_pos * (n_pos + 1) / 2.0) / (n_pos * n_neg)


def reliability_fit(preds, ys):
    """1-D logistic slope/intercept on logit(pred); diagnostic only."""
    X = [[1.0, logit(p)] for p in preds]
    b = irls_generic(X, list(ys))
    return {"slope": b[1], "intercept": b[0]}


# --------------------------------------------------------------- self-tests
def run_self_tests():
    rng = random.Random(12345)
    n = 4000
    # synthetic: truth depends on a hidden monotone score with mild noise
    scores, ys = [], []
    for _ in range(n):
        z = rng.gauss(0.0, 1.0)
        p = sigmoid(-2.0 + 0.9 * z)
        y = 1 if rng.random() < p else 0
        s = sigmoid(-3.0 + 1.4 * z + rng.gauss(0.0, 0.35))
        scores.append(s)
        ys.append(y)
    grid = [i / 100.0 for i in range(1, 100)]

    out = {"schema": "fclr_risk07_calibrators_selftest", "session": f"session_{UTC_STAMP}",
           "n_synthetic": n, "tests": {}}

    platt = fit_platt(scores, ys)
    pv = [apply_platt(s, platt) for s in grid]
    out["tests"]["C1_monotone_nondecreasing_in_score"] = all(pv[i] <= pv[i + 1] + 1e-12 for i in range(len(pv) - 1))
    out["tests"]["C1_params"] = {"a": platt[0], "b": platt[1]}

    kn = fit_isotonic(scores, ys)
    iv = [apply_isotonic(s, kn) for s in grid]
    out["tests"]["C2_monotone_nondecreasing_in_score"] = all(iv[i] <= iv[i + 1] + 1e-12 for i in range(len(iv) - 1))
    out["tests"]["C2_n_knots"] = len(kn["xs"])

    # C3 identity when p_train == mean_train_score
    const_scores = [0.2] * n
    const_ys = ([1] * 800) + ([0] * (n - 800))
    fake_params = fit_prior(const_scores, const_ys)
    ident_err = max(abs(apply_prior(s, fake_params) - s) for s in grid)
    out["tests"]["C3_identity_max_abs_error"] = ident_err
    out["tests"]["C3_identity_when_p_train_equals_mean_score"] = ident_err < 1e-9

    # bounds/finiteness on all calibrators
    bounded = True
    finite = True
    for name, fit in (("C1_platt", {"params": platt}), ("C2_isotonic", {"knots": kn}),
                      ("C3_prior_offset", {"params": fit_prior(scores, ys)})):
        for s in grid:
            v = apply_calibrator(name, s, fit)
            if not (0.0 <= v <= 1.0):
                bounded = False
            if not math.isfinite(v):
                finite = False
    out["tests"]["all_outputs_finite"] = finite
    out["tests"]["all_outputs_in_unit_interval"] = bounded

    # ECE sanity on synthetic data
    e = ece_equal_count([apply_platt(s, platt) for s in scores], ys)
    out["tests"]["ece_synthetic_platt"] = e
    out["tests"]["ece_bin_guard_ok"] = e["n_bins"] >= 1

    ok = (out["tests"]["C1_monotone_nondecreasing_in_score"]
          and out["tests"]["C2_monotone_nondecreasing_in_score"]
          and out["tests"]["C3_identity_when_p_train_equals_mean_score"]
          and out["tests"]["all_outputs_finite"]
          and out["tests"]["all_outputs_in_unit_interval"])
    out["all_self_tests_pass"] = bool(ok)
    return out


def main():
    SESSION_DIR.mkdir(parents=True, exist_ok=True)
    res = run_self_tests()
    p = SESSION_DIR / f"fclr_risk07_calibrators_{UTC_STAMP}.json"
    p.write_text(json.dumps(res, indent=2), encoding="utf-8")
    print(f"wrote {p} pass={res['all_self_tests_pass']}")


if __name__ == "__main__":
    main()
