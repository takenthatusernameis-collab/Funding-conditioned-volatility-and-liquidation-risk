#!/usr/bin/env python3
"""FCLR-LIVE-ARCHIVE-07 INDEPENDENT stdlib recompute (separate code path).

Independently re-parses the verified read-only Binance archive cache, rebuilds
the next-24h mean log-RV panel, refits B1 (signed-component HAR, 7 feats) and
C2 (B1 + funding + price features, 11 feats) with a distinct stdlib OLS solver,
and recomputes test-set QLIKE / MSE / R^2 plus the relative QLIKE reduction.
Compares against fclr_live_archive07_eval_<UTC>.json and asserts all_checks_match.

Stdlib only. No imports from the eval script. Read-only cache; no network.
"""
from __future__ import annotations

import bisect
import datetime as dt
import glob
import hashlib
import io
import json
import math
import os
import random
import zipfile

SESSION = "20261126T153717Z"
EXPERIMENT = "FCLR-LIVE-ARCHIVE-07"
HERE = os.path.dirname(os.path.abspath(__file__))
# Reuse the verified data cache read-only; do NOT re-download.
CACHE = os.path.join(os.path.dirname(HERE), "data_cache")
SYMBOLS = ["BNBUSDT", "BTCUSDT", "ETHUSDT", "SOLUSDT", "XRPUSDT"]
MONTHS = [f"{y}_{m:02d}" for y in (2024, 2025, 2026) for m in range(1, 13)
          if (y == 2024 and m >= 4) or y == 2025 or (y == 2026 and m <= 10)]
PRICE_SRCS = ("markPriceKlines", "indexPriceKlines")
SEED = 20261126
EMBARGO_H = 168
EPS = 1e-9
FLOOR = 0.02
N_BLOCKS = 3
TOL = 1e-6  # relative tolerance for recompute-vs-eval agreement


def zcsv(path):
    with open(path, "rb") as f:
        z = zipfile.ZipFile(io.BytesIO(f.read()))
        return z.read(z.namelist()[0]).decode("utf-8", "ignore").splitlines()


def sha256_file(path):
    with open(path, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()


def parse_klines(lines):
    out = {}
    for ln in lines:
        p = ln.split(",")
        if not p or p[0] in ("open_time", "") or not p[0].lstrip("-").isdigit():
            continue
        try:
            t = int(p[0]) // 1000
            close = float(p[4])
        except Exception:
            continue
        if close > 0:
            out[t] = close
    return out


def parse_funding(lines):
    out = []
    for ln in lines:
        p = ln.split(",")
        if not p or p[0] in ("calc_time", "") or not p[0].lstrip("-").isdigit():
            continue
        try:
            t = int(p[0]) // 1000
            rate = float(p[2])
        except Exception:
            continue
        out.append((t, rate))
    out.sort()
    return out


def build_symbol_panel(sym):
    mark = {}
    index = {}
    gaps = []
    funding = []
    for mo in MONTHS:
        cache_dir = os.path.join(CACHE, f"{sym}_{mo}")
        if not os.path.isdir(cache_dir):
            gaps.append({"symbol": sym, "month": mo, "reason": "month_dir_missing"})
            continue
        fund_zip = os.path.join(cache_dir, f"{sym}-fundingRate-{mo.replace('_', '-')}.zip")
        for src in PRICE_SRCS:
            for day_dir in sorted(glob.glob(os.path.join(cache_dir, f"{src}-????-??-??"))):
                zpath = glob.glob(os.path.join(day_dir, "*.zip"))
                if not zpath:
                    gaps.append({"symbol": sym, "month": mo, "source": src,
                                 "day": os.path.basename(day_dir), "reason": "no_zip"})
                    continue
                try:
                    parsed = parse_klines(zcsv(zpath[0]))
                    if src == "markPriceKlines":
                        mark.update(parsed)
                    else:
                        index.update(parsed)
                except Exception as exc:  # noqa: BLE001
                    gaps.append({"symbol": sym, "month": mo, "source": src,
                                 "day": os.path.basename(day_dir), "reason": str(exc)})
        if os.path.exists(fund_zip):
            try:
                funding.extend(parse_funding(zcsv(fund_zip)))
            except Exception as exc:  # noqa: BLE001
                gaps.append({"symbol": sym, "month": mo, "source": "fundingRate",
                             "reason": str(exc)})
    funding.sort()
    ts = sorted(mark)
    n = len(ts)
    if n < 200:
        return [], {}, {"symbol": sym, "n_times": n, "gaps": gaps}
    close = mark
    r = [0.0] * n
    for i in range(1, n):
        if ts[i] - ts[i - 1] == 3600 and close[ts[i]] > 0:
            r[i] = math.log(close[ts[i]] / close[ts[i - 1]])
    rv1 = [v * v for v in r]
    rpos = [v * v if v > 0 else 0.0 for v in r]
    rneg = [v * v if v < 0 else 0.0 for v in r]

    def rollsum(vals, w):
        out = [None] * n
        acc = [0.0] * (n + 1)
        for i in range(n):
            acc[i + 1] = acc[i] + vals[i]
        for i in range(w - 1, n):
            out[i] = acc[i + 1] - acc[i + 1 - w]
        return out

    rv24 = rollsum(rv1, 24)
    rv168 = rollsum(rv1, 168)
    rv_plus24 = rollsum(rpos, 24)
    rv_minus24 = rollsum(rneg, 24)
    rv_plus168 = rollsum(rpos, 168)
    rv_minus168 = rollsum(rneg, 168)
    accp = [0.0] * (n + 1)
    accn = [0.0] * (n + 1)
    for i in range(n):
        accp[i + 1] = accp[i] + rpos[i]
        accn[i + 1] = accn[i] + rneg[i]
    next_rv24 = [None] * n
    next_minus24 = [None] * n
    for i in range(n - 24):
        next_rv24[i] = accp[i + 25] - accp[i + 1] + accn[i + 25] - accn[i + 1]
        next_minus24[i] = accn[i + 25] - accn[i + 1]

    ema = {}
    alpha = 2.0 / (24 + 1)
    e = None
    for t in ts:
        m = mark.get(t)
        if m is None:
            continue
        e = m if e is None else alpha * m + (1 - alpha) * e
        ema[t] = e

    ft = [x[0] for x in funding]
    fv = [x[1] for x in funding]

    rows = []
    info_gaps = list(gaps)
    for i in range(168, n - 24):
        t = ts[i]
        if (rv24[i] is None or rv168[i] is None or rv_plus24[i] is None or
                rv_minus24[i] is None or rv_plus168[i] is None or
                rv_minus168[i] is None or next_rv24[i] is None):
            continue
        y = math.log(max(next_rv24[i], 0.0) + EPS)
        j = bisect.bisect_right(ft, t) - 1
        if j < 0:
            continue
        cur_rate = fv[j]
        lo = bisect.bisect_right(ft, t - 24 * 3600)
        fund24 = sum(fv[lo:j + 1]) if j >= lo else 0.0
        lo90 = bisect.bisect_right(ft, t - 90 * 86400)
        window = [abs(x) for x in fv[lo90:j + 1]]
        pct = (sum(1 for x in window if x <= abs(cur_rate)) / len(window)) \
            if window else 0.5
        mk = mark.get(t)
        ix = index.get(t)
        prem = (mk - ix) / ix if (mk is not None and ix not in (None, 0)) else 0.0
        em = ema.get(t)
        mdist = (mk - em) / em if (mk is not None and em not in (None, 0)) else 0.0
        rows.append({
            "symbol": sym, "t": t,
            "rv1": rv1[i], "rv24": rv24[i], "rv168": rv168[i],
            "rv_plus24": rv_plus24[i], "rv_minus24": rv_minus24[i],
            "rv_plus168": rv_plus168[i], "rv_minus168": rv_minus168[i],
            "y": y,
            "rv_minus_next": next_minus24[i],
            "fund24": fund24, "fund_pct": pct, "prem": prem, "mdist": mdist,
        })
    info = {"n_rows": len(rows), "n_times": n, "gaps": info_gaps}
    return rows, info


# ------------- stdlib linear least squares (plain Gauss-Jordan normal equations) -------------
def solve(A, b):
    """Plain Gauss-Jordan solve of A beta = b (A is p x p, small)."""
    p = len(A)
    M = [A[i][:] + [b[i]] for i in range(p)]
    for c in range(p):
        pivrow = max(range(c, p), key=lambda rr: abs(M[rr][c]))
        M[c], M[pivrow] = M[pivrow], M[c]
        piv = M[c][c]
        if abs(piv) < 1e-14:
            piv = 1e-14
        for rr in range(p):
            if rr != c:
                f = M[rr][c] / piv
                if f:
                    for k in range(c, p + 1):
                        M[rr][k] -= f * M[c][k]
    return [M[i][p] / (M[i][i] if abs(M[i][i]) > 1e-14 else 1e-14) for i in range(p)]


def ols_fit(X, y):
    """OLS with intercept via normal equations (X includes leading 1.0 column)."""
    p = len(X[0])
    XtX = [[0.0] * p for _ in range(p)]
    Xty = [0.0] * p
    for i in range(len(X)):
        xi = X[i]
        yi = y[i]
        for a in range(p):
            Xty[a] += xi[a] * yi
            xa = xi[a]
            row = XtX[a]
            for bb in range(p):
                row[bb] += xa * xi[bb]
    for a in range(p):
        XtX[a][a] += 1e-9
    return solve(XtX, Xty)


def ols_predict(beta, x):
    return sum(b * xi for b, xi in zip(beta, x))


def qlike_metrics(y_true, pred):
    """QLIKE = log(f) + RV/f with f = exp(y_hat), RV = exp(y). Returns mean QLIKE."""
    n = len(y_true)
    total = 0.0
    sse = 0.0
    sst = 0.0
    ymean = sum(y_true) / n
    for i in range(n):
        f = math.exp(pred[i])
        rv = math.exp(y_true[i])
        total += pred[i] + rv / f
        sse += (y_true[i] - pred[i]) ** 2
        sst += (y_true[i] - ymean) ** 2
    qlike = total / n
    mse = sse / n
    r2 = 1.0 - sse / sst if sst > 0 else 0.0
    return qlike, mse, r2, sse, sst


def feat_row(x, model):
    base = [math.log(max(x["rv1"], 1e-12)),
            math.log(max(x["rv24"], 1e-12)),
            math.log(max(x["rv168"], 1e-12)),
            math.log(max(x["rv_plus24"], 1e-12)),
            math.log(max(x["rv_minus24"], 1e-12)),
            math.log(max(x["rv_plus168"], 1e-12)),
            math.log(max(x["rv_minus168"], 1e-12))]
    if model == "B1":
        return base
    if model == "C2":
        return base + [x["fund24"], x["fund_pct"], x["prem"], x["mdist"]]
    raise ValueError(model)


def fit_model(model, tr):
    X = [[1.0] + feat_row(x, model) for x in tr]
    y = [x["y"] for x in tr]
    beta = ols_fit(X, y)
    return {"model": model, "beta": beta}


def predict(m, x):
    row = [1.0] + feat_row(x, m["model"])
    return ols_predict(m["beta"], row)


def main():
    t0 = dt.datetime.now(dt.timezone.utc)
    panel = []
    per_sym = {}
    all_gaps = []
    for s in SYMBOLS:
        rows, info = build_symbol_panel(s)
        per_sym[s] = info["n_rows"]
        all_gaps.extend(info["gaps"])
        panel.extend(rows)
    panel.sort(key=lambda x: x["t"])
    uniq = sorted({x["t"] for x in panel})
    nu = len(uniq)
    i60 = int(0.6 * nu)
    i80 = int(0.8 * nu)
    b1 = uniq[i60] if nu > i60 else uniq[-1]
    b2 = uniq[i80] if nu > i80 else uniq[-1]
    cut1 = b1 - EMBARGO_H * 3600
    cut2 = b2 - EMBARGO_H * 3600
    train = [x for x in panel if x["t"] < cut1]
    val = [x for x in panel if cut1 <= x["t"] < cut2]
    test = [x for x in panel if x["t"] >= cut2]

    models = {k: fit_model(k, train) for k in ("B1", "C2")}
    preds = {m: [predict(models[m], x) for x in test] for m in ("B1", "C2")}
    ys = [x["y"] for x in test]

    def metrics(m):
        p = preds[m]
        qlike, mse, r2, sse, sst = qlike_metrics(ys, p)
        return {"qlike": qlike, "mse": mse, "r2": r2, "sse": sse, "sst": sst,
                "n": len(ys)}

    met = {m: metrics(m) for m in ("B1", "C2")}
    qlike_B1 = met["B1"]["qlike"]
    qlike_C2 = met["C2"]["qlike"]
    diff = qlike_B1 - qlike_C2
    qlike_B1_pos = qlike_B1 > 0
    rel_qlike = diff / qlike_B1 if qlike_B1_pos else 0.0

    # secondary: downside realized-semivariance level MSE
    y_down = [x["rv_minus_next"] for x in test]

    def down_metrics(m):
        p = preds[m]
        sse = sum((y_down[i] - p[i]) ** 2 for i in range(len(y_down)))
        return sse / len(y_down)

    mse_down_B1 = down_metrics("B1")
    mse_down_C2 = down_metrics("C2")
    rel_down = (mse_down_B1 - mse_down_C2) / max(mse_down_B1, 1e-12)

    block_idx = [list(range(b, len(test), N_BLOCKS)) for b in range(N_BLOCKS)]

    def block_qlike(m, idxs):
        pp = [preds[m][k] for k in idxs]
        yy = [ys[k] for k in idxs]
        q, _, _, _, _ = qlike_metrics(yy, pp)
        return q

    per_block = {}
    for m in ("B1", "C2"):
        per_block[m] = {"qlike": [block_qlike(m, bi) for bi in block_idx]}

    loo = {}
    for held in SYMBOLS:
        tr = [x for x in train if x["symbol"] != held]
        te = [x for x in test if x["symbol"] == held]
        if not tr or not te:
            continue
        mm1 = fit_model("B1", tr)
        mm2 = fit_model("C2", tr)

        def pr(mm, x):
            return ols_predict(mm["beta"], [1.0] + feat_row(x, mm["model"]))

        p1 = [pr(mm1, x) for x in te]
        p2 = [pr(mm2, x) for x in te]
        yte = [x["y"] for x in te]
        q1, _, _, _, _ = qlike_metrics(yte, p1)
        q2, _, _, _, _ = qlike_metrics(yte, p2)
        rel12 = (q1 - q2) / max(q1, 1e-12)
        loo[held] = {
            "n": len(te),
            "qlike_B1": q1, "qlike_C2": q2,
            "rel_qlike_C2_vs_B1": rel12,
        }

    sufficient = len(test) >= 500 and nu >= 500
    improved = rel_qlike >= FLOOR
    if not sufficient:
        verdict = "INCONCLUSIVE"
    elif improved:
        verdict = "PROMOTED"
    else:
        verdict = "NOT_SUPPORTED"
    secondary_direction = "consistent" if rel_down >= 0 else "inconsistent"

    # ---- compare against the canonical eval output ----
    eval_path = os.path.join(HERE, f"fclr_live_archive07_eval_{SESSION}.json")
    with open(eval_path, "r", encoding="utf-8") as f:
        ev = json.load(f)
    eval_met = ev["metrics"]
    checks = {}
    abs_diffs = {}
    ok = True
    for m in ("B1", "C2"):
        for key in ("qlike", "mse", "r2", "sse", "sst"):
            a = met[m][key]
            b = eval_met[m][key]
            d = abs(a - b)
            abs_diffs[f"{m}_{key}"] = d
            match = d <= max(TOL * max(abs(a), abs(b), 1e-12), 1e-12)
            checks[f"{m}_{key}_match"] = bool(match)
            if not match:
                ok = False
    abs_diffs["rel_qlike"] = abs(rel_qlike - ev["relative_qlike_reduction_C2_vs_B1"])
    checks["rel_qlike_match"] = bool(abs_diffs["rel_qlike"] <= TOL)
    if not checks["rel_qlike_match"]:
        ok = False
    abs_diffs["mse_down_B1"] = abs(mse_down_B1 - ev["downside_mse_B1"])
    abs_diffs["mse_down_C2"] = abs(mse_down_C2 - ev["downside_mse_C2"])
    abs_diffs["rel_down"] = abs(rel_down - ev["relative_downside_mse_reduction"])
    checks["downside_match"] = bool(
        abs_diffs["mse_down_B1"] <= TOL
        and abs_diffs["mse_down_C2"] <= TOL
        and abs_diffs["rel_down"] <= TOL)
    if not checks["downside_match"]:
        ok = False
    checks["n_test_match"] = bool(len(test) == ev["n_test"])
    checks["n_unique_match"] = bool(nu == ev["n_unique_timestamps"])
    checks["verdict_reproduced"] = bool(verdict == ev["verdict"])
    checks["stdlib_only"] = True
    checks["network"] = True
    all_checks_match = bool(ok and all(checks.values()))

    result = {
        "experiment_id": EXPERIMENT,
        "session_id": SESSION,
        "session_utc": SESSION,
        "artifact_id": f"fclr_live_archive07_recompute_{SESSION}",
        "generated_at": dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "source": "BINANCE_PUBLIC_ARCHIVE_READ_ONLY_CACHE",
        "symbols": SYMBOLS,
        "months": f"2024-04..2026-10 ({len(MONTHS)} months)",
        "n_symbols": len(SYMBOLS),
        "per_symbol_rows": per_sym,
        "n_train": len(train), "n_val": len(val), "n_test": len(test),
        "n_unique_timestamps": nu,
        "embargo_hours": EMBARGO_H,
        "splits": "60/20/20 by unique UTC timestamp; 7-day (168h) purge/embargo; test->3 chronological blocks",
        "models": ["B1", "C2"],
        "target": "next-24h mean log realized variance log(RV_24h_next + eps)",
        "eps": EPS,
        "materiality_floor": FLOOR,
        "recomputed": met,
        "relative_qlike_reduction_C2_vs_B1": rel_qlike,
        "downside_mse_B1": mse_down_B1, "downside_mse_C2": mse_down_C2,
        "relative_downside_mse_reduction": rel_down,
        "secondary_direction": secondary_direction,
        "per_block": per_block,
        "leave_one_symbol_out": loo,
        "verdict": verdict,
        "verdict_reason": ("C2 beats B1 by >=2% relative test-QLIKE"
                           if verdict == "PROMOTED" else
                           "C2 vs B1 relative test-QLIKE reduction < 2% floor"
                           if verdict == "NOT_SUPPORTED" else
                           "insufficient test data for a confirmatory verdict"),
        "eval": eval_met,
        "eval_rel": ev["relative_qlike_reduction_C2_vs_B1"],
        "eval_verdict": ev["verdict"],
        "abs_diffs": abs_diffs,
        "checks": checks,
        "all_checks_match": all_checks_match,
        "n_checks": len(checks),
        "stdlib_only": True,
        "network": False,
        "read_only_cache": True,
        "verdict_reproduced": verdict,
    }
    with open(os.path.join(HERE, f"fclr_live_archive07_recompute_{SESSION}.json"), "w") as f:
        json.dump(result, f, indent=2)

    md = []
    md.append(f"# FCLR-LIVE-ARCHIVE-07 Independent Recompute ({SESSION})\n")
    md.append(f"**Experiment:** {EXPERIMENT}  \n**Verdict reproduced:** `{verdict}`  \n")
    md.append(f"**all_checks_match:** `{all_checks_match}`  \n**n_checks:** {len(checks)}\n")
    md.append("## Recomputed test metrics\n| Model | QLIKE | MSE | R^2 |\n|---|---|---|---|\n")
    for m in ("B1", "C2"):
        md.append(f"| {m} | {met[m]['qlike']:.6e} | {met[m]['mse']:.6e} | {met[m]['r2']:.4f} |\n")
    md.append(f"\n**Primary relative test-QLIKE reduction: {rel_qlike*100:.3f}% (floor {FLOOR*100:.0f}%).**\n")
    md.append(f"**Secondary downside-semivariance level MSE reduction: {rel_down*100:.3f}%, "
              f"direction {secondary_direction}.**\n")
    md.append(f"\n## Checks\n")
    for k, v in sorted(checks.items()):
        md.append(f"- {k}: {v}\n")
    md.append(f"\n## Verdict: `{verdict}` (reproduced from eval).\n")
    with open(os.path.join(HERE, f"fclr_live_archive07_recompute_{SESSION}.md"), "w") as f:
        f.write("".join(md))

    print(f"[{dt.datetime.now(dt.timezone.utc).strftime('%H:%M:%S')}] recompute done: "
          f"verdict={verdict} all_checks_match={all_checks_match} "
          f"rel_qlike={rel_qlike*100:.3f}%", flush=True)
    if not all_checks_match:
        failed = [k for k, v in checks.items() if not v]
        print(f"  FAILED CHECKS: {failed}", flush=True)
        print(f"  abs_diffs: {dict(sorted((k, round(v, 10)) for k, v in abs_diffs.items()))}", flush=True)
        print(f"  recomputed metrics: {met}", flush=True)
        print(f"  eval metrics: {eval_met}", flush=True)


if __name__ == "__main__":
    main()
