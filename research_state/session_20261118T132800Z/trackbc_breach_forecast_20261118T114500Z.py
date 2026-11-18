#!/usr/bin/env python3
"""
Track B/C breach-forecast campaign — FCLR-VOL-LIQ-BREACH-FORECAST-03.
Joins Track C causal volatility/funding features (at origin t) with Track B
modeled liquidation-boundary-breach labels; tests whether funding-conditioned
features predict modeled breaches beyond an RV-only baseline.

Stdlib only: math/csv/json/zipfile/datetime/statistics/random. No numpy/pandas/scipy.
Read-only cache (ZIP/CSV dir twins under research_state/data_cache/), no network.
EXPLORATORY/PILOT — single labeled month (2024-04); no forecast-gate pass claim.
"""
from __future__ import annotations

import json
import math
import random
import zipfile
from datetime import datetime, timezone, timedelta
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
RS = REPO / "research_state"
CACHE = RS / "data_cache"
SESSION_DIR = RS / "session_20261118T114500Z"
UTC_STAMP = "20261118T114500Z"

SYMBOLS = ["BTCUSDT", "ETHUSDT", "SOLUSDT", "XRPUSDT", "BNBUSDT"]
MONTHS = ["2024-03", "2024-04"]          # March = history for trailing windows; April = labels/eval
LABEL_MONTH = "2024-04"
SEED = 12345
BOOT_REPS = 500
RIDGE_LAMBDA = 1e-6
IRLS_MAX_ITERS = 100
IRLS_TOL = 1e-8
ALERT_FRAC = 0.05                         # precision@k alert budget

RV1, RV24, RV168 = 1, 24, 168


def ms_of_ymd(y, m, d):
    return int(datetime(y, m, d, tzinfo=timezone.utc).timestamp() * 1000)


def dir_of(symbol, year_month):
    y, mm = year_month.split("-")
    return f"{symbol}_{y}_{mm}"


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
    for ym in MONTHS:
        y, m = ym.split("-")
        for d in range(1, 32):
            try:
                datetime(int(y), int(m), d)
            except ValueError:
                continue
            day = f"{y}-{int(m):02d}-{d:02d}"
            lines = read_mark_lines(symbol, ym, day)
            if not lines:
                continue
            it = iter(lines)
            header = next(it, None)
            if header is None:
                continue
            cols = header.split(",")
            try:
                oi = cols.index("open_time"); ci = cols.index("close")
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
    for ym in MONTHS:
        lines = read_funding_lines(symbol, ym)
        if not lines:
            continue
        it = iter(lines)
        header = next(it, None)
        if header is None:
            continue
        cols = header.split(",")
        try:
            ti = cols.index("calc_time"); ri = cols.index("last_funding_rate")
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


def build_panel(symbol):
    marks = load_mark_series(symbol)
    funding = load_funding_series(symbol)
    n = len(marks)
    ret = [0.0] * n
    for i in range(1, n):
        if marks[i - 1][1] > 0 and marks[i][1] > 0:
            ret[i] = math.log(marks[i][1] / marks[i - 1][1])
    close_ms = [ts + 3_600_000 - 1 for ts, _ in marks]
    fund_rate = [0.0] * n
    fund_abs = [0.0] * n
    fund_hist = []                          # (index, rate) strictly causal funding observations
    fi = 0                                  # pointer into funding (sorted)
    for i in range(n):
        cm = close_ms[i]
        while fi < len(funding) and funding[fi][0] <= cm:
            fi += 1
        if fi > 0:
            rate = funding[fi - 1][1]
            fund_rate[i] = rate
            fund_abs[i] = abs(rate)
            fund_hist.append((i, rate))
    # prefix sums of squared returns for O(1) trailing RV
    pref = [0.0] * (n + 1)
    for i in range(n):
        pref[i + 1] = pref[i] + ret[i] * ret[i]
    return {
        "symbol": symbol, "marks": marks, "ret": ret, "close_ms": close_ms,
        "fund_rate": fund_rate, "fund_abs": fund_abs, "fund_hist": fund_hist,
        "pref": pref, "n": n,
    }


def trailing_rv(pref, i, win):
    lo = max(0, i - win + 1)
    return pref[i + 1] - pref[lo]


def funding_trails(fund_hist, i):
    vals = []
    for (bi, r) in fund_hist:
        if bi >= i:
            break
        vals.append(r)
    mean = sum(vals) / len(vals) if vals else 0.0
    ewma = 0.0
    has = False
    alpha = 2.0 / (min(len(vals), 168) + 1) if vals else 0.0
    prev = 0.0
    for (bi, r) in fund_hist:
        if bi >= i:
            break
        if not has:
            ewma = r; prev = r; has = True
        else:
            ewma = alpha * r + (1.0 - alpha) * prev
            prev = ewma
    return mean, (ewma if has else 0.0), len(vals)


def sigmoid(z):
    if z >= 0:
        return 1.0 / (1.0 + math.exp(-z))
    ez = math.exp(z)
    return ez / (1.0 + ez)


def solve_linear(A, b):
    """Gaussian elimination with partial pivot; solves A x = b (A is p×p, small)."""
    p = len(A)
    aug = [list(A[r]) + [b[r]] for r in range(p)]
    for col in range(p):
        piv = max(range(col, p), key=lambda r: abs(aug[r][col]))
        if abs(aug[piv][col]) < 1e-14:
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
        piv = aug[r][r]
        if abs(piv) < 1e-14:
            return None
        x[r] = s / piv
    return x


def irls_logistic(X, y):
    """Fit logistic regression via IRLS with fixed ridge. Returns beta (no intercept column; X includes intercept if desired)."""
    n = len(X)
    p = len(X[0]) if n else 0
    beta = [0.0] * p
    for _ in range(IRLS_MAX_ITERS):
        # eta, p_hat, weights, working response
        eta = [0.0] * n
        for i in range(n):
            s = 0.0
            row = X[i]
            for j in range(p):
                s += row[j] * beta[j]
            eta[i] = s
        phat = [sigmoid(e) for e in eta]
        W = [phat[i] * (1.0 - phat[i]) for i in range(n)]
        z = [0.0] * n
        for i in range(n):
            wi = W[i]
            z[i] = eta[i] + (y[i] - phat[i]) / (wi if wi > 1e-12 else 1e-12)
        # weighted normal equations: (X' W X + lambda I) beta = X' W z
        XtWX = [[0.0] * p for _ in range(p)]
        XtWz = [0.0] * p
        for i in range(n):
            wi = W[i]
            if wi == 0.0:
                continue
            row = X[i]
            zi = z[i]
            wzi = wi * zi
            for j in range(p):
                vj = row[j]
                if vj == 0.0:
                    continue
                XtWz[j] += vj * wzi
                for k in range(p):
                    XtWX[j][k] += vj * row[k] * wi
        for j in range(p):
            XtWX[j][j] += RIDGE_LAMBDA
        new_beta = solve_linear(XtWX, XtWz)
        if new_beta is None:
            return beta
        change = max(abs(new_beta[j] - beta[j]) for j in range(p))
        beta = new_beta
        if change < IRLS_TOL:
            break
    return beta


def predict(X, beta):
    out = []
    for row in X:
        s = 0.0
        for j in range(len(row)):
            s += row[j] * beta[j]
        out.append(sigmoid(s))
    return out


def auc(scores, y):
    """Mann-Whitney U ROC-AUC with average ranks for ties."""
    n_pos = sum(1 for v in y if v == 1)
    n_neg = len(y) - n_pos
    if n_pos == 0 or n_neg == 0:
        return float("nan")
    order = sorted(range(len(scores)), key=lambda i: scores[i])
    ranks = [0.0] * len(scores)
    i = 0
    while i < len(order):
        j = i
        while j + 1 < len(order) and scores[order[j + 1]] == scores[order[i]]:
            j += 1
        avg_rank = (i + j) / 2.0 + 1.0
        for k in range(i, j + 1):
            ranks[order[k]] = avg_rank
        i = j + 1
    rank_pos_sum = sum(ranks[i] for i in range(len(y)) if y[i] == 1)
    u = rank_pos_sum - n_pos * (n_pos + 1) / 2.0
    return u / (n_pos * n_neg)


def brier(scores, y):
    return sum((scores[i] - y[i]) ** 2 for i in range(len(y))) / len(y)


def precision_at_k(scores, y, k):
    if k <= 0:
        return float("nan")
    order = sorted(range(len(scores)), key=lambda i: -scores[i])
    top = order[:k]
    return sum(y[i] for i in top) / len(top)


def calibration_bins(scores, y, nbins=10):
    order = sorted(range(len(scores)), key=lambda i: scores[i])
    n = len(scores)
    bin_size = max(1, n // nbins)
    bins = []
    for b in range(nbins):
        sl = order[b * bin_size:(b + 1) * bin_size] if b < nbins - 1 else order[b * bin_size:]
        if not sl:
            continue
        mp = sum(scores[i] for i in sl) / len(sl)
        mo = sum(y[i] for i in sl) / len(sl)
        bins.append((mp, mo, len(sl)))
    return bins


def split_by_date(rows, train_dates, test_dates):
    train_set = set(train_dates)
    test_set = set(test_dates)
    tr, te = [], []
    for r in rows:
        d = r["entry_date"]
        if d in train_set:
            tr.append(r)
        elif d in test_set:
            te.append(r)
    return tr, te


def extract_features(panel, i):
    fmean, fewma, fn = funding_trails(panel["fund_hist"], i)
    return {
        "lrv1": trailing_rv(panel["pref"], i, RV1),
        "lrv24": trailing_rv(panel["pref"], i, RV24),
        "lrv168": trailing_rv(panel["pref"], i, RV168),
        "fund": panel["fund_rate"][i],
        "fund_abs": panel["fund_abs"][i],
        "fmean": fmean,
        "fewma": fewma,
        "fund_n": float(fn),
    }


def standardize(train_rows, feature_names):
    stats = {}
    for name in feature_names:
        vals = [r["features"][name] for r in train_rows]
        mu = sum(vals) / len(vals)
        var = sum((v - mu) ** 2 for v in vals) / len(vals)
        sd = math.sqrt(var)
        if sd == 0.0:
            sd = 1.0
        stats[name] = (mu, sd)
    return stats


def apply_std(row, feature_names, stats):
    return [row["features"][name] if False else (row["features"][name] - stats[name][0]) / stats[name][1] for name in feature_names]


def model_matrix(rows, feature_names, stats, with_intercept):
    X = []
    y = []
    for r in rows:
        xrow = [1.0] if with_intercept else []
        for name in feature_names:
            v = r["features"][name]
            if v is None:
                xrow = None
                break
            xrow.append((v - stats[name][0]) / stats[name][1])
        if xrow is None:
            continue
        X.append(xrow)
        y.append(1 if r["breached"] == 1 else 0)
    return X, y


def evaluate_split(panels, origin_index, rows, feature_names, train_dates, test_dates):
    """Train on train_dates, evaluate on test_dates. Returns dict of metrics per model/scenario."""
    train_rows, test_rows = split_by_date(rows, train_dates, test_dates)
    if not train_rows or not test_rows:
        return None
    stats = standardize(train_rows, feature_names)
    Xtr, ytr = model_matrix(train_rows, feature_names, stats, True)
    Xte, yte = model_matrix(test_rows, feature_names, stats, True)
    if not Xtr or not Xte:
        return None
    RV_ONLY = ["lrv1", "lrv24", "lrv168"]
    FUND_COND = ["lrv1", "lrv24", "lrv168", "fund", "fund_abs", "fmean", "fewma"]
    stats_rv = standardize(train_rows, RV_ONLY)
    stats_fc = standardize(train_rows, FUND_COND)
    Xtr_rv, _ = model_matrix(train_rows, RV_ONLY, stats_rv, True)
    Xtr_fc, _ = model_matrix(train_rows, FUND_COND, stats_fc, True)
    Xte_rv, _ = model_matrix(test_rows, RV_ONLY, stats_rv, True)
    Xte_fc, _ = model_matrix(test_rows, FUND_COND, stats_fc, True)
    beta_rv = irls_logistic(Xtr_rv, ytr)
    beta_fc = irls_logistic(Xtr_fc, ytr)
    if beta_rv is None or beta_fc is None:
        return None
    # Need consistent stats for prediction: rebuild test matrices with chosen stats
    pred_rv = predict(Xte_rv, beta_rv)
    pred_fc = predict(Xte_fc, beta_fc)
    out = {
        "n_train": len(train_rows), "n_test": len(test_rows),
        "n_train_pos": sum(ytr), "n_test_pos": sum(yte),
        "test_breach_rate": sum(yte) / len(yte),
    }
    for tag, pred, beta in (("rv_only", pred_rv, beta_rv), ("fund_cond", pred_fc, beta_fc)):
        out[tag] = {
            "auc": auc(pred, yte),
            "brier": brier(pred, yte),
            "precision_at_k": precision_at_k(pred, yte, max(1, int(math.ceil(ALERT_FRAC * len(yte))))),
            "k": max(1, int(math.ceil(ALERT_FRAC * len(yte)))),
            "calibration": calibration_bins(pred, yte),
            "mean_pred": sum(pred) / len(pred),
        }
    out["delta_auc"] = out["fund_cond"]["auc"] - out["rv_only"]["auc"]
    out["delta_precision_at_k"] = out["fund_cond"]["precision_at_k"] - out["rv_only"]["precision_at_k"]
    return out


def evaluate_per_scenario(panels, origin_index, rows, feature_names, train_dates, test_dates):
    train_rows, test_rows = split_by_date(rows, train_dates, test_dates)
    if not train_rows or not test_rows:
        return {}
    stats_rv = standardize(train_rows, ["lrv1", "lrv24", "lrv168"])
    stats_fc = standardize(train_rows, ["lrv1", "lrv24", "lrv168", "fund", "fund_abs", "fmean", "fewma"])
    Xtr_rv, ytr = model_matrix(train_rows, ["lrv1", "lrv24", "lrv168"], stats_rv, True)
    Xtr_fc, _ = model_matrix(train_rows, ["lrv1", "lrv24", "lrv168", "fund", "fund_abs", "fmean", "fewma"], stats_fc, True)
    beta_rv = irls_logistic(Xtr_rv, ytr)
    beta_fc = irls_logistic(Xtr_fc, ytr)
    if beta_rv is None or beta_fc is None:
        return {}
    res = {}
    scenarios = sorted({(r["leverage"], r["side"], r["horizon_hours"]) for r in test_rows})
    for (lev, side, h) in scenarios:
        sub = [r for r in test_rows if r["leverage"] == lev and r["side"] == side and r["horizon_hours"] == h]
        if not sub:
            continue
        Xte_rv, ys = model_matrix(sub, ["lrv1", "lrv24", "lrv168"], stats_rv, True)
        Xte_fc, _ = model_matrix(sub, ["lrv1", "lrv24", "lrv168", "fund", "fund_abs", "fmean", "fewma"], stats_fc, True)
        if not Xte_rv or not Xte_fc:
            continue
        pr = predict(Xte_rv, beta_rv)
        pf = predict(Xte_fc, beta_fc)
        k = max(1, int(math.ceil(ALERT_FRAC * len(ys))))
        res[f"L{lev}|{side}|H{h}"] = {
            "n": len(ys), "n_pos": sum(ys), "breach_rate": sum(ys) / len(ys),
            "auc_rv": auc(pr, ys), "auc_fc": auc(pf, ys),
            "delta_auc": auc(pf, ys) - auc(pr, ys),
            "prec_rv": precision_at_k(pr, ys, k),
            "prec_fc": precision_at_k(pf, ys, k),
            "delta_prec": precision_at_k(pf, ys, k) - precision_at_k(pr, ys, k),
        }
    return res


def block_bootstrap_delta_auc(test_rows, feature_names, stats_rv, stats_fc, beta_rv, beta_fc, seed, reps):
    """Block bootstrap over UTC-day test blocks (fixed fitted models), percentile CI."""
    by_day = {}
    for r in test_rows:
        by_day.setdefault(r["entry_date"], []).append(r)
    days = sorted(by_day.keys())
    if not days:
        return None
    rng = random.Random(seed)
    reps_list = []
    for _ in range(reps):
        chosen = [rng.choice(days) for _ in days]
        samp = []
        for d in chosen:
            samp.extend(by_day[d])
        if not samp:
            continue
        Xte_rv, ys = model_matrix(samp, ["lrv1", "lrv24", "lrv168"], stats_rv, True)
        Xte_fc, _ = model_matrix(samp, ["lrv1", "lrv24", "lrv168", "fund", "fund_abs", "fmean", "fewma"], stats_fc, True)
        if not Xte_rv or not Xte_fc:
            continue
        pr = predict(Xte_rv, beta_rv)
        pf = predict(Xte_fc, beta_fc)
        reps_list.append(auc(pf, ys) - auc(pr, ys))
    if not reps_list:
        return None
    reps_list.sort()
    lo = reps_list[int(math.floor(0.025 * len(reps_list)))]
    hi = reps_list[int(math.ceil(0.975 * len(reps_list))) - 1]
    mean = sum(reps_list) / len(reps_list)
    return {"mean": mean, "ci_lo": lo, "ci_hi": hi, "reps": len(reps_list)}


def loio_delta_auc(rows, feature_names, train_dates, test_dates):
    train_rows, test_rows = split_by_date(rows, train_dates, test_dates)
    if not train_rows or not test_rows:
        return {}
    all_syms = sorted({r["symbol"] for r in train_rows})
    out = {}
    for leave in all_syms:
        tr = [r for r in train_rows if r["symbol"] != leave]
        te = [r for r in test_rows if r["symbol"] != leave]
        if not tr or not te:
            continue
        stats_rv = standardize(tr, ["lrv1", "lrv24", "lrv168"])
        stats_fc = standardize(tr, ["lrv1", "lrv24", "lrv168", "fund", "fund_abs", "fmean", "fewma"])
        Xtr_rv, ytr = model_matrix(tr, ["lrv1", "lrv24", "lrv168"], stats_rv, True)
        Xtr_fc, _ = model_matrix(tr, ["lrv1", "lrv24", "lrv168", "fund", "fund_abs", "fmean", "fewma"], stats_fc, True)
        beta_rv = irls_logistic(Xtr_rv, ytr)
        beta_fc = irls_logistic(Xtr_fc, ytr)
        if beta_rv is None or beta_fc is None:
            continue
        Xte_rv, yte = model_matrix(te, ["lrv1", "lrv24", "lrv168"], stats_rv, True)
        Xte_fc, _ = model_matrix(te, ["lrv1", "lrv24", "lrv168", "fund", "fund_abs", "fmean", "fewma"], stats_fc, True)
        if not Xte_rv or not Xte_fc:
            continue
        pr = predict(Xte_rv, beta_rv)
        pf = predict(Xte_fc, beta_fc)
        out[leave] = auc(pf, yte) - auc(pr, yte)
    return out


def main():
    panels = {s: build_panel(s) for s in SYMBOLS}
    mark_index = {s: {ts: i for i, (ts, _) in enumerate(panels[s]["marks"])} for s in SYMBOLS}

    # Load Track B labels (carried into this session dir).
    label_path = None
    for p in sorted(SESSION_DIR.glob("trackb_breach_labels_*.json")):
        label_path = p
        break
    if label_path is None:
        raise SystemExit("no trackb_breach_labels_*.json found in session dir")
    lb = json.loads(label_path.read_text(encoding="utf-8", errors="ignore"))
    raw_rows = lb.get("rows", [])

    # Build dataset: join causal features (at entry origin) to each breach label row.
    rows = []
    n_missing_origin = 0
    n_missing_feat = 0
    for r in raw_rows:
        symbol = r[0]
        entry_ts = r[1]
        leverage = r[2]
        side = r[3]
        horizon = r[4]
        breached = r[5]
        panel = panels[symbol]
        mi = mark_index[symbol].get(entry_ts)
        if mi is None:
            n_missing_origin += 1
            continue
        if mi < RV168:
            n_missing_feat += 1
            continue
        feats = extract_features(panel, mi)
        entry_date = datetime.fromtimestamp(entry_ts / 1000, tz=timezone.utc).strftime("%Y-%m-%d")
        rows.append({
            "symbol": symbol, "entry_ts": entry_ts, "entry_date": entry_date,
            "leverage": leverage, "side": side, "horizon_hours": horizon,
            "breached": breached, "features": feats,
        })

    feature_names = ["lrv1", "lrv24", "lrv168", "fund", "fund_abs", "fmean", "fewma"]

    splits = [
        {"split": 1, "train": ["2024-04-01", "2024-04-15"], "embargo": ["2024-04-16", "2024-04-22"], "test": ["2024-04-23", "2024-04-30"]},
        {"split": 2, "train": ["2024-04-01", "2024-04-17"], "embargo": ["2024-04-18", "2024-04-24"], "test": ["2024-04-25", "2024-04-30"]},
    ]

    def date_range(a, b):
        out = []
        cur = datetime.strptime(a, "%Y-%m-%d").date()
        end = datetime.strptime(b, "%Y-%m-%d").date()
        while cur <= end:
            out.append(cur.isoformat())
            cur += timedelta(days=1)
        return out

    split_results = []
    all_boot = []
    for sp in splits:
        train_dates = set(date_range(*sp["train"]))
        test_dates = set(date_range(*sp["test"]))
        res = evaluate_split(panels, mark_index, rows, feature_names, train_dates, test_dates)
        if res is None:
            continue
        per_scenario = evaluate_per_scenario(panels, mark_index, rows, feature_names, train_dates, test_dates)
        res["per_scenario"] = per_scenario
        # block bootstrap for delta AUC on this split's test set
        train_rows, test_rows = split_by_date(rows, train_dates, test_dates)
        stats_rv = standardize(train_rows, ["lrv1", "lrv24", "lrv168"])
        stats_fc = standardize(train_rows, ["lrv1", "lrv24", "lrv168", "fund", "fund_abs", "fmean", "fewma"])
        Xtr_rv, ytr = model_matrix(train_rows, ["lrv1", "lrv24", "lrv168"], stats_rv, True)
        Xtr_fc, _ = model_matrix(train_rows, ["lrv1", "lrv24", "lrv168", "fund", "fund_abs", "fmean", "fewma"], stats_fc, True)
        beta_rv = irls_logistic(Xtr_rv, ytr)
        beta_fc = irls_logistic(Xtr_fc, ytr)
        boot = None
        if beta_rv is not None and beta_fc is not None and test_rows:
            boot = block_bootstrap_delta_auc(test_rows, feature_names, stats_rv, stats_fc, beta_rv, beta_fc, SEED, BOOT_REPS)
        res["bootstrap_delta_auc"] = boot
        # LOIO
        res["loio_delta_auc"] = loio_delta_auc(rows, feature_names, train_dates, test_dates)
        res["train_dates"] = sp["train"]
        res["test_dates"] = sp["test"]
        res["embargo_dates"] = sp["embargo"]
        split_results.append(res)
        if boot is not None:
            all_boot.append(boot)

    # Pooled across splits (simple mean of split delta AUCs; bootstrap reps pooled)
    pooled_delta_auc = None
    if all_boot:
        pooled_reps = []
        for b in all_boot:
            # reuse each split's bootstrap reps as approximate pooled draws (labelled as such)
            pooled_reps.extend([b["mean"]] * max(1, b["reps"] // 10))
        pooled_delta_auc = {
            "mean_delta_auc": sum(s["delta_auc"] for s in split_results) / len(split_results),
            "n_splits": len(split_results),
            "note": "pooled mean of split-level Delta AUC; block-bootstrap CI per split reported above.",
        }

    out = {
        "schema": "trackbc_breach_forecast",
        "timestamp_utc": UTC_STAMP,
        "campaign": "FCLR-VOL-LIQ-BREACH-FORECAST-03-20261118T103106Z",
        "track": "BC_breach_forecast",
        "label": "EXPLORATORY_PILOT",
        "network_used": False,
        "parquet_used": False,
        "numpy_used": False,
        "prereg": "trackbc_breach_prereg_20261118T114500Z.json",
        "outcome": "synthetic_modeled_boundary_breach (observed_liquidation_labels=false)",
        "instruments": SYMBOLS,
        "label_month": LABEL_MONTH,
        "feature_cache_months": MONTHS,
        "features": feature_names,
        "model_family": "stdlib IRLS logistic, ridge lambda=1e-6, max 100 iters, tol 1e-8, seed 12345",
        "baseline": "RV_only [lrv1,lrv24,lrv168]",
        "candidate": "funding_conditioned [lrv1,lrv24,lrv168,fund,fund_abs,fmean,fewma]",
        "splits": splits,
        "n_dataset_rows": len(rows),
        "n_missing_origin": n_missing_origin,
        "n_missing_feat": n_missing_feat,
        "n_unique_entry_origins": len({(r["symbol"], r["entry_ts"]) for r in rows}),
        "overall_breach_rate": sum(r["breached"] for r in rows) / len(rows) if rows else None,
        "split_results": split_results,
        "pooled_delta_auc": pooled_delta_auc,
        "bootstrap_seed": SEED,
        "bootstrap_reps": BOOT_REPS,
        "alert_frac": ALERT_FRAC,
        "honest_status": "EXPLORATORY/PILOT. Single labeled month (2024-04); two chronological train/test splits; block-bootstrap (fixed fitted models); no confirmatory/forecast-gate claim.",
    }
    out_path = SESSION_DIR / f"trackbc_breach_forecast_{UTC_STAMP}.json"
    out_path.write_text(json.dumps(out, indent=2), encoding="utf-8")
    print(json.dumps({
        "n_rows": len(rows),
        "n_origins": out["n_unique_entry_origins"],
        "overall_breach_rate": out["overall_breach_rate"],
        "splits": [(s["split"], s["delta_auc"], s["bootstrap_delta_auc"]["mean"] if s["bootstrap_delta_auc"] else None) for s in split_results],
        "pooled": pooled_delta_auc,
    }, indent=2))


if __name__ == "__main__":
    main()
