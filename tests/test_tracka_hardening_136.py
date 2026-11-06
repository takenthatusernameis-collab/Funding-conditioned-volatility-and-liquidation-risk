"""FCLR-NEXT-136: synthetic admissible trigger-readiness + contract-integrity hardening.

Deterministic, tmp-isolated, dep-light, no network, no parquet/outcome reads,
no real research_state writes. Exercises the admissible-trigger -> prereg ->
outcome-inspection seam with a synthetic admissible tmp manifest and proves
GO-seam + missing/invalid prereg => BLOCKED with stable machine fields across
gate/check/operator/harness paths. Verifies canonical outputs byte-identical.
"""
from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

REAL = Path(__file__).resolve().parent.parent
RS = REAL / "research_state"
RUN_MANIFEST = RS / "run_manifest.json"
FRONTIER = RS / "experiment_frontier.json"
EVAL_FCLR010 = RS / "evaluation_summary_FCLR010.md"
CANON = [FRONTIER, RUN_MANIFEST, EVAL_FCLR010]
BLOCKED_RC = "PREREG_OR_MANIFEST_BLOCK_AFTER_DRIFT_PASS"
SAFE_FALSE = ("outcomes_inspected", "canonical_outputs_mutated", "network", "writes_real_research_state")
READ_FALSE = ("reads_parquet", "reads_outcomes")


def _snap(paths):
    return {str(p): (p.read_bytes() if p.exists() else None) for p in paths}


def _unchanged(paths, before):
    for s, b in before.items():
        p = Path(s)
        a = p.read_bytes() if p.exists() else None
        if b != a:
            raise AssertionError(f"canonical target mutated: {s}")


def _assert_blocked_no_io(p, *, allow_reason_codes=(BLOCKED_RC,)):
    assert p.get("status") == "BLOCKED", p
    if p.get("reason_code") is not None:
        assert p.get("reason_code") in allow_reason_codes or str(p.get("reason_code", "")).startswith("ADMISSIBLE_SEAM_"), p
    for k in SAFE_FALSE:
        assert p.get(k) is False, (k, p.get(k), p)
    for k in READ_FALSE:
        assert p.get(k) in (False, None), (k, p.get(k), p)


def _valid_admissible_manifest(month="2026-11"):
    return {
        "track": "A",
        "source_family": "ironflow_hyperliquid_liquidations",
        "venue": "hyperliquid",
        "source": "ironflow/hyperliquid-liquidations",
        "month": month,
        "unauthenticated": True,
        "requires_api_key": False,
        "requires_signature": False,
        "observed_liquidations": True,
        "modeled_or_proxy": False,
        "merges_non_hyperliquid": False,
        "label_definition": "observed_hyperliquid_liquidation_event_rows_from_ironflow",
        "timestamp_normalized_utc": True,
        "artifacts": {
            "events": {
                "path": f"research_state/data_cache/ironflow_events/events/{month}.parquet",
                "url": f"https://huggingface.co/datasets/ironflow/hyperliquid-liquidations/resolve/main/data/events/{month}.parquet",
                "schema_fields": ["timestamp", "symbol", "liquidation_notional", "side"],
            },
            "fills": {
                "path": f"research_state/data_cache/ironflow_events/fills/{month}.parquet",
                "url": f"https://huggingface.co/datasets/ironflow/hyperliquid-liquidations/resolve/main/data/fills/{month}.parquet",
                "schema_fields": ["timestamp", "symbol", "size", "price"],
            },
        },
    }


def _write_json(path, obj):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj), encoding="utf-8")
    return str(path)


def _run(cmd):
    return subprocess.run(cmd, capture_output=True, text=True, cwd=str(REAL))


class Test136SyntheticAdmissibleGoMissingInvalidPrereg(unittest.TestCase):
    """Synthetic admissible tmp manifest (no network, no real research_state writes):
    GO-seam + missing/invalid prereg => BLOCKED with stable fields across paths."""

    def test_harness_go_seam_missing_prereg_blocked_stable(self):
        from scripts.fclr010_harness import FCLR010Harness
        h = FCLR010Harness(repo_root=REAL)
        before = _snap(CANON)
        m = _valid_admissible_manifest()
        with tempfile.TemporaryDirectory() as td:
            td = Path(td)
            missing = td / "no_prereg.json"
            loader = lambda *_a, **_k: (_ for _ in ()).throw(AssertionError("outcome loader must not run"))
            r = h.evaluate_forward(td / "nodata", td, pre_reg_path=missing, admissible_manifest=m, outcome_loader=loader)
        _assert_blocked_no_io(r)
        self.assertEqual(r.get("reason_code"), BLOCKED_RC, r)
        self.assertEqual(r.get("reason_code_detail"), "ADMISSIBLE_SEAM_GO_PREREG_REQUIRED", r)
        self.assertTrue(r.get("seam_go_prereg_required"), r)
        self.assertFalse(r.get("outcomes_inspected"), r)
        self.assertFalse(r.get("reads_outcomes"), r)
        self.assertFalse(r.get("reads_parquet"), r)
        self.assertTrue((r.get("admissible_seam_wired") or {}).get("pass"), r)
        _unchanged(CANON, before)

    def test_harness_go_seam_invalid_prereg_blocked_stable(self):
        from scripts.fclr010_harness import FCLR010Harness
        h = FCLR010Harness(repo_root=REAL)
        before = _snap(CANON)
        m = _valid_admissible_manifest()
        with tempfile.TemporaryDirectory() as td:
            td = Path(td)
            bad = td / "bad_prereg.json"
            bad.write_text("{broken json!!!")
            loader = lambda *_a, **_k: (_ for _ in ()).throw(AssertionError("outcome loader must not run"))
            r = h.evaluate_forward(td / "nodata", td, pre_reg_path=bad, admissible_manifest=m, outcome_loader=loader)
        _assert_blocked_no_io(r)
        self.assertEqual(r.get("reason_code"), BLOCKED_RC, r)
        self.assertEqual(r.get("reason_code_detail"), "PREREG_CONTENT_INVALID_FAIL_CLOSED", r)
        self.assertFalse(r.get("outcomes_inspected"), r)
        self.assertFalse(r.get("reads_outcomes"), r)
        self.assertFalse(r.get("reads_parquet"), r)
        self.assertTrue((r.get("admissible_seam_wired") or {}).get("pass"), r)
        _unchanged(CANON, before)

    def test_gate_go_seam_missing_prereg_blocked_stable(self):
        from scripts import tracka_resume_gate as gate
        before = _snap(CANON)
        m = _valid_admissible_manifest()
        with tempfile.TemporaryDirectory() as td:
            ap = _write_json(Path(td) / "adm.json", m)
            r = gate.decide("/nonexistent", td, pre_reg_path=None, admissible_manifest_path=ap, harness_repo_root=REAL)
        _assert_blocked_no_io(r)
        self.assertEqual(r.get("reason_code"), BLOCKED_RC, r)
        self.assertEqual(r.get("reason_code_detail"), "ADMISSIBLE_SEAM_GO_PREREG_REQUIRED", r)
        self.assertTrue(r.get("seam_go_prereg_required"), r)
        self.assertEqual(r.get("fail_closed_order"), "drift_preflight->admissible_seam->manifest_prereg", r)
        self.assertFalse(r.get("outcomes_inspected"), r)
        self.assertFalse(r.get("reads_outcomes"), r)
        self.assertFalse(r.get("reads_parquet"), r)
        self.assertTrue((r.get("admissible_seam_wired") or {}).get("pass"), r)
        _unchanged(CANON, before)

    def test_gate_go_seam_invalid_prereg_blocked_stable(self):
        from scripts import tracka_resume_gate as gate
        before = _snap(CANON)
        m = _valid_admissible_manifest()
        with tempfile.TemporaryDirectory() as td:
            ap = _write_json(Path(td) / "adm.json", m)
            bad = Path(td) / "bad_prereg.json"; bad.write_text("{broken")
            r = gate.decide("/nonexistent", td, pre_reg_path=str(bad), admissible_manifest_path=ap, harness_repo_root=REAL)
        _assert_blocked_no_io(r)
        self.assertEqual(r.get("reason_code"), BLOCKED_RC, r)
        self.assertEqual(r.get("reason_code_detail"), "PREREG_CONTENT_INVALID_FAIL_CLOSED", r)
        self.assertEqual(r.get("fail_closed_order"), "drift_preflight->admissible_seam->manifest_prereg", r)
        self.assertFalse(r.get("outcomes_inspected"), r)
        self.assertFalse(r.get("reads_outcomes"), r)
        self.assertFalse(r.get("reads_parquet"), r)
        self.assertTrue((r.get("admissible_seam_wired") or {}).get("pass"), r)
        _unchanged(CANON, before)

    def test_operator_go_seam_missing_prereg_blocked_stable(self):
        from scripts import tracka_resume_check as rc
        before = _snap(CANON)
        m = _valid_admissible_manifest()
        with tempfile.TemporaryDirectory() as td:
            ap = _write_json(Path(td) / "adm.json", m)
            r = rc.compose_operator_report(repo_root=REAL, research_state_dir=RS, harness_repo_root=REAL, admissible_candidate_path=ap)
        self.assertFalse(r.get("network"), r)
        self.assertFalse(r.get("writes_real_research_state"), r)
        self.assertTrue((r.get("admissible_seam_wired") or {}).get("pass"), r)
        gd = r.get("gate_decision") or {}
        _assert_blocked_no_io(gd)
        self.assertEqual(gd.get("reason_code"), BLOCKED_RC, gd)
        self.assertEqual(gd.get("reason_code_detail"), "ADMISSIBLE_SEAM_GO_PREREG_REQUIRED", gd)
        self.assertTrue(gd.get("seam_go_prereg_required"), gd)
        self.assertEqual(gd.get("fail_closed_order"), "drift_preflight->admissible_seam->manifest_prereg", gd)
        self.assertFalse(gd.get("outcomes_inspected"), gd)
        self.assertFalse(gd.get("reads_outcomes"), gd)
        self.assertFalse(gd.get("reads_parquet"), gd)
        _unchanged(CANON, before)

    def test_check_cli_go_seam_candidate_stable_fields(self):
        """Focused seam check (127 G1): GO candidate => stable GO/pass fields; no reads."""
        m = _valid_admissible_manifest()
        before = _snap(CANON)
        with tempfile.TemporaryDirectory() as td:
            ap = _write_json(Path(td) / "adm.json", m)
            r = _run([sys.executable, "scripts/tracka_resume_check.py", "--admissible-manifest", ap])
        self.assertEqual(r.returncode, 0, (r.returncode, r.stdout, r.stderr))
        d = json.loads(r.stdout)
        self.assertTrue(d.get("pass"), d)
        self.assertEqual(d.get("status"), "GO", d)
        self.assertEqual(d.get("reason_code"), "ADMISSIBLE_SEAM_GO", d)
        self.assertEqual(d.get("fail_closed_order"), "drift_preflight->admissible_seam", d)
        self.assertFalse(d.get("network"), d)
        self.assertFalse(d.get("writes_real_research_state"), d)
        self.assertFalse(d.get("reads_outcomes"), d)
        self.assertFalse(d.get("reads_parquet"), d)
        seam = d.get("admissible_seam") or {}
        self.assertTrue(seam.get("pass"), seam)
        self.assertEqual(seam.get("status"), "GO", seam)
        self.assertEqual(seam.get("reason_code"), "ADMISSIBLE_SEAM_GO", seam)
        self.assertEqual(seam.get("month"), "2026-11", seam)
        self.assertTrue(seam.get("fail_closed"), seam)
        self.assertFalse(seam.get("network"), seam)
        self.assertFalse(seam.get("reads_outcomes"), seam)
        self.assertFalse(seam.get("reads_parquet"), seam)
        _unchanged(CANON, before)

    def test_check_cli_invalid_missing_candidate_fail_closed_stable(self):
        before = _snap(CANON)
        with tempfile.TemporaryDirectory() as td:
            bad = Path(td) / "bad.json"; bad.write_text("{broken")
            r = _run([sys.executable, "scripts/tracka_resume_check.py", "--admissible-manifest", str(bad)])
            self.assertNotEqual(r.returncode, 0)
            d = json.loads(r.stdout)
            self.assertFalse(d.get("pass"), d)
            self.assertEqual(d.get("status"), "NO-GO", d)
            self.assertEqual(d.get("reason_code"), "ADMISSIBLE_CANDIDATE_LOAD_ERROR", d)
            seam = d.get("admissible_seam") or {}
            self.assertFalse(seam.get("pass"), seam)
            self.assertTrue(seam.get("fail_closed"), seam)
            self.assertFalse(seam.get("reads_outcomes"), seam)
            self.assertFalse(seam.get("reads_parquet"), seam)
            self.assertFalse(d.get("network"), d)
            r2 = _run([sys.executable, "scripts/tracka_resume_check.py", "--admissible-manifest", str(Path(td)/"missing.json")])
            self.assertNotEqual(r2.returncode, 0)
            d2 = json.loads(r2.stdout)
            self.assertEqual(d2.get("reason_code"), "ADMISSIBLE_CANDIDATE_PATH_MISSING", d2)
            self.assertTrue((d2.get("admissible_seam") or {}).get("fail_closed"), d2)
        _unchanged(CANON, before)

    def test_gate_cli_go_seam_missing_prereg_stable_json(self):
        m = _valid_admissible_manifest()
        before = _snap(CANON)
        with tempfile.TemporaryDirectory() as td:
            ap = _write_json(Path(td) / "adm.json", m)
            r = _run([sys.executable, "scripts/tracka_resume_gate.py", "--admissible-manifest", ap, "--json"])
        self.assertNotEqual(r.returncode, 0, r.stdout)
        d = json.loads(r.stdout)
        self.assertEqual(d.get("status"), "BLOCKED", d)
        self.assertEqual(d.get("reason_code"), BLOCKED_RC, d)
        self.assertEqual(d.get("reason_code_detail"), "ADMISSIBLE_SEAM_GO_PREREG_REQUIRED", d)
        self.assertTrue(d.get("seam_go_prereg_required"), d)
        self.assertEqual(d.get("fail_closed_order"), "drift_preflight->admissible_seam->manifest_prereg", d)
        self.assertFalse(d.get("outcomes_inspected"), d)
        self.assertFalse(d.get("reads_outcomes"), d)
        self.assertFalse(d.get("reads_parquet"), d)
        self.assertFalse(d.get("canonical_outputs_mutated"), d)
        self.assertFalse(d.get("network"), d)
        self.assertFalse(d.get("writes_real_research_state"), d)
        self.assertTrue((d.get("admissible_seam_wired") or {}).get("pass"), d)
        _unchanged(CANON, before)

    def test_operator_cli_go_seam_missing_prereg_stable_json(self):
        m = _valid_admissible_manifest()
        before = _snap(CANON)
        with tempfile.TemporaryDirectory() as td:
            ap = _write_json(Path(td) / "adm.json", m)
            r = _run([sys.executable, "scripts/tracka_operator_report.py", "--json", "--admissible-manifest", ap])
        self.assertNotEqual(r.returncode, 0, r.stdout)
        d = json.loads(r.stdout)
        self.assertFalse(d.get("network"), d)
        self.assertFalse(d.get("writes_real_research_state"), d)
        self.assertTrue((d.get("admissible_seam_wired") or {}).get("pass"), d)
        gd = d.get("gate_decision") or {}
        self.assertEqual(gd.get("status"), "BLOCKED", gd)
        self.assertEqual(gd.get("reason_code"), BLOCKED_RC, gd)
        self.assertEqual(gd.get("reason_code_detail"), "ADMISSIBLE_SEAM_GO_PREREG_REQUIRED", gd)
        self.assertTrue(gd.get("seam_go_prereg_required"), gd)
        self.assertFalse(gd.get("outcomes_inspected"), gd)
        self.assertFalse(gd.get("reads_outcomes"), gd)
        self.assertFalse(gd.get("reads_parquet"), gd)
        _unchanged(CANON, before)

    def test_canonical_outputs_identical_after_synthetic_exercises(self):
        before = _snap(CANON)
        m = _valid_admissible_manifest()
        with tempfile.TemporaryDirectory() as td:
            ap = _write_json(Path(td) / "adm.json", m)
            bad = Path(td) / "bad.json"; bad.write_text("{broken")
            _run([sys.executable, "scripts/tracka_resume_gate.py", "--admissible-manifest", ap, "--json"])
            _run([sys.executable, "scripts/tracka_operator_report.py", "--json", "--admissible-manifest", ap])
            _run([sys.executable, "scripts/tracka_resume_check.py", "--admissible-manifest", ap])
            _run([sys.executable, "scripts/tracka_resume_check.py", "--admissible-manifest", str(bad)])
            _run([sys.executable, "scripts/tracka_resume_gate.py", "--bogus", "--json"])
            _run([sys.executable, "scripts/tracka_resume_check.py", "--bogus"])
            _run([sys.executable, "scripts/tracka_operator_report.py", "--bogus", "--json"])
        _unchanged(CANON, before)


class Test136NoParquetOutcomeReadsOnRefusal(unittest.TestCase):
    def test_harness_explicit_loader_never_called_on_go_seam_block(self):
        from scripts.fclr010_harness import FCLR010Harness
        h = FCLR010Harness(repo_root=REAL)
        m = _valid_admissible_manifest()
        loader = lambda *_a, **_k: (_ for _ in ()).throw(AssertionError("outcome loader must not run"))
        with tempfile.TemporaryDirectory() as td:
            td = Path(td)
            # missing prereg
            r = h.evaluate_forward(td / "d", td, pre_reg_path=td / "missing.json", admissible_manifest=m, outcome_loader=loader)
            self.assertEqual(r.get("status"), "BLOCKED")
            self.assertFalse(r.get("reads_outcomes"))
            self.assertFalse(r.get("reads_parquet"))
            # invalid prereg
            bad = td / "bad.json"; bad.write_text("{x")
            r2 = h.evaluate_forward(td / "d", td, pre_reg_path=bad, admissible_manifest=m, outcome_loader=loader)
            self.assertEqual(r2.get("status"), "BLOCKED")
            self.assertFalse(r2.get("reads_outcomes"))
            self.assertFalse(r2.get("reads_parquet"))
            # execute_ready_data_load also guarded
            r3 = h.execute_ready_data_load(td / "d", bad, admissible_manifest=m, outcome_loader=loader)
            self.assertEqual(r3.get("status"), "BLOCKED")
            self.assertFalse(r3.get("outcomes_inspected"))


if __name__ == "__main__":
    unittest.main()
