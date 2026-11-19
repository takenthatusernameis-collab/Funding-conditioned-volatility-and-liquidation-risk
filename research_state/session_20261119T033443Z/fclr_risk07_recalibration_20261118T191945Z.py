#!/usr/bin/env python3
"""FCLR-LIQ-RISK-RECALIBRATION-07 — train-only recalibration of modeled breach risk.

Campaign: FCLR-LIQ-RISK-RECALIBRATION-07-20261118T191714Z
Session:  session_20261118T191945Z

Reuses the verified RISK-06 modeled label matrix (262,080 rows) and rebuilds the
RV/funding features from cached 1h mark+funding files (2024-03..2024-09 only).
Stdlib only: math/json/random/zipfile/datetime/pathlib/statistics.

Design frozen in fclr_risk07_prereg_20261118T191945Z.json BEFORE evaluation:
  - base score B0_rv_only (IRLS logistic, lrv1/lrv24/lrv168, ridge 1e-6)
  - train-only calibrators C1 Platt / C2 PAVA isotonic / C3 prior offset, all
    fitted on 5 contiguous UTC-day-block out-of-fold train scores
  - primary scenario L10|long|H24, pooled equal-weight over 12 scenarios
  - Brier (primary) + ECE (10 equal-count bins, merge <30)
  - UTC-day block bootstrap (2000 Brier reps, 400 exact ECE reps)
  - 200-draw label-permutation placebo
  - cross-scenario transfer for C1/C3

Usage:
  python3 fclr_risk07_recalibration_<UTC>.py --holdout 2024-07 [--nperm N]
  python3 fclr_risk07_recalibration_<UTC>.py --assemble
"""
from __future__ import annotations

import argparse
import importlib.util
import json
import math
import random
import statistics
import zipfile
from datetime import datetime, timezone, timedelta
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
RS = REPO / "research_state"
CACHE = RS / "data_cache"
SESSION_DIR = RS / "session_20261118T191945Z"
UTC_STAMP = "20261118T191945Z"
PARENT_DIR = RS / "session_20261118T182813Z"
PARENT_STAMP = "20261118T182813Z"

SYMBOLS = ["BTCUSDT", "ETHUSDT", "SOLUSDT", "XRPUSDT", "BNBUSDT"]
SIDES = ["long", "short"]
FEATURE_MONTHS = ["2024-03", "2024-04", "2024-05", "2024-06", "2024-07", "2024-08", "2024-09"]
LEVERAGES = [5, 10, 20]
HORIZONS = [4, 24]
SCENARIOS = [f"L{lev}|{sd}|H{h}" for lev in LEVERAGES for sd in SIDES for h in HORIZONS]
PRIMARY_SCENARIO = "L10|long|H24"
SEED = 12345
BOOT_REPS = 2000
ECE_BOOT_REPS = 400
N_PERM = 200
RIDGE_LAMBDA = 1e-6
IRLS_MAX_ITERS = 100
IRLS_TOL = 1e-8
N_FOLDS = 5
RV_BLOCK = ["lrv1", "lrv24", "lrv168"]
FEATURE_NAMES = RV_BLOCK + ["fund", "fund_abs", "fmean", "fewma", "fund_shock", "fund_z"]

HOLDS = {
    "2024-07": {"train": ("2024-04-01", "2024-06-23"), "embargo": ("2024-06-24", "2024-06-30"),
                "test": ("2024-07-01", "2024-07-31")},
    "2024-08": {"train": ("2024-04-01", "2024-07-24"), "embargo": ("2024-07-25", "2024-07-31"),
                "test": ("2024-08-01", "2024-08-31")},
    "2024-09": {"train": ("2024-04-01", "2024-08-24"), "embargo": ("2024-08-25", "2024-08-31"),
                "test": ("2024-09-01", "2024-09-30")},
}
HOLD_ORDER = ["2024-07", "2024-08", "2024-09"]

# import the frozen calibrator implementation from this session
_spec = importlib.util.spec_from_file_location(
    "risk07_cal", SESSION_DIR / f"fclr_risk07_calibrators_{UTC_STAMP}.py")
_cal = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_cal)
sigmoid = _cal.sigmoid
logit = _cal.logit
fit_platt = _cal.fit_platt
apply_platt = _cal.apply_platt
fit_isotonic = _cal.fit_isotonic
apply_isotonic = _cal.apply_isotonic
fit_prior = _cal.fit_prior
apply_prior = _cal.apply_prior
fit_calibrator = _cal.fit_calibrator
apply_calibrator = _cal.apply_calibrator
ece_equal_count = _cal.ece_equal_count
CALIBRATORS = _cal.CALIBRATORS


# ---------------------------------------------------------------- cache readers
def dir_of(symbol, year_month):
    y, m = year_month.split("-")
    return f"{symbol}_{y}_{m}"


def read_mark_lines(symbol, year_month, day):
    base = CACHE / dir_of(symbol, year_month) / f"markPriceKlines-{day}"
    csv_name = f"{symbol}-1h-{day}.csv"
    p = base / csv_name
    if p.is_file():
        return p.read_text(encoding="utf-8", errors="ignore").splitlines()
    zp = base / f"{symbol}-1h-{day}.zip"
    if zp.is_file():
        with zipfile.ZipFile(zp) as z:
            return z.read(csv_name).decode("utf-8", errors="ignore").splitlines()
    return []


def read_funding_lines(symbol, year_month):
    base = CACHE / dir_of(symbol, year_month)
    csv_name = f"{symbol}-fundingRate-{year_month}.csv"
    p = base / csv_name
    if p.is_file():
        return p.read_text(encoding="utf-8", errors="ignore").splitlines()
    zp = base / f"{symbol}-fundingRate-{year_month}.zip"
    if zp.is_file():
        with zipfile.ZipFile(zp) as z:
            return z.read(csv_name).decode("utf-8", errors="ignore").splitlines()
    return []


def load_mark_series(symbol):
    rows = []
    for ym in FEATURE_MONTHS:
        y, m = ym.split("-")
        for d in range(1, 32):
            day = f"{y}-{int(m):02d}-{d:02d}"
            try:
                datetime.strptime(day, "%Y-%m-%d")
            except ValueError:
                continue
            lines = read_mark_lines(symbol, ym, day)
            if not lines:
                continue
            it = iter(lines)
            header = next(it, None)
            if header is None:
                continue
            cols = header.split(",")
            try:
                oi = cols.index("open_time")
                ci = cols.index("close")
            except ValueError:
                continue
            for line in it:
                p = line.split(",")
                if len(p) <= max(oi, ci):
                    continue
                try:
                    rows.append((int(p[oi]), float(p[ci])))
                except ValueError:
                    continue
    rows.sort(key=lambda x: x[0])
    out = []
    for ts, px in rows:
        if out and out[-1][0] == ts:
            continue
        out.append((ts, px))
    return out


def load_funding_series(symbol):
    rows = []
    for ym in FEATURE_MONTHS:
        lines = read_funding_lines(symbol, ym)
        if not lines:
            continue
        it = iter(lines)
        header = next(it, None)
        if header is None:
            continue
        cols = header.split(",")
        try:
            ti = cols.index("calc_time")
            ri = cols.index("last_funding_rate")
        except ValueError:
            continue
        for line in it:
            p = line.split(",")
            if len(p) <= max(ti, ri):
                continue
            try:
                rows.append((int(p[ti]), float(p[ri])))
            except ValueError:
                continue
    rows.sort(key=lambda x: x[0])
    out = []
    for ts, rate in rows:
        if out and out[-1][0] == ts:
            continue
        out.append((ts, rate))
    return out


def build_feature_map(symbol):
    marks = load_mark_series(symbol)
    funding = load_funding_series(symbol)
    n = len(marks)
    ret = [0.0] * n
    for i in range(1, n):
        if marks[i - 1][1] > 0 and marks[i][1] > 0:
            ret[i] = math.log(marks[i][1] / marks[i - 1][1])
    pref = [0.0] * (n + 1)
    for i in range(n):
        pref[i + 1] = pref[i] + ret[i] * ret[i]

    def trailing_rv(i, win):
        lo = max(0, i - win + 1)
        return pref[i + 1] - pref[lo]

    close_ms = [ts + 3_600_000 - 1 for ts, _ in marks]
    fi = 0
    obs = []
    obs_sum = 0.0
    obs_sq = 0.0
    ewma = None
    feat = {}
    for i in range(n):
        cm = close_ms[i]
        while fi < len(funding) and funding[fi][0] <= cm:
            r = funding[fi][1]
            obs.append(r)
            obs_sum += r
            obs_sq += r * r
            alpha = 2.0 / (min(len(obs), 168) + 1)
            ewma = r if ewma is None else alpha * r + (1.0 - alpha) * ewma
            fi += 1
        if fi == 0:
            continue
        rate = funding[fi - 1][1]
        cnt = len(obs)
        fmean = obs_sum / cnt if cnt else 0.0
        var = (obs_sq / cnt - fmean * fmean) if cnt else 0.0
        sd = math.sqrt(var) if var > 0 else 0.0
        fz = ((rate - fmean) / sd) if sd > 0 else 0.0
        feat[marks[i][0]] = (
            trailing_rv(i, 1), trailing_rv(i, 24), trailing_rv(i, 168),
            rate, abs(rate), fmean, ewma if ewma is not None else 0.0,
            abs(rate - (ewma if ewma is not None else 0.0)), fz,
        )
    return feat


# --------------------------------------------------------------- linear algebra
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


def irls_logistic(X, y, max_iters=IRLS_MAX_ITERS, tol=IRLS_TOL, init=None):
    n = len(X)
    p = len(X[0]) if n else 0
    beta = list(init) if init else [0.0] * p
    for _ in range(max_iters):
        eta = [0.0] * n
        for i in range(n):
            row = X[i]
            s = 0.0
            for j in range(p):
                s += row[j] * beta[j]
            eta[i] = s
        phat = [sigmoid(e) for e in eta]
        W = [phat[i] * (1.0 - phat[i]) for i in range(n)]
        XtWX = [[0.0] * p for _ in range(p)]
        XtWz = [0.0] * p
        for i in range(n):
            wi = W[i]
            if wi == 0.0:
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
            XtWX[j][j] += RIDGE_LAMBDA
        nb = solve_linear(XtWX, XtWz)
        if nb is None:
            return beta
        change = max(abs(nb[j] - beta[j]) for j in range(p))
        beta = nb
        if change < tol:
            break
    return beta


def brier(preds, ys):
    return sum((preds[i] - ys[i]) ** 2 for i in range(len(ys))) / len(ys)


def logloss(preds, ys):
    s = 0.0
    for i in range(len(ys)):
        p = min(1.0 - 1e-12, max(1e-12, preds[i]))
        s += -(ys[i] * math.log(p) + (1 - ys[i]) * math.log(1.0 - p))
    return s / len(ys)


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


# ------------------------------------------------------------------ utilities
def day_of(ts_ms):
    return datetime.fromtimestamp(ts_ms / 1000, tz=timezone.utc).strftime("%Y-%m-%d")


def date_set(a, b):
    out = set()
    cur = datetime.strptime(a, "%Y-%m-%d").date()
    end = datetime.strptime(b, "%Y-%m-%d").date()
    while cur <= end:
        out.add(cur.isoformat())
        cur += timedelta(days=1)
    return out


def day_block_bootstrap(diff_by_day, counts_by_day, seed, reps):
    days = sorted(diff_by_day)
    if not days:
        return None
    rng = random.Random(seed)
    means = []
    nd = len(days)
    for _ in range(reps):
        sd = 0.0
        sc = 0
        for _ in range(nd):
            d = days[rng.randrange(nd)]
            sd += diff_by_day[d]
            sc += counts_by_day[d]
        if sc:
            means.append(sd / sc)
    means.sort()
    return {
        "mean": sum(means) / len(means),
        "ci_lo": means[int(math.floor(0.025 * len(means)))],
        "ci_hi": means[int(math.ceil(0.975 * len(means))) - 1],
        "reps": len(means),
    }


def percentile(sorted_vals, q):
    if not sorted_vals:
        return None
    k = (len(sorted_vals) - 1) * q
    lo = int(math.floor(k))
    hi = int(math.ceil(k))
    if lo == hi:
        return sorted_vals[lo]
    return sorted_vals[lo] + (sorted_vals[hi] - sorted_vals[lo]) * (k - lo)


# ---------------------------------------------------------------- dataset build
def dataset_cache_path():
    return SESSION_DIR / f"fclr_risk07_dataset_{UTC_STAMP}.json"


def build_dataset():
    labels_path = PARENT_DIR / f"fclr_risk06_labels_{PARENT_STAMP}.json"
    lab = json.loads(labels_path.read_text(encoding="utf-8"))
    raw = lab["rows"]
    feat_maps = {s: build_feature_map(s) for s in SYMBOLS}
    rows = []
    feats = []
    key = {}
    n_no_feat = 0
    for r in raw:
        sym_idx, entry_ts, lev, side_idx, horizon, breached = r[0], r[1], r[2], r[3], r[4], r[5]
        symbol = SYMBOLS[sym_idx]
        f = feat_maps[symbol].get(entry_ts)
        if f is None:
            n_no_feat += 1
            continue
        sc = f"L{lev}|{SIDES[side_idx]}|H{horizon}"
        sc_i = SCENARIOS.index(sc)
        k = (sym_idx, entry_ts)
        fi = key.get(k)
        if fi is None:
            fi = len(feats)
            key[k] = fi
            feats.append(f)
        rows.append((fi, day_of(entry_ts), sc_i, 1 if breached == 1 else 0, sym_idx))
    payload = {
        "schema": "fclr_risk07_dataset_cache",
        "session": f"session_{UTC_STAMP}",
        "n_rows": len(rows),
        "n_rows_without_features": n_no_feat,
        "n_unique_feature_origins": len(feats),
        "feature_names": FEATURE_NAMES,
        "scenarios": SCENARIOS,
        "symbols": SYMBOLS,
        "feats": [[round(v, 12) for v in f] for f in feats],
        "rows": [list(r) for r in rows],
    }
    dataset_cache_path().write_text(json.dumps(payload), encoding="utf-8")
    return payload


def load_dataset():
    p = dataset_cache_path()
    if p.is_file() and p.stat().st_size > 0:
        d = json.loads(p.read_text(encoding="utf-8"))
        return d["rows"], d["feats"], d["n_rows_without_features"]
    d = build_dataset()
    return d["rows"], d["feats"], d["n_rows_without_features"]


# ------------------------------------------------------------------ base model
def fit_base(rows_idx, rows, feats):
    idxs = [rows[i][0] for i in rows_idx]
    stats = []
    for j in range(3):
        vals = [feats[k][j] for k in idxs]
        mu = sum(vals) / len(vals)
        var = sum((v - mu) ** 2 for v in vals) / len(vals)
        sd = math.sqrt(var) if var > 0 else 1.0
        stats.append((mu, sd))
    X = []
    y = []
    for i in rows_idx:
        f = feats[rows[i][0]]
        X.append([1.0] + [(f[j] - stats[j][0]) / stats[j][1] for j in range(3)])
        y.append(rows[i][3])
    beta = irls_logistic(X, y)
    return beta, stats


def predict(rows_idx, rows, feats, beta, stats):
    out = []
    for i in rows_idx:
        f = feats[rows[i][0]]
        z = beta[0]
        for j in range(3):
            z += beta[j + 1] * ((f[j] - stats[j][0]) / stats[j][1])
        out.append(sigmoid(z))
    return out


# --------------------------------------------------------------- holdout stage
def partial_path(holdout):
    return SESSION_DIR / f"fclr_risk07_partial_{holdout}_{UTC_STAMP}.json"


def run_holdout(holdout, n_perm=N_PERM):
    rows, feats, n_no_feat = load_dataset()
    hold = HOLDS[holdout]
    train_days = date_set(*hold["train"])
    test_days = date_set(*hold["test"])

    by_sc_train = {}
    by_sc_test = {}
    for i, r in enumerate(rows):
        d = r[1]
        if d in train_days:
            by_sc_train.setdefault(r[2], []).append(i)
        elif d in test_days:
            by_sc_test.setdefault(r[2], []).append(i)

    # 5 contiguous UTC-day-block OOF folds over the train window
    all_train_days = sorted({rows[i][1] for sc in by_sc_train for i in by_sc_train[sc]})
    nd = len(all_train_days)
    fold_of_day = {}
    for k, d in enumerate(all_train_days):
        fold_of_day[d] = min(N_FOLDS - 1, (k * N_FOLDS) // nd)

    results = {"holdout": holdout, "train": list(hold["train"]), "embargo": list(hold["embargo"]),
               "test": list(hold["test"]), "n_folds": N_FOLDS, "scenarios": {}}
    oof_store = {}
    test_store = {}

    for sc_i, sc in enumerate(SCENARIOS):
        tr = by_sc_train.get(sc_i, [])
        te = by_sc_test.get(sc_i, [])
        if not tr or not te:
            continue
        # out-of-fold scores
        s_oof = [0.0] * len(tr)
        fold_idx = [fold_of_day[rows[i][1]] for i in tr]
        for f in range(N_FOLDS):
            fit_rows = [tr[k] for k in range(len(tr)) if fold_idx[k] != f]
            pred_rows = [tr[k] for k in range(len(tr)) if fold_idx[k] == f]
            if not fit_rows or not pred_rows:
                continue
            beta, stats = fit_base(fit_rows, rows, feats)
            preds = predict(pred_rows, rows, feats, beta, stats)
            j = 0
            for k in range(len(tr)):
                if fold_idx[k] == f:
                    s_oof[k] = preds[j]
                    j += 1
        y_tr = [rows[i][3] for i in tr]

        # final base model on full train window -> test scores
        beta, stats = fit_base(tr, rows, feats)
        s_test = predict(te, rows, feats, beta, stats)
        y_te = [rows[i][3] for i in te]
        day_te = [rows[i][1] for i in te]

        fits = {}
        preds = {"C0_identity": s_test}
        for name in CALIBRATORS:
            if name == "C0_identity":
                fits[name] = {}
                continue
            fit = fit_calibrator(name, s_oof, y_tr)
            fits[name] = fit
            preds[name] = [apply_calibrator(name, s, fit) for s in s_test]

        sc_metrics = {"n": len(te), "n_pos": sum(y_te),
                      "breach_rate": sum(y_te) / len(y_te),
                      "models": {}}
        for name in CALIBRATORS:
            p = preds[name]
            e = ece_equal_count(p, y_te)
            sc_metrics["models"][name] = {
                "brier": brier(p, y_te),
                "log_loss": logloss(p, y_te),
                "auc": auc(p, y_te),
                "mean_predicted": sum(p) / len(p),
                "calibration_in_the_large": sum(p) / len(p) - sum(y_te) / len(y_te),
                "ece": e["ece"],
                "ece_n_bins": e["n_bins"],
                "ece_min_bin": e["min_bin_size"],
            }
            if name != "C0_identity":
                m = sc_metrics["models"][name]
                b0 = sc_metrics["models"]["C0_identity"]
                m["delta_brier"] = b0["brier"] - m["brier"]
                m["delta_ece"] = b0["ece"] - m["ece"]
                m["delta_log_loss"] = b0["log_loss"] - m["log_loss"]
        if sc == PRIMARY_SCENARIO:
            for name in CALIBRATORS:
                sc_metrics["models"][name]["reliability"] = _cal.reliability_fit(preds[name], y_te)

        results["scenarios"][sc] = {"metrics": sc_metrics,
                                    "calibrator_fits": fits,
                                    "base_model": {"beta": beta, "stats": stats}}
        oof_store[sc] = {"s": [round(v, 9) for v in s_oof], "y": y_tr,
                         "scenario": sc}
        test_store[sc] = {"y": y_te, "day": day_te, "s": [round(v, 9) for v in s_test],
                          "preds": {k: [round(v, 9) for v in preds[k]] for k in CALIBRATORS}}

    # ---------------- primary-scenario bootstrap (Brier + exact ECE)
    sc = PRIMARY_SCENARIO
    if sc in results["scenarios"]:
        te = by_sc_test[SCENARIOS.index(sc)]
        y_te = test_store[sc]["y"]
        days = test_store[sc]["day"]
        p0 = test_store[sc]["preds"]["C0_identity"]
        boot = {}
        for name in ("C1_platt", "C2_isotonic", "C3_prior_offset"):
            pm = test_store[sc]["preds"][name]
            diff, cnt = {}, {}
            by_day = {}
            for k in range(len(te)):
                d = days[k]
                ea = (p0[k] - y_te[k]) ** 2
                eb = (pm[k] - y_te[k]) ** 2
                diff[d] = diff.get(d, 0.0) + (ea - eb)
                cnt[d] = cnt.get(d, 0) + 1
                by_day.setdefault(d, ([], [], []))
                by_day[d][0].append(p0[k])
                by_day[d][1].append(pm[k])
                by_day[d][2].append(y_te[k])
            b = day_block_bootstrap(diff, cnt, SEED, BOOT_REPS)
            ece_b = ece_bootstrap(by_day, SEED, ECE_BOOT_REPS)
            boot[name] = {"brier_bootstrap": b, "ece_bootstrap": ece_b}
        results["primary_bootstrap"] = boot

    # ---------------- pooled equal-weight deltas
    pooled = {}
    for name in ("C1_platt", "C2_isotonic", "C3_prior_offset"):
        db = [results["scenarios"][s]["metrics"]["models"][name]["delta_brier"]
              for s in SCENARIOS if s in results["scenarios"]]
        de = [results["scenarios"][s]["metrics"]["models"][name]["delta_ece"]
              for s in SCENARIOS if s in results["scenarios"]]
        dl = [results["scenarios"][s]["metrics"]["models"][name]["delta_log_loss"]
              for s in SCENARIOS if s in results["scenarios"]]
        pooled[name] = {"mean_delta_brier": sum(db) / len(db),
                        "mean_delta_ece": sum(de) / len(de),
                        "mean_delta_log_loss": sum(dl) / len(dl),
                        "n_scenarios": len(db)}
    results["pooled"] = pooled

    # ---------------- cross-scenario transfer (C1/C3)
    transfer = {"mean_delta_brier_by_calibrator": {}, "sign_agreement": {}}
    for name in ("C1_platt", "C3_prior_offset"):
        vals = []
        agree = 0
        pairs = 0
        for a in SCENARIOS:
            if a not in oof_store:
                continue
            fit = fit_calibrator(name, oof_store[a]["s"], oof_store[a]["y"])
            for b in SCENARIOS:
                if b == a or b not in test_store:
                    continue
                pb = [apply_calibrator(name, s, fit) for s in test_store[b]["s"]]
                d = brier(test_store[b]["s"], test_store[b]["y"]) - brier(pb, test_store[b]["y"])
                vals.append(d)
                own = results["scenarios"][b]["metrics"]["models"][name]["delta_brier"]
                if (d > 0) == (own > 0):
                    agree += 1
                pairs += 1
        transfer["mean_delta_brier_by_calibrator"][name] = sum(vals) / len(vals) if vals else None
        transfer["sign_agreement"][name] = {"agree": agree, "pairs": pairs,
                                            "fraction": agree / pairs if pairs else None}
    results["transfer"] = transfer

    # ---------------- label-permutation placebo (per holdout)
    placebo = {}
    rng = random.Random(SEED)
    sc_avail = [s for s in SCENARIOS if s in oof_store and s in test_store]
    for name in ("C1_platt", "C2_isotonic", "C3_prior_offset"):
        pooled_null = []
        primary_null = []
        for _ in range(n_perm):
            per_sc = []
            for s in sc_avail:
                y_perm = list(oof_store[s]["y"])
                rng.shuffle(y_perm)
                fit = fit_calibrator(name, oof_store[s]["s"], y_perm)
                pb = [apply_calibrator(name, v, fit) for v in test_store[s]["s"]]
                d = brier(test_store[s]["s"], test_store[s]["y"]) - brier(pb, test_store[s]["y"])
                per_sc.append(d)
                if s == PRIMARY_SCENARIO:
                    primary_null.append(d)
            pooled_null.append(sum(per_sc) / len(per_sc))
        pooled_null.sort()
        primary_null.sort()
        placebo[name] = {
            "n_permutations": n_perm,
            "pooled_null_mean": sum(pooled_null) / len(pooled_null),
            "pooled_null_p95": percentile(pooled_null, 0.95),
            "primary_null_mean": (sum(primary_null) / len(primary_null)) if primary_null else None,
            "primary_null_p95": percentile(primary_null, 0.95),
        }
    results["placebo"] = placebo

    # ---------------- LOIO (evaluation-side) on primary scenario
    if sc in results["scenarios"]:
        te = by_sc_test[SCENARIOS.index(sc)]
        loio = {}
        for name in ("C1_platt", "C2_isotonic", "C3_prior_offset"):
            vals = {}
            for si, symbol in enumerate(SYMBOLS):
                keep = [k for k, i in enumerate(te) if rows[i][4] != si]
                if not keep:
                    continue
                y = [test_store[sc]["y"][k] for k in keep]
                p0 = [test_store[sc]["preds"]["C0_identity"][k] for k in keep]
                pm = [test_store[sc]["preds"][name][k] for k in keep]
                vals[symbol] = brier(p0, y) - brier(pm, y)
            loio[name] = vals
        results["loio_primary_eval_side"] = loio

    results["n_rows_without_features"] = n_no_feat
    partial_path(holdout).write_text(json.dumps(results, indent=1), encoding="utf-8")
    print(f"[{holdout}] wrote {partial_path(holdout)} pooled={ {k: round(v['mean_delta_brier'], 6) for k, v in pooled.items()} }")
    return results


def ece_bootstrap(by_day, seed, reps):
    days = sorted(by_day)
    rng = random.Random(seed)
    nd = len(days)
    diffs = []
    for _ in range(reps):
        p0, pm, y = [], [], []
        for _ in range(nd):
            d = days[rng.randrange(nd)]
            a, b, c = by_day[d]
            p0.extend(a)
            pm.extend(b)
            y.extend(c)
        e0 = ece_equal_count(p0, y)["ece"]
        em = ece_equal_count(pm, y)["ece"]
        diffs.append(e0 - em)
    diffs.sort()
    return {"mean": sum(diffs) / len(diffs),
            "ci_lo": diffs[int(math.floor(0.025 * len(diffs)))],
            "ci_hi": diffs[int(math.ceil(0.975 * len(diffs))) - 1],
            "reps": len(diffs)}


# -------------------------------------------------------------------- assemble
def assemble():
    holds = {}
    for h in HOLD_ORDER:
        p = partial_path(h)
        if not p.is_file():
            raise SystemExit(f"missing partial for {h}: {p}")
        holds[h] = json.loads(p.read_text(encoding="utf-8"))

    # verdict / materiality floor
    n_hits_brier = {}
    n_hits_ece = {}
    for name in ("C1_platt", "C2_isotonic", "C3_prior_offset"):
        nb = 0
        ne = 0
        for h in HOLD_ORDER:
            pr = holds[h].get("primary_bootstrap", {}).get(name)
            if not pr:
                continue
            if pr["brier_bootstrap"]["mean"] > 0 and pr["brier_bootstrap"]["ci_lo"] > 0:
                nb += 1
            if pr["ece_bootstrap"]["mean"] >= 0.005 and pr["ece_bootstrap"]["ci_lo"] >= 0.0:
                ne += 1
        n_hits_brier[name] = nb
        n_hits_ece[name] = ne

    real_pooled = {}
    for name in ("C1_platt", "C2_isotonic", "C3_prior_offset"):
        real_pooled[name] = sum(holds[h]["pooled"][name]["mean_delta_brier"] for h in HOLD_ORDER) / len(HOLD_ORDER)
    real_pooled_ece = {}
    for name in ("C1_platt", "C2_isotonic", "C3_prior_offset"):
        real_pooled_ece[name] = sum(holds[h]["pooled"][name]["mean_delta_ece"] for h in HOLD_ORDER) / len(HOLD_ORDER)

    floor_detail = {}
    for name in ("C1_platt", "C3_prior_offset"):
        placebo_p95 = sum(holds[h]["placebo"][name]["pooled_null_p95"] for h in HOLD_ORDER) / len(HOLD_ORDER)
        cd1 = n_hits_brier[name] >= 2
        cd2 = n_hits_ece[name] >= 2
        cd3 = real_pooled[name] > placebo_p95
        floor_detail[name] = {
            "delta_brier_significant_holdouts": n_hits_brier[name],
            "delta_ece_material_holdouts": n_hits_ece[name],
            "real_mean_delta_brier": real_pooled[name],
            "placebo_p95_mean": placebo_p95,
            "criterion_1_brier_2of3": cd1,
            "criterion_2_ece_2of3": cd2,
            "criterion_3_beats_placebo_p95": cd3,
            "floor_met": bool(cd1 and cd2 and cd3),
        }
    floor_met = any(v["floor_met"] for v in floor_detail.values())
    verdict = "MATERIALITY_FLOOR_MET" if floor_met else "HONEST_NEGATIVE_OR_INCONCLUSIVE"

    holds_out = {}
    for h in HOLD_ORDER:
        d = holds[h]
        holds_out[h] = {
            "n_folds": d["n_folds"],
            "n_rows_without_features": d["n_rows_without_features"],
            "scenarios": {sc: d["scenarios"][sc]["metrics"] for sc in d["scenarios"]},
            "calibrator_fits": {sc: d["scenarios"][sc]["calibrator_fits"] for sc in d["scenarios"]},
            "primary_bootstrap": d.get("primary_bootstrap", {}),
            "pooled": d["pooled"],
            "transfer": d["transfer"],
            "placebo": d["placebo"],
            "loio_primary_eval_side": d.get("loio_primary_eval_side", {}),
            "base_model_primary": d["scenarios"].get(PRIMARY_SCENARIO, {}).get("base_model"),
        }

    payload = {
        "schema": "fclr_risk07_recalibration",
        "campaign": "FCLR-LIQ-RISK-RECALIBRATION-07-20261118T191714Z",
        "session": f"session_{UTC_STAMP}",
        "timestamp_utc": UTC_STAMP,
        "label": "EXPLORATORY_PILOT",
        "outcome": "synthetic_modeled_boundary_breach (observed_liquidation_labels=false)",
        "network_used": False,
        "parquet_used": False,
        "numpy_used": False,
        "prereg": f"fclr_risk07_prereg_{UTC_STAMP}.json",
        "calibrators_module": f"fclr_risk07_calibrators_{UTC_STAMP}.py",
        "instruments": SYMBOLS,
        "scenarios": SCENARIOS,
        "primary_scenario": PRIMARY_SCENARIO,
        "design": {
            "base_score": "B0_rv_only IRLS logistic on lrv1,lrv24,lrv168, ridge 1e-6, train-only z-score",
            "oof": f"{N_FOLDS} contiguous UTC-day-block folds inside each train window",
            "calibrator_fit_data": "out-of-fold train scores only",
            "test_scores": "base model refit on the full train window",
            "bootstrap": {"method": "UTC-day block, percentile CI95", "seed": SEED,
                          "brier_reps": BOOT_REPS, "ece_reps": ECE_BOOT_REPS},
            "placebo": {"method": "label permutation within scenario after OOF scores",
                        "seed": SEED, "n_permutations": N_PERM},
            "loio": "evaluation-side: primary-scenario test rows of one instrument dropped (models not refit)",
        },
        "holdouts": holds_out,
        "floor_evaluation": {
            "delta_brier_significant_holdouts": n_hits_brier,
            "delta_ece_material_holdouts": n_hits_ece,
            "real_mean_delta_brier": real_pooled,
            "real_mean_delta_ece": real_pooled_ece,
            "details": floor_detail,
            "n_holdouts": len(HOLD_ORDER),
            "floor_met": floor_met,
            "rule": "C1 or C3: dBIER>0 with CI_lo>0 in >=2/3 holdouts on L10|long|H24; mean dECE>=0.005 in >=2/3; real mean dBrier > 95th pct of permutation null",
        },
        "verdict": verdict,
        "honest_status": (
            "EXPLORATORY/PILOT. Modeled boundary breaches only; not observed liquidations. "
            "Three chronological holdouts, 7-day purge/embargo; train-only recalibration on OOF scores; "
            "UTC-day block bootstrap; label-permutation placebo. No confirmatory claim."
        ),
    }
    out_json = SESSION_DIR / f"fclr_risk07_recalibration_{UTC_STAMP}.json"
    out_json.write_text(json.dumps(payload, indent=2), encoding="utf-8")

    md = render_md(payload)
    (SESSION_DIR / f"fclr_risk07_recalibration_{UTC_STAMP}.md").write_text(md, encoding="utf-8")
    print(f"wrote {out_json}")
    print(f"verdict={verdict} floor={floor_met} real={ {k: round(v, 6) for k, v in real_pooled.items()} }")
    return payload


def render_md(p):
    L = [
        "# FCLR-LIQ-RISK-RECALIBRATION-07 — Train-Only Recalibration of Modeled Breach Risk",
        "",
        f"**Session:** `session_{UTC_STAMP}`  ",
        "**Campaign:** `FCLR-LIQ-RISK-RECALIBRATION-07-20261118T191714Z`  ",
        "**Label:** EXPLORATORY/PILOT — **not confirmatory**.  ",
        "**Outcome:** `synthetic_modeled_boundary_breach`, `observed_liquidation_labels=false`.  ",
        "**Stdlib only**; no network; no parquet; no sealed months.",
        "",
        f"**Verdict:** `{p['verdict']}`",
        "",
        "## Materiality floor",
        "",
        "| Calibrator | ΔBrier sig. holdouts (of 3) | ΔECE≥0.005 holdouts (of 3) | real mean ΔBrier | placebo p95 | floor met |",
        "|---|---|---|---|---|---|",
    ]
    for k, v in p["floor_evaluation"]["details"].items():
        L.append(f"| {k} | {v['delta_brier_significant_holdouts']} | {v['delta_ece_material_holdouts']} | "
                 f"{v['real_mean_delta_brier']:.6f} | {v['placebo_p95_mean']:.6f} | {v['floor_met']} |")
    L += [
        "",
        "## Primary scenario `L10|long|H24` — ΔBrier / ΔECE vs uncalibrated base",
        "",
        "| Holdout | Calibrator | ΔBrier | CI95 | ΔECE | CI95 | Brier C0 | Brier Cm |",
        "|---|---|---|---|---|---|---|---|",
    ]
    for h in HOLD_ORDER:
        d = p["holdouts"][h]
        sc = d["scenarios"].get(PRIMARY_SCENARIO)
        if not sc:
            continue
        for name in ("C1_platt", "C2_isotonic", "C3_prior_offset"):
            bb = d["primary_bootstrap"].get(name, {}).get("brier_bootstrap") or {}
            eb = d["primary_bootstrap"].get(name, {}).get("ece_bootstrap") or {}
            m = sc["models"][name]
            L.append(f"| {h} | {name} | {m['delta_brier']:.6f} | "
                     f"[{bb.get('ci_lo', float('nan')):.6f}, {bb.get('ci_hi', float('nan')):.6f}] | "
                     f"{m['delta_ece']:.6f} | "
                     f"[{eb.get('ci_lo', float('nan')):.6f}, {eb.get('ci_hi', float('nan')):.6f}] | "
                     f"{sc['models']['C0_identity']['brier']:.6f} | {m['brier']:.6f} |")
    L += [
        "",
        "## Pooled equal-weight deltas over 12 scenarios (mean inside each holdout)",
        "",
        "| Holdout | Calibrator | mean ΔBrier | mean ΔECE | mean Δlogloss |",
        "|---|---|---|---|---|",
    ]
    for h in HOLD_ORDER:
        for name, v in p["holdouts"][h]["pooled"].items():
            L.append(f"| {h} | {name} | {v['mean_delta_brier']:.6f} | {v['mean_delta_ece']:.6f} | "
                     f"{v['mean_delta_log_loss']:.6f} |")
    L += [
        "",
        "## Label-permutation placebo (200 draws, mean over scenarios)",
        "",
        "| Holdout | Calibrator | real mean ΔBrier | null mean | null p95 |",
        "|---|---|---|---|---|",
    ]
    for h in HOLD_ORDER:
        d = p["holdouts"][h]
        for name in ("C1_platt", "C2_isotonic", "C3_prior_offset"):
            pl = d["placebo"][name]
            real = d["pooled"][name]["mean_delta_brier"]
            L.append(f"| {h} | {name} | {real:.6f} | {pl['pooled_null_mean']:.6f} | {pl['pooled_null_p95']:.6f} |")
    L += [
        "",
        "## Cross-scenario transfer (fit on A train OOF, apply to B test)",
        "",
        "| Holdout | Calibrator | mean ΔBrier over ordered pairs | sign agreement |",
        "|---|---|---|---|",
    ]
    for h in HOLD_ORDER:
        tr = p["holdouts"][h]["transfer"]
        for name in ("C1_platt", "C3_prior_offset"):
            v = tr["mean_delta_brier_by_calibrator"].get(name)
            a = tr["sign_agreement"].get(name, {})
            L.append(f"| {h} | {name} | {v:.6f} | {a.get('fraction')} |")
    L += [
        "",
        "## Honest status",
        "",
        p["honest_status"],
        "",
        "Calibration deciles / reliability diagnostics and per-scenario metrics are in the JSON.",
    ]
    return "\n".join(L) + "\n"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--holdout", choices=HOLD_ORDER)
    ap.add_argument("--nperm", type=int, default=N_PERM)
    ap.add_argument("--assemble", action="store_true")
    ap.add_argument("--dataset", action="store_true")
    args = ap.parse_args()
    if args.dataset:
        d = build_dataset()
        print(f"dataset rows={d['n_rows']} feats={d['n_unique_feature_origins']} no_feat={d['n_rows_without_features']}")
        return
    if args.assemble:
        assemble()
        return
    if args.holdout:
        run_holdout(args.holdout, args.nperm)
        return
    ap.error("choose --dataset, --holdout, or --assemble")


if __name__ == "__main__":
    main()
