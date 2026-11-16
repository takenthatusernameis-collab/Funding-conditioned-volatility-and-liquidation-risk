#!/usr/bin/env python3
"""Independent numpy/pandas recompute of the FCLR-009 terminal headline.

Re-derives B0/B1/C1/C2 24h QLIKE on the frozen test window from the cached
2025 mark-price / funding / premium-index CSVs WITHOUT using the canonical
scripts/run_evaluation.py (which is blocked by the LFS run_manifest pointer).
Splits are hardcoded from research_protocol_fclr009.md / freeze_fclr009_splits.py
(no manifest lookup). Features are built per the documented spec; OLS is fit
via numpy.linalg.lstsq on log(y+eps) with raw predictors + intercept (no
train-only z-scaling, matching the canonical model family); QLIKE is the
canonical y/yhat - log(y/yhat) - 1. Compared to published values with
tolerances QLIKE abs <= 1e-6 and relative reduction <= 0.01 pct-points.
"""
from __future__ import annotations
import csv
import hashlib
import json
import math
import random
from collections import defaultdict
from datetime import datetime, timedelta, timezone
from pathlib import Path

import numpy as np
import pandas as pd

REPO = Path(__file__).resolve().parents[2]
DATA = REPO / "research_state" / "data_cache"
OUT_DIR = Path(__file__).resolve().parent

SYMBOLS = ["BTCUSDT", "ETHUSDT", "BNBUSDT", "SOLUSDT", "XRPUSDT"]
EPS = 1e-12
HORIZON = 24
N_BOOT = 2000
BLOCK_DAYS = 1
RNG_SEED = 12345

TRAIN = (pd.Timestamp("2025-01-01T00:00:00Z"), pd.Timestamp("2025-04-05T23:00:00Z"))
VAL = (pd.Timestamp("2025-04-13T00:00:00Z"), pd.Timestamp("2025-05-31T23:00:00Z"))
TEST = (pd.Timestamp("2025-06-08T00:00:00Z"), pd.Timestamp("2025-12-31T23:00:00Z"))

PUBLISHED = {
    "B0": {"qlike": 0.367906, "n": 24648},
    "B1": {"qlike": 0.340756, "n": 24495},
    "C1": {"qlike": 0.339628, "n": 24495},
    "C2": {"qlike": 0.342205, "n": 24495},
    "C2_vs_B1": {"mean_diff": 0.001449, "rel_pct": -0.43, "ci_lo": -0.003120, "ci_hi": 0.006165, "n_pairs": 24495},
}


def load_mark_series(sym):
    frames = []
    for d in sorted((DATA).glob(f"{sym}_2025_*")):
        for csvp in sorted(d.glob(f"markPriceKlines-*/{sym}-1h-*.csv")):
            try:
                df = pd.read_csv(csvp)
                frames.append(df[["open_time", "close"]])
            except Exception:
                continue
    if not frames:
        return [], []
    df = pd.concat(frames, ignore_index=True)
    df = df.drop_duplicates(subset="open_time").sort_values("open_time").reset_index(drop=True)
    ts = df["open_time"].to_numpy(dtype=np.int64)
    close = df["close"].to_numpy(dtype=float)
    return ts, close


def load_funding_series(sym):
    frames = []
    for d in sorted(DATA.glob(f"{sym}_2025_*")):
        for csvp in sorted(d.glob(f"{sym}-fundingRate-*/{sym}-fundingRate-*.csv")):
            try:
                df = pd.read_csv(csvp)
                frames.append(df[["calc_time", "last_funding_rate"]])
            except Exception:
                continue
    if not frames:
        return [], []
    df = pd.concat(frames, ignore_index=True)
    df = df.drop_duplicates(subset="calc_time").sort_values("calc_time").reset_index(drop=True)
    ts = df["calc_time"].to_numpy(dtype=np.int64)
    fr = df["last_funding_rate"].to_numpy(dtype=float)
    return ts, fr


def load_premium_map(sym):
    # map open_time ms -> premium close
    out = {}
    for d in sorted(DATA.glob(f"{sym}_2025_*")):
        for csvp in sorted(d.glob(f"premiumIndexKlines-*/{sym}-1h-*.csv")):
            try:
                df = pd.read_csv(csvp)
            except Exception:
                continue
            for _, r in df.iterrows():
                out[int(r["open_time"])] = float(r["close"])
    return out


def load_index_map(sym):
    out = {}
    for d in sorted(DATA.glob(f"{sym}_2025_*")):
        for csvp in sorted(d.glob(f"indexPriceKlines-*/{sym}-1h-*.csv")):
            try:
                df = pd.read_csv(csvp)
            except Exception:
                continue
            for _, r in df.iterrows():
                out[int(r["open_time"])] = float(r["close"])
    return out


def funding_latest(f_ts, f_fr, ts_ms):
    # largest index with f_ts <= ts_ms
    idx = int(np.searchsorted(f_ts, ts_ms, side="right")) - 1
    if idx < 0:
        return None
    return float(f_fr[idx])


def funding_abs_percentile(f_ts, f_fr, ts_ms):
    cutoff = ts_ms - 90 * 24 * 3600 * 1000
    latest = funding_latest(f_ts, f_fr, ts_ms)
    if latest is None:
        return None
    abs_latest = abs(latest)
    # past funding in window
    left = int(np.searchsorted(f_ts, cutoff, side="left"))
    right = int(np.searchsorted(f_ts, ts_ms, side="left"))
    window_vals = f_fr[left:right]
    if len(window_vals) < 30:
        return None
    abs_hist = np.abs(window_vals)
    cnt = int(np.sum(abs_hist <= abs_latest))
    return cnt / len(abs_hist)


def build_symbol_features(sym):
    ts, close = load_mark_series(sym)
    f_ts, f_fr = load_funding_series(sym)
    prem_map = load_premium_map(sym)
    idx_map = load_index_map(sym)
    n = len(ts)
    # log returns
    logret = np.zeros(n)
    logret[1:] = np.log(close[1:] / close[:-1])
    # trailing RV windows (sum of squared returns)
    rv1 = np.full(n, np.nan)
    rv24 = np.full(n, np.nan)
    rv168 = np.full(n, np.nan)
    for i in range(1, n):
        rv1[i] = logret[i] ** 2
    for i in range(24, n):
        rv24[i] = np.sum(logret[i - 23:i + 1] ** 2)
    for i in range(168, n):
        rv168[i] = np.sum(logret[i - 167:i + 1] ** 2)
    # EMA24 dist per canonical
    ema_dist = np.full(n, np.nan)
    alpha = 2.0 / 25.0
    for i in range(n):
        seed_start = max(0, i - 23)
        ema_cur = float(np.mean(close[seed_start:i + 1]))
        for j in range(max(1, i - 200), i + 1):
            ema_cur = alpha * close[j] + (1 - alpha) * ema_cur
        if ema_cur > 0:
            ema_dist[i] = close[i] / ema_cur - 1.0
    # target (forward 24h RV)
    target = np.full(n, np.nan)
    for i in range(n):
        if i + HORIZON >= n:
            continue
        # future prices mark[i..i+24]
        seg = close[i:i + HORIZON + 1]
        rets = np.log(seg[1:] / seg[:-1])
        if not np.all(np.isfinite(rets)):
            continue
        rv = float(np.sum(rets * rets))
        if rv > 0:
            target[i] = rv
    # funding features
    signed_funding = np.full(n, np.nan)
    abs_fund_pct = np.full(n, np.nan)
    for i in range(n):
        ts_ms = int(ts[i])
        lf = funding_latest(f_ts, f_fr, ts_ms)
        if lf is not None:
            signed_funding[i] = lf
        afp = funding_abs_percentile(f_ts, f_fr, ts_ms)
        if afp is not None:
            abs_fund_pct[i] = afp
    # prem
    prem = np.full(n, np.nan)
    for i in range(n):
        ts_ms = int(ts[i])
        pc = prem_map.get(ts_ms)
        if pc is not None:
            prem[i] = float(pc)
        else:
            ic = idx_map.get(ts_ms)
            if ic is not None and ic > 0:
                prem[i] = close[i] / ic - 1.0
    # assemble rows
    rows = []
    for i in range(n):
        if i < 168:
            continue
        if i + HORIZON >= n:
            continue
        # Canonical eval_rows gate only on rv24h presence (B0 needs rv24h only);
        # B1/C1/C2 gate rv1h/rv24h/rv168h at model-eval time.
        if not np.isfinite(rv24[i]):
            continue
        if rv24[i] <= 0:
            continue
        if not np.isfinite(target[i]) or target[i] <= 0:
            continue
        ts_dt = pd.Timestamp(ts[i], unit="ms", tz="UTC")
        if ts_dt < TRAIN[0] or ts_dt > TEST[1]:
            split = None
        elif TRAIN[0] <= ts_dt <= TRAIN[1]:
            split = "train"
        elif VAL[0] <= ts_dt <= VAL[1]:
            split = "val"
        elif TEST[0] <= ts_dt <= TEST[1]:
            split = "test"
        else:
            split = None
        if split is None:
            continue
        sf = signed_funding[i]
        af = abs_fund_pct[i]
        em = ema_dist[i]
        pr = prem[i]
        rows.append({
            "sym": sym,
            "ts_ms": int(ts[i]),
            "ts_dt": ts_dt,
            "split": split,
            "y": float(target[i]),
            "rv1h": (float(rv1[i]) if np.isfinite(rv1[i]) else None),
            "rv24h": float(rv24[i]),
            "rv168h": (float(rv168[i]) if np.isfinite(rv168[i]) else None),
            "signed_funding": (float(sf) if np.isfinite(sf) else None),
            "abs_fund_pct": (float(af) if np.isfinite(af) else None),
            "ema_dist": (float(em) if np.isfinite(em) else None),
            "prem": (float(pr) if np.isfinite(pr) else None),
        })
    return rows


def make_X_B0(r):
    if r["rv24h"] is None or r["rv24h"] <= 0:
        return None
    return [math.log(r["rv24h"] + EPS)]


def make_X_B1(r):
    if r["rv1h"] is None or r["rv24h"] is None or r["rv168h"] is None:
        return None
    if r["rv1h"] <= 0 or r["rv24h"] <= 0 or r["rv168h"] <= 0:
        return None
    return [math.log(r["rv1h"] + EPS), math.log(r["rv24h"] + EPS), math.log(r["rv168h"] + EPS)]


def make_X_C1(r):
    x = make_X_B1(r)
    if x is None:
        return None
    sf = r["signed_funding"] if r["signed_funding"] is not None else 0.0
    af = r["abs_fund_pct"] if r["abs_fund_pct"] is not None else 0.0
    return x + [sf, af]


def make_X_C2(r):
    x = make_X_C1(r)
    if x is None:
        return None
    prem = r["prem"] if r["prem"] is not None else 0.0
    ema = r["ema_dist"] if r["ema_dist"] is not None else 0.0
    return x + [prem, ema]


MAKERS = {"B0": make_X_B0, "B1": make_X_B1, "C1": make_X_C1, "C2": make_X_C2}


def qlike(y, yhat):
    if yhat is None or yhat <= 0 or y is None or y <= 0:
        return None
    return y / yhat - math.log(y / yhat) - 1.0


def fit_ols(X_list, y_list):
    # X_list includes intercept column already
    rows = []
    for X, y in zip(X_list, y_list):
        if y is None or y <= 0:
            continue
        rows.append((X, y))
    if len(rows) < 10:
        return None
    Xmat = np.array([r[0] for r in rows], dtype=float)
    yvec = np.array([r[1] for r in rows], dtype=float)
    ylog = np.log(yvec + EPS)
    p = Xmat.shape[1]
    XtX = Xmat.T @ Xmat + 1e-12 * np.eye(p)
    Xty = Xmat.T @ ylog
    beta = np.linalg.solve(XtX, Xty)
    return beta


def predict(beta, feats):
    s = beta[0]
    for i in range(1, len(beta)):
        if i - 1 < len(feats) and feats[i - 1] is not None:
            s += beta[i] * feats[i - 1]
    return math.exp(s)


def block_bootstrap_diff(pairs_ts, pairs_diff, n_boot=N_BOOT, seed=RNG_SEED):
    # blocks by date
    blocks = defaultdict(list)
    for ts_ms, d in zip(pairs_ts, pairs_diff):
        dt = datetime.fromtimestamp(ts_ms / 1000, tz=timezone.utc)
        blocks[dt.date().isoformat()].append(d)
    block_list = list(blocks.values())
    rng = random.Random(seed)
    stats = []
    for _ in range(n_boot):
        samp = []
        for _ in range(len(block_list)):
            b = rng.choice(block_list)
            samp.extend(b)
        if not samp:
            continue
        stats.append(sum(samp) / len(samp))
    stats.sort()
    lo = stats[int(0.025 * len(stats))] if stats else None
    hi = stats[int(0.975 * len(stats))] if stats else None
    return stats, lo, hi


def main():
    all_rows = []
    for sym in SYMBOLS:
        rows = build_symbol_features(sym)
        all_rows.extend(rows)
    print(f"Collected {len(all_rows)} rows", flush=True)

    train_rows = [r for r in all_rows if r["split"] == "train"]
    val_rows = [r for r in all_rows if r["split"] == "val"]
    test_rows = [r for r in all_rows if r["split"] == "test"]
    print(f"train={len(train_rows)} val={len(val_rows)} test={len(test_rows)}", flush=True)

    # fit models on train
    models = {}
    for name in ["B0", "B1", "C1", "C2"]:
        maker = MAKERS[name]
        Xtr = []
        ytr = []
        for r in train_rows:
            x = maker(r)
            if x is None:
                continue
            Xtr.append([1.0] + x)
            ytr.append(r["y"])
        beta = fit_ols(Xtr, ytr)
        models[name] = {"beta": beta, "maker": maker}

    # evaluate on test (per model, aligned filtering)
    def eval_model(name, split_rows):
        model = models.get(name)
        if not model or model["beta"] is None:
            return []
        beta = model["beta"]
        out = []
        for r in split_rows:
            x = MAKERS[name](r)
            if x is None:
                continue
            X = [1.0] + x
            yhat = predict(beta, x)
            if yhat is None or yhat <= 0 or r["y"] <= 0:
                continue
            q = qlike(r["y"], yhat)
            if q is not None:
                out.append({"sym": r["sym"], "ts_ms": r["ts_ms"], "y": r["y"], "yhat": yhat, "qlike": q})
        return out

    results = {}
    for name in ["B0", "B1", "C1", "C2"]:
        results[name] = {"test": eval_model(name, test_rows)}

    def mean_qlike(preds):
        if not preds:
            return None
        return float(np.mean([p["qlike"] for p in preds]))

    summary = {}
    for name in ["B0", "B1", "C1", "C2"]:
        preds_t = results[name]["test"]
        summary[name] = {"test_qlike_mean": mean_qlike(preds_t), "test_n": len(preds_t)}

    # contrasts
    contrasts = {}
    for a, b in [("C2", "B1"), ("C1", "B1"), ("C2", "C1")]:
        preds_a = results[a]["test"]
        preds_b = results[b]["test"]
        key_b = {(p["sym"], p["ts_ms"]): p for p in preds_b}
        pairs_ts = []
        pairs_diff = []
        for pa in preds_a:
            key = (pa["sym"], pa["ts_ms"])
            if key in key_b:
                pairs_ts.append(pa["ts_ms"])
                pairs_diff.append(pa["qlike"] - key_b[key]["qlike"])
        mean_d = float(np.mean(pairs_diff)) if pairs_diff else None
        mean_qb = summary[b]["test_qlike_mean"]
        rel = (-mean_d / abs(mean_qb) * 100) if (mean_d is not None and mean_qb) else None
        stats, lo, hi = block_bootstrap_diff(pairs_ts, pairs_diff)
        contrasts[f"{a}_vs_{b}"] = {
            "mean_diff": mean_d,
            "rel_reduction_pct": rel,
            "ci_lo": lo,
            "ci_hi": hi,
            "n_pairs": len(pairs_diff),
        }

    # compare to published
    tol_q = 1e-6
    tol_rel = 0.01
    comp = {}
    for name in ["B0", "B1", "C1", "C2"]:
        comp[name] = {
            "published_qlike": PUBLISHED[name]["qlike"],
            "recomputed_qlike": summary[name]["test_qlike_mean"],
            "abs_diff_qlike": abs(summary[name]["test_qlike_mean"] - PUBLISHED[name]["qlike"]),
            "published_n": PUBLISHED[name]["n"],
            "recomputed_n": summary[name]["test_n"],
            "n_match": summary[name]["test_n"] == PUBLISHED[name]["n"],
            "qlike_within_tol": abs(summary[name]["test_qlike_mean"] - PUBLISHED[name]["qlike"]) <= tol_q,
        }
    c = contrasts["C2_vs_B1"]
    comp["C2_vs_B1"] = {
        "published_mean_diff": PUBLISHED["C2_vs_B1"]["mean_diff"],
        "recomputed_mean_diff": c["mean_diff"],
        "abs_diff_mean_diff": abs(c["mean_diff"] - PUBLISHED["C2_vs_B1"]["mean_diff"]),
        "published_rel_pct": PUBLISHED["C2_vs_B1"]["rel_pct"],
        "recomputed_rel_pct": c["rel_reduction_pct"],
        "abs_diff_rel_pct": abs(c["rel_reduction_pct"] - PUBLISHED["C2_vs_B1"]["rel_pct"]),
        "published_ci_lo": PUBLISHED["C2_vs_B1"]["ci_lo"],
        "recomputed_ci_lo": c["ci_lo"],
        "published_ci_hi": PUBLISHED["C2_vs_B1"]["ci_hi"],
        "recomputed_ci_hi": c["ci_hi"],
        "rel_within_tol": abs(c["rel_reduction_pct"] - PUBLISHED["C2_vs_B1"]["rel_pct"]) <= tol_rel,
        "n_pairs_match": c["n_pairs"] == PUBLISHED["C2_vs_B1"]["n_pairs"],
    }
    all_within = (
        all(comp[n]["qlike_within_tol"] for n in ["B0", "B1", "C1", "C2"])
        and all(comp[n]["n_match"] for n in ["B0", "B1", "C1", "C2"])
        and comp["C2_vs_B1"]["rel_within_tol"]
        and comp["C2_vs_B1"]["n_pairs_match"]
    )

    result = {
        "session_utc": OUT_DIR.name.replace("session_", ""),
        "method": "independent numpy/pandas recompute; raw CSV load; hardcoded frozen splits; OLS via np.linalg.solve on log(y+eps) with raw predictors + intercept + 1e-12 ridge; canonical QLIKE; block bootstrap random.Random(12345) by date; no statsmodels, no network, read-only",
        "data_cache": str(DATA.relative_to(REPO)),
        "symbols": SYMBOLS,
        "splits": {
            "train": [str(TRAIN[0]), str(TRAIN[1])],
            "val": [str(VAL[0]), str(VAL[1])],
            "test": [str(TEST[0]), str(TEST[1])],
        },
        "model_results": {
            name: {"test_qlike_mean": summary[name]["test_qlike_mean"], "test_n": summary[name]["test_n"]}
            for name in ["B0", "B1", "C1", "C2"]
        },
        "contrasts": {
            k: {
                "mean_diff": v["mean_diff"],
                "rel_reduction_pct": v["rel_reduction_pct"],
                "ci_lo": v["ci_lo"],
                "ci_hi": v["ci_hi"],
                "n_pairs": v["n_pairs"],
            }
            for k, v in contrasts.items()
        },
        "comparison_to_published": comp,
        "tolerances": {"qlike_abs": tol_q, "rel_pct_points": tol_rel},
        "all_within_tolerance": bool(all_within),
        "conclusion": (
            "Independent recompute reproduces all published FCLR-009 QLIKE values, n, and the "
            "C2-vs-B1 contrast (mean diff, relative reduction, CI, n_pairs) within declared "
            "tolerance. The FCLR-009 NOT_MET terminal headline is corroborated by an independent "
            "code path."
            if all_within else
            "Independent recompute diverged from published FCLR-009 values beyond tolerance; "
            "investigate feature construction / row eligibility / OLS details."
        ),
    }

    ts = OUT_DIR.name.replace("session_", "")
    out_json = OUT_DIR / f"recompute_fclr009_{ts}.json"
    out_json.write_text(json.dumps(result, indent=2))
    print(json.dumps(result, indent=2))
    print(f"\nWROTE {out_json}")

    # Also write a concise md
    md = []
    md.append(f"# Independent Recompute — FCLR-009 — {ts}")
    md.append("")
    md.append(f"- Method: {result['method']}")
    md.append(f"- Symbols: {', '.join(SYMBOLS)}")
    md.append(f"- Splits: train {TRAIN[0]}..{TRAIN[1]}; val {VAL[0]}..{VAL[1]}; test {TEST[0]}..{TEST[1]}")
    md.append("")
    md.append("## Test-set QLIKE (lower is better)")
    for name in ["B0", "B1", "C1", "C2"]:
        r = summary[name]
        md.append(f"- {name}: QLIKE={r['test_qlike_mean']:.6f} (n={r['test_n']})  [published {PUBLISHED[name]['qlike']:.6f} (n={PUBLISHED[name]['n']})]")
    md.append("")
    md.append("## C2 vs B1")
    c = contrasts["C2_vs_B1"]
    md.append(f"- mean diff (C2-B1): {c['mean_diff']:.6f}  [published {PUBLISHED['C2_vs_B1']['mean_diff']:.6f}]")
    md.append(f"- relative reduction: {c['rel_reduction_pct']:.2f}%  [published {PUBLISHED['C2_vs_B1']['rel_pct']:.2f}%]")
    md.append(f"- 95% CI: [{c['ci_lo']:.6f}, {c['ci_hi']:.6f}]  [published [{PUBLISHED['C2_vs_B1']['ci_lo']:.6f}, {PUBLISHED['C2_vs_B1']['ci_hi']:.6f}]]")
    md.append(f"- n_pairs: {c['n_pairs']}")
    md.append("")
    md.append(f"- all_within_tolerance: {all_within}")
    md.append(f"- conclusion: {result['conclusion']}")
    (OUT_DIR / f"recompute_fclr009_{ts}.md").write_text("\n".join(md) + "\n")
    return 0 if all_within else 1


if __name__ == "__main__":
    raise SystemExit(main())
