#!/usr/bin/env python3
"""
FCLR-XSEC-008 Step 2: Alternative regime conditioning on overlapping hours.

Re-tests the regime-conditioned funding effect SUPPORTED for RV (FCLR-XSEC-002,
HIGH-RV regime, next-hour RV) and for liquidation intensity
(FCLR-XSEC-004/005 LOW-RV; FCLR-XSEC-006 ALL THREE UTC buckets, next-hour
notional-weighted liquidation intensity) under an alternative regime variable:
RV168/RV24 volatility-of-volatility (voV) ratio terciles, instead of RV tercile
or UTC session bucket, on the same frozen panels.

Primary A: within-(hour, voV-tercile) cross-sectional abs_funding_pct_trail rank
-> next-hour RV (target_rv24h). Declared on the HIGH voV tercile (analogue of
FCLR-XSEC-002 high-RV). Baseline: RV persistence.
Primary B: within-(hour, voV-tercile) cross-sectional abs_fund_pct rank ->
next-hour NOTIONAL-WEIGHTED observed liquidation intensity (sum of notional_usd,
dollar severity). Evaluated across all three voV terciles; passes if any tercile
clears gates (analogue of FCLR-XSEC-006 any-bucket). Baseline: RV persistence.

Inference: block bootstrap across whole UTC hours within each voV-tercile regime
family (seed 20261121, >= 2000 deterministic replicates), Holm correction over
the joint 6-test family, 95% CIs, 2% materiality floor
(|mean_diff| / mean_abs_outcome >= 0.02).

Verdict = SUPPORTED only if BOTH primary funding contrasts clear all three gates
(CI excludes zero, Holm passes, materiality floor met); otherwise report the
honest null as NOT_SUPPORTED.

Outcome data inspected before freeze: false. Protocol frozen first.
Cross-reference: FCLR-XSEC-002 (high-RV SUPPORTED), FCLR-XSEC-004 (low-RV
count-based SUPPORTED), FCLR-XSEC-005 (low-RV notional-weighted SUPPORTED),
FCLR-XSEC-006 (all three UTC buckets SUPPORTED), FCLR-XSEC-007 (NOT_SUPPORTED).
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

import numpy as np
import pandas as pd

REPO = Path(__file__).resolve().parents[2]
PANEL_FCLR001 = REPO / "research_state" / "fclr011_recompute_panel_20261115T234700Z.parquet"
PANEL_FCLR001_SHA256 = "41962f823e59de5989c7d854cb3180cad61a4cbc2f5f230133c41b321342c1f4"
PANEL_LIQ = REPO / "research_state" / "fclr_liq_combined_panel_20261115T181405Z.parquet"
PANEL_LIQ_SHA256 = "81a100d5d0625832bebabaabea13b786e15319577721cfe8507da5b779ec7f14"
SESSION = "20261121T054721Z"
OUT_DIR = REPO / "research_state" / f"session_{SESSION}"
SEED = 20261121
N_BOOT = 2000
ALPHA = 0.05
MATERIALITY_FLOOR = 0.02
MIN_COINS_PER_HOUR = 3

# Coin name mapping: FCLR-001 (USDT suffix) -> liquidation panel (no suffix).
COIN_MAP = {
    "BTCUSDT": "BTC",
    "ETHUSDT": "ETH",
    "BNBUSDT": "BNB",
    "SOLUSDT": "SOL",
    "XRPUSDT": "XRP",
}
OVERLAPPING_COINS = ["BTC", "ETH", "BNB", "SOL", "XRP"]

# Alternative regime variable: RV168/RV24 volatility-of-volatility ratio.
# Hours terciled ex-ante into low / mid / high voV regimes.
VOV_TERCILES = ["low", "mid", "high"]
PRIMARY_A_TERCILE = "high"          # analogue of FCLR-XSEC-002 high-RV
PRIMARY_B_TERCILES = ["low", "mid", "high"]  # analogue of FCLR-XSEC-006 any-bucket
PRIMARY_B_PASS_RULE = "any_tercile"


def load_fclr001() -> pd.DataFrame:
    df = pd.read_parquet(PANEL_FCLR001)
    df = df.sort_values(["coin", "ts"]).reset_index(drop=True)
    df["hour"] = df["ts"].dt.floor("h")
    df["coin_short"] = df["coin"].map(COIN_MAP)
    df = df[df["coin_short"].isin(OVERLAPPING_COINS)].copy()
    return df


def load_liquidation_hourly() -> pd.DataFrame:
    """Aggregate event-level liquidation panel to one (coin, hour) row.

    NOTIONAL-WEIGHTED intensity = sum(notional_usd) in the hour (dollar severity).
    Restricted to the 5 overlapping coins so Primary A and Primary B share the
    same coin universe for cross-panel reconciliation.
    """
    df = pd.read_parquet(PANEL_LIQ)
    df = df.sort_values(["coin", "timestamp"]).reset_index(drop=True)
    df["hour"] = df["timestamp"].dt.floor("h")
    df = df[df["coin"].isin(OVERLAPPING_COINS)].copy()
    g = (
        df.groupby(["coin", "hour"])
        .agg(
            notional_weighted_intensity=("notional_usd", "sum"),  # PRIMARY: dollar severity
            event_count=("notional_usd", "size"),                # SECONDARY: count (cross-ref only)
            abs_fund_pct=("abs_fund_pct", "mean"),
            rv24h=("rv24h", "mean"),
            rv168h=("rv168h", "mean"),
        )
        .reset_index()
    )
    return g


def add_next_hour_rv(f: pd.DataFrame) -> pd.DataFrame:
    f = f.sort_values(["coin_short", "hour"]).reset_index(drop=True)
    f["next_hour_rv"] = f.groupby("coin_short")["target_rv24h"].shift(-1)
    return f


def add_next_hour_intensity(g: pd.DataFrame) -> pd.DataFrame:
    g = g.sort_values(["coin", "hour"]).reset_index(drop=True)
    g["next_hour_notional_weighted_intensity"] = g.groupby("coin")["notional_weighted_intensity"].shift(-1)
    g["next_hour_event_count"] = g.groupby("coin")["event_count"].shift(-1)
    return g


def add_vov_ratio(f: pd.DataFrame) -> pd.DataFrame:
    """voV ratio = rv168h / rv24h per coin-hour where both non-null."""
    f = f.copy()
    f["vov_ratio"] = np.where(
        f["rv168h"].notna() & f["rv24h"].notna() & (f["rv24h"] > 0),
        f["rv168h"] / f["rv24h"],
        np.nan,
    )
    return f


def add_market_wide_vov(f: pd.DataFrame) -> pd.DataFrame:
    """Market-wide voV ratio per hour = mean across coins with a valid ratio."""
    mw = (
        f.groupby("hour")["vov_ratio"]
        .agg(["mean", "count"])
        .rename(columns={"mean": "market_vov", "count": "market_vov_n"})
    )
    f = f.merge(mw, on="hour", how="left")
    f["hour_eligible"] = f["market_vov_n"] >= MIN_COINS_PER_HOUR
    return f


def add_vov_tercile(f: pd.DataFrame) -> pd.DataFrame:
    """Assign each eligible hour to a market-wide voV tercile (low/mid/high)."""
    f = f.copy()
    eligible = f[f["hour_eligible"]].copy()
    terciles = eligible.groupby("hour")["market_vov"].first()
    if terciles.nunique() < 2:
        f["vov_tercile"] = np.nan
        return f
    tercile_labels = pd.qcut(terciles, q=3, labels=VOV_TERCILES)
    hour_to_tercile = tercile_labels.to_dict()
    f["vov_tercile"] = f["hour"].map(hour_to_tercile)
    return f


def paired_hourly_diff(df: pd.DataFrame, group_col: str, outcome_col: str) -> pd.DataFrame:
    """Mean(outcome_col) per (hour, group); return paired high-minus-low diff."""
    stats = (
        df.groupby(["hour", group_col])[outcome_col]
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


def add_funding_groups(df: pd.DataFrame, fund_col: str, coin_col: str) -> pd.DataFrame:
    """Within each hour, rank coins by fund_col; split high vs low funding."""
    df = df.copy()
    df["funding_rank_within_hour"] = df.groupby("hour")[fund_col].rank(method="average", ascending=False)
    n_coins = df.groupby("hour")[coin_col].transform("nunique")
    df["funding_pct_within_hour"] = df["funding_rank_within_hour"] / n_coins
    df["funding_group"] = np.where(df["funding_pct_within_hour"] <= 0.5, "high_funding", "low_funding")
    return df


def add_rv_groups(df: pd.DataFrame, rv_col: str, coin_col: str) -> pd.DataFrame:
    """Within each hour, rank coins by rv_col; split high vs low RV (persistence baseline)."""
    df = df.copy()
    df["rv_rank_within_hour"] = df.groupby("hour")[rv_col].rank(method="average", ascending=False)
    n_coins = df.groupby("hour")[coin_col].transform("nunique")
    df["rv_pct_within_hour"] = df["rv_rank_within_hour"] / n_coins
    df["rv_group"] = np.where(df["rv_pct_within_hour"] <= 0.5, "high_rv", "low_rv")
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


def summarize_contrast(diff: np.ndarray, seed: int, mean_abs_outcome: float) -> dict:
    n = len(diff)
    mean_diff = float(diff.mean()) if n > 0 else None
    boot = block_bootstrap(diff, seed)
    ci_low = float(np.percentile(boot, 2.5))
    ci_high = float(np.percentile(boot, 97.5))
    p_value = float(2 * min((boot >= 0).mean(), (boot <= 0).mean()))
    ci_excludes_zero = bool(ci_low > 0 or ci_high < 0)
    pos_count = int((diff > 0).sum()) if n > 0 else 0
    materiality_effect = (
        float(abs(mean_diff) / mean_abs_outcome) if mean_diff is not None and mean_abs_outcome > 0 else None
    )
    materiality_floor_met = bool(
        materiality_effect is not None and materiality_effect >= MATERIALITY_FLOOR
    )
    return {
        "n_hours": int(n),
        "mean_diff_high_minus_low": mean_diff,
        "ci_low": ci_low,
        "ci_high": ci_high,
        "p_value": p_value,
        "ci_excludes_zero": ci_excludes_zero,
        "positive_diff_count": pos_count,
        "positive_diff_share": float(pos_count / n) if n > 0 else None,
        "mean_abs_outcome": mean_abs_outcome,
        "materiality_effect": materiality_effect,
        "materiality_floor_met": materiality_floor_met,
    }


def main() -> None:
    # --- Verify panel hashes before any computation ---
    actual_fclr001_sha = hashlib.sha256(PANEL_FCLR001.read_bytes()).hexdigest()
    assert actual_fclr001_sha == PANEL_FCLR001_SHA256, f"FCLR-001 panel hash mismatch: {actual_fclr001_sha}"
    actual_liq_sha = hashlib.sha256(PANEL_LIQ.read_bytes()).hexdigest()
    assert actual_liq_sha == PANEL_LIQ_SHA256, f"Liquidation panel hash mismatch: {actual_liq_sha}"

    # --- Load panels ---
    f = load_fclr001()
    g = load_liquidation_hourly()
    print(f"FCLR-001 rows (5 overlapping coins): {len(f)}, hours: {f['hour'].nunique()}")
    print(f"Liquidation hourly rows (5 overlapping coins): {len(g)}, hours: {g['hour'].nunique()}")

    # --- Add next-hour targets ---
    f = add_next_hour_rv(f)
    g = add_next_hour_intensity(g)

    # --- Join on (coin, hour) using FCLR-001 funding + RV consistently ---
    f_join = f[["coin_short", "hour", "rv24h", "rv168h", "abs_funding_pct_trail", "signed_funding", "target_rv24h", "next_hour_rv"]].copy()
    f_join = f_join.rename(columns={"coin_short": "coin", "abs_funding_pct_trail": "abs_fund_pct"})
    g_join = g[["coin", "hour", "notional_weighted_intensity", "abs_fund_pct", "rv24h", "rv168h", "next_hour_notional_weighted_intensity", "next_hour_event_count"]].copy()

    joined = f_join.merge(g_join, on=["coin", "hour"], how="inner", suffixes=("_fclr", "_liq"))
    # Single consistent predictor/regime measure across both primaries (FCLR-001).
    joined = joined.rename(columns={"rv24h_fclr": "rv24h", "rv168h_fclr": "rv168h", "abs_fund_pct_fclr": "abs_fund_pct"})
    print(f"Joined rows: {len(joined)}, unique hours: {joined['hour'].nunique()}")

    # --- voV ratio per coin-hour + market-wide voV per hour + tercile ---
    joined = add_vov_ratio(joined)
    joined_eval = add_market_wide_vov(joined)
    joined_eval = joined_eval[joined_eval["hour_eligible"]].copy()
    joined_eval = add_vov_tercile(joined_eval)
    joined_eval = joined_eval[joined_eval["vov_tercile"].notna()].copy()
    joined_eval = joined_eval[
        joined_eval["next_hour_rv"].notna() & joined_eval["next_hour_notional_weighted_intensity"].notna()
    ].copy()
    print(f"Eval-eligible coin-hours: {len(joined_eval)}, unique hours: {joined_eval['hour'].nunique()}")

    # Mean absolute outcomes per tercile (materiality denominators).
    mean_abs_rv_by_terc = {t: float(joined_eval[joined_eval["vov_tercile"] == t]["next_hour_rv"].abs().mean()) for t in VOV_TERCILES}
    mean_abs_liq_by_terc = {t: float(joined_eval[joined_eval["vov_tercile"] == t]["next_hour_notional_weighted_intensity"].abs().mean()) for t in VOV_TERCILES}
    hours_per_terc = {t: int(joined_eval[joined_eval["vov_tercile"] == t]["hour"].nunique()) for t in VOV_TERCILES}
    print(f"Hours per voV tercile: {hours_per_terc}")
    print(f"Mean abs next-hour RV by tercile: {mean_abs_rv_by_terc}")
    print(f"Mean abs notional-weighted liq intensity by tercile: {mean_abs_liq_by_terc}")

    tests = {}

    # ===== PRIMARY A: within-(hour, voV-tercile) funding rank -> next-hour RV =====
    df_a = add_funding_groups(joined_eval.copy(), "abs_fund_pct", "coin")
    df_ar = add_rv_groups(joined_eval.copy(), "rv24h", "coin")

    primary_a_tests = []
    for terc in VOV_TERCILES:
        sub = df_a[df_a["vov_tercile"] == terc].copy()
        both = paired_hourly_diff(sub, "funding_group", "next_hour_rv")
        diff = both["diff"].values
        s = summarize_contrast(diff, SEED, mean_abs_rv_by_terc[terc])
        name = f"vov_tercile_{terc}_funding_contrast_rv"
        tests[name] = s
        primary_a_tests.append(name)

        # Baseline A: within-(hour, voV-tercile) RV persistence -> next-hour RV
        subr = df_ar[df_ar["vov_tercile"] == terc].copy()
        bothr = paired_hourly_diff(subr, "rv_group", "next_hour_rv")
        diffr = bothr["diff"].values
        sr = summarize_contrast(diffr, SEED, mean_abs_rv_by_terc[terc])
        tests[f"vov_tercile_{terc}_rv_persistence_baseline_rv"] = sr

    # ===== PRIMARY B: within-(hour, voV-tercile) funding rank -> next-hour notional-weighted liq intensity =====
    df_b = add_funding_groups(joined_eval.copy(), "abs_fund_pct", "coin")
    df_br = add_rv_groups(joined_eval.copy(), "rv24h", "coin")

    primary_b_tests = []
    for terc in VOV_TERCILES:
        sub = df_b[df_b["vov_tercile"] == terc].copy()
        both = paired_hourly_diff(sub, "funding_group", "next_hour_notional_weighted_intensity")
        diff = both["diff"].values
        s = summarize_contrast(diff, SEED, mean_abs_liq_by_terc[terc])
        name = f"vov_tercile_{terc}_funding_contrast_notional_weighted"
        tests[name] = s
        primary_b_tests.append(name)

        # Baseline B: within-(hour, voV-tercile) RV persistence -> next-hour notional-weighted liq intensity
        subr = df_br[df_br["vov_tercile"] == terc].copy()
        bothr = paired_hourly_diff(subr, "rv_group", "next_hour_notional_weighted_intensity")
        diffr = bothr["diff"].values
        sr = summarize_contrast(diffr, SEED, mean_abs_liq_by_terc[terc])
        tests[f"vov_tercile_{terc}_rv_persistence_baseline_notional_weighted"] = sr

    # ===== Holm correction over joint 6-test family =====
    all_family_names = primary_a_tests + primary_b_tests + [
        t for t in tests.keys() if t.endswith("_rv_persistence_baseline_rv") or t.endswith("_rv_persistence_baseline_notional_weighted")
    ]
    p_vals = [tests[t]["p_value"] for t in all_family_names]
    holm = holm_adjust(p_vals)
    for t, adj_p in zip(all_family_names, holm):
        tests[t]["holm_adj_p"] = float(adj_p)
        tests[t]["holm_passes"] = bool(adj_p < ALPHA)

    # ===== Per-primary verdicts =====
    # Primary A: HIGH voV tercile funding contrast (FCLR-XSEC-002 style)
    primary_a_tests_funding = [t for t in primary_a_tests if t.endswith("_funding_contrast_rv") and PRIMARY_A_TERCILE in t]
    primary_a_passed = any(
        tests[t]["ci_excludes_zero"] and tests[t]["holm_passes"] and tests[t]["materiality_floor_met"]
        for t in primary_a_tests_funding
    )

    # Primary B: any voV tercile funding contrast (FCLR-XSEC-006 style)
    primary_b_tests_funding = [t for t in primary_b_tests if t.endswith("_funding_contrast_notional_weighted")]
    primary_b_passed = any(
        tests[t]["ci_excludes_zero"] and tests[t]["holm_passes"] and tests[t]["materiality_floor_met"]
        for t in primary_b_tests_funding
    )

    gate_passed = bool(primary_a_passed and primary_b_passed)
    verdict = "SUPPORTED" if gate_passed else "NOT_SUPPORTED"

    # ===== Cross-panel reconciliation (sign agreement + magnitude) =====
    recon = {
        "shared_hours": int(joined_eval["hour"].nunique()),
        "primary_a_passed": bool(primary_a_passed),
        "primary_b_passed": bool(primary_b_passed),
        "joint_significance": gate_passed,
    }

    high_test = [t for t in primary_a_tests_funding]
    bucket_tests = primary_b_tests_funding
    sign_agreements = []
    if high_test and bucket_tests:
        high_rv_sign = np.sign(tests[high_test[0]]["mean_diff_high_minus_low"])
        for bt in bucket_tests:
            bucket_sign = np.sign(tests[bt]["mean_diff_high_minus_low"])
            sign_agreements.append({
                "bucket_test": bt,
                "high_voV_sign": float(high_rv_sign),
                "bucket_sign": float(bucket_sign),
                "sign_agreement": bool(high_rv_sign == bucket_sign),
            })
    recon["sign_agreements"] = sign_agreements

    # Magnitude correlation: per-hour effect sizes for RV contrast (high tercile)
    # vs liq intensity contrast (each tercile) on shared hours.
    def hourly_effect(sub, group_col, outcome_col):
        both = paired_hourly_diff(sub, group_col, outcome_col)
        return both.reset_index()[["hour", "diff"]].rename(columns={"diff": "effect"})

    df_a_high = add_funding_groups(joined_eval[joined_eval["vov_tercile"] == PRIMARY_A_TERCILE].copy(), "abs_fund_pct", "coin")
    rv_effect_by_hour = hourly_effect(df_a_high, "funding_group", "next_hour_rv")

    mag_corr = []
    for terc in VOV_TERCILES:
        df_b_terc = add_funding_groups(joined_eval[joined_eval["vov_tercile"] == terc].copy(), "abs_fund_pct", "coin")
        liq_effect_by_hour = hourly_effect(df_b_terc, "funding_group", "next_hour_notional_weighted_intensity")
        merged = rv_effect_by_hour.merge(liq_effect_by_hour, on="hour", suffixes=("_rv", "_liq"))
        if len(merged) > 3:
            corr = float(np.corrcoef(merged["effect_rv"], merged["effect_liq"])[0, 1])
        else:
            corr = None
        mag_corr.append({
            "tercile": terc,
            "n_shared_hours": int(len(merged)),
            "effect_size_correlation": corr,
        })
    recon["magnitude_correlation"] = mag_corr

    # ===== Print results =====
    print(f"\n=== FCLR-XSEC-008 Results (Alternative Regime Conditioning: voV ratio terciles) ===")
    print(f"FCLR-001 panel: {PANEL_FCLR001} (sha256 {PANEL_FCLR001_SHA256})")
    print(f"Liquidation panel: {PANEL_LIQ} (sha256 {PANEL_LIQ_SHA256})")
    print(f"Overlapping coins: {OVERLAPPING_COINS}")
    print(f"Joined coin-hours: {len(joined)}, eval-eligible coin-hours: {len(joined_eval)}")
    print(f"Unique shared hours: {joined_eval['hour'].nunique()}")
    print(f"Hours per voV tercile: {hours_per_terc}")
    for t in sorted(tests.keys()):
        s = tests[t]
        print(f"\n{t.replace('_', ' ').title()}:")
        print(f"  n_hours: {s['n_hours']}, mean diff: {s['mean_diff_high_minus_low']:.6f}")
        print(f"  95% CI: [{s['ci_low']:.6f}, {s['ci_high']:.6f}]")
        print(f"  p_value: {s['p_value']:.6f}", end="")
        if "holm_adj_p" in s:
            print(f", Holm adj_p: {s['holm_adj_p']:.6f}", end="")
        print()
        print(f"  CI excludes zero: {s['ci_excludes_zero']}, Holm passes: {s.get('holm_passes', False)}")
        print(f"  Materiality effect: {s['materiality_effect']}, floor met: {s['materiality_floor_met']}")
        print(f"  positive diffs: {s['positive_diff_count']} / {s['n_hours']}")
    print(f"\nPrimary A (voV HIGH tercile, funding->RV) passed: {primary_a_passed}")
    print(f"Primary B (voV any-tercile, funding->liq intensity) passed: {primary_b_passed}")
    print(f"\n--- Cross-Panel Reconciliation ---")
    print(f"Shared hours: {recon['shared_hours']}")
    print(f"Joint significance (both primaries pass): {recon['joint_significance']}")
    for sa in sign_agreements:
        print(f"  {sa['bucket_test']}: high_voV_sign={sa['high_voV_sign']}, bucket_sign={sa['bucket_sign']}, agreement={sa['sign_agreement']}")
    for mc in mag_corr:
        print(f"  {mc['tercile']}: n_shared_hours={mc['n_shared_hours']}, effect_corr={mc['effect_size_correlation']}")
    print(f"\nVerdict: {verdict} (gate_passed={gate_passed})")

    # Cross-reference to prior campaigns
    print("\n--- Cross-Reference to FCLR-XSEC-002 / XSEC-004 / XSEC-005 / XSEC-006 ---")
    print("FCLR-XSEC-002 high-RV funding contrast: CI [0.0046, 0.2348], p=0.019, materiality 1.09 -> SUPPORTED")
    print("FCLR-XSEC-004 low-RV count-based funding contrast: CI [448605.26, 841155.73], p=0.0, materiality 0.80 -> SUPPORTED")
    print("FCLR-XSEC-005 low-RV notional-weighted funding contrast: CI [452972.90, 850198.89], p=0.0, materiality 0.80 -> SUPPORTED")
    print("FCLR-XSEC-006 all three UTC buckets: Asian CI [162051, 521424], European CI [334550, 782272], US CI [94750, 698082] -> SUPPORTED")

    results = {
        "experiment_id": f"FCLR-XSEC-008-{SESSION}",
        "session_utc": SESSION,
        "panel_path_fclr001": str(PANEL_FCLR001),
        "panel_sha256_fclr001": PANEL_FCLR001_SHA256,
        "panel_path_liquidation": str(PANEL_LIQ),
        "panel_sha256_liquidation": PANEL_LIQ_SHA256,
        "panel_hash_verified_fclr001": actual_fclr001_sha == PANEL_FCLR001_SHA256,
        "panel_hash_verified_liquidation": actual_liq_sha == PANEL_LIQ_SHA256,
        "mechanism": "alternative_regime_conditioning_rv168_rv24_vol_of_vol_terciles",
        "estimand": "alternative_regime_conditioning_rv168_rv24_vol_of_vol_terciles",
        "outcome_data_inspected_before_freeze": False,
        "overlapping_coins": OVERLAPPING_COINS,
        "coin_name_mapping": COIN_MAP,
        "alternative_regime_variable": "rv168h / rv24h volatility-of-volatility ratio (market-wide per hour, terciled low/mid/high)",
        "n_joined_coin_hours": int(len(joined)),
        "n_eval_eligible_coin_hours": int(len(joined_eval)),
        "n_unique_shared_hours": int(joined_eval["hour"].nunique()),
        "hours_per_vov_tercile": hours_per_terc,
        "mean_abs_rv_by_tercile": mean_abs_rv_by_terc,
        "mean_abs_notional_weighted_liq_by_tercile": mean_abs_liq_by_terc,
        "seed": SEED,
        "n_bootstrap_reps": N_BOOT,
        "alpha": ALPHA,
        "materiality_floor": MATERIALITY_FLOOR,
        "min_coins_per_hour": MIN_COINS_PER_HOUR,
        "joint_family_size": len(all_family_names),
        "holm_correction": "holm",
        "primary_a_tercile": PRIMARY_A_TERCILE,
        "primary_b_terciles": PRIMARY_B_TERCILES,
        "primary_b_pass_rule": PRIMARY_B_PASS_RULE,
        "primary_a_tests": primary_a_tests,
        "primary_b_tests": primary_b_tests,
        "baseline_tests": [t for t in all_family_names if t.endswith("_baseline_rv") or t.endswith("_baseline_notional_weighted")],
        "tests": tests,
        "primary_a_passed": bool(primary_a_passed),
        "primary_b_passed": bool(primary_b_passed),
        "gate": {
            "ci_supports_improvement_primary_a": bool(primary_a_passed),
            "ci_supports_improvement_primary_b": bool(primary_b_passed),
            "holm_passes_primary_a": any(tests[t].get("holm_passes", False) for t in primary_a_tests_funding),
            "holm_passes_primary_b": any(tests[t].get("holm_passes", False) for t in primary_b_tests_funding),
            "materiality_met_primary_a": any(tests[t]["materiality_floor_met"] for t in primary_a_tests_funding),
            "materiality_met_primary_b": any(tests[t]["materiality_floor_met"] for t in primary_b_tests_funding),
            "gate_passed": bool(gate_passed),
            "verdict": verdict,
        },
        "verdict": verdict,
        "cross_panel_reconciliation": recon,
        "cross_reference": {
            "fclr_xsec_002_high_rv_funding_ci": [0.0046, 0.2348],
            "fclr_xsec_002_verdict": "SUPPORTED (high-RV tercile, next-hour RV)",
            "fclr_xsec_004_low_rv_funding_ci": [448605.26, 841155.73],
            "fclr_xsec_004_verdict": "SUPPORTED (count-based, low-RV tercile)",
            "fclr_xsec_005_low_rv_funding_ci": [452972.90, 850198.89],
            "fclr_xsec_005_verdict": "SUPPORTED (notional-weighted, low-RV tercile)",
            "fclr_xsec_006_all_buckets_funding_ci": {"asian": [162051, 521424], "european": [334550, 782272], "us": [94750, 698082]},
            "fclr_xsec_006_verdict": "SUPPORTED (notional-weighted, all three UTC session buckets)",
            "question": "does the regime-conditioned funding effect replicate under RV168/RV24 volatility-of-volatility terciles instead of RV tercile or UTC session bucket",
        },
    }

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    out_path = OUT_DIR / f"fclr_xsec008_evaluation_{SESSION}.json"
    with open(out_path, "w") as fh:
        json.dump(results, fh, indent=2)
    print(f"\nSaved evaluation to {out_path}")


if __name__ == "__main__":
    main()
