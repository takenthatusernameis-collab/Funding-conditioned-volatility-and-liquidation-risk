"""FCLR-HANDOFF-145: FCLR-POOLED-AUDIT-001 heavy-work gate regression.

The 2026-11-22T10:56:54Z handoff declared FCLR-POOLED-001 complete and named
FCLR-POOLED-AUDIT-001 as the next focus, but it did not bind that campaign in
scripts/check_handoff_heavywork_gate.py. A future session could therefore run a
trigger-only, prose-only, or generic audit session and still pass the gate.

These tmp-isolated tests pin the invariant that once FCLR-POOLED-AUDIT-001
starts, a post-start session must emit the frozen adversarial-audit protocol,
the heavy audit implementation + JSON + Markdown triad, the independent stdlib
recompute (py+json), the audit evidence package, the gate alias, and a trigger
check, with no zero-byte placeholders. Pre-start sessions are grandfathered.
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


class TestPooledAudit001CampaignGate(unittest.TestCase):
    START = "20261122T110000Z"

    def _repo(self, latest_sid="session_20261122T120000Z"):
        tmp = Path(tempfile.mkdtemp(prefix="fclr145pa_"))
        self.addCleanup(shutil.rmtree, tmp, ignore_errors=True)
        repo = tmp / "repo"
        sdir = repo / "research_state" / latest_sid
        sdir.mkdir(parents=True)
        # Carry-forward Phase-B/C bundle so only the pooled-audit contract binds.
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
            f"Campaign FCLR-POOLED-AUDIT-001-{self.START}\n"
            f"Latest session: research_state/{latest_sid}/\n"
        )
        return repo, sdir

    def _write_required(self, sdir, sid="20261122T120000Z", content="x"):
        for prefix, suffix in gate.POOLED_AUDIT_REQUIRED:
            if prefix == "trigger_check_":
                (sdir / f"trigger_check_{sid}.json").write_text(content)
                continue
            name_prefix = prefix.replace("fclr_pooled_audit_", "fclr_pooled_audit001_", 1)
            (sdir / f"{name_prefix}{sid}{suffix}").write_text(content)

    def test_post_start_trigger_only_fails_closed(self):
        repo, sdir = self._repo()
        (sdir / "trigger_check_20261122T120000Z.json").write_text("{}")
        res = gate.check(repo)
        self.assertFalse(res["pass"])
        self.assertTrue(res["pooled_audit"]["required"])
        self.assertTrue(res["pooled_audit"]["missing_required_artifacts"])
        self.assertTrue(any(f.startswith("POOLED_AUDIT_ARTIFACTS_MISSING")
                            for f in res["failures"]))

    def test_post_start_prose_only_fails_closed(self):
        repo, sdir = self._repo()
        (sdir / "audit_notes_20261122T120000Z.md").write_text("looks fine")
        res = gate.check(repo)
        self.assertFalse(res["pass"])
        self.assertTrue(any(f.startswith("POOLED_AUDIT_ARTIFACTS_MISSING")
                            for f in res["failures"]))

    def test_post_start_empty_files_fail_closed(self):
        repo, sdir = self._repo()
        self._write_required(sdir, content="")
        res = gate.check(repo)
        self.assertFalse(res["pass"])
        self.assertTrue(res["pooled_audit"]["required"])
        self.assertTrue(res["pooled_audit"]["empty_required_artifacts"])
        self.assertTrue(any(f.startswith("POOLED_AUDIT_ARTIFACTS_EMPTY")
                            for f in res["failures"]))

    def test_post_start_missing_trigger_fails_closed(self):
        repo, sdir = self._repo()
        for prefix, suffix in gate.POOLED_AUDIT_REQUIRED:
            if prefix == "trigger_check_":
                continue
            name_prefix = prefix.replace("fclr_pooled_audit_", "fclr_pooled_audit001_", 1)
            (sdir / f"{name_prefix}20261122T120000Z{suffix}").write_text("x")
        res = gate.check(repo)
        self.assertFalse(res["pass"])
        self.assertTrue(any(f.startswith("POOLED_AUDIT_TRIGGER_CHECK_MISSING")
                            for f in res["failures"]))

    def test_post_start_full_package_passes(self):
        repo, sdir = self._repo()
        self._write_required(sdir)
        res = gate.check(repo)
        self.assertTrue(res["pass"], res["failures"])
        self.assertTrue(res["pooled_audit"]["pass"])
        self.assertEqual(res["pooled_audit"]["artifact_family"], "pooled_audit001")

    def test_pre_start_session_is_grandfathered(self):
        repo, sdir = self._repo(latest_sid="session_20261122T092003Z")
        # Seed the completed pooled session with generic new-style heavy work so
        # the test isolates the pooled-audit contract under test.
        (sdir / "evidence_audit_20261122T092003Z.json").write_text("{}")
        (sdir / "independent_recompute_20261122T092003Z.json").write_text("{}")
        res = gate.check(repo)
        self.assertFalse(res["pooled_audit"]["required"])
        self.assertTrue(res["pass"], res["failures"])

    def test_generic_recompute_and_audit_do_not_satisfy_contract(self):
        repo, sdir = self._repo()
        (sdir / "evidence_audit_20261122T120000Z.json").write_text("{}")
        (sdir / "independent_recompute_20261122T120000Z.json").write_text("{}")
        (sdir / "trigger_check_20261122T120000Z.json").write_text("{}")
        res = gate.check(repo)
        self.assertFalse(res["pass"])
        self.assertTrue(res["pooled_audit"]["required"])
        self.assertTrue(any(f.startswith("POOLED_AUDIT_ARTIFACTS_MISSING")
                            for f in res["failures"]))


class TestHandoffGateCliContract(unittest.TestCase):
    def test_cli_json_pass_shape_includes_pooled_audit(self):
        import subprocess
        out = subprocess.run(
            [sys.executable, str(REAL / "scripts" / "check_handoff_heavywork_gate.py"), "--json"],
            capture_output=True, text=True,
        )
        self.assertEqual(out.returncode, 0, out.stderr)
        payload = json.loads(out.stdout)
        for k in ("pass", "reason_code", "network", "writes_real_research_state",
                  "read_only", "failures", "pooled_audit"):
            self.assertIn(k, payload)
        self.assertFalse(payload["network"])
        self.assertFalse(payload["writes_real_research_state"])
        self.assertTrue(payload["read_only"])
        self.assertTrue(payload["pass"])


if __name__ == "__main__":
    unittest.main()