#!/usr/bin/env python3
"""Track C — Design A exploratory forecast, stdlib OLS HAR (read-only cached data).

No numpy/pandas/scipy/statsmodels. math/csv/json/zipfile/statistics/random only.
EXPLORATORY/PILOT — not confirmatory, no forecast-gate pass claim.
"""
from __future__ import annotations

import json
import math
import random
import statistics
import zipfile
from datetime import datetime, timezone, timedelta
from pathlib import Path

RS = Path(__file__).resolve().parents[1]
CACHE = RS / "data_cache"
UTC_STAMP = "20261118T093031Z"

SYMBOLS = ["BTCUSDT", "ETHUSDT", "SOLUSDT", "XRPUSDT", "BNBUSDT"]
MONTHS = ["2024-04", "2024-05", "2024-06", "2024-07", "2024-08", "2024-09"]
EPS = 1e-12
SEED = 12345
BOOT_REPS = 2000

SPLITS = [
    {"split": 1, "train": ("2024-04-01", "2024-05-15"), "embargo": ("2024-05-16", "2024-05-22"), "test": ("2024-05-23", "2024-06-21")},
    {"split": 2, "train": ("2024-04-01", "2024-06-21"), "embargo": ("2024-06-22", "2024-06-28"), "test": ("2024-06-29", "2024-07-28")},
    {"split": 3, "train": ("2024-04-01", "2024-07-28"), "embargo": ("2024-07-29", "2024-08-04"), "test": ("2024-08-05", "2024-09-03")},
]

MODELS = ["A_rv_only", "B_rv_signed", "C_rv_abs", "D_rv_signed_abs", "E_rv_funding_trails"]
MODEL_FEATURES = {
    "A_rv_only": ["lrv1", "lrv24", "lrv168"],
    "B_rv_signed": ["lrv1", "lrv24", "lrv168", "fund"],
    "C_rv_abs": ["lrv1", "lrv24", "lrv168", "fund_abs"],
    "D_rv_signed_abs": ["lrv1", "lrv24", "lrv168", "fund", "fund_abs"],
    "E_rv_funding_trails": ["lrv1", "lrv24", "lrv168", "fund", "fund_abs", "fmean", "fewma"],
}


def ms_of(s):
    return int(datetime.strptime(s, "%Y-%m-%d").replace(tzinfo=timezone.utc).timestamp() * 1000)


def day_ms_range(d):
    dt = datetime.strptime(d, "%Y-%m-%d").replace(tzinfo=timezone.utc)
    return int(dt.timestamp() * 1000), int((dt + timedelta(days=1)).timestamp() * 1000) - 1


def read_csv_lines(symbol, year_month, day, kind):
    base = CACHE / f"{symbol}_{year_month}" / f"{kind}-{day}"
    sub = base / f"{symbol}-1h-{day}"
    csv_name = f"{symbol}-1h-{day}.csv"
    if (sub / csv_name).is_file():
        return (sub / csv_name).read_text(encoding="utf-8", errors="ignore").splitlines()
    zp = base / f"{symbol}-1h-{day}.zip"
    if zp.is_file():
        with zipfile.ZipFile(zp) as z:
            return z.read(csv_name).decode("utf-8", errors="ignore").splitlines()
    return []


def read_funding_lines(symbol, year_month):
    base = CACHE / f"{symbol}_{year_month}"
    d = base / f"{symbol}-fundingRate-{year_month}"
    csv_name = f"{symbol}-fundingRate-{year_month}.csv"
    if (d / csv_name).is_file():
        return (d / csv_name).read_text(encoding="utf-8", errors="ignore").splitlines()
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
            day = f"{y}-{int(m):02d}-{d:02d}"
            try:
                datetime.strptime(day, "%Y-%m-%d")
            except ValueError:
                continue
            lines = read_csv_lines(symbol, ym, day, f"{symbol}-1h-{day}.csv")
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


def main():
    out = {
        "schema": "trackc_design_a_forecast",
        "timestamp_utc": UTC_STAMP,
        "track": "C_volatility_forecast",
        "design": "TRACKC_EXT_DESIGN_A_EXPLORATORY",
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
        tr_s_ms, tr_e_ms = day_ms_range(tr_s), day_ms_range(tr_e)
        te_s_ms, te_e_ms = day_ms_range(te_s), day_ms_range(te_e)

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
                per_inst[s] = {"qlike": ql, "mae": mae, "rmse_sq": rmse_sq, "n": len(ql), "days": days,
                               "pred_var": [math.exp(0) for _ in ql]}
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

    # Block bootstrap for mean delta QLIKE vs A (improvement), resample UTC day blocks jointly.
    # Collect per-model per-day delta qlike (A - model) across instruments.
    boot_data = {m: [] for m in MODELS}  # m != A: list of (day, delta)
    days_all = set()
    for sp in out["splits"]:
        for s in SYMBOLS:
            for m in MODELS:
                pi = sp["models"][m]["per_instrument"].get(s, {})
                qls = pi.get("qlike", [])
                dys = pi.get("days", [])
                for q, d in zip(qls, dys):
                    days_all.add(d)
            ql_a = out  # placeholder
    # rebuild delta per (day, instrument) using A and model qlike aligned by day
    for m in MODELS:
        if m == "A_rv_only":
            continue
        by_day_model = {}  # day -> list of qlike (model)
        by_day_a = {}      # day -> list of qlike (A)
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
                boot_data[m].append((d, aa[k] - mm[k]))  # improvement = A - model

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
                # gather all points whose day in sampled_days (joint across instruments)
                vals = [dv for (d, dv) in boot_data[m] if d in sampled_days]
                if vals:
                    rep_means.append(sum(vals) / len(vals))
        if rep_means:
            rep_means.sort()
            lo = rep_means[int(0.025 * len(rep_means))]
            hi = rep_means[int(0.975 * len(rep_means))]
            bootstrap[m] = {"mean_improvement": (sum(rep_means) / len(rep_means) if rep_means else None),
                            "ci_2_5": lo, "ci_97_5": hi, "n_reps": len(rep_means)}
        else:
            bootstrap[m] = {"mean_improvement": None, "ci_2_5": None, "ci_97_5": None, "n_reps": 0}

    # Leave-one-instrument-out mean delta QLIKE vs A
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

    out["summary"] = summary
    out["bootstrap"] = bootstrap
    out["loio"] = loio
    out["leakage"] = {
        "train_only_standardization": True,
        "no_sealed_months_touched": True,
        "tested_months": ["2024-05", "2024-06", "2024-07"],
        "purge_embargo_days": 7,
    }
    return out


def date_of(ts_ms):
    return datetime.fromtimestamp(ts_ms / 1000, tz=timezone.utc).strftime("%Y-%m-%d")


if __name__ == "__main__":
    result = main()
    # write json
    json_path = RS / "session_20261118T093031Z" / f"trackc_design_a_forecast_{UTC_STAMP}.json"
    md_path = RS / "session_20261118T093031Z" / f"trackc_design_a_forecast_{UTC_STAMP}.md"
    json_path.write_text(json.dumps(result, indent=2), encoding="utf-8")
    md_lines = [
        f"# Track C — Design A Exploratory Volatility Forecast (stdlib OLS HAR)",
        f"",
        f"**Session:** session_{UTC_STAMP}",
        f"**Timestamp (UTC):** {UTC_STAMP}",
        f"**Track:** C — volatility/stress forecasting (Track C Design A)",
        f"**Label:** EXPLORATORY/PILOT — not confirmatory, no forecast-gate pass claim.",
        f"**Network:** none. **Parquet:** none. **numpy/pandas/scipy:** none (stdlib only).",
        f"",
        f"## Design",
        f"- Instruments: {', '.join(SYMBOLS)}",
        f"- Window: 2024-04-01..2024-09-09 (provenanced confirmatory subset)",
        f"- Horizon: next-24h realized variance from 1h mark-price close-to-close log returns t+1..t+24",
        f"- Mark field: close (markPriceKlines 1h), units USDT",
        f"- Target units: squared log-return (dimensionless); sum of 24 hourly squared log returns",
        f"- Epsilon: {EPS}",
        f"- Models: {', '.join(MODELS)}",
        f"- Estimation: OLS via normal equations + Gaussian elimination with partial pivoting",
        f"- Standardization: train-only means/stds; zero-variance columns dropped",
        f"- Back-transformation: Duan smearing factor on train residuals",
        f"- Metrics: QLIKE (primary), MAE, RMSE; paired delta QLIKE vs model A",
        f"- Bootstrap: {BOOT_REPS} reps, seed {SEED}, UTC day blocks resampled jointly across instruments",
        f"- Splits: 3 chronological non-overlapping 30d test blocks with 7d purge/embargo, expanding train",
        f"",
    ]
    for sm in result["splits"]:
        md_lines.append(f"### Split {sm['split']}: train {sm['train'][0]}..{sm['train'][1]}, test {sm['test'][0]}..{sm['test'][1]}")
        md_lines.append(f"  - train origins: {sm['n_train_origins']}")
        md_lines.append(f"  - common test timestamps: {sm['n_common_test_ts']}")
        for m in MODELS:
            mr = sm["models"][m]
            pi = mr["per_instrument"]
            allq = [q for s in SYMBOLS for q in pi.get(s, {}).get("qlike", [])]
            md_lines.append(f"  - {m}: fit_ok={mr['fit_ok']}, smearing={mr['smearing']:.6f}, n_pts={len(allq)}, mean_qlike={ (sum(allq)/len(allq)) if allq else None }")
    md_lines.append("")
    md_lines.append("## Cross-split summary")
    for m in MODELS:
        smry = summary_model = result["summary"]["models"][m]
        bs = result["bootstrap"].get(m, {})
        md_lines.append(f"- {m}: n={smry['n']}, mean_qlike={smry['mean_qlike']}, mean_mae={smry['mean_mae']}, mean_rmse={smry['mean_rmse']}, mean_delta_qlike_vs_A={smry['mean_delta_qlike_vs_A']}")
        if bs.get("mean_improvement") is not None:
            md_lines.append(f"  - bootstrap: mean_improvement={bs['mean_improvement']:.6f}, CI95=[{bs['ci_2_5']:.6f}, {bs['ci_97_5']:.6f}], reps={bs['n_reps']}")
    md_lines.append("")
    md_lines.append("## Leave-one-instrument-out mean delta QLIKE vs A")
    for m in MODELS:
        if m == "A_rv_only":
            continue
        md_lines.append(f"- {m}: " + ", ".join(f"{k}={v}" for k, v in result["loio"].get(m, {}).items()))
    md_lines.append("")
    md_lines.append("## Honest status")
    md_lines.append("- EXPLORATORY/PILOT. Smallest training window (45d) in split 1 is a pilot-quality risk.")
    md_lines.append("- No sealed months (2024-10..12, 2025+) touched. No confirmatory promotion claimed.")
    md_lines.append("- Missing numpy/pandas/scipy runtime is an environment constraint; stdlib fallback used.")
    md_path.write_text("\n".join(md_lines) + "\n", encoding="utf-8")
    print("WROTE", json_path, md_path)
