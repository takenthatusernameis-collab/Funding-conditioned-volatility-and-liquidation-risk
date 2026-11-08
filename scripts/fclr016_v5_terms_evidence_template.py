#!/usr/bin/env python3
"""Deterministic, read-only/non-evidentiary Gate 4 v5 terms-evidence TEMPLATE generator.

Emits ONLY a clearly non-evidentiary template at an explicit user-provided output path.
No outcomes, no network, no data loading, no canonical mutation. NEVER creates
RESOLVED_VERIFIED status and never overwrites existing evidence without --force-template.
A human/legal reviewer must complete verifiable fields before the file can become evidence.
"""
from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

TEMPLATE_STATUS = "TEMPLATE_NOT_EVIDENCE"
RESOLVED_STATUS = "RESOLVED_VERIFIED"
WARNING = (
    "NON-EVIDENTIARY TEMPLATE: This file cannot advance any Gate 4 v5 admissibility gate. "
    "A human/legal reviewer must complete all required verifiable fields and create a "
    "separate RESOLVED_VERIFIED artifact (never by renaming this template in place without "
    "full review evidence). Automated agents must not fabricate terms/license/reviews."
)


def _utc() -> str:
    return datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")


def build_template(scope_window: str) -> dict:
    return {
        "artifact": "fclr016_v5_terms_evidence_TEMPLATE",
        "schema_version": 1,
        "generated_utc": _utc(),
        "status": TEMPLATE_STATUS,
        "confirmatory_provenance_go": False,
        "admissibility_complete": False,
        "confirmatory_claim_go": "NO_GO",
        "fabricated": False,
        "no_confirmatory_outcomes": True,
        "human_review_required": True,
        "template_warning": WARNING,
        "scope_match": {
            "window": scope_window,
            "symbols": ["BTCUSDT", "ETHUSDT", "BNBUSDT", "SOLUSDT", "XRPUSDT"],
            "kinds": ["fundingRate", "klines", "markPriceKlines", "indexPriceKlines", "premiumIndexKlines"],
            "source": "Binance Vision (frozen Gate 4 v5 scope; human must verify terms for this scope)",
        },
        "required_human_fields_to_complete": {
            "terms_url_reviewed": None,
            "access_date_utc": None,
            "terms_version_or_snapshot_id": None,
            "not_provided_by_source_justification": None,
            "relevant_clause_summary": None,
            "reviewer_role": None,
            "reviewer_identity_or_contact_hash": None,
            "conclusion": None,
            "conditions_or_restrictions": None,
            "evidence_artifacts": None,
        },
        "resolution_instructions": [
            "Human/legal reviewer completes all required fields with verifiable facts only.",
            "Set fabricated=false only when facts are verified; never fabricate snapshots/URLs/reviews.",
            "Save as research_state/fclr016_local_audit/fclr016_v5_terms_evidence_RESOLVED_<UTC>.json (separate file).",
            "Set status=RESOLVED_VERIFIED only after human review is recorded and scope matches.",
            "Reconcile admissibility_refs_sha256/paths; promote prereg only after all guards green.",
            "Run validator/package/report/confirmatory guard; they must refuse until frozen+all GO.",
        ],
    }


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="Emit non-evidentiary FCLR-016 v5 terms-evidence template")
    ap.add_argument("--out", required=True, help="Explicit output path for template JSON")
    ap.add_argument("--scope-window", default="2025-08-01..2025-10-31")
    ap.add_argument("--force-template", action="store_true",
                    help="Allow overwriting an existing non-RESOLVED template/blocker file at --out; NEVER creates RESOLVED")
    args = ap.parse_args(argv)

    out = Path(args.out)
    if out.exists():
        if not args.force_template:
            print(json.dumps({"ok": False, "error": f"refusing overwrite without --force-template: {out}",
                              "status": TEMPLATE_STATUS, "confirmatory_claim_go": "NO_GO"}, sort_keys=True))
            return 2
        try:
            existing = json.loads(out.read_text(encoding="utf-8"))
        except Exception:
            existing = {}
        if isinstance(existing, dict) and existing.get("status") == RESOLVED_STATUS:
            print(json.dumps({"ok": False, "error": "refusing to overwrite RESOLVED_VERIFIED evidence",
                              "status": TEMPLATE_STATUS, "confirmatory_claim_go": "NO_GO"}, sort_keys=True))
            return 2

    tpl = build_template(args.scope_window)
    if tpl.get("status") == RESOLVED_STATUS:
        print(json.dumps({"ok": False, "error": "internal invariant: template status must not be RESOLVED_VERIFIED"}, sort_keys=True))
        return 2
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(tpl, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({
        "ok": True,
        "out": str(out),
        "status": tpl["status"],
        "confirmatory_provenance_go": False,
        "admissibility_complete": False,
        "confirmatory_claim_go": "NO_GO",
        "fabricated": False,
        "no_confirmatory_outcomes": True,
        "human_review_required": True,
        "warning": WARNING,
    }, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
