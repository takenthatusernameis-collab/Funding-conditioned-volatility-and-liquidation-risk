#!/usr/bin/env python3
"""Track A CLI/operator strict resume gate (FCLR-NEXT-102: bundled drift preflight).

Wires the 098 harness hardening + 101/102 drift preflight into the actual
operator/CLI resume path so that the decision hook fails-closed on repository
drift BEFORE manifest/prereg decision logic that could be misread as GO-ready
state.

Default path:
  1) drift preflight (read-only, <5s, no network, no real research_state writes)
     - if FAIL => BLOCKED with drift_preflight details (outcomes_inspected=false)
  2) prereg-before-outcomes always enforced first by harness
  3) strict full-manifest GO assessment by default when a source manifest is
     supplied (rejects minimal-only GO-shaped observed Hyperliquid claims that
     lack machine-verifiable provenance/label/coverage/block evidence).

An explicit compat/test-fixture flag (`--compat-fixture` / `strict_manifest_gate=False`
in the programmatic API) preserves the legacy minimal-fixture behavior; it is the
only path that may accept a minimal-only manifest.

This module is intentionally side-effect free on real research_state: every run
operates on tmp directories or read-only inputs. It is deterministic and offline.

CLI:
  python scripts/tracka_resume_gate.py \
      [--data PATH] [--output-dir PATH] [--prereg PATH] \
      [--manifest PATH] [--compat-fixture] [--skip-drift-preflight] [--json]
  Exit 0 => resume decision GO/READY; Exit 1 => BLOCKED.
"""
from __future__ import annotations

import argparse
import json
import sys
import tempfile
import time
from pathlib import Path
from typing import Any, Dict, Optional

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.fclr010_harness import FCLR010Harness
from scripts.tracka_resume_check import _valid_go, _valid_strict_manifest_go, drift_preflight


def _load_manifest(path: Optional[str]) -> Optional[Dict[str, Any]]:
    if not path:
        return None
    p = Path(path)
    if not p.exists() or not p.is_file():
        raise FileNotFoundError(f"manifest not found: {p}")
    raw = p.read_bytes()
    if raw.startswith(b"version https://git-lfs.github.com/spec/v1"):
        import subprocess
        r = subprocess.run(["git", "lfs", "smudge", "--"], input=raw, capture_output=True)
        if r.returncode != 0 or not r.stdout:
            raise RuntimeError(f"LFS smudge failed for {p}: {r.stderr[:120]!r}")
        raw = r.stdout
    return json.loads(raw)


def decide(data_path: str, output_dir: str, pre_reg_path: Optional[str],
           source_manifest: Optional[Dict[str, Any]] = None,
           strict_manifest_gate: Optional[bool] = None,
           compat_fixture: bool = False,
           repo_root: Optional[Path] = None,
           research_state_dir: Optional[Path] = None,
           harness_repo_root: Optional[Path] = None,
           skip_drift_preflight: bool = False,
           admissible_manifest_path: Optional[str] = None) -> Dict[str, Any]:
    """Single operator resume decision. No network, no real research_state writes.

    102: Runs drift preflight BEFORE manifest/prereg decision logic (fail-closed).
    Drift checks use repo_root/research_state_dir (default ROOT). Harness/splits
    use harness_repo_root (default ROOT) so tmp-isolated drift tests don't require
    a synthetic run_manifest. Default path: strict manifest gate ON when manifest
    supplied; prereg-before-outcomes always enforced first. Compat path preserved.
    """
    t0 = time.time()
    rr = Path(repo_root) if repo_root is not None else ROOT
    hrr = Path(harness_repo_root) if harness_repo_root is not None else ROOT
    pre = {"pass": True, "skipped": True, "reason": "skip_drift_preflight"} if skip_drift_preflight else drift_preflight(rr, research_state_dir=research_state_dir)
    if not pre.get("pass"):
        return {
            "status": "BLOCKED",
            "reason": "drift preflight failed (fail-closed before manifest/prereg decision)",
            "reason_code": "DRIFT_PREFLIGHT_FAIL_BEFORE_PREREG",
            "fail_closed_order": "drift_preflight->manifest_prereg",
            "outcomes_inspected": False,
            "prereg_required": True,
            "gate_script": "tracka_resume_gate",
            "compat_fixture": bool(compat_fixture),
            "drift_preflight": pre,
            "elapsed_s": round(time.time() - t0, 6),
            "network": False,
            "writes_real_research_state": False,
        }
    # 108: named admissible-seam check (manifest-only, no network/no parquet/no outcomes, fail-closed).
    # The gate runs the seam check first so a NO-GO candidate refuses early, but for a GO
    # candidate the SAME seam result is passed into the harness so the harness's seam logic
    # is the single source of truth for the downstream prereg/data-missing branches. This
    # preserves contract parity: harness, gate, operator and check all observe identical
    # reason_code_detail (ADMISSIBLE_SEAM_GO_PREREG_REQUIRED vs ADMISSIBLE_SEAM_GO_DATA_PATH_MISSING).
    admissible_seam = None
    admissible_manifest_dict = None
    if admissible_manifest_path is not None:
        try:
            from scripts.tracka_resume_check import admissible_seam_check
            admissible_seam = admissible_seam_check(candidate_path=admissible_manifest_path, repo_root=rr)
        except Exception as e:
            admissible_seam = {"pass": False, "status": "NO-GO", "reason_code": "ADMISSIBLE_SEAM_EXCEPTION",
                               "failures": ["seam_exception"], "error": repr(e),
                               "fail_closed": True, "network": False, "reads_outcomes": False, "reads_parquet": False}
        if admissible_seam.get("pass"):
            try:
                admissible_manifest_dict = _load_manifest(admissible_manifest_path)
            except Exception:
                admissible_manifest_dict = None
        if not (admissible_seam or {}).get("pass"):
            return {
                "status": "BLOCKED",
                "reason": "admissible seam validation failed (manifest-only, fail-closed, no outcomes inspected)",
                "reason_code": "ADMISSIBLE_SEAM_NOGO_BEFORE_PREREG",
                "fail_closed_order": "drift_preflight->admissible_seam->manifest_prereg",
                "outcomes_inspected": False,
                "reads_parquet": False,
                "reads_outcomes": False,
                "canonical_outputs_mutated": False,
                "prereg_required": True,
                "gate_script": "tracka_resume_gate",
                "compat_fixture": bool(compat_fixture),
                "drift_preflight": pre,
                "admissible_seam_wired": {k: admissible_seam.get(k) for k in ("pass","status","reason_code","failures","month","fail_closed","network","reads_outcomes","reads_parquet") if k in admissible_seam},
                "elapsed_s": round(time.time() - t0, 6),
                "network": False,
                "writes_real_research_state": False,
            }
    h = FCLR010Harness(repo_root=hrr)
    data_path = Path(data_path)
    # A pre-existing regular file (bad temp-path edge case) is fail-closed as a stable
    # JSON refusal (no traceback contract, no outcomes inspected).
    try:
        if output_dir is None:
            output_dir = Path(tempfile.mkdtemp(prefix="tracka_gate_"))
        else:
            output_dir = Path(output_dir)
            if output_dir.exists() and not output_dir.is_dir():
                raise NotADirectoryError(f"output_dir is not a directory: {output_dir}")
            output_dir.mkdir(parents=True, exist_ok=True)
    except Exception as e:
        return {
            "status": "BLOCKED",
            "reason": f"output_dir unusable (fail-closed, no outcomes): {e!r}",
            "reason_code": "PREREG_OR_MANIFEST_BLOCK_AFTER_DRIFT_PASS",
            "reason_code_detail": "OUTPUT_DIR_UNUSABLE_FAIL_CLOSED",
            "fail_closed_order": "drift_preflight->manifest_prereg",
            "outcomes_inspected": False,
            "prereg_required": True,
            "gate_script": "tracka_resume_gate",
            "compat_fixture": bool(compat_fixture),
            "drift_preflight": pre,
            "elapsed_s": round(time.time() - t0, 6),
            "network": False,
            "writes_real_research_state": False,
            "canonical_outputs_mutated": False,
            "reads_parquet": False,
            "reads_outcomes": False,
        }

    # Resolve strict gate default: default True for manifest-bearing GO decisions,
    # unless compat_fixture explicitly opts into the legacy minimal path.
    if source_manifest is not None and strict_manifest_gate is None:
        strict_manifest_gate = not compat_fixture

    result = h.evaluate_forward(
        data_path,
        output_dir,
        pre_reg_path=Path(pre_reg_path) if pre_reg_path else None,
        source_manifest=source_manifest,
        strict_manifest_gate=strict_manifest_gate,
    )
    result["gate_script"] = "tracka_resume_gate"
    result["compat_fixture"] = bool(compat_fixture)
    result["drift_preflight"] = pre
    if admissible_seam is not None:
        result["admissible_seam_wired"] = {k: admissible_seam.get(k) for k in ("pass","status","reason_code","failures","month","fail_closed","network","reads_outcomes","reads_parquet") if k in admissible_seam}
    # 103/108/110: machine-stable ordering/reason markers (semantics unchanged when no seam candidate)
    _order = "drift_preflight->admissible_seam->manifest_prereg" if admissible_seam is not None else "drift_preflight->manifest_prereg"
    if result.get("status") == "BLOCKED" and pre.get("pass"):
        result.setdefault("reason_code", "PREREG_OR_MANIFEST_BLOCK_AFTER_DRIFT_PASS")
        result.setdefault("fail_closed_order", _order)
        # 110 explicit surface: seam GO but prereg/data blocked => preserve the harness's
        # specific detail rather than overwriting it. The harness already emits the
        # precise reason_code_detail (ADMISSIBLE_SEAM_GO_PREREG_REQUIRED when prereg is
        # missing, ADMISSIBLE_SEAM_GO_DATA_PATH_MISSING when data path is missing) and only
        # sets seam_go_prereg_required in the prereg-missing branch. setdefault keeps the
        # more specific value and never conflates data-missing with prereg-missing.
        if admissible_seam is not None and admissible_seam.get("pass") and result.get("reason_code") == "PREREG_OR_MANIFEST_BLOCK_AFTER_DRIFT_PASS":
            result.setdefault("seam_go_prereg_required", True)
            result.setdefault("reason_code_detail", "ADMISSIBLE_SEAM_GO_PREREG_REQUIRED")
    elif result.get("status") in ("READY_FROZEN", "GO", "COMPLETE"):
        result.setdefault("reason_code", "RESUME_READY_AFTER_DRIFT_PASS")
        result.setdefault("fail_closed_order", _order)
    result["elapsed_s"] = round(time.time() - t0, 6)
    result["network"] = False
    result["writes_real_research_state"] = False
    return result


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="Track A strict CLI/operator resume gate (FCLR-NEXT-102 bundled drift preflight)")
    p.add_argument("--data", required=False, default="/nonexistent_tracka_resume", help="Data path to validate")
    p.add_argument("--output-dir", required=False, default=None, help="Output directory (tmp if omitted)")
    p.add_argument("--prereg", required=False, default=None, help="Pre-registration record path")
    p.add_argument("--manifest", required=False, default=None, help="Track A source manifest JSON path")
    p.add_argument("--admissible-manifest", required=False, default=None, dest="admissible_manifest",
                   help="108: candidate Ironflow month manifest/prereg JSON for named admissible-seam fail-closed check (manifest-only, no network/no parquet/no outcomes)")
    p.add_argument("--compat-fixture", action="store_true",
                   help="Explicit compat/test-fixture flag: preserve legacy minimal-fixture gate")
    p.add_argument("--skip-drift-preflight", action="store_true",
                   help="Controlled test use only: skip bundled drift preflight (default off)")
    p.add_argument("--json", action="store_true", help="Emit machine-readable JSON")
    return p


def main(argv=None) -> int:
    # G3/134: argparse contract violations (unknown flags, malformed CLI args) must
    # refuse as parseable JSON, never as an uncaught usage/traceback exit. --help is
    # allowed to exit 0 normally; any other SystemExit is a fail-closed JSON refusal.
    try:
        args = build_parser().parse_args(argv)
    except SystemExit as se:
        code = getattr(se, "code", 2)
        if code == 0:
            return 0
        print(json.dumps({"status": "BLOCKED",
                          "reason": "argparse contract violation (fail-closed, no outcomes): invalid CLI arguments",
                          "reason_code": "PREREG_OR_MANIFEST_BLOCK_AFTER_DRIFT_PASS",
                          "reason_code_detail": "ARGPARSE_CONTRACT_VIOLATION_FAIL_CLOSED",
                          "fail_closed_order": "drift_preflight->manifest_prereg",
                          "outcomes_inspected": False, "network": False,
                          "writes_real_research_state": False,
                          "canonical_outputs_mutated": False, "reads_parquet": False,
                          "reads_outcomes": False, "gate_script": "tracka_resume_gate",
                          "script": "tracka_resume_gate",
                          "drift_preflight": None, "exit_code": int(code) if isinstance(code, int) else 2}))
        return 1
    # 132 G3: resolve output_dir fail-closed before decide(); a pre-existing regular
    # file (bad temp-path edge case) must refuse as JSON, never traceback.
    try:
        if args.output_dir:
            output_dir = Path(args.output_dir)
            if output_dir.exists() and not output_dir.is_dir():
                raise NotADirectoryError(f"output_dir is not a directory: {output_dir}")
            output_dir.mkdir(parents=True, exist_ok=True)
        else:
            output_dir = Path(tempfile.mkdtemp(prefix="tracka_gate_"))
    except Exception as e:
        print(json.dumps({"status": "BLOCKED",
                          "reason": f"output_dir unusable (fail-closed, no outcomes): {e!r}",
                          "reason_code": "PREREG_OR_MANIFEST_BLOCK_AFTER_DRIFT_PASS",
                          "reason_code_detail": "OUTPUT_DIR_UNUSABLE_FAIL_CLOSED",
                          "fail_closed_order": "drift_preflight->manifest_prereg",
                          "outcomes_inspected": False, "network": False,
                          "writes_real_research_state": False,
                          "canonical_outputs_mutated": False,
                          "reads_parquet": False, "reads_outcomes": False,
                          "gate_script": "tracka_resume_gate", "drift_preflight": None}))
        return 1

    try:
        manifest = _load_manifest(args.manifest)
    except FileNotFoundError as e:
        print(json.dumps({"status": "BLOCKED", "reason": str(e), "reason_code": "PREREG_OR_MANIFEST_BLOCK_AFTER_DRIFT_PASS",
                          "fail_closed_order": "drift_preflight->manifest_prereg",
                          "outcomes_inspected": False, "network": False, "writes_real_research_state": False,
                          "canonical_outputs_mutated": False, "reads_parquet": False, "reads_outcomes": False,
                          "gate_script": "tracka_resume_gate", "drift_preflight": None}))
        return 1
    except Exception as e:
        # G2 (130): malformed manifest/prereg-adjacent CLI inputs must fail closed
        # with stable machine-readable refusal (no traceback contract, no outcomes).
        print(json.dumps({"status": "BLOCKED",
                          "reason": f"manifest parse/load failed (fail-closed, no outcomes): {e!r}",
                          "reason_code": "PREREG_OR_MANIFEST_BLOCK_AFTER_DRIFT_PASS",
                          "fail_closed_order": "drift_preflight->manifest_prereg",
                          "outcomes_inspected": False, "network": False,
                          "writes_real_research_state": False, "canonical_outputs_mutated": False,
                          "reads_parquet": False, "reads_outcomes": False,
                          "gate_script": "tracka_resume_gate", "drift_preflight": None}))
        return 1

    try:
        res = decide(
            data_path=args.data,
            output_dir=str(output_dir),
            pre_reg_path=args.prereg,
            source_manifest=manifest,
            compat_fixture=args.compat_fixture,
            skip_drift_preflight=args.skip_drift_preflight,
            admissible_manifest_path=args.admissible_manifest,
        )
    except Exception as e:
        # Fail-closed on unexpected decision errors: never inspect outcomes.
        res = {"status": "BLOCKED",
               "reason": f"gate decision failed (fail-closed, no outcomes): {e!r}",
               "reason_code": "PREREG_OR_MANIFEST_BLOCK_AFTER_DRIFT_PASS",
               "fail_closed_order": "drift_preflight->manifest_prereg",
               "outcomes_inspected": False, "network": False,
               "writes_real_research_state": False, "canonical_outputs_mutated": False,
               "reads_parquet": False, "reads_outcomes": False,
               "gate_script": "tracka_resume_gate"}
    print(json.dumps(res, indent=2, sort_keys=True))
    return 0 if res["status"] == "READY_FROZEN" else 1


if __name__ == "__main__":
    sys.exit(main())