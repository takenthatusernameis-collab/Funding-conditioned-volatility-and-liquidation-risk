"""FCLR-016 v5 promotion dry-run tests (deterministic, tmp-isolated, no network/outcomes).

Proves the read-only promotion dry-run harness:
- never claims GO / confirmatory_outcomes_permitted on real blocked package;
- refuses every mandatory matrix case (missing human fields, fabricated, agent-only,
  template/blocker-as-resolved, draft promoted claims, provenance GO while unresolved,
  refs sha256 mismatch, completeness inconsistency, expect-go contract on blocked);
- permits GO only for synthetic_test_fixture=true/no_real_terms_evidence=true tmp fixture;
- never loads data/network/outcome paths (monkeypatched boom);
- never mutates canonical artifacts or input package files;
- CLI emits JSON + markdown with required statement/fields.
"""
from __future__ import annotations

import copy
import importlib.util
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
SCRIPT = REPO / "scripts" / "fclr016_v5_promotion_dryrun.py"
AUDIT = REPO / "research_state/fclr016_local_audit"
PM_REAL = AUDIT / "fclr016_v5_provenance_license_manifest_20261108T014405Z.json"
CA_REAL = AUDIT / "fclr016_v5_completeness_leakage_audit_20261108T014405Z.json"
TE_REAL = AUDIT / "fclr016_v5_terms_evidence_BLOCKED_20261108T014835Z.json"
PR_REAL = AUDIT / "fclr016_v5_confirmatory_prereg_DRAFT_20261108T014835Z.json"
CANONICAL = [
    REPO / "research_state/experiment_frontier.json",
    REPO / "research_state/run_manifest.json",
    REPO / "research_state/evaluation_summary.md",
]
REAL_PKG = [PM_REAL, CA_REAL, TE_REAL, PR_REAL]


def _canonical_bytes():
    return {str(p): p.read_bytes() for p in CANONICAL if p.exists()}


def _pkg_bytes():
    return {str(p): p.read_bytes() for p in REAL_PKG}


def _load_mod():
    spec = importlib.util.spec_from_file_location("fclr016_v5_promotion_dryrun_testmod", SCRIPT)
    mod = importlib.util.module_from_spec(spec)
    assert spec and spec.loader
    sys.path.insert(0, str(REPO / "scripts"))
    spec.loader.exec_module(mod)
    return mod


def _run_cli(args):
    return subprocess.run([sys.executable, str(SCRIPT), *args], capture_output=True, text=True)


def _boom(*a, **k):
    raise AssertionError("DATA_NETWORK_OR_OUTCOME_LOADER_CALLED")


def _with_boom_loaders(fn):
    sys.path.insert(0, str(REPO / "scripts"))
    import run_funding_ablations as rfa
    sentinels = {}
    names = (
        "load_kline_series", "load_funding_series", "load_kline_panel", "load_funding_panel",
        "run_multisplit", "run_adversarial", "run_persistence",
        "run_rv_baseline", "run_funding_baseline", "run_augmented_baseline",
    )
    for name in names:
        if hasattr(rfa, name):
            sentinels[name] = getattr(rfa, name)
            setattr(rfa, name, _boom)
    try:
        return fn()
    finally:
        for name, orig in sentinels.items():
            setattr(rfa, name, orig)


class TestPromotionDryrunRealBlocked(unittest.TestCase):
    def test_real_blocked_never_go_and_inputs_canonicals_unchanged(self):
        before_c = _canonical_bytes()
        before_p = _pkg_bytes()
        report = _with_boom_loaders(lambda: _load_mod().run_dryrun(PM_REAL, CA_REAL, TE_REAL, PR_REAL))
        self.assertEqual(before_c, _canonical_bytes(), "canonical artifacts mutated")
        self.assertEqual(before_p, _pkg_bytes(), "real package inputs mutated")
        self.assertTrue(report["ok"], report.get("summary"))
        self.assertFalse(report["all_go"])
        self.assertFalse(report["confirmatory_outcomes_permitted"])
        self.assertTrue(report["no_confirmatory_outcomes"])
        self.assertTrue(report["no_network"])
        self.assertTrue(report["no_data_loading"])
        self.assertFalse(report["canonical_mutation"])
        self.assertTrue(report["input_artifacts_unchanged"])
        self.assertIn("Confirmatory outcomes still prohibited", report["no_confirmatory_outcomes_statement"])
        # scenario (a)
        a = next(s for s in report["scenarios"] if s["scenario_id"] == "a_real_blocked_package")
        self.assertTrue(a["actual_refused"])
        self.assertTrue(a["status"].startswith("PASS"))

    def test_cli_json_markdown_and_no_go(self):
        before_c = _canonical_bytes()
        before_p = _pkg_bytes()
        p = _run_cli([str(PM_REAL), str(CA_REAL), str(TE_REAL), str(PR_REAL)])
        self.assertEqual(before_c, _canonical_bytes())
        self.assertEqual(before_p, _pkg_bytes())
        self.assertEqual(p.returncode, 0, p.stderr + p.stdout[:400])
        self.assertIn("---MARKDOWN---", p.stdout)
        out = json.loads(p.stdout.split("---MARKDOWN---", 1)[0])
        self.assertEqual(out["validator"], "fclr016_v5_promotion_dryrun")
        self.assertFalse(out["all_go"])
        self.assertFalse(out["confirmatory_outcomes_permitted"])
        self.assertIn("Confirmatory outcomes still prohibited", out["no_confirmatory_outcomes_statement"])
        md = p.stdout.split("---MARKDOWN---", 1)[1]
        self.assertIn("Required human terms fields", md)
        self.assertIn("Forbidden values / shortcuts", md)
        self.assertNotIn("all_go (real): True", md)
        self.assertNotIn("confirmatory_outcomes_permitted: True", md)

    def test_json_only_flag(self):
        p = _run_cli(["--json-only", str(PM_REAL), str(CA_REAL), str(TE_REAL), str(PR_REAL)])
        self.assertEqual(p.returncode, 0, p.stderr)
        self.assertNotIn("---MARKDOWN---", p.stdout)
        out = json.loads(p.stdout)
        self.assertFalse(out["all_go"])


class TestMandatoryScenarioMatrix(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.report = _with_boom_loaders(lambda: _load_mod().run_dryrun(PM_REAL, CA_REAL, TE_REAL, PR_REAL))
        cls.by_id = {s["scenario_id"]: s for s in cls.report["scenarios"]}

    def _assert_refused(self, sid):
        s = self.by_id[sid]
        self.assertTrue(s["expected_refused"], sid)
        self.assertTrue(s["actual_refused"], sid)
        self.assertTrue(s["status"].startswith("PASS"), f"{sid}: {s}")

    def test_all_required_scenarios_present_and_pass(self):
        required = [
            "a_real_blocked_package", "b_missing_human_fields", "c_fabricated_true",
            "c_agent_only_reviewer", "d_template_as_resolved", "d_blocker_as_resolved",
            "e_draft_promoted_claims", "f_provenance_go_terms_unresolved",
            "g_refs_sha256_mismatch", "h_completeness_verdict_not_pass",
            "h_completeness_pass_inconsistent", "i_expect_go_blocked_contract",
            "j_synthetic_go_fixture_only",
        ]
        for sid in required:
            self.assertIn(sid, self.by_id, f"missing scenario {sid}")
            self.assertTrue(self.by_id[sid]["status"].startswith("PASS"), self.by_id[sid])
        self.assertEqual(self.report["summary"]["failed"], 0)

    def test_b_missing_human_fields_refused(self): self._assert_refused("b_missing_human_fields")
    def test_c_fabricated_refused(self): self._assert_refused("c_fabricated_true")
    def test_c_agent_only_refused(self): self._assert_refused("c_agent_only_reviewer")
    def test_d_template_refused(self): self._assert_refused("d_template_as_resolved")
    def test_d_blocker_refused(self): self._assert_refused("d_blocker_as_resolved")
    def test_e_draft_promoted_refused(self): self._assert_refused("e_draft_promoted_claims")
    def test_f_provenance_go_unresolved_refused(self): self._assert_refused("f_provenance_go_terms_unresolved")
    def test_g_sha_mismatch_refused(self): self._assert_refused("g_refs_sha256_mismatch")
    def test_h_verdict_not_pass_refused(self): self._assert_refused("h_completeness_verdict_not_pass")
    def test_h_pass_inconsistent_refused(self): self._assert_refused("h_completeness_pass_inconsistent")
    def test_i_expect_go_contract_refused(self): self._assert_refused("i_expect_go_blocked_contract")

    def test_j_synthetic_go_only_as_labeled_fixture(self):
        s = self.by_id["j_synthetic_go_fixture_only"]
        self.assertFalse(s["expected_refused"])
        self.assertFalse(s["actual_refused"])
        self.assertTrue(s["synthetic_test_fixture"])
        self.assertTrue(s["no_real_terms_evidence"])
        self.assertIn("SYNTHETIC_FIXTURE_ONLY", s["status"])
        self.assertTrue(s["result_summary"]["all_go"])
        # report-level guard remains non-GO
        self.assertFalse(self.report["all_go"])
        self.assertFalse(self.report["confirmatory_outcomes_permitted"])

    def test_required_human_fields_and_forbidden_values_listed(self):
        fields = " ".join(self.report["required_human_terms_fields"])
        for req in ("terms_url_reviewed", "access_date_utc", "reviewer_role", "fabricated", "status=RESOLVED_VERIFIED"):
            self.assertIn(req.split("=")[0], fields)
        forbidden = " ".join(self.report["forbidden_values_or_shortcuts"]).lower()
        for token in ("fabricated=true", "agent-only", "template_not_evidence", "expect-go", "sha256"):
            self.assertIn(token, forbidden)
        self.assertIn("confirmatory outcomes still prohibited", self.report["no_confirmatory_outcomes_statement"].lower())


class TestCandidateAndSafety(unittest.TestCase):
    def test_candidate_terms_evaluated_read_only(self):
        before_c = _canonical_bytes()
        before_p = _pkg_bytes()
        with tempfile.TemporaryDirectory() as td:
            cand = Path(td) / "candidate_terms.json"
            te = json.loads(TE_REAL.read_text())
            te["status"] = "RESOLVED_VERIFIED"
            te["fabricated"] = False
            te["terms_url_reviewed"] = ""  # incomplete -> must refuse
            cand.write_text(json.dumps(te))
            p = _run_cli(["--candidate-terms-evidence", str(cand), "--json-only",
                          str(PM_REAL), str(CA_REAL), str(TE_REAL), str(PR_REAL)])
        self.assertEqual(before_c, _canonical_bytes())
        self.assertEqual(before_p, _pkg_bytes())
        self.assertEqual(p.returncode, 0, p.stderr)
        out = json.loads(p.stdout)
        self.assertIsNotNone(out["candidate_evaluation"])
        self.assertFalse(out["candidate_evaluation"]["all_go"])

    def test_missing_file_refuses(self):
        p = _run_cli([str(PM_REAL), str(CA_REAL), str(TE_REAL), "/nonexistent/pr.json"])
        self.assertEqual(p.returncode, 2)
        out = json.loads(p.stdout.strip().splitlines()[0])
        self.assertFalse(out.get("all_go", False))
        self.assertFalse(out.get("confirmatory_outcomes_permitted", False))

    def test_module_has_no_data_or_network_tokens(self):
        src = SCRIPT.read_text(encoding="utf-8")
        forbidden = ["requests", "urllib.request", "httpx", "aiohttp", "read_parquet",
                     "pd.read_", "load_kline", "load_funding", "run_multisplit", "run_adversarial"]
        for token in forbidden:
            self.assertNotIn(token, src, f"promotion dryrun must not reference: {token}")


if __name__ == "__main__":
    unittest.main()
