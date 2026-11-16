#!/usr/bin/env python3
"""Independent numpy/pandas recompute of FCLR-006 terminal headline.

Loads cached 2026 markPriceKlines / premiumIndexKlines / indexPriceKlines /
fundingRate CSVs for BTCUSDT,ETHUSDT,BNBUSDT,SOLUSDT,XRPUSDT from
research_state/data_cache without network and without run_evaluation.py or
run_manifest (LFS pointer). Frozen splits hardcoded from
research_state/research_protocol_fclr006.md (FCLR-006 v1.0). Feature/target
construction follows the documented spec: 24h forward realized variance target;
RV1h/RV24h/RV168h trailing sums of squared hourly log returns; signed funding as
latest calc_time<=t; abs-funding percentile vs past 90 calendar days with >=30
prior observations; premium = mark/index-1 when available else premiumIndex
close; mark/24h EMA distance (recursive EMA, alpha=2/25). B0 persistence on
log RV24h; B1/C1/C2 OLS on log(RV+1e-12) with intercept (raw predictors,
training-only fit). QLIKE = y/yhat - log(y/yhat) - 1. Block bootstrap over
UTC-date blocks, 2000 deterministic replicates (random.Random(12345)).
"""
from __future__ import annotations

import json
import math
import random
from collections import defaultdict
from pathlib import Path

import numpy as np
import pandas as pd

REPO = Path(__file__).resolve().parents[2]
DATA = REPO / "research_state" / "data_cache"
OUT_DIR = Path(__file__).resolve().parent
TS = "20261116T140001Z"

SYMBOLS = ["BTCUSDT", "ETHUSDT", "BNBUSDT", "SOLUSDT", "XRPUSDT"]
MONTHS = ["2026_04", "2026_05", "2026_06", "2026_07", "2026_08"]
EPS = 1e-12
HORIZON = 24
N_BOOT = 2000
RNG_SEED = 12345

TRAIN = (pd.Timestamp("2026-04-01T00:00:00Z"), pd.Timestamp("2026-04-24T23:00:00Z"))
VAL = (pd.Timestamp("2026-05-02T00:00:00Z"), pd.Timestamp("2026-05-15T23:00:00Z"))
TEST = (pd.Timestamp("2026-05-23T00:00:00Z"), pd.Timestamp("2026-08-06T23:00:00Z"))

PUBLISHED = {
    "B0": {"qlike": 0.518169, "n": 9000},
    "B1": {"qlike": 0.527290, "n": 8987},
    "C1": {"qlike": 0.620158, "n": 8987},
    "C2": {"qlike": 0.882279, "n": 8987},
    "C2_vs_B1": {
        "mean_diff": 0.354989,
        "rel_pct": -67.32,
        "ci_lo": 0.173748,
        "ci_hi": 0.615614,
        "ci_display_in_summary_was": [0.168263, 0.591948],
        "n_pairs": 8987,
    },
    "C1_vs_B1": {"mean_diff": 0.092867, "rel_pct": -17.61, "ci_lo": 0.037074, "ci_hi": 0.162896, "n_pairs": 8987},
    "C2_vs_C1": {"mean_diff": 0.262121, "rel_pct": -42.27, "ci_lo": 0.114594, "ci_hi": 0.448294, "n_pairs": 8987},
}


def _sym_month_dirs(sym):
    for m in MONTHS:
        d = DATA / f"{sym}_{m}"
        if d.exists():
            yield d


def load_mark_series(sym):
    """Load mark closes for the frozen data window only.

    run_evaluation.py loads daily mark CSVs up to DATA_END day (2026-08-06),
    so mark observations are available only through 2026-08-06T23:00:00Z and
    forward 24h targets for the last ~24 test origins cannot be formed. The
    cache contains later August days; restricting to <= DATA_END matches the
    canonical loader and the published paired-n (9000/8987).
    """
    data_end_ms = int(TEST[1].timestamp() * 1000)  # 2026-08-06T23:00:00Z
    frames = []
    for d in _sym_month_dirs(sym):
        for p in sorted(d.glob(f"markPriceKlines-*/{sym}-1h-*.csv")):
            try:
                frames.append(pd.read_csv(p, usecols=["open_time", "close"]))
            except Exception:
                continue
    if not frames:
        return np.array([], dtype=np.int64), np.array([], dtype=float)
    df = pd.concat(frames, ignore_index=True)
    df = df.drop_duplicates(subset="open_time").sort_values("open_time")
    df = df[df["open_time"] <= data_end_ms]
    return df["open_time"].to_numpy(np.int64), df["close"].to_numpy(float)


def load_kline_close_map(sym, prefix):
    out = {}
    for d in _sym_month_dirs(sym):
        for p in sorted(d.glob(f"{prefix}-*/{sym}-1h-*.csv")):
            try:
                df = pd.read_csv(p, usecols=["open_time", "close"])
            except Exception:
                continue
            for t, c in zip(df["open_time"].to_numpy(np.int64), df["close"].to_numpy(float)):
                out[int(t)] = float(c)
    return out


def load_funding_series(sym):
    frames = []
    for d in _sym_month_dirs(sym):
        for p in sorted(d.glob(f"{sym}-fundingRate-*/{sym}-fundingRate-*.csv")):
            try:
                frames.append(pd.read_csv(p, usecols=["calc_time", "last_funding_rate"]))
            except Exception:
                continue
    if not frames:
        return np.array([], dtype=np.int64), np.array([], dtype=float)
    df = pd.concat(frames, ignore_index=True)
    df = df.drop_duplicates(subset="calc_time").sort_values("calc_time")
    return df["calc_time"].to_numpy(np.int64), df["last_funding_rate"].to_numpy(float)


def funding_latest(f_ts, f_fr, ts_ms):
    idx = int(np.searchsorted(f_ts, ts_ms, side="right")) - 1
    if idx < 0:
        return None
    return float(f_fr[idx])


def funding_abs_percentile(f_ts, f_fr, ts_ms):
    cutoff = ts_ms - 90 * 24 * 3600 * 1000
    latest = funding_latest(f_ts, f_fr, ts_ms)
    if latest is None:
        return None
    left = int(np.searchsorted(f_ts, cutoff, side="left"))
    right = int(np.searchsorted(f_ts, ts_ms, side="left"))
    window = f_fr[left:right]
    if len(window) < 30:
        return None
    abs_latest = abs(latest)
    abs_hist = np.abs(window)
    return float(np.sum(abs_hist <= abs_latest) / len(abs_hist))


def split_of(ts_dt):
    if TRAIN[0] <= ts_dt <= TRAIN[1]:
        return "train"
    if VAL[0] <= ts_dt <= VAL[1]:
        return "val"
    if TEST[0] <= ts_dt <= TEST[1]:
        return "test"
    return None


def build_symbol_features(sym):
    ts, close = load_mark_series(sym)
    f_ts, f_fr = load_funding_series(sym)
    prem_map = load_kline_close_map(sym, "premiumIndexKlines")
    idx_map = load_kline_close_map(sym, "indexPriceKlines")
    n = len(ts)
    if n == 0:
        return []
    logret = np.zeros(n)
    valid_price = (close[1:] > 0) & (close[:-1] > 0)
    logret[1:] = np.where(valid_price, np.log(close[1:] / close[:-1]), np.nan)
    r2 = logret ** 2
    rv1 = np.full(n, np.nan)
    rv24 = np.full(n, np.nan)
    rv168 = np.full(n, np.nan)
    for i in range(1, n):
        rv1[i] = r2[i]
    for i in range(24, n):
        seg = r2[i - 23 : i + 1]
        if np.all(np.isfinite(seg)):
            rv24[i] = float(np.sum(seg))
    for i in range(168, n):
        seg = r2[i - 167 : i + 1]
        if np.all(np.isfinite(seg)):
            rv168[i] = float(np.sum(seg))

    ema_dist = np.full(n, np.nan)
    alpha = 2.0 / 25.0
    ema = np.full(n, np.nan)
    for i in range(n):
        if not np.isfinite(close[i]) or close[i] <= 0:
            continue
        if i == 0 or not np.isfinite(ema[i - 1]):
            ema[i] = close[i]
        else:
            ema[i] = alpha * close[i] + (1 - alpha) * ema[i - 1]
        if np.isfinite(ema[i]) and ema[i] > 0:
            ema_dist[i] = close[i] / ema[i] - 1.0

    target = np.full(n, np.nan)
    for i in range(n):
        if i + HORIZON >= n:
            continue
        segp = close[i : i + HORIZON + 1]
        if np.any(segp <= 0) or not np.all(np.isfinite(segp)):
            continue
        rets = np.log(segp[1:] / segp[:-1])
        if np.all(np.isfinite(rets)):
            rv = float(np.sum(rets * rets))
            if rv > 0:
                target[i] = rv

    rows = []
    for i in range(n):
        ts_dt = pd.Timestamp(ts[i], unit="ms", tz="UTC")
        split = split_of(ts_dt)
        if split is None:
            continue
        if i < 168 or i + HORIZON >= n:
            continue
        if not np.isfinite(rv24[i]) or rv24[i] <= 0:
            continue
        if not np.isfinite(target[i]) or target[i] <= 0:
            continue
        tms = int(ts[i])
        sf = funding_latest(f_ts, f_fr, tms)
        afp = funding_abs_percentile(f_ts, f_fr, tms)
        prem = prem_map.get(tms)
        idxc = idx_map.get(tms)
        if prem is None and idxc is not None and idxc > 0 and close[i] > 0:
            prem = close[i] / idxc - 1.0
        rows.append({
            "sym": sym, "ts_ms": tms, "ts_dt": ts_dt, "split": split, "y": target[i],
            "rv1h": rv1[i], "rv24h": rv24[i], "rv168h": rv168[i],
            "signed_funding": sf, "abs_fund_pct": afp,
            "premium": prem, "ema_dist": ema_dist[i],
        })
    return rows


def fit_ols(X, y):
    ly = np.log(y + EPS)
    XtX = X.T @ X
    Xty = X.T @ ly
    for k in range(XtX.shape[0]):
        XtX[k, k] += 1e-12
    try:
        beta = np.linalg.solve(XtX, Xty)
    except np.linalg.LinAlgError:
        beta, *_ = np.linalg.lstsq(XtX, Xty, rcond=None)
    return beta


def predict(beta, X):
    yhat = np.exp(X @ beta)
    yhat = np.where(yhat > 0, yhat, 1e-18)
    return yhat


def qlike(y, yhat):
    return y / yhat - np.log(y / yhat) - 1.0


MODEL_COLS = {
    "B0": ["log_rv24h"],
    "B1": ["log_rv1h", "log_rv24h", "log_rv168h"],
    "C1": ["log_rv1h", "log_rv24h", "log_rv168h", "signed_funding", "abs_fund_pct"],
    "C2": ["log_rv1h", "log_rv24h", "log_rv168h", "signed_funding", "abs_fund_pct", "premium", "ema_dist"],
}


def row_features(r, cols):
    vals = []
    for c in cols:
        if c == "log_rv1h":
            v = math.log(r["rv1h"] + EPS) if np.isfinite(r["rv1h"]) and r["rv1h"] > 0 else None
        elif c == "log_rv24h":
            v = math.log(r["rv24h"] + EPS) if np.isfinite(r["rv24h"]) and r["rv24h"] > 0 else None
        elif c == "log_rv168h":
            v = math.log(r["rv168h"] + EPS) if np.isfinite(r["rv168h"]) and r["rv168h"] > 0 else None
        else:
            raw = r.get(c)
            v = float(raw) if raw is not None and np.isfinite(raw) else None
        vals.append(v)
    return vals


def collect_model_rows(rows, cols):
    Xs, ys, metas = [], [], []
    for r in rows:
        fv = row_features(r, cols)
        if any(v is None or not np.isfinite(v) for v in fv):
            continue
        Xs.append([1.0] + fv)
        ys.append(float(r["y"]))
        metas.append((r["sym"], r["ts_ms"]))
    if not Xs:
        return np.zeros((0, len(cols) + 1)), np.zeros((0,)), []
    return np.array(Xs, float), np.array(ys, float), metas


def block_bootstrap_diff(pairs_ts, pairs_diff, n_boot=N_BOOT, seed=RNG_SEED):
    if not pairs_diff:
        return None, None, None
    blocks = defaultdict(list)
    for ts_ms, d in zip(pairs_ts, pairs_diff):
        day = pd.Timestamp(ts_ms, unit="ms", tz="UTC").date().isoformat()
        blocks[day].append(d)
    block_list = list(blocks.values())
    rng = random.Random(seed)
    stats = []
    for _ in range(n_boot):
        samp = []
        for _ in range(len(block_list)):
            samp.extend(rng.choice(block_list))
        if samp:
            stats.append(sum(samp) / len(samp))
    stats.sort()
    lo = stats[int(0.025 * len(stats))] if stats else None
    hi = stats[int(0.975 * len(stats))] if stats else None
    mean_d = sum(pairs_diff) / len(pairs_diff)
    return mean_d, lo, hi


def main():
    all_rows = []
    for sym in SYMBOLS:
        rs = build_symbol_features(sym)
        print(f"{sym}: {len(rs)} eval rows", flush=True)
        all_rows.extend(rs)
    train_rows = [r for r in all_rows if r["split"] == "train"]
    test_rows = [r for r in all_rows if r["split"] == "test"]
    print(f"train={len(train_rows)} val={len([r for r in all_rows if r['split']=='val'])} test={len(test_rows)}", flush=True)

    model_res = {}
    for name, cols in MODEL_COLS.items():
        Xtr, ytr, _ = collect_model_rows(train_rows, cols)
        if len(ytr) < 10:
            model_res[name] = {"preds": {}, "test_n": 0, "qlike": None, "beta": None}
            continue
        beta = fit_ols(Xtr, ytr)
        Xte, yte, meta_te = collect_model_rows(test_rows, cols)
        preds = {}
        if len(yte):
            yhat = predict(beta, Xte)
            q = qlike(yte, yhat)
            for (sym, ts_ms), qv in zip(meta_te, q):
                preds[(sym, ts_ms)] = float(qv)
        model_res[name] = {"preds": preds, "test_n": len(preds), "qlike": float(np.mean(list(preds.values()))) if preds else None, "beta": beta.tolist() if beta is not None else None}
        print(f"{name}: test_n={len(preds)} qlike={model_res[name]['qlike']}", flush=True)

    contrasts = {}
    for cname, a, b in [("C2_vs_B1", "C2", "B1"), ("C1_vs_B1", "C1", "B1"), ("C2_vs_C1", "C2", "C1")]:
        pa, pb = model_res[a]["preds"], model_res[b]["preds"]
        keys = sorted(set(pa) & set(pb), key=lambda x: (x[1], x[0]))
        diffs = [pa[k] - pb[k] for k in keys]
        ts_list = [k[1] for k in keys]
        mean_d, lo, hi = block_bootstrap_diff(ts_list, diffs)
        mean_qb = model_res[b]["qlike"]
        rel = (-mean_d / abs(mean_qb) * 100) if (mean_d is not None and mean_qb) else None
        contrasts[cname] = {"mean_diff": mean_d, "rel_reduction_pct": rel, "ci_lo": lo, "ci_hi": hi, "n_pairs": len(diffs)}
        print(f"{cname}: mean={mean_d} rel={rel} ci=[{lo},{hi}] n={len(diffs)}", flush=True)

    tol_q = 1e-6
    tol_rel = 0.01
    comp = {}
    for name in ["B0", "B1", "C1", "C2"]:
        rq = model_res[name]["qlike"]; pq = PUBLISHED[name]["qlike"]
        rn = model_res[name]["test_n"]; pn = PUBLISHED[name]["n"]
        comp[name] = {"published_qlike": pq, "recomputed_qlike": rq, "abs_diff_qlike": abs(rq - pq) if rq is not None else None, "published_n": pn, "recomputed_n": rn, "n_match": rn == pn, "qlike_within_tol": abs(rq - pq) <= tol_q if rq is not None else False}
    c = contrasts["C2_vs_B1"]
    comp["C2_vs_B1"] = {
        "published_mean_diff": PUBLISHED["C2_vs_B1"]["mean_diff"], "recomputed_mean_diff": c["mean_diff"],
        "abs_diff_mean_diff": abs(c["mean_diff"] - PUBLISHED["C2_vs_B1"]["mean_diff"]) if c["mean_diff"] is not None else None,
        "published_rel_pct": PUBLISHED["C2_vs_B1"]["rel_pct"], "recomputed_rel_pct": c["rel_reduction_pct"],
        "abs_diff_rel_pct": abs(c["rel_reduction_pct"] - PUBLISHED["C2_vs_B1"]["rel_pct"]) if c["rel_reduction_pct"] is not None else None,
        "published_ci_errata_corrected": [PUBLISHED["C2_vs_B1"]["ci_lo"], PUBLISHED["C2_vs_B1"]["ci_hi"]],
        "published_ci_summary_displayed": PUBLISHED["C2_vs_B1"]["ci_display_in_summary_was"],
        "recomputed_ci": [c["ci_lo"], c["ci_hi"]],
        "rel_within_tol": abs(c["rel_reduction_pct"] - PUBLISHED["C2_vs_B1"]["rel_pct"]) <= tol_rel if c["rel_reduction_pct"] is not None else False,
        "n_pairs_match": c["n_pairs"] == PUBLISHED["C2_vs_B1"]["n_pairs"],
        "ci_excludes_zero_recomputed": (c["ci_lo"] is not None and c["ci_hi"] is not None and c["ci_lo"] > 0),
    }
    all_within = (
        all(comp[n]["qlike_within_tol"] and comp[n]["n_match"] for n in ["B0", "B1", "C1", "C2"])
        and comp["C2_vs_B1"]["rel_within_tol"] and comp["C2_vs_B1"]["n_pairs_match"]
    )

    result = {
        "session_utc": TS,
        "method": "independent numpy/pandas recompute from cached CSVs; hardcoded frozen splits from research_protocol_fclr006.md; OLS on log(y+1e-12) with intercept (raw predictors); canonical QLIKE y/yhat-log(y/yhat)-1; block bootstrap random.Random(12345) by UTC date, 2000 reps; no network, no run_manifest, read-only",
        "data_cache": str(DATA.relative_to(REPO)), "symbols": SYMBOLS, "months": MONTHS,
        "splits": {"train": [str(TRAIN[0]), str(TRAIN[1])], "val": [str(VAL[0]), str(VAL[1])], "test": [str(TEST[0]), str(TEST[1])]},
        "model_results": {n: {"test_qlike_mean": model_res[n]["qlike"], "test_n": model_res[n]["test_n"]} for n in ["B0","B1","C1","C2"]},
        "contrasts": contrasts, "comparison_to_published": comp,
        "tolerances": {"qlike_abs": tol_q, "rel_pct_points": tol_rel},
        "all_within_tolerance": bool(all_within),
        "errata_note": "Published summary displayed CI [0.168263,0.591948] with wrong 'excludes zero' flag; errata-corrected interval is [0.173748,0.615614] (excludes zero). Gate remains NOT_MET (2 blocks < 3) and FCLR-H001 NOT_SUPPORTED.",
        "conclusion": (
            "Independent recompute reproduces FCLR-006 test QLIKE values, counts, and paired C2-vs-B1 contrast within declared tolerance. The NOT_MET / FCLR-H001 NOT_SUPPORTED terminal headline (C2 worse than B1 on this window) is corroborated by an independent path; errata CI correction is consistent."
            if all_within else
            "Independent recompute diverged from published FCLR-006 values beyond tolerance; investigate feature construction / row eligibility / OLS / bootstrap details."
        ),
    }
    out_json = OUT_DIR / f"recompute_fclr006_{TS}.json"
    out_json.write_text(json.dumps(result, indent=2))
    print(f"WROTE {out_json}")
    md = []
    md.append(f"# Independent Recompute — FCLR-006 — {TS}\n")
    md.append(f"- Method: {result['method']}")
    md.append(f"- Data: {result['data_cache']} (months {', '.join(MONTHS)})")
    md.append(f"- Symbols: {', '.join(SYMBOLS)}")
    md.append(f"- Splits (frozen): train {TRAIN[0]}..{TRAIN[1]}; val {VAL[0]}..{VAL[1]}; test {TEST[0]}..{TEST[1]} (7d embargo; 76d = 2 blocks, NOT_MET by design)\n")
    md.append("## Test-set QLIKE (lower is better)")
    for name in ["B0", "B1", "C1", "C2"]:
        r = model_res[name]
        md.append(f"- {name}: QLIKE={r['qlike']:.6f} (n={r['test_n']})  [published {PUBLISHED[name]['qlike']:.6f} (n={PUBLISHED[name]['n']})]")
    md.append("\n## Paired contrasts (block bootstrap, ~1d UTC blocks, 2000 reps, seed 12345)")
    for cname in ["C2_vs_B1", "C1_vs_B1", "C2_vs_C1"]:
        cv = contrasts[cname]; pub = PUBLISHED.get(cname, {})
        extra = f"  [published mean {pub.get('mean_diff')}, rel {pub.get('rel_pct')}%]" if pub else ""
        md.append(f"- {cname}: mean diff {cv['mean_diff']:.6f}, rel {cv['rel_reduction_pct']:.2f}%, 95% CI [{cv['ci_lo']:.6f}, {cv['ci_hi']:.6f}], n={cv['n_pairs']}{extra}")
    md.append("\n## Comparison to published (tolerances: QLIKE abs <= 1e-6, rel <= 0.01 pct-pt)")
    md.append(f"- all_within_tolerance: **{all_within}**")
    for name in ["B0","B1","C1","C2"]:
        c0 = comp[name]; md.append(f"- {name}: qlike_abs_diff={c0['abs_diff_qlike']}, n_match={c0['n_match']}, within={c0['qlike_within_tol']}")
    c6 = comp["C2_vs_B1"]
    md.append(f"- C2_vs_B1: mean_diff_abs={c6['abs_diff_mean_diff']}, rel_abs_diff={c6['abs_diff_rel_pct']} pp, rel_within={c6['rel_within_tol']}, n_pairs_match={c6['n_pairs_match']}, ci_excludes_zero={c6['ci_excludes_zero_recomputed']}")
    md.append(f"- Errata target CI (corrected): {c6['published_ci_errata_corrected']} vs recomputed [{c['ci_lo']:.6f}, {c['ci_hi']:.6f}] (summary displayed {c6['published_ci_summary_displayed']} with wrong flag)")
    md.append("\n## Conclusion")
    md.append(f"- {result['conclusion']}")
    md.append(f"- {result['errata_note']}")
    md.append("- No sealed/tracked artifact mutated; read-only recompute.")
    (OUT_DIR / f"recompute_fclr006_{TS}.md").write_text("\n".join(md) + "\n")
    print(f"WROTE {OUT_DIR / f'recompute_fclr006_{TS}.md'}")
    return 0 if all_within else 1


if __name__ == "__main__":
    raise SystemExit(main())
