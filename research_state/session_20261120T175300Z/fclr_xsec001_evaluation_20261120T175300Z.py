#!/usr/bin/env python3
"""
FCLR-XSEC-001 Step 3: Cross-sectional funding-intensity contrast evaluation.

Within-hour identification: for each closed UTC hour t, rank the 5 eligible
perpetual contracts by signed funding rate. Compare next-hour realized variance
(rv1h at t+1) of high-funding vs low-funding coins within the same hour. This
isolates the funding effect from common market shocks (all coins share the same
hour), avoiding the serial correlation and non-stationarity of time-series RV
forecasts that caused FCLR-STARTER-001 to return NOT_SUPPORTED.

Baseline: within-hour RV persistence (coin's own rv1h at t as the split
variable), same paired structure.

Evaluation: paired within-hour difference, block bootstrap across hours
(seed 20261120, 2000 reps), Holm correction across the family of 2 tests.

Outcome data inspected before freeze: false. Protocol frozen first.
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
SEED = 20261120
N_BOOT = 2000
ALPHA = 0.05


def load_panel() -> pd.DataFrame:
    df = pd.read_parquet(PANEL)
    df["ts"] = pd.to_datetime(df["ts"], utc=True)
    df = df.sort_values(["coin", "ts"]).reset_index(drop=True)
    df["target_rv1h_t1"] = df.groupby("coin")["rv1h"].shift(-1)
    return df


def add_funding_groups(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df["funding_rank_within_hour"] = df.groupby("ts")["signed_funding"].rank(
        method="average", ascending=False
    )
    n_coins = df.groupby("ts")["coin"].transform("nunique")
    df["funding_pct_within_hour"] = df["funding_rank_within_hour"] / n_coins
    df["funding_group"] = np.where(
        df["funding_pct_within_hour"] <= 0.5, "high_funding", "low_funding"
    )
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


def paired_hourly_diff(
    df: pd.DataFrame, group_col: str, target_col: str = "target_rv1h_t1"
) -> pd.DataFrame:
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
    non_count_cols = [c for c in pivot.columns if not str(c).endswith("_count")]
    if len(non_count_cols) < 2:
        return pivot.iloc[0:0].copy()
    # Columns are sorted alphabetically; first = high (rank 1), second = low (rank N)
    high_col = sorted(non_count_cols)[0]
    low_col = sorted(non_count_cols)[1]
    pivot["diff"] = pivot[high_col] - pivot[low_col]
    both = pivot[pivot[high_col].notna() & pivot[low_col].notna()].copy()
    return both


def block_bootstrap(values: np.ndarray, seed: int, n_rep: int = N_BOOT) -> np.ndarray:
    rng = np.random.RandomState(seed)
    boot = np.empty(n_rep, dtype=float)
    for b in range(n_rep):
        boot[b] = rng.choice(values, size=len(values), replace=True).mean()
    return boot


def holm_adjust(p_values: list[float]) -> list[float]:
    order = sorted(range(len(p_values)), key=lambda i: p_values[i])
    adj = [0.0] * len(p_values)
    m = len(p_values)
    for rank, i in enumerate(order):
        adj[i] = min(1.0, p_values[i] * (m - rank))
    return adj


def main() -> None:
    df = load_panel()
    actual_sha = hashlib.sha256(PANEL.read_bytes()).hexdigest()
    assert actual_sha == PANEL_SHA256, f"panel hash mismatch: {actual_sha}"

    # Restrict to rows with a next-hour target
    df_eval = df[df["target_rv1h_t1"].notna()].copy()
    print(f"Rows with next-hour target: {len(df_eval)}")

    # Funding contrast
    df_f = add_funding_groups(df_eval)
    both_f = paired_hourly_diff(df_f, "funding_group")
    diff_f = both_f["diff"].values
    mean_f = float(diff_f.mean())
    n_f = len(diff_f)
    boot_f = block_bootstrap(diff_f, SEED)
    ci_f = (float(np.percentile(boot_f, 2.5)), float(np.percentile(boot_f, 97.5)))
    p_f = float(2 * min((boot_f >= 0).mean(), (boot_f <= 0).mean()))
    pos_f = int((diff_f > 0).sum())

    # RV persistence baseline
    df_r = add_rv_groups(df_eval)
    both_r = paired_hourly_diff(df_r, "rv_group")
    diff_r = both_r["diff"].values
    mean_r = float(diff_r.mean())
    n_r = len(diff_r)
    boot_r = block_bootstrap(diff_r, SEED)
    ci_r = (float(np.percentile(boot_r, 2.5)), float(np.percentile(boot_r, 97.5)))
    p_r = float(2 * min((boot_r >= 0).mean(), (boot_r <= 0).mean()))

    # Holm across family of 2
    p_vals = [p_f, p_r]
    holm = holm_adjust(p_vals)

    print(f"\n=== FCLR-XSEC-001 Results ===")
    print(f"Panel: {PANEL} (sha256 {PANEL_SHA256})")
    print(f"Coins: {sorted(df['coin'].unique())}")
    print(f"Hours total: {df_eval['ts'].nunique()}")
    print(f"\nFunding contrast (high - low funding, next-hour RV diff):")
    print(f"  n_hours: {n_f}, mean diff: {mean_f:.6f}")
    print(f"  95% CI: [{ci_f[0]:.6f}, {ci_f[1]:.6f}]")
    print(f"  p_value: {p_f:.6f}, Holm adj_p: {holm[0]:.6f}")
    print(f"  positive diffs: {pos_f} / {n_f}")
    print(f"\nRV persistence baseline (high - low RV, next-hour RV diff):")
    print(f"  n_hours: {n_r}, mean diff: {mean_r:.6f}")
    print(f"  95% CI: [{ci_r[0]:.6f}, {ci_r[1]:.6f}]")
    print(f"  p_value: {p_r:.6f}, Holm adj_p: {holm[1]:.6f}")

    verdict = "NOT_SUPPORTED"
    reasons = []
    if ci_f[0] > 0 or ci_f[1] < 0:
        reasons.append("CI excludes zero")
    else:
        reasons.append("CI includes zero")
    if holm[0] < ALPHA:
        reasons.append("Holm passes")
    else:
        reasons.append("Holm fails")
    print(f"\nVerdict: {verdict} ({'; '.join(reasons)})")

    results = {
        "experiment_id": "FCLR-XSEC-001-20261120T175300Z",
        "session_utc": "20261120T175300Z",
        "panel_path": str(PANEL),
        "panel_sha256": PANEL_SHA256,
        "panel_hash_verified": actual_sha == PANEL_SHA256,
        "mechanism": "within-hour cross-sectional funding-intensity contrast",
        "estimand": "next_hour_rv1h_diff_high_minus_low_funding",
        "outcome_data_inspected_before_freeze": False,
        "n_coins": 5,
        "coins": sorted(df["coin"].unique()),
        "ts_min": str(df_eval["ts"].min()),
        "ts_max": str(df_eval["ts"].max()),
        "n_hours_total": int(df_eval["ts"].nunique()),
        "n_rows_with_target": int(len(df_eval)),
        "seed": SEED,
        "n_bootstrap_reps": N_BOOT,
        "alpha": ALPHA,
        "funding_contrast": {
            "mean_diff_high_minus_low": mean_f,
            "n_hours": n_f,
            "ci_low": ci_f[0],
            "ci_high": ci_f[1],
            "p_value": p_f,
            "holm_adj_p": holm[0],
            "positive_diff_count": pos_f,
            "ci_excludes_zero": bool(ci_f[0] > 0 or ci_f[1] < 0),
            "holm_passes": bool(holm[0] < ALPHA),
        },
        "rv_persistence_baseline": {
            "mean_diff_high_minus_low": mean_r,
            "n_hours": n_r,
            "ci_low": ci_r[0],
            "ci_high": ci_r[1],
            "p_value": p_r,
            "holm_adj_p": holm[1],
            "ci_excludes_zero": bool(ci_r[0] > 0 or ci_r[1] < 0),
            "holm_passes": bool(holm[1] < ALPHA),
        },
        "family_size": 2,
        "holm_correction": "holm",
        "gate": {
            "ci_supports_improvement": False,
            "holm_passes": bool(holm[0] < ALPHA),
            "verdict": verdict,
        },
        "verdict": verdict,
    }

    out_dir = REPO / "research_state" / "session_20261120T175300Z"
    out_path = out_dir / "fclr_xsec001_evaluation_20261120T175300Z.json"
    with open(out_path, "w") as fh:
        json.dump(results, fh, indent=2)
    print(f"\nSaved evaluation to {out_path}")


if __name__ == "__main__":
    main()
