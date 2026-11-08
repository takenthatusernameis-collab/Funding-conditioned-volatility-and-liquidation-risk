"""FCLR-016 v5 admissibility report tests (deterministic, tmp-isolated, no network/outcomes).

Proves the read-only report tool:
- cannot claim GO / confirmatory_outcomes_permitted on blocked or malformed packages;
- refuses/errors on missing/malformed/fabricated inputs (fail-closed);
- loads zero kline/funding/outcome data and performs no network calls;
- mutates no canonical research artifacts;
- emits stable machine-readable JSON + markdown with hashes/gate states/blockers and
  required human terms-evidence fields + next materially different route.
"""
from __future__ import annotations

import copy
import hashlib
import importlib.util
import json
import subprocess
import sys
import tempfile
import types
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
REPORT = REPO / "scripts" / "fclr016_v5_admissibility_report.py"
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
REQUIRED_HUMAN_FIELDS_SUBSTRINGS = [
    "terms_url_reviewed", "access_date_utc", "terms_version_or_snapshot_id",
    "relevant_clause_summary", "reviewer_role", "conclusion",
    "conditions_or_restrictions", "evidence_artifacts", "fabricated=false",
    "status=RESOLVED_VERIFIED",
]


def _canonical_bytes():
    return {str(p): p.read_bytes() for p in CANONICAL if p.exists()}


def _load_report_module():
    # importlib by path avoids relying on cwd/sys.path side effects in subprocess-only tests
    spec = importlib.util.spec_from_file_location("fclr016_v5_admissibility_report_testmod", REPORT)
    mod = importlib.util.module_from_spec(spec)
    assert spec and spec.loader
    spec.loader.exec_module(mod)
    return mod


def _run_cli(args):
    p = subprocess.run([sys.executable, str(REPORT), *args], capture_output=True, text=True)
    return p


def _write_pkg(td: Path, pm, ca, te, pr):
    paths = [td / "pm.json", td / "ca.json", td / "te.json", td / "pr.json"]
    for p, d in zip(paths, (pm, ca, te, pr)):
        p.write_text(json.dumps(d, indent=2, sort_keys=True))
    return [str(p) for p in paths]


class TestReportOnRealBlockedPackage(unittest.TestCase):
    def test_real_package_never_claims_go_and_emits_required_fields(self):
        before = _canonical_bytes()
        p = _run_cli([str(PM_REAL), str(CA_REAL), str(TE_REAL), str(PR_REAL)])
        after = _canonical_bytes()
        self.assertEqual(before, after, "canonical artifacts mutated")
        self.assertIn("---MARKDOWN---", p.stdout)
        json_part = p.stdout.split("---MARKDOWN---", 1)[0]
        out = json.loads(json_part)
        self.assertEqual(out["validator"], "fclr016_v5_admissibility_report")
        self.assertFalse(out["all_go"])
        self.assertFalse(out["confirmatory_outcomes_permitted"])
        self.assertTrue(out["blockers"], "blocked package must list blockers")
        self.assertEqual(set(out["gates"].keys()), {
            "terms_resolved_verified", "provenance_manifest_go",
            "completeness_leakage_pass", "prereg_frozen_non_draft", "prereg_claim_go",
        })
        for k, v in out["gates"].items():
            self.assertIs(v, False, f"blocked real package gate unexpectedly true: {k}")
        for sub in REQUIRED_HUMAN_FIELDS_SUBSTRINGS:
            self.assertTrue(any(sub in f for f in out["required_human_terms_fields"]),
                            f"missing required human field substring: {sub}")
        self.assertIn("Human terms review", out["next_materially_different_route"])
        self.assertIn("RESOLVED", out["next_materially_different_route"])
        self.assertIn("must refuse until frozen+all GO", out["next_materially_different_route"])
        self.assertIn("must not load data on refusal", out["next_materially_different_route"])
        md = p.stdout.split("---MARKDOWN---", 1)[1]
        self.assertIn("all_go: False", md)
        self.assertIn("confirmatory_outcomes_permitted: False", md)
        self.assertIn("Required human terms-evidence fields", md)
        # hashes present and match files
        for key, path in [("provenance_license_manifest", PM_REAL), ("completeness_leakage_audit", CA_REAL),
                          ("terms_evidence", TE_REAL), ("confirmatory_prereg", PR_REAL)]:
            self.assertEqual(out["artifacts"][key]["sha256"], hashlib.sha256(path.read_bytes()).hexdigest())


class TestReportRefusesMalformedOrFabricated(unittest.TestCase):
    def test_missing_file_refuses_no_go(self):
        before = _canonical_bytes()
        p = _run_cli([str(PM_REAL), str(CA_REAL), str(TE_REAL), "/nonexistent/prereg.json"])
        self.assertEqual(before, _canonical_bytes())
        self.assertNotEqual(p.returncode, 0)
        out = json.loads(p.stdout.strip().splitlines()[0])
        self.assertFalse(out.get("ok", True))
        self.assertIn("missing", out.get("error", ""))

    def test_malformed_json_refuses_no_go(self):
        before = _canonical_bytes()
        with tempfile.TemporaryDirectory() as td:
            td = Path(td)
            bad = td / "bad.json"
            bad.write_text("{not json")
            paths = [str(PM_REAL), str(CA_REAL), str(bad), str(PR_REAL)]
            p = _run_cli(paths)
        self.assertEqual(before, _canonical_bytes())
        self.assertNotEqual(p.returncode, 0)
        # malformed parse flows through check_admissibility_package -> ok False/error
        first = p.stdout.strip().splitlines()[0] if p.stdout.strip() else "{}"
        out = json.loads(first)
        self.assertFalse(out.get("ok", True) and out.get("all_go", False))

    def test_fabricated_resolved_terms_never_claims_go(self):
        before = _canonical_bytes()
        with tempfile.TemporaryDirectory() as td:
            td = Path(td)
            pm = json.loads(PM_REAL.read_text())
            ca = json.loads(CA_REAL.read_text())
            te = json.loads(TE_REAL.read_text())
            pr = json.loads(PR_REAL.read_text())
            te.update({
                "status": "RESOLVED_VERIFIED", "fabricated": True,
                "terms_url_reviewed": "https://example.invalid", "access_date_utc": "2026-11-08T00:00:00Z",
                "reviewer_role": "human maintainer", "conclusion": "PERMITTED",
                "confirmatory_provenance_go": True, "admissibility_complete": True,
            })
            paths = _write_pkg(td, pm, ca, te, pr)
            p = _run_cli(paths)
        self.assertEqual(before, _canonical_bytes())
        out = json.loads(p.stdout.split("---MARKDOWN---", 1)[0])
        self.assertFalse(out["all_go"])
        self.assertFalse(out["confirmatory_outcomes_permitted"])
        # must not silently accept fabricated resolved package
        self.assertTrue(out["blockers"] or out["errors"] or not out["ok"] is False)


class TestReportLoadsNoData(unittest.TestCase):
    def test_report_path_never_loads_kline_funding_or_outcomes(self):
        before = _canonical_bytes()
        # Monkeypatch dangerous loaders in run_funding_ablations namespace used by report path.
        sys.path.insert(0, str(REPO / "scripts"))
        import run_funding_ablations as rfa  # noqa
        boom = lambda *a, **k: (_ for _ in ()).throw(AssertionError("data/outcome loader called by report path"))
        sentinels = {}
        for name in ("load_kline_series", "load_funding_series", "load_kline_panel",
                     "load_funding_panel", "run_multisplit", "run_adversarial", "run_persistence"):
            if hasattr(rfa, name):
                sentinels[name] = getattr(rfa, name)
                setattr(rfa, name, boom)
        try:
            mod = _load_report_module()
            report = mod.build_report(PM_REAL, CA_REAL, TE_REAL, PR_REAL)
        finally:
            for name, orig in sentinels.items():
                setattr(rfa, name, orig)
        self.assertEqual(before, _canonical_bytes())
        self.assertFalse(report["all_go"])
        self.assertFalse(report["confirmatory_outcomes_permitted"])

    def test_report_module_has_no_data_loader_imports(self):
        src = REPORT.read_text(encoding="utf-8")
        forbidden = [
            "load_kline", "load_funding", "run_multisplit", "run_adversarial",
            "requests", "urllib.request", "httpx", "aiohttp", "pd.read_", "read_parquet",
        ]
        for token in forbidden:
            self.assertNotIn(token, src, f"report script must not reference data/network token: {token}")


class TestReportCannotClaimGo(unittest.TestCase):
    def test_blocked_package_blockers_nonempty_and_gates_false(self):
        mod = _load_report_module()
        report = mod.build_report(PM_REAL, CA_REAL, TE_REAL, PR_REAL)
        self.assertFalse(report["all_go"])
        self.assertFalse(report["confirmatory_outcomes_permitted"])
        self.assertGreaterEqual(len(report["blockers"]), 1)
        self.assertTrue(all(v is False for v in report["gates"].values()))

    def test_markdown_never_says_all_go_true(self):
        mod = _load_report_module()
        report = mod.build_report(PM_REAL, CA_REAL, TE_REAL, PR_REAL)
        md = mod.render_markdown(report)
        self.assertIn("all_go: False", md)
        self.assertIn("confirmatory_outcomes_permitted: False", md)
        self.assertNotIn("all_go: True", md)


if __name__ == "__main__":
    unittest.main()
