#!/usr/bin/env python3
"""Independent FCLR-002/003 volatility recompute from the local 2024 cache.

The implementation deliberately does not import the canonical evaluation code,
read the LFS-backed run manifest, use the network, or write outside the session.
It reconstructs the frozen feature contract directly from the CSVs, fits OLS on
log(realized variance + 1e-12), evaluates canonical QLIKE, and uses the same
deterministic UTC-day block bootstrap seed for comparison.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
import random
from collections import defaultdict
from contextlib import contextmanager
from datetime import datetime, timedelta, timezone
from io import TextIOWrapper
from pathlib import Path
from zipfile import ZipFile

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

EXPERIMENTS = {
    "FCLR-002": {
        "train": ("2024-04-01T00:00:00Z", "2024-06-08T23:00:00Z"),
        "val": ("2024-06-16T00:00:00Z", "2024-07-15T23:00:00Z"),
        "test": ("2024-07-23T00:00:00Z", "2024-09-30T23:00:00Z"),
        "months": tuple(f"2024-{m:02d}" for m in range(1, 10)),
        "published": {
            "B0": {"qlike": 0.543471, "n": 8280},
            "B1": {"qlike": 0.487438, "n": 8274},
            "C1": {"qlike": 0.487455, "n": 8274},
            "C2": {"qlike": 0.442223, "n": 8274},
            "C2_vs_B1": {"mean_diff": -0.045215, "rel_pct": 9.28, "ci_lo": -0.097648, "ci_hi": -0.008788, "n_pairs": 8274},
            "C1_vs_B1": {"mean_diff": 0.000017, "rel_pct": -0.00, "ci_lo": -0.005982, "ci_hi": 0.006047, "n_pairs": 8274},
            "C2_vs_C1": {"mean_diff": -0.045232, "rel_pct": 9.28, "ci_lo": -0.098089, "ci_hi": -0.009173, "n_pairs": 8274},
        },
    },
    "FCLR-003": {
        "train": ("2024-04-01T00:00:00Z", "2024-07-23T23:00:00Z"),
        "val": ("2024-07-31T00:00:00Z", "2024-09-24T23:00:00Z"),
        "test": ("2024-10-02T00:00:00Z", "2024-12-31T23:00:00Z"),
        "months": tuple(f"2024-{m:02d}" for m in range(1, 13)),
        "published": {
            "B0": {"qlike": 0.486931, "n": 10800},
            "B1": {"qlike": 0.400689, "n": 10796},
            "C1": {"qlike": 0.389589, "n": 10796},
            "C2": {"qlike": 0.444702, "n": 10796},
            "C2_vs_B1": {"mean_diff": 0.044013, "rel_pct": -10.98, "ci_lo": 0.001487, "ci_hi": 0.093225, "n_pairs": 10796},
            "C1_vs_B1": {"mean_diff": -0.011100, "rel_pct": 2.77, "ci_lo": -0.016972, "ci_hi": -0.005925, "n_pairs": 10796},
            "C2_vs_C1": {"mean_diff": 0.055113, "rel_pct": -14.15, "ci_lo": 0.009734, "ci_hi": 0.107156, "n_pairs": 10796},
        },
    },
}


def iso(s: str) -> pd.Timestamp:
    return pd.Timestamp(s)


def read_csv_auto(path: Path) -> pd.DataFrame:
    if path.suffix == ".zip":
        with ZipFile(path) as archive:
            members = [n for n in archive.namelist() if n.endswith(".csv")]
            if not members:
                raise ValueError(f"no csv in {path}")
            with archive.open(members[0]) as stream:
                return pd.read_csv(TextIOWrapper(stream))
    return pd.read_csv(path)


def csv_frames(sym: str, kind: str, spec: dict) -> list[pd.DataFrame]:
    frames = []
    for month in spec["months"]:
        y, m = month.split("-")
        base = DATA / f"{sym}_{y}_{int(m):02d}"
        if not base.exists():
            continue
        pattern = {
            "mark": f"markPriceKlines-*/{sym}-1h-*.csv",
            "funding": f"{sym}-fundingRate-*/{sym}-fundingRate-*.csv",
            "premium": f"premiumIndexKlines-*/{sym}-1h-*.csv",
            "index": f"indexPriceKlines-*/{sym}-1h-*.csv",
        }[kind]
        paths = sorted(base.glob(pattern))
        if not paths:
            suffix = {"mark": "csv", "funding": "csv", "premium": "csv", "index": "csv"}[kind]
            zip_patterns = {
                "mark": f"markPriceKlines-*/{sym}-1h-*.zip",
                "funding": f"{sym}-fundingRate-*/{sym}-fundingRate-*.zip",
                "premium": f"premiumIndexKlines-*/{sym}-1h-*.zip",
                "index": f"indexPriceKlines-*/{sym}-1h-*.zip",
            }
            paths = sorted(base.glob(zip_patterns[kind]))
        for path in paths:
            try:
                frame = read_csv_auto(path)
                if kind == "funding":
                    frames.append(frame[["calc_time", "last_funding_rate"]])
                else:
                    frames.append(frame[["open_time", "close"]])
            except Exception:
                continue
    return frames


def dedup_sorted(frames: list[pd.DataFrame], ts_col: str, value_col: str) -> tuple[np.ndarray, np.ndarray]:
    if not frames:
        return np.array([], dtype=np.int64), np.array([], dtype=float)
    df = pd.concat(frames, ignore_index=True).drop_duplicates(subset=ts_col).sort_values(ts_col)
    return df[ts_col].to_numpy(dtype=np.int64), df[value_col].to_numpy(dtype=float)


def latest_at(ts: np.ndarray, values: np.ndarray, target: int) -> float | None:
    idx = int(np.searchsorted(ts, target, side="right")) - 1
    return float(values[idx]) if idx >= 0 else None


def funding_percentile(ts: np.ndarray, values: np.ndarray, target: int) -> float | None:
    latest = latest_at(ts, values, target)
    if latest is None:
        return None
    left = int(np.searchsorted(ts, target - 90 * 24 * 3600 * 1000, side="left"))
    right = int(np.searchsorted(ts, target, side="left"))
    history = values[left:right]
    if len(history) < 30:
        return None
    return float(np.mean(np.abs(history) <= abs(latest)))


def map_values(frames: list[pd.DataFrame]) -> dict[int, float]:
    out: dict[int, float] = {}
    for frame in frames:
        for row in frame.itertuples(index=False):
            out[int(row.open_time)] = float(row.close)
    return out


def build_rows(sym: str, spec: dict) -> list[dict]:
    mark_ts, close = dedup_sorted(csv_frames(sym, "mark", spec), "open_time", "close")
    fund_ts, fund = dedup_sorted(csv_frames(sym, "funding", spec), "calc_time", "last_funding_rate")
    prem = map_values(csv_frames(sym, "premium", spec))
    index = map_values(csv_frames(sym, "index", spec))
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
    rows = []
    for i in range(168, len(mark_ts)):
        ts_ms = int(mark_ts[i])
        dt = pd.Timestamp(ts_ms, unit="ms", tz="UTC")
        split = None
        for name in ("train", "val", "test"):
            lo, hi = (iso(x) for x in spec[name])
            if lo <= dt <= hi:
                split = name
                break
        if i + HORIZON >= len(mark_ts):
            continue
        if split is None or not np.isfinite(rv24[i]) or rv24[i] <= 0:
            continue
        future = close[i:i + HORIZON + 1]
        if len(future) < HORIZON + 1:
            continue
        if len(future) < HORIZON + 1:
            continue
        returns = np.log(future[1:] / future[:-1])
        if not np.all(np.isfinite(returns)):
            continue
        target = float(np.sum(returns * returns))
        if target <= 0:
            continue
        sf = latest_at(fund_ts, fund, ts_ms)
        prem_value = prem.get(ts_ms)
        if prem_value is None:
            idx_value = index.get(ts_ms)
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


def features(row: dict, model: str) -> list[float] | None:
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


def fit(train: list[dict], model: str) -> np.ndarray | None:
    xrows, ys = [], []
    for row in train:
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


def predict(beta: np.ndarray, x: list[float]) -> float:
    return math.exp(float(np.r_[1.0, x] @ beta))


def qlike(y: float, yhat: float) -> float:
    return y / yhat - math.log(y / yhat) - 1.0


def bootstrap(pairs: list[tuple[int, float]]) -> tuple[float, float]:
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


def evaluate(experiment: str) -> dict:
    spec = EXPERIMENTS[experiment]
    all_rows = []
    for sym in SYMBOLS:
        all_rows.extend(build_rows(sym, spec))
    split_rows = {s: [r for r in all_rows if r["split"] == s] for s in ("train", "val", "test")}
    models = {name: fit(split_rows["train"], name) for name in ("B0", "B1", "C1", "C2")}
    evaluated = {}
    for name, beta in models.items():
        predictions = []
        if beta is None:
            evaluated[name] = []
            continue
        for row in split_rows["test"]:
            x = features(row, name)
            if x is None or row["y"] <= 0:
                continue
            yhat = predict(beta, x)
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
        contrasts[f"{a}_vs_{b}"] = {"mean_diff": mean, "rel_reduction_pct": -mean / abs(base) * 100 if mean is not None and base else None, "ci_lo": lo, "ci_hi": hi, "n_pairs": len(pairs)}
    published = spec["published"]
    comparison = {}
    for name in ("B0", "B1", "C1", "C2"):
        value = summary[name]["test_qlike_mean"]
        comparison[name] = {"published_qlike": published[name]["qlike"], "recomputed_qlike": value, "abs_diff_qlike": abs(value - published[name]["qlike"]) if value is not None else None, "published_n": published[name]["n"], "recomputed_n": summary[name]["test_n"], "n_match": summary[name]["test_n"] == published[name]["n"], "qlike_within_tol": value is not None and abs(value - published[name]["qlike"]) <= 1e-6}
    for name in ("C2_vs_B1", "C1_vs_B1", "C2_vs_C1"):
        value = contrasts[name]
        if value["mean_diff"] is None or value["rel_reduction_pct"] is None:
            comparison[name] = {"published_mean_diff": published[name]["mean_diff"], "recomputed_mean_diff": None, "abs_diff_mean_diff": None, "published_rel_pct": published[name]["rel_pct"], "recomputed_rel_pct": None, "abs_diff_rel_pct": None, "published_ci_lo": published[name]["ci_lo"], "recomputed_ci_lo": None, "published_ci_hi": published[name]["ci_hi"], "recomputed_ci_hi": None, "rel_within_tol": False, "n_pairs_match": False}
        else:
            comparison[name] = {"published_mean_diff": published[name]["mean_diff"], "recomputed_mean_diff": value["mean_diff"], "abs_diff_mean_diff": abs(value["mean_diff"] - published[name]["mean_diff"]), "published_rel_pct": published[name]["rel_pct"], "recomputed_rel_pct": value["rel_reduction_pct"], "abs_diff_rel_pct": abs(value["rel_reduction_pct"] - published[name]["rel_pct"]), "published_ci_lo": published[name]["ci_lo"], "recomputed_ci_lo": value["ci_lo"], "published_ci_hi": published[name]["ci_hi"], "recomputed_ci_hi": value["ci_hi"], "rel_within_tol": abs(value["rel_reduction_pct"] - published[name]["rel_pct"]) <= 0.01, "n_pairs_match": value["n_pairs"] == published[name]["n_pairs"]}
    all_within = all(comparison[n]["qlike_within_tol"] and comparison[n]["n_match"] for n in ("B0", "B1", "C1", "C2")) and all(comparison[n]["rel_within_tol"] and comparison[n]["n_pairs_match"] for n in ("C2_vs_B1", "C1_vs_B1", "C2_vs_C1"))
    test_start, test_end = (iso(x) for x in spec["test"])
    test_days = (test_end - test_start).days + 1
    gate_blocks = test_days // 30
    c2 = contrasts["C2_vs_B1"]
    result = {
        "session_utc": OUT_DIR.name.replace("session_", ""),
        "experiment": experiment,
        "method": "independent csv/pandas/numpy recompute; hardcoded frozen splits; OLS on log(y+1e-12) with intercept and 1e-12 ridge; canonical QLIKE; UTC-day block bootstrap seed 12345; no network, LFS, canonical evaluator, or sealed-artifact mutation",
        "splits": spec,
        "counts": {name: len(split_rows[name]) for name in split_rows},
        "model_results": summary,
        "contrasts": contrasts,
        "comparison_to_published": comparison,
        "all_within_tolerance": bool(all_within),
        "gate": {"primary_c2_vs_b1_rel_pass": c2["rel_reduction_pct"] is not None and c2["rel_reduction_pct"] >= 2.0, "primary_c2_vs_b1_ci_pass": c2["ci_hi"] is not None and c2["ci_hi"] < 0, "instruments": len(SYMBOLS), "test_days": test_days, "blocks_30d": gate_blocks, "blocks_pass": gate_blocks >= 3, "overall": "NOT_MET"},
    }
    result["conclusion"] = "Recomputed values are within tolerance." if all_within else "Recomputed values diverge beyond tolerance; the divergence is a finding, not a tuning target."
    return result


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("experiment", choices=sorted(EXPERIMENTS))
    parser.add_argument("--out-dir", type=Path, default=OUT_DIR)
    args = parser.parse_args()
    result = evaluate(args.experiment)
    ts = OUT_DIR.name.replace("session_", "")
    out_dir = args.out_dir
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / f"recompute_{args.experiment.lower().replace('-', '')}_{ts}.json").write_text(json.dumps(result, indent=2) + "\n")
    lines = [f"# Independent Recompute — {args.experiment} — {ts}", "", f"- Method: {result['method']}", f"- Counts: {result['counts']}", "", "## Test-set QLIKE"]
    for name in ("B0", "B1", "C1", "C2"):
        value = result["model_results"][name]
        published = result["comparison_to_published"][name]
        lines.append(f"- {name}: {value['test_qlike_mean']} (n={value['test_n']}); published {published['published_qlike']:.6f} (n={published['published_n']}); abs diff {published['abs_diff_qlike']}")
    lines.append("")
    for name in ("C2_vs_B1", "C1_vs_B1", "C2_vs_C1"):
        value = result["contrasts"][name]
        published = result["comparison_to_published"][name]
        lines.append(f"- {name}: diff={value['mean_diff']}, rel={value['rel_reduction_pct']}%, CI=[{value['ci_lo']},{value['ci_hi']}], n={value['n_pairs']}; published diff={published['published_mean_diff']:.6f}, rel={published['published_rel_pct']:.2f}%")
    lines.extend(["", f"- all_within_tolerance: {result['all_within_tolerance']}", f"- conclusion: {result['conclusion']}", f"- gate: {result['gate']}"])
    (out_dir / f"recompute_{args.experiment.lower().replace('-', '')}_{ts}.md").write_text("\n".join(lines) + "\n")
    print(json.dumps({"experiment": args.experiment, "out_dir": str(out_dir), "all_within_tolerance": result["all_within_tolerance"], "models": result["model_results"], "contrasts": result["contrasts"]}, indent=2))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())