"""FCLR-024: deterministic tmp-isolated tests for read-only v5 scope-coherence report.

Proves: never claims GO/confirmatory_outcomes_permitted; emits explicit scope-alignment
blocker matrix; references local 2024-04..09 evidence as present_unverified/bounded only;
refuses missing/malformed inputs; no network/outcomes/data loading; no canonical mutation.
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
SCRIPT = REPO / "scripts" / "fclr024_v5_scope_coherence_report.py"
AUDIT = REPO / "research_state/fclr016_local_audit"
PM_REAL = AUDIT / "fclr016_v5_provenance_license_manifest_20261108T014405Z.json"
CA_REAL = AUDIT / "fclr016_v5_completeness_leakage_audit_20261108T014405Z.json"
TE_REAL = AUDIT / "fclr016_v5_terms_evidence_BLOCKED_20261108T014835Z.json"
PR_2024 = REPO / "research_state/fclr016_v5_confirmatory_prereg_DRAFT_NOT_FROZEN_20261108T213600Z.json"
CANONICAL = [
    REPO / "research_state/experiment_frontier.json",
    REPO / "research_state/run_manifest.json",
    REPO / "research_state/evaluation_summary.md",
]


def _canonical_bytes():
    return {str(p): p.read_bytes() for p in CANONICAL if p.exists()}


def _load_mod():
    spec = importlib.util.spec_from_file_location("fclr024_testmod", SCRIPT)
    mod = importlib.util.module_from_spec(spec)
    assert spec and spec.loader
    spec.loader.exec_module(mod)
    return mod


def _run_cli(args):
    return subprocess.run([sys.executable, str(SCRIPT), *args], capture_output=True, text=True)


class TestScopeCoherenceRealScopedPackage(unittest.TestCase):
    def test_real_scoped_prereg_reports_scope_mismatch_never_go(self):
        before = _canonical_bytes()
        p = _run_cli([str(PM_REAL), str(CA_REAL), str(TE_REAL), str(PR_2024), "--json-only"])
        self.assertEqual(before, _canonical_bytes())
        self.assertEqual(p.returncode, 0)
        out = json.loads(p.stdout)
        self.assertEqual(out["validator"], "fclr024_v5_scope_coherence_report")
        self.assertFalse(out["all_go"])
        self.assertFalse(out["confirmatory_outcomes_permitted"])
        self.assertFalse(out["creates_or_satisfies_evidence"])
        self.assertFalse(out["fabricates_provenance_completeness_license"])
        self.assertTrue(out["scope_coherence"]["prereg_scope_mismatch_vs_provenance_completeness"])
        self.assertEqual(out["scope_coherence"]["scope_windows"]["confirmatory_prereg"], "2024-04-01..2024-09-30")
        self.assertEqual(out["scope_coherence"]["scope_windows"]["provenance_license_manifest"], "2025-08-01..2025-10-31")
        matrix = {r["gate"]: r for r in out["gate_blocker_matrix"]}
        self.assertIn("scope_alignment_prereg_vs_provenance_completeness", matrix)
        self.assertTrue(matrix["scope_alignment_prereg_vs_provenance_completeness"]["blocker"])
        self.assertIn("prereg scope window mismatch", " ".join(out["errors"]))

    def test_local_2024_evidence_refs_present_unverified_only(self):
        mod = _load_mod()
        report = mod.build_scope_coherence_report(PM_REAL, CA_REAL, TE_REAL, PR_2024)
        self.assertFalse(report["all_go"])
        self.assertFalse(report["confirmatory_outcomes_permitted"])
        refs = report["local_2024_04_09_evidence_refs"]
        self.assertGreaterEqual(len(refs), 2)
        ids = {r["id"] for r in refs}
        self.assertIn("fclr015_input_manifest_2024_04_09", ids)
        self.assertIn("fclr017_gate4_cache_coverage_audit_latest", ids)
        for r in refs:
            self.assertTrue(r["reference_only"])
            self.assertFalse(r["usable_as_confirmatory_go"])
            self.assertFalse(r["confirmatory_go"])
            if r["evidence"].get("present"):
                self.assertTrue(r["present_unverified_bounded"])
                self.assertTrue(r["evidence"]["sha256"])


class TestScopeCoherenceRefusals(unittest.TestCase):
    def test_missing_file_refuses_no_go(self):
        before = _canonical_bytes()
        p = _run_cli([str(PM_REAL), str(CA_REAL), str(TE_REAL), "/nonexistent/pr.json"])
        self.assertEqual(before, _canonical_bytes())
        self.assertNotEqual(p.returncode, 0)
        out = json.loads(p.stdout.strip().splitlines()[0])
        self.assertFalse(out.get("all_go", True))
        self.assertFalse(out.get("confirmatory_outcomes_permitted", True))
        self.assertIn("missing", out.get("error", ""))

    def test_malformed_json_refuses_no_go(self):
        before = _canonical_bytes()
        with tempfile.TemporaryDirectory() as td:
            bad = Path(td) / "bad.json"
            bad.write_text("{not json")
            p = _run_cli([str(PM_REAL), str(CA_REAL), str(bad), str(PR_2024)])
        self.assertEqual(before, _canonical_bytes())
        self.assertNotEqual(p.returncode, 0)
        out = json.loads(p.stdout.strip().splitlines()[0])
        self.assertFalse(out.get("all_go", True))
        self.assertFalse(out.get("confirmatory_outcomes_permitted", True))


class TestScopeCoherenceNoDataLoading(unittest.TestCase):
    def test_no_data_network_tokens_in_script(self):
        src = SCRIPT.read_text(encoding="utf-8")
        for token in ("load_kline", "load_funding", "run_multisplit", "requests", "urllib.request", "httpx", "aiohttp", "pd.read_", "read_parquet"):
            self.assertNotIn(token, src)

    def test_module_import_safe_and_never_claims_go(self):
        sys.path.insert(0, str(REPO / "scripts"))
        import run_funding_ablations as rfa  # noqa
        boom = lambda *a, **k: (_ for _ in ()).throw(AssertionError("loader called"))
        sentinels = {}
        for name in ("load_kline_series", "load_funding_series", "run_multisplit", "run_adversarial"):
            if hasattr(rfa, name):
                sentinels[name] = getattr(rfa, name)
                setattr(rfa, name, boom)
        try:
            mod = _load_mod()
            report = mod.build_scope_coherence_report(PM_REAL, CA_REAL, TE_REAL, PR_2024)
        finally:
            for name, orig in sentinels.items():
                setattr(rfa, name, orig)
        self.assertFalse(report["all_go"])
        self.assertFalse(report["confirmatory_outcomes_permitted"])


if __name__ == "__main__":
    unittest.main()
