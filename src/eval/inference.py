"""Evaluation-time inference diagnostics (synthetic-testable, no I/O side effects).

Hardened helpers for block-bootstrap ΔQLIKE CIs used by exploratory Gate 4
workflows. Behavior is additive/compatible with existing callers: original
fields are preserved; diagnostic fields are appended.

NOT CONFIRMATORY by itself; callers must label outputs appropriately.
"""
from __future__ import annotations

from typing import Any, Dict, List, Optional

import numpy as np
import pandas as pd

MIN_BLOCKS_RECOMMENDED = 3
MIN_REPS_EFFECTIVE = 100


def _base_result(
    *,
    point: Optional[float],
    ci_low: Optional[float],
    ci_high: Optional[float],
    n_obs: int,
    n_blocks: int,
    n_reps: int,
    seed: int,
    block_hours: int,
    alpha: float,
) -> Dict[str, Any]:
    return {
        "point": point,
        "ci_low": ci_low,
        "ci_high": ci_high,
        "n_obs": int(n_obs),
        "n_blocks": int(n_blocks),
        "n_reps": int(n_reps),
        "seed": int(seed),
        "block_hours": int(block_hours),
        "alpha": float(alpha),
    }


def diagnose_block_bootstrap_inputs(
    diffs: np.ndarray,
    *,
    n_blocks_total: int,
    n_blocks_nonempty_finite: int,
    n_reps_requested: int,
    n_reps_effective: int,
) -> Dict[str, Any]:
    diffs = np.asarray(diffs, dtype=float)
    finite_mask = np.isfinite(diffs)
    n_finite_obs = int(np.sum(finite_mask))
    nonfinite_obs = int(diffs.size - n_finite_obs)
    flags: List[str] = []
    degenerate = False
    if diffs.size == 0:
        flags.append("empty_input")
        degenerate = True
    if nonfinite_obs > 0:
        flags.append("non_finite_diffs_present")
    if n_finite_obs == 0 and diffs.size > 0:
        flags.append("all_diffs_non_finite")
        degenerate = True
    if n_blocks_nonempty_finite < 1:
        flags.append("no_finite_blocks")
        degenerate = True
    elif n_blocks_nonempty_finite < MIN_BLOCKS_RECOMMENDED:
        flags.append("too_few_blocks")
        degenerate = True
    if n_reps_requested > 0 and n_reps_effective < 1:
        flags.append("no_effective_replicates")
        degenerate = True
    elif n_reps_effective > 0 and n_reps_effective < min(MIN_REPS_EFFECTIVE, n_reps_requested):
        flags.append("low_effective_replicates")
    if n_finite_obs > 0 and np.allclose(diffs[finite_mask], diffs[finite_mask][0], equal_nan=False):
        flags.append("constant_finite_diffs")
    return {
        "n_obs_total": int(diffs.size),
        "n_obs_finite": n_finite_obs,
        "n_obs_nonfinite": nonfinite_obs,
        "n_blocks_total": int(n_blocks_total),
        "n_blocks_nonempty_finite": int(n_blocks_nonempty_finite),
        "effective_block_count": int(n_blocks_nonempty_finite),
        "n_reps_requested": int(n_reps_requested),
        "n_reps_effective": int(n_reps_effective),
        "degenerate": bool(degenerate),
        "regime_flags": flags,
        "inference_ok": bool(not degenerate and n_reps_effective > 0 and n_finite_obs > 0),
    }


def block_bootstrap_delta_ci_diagnostic(
    paired: pd.DataFrame,
    *,
    block_hours: int = 24,
    n_reps: int = 2000,
    seed: int = 12345,
    alpha: float = 0.05,
    timestamp_col: str = "timestamp",
    diff_col: str = "diff",
    min_blocks: int = 1,
) -> Dict[str, Any]:
    """Block bootstrap CI for mean Δ (alt-base) with explicit diagnostics.

    Resamples whole UTC time blocks jointly across instruments (as represented in
    `paired`). Rejects non-finite diffs from inference accounting; reports
    effective block count and degenerate/too-few-block regimes. Compatible with
    `scripts.run_funding_ablations.block_bootstrap_delta_ci` return shape plus
    additive diagnostic fields.
    """
    from src.volatility import block_bootstrap as bb

    base = _base_result(
        point=None, ci_low=None, ci_high=None, n_obs=0, n_blocks=0, n_reps=0,
        seed=seed, block_hours=block_hours, alpha=alpha,
    )
    if paired is None or len(paired) == 0:
        diag = diagnose_block_bootstrap_inputs(
            np.array([], dtype=float), n_blocks_total=0, n_blocks_nonempty_finite=0,
            n_reps_requested=n_reps, n_reps_effective=0,
        )
        base.update(diag)
        base["ci_accounting_valid"] = False
        return base

    work = paired.copy()
    if timestamp_col not in work.columns or diff_col not in work.columns:
        diag = diagnose_block_bootstrap_inputs(
            np.array([], dtype=float), n_blocks_total=0, n_blocks_nonempty_finite=0,
            n_reps_requested=n_reps, n_reps_effective=0,
        )
        diag["regime_flags"] = list(diag.get("regime_flags", [])) + ["missing_required_columns"]
        diag["degenerate"] = True
        diag["inference_ok"] = False
        base.update(diag)
        base["ci_accounting_valid"] = False
        return base

    work["_block"] = pd.to_datetime(work[timestamp_col], utc=True, errors="coerce").dt.floor(f"{int(block_hours)}h")
    raw_diffs = pd.to_numeric(work[diff_col], errors="coerce").to_numpy(dtype=float)
    finite_mask = np.isfinite(raw_diffs) & pd.notna(work["_block"]).to_numpy()
    finite_work = work.loc[finite_mask, ["_block", diff_col]].copy()
    finite_work[diff_col] = pd.to_numeric(finite_work[diff_col], errors="coerce")

    blocks_all = work.groupby("_block", sort=True, dropna=True)[diff_col].apply(
        lambda s: pd.to_numeric(s, errors="coerce").to_numpy(dtype=float)
    ).to_dict()
    blocks_finite = {
        k: np.asarray(v[np.isfinite(v)], dtype=float)
        for k, v in finite_work.groupby("_block", sort=True)[diff_col].apply(
            lambda s: pd.to_numeric(s, errors="coerce").to_numpy(dtype=float)
        ).to_dict().items()
    }
    blocks_finite = {k: v for k, v in blocks_finite.items() if v.size > 0}
    keys = list(blocks_finite.keys())
    n_blocks_total = len(blocks_all)
    n_blocks_finite = len(keys)

    diag = diagnose_block_bootstrap_inputs(
        raw_diffs, n_blocks_total=n_blocks_total, n_blocks_nonempty_finite=n_blocks_finite,
        n_reps_requested=n_reps, n_reps_effective=0,
    )

    if n_blocks_finite < max(1, int(min_blocks)) or not keys:
        if n_blocks_finite < MIN_BLOCKS_RECOMMENDED and "too_few_blocks" not in diag["regime_flags"]:
            diag["regime_flags"].append("too_few_blocks")
            diag["degenerate"] = True
            diag["inference_ok"] = False
        point = float(np.mean(finite_work[diff_col])) if len(finite_work) else None
        base.update(_base_result(
            point=point, ci_low=point, ci_high=point, n_obs=int(np.sum(finite_mask)),
            n_blocks=n_blocks_finite, n_reps=0, seed=seed, block_hours=block_hours, alpha=alpha,
        ))
        base.update(diag)
        base["ci_accounting_valid"] = False
        return base

    point = float(finite_work[diff_col].mean())
    reps_idx = bb.circular_block_bootstrap_indices(n_blocks_finite, 1, int(n_reps), seed=int(seed))
    diffs_rep: List[float] = []
    for ridx in reps_idx:
        vals = []
        for bi in ridx:
            vals.append(blocks_finite[keys[int(bi)]])
        arr = np.concatenate(vals) if vals else np.array([], dtype=float)
        arr = arr[np.isfinite(arr)]
        if arr.size:
            diffs_rep.append(float(np.mean(arr)))

    diag = diagnose_block_bootstrap_inputs(
        raw_diffs, n_blocks_total=n_blocks_total, n_blocks_nonempty_finite=n_blocks_finite,
        n_reps_requested=n_reps, n_reps_effective=len(diffs_rep),
    )
    result = _base_result(
        point=point, ci_low=point, ci_high=point, n_obs=int(np.sum(finite_mask)),
        n_blocks=n_blocks_finite, n_reps=len(diffs_rep), seed=seed, block_hours=block_hours, alpha=alpha,
    )
    if diffs_rep:
        ds = np.sort(np.asarray(diffs_rep, dtype=float))
        lo_i = max(0, min(len(ds) - 1, int(np.floor((alpha / 2.0) * len(ds)))))
        hi_i = max(0, min(len(ds) - 1, int(np.ceil((1.0 - alpha / 2.0) * len(ds))) - 1))
        result["ci_low"] = float(ds[lo_i])
        result["ci_high"] = float(ds[hi_i])
        result["ci_accounting_valid"] = bool(
            np.isfinite(result["point"]) and np.isfinite(result["ci_low"]) and np.isfinite(result["ci_high"])
            and result["ci_low"] <= result["ci_high"]
        )
    else:
        result["ci_accounting_valid"] = False
    result.update(diag)
    return result
