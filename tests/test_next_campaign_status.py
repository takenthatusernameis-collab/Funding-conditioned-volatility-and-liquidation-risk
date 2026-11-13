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
        # 2025-07..2025-10 are complete, funding-backed and now inside Cell 6's
        # tested window (FCLR-FWD-VOL-2025H2-CROSS, executed 2026-11-13T10:22:40Z).
        for m in ("2025-07", "2025-08", "2025-09", "2025-10"):
            self.assertIn(m, windows)
            self.assertTrue(windows[m]["funding_available"], f"{m} funding not detected")
            self.assertTrue(windows[m]["inside_tested_window"],
                            f"{m} wrongly marked untested")
            self.assertEqual(windows[m]["tested_by"],
                             "FCLR-FWD-VOL-2025H2-CROSS (NOT_REPLICATED)")

    def test_pre_funding_months_flagged(self):
        windows = {w["month"]: w for w in self.mod.ready_windows()}
        self.assertFalse(windows["2024-01"]["funding_available"],
                         "2024-01 has no funding but was reported funded")

    def test_2026q1q2_window_marked_tested(self):
        """The FCLR-FWD-VOL-2025Q1Q2-CROSS test months must not be re-proposed."""
        windows = {w["month"]: w for w in self.mod.ready_windows()}
        for m in ("2026-01", "2026-02", "2026-03", "2026-04"):
            self.assertIn(m, windows)
            self.assertTrue(windows[m]["inside_tested_window"],
                            f"{m} wrongly marked untested after 2025Q1Q2 cell")
            self.assertEqual(windows[m]["tested_by"],
                             "FCLR-FWD-VOL-2025Q1Q2-CROSS (NOT_REPLICATED)")

    def test_no_ready_run_is_feasible_for_full_design(self):
        """The remaining READY months must not be reported as a full-design run.

        A 3-block pre-registered design needs >=127 contiguous days. After the
        2025Q1Q2 cell consumed 2026-01..2026-04, no contiguous READY run is long
        enough; the tool must say so instead of the old blanket 'executable'.
        """
        feas = self.mod.design_feasible_months(self.mod.ready_windows())
        self.assertFalse(feas["any_feasible"],
                         f"a ready run was called feasible: {feas['runs']}")
        for r in feas["runs"]:
            self.assertLess(r["span_days"], feas["min_design_days"])
            self.assertFalse(r["feasible"])

    def test_feasibility_logic_detects_a_long_run(self):
        """Guard the feasibility rule itself with a synthetic contiguous run."""
        rows = [{"month": m, "funding_available": True, "inside_tested_window": False}
                for m in ("2025-01", "2025-02", "2025-03", "2025-04", "2025-05")]
        feas = self.mod.design_feasible_months(rows)
        self.assertTrue(feas["any_feasible"])
        self.assertTrue(feas["runs"][0]["feasible"])

    def test_hyperliquid_bulk_frontier_detects_forward_window(self):
        """The real frontier: 2026-01-18..2026-04-30 must be surfaced as forward-feasible.

        Regression guard for the false 'cache exhausted' closure: the old tool
        only modelled the Binance 5-symbol design and declared the campaign
        exhausted while an untouched 103-day Hyperliquid region with observed
        liquidation labels sat cached.
        """
        bulk = self.mod.bulk_frontier()
        self.assertTrue(any(d for d in bulk["present"].values()),
                        "ironflow bulk cache should be present on disk")
        self.assertTrue(bulk["any_forward_feasible"],
                        f"untouched Hyperliquid forward window not detected: {bulk['runs']}")
        fwd = [r for r in bulk["runs"] if r["feasible_forward"]]
        self.assertTrue(fwd)
        self.assertGreaterEqual(fwd[0]["span_days"],
                                self.mod.MIN_FORWARD_DESIGN_DAYS)
        self.assertEqual(fwd[0]["start"], "2026-01-18")
        self.assertEqual(fwd[0]["end"], "2026-04-30")

    def test_bulk_tested_window_is_excluded(self):
        """Arm B's scored region (through 2026-01-17) must not count as untouched."""
        bulk = self.mod.bulk_frontier()
        for r in bulk["runs"]:
            # No run may start inside the tested window and run past it.
            self.assertFalse(
                r["start"] <= "2026-01-17" and r["end"] >= "2026-01-17",
                f"run overlaps tested Arm B region: {r}",
            )
        # The forward region must begin strictly after the tested boundary.
        fwd = [r for r in bulk["runs"] if r["feasible_forward"]]
        self.assertTrue(fwd)
        self.assertGreater(fwd[0]["start"], "2026-01-17")

    def test_campaign_status_message_distinguishes_domains(self):
        """The Binance exhaustion message must not claim the whole campaign is dead."""
        feasibility = self.mod.design_feasible_months(self.mod.ready_windows())
        bulk = self.mod.bulk_frontier()
        self.assertFalse(feasibility["any_feasible"])
        # Even with Binance exhausted, the bulk domain keeps the campaign alive.
        self.assertTrue(bulk["any_forward_feasible"])


if __name__ == "__main__":
    unittest.main()