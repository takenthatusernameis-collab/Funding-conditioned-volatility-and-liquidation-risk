#!/usr/bin/env python3
"""Guard the active FULLHIST/XSEC campaign against a false terminal closure.

The two preregs frozen at 2026-11-12T20:15:36Z are admissible and unexecuted.
While their outcome artifacts are absent, the frontier must keep the campaign at
rank-0 and must not present a CLOSED_TERMINAL program state.
"""
from __future__ import annotations

import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RS = ROOT / "research_state"
CAMPAIGN = "FCLR-FULLHISTORY-VOL-LIQ-20261112T201536Z"
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


class TestActiveCampaignGate(unittest.TestCase):
    def test_preregs_frozen_and_unexecuted(self):
        for exp, fn in PREREGS.items():
            p = json.loads((RS / fn).read_text())
            self.assertEqual(p["experiment_id"], exp)
            self.assertEqual(p["status"], "FROZEN_PRE_OUTCOMES")
            self.assertTrue(p["frozen_before_outcomes"])
            self.assertFalse(p["outcome_data_inspected_before_freeze"])

    def test_frontier_rank0_is_active_campaign_while_outcomes_absent(self):
        frontier = json.loads((RS / "experiment_frontier.json").read_text())
        outcomes_exist = any(list(RS.glob(g + "*.json")) for g in EVAL_GLOBS)
        rank0 = [e for e in frontier if e.get("rank") == 0]
        self.assertEqual(len(rank0), 1, f"expected exactly one rank-0 entry, got {len(rank0)}")
        for e in rank0:
            self.assertNotEqual(
                e.get("status"), "CLOSED_TERMINAL",
                "rank-0 must not be CLOSED_TERMINAL while the frozen preregs are unexecuted",
            )
        if not outcomes_exist:
            self.assertEqual(rank0[0].get("task"), CAMPAIGN)

    def test_registry_has_both_nonterminal_hypotheses(self):
        reg = json.loads((RS / "hypothesis_registry.json").read_text())
        by_id = {h["id"]: h for h in reg["hypotheses"]}
        for hid in HYPOTHESES:
            self.assertIn(hid, by_id)
            self.assertFalse(
                by_id[hid].get("terminal", False),
                f"{hid} must stay non-terminal until its evaluation artifact exists",
            )


if __name__ == "__main__":
    unittest.main()