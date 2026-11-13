#!/usr/bin/env python3
"""Guard against the false "nothing executable" closure.

Regression tests for scripts/next_campaign_status.py. The 2024q4 cell sat frozen
and unexecuted across several sessions because its prereg was never matched to an
evaluation artifact. These tests pin that detection.
"""
from __future__ import annotations

import importlib.util
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def _load():
    spec = importlib.util.spec_from_file_location(
        "next_campaign_status", ROOT / "scripts" / "next_campaign_status.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


class TestNextCampaignStatus(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.mod = _load()

    def test_tokens_are_distinctive(self):
        t = self.mod._tokens("FCLR-FWD-VOL-2024Q4-CROSS-20261113T091500Z")
        self.assertIn("2024Q4", t)
        self.assertIn("CROSS", t)

    def test_every_frozen_prereg_is_classified(self):
        st = self.mod.prereg_status()
        self.assertTrue(st["preregs"], "no preregs found")
        for r in st["preregs"]:
            self.assertIn("actionable_now", r)
            self.assertIsInstance(r["has_evaluation_artifact"], bool)

    def test_executed_cells_are_not_actionable(self):
        """Every cell executed this repository must not be re-proposed as pending."""
        st = self.mod.prereg_status()
        by_exp = {r["experiment_id"]: r for r in st["preregs"]}
        for exp in ("FCLR-FWD-VOL-2024Q4-CROSS-20261113T091500Z",
                    "FCLR-FWD-VOL-2025-CROSS-20261113T063000Z",
                    "FCLR-FWD-VOL-011-CONFIRM-20261113T041200Z"):
            self.assertIn(exp, by_exp, f"{exp} prereg missing")
            self.assertFalse(by_exp[exp]["actionable_now"],
                             f"{exp} executed but reported actionable")
            self.assertTrue(by_exp[exp]["has_evaluation_artifact"],
                            f"{exp} executed but artifact not detected")

    def test_no_actionable_prereg_while_cells_remain_terminal(self):
        """Fails loudly if a genuinely unexecuted prereg reappears undetected."""
        st = self.mod.prereg_status()
        actionable = [r["experiment_id"] for r in st["preregs"] if r["actionable_now"]]
        self.assertEqual(actionable, [],
                         f"unexecuted frozen preregs need attention: {actionable}")

    def test_funding_backed_months_are_detected(self):
        windows = {w["month"]: w for w in self.mod.ready_windows()}
        # 2025-07..2025-10 are complete, funding-backed and never tested.
        for m in ("2025-07", "2025-08", "2025-09", "2025-10"):
            self.assertIn(m, windows)
            self.assertTrue(windows[m]["funding_available"], f"{m} funding not detected")
            self.assertFalse(windows[m]["inside_tested_window"],
                             f"{m} wrongly marked tested")

    def test_pre_funding_months_flagged(self):
        windows = {w["month"]: w for w in self.mod.ready_windows()}
        self.assertFalse(windows["2024-01"]["funding_available"],
                         "2024-01 has no funding but was reported funded")


if __name__ == "__main__":
    unittest.main()