#!/usr/bin/env python3
"""FCLR-POOLED-ROBUST-002 gate regression.

tmp-isolated, read-only, no network, no parquet/outcome reads, no real
research_state writes.

FCLR-POOLED-AUDIT-001 (the RESEARCH_PROMPT.md §10 priority-8 adversarial audit)
found concrete, disclosed quality gaps that could have manufactured OR masked the
FCLR-POOLED-001 NOT_SUPPORTED null: d2 only a 1-hour train/test gap (no 48h
purge+embargo), d10 overlapping forward outcomes (pairwise Jaccard 0.52..0.92
dependence), d4 6.8% of rows above the 1% mark/index tolerance, d6/d7
delisting/survivorship, d9 threshold drift. The prior handoff told future agents
to "verify green and stop" — an inefficient escape hatch that would let the null
stand without ever testing whether it survives a leakage-hardened design.

These tests pin the invariant that once FCLR-POOLED-ROBUST-002 starts, a
post-start session cannot satisfy the heavy-work gate with a trigger-only,
prose-only, audit-only, verify-and-stop, or arbitrary recompute_* session. It
must emit the outcome-blind robustness prereg, the heavy robustness recompute
triad, the independent stdlib recompute, the evidence audit, the gate-critical
evidence_audit_ alias, and a trigger check, with no zero-byte placeholders.
Sessions predating the campaign start are grandfathered so the handoff refresh
that first announces the campaign stays green.
"""
from __future__ import annotations

import shutil
import sys
import tempfile
import unittest
from pathlib import Path

REAL = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REAL / "scripts"))

import check_handoff_heavywork_gate as gate  # noqa: E402


class TestPooledRobust002CampaignGate(unittest.TestCase):
    START = "20261122T180000Z"

    def _repo(self, latest_sid="session_20261122T190000Z"):
        tmp = Path(tempfile.mkdtemp(prefix="fclr147pr_"))
        self.addCleanup(shutil.rmtree, tmp, ignore_errors=True)
        repo = tmp / "repo"
        sdir = repo / "research_state" / latest_sid
        sdir.mkdir(parents=True)
        (repo / "AGENT_HANDOFF.md").write_text(
            "# AGENT HANDOFF\n\n## INITIAL TASK MESSAGE FOR NEXT AGENTIC WORK SESSION\n"
            f"Campaign FCLR-POOLED-ROBUST-002-{self.START}\n"
            f"Latest session: research_state/{latest_sid}/\n"
        )
        return repo, sdir

    def _touch(self, sdir, name, body="x"):
        (sdir / name).write_text(body)

    def _base_general_heavy(self, sdir):
        # Satisfy the generic new-style heavy check (evidence audit + fresh quant)
        # so only the robust-002 contract is under test.
        self._touch(sdir, "evidence_audit_20261122T190000Z.json", "{}")
        self._touch(sdir, "trigger_check_20261122T190000Z.json", "{}")

    def test_post_start_missing_robust_fails_closed(self):
        repo, sdir = self._repo()
        self._base_general_heavy(sdir)
        # A generic recompute_* / audit-only / verify-and-stop session.
        self._touch(sdir, "recompute_generic_x.json", "{}")
        res = gate.check(repo)
        self.assertFalse(res["pass"])
        self.assertTrue(res["pooled_robust_02"]["required"])
        self.assertTrue(res["pooled_robust_02"]["missing_required_artifacts"])
        self.assertTrue(any(f.startswith("POOLED_ROBUST_ARTIFACTS_MISSING")
                            for f in res["failures"]))

    def test_post_start_full_robust_set_passes(self):
        repo, sdir = self._repo()
        self._base_general_heavy(sdir)
        utc = "20261122T190000Z"
        for name in (
            f"fclr_pooled_robust002_prereg_{utc}.json",
            f"fclr_pooled_robust002_prereg_{utc}.md",
            f"fclr_pooled_robust002_robustness_{utc}.py",
            f"fclr_pooled_robust002_robustness_{utc}.json",
            f"fclr_pooled_robust002_robustness_{utc}.md",
            f"fclr_pooled_robust002_recompute_{utc}.py",
            f"fclr_pooled_robust002_recompute_{utc}.json",
            f"fclr_pooled_robust002_evidence_audit_{utc}.json",
            f"fclr_pooled_robust002_evidence_audit_{utc}.md",
        ):
            self._touch(sdir, name, "{}")
        res = gate.check(repo)
        self.assertTrue(res["pass"], res["failures"])
        self.assertTrue(res["pooled_robust_02"]["pass"])

    def test_zero_byte_robust_artifact_fails_closed(self):
        repo, sdir = self._repo()
        self._base_general_heavy(sdir)
        utc = "20261122T190000Z"
        for name in (
            f"fclr_pooled_robust002_prereg_{utc}.json",
            f"fclr_pooled_robust002_prereg_{utc}.md",
            f"fclr_pooled_robust002_robustness_{utc}.py",
            f"fclr_pooled_robust002_robustness_{utc}.json",
            f"fclr_pooled_robust002_robustness_{utc}.md",
            f"fclr_pooled_robust002_recompute_{utc}.py",
            f"fclr_pooled_robust002_recompute_{utc}.json",
            f"fclr_pooled_robust002_evidence_audit_{utc}.json",
            f"fclr_pooled_robust002_evidence_audit_{utc}.md",
        ):
            self._touch(sdir, name, "")
        res = gate.check(repo)
        self.assertFalse(res["pass"])
        self.assertTrue(res["pooled_robust_02"]["empty_required_artifacts"])
        self.assertTrue(any(f.startswith("POOLED_ROBUST_ARTIFACTS_EMPTY")
                            for f in res["failures"]))

    def test_missing_trigger_check_fails_closed(self):
        repo, sdir = self._repo()
        utc = "20261122T190000Z"
        for name in (
            f"fclr_pooled_robust002_prereg_{utc}.json",
            f"fclr_pooled_robust002_prereg_{utc}.md",
            f"fclr_pooled_robust002_robustness_{utc}.py",
            f"fclr_pooled_robust002_robustness_{utc}.json",
            f"fclr_pooled_robust002_robustness_{utc}.md",
            f"fclr_pooled_robust002_recompute_{utc}.py",
            f"fclr_pooled_robust002_recompute_{utc}.json",
            f"fclr_pooled_robust002_evidence_audit_{utc}.json",
            f"fclr_pooled_robust002_evidence_audit_{utc}.md",
        ):
            self._touch(sdir, name, "{}")
        # No evidence_audit_/trigger_check_ at all -> both generic heavy and the
        # robust trigger check fail.
        res = gate.check(repo)
        self.assertFalse(res["pass"])
        self.assertTrue(res["pooled_robust_02"]["required"])
        self.assertFalse(res["pooled_robust_02"]["has_trigger_check"])
        self.assertTrue(any(f.startswith("POOLED_ROBUST_TRIGGER_CHECK_MISSING")
                            for f in res["failures"]))

    def test_pre_start_session_is_grandfathered(self):
        repo, sdir = self._repo(latest_sid="session_20261122T170000Z")
        self._base_general_heavy(sdir)
        self._touch(sdir, "recompute_generic_x.json", "{}")
        res = gate.check(repo)
        self.assertFalse(res["pooled_robust_02"]["required"])
        self.assertTrue(res["pass"], res["failures"])


if __name__ == "__main__":
    unittest.main()