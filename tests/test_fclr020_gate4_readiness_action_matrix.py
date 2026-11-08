"""Tests for scripts/fclr020_gate4_readiness_action_matrix.py (read-only, no network)."""
from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
SCRIPT = REPO / "scripts" / "fclr020_gate4_readiness_action_matrix.py"
STATES = {"present_unverified", "present_blocker", "missing"}
FORBIDDEN_STATE_VALUES = {"satisfied", "pass", "go", "authorized", "ready_true"}


def run_script(out_dir: Path, f19: Path, extra=()):
    cmd = [sys.executable, str(SCRIPT), "--fclr019-json", str(f19), "--out-dir", str(out_dir), "--json-name", "idx.json", "--md-name", "idx.md", *extra]
    p = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
    doc = json.loads((out_dir / "idx.json").read_text()) if (out_dir / "idx.json").exists() else None
    return p, doc


def base_f19(candidates):
    return {
        "artifact": "fclr019_gate4_evidence_bundle_index",
        "draft_only": True, "no_confirmatory_outcomes": True, "exploratory_only": True, "no_network": True,
        "not_go_for_confirmatory_outcomes": True,
        "candidate_indices": candidates,
    }


def prereq(state, read_state="ok", evidence_ref=None, blocker_note=None, note=None, verification_note=None, extra=None):
    d = {"state": state, "read_state": read_state, "evidence_ref": evidence_ref}
    if blocker_note is not None: d["blocker_note"] = blocker_note
    if note is not None: d["note"] = note
    if verification_note is not None: d["verification_note"] = verification_note
    if extra: d.update(extra)
    return d


def candidate(window_id, prov_state, terms_state, pm_state, cl_state, draft_state, v5win_state, ff_state, leak_state, basis="test"):
    return {
        "window_id": window_id, "start": "2024-04-01", "end": "2024-09-30", "basis": basis,
        "index_summary_state": "present_blocker" if "present_blocker" in [prov_state, terms_state, pm_state, cl_state, draft_state, v5win_state, ff_state, leak_state] else ("missing" if "missing" in [prov_state, terms_state, pm_state, cl_state, draft_state, v5win_state, ff_state, leak_state] else "present_unverified"),
        "confirmatory_outcomes_go": False,
        "checklist": {
            "identity_provenance_range": prereq(prov_state, blocker_note="prov blocked" if prov_state=="present_blocker" else None, verification_note="prov unverified" if prov_state=="present_unverified" else None),
            "manifest_terms_evidence": {
                "summary_state": "present_blocker" if "present_blocker" in [pm_state, terms_state] else ("missing" if "missing" in [pm_state, terms_state] else "present_unverified"),
                "provenance_manifest": prereq(pm_state, blocker_note="pm blocked" if pm_state=="present_blocker" else None),
                "terms_evidence": prereq(terms_state, blocker_note="terms blocked" if terms_state=="present_blocker" else None),
            },
            "admissibility_package_status": {
                "summary_state": "present_blocker" if "present_blocker" in [cl_state, draft_state, v5win_state] else ("missing" if "missing" in [cl_state, draft_state, v5win_state] else "present_unverified"),
                "completeness_leakage_audit": prereq(cl_state, blocker_note="cl blocked" if cl_state=="present_blocker" else None),
                "confirmatory_prereg_draft_ref": prereq(draft_state, blocker_note="draft/not frozen" if draft_state=="present_blocker" else None),
                "v5_window_terms_state_from_fclr018": prereq(v5win_state, read_state="from_fclr018", evidence_ref="fclr018.window.v5_terms_blocker_state", blocker_note="v5 blocked" if v5win_state=="present_blocker" else None),
            },
            "fresh_frozen_prereg_before_outcomes_required": prereq(ff_state, read_state="policy_check", note="fresh frozen prereg missing" if ff_state=="missing" else None),
            "leakage_sufficiency_gates": prereq(leak_state, read_state="from_fclr018", blocker_note="leak/suff blocked" if leak_state=="present_blocker" else None, verification_note="leak/suff unverified" if leak_state=="present_unverified" else None),
        },
    }


class TestFclr020ReadinessActionMatrix(unittest.TestCase):
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
        self.assertTrue(doc["caveats"]["no_prerequisite_marked_satisfied"])
        self.assertTrue(doc["caveats"]["no_satisfaction_inferred_from_absent_blocker"])

    def _collect_rows(self, doc):
        rows = []
        for w in doc.get("window_action_matrices") or []:
            rows.extend(w.get("action_rows") or [])
        return rows

    def _assert_row_invariants(self, rows):
        for r in rows:
            self.assertIn(r["current_state"], STATES)
            self.assertFalse(r["authorizes_confirmatory_outcomes"])
            self.assertFalse(r["satisfied"])
            self.assertFalse(r["satisfaction_inferred"])
            self.assertIsInstance(r["action_required"], list)
            self.assertIsInstance(r["verification_command_or_check"], list)
            self.assertTrue(r["action_required"], f"missing actions: {r['prerequisite_id']}")
            self.assertTrue(r["verification_command_or_check"], f"missing checks: {r['prerequisite_id']}")

    def _find_row(self, rows, pid, wid=None):
        for r in rows:
            if r["prerequisite_id"] == pid and (wid is None or r["window_id"] == wid):
                return r
        self.fail(f"row not found: {pid} {wid}")

    def test_state_to_action_mapping_and_draft_metadata(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td); out_dir = root / "out"
            f19 = self._write(root / "f19.json", base_f19([
                candidate("w_block", "present_blocker","present_blocker","present_blocker","present_blocker","present_blocker","present_blocker","missing","present_blocker"),
                candidate("w_unv", "present_unverified","present_unverified","present_unverified","present_unverified","present_unverified","present_unverified","missing","present_unverified"),
                candidate("w_miss", "missing","missing","missing","missing","missing","missing","missing","missing"),
            ]))
            p, doc = run_script(out_dir, f19)
            self.assertEqual(p.returncode, 0, p.stderr + p.stdout)
            self._assert_draft_metadata(doc)
            rows = self._collect_rows(doc)
            self._assert_row_invariants(rows)
            self.assertTrue((out_dir / "fclr020_gate4_readiness_action_matrix_latest.json").exists())
            # blocked vs unverified provenance gets different actions
            rb = self._find_row(rows, "identity_provenance_range", "w_block")
            ru = self._find_row(rows, "identity_provenance_range", "w_unv")
            self.assertEqual(rb["current_state"], "present_blocker")
            self.assertEqual(ru["current_state"], "present_unverified")
            self.assertNotEqual(" ".join(rb["action_required"]), " ".join(ru["action_required"]))
            self.assertIn("Human review required", " ".join(ru["action_required"]))
            # no forbidden satisfied markers in states/flags
            blob = json.dumps(doc)
            self.assertNotIn('"satisfied": true', blob)
            self.assertNotIn('"satisfaction_inferred": true', blob)
            self.assertNotIn('"confirmatory_outcomes_go": true', blob)

    def test_fresh_frozen_prereg_missing_action_present(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td); out_dir = root / "out"
            f19 = self._write(root / "f19.json", base_f19([candidate("w1","present_unverified","present_blocker","present_blocker","present_blocker","present_blocker","present_blocker","missing","present_unverified")]))
            p, doc = run_script(out_dir, f19)
            self.assertEqual(p.returncode, 0, p.stderr)
            ff = self._find_row(self._collect_rows(doc), "fresh_frozen_prereg_before_outcomes_required", "w1")
            self.assertEqual(ff["current_state"], "missing")
            text = " ".join(ff["action_required"])
            self.assertIn("fresh confirmatory preregistration BEFORE any confirmatory outcomes", text)
            self.assertIn("NOT sufficient", text)
            self.assertFalse(ff["authorizes_confirmatory_outcomes"])

    def test_v5_blocker_propagation_and_no_satisfaction_inference(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td); out_dir = root / "out"
            # even with some unverified states, terms/admissibility blockers must keep actions explicit
            f19 = self._write(root / "f19.json", base_f19([candidate("w1","present_unverified","present_blocker","present_blocker","present_blocker","present_blocker","present_blocker","missing","present_unverified")]))
            p, doc = run_script(out_dir, f19)
            self.assertEqual(p.returncode, 0, p.stderr)
            rows = self._collect_rows(doc)
            terms = self._find_row(rows, "manifest_terms_evidence.terms_evidence", "w1")
            self.assertEqual(terms["current_state"], "present_blocker")
            self.assertIn("Human/legal action required", " ".join(terms["action_required"]))
            # absent blocker string must not produce satisfied state (we control via fixture: unverified has no blocker_note)
            prov = self._find_row(rows, "identity_provenance_range", "w1")
            self.assertEqual(prov["current_state"], "present_unverified")
            self.assertFalse(prov["satisfied"])
            self.assertFalse(prov["satisfaction_inferred"])

    def test_lfs_unreadable_and_missing_input_handling(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td); out_dir = root / "out"
            # fixture row cites an LFS-like path reference in evidence_ref and missing file
            c = candidate("w1","missing","missing","missing","missing","missing","missing","missing","missing")
            c["checklist"]["manifest_terms_evidence"]["terms_evidence"]["evidence_ref"] = str(root / "lfs.json")
            (root / "lfs.json").write_text("version https://git-lfs.github.com/spec/v1\noid sha256:abc\nsize 1\n")
            f19 = self._write(root / "f19.json", base_f19([c]))
            p, doc = run_script(out_dir, f19)
            self.assertEqual(p.returncode, 0, p.stderr)
            self._assert_draft_metadata(doc)
            terms = self._find_row(self._collect_rows(doc), "manifest_terms_evidence.terms_evidence", "w1")
            self.assertEqual(terms["evidence_snapshot"]["read_state"], "unavailable_pointer")
            self.assertFalse(terms["satisfied"])
            # missing input file
            p2, doc2 = run_script(root / "out2", root / "nope.json")
            self.assertEqual(p2.returncode, 0, p2.stderr)
            self.assertIn("error", doc2)
            self.assertTrue(doc2["not_go_for_confirmatory_outcomes"])
            self.assertFalse(doc2["confirmatory_outcomes_go"])

    def test_no_sealed_overwrite_and_real_fclr019_draft_flags(self):
        # run against real latest if present, but only into a temp out dir (no sealed overwrite)
        real_latest = REPO / "research_state" / "fclr019_local_audit" / "fclr019_gate4_evidence_bundle_index_latest.json"
        if not real_latest.exists():
            self.skipTest("real fclr019 latest not present")
        with tempfile.TemporaryDirectory() as td:
            out_dir = Path(td) / "out"
            p, doc = run_script(out_dir, real_latest)
            self.assertEqual(p.returncode, 0, p.stderr + p.stdout)
            self._assert_draft_metadata(doc)
            rows = self._collect_rows(doc)
            self._assert_row_invariants(rows)
            self.assertGreaterEqual(len(doc.get("window_action_matrices") or []), 1)
            # every window explicitly non-GO
            for w in doc.get("window_action_matrices") or []:
                self.assertFalse(w["confirmatory_outcomes_go"])


if __name__ == "__main__":
    unittest.main()
