#!/usr/bin/env python3
"""
FCLR-XSEC-004 Step 3: Regime-conditioned cross-sectional funding contrast on
NEXT-HOUR OBSERVED LIQUIDATION INTENSITY (not RV).

Estimand (pre-registered, freeze made before any outcome inspection):
  For each closed UTC hour t and market-wide-RV regime (high vs low tercile of
  cross-sectional mean rv24h at t), rank eligible coins by abs_fund_pct within
  (hour, regime); split high- vs low-funding. Compare next-hour observed
  liquidation intensity (sum of notional_usd per coin in hour t+1) of
  high-funding vs low-funding coins within the same hour and regime.

Specificity control: within-regime RV persistence baseline (coin's own rv24h at
t split high/low within (hour, regime)) predicting next-hour liquidation
intensity.

Inference: block bootstrap across whole UTC hours within each regime
(seed 20261120, >= 2000 deterministic replicates), Holm correction across the
4-test family (2 regimes x {funding contrast, persistence baseline}), 95% CIs,
2% materiality floor (|mean_diff| / mean_abs_outcome >= 0.02).

Verdict = SUPPORTED only if a funding-contrast CI excludes zero AND Holm passes
AND materiality clears; otherwise report the honest null as NOT_SUPPORTED.

Outcome data inspected before freeze: false. Protocol frozen first.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

import numpy as np
import pandas as pd

REPO = Path(__file__).resolve().parents[2]
PANEL = REPO / "research_state" / "fclr_liq_combined_panel_20261115T181405Z.parquet"
PANEL_SHA256 = "81a100d5d0625832bebabaabea13b786e15319577721cfe8507da5b779ec7f14"
SESSION = "20261120T230000Z"
OUT_DIR = REPO / "research_state" / f"session_{SESSION}"
SEED = 20261120
N_BOOT = 2000
ALPHA = 0.05
MATERIALITY_FLOOR = 0.02
MIN_COINS_PER_HOUR = 3


def load_panel() -> pd.DataFrame:
    df = pd.read_parquet(PANEL)
    df = df.sort_values(["coin", "timestamp"]).reset_index(drop=True)
    return df


def to_hourly(df: pd.DataFrame) -> pd.DataFrame:
    """Aggregate event-level panel to one (coin, hour) row.

    intensity   = sum(notional_usd) in the hour
    rv24h       = mean of coin rv24h within the hour
    abs_fund_pct= mean of coin abs_fund_pct within the hour
    """
    df = df.copy()
    df["hour"] = df["timestamp"].dt.floor("h")
    g = (
        df.groupby(["coin", "hour"])
        .agg(
            intensity=("notional_usd", "sum"),
            rv24h=("rv24h", "mean"),
            abs_fund_pct=("abs_fund_pct", "mean"),
            n_events=("notional_usd", "size"),
        )
        .reset_index()
    )
    return g


def add_next_hour_intensity(g: pd.DataFrame) -> pd.DataFrame:
    g = g.sort_values(["coin", "hour"]).reset_index(drop=True)
    g["next_hour_intensity"] = g.groupby("coin")["intensity"].shift(-1)
    return g


def add_market_wide_rv(g: pd.DataFrame) -> pd.DataFrame:
    g = g.copy()
    mw = g.groupby("hour")["rv24h"].agg(["mean", "count"]).rename(
        columns={"mean": "market_rv", "count": "market_rv_n"}
    )
    g = g.merge(mw, on="hour", how="left")
    g["hour_eligible"] = g["market_rv_n"] >= MIN_COINS_PER_HOUR
    return g


def add_regime(g: pd.DataFrame):
    g = g.copy()
    eligible = g[g["hour_eligible"]].copy()
    hour_mw = eligible.groupby("hour")["market_rv"].first()
    tercile_low = hour_mw.quantile(1 / 3)
    tercile_high = hour_mw.quantile(2 / 3)
    ts_to_regime = {}
    for hour, mv in hour_mw.items():
        if mv >= tercile_high:
            ts_to_regime[hour] = "high_rv_regime"
        elif mv <= tercile_low:
            ts_to_regime[hour] = "low_rv_regime"
        else:
            ts_to_regime[hour] = "mid_rv_regime"
    g["regime"] = g["hour"].map(ts_to_regime)
    return g, tercile_low, tercile_high


def paired_hourly_diff(df: pd.DataFrame, group_col: str) -> pd.DataFrame:
    """Mean(next_hour_intensity) per (hour, group); return paired high-minus-low diff."""
    stats = (
        df.groupby(["hour", group_col])["next_hour_intensity"]
        .agg(["mean", "count"])
        .reset_index()
    )
    if stats.empty:
        return stats.iloc[0:0].copy()
    pivot = stats.pivot(index="hour", columns=group_col, values="mean")
    counts = stats.pivot(index="hour", columns=group_col, values="count")
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
    """Within each (hour, regime), rank coins by abs_fund_pct; split high/low."""
    df = df.copy()
    df["funding_rank_within_hour_regime"] = df.groupby(["hour", "regime"])[
        "abs_fund_pct"
    ].rank(method="average", ascending=False)
    n_coins = df.groupby(["hour", "regime"])["coin"].transform("nunique")
    df["funding_pct_within_hour_regime"] = df["funding_rank_within_hour_regime"] / n_coins
    df["funding_group"] = np.where(
        df["funding_pct_within_hour_regime"] <= 0.5, "high_funding", "low_funding"
    )
    return df


def add_rv_groups(df: pd.DataFrame) -> pd.DataFrame:
    """Within each (hour, regime), rank coins by rv24h; split high/low (persistence baseline)."""
    df = df.copy()
    df["rv_rank_within_hour_regime"] = df.groupby(["hour", "regime"])["rv24h"].rank(
        method="average", ascending=False
    )
    n_coins = df.groupby(["hour", "regime"])["coin"].transform("nunique")
    df["rv_pct_within_hour_regime"] = df["rv_rank_within_hour_regime"] / n_coins
    df["rv_group"] = np.where(df["rv_pct_within_hour_regime"] <= 0.5, "high_rv", "low_rv")
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

    g = to_hourly(df)
    g = add_next_hour_intensity(g)
    g_eval = g[g["next_hour_intensity"].notna()].copy()

    g_eval = add_market_wide_rv(g_eval)
    g_eval = g_eval[g_eval["hour_eligible"]].copy()
    g_eval, tercile_low, tercile_high = add_regime(g_eval)
    g_regimes = g_eval[g_eval["regime"].isin(["high_rv_regime", "low_rv_regime"])].copy()

    # Mean absolute next-hour intensity per regime (materiality denominator).
    mean_abs_outcome = {}
    for regime in ["high_rv_regime", "low_rv_regime"]:
        sub = g_regimes[g_regimes["regime"] == regime]
        mean_abs_outcome[regime] = float(sub["next_hour_intensity"].abs().mean())

    tests = {}

    # --- Funding contrast per regime ---
    df_f = add_funding_groups(g_regimes.copy())
    for regime in ["high_rv_regime", "low_rv_regime"]:
        sub = df_f[df_f["regime"] == regime].copy()
        both = paired_hourly_diff(sub, "funding_group")
        diff = both["diff"].values
        s = summarize_contrast(diff, SEED)
        s["mean_abs_outcome"] = mean_abs_outcome[regime]
        s["materiality_effect"] = (
            float(abs(s["mean_diff_high_minus_low"]) / mean_abs_outcome[regime])
            if s["mean_diff_high_minus_low"] is not None else None
        )
        s["materiality_floor_met"] = bool(
            s["materiality_effect"] is not None and s["materiality_effect"] >= MATERIALITY_FLOOR
        )
        tests[f"{regime}_funding_contrast"] = s

    # --- RV persistence baseline per regime ---
    df_r = add_rv_groups(g_regimes.copy())
    for regime in ["high_rv_regime", "low_rv_regime"]:
        sub = df_r[df_r["regime"] == regime].copy()
        both = paired_hourly_diff(sub, "rv_group")
        diff = both["diff"].values
        s = summarize_contrast(diff, SEED)
        s["mean_abs_outcome"] = mean_abs_outcome[regime]
        s["materiality_effect"] = (
            float(abs(s["mean_diff_high_minus_low"]) / mean_abs_outcome[regime])
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

    # --- Verdict: funding-contrast must clear all three gates ---
    funding_tests = [t for t in test_names if t.endswith("_funding_contrast")]
    gate_passed = any(
        tests[t]["ci_excludes_zero"] and tests[t]["holm_passes"] and tests[t]["materiality_floor_met"]
        for t in funding_tests
    )
    verdict = "SUPPORTED" if gate_passed else "NOT_SUPPORTED"

    print(f"\n=== FCLR-XSEC-004 Results ===")
    print(f"Panel: {PANEL} (sha256 {PANEL_SHA256})")
    print(f"Coins: {sorted(df['coin'].unique())}")
    print(f"Hourly rows: {len(g)}, regime-eligible coin-hours: {len(g_regimes)}")
    print(f"Unique hours: {g_eval['hour'].nunique()}, regime-eligible hours: {g_regimes['hour'].nunique()}")
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
        "experiment_id": f"FCLR-XSEC-004-{SESSION}",
        "session_utc": SESSION,
        "panel_path": str(PANEL),
        "panel_sha256": PANEL_SHA256,
        "panel_hash_verified": actual_sha == PANEL_SHA256,
        "mechanism": "UTC-hour / market-wide-RV conditioning of the funding effect applied to observed liquidation intensity",
        "estimand": "regime_conditioned_cross_sectional_funding_effect_on_next_hour_liquidation_intensity",
        "outcome_data_inspected_before_freeze": False,
        "n_coins": 15,
        "coins": sorted(df["coin"].unique()),
        "ts_min": str(df["timestamp"].min()),
        "ts_max": str(df["timestamp"].max()),
        "n_hourly_rows": int(len(g)),
        "n_regime_eligible_coin_hours": int(len(g_regimes)),
        "n_unique_hours": int(g_eval["hour"].nunique()),
        "n_regime_eligible_hours": int(g_regimes["hour"].nunique()),
        "market_rv_tercile_low": float(tercile_low),
        "market_rv_tercile_high": float(tercile_high),
        "seed": SEED,
        "n_bootstrap_reps": N_BOOT,
        "alpha": ALPHA,
        "materiality_floor": MATERIALITY_FLOOR,
        "family_size": len(test_names),
        "holm_correction": "holm",
        "tests": tests,
        "funding_tests": funding_tests,
        "gate": {
            "ci_supports_improvement": any(tests[t]["ci_excludes_zero"] for t in funding_tests),
            "holm_passes_any_funding": any(tests[t]["holm_passes"] for t in funding_tests),
            "materiality_met_any_funding": any(tests[t]["materiality_floor_met"] for t in funding_tests),
            "gate_passed": bool(gate_passed),
            "verdict": verdict,
        },
        "verdict": verdict,
    }

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    out_path = OUT_DIR / f"fclr_xsec004_evaluation_{SESSION}.json"
    with open(out_path, "w") as fh:
        json.dump(results, fh, indent=2)
    print(f"\nSaved evaluation to {out_path}")


if __name__ == "__main__":
    main()
