"""Tests for scripts/fclr019_gate4_evidence_bundle_index.py (read-only, no network)."""
from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
SCRIPT = REPO / "scripts" / "fclr019_gate4_evidence_bundle_index.py"
STATES = {"present_unverified", "present_blocker", "missing"}


def run_script(out_dir: Path, f18: Path, extra=()):
    cmd = [sys.executable, str(SCRIPT), "--fclr018-json", str(f18), "--out-dir", str(out_dir), "--json-name", "idx.json", "--md-name", "idx.md", *extra]
    p = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
    doc = json.loads((out_dir / "idx.json").read_text()) if (out_dir / "idx.json").exists() else None
    return p, doc


def base_f18(windows):
    return {
        "artifact": "fclr018_gate4_prereg_readiness_matrix",
        "prereg_status": "DRAFT_NOT_FROZEN",
        "no_confirmatory_outcomes": True,
        "exploratory_only": True,
        "no_network": True,
        "candidate_windows": windows,
    }


def evidenced_window():
    return {
        "window_id": "cand_2024_04_09_evidenced",
        "start": "2024-04-01", "end": "2024-09-30", "basis": "fclr015_evidenced_bounded",
        "provenance_status": "IDENTITY_VERIFIED_BOUNDED_FCLR015",
        "confirmatory_eligibility": "INELIGIBLE_EXPLORATORY",
        "confirmatory_eligible_now": False,
        "confirmatory_ineligibility_reasons": ["v5_terms_blocker_unresolved_all_go_false"],
        "calendar_coverage_all_symbols_complete": True,
        "block_count_gate_ge_3": True,
        "v5_terms_blocker_state": {"all_go": False, "confirmatory_outcomes_permitted": False, "fabricated": False, "terms_status": "EXPLICIT_BLOCKER_UNRESOLVED"},
    }


def unverified_window():
    return {
        "window_id": "cand_2024_10_12_local_exploratory",
        "start": "2024-10-01", "end": "2024-12-31", "basis": "local_cache_contiguous_unprovenanced",
        "provenance_status": "UNVERIFIED",
        "confirmatory_eligibility": "INELIGIBLE_EXPLORATORY",
        "confirmatory_eligible_now": False,
        "confirmatory_ineligibility_reasons": ["v5_terms_blocker_unresolved_all_go_false", "provenance_not_identity_verified_bounded_fclr015"],
        "calendar_coverage_all_symbols_complete": False,
        "block_count_gate_ge_3": False,
        "v5_terms_blocker_state": {"all_go": False, "confirmatory_outcomes_permitted": False, "fabricated": False, "terms_status": "EXPLICIT_BLOCKER_UNRESOLVED"},
    }


class TestFclr019EvidenceBundleIndex(unittest.TestCase):
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
        self.assertFalse(doc["decision"]["confirmatory_ready_now"])
        self.assertFalse(doc["decision"]["confirmatory_outcomes_go"])
        self.assertTrue(doc["caveats"]["no_prerequisite_marked_satisfied"])

    def _collect_states(self, obj):
        out = []
        if isinstance(obj, dict):
            if obj.get("state") in STATES:
                out.append(obj["state"])
            for v in obj.values():
                out.extend(self._collect_states(v))
        elif isinstance(obj, list):
            for v in obj:
                out.extend(self._collect_states(v))
        return out

    def test_draft_metadata_and_no_confirmatory(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td); out_dir = root / "out"
            f18 = self._write(root / "f18.json", base_f18([evidenced_window(), unverified_window()]))
            # point v5 refs to missing to exercise missing states
            p, doc = run_script(out_dir, f18, ["--terms-evidence", "missing_terms.json", "--provenance-manifest", "missing_pm.json", "--completeness-leakage-audit", "missing_cl.json", "--confirmatory-prereg-draft", "missing_pr.json", "--fclr015-dir", str(root / "no_f15"), "--fclr016-dir", str(root / "no_f16")])
            self.assertEqual(p.returncode, 0, p.stderr + p.stdout)
            self._assert_draft_metadata(doc)
            self.assertEqual(doc["candidate_indices"][0]["confirmatory_outcomes_go"], False)
            self.assertTrue(all(s in STATES for s in self._collect_states(doc)))
            self.assertTrue((out_dir / "fclr019_gate4_evidence_bundle_index_latest.json").exists())

    def test_missing_and_lfs_pointer_states(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td); out_dir = root / "out"
            f18 = self._write(root / "f18.json", base_f18([evidenced_window()]))
            lfs = root / "lfs.json"
            lfs.write_text("version https://git-lfs.github.com/spec/v1\noid sha256:abc\nsize 1\n", encoding="utf-8")
            p, doc = run_script(out_dir, f18, ["--terms-evidence", str(lfs.relative_to(REPO) if False else lfs), "--provenance-manifest", str(root / "missing.json"), "--completeness-leakage-audit", str(root / "missing2.json"), "--confirmatory-prereg-draft", str(root / "missing3.json"), "--fclr015-dir", str(root / "no"), "--fclr016-dir", str(root / "no")])
            self.assertEqual(p.returncode, 0, p.stderr)
            self.assertEqual(doc["global_v5_evidence"]["terms_evidence"]["state"], "missing")
            self.assertEqual(doc["global_v5_evidence"]["terms_evidence"]["read_state"], "unavailable_pointer")
            self.assertEqual(doc["global_v5_evidence"]["provenance_manifest"]["state"], "missing")
            self.assertEqual(doc["fresh_frozen_prereg_before_outcomes_required"]["state"], "missing")

    def test_v5_blocker_propagation_and_provenance_labeling(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td); out_dir = root / "out"
            f18 = self._write(root / "f18.json", base_f18([evidenced_window(), unverified_window()]))
            terms = self._write(root / "terms.json", {"status": "EXPLICIT_BLOCKER_UNRESOLVED", "fabricated": False, "confirmatory_provenance_go": False})
            pm = self._write(root / "pm.json", {"confirmatory_provenance_go": False, "admissibility_complete": False, "license_terms": {"status": "EXPLICIT_BLOCKER_UNRESOLVED"}})
            cl = self._write(root / "cl.json", {"blockers_remaining": ["terms unresolved"], "completeness": {"ok": True}, "leakage_window_checks": {"ok": True}})
            pr = self._write(root / "pr.json", {"draft": True, "frozen_before_outcomes": False, "confirmatory_claim_go": "NO_GO"})
            f15dir = root / "f15"; f15dir.mkdir()
            self._write(f15dir / "probe_2024_04_09.json", {"ok": True})
            p, doc = run_script(out_dir, f18, ["--terms-evidence", str(terms), "--provenance-manifest", str(pm), "--completeness-leakage-audit", str(cl), "--confirmatory-prereg-draft", str(pr), "--fclr015-dir", str(f15dir), "--fclr016-dir", str(root / "f16")])
            self.assertEqual(p.returncode, 0, p.stderr)
            self.assertEqual(doc["global_v5_evidence"]["terms_evidence"]["state"], "present_blocker")
            ev = doc["candidate_indices"][0]
            uv = doc["candidate_indices"][1]
            self.assertEqual(ev["window_id"], "cand_2024_04_09_evidenced")
            self.assertEqual(ev["checklist"]["identity_provenance_range"]["state"], "present_unverified")
            self.assertEqual(ev["checklist"]["admissibility_package_status"]["v5_window_terms_state_from_fclr018"]["state"], "present_blocker")
            self.assertEqual(ev["index_summary_state"], "present_blocker")
            self.assertFalse(ev["confirmatory_outcomes_go"])
            self.assertEqual(uv["checklist"]["identity_provenance_range"]["state"], "present_blocker")
            self.assertIn("UNVERIFIED", uv["checklist"]["identity_provenance_range"]["blocker_note"])

    def test_fresh_frozen_prereg_missing_and_no_satisfied_states(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td); out_dir = root / "out"
            f18 = self._write(root / "f18.json", base_f18([evidenced_window()]))
            p, doc = run_script(out_dir, f18, ["--terms-evidence", "x", "--provenance-manifest", "y", "--completeness-leakage-audit", "z", "--confirmatory-prereg-draft", "w", "--fclr015-dir", str(root / "f15"), "--fclr016-dir", str(root / "f16")])
            self.assertEqual(p.returncode, 0, p.stderr)
            ff = doc["candidate_indices"][0]["checklist"]["fresh_frozen_prereg_before_outcomes_required"]
            self.assertEqual(ff["state"], "missing")
            # ensure index never emits "satisfied"/"go"/"pass" as a prerequisite state
            blob = json.dumps(doc)
            self.assertNotIn('"state": "satisfied"', blob)
            self.assertNotIn('"state": "pass"', blob)
            self.assertNotIn('"confirmatory_outcomes_go": true', blob.lower().replace(' ', ''))

    def test_unreadable_fclr018_reports_error_without_network_or_go(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td); out_dir = root / "out"
            bad = root / "f18.json"; bad.write_text("{not json", encoding="utf-8")
            p, doc = run_script(out_dir, bad, ["--terms-evidence", "x", "--provenance-manifest", "y", "--completeness-leakage-audit", "z", "--confirmatory-prereg-draft", "w"])
            self.assertEqual(p.returncode, 0, p.stderr)
            self.assertIn("error", doc)
            self.assertTrue(doc["draft_only"])
            self.assertTrue(doc["not_go_for_confirmatory_outcomes"])
            self.assertEqual(doc["candidate_indices"], [])


if __name__ == "__main__":
    unittest.main()
