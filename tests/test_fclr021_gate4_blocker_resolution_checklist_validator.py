"""Tests for scripts/fclr021_gate4_blocker_resolution_checklist_validator.py (read-only, no network)."""
from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
SCRIPT = REPO / "scripts" / "fclr021_gate4_blocker_resolution_checklist_validator.py"
STATES = {"present_unverified", "present_blocker", "missing"}
FORBIDDEN_TRUE = {'"satisfied": true', '"satisfaction_inferred": true', '"confirmatory_outcomes_go": true'}


def run_script(out_dir: Path, f20: Path, extra=()):
    cmd = [sys.executable, str(SCRIPT), "--fclr020-json", str(f20), "--out-dir", str(out_dir), "--json-name", "idx.json", "--md-name", "idx.md", *extra]
    p = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
    doc = json.loads((out_dir / "idx.json").read_text()) if (out_dir / "idx.json").exists() else None
    return p, doc


def base_f20(windows):
    return {
        "artifact": "fclr020_gate4_readiness_action_matrix",
        "draft_only": True, "no_confirmatory_outcomes": True, "exploratory_only": True, "no_network": True,
        "not_go_for_confirmatory_outcomes": True,
        "window_action_matrices": windows,
    }


def prereq(state, read_state="ok", evidence_ref=None, blocker_note=None, note=None, verification_note=None, extra=None):
    d = {"state": state, "read_state": read_state, "evidence_ref": evidence_ref}
    if blocker_note is not None: d["blocker_note"] = blocker_note
    if note is not None: d["note"] = note
    if verification_note is not None: d["verification_note"] = verification_note
    if extra: d.update(extra)
    return d


def action_row(window_id, prerequisite_id, prerequisite_label, state, action_required, verification_command_or_check, evidence_ref=None, read_state="ok", blocker_note=None, note=None, verification_note=None):
    node = {"state": state, "read_state": read_state, "evidence_ref": evidence_ref,
            "prerequisite_id": prerequisite_id, "prerequisite_label": prerequisite_label,
            "blocker_note": blocker_note, "note": note, "verification_note": verification_note}
    row = {
        "window_id": window_id,
        "prerequisite_id": prerequisite_id,
        "prerequisite_label": prerequisite_label,
        "current_state": state,
        "read_state": read_state,
        "evidence_ref": evidence_ref,
        "evidence_snapshot": {"path": evidence_ref, "exists": bool(evidence_ref), "read_state": read_state},
        "blocker_or_missing_reason": blocker_note or f"state={state}",
        "action_required": list(action_required),
        "verification_command_or_check": list(verification_command_or_check),
        "authorizes_confirmatory_outcomes": False,
        "satisfied": False,
        "satisfaction_inferred": False,
    }
    return row


def window(window_id, rows, basis="test", start="2024-04-01", end="2024-09-30", index_summary_state="present_blocker"):
    return {
        "window_id": window_id, "start": start, "end": end, "basis": basis,
        "index_summary_state": index_summary_state,
        "confirmatory_outcomes_go": False,
        "action_rows": rows,
    }


TERMS_ACTION = ["Resolve manifest and terms evidence blockers (human/legal) with verifiable evidence (fabricated=false)."]
TERMS_CHECK = ["python scripts/fclr016_v5_admissibility_report.py --bogus --json", "python scripts/fclr016_v5_promotion_dryrun.py --bogus --json"]
PROV_ACTION = ["Ensure provenance manifest exists, readable, hash-reconciled, identity-verified bounded context."]
PROV_CHECK = ["test -f X && sha256sum X", "python3 -c \"import json; json.load(open('X')); print('json_ok')\"", "python scripts/fclr015_gate4_cache_input_manifest.py --help"]
ADMIT_ACTION = ["Resolve completeness/leakage/admissibility blockers with verifiable evidence."]
ADMIT_CHECK = ["python -m unittest discover tests -q", "python scripts/check_tracka_scope_registry_drift.py", "python scripts/tracka_resume_check.py"]
PREREG_ACTION = ["Create/freeze a fresh confirmatory preregistration BEFORE any confirmatory outcomes; DRAFT not sufficient."]
PREREG_CHECK = ["python scripts/run_funding_ablations.py", "python -m unittest discover tests -q"]
LEAK_ACTION = ["Verify leakage controls, purge/embargo, >=3 non-overlapping 30-day blocks / >=5 symbols sufficiency."]
LEAK_CHECK = ["python scripts/run_funding_ablations.py", "python -m unittest discover tests -q"]


class TestFclr021BlockerResolutionChecklistValidator(unittest.TestCase):
    def _write(self, path: Path, obj):
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(obj, indent=2), encoding="utf-8")
        return path

    def _assert_draft_metadata(self, doc):
        self.assertTrue(doc["draft_only"])
        self.assertTrue(doc["no_confirmatory_outcomes"])
        self.assertTrue(doc["exploratory_only"])
        self.assertTrue(doc["no_network"])
        self.assertTrue(doc["not_go_for_confirmatory_outcomes"])
        self.assertFalse(doc["confirmatory_ready_now"])
        self.assertFalse(doc["confirmatory_outcomes_go"])
        self.assertFalse(doc["decision"]["confirmatory_ready_now"])
        self.assertFalse(doc["decision"]["confirmatory_outcomes_go"])
        self.assertFalse(doc["authorizes_confirmatory_outcomes"])
        self.assertTrue(doc["caveats"]["no_prerequisite_marked_satisfied"])
        self.assertTrue(doc["caveats"]["no_satisfaction_inferred_from_absent_blocker"])
        self.assertTrue(doc["caveats"]["coverage_ok_is_text_coverage_not_resolution"])
        blob = json.dumps(doc)
        for f in FORBIDDEN_TRUE:
            self.assertNotIn(f, blob)

    def _collect_rows(self, doc):
        return doc.get("coverage_matrix") or []

    def _assert_row_invariants(self, rows):
        for r in rows:
            self.assertIn(r["current_state"], STATES)
            self.assertIn(r["gate_class"], list(__import__("scripts.fclr021_gate4_blocker_resolution_checklist_validator", fromlist=["GATE_CLASSES"]).GATE_CLASSES) + [None])
            self.assertFalse(r["authorizes_confirmatory_outcomes"])
            self.assertFalse(r["satisfied"])
            self.assertFalse(r["satisfaction_inferred"])
            self.assertIsInstance(r["coverage_ok"], bool)
            self.assertIsInstance(r["missing_markers"], list)
            self.assertIsInstance(r["verification_command_or_check"], list)
            self.assertTrue(r["verification_command_or_check"], f"missing checks: {r['prerequisite_id']}")
            if r["coverage_ok"]:
                self.assertIsNone(r["missing_action_class"])
                self.assertEqual(r["missing_markers"], [])
            else:
                self.assertIsNotNone(r["missing_action_class"])

    def _find_row(self, rows, pid, wid=None):
        for r in rows:
            if r["prerequisite_id"] == pid and (wid is None or r["window_id"] == wid):
                return r
        self.fail(f"row not found: {pid} {wid}")

    def test_coverage_class_validation_and_draft_metadata(self):
        rows = [
            action_row("w1", "manifest_terms_evidence.terms_evidence", "Terms/license evidence", "present_blocker", TERMS_ACTION, TERMS_CHECK, blocker_note="terms blocked"),
            action_row("w1", "manifest_terms_evidence.provenance_manifest", "Provenance/license manifest", "present_blocker", PROV_ACTION, PROV_CHECK, blocker_note="pm blocked"),
            action_row("w1", "admissibility_package_status.completeness_leakage_audit", "Completeness/leakage audit", "present_blocker", ADMIT_ACTION, ADMIT_CHECK, blocker_note="cl blocked"),
            action_row("w1", "fresh_frozen_prereg_before_outcomes_required", "Fresh frozen prereg", "missing", PREREG_ACTION, PREREG_CHECK, blocker_note="prereg missing"),
            action_row("w1", "leakage_sufficiency_gates", "Leakage/sufficiency gates", "present_unverified", LEAK_ACTION, LEAK_CHECK, verification_note="leak/suff unverified"),
        ]
        with tempfile.TemporaryDirectory() as td:
            root = Path(td); out_dir = root / "out"
            f20 = self._write(root / "f20.json", base_f20([window("w1", rows)]))
            p, doc = run_script(out_dir, f20)
            self.assertEqual(p.returncode, 0, p.stderr + p.stdout)
            self._assert_draft_metadata(doc)
            rows_out = self._collect_rows(doc)
            self._assert_row_invariants(rows_out)
            self.assertTrue((out_dir / "fclr021_gate4_blocker_resolution_checklist_validator_latest.json").exists())
            self.assertTrue((out_dir / "fclr021_gate4_blocker_resolution_checklist_validator_latest.md").exists())
            # all five gate classes covered in this well-formed fixture
            for r in rows_out:
                self.assertTrue(r["coverage_ok"], f"expected covered: {r['prerequisite_id']} missing={r['missing_markers']}")
            self.assertEqual(doc["coverage_summary"]["total_rows"], 5)
            self.assertEqual(doc["coverage_summary"]["covered_rows"], 5)
            self.assertEqual(doc["coverage_summary"]["gap_rows"], 0)
            self.assertEqual(doc["missing_action_warnings"], [])

    def test_missing_action_warning_emission(self):
        # terms row whose action text lacks required markers -> coverage gap
        bad_terms_action = ["Do something vague about terms."]  # missing human/legal, fabricated=false, verifiable evidence
        rows = [
            action_row("w1", "manifest_terms_evidence.terms_evidence", "Terms/license evidence", "present_blocker", bad_terms_action, TERMS_CHECK, blocker_note="terms blocked"),
        ]
        with tempfile.TemporaryDirectory() as td:
            root = Path(td); out_dir = root / "out"
            f20 = self._write(root / "f20.json", base_f20([window("w1", rows)]))
            p, doc = run_script(out_dir, f20)
            self.assertEqual(p.returncode, 0, p.stderr)
            r = self._find_row(self._collect_rows(doc), "manifest_terms_evidence.terms_evidence", "w1")
            self.assertFalse(r["coverage_ok"])
            self.assertEqual(r["missing_action_class"], "terms_legal_evidence_resolution")
            self.assertTrue(len(r["missing_markers"]) > 0)
            warnings = doc["missing_action_warnings"]
            self.assertTrue(any(w["prerequisite"] == "manifest_terms_evidence.terms_evidence" for w in warnings))
            self.assertTrue(any("coverage gap" in w["warning"] for w in warnings))

    def test_fresh_frozen_prereg_missing_coverage_gap(self):
        rows = [
            action_row("w1", "fresh_frozen_prereg_before_outcomes_required", "Fresh frozen prereg", "missing",
                       ["A DRAFT prereg skeleton is not sufficient."], ["test ! -f research_state/NO_SUCH_FRESH_FROZEN_PREREG"],
                       blocker_note="fresh frozen prereg missing"),
        ]
        with tempfile.TemporaryDirectory() as td:
            root = Path(td); out_dir = root / "out"
            f20 = self._write(root / "f20.json", base_f20([window("w1", rows)]))
            p, doc = run_script(out_dir, f20)
            self.assertEqual(p.returncode, 0, p.stderr)
            r = self._find_row(self._collect_rows(doc), "fresh_frozen_prereg_before_outcomes_required", "w1")
            self.assertEqual(r["current_state"], "missing")
            self.assertFalse(r["coverage_ok"])
            self.assertEqual(r["missing_action_class"], "fresh_frozen_prereg_before_outcomes")
            self.assertFalse(r["satisfied"])
            self.assertFalse(r["satisfaction_inferred"])

    def test_v5_blocker_propagation_and_no_satisfaction_inference(self):
        rows = [
            action_row("w1", "manifest_terms_evidence.terms_evidence", "Terms/license evidence", "present_blocker",
                       TERMS_ACTION, TERMS_CHECK, blocker_note="terms_status=EXPLICIT_BLOCKER_UNRESOLVED"),
            action_row("w1", "identity_provenance_range", "Identity/provenance range", "present_unverified",
                       PROV_ACTION, PROV_CHECK, verification_note="prov unverified"),
        ]
        with tempfile.TemporaryDirectory() as td:
            root = Path(td); out_dir = root / "out"
            f20 = self._write(root / "f20.json", base_f20([window("w1", rows)]))
            p, doc = run_script(out_dir, f20)
            self.assertEqual(p.returncode, 0, p.stderr)
            terms = self._find_row(self._collect_rows(doc), "manifest_terms_evidence.terms_evidence", "w1")
            self.assertEqual(terms["current_state"], "present_blocker")
            self.assertFalse(terms["satisfied"])
            self.assertFalse(terms["satisfaction_inferred"])
            prov = self._find_row(self._collect_rows(doc), "identity_provenance_range", "w1")
            self.assertEqual(prov["current_state"], "present_unverified")
            self.assertFalse(prov["satisfied"])
            self.assertFalse(prov["satisfaction_inferred"])

    def test_lfs_unreadable_and_missing_input_handling(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td); out_dir = root / "out"
            # evidence_ref citing an LFS-like pointer file
            (root / "lfs.json").write_text("version https://git-lfs.github.com/spec/v1\noid sha256:abc\nsize 1\n")
            rows = [
                action_row("w1", "manifest_terms_evidence.terms_evidence", "Terms/license evidence", "present_blocker",
                           TERMS_ACTION, TERMS_CHECK, evidence_ref=str(root / "lfs.json"), blocker_note="terms blocked"),
            ]
            f20 = self._write(root / "f20.json", base_f20([window("w1", rows)]))
            p, doc = run_script(out_dir, f20)
            self.assertEqual(p.returncode, 0, p.stderr)
            r = self._find_row(self._collect_rows(doc), "manifest_terms_evidence.terms_evidence", "w1")
            self.assertEqual(r["evidence_snapshot"]["read_state"], "unavailable_pointer")
            self.assertFalse(r["satisfied"])
            # missing input file
            p2, doc2 = run_script(root / "out2", root / "nope.json")
            self.assertEqual(p2.returncode, 0, p2.stderr)
            self.assertIn("error", doc2)
            self.assertTrue(doc2["not_go_for_confirmatory_outcomes"])
            self.assertFalse(doc2["confirmatory_outcomes_go"])

    def test_no_sealed_overwrite_and_real_fclr020_draft_flags(self):
        real_latest = REPO / "research_state" / "fclr020_local_audit" / "fclr020_gate4_readiness_action_matrix_latest.json"
        if not real_latest.exists():
            self.skipTest("real fclr020 latest not present")
        with tempfile.TemporaryDirectory() as td:
            out_dir = Path(td) / "out"
            p, doc = run_script(out_dir, real_latest)
            self.assertEqual(p.returncode, 0, p.stderr + p.stdout)
            self._assert_draft_metadata(doc)
            rows = self._collect_rows(doc)
            self._assert_row_invariants(rows)
            self.assertGreaterEqual(len(rows), 1)
            for r in rows:
                self.assertFalse(r["authorizes_confirmatory_outcomes"])
                self.assertFalse(r["satisfied"])
                self.assertFalse(r["satisfaction_inferred"])


if __name__ == "__main__":
    unittest.main()
