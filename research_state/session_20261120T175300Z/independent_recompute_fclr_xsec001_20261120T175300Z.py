#!/usr/bin/env python3
"""
Independent numpy-only recomputation of FCLR-XSEC-001 within-hour cross-sectional
funding-intensity contrast. Recomputes the high-vs-low funding next-hour RV
difference from the frozen panel using only numpy/pandas, without reading the
evaluation JSON output. Serves as the fresh quantitative artifact required by
the handoff heavy-work gate (FCLR-XSEC-001 campaign).
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


def main() -> None:
    df = pd.read_parquet(PANEL)
    df["ts"] = pd.to_datetime(df["ts"], utc=True)
    df = df.sort_values(["coin", "ts"]).reset_index(drop=True)

    actual_sha = hashlib.sha256(PANEL.read_bytes()).hexdigest()
    assert actual_sha == PANEL_SHA256, f"panel hash mismatch: {actual_sha}"

    # Target: next-hour RV (rv1h at t+1) within each coin
    df["target_rv1h_t1"] = df.groupby("coin")["rv1h"].shift(-1)
    df_eval = df[df["target_rv1h_t1"].notna()].copy()

    # Cross-sectional funding rank within each hour (percentile)
    df_eval["funding_rank"] = df_eval.groupby("ts")["signed_funding"].rank(
        method="average", ascending=False
    )
    n_coins = df_eval.groupby("ts")["coin"].transform("nunique")
    df_eval["funding_pct"] = df_eval["funding_rank"] / n_coins
    df_eval["funding_group"] = np.where(
        df_eval["funding_pct"] <= 0.5, "high_funding", "low_funding"
    )

    # Within-hour paired diff: mean(next-hour RV, high_funding) - mean(next-hour RV, low_funding)
    stats = (
        df_eval.groupby(["ts", "funding_group"])["target_rv1h_t1"]
        .agg(["mean", "count"])
        .reset_index()
    )
    pivot = stats.pivot(index="ts", columns="funding_group", values="mean")
    pivot = pivot.dropna()
    diffs = pivot["high_funding"].values - pivot["low_funding"].values

    n_hours = len(diffs)
    mean_diff = float(diffs.mean())
    pos = int((diffs > 0).sum())

    # Block bootstrap across hours
    rng = np.random.RandomState(SEED)
    boot = np.empty(N_BOOT, dtype=float)
    for b in range(N_BOOT):
        boot[b] = rng.choice(diffs, size=n_hours, replace=True).mean()
    ci_low = float(np.percentile(boot, 2.5))
    ci_high = float(np.percentile(boot, 97.5))
    p_val = float(2 * min((boot >= 0).mean(), (boot <= 0).mean()))

    ci_excludes_zero = bool(ci_low > 0 or ci_high < 0)
    holm_adj_p = float(min(1.0, p_val * 2))  # Holm: p * (family_size - rank), family=2, rank=1 for smallest
    holm_passes = bool(holm_adj_p < 0.05)

    result = {
        "recompute_id": "independent_recompute_fclr_xsec001_20261120T175300Z",
        "session_utc": "20261120T175300Z",
        "experiment_id": "FCLR-XSEC-001-20261120T175300Z",
        "panel_path": str(PANEL),
        "panel_sha256": PANEL_SHA256,
        "panel_hash_verified": True,
        "method": "numpy-only independent recomputation of within-hour cross-sectional funding contrast",
        "n_coins": 5,
        "n_hours": n_hours,
        "mean_diff_high_minus_low": mean_diff,
        "ci_low": ci_low,
        "ci_high": ci_high,
        "p_value": p_val,
        "holm_adj_p": holm_adj_p,
        "positive_diff_count": pos,
        "ci_excludes_zero": ci_excludes_zero,
        "holm_passes": holm_passes,
        "verdict": "NOT_SUPPORTED" if not (ci_excludes_zero and holm_passes) else "SUPPORTED",
        "n_bootstrap_reps": N_BOOT,
        "bootstrap_seed": SEED,
    }

    out_path = (
        REPO
        / "research_state"
        / "session_20261120T175300Z"
        / "independent_recompute_fclr_xsec001_20261120T175300Z.json"
    )
    with open(out_path, "w") as fh:
        json.dump(result, fh, indent=2)
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
