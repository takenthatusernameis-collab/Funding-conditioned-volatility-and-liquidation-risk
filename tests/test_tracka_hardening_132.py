"""FCLR-NEXT-132: Track A evaluate_forward prereg-content fail-closed (G1),
admissible-seam exception reason-code parity across harness/check/gate/operator
(G2), CLI malformed-manifest refusal schema stability matrix (G3).

Deterministic, tmp-isolated, dep-light, no network, no parquet/outcome reads,
no real research_state writes.
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


class Test132G1PreregContentFailClosed(unittest.TestCase):
    """G1: evaluate_forward prereg-content fail-closed when prereg exists but
    content is malformed/unreadable. No outcome inspection, no parquet read."""

    def test_evaluate_forward_malformed_prereg_fail_closed_no_outcomes(self):
        from scripts.fclr010_harness import FCLR010Harness
        h = FCLR010Harness()
        with tempfile.TemporaryDirectory() as td:
            td = Path(td)
            prereg = td / "p.json"
            prereg.write_text("{broken json!!!")
            data = td / "d"
            data.mkdir()
            loader = lambda *_a, **_k: (_ for _ in ()).throw(AssertionError("loader must not run"))
            r = h.evaluate_forward(data, td, pre_reg_path=prereg, outcome_loader=loader)
        self.assertEqual(r.get("status"), "BLOCKED", r)
        self.assertEqual(r.get("reason_code_detail"), "PREREG_CONTENT_INVALID_FAIL_CLOSED", r)
        self.assertEqual(r.get("reason_code"), BLOCKED_RC, r)
        self.assertFalse(r.get("outcomes_inspected"), r)
        self.assertFalse(r.get("reads_parquet"), r)
        self.assertFalse(r.get("reads_outcomes"), r)
        self.assertFalse(r.get("network"), r)
        self.assertFalse(r.get("writes_real_research_state"), r)
        self.assertFalse(r.get("canonical_outputs_mutated"), r)
        self.assertIsNone(r.get("outcomes_loaded"), r)

    def test_evaluate_forward_unreadable_prereg_fail_closed(self):
        from scripts.fclr010_harness import FCLR010Harness
        h = FCLR010Harness()
        with tempfile.TemporaryDirectory() as td:
            td = Path(td)
            prereg = td / "p.json"
            prereg.write_text("not json at all")
            data = td / "d"
            data.mkdir()
            loader = lambda *_a, **_k: (_ for _ in ()).throw(AssertionError("loader must not run"))
            r = h.evaluate_forward(data, td, pre_reg_path=prereg, outcome_loader=loader)
        _assert_blocked_no_io(r)
        self.assertEqual(r.get("reason_code_detail"), "PREREG_CONTENT_INVALID_FAIL_CLOSED", r)

    def test_evaluate_forward_valid_prereg_still_ready(self):
        from scripts.fclr010_harness import FCLR010Harness
        h = FCLR010Harness()
        with tempfile.TemporaryDirectory() as td:
            td = Path(td)
            prereg = td / "p.json"
            prereg.write_text(json.dumps({"frozen": True, "status": "PREREGISTERED_OUTCOMES_NOT_INSPECTED"}))
            data = td / "d"
            data.mkdir()
            r = h.evaluate_forward(data, td, pre_reg_path=prereg, outcome_loader=None)
        self.assertEqual(r.get("status"), "READY_FROZEN", r)
        self.assertFalse(r.get("outcomes_inspected"), r)

    def test_execute_ready_data_load_malformed_prereg_fail_closed(self):
        from scripts.fclr010_harness import FCLR010Harness
        h = FCLR010Harness()
        with tempfile.TemporaryDirectory() as td:
            td = Path(td)
            prereg = td / "p.json"
            prereg.write_text("{broken")
            data = td / "d"
            data.mkdir()
            loader = lambda *_a, **_k: (_ for _ in ()).throw(AssertionError("loader must not run"))
            r = h.execute_ready_data_load(data, prereg, outcome_loader=loader)
        self.assertEqual(r.get("status"), "BLOCKED", r)
        self.assertFalse(r.get("outcomes_inspected"), r)
        self.assertFalse(r.get("reads_parquet"), r)
        self.assertFalse(r.get("reads_outcomes"), r)


class Test132G2AdmissibleSeamParity(unittest.TestCase):
    """G2: admissible-seam exception/malformed-shape reason-code parity across
    harness/check/gate/operator."""

    def test_harness_seam_exception_fail_closed_stable_fields(self):
        from scripts.fclr010_harness import FCLR010Harness
        h = FCLR010Harness()
        with tempfile.TemporaryDirectory() as td:
            td = Path(td)
            prereg = td / "p.json"
            prereg.write_text(json.dumps({"frozen": True}))
            data = td / "d"
            data.mkdir()
            with patch.object(h, "_evaluate_admissible_seam", side_effect=RuntimeError("seam boom")):
                r = h.execute_ready_data_load(data, prereg, admissible_manifest_path=str(td / "mf.json"))
        _assert_blocked_no_io(r, allow_reason_codes=(BLOCKED_RC, "ADMISSIBLE_SEAM_EXCEPTION", "ADMISSIBLE_SEAM_NOGO_BEFORE_OUTCOMES"))
        self.assertFalse(r.get("outcomes_inspected"), r)

    def test_harness_seam_malformed_shape_fail_closed(self):
        from scripts.fclr010_harness import FCLR010Harness
        h = FCLR010Harness()
        with tempfile.TemporaryDirectory() as td:
            td = Path(td)
            prereg = td / "p.json"
            prereg.write_text(json.dumps({"frozen": True}))
            data = td / "d"
            data.mkdir()
            with patch.object(h, "_evaluate_admissible_seam", return_value={"pass": False, "status": "NO-GO"}):
                r = h.execute_ready_data_load(data, prereg, admissible_manifest_path=str(td / "mf.json"))
        _assert_blocked_no_io(r)
        self.assertIn("ADMISSIBLE_SEAM", r.get("reason_code", ""))

    def test_check_cli_malformed_admissible_manifest_json_refusal(self):
        with tempfile.NamedTemporaryFile(suffix=".json", delete=False, mode="w") as f:
            f.write("{broken"); p = f.name
        r = subprocess.run([sys.executable, "scripts/tracka_resume_check.py", "--admissible-manifest", p],
                           capture_output=True, text=True, cwd=str(REAL))
        self.assertNotEqual(r.returncode, 0)
        d = json.loads(r.stdout)
        seam = d.get("admissible_seam") or {}
        self.assertFalse(seam.get("pass", True))
        self.assertTrue(seam.get("fail_closed", False))
        self.assertFalse(seam.get("reads_outcomes", True))
        self.assertFalse(seam.get("reads_parquet", True))
        self.assertFalse(seam.get("network", True))
        self.assertEqual(d.get("pass"), False)

    def test_gate_cli_malformed_admissible_manifest_json_refusal(self):
        with tempfile.NamedTemporaryFile(suffix=".json", delete=False, mode="w") as f:
            f.write("{broken"); p = f.name
        r = subprocess.run([sys.executable, "scripts/tracka_resume_gate.py", "--admissible-manifest", p, "--json"],
                           capture_output=True, text=True, cwd=str(REAL))
        self.assertNotEqual(r.returncode, 0)
        d = json.loads(r.stdout)
        seam = d.get("admissible_seam_wired") or {}
        self.assertFalse(seam.get("pass", True))
        self.assertTrue(seam.get("fail_closed", False) is True or d.get("status") == "BLOCKED")
        self.assertFalse(d.get("outcomes_inspected", False))
        self.assertFalse(d.get("network", False))
        self.assertFalse(d.get("writes_real_research_state", False))

    def test_operator_cli_malformed_admissible_manifest_json_refusal(self):
        with tempfile.NamedTemporaryFile(suffix=".json", delete=False, mode="w") as f:
            f.write("{broken"); p = f.name
        r = subprocess.run([sys.executable, "scripts/tracka_operator_report.py", "--json", "--admissible-manifest", p],
                           capture_output=True, text=True, cwd=str(REAL))
        self.assertNotEqual(r.returncode, 0)
        d = json.loads(r.stdout)
        seam = d.get("admissible_seam_wired") or d.get("admissible_seam_state") or {}
        self.assertFalse(seam.get("pass", True))
        self.assertFalse(d.get("network", False))
        self.assertFalse(d.get("writes_real_research_state", False))
        self.assertIn("failures", seam)
        self.assertIsInstance(seam.get("failures"), list)

    def test_gate_cli_malformed_manifest_json_refusal(self):
        with tempfile.NamedTemporaryFile(suffix=".json", delete=False, mode="w") as f:
            f.write("{broken"); p = f.name
        r = subprocess.run([sys.executable, "scripts/tracka_resume_gate.py", "--manifest", p, "--json"],
                           capture_output=True, text=True, cwd=str(REAL))
        self.assertNotEqual(r.returncode, 0)
        d = json.loads(r.stdout)
        self.assertEqual(d.get("status"), "BLOCKED")
        self.assertEqual(d.get("reason_code"), BLOCKED_RC)
        self.assertFalse(d.get("outcomes_inspected", False))
        self.assertFalse(d.get("network", False))
        self.assertFalse(d.get("writes_real_research_state", False))


class Test132G3CLIRefusalSchemaStability(unittest.TestCase):
    """G3: CLI refusal schema stability matrix for covered Track A CLIs on
    malformed --admissible-manifest / --manifest / bad temp-path edge cases."""

    def _run(self, cmd):
        return subprocess.run(cmd, capture_output=True, text=True, cwd=str(REAL))

    def _assert_refusal_shape(self, data):
        for k in REQ_REFUSAL:
            self.assertIn(k, data, f"missing refusal field {k}: {data}")
        self.assertEqual(data.get("status"), "BLOCKED", data)
        for k in SAFE_FALSE:
            self.assertIs(data.get(k), False, (k, data.get(k), data))

    def test_gate_cli_bad_output_dir_refusal_shape(self):
        """Bad temp-path edge case: pre-existing regular file as output_dir."""
        with tempfile.NamedTemporaryFile(suffix=".json", delete=False) as f:
            bad_dir = f.name
        r = self._run([sys.executable, "scripts/tracka_resume_gate.py",
                       "--output-dir", bad_dir, "--json"])
        self.assertNotEqual(r.returncode, 0)
        d = json.loads(r.stdout)
        self._assert_refusal_shape(d)
        self.assertEqual(d.get("reason_code_detail"), "OUTPUT_DIR_UNUSABLE_FAIL_CLOSED", d)

    def test_gate_cli_malformed_manifest_refusal_shape(self):
        with tempfile.NamedTemporaryFile(suffix=".json", delete=False, mode="w") as f:
            f.write("{broken"); p = f.name
        r = self._run([sys.executable, "scripts/tracka_resume_gate.py", "--manifest", p, "--json"])
        self.assertNotEqual(r.returncode, 0)
        d = json.loads(r.stdout)
        self._assert_refusal_shape(d)

    def test_gate_cli_malformed_admissible_manifest_refusal_shape(self):
        with tempfile.NamedTemporaryFile(suffix=".json", delete=False, mode="w") as f:
            f.write("{broken"); p = f.name
        r = self._run([sys.executable, "scripts/tracka_resume_gate.py",
                       "--admissible-manifest", p, "--json"])
        self.assertNotEqual(r.returncode, 0)
        d = json.loads(r.stdout)
        self._assert_refusal_shape(d)

    def test_check_cli_malformed_admissible_manifest_refusal_shape(self):
        with tempfile.NamedTemporaryFile(suffix=".json", delete=False, mode="w") as f:
            f.write("{broken"); p = f.name
        r = self._run([sys.executable, "scripts/tracka_resume_check.py", "--admissible-manifest", p])
        self.assertNotEqual(r.returncode, 0)
        d = json.loads(r.stdout)
        self.assertEqual(d.get("pass"), False, d)
        self.assertIn(d.get("status"), ("BLOCKED", "NO-GO"), d)
        self.assertIn("reason_code", d, d)
        self.assertFalse(d.get("network", False), d)
        self.assertFalse(d.get("writes_real_research_state", False), d)
        self.assertFalse(d.get("canonical_outputs_mutated", True), d)
        self.assertFalse(d.get("outcomes_inspected", True), d)

    def test_operator_cli_malformed_admissible_manifest_refusal_shape(self):
        with tempfile.NamedTemporaryFile(suffix=".json", delete=False, mode="w") as f:
            f.write("{broken"); p = f.name
        r = self._run([sys.executable, "scripts/tracka_operator_report.py", "--json", "--admissible-manifest", p])
        self.assertNotEqual(r.returncode, 0)
        d = json.loads(r.stdout)
        # Operator report passes (correctly detects block); assert refusal shape
        # is present in the embedded gate_decision instead.
        gate = d.get("gate_decision") or {}
        self._assert_refusal_shape(gate)
        self.assertFalse(d.get("network", False), d)
        self.assertFalse(d.get("writes_real_research_state", False), d)
        seam = d.get("admissible_seam_wired") or {}
        self.assertFalse(seam.get("pass", True))
        self.assertIsInstance(seam.get("failures"), list)

    def test_cli_argparse_contract_violation_refuses_as_json_all_clis(self):
        # G3/134: argparse contract violations (unknown flags, bad --output-dir) must
        # refuse as parseable JSON on every Track A CLI, never as an uncaught
        # usage/traceback exit. --help is the only allowed exit-0 non-JSON path.
        REQ = {"status", "reason_code", "outcomes_inspected", "network",
               "writes_real_research_state", "canonical_outputs_mutated",
               "reads_parquet", "reads_outcomes", "fail_closed_order"}
        cases = [
            (["scripts/tracka_resume_gate.py", "--bogus", "--json"], "tracka_resume_gate",
             "drift_preflight->manifest_prereg"),
            (["scripts/tracka_resume_check.py", "--bogus"], "tracka_resume_check",
             "drift_preflight->admissible_seam"),
            (["scripts/tracka_operator_report.py", "--bogus", "--json"], "tracka_operator_report",
             "drift_preflight->gate_decision->probe_invariant_state"),
            (["scripts/tracka_operator_report.py", "--output-dir", "/nonexistent/zzz", "--json"],
             "tracka_operator_report", "drift_preflight->gate_decision->probe_invariant_state"),
        ]
        for cmd, script, order in cases:
            r = self._run([sys.executable] + cmd)
            self.assertNotEqual(r.returncode, 0, f"{cmd}: {r.stdout}")
            self.assertNotIn("Traceback", r.stderr, f"{cmd}: {r.stderr}")
            self.assertNotIn("usage:", r.stdout, f"{cmd}: {r.stdout}")
            d = json.loads(r.stdout)
            for k in REQ:
                self.assertIn(k, d, f"{cmd} missing {k}: {d}")
            # gate uses gate_script; check/operator use script — accept either.
            self.assertIn(d.get("script") or d.get("gate_script"), (script, None), f"{cmd}: {d}")
            self.assertEqual(d.get("status"), "BLOCKED", f"{cmd}: {d}")
            self.assertEqual(d.get("reason_code"), BLOCKED_RC, f"{cmd}: {d}")
            self.assertEqual(d.get("reason_code_detail"), "ARGPARSE_CONTRACT_VIOLATION_FAIL_CLOSED", f"{cmd}: {d}")
            self.assertEqual(d.get("fail_closed_order"), order, f"{cmd}: {d}")
            for k in ("outcomes_inspected", "canonical_outputs_mutated", "network",
                      "writes_real_research_state", "reads_parquet", "reads_outcomes"):
                self.assertIs(d.get(k), False, f"{cmd} {k}: {d.get(k)}")
        # --help must still exit 0 (the only non-refusal exit).
        r = self._run([sys.executable, "scripts/tracka_operator_report.py", "--help"])
        self.assertEqual(r.returncode, 0)

    def test_operator_cli_bad_output_dir_refuses_as_json(self):
        # G3/134: bad --output-dir on the operator CLI (previously a traceback) now
        # refuses as parseable JSON with the stable seam-wired refusal shape.
        r = self._run([sys.executable, "scripts/tracka_operator_report.py",
                       "--output-dir", "/nonexistent/zzz", "--json"])
        self.assertNotEqual(r.returncode, 0)
        self.assertNotIn("Traceback", r.stderr)
        d = json.loads(r.stdout)
        self._assert_refusal_shape(d)
        self.assertEqual(d.get("reason_code_detail"), "ARGPARSE_CONTRACT_VIOLATION_FAIL_CLOSED", d)

    def test_canonical_outputs_not_mutated_on_argparse_refusal(self):
        before = _snap([FRONTIER, RUN_MANIFEST, EVAL_FCLR010])
        self._run([sys.executable, "scripts/tracka_resume_gate.py", "--bogus", "--json"])
        self._run([sys.executable, "scripts/tracka_resume_check.py", "--bogus"])
        self._run([sys.executable, "scripts/tracka_operator_report.py", "--bogus", "--json"])
        _unchanged([FRONTIER, RUN_MANIFEST, EVAL_FCLR010], before)

    def test_canonical_outputs_not_mutated_on_refusal(self):
        before = _snap([FRONTIER, RUN_MANIFEST, EVAL_FCLR010])
        with tempfile.NamedTemporaryFile(suffix=".json", delete=False, mode="w") as f:
            f.write("{broken"); p = f.name
        self._run([sys.executable, "scripts/tracka_resume_gate.py", "--manifest", p, "--json"])
        self._run([sys.executable, "scripts/tracka_operator_report.py", "--json", "--admissible-manifest", p])
        self._run([sys.executable, "scripts/tracka_resume_check.py", "--admissible-manifest", p])
        _unchanged([FRONTIER, RUN_MANIFEST, EVAL_FCLR010], before)


if __name__ == "__main__":
    unittest.main()
