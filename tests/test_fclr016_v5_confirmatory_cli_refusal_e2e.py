"""FCLR-016 v5 P0: end-to-end confirmatory CLI refusal before any data/outcome loading.

Covers:
- (a) `run_funding_ablations` confirmatory CLI on synthetic 2025+ invocation refuses
  via provenance/terms guard BEFORE any load_kline_series/load_funding_series/
  load_kline_panel/load_funding_panel or outcome computation (tmp-isolated, monkeypatched).
- (b) check_confirmatory_provenance with --terms-evidence cross-check rejects RESOLVED
  terms evidence missing required human fields, fabricated markers, agent-only reviewer,
  unresolved terms, and accepts synthetic fully-resolved fixtures (no false-accept).

Deterministic, no network, no canonical mutation.
"""
from __future__ import annotations

import copy
import hashlib
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "scripts"))
import run_funding_ablations as rfa  # noqa: E402
from run_funding_ablations import check_admissibility_package, check_confirmatory_provenance  # noqa: E402

RUN_FUNDING = REPO / "scripts" / "run_funding_ablations.py"
AUDIT = REPO / "research_state/fclr016_local_audit"
PM_REAL = AUDIT / "fclr016_v5_provenance_license_manifest_20261108T014405Z.json"
CA_REAL = AUDIT / "fclr016_v5_completeness_leakage_audit_20261108T014405Z.json"
TE_REAL = AUDIT / "fclr016_v5_terms_evidence_BLOCKED_20261108T014835Z.json"
PR_REAL = AUDIT / "fclr016_v5_confirmatory_prereg_DRAFT_20261108T014835Z.json"

SCOPE = {"window": "2025-08-01..2025-10-31", "months": ["2025-08", "2025-09", "2025-10"],
         "symbols": ["BTCUSDT", "ETHUSDT", "BNBUSDT", "SOLUSDT", "XRPUSDT"],
         "kinds": ["fundingRate", "klines", "markPriceKlines", "indexPriceKlines", "premiumIndexKlines"]}


def _write_json(td: Path, name: str, obj) -> str:
    p = td / name
    p.write_text(json.dumps(obj, indent=2, sort_keys=True))
    return str(p)


def _resolved_terms(**mut):
    te = {"artifact": "fclr016_v5_terms_evidence", "status": "RESOLVED_VERIFIED", "fabricated": False,
          "no_confirmatory_outcomes": True, "confirmatory_provenance_go": True, "admissibility_complete": True,
          "frozen_scope": SCOPE, "terms_url_reviewed": "https://example.invalid/terms",
          "access_date_utc": "2026-11-08T00:00:00Z",
          "terms_version_or_snapshot_id": "test-snapshot",
          "reviewer_role": "human maintainer (synthetic test fixture)",
          "conclusion": "PERMITTED_WITH_CONDITIONS", "conditions_or_restrictions": []}
    te.update(mut)
    return te


def _go_manifest(**mut):
    m = {"artifact": "fclr016_v5_provenance_license_manifest", "schema_version": 5,
         "confirmatory_provenance_go": True, "admissibility_complete": True,
         "no_confirmatory_outcomes": True, "fabricated": False, "confirmatory_claim_go": "GO",
         "cache_identity_vs_binance_vision": "GO_PARTIAL_BOUNDED_IDENTITY_ONLY", "frozen_scope": SCOPE,
         "license_terms": {"status": "RESOLVED_VERIFIED", "fabricated": False, "synthetic_test_fixture": True}}
    m.update(mut)
    return m


class Boom(Exception):
    pass


def _boom(*a, **k):
    raise Boom("DATA_LOAD_OR_OUTCOME_COMPUTATION_REACHED — guard failed")


class TestTermsEvidenceCrossCheckProvenanceGuard(unittest.TestCase):
    """(b) check_confirmatory_provenance + --terms-evidence rejects missing required human fields."""

    def _assert_refused(self, te_obj, manifest=None):
        with tempfile.TemporaryDirectory() as td:
            td = Path(td)
            tep = _write_json(td, "te.json", te_obj)
            mp = _write_json(td, "pm.json", manifest or _go_manifest())
            err = check_confirmatory_provenance(
                "2025-08-01", "2025-10-31", "G4V5_CONFIRMATORY", "prereg", "v5",
                confirmatory_flag=True, provenance_manifest=mp, terms_evidence=tep)
            self.assertIsNotNone(err, "expected refusal")
            return err

    def test_resolved_missing_terms_url_refused(self):
        self.assertIn("terms evidence", self._assert_refused(_resolved_terms(terms_url_reviewed="")).lower())

    def test_resolved_missing_access_date_refused(self):
        self.assertIn("terms evidence", self._assert_refused(_resolved_terms(access_date_utc=None)).lower())

    def test_resolved_missing_reviewer_refused(self):
        self.assertIn("terms evidence", self._assert_refused(_resolved_terms(reviewer_role="")).lower())

    def test_resolved_agent_only_reviewer_refused(self):
        self.assertIn("terms evidence", self._assert_refused(_resolved_terms(reviewer_role="automated agent only")).lower())

    def test_resolved_missing_conclusion_refused(self):
        self.assertIn("terms evidence", self._assert_refused(_resolved_terms(conclusion="")).lower())

    def test_resolved_fabricated_true_refused(self):
        err = self._assert_refused(_resolved_terms(fabricated=True))
        self.assertTrue("fabricated" in err.lower() or "terms evidence" in err.lower())

    def test_unresolved_terms_refused_even_with_go_manifest(self):
        te = json.loads(TE_REAL.read_text())
        err = self._assert_refused(te, manifest=_go_manifest())
        self.assertIn("not RESOLVED_VERIFIED", err)

    def test_terms_evidence_missing_file_refused(self):
        with tempfile.TemporaryDirectory() as td:
            mp = _write_json(Path(td), "pm.json", _go_manifest())
            err = check_confirmatory_provenance(
                "2025-08-01", "2025-10-31", "G4V5_CONFIRMATORY", "prereg", "v5",
                confirmatory_flag=True, provenance_manifest=mp, terms_evidence=str(Path(td) / "nope.json"))
        self.assertIsNotNone(err)
        self.assertIn("terms-evidence not found", err)

    def test_synthetic_resolved_terms_plus_go_manifest_accepted(self):
        with tempfile.TemporaryDirectory() as td:
            td = Path(td)
            tep = _write_json(td, "te.json", _resolved_terms())
            mp = _write_json(td, "pm.json", _go_manifest())
            err = check_confirmatory_provenance(
                "2025-08-01", "2025-10-31", "G4V5_CONFIRMATORY", "prereg", "v5",
                confirmatory_flag=True, provenance_manifest=mp, terms_evidence=tep)
            self.assertIsNone(err, err)

    def test_blocked_real_terms_crosscheck_refuses(self):
        err = check_confirmatory_provenance(
            "2025-08-01", "2025-10-31", "G4V5_CONFIRMATORY", "prereg", "v5",
            confirmatory_flag=True, provenance_manifest=str(PM_REAL), terms_evidence=str(TE_REAL))
        self.assertIsNotNone(err)


class TestConfirmatoryCLIRefusalBeforeDataLoad(unittest.TestCase):
    """(a) run_funding_ablations confirmatory CLI refuses before any data/outcome loading."""

    def _assert_no_load(self, argv, expect_refused=True):
        calls = {"kpanel": 0, "fpanel": 0, "ks": 0, "fs": 0, "multisplit": 0}
        def mk(name):
            def _f(*a, **k):
                calls[name] += 1
                raise Boom(name)
            return _f
        with patch.object(rfa, "load_kline_panel", mk("kpanel")), \
             patch.object(rfa, "load_funding_panel", mk("fpanel")), \
             patch.object(rfa, "load_kline_series", mk("ks")), \
             patch.object(rfa, "load_funding_series", mk("fs")), \
             patch.object(rfa, "run_multisplit", mk("multisplit")):
            try:
                rc = rfa.main(argv)
            except Boom as e:
                self.fail(f"data/outcome loading reached before guard: {e}")
        self.assertEqual(sum(calls.values()), 0, calls)
        if expect_refused:
            self.assertEqual(rc, 2)
        return rc, calls

    def test_confirmatory_2025_unprovenanced_refuses_no_load(self):
        self._assert_no_load([
            "--confirmatory", "--experiment-id", "G4V5_CONFIRMATORY_SYNTH",
            "--start", "2025-08-01", "--end", "2025-10-31",
            "--pre-registration", "research_state/fclr016_local_audit/fclr016_v5_confirmatory_prereg_DRAFT_20261108T014835Z.json",
            "--out-suffix", "_v5_confirmatory_synth",
        ])

    def test_confirmatory_with_blocked_provenance_manifest_refuses_no_load(self):
        self._assert_no_load([
            "--confirmatory", "--experiment-id", "G4V5_CONFIRMATORY_SYNTH",
            "--start", "2025-08-01", "--end", "2025-10-31",
            "--pre-registration", "research_state/fclr016_local_audit/fclr016_v5_confirmatory_prereg_DRAFT_20261108T014835Z.json",
            "--provenance-manifest", str(PM_REAL),
            "--out-suffix", "_v5_confirmatory_synth",
        ])

    def test_confirmatory_with_blocked_terms_evidence_crosscheck_refuses_no_load(self):
        with tempfile.TemporaryDirectory() as td:
            mp = _write_json(Path(td), "pm.json", _go_manifest())
            self._assert_no_load([
                "--confirmatory", "--experiment-id", "G4V5_CONFIRMATORY_SYNTH",
                "--start", "2025-08-01", "--end", "2025-10-31",
                "--pre-registration", "research_state/fclr016_local_audit/fclr016_v5_confirmatory_prereg_DRAFT_20261108T014835Z.json",
                "--provenance-manifest", mp, "--terms-evidence", str(TE_REAL),
                "--out-suffix", "_v5_confirmatory_synth",
            ])

    def test_confirmatory_with_resolved_terms_missing_human_fields_refuses_no_load(self):
        with tempfile.TemporaryDirectory() as td:
            td = Path(td)
            mp = _write_json(td, "pm.json", _go_manifest())
            tep = _write_json(td, "te.json", _resolved_terms(reviewer_role="automated agent"))
            self._assert_no_load([
                "--confirmatory", "--experiment-id", "G4V5_CONFIRMATORY_SYNTH",
                "--start", "2025-08-01", "--end", "2025-10-31",
                "--pre-registration", str(PR_REAL),
                "--provenance-manifest", mp, "--terms-evidence", tep,
                "--out-suffix", "_v5_confirmatory_synth",
            ])

    def test_subprocess_confirmatory_blocked_manifest_json_refusal(self):
        p = subprocess.run([sys.executable, str(RUN_FUNDING),
                            "--confirmatory", "--experiment-id", "G4V5_CONFIRMATORY_SYNTH",
                            "--start", "2025-08-01", "--end", "2025-10-31",
                            "--pre-registration", str(PR_REAL),
                            "--provenance-manifest", str(PM_REAL),
                            "--out-suffix", "_v5_confirmatory_synth"],
                           capture_output=True, text=True)
        self.assertEqual(p.returncode, 2)
        out = json.loads(p.stderr)
        self.assertEqual(out["status"], "REFUSED")
        self.assertIn("guard", out)

    def test_admissibility_package_check_mode_no_data_load(self):
        """Read-only package check must never touch loaders even when called via CLI path."""
        calls = {"kpanel": 0, "fpanel": 0, "ks": 0, "fs": 0, "multisplit": 0}
        def mk(name):
            def _f(*a, **k):
                calls[name] += 1
                raise Boom(name)
            return _f
        with patch.object(rfa, "load_kline_panel", mk("kpanel")), \
             patch.object(rfa, "load_funding_panel", mk("fpanel")), \
             patch.object(rfa, "load_kline_series", mk("ks")), \
             patch.object(rfa, "load_funding_series", mk("fs")), \
             patch.object(rfa, "run_multisplit", mk("multisplit")):
            rc = rfa.main(["--check-admissibility-package", str(PM_REAL), str(CA_REAL), str(TE_REAL), str(PR_REAL)])
        self.assertEqual(rc, 0)
        self.assertEqual(sum(calls.values()), 0, calls)

    def test_canonical_files_unchanged_after_refusal(self):
        before = {
            "frontier": (REPO / "research_state/experiment_frontier.json").read_bytes(),
            "manifest": (REPO / "research_state/run_manifest.json").read_bytes(),
            "summary": (REPO / "research_state/evaluation_summary.md").read_bytes(),
        }
        self._assert_no_load([
            "--confirmatory", "--experiment-id", "G4V5_CONFIRMATORY_SYNTH",
            "--start", "2025-08-01", "--end", "2025-10-31",
            "--pre-registration", str(PR_REAL),
            "--provenance-manifest", str(PM_REAL),
            "--out-suffix", "_v5_confirmatory_synth",
        ])
        self.assertEqual((REPO / "research_state/experiment_frontier.json").read_bytes(), before["frontier"])
        self.assertEqual((REPO / "research_state/run_manifest.json").read_bytes(), before["manifest"])
        self.assertEqual((REPO / "research_state/evaluation_summary.md").read_bytes(), before["summary"])


if __name__ == "__main__":
    unittest.main()
