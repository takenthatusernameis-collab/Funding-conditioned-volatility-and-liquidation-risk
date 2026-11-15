#!/usr/bin/env python3
"""Tests for FCLR-NEXT-002 power/MDE calibration (scripts/fclr_power_calibration.py)."""
from __future__ import annotations

import json
import math
import unittest
from pathlib import Path

import sys
REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "scripts"))
import fclr_power_calibration as cal  # noqa: E402

RS = REPO / "research_state"
OUT_UTC = "2026-11-15T01:34:12Z"
PREREG = RS / f"prereg_fclr_power_calibration_{OUT_UTC}.json"

VOL_CI_LO = -0.01310391699674236
VOL_CI_HI = 0.0279375456196109
VOL_SE = 0.010469953259366775  # from persisted corrected-audit CI
LIQ_Q5 = -0.020772393084283722
LIQ_Q95 = 0.01899805497678097
LIQ_SE = (LIQ_Q95 - LIQ_Q5) / (2 * cal.Z_95)


class TestAnalyticSEAndMDE(unittest.TestCase):
    def test_vol_h24_se_from_persisted_ci(self):
        se = cal.analytic_se_from_ci(VOL_CI_LO, VOL_CI_HI)
        self.assertAlmostEqual(se, VOL_SE, places=12)

    def test_liq_pooled_se(self):
        se = (LIQ_Q95 - LIQ_Q5) / (2 * cal.Z_95)
        self.assertAlmostEqual(se, LIQ_SE, places=12)

    def test_mde80_arithmetic(self):
        se = VOL_SE
        self.assertAlmostEqual(cal.MDE80_FACTOR * se, cal.MDE80_FACTOR * VOL_SE, places=12)
        self.assertAlmostEqual(cal.MDE80_FACTOR * se, 0.02933246628577565, places=12)

    def test_vol_floor_and_power(self):
        md = 0.006923170805123592
        rel = -1.9633752428119808
        floor = cal.vol_floor_abs(md, rel, 0.02)
        baseline = abs(md) / (abs(rel) / 100.0)
        self.assertAlmostEqual(baseline, 0.35261577380430364, places=10)
        self.assertAlmostEqual(floor, 0.007052315476086073, places=12)
        se = cal.analytic_se_from_ci(VOL_CI_LO, VOL_CI_HI)
        pwr = cal.power_two_sided(floor, se)
        # small but > nominal; must be underpowered vs 0.80
        self.assertLess(pwr, 0.20)
        self.assertGreater(pwr, 0.05)
        self.assertEqual(cal.verdict_from_power(pwr), "NULL_UNDERPOWERED")

    def test_liq_power_at_floor(self):
        pwr = cal.power_two_sided(0.05, LIQ_SE)
        self.assertGreater(pwr, 0.98)
        self.assertEqual(cal.verdict_from_power(pwr), "NULL_INFORMATIVE")

    def test_symmetry_flag(self):
        mid = (LIQ_Q5 + LIQ_Q95) / 2.0
        width = LIQ_Q95 - LIQ_Q5
        # mathematically fails 1% check (~2.23%); prereg treats failed symmetry as unstable
        self.assertGreater(abs(mid) / width, 0.01)

    def test_per_block_se_scaling(self):
        pooled_n = 6634
        for n in (2996, 1605, 2033):
            se_b = LIQ_SE * math.sqrt(pooled_n / n)
            self.assertTrue(math.isfinite(se_b) and se_b > LIQ_SE * 0.9)


class TestKnownAnswerAndMissing(unittest.TestCase):
    def test_known_answer_recovery(self):
        ka = cal.known_answer_self_test()
        self.assertTrue(ka["recovered_within_tolerance"])
        self.assertAlmostEqual(ka["se_recovered"], ka["se_true"], places=12)
        self.assertGreater(ka["power_at_true_delta"], 0.80)

    def test_missing_unstable_input_is_inconclusive(self):
        self.assertEqual(cal.verdict_from_power(None), "INCONCLUSIVE")
        self.assertEqual(cal.verdict_from_power(float('nan')), "INCONCLUSIVE")

    def test_vol_floor_missing_when_degenerate(self):
        self.assertIsNone(cal.vol_floor_abs(0.01, 0.0))


class TestNoSealedMutationAndPrereg(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.prereg = json.loads(PREREG.read_text())
        cls.sealed = [cal.VOL_EVAL, cal.VOL_PREREG, cal.VOL_PANEL, cal.LIQ_EVAL, cal.LIQ_PREREG, cal.LIQ_PANEL]
        cls.before = {str(p): cal.sha256_file(p) for p in cls.sealed}

    def test_prereg_frozen(self):
        d = self.prereg
        self.assertEqual(d["status"], "FROZEN_PRE_OUTCOMES")
        self.assertTrue(d["frozen_before_outcomes"])
        self.assertFalse(d["promotable"])
        self.assertEqual(d["max_status"], "EXPLORATORY_ONLY")
        self.assertTrue(d["does_not_reopen_sealed_verdict"])

    def test_sealed_inputs_unchanged(self):
        after = {str(p): cal.sha256_file(p) for p in self.sealed}
        self.assertEqual(after, self.before)

    def test_run_no_write_does_not_mutate_sealed(self):
        out = cal.run(out_utc=OUT_UTC, write=False)
        self.assertFalse(out["sealed_artifacts_mutated"])
        after = {str(p): cal.sha256_file(p) for p in self.sealed}
        self.assertEqual(after, self.before)


class TestEndToEndOutput(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.ej = RS / f"evaluation_summary_FCLR-POWER-CALIBRATION-{OUT_UTC}.json"
        cls.em = RS / f"evaluation_summary_FCLR-POWER-CALIBRATION-{OUT_UTC}.md"

    def test_eval_artifacts_exist_and_consistent(self):
        self.assertTrue(self.ej.exists(), "eval json must exist")
        d = json.loads(self.ej.read_text())
        self.assertEqual(d["status"], "VALID_EXPLORATORY")
        self.assertFalse(d["promotable"])
        self.assertEqual(d["max_status"], "EXPLORATORY_ONLY")
        self.assertFalse(d["sealed_artifacts_mutated"])
        self.assertAlmostEqual(d["volatility"]["primary"]["se_analytic"], VOL_SE, places=12)
        self.assertEqual(d["volatility"]["track_verdict"], "NULL_UNDERPOWERED")
        # symmetry fails 1% rule -> pooled track INCONCLUSIVE per prereg; but power still reported
        self.assertEqual(d["observed_liquidation"]["pooled"]["verdict"], "INCONCLUSIVE")
        self.assertFalse(d["observed_liquidation"]["pooled"]["symmetry_pass_1pct"])
        self.assertGreater(d["observed_liquidation"]["pooled"]["achieved_power_at_floor"], 0.98)
        self.assertTrue(d["known_answer_self_test"]["recovered_within_tolerance"])
        self.assertTrue(self.em.exists())
        txt = self.em.read_text()
        self.assertIn("NULL_UNDERPOWERED", txt)
        self.assertIn("INCONCLUSIVE", txt)

    def test_liq_per_block_are_flagged_approximations(self):
        d = json.loads(self.ej.read_text())
        for b, r in d["observed_liquidation"]["per_block"].items():
            self.assertIn("approximation", r["se_method"])


if __name__ == "__main__":
    unittest.main(verbosity=2)
