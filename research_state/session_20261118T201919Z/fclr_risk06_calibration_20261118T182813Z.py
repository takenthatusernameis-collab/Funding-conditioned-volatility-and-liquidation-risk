#!/usr/bin/env python3
"""FCLR-LIQ-RISK-CALIBRATION-06 — out-of-sample breach-risk calibration (stdlib).

Campaign: FCLR-LIQ-RISK-CALIBRATION-06-20261118T182600Z
Session:  session_20261118T182813Z

Question: do funding-conditioned features improve out-of-sample probabilistic
calibration (Brier primary, log-loss secondary) of modeled liquidation-boundary
breach risk over RV-only, across three chronological holdouts, beyond a
funding-permutation placebo?

Inputs (read-only): fclr_risk06_labels_<UTC>.json in this session dir plus cached
1h mark-price + funding files under research_state/data_cache/ for 2024-03..2024-09.

Output: fclr_risk06_calibration_<UTC>.json / .md
Stdlib only: math/json/random/zipfile/datetime/pathlib. No network. No sealed months.
Label semantics: synthetic_modeled_boundary_breach; observed_liquidation_labels=false.
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
SESSION_DIR = RS / "session_20261118T182813Z"
UTC_STAMP = "20261118T182813Z"

SYMBOLS = ["BTCUSDT", "ETHUSDT", "SOLUSDT", "XRPUSDT", "BNBUSDT"]
SIDES = ["long", "short"]
FEATURE_MONTHS = ["2024-03", "2024-04", "2024-05", "2024-06", "2024-07", "2024-08", "2024-09"]
PRIMARY_SCENARIO = "L10|long|H24"
SEED = 12345
BOOT_REPS = 2000
RIDGE_LAMBDA = 1e-6
IRLS_MAX_ITERS = 100
IRLS_TOL = 1e-8

RV_BLOCK = ["lrv1", "lrv24", "lrv168"]
FUND_BLOCK = ["fund", "fund_abs", "fmean", "fewma"]
SHOCK_BLOCK = ["fund_shock", "fund_z"]
MODELS = {
    "B0_rv_only": RV_BLOCK,
    "B1_funding_conditioned": RV_BLOCK + FUND_BLOCK,
    "B2_funding_shock": RV_BLOCK + SHOCK_BLOCK,
}

HOLDS = [
    {"holdout": "2024-07", "train": ("2024-04-01", "2024-06-23"),
     "embargo": ("2024-06-24", "2024-06-30"), "test": ("2024-07-01", "2024-07-31")},
    {"holdout": "2024-08", "train": ("2024-04-01", "2024-07-24"),
     "embargo": ("2024-07-25", "2024-07-31"), "test": ("2024-08-01", "2024-08-31")},
    {"holdout": "2024-09", "train": ("2024-04-01", "2024-08-24"),
     "embargo": ("2024-08-25", "2024-08-31"), "test": ("2024-09-01", "2024-09-30")},
]


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


# ------------------------------------------------------------------ feature map
def build_feature_map(symbol):
    """Return {entry_open_time_ms: feature dict} for every bar with 168h history."""
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

    # Causal funding state at each bar close: last funding obs with calc_time <= close.
    fi = 0
    fund_rate = [0.0] * n
    # trailing funding statistics over obs strictly before i
    obs = []          # rates added so far
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
        fund_rate[i] = rate
        cnt = len(obs)
        fmean = obs_sum / cnt if cnt else 0.0
        var = (obs_sq / cnt - fmean * fmean) if cnt else 0.0
        sd = math.sqrt(var) if var > 0 else 0.0
        fz = ((rate - fmean) / sd) if sd > 0 else 0.0
        feat[marks[i][0]] = {
            "lrv1": trailing_rv(i, 1),
            "lrv24": trailing_rv(i, 24),
            "lrv168": trailing_rv(i, 168),
            "fund": rate,
            "fund_abs": abs(rate),
            "fmean": fmean,
            "fewma": ewma if ewma is not None else 0.0,
            "fund_shock": abs(rate - (ewma if ewma is not None else 0.0)),
            "fund_z": fz,
        }
    return feat


# --------------------------------------------------------------- linear algebra
def sigmoid(z):
    if z >= 0:
        return 1.0 / (1.0 + math.exp(-z))
    ez = math.exp(z)
    return ez / (1.0 + ez)


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
        piv = aug[r][r]
        if abs(piv) < 1e-12:
            return None
        x[r] = s / piv
    return x


def irls_logistic(X, y):
    n = len(X)
    p = len(X[0]) if n else 0
    beta = [0.0] * p
    for _ in range(IRLS_MAX_ITERS):
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
        new_beta = solve_linear(XtWX, XtWz)
        if new_beta is None:
            return beta
        change = max(abs(new_beta[j] - beta[j]) for j in range(p))
        beta = new_beta
        if change < IRLS_TOL:
            break
    return beta


def predict_row(row, beta):
    s = 0.0
    for j in range(len(row)):
        s += row[j] * beta[j]
    return sigmoid(s)


# -------------------------------------------------------------------- metrics
def brier(preds, ys):
    return sum((preds[i] - ys[i]) ** 2 for i in range(len(ys))) / len(ys)


def logloss(preds, ys):
    eps = 1e-12
    s = 0.0
    for i in range(len(ys)):
        p = min(1.0 - eps, max(eps, preds[i]))
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
        avg_rank = (i + j) / 2.0 + 1.0
        for k in range(i, j + 1):
            ranks[order[k]] = avg_rank
        i = j + 1
    rank_pos_sum = sum(ranks[i] for i in range(len(y)) if y[i] == 1)
    u = rank_pos_sum - n_pos * (n_pos + 1) / 2.0
    return u / (n_pos * n_neg)


def decile_table(preds, ys, nbins=10):
    order = sorted(range(len(preds)), key=lambda i: preds[i])
    n = len(order)
    out = []
    for b in range(nbins):
        lo = b * n // nbins
        hi = (b + 1) * n // nbins
        sl = order[lo:hi]
        if not sl:
            continue
        mp = sum(preds[i] for i in sl) / len(sl)
        mo = sum(ys[i] for i in sl) / len(sl)
        out.append({"decile": b + 1, "n": len(sl), "mean_predicted": mp, "observed_rate": mo})
    return out


# --------------------------------------------------------------- design matrix
def standardize(rows, names):
    stats = {}
    for name in names:
        vals = [r["f"][name] for r in rows]
        mu = sum(vals) / len(vals)
        var = sum((v - mu) ** 2 for v in vals) / len(vals)
        sd = math.sqrt(var) if var > 0 else 1.0
        stats[name] = (mu, sd)
    return stats


def design(rows, names, stats):
    X = []
    y = []
    for r in rows:
        xrow = [1.0]
        for name in names:
            mu, sd = stats[name]
            xrow.append((r["f"][name] - mu) / sd)
        X.append(xrow)
        y.append(r["y"])
    return X, y


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
    """Percentile CI95 for mean per-row difference, resampling UTC days with replacement."""
    days = sorted(diff_by_day)
    if not days:
        return None
    rng = random.Random(seed)
    means = []
    for _ in range(reps):
        sd = 0.0
        sc = 0
        for _ in days:
            d = rng.choice(days)
            sd += diff_by_day[d]
            sc += counts_by_day[d]
        if sc:
            means.append(sd / sc)
    if not means:
        return None
    means.sort()
    lo = means[int(math.floor(0.025 * len(means)))]
    hi = means[int(math.ceil(0.975 * len(means))) - 1]
    return {"mean": sum(means) / len(means), "ci_lo": lo, "ci_hi": hi, "reps": len(means)}


def accumulate_day_stats(rows, pred_a, pred_b):
    """diff per row = err_A - err_B (Brier) where err = (p - y)^2."""
    diff = {}
    cnt = {}
    for i, r in enumerate(rows):
        d = r["day"]
        ea = (pred_a[i] - r["y"]) ** 2
        eb = (pred_b[i] - r["y"]) ** 2
        diff[d] = diff.get(d, 0.0) + (ea - eb)
        cnt[d] = cnt.get(d, 0) + 1
    return diff, cnt


def accumulate_logloss_day_stats(rows, pred_a, pred_b):
    eps = 1e-12
    diff = {}
    cnt = {}
    for i, r in enumerate(rows):
        d = r["day"]
        pa = min(1.0 - eps, max(eps, pred_a[i]))
        pb = min(1.0 - eps, max(eps, pred_b[i]))
        la = -(rows[i]["y"] * math.log(pa) + (1 - rows[i]["y"]) * math.log(1.0 - pa))
        lb = -(rows[i]["y"] * math.log(pb) + (1 - rows[i]["y"]) * math.log(1.0 - pb))
        diff[d] = diff.get(d, 0.0) + (la - lb)
        cnt[d] = cnt.get(d, 0) + 1
    return diff, cnt


# ------------------------------------------------------------------------ main
def main():
    labels_path = SESSION_DIR / f"fclr_risk06_labels_{UTC_STAMP}.json"
    lab = json.loads(labels_path.read_text(encoding="utf-8"))
    raw = lab["rows"]

    feat_maps = {s: build_feature_map(s) for s in SYMBOLS}

    dataset = []
    n_no_feat = 0
    for r in raw:
        sym_idx, entry_ts, lev, side_idx, horizon, breached = r[0], r[1], r[2], r[3], r[4], r[5]
        symbol = SYMBOLS[sym_idx]
        f = feat_maps[symbol].get(entry_ts)
        if f is None:
            n_no_feat += 1
            continue
        dataset.append({
            "symbol": symbol, "ts": entry_ts, "day": day_of(entry_ts),
            "scenario": f"L{lev}|{SIDES[side_idx]}|H{horizon}",
            "y": 1 if breached == 1 else 0, "f": f,
        })

    scenarios = sorted({r["scenario"] for r in dataset})

    # ---- placebo: permute funding features across origins, per symbol (deterministic)
    perm_map = {}
    rng = random.Random(SEED)
    for symbol in SYMBOLS:
        idxs = [i for i, r in enumerate(dataset) if r["symbol"] == symbol]
        donors = list(idxs)
        rng.shuffle(donors)
        for i, j in zip(idxs, donors):
            perm_map[i] = dataset[j]["f"]

    def funding_features_for(idx, row):
        return perm_map[idx] if idx in perm_map else row["f"]

    results = []
    for hold in HOLDS:
        train_dates = date_set(*hold["train"])
        test_dates = date_set(*hold["test"])
        train_idx = [i for i, r in enumerate(dataset) if r["day"] in train_dates]
        test_idx = [i for i, r in enumerate(dataset) if r["day"] in test_dates]

        # Fit per-scenario models
        fitted = {}
        for sc in scenarios:
            tr = [dataset[i] for i in train_idx if dataset[i]["scenario"] == sc]
            if not tr:
                continue
            per_model = {}
            for mname, names in MODELS.items():
                stats = standardize(tr, names)
                X, y = design(tr, names, stats)
                beta = irls_logistic(X, y)
                per_model[mname] = {"beta": beta, "stats": stats, "names": names}
            fitted[sc] = per_model

        # Placebo fits (B1/B2 on permuted funding features; B0 identical -> reuse)
        fitted_placebo = {}
        for sc in scenarios:
            tr = [dataset[i] for i in train_idx if dataset[i]["scenario"] == sc]
            if not tr:
                continue
            tr_perm = []
            for i in train_idx:
                r = dataset[i]
                if r["scenario"] != sc:
                    continue
                g = funding_features_for(i, r)
                tr_perm.append({"f": g, "y": r["y"]})
            pm = {}
            for mname in ("B1_funding_conditioned", "B2_funding_shock"):
                names = MODELS[mname]
                stats = standardize(tr_perm, names)
                X, y = design(tr_perm, names, stats)
                pm[mname] = {"beta": irls_logistic(X, y), "stats": stats, "names": names}
            fitted_placebo[sc] = pm

        # Predict + score, per scenario
        sc_stats = {}
        per_row_preds = {}     # scenario -> {model: {idx: pred}}
        for sc in scenarios:
            te_idx = [i for i in test_idx if dataset[i]["scenario"] == sc]
            if not te_idx or sc not in fitted:
                continue
            te = [dataset[i] for i in te_idx]
            ys = [r["y"] for r in te]
            preds = {}
            for mname, fit in fitted[sc].items():
                X, _ = design(te, fit["names"], fit["stats"])
                preds[mname] = [predict_row(X[k], fit["beta"]) for k in range(len(X))]
            preds_placebo = {}
            for mname, fit in fitted_placebo.get(sc, {}).items():
                te_perm = [{"f": funding_features_for(i, dataset[i]), "y": dataset[i]["y"]} for i in te_idx]
                X, _ = design(te_perm, fit["names"], fit["stats"])
                preds_placebo[mname] = [predict_row(X[k], fit["beta"]) for k in range(len(X))]
            per_row_preds[sc] = preds
            entry = {
                "n": len(ys), "n_pos": sum(ys),
                "breach_rate": sum(ys) / len(ys) if ys else None,
            }
            for mname in MODELS:
                if mname not in preds:
                    continue
                entry[mname] = {
                    "brier": brier(preds[mname], ys),
                    "log_loss": logloss(preds[mname], ys),
                    "auc": auc(preds[mname], ys),
                    "mean_predicted": sum(preds[mname]) / len(preds[mname]),
                }
            for mname in ("B1_funding_conditioned", "B2_funding_shock"):
                if mname in preds and mname in preds_placebo:
                    entry[mname]["placebo_brier"] = brier(preds_placebo[mname], ys)
                    entry[mname]["placebo_log_loss"] = logloss(preds_placebo[mname], ys)
            for mname in ("B1_funding_conditioned", "B2_funding_shock"):
                if mname in entry:
                    entry[mname]["delta_brier_vs_B0"] = entry["B0_rv_only"]["brier"] - entry[mname]["brier"]
                    entry[mname]["delta_logloss_vs_B0"] = entry["B0_rv_only"]["log_loss"] - entry[mname]["log_loss"]
                    if "placebo_brier" in entry[mname]:
                        entry[mname]["delta_brier_placebo_vs_B0"] = (
                            entry["B0_rv_only"]["brier"] - entry[mname]["placebo_brier"])
            sc_stats[sc] = entry

        # Primary scenario with bootstrap + deciles
        primary = {"scenario": PRIMARY_SCENARIO}
        if PRIMARY_SCENARIO in sc_stats:
            te_idx = [i for i in test_idx if dataset[i]["scenario"] == PRIMARY_SCENARIO]
            te = [dataset[i] for i in te_idx]
            ys = [r["y"] for r in te]
            p0 = per_row_preds[PRIMARY_SCENARIO]["B0_rv_only"]
            for mname in ("B1_funding_conditioned", "B2_funding_shock"):
                pm = per_row_preds[PRIMARY_SCENARIO][mname]
                diff, cnt = accumulate_day_stats(te, p0, pm)
                primary[mname] = {
                    "delta_brier": sc_stats[PRIMARY_SCENARIO][mname]["delta_brier_vs_B0"],
                    "bootstrap": day_block_bootstrap(diff, cnt, SEED, BOOT_REPS),
                }
                ldiff, lcnt = accumulate_logloss_day_stats(te, p0, pm)
                primary[mname]["bootstrap_logloss"] = day_block_bootstrap(ldiff, lcnt, SEED, BOOT_REPS)
            # calibration deciles for best model (lowest Brier)
            best = min(("B0_rv_only", "B1_funding_conditioned", "B2_funding_shock"),
                       key=lambda m: sc_stats[PRIMARY_SCENARIO][m]["brier"])
            primary["best_model"] = best
            primary["calibration_deciles"] = decile_table(per_row_preds[PRIMARY_SCENARIO][best], ys)

        # Pooled equal-weight ΔBrier over all 12 scenarios
        pooled = {}
        for mname in ("B1_funding_conditioned", "B2_funding_shock"):
            vals = [sc_stats[sc][mname]["delta_brier_vs_B0"] for sc in scenarios
                    if sc in sc_stats and mname in sc_stats[sc] and "delta_brier_vs_B0" in sc_stats[sc][mname]]
            pvals = [sc_stats[sc][mname]["delta_brier_placebo_vs_B0"] for sc in scenarios
                     if sc in sc_stats and mname in sc_stats[sc] and "delta_brier_placebo_vs_B0" in sc_stats[sc][mname]]
            if vals:
                pooled[mname] = {
                    "mean_delta_brier": sum(vals) / len(vals),
                    "n_scenarios": len(vals),
                    "mean_delta_brier_placebo": (sum(pvals) / len(pvals)) if pvals else None,
                }
        # pooled bootstrap (row-level with scenario weights = 1/12 folded into diff): use mean of scenario means
        pooled_boot = {}
        for mname in ("B1_funding_conditioned", "B2_funding_shock"):
            diff = {}
            cnt = {}
            for sc in scenarios:
                if sc not in sc_stats or mname not in per_row_preds.get(sc, {}):
                    continue
                te_idx = [i for i in test_idx if dataset[i]["scenario"] == sc]
                te = [dataset[i] for i in te_idx]
                d, c = accumulate_day_stats(te, per_row_preds[sc]["B0_rv_only"], per_row_preds[sc][mname])
                ns = len(scenarios)
                for k in d:
                    diff[k] = diff.get(k, 0.0) + d[k] / ns
                    cnt[k] = cnt.get(k, 0) + c[k] / ns
            pooled_boot[mname] = day_block_bootstrap(diff, cnt, SEED, BOOT_REPS)
        pooled["bootstrap"] = pooled_boot

        # LOIO on primary scenario
        loio = {}
        for mname in ("B1_funding_conditioned", "B2_funding_shock"):
            vals = {}
            for leave in SYMBOLS:
                tr = [dataset[i] for i in train_idx
                      if dataset[i]["scenario"] == PRIMARY_SCENARIO and dataset[i]["symbol"] != leave]
                te = [dataset[i] for i in test_idx
                      if dataset[i]["scenario"] == PRIMARY_SCENARIO and dataset[i]["symbol"] != leave]
                if not tr or not te:
                    continue
                names = MODELS[mname]
                stats0 = standardize(tr, RV_BLOCK)
                X0, y0 = design(tr, RV_BLOCK, stats0)
                b0 = irls_logistic(X0, y0)
                stats1 = standardize(tr, names)
                X1, _ = design(tr, names, stats1)
                b1 = irls_logistic(X1, y0)
                if b0 is None or b1 is None:
                    continue
                X0t, yt = design(te, RV_BLOCK, stats0)
                X1t, _ = design(te, names, stats1)
                p0 = [predict_row(row, b0) for row in X0t]
                p1 = [predict_row(row, b1) for row in X1t]
                vals[leave] = brier(p0, yt) - brier(p1, yt)
            loio[mname] = vals

        results.append({
            "holdout": hold["holdout"],
            "train": list(hold["train"]), "embargo": list(hold["embargo"]), "test": list(hold["test"]),
            "n_train_rows": len(train_idx), "n_test_rows": len(test_idx),
            "n_train_pos": sum(dataset[i]["y"] for i in train_idx),
            "n_test_pos": sum(dataset[i]["y"] for i in test_idx),
            "scenario_metrics": sc_stats,
            "primary": primary,
            "pooled": pooled,
            "loio_primary": loio,
        })

    # ------------------------------------------------------------ verdict
    primary_rows = [(r["holdout"], r["primary"]) for r in results]
    beat_counts = {}
    for mname in ("B1_funding_conditioned", "B2_funding_shock"):
        n_hits = 0
        for holdout, pr in primary_rows:
            info = pr.get(mname)
            if not info or not info.get("bootstrap"):
                continue
            if info["delta_brier"] > 0 and info["bootstrap"]["ci_lo"] > 0:
                n_hits += 1
        beat_counts[mname] = n_hits
    real_mean = {m: sum(r["primary"][m]["delta_brier"] for r in results
                        if m in r["primary"]) / len(results)
                 for m in ("B1_funding_conditioned", "B2_funding_shock")}
    placebo_mean = {}
    for m in ("B1_funding_conditioned", "B2_funding_shock"):
        vals = [r["primary"][m]["bootstrap"]["mean"] for r in results
                if m in r["primary"] and r["primary"][m].get("bootstrap")]
        placebo_mean[m] = None
    # placebo mean from scenario-level placebo brier diffs
    for m in ("B1_funding_conditioned", "B2_funding_shock"):
        vals = []
        for r in results:
            v = r["pooled"].get(m, {}).get("mean_delta_brier_placebo")
            if v is not None:
                vals.append(v)
        placebo_mean[m] = (sum(vals) / len(vals)) if vals else None

    floor_met = False
    for m in ("B1_funding_conditioned", "B2_funding_shock"):
        if beat_counts[m] >= 2 and placebo_mean[m] is not None and abs(real_mean[m]) > abs(placebo_mean[m]):
            floor_met = True

    payload = {
        "schema": "fclr_risk06_calibration",
        "campaign": "FCLR-LIQ-RISK-CALIBRATION-06-20261118T182600Z",
        "session": f"session_{UTC_STAMP}",
        "timestamp_utc": UTC_STAMP,
        "label": "EXPLORATORY_PILOT",
        "network_used": False,
        "parquet_used": False,
        "numpy_used": False,
        "outcome": "synthetic_modeled_boundary_breach (observed_liquidation_labels=false)",
        "prereg": f"fclr_risk06_prereg_{UTC_STAMP}.json",
        "instruments": SYMBOLS,
        "feature_cache_months": FEATURE_MONTHS,
        "scenarios": scenarios,
        "models": {k: v for k, v in MODELS.items()},
        "primary_scenario": PRIMARY_SCENARIO,
        "estimation": {"family": "stdlib IRLS logistic", "ridge_lambda": RIDGE_LAMBDA,
                       "max_iters": IRLS_MAX_ITERS, "tol": IRLS_TOL, "seed": SEED},
        "bootstrap": {"method": "UTC-day block, percentile CI95", "seed": SEED, "reps": BOOT_REPS},
        "placebo": {"method": "funding features permuted across entry origins per symbol, identical pipeline",
                    "seed": SEED},
        "fit_scope": "per-scenario models; pooled = equal-weight mean of per-scenario delta_brier",
        "n_dataset_rows": len(dataset),
        "n_rows_without_features": n_no_feat,
        "n_unique_origins": len({(r["symbol"], r["ts"]) for r in dataset}),
        "overall_breach_rate": (sum(r["y"] for r in dataset) / len(dataset)) if dataset else None,
        "holdouts": results,
        "floor_evaluation": {
            "beats_B0_by_holdout_primary": beat_counts,
            "real_mean_delta_brier_primary": real_mean,
            "placebo_mean_delta_brier_pooled": placebo_mean,
            "n_holdouts": len(results),
            "floor_met": floor_met,
            "rule": "B1 or B2 beats B0 (delta_brier>0, CI95 lower>0) in >=2/3 holdouts on L10|long|H24 AND |real mean| > |placebo mean|",
        },
        "verdict": (
            "MATERIALITY_FLOOR_MET" if floor_met else "HONEST_NEGATIVE_OR_INCONCLUSIVE"
        ),
        "honest_status": (
            "EXPLORATORY/PILOT. Modeled boundary breaches only; not observed liquidations. "
            "Three chronological holdouts with 7-day purge/embargo; stdlib per-scenario logistic; "
            "UTC-day block bootstrap; funding-permutation placebo. No confirmatory claim."
        ),
    }
    (SESSION_DIR / f"fclr_risk06_calibration_{UTC_STAMP}.json").write_text(
        json.dumps(payload, indent=2), encoding="utf-8")

    # ------------------------------------------------------------- markdown
    md = [
        "# FCLR-LIQ-RISK-CALIBRATION-06 — Out-of-Sample Breach-Risk Calibration",
        "",
        f"**Session:** `session_{UTC_STAMP}`  ",
        f"**Campaign:** `FCLR-LIQ-RISK-CALIBRATION-06-20261118T182600Z`  ",
        "**Label:** EXPLORATORY/PILOT — **not confirmatory**.  ",
        "**Outcome:** `synthetic_modeled_boundary_breach`, `observed_liquidation_labels=false`.  ",
        "**Stdlib only**; no network; no parquet; no sealed months.",
        "",
        f"**Verdict:** `{payload['verdict']}`",
        "",
        "## Dataset",
        f"- Rows: {payload['n_dataset_rows']} (unique origins {payload['n_unique_origins']}); "
        f"overall breach rate {payload['overall_breach_rate']}",
        f"- Rows without features: {n_no_feat}",
        "",
        "## Primary scenario `L10|long|H24` — ΔBrier vs B0 (positive = funding better)",
        "",
        "| Holdout | Model | ΔBrier | CI95 | Δlogloss | CI95 |",
        "|---|---|---|---|---|---|",
    ]
    for r in results:
        pr = r["primary"]
        for m in ("B1_funding_conditioned", "B2_funding_shock"):
            if m not in pr:
                continue
            b = pr[m].get("bootstrap") or {}
            lb = pr[m].get("bootstrap_logloss") or {}
            md.append(
                f"| {r['holdout']} | {m} | {pr[m]['delta_brier']:.4f} | "
                f"[{b.get('ci_lo')}, {b.get('ci_hi')}] | "
                f"{-(lb.get('mean') or 0.0):.4f} | "
                f"[{lb.get('ci_lo')}, {lb.get('ci_hi')}] |"
            )
    md += [
        "",
        "## Pooled equal-weight ΔBrier over 12 scenarios",
        "",
        "| Holdout | Model | mean ΔBrier | CI95 | placebo mean ΔBrier |",
        "|---|---|---|---|---|",
    ]
    for r in results:
        for m in ("B1_funding_conditioned", "B2_funding_shock"):
            p = r["pooled"].get(m)
            if not p:
                continue
            b = (r["pooled"].get("bootstrap") or {}).get(m) or {}
            md.append(
                f"| {r['holdout']} | {m} | {p['mean_delta_brier']:.4f} | "
                f"[{b.get('ci_lo')}, {b.get('ci_hi')}] | {p['mean_delta_brier_placebo']} |"
            )
    md += [
        "",
        "## Materiality floor",
        f"- Holdouts where B1 beats B0 (Δ>0, CI lo>0): **{beat_counts['B1_funding_conditioned']}/{len(results)}**",
        f"- Holdouts where B2 beats B0 (Δ>0, CI lo>0): **{beat_counts['B2_funding_shock']}/{len(results)}**",
        f"- Real mean ΔBrier: B1 {real_mean['B1_funding_conditioned']:.4f}, B2 {real_mean['B2_funding_shock']:.4f}",
        f"- Placebo mean ΔBrier: B1 {placebo_mean['B1_funding_conditioned']}, B2 {placebo_mean['B2_funding_shock']}",
        f"- **floor_met = {floor_met}**",
        "",
        "## Calibration deciles (best model, primary scenario, per holdout)",
        "",
    ]
    for r in results:
        pr = r["primary"]
        if "calibration_deciles" not in pr:
            continue
        md.append(f"### {r['holdout']} — best model `{pr['best_model']}`")
        md.append("")
        md.append("| decile | n | mean_predicted | observed_rate |")
        md.append("|---|---|---|---|")
        for dd in pr["calibration_deciles"]:
            md.append(f"| {dd['decile']} | {dd['n']} | {dd['mean_predicted']:.5f} | {dd['observed_rate']:.5f} |")
        md.append("")
    md += [
        "## LOIO (primary scenario)",
        "",
    ]
    for r in results:
        md.append(f"- {r['holdout']}: " + ", ".join(
            f"{m}=" + "{" + ", ".join(f"{k}:{v:.4f}" for k, v in r['loio_primary'][m].items()) + "}"
            for m in r['loio_primary']))
    md += [
        "",
        "## Honest status",
        "- EXPLORATORY/PILOT. Modeled boundary breaches only; never observed liquidations.",
        "- Positive/negative result is reported as-is; the floor is pre-registered and applied mechanically.",
        "- No sealed months, no network, no confirmatory promotion.",
    ]
    (SESSION_DIR / f"fclr_risk06_calibration_{UTC_STAMP}.md").write_text("\n".join(md) + "\n", encoding="utf-8")

    print(json.dumps({
        "n_rows": len(dataset),
        "overall_breach_rate": payload["overall_breach_rate"],
        "verdict": payload["verdict"],
        "floor": payload["floor_evaluation"],
        "primary_by_holdout": [
            {m: {"delta": r["primary"][m]["delta_brier"],
                 "ci": r["primary"][m]["bootstrap"]} for m in
             ("B1_funding_conditioned", "B2_funding_shock") if m in r["primary"]}
            for r in results
        ],
    }, indent=2))


if __name__ == "__main__":
    main()
