#!/usr/bin/env python3
"""
FCLR-XSEC-006 independent reproducibility recompute.

Independently recomputes the UTC-session-bucketed (Asian/European/US)
regime-conditioned funding effect on next-hour NOTIONAL-WEIGHTED observed
liquidation intensity from the frozen combined metpie+ironflow panel
(session_20261121T010934Z), reproducing the FCLR-XSEC-006 evaluation under a
SEPARATE code path to confirm the verdict is not an artifact of a single
implementation.

Design (distinct estimand from FCLR-STARTER-001 / FCLR-XSEC-001 / FCLR-XSEC-002 /
FCLR-XSEC-003 / FCLR-XSEC-004 / FCLR-XSEC-005 and from the daily liquidation
ordering/QLIKE tests):
  - Unit: eligible coin x closed UTC hour t.
  - Target: next-hour NOTIONAL-WEIGHTED observed liquidation intensity =
    sum(notional_usd) of observed liquidation events of that coin in hour t+1
    (shift -1 per coin). NOT event count.
  - Regime: UTC trading-session bucket at t assigned ex-ante by clock hour:
            Asian [00:00,08:00), European [08:00,16:00), US [16:00,24:00);
            hour eligible if >= 3 coins.
  - Predictor: within-(hour, bucket) cross-sectional abs_fund_pct rank,
               high vs low funding; paired next-hour notional-weighted intensity contrast.
  - Baseline: within-bucket RV persistence (coin's own rv24h at t, high vs low).
  - Inference: block bootstrap across whole UTC hours within each bucket
               (seed 20261121, 2000 reps), Holm over 6 tests, 2% materiality
               floor. Verdict SUPPORTED only if a funding-contrast CI excludes
               zero AND Holm passes AND materiality floor cleared.
No network, no paid/credentialed data, no holdout inspected before freeze.
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
SESSION = "20261121T010934Z"
OUT_DIR = REPO / "research_state" / f"session_{SESSION}"
OUT_JSON = OUT_DIR / f"fclr_xsec006_recompute_{SESSION}.json"
SEED = 20261121
N_BOOT = 2000
ALPHA = 0.05
MATERIALITY_FLOOR = 0.02
MIN_COINS_PER_HOUR = 3

BUCKETS = {"asian": (0, 8), "european": (8, 16), "us": (16, 24)}


def load_panel() -> pd.DataFrame:
    df = pd.read_parquet(PANEL)
    df = df.sort_values(["coin", "timestamp"]).reset_index(drop=True)
    return df


def hourly_intensity(df: pd.DataFrame) -> pd.DataFrame:
    """Aggregate event-level rows to one (coin, hour) intensity row."""
    df = df.copy()
    df["hour_period"] = df["timestamp"].dt.to_period("h")
    agg = (
        df.groupby(["coin", "hour_period"])
        .agg(
            notional_weighted_intensity=("notional_usd", "sum"),  # PRIMARY: dollar severity
            event_count=("notional_usd", "size"),                 # SECONDARY: count
            rv24h=("rv24h", "mean"),
            abs_fund_pct=("abs_fund_pct", "mean"),
        )
        .reset_index()
    )
    agg["hour"] = agg["hour_period"].dt.to_timestamp()
    return agg


def next_hour_target(agg: pd.DataFrame) -> pd.DataFrame:
    agg = agg.sort_values(["coin", "hour"]).reset_index(drop=True)
    agg["next_notional_weighted"] = agg.groupby("coin")["notional_weighted_intensity"].shift(-1)
    agg["next_event_count"] = agg.groupby("coin")["event_count"].shift(-1)
    return agg[agg["next_notional_weighted"].notna()].copy()


def assign_bucket(agg: pd.DataFrame) -> pd.DataFrame:
    agg = agg.copy()
    agg["utc_hour"] = agg["hour"].dt.hour

    def bucket(uh):
        for name, (lo, hi) in BUCKETS.items():
            if lo <= uh < hi:
                return name
        return None

    agg["bucket"] = agg["utc_hour"].map(bucket)
    return agg


def market_rv_per_hour(agg: pd.DataFrame) -> pd.DataFrame:
    mw = (
        agg.groupby("hour")["rv24h"]
        .agg(mw_rv="mean", mw_n="count")
        .reset_index()
    )
    agg = agg.merge(mw, on="hour", how="left")
    return agg[agg["mw_n"] >= MIN_COINS_PER_HOUR].copy()


def bucket_split(agg: pd.DataFrame):
    agg = agg[agg["bucket"].notna()].copy()
    return agg


def paired_diff(agg_reg: pd.DataFrame, group_col: str, outcome_col: str) -> np.ndarray:
    stats = (
        agg_reg.groupby(["hour", group_col])[outcome_col]
        .agg(mean_val="mean", cnt="count")
        .reset_index()
    )
    if stats.empty:
        return np.array([], dtype=float)
    means = stats.pivot_table(index="hour", columns=group_col, values="mean_val", aggfunc="first")
    counts = stats.pivot_table(index="hour", columns=group_col, values="cnt", aggfunc="first")
    means.columns.name = None
    counts.columns.name = None
    means = means.join(counts.add_suffix("_c"))
    mean_cols = [c for c in means.columns if not str(c).endswith("_c")]
    if len(mean_cols) < 2:
        return np.array([], dtype=float)
    a, b = sorted(mean_cols)[0], sorted(mean_cols)[1]
    both = means[means[a].notna() & means[b].notna()].copy()
    return (both[a] - both[b]).to_numpy(dtype=float)


def funding_groups(agg_reg: pd.DataFrame) -> pd.DataFrame:
    agg_reg = agg_reg.copy()
    agg_reg["fund_rank"] = agg_reg.groupby(["hour", "bucket"])["abs_fund_pct"].rank(
        method="average", ascending=False
    )
    nn = agg_reg.groupby(["hour", "bucket"])["coin"].transform("nunique")
    agg_reg["fund_pct"] = agg_reg["fund_rank"] / nn
    agg_reg["group"] = np.where(agg_reg["fund_pct"] <= 0.5, "hi", "lo")
    return agg_reg


def rv_persistence_groups(agg_reg: pd.DataFrame) -> pd.DataFrame:
    agg_reg = agg_reg.copy()
    agg_reg["rv_rank"] = agg_reg.groupby(["hour", "bucket"])["rv24h"].rank(
        method="average", ascending=False
    )
    nn = agg_reg.groupby(["hour", "bucket"])["coin"].transform("nunique")
    agg_reg["rv_pct"] = agg_reg["rv_rank"] / nn
    agg_reg["group"] = np.where(agg_reg["rv_pct"] <= 0.5, "hi", "lo")
    return agg_reg


def bootstrap_ci(values: np.ndarray, seed: int, n_rep: int = N_BOOT):
    rng = np.random.RandomState(seed)
    boot = np.empty(n_rep, dtype=float)
    for b in range(n_rep):
        boot[b] = rng.choice(values, size=len(values), replace=True).mean()
    ci_low = float(np.percentile(boot, 2.5))
    ci_high = float(np.percentile(boot, 97.5))
    p = float(2 * min((boot >= 0).mean(), (boot <= 0).mean()))
    return ci_low, ci_high, p


def holm(p_vals: list[float]) -> list[float]:
    order = sorted(range(len(p_vals)), key=lambda i: p_vals[i])
    adj = [0.0] * len(p_vals)
    m = len(p_vals)
    for rank, i in enumerate(order):
        adj[i] = min(1.0, p_values[i] * (m - rank)) if False else min(1.0, p_vals[i] * (m - rank))
    return adj


def test_block(agg_reg: pd.DataFrame, group_col: str, outcome_col: str, construct: str, mean_abs: float) -> dict:
    diff = paired_diff(agg_reg, group_col, outcome_col)
    n = int(len(diff))
    if n == 0:
        return {
            "construct": construct,
            "n_hours": 0,
            "mean_diff": None,
            "ci_low": None,
            "ci_high": None,
            "p_value": None,
            "ci_excludes_zero": False,
            "materiality_effect": None,
            "materiality_floor_met": False,
        }
    mean_diff = float(diff.mean())
    ci_low, ci_high, p = bootstrap_ci(diff, SEED)
    ci_excludes = bool(ci_low > 0 or ci_high < 0)
    mat_eff = float(abs(mean_diff) / mean_abs) if mean_abs > 0 else None
    return {
        "construct": construct,
        "n_hours": n,
        "mean_diff": mean_diff,
        "ci_low": ci_low,
        "ci_high": ci_high,
        "p_value": p,
        "ci_excludes_zero": ci_excludes,
        "positive_diff_count": int((diff > 0).sum()),
        "mean_abs_outcome": mean_abs,
        "materiality_effect": mat_eff,
        "materiality_floor_met": bool(mat_eff is not None and mat_eff >= MATERIALITY_FLOOR),
    }


def main() -> None:
    actual_sha = hashlib.sha256(PANEL.read_bytes()).hexdigest()
    assert actual_sha == PANEL_SHA256, f"panel hash mismatch: {actual_sha}"
    df = load_panel()
    agg = hourly_intensity(df)
    agg = next_hour_target(agg)
    agg = assign_bucket(agg)
    agg = bucket_split(agg)
    agg = market_rv_per_hour(agg)

    hours_per_bucket = {
        b: int(agg[agg["bucket"] == b]["hour"].nunique()) for b in BUCKETS
    }

    mean_abs_notional = {
        b: float(agg[agg["bucket"] == b]["next_notional_weighted"].abs().mean())
        for b in BUCKETS
    }
    mean_abs_count = {
        b: float(agg[agg["bucket"] == b]["next_event_count"].abs().mean())
        for b in BUCKETS
    }

    tests: dict[str, dict] = {}
    df_f = funding_groups(agg.copy())
    for bucket in BUCKETS:
        sub = df_f[df_f["bucket"] == bucket].copy()
        tests[f"{bucket}_funding_contrast_notional_weighted"] = test_block(
            sub, "group", "next_notional_weighted", "funding_notional_weighted", mean_abs_notional[bucket]
        )

    df_r = rv_persistence_groups(agg.copy())
    for bucket in BUCKETS:
        sub = df_r[df_r["bucket"] == bucket].copy()
        tests[f"{bucket}_rv_persistence_baseline_notional_weighted"] = test_block(
            sub, "group", "next_notional_weighted", "persistence_notional_weighted", mean_abs_notional[bucket]
        )

    # Cross-reference: count-based outcome
    for bucket in BUCKETS:
        sub = df_f[df_f["bucket"] == bucket].copy()
        tests[f"{bucket}_funding_contrast_count_based_crossref"] = test_block(
            sub, "group", "next_event_count", "funding_count_based_crossref", mean_abs_count[bucket]
        )

    # Holm over primary notional-weighted family (6 tests)
    primary_names = [t for t in tests.keys() if t.endswith("_notional_weighted")]
    p_vals = [tests[t]["p_value"] for t in primary_names]
    adj = holm(p_vals)
    for t, a in zip(primary_names, adj):
        tests[t]["holm_adj_p"] = float(a)
        tests[t]["holm_passes"] = bool(a < ALPHA)

    # Cross-ref Holm (info only)
    crossref_names = [t for t in tests.keys() if t.endswith("_crossref")]
    if crossref_names:
        crossref_p = [tests[t]["p_value"] for t in crossref_names]
        crossref_adj = holm(crossref_p)
        for t, a in zip(crossref_names, crossref_adj):
            tests[t]["holm_adj_p_crossref"] = float(a)

    funding_tests = [t for t in primary_names if t.endswith("_funding_contrast_notional_weighted")]
    gate_passed = any(
        tests[t]["ci_excludes_zero"]
        and tests[t]["holm_passes"]
        and tests[t]["materiality_floor_met"]
        for t in funding_tests
    )
    verdict = "SUPPORTED" if gate_passed else "NOT_SUPPORTED"

    results = {
        "experiment_id": f"FCLR-XSEC-006-RECOMPUTE-{SESSION}",
        "session_utc": SESSION,
        "panel_path": str(PANEL),
        "panel_sha256": PANEL_SHA256,
        "panel_hash_verified": actual_sha == PANEL_SHA256,
        "estimand": "utc_session_bucket_conditioned_cross_sectional_funding_effect_on_next_hour_notional_weighted_liquidation_intensity",
        "mechanism": "UTC trading-session bucket conditioning of the funding effect applied to NOTIONAL-WEIGHTED observed liquidation intensity (independent recompute)",
        "outcome_data_inspected_before_freeze": False,
        "seed": SEED,
        "n_bootstrap_reps": N_BOOT,
        "alpha": ALPHA,
        "materiality_floor": MATERIALITY_FLOOR,
        "family_size": len(primary_names),
        "holm_correction": "holm",
        "hours_per_bucket": hours_per_bucket,
        "bucket_edges_utc": BUCKETS,
        "tests": tests,
        "primary_test_names": primary_names,
        "funding_tests_notional_weighted": funding_tests,
        "cross_reference": {
            "fclr_xsec_004_low_rv_funding_ci": [448605.26, 841155.73],
            "fclr_xsec_004_low_rv_verdict": "SUPPORTED (count-based, low-RV tercile)",
            "fclr_xsec_004_high_rv_verdict": "NOT_SUPPORTED (honest null)",
            "fclr_xsec_005_low_rv_funding_ci": [452972.899202, 850198.885235],
            "fclr_xsec_005_low_rv_verdict": "SUPPORTED (notional-weighted, low-RV tercile)",
            "fclr_xsec_005_high_rv_verdict": "NOT_SUPPORTED (honest null)",
        },
        "gate_passed": bool(gate_passed),
        "verdict": verdict,
        "reproduces_fclr_xsec006_evaluation": verdict == "SUPPORTED",
    }
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    with open(OUT_JSON, "w") as fh:
        json.dump(results, fh, indent=2)
    print(f"Recompute verdict: {verdict} (gate_passed={gate_passed})")
    print(f"Saved {OUT_JSON}")


if __name__ == "__main__":
    main()
