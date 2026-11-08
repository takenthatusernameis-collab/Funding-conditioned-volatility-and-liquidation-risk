"""FCLR-016 v5 admissibility validator tests (deterministic, read-only, no network/outcomes)."""
import json, subprocess, sys, tempfile, unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
VALIDATOR = REPO / "scripts" / "fclr016_validate_v5_admissibility.py"
AUDIT = REPO / "research_state/fclr016_local_audit"


class TestFclr016V5Validator(unittest.TestCase):
    def _run(self, *args):
        p = subprocess.run([sys.executable, str(VALIDATOR), *args], capture_output=True, text=True)
        return p.returncode, json.loads(p.stdout)

    def test_current_blocked_package_validates_and_not_go(self):
        rc, out = self._run(
            "--provenance-manifest", str(AUDIT / "fclr016_v5_provenance_license_manifest_20261108T014405Z.json"),
            "--completeness-audit", str(AUDIT / "fclr016_v5_completeness_leakage_audit_20261108T014405Z.json"),
            "--terms-evidence", str(AUDIT / "fclr016_v5_terms_evidence_BLOCKED_20261108T014835Z.json"),
            "--prereg-draft", str(AUDIT / "fclr016_v5_confirmatory_prereg_DRAFT_20261108T014835Z.json"),
        )
        self.assertEqual(rc, 0)
        self.assertTrue(out["ok"])
        self.assertFalse(out["all_go"])
        self.assertFalse(out["confirmatory_outcomes_permitted"])
        self.assertIn("hashes", out)

    def test_expect_go_refused_on_blocked_package(self):
        p = subprocess.run([sys.executable, str(VALIDATOR),
            "--provenance-manifest", str(AUDIT / "fclr016_v5_provenance_license_manifest_20261108T014405Z.json"),
            "--completeness-audit", str(AUDIT / "fclr016_v5_completeness_leakage_audit_20261108T014405Z.json"),
            "--terms-evidence", str(AUDIT / "fclr016_v5_terms_evidence_BLOCKED_20261108T014835Z.json"),
            "--prereg-draft", str(AUDIT / "fclr016_v5_confirmatory_prereg_DRAFT_20261108T014835Z.json"),
            "--expect-go"], capture_output=True, text=True)
        self.assertNotEqual(p.returncode, 0)
        self.assertIn("expect-go", p.stdout)

    def test_draft_cannot_claim_frozen(self):
        with tempfile.TemporaryDirectory() as td:
            td = Path(td)
            for src in ["fclr016_v5_provenance_license_manifest_20261108T014405Z.json",
                        "fclr016_v5_completeness_leakage_audit_20261108T014405Z.json",
                        "fclr016_v5_terms_evidence_BLOCKED_20261108T014835Z.json",
                        "fclr016_v5_confirmatory_prereg_DRAFT_20261108T014835Z.json"]:
                (td/src).write_bytes((AUDIT/src).read_bytes())
            pr = json.loads((td/"fclr016_v5_confirmatory_prereg_DRAFT_20261108T014835Z.json").read_text())
            pr["frozen_before_outcomes"] = True
            (td/"fclr016_v5_confirmatory_prereg_DRAFT_20261108T014835Z.json").write_text(json.dumps(pr))
            p = subprocess.run([sys.executable, str(VALIDATOR),
                "--provenance-manifest", str(td/"fclr016_v5_provenance_license_manifest_20261108T014405Z.json"),
                "--completeness-audit", str(td/"fclr016_v5_completeness_leakage_audit_20261108T014405Z.json"),
                "--terms-evidence", str(td/"fclr016_v5_terms_evidence_BLOCKED_20261108T014835Z.json"),
                "--prereg-draft", str(td/"fclr016_v5_confirmatory_prereg_DRAFT_20261108T014835Z.json")], capture_output=True, text=True)
            self.assertNotEqual(p.returncode, 0)
            self.assertIn("frozen_before_outcomes", p.stdout)


    def test_resolved_terms_without_human_review_fields_refused(self):
        with tempfile.TemporaryDirectory() as td:
            td = Path(td)
            for src in ["fclr016_v5_provenance_license_manifest_20261108T014405Z.json",
                        "fclr016_v5_completeness_leakage_audit_20261108T014405Z.json",
                        "fclr016_v5_terms_evidence_BLOCKED_20261108T014835Z.json",
                        "fclr016_v5_confirmatory_prereg_DRAFT_20261108T014835Z.json"]:
                (td/src).write_bytes((AUDIT/src).read_bytes())
            te = json.loads((td/"fclr016_v5_terms_evidence_BLOCKED_20261108T014835Z.json").read_text())
            te.update({"status": "RESOLVED_VERIFIED", "fabricated": False, "reviewer_role": "automated agent only"})
            (td/"fclr016_v5_terms_evidence_BLOCKED_20261108T014835Z.json").write_text(json.dumps(te))
            p = subprocess.run([sys.executable, str(VALIDATOR),
                "--provenance-manifest", str(td/"fclr016_v5_provenance_license_manifest_20261108T014405Z.json"),
                "--completeness-audit", str(td/"fclr016_v5_completeness_leakage_audit_20261108T014405Z.json"),
                "--terms-evidence", str(td/"fclr016_v5_terms_evidence_BLOCKED_20261108T014835Z.json"),
                "--prereg-draft", str(td/"fclr016_v5_confirmatory_prereg_DRAFT_20261108T014835Z.json")], capture_output=True, text=True)
            self.assertNotEqual(p.returncode, 0)
            self.assertTrue("terms_url_reviewed" in p.stdout or "reviewer_role" in p.stdout or "agent-only" in p.stdout)

    def test_terms_hash_ref_mismatch_refused_when_present(self):
        with tempfile.TemporaryDirectory() as td:
            td = Path(td)
            for src in ["fclr016_v5_provenance_license_manifest_20261108T014405Z.json",
                        "fclr016_v5_completeness_leakage_audit_20261108T014405Z.json",
                        "fclr016_v5_terms_evidence_BLOCKED_20261108T014835Z.json",
                        "fclr016_v5_confirmatory_prereg_DRAFT_20261108T014835Z.json"]:
                (td/src).write_bytes((AUDIT/src).read_bytes())
            pr = json.loads((td/"fclr016_v5_confirmatory_prereg_DRAFT_20261108T014835Z.json").read_text())
            pr.setdefault("admissibility_refs_sha256", {})["terms_evidence"] = "0" * 64
            (td/"fclr016_v5_confirmatory_prereg_DRAFT_20261108T014835Z.json").write_text(json.dumps(pr))
            p = subprocess.run([sys.executable, str(VALIDATOR),
                "--provenance-manifest", str(td/"fclr016_v5_provenance_license_manifest_20261108T014405Z.json"),
                "--completeness-audit", str(td/"fclr016_v5_completeness_leakage_audit_20261108T014405Z.json"),
                "--terms-evidence", str(td/"fclr016_v5_terms_evidence_BLOCKED_20261108T014835Z.json"),
                "--prereg-draft", str(td/"fclr016_v5_confirmatory_prereg_DRAFT_20261108T014835Z.json")], capture_output=True, text=True)
            self.assertNotEqual(p.returncode, 0)
            self.assertIn("terms_evidence", p.stdout)
