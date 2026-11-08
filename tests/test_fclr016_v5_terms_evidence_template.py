"""FCLR-016 v5 terms-evidence TEMPLATE tests (deterministic, tmp-isolated, no network/outcomes).

Proves template:
- is emitted as TEMPLATE_NOT_EVIDENCE (never RESOLVED_VERIFIED) at explicit output path only;
- cannot advance any gate / cannot be mistaken for RESOLVED_VERIFIED by validator, package check,
  report, or confirmatory provenance guard (terms cross-check);
- refuses overwrite of existing evidence without --force-template and never overwrites RESOLVED;
- writes only requested output path; no network/data loaders; canonical artifacts unchanged.
"""
from __future__ import annotations

import hashlib
import importlib.util
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
SCRIPTS = REPO / "scripts"
TEMPLATE = SCRIPTS / "fclr016_v5_terms_evidence_template.py"
VALIDATOR = SCRIPTS / "fclr016_validate_v5_admissibility.py"
REPORT = SCRIPTS / "fclr016_v5_admissibility_report.py"
AUDIT = REPO / "research_state/fclr016_local_audit"
PM_REAL = AUDIT / "fclr016_v5_provenance_license_manifest_20261108T014405Z.json"
CA_REAL = AUDIT / "fclr016_v5_completeness_leakage_audit_20261108T014405Z.json"
TE_BLOCKED = AUDIT / "fclr016_v5_terms_evidence_BLOCKED_20261108T014835Z.json"
PR_REAL = AUDIT / "fclr016_v5_confirmatory_prereg_DRAFT_20261108T014835Z.json"
CANONICAL = [
    REPO / "research_state/experiment_frontier.json",
    REPO / "research_state/run_manifest.json",
    REPO / "research_state/evaluation_summary.md",
]
SCOPE = {"window": "2025-08-01..2025-10-31", "months": ["2025-08", "2025-09", "2025-10"],
         "symbols": ["BTCUSDT", "ETHUSDT", "BNBUSDT", "SOLUSDT", "XRPUSDT"],
         "kinds": ["fundingRate", "klines", "markPriceKlines", "indexPriceKlines", "premiumIndexKlines"]}


def _canon():
    return {str(p): p.read_bytes() for p in CANONICAL if p.exists()}


def _run(args):
    return subprocess.run([sys.executable, *args], capture_output=True, text=True)


def _synthetic_go_package_with_terms(td: Path, te: dict):
    """Package whose other artifacts are synthetic GO-shaped but terms are supplied by caller."""
    pm = {"artifact": "fclr016_v5_provenance_license_manifest", "schema_version": 5,
          "confirmatory_provenance_go": True, "admissibility_complete": True,
          "no_confirmatory_outcomes": True, "fabricated": False, "confirmatory_claim_go": "GO",
          "cache_identity_vs_binance_vision": "GO", "frozen_scope": SCOPE,
          "license_terms": {"status": "RESOLVED_VERIFIED", "fabricated": False, "synthetic_test_fixture": True}}
    ca = {"artifact": "fclr016_v5_completeness_leakage_audit", "confirmatory_claim_go": "NO_GO",
          "admissibility_complete": True, "no_confirmatory_outcomes": True, "fabricated": False,
          "frozen_scope": SCOPE, "verdict": "PASS_COMPLETENESS_LEAKAGE_DETERMINISTIC", "completeness": {"ok": True}}
    pr = {"artifact": "fclr016_v5_confirmatory_prereg", "draft": False, "frozen_before_outcomes": True,
          "promotable_to_frozen": True, "confirmatory_claim_go": "GO", "admissibility_complete": True,
          "license_terms_resolved": True, "no_confirmatory_outcomes": True, "fabricated": False,
          "frozen_scope": SCOPE, "gates": {"confirmatory_outcomes_permitted": True},
          "admissibility_refs_sha256": {}}
    paths = [td / "pm.json", td / "ca.json", td / "te.json", td / "pr.json"]
    for p, d in zip(paths, (pm, ca, te, pr)):
        p.write_text(json.dumps(d, indent=2, sort_keys=True))
    pr["admissibility_refs_sha256"] = {k: hashlib.sha256(paths[i].read_bytes()).hexdigest()
                                       for i, k in enumerate(["provenance_license_manifest", "completeness_leakage_audit", "terms_evidence"])}
    paths[3].write_text(json.dumps(pr, indent=2, sort_keys=True))
    return [str(p) for p in paths]


class TestTemplateGeneration(unittest.TestCase):
    def test_emits_template_not_evidence_at_explicit_path_only(self):
        before = _canon()
        with tempfile.TemporaryDirectory() as td:
            td = Path(td)
            out = td / "sub" / "fclr016_v5_terms_evidence_TEMPLATE.json"
            other = td / "other.json"
            p = _run([str(TEMPLATE), "--out", str(out), "--scope-window", "2025-08-01..2025-10-31"])
            self.assertEqual(p.returncode, 0, p.stdout + p.stderr)
            res = json.loads(p.stdout)
            self.assertTrue(res["ok"])
            self.assertEqual(res["status"], "TEMPLATE_NOT_EVIDENCE")
            self.assertFalse(res["confirmatory_provenance_go"])
            self.assertFalse(res["admissibility_complete"])
            self.assertEqual(res["confirmatory_claim_go"], "NO_GO")
            self.assertTrue(res["human_review_required"])
            self.assertTrue(out.exists())
            self.assertFalse(other.exists())
            tpl = json.loads(out.read_text())
            self.assertEqual(tpl["status"], "TEMPLATE_NOT_EVIDENCE")
            self.assertNotEqual(tpl["status"], "RESOLVED_VERIFIED")
            self.assertFalse(tpl["confirmatory_provenance_go"])
            self.assertFalse(tpl["admissibility_complete"])
            self.assertTrue(tpl["no_confirmatory_outcomes"])
            self.assertTrue(tpl["human_review_required"])
            for f in ["terms_url_reviewed", "access_date_utc", "terms_version_or_snapshot_id",
                      "relevant_clause_summary", "reviewer_role", "conclusion"]:
                self.assertIn(f, tpl["required_human_fields_to_complete"])
                self.assertIsNone(tpl["required_human_fields_to_complete"][f])
            self.assertEqual(tpl["scope_match"]["window"], "2025-08-01..2025-10-31")
        self.assertEqual(before, _canon())

    def test_never_creates_resolved_status(self):
        with tempfile.TemporaryDirectory() as td:
            out = Path(td) / "t.json"
            _run([str(TEMPLATE), "--out", str(out)])
            txt = out.read_text()
            self.assertNotIn("RESOLVED_VERIFIED", json.loads(txt)["status"])
            self.assertEqual(json.loads(txt)["confirmatory_claim_go"], "NO_GO")


class TestTemplateOverwriteSafety(unittest.TestCase):
    def test_refuses_overwrite_without_force(self):
        before = _canon()
        with tempfile.TemporaryDirectory() as td:
            out = Path(td) / "t.json"
            self.assertEqual(_run([str(TEMPLATE), "--out", str(out)]).returncode, 0)
            p = _run([str(TEMPLATE), "--out", str(out)])
            self.assertNotEqual(p.returncode, 0)
            res = json.loads(p.stdout)
            self.assertFalse(res["ok"])
            self.assertIn("force-template", res["error"])
        self.assertEqual(before, _canon())

    def test_force_overwrites_non_resolved_only(self):
        with tempfile.TemporaryDirectory() as td:
            out = Path(td) / "t.json"
            _run([str(TEMPLATE), "--out", str(out)])
            p = _run([str(TEMPLATE), "--out", str(out), "--force-template"])
            self.assertEqual(p.returncode, 0, p.stdout)

    def test_never_overwrites_resolved_evidence(self):
        with tempfile.TemporaryDirectory() as td:
            out = Path(td) / "resolved.json"
            out.write_text(json.dumps({"status": "RESOLVED_VERIFIED", "fabricated": False}))
            p = _run([str(TEMPLATE), "--out", str(out), "--force-template"])
            self.assertNotEqual(p.returncode, 0)
            res = json.loads(p.stdout)
            self.assertIn("RESOLVED_VERIFIED", res["error"])
            self.assertEqual(json.loads(out.read_text())["status"], "RESOLVED_VERIFIED")


class TestTemplateCannotAdvanceGates(unittest.TestCase):
    def test_validator_refuses_template_as_evidence(self):
        before = _canon()
        with tempfile.TemporaryDirectory() as td:
            td = Path(td)
            te_out = td / "template.json"
            _run([str(TEMPLATE), "--out", str(te_out)])
            # use real package but swap terms evidence for template
            p = _run([str(VALIDATOR), "--provenance-manifest", str(PM_REAL),
                      "--completeness-audit", str(CA_REAL), "--terms-evidence", str(te_out),
                      "--prereg-draft", str(PR_REAL)])
            out = json.loads(p.stdout)
            # validator contract: consistent blocked package => ok=true, all_go=false (exit 0 unless --expect-go)
            self.assertFalse(out.get("all_go", False))
            self.assertFalse(out.get("confirmatory_outcomes_permitted", False))
            self.assertFalse(out.get("gates", {}).get("terms_resolved_verified", True))
            self.assertTrue(out.get("blockers"))
        self.assertEqual(before, _canon())

    def test_package_check_never_treats_template_as_resolved(self):
        sys.path.insert(0, str(SCRIPTS))
        from run_funding_ablations import check_admissibility_package  # noqa
        with tempfile.TemporaryDirectory() as td:
            td = Path(td)
            te_out = td / "template.json"
            _run([str(TEMPLATE), "--out", str(te_out)])
            paths = _synthetic_go_package_with_terms(td, json.loads(te_out.read_text()))
            pkg = check_admissibility_package(*paths)
            self.assertFalse(pkg["all_go"])
            self.assertFalse(pkg["confirmatory_outcomes_permitted"])
            self.assertFalse(pkg["gates"]["terms_resolved_verified"])

    def test_report_never_claims_go_for_template(self):
        before = _canon()
        with tempfile.TemporaryDirectory() as td:
            td = Path(td)
            te_out = td / "template.json"
            _run([str(TEMPLATE), "--out", str(te_out)])
            paths = _synthetic_go_package_with_terms(td, json.loads(te_out.read_text()))
            p = _run([str(REPORT), *paths])
            out = json.loads(p.stdout.split("---MARKDOWN---", 1)[0])
            self.assertFalse(out["all_go"])
            self.assertFalse(out["confirmatory_outcomes_permitted"])
            self.assertIn("terms_resolved_verified", out["blockers"] if out["blockers"] else out.get("gates", {}))
        self.assertEqual(before, _canon())

    def test_provenance_guard_refuses_template_via_terms_evidence(self):
        sys.path.insert(0, str(SCRIPTS))
        from run_funding_ablations import check_confirmatory_provenance  # noqa
        with tempfile.TemporaryDirectory() as td:
            td = Path(td)
            te_out = td / "template.json"
            _run([str(TEMPLATE), "--out", str(te_out)])
            # even paired with a GO-shaped manifest, unresolved/template terms must be refused in cross-check path
            paths = _synthetic_go_package_with_terms(td, json.loads(TE_BLOCKED.read_text()))
            pm_path = paths[0]
            prov = check_confirmatory_provenance("2025-08-01", "2025-10-31", "G4V5_CONFIRMATORY",
                                                 "prereg", "v5", confirmatory_flag=True,
                                                 provenance_manifest=pm_path, terms_evidence=str(te_out))
            self.assertIsNotNone(prov)
            self.assertTrue("not RESOLVED_VERIFIED" in prov or "NO_GO" in prov or "REFUSED" in prov.upper())


class TestTemplateNoDataNetworkCanonical(unittest.TestCase):
    def test_no_data_or_network_tokens_and_no_canonical_mutation(self):
        before = _canon()
        src = TEMPLATE.read_text(encoding="utf-8")
        # Code-level loader/network tokens (docstring may state "no outcomes" as policy text).
        for token in ["load_kline", "load_funding", "run_multisplit", "run_adversarial",
                      "run_persistence", "compute_outcome", "requests", "urllib.request",
                      "httpx", "aiohttp", "pd.read_", "read_parquet", "socket", "urlopen"]:
            self.assertNotIn(token, src, token)
        with tempfile.TemporaryDirectory() as td:
            out = Path(td) / "t.json"
            p = _run([str(TEMPLATE), "--out", str(out)])
            self.assertEqual(p.returncode, 0)
        self.assertEqual(before, _canon())

    def test_template_json_contains_loud_warning(self):
        with tempfile.TemporaryDirectory() as td:
            out = Path(td) / "t.json"
            _run([str(TEMPLATE), "--out", str(out)])
            tpl = json.loads(out.read_text())
            self.assertIn("NON-EVIDENTIARY", tpl["template_warning"])
            self.assertTrue(tpl["human_review_required"])


if __name__ == "__main__":
    unittest.main()
