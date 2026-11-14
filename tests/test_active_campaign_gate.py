#!/usr/bin/env python3
"""Guard the FULLHIST/XSEC campaign against a false terminal closure.

The two preregs frozen at 2026-11-12T20:15:36Z are admissible and were executed
at 2026-11-13T00:xx:xxZ, producing timestamped evaluation artifacts. The preregs
themselves remain FROZEN_PRE_OUTCOMES (never mutated); the hypotheses they feed
are now terminal with verdicts, and the frontier reflects completion.

If either evaluation artifact is ever deleted, this test must fail loudly so
the campaign cannot silently revert to a CLOSED_TERMINAL state.
"""
from __future__ import annotations

import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RS = ROOT / "research_state"
# Rank-0 advances as phases close, so this guard must not pin a campaign id.
# It pins the *invariant*: exactly one rank-0 entry, it is ACTIVE with a concrete
# unfinished task and a phase list, and every completed campaign stays demoted.
ACTIVE_CAMPAIGN_ID_PREFIX = "FCLR-"
COMPLETED_STATUSES = {
    "COMPLETED_VALIDATED",
    "SUPERSEDED_TERMINAL",
    "SUPERSEDED_BY_FCLR_HEAVY_CONFIRM",
    "SUPERSEDED",
}
# Active (non-terminal) rank-0 states. The campaign legitimately alternates between
# READY_EXECUTE (an agent-removable heavy cell is open) and TRIGGER_ONLY (all cached
# data is exhausted and the only path forward is an external material trigger). Both
# are active, both carry a concrete unfinished task, and neither may be terminal.
ACTIVE_STATUSES = {"READY_EXECUTE", "TRIGGER_ONLY"}
PREREGS = {
    "TRACKA-VOL-FULLHIST-20261112T201536Z": "prereg_tracka_vol_fullhist_20261112T201536Z.json",
    "TRACKA-LIQ-XSEC-20261112T201536Z": "prereg_tracka_liq_xsec_20261112T201536Z.json",
}
EVAL_GLOBS = (
    "evaluation_summary_TRACKA-VOL-FULLHIST-",
    "evaluation_summary_TRACKA-LIQ-XSEC-",
)
HYPOTHESES = (
    "H_tracka_hl_funding_conditioned_volatility_fullhistory",
    "H_tracka_hl_liquidation_cross_sectional_funding",
)
EXPECTED_VERDICTS = {
    "H_tracka_hl_funding_conditioned_volatility_fullhistory": {
        "terminal": True,
        "terminal_class": "NOT_MET",
        "experiment_id": "TRACKA-VOL-FULLHIST-20261112T201536Z",
    },
    "H_tracka_hl_liquidation_cross_sectional_funding": {
        "terminal": True,
        "terminal_class": "EXPLORATORY_NULL",
        "experiment_id": "TRACKA-LIQ-XSEC-20261112T201536Z",
    },
}


class TestActiveCampaignGate(unittest.TestCase):
    def test_preregs_remain_frozen(self):
        for exp, fn in PREREGS.items():
            p = json.loads((RS / fn).read_text())
            self.assertEqual(p["experiment_id"], exp)
            self.assertEqual(p["status"], "FROZEN_PRE_OUTCOMES")
            self.assertTrue(p["frozen_before_outcomes"])
            self.assertFalse(p["outcome_data_inspected_before_freeze"])

    def test_evaluation_artifacts_exist_for_both_arms(self):
        for g in EVAL_GLOBS:
            hits = sorted(RS.glob(g + "*.json"))
            self.assertTrue(hits, f"missing evaluation artifact for {g}")
            for h in hits:
                self.assertTrue(h.stat().st_size > 0, f"empty artifact {h}")

    def test_frontier_rank0_is_active_heavy_campaign(self):
        frontier = json.loads((RS / "experiment_frontier.json").read_text())
        rank0 = [e for e in frontier if e.get("rank") == 0]
        self.assertEqual(len(rank0), 1, f"expected exactly one rank-0 entry, got {len(rank0)}")
        e = rank0[0]
        # The active campaign advances as phases close. Rank 0 must be the
        # current heavy campaign and must carry a concrete unfinished task.
        self.assertTrue(str(e.get("task", "")).startswith(ACTIVE_CAMPAIGN_ID_PREFIX))
        self.assertNotIn(e.get("status"), COMPLETED_STATUSES,
                         "rank-0 must never hold a completed/superseded campaign")
        self.assertIn(e.get("status"), ACTIVE_STATUSES,
                      "rank-0 must hold an active (non-terminal) status: READY_EXECUTE or TRIGGER_ONLY")
        self.assertIn(e.get("program_status"), {"ACTIVE", "BOUNDED_TRIGGER_ONLY"},
                      "rank-0 program_status must be ACTIVE or BOUNDED_TRIGGER_ONLY")
        self.assertTrue(e.get("next_unfinished_task"))
        self.assertTrue(e.get("phases"))
        # Every other campaign must be demoted, not deleted.
        others = [x for x in frontier if x.get("rank") != 0]
        self.assertTrue(others, "completed campaigns must be retained, not deleted")
        for x in others:
            self.assertIn(x.get("status"), COMPLETED_STATUSES,
                          f"non-rank-0 entry {x.get('task')} must carry a terminal status")

    def test_prior_campaign_prereg_remains_frozen(self):
        p = json.loads((RS / "prereg_fclr_fwd_vol_011_confirm_20261113T041200Z.json").read_text())
        self.assertEqual(p["status"], "FROZEN_PRE_OUTCOMES")
        self.assertTrue(p["frozen_before_outcomes"])
        self.assertFalse(p["outcome_data_inspected_before_freeze"])

    def test_registry_hypotheses_are_terminal_with_verdicts(self):
        reg = json.loads((RS / "hypothesis_registry.json").read_text())
        by_id = {h["id"]: h for h in reg["hypotheses"]}
        for hid, expect in EXPECTED_VERDICTS.items():
            self.assertIn(hid, by_id, f"{hid} missing from registry")
            h = by_id[hid]
            self.assertTrue(h.get("terminal", False),
                            f"{hid} must be terminal after its evaluation artifact exists")
            self.assertEqual(h.get("terminal_class"), expect["terminal_class"],
                             f"{hid} terminal_class mismatch")
            self.assertEqual(h.get("experiment_id"), expect["experiment_id"])
            self.assertIsNotNone(h.get("last_verdict"),
                                 f"{hid} must record a last_verdict")


if __name__ == "__main__":
    unittest.main()