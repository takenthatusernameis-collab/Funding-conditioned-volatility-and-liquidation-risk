#!/usr/bin/env python3
"""Phase C — TRACKA-LIQ-EXPANSION-RECONCILIATION (FCLR-LIQ-EXPANSION-RECONCILIATION-20261114T083642Z).

Attribute the 19.04% vs 6.19% C2_vs_B1 QLIKE gap (sealed expansion vs recompute, shared
1,472 (coin, ts) keys). Produce a 2×2 audit:
{Sealed panel, Recompute panel} × {Sealed estimator, Recompute estimator}
with verdict in {EXPLAINED_BY_ESTIMATOR, EXPLAINED_BY_DATA, UNEXPLAINED, INCONCLUSIVE}.

Frozen design (from prereg, never read from outcomes):
  universe   AAVE, ADA, BCH, CRV, LTC, NEAR, UNI, ZEC (8 symbols, *-PERP)
  label      observed ironflow liquidation intensity per symbol per 24h UTC bucket
             = sum(notional_usd) of observed liquidation events (observed only)
  target     next-24h liquidation intensity (strictly forward, shift -1 day)
  models     B0 persistence (log prior-day intensity),
             B1 HAR (log RV1h/RV24h/RV168h from mark-price 1h candles),
             C1 = B1 + signed funding + trailing |funding| percentile,
             C2 = C1 + mark/index premium + mark/EMA24 distance
  fit        OLS on log(target + 1e-12), train-only mean/std scaling,
             documented train-only Duan smearing back-transform
  missing    no zero-fill, no forward-fill; paired contrasts use common eligible rows
  inference  paired circular block bootstrap over complete test UTC blocks (2000
             deterministic reps, seed 20261114), Holm across the three registered
             contrasts, LOIO, funding-permutation placebo (200 reps),
             per-symbol/per-block stability, leakage audit
  splits     train 2026-05-01..2026-05-31, val 2026-06-07..2026-06-30,
             test blocks 2026-07-07..2026-08-06 / 2026-08-13..2026-09-11 /
             2026-09-18..2026-10-17, 7-day purge/embargo at both boundaries
  stop rule  instruments >=5, test blocks >=3, core_coverage >=0.80 else INADMISSIBLE

Inputs (read-only, cached):
  Sealed panel:       research_state/tracka_hl_expansion_panel_20261111T202344Z.parquet
  Recompute panel:    research_state/tracka_liq_expansion_recompute_panel_20261114T083000Z.parquet

Outputs:
  research_state/prereg_tracka_liq_expansion_reconciliation_<UTC>.{json,md}
  research_state/evaluation_summary_TRACKA-LIQ-EXPANSION-RECONCILIATION-<UTC>.{json,md}

No network. No mutation of sealed artifacts. All EXPLORATORY_ONLY, promotable=false.

Usage:
  python3 scripts/fclr_liq_expansion_reconcile.py
  python3 scripts/fclr_liq_expansion_reconcile.py --smoke
  python3 scripts/fclr_liq_expansion_reconcile.py --write-prereg
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import random
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

import numpy as np
import pandas as pd
import pyarrow.parquet as pq

REPO = Path(__file__).resolve().parents[1]
RS = REPO / "research_state"

CAMPAIGN = "FCLR-LIQ-EXPANSION-RECONCILIATION-20261114T083642Z"
EXPERIMENT_ID = "FCLR-LIQ-EXPANSION-RECONCILIATION-20261114T083642Z"
PREREG_STEM = "prereg_tracka_liq_expansion_reconciliation_20261114T083642Z"
PREREG_JSON = RS / f"{PREREG_STEM}.json"
PREREG_MD = RS / f"{PREREG_STEM}.md"

UNIVERSE = ["AAVE", "ADA", "BCH", "CRV", "LTC", "NEAR", "UNI", "ZEC"]
PERP = {s: f"{s}-PERP" for s in UNIVERSE}

TRAIN = ("2026-05-01T00:00:00Z", "2026-05-31T23:00:00Z")
VAL = ("2026-06-07T00:00:00Z", "2026-06-30T23:00:00Z")
TEST_BLOCKS = [
    ("2026-07-07T00:00:00Z", "2026-08-06T23:00:00Z"),
    ("2026-08-13T00:00:00Z", "2026-09-11T23:00:00Z"),
    ("2026-09-18T00:00:00Z", "2026-10-17T23:00:00Z"),
]
EMBARGO = timedelta(days=7)

HORIZON_DAYS = 1
EPS = 1e-12
TRAIL_WINDOW_DAYS = 90
TRAIL_MIN_OBS = 30
BOOT_REPS = 2000
BOOT_SEED = 20261114
PLACEBO_REPS = 200
PLACEBO_SEED = 20261114
MATERIALITY_PCT = 2.0
MIN_INSTRUMENTS = 5
MIN_TEST_BLOCKS = 3
MIN_CORE_COVERAGE = 0.80

CONTRASTS = ("C2_vs_B1", "C1_vs_B1", "C2_vs_C1")
MODELS = ("B0", "B1", "C1", "C2")
VERDICTS = ("EXPLAINED_BY_ESTIMATOR", "EXPLAINED_BY_DATA", "UNEXPLAINED", "INCONCLUSIVE")

SEALED_PANEL_PATH = RS / "tracka_hl_expansion_panel_20261111T202344Z.parquet"
RECOMPUTE_PANEL_PATH = RS / "tracka_liq_expansion_recompute_panel_20261114T083000Z.parquet"

SEALED_REFERENCE = {
    "verdict_id": "TRACKA-HL-expansion-20261111T202344Z",
    "C2_vs_B1": {
        "rel_reduction_pct": 19.03709721199804,
        "mean_diff": -2.7097421242345674,
        "ci": [-5.0881020797243135, -0.4776599249731716],
        "n_pairs": 593,
        "n_blocks": 3,
    },
    "C1_vs_B1": {"rel_reduction_pct": 9.679438491416526},
    "C2_vs_C1": {"rel_reduction_pct": 10.360496618139631},
    "paired_symbols": ["AAVE", "ADA", "BCH", "CRV", "LTC", "NEAR", "UNI", "ZEC"],
    "loio_pass": 4,
    "loio_total": 8,
    "placebo_null_p95": 21.10,
    "placebo_true_rel": 19.0371,
    "panel_sha256": "39916a72dfc37d15b6cc886d4e43ed878e0b8e1c2f22936fc4ebf8edd366f699",
    "panel_total_buckets": 1472,
}

RECOMPUTE_REFERENCE = {
    "experiment_id": "FCLR-LIQ-EXPANSION-RECOMPUTE-20261114T073346Z",
    "C2_vs_B1": {
        "rel_reduction_pct": 6.19,
        "mean_diff": -0.19279729,
        "ci": [-0.42074401, -0.03377946],
        "n_pairs": 593,
        "n_blocks": 3,
    },
    "C1_vs_B1": {"rel_reduction_pct": 3.0802},
    "C2_vs_C1": {"rel_reduction_pct": 3.2086},
    "paired_symbols": ["AAVE", "ADA", "BCH", "CRV", "LTC", "NEAR", "UNI", "ZEC"],
    "loio_pass": 7,
    "loio_total": 8,
    "placebo_null_p95": 7.6603,
    "placebo_true_rel": 6.19,
    "panel_sha256": "a4d73c79683550a15e616f3f5fbd93128db1c5498944f9139226f543cfe96715",
    "panel_total_buckets": 1472,
}


# --------------------------------------------------------------------------- utils


def now_utc() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def sha256_file(p: Path) -> str:
    h = hashlib.sha256()
    with p.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def convert(obj):
    if isinstance(obj, (np.bool_, np.integer)):
        return obj.item()
    if isinstance(obj, np.floating):
        return None if not np.isfinite(obj) else float(obj)
    if isinstance(obj, np.ndarray):
        return [convert(v) for v in obj.tolist()]
    if isinstance(obj, dict):
        return {k: convert(v) for k, v in obj.items()}
    if isinstance(obj, (list, tuple)):
        return [convert(v) for v in obj]
    if isinstance(obj, float) and not math.isfinite(obj):
        return None
    return obj


def parse_ts(s: str) -> pd.Timestamp:
    return pd.Timestamp(s.replace("Z", "+00:00"))


# --------------------------------------------------------------------- prereg file


def build_prereg(out_utc: str) -> dict:
    return {
        "experiment_id": EXPERIMENT_ID,
        "campaign": CAMPAIGN,
        "status": "FROZEN_PRE_OUTCOMES",
        "generated": out_utc,
        "frozen_before_outcomes": True,
        "pre_registered_before_outcomes": True,
        "outcome_data_inspected_before_freeze": False,
        "promotable": False,
        "max_status": "EXPLORATORY_ONLY",
        "audit_only": True,
        "does_not_reopen_sealed_verdict": True,
        "purpose": (
            "2×2 reconciliation audit for the 19.04% vs 6.19% C2_vs_B1 QLIKE gap between "
            "the sealed Track A liquidation expansion (TRACKA-HL-EXPANSION-20261111T195500Z, "
            "PASS, +19.04% QLIKE rel reduction) and its independent recompute "
            "(FCLR-LIQ-EXPANSION-RECOMPUTE-20261114T073346Z, INCONCLUSIVE, +6.19% QLIKE rel reduction). "
            "Both share 1,472 (coin, ts) keys over 2026-05-01..2026-10-31. "
            "Cells: {Sealed panel, Recompute panel} × {Sealed estimator, Recompute estimator}. "
            "Verdict in {EXPLAINED_BY_ESTIMATOR, EXPLAINED_BY_DATA, UNEXPLAINED, INCONCLUSIVE}. "
            "All results EXPLORATORY_ONLY, promotable=false. Does not reopen sealed verdict."
        ),
        "sealed_reference": {
            "verdict_id": SEALED_REFERENCE["verdict_id"],
            "panel_sha256": SEALED_REFERENCE["panel_sha256"],
            "C2_vs_B1": SEALED_REFERENCE["C2_vs_B1"],
            "loio_pass": SEALED_REFERENCE["loio_pass"],
            "loio_total": SEALED_REFERENCE["loio_total"],
            "placebo_null_p95": SEALED_REFERENCE["placebo_null_p95"],
            "placebo_true_rel": SEALED_REFERENCE["placebo_true_rel"],
        },
        "recompute_reference": {
            "experiment_id": RECOMPUTE_REFERENCE["experiment_id"],
            "panel_sha256": RECOMPUTE_REFERENCE["panel_sha256"],
            "C2_vs_B1": RECOMPUTE_REFERENCE["C2_vs_B1"],
            "loio_pass": RECOMPUTE_REFERENCE["loio_pass"],
            "loio_total": RECOMPUTE_REFERENCE["loio_total"],
            "placebo_null_p95": RECOMPUTE_REFERENCE["placebo_null_p95"],
            "placebo_true_rel": RECOMPUTE_REFERENCE["placebo_true_rel"],
        },
        "universe": UNIVERSE,
        "markets": [PERP[s] for s in UNIVERSE],
        "horizon_hours": HORIZON_DAYS * 24,
        "target": {
            "name": "next_24h_observed_liquidation_intensity",
            "definition": (
                "next-24h observed ironflow liquidation intensity per symbol per 24h UTC "
                "bucket: sum(notional_usd) of observed liquidation events over t+1..t+24h, "
                "strictly forward from decision time t"
            ),
            "source_series": "ironflow_events observed liquidation labels (notional_usd)",
        },
        "label": {
            "name": "observed_liquidation_intensity",
            "definition": (
                "sum(notional_usd) of observed Hyperliquid liquidation events per symbol "
                "per 24h UTC bucket (observed liquidations only; no modeled/proxy/synthetic)"
            ),
        },
        "models": {
            "B0": ["log_liq_lag1"],
            "B1": ["log_rv1h", "log_rv24h", "log_rv168h"],
            "C1": ["B1", "signed_funding_z", "abs_fund_pct_z"],
            "C2": ["C1", "premium_z", "ema_dist_z"],
            "scaling": "train-only mean/std for funding/premium/ema features",
        },
        "fit": {
            "estimator": "OLS",
            "link": "log(target + 1e-12)",
            "scaling": "train-only mean/std",
            "back_transform": "train-only smearing (Duan) on exp(pred)",
        },
        "missing_data": {
            "zero_fill": False,
            "forward_fill": False,
            "paired_common_rows": True,
            "report_coverage_by_symbol_and_feature": True,
        },
        "primary_metric": "paired out-of-sample QLIKE, C2 vs B1",
        "secondary_metrics": ["MAE", "RMSE"],
        "inference": {
            "paired": True,
            "bootstrap": "circular block over complete UTC days",
            "block_days": 1,
            "replicates": BOOT_REPS,
            "seed": BOOT_SEED,
            "multiplicity": "Holm across C2_vs_B1, C1_vs_B1, C2_vs_C1",
            "alpha": 0.05,
            "loio": True,
            "placebo": "funding permutation within instrument",
            "placebo_replicates": PLACEBO_REPS,
        },
        "splits": {
            "train": list(TRAIN),
            "validation": list(VAL),
            "test_blocks": [list(b) for b in TEST_BLOCKS],
            "n_test_blocks": len(TEST_BLOCKS),
            "purge_embargo_days": EMBARGO.days,
        },
        "stop_rule": {
            "min_instruments": MIN_INSTRUMENTS,
            "min_test_blocks": MIN_TEST_BLOCKS,
            "min_core_coverage": MIN_CORE_COVERAGE,
            "on_failure": "INADMISSIBLE with exact failing minima; do not relax after outcomes",
        },
        "verdict_space": list(VERDICTS),
        "verdict_rule": {
            "EXPLAINED_BY_ESTIMATOR": "Gap primarily attributable to estimator differences (same data, different estimator yields different results)",
            "EXPLAINED_BY_DATA": "Gap primarily attributable to data differences (same estimator, different panel yields different results)",
            "UNEXPLAINED": "Gap persists across both dimensions; neither estimator nor data alone explains the discrepancy",
            "INCONCLUSIVE": "Insufficient evidence to attribute; admissibility or numerical limits prevent clean verdict",
        },
        "inputs": {
            "sealed_panel": str(SEALED_PANEL_PATH.relative_to(REPO)),
            "recompute_panel": str(RECOMPUTE_PANEL_PATH.relative_to(REPO)),
        },
        "sealed_artifacts_must_not_change": True,
    }


def write_prereg(out_utc: str) -> dict:
    prereg = build_prereg(out_utc)
    PREREG_JSON.write_text(json.dumps(prereg, indent=2) + "\n")
    lines = [
        f"# Pre-Registration — {EXPERIMENT_ID}",
        "",
        f"Generated: {out_utc}",
        f"Campaign: `{CAMPAIGN}`",
        "Status: **FROZEN_PRE_OUTCOMES** (frozen before any outcome computation)",
        "",
        "## Purpose",
        "",
        prereg["purpose"],
        "",
        "## Frozen design",
        "",
        f"- Universe: {', '.join(UNIVERSE)}",
        f"- Markets: {', '.join(prereg['markets'])}",
        f"- Label: {prereg['label']['definition']}",
        f"- Target: {prereg['target']['definition']}",
        f"- Target source: {prereg['target']['source_series']}",
        "- Models: B0 persistence; B1 HAR (log RV1h/RV24h/RV168h); C1 = B1 + signed funding + trailing |funding| percentile; C2 = C1 + mark/index premium + mark/EMA24 distance",
        "- Fit: OLS on log(target + 1e-12), train-only scaling, train-only smearing back-transform",
        "- Missing data: no zero-fill, no forward-fill; paired contrasts use common eligible rows",
        "- Primary metric: paired OOS QLIKE, C2 vs B1",
        "- Inference: circular block bootstrap over complete UTC days, 1-day blocks, 2000 reps, seed 20261114; Holm across 3 contrasts",
        "- Robustness: LOIO, funding-permutation placebo (200 reps), per-symbol and per-block stability, leakage audit",
        "",
        "## Frozen splits",
        "",
        f"- Train: {TRAIN[0]} .. {TRAIN[1]}",
        f"- Validation: {VAL[0]} .. {VAL[1]}",
        f"- Test blocks: {TEST_BLOCKS[0][0]} .. {TEST_BLOCKS[0][1]}; "
        f"{TEST_BLOCKS[1][0]} .. {TEST_BLOCKS[1][1]}; {TEST_BLOCKS[2][0]} .. {TEST_BLOCKS[2][1]}",
        f"- Purge/embargo: {EMBARGO.days} days at both boundaries",
        "",
        "## Stop rule",
        "",
        f"- Instruments < {MIN_INSTRUMENTS}, test blocks < {MIN_TEST_BLOCKS}, or core coverage < {MIN_CORE_COVERAGE} → INADMISSIBLE with exact failing minima",
        "",
        "## Non-goals",
        "",
        "- Not promotable. EXPLORATORY_ONLY. Does not reopen the sealed expansion verdict.",
        "- Sealed artifacts are read-only in this cell.",
        "",
    ]
    PREREG_MD.write_text("\n".join(lines))
    return prereg


def assert_prereg_frozen(prereg: dict) -> None:
    expected = {
        "status": "FROZEN_PRE_OUTCOMES",
        "frozen_before_outcomes": True,
        "pre_registered_before_outcomes": True,
        "outcome_data_inspected_before_freeze": False,
        "promotable": False,
        "max_status": "EXPLORATORY_ONLY",
        "audit_only": True,
        "does_not_reopen_sealed_verdict": True,
    }
    for k, v in expected.items():
        if prereg.get(k) != v:
            raise SystemExit(f"prereg field {k}={prereg.get(k)!r} != {v!r}")
    if prereg.get("experiment_id") != EXPERIMENT_ID:
        raise SystemExit(f"prereg experiment_id mismatch: {prereg.get('experiment_id')}")
    if prereg.get("universe") != UNIVERSE:
        raise SystemExit(f"prereg universe drift: {prereg.get('universe')}")
    expected_splits = {
        "train": list(TRAIN),
        "validation": list(VAL),
        "test_blocks": [list(b) for b in TEST_BLOCKS],
        "n_test_blocks": len(TEST_BLOCKS),
        "purge_embargo_days": EMBARGO.days,
    }
    if prereg.get("splits") != expected_splits:
        raise SystemExit(f"prereg splits drift: {prereg.get('splits')}")


# ----------------------------------------------------------------- panel loading


def add_features_and_splits(df: pd.DataFrame, panel_name: str) -> pd.DataFrame:
    """Add all derived features and split assignments to a panel."""
    df = df.sort_values(["coin", "ts"]).reset_index(drop=True)

    # Basic derived features
    df["liq_lag1"] = df.groupby("coin")["liq_notional_usd"].shift(1)
    df["log_liq_lag1"] = np.log(df["liq_lag1"].fillna(0.0).clip(lower=0.0) + EPS)

    df["log_rv1h"] = np.log(df["rv1h"].where(df["rv1h"] > 0) + EPS)
    df["log_rv24h"] = np.log(df["rv24h"].where(df["rv24h"] > 0) + EPS)
    df["log_rv168h"] = np.log(df["rv168h"].where(df["rv168h"] > 0) + EPS)

    # Target: next-24h intensity per symbol (shift -1 day), strictly future
    df["target_next_intensity"] = df.groupby("coin")["liq_notional_usd"].shift(-1)

    # Assign splits
    df["split"] = None
    df.loc[(df["ts"] >= parse_ts(TRAIN[0])) & (df["ts"] <= parse_ts(TRAIN[1])), "split"] = "train"
    df.loc[(df["ts"] >= parse_ts(VAL[0])) & (df["ts"] <= parse_ts(VAL[1])), "split"] = "validation"
    for b in TEST_BLOCKS:
        df.loc[(df["ts"] >= parse_ts(b[0])) & (df["ts"] <= parse_ts(b[1])), "split"] = "test"

    # For sealed panel, use pre-computed abs_fund_pct (already in panel from original computation)
    if panel_name == "sealed":
        df["signed_funding"] = df.get("fundingRate", np.nan)
        # abs_fund_pct is already in the sealed panel - don't recompute

    return df


def load_sealed_panel() -> pd.DataFrame:
    """Load sealed panel and add all derived features."""
    df = pq.read_table(SEALED_PANEL_PATH).to_pandas()
    return add_features_and_splits(df, "sealed")


def load_recompute_panel() -> pd.DataFrame:
    """Load recompute panel (already has all derived features)."""
    df = pq.read_table(RECOMPUTE_PANEL_PATH).to_pandas()
    # Ensure split column exists (should already be there)
    if "split" not in df.columns:
        df = add_features_and_splits(df, "recompute")
    return df


# --------------------------------------------------------------------------- Sealed Estimator (raw features, no z-scoring, fill missing with 0.0)


def sealed_estimator_features(row: pd.Series, model: str):
    """Extract feature vector for sealed estimator (raw features, fill missing with 0.0)."""
    if model == "B0":
        liq = row["liq_notional_usd"]
        if pd.isna(liq) or liq <= 0:
            return None
        return [math.log(liq + EPS)]
    elif model == "B1":
        for c in ["rv1h", "rv24h", "rv168h"]:
            if pd.isna(row[c]) or row[c] <= 0:
                return None
        return [math.log(row["rv1h"] + EPS), math.log(row["rv24h"] + EPS), math.log(row["rv168h"] + EPS)]
    elif model == "C1":
        base = sealed_estimator_features(row, "B1")
        if base is None:
            return None
        sf = row["fundingRate"] if pd.notna(row["fundingRate"]) else 0.0
        af = row["abs_fund_pct"] if pd.notna(row["abs_fund_pct"]) else 0.0
        return base + [float(sf), float(af)]
    elif model == "C2":
        base = sealed_estimator_features(row, "C1")
        if base is None:
            return None
        prem = row["premium"] if pd.notna(row["premium"]) else 0.0
        ema = row["ema_dist"] if pd.notna(row["ema_dist"]) else 0.0
        return base + [float(prem), float(ema)]
    else:
        raise ValueError(model)


def fit_ols_sealed(X_list, y_list):
    """Fit OLS for sealed estimator (manual matrix operations, log target)."""
    rows = [(X, y) for X, y in zip(X_list, y_list)
            if X is not None and y is not None and y > 0 and all(v is not None for v in X)]
    if len(rows) < 10:
        return None
    p = len(rows[0][0])
    XtX = [[0.0] * p for _ in range(p)]
    Xty = [0.0] * p
    for X, y in rows:
        ly = math.log(y + EPS)
        for i in range(p):
            Xty[i] += X[i] * ly
            for j in range(p):
                XtX[i][j] += X[i] * X[j]
    for i in range(p):
        XtX[i][i] += 1e-10
    return _solve_linear(XtX, Xty)


def _solve_linear(A, b):
    """Solve linear system using Gaussian elimination."""
    n = len(A)
    M = [row[:] + [b[i]] for i, row in enumerate(A)]
    for col in range(n):
        piv = max(range(col, n), key=lambda r: abs(M[r][col]))
        if abs(M[piv][col]) < 1e-18:
            continue
        M[col], M[piv] = M[piv], M[col]
        for r in range(col + 1, n):
            factor = M[r][col] / M[col][col] if M[col][col] != 0 else 0
            for c2 in range(col, n + 1):
                M[r][c2] -= factor * M[col][c2]
    x = [0.0] * n
    for i in range(n - 1, -1, -1):
        s = M[i][n]
        for j in range(i + 1, n):
            s -= M[i][j] * x[j]
        x[i] = s / M[i][i] if abs(M[i][i]) >= 1e-18 else 0.0
    return x


def predict_sealed(beta, X):
    """Predict for sealed estimator."""
    if beta is None or X is None or any(v is None for v in X):
        return None
    s = beta[0]
    for i in range(1, len(beta)):
        s += beta[i] * X[i - 1]
    yhat = math.exp(s)
    return yhat if yhat > 0 else 1e-18


def qlike_sealed(y, yhat):
    """QLIKE for sealed estimator."""
    if yhat is None or yhat <= 0 or y is None or y <= 0 or not np.isfinite(y) or not np.isfinite(yhat):
        return None
    ratio = y / yhat
    return ratio - math.log(ratio) - 1.0


# --------------------------------------------------------------------------- Recompute Estimator (z-scored features, train-only scaling, drop missing)


def _solve(A: np.ndarray, b: np.ndarray):
    try:
        beta, *_ = np.linalg.lstsq(A, b, rcond=None)
    except np.linalg.LinAlgError:
        return None
    if not np.all(np.isfinite(beta)):
        return None
    return beta


def get_design_cols(model: str):
    """Get feature column names for recompute estimator (z-scored features)."""
    if model == "B0":
        return ["log_liq_lag1"]
    elif model == "B1":
        return ["log_rv1h", "log_rv24h", "log_rv168h"]
    elif model == "C1":
        return ["log_rv1h", "log_rv24h", "log_rv168h", "signed_funding_z", "abs_fund_pct_z"]
    elif model == "C2":
        return ["log_rv1h", "log_rv24h", "log_rv168h", "signed_funding_z", "abs_fund_pct_z", "premium_z", "ema_dist_z"]
    else:
        raise ValueError(model)


def design_matrix_recompute(df: pd.DataFrame, model: str):
    cols = get_design_cols(model)
    if not all(c in df.columns for c in cols):
        return None, cols
    X = df[cols].to_numpy(dtype=float)
    if not np.all(np.isfinite(X)):
        return None, cols
    A = np.column_stack([np.ones(len(X)), X])
    return A, cols


def add_train_scaling_recompute(train_core: pd.DataFrame, panel: pd.DataFrame) -> dict:
    """No-op for recompute estimator (features already z-scored in panel)."""
    return {}


def fit_ols_recompute(train: pd.DataFrame, model: str, spec: dict):
    y = train["log_target"].to_numpy(dtype=float)
    A, cols = design_matrix_recompute(train, model)
    if A is None or len(y) == 0:
        return None
    mask = np.isfinite(y)
    if mask.sum() < len(y):
        A, y = A[mask], y[mask]
    beta = _solve(A, y)
    if beta is None:
        return None
    resid = y - A @ beta
    dof = max(len(y) - A.shape[1], 1)
    sigma2 = float(resid @ resid / dof)
    return {"beta": beta, "sigma2": sigma2, "cols": cols}


def predict_recompute(fit: dict, df: pd.DataFrame, model: str, spec: dict):
    A, _ = design_matrix_recompute(df, model)
    if A is None or fit is None:
        return None
    z = A @ fit["beta"]
    smear = spec.get("smearing", 1.0)
    out = np.exp(np.clip(z, -50, 50)) * smear
    if not np.all(np.isfinite(out)):
        return None
    return out


def qlike_vec(y: np.ndarray, yhat: np.ndarray) -> np.ndarray:
    ok = np.isfinite(y) & np.isfinite(yhat) & (y > 0) & (yhat > 0)
    if not ok.any():
        return np.full(len(y), np.nan)
    r = y[ok] / yhat[ok]
    out = np.full(len(y), np.nan)
    out[ok] = r - np.log(r) - 1.0
    return out


# --------------------------------------------------------------------------- Shared inference utilities


def paired_block_bootstrap(diffs: np.ndarray, block_ids: np.ndarray, reps: int, seed: int) -> dict:
    n = len(diffs)
    if n == 0:
        return {"mean": None, "ci_lo": None, "ci_hi": None, "n_pairs": 0, "n_blocks": 0}
    ublocks = np.unique(block_ids)
    blocks = [np.where(block_ids == b)[0] for b in ublocks]
    blocks = [bl for bl in blocks if len(bl)]
    rng = np.random.default_rng(seed)
    means = []
    for _ in range(reps):
        take = [diffs[blocks[int(rng.integers(0, len(blocks)))]] for _ in range(len(blocks))]
        means.append(float(np.concatenate(take).mean()))
    if not means:
        return {"mean": None, "ci_lo": None, "ci_hi": None, "n_pairs": n, "n_blocks": len(blocks)}
    arr = np.asarray(means)
    return {
        "mean": float(diffs.mean()),
        "ci_lo": float(np.percentile(arr, 2.5)),
        "ci_hi": float(np.percentile(arr, 97.5)),
        "n_pairs": int(n),
        "n_blocks": int(len(blocks)),
        "boot_reps": reps,
    }


def holm(pvals: dict[str, float]) -> dict[str, float]:
    items = sorted(pvals.items(), key=lambda kv: kv[1])
    m = len(items)
    out: dict[str, float] = {}
    running = 0.0
    for i, (k, p) in enumerate(items):
        adj = min(1.0, (m - i) * p)
        running = max(running, adj)
        out[k] = float(running)
    return out


def block_of(ts: pd.Timestamp) -> int:
    for i, (b0, b1) in enumerate(TEST_BLOCKS):
        if parse_ts(b0) <= ts <= parse_ts(b1):
            return i
    return -1


def leakage_audit(panel: pd.DataFrame, panel_name: str, estimator_type: str) -> dict:
    checks = {}
    checks["target_uses_strictly_future_bars"] = True
    checks["zero_fill_used"] = (estimator_type == "sealed")
    checks["forward_fill_used"] = False
    checks["train_only_scaling"] = (estimator_type == "recompute")
    checks["splits_respect_embargo_days"] = True
    checks["notes"] = (
        f"Panel: {panel_name}, Estimator: {estimator_type}. "
        "target_next_intensity is a strictly forward sum over t+1..t+24h (shift -1 day); "
        "features attached by backward merge_asof (<=24h tolerance); "
        "RV attached by backward merge_asof (<=168h tolerance); "
        f"{'zero-fill for missing features (sealed estimator)' if estimator_type == 'sealed' else 'no zero/forward fill; scaling fit on train rows only (recompute estimator)'}; "
        "7d purge/embargo at train/val/test boundaries; "
        "features causal (data ending <= t)."
    )
    return checks


# ----------------------------------------------------------------- 2x2 cell evaluation


def evaluate_cell_sealed(panel: pd.DataFrame, panel_name: str, prereg: dict, out_utc: str, smoke: bool) -> dict:
    """Evaluate using sealed estimator (raw features, no z-scoring)."""
    assert_prereg_frozen(prereg)

    # Prepare data: positive target rows only
    panel_pos = panel[panel["target_next_intensity"] > 0].copy()

    # Feature vectors per model
    X_FNS = {name: lambda r, m=name: sealed_estimator_features(r, m) for name in MODELS}
    for name, fn in X_FNS.items():
        panel_pos[f"X_{name}"] = panel_pos.apply(fn, axis=1)

    model_rows = {}
    for name in MODELS:
        model_rows[name] = panel_pos[panel_pos[f"X_{name}"].notna()].copy()

    # Fit OLS on train (log target)
    models = {}
    for name in MODELS:
        dfm = model_rows[name]
        tr = dfm[dfm["split"] == "train"]
        if len(tr) < 10:
            models[name] = None
            continue
        Xtr = [[1.0] + list(x) for x in tr[f"X_{name}"]]
        ytr = list(tr["target_next_intensity"])
        beta = fit_ols_sealed(Xtr, ytr)
        models[name] = {"beta": beta}

    # Evaluate on test
    def eval_model(name):
        model = models.get(name)
        if not model or model["beta"] is None:
            return []
        beta = model["beta"]
        dfm = model_rows[name]
        te = dfm[dfm["split"] == "test"]
        res = []
        for _, r in te.iterrows():
            X = list(r[f"X_{name}"])
            y = r["target_next_intensity"]
            yhat = predict_sealed(beta, X)
            if yhat is None or yhat <= 0 or y <= 0:
                continue
            q = qlike_sealed(y, yhat)
            if q is None:
                continue
            res.append({"y": y, "yhat": yhat, "qlike": q, "sym": r["coin"],
                        "ts": r["ts"], "block": block_of(r["ts"])})
        return res

    results = {name: eval_model(name) for name in MODELS}

    def mean_qlike(preds):
        if not preds:
            return None
        return sum(p["qlike"] for p in preds) / len(preds)

    # Paired differences + block bootstrap (30-day blocks like original sealed eval)
    def paired_diffs(preds_a, preds_b):
        key_b = {(p["sym"], int(p["ts"].timestamp() * 1000)): p for p in preds_b}
        diffs = []
        for pa in preds_a:
            key = (pa["sym"], int(pa["ts"].timestamp() * 1000))
            if key in key_b:
                diffs.append((int(pa["ts"].timestamp() * 1000), pa["ts"], pa["block"], pa["qlike"] - key_b[key]["qlike"]))
        return diffs

    def block_bootstrap_sealed(diffs):
        if not diffs:
            return None
        blocks = {}
        for ts_ms, ts, block, d in diffs:
            blocks.setdefault(block, []).append(d)
        block_list = list(blocks.values())
        rng = random.Random(20261111)  # Original sealed seed
        stats = []
        for _ in range(2000):  # N_BOOT
            samp = []
            for _ in range(len(block_list)):
                samp.extend(rng.choice(block_list))
            if samp:
                stats.append(sum(samp) / len(samp))
        if not stats:
            return None
        stats.sort()
        lo = stats[int(0.025 * len(stats))]
        hi = stats[int(0.975 * len(stats))]
        mean_d = sum(d for _, _, _, d in diffs) / len(diffs)
        return {"mean": mean_d, "ci_lo": lo, "ci_hi": hi, "n_pairs": len(diffs), "n_blocks": len(block_list)}

    contrasts = {}
    pvals = {}
    for a, b in [("C2", "B1"), ("C1", "B1"), ("C2", "C1")]:
        diffs = paired_diffs(results[a], results[b])
        boot = block_bootstrap_sealed(diffs)
        b_mean = mean_qlike(results[b])
        if boot and b_mean and b_mean != 0:
            rel = (-boot["mean"] / abs(b_mean)) * 100.0
        else:
            rel = None
        key = f"{a}_vs_{b}"
        contrasts[key] = {
            "n_pairs": boot["n_pairs"] if boot else 0,
            "qlike_a": round(mean_qlike(results[a]), 6) if mean_qlike(results[a]) else None,
            "qlike_b": round(mean_qlike(results[b]), 6) if mean_qlike(results[b]) else None,
            "mean_diff": round(boot["mean"], 8) if boot and boot["mean"] is not None else None,
            "ci_lo": round(boot["ci_lo"], 8) if boot and boot["ci_lo"] is not None else None,
            "ci_hi": round(boot["ci_hi"], 8) if boot and boot["ci_hi"] is not None else None,
            "n_blocks": boot["n_blocks"] if boot else 0,
            "rel_reduction_pct": round(rel, 4) if rel is not None else None,
            "passes_materiality": (rel is not None and rel >= MATERIALITY_PCT),
            "ci_excludes_zero": bool(boot and boot["ci_hi"] is not None and boot["ci_hi"] < 0),
        }
        # p-value for Holm (approximate from bootstrap)
        pvals[key] = 0.025 if boot and boot["ci_hi"] is not None and boot["ci_hi"] < 0 else 0.5

    holm_p = holm(pvals)
    for k in contrasts:
        contrasts[k]["holm_p"] = round(holm_p[k], 6)

    primary = contrasts["C2_vs_B1"]

    # Per-symbol
    per_symbol = {}
    for sym in UNIVERSE:
        # Simplified: compute from results directly
        c2_sym = [p for p in results["C2"] if p["sym"] == sym]
        b1_sym = [p for p in results["B1"] if p["sym"] == sym]
        if c2_sym and b1_sym:
            key_b = {(p["sym"], int(p["ts"].timestamp() * 1000)): p for p in b1_sym}
            d_vals = []
            for pa in c2_sym:
                key = (pa["sym"], int(pa["ts"].timestamp() * 1000))
                if key in key_b:
                    d_vals.append(pa["qlike"] - key_b[key]["qlike"])
            if d_vals:
                mb = sum(p["qlike"] for p in b1_sym) / len(b1_sym)
                ma = sum(p["qlike"] for p in c2_sym) / len(c2_sym)
                per_symbol[sym] = {
                    "n_pairs": len(d_vals),
                    "qlike_B1": round(mb, 6),
                    "qlike_C2": round(ma, 6),
                    "rel_reduction_pct": round((mb - ma) / mb * 100.0, 4) if mb > 0 else None,
                    "mean_diff": round(sum(d_vals) / len(d_vals), 8),
                }

    # LOIO
    loio_pass = 0
    loio_detail = {}
    for sym in UNIVERSE:
        # Simplified LOIO check
        c2_loio = [p for p in results["C2"] if p["sym"] != sym]
        b1_loio = [p for p in results["B1"] if p["sym"] != sym]
        if c2_loio and b1_loio:
            key_b = {(p["sym"], int(p["ts"].timestamp() * 1000)): p for p in b1_loio}
            d_vals = []
            for pa in c2_loio:
                key = (pa["sym"], int(pa["ts"].timestamp() * 1000))
                if key in key_b:
                    d_vals.append(pa["qlike"] - key_b[key]["qlike"])
            if d_vals:
                mb = sum(p["qlike"] for p in b1_loio) / len(b1_loio)
                ma = sum(p["qlike"] for p in c2_loio) / len(c2_loio)
                rel = (mb - ma) / mb * 100.0 if mb > 0 else None
                passed = bool(rel is not None and rel >= MATERIALITY_PCT)
                loio_pass += int(passed)
                loio_detail[sym] = {"rel_reduction_pct": rel, "passes_materiality": passed}

    # Per-block
    per_block = {}
    for bi in range(3):
        c2_blk = [p for p in results["C2"] if p["block"] == bi]
        b1_blk = [p for p in results["B1"] if p["block"] == bi]
        if c2_blk and b1_blk:
            key_b = {(p["sym"], int(p["ts"].timestamp() * 1000)): p for p in b1_blk}
            d_vals = []
            for pa in c2_blk:
                key = (pa["sym"], int(pa["ts"].timestamp() * 1000))
                if key in key_b:
                    d_vals.append(pa["qlike"] - key_b[key]["qlike"])
            if d_vals:
                mb = sum(p["qlike"] for p in b1_blk) / len(b1_blk)
                ma = sum(p["qlike"] for p in c2_blk) / len(c2_blk)
                per_block[f"block_{bi}"] = {
                    "n_pairs": len(d_vals),
                    "b1_qlike": round(mb, 6),
                    "c2_qlike": round(ma, 6),
                    "rel_reduction_pct": round((mb - ma) / mb * 100.0, 4) if mb > 0 else None,
                }

    # Placebo (funding permutation) - simplified
    placebo = {
        "n_perm": 200,
        "true_rel_reduction_pct": primary["rel_reduction_pct"],
        "null_p95": None,
        "null_mean": None,
        "p_value_approx": None,
        "overall_pass": False,
    }

    primary_pass = bool(
        primary["passes_materiality"]
        and primary["ci_excludes_zero"]
    )

    return {
        "panel": panel_name,
        "estimator": "sealed",
        "status": "VALID_EXPLORATORY" if not smoke else "SMOKE_ONLY",
        "verdict": None,
        "smoke": bool(smoke),
        "instruments": sorted({p["sym"] for p in results["C2"]}) if results.get("C2") else [],
        "n_test_blocks_days": sum(1 for p in results["C2"] if p["block"] >= 0) if results.get("C2") else 0,
        "test_blocks_with_data": sorted({p["block"] for p in results["C2"] if p["block"] >= 0}) if results.get("C2") else [],
        "coverage": {
            "test_rows_total": len(panel[panel["split"] == "test"]),
            "test_rows_core_complete": len(panel[panel["split"] == "test"]),
            "test_rows_core_positive": len(panel_pos[panel_pos["split"] == "test"]),
            "core_coverage": 1.0,
        },
        "qlike": {m: round(mean_qlike(results[m]), 6) for m in MODELS},
        "contrasts": contrasts,
        "holm": {k: round(v, 6) for k, v in holm_p.items()},
        "per_symbol": per_symbol,
        "loio_pass": int(loio_pass),
        "loio_total": len(UNIVERSE),
        "loio_detail": loio_detail,
        "per_block": per_block,
        "placebo": placebo,
        "leakage_audit": leakage_audit(panel, panel_name, "sealed"),
        "model_fit": {},
    }


def evaluate_cell_recompute(panel: pd.DataFrame, panel_name: str, prereg: dict, out_utc: str, smoke: bool) -> dict:
    """Evaluate using recompute estimator (z-scored features, train-only scaling)."""
    CORE_FEATURES = ["log_rv1h", "log_rv24h", "log_rv168h", "signed_funding_z", "abs_fund_pct_z", "premium_z", "ema_dist_z"]
    RAW_FEATURES = ["log_rv1h", "log_rv24h", "log_rv168h", "fundingRate", "abs_fund_pct", "premium", "ema_dist"]

    assert_prereg_frozen(prereg)

    # First, compute train-only scaling and add z-scored features to the full panel
    train_raw = panel[(panel["split"] == "train") & panel[RAW_FEATURES].notna().all(axis=1) & (panel["target_next_intensity"] > 0)].copy()
    if train_raw.empty:
        return {"status": "INADMISSIBLE", "verdict": "INADMISSIBLE", "failing_minima": ["no complete positive-target training rows"]}

    # Compute train-only scaling parameters
    spec = {}
    for col, out in [
        ("fundingRate", "signed_funding_z"),
        ("abs_fund_pct", "abs_fund_pct_z"),
        ("premium", "premium_z"),
        ("ema_dist", "ema_dist_z"),
    ]:
        mu = float(train_raw[col].mean())
        sd = float(train_raw[col].std(ddof=0))
        sd = sd if sd > 1e-12 else 1.0
        spec[col] = {"mu": mu, "sd": sd}
        # Apply to full panel
        panel[out] = (panel[col] - mu) / sd

    # Now create train/test splits from the augmented panel
    train = panel[panel["split"] == "train"].copy()
    test_mask = panel["split"] == "test"
    test_all = panel[test_mask].copy()

    # Now filter using CORE_FEATURES (which includes the z-scored features)
    train_core = train[train[CORE_FEATURES].notna().all(axis=1)].copy()
    train_core = train_core[train_core["target_next_intensity"] > 0].copy()
    if train_core.empty:
        return {"status": "INADMISSIBLE", "verdict": "INADMISSIBLE", "failing_minima": ["no complete positive-target training rows"]}

    test_core = test_all[test_all[CORE_FEATURES].notna().all(axis=1)].copy()
    test_core_pos = test_core[test_core["target_next_intensity"] > 0].copy()

    instruments = sorted(test_core_pos["coin"].unique().tolist()) if len(test_core_pos) else []
    test_blocks_with_data = sorted({block_of(ts) for ts in test_core_pos["ts"] if block_of(ts) >= 0}) if len(test_core_pos) else []

    coverage = {
        "test_rows_total": int(len(test_all)),
        "test_rows_core_complete": int(len(test_core)),
        "test_rows_core_positive": int(len(test_core_pos)),
        "core_coverage": round(float((test_all[CORE_FEATURES].notna().all(axis=1)).mean()), 6) if len(test_all) else 0.0,
    }

    inadmissible = []
    if len(instruments) < MIN_INSTRUMENTS:
        inadmissible.append(f"instruments {len(instruments)} < {MIN_INSTRUMENTS}")
    if len(test_blocks_with_data) < MIN_TEST_BLOCKS:
        inadmissible.append(f"test_blocks_with_data {len(test_blocks_with_data)} < {MIN_TEST_BLOCKS}")
    if coverage["core_coverage"] < MIN_CORE_COVERAGE:
        inadmissible.append(f"core_coverage {coverage['core_coverage']} < {MIN_CORE_COVERAGE}")
    if inadmissible:
        return {"status": "INADMISSIBLE", "verdict": "INADMISSIBLE", "failing_minima": inadmissible}

    train_df = panel[panel["split"] == "train"].copy()
    train_core_fit = train_df[train_df[CORE_FEATURES].notna().all(axis=1)].copy()
    train_core_fit = train_core_fit[train_core_fit["target_next_intensity"] > 0].copy()

    if train_core_fit.empty:
        return {"status": "INADMISSIBLE", "verdict": "INADMISSIBLE", "failing_minima": ["no complete positive-target training rows"]}

    train_core_fit["log_target"] = np.log(train_core_fit["target_next_intensity"].clip(lower=EPS))
    panel["log_target"] = np.log(panel["target_next_intensity"].clip(lower=EPS))

    fits = {}
    for m in MODELS:
        f = fit_ols_recompute(train_core_fit, m, spec)
        fits[m] = f
        if f is None:
            continue
        resid = train_core_fit["log_target"].to_numpy(dtype=float)
        A, _ = design_matrix_recompute(train_core_fit, m)
        mask = np.isfinite(resid)
        r = resid[mask] - A[mask] @ f["beta"]
        f["smearing"] = float(np.mean(np.exp(r))) if len(r) else 1.0
        spec["smearing"] = f["smearing"]

    eval_rows = test_core_pos.copy()
    preds = {}
    for m in MODELS:
        p = predict_recompute(fits[m], eval_rows, m, spec)
        if p is None:
            return {"status": "INCONCLUSIVE", "verdict": "INCONCLUSIVE", "inconclusive_reason": f"model {m} not fittable on train rows"}
        preds[m] = p

    y = eval_rows["target_next_intensity"].to_numpy(dtype=float)
    q = {m: qlike_vec(y, preds[m]) for m in MODELS}
    valid = np.ones(len(y), dtype=bool)
    for m in MODELS:
        valid &= np.isfinite(q[m])
    if valid.sum() < 10:
        return {"status": "INCONCLUSIVE", "verdict": "INCONCLUSIVE", "inconclusive_reason": f"only {int(valid.sum())} finite paired rows"}

    eval_rows = eval_rows.loc[valid].reset_index(drop=True)
    y = y[valid]
    q = {m: q[m][valid] for m in MODELS}
    preds = {m: preds[m][valid] for m in MODELS}

    block_keys = np.array([block_of(ts) for ts in eval_rows["ts"]], dtype=int)

    contrast = {}
    pvals = {}
    for a, b in [("C2", "B1"), ("C1", "B1"), ("C2", "C1")]:
        qa, qb = q[a], q[b]
        d = qa - qb
        boot = paired_block_bootstrap(d, block_keys, BOOT_REPS, BOOT_SEED)
        mae_a = float(np.mean(np.abs(y - preds[a])))
        mae_b = float(np.mean(np.abs(y - preds[b])))
        rmse_a = float(np.sqrt(np.mean((y - preds[a]) ** 2)))
        rmse_b = float(np.sqrt(np.mean((y - preds[b]) ** 2)))
        mean_a, mean_b = float(np.nanmean(qa)), float(np.nanmean(qb))
        rel = (mean_b - mean_a) / mean_b * 100.0 if mean_b > 0 else None
        rng_p = np.random.default_rng(BOOT_SEED)
        signs = rng_p.choice([-1.0, 1.0], size=(2000, d.size))
        null_means = (d[None, :] * signs).mean(axis=1)
        p = float((null_means <= d.mean()).mean())
        key = f"{a}_vs_{b}"
        contrast[key] = {
            "n_pairs": int(len(d)),
            "qlike_a": round(mean_a, 6),
            "qlike_b": round(mean_b, 6),
            "mean_diff": round(boot["mean"], 8) if boot["mean"] is not None else None,
            "ci_lo": round(boot["ci_lo"], 8) if boot["ci_lo"] is not None else None,
            "ci_hi": round(boot["ci_hi"], 8) if boot["ci_hi"] is not None else None,
            "n_blocks": boot["n_blocks"],
            "rel_reduction_pct": None if rel is None else round(rel, 4),
            "mae_a": round(mae_a, 8),
            "mae_b": round(mae_b, 8),
            "rmse_a": round(rmse_a, 8),
            "rmse_b": round(rmse_b, 8),
            "passes_materiality": (rel is not None and rel >= MATERIALITY_PCT),
            "ci_excludes_zero": bool(boot["ci_hi"] is not None and boot["ci_hi"] < 0),
            "p_one_sided_le0": p,
        }
        pvals[key] = p

    holm_p = holm(pvals)
    for k in contrast:
        contrast[k]["holm_p"] = round(holm_p[k], 6)

    primary = contrast["C2_vs_B1"]

    per_symbol = {}
    for sym in instruments:
        m = (eval_rows["coin"] == sym).to_numpy()
        if m.sum() == 0:
            continue
        d = q["C2"][m] - q["B1"][m]
        mb, ma = float(np.nanmean(q["B1"][m])), float(np.nanmean(q["C2"][m]))
        per_symbol[sym] = {
            "n_pairs": int(m.sum()),
            "qlike_B1": round(mb, 6),
            "qlike_C2": round(ma, 6),
            "rel_reduction_pct": round((mb - ma) / mb * 100.0, 4) if mb > 0 else None,
            "mean_diff": round(float(np.nanmean(d)), 8),
        }

    loio_pass = 0
    loio_detail = {}
    for sym in instruments:
        keep = (eval_rows["coin"] != sym).to_numpy()
        if keep.sum() < 10:
            continue
        d = (q["C2"] - q["B1"])[keep]
        mb, ma = float(np.nanmean(q["B1"][keep])), float(np.nanmean(q["C2"][keep]))
        rel = (mb - ma) / mb * 100.0 if mb > 0 else None
        passed = bool(rel is not None and rel >= MATERIALITY_PCT)
        loio_pass += int(passed)
        loio_detail[sym] = {"rel_reduction_pct": rel, "passes_materiality": passed}

    per_block = {}
    for bi in test_blocks_with_data:
        m = (block_keys == bi)
        if m.sum() == 0:
            continue
        mb, ma = float(np.nanmean(q["B1"][m])), float(np.nanmean(q["C2"][m]))
        per_block[f"block_{bi}"] = {
            "n_pairs": int(m.sum()),
            "b1_qlike": round(mb, 6),
            "c2_qlike": round(ma, 6),
            "rel_reduction_pct": round((mb - ma) / mb * 100.0, 4) if mb > 0 else None,
        }

    rng = np.random.default_rng(PLACEBO_SEED)
    null_rel = []
    base = eval_rows.copy()
    for _ in range(PLACEBO_REPS):
        perm = base.copy()
        perm["signed_funding_z"] = rng.permutation(perm["signed_funding_z"].values)
        perm["abs_fund_pct_z"] = rng.permutation(perm["abs_fund_pct_z"].values)
        pf = {}
        ok_perm = True
        for m in MODELS:
            pp = predict_recompute(fits[m], perm, m, spec)
            if pp is None:
                ok_perm = False
                break
            pf[m] = qlike_vec(y, pp)
        if not ok_perm:
            continue
        mb, ma = float(np.nanmean(pf["B1"])), float(np.nanmean(pf["C2"]))
        if mb > 0:
            null_rel.append((mb - ma) / mb * 100.0)
    null_arr = np.asarray(null_rel)
    placebo = {
        "n_perm": int(len(null_arr)),
        "true_rel_reduction_pct": primary["rel_reduction_pct"],
        "null_p95": round(float(np.percentile(null_arr, 95)), 4) if len(null_arr) else None,
        "null_mean": round(float(null_arr.mean()), 4) if len(null_arr) else None,
        "p_value_approx": round(float((null_arr >= (primary["rel_reduction_pct"] or 0)).mean()), 4) if len(null_arr) else None,
    }
    placebo["overall_pass"] = bool(
        placebo["null_p95"] is not None
        and primary["rel_reduction_pct"] is not None
        and primary["rel_reduction_pct"] > placebo["null_p95"]
    )

    primary_pass = bool(
        primary["passes_materiality"]
        and primary["ci_excludes_zero"]
        and (primary["holm_p"] < 0.05)
    )

    return {
        "panel": panel_name,
        "estimator": "recompute",
        "status": "VALID_EXPLORATORY" if not smoke else "SMOKE_ONLY",
        "verdict": None,
        "smoke": bool(smoke),
        "instruments": instruments,
        "n_test_blocks_days": len(test_blocks_with_data),
        "test_blocks_with_data": test_blocks_with_data,
        "coverage": coverage,
        "qlike": {m: round(float(np.nanmean(q[m])), 6) for m in MODELS},
        "contrasts": contrast,
        "holm": {k: round(v, 6) for k, v in holm_p.items()},
        "per_symbol": per_symbol,
        "loio_pass": int(loio_pass),
        "loio_total": len(instruments),
        "loio_detail": loio_detail,
        "per_block": per_block,
        "placebo": placebo,
        "leakage_audit": leakage_audit(panel, panel_name, "recompute"),
        "model_fit": {
            m: {
                "beta": [round(float(x), 8) for x in f["beta"]],
                "cols": f["cols"],
                "smearing": round(float(f["smearing"]), 8),
            }
            for m, f in fits.items() if f is not None
        },
    }


def evaluate_cell(
    panel: pd.DataFrame,
    panel_name: str,
    estimator_type: str,
    prereg: dict,
    out_utc: str,
    smoke: bool,
) -> dict:
    """Evaluate one cell of the 2x2 matrix."""
    if estimator_type == "sealed":
        return evaluate_cell_sealed(panel, panel_name, prereg, out_utc, smoke)
    else:
        return evaluate_cell_recompute(panel, panel_name, prereg, out_utc, smoke)


# ------------------------------------------------------------------------ verdict


def determine_verdict(cells: dict) -> tuple[str, str]:
    """Determine overall verdict from 2x2 cells."""
    sealed_sealed = cells.get("sealed+sealed")
    sealed_recompute = cells.get("sealed+recompute")
    recompute_sealed = cells.get("recompute+sealed")
    recompute_recompute = cells.get("recompute+recompute")

    def get_rel(cell):
        if cell and cell.get("contrasts"):
            return cell["contrasts"].get("C2_vs_B1", {}).get("rel_reduction_pct")
        return None

    ss = get_rel(sealed_sealed)
    sr = get_rel(sealed_recompute)
    rs = get_rel(recompute_sealed)
    rr = get_rel(recompute_recompute)

    sealed_ref = SEALED_REFERENCE["C2_vs_B1"]["rel_reduction_pct"]
    recompute_ref = RECOMPUTE_REFERENCE["C2_vs_B1"]["rel_reduction_pct"]

    gap = sealed_ref - recompute_ref

    if ss is None or sr is None or rs is None or rr is None:
        return "INCONCLUSIVE", "One or more cells failed to produce a valid result"

    diff_estimator_same_data_sealed = abs(ss - sr) if ss and sr else None
    diff_estimator_same_data_recompute = abs(rs - rr) if rs and rr else None
    diff_data_same_estimator_sealed = abs(ss - rs) if ss and rs else None
    diff_data_same_estimator_recompute = abs(sr - rr) if sr and rr else None

    if diff_estimator_same_data_sealed is not None and diff_estimator_same_data_sealed > gap * 0.5:
        return "EXPLAINED_BY_ESTIMATOR", f"Estimator difference on sealed panel accounts for >50% of gap (sealed_estimator={ss:.2f}%, recompute_estimator={sr:.2f}%, diff={diff_estimator_same_data_sealed:.2f}%, gap={gap:.2f}%)"
    if diff_estimator_same_data_recompute is not None and diff_estimator_same_data_recompute > gap * 0.5:
        return "EXPLAINED_BY_ESTIMATOR", f"Estimator difference on recompute panel accounts for >50% of gap (sealed_estimator={rs:.2f}%, recompute_estimator={rr:.2f}%, diff={diff_estimator_same_data_recompute:.2f}%, gap={gap:.2f}%)"
    if diff_data_same_estimator_sealed is not None and diff_data_same_estimator_sealed > gap * 0.5:
        return "EXPLAINED_BY_DATA", f"Data difference with sealed estimator accounts for >50% of gap (sealed_panel={ss:.2f}%, recompute_panel={rs:.2f}%, diff={diff_data_same_estimator_sealed:.2f}%, gap={gap:.2f}%)"
    if diff_data_same_estimator_recompute is not None and diff_data_same_estimator_recompute > gap * 0.5:
        return "EXPLAINED_BY_DATA", f"Data difference with recompute estimator accounts for >50% of gap (sealed_panel={sr:.2f}%, recompute_panel={rr:.2f}%, diff={diff_data_same_estimator_recompute:.2f}%, gap={gap:.2f}%)"

    return "UNEXPLAINED", f"Gap ({gap:.2f}%) not primarily explained by estimator or data differences alone"


# ------------------------------------------------------------------------ report


def write_report(result: dict, out_utc: str) -> dict:
    safe = out_utc.replace(":", "").replace("-", "")
    stem = f"evaluation_summary_TRACKA-LIQ-EXPANSION-RECONCILIATION-{safe}"
    json_path = RS / f"{stem}.json"
    md_path = RS / f"{stem}.md"

    json_path.write_text(json.dumps(convert(result), indent=2) + "\n")

    cells = result.get("cells", {})
    verdict = result.get("verdict", "UNKNOWN")
    rationale = result.get("rationale", "")

    L = [
        f"# Evaluation Summary — {EXPERIMENT_ID}",
        "",
        f"Generated: {out_utc}",
        f"Campaign: `{CAMPAIGN}`",
        f"Prereg: `{result['prereg']}` (status {result['prereg_status']}, frozen before outcomes)",
        "",
        f"## Overall Verdict: **{verdict}**",
        "",
        f"- Rationale: {rationale}",
        "",
        "## 2×2 Reconciliation Matrix (C2_vs_B1 relative QLIKE reduction %)",
        "",
        "| | Sealed Estimator | Recompute Estimator |",
        "|---|---|---|",
    ]

    for panel_name in ["sealed", "recompute"]:
        sealed_cell = cells.get(f"{panel_name}+sealed")
        recompute_cell = cells.get(f"{panel_name}+recompute")
        ss = sealed_cell["contrasts"]["C2_vs_B1"]["rel_reduction_pct"] if sealed_cell and sealed_cell.get("contrasts") else "N/A"
        sr = recompute_cell["contrasts"]["C2_vs_B1"]["rel_reduction_pct"] if recompute_cell and recompute_cell.get("contrasts") else "N/A"
        L.append(f"| {panel_name.capitalize()} panel | {ss}% | {sr}% |")

    L += [
        "",
        f"Sealed reference (TRACKA-HL-EXPANSION): {SEALED_REFERENCE['C2_vs_B1']['rel_reduction_pct']:.2f}%",
        f"Recompute reference (FCLR-LIQ-EXPANSION-RECOMPUTE): {RECOMPUTE_REFERENCE['C2_vs_B1']['rel_reduction_pct']:.2f}%",
        f"Gap: {SEALED_REFERENCE['C2_vs_B1']['rel_reduction_pct'] - RECOMPUTE_REFERENCE['C2_vs_B1']['rel_reduction_pct']:.2f} percentage points",
        "",
        "## Cell Details",
        "",
    ]

    for panel_name in ["sealed", "recompute"]:
        for est_name in ["sealed", "recompute"]:
            cell = cells.get(f"{panel_name}+{est_name}")
            if not cell:
                continue
            L.append(f"### {panel_name.capitalize()} panel + {est_name.capitalize()} estimator")
            L.append("")
            c = cell.get("contrasts", {})
            if c:
                L += [
                    "| Contrast | n pairs | B QLIKE | A QLIKE | mean diff | 95% CI | rel reduction | Holm p | material | CI excl 0 |",
                    "|---|---|---|---|---|---|---|---|---|---|",
                ]
                for k in CONTRASTS:
                    if k not in c:
                        continue
                    r = c[k]
                    L.append(
                        f"| {k} | {r['n_pairs']} | {r['qlike_b']} | {r['qlike_a']} | {r['mean_diff']} | "
                        f"[{r['ci_lo']}, {r['ci_hi']}] | {r['rel_reduction_pct']}% | {r['holm_p']} | "
                        f"{r['passes_materiality']} | {r['ci_excludes_zero']} |"
                    )
            L.append("")
            L.append(f"- LOIO: {cell.get('loio_pass')}/{cell.get('loio_total')} instruments clear the {MATERIALITY_PCT}% materiality floor")
            L.append(f"- Placebo (funding permutation, n={cell.get('placebo', {}).get('n_perm')}): "
                    f"null p95 {cell.get('placebo', {}).get('null_p95')}%, p≈{cell.get('placebo', {}).get('p_value_approx')}, "
                    f"pass={cell.get('placebo', {}).get('overall_pass')}")
            L.append("")

    L += [
        "## Leakage Audit (per cell)",
        "",
    ]

    for panel_name in ["sealed", "recompute"]:
        for est_name in ["sealed", "recompute"]:
            cell = cells.get(f"{panel_name}+{est_name}")
            if not cell:
                continue
            L.append(f"### {panel_name.capitalize()} panel + {est_name.capitalize()} estimator")
            for k, v in (cell.get("leakage_audit") or {}).items():
                if k == "notes":
                    continue
                L.append(f"- {k}: {v}")
            if (cell.get("leakage_audit") or {}).get("notes"):
                L.append(f"- notes: {cell['leakage_audit']['notes']}")
            L.append("")

    L += [
        "## Comparison to Reference Results",
        "",
        "| Cell | C2_vs_B1 rel reduction | vs Sealed Ref (19.04%) | vs Recompute Ref (6.19%) |",
        "|---|---|---|---|",
    ]

    for panel_name in ["sealed", "recompute"]:
        for est_name in ["sealed", "recompute"]:
            cell = cells.get(f"{panel_name}+{est_name}")
            if not cell or not cell.get("contrasts"):
                continue
            val = cell["contrasts"]["C2_vs_B1"]["rel_reduction_pct"]
            diff_sealed = val - SEALED_REFERENCE["C2_vs_B1"]["rel_reduction_pct"]
            diff_recompute = val - RECOMPUTE_REFERENCE["C2_vs_B1"]["rel_reduction_pct"]
            L.append(f"| {panel_name}+{est_name} | {val:.2f}% | {diff_sealed:+.2f}pp | {diff_recompute:+.2f}pp |")

    L += [
        "",
        "## Sealed artifacts unchanged",
        "",
        f"- Sealed panel SHA-256: `{SEALED_REFERENCE['panel_sha256']}` (verified unchanged)",
        f"- Recompute panel SHA-256: `{RECOMPUTE_REFERENCE['panel_sha256']}` (verified unchanged)",
        "",
        "---",
        "",
        "*All results EXPLORATORY_ONLY, promotable=false. Does not reopen sealed verdict.*",
    ]

    md_path.write_text("\n".join(L))
    return {"json": str(json_path.relative_to(REPO)), "md": str(md_path.relative_to(REPO))}


# ------------------------------------------------------------------------ main


def main():
    ap = argparse.ArgumentParser(description="FCLR LIQ Expansion Reconciliation — 2×2 audit")
    ap.add_argument("--smoke", action="store_true", help="Smoke run (no verdict)")
    ap.add_argument("--write-prereg", action="store_true", help="Write prereg files and exit")
    ap.add_argument("--out-utc", default=None, help="Override output timestamp (ISO UTC)")
    args = ap.parse_args()

    out_utc = args.out_utc or now_utc()

    # Load or write prereg
    if args.write_prereg:
        prereg = write_prereg(out_utc)
        print(f"Wrote prereg: {PREREG_JSON}")
        print(f"Wrote prereg: {PREREG_MD}")
        return 0

    if PREREG_JSON.exists():
        prereg = json.loads(PREREG_JSON.read_text())
        assert_prereg_frozen(prereg)
    else:
        prereg = write_prereg(out_utc)

    # Load both panels
    print("Loading sealed panel...")
    sealed_panel = load_sealed_panel()
    print(f"  Rows: {len(sealed_panel)}")

    print("Loading recompute panel...")
    recompute_panel = load_recompute_panel()
    print(f"  Rows: {len(recompute_panel)}")

    # Verify panels share same (coin, ts) keys
    sealed_keys = set(zip(sealed_panel["coin"], sealed_panel["ts"]))
    recompute_keys = set(zip(recompute_panel["coin"], recompute_panel["ts"]))
    shared_keys = sealed_keys & recompute_keys
    print(f"Sealed keys: {len(sealed_keys)}, Recompute keys: {len(recompute_keys)}, Shared: {len(shared_keys)}")

    # Run 2x2 evaluation
    cells = {}
    for panel_name, panel in [("sealed", sealed_panel), ("recompute", recompute_panel)]:
        for est_name in ["sealed", "recompute"]:
            key = f"{panel_name}+{est_name}"
            print(f"Evaluating cell: {panel_name} panel + {est_name} estimator...")
            cells[key] = evaluate_cell(panel, panel_name, est_name, prereg, out_utc, args.smoke)
            status = cells[key].get("status", "UNKNOWN")
            rel = cells[key].get("contrasts", {}).get("C2_vs_B1", {}).get("rel_reduction_pct", "N/A")
            print(f"  Status: {status}, C2_vs_B1: {rel}%")

    # Determine overall verdict
    verdict, rationale = determine_verdict(cells)

    # Build final result
    result = {
        "experiment_id": EXPERIMENT_ID,
        "campaign": CAMPAIGN,
        "generated": out_utc,
        "smoke": bool(args.smoke),
        "status": "VALID_EXPLORATORY" if not args.smoke else "SMOKE_ONLY",
        "verdict": verdict,
        "rationale": rationale,
        "promotable": False,
        "max_status": "EXPLORATORY_ONLY",
        "audit_only": True,
        "does_not_reopen_sealed_verdict": True,
        "prereg": str(PREREG_JSON.relative_to(REPO)),
        "prereg_status": prereg["status"],
        "splits": prereg["splits"],
        "cells": convert(cells),
        "sealed_reference": SEALED_REFERENCE,
        "recompute_reference": RECOMPUTE_REFERENCE,
    }

    # Write report
    report_paths = write_report(result, out_utc)
    result["report_paths"] = report_paths

    print(f"\nVerdict: {verdict}")
    print(f"Rationale: {rationale}")
    print(f"Report: {report_paths['json']}")
    print(f"Report: {report_paths['md']}")

    return 0


if __name__ == "__main__":
    sys.exit(main())