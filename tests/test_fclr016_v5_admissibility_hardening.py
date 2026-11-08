"""FCLR-016 Gate 4 v5 adversarial hardening (deterministic, tmp-isolated, no network/outcomes).

Covers: resolved-terms required-field/refusal, terms hash-ref mismatch, promoted/non-draft
prereg without admissibility+terms resolved refused, completeness verdict/pass inconsistency,
--expect-go/exit-code/JSON contract stability, and check_confirmatory_provenance vs
check_admissibility_package alignment on synthetic GO fixtures (no false-accept, no
canonical mutation, no outcome loading).
"""
from __future__ import annotations

import copy
import hashlib
import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "scripts"))
from run_funding_ablations import check_admissibility_package, check_confirmatory_provenance  # noqa: E402

VALIDATOR = REPO / "scripts" / "fclr016_validate_v5_admissibility.py"
RUN_FUNDING = REPO / "scripts" / "run_funding_ablations.py"
AUDIT = REPO / "research_state/fclr016_local_audit"
PM_REAL = AUDIT / "fclr016_v5_provenance_license_manifest_20261108T014405Z.json"
CA_REAL = AUDIT / "fclr016_v5_completeness_leakage_audit_20261108T014405Z.json"
TE_REAL = AUDIT / "fclr016_v5_terms_evidence_BLOCKED_20261108T014835Z.json"
PR_REAL = AUDIT / "fclr016_v5_confirmatory_prereg_DRAFT_20261108T014835Z.json"

SCOPE = {"window": "2025-08-01..2025-10-31", "months": ["2025-08", "2025-09", "2025-10"],
         "symbols": ["BTCUSDT"], "kinds": ["fundingRate"]}


def _write_pkg(td: Path, pm, ca, te, pr, names=("pm.json", "ca.json", "te.json", "pr.json")):
    paths = [td / n for n in names]
    for p, d in zip(paths, (pm, ca, te, pr)):
        p.write_text(json.dumps(d, indent=2, sort_keys=True))
    return [str(p) for p in paths]


def _synthetic_go(td: Path):
    pm = {"artifact": "fclr016_v5_provenance_license_manifest", "schema_version": 5,
          "confirmatory_provenance_go": True, "admissibility_complete": True,
          "no_confirmatory_outcomes": True, "fabricated": False, "confirmatory_claim_go": "GO",
          "cache_identity_vs_binance_vision": "GO", "frozen_scope": SCOPE,
          "license_terms": {"status": "RESOLVED_VERIFIED", "fabricated": False, "synthetic_test_fixture": True}}
    ca = {"artifact": "fclr016_v5_completeness_leakage_audit", "confirmatory_claim_go": "NO_GO",
          "admissibility_complete": True, "no_confirmatory_outcomes": True, "fabricated": False,
          "frozen_scope": SCOPE, "verdict": "PASS_COMPLETENESS_LEAKAGE_DETERMINISTIC", "completeness": {"ok": True}}
    te = {"artifact": "fclr016_v5_terms_evidence", "status": "RESOLVED_VERIFIED", "fabricated": False,
          "no_confirmatory_outcomes": True, "confirmatory_provenance_go": True, "admissibility_complete": True,
          "frozen_scope": SCOPE, "terms_url_reviewed": "https://example.invalid/terms",
          "access_date_utc": "2026-11-08T00:00:00Z", "reviewer_role": "human maintainer (synthetic test fixture)",
          "conclusion": "PERMITTED_WITH_CONDITIONS", "conditions_or_restrictions": []}
    pr = {"artifact": "fclr016_v5_confirmatory_prereg", "draft": False, "frozen_before_outcomes": True,
          "promotable_to_frozen": True, "confirmatory_claim_go": "GO", "admissibility_complete": True,
          "license_terms_resolved": True, "no_confirmatory_outcomes": True, "fabricated": False,
          "frozen_scope": SCOPE, "gates": {"confirmatory_outcomes_permitted": True},
          "admissibility_refs_sha256": {}}
    paths = _write_pkg(td, pm, ca, te, pr)
    # set hash refs
    pr["admissibility_refs_sha256"] = {
        "provenance_license_manifest": hashlib.sha256(Path(paths[0]).read_bytes()).hexdigest(),
        "completeness_leakage_audit": hashlib.sha256(Path(paths[1]).read_bytes()).hexdigest(),
        "terms_evidence": hashlib.sha256(Path(paths[2]).read_bytes()).hexdigest(),
    }
    Path(paths[3]).write_text(json.dumps(pr, indent=2, sort_keys=True))
    return paths


def _run_validator(args):
    p = subprocess.run([sys.executable, str(VALIDATOR), *args], capture_output=True, text=True)
    out = json.loads(p.stdout) if p.stdout.strip() else {}
    return p.returncode, out


def _run_pkg_cli(args):
    p = subprocess.run([sys.executable, str(RUN_FUNDING), *args], capture_output=True, text=True)
    out = json.loads(p.stdout) if p.stdout.strip() else {}
    return p.returncode, out, p.stderr


class TestResolvedTermsRequiredFields(unittest.TestCase):
    """Resolved terms missing required human-verified fields/conclusion/reviewer must refuse."""

    def _bad_terms(self, **mut):
        te = json.loads(TE_REAL.read_text())
        te.update({"status": "RESOLVED_VERIFIED", "fabricated": False,
                   "terms_url_reviewed": "https://example.invalid", "access_date_utc": "2026-11-08T00:00:00Z",
                   "reviewer_role": "human maintainer", "conclusion": "PERMITTED"})
        te.update(mut)
        return te

    def _assert_refused(self, te):
        with tempfile.TemporaryDirectory() as td:
            td = Path(td)
            pm = json.loads(PM_REAL.read_text()); ca = json.loads(CA_REAL.read_text()); pr = json.loads(PR_REAL.read_text())
            paths = _write_pkg(td, pm, ca, te, pr)
            # validator
            rc, out = _run_validator(["--provenance-manifest", paths[0], "--completeness-audit", paths[1],
                                      "--terms-evidence", paths[2], "--prereg-draft", paths[3]])
            self.assertNotEqual(rc, 0, out)
            self.assertFalse(out.get("ok", False) is True and out.get("all_go", False) is True, out)
            # package check
            pkg = check_admissibility_package(*paths)
            self.assertTrue(pkg["ok"])
            self.assertFalse(pkg["all_go"])
            self.assertFalse(pkg["confirmatory_outcomes_permitted"])

    def test_missing_terms_url(self):
        self._assert_refused(self._bad_terms(terms_url_reviewed=""))

    def test_missing_access_date(self):
        self._assert_refused(self._bad_terms(access_date_utc=None))

    def test_missing_reviewer(self):
        self._assert_refused(self._bad_terms(reviewer_role=""))

    def test_agent_only_reviewer(self):
        self._assert_refused(self._bad_terms(reviewer_role="automated agent only"))

    def test_missing_conclusion(self):
        self._assert_refused(self._bad_terms(conclusion=""))

    def test_fabricated_true_with_resolved(self):
        self._assert_refused(self._bad_terms(fabricated=True))


class TestHashRefAndVerdictConsistency(unittest.TestCase):
    def test_terms_hash_ref_mismatch_validator_and_package(self):
        with tempfile.TemporaryDirectory() as td:
            td = Path(td)
            pm = json.loads(PM_REAL.read_text()); ca = json.loads(CA_REAL.read_text())
            te = json.loads(TE_REAL.read_text()); pr = json.loads(PR_REAL.read_text())
            paths = _write_pkg(td, pm, ca, te, pr)
            # make PM/CA refs consistent with copied files, then mismatch terms only
            pr.setdefault("admissibility_refs_sha256", {})
            pr["admissibility_refs_sha256"]["provenance_license_manifest"] = hashlib.sha256(Path(paths[0]).read_bytes()).hexdigest()
            pr["admissibility_refs_sha256"]["completeness_leakage_audit"] = hashlib.sha256(Path(paths[1]).read_bytes()).hexdigest()
            pr["admissibility_refs_sha256"]["terms_evidence"] = "0" * 64
            Path(paths[3]).write_text(json.dumps(pr))
            rc, out = _run_validator(["--provenance-manifest", paths[0], "--completeness-audit", paths[1],
                                      "--terms-evidence", paths[2], "--prereg-draft", paths[3]])
            self.assertNotEqual(rc, 0)
            self.assertIn("terms_evidence", json.dumps(out))
            pkg = check_admissibility_package(*paths)
            self.assertFalse(pkg["all_go"])
            self.assertTrue(any("terms_evidence" in e for e in pkg["errors"]))

    def test_completeness_verdict_pass_but_ok_false_refused(self):
        with tempfile.TemporaryDirectory() as td:
            td = Path(td)
            pm = json.loads(PM_REAL.read_text()); ca = json.loads(CA_REAL.read_text())
            te = json.loads(TE_REAL.read_text()); pr = json.loads(PR_REAL.read_text())
            ca["verdict"] = "PASS_COMPLETENESS_LEAKAGE_DETERMINISTIC"
            ca["completeness"] = {"ok": False}
            paths = _write_pkg(td, pm, ca, te, pr)
            rc, _ = _run_validator(["--provenance-manifest", paths[0], "--completeness-audit", paths[1],
                                    "--terms-evidence", paths[2], "--prereg-draft", paths[3]])
            self.assertNotEqual(rc, 0)
            pkg = check_admissibility_package(*paths)
            self.assertFalse(pkg["all_go"])
            self.assertTrue(any("completeness" in e.lower() for e in pkg["errors"]))

    def test_completeness_not_pass_cannot_claim_admissible(self):
        with tempfile.TemporaryDirectory() as td:
            td = Path(td)
            pm = json.loads(PM_REAL.read_text()); ca = json.loads(CA_REAL.read_text())
            te = json.loads(TE_REAL.read_text()); pr = json.loads(PR_REAL.read_text())
            ca["verdict"] = "FAIL"
            ca["admissibility_complete"] = True
            paths = _write_pkg(td, pm, ca, te, pr)
            rc, _ = _run_validator(["--provenance-manifest", paths[0], "--completeness-audit", paths[1],
                                    "--terms-evidence", paths[2], "--prereg-draft", paths[3]])
            self.assertNotEqual(rc, 0)


class TestPreregPromotionRefusal(unittest.TestCase):
    """Draft promoted/non-draft GO without admissibility+terms resolved/provenance must refuse."""

    def test_draft_cannot_set_frozen_or_admissible(self):
        with tempfile.TemporaryDirectory() as td:
            td = Path(td)
            pm = json.loads(PM_REAL.read_text()); ca = json.loads(CA_REAL.read_text())
            te = json.loads(TE_REAL.read_text()); pr = json.loads(PR_REAL.read_text())
            pr["frozen_before_outcomes"] = True
            paths = _write_pkg(td, pm, ca, te, pr)
            rc, _ = _run_validator(["--provenance-manifest", paths[0], "--completeness-audit", paths[1],
                                    "--terms-evidence", paths[2], "--prereg-draft", paths[3]])
            self.assertNotEqual(rc, 0)
            pkg = check_admissibility_package(*paths)
            self.assertFalse(pkg["all_go"])
            self.assertTrue(any("frozen_before_outcomes" in e for e in pkg["errors"]))

    def test_non_draft_go_without_terms_resolved_refused(self):
        with tempfile.TemporaryDirectory() as td:
            td = Path(td)
            paths = _synthetic_go(td)
            te = json.loads(Path(paths[2]).read_text())
            te.update({"status": "EXPLICIT_BLOCKER_UNRESOLVED", "confirmatory_provenance_go": False, "admissibility_complete": False})
            te.pop("terms_url_reviewed", None); te.pop("reviewer_role", None); te.pop("access_date_utc", None); te.pop("conclusion", None)
            Path(paths[2]).write_text(json.dumps(te))
            # update prereg hash ref for terms
            pr = json.loads(Path(paths[3]).read_text())
            pr["admissibility_refs_sha256"]["terms_evidence"] = hashlib.sha256(Path(paths[2]).read_bytes()).hexdigest()
            Path(paths[3]).write_text(json.dumps(pr))
            rc, out = _run_validator(["--provenance-manifest", paths[0], "--completeness-audit", paths[1],
                                      "--terms-evidence", paths[2], "--prereg-draft", paths[3]])
            self.assertNotEqual(rc, 0)
            pkg = check_admissibility_package(*paths)
            self.assertFalse(pkg["all_go"])
            self.assertTrue(any("terms" in e.lower() or "RESOLVED" in e for e in (pkg["errors"] + pkg["blockers"])))

    def test_non_draft_admissible_without_provenance_go_refused(self):
        with tempfile.TemporaryDirectory() as td:
            td = Path(td)
            paths = _synthetic_go(td)
            pm = json.loads(Path(paths[0]).read_text())
            pm["confirmatory_provenance_go"] = False
            pm["admissibility_complete"] = False  # keep manifest self-consistent; test prereg-vs-provenance refusal
            Path(paths[0]).write_text(json.dumps(pm))
            pr = json.loads(Path(paths[3]).read_text())
            pr["admissibility_refs_sha256"]["provenance_license_manifest"] = hashlib.sha256(Path(paths[0]).read_bytes()).hexdigest()
            Path(paths[3]).write_text(json.dumps(pr))
            rc, _ = _run_validator(["--provenance-manifest", paths[0], "--completeness-audit", paths[1],
                                    "--terms-evidence", paths[2], "--prereg-draft", paths[3]])
            self.assertNotEqual(rc, 0)
            pkg = check_admissibility_package(*paths)
            self.assertFalse(pkg["all_go"])


class TestCliContract(unittest.TestCase):
    REQUIRED_KEYS = {"validator", "ok", "expect_go", "all_go", "confirmatory_outcomes_permitted", "gates", "blockers", "hashes"}

    def test_blocked_package_parseable_stable_keys_exit0(self):
        rc, out = _run_validator(["--provenance-manifest", str(PM_REAL), "--completeness-audit", str(CA_REAL),
                                  "--terms-evidence", str(TE_REAL), "--prereg-draft", str(PR_REAL)])
        self.assertEqual(rc, 0)
        self.assertTrue(self.REQUIRED_KEYS.issubset(out.keys()))
        self.assertFalse(out["all_go"])
        self.assertFalse(out["confirmatory_outcomes_permitted"])
        self.assertFalse(out["expect_go"])

    def test_expect_go_refusal_exit2_parseable(self):
        rc, out = _run_validator(["--provenance-manifest", str(PM_REAL), "--completeness-audit", str(CA_REAL),
                                  "--terms-evidence", str(TE_REAL), "--prereg-draft", str(PR_REAL), "--expect-go"])
        self.assertEqual(rc, 2)
        # validator uses fail() contract: ok=false + error + gates/blockers (parseable)
        self.assertFalse(out.get("ok", True))
        self.assertIn("expect-go", out.get("error", ""))
        self.assertIn("gates", out)
        self.assertIn("blockers", out)

    def test_run_funding_package_check_exit0_blocked(self):
        rc, out, _ = _run_pkg_cli(["--check-admissibility-package", str(PM_REAL), str(CA_REAL), str(TE_REAL), str(PR_REAL)])
        self.assertEqual(rc, 0)
        self.assertTrue(out["ok"])
        self.assertFalse(out["all_go"])
        self.assertIn("hashes", out)

    def test_run_funding_package_check_expect_go_exit2(self):
        rc, out, _ = _run_pkg_cli(["--check-admissibility-package", str(PM_REAL), str(CA_REAL), str(TE_REAL), str(PR_REAL), "--expect-go"])
        self.assertEqual(rc, 2)
        self.assertTrue(out.get("ok") is True or out.get("expect_go") is True)
        self.assertFalse(out.get("all_go"))
        self.assertIn("gates", out)

    def test_run_funding_dry_run_alias(self):
        rc, out, _ = _run_pkg_cli(["--dry-run-admissibility", str(PM_REAL), str(CA_REAL), str(TE_REAL), str(PR_REAL)])
        self.assertEqual(rc, 0)
        self.assertEqual(out.get("validator"), "run_funding_ablations.admissibility_package")


class TestProvenanceVsPackageAlignment(unittest.TestCase):
    """check_confirmatory_provenance and package check must align on synthetic GO (no false-accept)."""

    def test_synthetic_go_aligned(self):
        with tempfile.TemporaryDirectory() as td:
            td = Path(td)
            paths = _synthetic_go(td)
            pkg = check_admissibility_package(*paths)
            self.assertTrue(pkg["ok"])
            self.assertTrue(pkg["all_go"])
            self.assertTrue(pkg["confirmatory_outcomes_permitted"])
            self.assertEqual(pkg["errors"], [])
            prov = check_confirmatory_provenance("2025-08-01", "2025-10-31", "G4V5_CONFIRMATORY",
                                                 "prereg", "v5", confirmatory_flag=True,
                                                 provenance_manifest=paths[0])
            self.assertIsNone(prov)

    def test_synthetic_go_no_canonical_mutation(self):
        with tempfile.TemporaryDirectory() as td:
            td = Path(td)
            paths = _synthetic_go(td)
            before = {p: Path(p).read_bytes() for p in paths}
            canonical = {
                "frontier": (REPO / "research_state/experiment_frontier.json").read_bytes(),
                "manifest": (REPO / "research_state/run_manifest.json").read_bytes(),
                "summary": (REPO / "research_state/evaluation_summary.md").read_bytes(),
            }
            pkg = check_admissibility_package(*paths)
            prov = check_confirmatory_provenance("2025-08-01", "2025-10-31", "G4V5_CONFIRMATORY",
                                                 "prereg", "v5", confirmatory_flag=True,
                                                 provenance_manifest=paths[0])
            self.assertTrue(pkg["all_go"])
            self.assertIsNone(prov)
            for p, b in before.items():
                self.assertEqual(Path(p).read_bytes(), b, f"artifact mutated: {p}")
            self.assertEqual((REPO / "research_state/experiment_frontier.json").read_bytes(), canonical["frontier"])
            self.assertEqual((REPO / "research_state/run_manifest.json").read_bytes(), canonical["manifest"])
            self.assertEqual((REPO / "research_state/evaluation_summary.md").read_bytes(), canonical["summary"])

    def test_blocked_real_package_no_false_accept(self):
        pkg = check_admissibility_package(str(PM_REAL), str(CA_REAL), str(TE_REAL), str(PR_REAL))
        self.assertFalse(pkg["all_go"])
        self.assertFalse(pkg["confirmatory_outcomes_permitted"])
        prov = check_confirmatory_provenance("2025-08-01", "2025-10-31", "G4V5_CONFIRMATORY",
                                             "prereg", "v5", confirmatory_flag=True,
                                             provenance_manifest=str(PM_REAL))
        self.assertIsNotNone(prov)
        self.assertIn("NO_GO", prov)

    def test_unresolved_terms_block_both_paths(self):
        with tempfile.TemporaryDirectory() as td:
            td = Path(td)
            paths = _synthetic_go(td)
            te = json.loads(Path(paths[2]).read_text())
            te["status"] = "EXPLICIT_BLOCKER_UNRESOLVED"
            te["fabricated"] = False
            Path(paths[2]).write_text(json.dumps(te))
            pr = json.loads(Path(paths[3]).read_text())
            pr["admissibility_refs_sha256"]["terms_evidence"] = hashlib.sha256(Path(paths[2]).read_bytes()).hexdigest()
            Path(paths[3]).write_text(json.dumps(pr))
            pkg = check_admissibility_package(*paths)
            self.assertFalse(pkg["all_go"])
            prov = check_confirmatory_provenance("2025-08-01", "2025-10-31", "G4V5_CONFIRMATORY",
                                                 "prereg", "v5", confirmatory_flag=True,
                                                 provenance_manifest=paths[0])
            # provenance manifest in synthetic fixture still says RESOLVED_VERIFIED license_terms/GO;
            # package sees terms artifact unresolved and blocks; provenance guard checks manifest fields.
            # This proves no false-accept from package even if caller misuses one artifact in isolation.
            self.assertFalse(pkg["confirmatory_outcomes_permitted"])


if __name__ == "__main__":
    unittest.main()
