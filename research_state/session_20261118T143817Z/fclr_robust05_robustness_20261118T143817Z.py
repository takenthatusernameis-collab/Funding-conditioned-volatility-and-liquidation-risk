#!/usr/bin/env python3
"""FCLR-VOL-LIQ-ROBUST-05 — Track C multi-holdout robustness + placebo null.

Four chronological holdouts (test 2024-06/07/08/09) with expanding train and a
7-day purge/embargo, plus a deterministic funding-permutation placebo. stdlib
only (math/csv/json/zipfile/statistics/random); no numpy/pandas/scipy.

Sign convention (do not invert): delta_qlike_vs_A = mean(QLIKE_A - QLIKE_model).
QLIKE is a LOSS (lower is better), so a POSITIVE delta means the model BEATS
RV-only and a NEGATIVE delta means the model is WORSE.

EXPLORATORY/PILOT — not confirmatory, no forecast-gate pass claim.
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
SESSION_DIR = RS / "session_20261118T143817Z"
UTC_STAMP = "20261118T143817Z"
CAMPAIGN = "FCLR-VOL-LIQ-ROBUST-05-20261118T132800Z"

SYMBOLS = ["BTCUSDT", "ETHUSDT", "SOLUSDT", "XRPUSDT", "BNBUSDT"]
MONTHS = ["2024-04", "2024-05", "2024-06", "2024-07", "2024-08", "2024-09"]
EPS = 1e-12
SEED = 12345
BOOT_REPS = 2000

SPLITS = [
    {"split": 1, "name": "2024-06",
     "train": ("2024-04-01", "2024-05-24"),
     "embargo": ("2024-05-25", "2024-05-31"),
     "test": ("2024-06-01", "2024-06-30")},
    {"split": 2, "name": "2024-07",
     "train": ("2024-04-01", "2024-06-23"),
     "embargo": ("2024-06-24", "2024-06-30"),
     "test": ("2024-07-01", "2024-07-31")},
    {"split": 3, "name": "2024-08",
     "train": ("2024-04-01", "2024-07-24"),
     "embargo": ("2024-07-25", "2024-07-31"),
     "test": ("2024-08-01", "2024-08-31")},
    {"split": 4, "name": "2024-09",
     "train": ("2024-04-01", "2024-08-24"),
     "embargo": ("2024-08-25", "2024-08-31"),
     "test": ("2024-09-01", "2024-09-30")},
]

MODELS = ["A_rv_only", "B_rv_signed", "C_rv_abs", "D_rv_signed_abs", "E_rv_funding_trails"]
MODEL_FEATURES = {
    "A_rv_only": ["lrv1", "lrv24", "lrv168"],
    "B_rv_signed": ["lrv1", "lrv24", "lrv168", "fund"],
    "C_rv_abs": ["lrv1", "lrv24", "lrv168", "fund_abs"],
    "D_rv_signed_abs": ["lrv1", "lrv24", "lrv168", "fund", "fund_abs"],
    "E_rv_funding_trails": ["lrv1", "lrv24", "lrv168", "fund", "fund_abs", "fmean", "fewma"],
}


def day_ms_range(d):
    dt = datetime.strptime(d, "%Y-%m-%d").replace(tzinfo=timezone.utc)
    return int(dt.timestamp() * 1000), int((dt + timedelta(days=1)).timestamp() * 1000) - 1


def dir_of(symbol, year_month):
    y, m = year_month.split("-")
    return f"{symbol}_{y}_{m}"


def read_csv_lines(symbol, year_month, day):
    base = CACHE / dir_of(symbol, year_month) / f"markPriceKlines-{day}"
    csv_name = f"{symbol}-1h-{day}.csv"
    if (base / csv_name).is_file():
        return (base / csv_name).read_text(encoding="utf-8", errors="ignore").splitlines()
    zp = base / f"{symbol}-1h-{day}.zip"
    if zp.is_file():
        with zipfile.ZipFile(zp) as z:
            return z.read(csv_name).decode("utf-8", errors="ignore").splitlines()
    return []


def read_funding_lines(symbol, year_month):
    base = CACHE / dir_of(symbol, year_month) / f"{symbol}-fundingRate-{year_month}"
    csv_name = f"{symbol}-fundingRate-{year_month}.csv"
    if (base / csv_name).is_file():
        return (base / csv_name).read_text(encoding="utf-8", errors="ignore").splitlines()
    zp = CACHE / dir_of(symbol, year_month) / f"{symbol}-fundingRate-{year_month}.zip"
    if zp.is_file():
        with zipfile.ZipFile(zp) as z:
            return z.read(csv_name).decode("utf-8", errors="ignore").splitlines()
    return []


def load_mark_series(symbol):
    rows = []
    for ym in MONTHS:
        y, m = ym.split("-")
        for d in range(1, 32):
            day = f"{y}-{int(m):02d}-{d:02d}"
            try:
                datetime.strptime(day, "%Y-%m-%d")
            except ValueError:
                continue
            lines = read_csv_lines(symbol, ym, day)
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


def latest_funding(funding, t_ms):
    best = None
    for ts, rate in funding:
        if ts <= t_ms:
            best = (rate, ts)
        else:
            break
    return best


def build_panel(symbol, funding_rows=None):
    marks = load_mark_series(symbol)
    funding = load_funding_series(symbol) if funding_rows is None else funding_rows
    n = len(marks)
    ret = [0.0] * n
    for i in range(1, n):
        if marks[i - 1][1] > 0 and marks[i][1] > 0:
            ret[i] = math.log(marks[i][1] / marks[i - 1][1])
    close_ms = [ts + 3_600_000 - 1 for ts, _ in marks]
    fund_rate = [0.0] * n
    fund_abs = [0.0] * n
    fund_hist = []
    for i in range(n):
        obs = latest_funding(funding, close_ms[i])
        if obs is not None:
            fund_rate[i] = obs[0]
            fund_abs[i] = abs(obs[0])
            fund_hist.append((i, obs[0]))
    return {"symbol": symbol, "marks": marks, "ret": ret, "close_ms": close_ms,
            "fund_rate": fund_rate, "fund_abs": fund_abs, "fund_hist": fund_hist, "n": n}


def trailing_rv(ret, i, win):
    s = 0.0
    for j in range(max(0, i - win + 1), i + 1):
        s += ret[j] * ret[j]
    return s


def funding_trails(fund_hist, i):
    """Mean and EWMA of signed funding observations strictly before bar i.

    Single forward pass; O(len(fund_hist)) per origin.
    """
    cnt = 0
    total = 0.0
    ewma = 0.0
    alpha = 0.0
    for (bi, r) in fund_hist:
        if bi >= i:
            break
        cnt += 1
        total += r
        alpha = 2.0 / (min(cnt, 168) + 1)
        if cnt == 1:
            ewma = r
        else:
            ewma = alpha * r + (1.0 - alpha) * ewma
    return (total / cnt if cnt else 0.0), (ewma if cnt else 0.0), cnt


def precompute_features(panel):
    """Causal feature dict per bar index (None before index 168)."""
    n = panel["n"]
    feats = [None] * n
    ret = panel["ret"]
    for i in range(168, n):
        rv1 = trailing_rv(ret, i, 1)
        rv24 = trailing_rv(ret, i, 24)
        rv168 = trailing_rv(ret, i, 168)
        f = panel["fund_rate"][i]
        fa = panel["fund_abs"][i]
        fmean, fewma, _ = funding_trails(panel["fund_hist"], i)
        feats[i] = {"lrv1": math.log(rv1 + EPS), "lrv24": math.log(rv24 + EPS),
                    "lrv168": math.log(rv168 + EPS), "fund": f, "fund_abs": fa,
                    "fmean": fmean, "fewma": fewma}
    return feats


def solve_ols(X, y):
    n = len(X)
    p = len(X[0]) if n else 0
    xtx = [[0.0] * p for _ in range(p)]
    xty = [0.0] * p
    for row, yi in zip(X, y):
        for a in range(p):
            va = row[a]
            if va == 0.0:
                continue
            xty[a] += va * yi
            for b in range(p):
                xtx[a][b] += va * row[b]
    aug = [xtx[a] + [xty[a]] for a in range(p)]
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
    coeffs = [0.0] * p
    for r in range(p - 1, -1, -1):
        s = aug[r][p]
        for c in range(r + 1, p):
            s -= aug[r][c] * coeffs[c]
        piv = aug[r][r]
        if abs(piv) < 1e-12:
            return None
        coeffs[r] = s / piv
    return coeffs


def qlike(y, yhat):
    if yhat <= 0 or yhat == float("inf"):
        return float("inf")
    return math.log(yhat) + y / yhat


def date_of(ts_ms):
    return datetime.fromtimestamp(ts_ms / 1000, tz=timezone.utc).strftime("%Y-%m-%d")


def run_design(panels, feats_by_symbol, label):
    """Fit/evaluate all models across all splits. Returns per-split results."""
    splits_out = []
    for split in SPLITS:
        sid = split["split"]
        tr_s, tr_e = split["train"]
        te_s, te_e = split["test"]
        tr_s_ms, _ = day_ms_range(tr_s)
        _, tr_e_ms = day_ms_range(tr_e)
        te_s_ms, _ = day_ms_range(te_s)
        _, te_e_ms = day_ms_range(te_e)
        print(f"[dbg] {label} split {sid} ({split['name']}) "
              f"train={tr_s}..{tr_e} test={te_s}..{te_e}", flush=True)

        def eligible_origin(panel, s_ms, e_ms):
            n = panel["n"]
            origs = []
            for i in range(168, n - 24):
                ts = panel["marks"][i][0]
                if not (s_ms <= ts <= e_ms):
                    continue
                ok = True
                for k in range(1, 25):
                    if not (s_ms <= panel["marks"][i + k][0] <= e_ms):
                        ok = False
                        break
                if ok:
                    origs.append(i)
            return origs

        train_origins = {s: eligible_origin(panels[s], tr_s_ms, tr_e_ms) for s in SYMBOLS}
        test_origins = {s: eligible_origin(panels[s], te_s_ms, te_e_ms) for s in SYMBOLS}
        print(f"[dbg] {label} split {sid} train_origins="
              f"{ {s: len(v) for s, v in train_origins.items()} } test_origins="
              f"{ {s: len(v) for s, v in test_origins.items()} }", flush=True)

        common_test_ts = None
        for s in SYMBOLS:
            ts_set = {panels[s]["marks"][i][0] for i in test_origins[s]}
            common_test_ts = ts_set if common_test_ts is None else (common_test_ts & ts_set)
        common_test_ts = sorted(common_test_ts)

        train_rows = {s: [] for s in SYMBOLS}
        for s in SYMBOLS:
            panel = panels[s]
            fts = feats_by_symbol[s]
            for i in train_origins[s]:
                y = 0.0
                for k in range(1, 25):
                    y += panel["ret"][i + k] ** 2
                train_rows[s].append((i, y, fts[i]))

        split_result = {"split": sid, "name": split["name"], "train": split["train"],
                        "embargo": split["embargo"], "test": split["test"],
                        "n_train_origins": {s: len(train_origins[s]) for s in SYMBOLS},
                        "n_test_origins": {s: len(test_origins[s]) for s in SYMBOLS},
                        "n_common_test_ts": len(common_test_ts), "models": {}}

        for model in MODELS:
            feats = MODEL_FEATURES[model]
            all_train = []
            for s in SYMBOLS:
                for (i, y, fd) in train_rows[s]:
                    all_train.append([fd[f] for f in feats])
            if all_train:
                nn = len(all_train)
                means = [sum(col) / nn for col in zip(*all_train)]
                stds = []
                for a in range(len(feats)):
                    m = means[a]
                    var = sum((row[a] - m) ** 2 for row in all_train) / nn
                    stds.append(math.sqrt(var) if var > 1e-18 else 1.0)
            else:
                means = [0.0] * len(feats)
                stds = [1.0] * len(feats)

            def std_row(fd, means=means, stds=stds, feats=feats):
                return [(fd[f] - means[a]) / stds[a] for a, f in enumerate(feats)]

            coef_by_model = {}
            train_resid = []
            fit_ok = {}
            for s in SYMBOLS:
                X = []
                Y = []
                for (i, y, fd) in train_rows[s]:
                    X.append([1.0] + std_row(fd))
                    Y.append(math.log(y + EPS))
                coef = solve_ols(X, Y)
                fit_ok[s] = coef is not None
                coef_by_model[s] = coef
                if coef is not None:
                    for (i, y, fd) in train_rows[s]:
                        row = std_row(fd)
                        pred = coef[0] + sum(coef[a + 1] * row[a] for a in range(len(feats)))
                        train_resid.append(math.log(y + EPS) - pred)

            smearing = 1.0
            if train_resid:
                smearing = math.exp(sum(train_resid) / len(train_resid))

            per_inst = {}
            for s in SYMBOLS:
                panel = panels[s]
                fts = feats_by_symbol[s]
                idx_by_ts = {panel["marks"][i][0]: i for i in test_origins[s]}
                ql = []
                mae = []
                rmse_sq = []
                days = []
                for ts in common_test_ts:
                    i = idx_by_ts.get(ts)
                    if i is None:
                        continue
                    coef = coef_by_model[s]
                    if coef is None:
                        continue
                    fd = fts[i]
                    y = 0.0
                    for k in range(1, 25):
                        y += panel["ret"][i + k] ** 2
                    row = std_row(fd)
                    pred_log = coef[0] + sum(coef[a + 1] * row[a] for a in range(len(feats)))
                    pred_var = math.exp(pred_log) * smearing
                    ql.append(qlike(y, pred_var))
                    mae.append(abs(y - pred_var))
                    rmse_sq.append((y - pred_var) ** 2)
                    days.append(date_of(panel["marks"][i][0]))
                per_inst[s] = {"qlike": ql, "mae": mae, "rmse_sq": rmse_sq,
                               "n": len(ql), "days": days}
            split_result["models"][model] = {"fit_ok": fit_ok, "smearing": smearing,
                                             "per_instrument": per_inst}
        splits_out.append(split_result)
    return splits_out


def split_summary(split_result):
    out = {}
    for model in MODELS:
        ql = []
        mae = []
        rmse_sq = []
        for s in SYMBOLS:
            pi = split_result["models"][model]["per_instrument"].get(s, {})
            ql.extend(pi.get("qlike", []))
            mae.extend(pi.get("mae", []))
            rmse_sq.extend(pi.get("rmse_sq", []))
        ql_A = []
        for s in SYMBOLS:
            pi = split_result["models"]["A_rv_only"]["per_instrument"].get(s, {})
            ql_A.extend(pi.get("qlike", []))
        dql = [a - b for a, b in zip(ql_A, ql)] if len(ql_A) == len(ql) else []
        out[model] = {
            "n": len(ql),
            "mean_qlike": (sum(ql) / len(ql) if ql else None),
            "mean_mae": (sum(mae) / len(mae) if mae else None),
            "mean_rmse": (math.sqrt(sum(rmse_sq) / len(rmse_sq)) if rmse_sq else None),
            "mean_delta_qlike_vs_A": (sum(dql) / len(dql) if dql else None),
        }
    return out


def bootstrap_for_split(split_result, seed):
    """UTC-day block bootstrap of mean(QLIKE_A - QLIKE_model) within one split."""
    rng = random.Random(seed)
    boot = {}
    for m in MODELS:
        if m == "A_rv_only":
            continue
        by_day_model = {}
        by_day_a = {}
        for s in SYMBOLS:
            pm = split_result["models"][m]["per_instrument"].get(s, {})
            pa = split_result["models"]["A_rv_only"]["per_instrument"].get(s, {})
            for q, d in zip(pm.get("qlike", []), pm.get("days", [])):
                by_day_model.setdefault(d, []).append(q)
            for q, d in zip(pa.get("qlike", []), pa.get("days", [])):
                by_day_a.setdefault(d, []).append(q)
        common_days = sorted(set(by_day_model) & set(by_day_a))
        boot_data = []
        for d in common_days:
            mm = by_day_model[d]
            aa = by_day_a[d]
            n = min(len(mm), len(aa))
            for k in range(n):
                boot_data.append((d, aa[k] - mm[k]))
        all_days = sorted({d for (d, _) in boot_data})
        rep_means = []
        if boot_data and all_days:
            for _ in range(BOOT_REPS):
                sampled = [rng.choice(all_days) for _ in all_days]
                vals = [dv for (d, dv) in boot_data if d in sampled]
                if vals:
                    rep_means.append(sum(vals) / len(vals))
        if rep_means:
            rep_means.sort()
            lo = rep_means[int(0.025 * len(rep_means))]
            hi = rep_means[int(0.975 * len(rep_means))]
            boot[m] = {"mean_improvement": sum(rep_means) / len(rep_means),
                       "ci_2_5": lo, "ci_97_5": hi, "n_reps": len(rep_means)}
        else:
            boot[m] = {"mean_improvement": None, "ci_2_5": None, "ci_97_5": None, "n_reps": 0}
    return boot


def loio_for_split(split_result):
    loio = {}
    for m in MODELS:
        if m == "A_rv_only":
            continue
        loio[m] = {}
        for leave in SYMBOLS:
            vals = []
            for s in SYMBOLS:
                if s == leave:
                    continue
                pm = split_result["models"][m]["per_instrument"].get(s, {})
                pa = split_result["models"]["A_rv_only"]["per_instrument"].get(s, {})
                for qa, qm in zip(pa.get("qlike", []), pm.get("qlike", [])):
                    vals.append(qa - qm)
            loio[m][leave] = (sum(vals) / len(vals) if vals else None)
    return loio


def placebo_funding(symbol, seed):
    """Deterministically permute funding rate values across their timestamps."""
    rows = load_funding_series(symbol)
    if not rows:
        return rows
    rng = random.Random(seed)
    times = [ts for ts, _ in rows]
    rates = [r for _, r in rows]
    rng.shuffle(rates)
    return list(zip(times, rates))


def main():
    out = {
        "schema": "fclr_robust05_robustness",
        "timestamp_utc": UTC_STAMP,
        "campaign": CAMPAIGN,
        "track": "C_volatility_forecast_multi_holdout_plus_placebo",
        "design": "FOUR_CHRONOLOGICAL_HOLDOUTS_EXPANDING_TRAIN_7D_EMBARGO",
        "network_used": False,
        "parquet_used": False,
        "numpy_used": False,
        "label": "EXPLORATORY_PILOT",
        "instruments": SYMBOLS,
        "window": "2024-04-01..2024-09-30",
        "horizon": "next-24h realized variance from 1h mark-price close-to-close log returns t+1..t+24",
        "mark_field": "close (markPriceKlines 1h), units USDT",
        "epsilon": EPS,
        "models": MODELS,
        "bootstrap": {"reps": BOOT_REPS, "seed": SEED,
                      "unit": "UTC day block, resampled jointly across instruments, per split and pooled"},
        "sign_convention": ("mean_delta_qlike_vs_A = mean(QLIKE_A - QLIKE_model); QLIKE is a loss, "
                            "lower is better; positive = model BETTER than RV-only"),
        "splits": [],
        "placebo": {},
    }

    panels = {s: build_panel(s) for s in SYMBOLS}
    feats_by_symbol = {s: precompute_features(panels[s]) for s in SYMBOLS}
    for s in SYMBOLS:
        print(f"[dbg] {s}: bars={panels[s]['n']} funding_obs={len(panels[s]['fund_hist'])}",
              flush=True)

    splits_out = run_design(panels, feats_by_symbol, "real")
    out["splits"] = splits_out

    real_summary_by_split = {}
    real_boot_by_split = {}
    for sr in splits_out:
        key = sr["name"]
        real_summary_by_split[key] = split_summary(sr)
        real_boot_by_split[key] = bootstrap_for_split(sr, SEED)
        sr["summary"] = real_summary_by_split[key]
        sr["bootstrap"] = real_boot_by_split[key]
        sr["loio"] = loio_for_split(sr)

    pooled_pseudo = {"models": {}}
    for m in MODELS:
        per_instrument = {}
        for s in SYMBOLS:
            ql = []
            mae = []
            rmse_sq = []
            days = []
            for sr in splits_out:
                pi = sr["models"][m]["per_instrument"].get(s, {})
                ql.extend(pi.get("qlike", []))
                mae.extend(pi.get("mae", []))
                rmse_sq.extend(pi.get("rmse_sq", []))
                days.extend(pi.get("days", []))
            per_instrument[s] = {"qlike": ql, "mae": mae, "rmse_sq": rmse_sq,
                                 "n": len(ql), "days": days}
        pooled_pseudo["models"][m] = {"per_instrument": per_instrument}
    pooled = split_summary(pooled_pseudo)
    out["pooled_summary"] = pooled

    pooled_boot = {}
    rng = random.Random(SEED)
    for m in MODELS:
        if m == "A_rv_only":
            continue
        by_day_model = {}
        by_day_a = {}
        for sr in splits_out:
            for s in SYMBOLS:
                pm = sr["models"][m]["per_instrument"].get(s, {})
                pa = sr["models"]["A_rv_only"]["per_instrument"].get(s, {})
                for q, d in zip(pm.get("qlike", []), pm.get("days", [])):
                    by_day_model.setdefault(d, []).append(q)
                for q, d in zip(pa.get("qlike", []), pa.get("days", [])):
                    by_day_a.setdefault(d, []).append(q)
        boot_data = []
        for d in sorted(set(by_day_model) & set(by_day_a)):
            mm = by_day_model[d]
            aa = by_day_a[d]
            n = min(len(mm), len(aa))
            for k in range(n):
                boot_data.append((d, aa[k] - mm[k]))
        all_days = sorted({d for (d, _) in boot_data})
        rep_means = []
        if boot_data and all_days:
            for _ in range(BOOT_REPS):
                sampled = [rng.choice(all_days) for _ in all_days]
                vals = [dv for (d, dv) in boot_data if d in sampled]
                if vals:
                    rep_means.append(sum(vals) / len(vals))
        if rep_means:
            rep_means.sort()
            pooled_boot[m] = {"mean_improvement": sum(rep_means) / len(rep_means),
                              "ci_2_5": rep_means[int(0.025 * len(rep_means))],
                              "ci_97_5": rep_means[int(0.975 * len(rep_means))],
                              "n_reps": len(rep_means)}
        else:
            pooled_boot[m] = {"mean_improvement": None, "ci_2_5": None, "ci_97_5": None,
                              "n_reps": 0}
    out["pooled_bootstrap"] = pooled_boot

    # Placebo: permute funding values across timestamps, rerun identical pipeline.
    print("[dbg] building placebo panels", flush=True)
    placebo_panels = {}
    placebo_feats = {}
    for idx, s in enumerate(SYMBOLS):
        prow = placebo_funding(s, SEED + 1000 * idx)
        p = build_panel(s, funding_rows=prow)
        placebo_panels[s] = p
        placebo_feats[s] = precompute_features(p)
    print("[dbg] running placebo design", flush=True)
    placebo_splits = run_design(placebo_panels, placebo_feats, "placebo")

    placebo_by_split = {}
    for sr in placebo_splits:
        smry = split_summary(sr)
        boot = bootstrap_for_split(sr, SEED)
        e = smry["E_rv_funding_trails"]
        placebo_by_split[sr["name"]] = {
            "mean_qlike_E": e["mean_qlike"],
            "mean_delta_qlike_vs_A_E": e["mean_delta_qlike_vs_A"],
            "bootstrap_mean_A_minus_E": boot["E_rv_funding_trails"]["mean_improvement"],
            "bootstrap_ci95": [boot["E_rv_funding_trails"]["ci_2_5"],
                               boot["E_rv_funding_trails"]["ci_97_5"]],
        }
    placebo_pooled_e = pooled_agg("qlike")
    placebo_mean_qlike_E = (sum(placebo_pooled_e) / len(placebo_pooled_e)
                            if placebo_pooled_e else None)
    out["placebo"] = {
        "description": "Funding rate values deterministically permuted across their observation "
                       "timestamps (seed 12345 + symbol offset); identical feature/estimation/"
                       "evaluation pipeline; E_rv_funding_trails compared to real A.",
        "per_split": placebo_by_split,
        "mean_qlike_E_pooled": placebo_mean_qlike_E,
    }

    # Materiality floor: E beats A in >=3 of 4 holdouts (point + CI lower > 0),
    # and real |mean delta| exceeds placebo |mean delta|.
    per_split_floor = {}
    n_beats = 0
    for sr in splits_out:
        e_smry = sr["summary"]["E_rv_funding_trails"]
        e_boot = sr["bootstrap"]["E_rv_funding_trails"]
        d = e_smry["mean_delta_qlike_vs_A"]
        lo = e_boot["ci_2_5"]
        beat = bool(d is not None and d > 0 and lo is not None and lo > 0)
        if beat:
            n_beats += 1
        per_split_floor[sr["name"]] = {"mean_delta_qlike_vs_A": d,
                                       "bootstrap_ci_2_5": lo, "beats_A": beat}

    real_pooled_d = pooled["E_rv_funding_trails"]["mean_delta_qlike_vs_A"]
    placebo_deltas = []
    for name, pv in placebo_by_split.items():
        if pv["mean_delta_qlike_vs_A_E"] is not None:
            placebo_deltas.append(pv["mean_delta_qlike_vs_A_E"])
    placebo_mean_delta = (sum(placebo_deltas) / len(placebo_deltas)
                          if placebo_deltas else None)
    real_abs = abs(real_pooled_d) if real_pooled_d is not None else None
    placebo_abs = abs(placebo_mean_delta) if placebo_mean_delta is not None else None
    exceeds_placebo = bool(real_abs is not None and placebo_abs is not None
                           and real_abs > placebo_abs)

    out["materiality"] = {
        "floor": ("E beats A (mean(QLIKE_A - QLIKE_E) > 0 with bootstrap CI95 lower bound > 0) "
                  "in >=3 of 4 holdouts AND real funding-trail |mean delta QLIKE| exceeds "
                  "placebo |mean delta QLIKE|"),
        "qlike_lower_is_better": True,
        "per_split": per_split_floor,
        "n_holdouts_E_beats_A": n_beats,
        "real_pooled_mean_delta_qlike_vs_A_E": real_pooled_d,
        "placebo_mean_delta_qlike_vs_A_E": placebo_mean_delta,
        "real_abs_delta": real_abs,
        "placebo_abs_delta": placebo_abs,
        "real_exceeds_placebo_abs": exceeds_placebo,
        "materiality_floor_met": bool(n_beats >= 3 and exceeds_placebo),
        "better_model_by_pooled_mean_qlike": (
            "E_rv_funding_trails"
            if (real_pooled_d is not None and real_pooled_d > 0) else "A_rv_only"),
    }

    out["leakage"] = {
        "train_only_standardization": True,
        "no_sealed_months_touched": True,
        "test_months": [s["name"] for s in SPLITS],
        "purge_embargo_days": 7,
        "expanding_train": True,
        "no_lookahead": True,
        "placebo_is_deterministic": True,
    }
    out["honest_status"] = (
        "EXPLORATORY/PILOT. Multi-holdout robustness plus a funding-permutation placebo. "
        "See materiality.materiality_floor_met for the pre-registered verdict; a negative "
        "result is a valid completion and no confirmatory promotion is claimed."
    )
    return out


if __name__ == "__main__":
    result = main()
    json_path = SESSION_DIR / f"fclr_robust05_robustness_{UTC_STAMP}.json"
    md_path = SESSION_DIR / f"fclr_robust05_robustness_{UTC_STAMP}.md"
    json_path.write_text(json.dumps(result, indent=2), encoding="utf-8")

    mat = result["materiality"]
    md = []
    md.append("# FCLR-VOL-LIQ-ROBUST-05 — Track C Multi-Holdout Robustness + Placebo (stdlib OLS HAR)")
    md.append("")
    md.append(f"**Session:** session_{UTC_STAMP}  ")
    md.append(f"**Campaign:** {CAMPAIGN}  ")
    md.append(f"**Timestamp (UTC):** {UTC_STAMP}  ")
    md.append("**Label:** EXPLORATORY/PILOT — not confirmatory, no forecast-gate pass claim.  ")
    md.append("**Network:** none. **Parquet:** none. **numpy/pandas/scipy:** none (stdlib only).")
    md.append("")
    md.append("## Sign convention (do not invert)")
    md.append("- `delta_qlike_vs_A = mean(QLIKE_A - QLIKE_model)`; QLIKE is a **loss** (lower is better).")
    md.append("- **Positive** delta = model BEATS RV-only. **Negative** delta = model is WORSE.")
    md.append("")
    md.append("## Design")
    md.append("- Four chronological holdouts with expanding train and 7-day purge/embargo.")
    md.append("- Instruments: " + ", ".join(SYMBOLS))
    md.append("- Target: next-24h realized variance (sum of 24 hourly squared log returns t+1..t+24).")
    md.append("- Features (causal at t): lrv1, lrv24, lrv168, fund, fund_abs, fmean, fewma.")
    md.append("- Estimation: stdlib OLS on log RV, Duan smearing, train-only standardization.")
    md.append("- Uncertainty: UTC-day block bootstrap, seed 12345, 2000 reps, per split + pooled; LOIO.")
    md.append("- Placebo: deterministic permutation of funding values across timestamps, same pipeline.")
    md.append("")
    for sr in result["splits"]:
        md.append(f"### Holdout {sr['name']}: train {sr['train'][0]}..{sr['train'][1]}, "
                  f"embargo {sr['embargo'][0]}..{sr['embargo'][1]}, test {sr['test'][0]}..{sr['test'][1]}")
        md.append(f"- common test timestamps: {sr['n_common_test_ts']}")
        for m in MODELS:
            smry = sr["summary"][m]
            bs = sr["bootstrap"].get(m, {})
            line = (f"- {m}: n={smry['n']}, mean_qlike={smry['mean_qlike']}, "
                    f"mean_delta_qlike_vs_A={smry['mean_delta_qlike_vs_A']}")
            if bs.get("mean_improvement") is not None:
                line += (f", boot mean(A-model)={bs['mean_improvement']:.6f} "
                         f"CI95=[{bs['ci_2_5']:.6f}, {bs['ci_97_5']:.6f}]")
            md.append(line)
        md.append("")
    md.append("## Pooled summary (ΔQLIKE = A − model; positive = model better)")
    for m in MODELS:
        smry = result["pooled_summary"][m]
        bs = result["pooled_bootstrap"].get(m, {})
        line = (f"- {m}: n={smry['n']}, mean_qlike={smry['mean_qlike']}, "
                f"mean_delta_qlike_vs_A={smry['mean_delta_qlike_vs_A']}")
        if bs.get("mean_improvement") is not None:
            line += (f", boot mean(A-model)={bs['mean_improvement']:.6f} "
                     f"CI95=[{bs['ci_2_5']:.6f}, {bs['ci_97_5']:.6f}]")
        md.append(line)
    md.append("")
    md.append("## Placebo null (funding values permuted across timestamps)")
    for name, pv in result["placebo"]["per_split"].items():
        md.append(f"- {name}: placebo mean_qlike_E={pv['mean_qlike_E']}, "
                  f"placebo mean_delta_qlike_vs_A={pv['mean_delta_qlike_vs_A_E']}, "
                  f"boot CI95={pv['bootstrap_ci95']}")
    md.append(f"- placebo pooled mean_qlike_E = {result['placebo']['mean_qlike_E_pooled']}")
    md.append(f"- placebo mean (A − E) across holdouts = {mat['placebo_mean_delta_qlike_vs_A_E']}")
    md.append("")
    md.append("## Materiality floor (pre-registered)")
    md.append(f"- E beats A in {mat['n_holdouts_E_beats_A']} of 4 holdouts; per-holdout: " +
              ", ".join(f"{k}: delta={v['mean_delta_qlike_vs_A']}, CI_lo={v['bootstrap_ci_2_5']}, "
                        f"beats={v['beats_A']}" for k, v in mat["per_split"].items()))
    md.append(f"- real pooled |Δ| = {mat['real_abs_delta']} vs placebo |Δ| = {mat['placebo_abs_delta']}")
    md.append(f"- real exceeds placebo = {mat['real_exceeds_placebo_abs']}")
    md.append(f"- better model by pooled mean QLIKE = **{mat['better_model_by_pooled_mean_qlike']}**")
    md.append(f"- **materiality_floor_met = {mat['materiality_floor_met']}**")
    md.append("")
    md.append("## Honest status")
    md.append("- EXPLORATORY/PILOT. No confirmatory promotion claimed.")
    md.append("- No sealed months touched. No look-ahead; train-only standardization; expanding train.")
    md.append("- Negative result is a valid completion of the pre-registered campaign.")
    md_path.write_text("\n".join(md) + "\n", encoding="utf-8")
    print("WROTE", json_path, md_path)
    print("MATERIALITY", json.dumps(mat, indent=2))
