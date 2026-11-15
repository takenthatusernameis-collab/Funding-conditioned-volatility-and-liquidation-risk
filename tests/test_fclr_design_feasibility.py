#!/usr/bin/env python3
"""Tests for FCLR-DESIGN-FEASIBILITY (scripts/fclr_design_feasibility.py)."""
from __future__ import annotations

import json
import math
import unittest
from pathlib import Path

import sys
REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "scripts"))
import fclr_design_feasibility as fea  # noqa: E402

RS = REPO / "research_state"
OUT_UTC = "2026-11-15T02:35:00Z"
PREREG = RS / f"prereg_fclr_design_feasibility_{OUT_UTC}.json"
POWER_EVAL = RS / "evaluation_summary_FCLR-POWER-CALIBRATION-2026-11-15T01:34:12Z.json"

# Self-check anchors from AGENT_HANDOFF.md (persisted constants)
Z_975 = 1.959963984540054
Z_80 = 0.8416212335729143
Z_95 = 1.6448536269514722
MDE80_FACTOR = 2.8015852181129683


class TestRequiredNInversionArithmetic(unittest.TestCase):
    def test_vol_primary_anchor(self):
        # Vol: SE_req = 0.007052315476086073 / mde80_factor; n_req = 10800*(0.010469953259366775/SE_req)^2
        floor = 0.007052315476086073
        se_obs = 0.010469953259366775
        n_obs = 10800.0
        se_req = fea.se_required_for_floor(floor)
        self.assertAlmostEqual(se_req, 0.0025172590, places=9)
        n_req = fea.required_n(se_obs, se_req, n_obs)
        self.assertAlmostEqual(n_req, 186834.7, delta=1.0)
        self.assertEqual(fea.decidability(n_req, n_obs), "UNDECIDABLE_ON_CACHE")

    def test_liq_analytic_anchor(self):
        floor = 0.05
        se_obs = 0.012089357803458227
        n_obs = 6634.0
        se_req = fea.se_required_for_floor(floor)
        self.assertAlmostEqual(se_req, 0.0178470388, places=9)
        self.assertLess(se_obs, se_req)
        n_req = fea.required_n(se_obs, se_req, n_obs)
        self.assertLess(n_req, n_obs)
        self.assertEqual(fea.decidability(n_req, n_obs), "DECIDABLE_ON_CACHE")

    def test_liq_robust_anchor_no_flip(self):
        # SE_robust = max(|q5|,|q95|)/z_95 with q5=-0.020772393084283722,q95=0.01899805497678097
        q5 = -0.020772393084283722
        q95 = 0.01899805497678097
        se_robust = max(abs(q5), abs(q95)) / Z_95
        self.assertAlmostEqual(se_robust, 0.0126287183, places=9)
        se_req = 0.05 / MDE80_FACTOR
        self.assertLess(se_robust, se_req)
        n_req = fea.required_n(se_robust, se_req, 6634.0)
        self.assertLess(n_req, 6634.0)
        self.assertEqual(fea.decidability(n_req, 6634.0), "DECIDABLE_ON_CACHE")

    def test_mde80_factor_constant(self):
        self.assertAlmostEqual(fea.MDE80_FACTOR, MDE80_FACTOR, places=12)
        self.assertAlmostEqual(fea.Z_975, Z_975, places=12)
        self.assertAlmostEqual(fea.Z_80, Z_80, places=12)
        self.assertAlmostEqual(fea.Z_95, Z_95, places=12)


class TestDecidabilityBoundaryAndFlip(unittest.TestCase):
    def test_boundary_equal_is_decidable(self):
        self.assertEqual(fea.decidability(100.0, 100.0), "DECIDABLE_ON_CACHE")

    def test_boundary_above_is_undecidable(self):
        self.assertEqual(fea.decidability(100.0001, 100.0), "UNDECIDABLE_ON_CACHE")

    def test_nonfinite_is_inconclusive(self):
        self.assertEqual(fea.decidability(float("nan"), 100.0), "INCONCLUSIVE")
        self.assertEqual(fea.decidability(10.0, float("nan")), "INCONCLUSIVE")
        self.assertEqual(fea.decidability(10.0, 0.0), "INCONCLUSIVE")

    def test_symmetry_robustness_flip_detection(self):
        # Construct a case where analytic is decidable but robust is not
        floor = 0.05
        se_req = fea.se_required_for_floor(floor)
        n_obs = 1000.0
        se_analytic = se_req * 0.9  # decidable
        se_robust = se_req * 1.1    # undecidable
        self.assertEqual(fea.decidability(fea.required_n(se_analytic, se_req, n_obs), n_obs), "DECIDABLE_ON_CACHE")
        self.assertEqual(fea.decidability(fea.required_n(se_robust, se_req, n_obs), n_obs), "UNDECIDABLE_ON_CACHE")


class TestKnownAnswerAndMissing(unittest.TestCase):
    def test_known_answer_recovery(self):
        ka = fea.known_answer_self_test()
        self.assertTrue(ka["recovered_80pct_within_tolerance"])
        self.assertAlmostEqual(ka["power_at_nreq"], 0.80, places=5)

    def test_missing_unstable_se(self):
        self.assertTrue(math.isnan(fea.se_required_for_floor(float("nan"))))
        self.assertTrue(math.isnan(fea.se_required_for_floor(-1.0)))
        self.assertTrue(math.isnan(fea.required_n(0.1, float("nan"), 100.0)))

    def test_power_helper(self):
        # sanity: higher delta => higher power
        self.assertGreater(fea.power_two_sided(0.1, 0.02), fea.power_two_sided(0.01, 0.02))


class TestPreregAndNoMutation(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.prereg = json.loads(PREREG.read_text())
        cls.sealed_paths = [p for p in sorted(fea.SEALED) if p.exists()]
        cls.before = {str(p): fea.sha256_file(p) for p in cls.sealed_paths}

    def test_prereg_frozen(self):
        d = self.prereg
        self.assertEqual(d["status"], "FROZEN_PRE_OUTCOMES")
        self.assertTrue(d["frozen_before_outcomes"])
        self.assertFalse(d["outcome_data_inspected_before_freeze"])
        self.assertFalse(d["promotable"])
        self.assertEqual(d["max_status"], "EXPLORATORY_ONLY")
        self.assertTrue(d["does_not_reopen_sealed_verdict"])

    def test_prereg_inputs_match(self):
        inp = self.prereg["inputs"]
        self.assertEqual(inp["power_calibration_eval_sha256"], fea.sha256_file(fea.POWER_EVAL))
        self.assertEqual(inp["vol_panel_sha256"], fea.sha256_file(fea.VOL_PANEL))
        self.assertEqual(inp["liq_panel_sha256"], fea.sha256_file(fea.LIQ_PANEL))

    def test_sealed_inputs_unchanged(self):
        after = {str(p): fea.sha256_file(p) for p in self.sealed_paths}
        self.assertEqual(after, self.before)

    def test_run_no_write_no_mutation(self):
        out = fea.run(out_utc=OUT_UTC, write=False)
        self.assertFalse(out["sealed_artifacts_mutated"])
        after = {str(p): fea.sha256_file(p) for p in self.sealed_paths}
        self.assertEqual(after, self.before)


class TestEndToEndOutput(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.ej = RS / f"evaluation_summary_FCLR-DESIGN-FEASIBILITY-{OUT_UTC}.json"
        cls.em = RS / f"evaluation_summary_FCLR-DESIGN-FEASIBILITY-{OUT_UTC}.md"
        cls.power = json.loads(POWER_EVAL.read_text())

    def test_eval_artifacts_exist(self):
        self.assertTrue(self.ej.exists(), "eval JSON missing")
        self.assertTrue(self.em.exists(), "eval MD missing")

    def test_verdicts_match_anchors(self):
        d = json.loads(self.ej.read_text())
        self.assertEqual(d["volatility"]["track_verdict"], "UNDECIDABLE_ON_CACHE")
        self.assertEqual(d["volatility"]["primary"]["verdict"], "UNDECIDABLE_ON_CACHE")
        self.assertEqual(d["observed_liquidation"]["pooled"]["analytic_decidability"], "DECIDABLE_ON_CACHE")
        self.assertEqual(d["observed_liquidation"]["pooled"]["robust_decidability"], "DECIDABLE_ON_CACHE")
        self.assertFalse(d["observed_liquidation"]["symmetry_robustness"]["verdict_flips_due_to_instability"])
        self.assertEqual(d["observed_liquidation"]["track_verdict"], "DECIDABLE_ON_CACHE")
        self.assertFalse(d["promotable"])
        self.assertEqual(d["max_status"], "EXPLORATORY_ONLY")

    def test_numeric_anchors(self):
        d = json.loads(self.ej.read_text())
        vp = d["volatility"]["primary"]
        self.assertAlmostEqual(vp["se_req_for_80pct"], 0.0025172590, places=9)
        self.assertAlmostEqual(vp["n_req_contrast"], 186834.7, delta=1.5)
        lp = d["observed_liquidation"]["pooled"]
        self.assertAlmostEqual(lp["se_req_for_80pct"], 0.0178470388, places=9)
        self.assertLess(lp["n_req_pooled"], lp["n_available_pooled"])
        self.assertAlmostEqual(lp["se_robust"], 0.0126287183, places=9)

    def test_sealed_hashes_recorded_unchanged(self):
        d = json.loads(self.ej.read_text())
        self.assertFalse(d["sealed_artifacts_mutated"])
        self.assertEqual(d["sealed_hashes_before"], d["sealed_hashes_after"])


if __name__ == "__main__":
    unittest.main()
