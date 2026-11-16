"""FCLR-NEXT-143: handoff-freshness + mandatory-heavy-work gate regression.

tmp-isolated, read-only, no network, no parquet/outcome reads, no real
research_state writes. Closes the last structural bottleneck in the
trigger-only frontier: the mandated heavy campaign (FCLR-RCA-011 / Phase-B)
was prose-only, so a future session could "complete" by running only the
trigger check + the unittest suite and skipping the heavy artifacts.

These tests pin the invariant that the durable handoff must point at a
self-contained heavy-session evidence bundle, and that the gate fails
loudly if that bundle is incomplete or the root churn cap is breached.
"""
from __future__ import annotations

import json
import shutil
import sys
import tempfile
import unittest
from pathlib import Path

REAL = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REAL / "scripts"))

import check_handoff_heavywork_gate as gate  # noqa: E402


class TestHandoffGateOnRealRepo(unittest.TestCase):
    def test_real_repo_gate_passes(self):
        res = gate.check(REAL)
        self.assertTrue(
            res["pass"],
            f"handoff-heavywork gate must pass on the real repo: {res['failures']}",
        )
        self.assertEqual(res["reason_code"], "OK")

    def test_real_repo_handoff_has_markers(self):
        res = gate.check(REAL)
        self.assertTrue(res["handoff_exists"])
        self.assertTrue(res["handoff_markers_ok"])

    def test_real_repo_heavy_session_self_contained(self):
        res = gate.check(REAL)
        self.assertTrue(res["heavy_session_exists"])
        self.assertEqual(res["heavy_session_missing"], [])
        sid = res["heavy_session_id"]
        self.assertTrue(sid and sid.startswith("session_"))

    def test_real_repo_root_count_within_cap(self):
        res = gate.check(REAL)
        self.assertLessEqual(res["root_count"], res["root_count_cap"])


class TestHandoffGateFailsClosed(unittest.TestCase):
    """Prove the gate refuses (exit non-zero, machine-readable reasons) when the
    handoff or its heavy evidence bundle is missing/incomplete — so a future
    session cannot skip the mandated campaign and still pass the suite."""

    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp(prefix="fclr143_"))
        self.repo = self.tmp / "repo"
        (self.repo / "research_state").mkdir(parents=True)
        # Minimal valid handoff pointing at one session dir.
        self.sid = "session_20261116T035833Z"
        sdir = self.repo / "research_state" / self.sid
        sdir.mkdir()
        for name in (
            "rca011_feature_attribution_x.json",
            "rca011_impl_crosscheck_x.json",
            "rca011_sealed_bridge_x.md",
            "prereg_template_trigger_gated_x.json",
            "program_power_synthesis_x.md",
        ):
            (sdir / name).write_text("x")
        (self.repo / "AGENT_HANDOFF.md").write_text(
            "# AGENT HANDOFF\n\n## INITIAL TASK MESSAGE FOR NEXT AGENTIC WORK SESSION\n"
            f"See research_state/{self.sid}/ for evidence.\n"
        )

    def tearDown(self):
        shutil.rmtree(self.tmp, ignore_errors=True)

    def test_valid_minimal_bundle_passes(self):
        res = gate.check(self.repo)
        self.assertTrue(res["pass"], res["failures"])
        self.assertEqual(res["heavy_session_id"], self.sid)

    def test_missing_handoff_fails(self):
        (self.repo / "AGENT_HANDOFF.md").unlink()
        res = gate.check(self.repo)
        self.assertFalse(res["pass"])
        self.assertIn("HANDOFF_MISSING", res["failures"])

    def test_missing_markers_fail(self):
        (self.repo / "AGENT_HANDOFF.md").write_text("# AGENT HANDOFF\nno task section\n")
        res = gate.check(self.repo)
        self.assertFalse(res["pass"])
        self.assertTrue(any(f.startswith("HANDOFF_MARKERS_MISSING") for f in res["failures"]))

    def test_missing_session_dir_fails(self):
        shutil.rmtree(self.repo / "research_state" / self.sid)
        res = gate.check(self.repo)
        self.assertFalse(res["pass"])
        self.assertTrue(any(f.startswith("HEAVY_SESSION_DIR_MISSING") for f in res["failures"]))

    def test_incomplete_phase_b_fails(self):
        # Remove the prereg template -> Phase-B set incomplete.
        sdir = self.repo / "research_state" / self.sid
        for p in sdir.glob("prereg_template_trigger_gated_*"):
            p.unlink()
        res = gate.check(self.repo)
        self.assertFalse(res["pass"])
        self.assertTrue(any("prereg_template_trigger_gated_" in x for f in res["failures"] for x in [f]))

    def test_incomplete_phase_c_fails(self):
        sdir = self.repo / "research_state" / self.sid
        for p in sdir.glob("program_power_synthesis_*"):
            p.unlink()
        res = gate.check(self.repo)
        self.assertFalse(res["pass"])
        self.assertTrue(any("program_power_synthesis_" in f for f in res["failures"]))

    def test_unrecorded_session_id_fails(self):
        (self.repo / "AGENT_HANDOFF.md").write_text(
            "# AGENT HANDOFF\n\n## INITIAL TASK MESSAGE FOR NEXT AGENTIC WORK SESSION\n"
            "No session referenced.\n"
        )
        res = gate.check(self.repo)
        self.assertFalse(res["pass"])
        self.assertIn("HEAVY_SESSION_ID_UNRECORDED", res["failures"])

    def test_root_count_cap_breach_fails(self):
        # Flood the root with >cap files (tmp-isolated; never touches real state).
        rs = self.repo / "research_state"
        for i in range(gate.ROOT_COUNT_CAP + 5):
            (rs / f"junk_{i}.json").write_text("{}")
        res = gate.check(self.repo)
        self.assertFalse(res["pass"])
        self.assertTrue(any(f.startswith("ROOT_COUNT_EXCEEDS_CAP") for f in res["failures"]))


class TestHandoffGateCliContract(unittest.TestCase):
    def test_cli_json_pass_shape(self):
        import subprocess
        out = subprocess.run(
            [sys.executable, str(REAL / "scripts" / "check_handoff_heavywork_gate.py"), "--json"],
            capture_output=True, text=True,
        )
        self.assertEqual(out.returncode, 0, out.stderr)
        payload = json.loads(out.stdout)
        for k in ("pass", "reason_code", "network", "writes_real_research_state", "read_only", "failures"):
            self.assertIn(k, payload)
        self.assertFalse(payload["network"])
        self.assertFalse(payload["writes_real_research_state"])
        self.assertTrue(payload["read_only"])
        self.assertTrue(payload["pass"])


if __name__ == "__main__":
    unittest.main()