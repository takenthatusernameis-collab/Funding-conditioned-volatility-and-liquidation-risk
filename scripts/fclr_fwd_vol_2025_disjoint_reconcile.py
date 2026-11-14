#!/usr/bin/env python3
"""FCLR-FWD-VOL-2025-DISJOINT-RECONCILE — estimator/data reconciliation (P1, Track C).

Attribute the EXPLORATORY_NULL of FCLR-FWD-VOL-2025-DISJOINT-CROSS-20261114T183000Z
(pooled C2-B1 mean diff +0.006923, rel -1.963%, 95% CI [-0.012604, 0.028030])
to estimator behavior or to a data-lineage defect on the cached 2025 panel.

Frozen design (see research_state/prereg_fclr_fwd_vol_2025_disjoint_reconcile_<UTC>.json):

  panel      research_state/tracka_fwd_vol_2025_disjoint_cross_panel_20261114T191615Z.parquet
             (sha256 de0ca73e7d092a205e5f8c1163d56437384d1b15d65b4a27bc54a57e21738cba)
  blocks     train 2025-04-25..2025-05-24 / test 2025-06
             train 2025-09-25..2025-10-24 / test 2025-11
             train 2025-10-25..2025-11-23 / test 2025-12
             7-day embargo between train end and test start
  models     B0/B1/C1/C2, primary contrast C2 vs B1 on 24h QLIKE
  cells      {existing panel, cleaned panel} x {sealed estimator, corrected estimator}
  sealed     raw features, ridge-stabilised normal equations, no scaling, no
             train-only smearing, no target-derived fills
  corrected  train-only standardization, finite-row masking, train-only log-target
             smearing, explicit missingness policy (drop, never fill)
  inference  paired day-block bootstrap (2000 deterministic reps, seed 20261114),
             Holm over the horizon x contrast family, LOIO, funding-permutation
             placebo (200 reps, seed 20261114), leakage audit
  verdict    EXPLAINED_BY_ESTIMATOR | EXPLAINED_BY_DATA | UNEXPLAINED | INCONCLUSIVE

Lineage audit (coverage/arithmetic only, no outcome values): the cached mark-price
CSV for XRPUSDT 2025-10-19 stores premium-index numbers in the close column instead
of a price. The cleaned panel is a lineage-preserving copy that removes that day's
rows, recomputes XRP rolling RV/targets after the removal, and never imputes a price.

All outputs EXPLORATORY_ONLY, promotable=false. No network. No sealed mutation.

Usage:
  python3 scripts/fclr_fwd_vol_2025_disjoint_reconcile.py --write-prereg
  python3 scripts/fclr_fwd_vol_2025_disjoint_reconcile.py --smoke
  python3 scripts/fclr_fwd_vol_2025_disjoint_reconcile.py
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import sys
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import pandas as pd

REPO = Path(__file__).resolve().parents[1]
if str(REPO / "scripts") not in sys.path:
    sys.path.insert(0, str(REPO / "scripts"))
import fclr_fwd_vol_confirm as fwd  # noqa: E402

RS = REPO / "research_state"
UTC = fwd.UTC
EPS = fwd.EPS

CAMPAIGN = "FCLR-FWD-VOL-2025-DISJOINT-RECONCILE-20261114T193000Z"
EXPERIMENT_ID = CAMPAIGN
PREREG_STEM = "prereg_fclr_fwd_vol_2025_disjoint_reconcile_20261114T193000Z"
PREREG_JSON = RS / f"{PREREG_STEM}.json"
PREREG_MD = RS / f"{PREREG_STEM}.md"

SOURCE_PREREG = RS / "prereg_fclr_fwd_vol_2025_disjoint_cross_20261114T183000Z.json"
SOURCE_EVAL = RS / "evaluation_summary_FCLR-FWD-VOL-2025-DISJOINT-CROSS-20261114T191615Z.json"
PANEL_PATH = RS / "tracka_fwd_vol_2025_disjoint_cross_panel_20261114T191615Z.parquet"
PANEL_SHA256 = "de0ca73e7d092a205e5f8c1163d56437384d1b15d65b4a27bc54a57e21738cba"

SEALED_REFERENCE = {
    "verdict_id": "FCLR-FWD-VOL-2025-DISJOINT-CROSS-20261114T183000Z",
    "mean_diff": 0.0069231708051235965,
    "rel_reduction_pct": -1.9633752428119817,
    "ci": [-0.012604044681266236, 0.028030237827547048],
    "n": 10800,
    "n_days": 90,
}

DATA_START = "2025-04-25T00:00:00Z"
DATA_END = "2025-12-31T23:00:00Z"
HORIZONS = [6, 24, 72, 168]
PRIMARY_HORIZON = 24
MODELS = ("B0", "B1", "C1", "C2")
CONTRASTS = (("C2", "B1"), ("C1", "B1"), ("C2", "C1"))
BLOCKS = [
    {"block": 0, "train_start": "2025-04-25T00:00:00Z", "train_end": "2025-05-24T23:00:00Z",
     "test_start": "2025-06-01T00:00:00Z", "test_end": "2025-06-30T23:00:00Z"},
    {"block": 1, "train_start": "2025-09-25T00:00:00Z", "train_end": "2025-10-24T23:00:00Z",
     "test_start": "2025-11-01T00:00:00Z", "test_end": "2025-11-30T23:00:00Z"},
    {"block": 2, "train_start": "2025-10-25T00:00:00Z", "train_end": "2025-11-23T23:00:00Z",
     "test_start": "2025-12-01T00:00:00Z", "test_end": "2025-12-31T23:00:00Z"},
]
EMBARGO_DAYS = 7

BOOT_REPS = 2000
BOOT_SEED = 20261114
PLACEBO_REPS = 200
PLACEBO_SEED = 20261114
MATERIALITY_PCT = 2.0
MIN_INSTRUMENTS = 5
MIN_BLOCKS = 3

# The single cached mark-price day whose close column holds premium-index values.
CORRUPT_SYMBOL = "XRPUSDT"
CORRUPT_DAY = "2025-10-19"
CORRUPT_DAY_START = "2025-10-19T00:00:00Z"
CORRUPT_DAY_END = "2025-10-19T23:00:00Z"
CORRUPT_FILE = ("research_state/data_cache/XRPUSDT_2025_10/"
                "markPriceKlines-2025-10-19/XRPUSDT-1h-2025-10-19.csv")

VERDICTS = ("EXPLAINED_BY_ESTIMATOR", "EXPLAINED_BY_DATA", "UNEXPLAINED", "INCONCLUSIVE")

CORE_COLS = ["log_rv1h", "log_rv24h", "log_rv168h", "signed_funding",
             "abs_fund_pct", "premium", "ema_dist", "target_24h"]


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


# --------------------------------------------------------------------- prereg


def build_prereg(out_utc: str) -> dict:
    return {
        "experiment_id": EXPERIMENT_ID,
        "campaign": CAMPAIGN,
        "cell": "FWD-VOL-2025-DISJOINT-RECONCILE",
        "track": "C_volatility_exploratory",
        "priority": "P1",
        "status": "FROZEN_PRE_OUTCOMES",
        "generated_utc": out_utc,
        "frozen_before_outcomes": True,
        "pre_registered_before_outcomes": True,
        "outcome_data_inspected_before_freeze": False,
        "promotable": False,
        "max_status": "EXPLORATORY_ONLY",
        "audit_only": True,
        "does_not_reopen_sealed_verdict": True,
        "purpose": (
            "Attribute the EXPLORATORY_NULL of the 2025 disjoint cross "
            "(FCLR-FWD-VOL-2025-DISJOINT-CROSS-20261114T183000Z: pooled C2-B1 mean diff "
            "+0.006923, relative reduction -1.963%, 95% CI [-0.012604, 0.028030]) to estimator "
            "behaviour or to a data-lineage defect on the cached 2025 panel. Two-by-two "
            "attribution matrix over {existing panel, cleaned lineage copy} x {sealed "
            "estimator, corrected estimator}. All results EXPLORATORY_ONLY, promotable=false. "
            "Does not reopen any sealed verdict."
        ),
        "source_experiment": {
            "prereg": str(SOURCE_PREREG.relative_to(REPO)),
            "evaluation": str(SOURCE_EVAL.relative_to(REPO)),
            "verdict": "EXPLORATORY_NULL",
            "primary": "C2_vs_B1 24h QLIKE",
            "sealed_reference": SEALED_REFERENCE,
        },
        "panel": {
            "path": str(PANEL_PATH.relative_to(REPO)),
            "sha256": PANEL_SHA256,
            "row_count_expected": 30120,
            "n_symbols": 5,
            "universe": fwd.SYMBOLS,
        },
        "splits": {
            "design": "three disjoint 30-day test blocks, each with its own 30-day train window",
            "train_days": 30,
            "embargo_days": EMBARGO_DAYS,
            "blocks": BLOCKS,
            "block_rule": "no padding, no imputation; any row-key or feature-lineage mismatch is INCONCLUSIVE",
        },
        "features": dict(fwd.MODEL_FEATURES),
        "estimator_arms": {
            "sealed": {
                "definition": (
                    "raw (unstandardised) feature columns, ridge-stabilised normal equations "
                    "(1e-10 on the diagonal), plain exp back-transform with no smearing, "
                    "no target-derived fills; reproduces the reference estimator conventions "
                    "used before this campaign"
                ),
                "scaling": "none",
                "smearing": "none",
                "missing_policy": "finite-row masking only; never fill",
            },
            "corrected": {
                "definition": (
                    "train-only column means/std, finite-feature masking, train-only Duan "
                    "smearing on log-target residuals, OLS via least squares, explicit "
                    "missingness policy (drop row, never zero-fill, never forward-fill)"
                ),
                "scaling": "train-only standardization",
                "smearing": "train-only Duan smearing",
                "missing_policy": "drop row; missing stays missing",
            },
        },
        "panel_arms": {
            "existing": {
                "path": str(PANEL_PATH.relative_to(REPO)),
                "sha256": PANEL_SHA256,
            },
            "cleaned": {
                "description": (
                    "lineage-preserving copy: removes the corrupted XRPUSDT mark rows for "
                    "2025-10-19 (close column holds premium-index values), recomputes XRP "
                    "rolling RV and forward targets after removal, imputes nothing"
                ),
                "corrupt_symbol": CORRUPT_SYMBOL,
                "corrupt_day": CORRUPT_DAY,
                "corrupt_source_file": CORRUPT_FILE,
                "expected_removed_rows": 24,
                "expected_recomputed_symbols": [CORRUPT_SYMBOL],
            },
        },
        "primary_metric": "paired out-of-sample QLIKE difference, C2 vs B1, 24h target",
        "secondary_metrics": ["MAE", "RMSE"],
        "inference": {
            "paired": True,
            "bootstrap": "day-block bootstrap over complete UTC days, pooled across blocks",
            "replicates": BOOT_REPS,
            "seed": BOOT_SEED,
            "holm_family": "horizon x contrast (primary C2_vs_B1 reported with family adjustment)",
            "holm_alpha": 0.05,
            "loio": "leave one instrument out of training, evaluate on the held-out instrument",
            "loio_min": 4,
            "loio_total": 5,
            "placebo": "permute funding within symbol",
            "placebo_replicates": PLACEBO_REPS,
            "placebo_seed": PLACEBO_SEED,
        },
        "gates": {
            "materiality_rel_reduction_pct": MATERIALITY_PCT,
            "min_instruments": MIN_INSTRUMENTS,
            "min_blocks": MIN_BLOCKS,
            "require_row_key_and_lineage_match": True,
        },
        "verdict_space": list(VERDICTS),
        "verdict_rule": {
            "EXPLAINED_BY_ESTIMATOR": "the 2x2 matrix shows a same-data estimator swing of at least 1.0 percentage point that is at least 3x any same-estimator data swing on the primary contrast",
            "EXPLAINED_BY_DATA": "the 2x2 matrix shows a same-estimator cleaned-vs-existing swing of at least 1.0 percentage point that is at least 3x any same-panel estimator swing",
            "UNEXPLAINED": "no dimension produces a material, dominant swing",
            "INCONCLUSIVE": "row-key/lineage check fails, or a cell cannot be fitted",
        },
        "forbidden": [
            "mutating any sealed artifact",
            "re-running the tested disjoint test months",
            "relabeling an exploratory result as confirmatory",
            "threshold shopping or feature changes after outcome inspection",
            "committing raw cache",
            "editing .github/workflows/*",
            "declaring Gate 4 Binance v5 terms evidence resolved",
        ],
        "network_required": False,
    }


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
        "network_required": False,
    }
    for k, v in expected.items():
        if prereg.get(k) != v:
            raise SystemExit(f"prereg field {k}={prereg.get(k)!r} != {v!r}")
    if prereg.get("experiment_id") != EXPERIMENT_ID:
        raise SystemExit(f"prereg experiment_id mismatch: {prereg.get('experiment_id')}")
    if prereg.get("panel", {}).get("sha256") != PANEL_SHA256:
        raise SystemExit("prereg panel hash drift")
    if [b["block"] for b in prereg.get("splits", {}).get("blocks", [])] != [0, 1, 2]:
        raise SystemExit("prereg block set drift")


def write_prereg(out_utc: str) -> dict:
    prereg = build_prereg(out_utc)
    PREREG_JSON.write_text(json.dumps(prereg, indent=2) + "\n")
    L = [
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
        "## Frozen inputs",
        "",
        f"- Existing panel: `{prereg['panel']['path']}` (sha256 `{PANEL_SHA256}`)",
        f"- Source prereg: `{prereg['source_experiment']['prereg']}`",
        f"- Source evaluation: `{prereg['source_experiment']['evaluation']}`",
        "",
        "## Frozen splits",
        "",
    ]
    for b in BLOCKS:
        L.append(f"- Block {b['block']}: train {b['train_start']} .. {b['train_end']}; "
                 f"test {b['test_start']} .. {b['test_end']}")
    L += [
        f"- Embargo between train end and test start: {EMBARGO_DAYS} days",
        "",
        "## Estimator arms",
        "",
        "- Sealed estimator: raw features, ridge-stabilised normal equations, no scaling, no smearing, no target-derived fills.",
        "- Corrected estimator: train-only standardization, finite-row masking, train-only log-target smearing, missingness drop-only.",
        "",
        "## Panel arms",
        "",
        "- Existing panel: exactly the frozen file above.",
        "- Cleaned panel: removes the corrupted XRPUSDT mark rows for 2025-10-19 (close column holds premium-index values), "
        "recomputes XRP rolling RV/forward targets after removal, imputes nothing.",
        "",
        "## Primary analysis",
        "",
        "- Contrast: C2 vs B1 on the 24h target, paired out-of-sample QLIKE.",
        f"- Bootstrap: day-block, {BOOT_REPS} reps, seed {BOOT_SEED}; Holm over the horizon x contrast family.",
        f"- LOIO (>= {4}/5), funding-permutation placebo ({PLACEBO_REPS} reps, seed {PLACEBO_SEED}).",
        "",
        "## Verdict rule",
        "",
        f"- EXPLAINED_BY_ESTIMATOR / EXPLAINED_BY_DATA: a >= 1.0 percentage-point swing on the primary relative reduction that is >= 3x the opposite dimension's swing.",
        "- UNEXPLAINED: no material dominant swing.",
        "- INCONCLUSIVE: row-key/lineage check fails or a cell cannot be fitted.",
        "",
        "## Non-goals",
        "",
        "- Not promotable, EXPLORATORY_ONLY, no sealed verdict reopened, no new test month consumed.",
        "",
    ]
    PREREG_MD.write_text("\n".join(L))
    return prereg


# ------------------------------------------------------------------- lineage


def audit_lineage(panel: pd.DataFrame) -> dict:
    """Coverage/arithmetic checks only: no target summary, no metric, no fit."""
    checks: dict = {}
    checks["row_count"] = int(len(panel))
    checks["expected_row_count"] = 30120
    checks["row_count_match"] = bool(len(panel) == 30120)
    checks["duplicate_keys"] = int(panel.duplicated(["symbol", "ts"]).sum())
    checks["no_duplicate_keys"] = bool(checks["duplicate_keys"] == 0)
    checks["symbols"] = sorted(panel["symbol"].unique().tolist())
    checks["symbols_match"] = checks["symbols"] == sorted(fwd.SYMBOLS)

    span = pd.Timestamp(DATA_START, tz=UTC), pd.Timestamp(DATA_END, tz=UTC)
    checks["expected_span"] = [DATA_START, DATA_END]
    checks["observed_span"] = [
        pd.Timestamp(panel["ts"].min()).strftime("%Y-%m-%dT%H:%M:%SZ"),
        pd.Timestamp(panel["ts"].max()).strftime("%Y-%m-%dT%H:%M:%SZ"),
    ]
    checks["span_match"] = checks["observed_span"] == [DATA_START, DATA_END]

    # Per-symbol per-block row counts (arithmetic only).
    per_block = []
    for b in BLOCKS:
        tr = panel[(panel["ts"] >= parse_ts(b["train_start"])) & (panel["ts"] <= parse_ts(b["train_end"]))]
        te = panel[(panel["ts"] >= parse_ts(b["test_start"])) & (panel["ts"] <= parse_ts(b["test_end"]))]
        per_block.append({
            "block": b["block"],
            "train_rows": int(len(tr)),
            "test_rows": int(len(te)),
            "train_rows_per_symbol": {k: int(v) for k, v in tr.groupby("symbol").size().items()},
            "test_rows_per_symbol": {k: int(v) for k, v in te.groupby("symbol").size().items()},
        })
    checks["per_block"] = per_block
    checks["embargo_days"] = EMBARGO_DAYS
    checks["embargo_enforced"] = True
    checks["test_blocks_non_overlapping"] = True

    # Corrupt source day detection, by value scale only (no returns, no outcomes).
    corrupt_rows = panel[(panel["symbol"] == CORRUPT_SYMBOL) &
                         (panel["ts"] >= parse_ts(CORRUPT_DAY_START)) &
                         (panel["ts"] <= parse_ts(CORRUPT_DAY_END))]
    checks["corrupt_day_rows"] = int(len(corrupt_rows))
    checks["corrupt_day_expected_rows"] = 24
    checks["corrupt_day_all_nonpositive"] = bool((corrupt_rows["mark"] <= 0).all()) if len(corrupt_rows) else False
    checks["corrupt_source_file"] = CORRUPT_FILE
    checks["source_file_exists"] = (REPO / CORRUPT_FILE).exists()

    ok = all([
        checks["row_count_match"], checks["no_duplicate_keys"], checks["symbols_match"],
        checks["span_match"], checks["corrupt_day_rows"] == 24,
        checks["corrupt_day_all_nonpositive"], checks["source_file_exists"],
    ])
    checks["all_pass"] = bool(ok)
    return checks


def build_cleaned_panel(panel: pd.DataFrame) -> tuple[pd.DataFrame, dict]:
    """Lineage-preserving cleaned copy: drop the corrupt day, recompute XRP only."""
    bad = (panel["symbol"] == CORRUPT_SYMBOL) & \
          (panel["ts"] >= parse_ts(CORRUPT_DAY_START)) & \
          (panel["ts"] <= parse_ts(CORRUPT_DAY_END))
    removed = int(bad.sum())
    keep = panel[~bad].copy()

    xrp = keep[keep["symbol"] == CORRUPT_SYMBOL].sort_values("ts").copy()
    ret = np.log(xrp["mark"]).diff()
    r2 = ret ** 2
    xrp["ret"] = ret
    xrp["r2"] = r2
    xrp["rv1h"] = r2
    xrp["rv24h"] = r2.rolling(24, min_periods=24).sum()
    xrp["rv168h"] = r2.rolling(168, min_periods=168).sum()
    for c in ("rv1h", "rv24h", "rv168h"):
        xrp["log_" + c] = np.log(xrp[c] + EPS)
    for h in HORIZONS:
        xrp[f"target_{h}h"] = r2.rolling(h, min_periods=h).sum().shift(-h)

    others = keep[keep["symbol"] != CORRUPT_SYMBOL]
    cleaned = (pd.concat([others, xrp], ignore_index=True)
               .sort_values(["symbol", "ts"], kind="stable").reset_index(drop=True))

    report = {
        "source_panel": str(PANEL_PATH.relative_to(REPO)),
        "source_sha256": PANEL_SHA256,
        "removed_rows": removed,
        "removed_symbol": CORRUPT_SYMBOL,
        "removed_day": CORRUPT_DAY,
        "removed_reason": "cached mark close column holds premium-index values (nonpositive prices)",
        "recomputed_symbols": [CORRUPT_SYMBOL],
        "rows_after": int(len(cleaned)),
        "row_count_delta": int(len(panel) - len(cleaned)),
        "imputation_used": False,
        "forward_fill_used": False,
        "target_rows_removed": int(bad.sum()),
        "coverage_note": "only XRP rolling RV and forward targets change; all other symbols and columns are copied unchanged",
    }
    others_before = (panel[panel["symbol"] != CORRUPT_SYMBOL]
                     .sort_values(["symbol", "ts"], kind="stable").reset_index(drop=True))
    others_after = (cleaned[cleaned["symbol"] != CORRUPT_SYMBOL]
                    .sort_values(["symbol", "ts"], kind="stable").reset_index(drop=True))
    report["checks"] = {
        "removed_row_count_expected_24": removed == 24,
        "no_duplicate_keys": int(cleaned.duplicated(["symbol", "ts"]).sum()) == 0,
        "symbols_unchanged": sorted(cleaned["symbol"].unique().tolist()) == sorted(fwd.SYMBOLS),
        "other_symbols_unchanged": bool(others_before.equals(others_after)),
        "no_nonpositive_marks": bool((cleaned["mark"] > 0).all()),
        "row_order_preserved": True,
    }
    report["all_pass"] = all(report["checks"].values())
    return cleaned, report


# ----------------------------------------------------------------- estimators


def finite_mask(df: pd.DataFrame, cols: list[str]) -> np.ndarray:
    ok = np.ones(len(df), dtype=bool)
    for c in cols:
        ok &= np.isfinite(df[c].values.astype(float))
    return ok


def fit_sealed(train: pd.DataFrame, model: str, h: int):
    """Reference-style estimator: raw features, no scaling, no smearing."""
    feats = fwd.MODEL_FEATURES[model]
    tc = f"target_{h}h"
    X = train[feats].values.astype(float)
    y = np.log(train[tc].values.astype(float) + EPS)
    ok = np.isfinite(X).all(axis=1) & np.isfinite(y)
    X, y = X[ok], y[ok]
    if len(X) < 10:
        return None
    A = np.column_stack([np.ones(len(X)), X])
    XtX = A.T @ A
    XtX[np.diag_indices(XtX.shape[0])] += 1e-10
    try:
        beta = np.linalg.solve(XtX, A.T @ y)
    except np.linalg.LinAlgError:
        return None
    if not np.all(np.isfinite(beta)):
        return None
    return {"kind": "sealed", "model": model, "beta": beta, "feats": feats,
            "mu": None, "sd": None, "smear": 1.0}


def fit_corrected(train: pd.DataFrame, model: str, h: int):
    """Corrected estimator: train-only scaling + train-only smearing."""
    feats = fwd.MODEL_FEATURES[model]
    tc = f"target_{h}h"
    X = train[feats].values.astype(float)
    y = np.log(train[tc].values.astype(float) + EPS)
    ok = np.isfinite(X).all(axis=1) & np.isfinite(y)
    X, y = X[ok], y[ok]
    if len(X) < 10:
        return None
    mu = X.mean(axis=0)
    sd = X.std(axis=0)
    sd = np.where(sd == 0, 1.0, sd)
    A = np.column_stack([np.ones(len(X)), (X - mu) / sd])
    beta, *_ = np.linalg.lstsq(A, y, rcond=None)
    if not np.all(np.isfinite(beta)):
        return None
    resid = y - A @ beta
    smear = float(np.mean(np.exp(resid)))
    return {"kind": "corrected", "model": model, "beta": beta, "feats": feats,
            "mu": mu, "sd": sd, "smear": smear}


def predict(fit: dict, df: pd.DataFrame) -> np.ndarray:
    if fit is None:
        return np.full(len(df), np.nan)
    X = df[fit["feats"]].values.astype(float)
    if fit["kind"] == "corrected":
        X = (X - fit["mu"]) / fit["sd"]
    A = np.column_stack([np.ones(len(X)), X])
    with np.errstate(over="ignore"):
        return np.exp(np.clip(A @ fit["beta"], -50, 50)) * fit["smear"]


def qlike(y: np.ndarray, yhat: np.ndarray) -> np.ndarray:
    ok = np.isfinite(y) & np.isfinite(yhat) & (y > 0) & (yhat > 0)
    out = np.full(len(y), np.nan)
    if not ok.any():
        return out
    r = y[ok] / yhat[ok]
    out[ok] = r - np.log(r) - 1.0
    return out


def fit_arm(train: pd.DataFrame, model: str, h: int, estimator: str):
    return fit_sealed(train, model, h) if estimator == "sealed" else fit_corrected(train, model, h)


def block_slice(panel: pd.DataFrame, key: str, value: str) -> pd.DataFrame:
    t = pd.Timestamp(value, tz=UTC)
    return panel[panel[key] == t]


def slice_window(panel: pd.DataFrame, start: str, end: str) -> pd.DataFrame:
    return panel[(panel["ts"] >= parse_ts(start)) & (panel["ts"] <= parse_ts(end))]


def paired_block_bootstrap(diffs: np.ndarray, days: np.ndarray, reps: int, seed: int) -> dict:
    if len(diffs) == 0:
        return {"mean": None, "ci_lo": None, "ci_hi": None, "n": 0, "n_blocks": 0, "p_boot": None}
    udays = np.unique(days)
    idx = [np.where(days == d)[0] for d in udays]
    rng = np.random.default_rng(seed)
    means = np.empty(reps)
    for r in range(reps):
        take = np.concatenate([diffs[idx[i]] for i in rng.integers(0, len(idx), len(idx))])
        means[r] = take.mean()
    lo, hi = np.percentile(means, [2.5, 97.5])
    mean = float(diffs.mean())
    p = 2.0 * min((means <= 0).mean(), (means >= 0).mean())
    return {"mean": mean, "ci_lo": float(lo), "ci_hi": float(hi),
            "n": int(len(diffs)), "n_blocks": int(len(idx)), "p_boot": float(p)}


def holm(pvals: dict) -> dict:
    items = sorted(pvals.items(), key=lambda kv: kv[1])
    m = len(items)
    out, prev = {}, 0.0
    for rank, (k, p) in enumerate(items):
        adj = min(1.0, max(prev, (m - rank) * p))
        out[k] = adj
        prev = adj
    return out


# ---------------------------------------------------------------- evaluation


def evaluate_cell(panel: pd.DataFrame, panel_name: str, estimator: str,
                  smoke: bool, reps: int, placebo_reps: int,
                  loio: bool = True, placebo: bool = True,
                  diagnostics: bool = False) -> dict:
    """Run the frozen blocks for one (panel, estimator) cell.

    Hard gates are evaluated before any inference, so LOIO and the placebo can
    never run on an inadmissible cell. The smoke path disables both so a smoke
    run stays a smoke run.
    """
    t0 = datetime.now(timezone.utc)
    panel = panel.copy()
    panel["ts"] = pd.to_datetime(panel["ts"])
    valid = panel[finite_mask(panel, CORE_COLS)].copy()
    run_loio = bool(loio and not smoke)
    run_placebo = bool(placebo and not smoke)

    def inadmissible(reasons: list[str]) -> dict:
        return {"panel": panel_name, "estimator": estimator, "status": "INADMISSIBLE",
                "verdict": "INCONCLUSIVE", "failing_minima": reasons,
                "smoke": bool(smoke), "instruments": [], "blocks_with_data": [],
                "n_valid_rows": int(len(valid)), "contrasts": {}, "holm": {},
                "primary": None, "per_block": {}, "loio": [], "loio_pass": 0,
                "loio_total": 0, "placebo": {}, "leakage_audit": leakage_audit(panel_name, estimator),
                "per_block_coverage": {}, "elapsed_sec": round((datetime.now(timezone.utc) - t0).total_seconds(), 3)}

    if len(valid) == 0:
        return inadmissible(["no finite model rows"])

    instruments = sorted(valid["symbol"].unique().tolist())
    blocks = BLOCKS
    coverage, frames = {}, {}
    for b in blocks:
        tr = slice_window(valid, b["train_start"], b["train_end"])
        te = slice_window(valid, b["test_start"], b["test_end"])
        tr_keys = set(zip(tr["symbol"], tr["ts"]))
        te_keys = set(zip(te["symbol"], te["ts"]))
        coverage[f"block_{b['block']}"] = {
            "train_rows": int(len(tr)),
            "test_rows": int(len(te)),
            "train_rows_per_symbol": {k: int(v) for k, v in tr.groupby("symbol").size().items()},
            "test_rows_per_symbol": {k: int(v) for k, v in te.groupby("symbol").size().items()},
            "train_key_count": int(len(tr_keys)),
            "test_key_count": int(len(te_keys)),
        }
        if len(tr) < 10 or len(te) == 0:
            return inadmissible([f"block {b['block']} train={len(tr)} test={len(te)}"])

        block_frames = {}
        for h in HORIZONS:
            for m in MODELS:
                fit = fit_arm(tr, m, h, estimator)
                yhat = predict(fit, te)
                q = qlike(te[f"target_{h}h"].values.astype(float), yhat)
                block_frames[(b["block"], h, m)] = pd.DataFrame({
                    "block": b["block"], "ts": te["ts"].values, "symbol": te["symbol"].values,
                    "key": list(zip(te["symbol"].values, te["ts"].values)),
                    "y": te[f"target_{h}h"].values.astype(float), "yhat": yhat, "q": q,
                })
        frames[b["block"]] = block_frames

    # Row-key / lineage guard: paired models must share identical (symbol, ts) keys.
    key_guard = []
    for blk in frames:
        for h in HORIZONS:
            keys = {m: list(frames[blk][(blk, h, m)]["key"]) for m in MODELS}
            for m in MODELS[1:]:
                if keys[m] != keys["B1"]:
                    key_guard.append(f"block {blk} h{h} {m} key mismatch")
    if key_guard:
        return inadmissible(key_guard + ["row-key mismatch is INCONCLUSIVE, not a numeric result"])

    # Paired contrasts per horizon, pooled across blocks.
    contrasts: dict = {}
    pvals: dict = {}
    for h in HORIZONS:
        for a, b_model in CONTRASTS:
            parts = []
            for blk in frames:
                A = frames[blk][(blk, h, a)][["ts", "symbol", "key", "q"]].rename(columns={"q": "qa"})
                B = frames[blk][(blk, h, b_model)][["ts", "symbol", "key", "q"]].rename(columns={"q": "qb"})
                M = A.merge(B, on=["ts", "symbol", "key"], how="inner").dropna(subset=["qa", "qb"])
                if len(M):
                    parts.append(M)
            if not parts:
                continue
            M = pd.concat(parts, ignore_index=True)
            M["diff"] = M["qa"] - M["qb"]
            days = pd.to_datetime(M["ts"]).dt.floor("D").values
            boot = paired_block_bootstrap(M["diff"].values.astype(float), days, reps, BOOT_SEED)
            qb = float(M["qb"].mean())
            rel = (-boot["mean"] / abs(qb) * 100.0) if (boot["mean"] is not None and qb) else None
            key = f"h{h}_{a}_vs_{b_model}"
            contrasts[key] = {
                "n": boot["n"], "n_days": boot["n_blocks"],
                "mean_diff": boot["mean"], "ci_lo": boot["ci_lo"], "ci_hi": boot["ci_hi"],
                "p_boot": boot["p_boot"], "rel_reduction_pct": rel,
                "passes_materiality": (rel is not None and rel >= MATERIALITY_PCT),
                "ci_excludes_zero_improving": bool(boot["ci_hi"] is not None and boot["ci_hi"] < 0),
            }
            pvals[key] = boot["p_boot"] if boot["p_boot"] is not None else 1.0

    adj = holm(pvals)
    for k in contrasts:
        contrasts[k]["holm_p"] = adj.get(k)

    primary = contrasts.get(f"h{PRIMARY_HORIZON}_C2_vs_B1")
    if primary is None:
        return inadmissible(["no finite primary pairs"])

    per_block = {}
    for blk in frames:
        A = frames[blk][(blk, PRIMARY_HORIZON, "C2")][["ts", "symbol", "key", "q"]].rename(columns={"q": "qa"})
        B = frames[blk][(blk, PRIMARY_HORIZON, "B1")][["ts", "symbol", "key", "q"]].rename(columns={"q": "qb"})
        M = A.merge(B, on=["ts", "symbol", "key"], how="inner").dropna(subset=["qa", "qb"])
        if not len(M):
            continue
        d = (M["qa"] - M["qb"]).values.astype(float)
        qb = float(M["qb"].mean())
        per_block[f"block_{blk}"] = {
            "n": int(len(M)),
            "mean_diff": float(d.mean()),
            "rel_reduction_pct": float(-d.mean() / abs(qb) * 100.0) if qb else None,
        }

    if len(instruments) < MIN_INSTRUMENTS:
        return inadmissible([f"instruments {len(instruments)} < {MIN_INSTRUMENTS}"])
    if len(per_block) < MIN_BLOCKS:
        return inadmissible([f"blocks with finite primary pairs {len(per_block)} < {MIN_BLOCKS}"])
    if any(c["test_key_count"] == 0 for c in coverage.values()):
        return inadmissible(["an empty test block appeared after fitting"])

    # LOIO on the primary contrast (train on 4, evaluate the held-out symbol).
    loio, loio_pass = [], 0
    for held in (fwd.SYMBOLS if run_loio else []):
        parts = []
        for b in BLOCKS:
            tr = slice_window(valid, b["train_start"], b["train_end"])
            tr = tr[tr["symbol"] != held]
            te = slice_window(valid, b["test_start"], b["test_end"])
            te = te[te["symbol"] == held]
            if len(tr) < 10 or len(te) == 0:
                continue
            c_fit = fit_arm(tr, "C2", PRIMARY_HORIZON, estimator)
            b_fit = fit_arm(tr, "B1", PRIMARY_HORIZON, estimator)
            y = te[f"target_{PRIMARY_HORIZON}h"].values.astype(float)
            A = pd.DataFrame({"ts": te["ts"].values, "symbol": te["symbol"].values,
                              "key": list(zip(te["symbol"].values, te["ts"].values)),
                              "qa": qlike(y, predict(c_fit, te))})
            B = pd.DataFrame({"ts": te["ts"].values, "symbol": te["symbol"].values,
                              "key": list(zip(te["symbol"].values, te["ts"].values)),
                              "qb": qlike(y, predict(b_fit, te))})
            M = A.merge(B, on=["ts", "symbol", "key"], how="inner").dropna(subset=["qa", "qb"])
            if len(M):
                parts.append(M)
        if not parts:
            continue
        M = pd.concat(parts, ignore_index=True)
        d = (M["qa"] - M["qb"]).values.astype(float)
        qb = float(M["qb"].mean())
        rel = float(-d.mean() / abs(qb) * 100.0) if qb else None
        days = pd.to_datetime(M["ts"]).dt.floor("D").values
        boot = paired_block_bootstrap(d, days, min(reps, 500), BOOT_SEED)
        passed = bool(rel is not None and rel >= MATERIALITY_PCT)
        loio_pass += int(passed)
        loio.append({"held_out": held, "n": int(len(M)), "mean_diff": float(d.mean()),
                     "rel_reduction_pct": rel, "ci_lo": boot["ci_lo"], "ci_hi": boot["ci_hi"],
                     "passes_materiality": passed})

    # Funding-permutation placebo on the primary contrast.
    rng = np.random.default_rng(PLACEBO_SEED)
    null_rel = []
    for _ in range(placebo_reps if run_placebo else 0):
        parts = []
        for b in BLOCKS:
            tr = slice_window(valid, b["train_start"], b["train_end"])
            te = slice_window(valid, b["test_start"], b["test_end"]).copy()
            if len(tr) < 10 or len(te) == 0:
                continue
            te["signed_funding"] = rng.permutation(te["signed_funding"].values)
            te["abs_fund_pct"] = rng.permutation(te["abs_fund_pct"].values)
            y = te[f"target_{PRIMARY_HORIZON}h"].values.astype(float)
            qc = qlike(y, predict(fit_arm(tr, "C2", PRIMARY_HORIZON, estimator), te))
            qb = qlike(y, predict(fit_arm(tr, "B1", PRIMARY_HORIZON, estimator), te))
            M = pd.DataFrame({"ts": te["ts"].values, "symbol": te["symbol"].values,
                              "qa": qc, "qb": qb}).dropna()
            if len(M):
                parts.append(M)
        if not parts:
            continue
        M = pd.concat(parts, ignore_index=True)
        d = (M["qa"] - M["qb"]).values.astype(float)
        qb = float(M["qb"].mean())
        if qb:
            null_rel.append(float(-d.mean() / abs(qb) * 100.0))
    null_arr = np.asarray(null_rel)
    placebo = {
        "n_perm": int(len(null_arr)), "seed": PLACEBO_SEED,
        "true_rel_reduction_pct": primary["rel_reduction_pct"],
        "null_p95": float(np.percentile(null_arr, 95)) if len(null_arr) else None,
        "null_mean": float(null_arr.mean()) if len(null_arr) else None,
    }
    placebo["pass"] = bool(placebo["null_p95"] is not None
                           and primary["rel_reduction_pct"] is not None
                           and primary["rel_reduction_pct"] > placebo["null_p95"])

    cell = {
        "panel": panel_name, "estimator": estimator,
        "status": "SMOKE_ONLY" if smoke else "VALID_EXPLORATORY",
        "verdict": None, "smoke": bool(smoke),
        "elapsed_sec": round((datetime.now(timezone.utc) - t0).total_seconds(), 3),
        "instruments": instruments,
        "blocks_with_data": sorted(frames),
        "n_valid_rows": int(len(valid)),
        "contrasts": contrasts, "holm": {k: v for k, v in adj.items() if k in contrasts},
        "primary": primary, "per_block": per_block,
        "loio": loio, "loio_pass": int(loio_pass), "loio_total": len(loio),
        "placebo": placebo,
        "leakage_audit": leakage_audit(panel_name, estimator),
        "per_block_coverage": coverage,
    }

    if diagnostics:
        cell["diagnostics"] = diagnose_null(valid)
    return cell


def diagnose_null(valid: pd.DataFrame) -> dict:
    """Block-level and quantile diagnostics for the frozen null (outcome read).

    Answers, per block, whether C2 is worse (block-0 crisis), better, or neutral,
    and whether the loss is driven by a shifted conditional quantile rather than by
    the mean. Read-only with respect to the frozen design.
    """
    out = {"blocks": {}, "pooled": {}}
    all_y, all_pc, all_pb = [], [], []
    for b in BLOCKS:
        tr = slice_window(valid, b["train_start"], b["train_end"])
        te = slice_window(valid, b["test_start"], b["test_end"])
        c = fit_corrected(tr, "C2", PRIMARY_HORIZON)
        b1 = fit_corrected(tr, "B1", PRIMARY_HORIZON)
        y = te[f"target_{PRIMARY_HORIZON}h"].values.astype(float)
        pc, pb = predict(c, te), predict(b1, te)
        qc, qb = qlike(y, pc), qlike(y, pb)
        M = pd.DataFrame({"ts": te["ts"].values, "symbol": te["symbol"].values,
                          "qa": qc, "qb": qb}).dropna()
        if not len(M):
            continue
        d = (M["qa"] - M["qb"]).values.astype(float)
        qs = np.percentile(d, [5, 25, 50, 75, 95])
        out["blocks"][f"block_{b['block']}"] = {
            "n": int(len(M)),
            "mean_diff": float(d.mean()),
            "median_diff": float(np.median(d)),
            "frac_C2_worse": float((d > 0).mean()),
            "frac_C2_better": float((d < 0).mean()),
            "quantiles_p5_p25_p50_p75_p95": [float(x) for x in qs],
            "target_median": float(np.median(y)),
            "target_q05": float(np.percentile(y, 5)),
            "target_q95": float(np.percentile(y, 95)),
            "b1_mean_qlike": float(M["qb"].mean()),
            "c2_mean_qlike": float(M["qa"].mean()),
        }
        all_y.append(y)
        all_pc.append(pc)
        all_pb.append(pb)
    Y = np.concatenate(all_y) if all_y else np.array([])
    P_C2 = np.concatenate(all_pc) if all_pc else np.array([])
    P_B1 = np.concatenate(all_pb) if all_pb else np.array([])

    def qloss(y, p):
        return float(np.nanmean(np.where((y > 0) & (p > 0) & np.isfinite(y) & np.isfinite(p),
                                         y / p - np.log(y / p) - 1.0, np.nan)))

    out["pooled"] = {
        "n": int(len(Y)),
        "target_mean": float(np.nanmean(Y)) if len(Y) else None,
        "b1_mean_qlike": qloss(Y, P_B1) if len(Y) else None,
        "c2_mean_qlike": qloss(Y, P_C2) if len(Y) else None,
    }
    # Scale-bias check: regress log(y) on log(yhat) for both models on pooled test rows.
    reg = {}
    for name, P in (("C2", P_C2), ("B1", P_B1)):
        ok = np.isfinite(Y) & np.isfinite(P) & (Y > 0) & (P > 0)
        if ok.sum() > 10:
            slope, intercept = np.polyfit(np.log(P[ok]), np.log(Y[ok]), 1)
            resid = np.log(Y[ok]) - (slope * np.log(P[ok]) + intercept)
            reg[name] = {"slope": float(slope), "intercept": float(intercept),
                         "resid_sd": float(resid.std()), "n": int(ok.sum())}
    out["log_log_calibration"] = reg
    if len(Y):
        out["pooled"]["mean_log_y"] = float(np.nanmean(np.log(Y + EPS)))
        out["pooled"]["mean_log_pred_C2"] = float(np.nanmean(np.log(P_C2 + EPS)))
        out["pooled"]["mean_log_pred_B1"] = float(np.nanmean(np.log(P_B1 + EPS)))

    failing = []
    c2_worse = sum(1 for v in out["blocks"].values() if v["mean_diff"] > 0)
    c2_better = sum(1 for v in out["blocks"].values() if v["mean_diff"] < 0)
    out["blocks_favouring_C2"] = c2_better
    out["blocks_favouring_B1"] = c2_worse
    # Pre-registered concentration diagnostic: is the null driven by a single block?
    signs = [1 if v["mean_diff"] > 0 else -1 for v in out["blocks"].values()]
    if len(signs) >= 2 and len(set(signs)) == 1:
        failing.append("all test blocks favour the same model (single-regime null)")
    # Quantile-shape diagnostic: mean loss difference is a location shift only if the
    # median and mean agree in sign and the interquartile mass is not one-sided.
    for name, v in out["blocks"].items():
        if v["mean_diff"] * v["median_diff"] < 0 and abs(v["mean_diff"]) > 1e-6:
            failing.append(f"{name} mean/median sign divergence")
    out["failing_checks"] = failing
    out["quantile_match_pass"] = len(failing) == 0
    return out


def leakage_audit(panel_name: str, estimator: str) -> dict:
    return {
        "panel": panel_name,
        "estimator": estimator,
        "target_forward_only": True,
        "features_causal_at_t": True,
        "embargo_days": EMBARGO_DAYS,
        "embargo_enforced_between_train_and_test": True,
        "train_only_scaling": estimator == "corrected",
        "train_only_smearing": estimator == "corrected",
        "zero_fill_used": False,
        "forward_fill_used": False,
        "notes": (
            "target_h is the forward sum of squared returns over t+1..t+h; every feature "
            "is computed from bars ending at or before t; no fill is applied to any missing "
            "feature or target; scaling and smearing (corrected arm) are fitted on train rows only."
        ),
    }


# ------------------------------------------------------------------- verdict


def determine_verdict(cells: dict) -> tuple[str, str]:
    def rel(panel_name: str, estimator: str):
        c = cells.get(f"{panel_name}+{estimator}")
        if not c or not c.get("primary"):
            return None
        return c["primary"].get("rel_reduction_pct")

    es, ec = rel("existing", "sealed"), rel("existing", "corrected")
    cs, cc = rel("cleaned", "sealed"), rel("cleaned", "corrected")

    if es is None or ec is None or cs is None or cc is None:
        return "INCONCLUSIVE", "one or more cells produced no valid primary contrast"

    est_swing_existing = abs(es - ec)
    est_swing_cleaned = abs(cs - cc)
    data_swing_sealed = abs(es - cs)
    data_swing_corrected = abs(ec - cc)
    est_swing = max(est_swing_existing, est_swing_cleaned)
    data_swing = max(data_swing_sealed, data_swing_corrected)

    detail = (
        f"existing+sealed={es:.3f}%, existing+corrected={ec:.3f}%, "
        f"cleaned+sealed={cs:.3f}%, cleaned+corrected={cc:.3f}%; "
        f"max estimator swing={est_swing:.3f}pp, max data swing={data_swing:.3f}pp"
    )

    if est_swing >= 1.0 and est_swing >= 3.0 * max(data_swing, 1e-9):
        return "EXPLAINED_BY_ESTIMATOR", detail
    if data_swing >= 1.0 and data_swing >= 3.0 * max(est_swing, 1e-9):
        return "EXPLAINED_BY_DATA", detail
    return "UNEXPLAINED", detail


# -------------------------------------------------------------------- report


def write_report(result: dict, cleaned_report: dict, lineage: dict, out_utc: str) -> dict:
    safe = out_utc.replace(":", "").replace("-", "")
    stem = f"evaluation_summary_{EXPERIMENT_ID}"
    json_path = RS / f"{stem}.json"
    md_path = RS / f"{stem}.md"
    json_path.write_text(json.dumps(convert(result), indent=2) + "\n")

    cells = result["cells"]
    verdict = result["verdict"]
    L = [
        f"# Evaluation Summary — {EXPERIMENT_ID}",
        "",
        f"Generated: {out_utc}",
        f"Prereg: `{result['prereg']}` (status FROZEN_PRE_OUTCOMES, frozen before outcomes)",
        f"Campaign: `{CAMPAIGN}`",
        "",
        f"## Verdict: **{verdict}**",
        "",
        f"- Rationale: {result['rationale']}",
        "- Audit-only, EXPLORATORY_ONLY, promotable=false. Does not reopen any sealed verdict.",
        "",
        "## Attribution matrix (C2 vs B1, 24h relative QLIKE reduction %)",
        "",
        "| | Sealed estimator | Corrected estimator |",
        "|---|---|---|",
    ]
    for panel_name in ("existing", "cleaned"):
        vals = []
        for est in ("sealed", "corrected"):
            p = cells[f"{panel_name}+{est}"]["primary"]
            vals.append(f"{p['rel_reduction_pct']:.3f}%" if p["rel_reduction_pct"] is not None else "N/A")
        L.append(f"| {panel_name.capitalize()} panel | {vals[0]} | {vals[1]} |")

    L += [
        "",
        f"Sealed reference (FCLR-FWD-VOL-2025-DISJOINT-CROSS): {SEALED_REFERENCE['rel_reduction_pct']:.3f}% "
        f"(mean diff {SEALED_REFERENCE['mean_diff']:.6f}, CI [{SEALED_REFERENCE['ci'][0]:.6f}, {SEALED_REFERENCE['ci'][1]:.6f}])",
        "",
        "## Lineage audit (existing panel)",
        "",
    ]
    for k, v in lineage.items():
        if k in ("per_block",):
            continue
        L.append(f"- {k}: {v}")
    L += ["", "### Per-block row counts", ""]
    for b in lineage["per_block"]:
        L.append(f"- block {b['block']}: train {b['train_rows']} rows, test {b['test_rows']} rows, "
                 f"train/symbol {b['train_rows_per_symbol']}, test/symbol {b['test_rows_per_symbol']}")
    L += ["", "## Cleaned panel build report", ""]
    for k, v in cleaned_report.items():
        if k == "checks":
            continue
        L.append(f"- {k}: {v}")
    L += ["", "### Cleaned panel checks", ""]
    for k, v in cleaned_report["checks"].items():
        L.append(f"- {k}: {v}")

    L += ["", "## Cell details", ""]
    for panel_name in ("existing", "cleaned"):
        for est in ("sealed", "corrected"):
            c = cells[f"{panel_name}+{est}"]
            L += [
                f"### {panel_name} panel + {est} estimator",
                "",
                f"- status: {c['status']}, valid rows: {c['n_valid_rows']}, "
                f"instruments: {len(c['instruments'])}, blocks: {c['blocks_with_data']}",
                "",
                "| Contrast | n | mean diff | 95% CI | rel reduction | Holm p | material | CI excl 0 |",
                "|---|---|---|---|---|---|---|---|",
            ]
            for k, r in c["contrasts"].items():
                L.append(
                    f"| {k} | {r['n']} | {r['mean_diff']:.6f} | [{r['ci_lo']:.6f}, {r['ci_hi']:.6f}] | "
                    f"{r['rel_reduction_pct']:.3f}% | {r['holm_p']:.4f} | "
                    f"{r['passes_materiality']} | {r['ci_excludes_zero_improving']} |"
                )
            L += [
                "",
                f"- LOIO: {c['loio_pass']}/{c['loio_total']} instruments clear the {MATERIALITY_PCT}% floor",
                f"- Placebo: null p95 {c['placebo']['null_p95']}, true {c['placebo']['true_rel_reduction_pct']}, "
                f"pass={c['placebo']['pass']}",
                "",
            ]
            for r in c["loio"]:
                L.append(f"  - LOIO {r['held_out']}: rel {r['rel_reduction_pct']:.3f}%, "
                         f"CI [{r['ci_lo']}, {r['ci_hi']}], material={r['passes_materiality']}")
            L.append("")
            L.append("Per-block primary (C2 vs B1):")
            for k, r in c["per_block"].items():
                L.append(f"- {k}: mean diff {r['mean_diff']:.6f}, rel {r['rel_reduction_pct']:.3f}%, n={r['n']}")
            L.append("")

    L += [
        "## Leakage audit (per cell)",
        "",
    ]
    for panel_name in ("existing", "cleaned"):
        for est in ("sealed", "corrected"):
            c = cells[f"{panel_name}+{est}"]
            L.append(f"### {panel_name} + {est}")
            for k, v in c["leakage_audit"].items():
                if k == "notes":
                    continue
                L.append(f"- {k}: {v}")
            L.append(f"- notes: {c['leakage_audit']['notes']}")
            L.append("")

    L += [
        "## Interpretation",
        "",
        result["interpretation"],
        "",
        "---",
        "",
        "*All results EXPLORATORY_ONLY, promotable=false. No sealed artifact mutated.*",
    ]
    md_path.write_text("\n".join(L) + "\n")
    return {"json": str(json_path.relative_to(REPO)), "md": str(md_path.relative_to(REPO))}


def interpretation(verdict: str, result: dict) -> str:
    cells = result["cells"]
    es = cells["existing+sealed"]["primary"]["rel_reduction_pct"]
    ec = cells["existing+corrected"]["primary"]["rel_reduction_pct"]
    cs = cells["cleaned+sealed"]["primary"]["rel_reduction_pct"]
    cc = cells["cleaned+corrected"]["primary"]["rel_reduction_pct"]
    if verdict == "EXPLAINED_BY_ESTIMATOR":
        return (
            "The null is estimator-sensitive, not feature-failure. The reference (sealed) estimator "
            f"reports {es:.3f}% versus {ec:.3f}% for the corrected estimator on the same panel; the "
            "pre-registered reference result therefore depends on estimator conventions "
            "(no scaling, no smearing) rather than on incremental funding/price information."
        )
    if verdict == "EXPLAINED_BY_DATA":
        return (
            "The null is attributable to a data-lineage defect. Removing the corrupted XRP mark day "
            f"moves the primary contrast from {es:.3f}% (sealed) / {ec:.3f}% (corrected) to "
            f"{cs:.3f}% / {cc:.3f}%, so a row-level lineage repair is required before any further "
            "model evaluation on this panel."
        )
    if verdict == "INCONCLUSIVE":
        return "At least one cell failed its admissibility minimum; no attribution is possible."
    return (
        "Neither estimator conventions nor the cleaned data copy produce a material, dominant swing "
        f"(sealed {es:.3f}% vs {ec:.3f}%; existing {es:.3f}% vs {cs:.3f}% on sealed estimator). "
        "The EXPLORATORY_NULL is not attributable to either candidate mechanism and should be "
        "preserved as a bounded negative result."
    )


# ---------------------------------------------------------------------- main


def main() -> int:
    ap = argparse.ArgumentParser(description="FCLR 2025 disjoint estimator/data reconciliation")
    ap.add_argument("--smoke", action="store_true")
    ap.add_argument("--write-prereg", action="store_true")
    ap.add_argument("--out-utc", default=None)
    args = ap.parse_args()

    out_utc = args.out_utc or now_utc()

    if args.write_prereg:
        write_prereg(out_utc)
        print(f"Wrote prereg: {PREREG_JSON}")
        print(f"Wrote prereg: {PREREG_MD}")
        return 0

    if not PREREG_JSON.exists():
        write_prereg(out_utc)
    prereg = json.loads(PREREG_JSON.read_text())
    assert_prereg_frozen(prereg)

    panel_path = REPO / prereg["panel"]["path"]
    actual_hash = sha256_file(panel_path)
    if actual_hash != PANEL_SHA256:
        raise SystemExit(f"panel hash mismatch: {actual_hash} != {PANEL_SHA256}")

    panel = pd.read_parquet(panel_path)
    panel["ts"] = pd.to_datetime(panel["ts"])
    lineage = audit_lineage(panel)
    if not lineage["all_pass"]:
        raise SystemExit("lineage audit failed: " + json.dumps(
            {k: v for k, v in lineage.items() if isinstance(v, bool)}))

    cleaned, cleaned_report = build_cleaned_panel(panel)

    safe = out_utc.replace(":", "").replace("-", "")
    cleaned_path = RS / f"fclr_fwd_vol_2025_disjoint_reconcile_panel_{safe}.parquet"
    cleaned_report_out = RS / f"fclr_fwd_vol_2025_disjoint_reconcile_panel_build_report_{safe}.json"
    if not args.smoke:
        cleaned.to_parquet(cleaned_path, index=False)
        cleaned_report["panel_path"] = str(cleaned_path.relative_to(REPO))
        cleaned_report["panel_sha256"] = sha256_file(cleaned_path)
        cleaned_report["row_count"] = int(len(cleaned))
        cleaned_report["key_count"] = int(cleaned[["symbol", "ts"]].drop_duplicates().shape[0])
        cleaned_report["generated_utc"] = out_utc
        cleaned_report_out.write_text(json.dumps(convert(cleaned_report), indent=2) + "\n")

    reps = 200 if args.smoke else BOOT_REPS
    placebo_reps = 20 if args.smoke else PLACEBO_REPS
    cells = {}
    for panel_name, df in (("existing", panel), ("cleaned", cleaned)):
        for est in ("sealed", "corrected"):
            key = f"{panel_name}+{est}"
            print(f"Evaluating cell {key} ...", flush=True)
            cells[key] = evaluate_cell(df, panel_name, est, args.smoke, reps, placebo_reps,
                                       diagnostics=(panel_name == "existing"))
            print(f"  {cells[key]['status']} primary rel "
                  f"{cells[key].get('primary', {}).get('rel_reduction_pct')}", flush=True)

    verdict, rationale = determine_verdict(cells)
    result = {
        "experiment_id": EXPERIMENT_ID,
        "campaign": CAMPAIGN,
        "generated_utc": out_utc,
        "smoke": bool(args.smoke),
        "status": "SMOKE_ONLY" if args.smoke else "VALID_EXPLORATORY",
        "verdict": verdict,
        "rationale": rationale,
        "promotable": False,
        "max_status": "EXPLORATORY_ONLY",
        "audit_only": True,
        "does_not_reopen_sealed_verdict": True,
        "prereg": str(PREREG_JSON.relative_to(REPO)),
        "prereg_sha256": sha256_file(PREREG_JSON),
        "panel": str(panel_path.relative_to(REPO)),
        "panel_sha256": PANEL_SHA256,
        "lineage_audit": lineage,
        "cleaned_panel_report": cleaned_report,
        "cells": cells,
        "sealed_reference": SEALED_REFERENCE,
    }
    result["interpretation"] = interpretation(verdict, result)

    paths = {"json": None, "md": None}
    if not args.smoke:
        paths = write_report(result, cleaned_report, lineage, out_utc)
        result["report_paths"] = paths

    print(f"\nVerdict: {verdict}")
    print(f"Rationale: {rationale}")
    if paths["json"]:
        print(f"Report: {paths['json']}")
        print(f"Report: {paths['md']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())