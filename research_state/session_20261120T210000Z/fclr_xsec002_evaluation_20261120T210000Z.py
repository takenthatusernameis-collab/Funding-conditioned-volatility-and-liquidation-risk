#!/usr/bin/env python3
"""
FCLR-XSEC-002 Step 3: Regime-conditioned funding contrast evaluation.

Within each market-wide-RV regime (high vs low tercile), for each closed UTC
hour t, rank the eligible coins by abs_funding_pct_trail (require
abs_funding_trail_n >= 30) and split into high- vs low-funding. Compare
next-hour realized variance (rv1h at t+1) of high-funding vs low-funding coins
within the same hour and regime. Same paired within-hour structure as
FCLR-XSEC-001, now conditioned on regime.

Baseline: within-regime RV persistence (coin's own rv1h at t split high/low
within regime), same paired structure per regime.

Evaluation: block bootstrap across whole UTC hours within each regime
(seed 20261120, >= 2,000 deterministic replicates), Holm correction across the
full family (2 regimes x {funding contrast, persistence baseline} = 4 tests),
95% CIs, 2% materiality floor. Verdict = NOT_SUPPORTED unless at least one test
has CI excluding zero AND Holm passes AND effect clears materiality floor;
otherwise report the honest null.

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
SESSION = "20261120T210000Z"
OUT_DIR = REPO / "research_state" / f"session_{SESSION}"
SEED = 20261120
N_BOOT = 2000
ALPHA = 0.05
MATERIALITY_FLOOR = 0.02
MIN_COINS_PER_HOUR = 3
MIN_FUNDING_OBS = 30


def load_panel() -> pd.DataFrame:
    df = pd.read_parquet(PANEL)
    df["ts"] = pd.to_datetime(df["ts"], utc=True)
    df = df.sort_values(["coin", "ts"]).reset_index(drop=True)
    df["target_rv1h_t1"] = df.groupby("coin")["rv1h"].shift(-1)
    return df


def add_market_wide_rv(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    mw = df.groupby("ts")["rv1h"].agg(["mean", "count"]).rename(
        columns={"mean": "market_rv1h", "count": "market_rv1h_n"}
    )
    df = df.merge(mw, on="ts", how="left")
    df["hour_regime_eligible"] = df["market_rv1h_n"] >= MIN_COINS_PER_HOUR
    return df


def add_regime(df: pd.DataFrame):
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


def add_funding_groups(df: pd.DataFrame) -> pd.DataFrame:
    """Within each (ts, regime), rank coins by abs_funding_pct_trail; split high/low."""
    df = df.copy()
    # Require adequate trailing funding observation count.
    df = df[df["abs_funding_trail_n"] >= MIN_FUNDING_OBS].copy()
    df["funding_rank_within_hour_regime"] = df.groupby(["ts", "regime"])[
        "abs_funding_pct_trail"
    ].rank(method="average", ascending=False)
    n_coins = df.groupby(["ts", "regime"])["coin"].transform("nunique")
    df["funding_pct_within_hour_regime"] = df["funding_rank_within_hour_regime"] / n_coins
    df["funding_group"] = np.where(
        df["funding_pct_within_hour_regime"] <= 0.5, "high_funding", "low_funding"
    )
    return df


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


def summarize_contrast(diff: np.ndarray, seed: int) -> dict:
    n = len(diff)
    mean_diff = float(diff.mean()) if n > 0 else None
    boot = block_bootstrap(diff, seed)
    ci_low = float(np.percentile(boot, 2.5))
    ci_high = float(np.percentile(boot, 97.5))
    p_value = float(2 * min((boot >= 0).mean(), (boot <= 0).mean()))
    ci_excludes_zero = bool(ci_low > 0 or ci_high < 0)
    pos_count = int((diff > 0).sum()) if n > 0 else 0
    return {
        "n_hours": int(n),
        "mean_diff_high_minus_low": mean_diff,
        "ci_low": ci_low,
        "ci_high": ci_high,
        "p_value": p_value,
        "ci_excludes_zero": ci_excludes_zero,
        "positive_diff_count": pos_count,
        "positive_diff_share": float(pos_count / n) if n > 0 else None,
    }


def main() -> None:
    df = load_panel()
    actual_sha = hashlib.sha256(PANEL.read_bytes()).hexdigest()
    assert actual_sha == PANEL_SHA256, f"panel hash mismatch: {actual_sha}"

    # Restrict to rows with a next-hour target.
    df_eval = df[df["target_rv1h_t1"].notna()].copy()

    # Market-wide RV and regime split.
    df_eval = add_market_wide_rv(df_eval)
    df_eval = df_eval[df_eval["hour_regime_eligible"]].copy()
    df_eval, tercile_low, tercile_high = add_regime(df_eval)
    df_regimes = df_eval[df_eval["regime"].isin(["high_rv_regime", "low_rv_regime"])].copy()

    # Mean absolute target per regime (for materiality floor).
    mean_abs_target = {}
    for regime in ["high_rv_regime", "low_rv_regime"]:
        sub = df_regimes[df_regimes["regime"] == regime]
        mean_abs_target[regime] = float(sub["target_rv1h_t1"].abs().mean())

    tests = {}

    # --- Funding contrast per regime ---
    df_f = add_funding_groups(df_regimes.copy())
    for regime in ["high_rv_regime", "low_rv_regime"]:
        sub = df_f[df_f["regime"] == regime].copy()
        both = paired_hourly_diff(sub, "funding_group")
        diff = both["diff"].values
        s = summarize_contrast(diff, SEED)
        s["mean_abs_target"] = mean_abs_target[regime]
        s["materiality_effect"] = (
            float(abs(s["mean_diff_high_minus_low"]) / mean_abs_target[regime])
            if s["mean_diff_high_minus_low"] is not None else None
        )
        s["materiality_floor_met"] = bool(
            s["materiality_effect"] is not None and s["materiality_effect"] >= MATERIALITY_FLOOR
        )
        tests[f"{regime}_funding_contrast"] = s

    # --- RV persistence baseline per regime ---
    df_r = df_regimes.copy()
    df_r = df_r.sort_values(["coin", "ts"]).reset_index(drop=True)
    df_r["rv_rank_within_hour_regime"] = df_r.groupby(["ts", "regime"])["rv1h"].rank(
        method="average", ascending=False
    )
    n_coins_r = df_r.groupby(["ts", "regime"])["coin"].transform("nunique")
    df_r["rv_pct_within_hour_regime"] = df_r["rv_rank_within_hour_regime"] / n_coins_r
    df_r["rv_group"] = np.where(df_r["rv_pct_within_hour_regime"] <= 0.5, "high_rv", "low_rv")
    for regime in ["high_rv_regime", "low_rv_regime"]:
        sub = df_r[df_r["regime"] == regime].copy()
        both = paired_hourly_diff(sub, "rv_group")
        diff = both["diff"].values
        s = summarize_contrast(diff, SEED)
        s["mean_abs_target"] = mean_abs_target[regime]
        s["materiality_effect"] = (
            float(abs(s["mean_diff_high_minus_low"]) / mean_abs_target[regime])
            if s["mean_diff_high_minus_low"] is not None else None
        )
        s["materiality_floor_met"] = bool(
            s["materiality_effect"] is not None and s["materiality_effect"] >= MATERIALITY_FLOOR
        )
        tests[f"{regime}_rv_persistence_baseline"] = s

    # --- Holm correction over family of 4 ---
    test_names = list(tests.keys())
    p_vals = [tests[t]["p_value"] for t in test_names]
    holm = holm_adjust(p_vals)
    for t, adj_p in zip(test_names, holm):
        tests[t]["holm_adj_p"] = float(adj_p)
        tests[t]["holm_passes"] = bool(adj_p < ALPHA)

    # --- Verdict ---
    gate_passed = any(
        tests[t]["ci_excludes_zero"] and tests[t]["holm_passes"] and tests[t]["materiality_floor_met"]
        for t in test_names
    )
    verdict = "SUPPORTED" if gate_passed else "NOT_SUPPORTED"

    print(f"\n=== FCLR-XSEC-002 Results ===")
    print(f"Panel: {PANEL} (sha256 {PANEL_SHA256})")
    print(f"Coins: {sorted(df['coin'].unique())}")
    print(f"Regime-eligible hours: {df_regimes['ts'].nunique()}")
    print(f"Market-wide RV tercile boundaries: low={tercile_low:.6e}, high={tercile_high:.6e}")
    for t in test_names:
        s = tests[t]
        print(f"\n{t.replace('_', ' ').title()}:")
        print(f"  n_hours: {s['n_hours']}, mean diff: {s['mean_diff_high_minus_low']:.6f}")
        print(f"  95% CI: [{s['ci_low']:.6f}, {s['ci_high']:.6f}]")
        print(f"  p_value: {s['p_value']:.6f}, Holm adj_p: {s['holm_adj_p']:.6f}")
        print(f"  CI excludes zero: {s['ci_excludes_zero']}, Holm passes: {s['holm_passes']}")
        print(f"  Materiality effect: {s['materiality_effect']}, floor met: {s['materiality_floor_met']}")
        print(f"  positive diffs: {s['positive_diff_count']} / {s['n_hours']}")
    print(f"\nVerdict: {verdict} (gate_passed={gate_passed})")

    results = {
        "experiment_id": "FCLR-XSEC-002-20261120T210000Z",
        "session_utc": SESSION,
        "panel_path": str(PANEL),
        "panel_sha256": PANEL_SHA256,
        "panel_hash_verified": actual_sha == PANEL_SHA256,
        "mechanism": "UTC-hour / market-wide-RV conditioning of the funding effect",
        "estimand": "utc_hour_market_wide_rv_conditioning_rv1h",
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
        "seed": SEED,
        "n_bootstrap_reps": N_BOOT,
        "alpha": ALPHA,
        "materiality_floor": MATERIALITY_FLOOR,
        "family_size": len(test_names),
        "holm_correction": "holm",
        "tests": tests,
        "gate": {
            "ci_supports_improvement": any(tests[t]["ci_excludes_zero"] for t in test_names),
            "holm_passes_any": any(tests[t]["holm_passes"] for t in test_names),
            "materiality_met_any": any(tests[t]["materiality_floor_met"] for t in test_names),
            "gate_passed": bool(gate_passed),
            "verdict": verdict,
        },
        "verdict": verdict,
    }

    out_path = OUT_DIR / f"fclr_xsec002_evaluation_{SESSION}.json"
    with open(out_path, "w") as fh:
        json.dump(results, fh, indent=2)
    print(f"\nSaved evaluation to {out_path}")


if __name__ == "__main__":
    main()
