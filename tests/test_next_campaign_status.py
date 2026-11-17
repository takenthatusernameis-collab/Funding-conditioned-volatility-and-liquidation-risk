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

    def test_disjoint_campaign_is_executed(self):
        """The frozen 2025 disjoint campaign is executed (not actionable)."""
        st = self.mod.prereg_status()
        by_exp = {r["experiment_id"]: r for r in st["preregs"]}
        exp = "FCLR-FWD-VOL-2025-DISJOINT-CROSS-20261114T183000Z"
        self.assertIn(exp, by_exp, f"{exp} prereg missing")
        self.assertTrue(by_exp[exp]["frozen_before_outcomes"])
        self.assertFalse(by_exp[exp]["outcomes_inspected_before_freeze"])
        self.assertTrue(by_exp[exp]["has_evaluation_artifact"])
        self.assertFalse(by_exp[exp]["actionable_now"])

    def test_terminal_preregs_are_not_actionable(self):
        """Executed/terminal cells must not be re-proposed as pending."""
        st = self.mod.prereg_status()
        by_exp = {r["experiment_id"]: r for r in st["preregs"]}
        for exp in ("FCLR-FWD-VOL-2024Q4-CROSS-20261113T091500Z",
                    "FCLR-FWD-VOL-2025-CROSS-20261113T063000Z",
                    "FCLR-FWD-VOL-011-CONFIRM-20261113T041200Z",
                    "FCLR-FWD-VOL-2025Q1Q2-CROSS-20261113T111601Z"):
            self.assertIn(exp, by_exp, f"{exp} prereg missing")
            self.assertFalse(by_exp[exp]["actionable_now"],
                             f"{exp} terminal but reported actionable")
            self.assertTrue(by_exp[exp]["has_evaluation_artifact"],
                            f"{exp} terminal but artifact not detected")

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

    def test_disjoint_campaign_months_are_marked_tested(self):
        """Executed disjoint test months must not be re-proposed as fresh blocks.

        2025-06/2025-11/2025-12 were consumed by the sealed 2025 disjoint cross
        (EXPLORATORY_NULL); 2024-06 was consumed by the singleton estimator
        diagnostic (EXPLAINED_BY_ESTIMATOR). The frontier must report them as
        tested, not executable, to prevent duplicate sealed-cell work.
        """
        windows = {w["month"]: w for w in self.mod.ready_windows()}
        frontier = self.mod.disjoint_block_frontier(self.mod.ready_windows())
        feasible = {b["month"]: b for b in frontier["feasible_blocks"]}
        for m in ("2024-06", "2025-06", "2025-11", "2025-12"):
            self.assertIn(m, windows, f"{m} missing from cache inventory")
            self.assertTrue(windows[m]["inside_tested_window"],
                            f"{m} executed but wrongly marked untested")
            self.assertIn("DISJOINT", windows[m]["tested_by"] or "",
                          f"{m} lacks executed-cell attribution: {windows[m]}")
            self.assertNotIn(m, feasible,
                             f"{m} executed but re-proposed as feasible: {feasible}")
        self.assertGreaterEqual(frontier["n_feasible"], 0)
        self.assertFalse(frontier["campaign_feasible"])

    def test_nested_csv_layout_is_counted(self):
        """A deeper CSV nesting must not make a complete month look empty."""
        import tempfile
        old_cache = self.mod.CACHE
        try:
            with tempfile.TemporaryDirectory() as td:
                self.mod.CACHE = Path(td)
                base = Path(td) / "BTCUSDT_2025_06"
                for kind in self.mod.KINDS:
                    day = base / f"{kind}-2025-06-01" / "nested" / "deeper"
                    day.mkdir(parents=True)
                    for i in range(30):
                        (day / f"BTCUSDT-1h-2025-06-{i + 1:02d}.csv").write_text("open_time,close\n")
                counts = self.mod.kline_months("BTCUSDT")
                self.assertEqual(counts["2025-06"]["markPriceKlines"], 30)
                self.assertEqual(counts["2025-06"]["premiumIndexKlines"], 30)
                self.assertEqual(counts["2025-06"]["indexPriceKlines"], 30)
        finally:
            self.mod.CACHE = old_cache

    def test_hyperliquid_bulk_forward_window_now_tested(self):
        """The 2026-01-18..2026-04-30 forward reserve is tested and exhausted.

        TRACKA-LIQ-XSEC-FORWARD (EXPLORATORY_NULL) and TRACKA-VOL-FORWARD
        (EXPLORATORY_NULL/VALID_EXPLORATORY) consumed the region per
        AGENT_HANDOFF 2026-11-14T13:15:35Z, so it must NOT be surfaced as an
        executable forward-feasible frontier. Regression guard against a false
        re-opening of a tested window (the inverse of the old false-closure bug).
        """
        bulk = self.mod.bulk_frontier()
        self.assertTrue(any(d for d in bulk["present"].values()),
                        "ironflow bulk cache should be present on disk")
        self.assertFalse(bulk["any_forward_feasible"],
                         f"tested forward window must not be forward-feasible: {bulk['runs']}")
        fwd = [r for r in bulk["runs"] if r["feasible_forward"]]
        self.assertEqual(fwd, [], f"no forward-feasible run may remain: {fwd}")
        self.assertFalse(bulk["any_feasible"])

    def test_bulk_tested_window_is_excluded(self):
        """Arm B's scored region (through 2026-01-17) must not count as untouched."""
        bulk = self.mod.bulk_frontier()
        # With Arm B (through 2026-01-17) and the forward reserve
        # (2026-01-18..2026-04-30) both tested, no run may be feasible or
        # forward-feasible. The only possible residual is the short pre-burn-in
        # prefix (2025-05-01..2025-05-24), which is far below design minimum.
        for r in bulk["runs"]:
            self.assertFalse(r["feasible"], f"run wrongly feasible: {r}")
            self.assertFalse(r["feasible_forward"], f"run wrongly forward-feasible: {r}")
            self.assertLess(r["span_days"], self.mod.MIN_FORWARD_DESIGN_DAYS)
        self.assertFalse(bulk["any_feasible"])
        self.assertFalse(bulk["any_forward_feasible"])
        for r in bulk["runs"]:
            self.assertFalse(
                r["start"] <= "2026-01-17" and r["end"] >= "2026-01-17",
                f"run overlaps tested Arm B region: {r}",
            )

    def test_campaign_status_message_distinguishes_domains(self):
        """All three sources of fresh 3-block work are now exhausted.

        The old contiguous-only check said no heavy work remained; the disjoint
        frontier then reopened already-tested months. Both bugs are fixed: the
        status must report no feasible contiguous, disjoint, or Hyperliquid run.
        Bounded cached-panel audits may remain, but they are not 3-block cells.
        """
        feasibility = self.mod.design_feasible_months(self.mod.ready_windows())
        disjoint = self.mod.disjoint_block_frontier(self.mod.ready_windows())
        bulk = self.mod.bulk_frontier()
        self.assertFalse(feasibility["any_feasible"])
        self.assertFalse(bulk["any_feasible"])
        self.assertFalse(bulk["any_forward_feasible"])
        self.assertFalse(disjoint["campaign_feasible"])
        self.assertGreaterEqual(disjoint["n_feasible"], 0)

    def test_extended_frontier_excludes_fclr011_tested_windows(self):
        """FCLR-011 (2026-05-08..2026-08-06) + FWD-VOL-011-CONFIRM forward
        (2026-08-03..2026-10-31) consume 2026-05-01..2026-10-31 in the extended
        Hyperliquid stores too. Before the fix, BULK_TESTED_WINDOWS listed only the
        two ironflow ranges, so hl_extended_frontier() wrongly surfaced
        2026-05-01..2026-10-31 (184d) as FEASIBLE phantom heavy work, contradicting
        AGENT_HANDOFF's 'no feasible 3-block design in ANY domain'. Guard against a
        re-opening of an already-tested window (inverse of the old false-closure bug).
        """
        hl = self.mod.hl_extended_frontier()
        for r in hl["runs"]:
            # No run may overlap the consumed 2026-05-08..2026-10-31 region.
            overlaps = not (r["end"] < "2026-05-08" or r["start"] > "2026-10-31")
            self.assertFalse(
                overlaps and r["span_days"] >= self.mod.MIN_FORWARD_DESIGN_DAYS,
                f"phantom feasible run over tested FCLR-011 windows: {r}",
            )
            self.assertFalse(r["feasible"], f"run wrongly feasible: {r}")
            self.assertFalse(r["feasible_forward"], f"run wrongly forward-feasible: {r}")
        self.assertFalse(hl["any_feasible"])
        self.assertFalse(hl["any_forward_feasible"])

    def test_bulk_tested_windows_cover_fclr011(self):
        """The FCLR-011 + forward-walk Binance windows must be registered so no
        domain re-proposes them as untouched."""
        covered = [(a, b) for (a, b, _lbl) in self.mod.BULK_TESTED_WINDOWS]
        # A window starting on/before 2026-05-08 and ending on/after 2026-08-06.
        self.assertTrue(
            any(a <= "2026-05-08" and b >= "2026-08-06" for (a, b) in covered),
            f"FCLR-011 test window not covered: {covered}",
        )
        # A window covering the forward walk through 2026-10-31.
        self.assertTrue(
            any(a <= "2026-08-03" and b >= "2026-10-31" for (a, b) in covered),
            f"forward-walk window not covered: {covered}",
        )

    def test_markfund_frontier_reproduces_certified_closed_verdict(self):
        """The mark+funding-only frontier must reproduce the closed verdict:
        no >=3-block design can be frozen.

        FCLR-LEDGER-INTEGRITY-01 (2026-11-17T234500Z): FCLR-003's sealed
        NEGATIVE test window (2024-10-02..2024-12-31) was missing from
        TESTED_WINDOWS, so the frontier wrongly listed 2024-10/11/12 as
        "individually feasible". Those are FCLR-003 *test* months (B0/B1/C1
        already scored) and must never be re-proposed. With the ledger fixed,
        the only individually-feasible mark+funding month is 2025-01 (its
        30-day train window is FCLR-003 test, allowed as pre-test history),
        which is a single block < 3, so the campaign is closed. The
        completeness rule is NOT weakened: only mark+funding months with all 5
        symbols covered count.
        """
        mf = self.mod.markfund_frontier()
        self.assertEqual(mf["estimand"], "mark+funding-only")
        self.assertEqual(mf["min_blocks_required"], 3)
        self.assertEqual(mf["n_individually_feasible"], 1)
        self.assertEqual(set(mf["individually_feasible_months"]), {"2025-01"})
        self.assertEqual(mf["max_mutually_non_overlapping"], 1)
        self.assertEqual(mf["non_overlapping_selection"], ["2025-01"])
        self.assertEqual(mf["n_overlapping_pairs"], 0)
        self.assertFalse(mf["campaign_feasible_non_overlapping"])
        self.assertTrue(mf["any_individually_feasible"])
        self.assertFalse(mf["any_contiguous_run_ge_min_design_days"])

    def test_fclr003_sealed_test_months_not_reproposed(self):
        """FCLR-003's sealed NEGATIVE test months (2024-10/11/12) must never be
        re-proposed as fresh blocks. Regression guard for the ledger omission
        fixed in FCLR-LEDGER-INTEGRITY-01: before the fix the frontier listed
        them as individually feasible, inviting a direct re-score of sealed
        data (a §17 violation)."""
        mf = self.mod.markfund_frontier()
        for m in ("2024-10", "2024-11", "2024-12"):
            self.assertNotIn(m, mf["individually_feasible_months"],
                             f"{m} is FCLR-003 sealed test but re-proposed")
            self.assertTrue(self.mod._inside_tested(m),
                            f"{m} (FCLR-003 test) not marked tested: ledger gap")
        windows = {w["month"]: w for w in self.mod.ready_windows()}
        for m in ("2024-10", "2024-11", "2024-12"):
            self.assertTrue(self.mod._inside_tested(m),
                            f"{m} (FCLR-003 test) not marked tested: ledger gap")
            if m in windows:
                self.assertTrue(windows[m]["inside_tested_window"],
                                f"{m} wrongly marked untested")
                self.assertIn("FCLR-003", windows[m]["tested_by"] or "",
                              f"{m} lacks FCLR-003 attribution: {windows[m]}")

    def test_markfund_frontier_excludes_tested_windows(self):
        """Test months inside TESTED_WINDOWS must not be proposed as fresh
        mark+funding-only blocks (prevents duplicate sealed-cell work)."""
        mf = self.mod.markfund_frontier()
        for c in mf["candidate_test_months"]:
            self.assertFalse(c["test_month_inside_tested_window"],
                             f"tested month re-proposed: {c['test_month']}")
            self.assertFalse(self.mod._inside_tested(c["test_month"]),
                             f"tested month leaked into candidates: {c['test_month']}")

    def test_markfund_frontier_non_overlap_selection_is_disjoint(self):
        """The greedy non-overlapping selection must be genuinely pairwise
        non-overlapping on [train_start, test_end] (no cross-block leakage)."""
        from datetime import date
        mf = self.mod.markfund_frontier()
        by_month = {c["test_month"]: c for c in mf["candidate_test_months"]}
        sel = mf["non_overlapping_selection"]
        windows = [(date.fromisoformat(by_month[m]["train_start"]),
                    date.fromisoformat(by_month[m]["test_end"]))
                   for m in sel]
        for i in range(len(windows)):
            for j in range(i + 1, len(windows)):
                a, b = windows[i], windows[j]
                self.assertFalse(
                    max(a[0], b[0]) <= min(a[1], b[1]),
                    f"selection blocks overlap: {sel[i]} vs {sel[j]}",
                )

    def test_markfund_frontier_in_json_output(self):
        """--json must expose the markfund_frontier key with the closed verdict."""
        import json
        import subprocess
        import sys
        out = subprocess.run(
            [sys.executable, str(self.mod.REPO / "scripts"
             / "next_campaign_status.py"), "--json"],
            capture_output=True, text=True, check=True,
        ).stdout
        data = json.loads(out)
        self.assertIn("markfund_frontier", data)
        mf = data["markfund_frontier"]
        self.assertEqual(mf["n_individually_feasible"], 1)
        self.assertEqual(mf["max_mutually_non_overlapping"], 1)
        self.assertFalse(mf["campaign_feasible_non_overlapping"])


if __name__ == "__main__":
    unittest.main()