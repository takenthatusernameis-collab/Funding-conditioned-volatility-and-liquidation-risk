#!/usr/bin/env python3
"""Tests for scripts/fclr_liq_expansion_reconcile.py (Phase C — TRACKA-LIQ-EXPANSION-RECONCILIATION).

Pins the invariant that the prereg stays FROZEN_PRE_OUTCOMES, the 2×2 matrix
is produced with all four cells, and sealed artifacts are never mutated.
No network, no outcome recomputation — file-level checks only.
"""
from __future__ import annotations

import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
RS = ROOT / "research_state"

PREREG_GLOB = "prereg_tracka_liq_expansion_reconciliation_20261114T083642Z.json"
EVAL_GLOB = "evaluation_summary_TRACKA-LIQ-EXPANSION-RECONCILIATION-*.json"
SEALED_PANEL = "tracka_hl_expansion_panel_20261111T202344Z.parquet"
SEALED_EVAL = "tracka_hl_expansion_eval_result_20261111T202344Z.json"
RECOMPUTE_PANEL = "tracka_liq_expansion_recompute_panel_20261114T083000Z.parquet"
RECOMPUTE_EVAL = "evaluation_summary_TRACKA-LIQ-EXPANSION-RECOMPUTE-20261114T083000Z.json"


def _latest(glob: str):
    cands = sorted(RS.glob(glob))
    return cands[-1] if cands else None


def _read_json(path: Path):
    try:
        return json.loads(path.read_text())
    except Exception:
        return None


class TestLiqExpansionReconcilePrereg(unittest.TestCase):
    def test_prereg_exists_and_is_frozen(self):
        p = _latest(PREREG_GLOB)
        self.assertIsNotNone(p, "frozen prereg must exist")
        spec = _read_json(p)
        self.assertIsNotNone(spec, "prereg must be valid JSON")
        self.assertEqual(spec.get("status"), "FROZEN_PRE_OUTCOMES")
        self.assertTrue(spec.get("frozen_before_outcomes"), "frozen_before_outcomes must be true")
        self.assertTrue(spec.get("pre_registered_before_outcomes"), "pre_registered_before_outcomes must be true")
        self.assertFalse(spec.get("outcome_data_inspected_before_freeze"), "outcome_data_inspected_before_freeze must be false")
        self.assertFalse(spec.get("promotable"), "promotable must be false")
        self.assertEqual(spec.get("max_status"), "EXPLORATORY_ONLY")
        self.assertEqual(spec.get("experiment_id"), "FCLR-LIQ-EXPANSION-RECONCILIATION-20261114T083642Z")


class TestLiqExpansionReconcileEvaluation(unittest.TestCase):
    def test_evaluation_summary_exists_with_recognised_verdict(self):
        p = _latest(EVAL_GLOB)
        self.assertIsNotNone(p, "evaluation summary must exist")
        spec = _read_json(p)
        self.assertIsNotNone(spec, "evaluation summary must be valid JSON")
        verdict = spec.get("verdict")
        self.assertIn(verdict, {"EXPLAINED_BY_ESTIMATOR", "EXPLAINED_BY_DATA", "UNEXPLAINED", "INCONCLUSIVE"},
                      f"verdict must be recognised, got {verdict!r}")

    def test_2x2_matrix_complete(self):
        p = _latest(EVAL_GLOB)
        self.assertIsNotNone(p, "evaluation summary must exist")
        spec = _read_json(p)
        self.assertIsNotNone(spec, "evaluation summary must be valid JSON")

        cells = spec.get("cells") or {}
        # Check all four cells exist
        expected_cells = {"sealed+sealed", "sealed+recompute", "recompute+sealed", "recompute+recompute"}
        for cell_key in expected_cells:
            self.assertIn(cell_key, cells, f"cell {cell_key} must be present")
            cell = cells[cell_key]
            self.assertIsInstance(cell, dict, f"cell {cell_key} must be a dict")
            self.assertIn("contrasts", cell, f"cell {cell_key} must have contrasts")
            contrasts = cell["contrasts"]
            for k in ("C2_vs_B1", "C1_vs_B1", "C2_vs_C1"):
                self.assertIn(k, contrasts, f"cell {cell_key} contrast {k} must be present")

    def test_sealed_estimator_matches_sealed_reference(self):
        p = _latest(EVAL_GLOB)
        self.assertIsNotNone(p, "evaluation summary must exist")
        spec = _read_json(p)
        self.assertIsNotNone(spec, "evaluation summary must be valid JSON")

        cells = spec.get("cells") or {}
        sealed_sealed = cells.get("sealed+sealed")
        self.assertIsNotNone(sealed_sealed, "sealed+sealed cell must exist")

        rel = sealed_sealed["contrasts"]["C2_vs_B1"]["rel_reduction_pct"]
        self.assertAlmostEqual(rel, 19.0371, places=2,
                               msg="sealed+sealed C2_vs_B1 must match sealed reference (~19.04%)")

    def test_recompute_estimator_matches_recompute_reference(self):
        p = _latest(EVAL_GLOB)
        self.assertIsNotNone(p, "evaluation summary must exist")
        spec = _read_json(p)
        self.assertIsNotNone(spec, "evaluation summary must be valid JSON")

        cells = spec.get("cells") or {}
        recompute_recompute = cells.get("recompute+recompute")
        self.assertIsNotNone(recompute_recompute, "recompute+recompute cell must exist")

        rel = recompute_recompute["contrasts"]["C2_vs_B1"]["rel_reduction_pct"]
        self.assertAlmostEqual(rel, 6.19, places=2,
                               msg="recompute+recompute C2_vs_B1 must match recompute reference (~6.19%)")


class TestSealedArtifactsImmutable(unittest.TestCase):
    def test_sealed_panel_unchanged(self):
        p = RS / SEALED_PANEL
        self.assertTrue(p.exists(), "sealed panel must still exist")

    def test_sealed_eval_unchanged(self):
        p = RS / SEALED_EVAL
        self.assertTrue(p.exists(), "sealed eval must still exist")
        spec = _read_json(p)
        self.assertIsNotNone(spec, "sealed eval must be valid JSON")
        c2 = (spec.get("contrasts") or {}).get("C2_vs_B1") or {}
        self.assertAlmostEqual(c2.get("rel_reduction_pct"), 19.0371, places=4,
                               msg="sealed C2_vs_B1 rel reduction must not be altered")

    def test_recompute_panel_unchanged(self):
        p = RS / RECOMPUTE_PANEL
        self.assertTrue(p.exists(), "recompute panel must still exist")

    def test_recompute_eval_unchanged(self):
        p = RS / RECOMPUTE_EVAL
        self.assertTrue(p.exists(), "recompute eval must still exist")
        spec = _read_json(p)
        self.assertIsNotNone(spec, "recompute eval must be valid JSON")
        c2 = (spec.get("contrasts") or {}).get("C2_vs_B1") or {}
        self.assertAlmostEqual(c2.get("rel_reduction_pct"), 6.19, places=4,
                               msg="recompute C2_vs_B1 rel reduction must not be altered")


class TestReconcileVerdictLogic(unittest.TestCase):
    def test_verdict_explained_by_estimator(self):
        """Verify that when panels are identical but estimators differ, verdict is EXPLAINED_BY_ESTIMATOR."""
        p = _latest(EVAL_GLOB)
        self.assertIsNotNone(p, "evaluation summary must exist")
        spec = _read_json(p)
        self.assertIsNotNone(spec, "evaluation summary must be valid JSON")

        verdict = spec.get("verdict")
        self.assertEqual(verdict, "EXPLAINED_BY_ESTIMATOR",
                         "Since panels are identical but estimators produce different results, "
                         "verdict must be EXPLAINED_BY_ESTIMATOR")

        rationale = spec.get("rationale", "")
        self.assertIn("Estimator difference", rationale,
                      "Rationale must mention estimator difference")
        self.assertIn("12.85", rationale,
                      "Rationale must quantify the gap")


if __name__ == "__main__":
    unittest.main()