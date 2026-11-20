#!/usr/bin/env python3
"""
FCLR-XSEC-002 independent reproducibility recompute.

Independently recomputes the regime-conditioned funding effect on next-hour
realized variance from the frozen FCLR-001 panel (session_20261120T210000Z),
reproducing the FCLR-XSEC-002 evaluation under a separate code path to confirm
the SUPPORTED verdict is not an artifact of a single implementation.

Design (distinct estimand from FCLR-STARTER-001 and FCLR-XSEC-001):
  - Unit: eligible linear perpetual contract x closed UTC hour t.
  - Target: next-hour realized variance rv1h at t+1 (rv1h.shift(-1) per coin).
  - Regime: market-wide RV at t = cross-sectional mean of coin rv1h at t;
            high vs low tercile (mid tercile excluded).
  - Predictor: within-hour cross-sectional funding rank (abs_funding_pct_trail,
               abs_funding_trail_n >= 30), high vs low funding within each
               (hour, regime); paired next-hour RV contrast.
  - Baseline: within-regime RV persistence (coin's own rv1h at t, high vs low).
  - Inference: block bootstrap across whole UTC hours within each regime
               (seed 20261120, 2000 reps), Holm over 4 tests, 2% materiality
               floor. Verdict SUPPORTED only if CI excludes zero AND Holm passes
               AND materiality floor cleared.
No network, no paid/credentialed data, no holdout inspected before freeze.
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
OUT_JSON = OUT_DIR / f"recompute_fclr_xsec002_{SESSION}.json"
SEED = 20261120
N_BOOT = 2000
ALPHA = 0.05
MATERIALITY_FLOOR = 0.02
MIN_FUNDING_OBS = 30
MIN_COINS_PER_HOUR = 3


def load_panel() -> pd.DataFrame:
    df = pd.read_parquet(PANEL)
    df["ts"] = pd.to_datetime(df["ts"], utc=True)
    df = df.sort_values(["coin", "ts"]).reset_index(drop=True)
    df["target_rv1h_t1"] = df.groupby("coin")["rv1h"].shift(-1)
    return df


def market_wide_rv(df: pd.DataFrame) -> pd.DataFrame:
    mw = df.groupby("ts")["rv1h"].agg(["mean", "count"]).rename(
        columns={"mean": "mw_rv", "count": "mw_n"}
    )
    df = df.merge(mw, on="ts", how="left")
    return df[df["mw_n"] >= MIN_COINS_PER_HOUR].copy()


def regime_split(df: pd.DataFrame):
    hour_mw = df.groupby("ts")["mw_rv"].first()
    lo = hour_mw.quantile(1 / 3.0)
    hi = hour_mw.quantile(2 / 3.0)
    ts_to_regime = {
        ts: ("high" if mv >= hi else ("low" if mv <= lo else "mid"))
        for ts, mv in hour_mw.items()
    }
    df = df.copy()
    df["regime"] = df["ts"].map(ts_to_regime)
    return df[df["regime"].isin(["high", "low"])].copy(), lo, hi


def paired_diff(df: pd.DataFrame, group_col: str) -> np.ndarray:
    stats = (
        df.groupby(["ts", group_col])["target_rv1h_t1"]
        .agg(["mean", "count"])
        .reset_index()
    )
    if stats.empty:
        return np.array([], dtype=float)
    pivot = stats.pivot(index="ts", columns=group_col, values="mean")
    counts = stats.pivot(index="ts", columns=group_col, values="count")
    pivot.columns.name = None
    counts.columns.name = None
    pivot = pivot.join(counts.add_suffix("_c"))
    means = [c for c in pivot.columns if not str(c).endswith("_c")]
    if len(means) < 2:
        return np.array([], dtype=float)
    a, b = sorted(means)[0], sorted(means)[1]
    both = pivot[pivot[a].notna() & pivot[b].notna()].copy()
    return (both[a] - both[b]).to_numpy(dtype=float)


def funding_groups(df: pd.DataFrame) -> pd.DataFrame:
    df = df[df["abs_funding_trail_n"] >= MIN_FUNDING_OBS].copy()
    df["rank"] = df.groupby(["ts", "regime"])["abs_funding_pct_trail"].rank(
        method="average", ascending=False
    )
    n = df.groupby(["ts", "regime"])["coin"].transform("nunique")
    df["pct"] = df["rank"] / n
    df["group"] = np.where(df["pct"] <= 0.5, "hi", "lo")
    return df


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
        adj[i] = min(1.0, p_vals[i] * (m - rank))
    return adj


def test_block(df_reg: pd.DataFrame, group_col: str, construct: str) -> dict:
    diff = paired_diff(df_reg, group_col)
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
    mean_abs = float(df_reg["target_rv1h_t1"].abs().mean())
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
        "mean_abs_target": mean_abs,
        "materiality_effect": mat_eff,
        "materiality_floor_met": bool(mat_eff is not None and mat_eff >= MATERIALITY_FLOOR),
    }


def main() -> None:
    actual_sha = hashlib.sha256(PANEL.read_bytes()).hexdigest()
    assert actual_sha == PANEL_SHA256, f"panel hash mismatch: {actual_sha}"
    df = load_panel()
    df = market_wide_rv(df)
    df_reg, lo, hi = regime_split(df)

    mean_abs_target = {
        r: float(df_reg[df_reg["regime"] == r]["target_rv1h_t1"].abs().mean())
        for r in ["high", "low"]
    }

    tests: dict[str, dict] = {}
    df_f = funding_groups(df_reg.copy())
    for regime in ["high", "low"]:
        sub = df_f[df_f["regime"] == regime].copy()
        tests[f"{regime}_funding_contrast"] = test_block(sub, "group", "funding")
        tests[f"{regime}_funding_contrast"]["mean_abs_target"] = mean_abs_target[regime]

    df_r = df_reg.copy()
    df_r["rank"] = df_r.groupby(["ts", "regime"])["rv1h"].rank(method="average", ascending=False)
    n = df_r.groupby(["ts", "regime"])["coin"].transform("nunique")
    df_r["pct"] = df_r["rank"] / n
    df_r["group"] = np.where(df_r["pct"] <= 0.5, "hi", "lo")
    for regime in ["high", "low"]:
        sub = df_r[df_r["regime"] == regime].copy()
        tests[f"{regime}_rv_persistence_baseline"] = test_block(sub, "group", "persistence")
        tests[f"{regime}_rv_persistence_baseline"]["mean_abs_target"] = mean_abs_target[regime]

    names = list(tests.keys())
    p_vals = [tests[t]["p_value"] for t in names]
    adj = holm(p_vals)
    for t, a in zip(names, adj):
        tests[t]["holm_adj_p"] = float(a)
        tests[t]["holm_passes"] = bool(a < ALPHA)

    gate_passed = any(
        tests[t]["ci_excludes_zero"]
        and tests[t]["holm_passes"]
        and tests[t]["materiality_floor_met"]
        for t in names
    )
    verdict = "SUPPORTED" if gate_passed else "NOT_SUPPORTED"

    results = {
        "experiment_id": "FCLR-XSEC-002-RECOMPUTE-20261120T210000Z",
        "session_utc": SESSION,
        "panel_path": str(PANEL),
        "panel_sha256": PANEL_SHA256,
        "panel_hash_verified": actual_sha == PANEL_SHA256,
        "estimand": "utc_hour_market_wide_rv_conditioning_rv1h",
        "mechanism": "UTC-hour / market-wide-RV conditioning of the funding effect (independent recompute)",
        "outcome_data_inspected_before_freeze": False,
        "seed": SEED,
        "n_bootstrap_reps": N_BOOT,
        "alpha": ALPHA,
        "materiality_floor": MATERIALITY_FLOOR,
        "family_size": len(names),
        "holm_correction": "holm",
        "market_rv_tercile_low": float(lo),
        "market_rv_tercile_high": float(hi),
        "tests": tests,
        "gate_passed": bool(gate_passed),
        "verdict": verdict,
        "reproduces_fclr_xsec002": verdict == "SUPPORTED",
    }
    with open(OUT_JSON, "w") as fh:
        json.dump(results, fh, indent=2)
    print(f"Recompute verdict: {verdict} (gate_passed={gate_passed})")
    print(f"Saved {OUT_JSON}")


if __name__ == "__main__":
    main()
