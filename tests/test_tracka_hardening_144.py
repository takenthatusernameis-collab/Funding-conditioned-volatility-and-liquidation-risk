"""FCLR-NEXT-144: FCLR-LIQ-CONTAGION-002 robustness-reconciliation gate regression.

tmp-isolated, read-only, no network, no parquet/outcome reads, no real
research_state writes. Closes the bottleneck left by the 2026-11-21T19:51:14Z
handoff, which declared the frozen-data frontier exhausted and told future
agents to "verify green and stop" — letting them dodge the disclosed,
unresolved methodological discrepancy from FCLR-LIQ-CONTAGION-001 (eval = 11
edges vs independent recompute = 58 edges; the declared 2% per-edge materiality
floor was asserted True but never actually computed; funding-tercile and
temporal-stability results were never reconciled against the primary edge set).

These tests pin the invariant that once FCLR-LIQ-CONTAGION-002 starts, a
post-start session cannot satisfy the heavy-work gate with a trigger-only,
prose-only, audit-only, verify-and-stop, or arbitrary recompute_* session. It
must emit the outcome-blind reconciliation prereg, the heavy reconciliation
evaluation triad, the independent stdlib recompute, the contagion evidence
audit, the gate-critical evidence_audit_ alias, and a trigger check, with no
zero-byte placeholders. Sessions predating the campaign start (including the
CONTAGION-001 session_20261121T193000Z) are grandfathered.
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


class TestContagion002CampaignGate(unittest.TestCase):
    """FCLR-LIQ-CONTAGION-002: once the robustness-reconciliation campaign has
    started, a post-start session cannot satisfy the heavy-work gate with a
    trigger-only, prose-only, audit-only, verify-and-stop, or arbitrary
    recompute_* session. It must emit the outcome-blind reconciliation prereg,
    the reconciliation evaluation triad, the independent stdlib recompute, the
    contagion evidence audit, the gate-critical evidence_audit_ alias, and a
    trigger check, with no zero-byte placeholders. Sessions predating the
    campaign are grandfathered."""

    START = "20261121T200000Z"

    def _repo(self, latest_sid="session_20261121T210000Z",
              handoff_campaigns=("FCLR-LIQ-CONTAGION-002",)):
        tmp = Path(tempfile.mkdtemp(prefix="fclr144ct2_"))
        self.addCleanup(shutil.rmtree, tmp, ignore_errors=True)
        repo = tmp / "repo"
        sdir = repo / "research_state" / latest_sid
        sdir.mkdir(parents=True)
        # Carry-forward Phase-B/C bundle so only the 002 contract is tested.
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
        campaign_lines = "".join(f"Campaign {c}-{self.START}\n" for c in handoff_campaigns)
        (repo / "AGENT_HANDOFF.md").write_text(
            "# AGENT HANDOFF\n\n## INITIAL TASK MESSAGE FOR NEXT AGENTIC WORK SESSION\n"
            f"{campaign_lines}"
            f"Latest session: research_state/{latest_sid}/\n"
        )
        return repo, sdir

    def _write_package(self, sdir, utc):
        for prefix, suffix in gate.CONTAGION_002_REQUIRED:
            if prefix in ("evidence_audit_", "trigger_check_"):
                continue
            (sdir / f"{prefix}{utc}{suffix}").write_text("x")
        (sdir / f"evidence_audit_{utc}.json").write_text("{}")

    def test_post_start_audit_only_fails_closed(self):
        repo, sdir = self._repo()
        (sdir / "trigger_check_20261121T210000Z.json").write_text("{}")
        res = gate.check(repo)
        self.assertFalse(res["pass"])
        self.assertTrue(res["contagion_002"]["required"])
        self.assertTrue(res["contagion_002"]["missing_required_artifacts"])
        self.assertTrue(any(f.startswith("CONTAGION_002_ARTIFACTS_MISSING")
                            for f in res["failures"]))

    def test_post_start_verify_and_stop_fails_closed(self):
        # A "verify green and stop" session that only drops a trigger check and
        # a generic recompute_* file (no reconciliation artifacts) must fail.
        repo, sdir = self._repo()
        (sdir / "trigger_check_20261121T210000Z.json").write_text("{}")
        (sdir / "recompute_stopgap_20261121T210000Z.json").write_text("{}")
        res = gate.check(repo)
        self.assertFalse(res["pass"])
        self.assertTrue(res["contagion_002"]["required"])
        self.assertTrue(any(f.startswith("CONTAGION_002_ARTIFACTS_MISSING")
                            for f in res["failures"]))

    def test_post_start_package_without_trigger_fails_closed(self):
        repo, sdir = self._repo()
        self._write_package(sdir, "20261121T210000Z")  # no trigger_check
        res = gate.check(repo)
        self.assertFalse(res["pass"])
        self.assertTrue(res["contagion_002"]["required"])
        self.assertTrue(any(f.startswith("CONTAGION_002_TRIGGER_CHECK_MISSING")
                            for f in res["failures"]))

    def test_post_start_empty_files_fail_closed(self):
        repo, sdir = self._repo()
        self._write_package(sdir, "20261121T210000Z")
        (sdir / "trigger_check_20261121T210000Z.json").write_text("{}")
        # Zero out one required artifact.
        victim = next(
            p for p in sdir.iterdir()
            if p.name.startswith("fclr_liq_contagion02_recon_") and p.suffix == ".py"
        )
        victim.write_text("")
        res = gate.check(repo)
        self.assertFalse(res["pass"])
        self.assertTrue(res["contagion_002"]["required"])
        self.assertTrue(res["contagion_002"]["empty_required_artifacts"])
        self.assertTrue(any(f.startswith("CONTAGION_002_ARTIFACTS_EMPTY")
                            for f in res["failures"]))

    def test_post_start_full_package_and_trigger_passes(self):
        repo, sdir = self._repo()
        self._write_package(sdir, "20261121T210000Z")
        (sdir / "trigger_check_20261121T210000Z.json").write_text("{}")
        res = gate.check(repo)
        self.assertTrue(res["pass"], res["failures"])
        self.assertTrue(res["contagion_002"]["pass"])

    def test_pre_start_session_is_grandfathered(self):
        # The CONTAGION-001 session (20261121T193000Z) predates the 002 start and
        # must not be forced to carry 002 artifacts.
        repo, sdir = self._repo(latest_sid="session_20261121T193000Z")
        (sdir / "fclr_liq_contagion01_prereg_20261121T193000Z.json").write_text("{}")
        (sdir / "fclr_liq_contagion01_eval_20261121T193000Z.py").write_text("x")
        (sdir / "fclr_liq_contagion01_eval_20261121T193000Z.json").write_text("{}")
        (sdir / "fclr_liq_contagion01_eval_20261121T193000Z.md").write_text("x")
        (sdir / "fclr_liq_contagion01_recompute_20261121T193000Z.py").write_text("x")
        (sdir / "fclr_liq_contagion01_recompute_20261121T193000Z.json").write_text("{}")
        (sdir / "fclr_liq_contagion01_evidence_audit_20261121T193000Z.json").write_text("{}")
        (sdir / "fclr_liq_contagion01_evidence_audit_20261121T193000Z.md").write_text("x")
        (sdir / "evidence_audit_20261121T193000Z.json").write_text("{}")
        (sdir / "trigger_check_20261121T193000Z.json").write_text("{}")
        res = gate.check(repo)
        self.assertFalse(res["contagion_002"]["required"])
        self.assertTrue(res["pass"], res["failures"])

    def test_ladder_binds_highest_contagion_campaign(self):
        # When the handoff references BOTH 001 (history) and 002 (active), the
        # gate must bind 002 artifacts and leave 001 unbound (it is completed).
        repo, sdir = self._repo(
            handoff_campaigns=(
                "FCLR-LIQ-CONTAGION-001",
                "FCLR-LIQ-CONTAGION-002",
            )
        )
        self._write_package(sdir, "20261121T210000Z")
        (sdir / "trigger_check_20261121T210000Z.json").write_text("{}")
        res = gate.check(repo)
        self.assertTrue(res["pass"], res["failures"])
        self.assertTrue(res["contagion_002"]["required"])
        self.assertFalse(res["contagion"]["required"])

    def test_only_001_referenced_does_not_bind_002(self):
        # A handoff whose highest CONTAGION campaign is 001 must not bind the
        # 002 reconciliation contract; the dedicated 001 state function handles it.
        repo, sdir = self._repo(
            handoff_campaigns=("FCLR-LIQ-CONTAGION-001",)
        )
        # Emit only the 001 package (no 002 artifacts).
        for prefix, suffix in gate.CONTAGION_REQUIRED:
            if prefix in ("evidence_audit_", "trigger_check_"):
                continue
            (sdir / f"{prefix}20261121T210000Z{suffix}").write_text("x")
        (sdir / f"evidence_audit_20261121T210000Z.json").write_text("{}")
        (sdir / "trigger_check_20261121T210000Z.json").write_text("{}")
        res = gate.check(repo)
        self.assertFalse(res["contagion_002"]["required"])
        self.assertTrue(res["pass"], res["failures"])


class TestHandoffGateCliContract(unittest.TestCase):
    def test_cli_json_pass_shape(self):
        import subprocess
        out = subprocess.run(
            [sys.executable, str(REAL / "scripts" / "check_handoff_heavywork_gate.py"), "--json"],
            capture_output=True, text=True,
        )
        self.assertEqual(out.returncode, 0, out.stderr)
        payload = json.loads(out.stdout)
        for k in ("pass", "reason_code", "network", "writes_real_research_state", "read_only", "failures", "contagion_002"):
            self.assertIn(k, payload)
        self.assertFalse(payload["network"])
        self.assertFalse(payload["writes_real_research_state"])
        self.assertTrue(payload["read_only"])
        self.assertTrue(payload["pass"])


if __name__ == "__main__":
    unittest.main()