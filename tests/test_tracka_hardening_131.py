"""FCLR-NEXT-131: harness seam/manifest-evaluator/prereg exception fail-closed
matrix (G1), operator/CLI JSON refusal parity on malformed admissible-manifest
contracts (G2), refusal_payload/guard snapshot field stability (G3).

Deterministic, tmp-isolated, dep-light, no network, no parquet/outcome reads,
no real research_state writes.
"""
from __future__ import annotations

import io
import json
import subprocess
import sys
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

REAL = Path(__file__).resolve().parent.parent
RS = REAL / "research_state"
FRONTIER = RS / "experiment_frontier.json"
RUN_MANIFEST = RS / "run_manifest.json"
EVAL_FCLR010 = RS / "evaluation_summary_FCLR010.md"
BLOCKED_RC = "PREREG_OR_MANIFEST_BLOCK_AFTER_DRIFT_PASS"
SAFE_FALSE = ("outcomes_inspected", "canonical_outputs_mutated", "network", "writes_real_research_state")
REQ_REFUSAL = {"status", "outcomes_inspected", "canonical_outputs_mutated", "network", "writes_real_research_state", "reason_code"}


def _snap(paths):
    return {str(p): (p.read_bytes() if p.exists() else None) for p in paths}


def _unchanged(paths, before):
    for s, b in before.items():
        p = Path(s)
        a = p.read_bytes() if p.exists() else None
        if b != a:
            raise AssertionError(f"canonical target mutated: {s}")


def _assert_blocked_no_io(p, allow_reason_codes=(BLOCKED_RC,)):
    assert p.get("status") == "BLOCKED", p
    if p.get("reason_code") is not None:
        assert p.get("reason_code") in allow_reason_codes or p.get("reason_code", "").startswith("ADMISSIBLE_SEAM_"), p
    for k in SAFE_FALSE:
        assert p.get(k) is False, (k, p.get(k), p)
    assert p.get("reads_parquet") in (False, None), p.get("reads_parquet")
    assert p.get("reads_outcomes") in (False, None), p.get("reads_outcomes")


class Test131G1HarnessExceptionMatrix(unittest.TestCase):
    """G1: harness seam/guard exception fail-closed with stable refusal fields."""

    def test_execute_ready_data_load_seam_check_raises_fail_closed(self):
        from scripts.fclr010_harness import FCLR010Harness
        h = FCLR010Harness()
        with tempfile.TemporaryDirectory() as td:
            td = Path(td)
            prereg = td / "p.json"; prereg.write_text(json.dumps({"frozen": True}))
            data = td / "d"; data.mkdir()
            with patch.object(h, "_evaluate_admissible_seam", side_effect=RuntimeError("boom")):
                r = h.execute_ready_data_load(data, prereg, admissible_manifest_path=str(td / "mf.json"))
        _assert_blocked_no_io(r, allow_reason_codes=(BLOCKED_RC, "ADMISSIBLE_SEAM_NOGO_BEFORE_OUTCOMES", "ADMISSIBLE_SEAM_EXCEPTION", "ADMISSIBLE_SEAM_NOGO_BEFORE_PREREG"))
        assert r.get("outcomes_loaded") in (None, False), r

    def test_execute_ready_data_load_seam_malformed_shape_fail_closed(self):
        from scripts.fclr010_harness import FCLR010Harness
        h = FCLR010Harness()
        with tempfile.TemporaryDirectory() as td:
            td = Path(td)
            prereg = td / "p.json"; prereg.write_text(json.dumps({"frozen": True}))
            data = td / "d"; data.mkdir()
            with patch.object(h, "_evaluate_admissible_seam", return_value={"pass": False}):  # malformed/minimal
                r = h.execute_ready_data_load(data, prereg, admissible_manifest_path=str(td / "mf.json"))
        _assert_blocked_no_io(r)
        assert "ADMISSIBLE_SEAM" in (r.get("reason_code") or ""), r

    def test_evaluate_forward_manifest_evaluator_raises_fail_closed(self):
        from scripts.fclr010_harness import FCLR010Harness
        h = FCLR010Harness()
        with tempfile.TemporaryDirectory() as td:
            td = Path(td)
            prereg = td / "p.json"; prereg.write_text(json.dumps({"frozen": True}))
            data = td / "d"; data.mkdir()
            with patch("scripts.tracka_rubric.assess_strict_manifest", side_effect=RuntimeError("boom")):
                r = h.evaluate_forward(data, td, pre_reg_path=prereg,
                                       source_manifest={"venue": "hyperliquid", "observed_liquidations": True, "claims_3x30d_blocks": True})
        _assert_blocked_no_io(r)
        mg = r.get("manifest_gate") or {}
        assert mg.get("status") in ("NO-GO", "BLOCKED"), mg
        assert mg.get("go") is False
        assert r.get("prereg_required") is False
        assert r.get("outcomes_inspected") is False

    def test_evaluate_forward_invalid_prereg_content_no_outcome_inspection(self):
        from scripts.fclr010_harness import FCLR010Harness
        h = FCLR010Harness()
        with tempfile.TemporaryDirectory() as td:
            td = Path(td)
            prereg = td / "p.json"; prereg.write_text("{broken")
            data = td / "d"; data.mkdir()
            loader = lambda *_a, **_k: (_ for _ in ()).throw(AssertionError("loader must not run"))
            r = h.evaluate_forward(data, td, pre_reg_path=prereg, outcome_loader=loader)
        # existing behavior: broken prereg file exists => harness may treat as present path and reach READY_FROZEN
        # without parsing content in evaluate_forward; fail-closed contract requires no outcome inspection
        # unless gates fully pass in a way that invokes explicit loader. We assert no implicit outcome reads
        # and stable flags.
        assert r.get("status") in ("READY_FROZEN", "BLOCKED"), r
        assert r.get("outcomes_inspected") is False
        if r.get("status") == "BLOCKED":
            _assert_blocked_no_io(r)

    def test_execute_ready_data_load_invalid_prereg_no_outcome_load(self):
        from scripts.fclr010_harness import FCLR010Harness
        h = FCLR010Harness()
        with tempfile.TemporaryDirectory() as td:
            td = Path(td)
            prereg = td / "p.json"; prereg.write_text("{broken")
            data = td / "d"; data.mkdir()
            loader = lambda *_a, **_k: (_ for _ in ()).throw(AssertionError("loader must not run"))
            r = h.execute_ready_data_load(data, prereg, outcome_loader=loader)
        assert r.get("status") in ("READY_FROZEN", "BLOCKED"), r
        assert r.get("outcomes_inspected") is False
        assert r.get("reads_parquet") in (False, None)
        assert r.get("reads_outcomes") in (False, None)
        if r.get("status") == "BLOCKED":
            _assert_blocked_no_io(r)

    def test_guarded_execute_manifest_evaluator_exception_fail_closed(self):
        from scripts import fclr010_guarded_entry as ge
        with tempfile.TemporaryDirectory() as td:
            td = Path(td)
            prereg = td / "p.json"; prereg.write_text(json.dumps({"frozen": True}))
            data = td / "d"; data.mkdir()
            loader = lambda *_a, **_k: (_ for _ in ()).throw(AssertionError("loader must not run"))
            with patch("scripts.tracka_rubric.assess_strict_manifest", side_effect=RuntimeError("boom")):
                r = ge.guarded_execute(data_path=data, pre_reg_path=prereg,
                                       source_manifest={"venue": "hyperliquid", "observed_liquidations": True},
                                       outcome_loader=loader, allow_default_loader=False)
        _assert_blocked_no_io(r)
        assert r.get("canonical_outputs_mutated") is False
        assert r.get("network") is False
        assert r.get("writes_real_research_state") is False


class Test131G2CLIJSONParity(unittest.TestCase):
    """G2: operator/gate/check JSON refusal parity on malformed admissible-manifest contracts."""

    def _run(self, cmd):
        return subprocess.run(cmd, capture_output=True, text=True, cwd=str(REAL))

    def _assert_json_refusal(self, stdout, expect_status_blocked=True):
        data = json.loads(stdout)
        if expect_status_blocked:
            # gate/operator return top-level BLOCKED or pass+blocked gate; check --admissible-manifest returns admissible_seam block.
            seam = data.get("admissible_seam") or data.get("admissible_seam_state") or {}
            gate = data.get("gate_decision") or {}
            blocked = data.get("status") == "BLOCKED" or gate.get("status") == "BLOCKED" or seam.get("status") == "NO-GO" or data.get("pass") is False
            assert blocked, data
        return data

    def test_tracka_resume_gate_malformed_admissible_manifest_json_refusal(self):
        with tempfile.NamedTemporaryFile(suffix=".json", delete=False, mode="w") as f:
            f.write("{broken"); p = f.name
        r = self._run([sys.executable, "scripts/tracka_resume_gate.py", "--admissible-manifest", p, "--json"])
        self.assertNotEqual(r.returncode, 0)
        d = self._assert_json_refusal(r.stdout)
        seam = d.get("admissible_seam_wired") or {}
        self.assertFalse(seam.get("pass", True))
        self.assertTrue(seam.get("fail_closed", False) is True or d.get("status") == "BLOCKED")
        self.assertFalse(d.get("outcomes_inspected", False))
        self.assertFalse(d.get("network", False))
        self.assertFalse(d.get("writes_real_research_state", False))

    def test_tracka_operator_report_malformed_admissible_manifest_json_refusal(self):
        with tempfile.NamedTemporaryFile(suffix=".json", delete=False, mode="w") as f:
            f.write("{broken"); p = f.name
        r = self._run([sys.executable, "scripts/tracka_operator_report.py", "--json", "--admissible-manifest", p])
        self.assertNotEqual(r.returncode, 0)
        d = json.loads(r.stdout)
        seam = d.get("admissible_seam_wired") or d.get("admissible_seam_state") or {}
        self.assertFalse(seam.get("pass", True))
        self.assertFalse(d.get("network", False))
        self.assertFalse(d.get("writes_real_research_state", False))
        self.assertIn("failures", seam)
        self.assertIsInstance(seam.get("failures"), list)

    def test_tracka_resume_check_malformed_admissible_manifest_json_refusal(self):
        with tempfile.NamedTemporaryFile(suffix=".json", delete=False, mode="w") as f:
            f.write("{broken"); p = f.name
        r = self._run([sys.executable, "scripts/tracka_resume_check.py", "--admissible-manifest", p])
        self.assertNotEqual(r.returncode, 0)
        d = json.loads(r.stdout)
        seam = d.get("admissible_seam") or {}
        self.assertFalse(seam.get("pass", True))
        self.assertTrue(seam.get("fail_closed", False))
        self.assertFalse(seam.get("reads_outcomes", True))
        self.assertFalse(seam.get("reads_parquet", True))
        self.assertFalse(seam.get("network", True))
        self.assertEqual(d.get("pass"), False)

    def test_tracka_resume_check_missing_admissible_manifest_json_refusal(self):
        r = self._run([sys.executable, "scripts/tracka_resume_check.py", "--admissible-manifest", "/nonexistent_131.json"])
        self.assertNotEqual(r.returncode, 0)
        d = json.loads(r.stdout)
        seam = d.get("admissible_seam") or {}
        self.assertEqual(seam.get("reason_code"), "ADMISSIBLE_CANDIDATE_PATH_MISSING")
        self.assertFalse(d.get("outcomes_inspected", False) is True)


class Test131G3RefusalPayloadStability(unittest.TestCase):
    """G3: refusal_payload/guard snapshot field stability + safe boolean normalization."""

    REQ_BOOL = ("outcomes_inspected", "canonical_outputs_mutated", "network", "writes_real_research_state")
    REQ = ("status", "reason_code") + REQ_BOOL

    def test_refusal_payload_always_includes_required_fields(self):
        from scripts.fclr010_guarded_entry import refusal_payload
        p = refusal_payload(script="x")
        for k in self.REQ:
            self.assertIn(k, p, k)
        self.assertEqual(p["status"], "BLOCKED")
        for k in self.REQ_BOOL:
            self.assertIs(p[k], False, (k, p[k]))

    def test_refusal_payload_tolerates_missing_extra_guard_keys(self):
        from scripts.fclr010_guarded_entry import refusal_payload
        p = refusal_payload(script="x", guard={"status": "BLOCKED"})  # minimal/missing keys
        for k in self.REQ:
            self.assertIn(k, p)
        self.assertIs(p["outcomes_inspected"], False)
        self.assertIsInstance(p.get("guard"), dict)

    def test_refusal_payload_tolerates_extra_guard_keys_without_raising(self):
        from scripts.fclr010_guarded_entry import refusal_payload
        p = refusal_payload(script="x", guard={"status": "BLOCKED", "unexpected": {"nested": 1}, "reads_parquet": None})
        for k in self.REQ:
            self.assertIn(k, p)
        self.assertIs(p["canonical_outputs_mutated"], False)

    def test_guarded_execute_blocked_normalizes_absent_booleans(self):
        from scripts import fclr010_guarded_entry as ge
        before = _snap([FRONTIER, RUN_MANIFEST, EVAL_FCLR010])
        sparse = {"status": "BLOCKED", "reason_code": BLOCKED_RC}  # missing safety booleans
        with patch.object(ge, "FCLR010Harness") as H:
            H.return_value.execute_ready_data_load.return_value = sparse
            r = ge.guarded_execute(data_path=Path("/tmp/d"), pre_reg_path=Path("/tmp/p"), allow_default_loader=False)
        self.assertEqual(r["status"], "BLOCKED")
        for k in self.REQ_BOOL:
            self.assertIs(r[k], False, (k, r.get(k)))
        self.assertIs(r.get("reads_parquet"), False)
        self.assertIs(r.get("reads_outcomes"), False)
        self.assertIsNone(r.get("outcomes_loaded"))
        _unchanged([FRONTIER, RUN_MANIFEST, EVAL_FCLR010], before)

    def test_guarded_execute_blocked_normalizes_truthy_safety_fields_to_false(self):
        from scripts import fclr010_guarded_entry as ge
        bad = {"status": "BLOCKED", "reason_code": BLOCKED_RC,
               "outcomes_inspected": True, "canonical_outputs_mutated": True, "network": True,
               "writes_real_research_state": True, "reads_parquet": True, "reads_outcomes": True}
        with patch.object(ge, "FCLR010Harness") as H:
            H.return_value.execute_ready_data_load.return_value = bad
            r = ge.guarded_execute(data_path=Path("/tmp/d"), pre_reg_path=Path("/tmp/p"), allow_default_loader=False)
        for k in ("outcomes_inspected", "canonical_outputs_mutated", "network", "writes_real_research_state", "reads_parquet", "reads_outcomes"):
            self.assertIs(r[k], False, (k, r[k]))


if __name__ == "__main__":
    unittest.main()
