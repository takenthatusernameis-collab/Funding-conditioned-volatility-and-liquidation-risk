"""FCLR-NEXT-132: v5 admissibility CLI/guard refusal parity under edge seams.

Covers handoff deliverables (tmp-isolated, deterministic, no network, no
kline/funding/outcome loaders, no real research_state writes):
1. Empty/unreadable/nonexistent data-path seams under valid prereg/package refs:
   confirmatory/expect-go paths remain blocked with stable machine-readable reason
   codes and NO outcome/data loader is called.
2. CLI argparse/edge-case contracts for preflight/admissibility-report/promotion-dryrun:
   missing/extra args, malformed JSON, unreadable files, candidate-path edges.
   Refusal output stable: ok:false or explicit refusal, all_go:false where
   applicable, confirmatory_outcomes_permitted:false, no GO claim.
3. Cross-CLI parity + canonical/output integrity: same real blocked 4-artifact
   package => consistent blocked/refusal semantics; same synthetic tmp GO fixture
   (labeled synthetic_test_fixture=true, no_real_terms_evidence=true semantics in
   fixture metadata) => consistent synthetic-only GO semantics in dryrun fixture
   scenario only, never real evidence/canonicals mutated.
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
import fclr016_v5_preflight_summary as preflight  # noqa: E402
import fclr016_v5_admissibility_report as adm_report  # noqa: E402
import fclr016_v5_promotion_dryrun as dryrun  # noqa: E402

AUDIT = REPO / "research_state/fclr016_local_audit"
PM = AUDIT / "fclr016_v5_provenance_license_manifest_20261108T014405Z.json"
CA = AUDIT / "fclr016_v5_completeness_leakage_audit_20261108T014405Z.json"
TE = AUDIT / "fclr016_v5_terms_evidence_BLOCKED_20261108T014835Z.json"
PR = AUDIT / "fclr016_v5_confirmatory_prereg_DRAFT_20261108T014835Z.json"
REAL_BLOCKED = [PM, CA, TE, PR]

SCOPE = {"window": "2025-08-01..2025-10-31", "months": ["2025-08", "2025-09", "2025-10"],
         "symbols": ["BTCUSDT", "ETHUSDT", "BNBUSDT", "SOLUSDT", "XRPUSDT"],
         "kinds": ["fundingRate", "klines", "markPriceKlines", "indexPriceKlines", "premiumIndexKlines"]}
CLIS = [
    ("preflight", [sys.executable, str(REPO / "scripts/fclr016_v5_preflight_summary.py")]),
    ("report", [sys.executable, str(REPO / "scripts/fclr016_v5_admissibility_report.py")]),
    ("promotion_dryrun", [sys.executable, str(REPO / "scripts/fclr016_v5_promotion_dryrun.py")]),
]


def _write_json(td: Path, name: str, obj) -> Path:
    p = td / name
    p.write_text(json.dumps(obj, indent=2, sort_keys=True), encoding="utf-8")
    return p


def _resolved_terms(**mut):
    te = {"artifact": "fclr016_v5_terms_evidence", "status": "RESOLVED_VERIFIED", "fabricated": False,
          "no_confirmatory_outcomes": True, "confirmatory_provenance_go": True, "admissibility_complete": True,
          "frozen_scope": SCOPE, "terms_url_reviewed": "https://example.invalid/terms",
          "access_date_utc": "2026-11-08T00:00:00Z", "terms_version_or_snapshot_id": "synthetic-snapshot",
          "reviewer_role": "human maintainer (synthetic test fixture, no real terms evidence)",
          "conclusion": "PERMITTED", "conditions_or_restrictions": [],
          "synthetic_test_fixture": True, "no_real_terms_evidence": True}
    te.update(mut)
    return te


def _go_manifest(**mut):
    m = {"artifact": "fclr016_v5_provenance_license_manifest", "schema_version": 5,
         "confirmatory_provenance_go": True, "admissibility_complete": True,
         "no_confirmatory_outcomes": True, "fabricated": False, "confirmatory_claim_go": "GO",
         "cache_identity_vs_binance_vision": "GO_PARTIAL_BOUNDED", "frozen_scope": SCOPE,
         "license_terms": {"status": "RESOLVED_VERIFIED", "fabricated": False, "synthetic_test_fixture": True}}
    m.update(mut)
    return m


def _go_completeness(**mut):
    ca = {"artifact": "fclr016_v5_completeness_leakage_audit", "verdict": "PASS_COMPLETENESS_LEAKAGE_DETERMINISTIC",
          "admissibility_complete": True, "completeness": {"ok": True}, "no_confirmatory_outcomes": True,
          "fabricated": False, "confirmatory_claim_go": "NO_GO", "frozen_scope": SCOPE}
    ca.update(mut)
    return ca


def _go_prereg(pm_p: Path, ca_p: Path, te_p: Path, **mut):
    pr = {"artifact": "fclr016_v5_confirmatory_prereg", "draft": False, "frozen_before_outcomes": True,
          "promotable_to_frozen": True, "admissibility_complete": True, "license_terms_resolved": True,
          "confirmatory_claim_go": "GO", "confirmatory_provenance_go": True, "no_confirmatory_outcomes": True,
          "frozen_scope": SCOPE, "gates": {"confirmatory_outcomes_permitted": True},
          "admissibility_refs_sha256": {
              "provenance_license_manifest": hashlib.sha256(pm_p.read_bytes()).hexdigest(),
              "completeness_leakage_audit": hashlib.sha256(ca_p.read_bytes()).hexdigest(),
              "terms_evidence": hashlib.sha256(te_p.read_bytes()).hexdigest(),
          }}
    pr.update(mut)
    return pr


def _parse_json_stdout(stdout: str):
    for line in stdout.splitlines():
        s = line.strip()
        if s.startswith("{"):
            try:
                return json.loads(s if "\n" not in s else stdout.split("---MARKDOWN---")[0])
            except Exception:
                pass
    return json.loads(stdout.split("---MARKDOWN---")[0].strip())


def _assert_refusal_contract(self, obj, *, expect_all_go_key=True):
    self.assertIsInstance(obj, dict)
    self.assertFalse(obj.get("ok"), obj)
    self.assertFalse(obj.get("confirmatory_outcomes_permitted"), obj)
    if expect_all_go_key or "all_go" in obj:
        self.assertFalse(obj.get("all_go"), obj)
    # never a GO claim
    text = json.dumps(obj, sort_keys=True).upper()
    self.assertNotIn('"CONFIRMATORY_CLAIM_GO": "GO"', text.replace(" ", ""))
    self.assertFalse(obj.get("confirmatory_provenance_go") is True and obj.get("all_go") is True, obj)


class TestMalformedUnreadableEdgeSeams(unittest.TestCase):
    def test_malformed_json_all_clis_stable_refusal(self):
        with tempfile.TemporaryDirectory() as td:
            bad = _write_json(Path(td), "bad.json", None)
            bad.write_text("{not json", encoding="utf-8")
            for name, cmd in CLIS:
                p = subprocess.run(cmd + [str(bad), str(CA), str(TE), str(PR)], capture_output=True, text=True)
                self.assertEqual(p.returncode, 2, (name, p.stdout, p.stderr))
                j = _parse_json_stdout(p.stdout)
                _assert_refusal_contract(self, j)
                self.assertIn("cannot", (j.get("error") or "").lower() + json.dumps(j).lower(), (name, j))

    def test_unreadable_directory_path_all_clis_stable_refusal(self):
        with tempfile.TemporaryDirectory() as td:
            d = Path(td) / "adir"
            d.mkdir()
            for name, cmd in CLIS:
                p = subprocess.run(cmd + [str(d), str(CA), str(TE), str(PR)], capture_output=True, text=True)
                self.assertEqual(p.returncode, 2, name)
                j = _parse_json_stdout(p.stdout)
                _assert_refusal_contract(self, j)
                self.assertIn("not a file", (j.get("error") or "").lower(), (name, j))

    def test_nonexistent_file_all_clis_stable_refusal(self):
        missing = "/nonexistent/fclr016_v5_missing_132.json"
        for name, cmd in CLIS:
            p = subprocess.run(cmd + [missing, str(CA), str(TE), str(PR)], capture_output=True, text=True)
            self.assertEqual(p.returncode, 2, name)
            j = _parse_json_stdout(p.stdout)
            _assert_refusal_contract(self, j)
            self.assertIn("missing", (j.get("error") or "").lower(), (name, j))

    def test_run_funding_ablations_check_package_malformed_unreadable_nonexistent(self):
        cmd = [sys.executable, str(REPO / "scripts/run_funding_ablations.py"), "--check-admissibility-package"]
        with tempfile.TemporaryDirectory() as td:
            td = Path(td)
            bad = td / "bad.json"; bad.write_text("{bad", encoding="utf-8")
            d = td / "adir"; d.mkdir()
            for target in [str(bad), str(d), "/nonexistent/nope.json"]:
                p = subprocess.run(cmd + [target, str(CA), str(TE), str(PR)], capture_output=True, text=True)
                self.assertEqual(p.returncode, 2, target)
                j = json.loads(p.stdout)
                self.assertFalse(j.get("ok"), j)
                self.assertFalse(j.get("all_go"), j)
                self.assertFalse(j.get("confirmatory_outcomes_permitted"), j)
                self.assertEqual(j.get("validator"), "run_funding_ablations.admissibility_package")

    def test_run_funding_ablations_expect_go_malformed_package_refuses_no_load(self):
        calls = {"k": 0, "f": 0, "m": 0}
        def boom(name):
            def _f(*a, **k):
                calls[name] += 1
                raise AssertionError(f"{name} loader called")
            return _f
        with tempfile.TemporaryDirectory() as td:
            bad = Path(td) / "bad.json"; bad.write_text("{bad", encoding="utf-8")
            with patch.object(rfa, "load_kline_panel", boom("k")), \
                 patch.object(rfa, "load_funding_panel", boom("f")), \
                 patch.object(rfa, "run_multisplit", boom("m")):
                rc = rfa.main(["--check-admissibility-package", str(bad), str(CA), str(TE), str(PR), "--expect-go"])
        self.assertEqual(rc, 2)
        self.assertEqual(calls, {"k": 0, "f": 0, "m": 0})


class TestCandidateAndArgEdgeCases(unittest.TestCase):
    def test_promotion_dryrun_missing_candidate_refuses_stably(self):
        p = subprocess.run([sys.executable, str(REPO / "scripts/fclr016_v5_promotion_dryrun.py"),
                            str(PM), str(CA), str(TE), str(PR),
                            "--candidate-terms-evidence", "/nonexistent/cand.json"],
                           capture_output=True, text=True)
        self.assertEqual(p.returncode, 2)
        j = _parse_json_stdout(p.stdout)
        _assert_refusal_contract(self, j)
        self.assertIn("candidate", (j.get("error") or "").lower())

    def test_promotion_dryrun_candidate_directory_refuses_stably(self):
        with tempfile.TemporaryDirectory() as td:
            d = Path(td) / "cand"; d.mkdir()
            p = subprocess.run([sys.executable, str(REPO / "scripts/fclr016_v5_promotion_dryrun.py"),
                                str(PM), str(CA), str(TE), str(PR), "--candidate-prereg", str(d)],
                               capture_output=True, text=True)
            self.assertEqual(p.returncode, 2)
            j = _parse_json_stdout(p.stdout)
            _assert_refusal_contract(self, j)
            self.assertIn("candidate", (j.get("error") or "").lower())

    def test_missing_required_args_return_nonzero(self):
        for name, cmd in CLIS:
            p = subprocess.run(cmd, capture_output=True, text=True)
            self.assertNotEqual(p.returncode, 0, name)


class TestConfirmatoryDataPathSeamNoLoad(unittest.TestCase):
    def _synthetic_go_pkg(self, td: Path):
        te = _write_json(td, "te.json", _resolved_terms())
        pm = _write_json(td, "pm.json", _go_manifest())
        ca = _write_json(td, "ca.json", _go_completeness())
        pr = _write_json(td, "pr.json", _go_prereg(pm, ca, te))
        return pm, ca, te, pr

    def test_synthetic_go_confirmatory_empty_data_dirs_refuses_no_loader(self):
        calls = {"k": 0, "f": 0, "m": 0}
        def boom(name):
            def _f(*a, **k):
                calls[name] += 1
                raise AssertionError(f"{name} loader/outcome called")
            return _f
        with tempfile.TemporaryDirectory() as td:
            td = Path(td)
            pm, ca, te, pr = self._synthetic_go_pkg(td)
            empty = td / "empty"; empty.mkdir()
            import io, contextlib
            buf = io.StringIO()
            with patch.object(rfa, "load_kline_panel", boom("k")), \
                 patch.object(rfa, "load_funding_panel", boom("f")), \
                 patch.object(rfa, "run_multisplit", boom("m")), \
                 patch.object(rfa, "RAW", empty), patch.object(rfa, "CACHE", empty), \
                 contextlib.redirect_stderr(buf):
                rc = rfa.main(["--confirmatory", "--experiment-id", "G4V5_SYNTH_EMPTY_DATA",
                               "--start", "2025-08-01", "--end", "2025-10-31",
                               "--pre-registration", str(pr), "--provenance-manifest", str(pm),
                               "--terms-evidence", str(te), "--out-suffix", "_synth132", "--include-cache"])
        self.assertEqual(rc, 2)
        self.assertEqual(calls, {"k": 0, "f": 0, "m": 0})
        j = json.loads(buf.getvalue())
        self.assertEqual(j["status"], "REFUSED")
        self.assertEqual(j["guard"], "confirmatory_data_path_seam")
        self.assertFalse(j["confirmatory_outcomes_permitted"])
        self.assertTrue(j["no_data_loaded"])
        self.assertTrue(j["no_outcomes_computed"])
        self.assertIsInstance(j["reason_codes"], list)
        self.assertTrue(j["reason_codes"])

    def test_synthetic_go_confirmatory_nonexistent_data_dirs_refuses_no_loader(self):
        calls = {"k": 0, "f": 0, "m": 0}
        def boom(name):
            def _f(*a, **k):
                calls[name] += 1
                raise AssertionError(f"{name} loader/outcome called")
            return _f
        with tempfile.TemporaryDirectory() as td:
            td = Path(td)
            pm, ca, te, pr = self._synthetic_go_pkg(td)
            missing = td / "does_not_exist"
            import io, contextlib
            buf = io.StringIO()
            with patch.object(rfa, "load_kline_panel", boom("k")), \
                 patch.object(rfa, "load_funding_panel", boom("f")), \
                 patch.object(rfa, "run_multisplit", boom("m")), \
                 patch.object(rfa, "RAW", missing), patch.object(rfa, "CACHE", missing), \
                 contextlib.redirect_stderr(buf):
                rc = rfa.main(["--confirmatory", "--experiment-id", "G4V5_SYNTH_NODATA",
                               "--start", "2025-08-01", "--end", "2025-10-31",
                               "--pre-registration", str(pr), "--provenance-manifest", str(pm),
                               "--terms-evidence", str(te), "--out-suffix", "_synth132"])
        self.assertEqual(rc, 2)
        self.assertEqual(calls, {"k": 0, "f": 0, "m": 0})
        j = json.loads(buf.getvalue())
        self.assertEqual(j["guard"], "confirmatory_data_path_seam")
        self.assertTrue(any("missing" in r or "data_root" in r for r in j["reason_codes"]))


class TestCrossCLIParity(unittest.TestCase):
    def _canon_hashes(self):
        return {p.name: hashlib.sha256(p.read_bytes()).hexdigest() for p in [PM, CA, TE, PR]}

    def test_real_blocked_package_consistent_across_clis_and_package_check(self):
        before = self._canon_hashes()
        pkg = rfa.check_admissibility_package(str(PM), str(CA), str(TE), str(PR), expect_go=True)
        self.assertTrue(pkg.get("ok"))
        self.assertFalse(pkg.get("all_go"))
        self.assertFalse(pkg.get("confirmatory_outcomes_permitted"))
        self.assertTrue(pkg.get("expect_go_refused"))

        pf = preflight.build_preflight_summary(PM, CA, TE, PR)
        self.assertTrue(pf.get("ok"))
        self.assertFalse(pf.get("all_go"))
        self.assertFalse(pf.get("confirmatory_outcomes_permitted"))
        self.assertTrue(pf.get("expect_go_refused"))

        ar = adm_report.build_report(PM, CA, TE, PR)
        self.assertTrue(ar.get("ok"))
        self.assertFalse(ar.get("all_go"))
        self.assertFalse(ar.get("confirmatory_outcomes_permitted"))

        dr = dryrun.run_dryrun(PM, CA, TE, PR)
        self.assertTrue(dr.get("ok"))
        self.assertFalse(dr.get("all_go"))
        self.assertFalse(dr.get("confirmatory_outcomes_permitted"))
        # all real/non-synthetic scenarios refuse (synthetic GO fixture is expected NOT refused)
        non_synth = [s for s in dr.get("scenarios", []) if not s.get("synthetic_test_fixture")]
        self.assertTrue(all(s.get("expected_refused") and s.get("actual_refused") and s.get("status", "").startswith("PASS")
                            for s in non_synth))

        # CLI subprocess parity (machine-readable blocked contracts)
        for name, cmd in CLIS:
            p = subprocess.run(cmd + [str(PM), str(CA), str(TE), str(PR)], capture_output=True, text=True)
            j = _parse_json_stdout(p.stdout)
            self.assertTrue(j.get("ok"), (name, j))
            self.assertFalse(j.get("all_go"), (name, j))
            self.assertFalse(j.get("confirmatory_outcomes_permitted"), (name, j))

        pkg_cli = subprocess.run([sys.executable, str(REPO / "scripts/run_funding_ablations.py"),
                                  "--check-admissibility-package", str(PM), str(CA), str(TE), str(PR), "--expect-go"],
                                 capture_output=True, text=True)
        j = json.loads(pkg_cli.stdout)
        self.assertEqual(pkg_cli.returncode, 2)
        self.assertFalse(j.get("all_go"))
        self.assertTrue(j.get("expect_go_refused"))

        self.assertEqual(before, self._canon_hashes(), "real canonical inputs mutated")

    def test_synthetic_tmp_go_fixture_consistent_and_canonicals_unchanged(self):
        before = self._canon_hashes()
        with tempfile.TemporaryDirectory() as td:
            td = Path(td)
            te = _write_json(td, "te.json", _resolved_terms())
            pm = _write_json(td, "pm.json", _go_manifest())
            ca = _write_json(td, "ca.json", _go_completeness())
            pr = _write_json(td, "pr.json", _go_prereg(pm, ca, te))

            # Full synthetic tmp GO package (labeled synthetic_test_fixture/no_real_terms_evidence in terms/license metadata)
            pkg = rfa.check_admissibility_package(str(pm), str(ca), str(te), str(pr), expect_go=True)
            self.assertTrue(pkg.get("ok"))
            self.assertTrue(pkg.get("all_go"), pkg)
            self.assertTrue(pkg.get("confirmatory_outcomes_permitted"), pkg)
            self.assertFalse(pkg.get("expect_go_refused"), pkg)

            pf = preflight.build_preflight_summary(pm, ca, te, pr)
            self.assertTrue(pf.get("all_go"))
            self.assertTrue(pf.get("confirmatory_outcomes_permitted"))
            self.assertFalse(pf.get("expect_go_refused"))

            ar = adm_report.build_report(pm, ca, te, pr)
            self.assertTrue(ar.get("all_go"))
            self.assertTrue(ar.get("confirmatory_outcomes_permitted"))

            # promotion dryrun takes real blocked package as required args; verifies its own
            # internal synthetic GO fixture scenario and never grants top-level real GO.
            dr = dryrun.run_dryrun(PM, CA, TE, PR)
            self.assertTrue(dr.get("ok"))
            self.assertFalse(dr.get("all_go"), "dryrun top-level real package must remain non-GO")
            synth = [x for x in dr["scenarios"] if x.get("synthetic_test_fixture")]
            self.assertTrue(synth)
            j = next(x for x in dr["scenarios"] if x.get("scenario_id") == "j_synthetic_go_fixture_only")
            self.assertTrue(j.get("status", "").startswith("PASS"), j)
            self.assertFalse(j.get("actual_refused"), j)  # synthetic fixture accepted by guard logic
            self.assertTrue(j.get("result_summary", {}).get("all_go"), j)  # synthetic fixture GO only

        self.assertEqual(before, self._canon_hashes(), "canonical real inputs mutated by synthetic fixture run")


class TestCanonicalTargetsUnchanged(unittest.TestCase):
    CANONICAL = [
        REPO / "research_state/experiment_frontier.json",
        REPO / "research_state/run_manifest.json",
        REPO / "research_state/evaluation_summary.md",
    ]

    def test_clis_and_package_check_do_not_mutate_canonicals(self):
        before = {str(p): (p.read_bytes() if p.exists() else None) for p in self.CANONICAL}
        subprocess.run([sys.executable, str(REPO / "scripts/fclr016_v5_preflight_summary.py"),
                        str(PM), str(CA), str(TE), str(PR)], capture_output=True)
        subprocess.run([sys.executable, str(REPO / "scripts/fclr016_v5_admissibility_report.py"),
                        str(PM), str(CA), str(TE), str(PR)], capture_output=True)
        subprocess.run([sys.executable, str(REPO / "scripts/fclr016_v5_promotion_dryrun.py"),
                        str(PM), str(CA), str(TE), str(PR)], capture_output=True)
        rfa.check_admissibility_package(str(PM), str(CA), str(TE), str(PR), expect_go=True)
        after = {str(p): (p.read_bytes() if p.exists() else None) for p in self.CANONICAL}
        self.assertEqual(before, after)


if __name__ == "__main__":
    unittest.main()
