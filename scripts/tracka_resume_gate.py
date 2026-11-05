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
    return json.loads(p.read_text(encoding="utf-8"))


def decide(data_path: str, output_dir: str, pre_reg_path: Optional[str],
           source_manifest: Optional[Dict[str, Any]] = None,
           strict_manifest_gate: Optional[bool] = None,
           compat_fixture: bool = False,
           repo_root: Optional[Path] = None,
           research_state_dir: Optional[Path] = None,
           harness_repo_root: Optional[Path] = None,
           skip_drift_preflight: bool = False) -> Dict[str, Any]:
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
            "outcomes_inspected": False,
            "prereg_required": True,
            "gate_script": "tracka_resume_gate",
            "compat_fixture": bool(compat_fixture),
            "drift_preflight": pre,
            "elapsed_s": round(time.time() - t0, 6),
            "network": False,
            "writes_real_research_state": False,
        }
    h = FCLR010Harness(repo_root=hrr)
    data_path = Path(data_path)
    if output_dir is None:
        output_dir = Path(tempfile.mkdtemp(prefix="tracka_gate_"))
    else:
        output_dir = Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)

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
    p.add_argument("--compat-fixture", action="store_true",
                   help="Explicit compat/test-fixture flag: preserve legacy minimal-fixture gate")
    p.add_argument("--skip-drift-preflight", action="store_true",
                   help="Controlled test use only: skip bundled drift preflight (default off)")
    p.add_argument("--json", action="store_true", help="Emit machine-readable JSON")
    return p


def main(argv=None) -> int:
    args = build_parser().parse_args(argv)
    output_dir = Path(args.output_dir) if args.output_dir else Path(tempfile.mkdtemp(prefix="tracka_gate_"))
    output_dir.mkdir(parents=True, exist_ok=True)

    try:
        manifest = _load_manifest(args.manifest)
    except FileNotFoundError as e:
        print(json.dumps({"status": "BLOCKED", "reason": str(e), "outcomes_inspected": False, "drift_preflight": None}))
        return 1

    res = decide(
        data_path=args.data,
        output_dir=str(output_dir),
        pre_reg_path=args.prereg,
        source_manifest=manifest,
        compat_fixture=args.compat_fixture,
        skip_drift_preflight=args.skip_drift_preflight,
    )
    print(json.dumps(res, indent=2, sort_keys=True))
    return 0 if res["status"] == "READY_FROZEN" else 1


if __name__ == "__main__":
    sys.exit(main())