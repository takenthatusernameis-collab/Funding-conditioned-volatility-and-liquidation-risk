"""FCLR-016 v5 preflight summary tests (deterministic, tmp-isolated, no network/outcomes).

Proves the read-only preflight summary:
- never claims GO / confirmatory_outcomes_permitted on blocked/template/malformed inputs;
- refuses missing/fabricated/resolved-without-human-fields/agent-only reviewer cases via parity gates;
- runs validator/package/report parity (no data loading) and emits machine-readable JSON + markdown
  human action checklist + refusal matrix;
- cannot mutate canonical research artifacts;
- has no data/network loader references.
"""
from __future__ import annotations

import copy
import hashlib
import importlib.util
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
SCRIPT = REPO / "scripts" / "fclr016_v5_preflight_summary.py"
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
SCOPE = {"window": "2025-08-01..2025-10-31", "months": ["2025-08", "2025-09", "2025-10"],
         "symbols": ["BTCUSDT"], "kinds": ["fundingRate"]}


def _canonical_bytes():
    return {str(p): p.read_bytes() for p in CANONICAL if p.exists()}


def _load_mod():
    spec = importlib.util.spec_from_file_location("fclr016_v5_preflight_summary_testmod", SCRIPT)
    mod = importlib.util.module_from_spec(spec)
    assert spec and spec.loader
    spec.loader.exec_module(mod)
    return mod


def _run_cli(args):
    return subprocess.run([sys.executable, str(SCRIPT), *args], capture_output=True, text=True)


def _write_pkg(td: Path, pm, ca, te, pr):
    paths = [td / "pm.json", td / "ca.json", td / "te.json", td / "pr.json"]
    for p, d in zip(paths, (pm, ca, te, pr)):
        p.write_text(json.dumps(d, indent=2, sort_keys=True))
    return [str(p) for p in paths]


class TestRealBlockedPackage(unittest.TestCase):
    def test_never_claims_go_and_emits_checklist_refusal_matrix(self):
        before = _canonical_bytes()
        mod = _load_mod()
        s = mod.build_preflight_summary(PM_REAL, CA_REAL, TE_REAL, PR_REAL)
        after = _canonical_bytes()
        self.assertEqual(before, after, "canonical artifacts mutated")
        self.assertFalse(s["all_go"])
        self.assertFalse(s["confirmatory_outcomes_permitted"])
        self.assertTrue(s["expect_go_refused"])
        self.assertTrue(s["blockers"])
        self.assertTrue(all(v is False for v in s["gates"].values()))
        # required human fields
        field_names = [x["field"] if isinstance(x, dict) else str(x) for x in s["required_human_terms_fields"]]
        for req in ("terms_url_reviewed", "access_date_utc", "reviewer_role", "conclusion", "fabricated", "status"):
            self.assertTrue(any(req in n for n in field_names), f"missing human field: {req}")
        self.assertTrue(any("fabricated!=false" in x.get("forbidden", "") or "fabricated" in x.get("forbidden", "") for x in s["forbidden_values"]))
        self.assertTrue(any("agent" in x.get("forbidden", "").lower() for x in s["forbidden_values"]))
        self.assertTrue(any("template" in x.get("forbidden", "").lower() for x in s["forbidden_values"]))
        # promotion sequence / refusal matrix
        seq = " ".join(s["promotion_sequence"])
        self.assertIn("RESOLVED", seq)
        self.assertIn("reconcile", seq.lower())
        self.assertIn("--expect-go", seq)
        self.assertIn("must not load data on refusal", seq)
        attempts = " ".join(r["attempt"] for r in s["refusal_matrix"])
        for needle in ("draft", "RESOLVED", "GO", "data", "fabricated"):
            self.assertIn(needle.lower(), attempts.lower(), f"missing refusal attempt: {needle}")
        self.assertTrue(all(r["status"] == "REFUSED" for r in s["refusal_matrix"] if "terms" in r["attempt"].lower() or "draft" in r["attempt"].lower() or "GO" in r["attempt"]))
        # hashes present
        for key in ("provenance_license_manifest", "completeness_leakage_audit", "terms_evidence", "confirmatory_prereg"):
            self.assertEqual(len(s["artifacts"][key]["sha256"]), 64)

    def test_cli_emits_json_and_markdown_no_go(self):
        before = _canonical_bytes()
        p = _run_cli([str(PM_REAL), str(CA_REAL), str(TE_REAL), str(PR_REAL)])
        self.assertEqual(before, _canonical_bytes())
        self.assertIn("---MARKDOWN---", p.stdout)
        out = json.loads(p.stdout.split("---MARKDOWN---", 1)[0])
        self.assertFalse(out["all_go"])
        self.assertFalse(out["confirmatory_outcomes_permitted"])
        self.assertEqual(out["validator"], "fclr016_v5_preflight_summary")
        md = p.stdout.split("---MARKDOWN---", 1)[1]
        self.assertIn("all_go: False", md)
        self.assertIn("Human action checklist", md)
        self.assertIn("Refusal matrix", md)
        self.assertNotIn("all_go: True", md)


class TestRefusesBadInputs(unittest.TestCase):
    def test_missing_file_refuses(self):
        before = _canonical_bytes()
        p = _run_cli([str(PM_REAL), str(CA_REAL), str(TE_REAL), "/nonexistent/prereg.json"])
        self.assertEqual(before, _canonical_bytes())
        self.assertNotEqual(p.returncode, 0)
        out = json.loads(p.stdout.strip().splitlines()[0])
        self.assertFalse(out.get("ok", True))
        self.assertFalse(out.get("all_go", False))
        self.assertFalse(out.get("confirmatory_outcomes_permitted", False))
        self.assertIn("missing", out.get("error", ""))

    def test_malformed_json_refuses_no_go(self):
        before = _canonical_bytes()
        with tempfile.TemporaryDirectory() as td:
            td = Path(td)
            bad = td / "bad.json"
            bad.write_text("{not json")
            p = _run_cli([str(PM_REAL), str(CA_REAL), str(bad), str(PR_REAL)])
        self.assertEqual(before, _canonical_bytes())
        self.assertNotEqual(p.returncode, 0)
        out = json.loads(p.stdout.strip().splitlines()[0])
        self.assertFalse(out.get("all_go", False))
        self.assertFalse(out.get("confirmatory_outcomes_permitted", False))

    def _assert_never_go(self, te_mut, pr_mut=None, pm_mut=None):
        before = _canonical_bytes()
        with tempfile.TemporaryDirectory() as td:
            td = Path(td)
            pm = json.loads(PM_REAL.read_text()); ca = json.loads(CA_REAL.read_text())
            te = json.loads(TE_REAL.read_text()); pr = json.loads(PR_REAL.read_text())
            te.update(te_mut)
            if pr_mut: pr.update(pr_mut)
            if pm_mut: pm.update(pm_mut)
            paths = _write_pkg(td, pm, ca, te, pr)
            p = _run_cli(paths)
        self.assertEqual(before, _canonical_bytes())
        text = p.stdout
        if "---MARKDOWN---" in text:
            out = json.loads(text.split("---MARKDOWN---", 1)[0])
        else:
            out = json.loads(text.strip().splitlines()[0])
        self.assertFalse(out.get("all_go", False), out)
        self.assertFalse(out.get("confirmatory_outcomes_permitted", False), out)

    def test_fabricated_resolved_never_go(self):
        self._assert_never_go({"status": "RESOLVED_VERIFIED", "fabricated": True,
                               "terms_url_reviewed": "https://example.invalid", "access_date_utc": "2026-11-08T00:00:00Z",
                               "reviewer_role": "human maintainer", "conclusion": "PERMITTED"})

    def test_resolved_missing_human_fields_never_go(self):
        self._assert_never_go({"status": "RESOLVED_VERIFIED", "fabricated": False,
                               "terms_url_reviewed": "", "reviewer_role": "human maintainer",
                               "access_date_utc": "2026-11-08T00:00:00Z", "conclusion": "PERMITTED"})

    def test_agent_only_reviewer_never_go(self):
        self._assert_never_go({"status": "RESOLVED_VERIFIED", "fabricated": False,
                               "terms_url_reviewed": "https://example.invalid", "access_date_utc": "2026-11-08T00:00:00Z",
                               "reviewer_role": "automated agent only", "conclusion": "PERMITTED"})

    def test_template_as_evidence_never_go(self):
        self._assert_never_go({"status": "TEMPLATE_NOT_EVIDENCE", "fabricated": False})

    def test_draft_promoted_claims_never_go(self):
        self._assert_never_go({}, pr_mut={"draft": False, "confirmatory_claim_go": "GO", "admissibility_complete": True,
                                          "frozen_before_outcomes": True, "license_terms_resolved": True})


class TestParityAndNoDataLoading(unittest.TestCase):
    def test_parity_with_package_check(self):
        mod = _load_mod()
        s = mod.build_preflight_summary(PM_REAL, CA_REAL, TE_REAL, PR_REAL)
        sys.path.insert(0, str(REPO / "scripts"))
        import run_funding_ablations as rfa
        pkg = rfa.check_admissibility_package(str(PM_REAL), str(CA_REAL), str(TE_REAL), str(PR_REAL), expect_go=True)
        self.assertEqual(s["all_go"], pkg.get("all_go"))
        self.assertEqual(s["confirmatory_outcomes_permitted"], pkg.get("confirmatory_outcomes_permitted"))
        self.assertEqual(s["gates"], pkg.get("gates"))
        self.assertEqual(s["blockers"], pkg.get("blockers"))
        self.assertEqual(s["package_parity"]["all_go"], pkg.get("all_go"))

    def test_module_has_no_data_or_network_tokens(self):
        src = SCRIPT.read_text(encoding="utf-8")
        forbidden = ["load_kline", "load_funding", "run_multisplit", "run_adversarial", "run_persistence",
                     "requests", "urllib.request", "httpx", "aiohttp", "pd.read_", "read_parquet", "numpy", "pandas"]
        for token in forbidden:
            self.assertNotIn(token, src, f"preflight summary must not reference: {token}")

    def test_build_path_never_calls_outcome_loaders(self):
        before = _canonical_bytes()
        sys.path.insert(0, str(REPO / "scripts"))
        import run_funding_ablations as rfa
        boom = lambda *a, **k: (_ for _ in ()).throw(AssertionError("data/outcome loader called"))
        sentinels = {}
        for name in ("load_kline_series", "load_funding_series", "load_kline_panel", "load_funding_panel",
                     "run_multisplit", "run_adversarial", "run_persistence"):
            if hasattr(rfa, name):
                sentinels[name] = getattr(rfa, name)
                setattr(rfa, name, boom)
        try:
            mod = _load_mod()
            s = mod.build_preflight_summary(PM_REAL, CA_REAL, TE_REAL, PR_REAL)
        finally:
            for name, orig in sentinels.items():
                setattr(rfa, name, orig)
        self.assertEqual(before, _canonical_bytes())
        self.assertFalse(s["all_go"])


if __name__ == "__main__":
    unittest.main()
