#!/usr/bin/env python3
"""
FCLR-XSEC-008 Step 3: INDEPENDENT recompute (second code path).

Reproduces the FCLR-XSEC-008 alternative-regime conditioning evaluation from the
frozen panels using a deliberately different implementation than the evaluation
script, so the verdict is not a single-implementation artifact.

Design differences vs fclr_xsec008_evaluation_*.py:
  - numpy.random.Generator (PCG64) block bootstrap instead of RandomState;
  - hour-block resampling via Generator.integers index draws;
  - manual dictionary-based (hour, tercile, group) assembly instead of pandas pivot;
  - independent Holm step-down implementation;
  - same estimand: voV (rv168h/rv24h) ratio terciles, Primary A = HIGH tercile funding->RV,
    Primary B = any-tercile funding->notional-weighted liq intensity; Holm over joint family;
    2% materiality floor.

Verdict = SUPPORTED only if BOTH primary funding contrasts clear all three gates
(CI excludes zero, Holm passes, materiality >= 0.02); else honest NOT_SUPPORTED.
"""
from __future__ import annotations

import hashlib
import json
from collections import defaultdict
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
RNG_SEED = 20261121
N_BOOT = 2000
ALPHA = 0.05
MATERIALITY_FLOOR = 0.02
MIN_COINS_PER_HOUR = 3

COIN_MAP = {"BTCUSDT": "BTC", "ETHUSDT": "ETH", "BNBUSDT": "BNB", "SOLUSDT": "SOL", "XRPUSDT": "XRP"}
OVERLAPPING_COINS = ["BTC", "ETH", "BNB", "SOL", "XRP"]
VOV_TERCILES = ["low", "mid", "high"]
PRIMARY_A_TERCILE = "high"
PRIMARY_B_TERCILES = ["low", "mid", "high"]


def _ci_pvalue(diff_vals, rng):
    n = len(diff_vals)
    if n == 0:
        return None, None, None, None
    mean_diff = float(np.mean(diff_vals))
    reps = np.empty(N_BOOT, dtype=float)
    idx = np.arange(n)
    for b in range(N_BOOT):
        draw = rng.integers(0, n, size=n)
        reps[b] = float(np.mean(diff_vals[draw]))
    ci_low = float(np.percentile(reps, 2.5))
    ci_high = float(np.percentile(reps, 97.5))
    p_value = float(2.0 * min((reps >= 0.0).mean(), (reps <= 0.0).mean()))
    return mean_diff, ci_low, ci_high, p_value


def _holm(p_vals):
    order = sorted(range(len(p_vals)), key=lambda i: p_vals[i])
    adj = [0.0] * len(p_vals)
    m = len(p_vals)
    for rank, i in enumerate(order):
        adj[i] = min(1.0, float(p_vals[i]) * (m - rank))
    return adj


def main() -> None:
    # --- Verify panel hashes before any computation ---
    actual_fclr001_sha = hashlib.sha256(PANEL_FCLR001.read_bytes()).hexdigest()
    assert actual_fclr001_sha == PANEL_FCLR001_SHA256, f"FCLR-001 hash mismatch: {actual_fclr001_sha}"
    actual_liq_sha = hashlib.sha256(PANEL_LIQ.read_bytes()).hexdigest()
    assert actual_liq_sha == PANEL_LIQ_SHA256, f"Liquidation hash mismatch: {actual_liq_sha}"

    # --- Load FCLR-001 panel ---
    f = pd.read_parquet(PANEL_FCLR001).sort_values(["coin", "ts"]).reset_index(drop=True)
    f["hour"] = f["ts"].dt.floor("h")
    f["coin_short"] = f["coin"].map(COIN_MAP)
    f = f[f["coin_short"].isin(OVERLAPPING_COINS)].copy()
    f = f.rename(columns={"abs_funding_pct_trail": "abs_fund_pct"})
    f["next_hour_rv"] = f.groupby("coin_short")["target_rv24h"].shift(-1)

    # --- Load + aggregate liquidation panel to (coin, hour) ---
    d = pd.read_parquet(PANEL_LIQ).sort_values(["coin", "timestamp"]).reset_index(drop=True)
    d["hour"] = d["timestamp"].dt.floor("h")
    d = d[d["coin"].isin(OVERLAPPING_COINS)].copy()
    g = (
        d.groupby(["coin", "hour"])
        .agg(
            notional_weighted_intensity=("notional_usd", "sum"),
            abs_fund_pct=("abs_fund_pct", "mean"),
            rv24h=("rv24h", "mean"),
            rv168h=("rv168h", "mean"),
        )
        .reset_index()
    )
    g["next_hour_notional_weighted_intensity"] = g.groupby("coin")["notional_weighted_intensity"].shift(-1)

    # --- Join on (coin, hour); single consistent predictor from FCLR-001 ---
    j = f[["coin_short", "hour", "rv24h", "rv168h", "abs_fund_pct", "next_hour_rv"]].copy()
    j = j.rename(columns={"coin_short": "coin"})
    g2 = g[["coin", "hour", "notional_weighted_intensity", "abs_fund_pct", "rv24h", "rv168h", "next_hour_notional_weighted_intensity"]].copy()
    joined = j.merge(g2, on=["coin", "hour"], how="inner", suffixes=("_fclr", "_liq"))
    joined = joined.rename(columns={"rv24h_fclr": "rv24h", "rv168h_fclr": "rv168h", "abs_fund_pct_fclr": "abs_fund_pct"})

    # --- voV ratio per coin-hour; market-wide voV per hour; tercile hours ---
    joined["vov_ratio"] = np.where(
        joined["rv168h"].notna() & joined["rv24h"].notna() & (joined["rv24h"] > 0),
        joined["rv168h"] / joined["rv24h"],
        np.nan,
    )
    mw = joined.groupby("hour")["vov_ratio"].agg(["mean", "count"]).rename(columns={"mean": "market_vov", "count": "n"})
    joined = joined.merge(mw, on="hour", how="left")
    joined = joined[joined["n"] >= MIN_COINS_PER_HOUR].copy()
    hour_vov = joined.groupby("hour")["market_vov"].first()
    terc_labels = pd.qcut(hour_vov, q=3, labels=VOV_TERCILES)
    hour_to_terc = terc_labels.to_dict()
    joined["vov_tercile"] = joined["hour"].map(hour_to_terc)
    joined = joined[joined["vov_tercile"].notna()].copy()
    joined = joined[joined["next_hour_rv"].notna() & joined["next_hour_notional_weighted_intensity"].notna()].copy()

    print(f"Recompute eval-eligible coin-hours: {len(joined)}, unique hours: {joined['hour'].nunique()}")
    print(f"Hours per voV tercile: {joined.groupby('vov_tercile')['hour'].nunique().to_dict()}")

    # Mean abs outcomes per tercile (materiality denominators).
    mean_abs_rv = {t: float(joined.loc[joined["vov_tercile"] == t, "next_hour_rv"].abs().mean()) for t in VOV_TERCILES}
    mean_abs_liq = {t: float(joined.loc[joined["vov_tercile"] == t, "next_hour_notional_weighted_intensity"].abs().mean()) for t in VOV_TERCILES}

    rng = np.random.default_rng(RNG_SEED)

    # Compute within-hour funding rank once for all of joined (single pass).
    sub_all = joined.copy()
    sub_all["fund_rank"] = sub_all.groupby("hour")["abs_fund_pct"].rank(method="average", ascending=False)
    n_per_hour = sub_all.groupby("hour")["coin"].transform("nunique")
    sub_all["fund_pct"] = sub_all["fund_rank"] / n_per_hour
    sub_all["fund_group"] = np.where(sub_all["fund_pct"] <= 0.5, "high_funding", "low_funding")

    # Build per-(hour, tercile) high/low funding diff arrays.
    def build_diffs(outcome_col):
        out = {}
        for terc in VOV_TERCILES:
            sub_t = sub_all[sub_all["vov_tercile"] == terc]
            by_hour = defaultdict(lambda: {"high_funding": [], "low_funding": []})
            for _, row in sub_t.iterrows():
                by_hour[row["hour"]][row["fund_group"]].append(row[outcome_col])
            diffs = []
            for h in sorted(by_hour.keys()):
                g = by_hour[h]
                if len(g["high_funding"]) == 0 or len(g["low_funding"]) == 0:
                    continue
                diffs.append(float(np.mean(g["high_funding"])) - float(np.mean(g["low_funding"])))
            out[terc] = np.array(diffs, dtype=float)
        return out

    rv_diffs = build_diffs("next_hour_rv")
    liq_diffs = build_diffs("next_hour_notional_weighted_intensity")

    # Summaries.
    def summarize(diff_arr, mean_abs_outcome):
        if diff_arr is None or len(diff_arr) == 0:
            return {"n_hours": 0, "mean_diff": None, "ci_low": None, "ci_high": None, "p_value": None,
                    "ci_excludes_zero": False, "materiality_effect": None, "materiality_floor_met": False}
        mean_diff, ci_low, ci_high, p_value = _ci_pvalue(diff_arr, rng)
        ci_excludes_zero = bool(ci_low > 0 or ci_high < 0)
        mat_eff = float(abs(mean_diff) / mean_abs_outcome) if (mean_diff is not None and mean_abs_outcome > 0) else None
        mat_floor = bool(mat_eff is not None and mat_eff >= MATERIALITY_FLOOR)
        return {"n_hours": int(len(diff_arr)), "mean_diff": mean_diff, "ci_low": ci_low, "ci_high": ci_high,
                "p_value": p_value, "ci_excludes_zero": ci_excludes_zero, "materiality_effect": mat_eff,
                "materiality_floor_met": mat_floor}

    test_names = []
    test_pvals = []
    summaries = {}

    # Primary A: HIGH tercile funding->RV.
    for terc in VOV_TERCILES:
        name_a = f"vov_{terc}_funding_rv"
        s_a = summarize(rv_diffs[terc], mean_abs_rv[terc])
        summaries[name_a] = s_a
        test_names.append(name_a); test_pvals.append(s_a["p_value"])
        # baseline A: RV persistence within hour-tercile (high vs low rv24h)
        sub = joined[joined["vov_tercile"] == terc].copy()
        sub["rv_rank"] = sub.groupby("hour")["rv24h"].rank(method="average", ascending=False)
        nph = sub.groupby("hour")["coin"].transform("nunique")
        sub["rv_pct"] = sub["rv_rank"] / nph
        sub["rv_group"] = np.where(sub["rv_pct"] <= 0.5, "high_rv", "low_rv")
        by_hour = defaultdict(lambda: {"high_rv": [], "low_rv": []})
        for _, row in sub.iterrows():
            by_hour[row["hour"]][row["rv_group"]].append(row["next_hour_rv"])
        bd = []
        for h in sorted(by_hour.keys()):
            g2_ = by_hour[h]
            if len(g2_["high_rv"]) == 0 or len(g2_["low_rv"]) == 0:
                continue
            bd.append(float(np.mean(g2_["high_rv"])) - float(np.mean(g2_["low_rv"])))
        name_ba = f"vov_{terc}_rvpersistence_rv"
        s_ba = summarize(np.array(bd, dtype=float), mean_abs_rv[terc])
        summaries[name_ba] = s_ba
        test_names.append(name_ba); test_pvals.append(s_ba["p_value"])

    # Primary B: all terciles funding->liq intensity.
    for terc in VOV_TERCILES:
        name_b = f"vov_{terc}_funding_liq"
        s_b = summarize(liq_diffs[terc], mean_abs_liq[terc])
        summaries[name_b] = s_b
        test_names.append(name_b); test_pvals.append(s_b["p_value"])
        # baseline B: RV persistence within hour-tercile -> liq intensity
        sub = joined[joined["vov_tercile"] == terc].copy()
        sub["rv_rank"] = sub.groupby("hour")["rv24h"].rank(method="average", ascending=False)
        nph = sub.groupby("hour")["coin"].transform("nunique")
        sub["rv_pct"] = sub["rv_rank"] / nph
        sub["rv_group"] = np.where(sub["rv_pct"] <= 0.5, "high_rv", "low_rv")
        by_hour = defaultdict(lambda: {"high_rv": [], "low_rv": []})
        for _, row in sub.iterrows():
            by_hour[row["hour"]][row["rv_group"]].append(row["next_hour_notional_weighted_intensity"])
        bd = []
        for h in sorted(by_hour.keys()):
            g2_ = by_hour[h]
            if len(g2_["high_rv"]) == 0 or len(g2_["low_rv"]) == 0:
                continue
            bd.append(float(np.mean(g2_["high_rv"])) - float(np.mean(g2_["low_rv"])))
        name_bb = f"vov_{terc}_rvpersistence_liq"
        s_bb = summarize(np.array(bd, dtype=float), mean_abs_liq[terc])
        summaries[name_bb] = s_bb
        test_names.append(name_bb); test_pvals.append(s_bb["p_value"])

    holm = _holm(test_pvals)
    for name, adj_p in zip(test_names, holm):
        summaries[name]["holm_adj_p"] = float(adj_p)
        summaries[name]["holm_passes"] = bool(adj_p < ALPHA)

    primary_a_name = f"vov_{PRIMARY_A_TERCILE}_funding_rv"
    primary_a_passed = bool(
        summaries[primary_a_name]["ci_excludes_zero"]
        and summaries[primary_a_name]["holm_passes"]
        and summaries[primary_a_name]["materiality_floor_met"]
    )

    primary_b_names = [f"vov_{t}_funding_liq" for t in PRIMARY_B_TERCILES]
    primary_b_passed = bool(
        any(
            summaries[n]["ci_excludes_zero"] and summaries[n]["holm_passes"] and summaries[n]["materiality_floor_met"]
            for n in primary_b_names
        )
    )

    gate_passed = bool(primary_a_passed and primary_b_passed)
    verdict = "SUPPORTED" if gate_passed else "NOT_SUPPORTED"

    print(f"\n=== FCLR-XSEC-008 Independent Recompute ===")
    print(f"Primary A (voV {PRIMARY_A_TERCILE} funding->RV): passed={primary_a_passed}")
    print(f"  {summaries[primary_a_name]}")
    print(f"Primary B (voV any-tercile funding->liq): passed={primary_b_passed}")
    for n in primary_b_names:
        print(f"  {n}: {summaries[n]}")
    print(f"Joint gate_passed={gate_passed} -> verdict={verdict}")

    results = {
        "experiment_id": f"FCLR-XSEC-008-{SESSION}",
        "session_utc": SESSION,
        "method": "independent numpy Generator block bootstrap + manual hour-tercile grouping + independent Holm",
        "panel_path_fclr001": str(PANEL_FCLR001),
        "panel_sha256_fclr001": PANEL_FCLR001_SHA256,
        "panel_path_liquidation": str(PANEL_LIQ),
        "panel_sha256_liquidation": PANEL_LIQ_SHA256,
        "panel_hash_verified_fclr001": actual_fclr001_sha == PANEL_FCLR001_SHA256,
        "panel_hash_verified_liquidation": actual_liq_sha == PANEL_LIQ_SHA256,
        "outcome_data_inspected_before_freeze": False,
        "seed": RNG_SEED,
        "n_bootstrap_reps": N_BOOT,
        "alpha": ALPHA,
        "materiality_floor": MATERIALITY_FLOOR,
        "primary_a_tercile": PRIMARY_A_TERCILE,
        "primary_b_terciles": PRIMARY_B_TERCILES,
        "summaries": summaries,
        "primary_a_passed": bool(primary_a_passed),
        "primary_b_passed": bool(primary_b_passed),
        "gate": {
            "primary_a_passed": bool(primary_a_passed),
            "primary_b_passed": bool(primary_b_passed),
            "gate_passed": bool(gate_passed),
            "verdict": verdict,
        },
        "verdict": verdict,
        "recompute_concurs_with_evaluation": None,  # filled after comparing to evaluation JSON
    }

    # Concurrence check vs evaluation JSON.
    eval_path = OUT_DIR / f"fclr_xsec008_evaluation_{SESSION}.json"
    if eval_path.exists():
        eval_data = json.loads(eval_path.read_text())
        eval_verdict = eval_data.get("verdict")
        results["recompute_concurs_with_evaluation"] = bool(eval_verdict == verdict)
        results["evaluation_verdict"] = eval_verdict
    else:
        results["recompute_concurs_with_evaluation"] = None
        results["evaluation_verdict"] = None

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    out_path = OUT_DIR / f"fclr_xsec008_recompute_{SESSION}.json"
    with open(out_path, "w") as fh:
        json.dump(results, fh, indent=2)
    print(f"\nSaved recompute to {out_path}")
    print(f"Recompute concurs with evaluation: {results['recompute_concurs_with_evaluation']}")


if __name__ == "__main__":
    main()
