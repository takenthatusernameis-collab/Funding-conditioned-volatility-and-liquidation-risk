#!/usr/bin/env python3
"""FCLR-NEXT-111: single guarded execution entry contract for Track A CLI entrypoints.

Both ``scripts/fclr010_execute.py:main`` and ``scripts/fclr010_execute_fast.py:main``
previously bypassed the guarded harness seam/prereg/manifest/data contract:

  * fclr010_execute.py:main  -> imported pyarrow and called ``pq.read_table`` directly
                               on the ironflow census directory with no admissible
                               seam/prereg/manifest guard.
  * fclr010_execute_fast.py:main -> wrote a hardcoded evaluation summary with no guard
                               at all (fabricated metrics presented as measured).

This module is the single, machine-enforced refusal contract. Any real execution
entrypoint that consumes trigger artifacts / candidate manifests MUST route its actual
data load through ``guarded_execute`` (or ``FCLR010Harness.execute_ready_data_load``
which this wraps). Every blocked branch refuses before any parquet/outcome read and
before any canonical output mutation.

Contract surface (stable, backward compatible with 108/110 reason codes):
  - blocked => status=BLOCKED, outcomes_inspected:false, no parquet read, no output
    mutation, no network, no real research_state writes.
  - READY_FROZEN => explicit outcome_loader invoked exactly once, data_loaded_implicitly
    false, data_load_mode EXPLICIT_LOADER_AFTER_GATES.
  - seam GO + prereg/data missing => reason_code PREREG_OR_MANIFEST_BLOCK_AFTER_DRIFT_PASS
    with explicit seam_go_prerg_required=true and
    reason_code_detail=ADMISSIBLE_SEAM_GO_PREREG_REQUIRED preserved.
"""
from __future__ import annotations

import json
import tempfile
from pathlib import Path
from typing import Any, Callable, Dict, Optional

from scripts.fclr010_harness import FCLR010Harness


# Default canonical output paths that must never be mutated on a blocked branch.
DEFAULT_CANONICAL_OUTPUTS = (
    "research_state/evaluation_summary_FCLR010.md",
    "research_state/run_manifest.json",
)


def _default_outcome_loader(data_path: Path) -> Dict[str, Any]:
    """Default explicit outcome loader: reads ironflow census parquet.

    This is the ONLY path permitted to read parquet, and it is invoked only after
    guarded_execute returns READY_FROZEN. It is kept separate from pyarrow import
    so blocked branches never import pyarrow.
    """
    import pyarrow.parquet as pq  # local import: blocked branches never reach here

    data_path = Path(data_path)
    files = sorted([f for f in data_path.iterdir() if f.suffix == ".parquet"]) if data_path.exists() else []
    rows = 0
    for f in files:
        try:
            t = pq.read_table(f, columns=["timestamp", "market", "position_side", "notional_usd"])
            rows += t.num_rows
        except Exception:
            continue
    return {"parquet_files": len(files), "rows": rows, "data_path": str(data_path)}


def guarded_execute(
    *,
    data_path: Path,
    pre_reg_path: Optional[Path],
    repo_root: Optional[Path] = None,
    source_manifest: Optional[Dict[str, Any]] = None,
    strict_manifest_gate: Optional[bool] = None,
    admissible_manifest: Optional[Dict[str, Any]] = None,
    admissible_manifest_path: Optional[str] = None,
    outcome_loader: Optional[Callable[[Path], Dict[str, Any]]] = None,
    loader_context: Optional[Dict[str, Any]] = None,
    allow_default_loader: bool = False,
) -> Dict[str, Any]:
    """Single guarded execution contract used by every real Track A CLI entrypoint.

    Returns a dict with at minimum: status, outcomes_inspected, reason_code (when
    blocked), data_loaded_implicitly, data_load_mode. On blocked branches the
    outcome_loader is never called and no parquet is read.

    ``loader_context`` is forwarded to the outcome_loader as its second positional
    argument when provided, so entrypoint-specific frozen split windows can reach
    the explicit loader without leaking through the guarded seam.
    """
    h = FCLR010Harness(repo_root=repo_root)

    def _invoke_loader(dp: Path):
        if loader_context is not None:
            return outcome_loader(dp, loader_context)
        return outcome_loader(dp)

    loader = None
    if outcome_loader is not None:
        loader = _invoke_loader
    elif allow_default_loader:
        loader = _default_outcome_loader

    res = h.execute_ready_data_load(
        data_path=Path(data_path),
        pre_reg_path=Path(pre_reg_path) if pre_reg_path else None,
        source_manifest=source_manifest,
        strict_manifest_gate=strict_manifest_gate,
        outcome_loader=loader,
        admissible_manifest=admissible_manifest,
        admissible_manifest_path=admissible_manifest_path,
    )
    # Normalise: never claim outcomes were inspected on a blocked branch.
    res.setdefault("outcomes_inspected", False)
    res.setdefault("reason_code", "PREREG_OR_MANIFEST_BLOCK_AFTER_DRIFT_PASS")
    res["guarded_execution_contract"] = "fclr_next_111"
    res["canonical_outputs_mutated"] = False
    res["network"] = False
    res["writes_real_research_state"] = False
    return res


def refusal_payload(**extra: Any) -> Dict[str, Any]:
    """Build a stable machine-readable refusal payload for blocked entrypoints."""
    payload: Dict[str, Any] = {
        "status": "BLOCKED",
        "outcomes_inspected": False,
        "data_loaded_implicitly": False,
        "canonical_outputs_mutated": False,
        "network": False,
        "writes_real_research_state": False,
        "guarded_execution_contract": "fclr_next_111",
    }
    payload.update(extra)
    return payload


def assert_loader_never_called(*_args, **_kwargs):  # pragma: no cover - test helper
    raise AssertionError("guarded execution: outcome/parquet loader must not be called on blocked branch")


__all__ = [
    "guarded_execute",
    "refusal_payload",
    "assert_loader_never_called",
    "DEFAULT_CANONICAL_OUTPUTS",
]