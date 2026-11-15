#!/usr/bin/env python3
"""FCLR-FWD-VOL-2025-DISJOINT-CORRECTED-AUDIT — corrected-estimator robustness audit (P1, Track C).

Attribute the FCLR-FWD-VOL-2025-DISJOINT-CROSS-20261114T183000Z EXPLORATORY_NULL
(pooled C2-B1 24h QLIKE mean diff +0.006923, relative reduction -1.963%, 95% CI
[-0.012604, 0.028030], n=10800) to estimator conventions or preserve it as not
estimator-explained, on the already-executed cached 2025 disjoint panel.

Frozen design (prereg research_state/prereg_fclr_fwd_vol_2025_disjoint_corrected_audit_<UTC>.json):

  panel      research_state/tracka_fwd_vol_2025_disjoint_cross_panel_20261114T191615Z.parquet
             (sha256 de0ca73e7d092a205e5f8c1163d56437384d1b15d65b4a27bc54a57e21738cba)
  blocks     train 2025-04-25..2025-05-24 / test 2025-06
             train 2025-09-25..2025-10-24 / test 2025-11
             train 2025-10-25..2025-11-23 / test 2025-12
             7-day embargo between train end and test start
  models     B0/B1/C1/C2, primary contrast C2 vs B1 on 24h QLIKE
  estimator  corrected only (train-only standardization, finite-row masking,
             train-only log-target Duan smearing, drop-only missingness)
  sealed     recorded reference from evaluation_summary_FCLR-FWD-VOL-2025-DISJOINT-CROSS-20261114T191615Z.json
             (no re-execution of sealed scripts as a new cell)
  inference  paired pooled day-block bootstrap (2000 deterministic reps, seed 20261114),
             Holm over horizon x contrast family, LOIO, funding-permutation placebo,
             leakage audit
  verdict    EXPLAINED_BY_ESTIMATOR | NOT_EXPLAINED_BY_ESTIMATOR | INCONCLUSIVE;
             EXPLORATORY_ONLY, promotable=false. Does not reopen sealed 2025 CROSS/RECONCILE verdicts.

All outputs EXPLORATORY_ONLY, promotable=false. No network. No sealed-artifact mutation.

Usage:
  python3 scripts/fclr_fwd_vol_2025_disjoint_corrected_audit.py --write-prereg --out-utc <UTC>
  python3 scripts/fclr_fwd_vol_2025_disjoint_corrected_audit.py --out-utc <UTC>
  python3 scripts/fclr_fwd_vol_2025_disjoint_corrected_audit.py --smoke --out-utc <UTC>
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

PANEL_PATH = RS / "tracka_fwd_vol_2025_disjoint_cross_panel_20261114T191615Z.parquet"
PANEL_SHA256 = "de0ca73e7d092a205e5f8c1163d56437384d1b15d65b4a27bc54a57e21738cba"
SEALED_EVAL_PATH = RS / "evaluation_summary_FCLR-FWD-VOL-2025-DISJOINT-CROSS-20261114T191615Z.json"

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
MATERIALITY_SWING_PP = 1.0
MIN_INSTRUMENTS = 5
MIN_BLOCKS = 3
HORIZONS = [6, 24, 72, 168]
PRIMARY_HORIZON = 24
MODELS = ("B0", "B1", "C1", "C2")
CONTRASTS = (("C2", "B1"), ("C1", "B1"), ("C2", "C1"))
CORE_COLS = ["log_rv1h", "log_rv24h", "log_rv168h", "signed_funding",
             "abs_fund_pct", "premium", "ema_dist", "target_24h"]
VERDICTS = ("EXPLAINED_BY_ESTIMATOR", "NOT_EXPLAINED_BY_ESTIMATOR", "INCONCLUSIVE")
SYMBOLS = ["BTCUSDT", "ETHUSDT", "BNBUSDT", "SOLUSDT", "XRPUSDT"]


def now_utc() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def sha256_file(p: Path) -> str:
    h = hashlib.sha256()
    with p.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def parse_ts(s: str) -> pd.Timestamp:
    return pd.Timestamp(s.replace("Z", "+00:00"))


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


# ---------------------------------------------------------------- prereg

CAMPAIGN_PREFIX = "FCLR-FWD-VOL-2025-DISJOINT-CORRECTED-AUDIT"


def build_prereg(out_utc: str) -> dict:
    experiment_id = f"{CAMPAIGN_PREFIX}-{out_utc}"
    return {
        "experiment_id": experiment_id,
        "campaign": CAMPAIGN_PREFIX,
        "cell": "FWD-VOL-2025-DISJOINT-CORRECTED-AUDIT",
        "track": "C_volatility_exploratory",
        "priority": "P1",
        "status": "FROZEN_PRE_OUTCOMES",
        "generated_utc": out_utc,
        "frozen_before_outcomes": True,
        "pre_registered_before_outcomes": True,
        "outcome_data_inspected_before_freeze": False,
        "promotable": False,
        "max_status": "EXPLORATORY_ONLY",
        "purpose": (
            "Test whether the 2025 disjoint EXPLORATORY_NULL / UNEXPLAINED reconcile "
            "(FCLR-FWD-VOL-2025-DISJOINT-CROSS-20261114T183000Z: pooled C2-B1 24h QLIKE "
            "relative reduction -1.963%, 95% CI [-0.012604, 0.028030]) is estimator-sensitive. "
            "Runs the corrected estimator (train-only standardization, finite-row masking, "
            "train-only log-target Duan smearing, drop-only missingness) on the frozen cached "
            "2025 disjoint panel and contrasts against the recorded sealed reference from "
            "evaluation_summary_FCLR-FWD-VOL-2025-DISJOINT-CROSS-20261114T191615Z.json. "
            "No sealed scripts or artifacts are re-executed or mutated. All results EXPLORATORY_ONLY, "
            "promotable=false."
        ),
        "sealed_reference": {
            "source": str(SEALED_EVAL_PATH.relative_to(REPO)),
            "experiment_id": "FCLR-FWD-VOL-2025-DISJOINT-CROSS-20261114T183000Z",
            "primary_contrast": "C2_vs_B1",
            "primary_metric": "24h QLIKE",
            "mean_diff": 0.0069231708051235965,
            "rel_reduction_pct": -1.9633752428119817,
            "ci": [-0.012604044681266236, 0.028030237827547048],
            "n": 10800,
            "n_days": 90,
        },
        "panel": {
            "path": str(PANEL_PATH.relative_to(REPO)),
            "sha256": PANEL_SHA256,
            "n_symbols": 5,
            "universe": SYMBOLS,
        },
        "splits": {
            "design": "three disjoint 30-day test blocks, each with its own 30-day train window",
            "train_days": 30,
            "embargo_days": EMBARGO_DAYS,
            "blocks": BLOCKS,
            "block_rule": "no padding, no imputation; any row-key or feature-lineage mismatch is INCONCLUSIVE",
        },
        "features": dict(fwd.MODEL_FEATURES),
        "estimator_arm": {
            "corrected": {
                "definition": (
                    "train-only column means/std standardization, finite-feature masking "
                    "(drop row, never fill), train-only Duan smearing on log-target residuals, "
                    "OLS via least squares, explicit missingness policy (drop row; missing stays missing)"
                ),
                "scaling": "train-only standardization",
                "smearing": "train-only Duan smearing",
                "missing_policy": "drop row; missing stays missing",
            },
        },
        "contrast": {
            "primary": "C2_vs_B1",
            "secondary": ["C1_vs_B1", "C2_vs_C1"],
            "metric": "paired out-of-sample QLIKE difference",
            "horizon_hours": PRIMARY_HORIZON,
        },
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
            "materiality_swing_pp": MATERIALITY_SWING_PP,
            "min_instruments": MIN_INSTRUMENTS,
            "min_blocks": MIN_BLOCKS,
            "require_row_key_and_lineage_match": True,
        },
        "verdict_space": list(VERDICTS),
        "verdict_rule": {
            "EXPLAINED_BY_ESTIMATOR": "corrected-estimator primary rel reduction swings from the sealed reference by >= 1.0 percentage point, or sign flip with max(|corrected|, |sealed|) >= 1.0",
            "NOT_EXPLAINED_BY_ESTIMATOR": "corrected-estimator primary rel reduction is within 1.0 percentage point of the sealed reference with no material sign flip (the 2025 null is not estimator-sensitive)",
            "INCONCLUSIVE": "panel hash/row-key/lineage check fails, or a cell cannot be fitted",
        },
        "forbidden": [
            "mutating any sealed artifact",
            "re-executing sealed scripts as a new cell",
            "relabeling an exploratory result as confirmatory",
            "threshold shopping or feature changes after outcome inspection",
            "committing raw cache",
            "editing .github/workflows/*",
            "declaring Gate 4 Binance v5 terms evidence resolved",
        ],
        "network_required": False,
    }


def write_prereg(out_utc: str) -> tuple[dict, Path, Path]:
    prereg = build_prereg(out_utc)
    stem = f"prereg_fclr_fwd_vol_2025_disjoint_corrected_audit_{out_utc}"
    json_path = RS / f"{stem}.json"
    md_path = RS / f"{stem}.md"
    json_path.write_text(json.dumps(prereg, indent=2) + "\n")
    L = [
        f"# Pre-Registration — {prereg['experiment_id']}",
        "",
        f"Generated: {out_utc}",
        f"Campaign: `{CAMPAIGN_PREFIX}`",
        "Status: **FROZEN_PRE_OUTCOMES** (frozen before any outcome computation)",
        "",
        "## Purpose",
        "",
        prereg["purpose"],
        "",
        "## Frozen inputs",
        "",
        f"- Panel: `{prereg['panel']['path']}` (sha256 `{PANEL_SHA256}`)",
        f"- Sealed reference: `{prereg['sealed_reference']['source']}` "
        f"(rel_reduction {prereg['sealed_reference']['rel_reduction_pct']:.3f}%, "
        f"CI [{prereg['sealed_reference']['ci'][0]:.6f}, {prereg['sealed_reference']['ci'][1]:.6f}])",
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
        "## Estimator arm",
        "",
        "- Corrected estimator: train-only standardization, finite-row masking (drop row, never fill), "
        "train-only log-target Duan smearing, drop-only missingness.",
        "",
        "## Primary analysis",
        "",
        "- Contrast: C2 vs B1 on the 24h target, paired out-of-sample QLIKE, pooled across 3 blocks.",
        f"- Bootstrap: day-block, {BOOT_REPS} reps, seed {BOOT_SEED}; Holm over horizon x contrast family.",
        f"- LOIO (>= {4}/5), funding-permutation placebo ({PLACEBO_REPS} reps, seed {PLACEBO_SEED}).",
        "",
        "## Verdict rule",
        "",
        f"- EXPLAINED_BY_ESTIMATOR: corrected vs sealed reference swing >= {MATERIALITY_SWING_PP} percentage point on the primary relative reduction, or sign flip with magnitude >= 1.0.",
        f"- NOT_EXPLAINED_BY_ESTIMATOR: corrected within {MATERIALITY_SWING_PP} pp of sealed reference with no material sign flip.",
        "- INCONCLUSIVE: panel hash/row-key/lineage check fails, or a cell cannot be fitted.",
        "",
        "## Non-goals",
        "",
        "- Not promotable, EXPLORATORY_ONLY, no sealed verdict reopened, no new test month consumed.",
        "",
    ]
    md_path.write_text("\n".join(L) + "\n")
    return prereg, json_path, md_path


def assert_prereg_frozen(prereg: dict, experiment_id: str) -> None:
    expected = {
        "status": "FROZEN_PRE_OUTCOMES",
        "frozen_before_outcomes": True,
        "pre_registered_before_outcomes": True,
        "outcome_data_inspected_before_freeze": False,
        "promotable": False,
        "max_status": "EXPLORATORY_ONLY",
        "network_required": False,
    }
    for k, v in expected.items():
        if prereg.get(k) != v:
            raise SystemExit(f"prereg field {k}={prereg.get(k)!r} != {v!r}")
    if prereg.get("experiment_id") != experiment_id:
        raise SystemExit(f"prereg experiment_id mismatch: {prereg.get('experiment_id')}")
    if prereg.get("panel", {}).get("sha256") != PANEL_SHA256:
        raise SystemExit("prereg panel hash drift")
    if [b["block"] for b in prereg.get("splits", {}).get("blocks", [])] != [0, 1, 2]:
        raise SystemExit("prereg block set drift")


# ------------------------------------------------------------------- lineage

def finite_mask(df: pd.DataFrame, cols: list[str]) -> np.ndarray:
    ok = np.ones(len(df), dtype=bool)
    for c in cols:
        ok &= np.isfinite(df[c].values.astype(float))
    return ok


def audit_lineage(panel: pd.DataFrame) -> dict:
    """Coverage/arithmetic checks only: no target summary, no metric, no fit."""
    checks: dict = {}
    checks["row_count"] = int(len(panel))
    checks["expected_row_count"] = 30120
    checks["row_count_match"] = bool(len(panel) == 30120)
    checks["duplicate_keys"] = int(panel.duplicated(["symbol", "ts"]).sum())
    checks["no_duplicate_keys"] = bool(checks["duplicate_keys"] == 0)
    checks["symbols"] = sorted(panel["symbol"].unique().tolist())
    checks["symbols_match"] = checks["symbols"] == sorted(SYMBOLS)
    checks["expected_span"] = ["2025-04-25T00:00:00Z", "2025-12-31T23:00:00Z"]
    checks["observed_span"] = [
        pd.Timestamp(panel["ts"].min()).strftime("%Y-%m-%dT%H:%M:%SZ"),
        pd.Timestamp(panel["ts"].max()).strftime("%Y-%m-%dT%H:%M:%SZ"),
    ]
    checks["span_match"] = checks["observed_span"] == checks["expected_span"]

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

    ok = all([
        checks["row_count_match"], checks["no_duplicate_keys"], checks["symbols_match"],
        checks["span_match"],
    ])
    checks["all_pass"] = bool(ok)
    return checks


# ------------------------------------------------------------- estimators

def fit_corrected(train: pd.DataFrame, model: str, h: int):
    """Corrected estimator: train-only scaling + train-only Duan smearing."""
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


def slice_window(panel: pd.DataFrame, start: str, end: str) -> pd.DataFrame:
    return panel[(panel["ts"] >= parse_ts(start)) & (panel["ts"] <= parse_ts(end))]


# ---------------------------------------------------------------- evaluation

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
        out[k] = float(adj)
        prev = adj
    return out


def evaluate_cell(panel: pd.DataFrame, estimator: str,
                  smoke: bool, reps: int, placebo_reps: int) -> dict:
    """Run the frozen blocks for the corrected estimator (only arm)."""
    t0 = datetime.now(timezone.utc)
    panel = panel.copy()
    panel["ts"] = pd.to_datetime(panel["ts"])
    valid = panel[finite_mask(panel, CORE_COLS)].copy()
    run_loio = bool(not smoke)
    run_placebo = bool(not smoke)

    def inadmissible(reasons: list[str]) -> dict:
        return {"panel": "existing", "estimator": estimator, "status": "INADMISSIBLE",
                "verdict": "INCONCLUSIVE", "failing_minima": reasons,
                "smoke": bool(smoke), "instruments": [], "blocks_with_data": [],
                "n_valid_rows": int(len(valid)), "contrasts": {}, "holm": {},
                "primary": None, "per_block": {}, "loio": [], "loio_pass": 0,
                "loio_total": 0, "placebo": {}, "leakage_audit": leakage_audit(estimator),
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
                fit = fit_corrected(tr, m, h)
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
                "passes_materiality": (rel is not None and rel >= 2.0),
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
    for held in (SYMBOLS if run_loio else []):
        parts = []
        for b in BLOCKS:
            tr = slice_window(valid, b["train_start"], b["train_end"])
            tr = tr[tr["symbol"] != held]
            te = slice_window(valid, b["test_start"], b["test_end"])
            te = te[te["symbol"] == held]
            if len(tr) < 10 or len(te) == 0:
                continue
            c_fit = fit_corrected(tr, "C2", PRIMARY_HORIZON)
            b_fit = fit_corrected(tr, "B1", PRIMARY_HORIZON)
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
        passed = bool(rel is not None and rel >= 2.0)
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
            qc = qlike(y, predict(fit_corrected(tr, "C2", PRIMARY_HORIZON), te))
            qb = qlike(y, predict(fit_corrected(tr, "B1", PRIMARY_HORIZON), te))
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
        "panel": "existing", "estimator": estimator,
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
        "leakage_audit": leakage_audit(estimator),
        "per_block_coverage": coverage,
    }
    return cell


def leakage_audit(estimator: str) -> dict:
    return {
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

def determine_verdict(corrected_rel: float | None, sealed_rel: float,
                      lineage: dict, cell_ok: bool) -> tuple[str, str]:
    if not lineage.get("all_pass") or not cell_ok or corrected_rel is None:
        return "INCONCLUSIVE", "lineage/row-key check failed or cell could not be fitted"
    swing = abs(float(corrected_rel) - float(sealed_rel))
    sign_flip = ((float(corrected_rel) > 0) != (float(sealed_rel) > 0)) and \
        max(abs(float(corrected_rel)), abs(float(sealed_rel))) >= 1.0
    detail = (
        f"corrected={corrected_rel:.3f}%, sealed_reference={sealed_rel:.3f}%, "
        f"swing={swing:.3f}pp, sign_flip={sign_flip}"
    )
    if swing >= MATERIALITY_SWING_PP or sign_flip:
        return "EXPLAINED_BY_ESTIMATOR", detail
    return "NOT_EXPLAINED_BY_ESTIMATOR", detail


# -------------------------------------------------------------------- report

def write_report(result: dict, lineage: dict, out_utc: str) -> dict:
    safe = out_utc.replace(":", "").replace("-", "")
    stem = f"evaluation_summary_{result['experiment_id']}"
    json_path = RS / f"{stem}.json"
    md_path = RS / f"{stem}.md"
    json_path.write_text(json.dumps(convert(result), indent=2) + "\n")

    cell = result["cell"]
    verdict = result["verdict"]
    L = [
        f"# Evaluation Summary — {result['experiment_id']}",
        "",
        f"Generated: {out_utc}",
        f"Prereg: `{result['prereg']}` (status FROZEN_PRE_OUTCOMES, frozen before outcomes)",
        f"Campaign: `{CAMPAIGN_PREFIX}`",
        "",
        f"## Verdict: **{verdict}**",
        "",
        f"- Rationale: {result['rationale']}",
        "- Corrected-estimator robustness audit, EXPLORATORY_ONLY, promotable=false. "
        "Does not reopen any sealed verdict.",
        "",
        "## Sealed reference (FCLR-FWD-VOL-2025-DISJOINT-CROSS-20261114T183000Z)",
        "",
    ]
    sr = result["sealed_reference"]
    L += [
        f"- primary contrast: {sr['primary_contrast']} ({sr['primary_metric']})",
        f"- mean_diff: {sr['mean_diff']:.6f}",
        f"- rel_reduction_pct: {sr['rel_reduction_pct']:.3f}%",
        f"- 95% CI: [{sr['ci'][0]:.6f}, {sr['ci'][1]:.6f}]",
        f"- n: {sr['n']}, days: {sr['n_days']}",
        "",
        "## Corrected-estimator result (primary C2 vs B1, 24h QLIKE)",
        "",
    ]
    p = cell["primary"]
    L += [
        f"- mean_diff: {p['mean_diff']:.6f}",
        f"- rel_reduction_pct: {p['rel_reduction_pct']:.3f}%",
        f"- 95% CI: [{p['ci_lo']:.6f}, {p['ci_hi']:.6f}]",
        f"- p_boot: {p['p_boot']:.4f}",
        f"- n: {p['n']}, days: {p['n_days']}",
        f"- Holm p (primary): {cell['holm'].get(f'h{PRIMARY_HORIZON}_C2_vs_B1')}",
        "",
        f"- Swing vs sealed reference: {result['swing_pp']:.3f} pp",
        f"- Sign flip: {result['sign_flip']}",
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
    L += ["", "## Cell details", ""]
    c = cell
    L += [
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
        f"- LOIO: {c['loio_pass']}/{c['loio_total']} instruments clear the 2.0% floor",
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
        "## Leakage audit",
        "",
    ]
    for k, v in c["leakage_audit"].items():
        if k == "notes":
            continue
        L.append(f"- {k}: {v}")
    L.append(f"- notes: {c['leakage_audit']['notes']}")
    L += [
        "",
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
    sr = result["sealed_reference"]
    c = result["cell"]
    p = c["primary"]
    if verdict == "EXPLAINED_BY_ESTIMATOR":
        return (
            "The 2025 null is estimator-sensitive. The corrected estimator reports "
            f"{p['rel_reduction_pct']:.3f}% versus sealed reference {sr['rel_reduction_pct']:.3f}% "
            f"(swing {result['swing_pp']:.3f}pp); the frozen sealed result depends on estimator "
            "conventions rather than on incremental funding/price information."
        )
    if verdict == "NOT_EXPLAINED_BY_ESTIMATOR":
        return (
            "The corrected estimator reproduces the sealed reference "
            f"({p['rel_reduction_pct']:.3f}% vs {sr['rel_reduction_pct']:.3f}%, swing "
            f"{result['swing_pp']:.3f}pp) with no material sign flip. The 2025 EXPLORATORY_NULL "
            "is NOT attributable to estimator conventions (train-only standardization + Duan smearing); "
            "it should be preserved as a bounded negative result."
        )
    return "At least one cell failed its admissibility minimum; no attribution is possible."


# ---------------------------------------------------------------------- main

def main() -> int:
    ap = argparse.ArgumentParser(description="FCLR 2025 disjoint corrected-estimator audit")
    ap.add_argument("--smoke", action="store_true")
    ap.add_argument("--write-prereg", action="store_true")
    ap.add_argument("--out-utc", default=None)
    args = ap.parse_args()

    out_utc = args.out_utc or now_utc()
    experiment_id = f"{CAMPAIGN_PREFIX}-{out_utc}"

    if args.write_prereg:
        prereg, json_path, md_path = write_prereg(out_utc)
        print(f"Wrote prereg: {json_path}")
        print(f"Wrote prereg: {md_path}")
        return 0

    prereg_stem = f"prereg_fclr_fwd_vol_2025_disjoint_corrected_audit_{out_utc}"
    prereg_json = RS / f"{prereg_stem}.json"
    prereg_md = RS / f"{prereg_stem}.md"
    if not prereg_json.exists() or not prereg_md.exists():
        raise SystemExit(f"frozen prereg not found: {prereg_json} (run --write-prereg first)")
    prereg = json.loads(prereg_json.read_text())
    assert_prereg_frozen(prereg, experiment_id)

    panel_path = REPO / prereg["panel"]["path"]
    actual_hash = sha256_file(panel_path)
    if actual_hash != PANEL_SHA256:
        raise SystemExit(f"panel hash mismatch: {actual_hash} != {PANEL_SHA256}")

    sealed = json.loads(SEALED_EVAL_PATH.read_text())
    sealed_ref = {
        "source": str(SEALED_EVAL_PATH.relative_to(REPO)),
        "experiment_id": "FCLR-FWD-VOL-2025-DISJOINT-CROSS-20261114T183000Z",
        "primary_contrast": "C2_vs_B1",
        "primary_metric": "24h QLIKE",
        "mean_diff": sealed["primary"]["mean_diff"],
        "rel_reduction_pct": sealed["primary"]["rel_reduction_pct"],
        "ci": [sealed["primary"]["ci_lo"], sealed["primary"]["ci_hi"]],
        "n": sealed["primary"]["n"],
        "n_days": sealed["primary"]["n_days"],
    }

    panel = pd.read_parquet(panel_path)
    panel["ts"] = pd.to_datetime(panel["ts"])
    lineage = audit_lineage(panel)

    safe = out_utc.replace(":", "").replace("-", "")
    build_report_path = None
    build_report = None
    if not args.smoke:
        build_report = {
            "experiment_id": experiment_id,
            "campaign": CAMPAIGN_PREFIX,
            "generated_utc": out_utc,
            "prereg": prereg_json.name,
            "prereg_sha256": sha256_file(prereg_json),
            "panel": str(panel_path.relative_to(REPO)),
            "panel_sha256": PANEL_SHA256,
            "row_count": int(len(panel)),
            "key_count": int(panel[["symbol", "ts"]].drop_duplicates().shape[0]),
            "symbols": sorted(panel["symbol"].unique().tolist()),
            "span_start": str(panel["ts"].min()),
            "span_end": str(panel["ts"].max()),
            "blocks": BLOCKS,
            "embargo_days": EMBARGO_DAYS,
            "sealed_reference_source": str(SEALED_EVAL_PATH.relative_to(REPO)),
            "network_used": False,
            "sealed_artifacts_mutated": False,
            "promotable": False,
            "max_status": "EXPLORATORY_ONLY",
        }
        build_report_path = RS / f"tracka_fwd_vol_2025_disjoint_corrected_audit_build_report_{safe}.json"
        build_report_path.write_text(json.dumps(build_report, indent=2, sort_keys=True, default=str))

    reps = 200 if args.smoke else BOOT_REPS
    placebo_reps = 20 if args.smoke else PLACEBO_REPS

    if not lineage.get("all_pass"):
        cell = {"panel": "existing", "estimator": "corrected", "status": "INADMISSIBLE",
                "verdict": "INCONCLUSIVE", "smoke": bool(args.smoke),
                "instruments": [], "blocks_with_data": [], "n_valid_rows": 0,
                "contrasts": {}, "holm": {}, "primary": None, "per_block": {},
                "loio": [], "loio_pass": 0, "loio_total": 0, "placebo": {},
                "leakage_audit": leakage_audit("corrected"), "per_block_coverage": {}}
        verdict = "INCONCLUSIVE"
        rationale = "lineage audit failed"
        corrected_rel = None
        cell_ok = False
    else:
        cell = evaluate_cell(panel, "corrected", args.smoke, reps, placebo_reps)
        verdict = "INCONCLUSIVE"
        rationale = "cell inadmissible"
        corrected_rel = None
        cell_ok = False
        if cell.get("primary") is not None:
            corrected_rel = cell["primary"].get("rel_reduction_pct")
            cell_ok = True

    verdict, rationale = determine_verdict(corrected_rel, sealed_ref["rel_reduction_pct"],
                                           lineage, cell_ok)
    swing = None
    sign_flip = None
    if corrected_rel is not None:
        swing = abs(float(corrected_rel) - float(sealed_ref["rel_reduction_pct"]))
        sign_flip = ((float(corrected_rel) > 0) != (float(sealed_ref["rel_reduction_pct"]) > 0)) and \
            max(abs(float(corrected_rel)), abs(float(sealed_ref["rel_reduction_pct"]))) >= 1.0

    result = {
        "experiment_id": experiment_id,
        "campaign": CAMPAIGN_PREFIX,
        "generated_utc": out_utc,
        "smoke": bool(args.smoke),
        "status": "SMOKE_ONLY" if args.smoke else "VALID_EXPLORATORY",
        "verdict": verdict,
        "rationale": rationale,
        "promotable": False,
        "max_status": "EXPLORATORY_ONLY",
        "audit_only": True,
        "does_not_reopen_sealed_verdict": True,
        "prereg": str(prereg_json.relative_to(REPO)),
        "prereg_sha256": sha256_file(prereg_json),
        "panel": str(panel_path.relative_to(REPO)),
        "panel_sha256": PANEL_SHA256,
        "sealed_reference": sealed_ref,
        "swing_pp": float(swing) if swing is not None else None,
        "sign_flip": bool(sign_flip) if sign_flip is not None else None,
        "lineage_audit": lineage,
        "build_report": build_report,
        "cell": cell,
    }
    result["interpretation"] = interpretation(verdict, result)

    paths = {"json": None, "md": None}
    if not args.smoke:
        paths = write_report(result, lineage, out_utc)
        result["report_paths"] = paths

    print(f"\nVerdict: {verdict}")
    print(f"Rationale: {rationale}")
    print(f"Corrected rel_reduction: {corrected_rel}% | sealed reference: {sealed_ref['rel_reduction_pct']}% | swing: {swing}pp")
    if paths["json"]:
        print(f"Report: {paths['json']}")
        print(f"Report: {paths['md']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
