#!/usr/bin/env python3
"""Track A CLI/operator strict resume gate (FCLR-NEXT-099).

Wires the 098 harness hardening into the actual operator/CLI resume path so that
the decision hook used by future agents and CI refuses to proceed without:

  1) a pre-registration record (PREREG-BEFORE-OUTCOMES, always, before any
     outcome/data content is inspected), and
  2) a strict full-manifest GO assessment by default when a source manifest is
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
      [--manifest PATH] [--compat-fixture] [--json]
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
from scripts.tracka_resume_check import _valid_go, _valid_strict_manifest_go


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
           compat_fixture: bool = False) -> Dict[str, Any]:
    """Single operator resume decision. No network, no real research_state writes.

    Default path (compat_fixture=False): strict manifest gate ON when a manifest
    is supplied; prereg-before-outcomes always enforced first.
    Compat/test-fixture path (compat_fixture=True): legacy minimal-fixture gate
    preserved for callers/tests that explicitly opt in.
    """
    t0 = time.time()
    h = FCLR010Harness(repo_root=ROOT)
    data_path = Path(data_path)
    output_dir = Path(output_dir)

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
    result["elapsed_s"] = round(time.time() - t0, 6)
    result["network"] = False
    result["writes_real_research_state"] = False
    return result


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="Track A strict CLI/operator resume gate (FCLR-NEXT-099)")
    p.add_argument("--data", required=False, default="/nonexistent_tracka_resume", help="Data path to validate")
    p.add_argument("--output-dir", required=False, default=None, help="Output directory (tmp if omitted)")
    p.add_argument("--prereg", required=False, default=None, help="Pre-registration record path")
    p.add_argument("--manifest", required=False, default=None, help="Track A source manifest JSON path")
    p.add_argument("--compat-fixture", action="store_true",
                   help="Explicit compat/test-fixture flag: preserve legacy minimal-fixture gate")
    p.add_argument("--json", action="store_true", help="Emit machine-readable JSON")
    return p


def main(argv=None) -> int:
    args = build_parser().parse_args(argv)
    output_dir = Path(args.output_dir) if args.output_dir else Path(tempfile.mkdtemp(prefix="tracka_gate_"))
    output_dir.mkdir(parents=True, exist_ok=True)

    try:
        manifest = _load_manifest(args.manifest)
    except FileNotFoundError as e:
        print(json.dumps({"status": "BLOCKED", "reason": str(e), "outcomes_inspected": False}))
        return 1

    res = decide(
        data_path=args.data,
        output_dir=str(output_dir),
        pre_reg_path=args.prereg,
        source_manifest=manifest,
        compat_fixture=args.compat_fixture,
    )
    print(json.dumps(res, indent=2, sort_keys=True))
    return 0 if res["status"] == "READY_FROZEN" else 1


if __name__ == "__main__":
    sys.exit(main())