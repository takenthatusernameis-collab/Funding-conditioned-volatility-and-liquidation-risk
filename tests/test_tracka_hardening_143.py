"""FCLR-NEXT-143: handoff-freshness + mandatory-heavy-work gate regression.

tmp-isolated, read-only, no network, no parquet/outcome reads, no real
research_state writes. Closes the last structural bottleneck in the
trigger-only frontier: the mandated heavy campaign (FCLR-RCA-011 / Phase-B)
was prose-only, so a future session could "complete" by running only the
trigger check + the unittest suite and skipping the heavy artifacts.

These tests pin the invariant that the durable handoff must point at a
heavy session that either contains the Phase-B/C bundle or carries it forward
with a fresh evidence audit and quantitative artifact. The gate must also fail
loudly if the latest session is incomplete or the root churn cap is breached.
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

    def test_new_style_latest_session_with_audit_and_quant_passes(self):
        # A later audit session may carry the complete bundle forward and add a
        # fresh quantitative artifact instead of copying Phase-B into itself.
        latest_sid = "session_20261116T115028Z"
        latest = self.repo / "research_state" / latest_sid
        latest.mkdir()
        (latest / "evidence_audit_x.md").write_text("x")
        (latest / "independent_recompute_x.json").write_text("{}")
        with (self.repo / "AGENT_HANDOFF.md").open("a") as fh:
            fh.write(f"\nLatest session: research_state/{latest_sid}/\n")
        res = gate.check(self.repo)
        self.assertTrue(res["pass"], res["failures"])
        self.assertEqual(res["heavy_session_id"], self.sid)
        self.assertEqual(res["latest_session_id"], latest_sid)
        self.assertTrue(res["latest_session_evidence"]["has_audit"])
        self.assertTrue(res["latest_session_evidence"]["has_new_quant"])

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


class TestFrontierVerifyCampaignGate(unittest.TestCase):
    """FCLR-FRONTIER-VERIFY-06: once the campaign has started, a post-start
    session cannot satisfy the heavy-work gate with an arbitrary recompute_*
    artifact. It must emit the exact exhaustive-audit triad and a trigger check.
    Sessions predating the campaign remain grandfathered."""

    START = "20261117T130551Z"

    def _repo(self, latest_sid="session_20261117T140000Z"):
        tmp = Path(tempfile.mkdtemp(prefix="fclr143fv_"))
        self.addCleanup(shutil.rmtree, tmp, ignore_errors=True)
        repo = tmp / "repo"
        sdir = repo / "research_state" / latest_sid
        sdir.mkdir(parents=True)
        # Carry-forward Phase-B/C bundle so only the new frontier contract is tested.
        base = repo / "research_state" / "session_20261116T035833Z"
        base.mkdir()
        for name in (
            "rca011_feature_attribution_x.json",
            "rca011_impl_crosscheck_x.json",
            "rca011_sealed_bridge_x.md",
            "prereg_template_trigger_gated_x.json",
            "program_power_synthesis_x.md",
        ):
            (base / name).write_text("x")
        (sdir / "evidence_audit_x.md").write_text("x")
        (repo / "AGENT_HANDOFF.md").write_text(
            "# AGENT HANDOFF\n\n## INITIAL TASK MESSAGE FOR NEXT AGENTIC WORK SESSION\n"
            f"Campaign FCLR-FRONTIER-VERIFY-06-{self.START}\n"
            f"Latest session: research_state/{latest_sid}/\n"
        )
        return repo, sdir

    def test_post_start_generic_recompute_only_fails_closed(self):
        repo, sdir = self._repo()
        (sdir / "recompute_generic_x.json").write_text("{}")
        res = gate.check(repo)
        self.assertFalse(res["pass"])
        self.assertTrue(res["frontier_verify"]["required"])
        self.assertTrue(res["frontier_verify"]["missing_required_artifacts"])
        self.assertTrue(any(f.startswith("FRONTIER_VERIFY_ARTIFACTS_MISSING")
                            for f in res["failures"]))
        self.assertTrue(any(f.startswith("FRONTIER_VERIFY_TRIGGER_CHECK_MISSING")
                            for f in res["failures"]))

    def test_post_start_exact_triad_and_trigger_passes(self):
        repo, sdir = self._repo()
        for suffix in (".py", ".json", ".md"):
            (sdir / f"recompute_frontier_exhaustive_audit_20261117T140000Z{suffix}").write_text("x")
        (sdir / "trigger_check_20261117T140000Z.json").write_text("{}")
        res = gate.check(repo)
        self.assertTrue(res["pass"], res["failures"])
        self.assertTrue(res["frontier_verify"]["pass"])

    def test_pre_start_session_is_grandfathered(self):
        repo, sdir = self._repo(latest_sid="session_20261117T000000Z")
        (sdir / "recompute_generic_x.json").write_text("{}")
        res = gate.check(repo)
        self.assertFalse(res["frontier_verify"]["required"])
        self.assertTrue(res["pass"], res["failures"])


class TestTriggerReadinessCampaignGate(unittest.TestCase):
    """FCLR-TRIGGER-READINESS-01: once the campaign has started, a post-start
    session cannot satisfy the heavy-work gate with an arbitrary recompute_*
    artifact or a trigger-check-only session. It must emit the outcome-blind
    trigger-activation package (executor + self-test + readiness certificate)
    plus a trigger check. Sessions predating the campaign are grandfathered."""

    START = "20261117T203325Z"

    def _repo(self, latest_sid="session_20261118T000000Z"):
        tmp = Path(tempfile.mkdtemp(prefix="fclr143tr_"))
        self.addCleanup(shutil.rmtree, tmp, ignore_errors=True)
        repo = tmp / "repo"
        sdir = repo / "research_state" / latest_sid
        sdir.mkdir(parents=True)
        # Carry-forward Phase-B/C bundle so only the trigger-readiness contract.
        base = repo / "research_state" / "session_20261116T035833Z"
        base.mkdir()
        for name in (
            "rca011_feature_attribution_x.json",
            "rca011_impl_crosscheck_x.json",
            "rca011_sealed_bridge_x.md",
            "prereg_template_trigger_gated_x.json",
            "program_power_synthesis_x.md",
        ):
            (base / name).write_text("x")
        (sdir / "evidence_audit_x.md").write_text("x")
        (repo / "AGENT_HANDOFF.md").write_text(
            "# AGENT HANDOFF\n\n## INITIAL TASK MESSAGE FOR NEXT AGENTIC WORK SESSION\n"
            f"Campaign FCLR-TRIGGER-READINESS-01-{self.START}\n"
            f"Latest session: research_state/{latest_sid}/\n"
        )
        return repo, sdir

    def _write_package(self, sdir):
        for prefix, suffix in gate.TRIGGER_READINESS_REQUIRED:
            (sdir / f"{prefix}20261118T000000Z{suffix}").write_text("x")

    def test_post_start_generic_recompute_only_fails_closed(self):
        repo, sdir = self._repo()
        (sdir / "recompute_generic_x.json").write_text("{}")
        (sdir / "trigger_check_20261118T000000Z.json").write_text("{}")
        res = gate.check(repo)
        self.assertFalse(res["pass"])
        self.assertTrue(res["trigger_readiness"]["required"])
        self.assertTrue(res["trigger_readiness"]["missing_required_artifacts"])
        self.assertTrue(any(f.startswith("TRIGGER_READINESS_ARTIFACTS_MISSING")
                            for f in res["failures"]))

    def test_post_start_package_without_trigger_check_fails_closed(self):
        repo, sdir = self._repo()
        self._write_package(sdir)  # full package, but no trigger_check_*.json
        res = gate.check(repo)
        self.assertFalse(res["pass"])
        self.assertTrue(res["trigger_readiness"]["required"])
        self.assertTrue(any(f.startswith("TRIGGER_READINESS_TRIGGER_CHECK_MISSING")
                            for f in res["failures"]))

    def test_post_start_full_package_and_trigger_passes(self):
        repo, sdir = self._repo()
        self._write_package(sdir)
        (sdir / "trigger_check_20261118T000000Z.json").write_text("{}")
        res = gate.check(repo)
        self.assertTrue(res["pass"], res["failures"])
        self.assertTrue(res["trigger_readiness"]["pass"])

    def test_pre_start_session_is_grandfathered(self):
        repo, sdir = self._repo(latest_sid="session_20261117T000000Z")
        (sdir / "recompute_generic_x.json").write_text("{}")
        res = gate.check(repo)
        self.assertFalse(res["trigger_readiness"]["required"])
        self.assertTrue(res["pass"], res["failures"])


class TestLedgerIntegrityCampaignGate(unittest.TestCase):
    """FCLR-LEDGER-INTEGRITY-02: once the ledger-integrity campaign has started,
    a post-start session cannot satisfy the heavy-work gate with an arbitrary
    recompute_* artifact or a trigger-check-only session. It must emit the
    outcome-blind ledger audit + frontier recompute + trigger check + refreshed
    trigger-activation readiness. Sessions predating the campaign are
    grandfathered."""

    START = "20261118T000000Z"

    def _repo(self, latest_sid="session_20261118T010000Z"):
        tmp = Path(tempfile.mkdtemp(prefix="fclr143li_"))
        self.addCleanup(shutil.rmtree, tmp, ignore_errors=True)
        repo = tmp / "repo"
        sdir = repo / "research_state" / latest_sid
        sdir.mkdir(parents=True)
        # Carry-forward Phase-B/C bundle so only the ledger contract is tested.
        base = repo / "research_state" / "session_20261116T035833Z"
        base.mkdir()
        for name in (
            "rca011_feature_attribution_x.json",
            "rca011_impl_crosscheck_x.json",
            "rca011_sealed_bridge_x.md",
            "prereg_template_trigger_gated_x.json",
            "program_power_synthesis_x.md",
        ):
            (base / name).write_text("x")
        (sdir / "evidence_audit_x.md").write_text("x")
        (repo / "AGENT_HANDOFF.md").write_text(
            "# AGENT HANDOFF\n\n## INITIAL TASK MESSAGE FOR NEXT AGENTIC WORK SESSION\n"
            f"Campaign FCLR-LEDGER-INTEGRITY-02-{self.START}\n"
            f"Latest session: research_state/{latest_sid}/\n"
        )
        return repo, sdir

    def _write_required(self, sdir, sid="20261118T010000Z"):
        for prefix, suffix in gate.LEDGER_INTEGRITY_REQUIRED:
            (sdir / f"{prefix}{sid}{suffix}").write_text("x")

    def test_post_start_generic_recompute_only_fails_closed(self):
        repo, sdir = self._repo()
        (sdir / "recompute_generic_x.json").write_text("{}")
        (sdir / "trigger_check_20261118T010000Z.json").write_text("{}")
        res = gate.check(repo)
        self.assertFalse(res["pass"])
        self.assertTrue(res["ledger_integrity"]["required"])
        self.assertTrue(res["ledger_integrity"]["missing_required_artifacts"])
        self.assertTrue(any(f.startswith("LEDGER_INTEGRITY_ARTIFACTS_MISSING")
                            for f in res["failures"]))

    def test_post_start_full_ledger_set_passes(self):
        repo, sdir = self._repo()
        self._write_required(sdir)
        res = gate.check(repo)
        self.assertTrue(res["pass"], res["failures"])
        self.assertTrue(res["ledger_integrity"]["pass"])

    def test_post_start_missing_readiness_fails_closed(self):
        repo, sdir = self._repo()
        for prefix, suffix in gate.LEDGER_INTEGRITY_REQUIRED:
            if prefix == "trigger_activation_readiness_":
                continue
            (sdir / f"{prefix}20261118T010000Z{suffix}").write_text("x")
        (sdir / "trigger_check_20261118T010000Z.json").write_text("{}")
        res = gate.check(repo)
        self.assertFalse(res["pass"])
        self.assertTrue(any(f.startswith("LEDGER_INTEGRITY_ARTIFACTS_MISSING")
                            for f in res["failures"]))

    def test_pre_start_session_is_grandfathered(self):
        repo, sdir = self._repo(latest_sid="session_20261117T000000Z")
        (sdir / "recompute_generic_x.json").write_text("{}")
        res = gate.check(repo)
        self.assertFalse(res["ledger_integrity"]["required"])
        self.assertTrue(res["pass"], res["failures"])


class TestHandoffFreshnessGate(unittest.TestCase):
    """FCLR-TRIGGER-READINESS-01: a newer on-disk session that is not recorded
    in the handoff fails closed. The gate must not stay green merely because the
    handoff still points at an older session while a post-campaign session skips
    the trigger-activation package."""

    START = "20261117T203457Z"

    def _repo(self, handoff_sid="session_20261117T194457Z",
              disk_sid="session_20261118T000000Z"):
        tmp = Path(tempfile.mkdtemp(prefix="fclr143fresh_"))
        self.addCleanup(shutil.rmtree, tmp, ignore_errors=True)
        repo = tmp / "repo"
        rs = repo / "research_state"
        rs.mkdir(parents=True)
        # Complete carried-forward Phase-B/C bundle.
        base = rs / "session_20261116T035833Z"
        base.mkdir()
        for name in (
            "rca011_feature_attribution_x.json",
            "rca011_impl_crosscheck_x.json",
            "rca011_sealed_bridge_x.md",
            "prereg_template_trigger_gated_x.json",
            "program_power_synthesis_x.md",
        ):
            (base / name).write_text("x")
        # Older session referenced by the handoff.
        old = rs / handoff_sid
        old.mkdir()
        (old / "evidence_audit_x.md").write_text("x")
        (old / "recompute_x.json").write_text("{}")
        # Newer session on disk, not yet referenced by the handoff.
        new = rs / disk_sid
        new.mkdir()
        (new / "evidence_audit_x.md").write_text("x")
        (new / "trigger_check_x.json").write_text("{}")
        (repo / "AGENT_HANDOFF.md").write_text(
            "# AGENT HANDOFF\n\n## INITIAL TASK MESSAGE FOR NEXT AGENTIC WORK SESSION\n"
            f"Campaign FCLR-TRIGGER-READINESS-01-{self.START}\n"
            f"Latest session: research_state/{handoff_sid}/\n"
        )
        return repo, new

    def test_newer_disk_session_not_in_handoff_fails_closed(self):
        repo, _ = self._repo()
        res = gate.check(repo)
        self.assertFalse(res["pass"])
        self.assertTrue(res["handoff_stale"])
        self.assertTrue(any(f.startswith("HANDOFF_STALE_LATEST_SESSION")
                            for f in res["failures"]))

    def test_handoff_recorded_new_session_is_checked_and_passes(self):
        repo, new = self._repo()
        text = (repo / "AGENT_HANDOFF.md").read_text()
        text += "\nLatest session: research_state/session_20261118T000000Z/\n"
        (repo / "AGENT_HANDOFF.md").write_text(text)
        for prefix, suffix in gate.TRIGGER_READINESS_REQUIRED:
            (new / f"{prefix}20261118T000000Z{suffix}").write_text("x")
        res = gate.check(repo)
        self.assertTrue(res["pass"], res["failures"])
        self.assertFalse(res["handoff_stale"])
        self.assertEqual(res["latest_session_id"], "session_20261118T000000Z")


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