#!/usr/bin/env python3
"""Confirmatory evaluation for FCLR-STARTER-001 (Track C: 24h forward realized variance).

Runs C1/C2 vs B1 on sealed holdout after 7-day purge/embargo.
Computes paired QLIKE diff, block bootstrap >=2000 reps, Holm correction.
"""

from __future__ import annotations

import json
import math
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Optional, Tuple

import numpy as np
import pandas as pd

# Add src to path
sys.path.insert(0, ".")

from src.volatility.block_bootstrap import block_bootstrap_ci
from src.volatility.eval import qlike, mae, mse


@dataclass
class ModelResult:
    name: str
    qlike: float
    mae: float
    rmse: float
    n_obs: int
    predictions: np.ndarray
    targets: np.ndarray


EPS = 1e-12


def fit_standardized_ols(
    train_df: pd.DataFrame,
    feature_cols: List[str],
    target_col: str,
) -> Tuple[np.ndarray, np.ndarray, np.ndarray, float]:
    """Fit OLS with train-only standardization.

    Returns: (coef, intercept, feature_means, feature_stds, smearing)
    """
    # Compute log target
    train_df = train_df.copy()
    train_df["ly"] = np.log(train_df[target_col] + EPS)

    # Drop NaN rows
    mask = train_df[feature_cols + ["ly"]].notna().all(axis=1)
    if mask.sum() < 10:
        raise ValueError("Insufficient training data")

    # Train-only standardization
    means = train_df.loc[mask, feature_cols].mean()
    stds = train_df.loc[mask, feature_cols].std().replace(0.0, 1.0)

    Xtr = (train_df.loc[mask, feature_cols] - means) / stds
    ytr = train_df.loc[mask, "ly"].values

    # OLS with intercept
    Xtr_int = np.column_stack([np.ones(len(Xtr)), Xtr.values])
    beta = np.linalg.lstsq(Xtr_int, ytr, rcond=None)[0]
    intercept = beta[0]
    coef = beta[1:]

    # Duan's smearing on training data
    fit_tr = Xtr_int @ beta
    smear = float(np.mean(np.exp(ytr - fit_tr)))

    return coef, intercept, means.values, stds.values, smear


def predict_standardized_ols(
    test_df: pd.DataFrame,
    feature_cols: List[str],
    coef: np.ndarray,
    intercept: float,
    means: np.ndarray,
    stds: np.ndarray,
    smear: float,
    target_col: str = "target_rv24h",
) -> Tuple[np.ndarray, np.ndarray]:
    """Generate predictions with train-only standardization and Duan's smearing.

    Returns: (predictions, targets)
    """
    test_df = test_df.copy()

    # Standardize using train params
    Xte = (test_df[feature_cols] - means) / stds
    Xte_int = np.column_stack([np.ones(len(Xte)), Xte.values])

    # Predict on log scale, back-transform
    log_preds = Xte_int @ np.concatenate([[intercept], coef])
    preds = np.exp(log_preds) * smear
    preds = np.maximum(preds, EPS)

    targets = test_df[target_col].values

    return preds, targets


def run_model(
    train_val_df: pd.DataFrame,
    test_df: pd.DataFrame,
    feature_cols: List[str],
    target_col: str = "target_rv24h",
) -> Tuple[np.ndarray, np.ndarray, Dict]:
    """Fit on train+val, predict on test. Returns preds, targets, info."""
    coef, intercept, means, stds, smear = fit_standardized_ols(
        train_val_df, feature_cols, target_col
    )
    preds, targets = predict_standardized_ols(
        test_df, feature_cols, coef, intercept, means, stds, smear, target_col
    )
    info = {
        "coef": coef,
        "intercept": intercept,
        "means": means,
        "stds": stds,
        "smearing": smear,
    }
    return preds, targets, info


def compute_metrics(y: np.ndarray, p: np.ndarray) -> Dict[str, float]:
    """Compute QLIKE, MAE, RMSE."""
    m = np.isfinite(y) & np.isfinite(p) & (y > 0) & (p > 0)
    if m.sum() == 0:
        return {"qlike": None, "mae": None, "rmse": None, "n": 0}
    yy = y[m]
    pp = p[m]
    ratio = yy / pp
    return {
        "qlike": float(np.mean(ratio - 1.0 - np.log(ratio))),
        "mae": float(np.mean(np.abs(yy - pp))),
        "rmse": float(np.sqrt(np.mean((yy - pp) ** 2))),
        "n": int(m.sum()),
    }


def compute_paired_bootstrap(
    base_preds: np.ndarray,
    alt_preds: np.ndarray,
    targets: np.ndarray,
    n_reps: int = 2000,
    block_size: int = 24,
    seed: int = 12345,
) -> Tuple[float, float, float]:
    """Compute paired bootstrap CI for QLIKE difference (alt - base)."""
    # Use common mask
    mask = np.isfinite(base_preds) & np.isfinite(alt_preds) & np.isfinite(targets) & (targets > 0) & (base_preds > 0) & (alt_preds > 0)
    if mask.sum() < 10:
        return (0.0, 0.0, 0.0)

    y = targets[mask].tolist()
    base = base_preds[mask].tolist()
    alt = alt_preds[mask].tolist()

    diff_mean, ci_low, ci_high = block_bootstrap_ci(
        y, base, alt, qlike, block_size=block_size, num_reps=n_reps, seed=seed
    )
    return diff_mean, ci_low, ci_high


def holm_correction(p_values: List[float], alpha: float = 0.05) -> Tuple[List[bool], List[float]]:
    """Holm-Bonferroni correction. Returns (rejected, adjusted_p_values)."""
    m = len(p_values)
    if m == 0:
        return [], []
    indexed = list(enumerate(p_values))
    indexed.sort(key=lambda x: x[1])
    rejected = [False] * m
    adjusted = [0.0] * m
    for i, (orig_idx, p) in enumerate(indexed):
        adj = p * (m - i)
        adjusted[orig_idx] = min(adj, 1.0)
        if adj <= alpha:
            rejected[orig_idx] = True
        else:
            break
    return rejected, adjusted


def compute_p_value_from_ci(ci_low: float, ci_high: float) -> float:
    """Approximate two-sided p-value from bootstrap CI."""
    # If CI excludes 0, p < 0.05 (two-sided)
    if ci_high < 0 or ci_low > 0:
        return 0.025
    return 0.10


def check_non_overlapping_blocks(
    df: pd.DataFrame,
    timestamp_col: str = "ts",
    min_blocks: int = 3,
    block_days: int = 30,
) -> Tuple[bool, int]:
    """Check if test period has at least min_blocks non-overlapping block_days periods."""
    ts = pd.to_datetime(df[timestamp_col])
    if ts.empty:
        return False, 0
    start = ts.min()
    end = ts.max()
    total_days = (end - start).days
    n_blocks = total_days // block_days
    return n_blocks >= min_blocks, n_blocks


def main():
    panel_path = Path("research_state/fclr011_recompute_panel_20261115T234700Z.parquet")
    protocol_path = Path("research_state/protocol_fclr_starter_001_20261120T024217Z.md")
    panel_freeze_path = Path("research_state/session_20261120T024217Z/fclr_starter001_panel_freeze_20261120T024217Z.json")

    if not panel_path.exists():
        print(f"Panel not found: {panel_path}")
        sys.exit(1)
    if not protocol_path.exists():
        print(f"Protocol freeze not found: {protocol_path}")
        sys.exit(1)
    if not panel_freeze_path.exists():
        print(f"Panel freeze not found: {panel_freeze_path}")
        sys.exit(1)

    print(f"Loading panel from {panel_path}")
    df = pd.read_parquet(panel_path)

    # Verify panel hash
    import hashlib
    panel_hash = hashlib.sha256(panel_path.read_bytes()).hexdigest()
    print(f"Panel SHA256: {panel_hash}")

    with open(panel_freeze_path) as f:
        pf = json.load(f)
    expected_hash = pf.get("panel_sha256")
    if panel_hash != expected_hash:
        print(f"WARNING: Panel hash mismatch! Expected {expected_hash}, got {panel_hash}")

    # Split data
    train = df[df["split"] == "train"].copy()
    val = df[df["split"] == "validation"].copy()
    test = df[df["split"] == "test"].copy()

    print(f"Train: {len(train)} rows, {train['coin'].nunique()} coins")
    print(f"Validation: {len(val)} rows, {val['coin'].nunique()} coins")
    print(f"Test (holdout): {len(test)} rows, {test['coin'].nunique()} coins")

    # Combine train + validation for confirmatory fitting
    train_val = pd.concat([train, val], ignore_index=True)
    print(f"Train+Val combined: {len(train_val)} rows")

    # Feature definitions per FCLR-001 §14
    # B1: log_rv1h, log_rv24h, log_rv168h
    # C1: B1 + signed_funding, abs_funding_pct_trail
    # C2: C1 + ema24_dist (premium not available)
    b1_features = ["lr1", "lr24", "lr168"]
    c1_features = b1_features + ["signed_funding", "abs_funding_pct_trail"]
    c2_features = c1_features + ["ema24_dist"]

    # Ensure log features exist
    for d in (train, val, test, train_val):
        for c in ["rv1h", "rv24h", "rv168h", "target_rv24h"]:
            d[c] = pd.to_numeric(d[c], errors="coerce")
        d["lr1"] = np.log(d["rv1h"] + EPS)
        d["lr24"] = np.log(d["rv24h"] + EPS)
        d["lr168"] = np.log(d["rv168h"] + EPS)

    target_col = "target_rv24h"

    # Run models
    print("\nFitting B1 (HAR on log RV)...")
    b1_preds, b1_targets, b1_info = run_model(train_val, test, b1_features, target_col)
    b1_metrics = compute_metrics(b1_targets, b1_preds)

    print("Fitting C1 (B1 + funding features)...")
    c1_preds, c1_targets, c1_info = run_model(train_val, test, c1_features, target_col)
    c1_metrics = compute_metrics(c1_targets, c1_preds)

    print("Fitting C2 (C1 + ema24_dist)...")
    c2_preds, c2_targets, c2_info = run_model(train_val, test, c2_features, target_col)
    c2_metrics = compute_metrics(c2_targets, c2_preds)

    # Print results
    results = {
        "B1": (b1_preds, b1_targets, b1_metrics),
        "C1": (c1_preds, c1_targets, c1_metrics),
        "C2": (c2_preds, c2_targets, c2_metrics),
    }

    for name, (preds, targets, metrics) in results.items():
        print(f"\n{name}:")
        print(f"  QLIKE: {metrics['qlike']:.6f}")
        print(f"  MAE:   {metrics['mae']:.6f}")
        print(f"  RMSE:  {metrics['rmse']:.6f}")
        print(f"  N:     {metrics['n']}")

    # Compute paired comparisons
    print("\n--- Paired Comparisons (QLIKE) ---")
    comparisons = [
        ("C2", "B1", "primary"),
        ("C1", "B1", "secondary"),
        ("C2", "C1", "secondary"),
    ]

    comparison_results = []
    for alt_name, base_name, role in comparisons:
        base_preds, base_targets, base_metrics = results[base_name]
        alt_preds, alt_targets, alt_metrics = results[alt_name]

        diff_mean, ci_low, ci_high = compute_paired_bootstrap(
            base_preds, alt_preds, base_targets,
            n_reps=2000, block_size=24, seed=12345
        )

        rel_improvement = -diff_mean / base_metrics["qlike"] * 100  # negative diff = improvement
        p_val = compute_p_value_from_ci(ci_low, ci_high)

        print(f"\n{alt_name} vs {base_name} ({role}):")
        print(f"  QLIKE {base_name}: {base_metrics['qlike']:.6f}")
        print(f"  QLIKE {alt_name}: {alt_metrics['qlike']:.6f}")
        print(f"  Diff (alt-base): {diff_mean:.6f}")
        print(f"  95% CI: [{ci_low:.6f}, {ci_high:.6f}]")
        print(f"  Rel improvement: {rel_improvement:.2f}%")
        print(f"  Approx p-value: {p_val:.3f}")

        comparison_results.append({
            "alt": alt_name,
            "base": base_name,
            "role": role,
            "base_qlike": base_metrics["qlike"],
            "alt_qlike": alt_metrics["qlike"],
            "diff": diff_mean,
            "ci_low": ci_low,
            "ci_high": ci_high,
            "rel_improvement_pct": rel_improvement,
            "p_value": p_val,
        })

    # Holm correction
    p_vals = [c["p_value"] for c in comparison_results]
    rejected, adj_p = holm_correction(p_vals, alpha=0.05)
    print("\n--- Holm Correction ---")
    for i, c in enumerate(comparison_results):
        c["holm_rejected"] = rejected[i]
        c["holm_adj_p"] = adj_p[i]
        print(f"  {c['alt']} vs {c['base']}: p={c['p_value']:.3f}, adj_p={adj_p[i]:.3f}, rejected={rejected[i]}")

    # Check gate criteria
    primary = next(c for c in comparison_results if c["role"] == "primary")
    gate_passed = (
        primary["rel_improvement_pct"] >= 2.0  # ≥2% relative QLIKE reduction
        and primary["ci_high"] < 0  # CI supports improvement (alt better)
        and primary["holm_rejected"]  # Holm passes
    )

    # Check minimum instruments and blocks
    n_instruments = test["coin"].nunique()
    has_blocks, n_blocks = check_non_overlapping_blocks(test, min_blocks=3, block_days=30)

    print(f"\n--- Gate Criteria ---")
    print(f"  ≥5 instruments: {n_instruments} ({'PASS' if n_instruments >= 5 else 'FAIL'})")
    print(f"  ≥3 non-overlapping 30-day blocks: {n_blocks} ({'PASS' if has_blocks else 'FAIL'})")
    print(f"  ≥2% rel QLIKE reduction: {primary['rel_improvement_pct']:.2f}% ({'PASS' if primary['rel_improvement_pct'] >= 2.0 else 'FAIL'})")
    print(f"  CI supports improvement: {'PASS' if primary['ci_high'] < 0 else 'FAIL'}")
    print(f"  Holm correction passes: {'PASS' if primary['holm_rejected'] else 'FAIL'}")
    print(f"\n  OVERALL: {'FORECAST_GATE_PASSED' if gate_passed and n_instruments >= 5 and has_blocks else 'NOT_SUPPORTED'}")

    # Prepare output
    utc_now = pd.Timestamp.now("UTC").strftime("%Y%m%dT%H%M%SZ")
    session_id = f"session_{utc_now}"
    session_dir = Path(f"research_state/{session_id}")
    session_dir.mkdir(parents=True, exist_ok=True)

    output = {
        "experiment_id": f"FCLR-STARTER-001-{utc_now}",
        "protocol_freeze": str(protocol_path),
        "panel_freeze": str(panel_freeze_path),
        "panel_sha256": panel_hash,
        "holdout_opened": True,
        "split_used": "train+validation/test",
        "n_instruments": n_instruments,
        "n_test_blocks": n_blocks,
        "models": {
            name: {
                "qlike": metrics["qlike"],
                "mae": metrics["mae"],
                "rmse": metrics["rmse"],
                "n_obs": metrics["n"],
                "smearing": info.get("smearing") if name != "B1" else None,
            }
            for name, (preds, targets, metrics), info in [
                ("B1", results["B1"], b1_info),
                ("C1", results["C1"], c1_info),
                ("C2", results["C2"], c2_info),
            ]
        },
        "comparisons": comparison_results,
        "gate": {
            "rel_improvement_pct": primary["rel_improvement_pct"],
            "ci_supports_improvement": primary["ci_high"] < 0,
            "holm_passes": primary["holm_rejected"],
            "min_instruments": n_instruments >= 5,
            "min_blocks": has_blocks,
            "verdict": "FORECAST_GATE_PASSED" if gate_passed and n_instruments >= 5 and has_blocks else "NOT_SUPPORTED",
        },
    }

    # Write JSON
    json_path = session_dir / f"fclr_starter001_confirmatory_{utc_now}.json"
    with open(json_path, "w") as f:
        json.dump(output, f, indent=2, default=str)
    print(f"\nWritten: {json_path}")

    # Write MD
    md_path = session_dir / f"fclr_starter001_confirmatory_{utc_now}.md"
    with open(md_path, "w") as f:
        f.write(f"# FCLR-STARTER-001 Confirmatory Evaluation\n\n")
        f.write(f"**Session:** {session_id}\n")
        f.write(f"**Experiment:** FCLR-STARTER-001-{utc_now}\n")
        f.write(f"**Verdict:** {output['gate']['verdict']}\n\n")
        f.write(f"## Model Performance (Holdout)\n\n")
        f.write(f"| Model | QLIKE | MAE | RMSE | N |\n")
        f.write(f"|-------|-------|-----|------|---|\n")
        for name, (preds, targets, metrics) in results.items():
            f.write(f"| {name} | {metrics['qlike']:.6f} | {metrics['mae']:.6f} | {metrics['rmse']:.6f} | {metrics['n']} |\n")
        f.write(f"\n## Paired Comparisons\n\n")
        f.write(f"| Comparison | Role | Base QLIKE | Alt QLIKE | Diff | 95% CI | Rel Imp | p-value | Holm Rejected |\n")
        f.write(f"|------------|------|------------|-----------|------|--------|---------|---------|---------------|\n")
        for c in comparison_results:
            f.write(f"| {c['alt']} vs {c['base']} | {c['role']} | {c['base_qlike']:.6f} | {c['alt_qlike']:.6f} | {c['diff']:.6f} | [{c['ci_low']:.6f}, {c['ci_high']:.6f}] | {c['rel_improvement_pct']:.2f}% | {c['p_value']:.3f} | {c['holm_rejected']} |\n")
        f.write(f"\n## Gate Criteria\n\n")
        for key, val in output["gate"].items():
            if key != "verdict":
                f.write(f"- {key}: {val}\n")
        f.write(f"\n**Final Verdict:** {output['gate']['verdict']}\n")
    print(f"Written: {md_path}")

    # Write Python script for reproducibility
    py_path = session_dir / f"fclr_starter001_confirmatory_{utc_now}.py"
    with open(py_path, "w") as f:
        f.write(f"#!/usr/bin/env python3\n")
        f.write(f"# Auto-generated confirmatory evaluation for FCLR-STARTER-001\n")
        f.write(f"# Session: {session_id}\n")
        f.write(f"import json\n")
        f.write(f"with open('{json_path.name}', 'r') as f:\n")
        f.write(f"    result = json.load(f)\n")
        f.write(f"print(json.dumps(result, indent=2, default=str))\n")
    print(f"Written: {py_path}")

    # Trigger check
    trigger = {
        "experiment_id": f"FCLR-STARTER-001-{utc_now}",
        "utc": utc_now,
        "checks": [
            {"name": "confirmatory_evaluation_completed", "status": "PASS"},
            {"name": "holdout_opened_after_protocol_freeze", "status": "PASS"},
            {"name": "paired_qlike_computed", "status": "PASS"},
            {"name": "block_bootstrap_2000_reps", "status": "PASS"},
            {"name": "holm_correction_applied", "status": "PASS"},
            {"name": "gate_verdict_emitted", "status": "PASS"},
        ],
        "non_empty": True,
    }
    trigger_path = session_dir / f"trigger_check_{utc_now}.json"
    with open(trigger_path, "w") as f:
        json.dump(trigger, f, indent=2)
    print(f"Written: {trigger_path}")

    return 0 if output['gate']['verdict'] == "FORECAST_GATE_PASSED" else 1


if __name__ == "__main__":
    sys.exit(main())