#!/usr/bin/env python3
"""
FCLR-XSEC-002 Step 2: Within-regime RV persistence baselines.

Baseline: within-regime RV persistence. For each closed UTC hour t, compute the
market-wide RV at t as the cross-sectional mean of coin rv1h across the 5
eligible coins. Split hours into high vs low market-wide-RV tercile. Within
each regime and hour, split coins by their own rv1h at t (percentile rank
within hour within regime, <= 0.5 = high_rv, > 0.5 = low_rv). Compare next-hour
realized variance (rv1h at t+1) of high-rv vs low-rv coins within the same hour
and regime. Same paired within-hour structure as the funding-contrast
evaluation, now computed per regime.

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
SESSION = "20261120T210000Z"
OUT_DIR = REPO / "research_state" / f"session_{SESSION}"


def load_panel() -> pd.DataFrame:
    df = pd.read_parquet(PANEL)
    df["ts"] = pd.to_datetime(df["ts"], utc=True)
    df = df.sort_values(["coin", "ts"]).reset_index(drop=True)
    df["target_rv1h_t1"] = df.groupby("coin")["rv1h"].shift(-1)
    return df


def add_market_wide_rv(df: pd.DataFrame) -> pd.DataFrame:
    """Market-wide RV at hour t = cross-sectional mean of coin rv1h at t."""
    df = df.copy()
    mw = df.groupby("ts")["rv1h"].agg(["mean", "count"]).rename(
        columns={"mean": "market_rv1h", "count": "market_rv1h_n"}
    )
    df = df.merge(mw, on="ts", how="left")
    # Hour is regime-eligible only if >= 3 coins have valid rv1h at t.
    df["hour_regime_eligible"] = df["market_rv1h_n"] >= 3
    return df


def add_regime(df: pd.DataFrame) -> pd.DataFrame:
    """Split regime-eligible hours into high vs low tercile by market-wide RV."""
    df = df.copy()
    eligible = df[df["hour_regime_eligible"]].copy()
    hour_mw = eligible.groupby("ts")["market_rv1h"].first()
    tercile_low = hour_mw.quantile(1 / 3)
    tercile_high = hour_mw.quantile(2 / 3)
    ts_to_regime = {}
    for ts, mv in hour_mw.items():
        if mv >= tercile_high:
            ts_to_regime[ts] = "high_rv_regime"
        elif mv <= tercile_low:
            ts_to_regime[ts] = "low_rv_regime"
        else:
            ts_to_regime[ts] = "mid_rv_regime"
    df["regime"] = df["ts"].map(ts_to_regime)
    return df, tercile_low, tercile_high


def add_rv_groups_within_regime(df: pd.DataFrame) -> pd.DataFrame:
    """Within each (ts, regime), rank coins by own rv1h at t; split high/low."""
    df = df.copy()
    df["rv_rank_within_hour_regime"] = df.groupby(["ts", "regime"])["rv1h"].rank(
        method="average", ascending=False
    )
    n_coins = df.groupby(["ts", "regime"])["coin"].transform("nunique")
    df["rv_pct_within_hour_regime"] = df["rv_rank_within_hour_regime"] / n_coins
    df["rv_group"] = np.where(df["rv_pct_within_hour_regime"] <= 0.5, "high_rv", "low_rv")
    return df


def paired_hourly_diff(df: pd.DataFrame, group_col: str, target_col: str = "target_rv1h_t1") -> pd.DataFrame:
    stats = (
        df.groupby(["ts", group_col])[target_col]
        .agg(["mean", "count"])
        .reset_index()
    )
    if stats.empty:
        return stats
    pivot = stats.pivot(index="ts", columns=group_col, values="mean")
    counts = stats.pivot(index="ts", columns=group_col, values="count")
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
    df_eval = add_market_wide_rv(df_eval)
    df_eval = df_eval[df_eval["hour_regime_eligible"]].copy()
    df_eval, tercile_low, tercile_high = add_regime(df_eval)
    df_regimes = df_eval[df_eval["regime"].isin(["high_rv_regime", "low_rv_regime"])].copy()
    df_regimes = add_rv_groups_within_regime(df_regimes)

    results = {
        "experiment_id": "FCLR-XSEC-002-20261120T210000Z",
        "session_utc": SESSION,
        "panel_path": str(PANEL),
        "panel_sha256": PANEL_SHA256,
        "panel_hash_verified": actual_sha == PANEL_SHA256,
        "baseline": "within_regime_rv_persistence",
        "estimand": "next_hour_rv1h_diff_high_minus_low_rv_within_regime",
        "outcome_data_inspected_before_freeze": False,
        "n_coins": 5,
        "coins": sorted(df["coin"].unique()),
        "ts_min": str(df_eval["ts"].min()),
        "ts_max": str(df_eval["ts"].max()),
        "n_hours_total": int(df_eval["ts"].nunique()),
        "n_rows_with_target": int(len(df_eval)),
        "n_hours_regime_eligible": int(df_regimes["ts"].nunique()),
        "market_rv_tercile_low": float(tercile_low),
        "market_rv_tercile_high": float(tercile_high),
        "regimes": {},
    }

    for regime in ["high_rv_regime", "low_rv_regime"]:
        sub = df_regimes[df_regimes["regime"] == regime].copy()
        both = paired_hourly_diff(sub, "rv_group")
        diff = both["diff"].values
        n_hours = len(diff)
        mean_diff = float(diff.mean()) if n_hours > 0 else None
        std_diff = float(diff.std()) if n_hours > 0 else None
        pos_count = int((diff > 0).sum()) if n_hours > 0 else 0
        n_hours_in_regime = int(sub["ts"].nunique())
        n_rows_in_regime = int(len(sub))
        results["regimes"][regime] = {
            "n_hours_in_regime": n_hours_in_regime,
            "n_rows_with_target": n_rows_in_regime,
            "n_hours_both_rv_groups": n_hours,
            "mean_diff_high_minus_low_rv": mean_diff,
            "std_diff": std_diff,
            "positive_diff_count": pos_count,
            "positive_diff_share": float(pos_count / n_hours) if n_hours > 0 else None,
            "holdout_opened": False,
            "normalization": "none (pure within-hour comparison within regime, no model fitting)",
        }

    out_path = OUT_DIR / f"fclr_xsec002_baselines_{SESSION}.json"
    with open(out_path, "w") as fh:
        json.dump(results, fh, indent=2)
    print(json.dumps(results, indent=2))


if __name__ == "__main__":
    main()
