#!/usr/bin/env python3
"""
Create pre-registration for LIQUIDATION_FORWARD_VALIDATE_004 BEFORE inspecting outcomes
"""
import json
from datetime import datetime, timezone
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent
MANIFEST = REPO_ROOT / "research_state" / "run_manifest.json"


def main():
    ts = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    with open(MANIFEST) as f:
        manifest = json.load(f)
    splits = manifest.get("split_boundaries_fclr010", {})
    prereg = {
        "experiment_id": "LIQUIDATION_FORWARD_VALIDATE_004",
        "campaign": "LIQUIDATION_FORWARD_VALIDATE_HEAVY-004d",
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "pre_registered_before_outcomes": True,
        "frozen_before_outcomes": True,
        "protocol_ref": "research_state/research_protocol_fclr010.md v1.0",
        "harness_ref": "scripts/fclr010_harness.py",
        "track": "A",
        "primary_contrast": "C2_vs_B1",
        "primary_metric": "brier",
        "bootstrap_reps": 2000,
        "splits_from_manifest": splits,
        "multiplicity": {"plan": "Holm across registered family if applicable"},
        "rubric_go": {
            "min_symbols": 5,
            "min_blocks_or_month": ">=1 complete month with >=5 symbols OR >=3 non-overlapping 30-day blocks",
            "completeness_doc_required": True,
            "license_ok": True,
            "unauthenticated_only": True,
            "no_requester_pays": True,
            "schema_compatible_fclr010": True
        },
        "notes": "Pre-registered before inspecting any post-2026-10-31 label/outcome columns"
    }
    out = REPO_ROOT / "research_state" / f"experiment_prereg_LIQUIDATION_FORWARD_VALIDATE_004_{ts}.json"
    with open(out, "w") as f:
        json.dump(prereg, f, indent=2)
    print(f"Wrote: {out}")


if __name__ == "__main__":
    main()
