"""Tests for scripts/fclr022_gate4_blocker_resolution_evidence_preflight.py (read-only, no network)."""
from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
SCRIPT = REPO / "scripts" / "fclr022_gate4_blocker_resolution_evidence_preflight.py"
FORBIDDEN_TRUE = [
    '"satisfied": true',
    '"satisfaction_inferred": true',
    '"confirmatory_outcomes_go": true',
    '"resolution_ready": true',
    '"authorizes_confirmatory_outcomes": true',
]


def run_script(out_dir: Path, f21: Path, extra=()):
    cmd = [sys.executable, str(SCRIPT), "--fclr021", str(f21), "--out", str(out_dir), *extra]
    p = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
    doc_path = out_dir / "fclr022_gate4_blocker_resolution_evidence_preflight_latest.json"
    doc = json.loads(doc_path.read_text()) if doc_path.exists() else None
    return p, doc, doc_path


def write_json(path: Path, obj):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, indent=2), encoding="utf-8")
    return path


def gap(window, prerequisite, current_state="present_unverified", gate_class="provenance_manifest_evidence",
        evidence_ref=None, reason=None, missing_action_class=None):
    return {
        "window": window,
        "prerequisite": prerequisite,
        "current_state": current_state,
        "gate_class": gate_class,
        "evidence_ref": evidence_ref,
        "reason": reason or f"{prerequisite} blocked",
        "missing_action_class": missing_action_class or gate_class,
    }


def f21_doc(gaps):
    return {
        "artifact": "fclr021_gate4_blocker_resolution_checklist_validator",
        "draft_only": True, "no_confirmatory_outcomes": True, "exploratory_only": True,
        "no_network": True, "not_go_for_confirmatory_outcomes": True,
        "confirmatory_ready_now": False, "confirmatory_outcomes_go": False,
        "missing_action_warnings": gaps,
    }


class TestFclr022BlockerResolutionEvidencePreflight(unittest.TestCase):
    def _assert_draft_metadata(self, doc):
        self.assertTrue(doc["draft_only"])
        self.assertTrue(doc["no_confirmatory_outcomes"])
        self.assertTrue(doc["exploratory_only"])
        self.assertTrue(doc["no_network"])
        self.assertTrue(doc["not_go_for_confirmatory_outcomes"])
        self.assertFalse(doc["confirmatory_ready_now"])
        self.assertFalse(doc["confirmatory_outcomes_go"])
        self.assertFalse(doc["authorizes_confirmatory_outcomes"])
        self.assertFalse(doc["satisfied"])
        self.assertFalse(doc["satisfaction_inferred"])
        blob = json.dumps(doc)
        for f in FORBIDDEN_TRUE:
            self.assertNotIn(f, blob)

    def _assert_row_invariants(self, rows):
        for r in rows:
            self.assertFalse(r["resolution_ready"])
            self.assertIn("evidence_present", r)
            self.assertIn("read_state", r)
            self.assertIn("sha256", r)
            self.assertIn("bytes", r)
            self.assertIn("reason_copied_from_index", r)
            self.assertIn("missing_action_class", r)
            self.assertIn("evidence_ref", r)
            if not r["evidence_present"]:
                self.assertIsNone(r["sha256"])

    def test_evidence_presence_and_missing_path_checked(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td); out_dir = root / "out"
            present = root / "evidence.txt"
            present.write_text("ok", encoding="utf-8")
            gaps = [
                gap("w1", "p_present", evidence_ref=str(present)),
                gap("w1", "p_missing", evidence_ref=str(root / "nope.txt")),
                gap("w1", "p_none", evidence_ref=None),
            ]
            f21 = write_json(root / "f21.json", f21_doc(gaps))
            p, doc, latest = run_script(out_dir, f21)
            self.assertEqual(p.returncode, 0, p.stderr + p.stdout)
            self.assertTrue(latest.exists())
            self._assert_draft_metadata(doc)
            rows = doc["resolution_readiness_rows"]
            self.assertEqual(len(rows), 3)
            self._assert_row_invariants(rows)
            by_p = {r["prerequisite"]: r for r in rows}
            self.assertTrue(by_p["p_present"]["evidence_present"])
            self.assertEqual(by_p["p_present"]["read_state"], "ok")
            self.assertIsInstance(by_p["p_present"]["sha256"], str)
            self.assertGreater(by_p["p_present"]["bytes"], 0)
            self.assertFalse(by_p["p_present"]["resolution_ready"])
            self.assertFalse(by_p["p_missing"]["evidence_present"])
            self.assertEqual(by_p["p_missing"]["read_state"], "missing")
            self.assertIsNone(by_p["p_missing"]["sha256"])
            self.assertFalse(by_p["p_none"]["evidence_present"])
            self.assertEqual(by_p["p_none"]["read_state"], "no_path_cited")
            warnings = doc["resolution_readiness_warnings"]
            self.assertTrue(any(w["prerequisite"] == "p_missing" for w in warnings))
            self.assertTrue(any(w["prerequisite"] == "p_none" for w in warnings))

    def test_lfs_pointer_unreadable_not_fabricated_as_present(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td); out_dir = root / "out"
            lfs = root / "ptr.json"
            lfs.write_text("version https://git-lfs.github.com/spec/v1\noid sha256:abc\nsize 1\n")
            f21 = write_json(root / "f21.json", f21_doc([gap("w1", "p_lfs", evidence_ref=str(lfs))]))
            p, doc, _ = run_script(out_dir, f21)
            self.assertEqual(p.returncode, 0, p.stderr)
            row = doc["resolution_readiness_rows"][0]
            self.assertTrue(row["evidence_present"] is False)
            self.assertEqual(row["read_state"], "unavailable_pointer")
            self.assertIsNone(row["sha256"])
            self.assertFalse(row["resolution_ready"])
            self.assertTrue(any(w["type"] == "resolution_readiness_warning" for w in doc["resolution_readiness_warnings"]))

    def test_missing_unreadable_input_handling(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td); out_dir = root / "out"
            p, doc, _ = run_script(out_dir, root / "nope.json")
            self.assertEqual(p.returncode, 0, p.stderr)
            self._assert_draft_metadata(doc)
            self.assertNotEqual(doc["input_state"], "ok")
            self.assertTrue(any(w["type"] == "input_unavailable" for w in doc["resolution_readiness_warnings"]))
            self.assertEqual(doc["row_count"], 0)

    def test_no_fabrication_as_present_and_resolution_ready_always_false(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td); out_dir = root / "out"
            # even if a readable file exists, resolution_ready must remain false
            present = root / "evidence.json"
            present.write_text('{"ok": true}', encoding="utf-8")
            f21 = write_json(root / "f21.json", f21_doc([gap("w1", "p1", evidence_ref=str(present), reason="terms blocked")]))
            p, doc, _ = run_script(out_dir, f21)
            self.assertEqual(p.returncode, 0, p.stderr)
            row = doc["resolution_readiness_rows"][0]
            self.assertTrue(row["evidence_present"])
            self.assertFalse(row["resolution_ready"])
            self.assertEqual(row["reason_copied_from_index"], "terms blocked")
            self.assertFalse(doc["authorizes_confirmatory_outcomes"])
            self.assertFalse(doc["satisfied"])

    def test_draft_only_metadata_and_no_sealed_overwrite(self):
        real = REPO / "research_state" / "fclr021_local_audit" / "fclr021_gate4_blocker_resolution_checklist_validator_latest.json"
        if not real.exists():
            self.skipTest("real fclr021 latest not present")
        with tempfile.TemporaryDirectory() as td:
            out_dir = Path(td) / "out"
            p, doc, _ = run_script(out_dir, real)
            self.assertEqual(p.returncode, 0, p.stderr + p.stdout)
            self._assert_draft_metadata(doc)
            self._assert_row_invariants(doc["resolution_readiness_rows"])
            for r in doc["resolution_readiness_rows"]:
                self.assertFalse(r["resolution_ready"])
                self.assertFalse(r.get("satisfied", False))
            # outputs only in temp out dir
            self.assertTrue((out_dir / "fclr022_gate4_blocker_resolution_evidence_preflight_latest.json").exists())


if __name__ == "__main__":
    unittest.main()
