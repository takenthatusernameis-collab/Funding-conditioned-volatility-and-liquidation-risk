"""FCLR-016 Gate 4 v5: admissibility guard/matrix tests (deterministic, no network/outcomes)."""
import json, sys, tempfile, unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "scripts"))
from run_funding_ablations import check_confirmatory_provenance, check_admissibility_package

AUDIT = REPO / "research_state/fclr016_local_audit"
PM = AUDIT / "fclr016_v5_provenance_license_manifest_20261108T014405Z.json"
CA = AUDIT / "fclr016_v5_completeness_leakage_audit_20261108T014405Z.json"
TE = AUDIT / "fclr016_v5_terms_evidence_BLOCKED_20261108T014835Z.json"
PR = AUDIT / "fclr016_v5_confirmatory_prereg_DRAFT_20261108T014835Z.json"


def _base_v5(**overrides):
    m = {
        "artifact": "fclr016_v5_provenance_license_manifest",
        "schema_version": 5,
        "confirmatory_provenance_go": False,
        "admissibility_complete": False,
        "no_confirmatory_outcomes": True,
        "cache_identity_vs_binance_vision": "GO_PARTIAL_BOUNDED_IDENTITY_ONLY",
        "frozen_scope": {"window": "2025-08-01..2025-10-31", "months": ["2025-08", "2025-09", "2025-10"], "symbols": ["BTCUSDT"], "kinds": ["fundingRate"]},
        "license_terms": {"status": "EXPLICIT_BLOCKER_UNRESOLVED", "fabricated": False},
    }
    m.update(overrides)
    return m


class TestFclr016V5Guard(unittest.TestCase):
    def _check(self, manifest, start="2025-08-01", end="2025-10-31", confirmatory=True):
        with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False) as f:
            json.dump(manifest, f)
            p = f.name
        try:
            return check_confirmatory_provenance(start, end, "G4V5", "prereg.json", "v5", confirmatory_flag=confirmatory, provenance_manifest=p)
        finally:
            Path(p).unlink(missing_ok=True)

    def test_v5_unresolved_terms_refused(self):
        err = self._check(_base_v5())
        self.assertIsNotNone(err)
        self.assertIn("confirmatory_provenance_go!=true", err)

    def test_v5_identity_only_string_not_enough_even_if_flags_forged(self):
        # fail-closed: license not resolved
        m = _base_v5(confirmatory_provenance_go=True, admissibility_complete=True)
        err = self._check(m)
        self.assertIsNotNone(err)
        self.assertIn("license_terms", err)

    def test_v5_fabricated_marker_refused(self):
        m = _base_v5(confirmatory_provenance_go=True, admissibility_complete=True,
                     license_terms={"status": "RESOLVED_VERIFIED", "fabricated": True})
        err = self._check(m)
        self.assertIn("fabricated", err)

    def test_v5_scope_mismatch_refused(self):
        m = _base_v5(confirmatory_provenance_go=True, admissibility_complete=True,
                     license_terms={"status": "RESOLVED_VERIFIED", "fabricated": False},
                     cache_identity_vs_binance_vision="GO_PARTIAL_BOUNDED")
        err = self._check(m, start="2025-07-01")
        self.assertIn("scope", err.lower())

    def test_v5_fully_resolved_synthetic_fixture_accepted(self):
        # Synthetic test fixture only - validates guard logic; not a repo evidence artifact.
        m = _base_v5(confirmatory_provenance_go=True, admissibility_complete=True,
                     license_terms={"status": "RESOLVED_VERIFIED", "fabricated": False, "synthetic_test_fixture": True},
                     cache_identity_vs_binance_vision="GO_PARTIAL_BOUNDED")
        err = self._check(m)
        self.assertIsNone(err)

    def test_exploratory_not_blocked_by_v5_manifest(self):
        # explicit exploratory naming/flag: guard should not enforce confirmatory v5 GO fields
        err = check_confirmatory_provenance(
            "2025-08-01", "2025-10-31", "G4V5_EXPLORATORY", "prereg_exploratory.json", "v5_exploratory",
            confirmatory_flag=False,
            provenance_manifest=(lambda p=__import__('tempfile').NamedTemporaryFile('w',suffix='.json',delete=False): (json.dump(_base_v5(), p), p.close(), p.name)[2])(),
        )
        self.assertIsNone(err)

    def test_actual_v5_manifest_file_refused(self):
        mp = REPO / "research_state/fclr016_local_audit/fclr016_v5_provenance_license_manifest_20261108T014405Z.json"
        if not mp.exists():
            self.skipTest("manifest not present")
        err = check_confirmatory_provenance("2025-08-01", "2025-10-31", "G4V5", "prereg", "v5", confirmatory_flag=True, provenance_manifest=str(mp))
        self.assertIsNotNone(err)
        self.assertIn("NO_GO", err)


class TestFclr016V5AdmissibilityPackage(unittest.TestCase):
    """check_admissibility_package(): read-only package check, no outcomes/data loaded."""

    def test_current_blocked_package_ok_not_go(self):
        result = check_admissibility_package(str(PM), str(CA), str(TE), str(PR))
        self.assertTrue(result["ok"])
        self.assertFalse(result["all_go"])
        self.assertFalse(result["confirmatory_outcomes_permitted"])
        self.assertEqual(result["blockers"], ["terms_resolved_verified", "provenance_manifest_go",
                                              "completeness_leakage_pass", "prereg_frozen_non_draft", "prereg_claim_go"])
        self.assertEqual(set(result["hashes"].keys()), {"provenance_manifest", "completeness_audit", "terms_evidence", "prereg_draft"})
        self.assertEqual(result["hashes"]["completeness_audit"], "32dfcddca782cf7e2f029b2814dd86c5054a0d5069785ab29e8814fd98ccfca8")
        self.assertEqual(result["hashes"]["provenance_manifest"], "6888116a707a4fe1bad84d6fb1b957dfdd2890c2ce48a3c3bc9430e17f325346")

    def test_expect_go_refused_on_blocked_package(self):
        result = check_admissibility_package(str(PM), str(CA), str(TE), str(PR), expect_go=True)
        self.assertTrue(result["ok"])
        self.assertFalse(result["all_go"])
        self.assertTrue(result["expect_go"])

    def test_missing_file_returns_error(self):
        result = check_admissibility_package(str(PM), str(CA), str(TE), "/nonexistent/prereg.json")
        self.assertFalse(result.get("ok", False))
        self.assertIn("missing", result.get("error", ""))

    def test_draft_cannot_claim_frozen(self):
        import tempfile
        td = Path(tempfile.mkdtemp())
        for src, name in [(PM, "pm.json"), (CA, "ca.json"), (TE, "te.json"), (PR, "pr.json")]:
            (td / name).write_bytes(Path(src).read_bytes())
        pr = json.loads((td / "pr.json").read_text())
        pr["frozen_before_outcomes"] = True
        (td / "pr.json").write_text(json.dumps(pr))
        result = check_admissibility_package(str(td / "pm.json"), str(td / "ca.json"), str(td / "te.json"), str(td / "pr.json"))
        self.assertTrue(result["ok"])
        self.assertFalse(result["all_go"])
        self.assertIn("prereg_frozen_non_draft", result["blockers"])
        self.assertIn("draft prereg cannot set frozen_before_outcomes=true", result["errors"])

    def test_terms_hash_ref_mismatch_refused_when_present(self):
        import tempfile
        td = Path(tempfile.mkdtemp())
        for src, name in [(PM, "pm.json"), (CA, "ca.json"), (TE, "te.json"), (PR, "pr.json")]:
            (td / name).write_bytes(Path(src).read_bytes())
        pr = json.loads((td / "pr.json").read_text())
        pr.setdefault("admissibility_refs_sha256", {})["terms_evidence"] = "0" * 64
        (td / "pr.json").write_text(json.dumps(pr))
        result = check_admissibility_package(str(td / "pm.json"), str(td / "ca.json"), str(td / "te.json"), str(td / "pr.json"))
        self.assertTrue(result["ok"])
        self.assertFalse(result["all_go"])
        self.assertIn("terms_evidence", result["errors"][0])


if __name__ == "__main__":
    unittest.main()
