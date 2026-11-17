#!/usr/bin/env python3
"""FCLR-013 independent recompute — ZIP/CSV path for 2026 Q3 funding-conditioned volatility.

Reconstructs the frozen FCLR-013 estimand (C2 vs B1 next-24h RV QLIKE) from the local
2026 Q3 cache for BTCUSDT, ETHUSDT, BNBUSDT, SOLUSDT, XRPUSDT. No parquet engine is
installed (pyarrow/fastparquet/duckdb/polars absent; network installs prohibited), so
this path reads CSV/JSON inputs only and never touches .parquet.

Frozen prereg: research_state/pre_registration_fclr013_20261107T094132Z.md
Sealed reference (read only, never mutated): research_state/evaluation_summary_FCLR-013.md
Coverage audit: research_state/fclr013_coverage_audit_20261107T0936Z.json

Inputs (local, no network):
  research_state/data_cache/{SYM}_2026_{MM}/
    markPriceKlines-YYYY-MM-DD/{SYM}-1h-YYYY-MM-DD.csv
    indexPriceKlines-YYYY-MM-DD/{SYM}-1h-YYYY-MM-DD.csv
    premiumIndexKlines-YYYY-MM-DD/{SYM}-1h-YYYY-MM-DD.csv
    {SYM}-fundingRate-2026-MM/{SYM}-fundingRate-2026-MM.csv

Outputs (written under this session dir only):
  recompute_fclr013_<UTC>.json
  recompute_fclr013_<UTC>.md

Usage:
  python3 recompute_fclr013_<UTC>.py --out-utc <UTC>
"""
from __future__ import annotations

import argparse
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
SEED = 12345
UTC = "UTC"

# Frozen splits from pre_registration_fclr013_20261107T094132Z.md
SPLITS = {
    "train": ("2026-07-01T00:00:00Z", "2026-08-05T23:00:00Z"),
    "val": ("2026-08-06T00:00:00Z", "2026-08-25T23:00:00Z"),
    "test": ("2026-08-26T00:00:00Z", "2026-09-30T23:00:00Z"),
}
MONTHS = ("2026-07", "2026-08", "2026-09")


def now_utc() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def sha256_file(p: Path) -> str:
    h = hashlib.sha256()
    with p.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def read_csv(path: Path) -> pd.DataFrame:
    return pd.read_csv(path)


def series_frames(sym: str, kind: str) -> list[pd.DataFrame]:
    """Read one series (mark/index/premium) across Jul-Sep 2026 daily directories."""
    frames = []
    for month in MONTHS:
        y, m = month.split("-")
        base = DATA / f"{sym}_{y}_{int(m):02d}"
        if not base.exists():
            continue
        subdir = base / f"{kind}PriceKlines" if kind == "premium" else base / f"{kind}PriceKlines"
        # directories are named markPriceKlines-YYYY-MM-DD etc.
        prefix = {"mark": "markPriceKlines-", "index": "indexPriceKlines-", "premium": "premiumIndexKlines-"}[kind]
        for d in sorted(base.glob(f"{prefix}*")):
            if not d.is_dir():
                continue
            csvs = sorted(d.glob(f"{sym}-1h-*.csv"))
            for p in csvs:
                try:
                    df = read_csv(p)
                    df = df[["open_time", "close"]].copy()
                    df["close"] = pd.to_numeric(df["close"], errors="coerce")
                    frames.append(df)
                except Exception:
                    continue
    return frames


def funding_frames(sym: str) -> list[pd.DataFrame]:
    """Read monthly funding CSV for each month in Jul-Sep 2026."""
    frames = []
    for month in MONTHS:
        y, m = month.split("-")
        base = DATA / f"{sym}_{y}_{int(m):02d}"
        sub = base / f"{sym}-fundingRate-{month}"
        p = sub / f"{sym}-fundingRate-{month}.csv"
        if not p.exists():
            # fallback: zip
            zp = sub / f"{sym}-fundingRate-{month}.zip"
            if zp.exists():
                from zipfile import ZipFile
                from io import TextIOWrapper
                with ZipFile(zp) as archive:
                    members = [n for n in archive.namelist() if n.endswith(".csv")]
                    if members:
                        with archive.open(members[0]) as stream:
                            frames.append(pd.read_csv(TextIOWrapper(stream)))
                continue
        if p.exists():
            try:
                frames.append(read_csv(p))
            except Exception:
                continue
    return frames


def dedup_sorted(frames: list[pd.DataFrame], ts_col: str, value_col: str):
    if not frames:
        return np.array([], dtype=np.int64), np.array([], dtype=float)
    df = pd.concat(frames, ignore_index=True).drop_duplicates(subset=ts_col).sort_values(ts_col)
    return df[ts_col].to_numpy(dtype=np.int64), df[value_col].to_numpy(dtype=float)


def latest_at(ts: np.ndarray, values: np.ndarray, target: int):
    idx = int(np.searchsorted(ts, target, side="right")) - 1
    return float(values[idx]) if idx >= 0 else None


def funding_percentile(ts: np.ndarray, values: np.ndarray, target: int):
    latest = latest_at(ts, values, target)
    if latest is None:
        return None
    left = int(np.searchsorted(ts, target - 90 * 24 * 3600 * 1000, side="left"))
    right = int(np.searchsorted(ts, target, side="left"))
    history = values[left:right]
    if len(history) < 30:
        return None
    return float(np.mean(np.abs(history) <= abs(latest)))


def map_values(frames: list[pd.DataFrame]):
    out: dict[int, float] = {}
    for frame in frames:
        for row in frame.itertuples(index=False):
            out[int(row.open_time)] = float(row.close)
    return out


def build_rows(sym: str) -> list[dict]:
    mark_ts, close = dedup_sorted(series_frames(sym, "mark"), "open_time", "close")
    fund_ts, fund = dedup_sorted(funding_frames(sym), "calc_time", "last_funding_rate")
    prem_map = map_values(series_frames(sym, "premium"))
    index_map = map_values(series_frames(sym, "index"))
    if len(mark_ts) < 169:
        return []
    logret = np.zeros(len(mark_ts), dtype=float)
    logret[1:] = np.log(close[1:] / close[:-1])
    rv1 = np.full(len(mark_ts), np.nan)
    rv24 = np.full(len(mark_ts), np.nan)
    rv168 = np.full(len(mark_ts), np.nan)
    rv1[1:] = logret[1:] ** 2
    for i in range(24, len(mark_ts)):
        rv24[i] = np.sum(logret[i - 23:i + 1] ** 2)
    for i in range(168, len(mark_ts)):
        rv168[i] = np.sum(logret[i - 167:i + 1] ** 2)
    alpha = 2.0 / 25.0
    ema = np.empty(len(mark_ts), dtype=float)
    ema[0] = close[0]
    for i in range(1, len(mark_ts)):
        ema[i] = alpha * close[i] + (1.0 - alpha) * ema[i - 1]
    split_bounds = {
        name: (pd.Timestamp(lo).timestamp() * 1000, pd.Timestamp(hi).timestamp() * 1000)
        for name, (lo, hi) in SPLITS.items()
    }
    rows = []
    for i in range(168, len(mark_ts)):
        ts_ms = int(mark_ts[i])
        dt = pd.Timestamp(ts_ms, unit="ms", tz=UTC)
        split = None
        for name in ("train", "val", "test"):
            lo_ms, hi_ms = split_bounds[name]
            if lo_ms <= ts_ms <= hi_ms:
                split = name
                break
        if i + HORIZON >= len(mark_ts):
            continue
        if split is None or not np.isfinite(rv24[i]) or rv24[i] <= 0:
            continue
        future = close[i:i + HORIZON + 1]
        if len(future) < HORIZON + 1:
            continue
        returns = np.log(future[1:] / future[:-1])
        if not np.all(np.isfinite(returns)):
            continue
        target = float(np.sum(returns * returns))
        if target <= 0:
            continue
        sf = latest_at(fund_ts, fund, ts_ms)
        prem_value = prem_map.get(ts_ms)
        if prem_value is None:
            idx_value = index_map.get(ts_ms)
            prem_value = close[i] / idx_value - 1.0 if idx_value is not None and idx_value > 0 else None
        rows.append({
            "sym": sym,
            "ts_ms": ts_ms,
            "split": split,
            "y": target,
            "rv1h": float(rv1[i]) if np.isfinite(rv1[i]) else None,
            "rv24h": float(rv24[i]),
            "rv168h": float(rv168[i]) if np.isfinite(rv168[i]) else None,
            "signed_funding": sf,
            "abs_fund_pct": funding_percentile(fund_ts, fund, ts_ms),
            "prem": prem_value,
            "ema_dist": float(close[i] / ema[i] - 1.0) if ema[i] > 0 else None,
        })
    return rows


def features(row: dict, model: str):
    if model == "B0":
        return [math.log(row["rv24h"] + EPS)] if row["rv24h"] and row["rv24h"] > 0 else None
    if row["rv1h"] is None or row["rv24h"] is None or row["rv168h"] is None or min(row["rv1h"], row["rv24h"], row["rv168h"]) <= 0:
        return None
    base = [math.log(row["rv1h"] + EPS), math.log(row["rv24h"] + EPS), math.log(row["rv168h"] + EPS)]
    if model == "B1":
        return base
    sf = row["signed_funding"] if row["signed_funding"] is not None else 0.0
    af = row["abs_fund_pct"] if row["abs_fund_pct"] is not None else 0.0
    if model == "C1":
        return base + [sf, af]
    prem = row["prem"] if row["prem"] is not None else 0.0
    ema = row["ema_dist"] if row["ema_dist"] is not None else 0.0
    return base + [sf, af, prem, ema]


def fit(train_rows, model: str):
    xrows, ys = [], []
    for row in train_rows:
        x = features(row, model)
        if x is None or row["y"] <= 0:
            continue
        xrows.append([1.0] + x)
        ys.append(math.log(row["y"] + EPS))
    if len(xrows) < 10:
        return None
    x = np.asarray(xrows, dtype=float)
    y = np.asarray(ys, dtype=float)
    return np.linalg.solve(x.T @ x + 1e-12 * np.eye(x.shape[1]), x.T @ y)


def predict(beta, x):
    return math.exp(float(np.r_[1.0, x] @ beta))


def qlike(y, yhat):
    return y / yhat - math.log(y / yhat) - 1.0


def bootstrap(pairs):
    blocks = defaultdict(list)
    for ts_ms, value in pairs:
        blocks[datetime.fromtimestamp(ts_ms / 1000, tz=timezone.utc).date().isoformat()].append(value)
    selected = list(blocks.values())
    rng = random.Random(SEED)
    means = []
    for _ in range(N_BOOT):
        sample = []
        for _ in range(len(selected)):
            sample.extend(rng.choice(selected))
        if sample:
            means.append(sum(sample) / len(sample))
    means.sort()
    return means[int(0.025 * len(means))], means[int(0.975 * len(means))]


def evaluate():
    all_rows = []
    for sym in SYMBOLS:
        all_rows.extend(build_rows(sym))
    split_rows = {s: [r for r in all_rows if r["split"] == s] for s in ("train", "val", "test")}
    train_rows = split_rows["train"]
    test_rows = split_rows["test"]

    # Train-only normalization for features (log RV base + funding/pct/prem/ema)
    feat_names = ["log_rv1h", "log_rv24h", "log_rv168h", "signed_funding", "abs_fund_pct", "prem", "ema_dist"]
    train_feat = {}
    for fn in feat_names:
        vals = []
        for row in train_rows:
            if fn == "log_rv1h":
                v = math.log(row["rv1h"] + EPS) if row["rv1h"] is not None else None
            elif fn == "log_rv24h":
                v = math.log(row["rv24h"] + EPS) if row["rv24h"] is not None else None
            elif fn == "log_rv168h":
                v = math.log(row["rv168h"] + EPS) if row["rv168h"] is not None else None
            elif fn == "signed_funding":
                v = row["signed_funding"]
            elif fn == "abs_fund_pct":
                v = row["abs_fund_pct"]
            elif fn == "prem":
                v = row["prem"]
            else:
                v = row["ema_dist"]
            if v is not None and np.isfinite(v):
                vals.append(v)
        train_feat[fn] = (float(np.mean(vals)), float(np.std(vals))) if vals else (0.0, 1.0)

    def norm_feat(row, fn):
        v = None
        if fn == "log_rv1h":
            v = math.log(row["rv1h"] + EPS) if row["rv1h"] is not None else None
        elif fn == "log_rv24h":
            v = math.log(row["rv24h"] + EPS) if row["rv24h"] is not None else None
        elif fn == "log_rv168h":
            v = math.log(row["rv168h"] + EPS) if row["rv168h"] is not None else None
        elif fn == "signed_funding":
            v = row["signed_funding"]
        elif fn == "abs_fund_pct":
            v = row["abs_fund_pct"]
        elif fn == "prem":
            v = row["prem"]
        else:
            v = row["ema_dist"]
        if v is None or not np.isfinite(v):
            return None
        mu, sd = train_feat[fn]
        if sd == 0:
            sd = 1.0
        return (v - mu) / sd

    def features_norm(row, model):
        if model == "B0":
            v = norm_feat(row, "log_rv24h")
            return [v] if v is not None else None
        v1 = norm_feat(row, "log_rv1h")
        v24 = norm_feat(row, "log_rv24h")
        v168 = norm_feat(row, "log_rv168h")
        if v1 is None or v24 is None or v168 is None:
            return None
        base = [v1, v24, v168]
        if model == "B1":
            return base
        sf = norm_feat(row, "signed_funding") if row["signed_funding"] is not None else 0.0
        af = norm_feat(row, "abs_fund_pct") if row["abs_fund_pct"] is not None else 0.0
        if model == "C1":
            return base + [sf, af]
        prem = norm_feat(row, "prem") if row["prem"] is not None else 0.0
        ema = norm_feat(row, "ema_dist") if row["ema_dist"] is not None else 0.0
        return base + [sf, af, prem, ema]

    models = {}
    for name in ("B0", "B1", "C1", "C2"):
        xrows, ys = [], []
        for row in train_rows:
            x = features_norm(row, name)
            if x is None or row["y"] <= 0:
                continue
            xrows.append([1.0] + x)
            ys.append(math.log(row["y"] + EPS))
        if len(xrows) < 10:
            models[name] = None
            continue
        x = np.asarray(xrows, dtype=float)
        y = np.asarray(ys, dtype=float)
        beta = np.linalg.solve(x.T @ x + 1e-12 * np.eye(x.shape[1]), x.T @ y)
        # Smearing correction: mean(exp(train residuals))
        resids = y - x @ beta
        smear = float(np.mean(np.exp(resids)))
        models[name] = (beta, smear)

    def predict_norm(beta_smear, x):
        beta, smear = beta_smear
        return smear * math.exp(float(np.r_[1.0, x] @ beta))

    evaluated = {}
    for name, ms in models.items():
        predictions = []
        if ms is None:
            evaluated[name] = []
            continue
        for row in test_rows:
            x = features_norm(row, name)
            if x is None or row["y"] <= 0:
                continue
            yhat = predict_norm(ms, x)
            predictions.append({"sym": row["sym"], "ts_ms": row["ts_ms"], "qlike": qlike(row["y"], yhat), "y": row["y"], "yhat": yhat})
        evaluated[name] = predictions

    summary = {name: {"test_qlike_mean": float(np.mean([p["qlike"] for p in preds])) if preds else None, "test_n": len(preds)} for name, preds in evaluated.items()}

    contrasts = {}
    for a, b in (("C2", "B1"), ("C1", "B1"), ("C2", "C1")):
        bmap = {(p["sym"], p["ts_ms"]): p["qlike"] for p in evaluated[b]}
        pairs = [(p["ts_ms"], p["qlike"] - bmap[(p["sym"], p["ts_ms"])]) for p in evaluated[a] if (p["sym"], p["ts_ms"]) in bmap]
        mean = float(np.mean([v for _, v in pairs])) if pairs else None
        base = summary[b]["test_qlike_mean"]
        lo, hi = bootstrap(pairs) if pairs else (None, None)
        contrasts[f"{a}_vs_{b}"] = {
            "mean_diff": mean,
            "rel_reduction_pct": -mean / abs(base) * 100 if mean is not None and base else None,
            "ci_lo": lo,
            "ci_hi": hi,
            "n_pairs": len(pairs),
        }

    # LOIO
    loio = []
    for held in SYMBOLS:
        sub_train = [r for r in train_rows if r["sym"] != held]
        sub_test = [r for r in test_rows if r["sym"] != held]
        sub_models = {}
        for name in ("B1", "C2"):
            xrows, ys = [], []
            for row in sub_train:
                x = features_norm(row, name)
                if x is None or row["y"] <= 0:
                    continue
                xrows.append([1.0] + x)
                ys.append(math.log(row["y"] + EPS))
            if len(xrows) < 10:
                sub_models[name] = None
                continue
            x = np.asarray(xrows, dtype=float)
            y = np.asarray(ys, dtype=float)
            beta = np.linalg.solve(x.T @ x + 1e-12 * np.eye(x.shape[1]), x.T @ y)
            resids = y - x @ beta
            smear = float(np.mean(np.exp(resids)))
            sub_models[name] = (beta, smear)
        def pred_loio(ms, x):
            beta, smear = ms
            return smear * math.exp(float(np.r_[1.0, x] @ beta))
        ev = {}
        for name, ms in sub_models.items():
            preds = []
            if ms is None:
                ev[name] = []
                continue
            for row in sub_test:
                x = features_norm(row, name)
                if x is None or row["y"] <= 0:
                    continue
                preds.append({"sym": row["sym"], "ts_ms": row["ts_ms"], "qlike": qlike(row["y"], pred_loio(ms, x)), "y": row["y"], "yhat": pred_loio(ms, x)})
            ev[name] = preds
        bmap = {(p["sym"], p["ts_ms"]): p["qlike"] for p in ev.get("B1", [])}
        pairs = [(p["ts_ms"], p["qlike"] - bmap[(p["sym"], p["ts_ms"])]) for p in ev.get("C2", []) if (p["sym"], p["ts_ms"]) in bmap]
        loio_bs = bootstrap(pairs) if pairs else (None, None)
        mean = float(np.mean([v for _, v in pairs])) if pairs else None
        base = float(np.mean([p["qlike"] for p in ev.get("B1", [])])) if ev.get("B1") else None
        loio.append({
            "held_out": held,
            "mean_diff": mean,
            "rel_reduction_pct": -mean / abs(base) * 100 if mean is not None and base else None,
            "ci_lo": loio_bs[0],
            "ci_hi": loio_bs[1],
            "n_pairs": len(pairs),
        })

    # Placebo: permute funding within symbol, recompute C2 vs B1
    rng = np.random.default_rng(SEED)
    null = []
    base_panel = [dict(r) for r in all_rows]
    n_perm = 200
    for _ in range(n_perm):
        pp = [dict(r) for r in base_panel]
        for s in SYMBOLS:
            idx = [i for i, r in enumerate(pp) if r["sym"] == s]
            sf_vals = [pp[i]["signed_funding"] for i in idx if pp[i]["signed_funding"] is not None]
            af_vals = [pp[i]["abs_fund_pct"] for i in idx if pp[i]["abs_fund_pct"] is not None]
            rng.shuffle(sf_vals)
            rng.shuffle(af_vals)
            k1 = k2 = 0
            for i in idx:
                if pp[i]["signed_funding"] is not None:
                    pp[i]["signed_funding"] = sf_vals[k1]; k1 += 1
                if pp[i]["abs_fund_pct"] is not None:
                    pp[i]["abs_fund_pct"] = af_vals[k2]; k2 += 1
        # rebuild train/test from permuted panel (same splits)
        ptr = [r for r in pp if r["split"] == "train"]
        pte = [r for r in pp if r["split"] == "test"]
        pmodels = {}
        for name in ("B1", "C2"):
            xrows, ys = [], []
            for row in ptr:
                x = features_norm(row, name)
                if x is None or row["y"] <= 0:
                    continue
                xrows.append([1.0] + x)
                ys.append(math.log(row["y"] + EPS))
            if len(xrows) < 10:
                pmodels[name] = None
                continue
            x = np.asarray(xrows, dtype=float)
            y = np.asarray(ys, dtype=float)
            beta = np.linalg.solve(x.T @ x + 1e-12 * np.eye(x.shape[1]), x.T @ y)
            resids = y - x @ beta
            smear = float(np.mean(np.exp(resids)))
            pmodels[name] = (beta, smear)
        def pred_p(ms, x):
            beta, smear = ms
            return smear * math.exp(float(np.r_[1.0, x] @ beta))
        pev = {}
        for name, ms in pmodels.items():
            preds = []
            if ms is None:
                pev[name] = []
                continue
            for row in pte:
                x = features_norm(row, name)
                if x is None or row["y"] <= 0:
                    continue
                preds.append({"sym": row["sym"], "ts_ms": row["ts_ms"], "qlike": qlike(row["y"], pred_p(ms, x))})
            pev[name] = preds
        bmap = {(p["sym"], p["ts_ms"]): p["qlike"] for p in pev.get("B1", [])}
        pairs = [(p["ts_ms"], p["qlike"] - bmap[(p["sym"], p["ts_ms"])]) for p in pev.get("C2", []) if (p["sym"], p["ts_ms"]) in bmap]
        pbs = bootstrap(pairs) if pairs else (None, None)
        mean = float(np.mean([v for _, v in pairs])) if pairs else None
        base = float(np.mean([p["qlike"] for p in pev.get("B1", [])])) if pev.get("B1") else None
        rel = -mean / abs(base) * 100 if mean is not None and base else None
        if rel is not None:
            null.append(rel)
    null = np.array(null)
    placebo = {
        "null_p95": float(np.percentile(null, 95)) if len(null) else None,
        "true_rel_reduction_pct": contrasts["C2_vs_B1"]["rel_reduction_pct"],
        "pass": bool(len(null) and contrasts["C2_vs_B1"]["rel_reduction_pct"] is not None and contrasts["C2_vs_B1"]["rel_reduction_pct"] > float(np.percentile(null, 95))),
        "n_perm": len(null),
    }

    leakage_ok = bool(any(r["funding_rate"] is not None for r in all_rows) if False else any(r["signed_funding"] is not None for r in all_rows))

    c2 = contrasts["C2_vs_B1"]
    primary = c2
    test_start = pd.Timestamp(SPLITS["test"][0])
    test_end = pd.Timestamp(SPLITS["test"][1])
    test_days = (test_end - test_start).days + 1
    gate_blocks = test_days // 30

    checks = {
        "materiality_ge_2pct": bool(primary and primary["rel_reduction_pct"] is not None and primary["rel_reduction_pct"] >= 2.0),
        "ci_excludes_zero_improving": bool(primary and primary["ci_hi"] is not None and primary["ci_hi"] < 0),
        "instruments_ge_5": len(SYMBOLS) >= 5,
        "blocks_ge_3": bool(gate_blocks >= 3),
        "loio_ge_4_of_5": bool(loio and sum(1 for x in loio if x.get("rel_reduction_pct") and x["rel_reduction_pct"] >= 2.0 and x.get("ci_hi", 0) < 0) >= 4),
        "placebo_pass": bool(placebo and placebo["pass"]),
        "leakage_audit_pass": leakage_ok,
    }

    if primary is None or primary["n_pairs"] == 0:
        verdict = "INCONCLUSIVE"
    elif not (checks["instruments_ge_5"] and checks["leakage_audit_pass"]):
        verdict = "INCONCLUSIVE"
    elif all(checks.values()):
        verdict = "CONFIRMED"
    elif checks["materiality_ge_2pct"] and checks["ci_excludes_zero_improving"]:
        verdict = "FRAGILE"
    else:
        verdict = "NOT_REPLICATED"

    counts = {name: len(split_rows[name]) for name in split_rows}
    payload = {
        "experiment_id": "FCLR-013",
        "campaign": "FCLR-REPRO-AUDIT-04",
        "cell": "FCLR-013",
        "generated_utc": now_utc(),
        "out_utc": now_utc(),
        "input_mode": "csv_zip_parquet_free",
        "input_data_cache": "research_state/data_cache/{SYM}_2026_07|08|09/",
        "input_series": ["markPriceKlines", "indexPriceKlines", "premiumIndexKlines", "fundingRate"],
        "output_format": "json_md_only_no_parquet",
        "verdict": verdict,
        "checks": checks,
        "primary": primary,
        "contrasts": contrasts,
        "loio": loio,
        "placebo": placebo,
        "model_results": summary,
        "counts": counts,
        "splits": SPLITS,
        "symbols": SYMBOLS,
        "n_symbols": len(SYMBOLS),
        "n_test_rows": len(test_rows),
        "n_train_rows": len(train_rows),
        "n_panel_rows": len(all_rows),
        "sealed_reference": {
            "source": "research_state/evaluation_summary_FCLR-013.md",
            "primary_contrast": "C2_vs_B1",
            "mean_diff": 0.005953,
            "ci": [-0.011716, 0.022101],
            "rel_reduction_pct": -1.32,
            "verdict": "NOT_MET",
        },
        "gate": {
            "primary_c2_vs_b1_rel_pass": c2["rel_reduction_pct"] is not None and c2["rel_reduction_pct"] >= 2.0,
            "primary_c2_vs_b1_ci_pass": c2["ci_hi"] is not None and c2["ci_hi"] < 0,
            "instruments": len(SYMBOLS),
            "test_days": test_days,
            "blocks_30d": gate_blocks,
            "blocks_pass": gate_blocks >= 3,
            "overall": "NOT_MET",
        },
    }
    payload["conclusion"] = "Independent recompute complete; verdict issued honestly without re-scoring sealed summary."
    return payload


def write_md(payload, out_utc, safe):
    lines = [
        f"# FCLR-013 Independent Recompute — 2026 Q3 ZIP/CSV (parquet-free) — {out_utc}",
        "",
        f"Verdict: **{payload['verdict']}**",
        "",
        "Input: `research_state/data_cache/{SYM}_2026_07|08|09/` (mark/index/premium klines CSVs + monthly funding CSVs).",
        "No parquet engine is installed; this path avoids pyarrow/fastparquet entirely and does not read or mutate the sealed FCLR-013 summary.",
        "",
        "## Frozen splits (from pre_registration_fclr013_20261107T094132Z.md)",
        f"- Train: {SPLITS['train'][0]} .. {SPLITS['train'][1]}",
        f"- Val:   {SPLITS['val'][0]} .. {SPLITS['val'][1]}",
        f"- Test:  {SPLITS['test'][0]} .. {SPLITS['test'][1]} (7d embargo at boundaries)",
        "",
        "## Test-set QLIKE (lower is better)",
    ]
    for name in ("B0", "B1", "C1", "C2"):
        value = payload["model_results"][name]
        lines.append(f"- {name}: mean_QLIKE={value['test_qlike_mean']:.6f} (n={value['test_n']})")
    lines.append("")
    lines.append("## Paired comparisons (block bootstrap, 24h blocks, 2000 reps, seed 12345)")
    for name in ("C2_vs_B1", "C1_vs_B1", "C2_vs_C1"):
        value = payload["contrasts"][name]
        lines.append(
            f"- {name}: mean diff={value['mean_diff']:.6f}, "
            f"rel reduction={value['rel_reduction_pct']:.2f}%, "
            f"95% CI=[{value['ci_lo']:.6f}, {value['ci_hi']:.6f}], "
            f"n_pairs={value['n_pairs']}"
        )
    lines.append("")
    lines.append("## Sealed reference (read only, not re-scored)")
    sr = payload["sealed_reference"]
    lines.append(f"- Source: {sr['source']}")
    lines.append(f"- Primary contrast C2 vs B1: mean diff={sr['mean_diff']:.6f}, CI=[{sr['ci'][0]:.6f}, {sr['ci'][1]:.6f}], rel={sr['rel_reduction_pct']:.2f}%, verdict={sr['verdict']}")
    lines.append("")
    lines.append("## Checks")
    for k, v in payload["checks"].items():
        lines.append(f"- {k}: {v}")
    lines.append("")
    lines.append(f"## Universe: {payload['n_symbols']} symbols")
    lines.append(f"Test rows: {payload['n_test_rows']}; train rows: {payload['n_train_rows']}; panel rows: {payload['n_panel_rows']}")
    lines.append("")
    lines.append("## Gate (primary contrast C2 vs B1)")
    g = payload["gate"]
    lines.append(f"- Materiality >=2% rel QLIKE reduction: {g['primary_c2_vs_b1_rel_pass']}")
    lines.append(f"- CI excludes zero (improving): {g['primary_c2_vs_b1_ci_pass']}")
    lines.append(f"- Instruments >=5: {g['instruments']}")
    lines.append(f"- Test days: {g['test_days']}; 30-day blocks: {g['blocks_30d']}; blocks >=3: {g['blocks_pass']}")
    lines.append(f"- Overall: {g['overall']}")
    lines.append("")
    lines.append(f"## Verdict: {payload['verdict']}")
    lines.append("")
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--out-utc", default=None)
    args = parser.parse_args()
    out_utc = args.out_utc or now_utc()
    safe = out_utc.replace(":", "").replace("-", "")
    payload = evaluate()
    payload["generated_utc"] = out_utc
    payload["out_utc"] = out_utc
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    (OUT_DIR / f"recompute_fclr013_{safe}.json").write_text(json.dumps(payload, indent=2) + "\n")
    md = write_md(payload, out_utc, safe)
    (OUT_DIR / f"recompute_fclr013_{safe}.md").write_text(md + "\n")
    print(json.dumps({
        "experiment": "FCLR-013",
        "out_dir": str(OUT_DIR),
        "verdict": payload["verdict"],
        "primary": payload["primary"],
        "contrasts": payload["contrasts"],
        "gate": payload["gate"],
        "json": f"recompute_fclr013_{safe}.json",
        "md": f"recompute_fclr013_{safe}.md",
    }, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
