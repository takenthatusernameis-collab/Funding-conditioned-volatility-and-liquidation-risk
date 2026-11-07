#!/usr/bin/env python3
"""FCLR-NEXT-138: FCLR-014 manifest guardrail — committed-anchor integrity.

The FCLR-014 local-audit anchors (provenance decision, admissibility audit, candidate
inventory, prereg draft) are the single source of truth for the NO-GO provenance verdict.
This test pins their sha256 so that no later session can silently rewrite a dated
evidence artifact (e.g. flip NO-GO to GO, or reclassify consumed windows) without the
canonical integrity test failing. Additive only: no prior artifact is modified, no
outcomes are computed, no network/creds used.
"""
import hashlib
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
RS = ROOT / "research_state"
AUDIT = RS / "fclr014_local_audit"

# Dated FCLR-014 local-audit anchors (committed, outcome-free, evidence for the
# provenance NO-GO verdict). If any hash changes the artifact was rewritten and the
# session must stop and reconcile before any confirmatory work.
ANCHORS = {
    "FCLR-014-provenance-decision": {
        "path": AUDIT / "fclr014_provenance_decision_20261107T133102Z.md",
        "sha256": "4581333380fb5debf502b63db62920b668c461fea6cdcb5eed98c861f08a27d6",
        "must_contain": [
            "NO-GO FOR CONFIRMATORY CLAIMS",
            "provenance UNVERIFIED",
            "2025-01..2025-12, 2026-01..2026-06, 2026-10",
        ],
        "must_not_contain": ["provenance verified", "GO for confirmatory"],
    },
    "FCLR-014-admissibility-audit": {
        "path": RS / "local_data_admissibility_audit_20261107.md",
        "sha256": "5279e9d0c57060e8657b8f7452d0755d80cead1aa457345a3965ddcdd77bc997",
        "must_contain": [
            "NO-GO for confirmatory reopen as-is",
            "2024-01..03",
            "FCLR-002/003",
        ],
        # Flip signal: a bare affirmative GO verdict line (NO-GO prefix removed).
        "must_not_contain": ["**GO for confirmatory reopen as-is**"],
    },
    "FCLR-014-candidate-inventory": {
        "path": AUDIT / "fclr014_cache_candidate_inventory_20261107T131603Z.json",
        "sha256": "5d0fcff387f2532cea11a152dd08832d8cfb0cc416d004b5167d94941ce2bc82",
        "must_contain": [
            '"status": "CONSUMED/EXCLUDED"',
            "2024_01",
        ],
        "must_not_contain": [],
    },
    "FCLR-014-prereg-draft": {
        "path": AUDIT / "fclr014_prereg_draft_20261107T131603Z.md",
        "sha256": "193a5a18418d3680e9fbcbce9f50d77df10c15c536bc7b5af26a686a32d47a8f",
        "must_contain": [
            "DRAFT. **No outcomes inspected.",
            "DO NOT EXECUTE OUTCOMES FROM THIS DRAFT",
            "**BLOCKER:** unauthenticated origin",
        ],
        # Flip signal: the header being promoted from DRAFT to a frozen prereg.
        "must_not_contain": ["FROZEN PRE-REGISTRATION", "frozen preregistration"],
    },
}


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


class TestFCLR014AnchorIntegrity(unittest.TestCase):
    def test_all_anchor_hashes_unchanged(self):
        for label, spec in ANCHORS.items():
            self.assertTrue(
                spec["path"].exists(),
                f"{label} anchor missing: {spec['path']}",
            )
            actual = _sha256(spec["path"])
            self.assertEqual(
                actual,
                spec["sha256"],
                f"{label} anchor sha256 changed (evidence rewritten): "
                f"expected {spec['sha256']}, got {actual}",
            )

    def test_anchor_verdict_strings_preserved(self):
        for label, spec in ANCHORS.items():
            text = spec["path"].read_text(encoding="utf-8")
            for needle in spec["must_contain"]:
                self.assertIn(
                    needle,
                    text,
                    f"{label}: required verdict string missing/altered: {needle!r}",
                )
            for forbidden in spec["must_not_contain"]:
                self.assertNotIn(
                    forbidden,
                    text,
                    f"{label}: verdict flipped to GO: {forbidden!r}",
                )

    def test_prereg_draft_stays_unfrozen(self):
        # The prereg draft must never be promoted in place to a frozen prereg: its
        # header must remain a DRAFT header and it must not contain a frozen-prereg
        # declaration. (The checklist line `frozen_before_outcomes=true` is a
        # pre-outcome requirement, not a declaration that the draft is frozen.)
        spec = ANCHORS["FCLR-014-prereg-draft"]
        text = spec["path"].read_text(encoding="utf-8")
        self.assertIn("DRAFT", text.splitlines()[0])
        self.assertNotIn("FROZEN PRE-REGISTRATION", text)
        self.assertNotIn("frozen preregistration", text.lower())


if __name__ == "__main__":
    unittest.main()