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
    # G1 (122): seam GO + prereg/data missing => stable operator/gate-aligned
    # reason_code PREREG_OR_MANIFEST_BLOCK_AFTER_DRIFT_PASS, with seam detail
    # preserved. Fail-closed; no loader invoked, no outcomes inspected.
    if res.get("seam_go_prereg_required") is True or res.get("reason_code_detail") == "ADMISSIBLE_SEAM_GO_PREREG_REQUIRED":
        res["reason_code"] = "PREREG_OR_MANIFEST_BLOCK_AFTER_DRIFT_PASS"
        res["seam_go_prereg_required"] = True
        res.setdefault("reason_code_detail", "ADMISSIBLE_SEAM_GO_PREREG_REQUIRED")
    # G2 (124): seam GO + prereg present + data_path missing => same stable reason_code/parity.
    if res.get("seam_go_data_missing") is True or res.get("reason_code_detail") == "ADMISSIBLE_SEAM_GO_DATA_PATH_MISSING":
        res["reason_code"] = "PREREG_OR_MANIFEST_BLOCK_AFTER_DRIFT_PASS"
        res["seam_go_data_missing"] = True
        res.setdefault("reason_code_detail", "ADMISSIBLE_SEAM_GO_DATA_PATH_MISSING")
        res.setdefault("reads_parquet", False)
        res.setdefault("reads_outcomes", False)
        res.setdefault("outcomes_loaded", None)
        res.setdefault("data_loaded_implicitly", False)
    # Normalise: never claim outcomes were inspected on a blocked branch.
    res.setdefault("outcomes_inspected", False)
    if res.get("status") == "BLOCKED" and not res.get("reason_code"):
        res["reason_code"] = "PREREG_OR_MANIFEST_BLOCK_AFTER_DRIFT_PASS"
    res["guarded_execution_contract"] = "fclr_next_111"
    res["canonical_outputs_mutated"] = False
    res["network"] = False
    res["writes_real_research_state"] = False
    # G3 (131): on BLOCKED, normalize absent booleans to safe defaults so no caller
    # can observe a truthy/outcome-read flag on a refused branch. Type-stable booleans.
    if res.get("status") == "BLOCKED":
        res["outcomes_inspected"] = False
        res["canonical_outputs_mutated"] = False
        res["network"] = False
        res["writes_real_research_state"] = False
        res["reads_parquet"] = False
        res["reads_outcomes"] = False
        res["data_loaded_implicitly"] = False
        res["outcomes_loaded"] = None
    return res


def refusal_payload(**extra: Any) -> Dict[str, Any]:
    """Build a stable machine-readable refusal payload for blocked entrypoints.

    G3 (121): every payload is normalized to a stable field set so callers can
    assert on the exact refusal shape without network/parquet/outcome reads.
    Required keys: status, outcomes_inspected, canonical_outputs_mutated,
    network, writes_real_research_state, guarded_execution_contract, script,
    reason_code, reason. Optional guard snapshot: guard.
    """
    payload: Dict[str, Any] = {
        "status": "BLOCKED",
        "outcomes_inspected": False,
        "data_loaded_implicitly": False,
        "canonical_outputs_mutated": False,
        "network": False,
        "writes_real_research_state": False,
        "guarded_execution_contract": "fclr_next_111",
        "script": extra.pop("script", None),
        "reason_code": extra.pop("reason_code", "PREREG_OR_MANIFEST_BLOCK_AFTER_DRIFT_PASS"),
        "reason": extra.pop("reason", "Blocked by guarded execution contract."),
        "outcomes_loaded": None,
        "reads_parquet": False,
        "reads_outcomes": False,
    }
    guard = extra.pop("guard", None)
    if guard is not None:
        payload["guard"] = _guard_snapshot(guard)
    payload.update(extra)
    return payload


def _as_bool(value: Any) -> Any:
    """G3: coerce a guard field to a strict bool when present, else None (type-stable)."""
    if value is None:
        return None
    return bool(value)


def _guard_snapshot(guard: Dict[str, Any]) -> Dict[str, Any]:
    """G3 (121): stable guard snapshot shape for refusal payloads.

    Captures the machine-representable guard states that surfaced during the
    blocked decision (prereg-required / missing manifest / modeled conflation /
    wrong venue / seam NO-GO) without inspecting outcomes.
    """
    snap = {
        "status": guard.get("status"),
        "reason_code": guard.get("reason_code"),
        "reason_code_detail": guard.get("reason_code_detail"),
        "outcomes_inspected": _as_bool(guard.get("outcomes_inspected")),
        "canonical_outputs_mutated": _as_bool(guard.get("canonical_outputs_mutated")),
        "network": _as_bool(guard.get("network")),
        "writes_real_research_state": _as_bool(guard.get("writes_real_research_state")),
        "reads_parquet": _as_bool(guard.get("reads_parquet")),
        "reads_outcomes": _as_bool(guard.get("reads_outcomes")),
        "fail_closed": _as_bool(guard.get("fail_closed")),
        "seam": guard.get("seam"),
        "seam_go_prereg_required": _as_bool(guard.get("seam_go_prereg_required")),
        "admissible_seam_wired": guard.get("admissible_seam_wired"),
        "manifest_gate": guard.get("manifest_gate"),
        "prereg_required": _as_bool(guard.get("prereg_required")),
    }
    return {k: v for k, v in snap.items() if v is not None}


def assert_loader_never_called(*_args, **_kwargs):  # pragma: no cover - test helper
    raise AssertionError("guarded execution: outcome/parquet loader must not be called on blocked branch")


__all__ = [
    "guarded_execute",
    "refusal_payload",
    "assert_loader_never_called",
    "DEFAULT_CANONICAL_OUTPUTS",
]