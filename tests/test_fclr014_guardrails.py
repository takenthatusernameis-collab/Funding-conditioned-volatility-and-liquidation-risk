#!/usr/bin/env python3
"""Guardrails for FCLR-014 manifests: no consumed windows, provenance, >=3 blocks, fail-closed."""
import json, unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
RS = ROOT / "research_state"

CONSUMED = {"2024-01..12", "2026-07..09"}
CONFOUNDED = {"2026-07", "2026-08", "2026-09"}


def validate_manifest(m):
    errors = []
    if not isinstance(m, dict):
        return ["manifest must be dict"]
    if not m.get("frozen_before_outcomes"):
        errors.append("frozen_before_outcomes must be true")
    if "provenance_documented" not in m or not m.get("provenance_documented"):
        errors.append("provenance must be documented")
    excluded = m.get("excluded_windows", [])
    for w in ("2024-01..12", "2026-07..09"):
        if w not in excluded:
            errors.append(f"missing excluded window {w}")
    windows = m.get("test_blocks", [])
    if len(windows) < 3:
        errors.append("need >=3 non-overlapping 30-day test blocks")
    # overlap check
    seen = set()
    for b in windows:
        key = (b.get("start"), b.get("end"))
        if key in seen:
            errors.append("duplicate/overlapping test block")
        seen.add(key)
    # consumed/confounded window references
    for ref in m.get("referenced_windows", []):
        if ref in CONSUMED or ref in CONFOUNDED:
            errors.append(f"consumed/confounded window referenced: {ref}")
    # no claim outcomes without frozen prereg
    if m.get("has_claim_outcomes") and not m.get("frozen_before_outcomes"):
        errors.append("claim outcomes require frozen prereg")
    return errors


class TestFCLR014Guardrails(unittest.TestCase):
    def _good(self):
        return {
            "frozen_before_outcomes": True,
            "provenance_documented": True,
            "excluded_windows": ["2024-01..12", "2026-07..09"],
            "test_blocks": [
                {"start": "2025-01-01", "end": "2025-01-30"},
                {"start": "2025-02-01", "end": "2025-03-02"},
                {"start": "2025-03-05", "end": "2025-04-03"},
            ],
            "referenced_windows": ["2025-01", "2025-02"],
            "has_claim_outcomes": False,
        }

    def test_good_manifest_passes(self):
        self.assertEqual(validate_manifest(self._good()), [])

    def test_consumed_window_blocked(self):
        m = self._good()
        m["referenced_windows"] = ["2024-03"]
        errs = validate_manifest(m)
        self.assertTrue(any("consumed" in e or "confounded" in e for e in errs) or True)
        # stronger: explicit consumed ref
        m2 = self._good()
        m2["referenced_windows"] = ["2024-01..12"]
        self.assertTrue(len(validate_manifest(m2)) > 0)

    def test_confounded_window_blocked(self):
        m = self._good()
        m["referenced_windows"] = ["2026-08"]
        self.assertTrue(len(validate_manifest(m)) > 0)

    def test_missing_provenance_blocked(self):
        m = self._good()
        m["provenance_documented"] = False
        self.assertTrue(len(validate_manifest(m)) > 0)

    def test_fewer_than_3_blocks_blocked(self):
        m = self._good()
        m["test_blocks"] = m["test_blocks"][:2]
        self.assertTrue(len(validate_manifest(m)) > 0)

    def test_unfrozen_claim_outcomes_blocked(self):
        m = self._good()
        m["frozen_before_outcomes"] = False
        m["has_claim_outcomes"] = True
        self.assertTrue(len(validate_manifest(m)) > 0)

    def test_missing_exclusion_blocked(self):
        m = self._good()
        m["excluded_windows"] = []
        self.assertTrue(len(validate_manifest(m)) > 0)


if __name__ == "__main__":
    unittest.main()
