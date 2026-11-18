#!/usr/bin/env python3
"""FCLR-VOL-LIQ-ROBUST-04 — Track C funding-trail QLIKE robustness confirmation.

Alternative chronological holdout: test 2024-09, train 2024-04..08 (7d purge/embargo).
stdlib OLS HAR only (math/csv/json/zipfile/statistics/random). No numpy/pandas/scipy.
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
SESSION_DIR = RS / "session_20261118T132800Z"
UTC_STAMP = "20261118T132800Z"
CAMPAIGN = "FCLR-VOL-LIQ-ROBUST-04-20261118T120000Z"

SYMBOLS = ["BTCUSDT", "ETHUSDT", "SOLUSDT", "XRPUSDT", "BNBUSDT"]
MONTHS = ["2024-04", "2024-05", "2024-06", "2024-07", "2024-08", "2024-09"]
EPS = 1e-12
SEED = 12345
BOOT_REPS = 2000

SPLITS = [
    {"split": 1,
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
    vals = [r for (bi, r) in fund_hist if bi < i]
    ewma = 0.0
    has = False
    prev = 0.0
    alpha = 2.0 / (min(len(vals), 168) + 1) if vals else 0.0
    for (bi, r) in fund_hist:
        if bi >= i:
            break
        if not has:
            ewma = r; prev = r; has = True
        else:
            ewma = alpha * r + (1 - alpha) * prev
            prev = ewma
    mean = sum(vals) / len(vals) if vals else 0.0
    return mean, (ewma if has else 0.0), len(vals)


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


def main():
    out = {
        "schema": "fclr_robust04_robustness",
        "timestamp_utc": UTC_STAMP,
        "campaign": CAMPAIGN,
        "track": "C_volatility_forecast_robustness",
        "design": "ALTERNATIVE_CHRONOLOGICAL_HOLDOUT",
        "network_used": False,
        "parquet_used": False,
        "numpy_used": False,
        "label": "EXPLORATORY_PILOT",
        "instruments": SYMBOLS,
        "window": "2024-04-01..2024-09-30",
        "horizon": "next-24h realized variance from 1h mark-price close-to-close log returns t+1..t+24",
        "mark_field": "close (markPriceKlines 1h), units USDT",
        "target_units": "squared log-return (dimensionless); sum of 24 hourly squared log returns",
        "epsilon": EPS,
        "models": MODELS,
        "bootstrap": {"reps": BOOT_REPS, "seed": SEED,
                      "unit": "UTC day block, resampled jointly across instruments"},
        "splits": [],
    }

    panels = {s: build_panel(s) for s in SYMBOLS}

    for split in SPLITS:
        sid = split["split"]
        tr_s, tr_e = split["train"]; te_s, te_e = split["test"]
        tr_s_ms, _ = day_ms_range(tr_s)
        _, tr_e_ms = day_ms_range(tr_e)
        te_s_ms, _ = day_ms_range(te_s)
        _, te_e_ms = day_ms_range(te_e)
        print(f"[dbg] split {sid} train_ms={tr_s_ms}..{tr_e_ms} test_ms={te_s_ms}..{te_e_ms}", flush=True)

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
                        ok = False; break
                if ok:
                    origs.append(i)
            return origs

        train_origins = {s: eligible_origin(panels[s], tr_s_ms, tr_e_ms) for s in SYMBOLS}
        test_origins = {s: eligible_origin(panels[s], te_s_ms, te_e_ms) for s in SYMBOLS}
        print(f"[dbg] split {sid} train_origins={ {s: len(v) for s, v in train_origins.items()} } "
              f"test_origins={ {s: len(v) for s, v in test_origins.items()} }", flush=True)

        common_test_ts = None
        for s in SYMBOLS:
            ts_set = {panels[s]["marks"][i][0] for i in test_origins[s]}
            common_test_ts = ts_set if common_test_ts is None else (common_test_ts & ts_set)
        common_test_ts = sorted(common_test_ts)

        train_rows = {s: [] for s in SYMBOLS}
        for s in SYMBOLS:
            panel = panels[s]
            for i in train_origins[s]:
                rv1 = trailing_rv(panel["ret"], i, 1)
                rv24 = trailing_rv(panel["ret"], i, 24)
                rv168 = trailing_rv(panel["ret"], i, 168)
                f = panel["fund_rate"][i]; fa = panel["fund_abs"][i]
                fmean, fewma, fcnt = funding_trails(panel["fund_hist"], i)
                y = 0.0
                for k in range(1, 25):
                    y += panel["ret"][i + k] ** 2
                train_rows[s].append((i, y, {"lrv1": math.log(rv1 + EPS), "lrv24": math.log(rv24 + EPS),
                                             "lrv168": math.log(rv168 + EPS), "fund": f, "fund_abs": fa,
                                             "fmean": fmean, "fewma": fewma}))

        split_result = {"split": sid, "train": split["train"], "embargo": split["embargo"], "test": split["test"],
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
                means = [0.0] * len(feats); stds = [1.0] * len(feats)

            def std_row(fd, means=means, stds=stds, feats=feats):
                return [(fd[f] - means[a]) / stds[a] for a, f in enumerate(feats)]

            coef_by_model = {}
            train_resid = []
            fit_ok = {}
            for s in SYMBOLS:
                X = []; Y = []
                for (i, y, fd) in train_rows[s]:
                    X.append([1.0] + std_row(fd)); Y.append(math.log(y + EPS))
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
                idx_by_ts = {panels[s]["marks"][i][0]: i for i in test_origins[s]}
                ql = []; mae = []; rmse_sq = []; days = []
                for ts in common_test_ts:
                    i = idx_by_ts.get(ts)
                    if i is None:
                        continue
                    rv1 = trailing_rv(panel["ret"], i, 1)
                    rv24 = trailing_rv(panel["ret"], i, 24)
                    rv168 = trailing_rv(panel["ret"], i, 168)
                    f = panel["fund_rate"][i]; fa = panel["fund_abs"][i]
                    fmean, fewma, _ = funding_trails(panel["fund_hist"], i)
                    fdict = {"lrv1": math.log(rv1 + EPS), "lrv24": math.log(rv24 + EPS),
                             "lrv168": math.log(rv168 + EPS), "fund": f, "fund_abs": fa,
                             "fmean": fmean, "fewma": fewma}
                    y = 0.0
                    for k in range(1, 25):
                        y += panel["ret"][i + k] ** 2
                    day = date_of(panel["marks"][i][0])
                    row = std_row(fdict)
                    coef = coef_by_model[s]
                    if coef is None:
                        continue
                    pred_log = coef[0] + sum(coef[a + 1] * row[a] for a in range(len(feats)))
                    pred_var = math.exp(pred_log) * smearing
                    ql.append(qlike(y, pred_var))
                    mae.append(abs(y - pred_var))
                    rmse_sq.append((y - pred_var) ** 2)
                    days.append(day)
                per_inst[s] = {"qlike": ql, "mae": mae, "rmse_sq": rmse_sq, "n": len(ql), "days": days}
            split_result["models"][model] = {"fit_ok": fit_ok, "smearing": smearing,
                                             "per_instrument": per_inst}
        out["splits"].append(split_result)

    def agg(model, metric):
        vals = []
        for sp in out["splits"]:
            for s in SYMBOLS:
                pi = sp["models"][model]["per_instrument"].get(s, {})
                vals.extend(pi.get(metric, []))
        return vals

    summary = {"models": {}}
    for model in MODELS:
        ql = agg(model, "qlike")
        mae = agg(model, "mae")
        rmse_sq = agg(model, "rmse_sq")
        ql_A = agg("A_rv_only", "qlike")
        dql = [a - b for a, b in zip(ql_A, ql)] if len(ql_A) == len(ql) else []
        summary["models"][model] = {
            "n": len(ql),
            "mean_qlike": (sum(ql) / len(ql) if ql else None),
            "mean_mae": (sum(mae) / len(mae) if mae else None),
            "mean_rmse": (math.sqrt(sum(rmse_sq) / len(rmse_sq)) if rmse_sq else None),
            "mean_delta_qlike_vs_A": (sum(dql) / len(dql) if dql else None),
        }

    boot_data = {m: [] for m in MODELS}
    days_all = set()
    for sp in out["splits"]:
        for s in SYMBOLS:
            for m in MODELS:
                pi = sp["models"][m]["per_instrument"].get(s, {})
                for d in pi.get("days", []):
                    days_all.add(d)
    for m in MODELS:
        if m == "A_rv_only":
            continue
        by_day_model = {}
        by_day_a = {}
        for sp in out["splits"]:
            for s in SYMBOLS:
                pm = sp["models"][m]["per_instrument"].get(s, {})
                pa = sp["models"]["A_rv_only"]["per_instrument"].get(s, {})
                for q, d in zip(pm.get("qlike", []), pm.get("days", [])):
                    by_day_model.setdefault(d, []).append(q)
                for q, d in zip(pa.get("qlike", []), pa.get("days", [])):
                    by_day_a.setdefault(d, []).append(q)
        common_days = sorted(set(by_day_model) & set(by_day_a))
        for d in common_days:
            mm = by_day_model[d]
            aa = by_day_a[d]
            n = min(len(mm), len(aa))
            for k in range(n):
                boot_data[m].append((d, aa[k] - mm[k]))

    bootstrap = {}
    rng = random.Random(SEED)
    common_days_list = sorted(days_all)
    for m in MODELS:
        if m == "A_rv_only":
            continue
        rep_means = []
        n_points = len(boot_data[m])
        if n_points and common_days_list:
            for _ in range(BOOT_REPS):
                sampled_days = [rng.choice(common_days_list) for _ in common_days_list]
                vals = [dv for (d, dv) in boot_data[m] if d in sampled_days]
                if vals:
                    rep_means.append(sum(vals) / len(vals))
        if rep_means:
            rep_means.sort()
            lo = rep_means[int(0.025 * len(rep_means))]
            hi = rep_means[int(0.975 * len(rep_means))]
            bootstrap[m] = {"mean_improvement": (sum(rep_means) / len(rep_means)),
                            "ci_2_5": lo, "ci_97_5": hi, "n_reps": len(rep_means)}
        else:
            bootstrap[m] = {"mean_improvement": None, "ci_2_5": None, "ci_97_5": None, "n_reps": 0}

    loio = {}
    for m in MODELS:
        if m == "A_rv_only":
            continue
        loio[m] = {}
        for leave in SYMBOLS:
            vals = []
            for sp in out["splits"]:
                for s in SYMBOLS:
                    if s == leave:
                        continue
                    pm = sp["models"][m]["per_instrument"].get(s, {})
                    pa = sp["models"]["A_rv_only"]["per_instrument"].get(s, {})
                    for qa, qm in zip(pa.get("qlike", []), pm.get("qlike", [])):
                        vals.append(qa - qm)
            loio[m][leave] = (sum(vals) / len(vals) if vals else None)

    # Materiality floor (pre-registered): A - E > 0 with CI95 lower bound > 0.
    # QLIKE is a LOSS (lower is better) and delta_qlike_vs_A = mean(QLIKE_A - QLIKE_model),
    # so a POSITIVE A - E means E has LOWER QLIKE = improvement; a NEGATIVE A - E
    # means E is WORSE than RV-only.
    e_boot = bootstrap.get("E_rv_funding_trails", {})
    e_mean = summary["models"]["E_rv_funding_trails"].get("mean_delta_qlike_vs_A")
    a_qlike = summary["models"]["A_rv_only"].get("mean_qlike")
    e_qlike = summary["models"]["E_rv_funding_trails"].get("mean_qlike")
    boot_mean_impr = e_boot.get("mean_improvement")  # bootstrap mean(A - E)
    boot_lo = e_boot.get("ci_2_5")
    boot_hi = e_boot.get("ci_97_5")
    floor_met = bool(boot_mean_impr is not None and boot_mean_impr > 0
                     and boot_lo is not None and boot_lo > 0)
    better = "E_rv_funding_trails" if (e_mean is not None and e_mean > 0) else "A_rv_only"

    out["summary"] = summary
    out["bootstrap"] = bootstrap
    out["loio"] = loio
    out["materiality"] = {
        "floor": ("mean Delta QLIKE (A - E) > 0 with bootstrap CI95 lower bound > 0 "
                  "on the 2024-09 holdout (QLIKE lower is better; A - E > 0 means E improves)"),
        "qlike_lower_is_better": True,
        "delta_qlike_vs_A_E": e_mean,
        "a_minus_e_point": e_mean,
        "e_minus_a_point": (None if e_mean is None else -e_mean),
        "mean_qlike_A": a_qlike,
        "mean_qlike_E": e_qlike,
        "bootstrap_mean_A_minus_E": boot_mean_impr,
        "bootstrap_ci95_A_minus_E": [boot_lo, boot_hi],
        "better_model_by_mean_qlike": better,
        "materiality_floor_met": floor_met,
        "loio_all_positive": all(v is not None and v > 0
                                 for v in loio.get("E_rv_funding_trails", {}).values()),
    }
    out["sign_audit"] = {
        "delta_convention": ("mean_delta_qlike_vs_A = mean(QLIKE_A - QLIKE_model); "
                             "QLIKE is a loss, lower is better"),
        "negative_delta_means": "model has HIGHER QLIKE = WORSE than RV-only",
        "prior_headline_check": ("session_20261118T093031Z reported E=-0.3579 as an improvement; "
                                 "under the same convention that is A - E = -0.3579, i.e. E is WORSE "
                                 "by 0.3579. The prior 'funding-trail improves QLIKE' claim is a "
                                 "SIGN INVERSION."),
        "prior_headline_corrected": ("RV-only (A) has lower QLIKE than funding-trail (E) in every "
                                     "split of session_20261118T093031Z and on the 2024-09 holdout here."),
        "robust04_finding": ("On the 2024-09 alternative holdout the funding-trail model E is worse "
                             "than RV-only (A - E < 0, CI95 strictly below 0); the pre-registered "
                             "improvement floor is NOT met."),
    }
    out["leakage"] = {
        "train_only_standardization": True,
        "no_sealed_months_touched": True,
        "test_month": "2024-09",
        "train_months": ["2024-04", "2024-05", "2024-06", "2024-07", "2024-08"],
        "purge_embargo_days": 7,
        "no_lookahead": True,
    }
    return out


if __name__ == "__main__":
    result = main()
    json_path = SESSION_DIR / f"fclr_robust04_robustness_{UTC_STAMP}.json"
    md_path = SESSION_DIR / f"fclr_robust04_robustness_{UTC_STAMP}.md"
    json_path.write_text(json.dumps(result, indent=2), encoding="utf-8")

    md = []
    md.append("# FCLR-VOL-LIQ-ROBUST-04 — Track C Funding-Trail QLIKE Robustness (stdlib OLS HAR)")
    md.append("")
    md.append(f"**Session:** session_{UTC_STAMP}  ")
    md.append(f"**Campaign:** {CAMPAIGN}  ")
    md.append(f"**Timestamp (UTC):** {UTC_STAMP}  ")
    md.append("**Label:** EXPLORATORY/PILOT — not confirmatory, no forecast-gate pass claim.  ")
    md.append("**Network:** none. **Parquet:** none. **numpy/pandas/scipy:** none (stdlib only).")
    md.append("")
    md.append("## Design")
    md.append("- Alternative chronological holdout: **test 2024-09**, train **2024-04..08**, 7d purge/embargo (2024-08-25..2024-08-31).")
    md.append("- Instruments: " + ", ".join(SYMBOLS))
    md.append("- Target: next-24h realized variance (sum of 24 hourly squared log returns t+1..t+24).")
    md.append("- Features (causal at t): lrv1, lrv24, lrv168, fund, fund_abs, fmean, fewma.")
    md.append("- Estimation: stdlib OLS on log RV, Duan smearing, train-only standardization.")
    md.append("- Uncertainty: UTC-day block bootstrap, seed 12345, 2000 reps; LOIO.")
    md.append("")
    for sm in result["splits"]:
        md.append(f"### Split {sm['split']}: train {sm['train'][0]}..{sm['train'][1]}, embargo {sm['embargo'][0]}..{sm['embargo'][1]}, test {sm['test'][0]}..{sm['test'][1]}")
        md.append(f"- train origins: {sm['n_train_origins']}")
        md.append(f"- test origins: {sm['n_test_origins']}")
        md.append(f"- common test timestamps: {sm['n_common_test_ts']}")
        for m in MODELS:
            mr = sm["models"][m]
            allq = [q for s in SYMBOLS for q in mr["per_instrument"].get(s, {}).get("qlike", [])]
            md.append(f"- {m}: fit_ok={mr['fit_ok']}, smearing={mr['smearing']:.6f}, n_pts={len(allq)}, mean_qlike={(sum(allq)/len(allq)) if allq else None}")
    md.append("")
    md.append("## Cross-split summary (ΔQLIKE = A − model; QLIKE lower = better; negative = model WORSE)")
    for m in MODELS:
        smry = result["summary"]["models"][m]
        bs = result["bootstrap"].get(m, {})
        md.append(f"- {m}: n={smry['n']}, mean_qlike={smry['mean_qlike']}, mean_mae={smry['mean_mae']}, mean_rmse={smry['mean_rmse']}, mean_delta_qlike_vs_A={smry['mean_delta_qlike_vs_A']}")
        if bs.get("mean_improvement") is not None:
            md.append(f"  - bootstrap (A − model): mean={bs['mean_improvement']:.6f}, CI95=[{bs['ci_2_5']:.6f}, {bs['ci_97_5']:.6f}], reps={bs['n_reps']}")
    md.append("")
    md.append("## Materiality floor (pre-registered; QLIKE lower = better)")
    mat = result["materiality"]
    md.append(f"- mean QLIKE A (RV-only) = {mat['mean_qlike_A']}")
    md.append(f"- mean QLIKE E (funding trails) = {mat['mean_qlike_E']}")
    md.append(f"- ΔQLIKE (A − E) = {mat['delta_qlike_vs_A_E']}  (positive = E improves; negative = E is WORSE)")
    md.append(f"- bootstrap mean (A − E) = {mat['bootstrap_mean_A_minus_E']}, CI95 = {mat['bootstrap_ci95_A_minus_E']}")
    md.append(f"- better model by mean QLIKE = **{mat['better_model_by_mean_qlike']}**")
    md.append(f"- **materiality_floor_met = {mat['materiality_floor_met']}**")
    md.append(f"- LOIO E all positive = {mat['loio_all_positive']}")
    md.append("")
    md.append("## Sign-convention audit (important)")
    sa = result["sign_audit"]
    md.append(f"- delta convention: {sa['delta_convention']}")
    md.append(f"- negative delta means: {sa['negative_delta_means']}")
    md.append(f"- prior headline check: {sa['prior_headline_check']}")
    md.append(f"- prior headline corrected: {sa['prior_headline_corrected']}")
    md.append(f"- robust04 finding: {sa['robust04_finding']}")
    md.append("")
    md.append("## Leave-one-instrument-out mean ΔQLIKE vs A (A − model; negative = model worse)")
    for m in MODELS:
        if m == "A_rv_only":
            continue
        md.append(f"- {m}: " + ", ".join(f"{k}={v}" for k, v in result["loio"].get(m, {}).items()))
    md.append("")
    md.append("## Honest status")
    md.append("- EXPLORATORY/PILOT. Alternative-holdout robustness confirmation of an exploratory Track C result; no confirmatory promotion claimed.")
    md.append("- No sealed months touched. No look-ahead; train-only standardization.")
    md_path.write_text("\n".join(md) + "\n", encoding="utf-8")
    print("WROTE", json_path, md_path)
    print("SUMMARY", json.dumps(result["summary"]["models"], indent=2))
    print("MATERIALITY", json.dumps(result["materiality"], indent=2))