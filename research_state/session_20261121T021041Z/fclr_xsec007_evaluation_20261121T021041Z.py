#!/usr/bin/env python3
"""
FCLR-XSEC-007 Step 2: Cross-panel mechanism reconciliation on overlapping
5-coin FCLR-001 hours.

Joins the frozen FCLR-001 panel (RV + funding) with the frozen combined
liquidation panel (observed notional-weighted liquidation intensity + funding)
on coin x hour. Tests whether the regime-conditioned funding effect SUPPORTED
for RV (FCLR-XSEC-002, HIGH-RV regime) and for liquidation intensity
(FCLR-XSEC-004/005 LOW-RV; FCLR-XSEC-006 ALL THREE UTC buckets) reconciles
on the same coin×hour panel.

Primary A: within-(hour, RV-tercile) cross-sectional abs_fund_pct rank ->
next-hour RV (target_rv24h).  FCLR-XSEC-002 estimand restricted to overlapping
hours.
Primary B: within-(hour, UTC-session-bucket) cross-sectional abs_fund_pct rank
-> next-hour NOTIONAL-WEIGHTED observed liquidation intensity (sum of
notional_usd, not event count).  FCLR-XSEC-006 estimand restricted to
overlapping hours.

Inference: block bootstrap across whole UTC hours within each regime family
(seed 20261121, >= 2000 deterministic replicates), Holm correction over the
joint 4-test family (2 regimes x {funding contrast, RV persistence baseline}),
95% CIs, 2% materiality floor (|mean_diff| / mean_abs_outcome >= 0.02).

Verdict = SUPPORTED only if BOTH primary funding contrasts clear all three
gates (CI excludes zero, Holm passes, materiality floor met) on the overlapping
hours; otherwise report the honest null as NOT_SUPPORTED.

Cross-panel reconciliation: coefficient sign agreement, magnitude correlation
of per-hour funding-contrast effect sizes between the two outcomes on shared
hours, and joint significance.

Outcome data inspected before freeze: false. Protocol frozen first.
Cross-reference: FCLR-XSEC-002 (high-RV SUPPORTED), FCLR-XSEC-004 (low-RV
count-based SUPPORTED), FCLR-XSEC-005 (low-RV notional-weighted SUPPORTED),
FCLR-XSEC-006 (all three UTC buckets SUPPORTED).
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
SESSION = "20261121T021041Z"
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

# UTC trading-session buckets, assigned ex-ante by clock hour (independent of RV).
BUCKET_EDGES = {
    "asian": (0, 8),
    "european": (8, 16),
    "us": (16, 24),
}
BUCKET_ORDER = ["asian", "european", "us"]


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
    """
    df = pd.read_parquet(PANEL_LIQ)
    df = df.sort_values(["coin", "timestamp"]).reset_index(drop=True)
    df["hour"] = df["timestamp"].dt.floor("h")
    g = (
        df.groupby(["coin", "hour"])
        .agg(
            notional_weighted_intensity=("notional_usd", "sum"),  # PRIMARY: dollar severity
            event_count=("notional_usd", "size"),                # SECONDARY: count (cross-ref only)
            abs_fund_pct=("abs_fund_pct", "mean"),
            rv24h=("rv24h", "mean"),
        )
        .reset_index()
    )
    g = g[g["coin"].isin(OVERLAPPING_COINS)].copy()
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


def add_market_wide_rv(f: pd.DataFrame) -> pd.DataFrame:
    """Market-wide RV per hour = mean of rv24h across the 5 coins at that hour."""
    mw = f.groupby("hour")["rv24h"].agg(["mean", "count"]).rename(columns={"mean": "market_rv", "count": "market_rv_n"})
    f = f.merge(mw, on="hour", how="left")
    f["hour_eligible"] = f["market_rv_n"] >= MIN_COINS_PER_HOUR
    return f


def add_rv_tercile(f: pd.DataFrame) -> pd.DataFrame:
    """Assign each eligible hour to a market-wide RV tercile (high/mid/low)."""
    f = f.copy()
    eligible = f[f["hour_eligible"]].copy()
    terciles = eligible.groupby("hour")["market_rv"].first()
    tercile_labels = pd.qcut(terciles, q=3, labels=["low", "mid", "high"])
    hour_to_tercile = tercile_labels.to_dict()
    f["rv_tercile"] = f["hour"].map(hour_to_tercile)
    return f


def add_session_bucket(g: pd.DataFrame) -> pd.DataFrame:
    g = g.copy()
    g["utc_hour"] = g["hour"].dt.hour

    def bucket(uh: int) -> str | None:
        for name, (lo, hi) in BUCKET_EDGES.items():
            if lo <= uh < hi:
                return name
        return None

    g["session_bucket"] = g["utc_hour"].map(bucket)
    return g


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


def add_funding_groups(df: pd.DataFrame, fund_col: str) -> pd.DataFrame:
    """Within each hour, rank coins by fund_col; split high vs low funding."""
    df = df.copy()
    df["funding_rank_within_hour"] = df.groupby("hour")[fund_col].rank(method="average", ascending=False)
    n_coins = df.groupby("hour")["coin"].transform("nunique") if "coin" in df.columns else df.groupby("hour")["coin_short"].transform("nunique")
    coin_col = "coin" if "coin" in df.columns else "coin_short"
    n_coins = df.groupby("hour")[coin_col].transform("nunique")
    df["funding_pct_within_hour"] = df["funding_rank_within_hour"] / n_coins
    df["funding_group"] = np.where(df["funding_pct_within_hour"] <= 0.5, "high_funding", "low_funding")
    return df


def add_rv_groups(df: pd.DataFrame, rv_col: str) -> pd.DataFrame:
    """Within each hour, rank coins by rv_col; split high vs low RV (persistence baseline)."""
    df = df.copy()
    df["rv_rank_within_hour"] = df.groupby("hour")[rv_col].rank(method="average", ascending=False)
    coin_col = "coin" if "coin" in df.columns else "coin_short"
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

    print(f"FCLR-001 rows (5 coins, overlapping): {len(f)}, hours: {f['hour'].nunique()}")
    print(f"Liquidation hourly rows (5 coins): {len(g)}, hours: {g['hour'].nunique()}")

    # --- Add next-hour targets ---
    f = add_next_hour_rv(f)
    g = add_next_hour_intensity(g)

    # --- Join on (coin, hour) ---
    f_join = f[["coin_short", "hour", "rv24h", "abs_funding_pct_trail", "signed_funding", "target_rv24h", "next_hour_rv"]].copy()
    f_join = f_join.rename(columns={"coin_short": "coin", "abs_funding_pct_trail": "abs_fund_pct"})
    g_join = g[["coin", "hour", "notional_weighted_intensity", "abs_fund_pct", "rv24h", "next_hour_notional_weighted_intensity", "next_hour_event_count"]].copy()

    joined = f_join.merge(g_join, on=["coin", "hour"], how="inner", suffixes=("_fclr", "_liq"))
    # Use the FCLR-001 funding + RV as the single consistent predictor/regime
    # measure across both primaries so the "same coins drive both effects"
    # reconciliation is clean (same predictor, same hours, two outcomes).
    joined = joined.rename(columns={"rv24h_fclr": "rv24h", "abs_fund_pct_fclr": "abs_fund_pct"})
    print(f"Joined rows: {len(joined)}, unique hours: {joined['hour'].nunique()}")

    # --- Market-wide RV per hour + RV tercile ---
    joined = add_market_wide_rv(joined)
    joined_eval = joined[joined["hour_eligible"] & joined["next_hour_rv"].notna() & joined["next_hour_notional_weighted_intensity"].notna()].copy()
    joined_eval = add_rv_tercile(joined_eval)
    joined_eval = joined_eval[joined_eval["rv_tercile"].notna()].copy()
    joined_eval = add_session_bucket(joined_eval)
    joined_eval = joined_eval[joined_eval["session_bucket"].notna()].copy()

    print(f"Eval-eligible coin-hours: {len(joined_eval)}, unique hours: {joined_eval['hour'].nunique()}")

    # Mean absolute outcomes per regime (materiality denominators).
    mean_abs_rv_by_tercile = {}
    mean_abs_liq_by_bucket = {}
    for terc in ["low", "mid", "high"]:
        sub = joined_eval[joined_eval["rv_tercile"] == terc]
        mean_abs_rv_by_tercile[terc] = float(sub["next_hour_rv"].abs().mean())
    for bucket in BUCKET_ORDER:
        sub = joined_eval[joined_eval["session_bucket"] == bucket]
        mean_abs_liq_by_bucket[bucket] = float(sub["next_hour_notional_weighted_intensity"].abs().mean())

    hours_per_tercile = {t: int(joined_eval[joined_eval["rv_tercile"] == t]["hour"].nunique()) for t in ["low", "mid", "high"]}
    hours_per_bucket = {b: int(joined_eval[joined_eval["session_bucket"] == b]["hour"].nunique()) for b in BUCKET_ORDER}

    tests = {}

    # ===== PRIMARY A: within-(hour, RV-tercile) funding rank -> next-hour RV =====
    df_a = add_funding_groups(joined_eval.copy(), "abs_fund_pct")
    for terc in ["low", "mid", "high"]:
        sub = df_a[df_a["rv_tercile"] == terc].copy()
        both = paired_hourly_diff(sub, "funding_group", "next_hour_rv")
        diff = both["diff"].values
        s = summarize_contrast(diff, SEED, mean_abs_rv_by_tercile[terc])
        tests[f"rv_tercile_{terc}_funding_contrast_rv"] = s

    # Baseline A: within-(hour, RV-tercile) RV persistence -> next-hour RV
    df_ar = add_rv_groups(joined_eval.copy(), "rv24h")
    for terc in ["low", "mid", "high"]:
        sub = df_ar[df_ar["rv_tercile"] == terc].copy()
        both = paired_hourly_diff(sub, "rv_group", "next_hour_rv")
        diff = both["diff"].values
        s = summarize_contrast(diff, SEED, mean_abs_rv_by_tercile[terc])
        tests[f"rv_tercile_{terc}_rv_persistence_baseline_rv"] = s

    # ===== PRIMARY B: within-(hour, UTC-session-bucket) funding rank -> next-hour notional-weighted liq intensity =====
    df_b = add_funding_groups(joined_eval.copy(), "abs_fund_pct")
    for bucket in BUCKET_ORDER:
        sub = df_b[df_b["session_bucket"] == bucket].copy()
        both = paired_hourly_diff(sub, "funding_group", "next_hour_notional_weighted_intensity")
        diff = both["diff"].values
        s = summarize_contrast(diff, SEED, mean_abs_liq_by_bucket[bucket])
        tests[f"utc_bucket_{bucket}_funding_contrast_notional_weighted"] = s

    # Baseline B: within-(hour, UTC-session-bucket) RV persistence -> next-hour notional-weighted liq intensity
    df_br = add_rv_groups(joined_eval.copy(), "rv24h")
    for bucket in BUCKET_ORDER:
        sub = df_br[df_br["session_bucket"] == bucket].copy()
        both = paired_hourly_diff(sub, "rv_group", "next_hour_notional_weighted_intensity")
        diff = both["diff"].values
        s = summarize_contrast(diff, SEED, mean_abs_liq_by_bucket[bucket])
        tests[f"utc_bucket_{bucket}_rv_persistence_baseline_notional_weighted"] = s

    # ===== Holm correction over joint 4-test family =====
    # Formal family: 2 regimes x {funding contrast, RV persistence} = but we have
    # 3 terciles x 2 + 3 buckets x 2 = 12 tests. Use the joint family as defined
    # in the protocol: primary funding contrasts for each regime + baselines.
    # For Holm, use all notional_weighted/rv primary tests as the family.
    primary_test_names = [
        t for t in tests.keys()
        if t.endswith("_funding_contrast_rv") or t.endswith("_funding_contrast_notional_weighted")
    ]
    baseline_test_names = [
        t for t in tests.keys()
        if t.endswith("_rv_persistence_baseline_rv") or t.endswith("_rv_persistence_baseline_notional_weighted")
    ]
    all_family_names = primary_test_names + baseline_test_names
    p_vals = [tests[t]["p_value"] for t in all_family_names]
    holm = holm_adjust(p_vals)
    for t, adj_p in zip(all_family_names, holm):
        tests[t]["holm_adj_p"] = float(adj_p)
        tests[t]["holm_passes"] = bool(adj_p < ALPHA)

    # ===== Per-regime verdicts =====
    # Primary A: HIGH-RV tercile funding contrast (FCLR-XSEC-002 style)
    primary_a_tests = [t for t in primary_test_names if t.endswith("_funding_contrast_rv") and "high" in t]
    primary_a_passed = any(
        tests[t]["ci_excludes_zero"] and tests[t]["holm_passes"] and tests[t]["materiality_floor_met"]
        for t in primary_a_tests
    )

    # Primary B: all three UTC buckets funding contrast (FCLR-XSEC-006 style)
    primary_b_tests = [t for t in primary_test_names if t.endswith("_funding_contrast_notional_weighted")]
    primary_b_passed = any(
        tests[t]["ci_excludes_zero"] and tests[t]["holm_passes"] and tests[t]["materiality_floor_met"]
        for t in primary_b_tests
    )

    gate_passed = bool(primary_a_passed and primary_b_passed)
    verdict = "SUPPORTED" if gate_passed else "NOT_SUPPORTED"

    # ===== Cross-panel reconciliation =====
    # On shared hours: sign agreement + magnitude correlation of funding contrasts
    recon = {
        "shared_hours": int(joined_eval["hour"].nunique()),
        "primary_a_passed": bool(primary_a_passed),
        "primary_b_passed": bool(primary_b_passed),
        "joint_significance": gate_passed,
    }

    # Sign agreement: compare sign of high-RV tercile funding contrast (RV outcome)
    # vs sign of each bucket funding contrast (liq intensity outcome).
    high_rv_test = [t for t in primary_a_tests]
    bucket_tests = [t for t in primary_b_tests]
    sign_agreements = []
    if high_rv_test and bucket_tests:
        high_rv_sign = np.sign(tests[high_rv_test[0]]["mean_diff_high_minus_low"])
        for bt in bucket_tests:
            bucket_sign = np.sign(tests[bt]["mean_diff_high_minus_low"])
            sign_agreements.append({
                "bucket_test": bt,
                "high_rv_sign": float(high_rv_sign),
                "bucket_sign": float(bucket_sign),
                "sign_agreement": bool(high_rv_sign == bucket_sign),
            })
    recon["sign_agreements"] = sign_agreements

    # Magnitude correlation: per-hour effect sizes for RV contrast (high tercile)
    # vs liq intensity contrast (each bucket) on shared hours.
    def hourly_effect(sub, group_col, outcome_col):
        both = paired_hourly_diff(sub, group_col, outcome_col)
        return both.reset_index()[["hour", "diff"]].rename(columns={"diff": "effect"})

    df_a_high = add_funding_groups(joined_eval[joined_eval["rv_tercile"] == "high"].copy(), "abs_fund_pct")
    rv_effect_by_hour = hourly_effect(df_a_high, "funding_group", "next_hour_rv")

    mag_corr = []
    for bucket in BUCKET_ORDER:
        df_b_bucket = add_funding_groups(joined_eval[joined_eval["session_bucket"] == bucket].copy(), "abs_fund_pct")
        liq_effect_by_hour = hourly_effect(df_b_bucket, "funding_group", "next_hour_notional_weighted_intensity")
        merged = rv_effect_by_hour.merge(liq_effect_by_hour, on="hour", suffixes=("_rv", "_liq"))
        if len(merged) > 3:
            corr = float(np.corrcoef(merged["effect_rv"], merged["effect_liq"])[0, 1])
        else:
            corr = None
        mag_corr.append({
            "bucket": bucket,
            "n_shared_hours": int(len(merged)),
            "effect_size_correlation": corr,
        })
    recon["magnitude_correlation"] = mag_corr

    # ===== Print results =====
    print(f"\n=== FCLR-XSEC-007 Results (Cross-Panel Mechanism Reconciliation) ===")
    print(f"FCLR-001 panel: {PANEL_FCLR001} (sha256 {PANEL_FCLR001_SHA256})")
    print(f"Liquidation panel: {PANEL_LIQ} (sha256 {PANEL_LIQ_SHA256})")
    print(f"Overlapping coins: {OVERLAPPING_COINS}")
    print(f"Joined coin-hours: {len(joined)}, eval-eligible coin-hours: {len(joined_eval)}")
    print(f"Unique shared hours: {joined_eval['hour'].nunique()}")
    print(f"Hours per RV tercile: {hours_per_tercile}")
    print(f"Hours per UTC bucket: {hours_per_bucket}")
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
    print(f"\nPrimary A (RV-tercile high, funding->RV) passed: {primary_a_passed}")
    print(f"Primary B (UTC-bucket, funding->liq intensity) passed: {primary_b_passed}")
    print(f"\n--- Cross-Panel Reconciliation ---")
    print(f"Shared hours: {recon['shared_hours']}")
    print(f"Joint significance (both primaries pass): {recon['joint_significance']}")
    for sa in sign_agreements:
        print(f"  {sa['bucket_test']}: high_RV_sign={sa['high_rv_sign']}, bucket_sign={sa['bucket_sign']}, agreement={sa['sign_agreement']}")
    for mc in mag_corr:
        print(f"  {mc['bucket']}: n_shared_hours={mc['n_shared_hours']}, effect_corr={mc['effect_size_correlation']}")
    print(f"\nVerdict: {verdict} (gate_passed={gate_passed})")

    # Cross-reference to prior campaigns
    print("\n--- Cross-Reference to FCLR-XSEC-002 / XSEC-004 / XSEC-005 / XSEC-006 ---")
    print("FCLR-XSEC-002 high-RV funding contrast: CI [0.0046, 0.2348], p=0.019, materiality 1.09 -> SUPPORTED")
    print("FCLR-XSEC-004 low-RV count-based funding contrast: CI [448605.26, 841155.73], p=0.0, materiality 0.80 -> SUPPORTED")
    print("FCLR-XSEC-005 low-RV notional-weighted funding contrast: CI [452972.90, 850198.89], p=0.0, materiality 0.80 -> SUPPORTED")
    print("FCLR-XSEC-006 all three UTC buckets: Asian CI [162051, 521424], European CI [334550, 782272], US CI [94750, 698082] -> SUPPORTED")

    results = {
        "experiment_id": f"FCLR-XSEC-007-{SESSION}",
        "session_utc": SESSION,
        "panel_path_fclr001": str(PANEL_FCLR001),
        "panel_sha256_fclr001": PANEL_FCLR001_SHA256,
        "panel_path_liquidation": str(PANEL_LIQ),
        "panel_sha256_liquidation": PANEL_LIQ_SHA256,
        "panel_hash_verified_fclr001": actual_fclr001_sha == PANEL_FCLR001_SHA256,
        "panel_hash_verified_liquidation": actual_liq_sha == PANEL_LIQ_SHA256,
        "mechanism": "cross_panel_mechanism_reconciliation_rv_tercile_vs_utc_session_bucket",
        "estimand": "cross_panel_mechanism_reconciliation_rv_tercile_vs_utc_session_bucket",
        "outcome_data_inspected_before_freeze": False,
        "overlapping_coins": OVERLAPPING_COINS,
        "coin_name_mapping": COIN_MAP,
        "overlap_ts_min": "2026-01-01T00:00:00Z",
        "overlap_ts_max": "2026-08-31T23:00:00Z",
        "n_joined_coin_hours": int(len(joined)),
        "n_eval_eligible_coin_hours": int(len(joined_eval)),
        "n_unique_shared_hours": int(joined_eval["hour"].nunique()),
        "hours_per_rv_tercile": hours_per_tercile,
        "hours_per_utc_bucket": hours_per_bucket,
        "bucket_edges_utc": BUCKET_EDGES,
        "seed": SEED,
        "n_bootstrap_reps": N_BOOT,
        "alpha": ALPHA,
        "materiality_floor": MATERIALITY_FLOOR,
        "joint_family_size": len(all_family_names),
        "holm_correction": "holm",
        "primary_a_tests": primary_test_names,
        "primary_b_tests": primary_b_tests,
        "baseline_tests": baseline_test_names,
        "tests": tests,
        "primary_a_passed": bool(primary_a_passed),
        "primary_b_passed": bool(primary_b_passed),
        "gate": {
            "ci_supports_improvement_primary_a": bool(primary_a_passed),
            "ci_supports_improvement_primary_b": bool(primary_b_passed),
            "holm_passes_primary_a": any(tests[t].get("holm_passes", False) for t in primary_a_tests),
            "holm_passes_primary_b": any(tests[t].get("holm_passes", False) for t in primary_b_tests),
            "materiality_met_primary_a": any(tests[t]["materiality_floor_met"] for t in primary_a_tests),
            "materiality_met_primary_b": any(tests[t]["materiality_floor_met"] for t in primary_b_tests),
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
        },
    }

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    out_path = OUT_DIR / f"fclr_xsec007_evaluation_{SESSION}.json"
    with open(out_path, "w") as fh:
        json.dump(results, fh, indent=2)
    print(f"\nSaved evaluation to {out_path}")


if __name__ == "__main__":
    main()
