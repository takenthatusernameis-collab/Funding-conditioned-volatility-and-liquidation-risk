#!/usr/bin/env python3
"""
FCLR-XSEC-001 Step 2: Within-hour RV persistence baseline.

Baseline: within-hour RV persistence. For each closed UTC hour t, split the 5
eligible perpetual contracts by their own rv1h at t (percentile rank within
hour, <= 0.5 = high_rv, > 0.5 = low_rv). Compare next-hour realized variance
(rv1h at t+1) of high-rv vs low-rv coins within the same hour. Same paired
within-hour structure as the funding-contrast evaluation.

Holdout NOT opened. Train-only normalization not applicable (no model fitting;
pure within-hour comparison). All inputs causal at t.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

import numpy as np
import pandas as pd

REPO = Path(__file__).resolve().parents[2]
PANEL = REPO / "research_state" / "fclr011_recompute_panel_20261115T234700Z.parquet"
PANEL_SHA256 = "41962f823e59de5989c7d854cb3180cad61a4cbc2f5f230133c41b321342c1f4"


def load_panel() -> pd.DataFrame:
    df = pd.read_parquet(PANEL)
    df["ts"] = pd.to_datetime(df["ts"], utc=True)
    df = df.sort_values(["coin", "ts"]).reset_index(drop=True)
    df["target_rv1h_t1"] = df.groupby("coin")["rv1h"].shift(-1)
    return df


def add_rv_groups(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df["rv_rank_within_hour"] = df.groupby("ts")["rv1h"].rank(
        method="average", ascending=False
    )
    n_coins = df.groupby("ts")["coin"].transform("nunique")
    df["rv_pct_within_hour"] = df["rv_rank_within_hour"] / n_coins
    df["rv_group"] = np.where(df["rv_pct_within_hour"] <= 0.5, "high_rv", "low_rv")
    return df


def paired_hourly_diff(df: pd.DataFrame) -> pd.DataFrame:
    stats = (
        df.groupby(["ts", "rv_group"])["target_rv1h_t1"]
        .agg(["mean", "count"])
        .reset_index()
    )
    if stats.empty:
        return stats
    pivot = stats.pivot(index="ts", columns="rv_group", values="mean")
    counts = stats.pivot(index="ts", columns="rv_group", values="count")
    pivot.columns.name = None
    counts.columns.name = None
    pivot = pivot.join(counts.add_suffix("_count"))
    cols = [c for c in pivot.columns if not str(c).endswith("_count")]
    if len(cols) < 2:
        return pivot.iloc[0:0].copy()
    high_col, low_col = sorted(cols)[0], sorted(cols)[1]
    pivot["diff"] = pivot[high_col] - pivot[low_col]
    both = pivot[pivot[high_col].notna() & pivot[low_col].notna()].copy()
    return both


def main() -> None:
    df = load_panel()
    actual_sha = hashlib.sha256(PANEL.read_bytes()).hexdigest()
    assert actual_sha == PANEL_SHA256, f"panel hash mismatch: {actual_sha}"

    df_eval = df[df["target_rv1h_t1"].notna()].copy()
    df_r = add_rv_groups(df_eval)
    both = paired_hourly_diff(df_r)

    diff = both["diff"].values
    n_hours = len(diff)
    mean_diff = float(diff.mean()) if n_hours > 0 else None
    std_diff = float(diff.std()) if n_hours > 0 else None
    pos_count = int((diff > 0).sum()) if n_hours > 0 else 0

    out = {
        "experiment_id": "FCLR-XSEC-001-20261120T175300Z",
        "session_utc": "20261120T175300Z",
        "panel_path": str(PANEL),
        "panel_sha256": PANEL_SHA256,
        "panel_hash_verified": actual_sha == PANEL_SHA256,
        "baseline": "within_hour_rv_persistence",
        "estimand": "next_hour_rv1h_diff_high_minus_low_rv",
        "outcome_data_inspected_before_freeze": False,
        "n_coins": 5,
        "coins": sorted(df["coin"].unique()),
        "ts_min": str(df_eval["ts"].min()),
        "ts_max": str(df_eval["ts"].max()),
        "n_hours_total": int(df_eval["ts"].nunique()),
        "n_rows_with_target": int(len(df_eval)),
        "n_hours_both_groups": n_hours,
        "mean_diff_high_minus_low": mean_diff,
        "std_diff": std_diff,
        "positive_diff_count": pos_count,
        "positive_diff_share": float(pos_count / n_hours) if n_hours > 0 else None,
        "holdout_opened": False,
        "normalization": "none (pure within-hour comparison, no model fitting)",
    }

    out_dir = REPO / "research_state" / "session_20261120T175300Z"
    out_path = out_dir / "fclr_xsec001_baselines_20261120T175300Z.json"
    with open(out_path, "w") as fh:
        json.dump(out, fh, indent=2)
    print(json.dumps(out, indent=2))


if __name__ == "__main__":
    main()
