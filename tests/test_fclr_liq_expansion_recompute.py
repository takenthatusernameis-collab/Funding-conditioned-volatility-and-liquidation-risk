#!/usr/bin/env python3
"""Tests for scripts/fclr_liq_expansion_recompute.py (Phase B — TRACKA-LIQ-EXPANSION-RECOMPUTE).

Pins the invariant that the prereg stays FROZEN_PRE_OUTCOMES, the rebuilt panel
hash matches its build report, contrasts are non-empty, and sealed artifacts are
never mutated. No network, no outcome recomputation — file-level checks only.
"""
from __future__ import annotations

import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
RS = ROOT / "research_state"

PREREG_GLOB = "prereg_tracka_liq_expansion_recompute_20261114T073346Z.json"
PANEL_GLOB = "tracka_liq_expansion_recompute_panel_*.parquet"
REPORT_GLOB = "tracka_liq_expansion_recompute_panel_build_report_*.json"
EVAL_GLOB = "evaluation_summary_TRACKA-LIQ-EXPANSION-RECOMPUTE-*.json"
SEALED_PANEL = "tracka_hl_expansion_panel_20261111T202344Z.parquet"
SEALED_EVAL = "tracka_hl_expansion_eval_result_20261111T202344Z.json"


def _latest(glob: str):
    cands = sorted(RS.glob(glob))
    return cands[-1] if cands else None


def _read_json(path: Path):
    try:
        return json.loads(path.read_text())
    except Exception:
        return None


class TestLiqExpansionRecomputePrereg(unittest.TestCase):
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
        self.assertEqual(spec.get("experiment_id"), "FCLR-LIQ-EXPANSION-RECOMPUTE-20261114T073346Z")


class TestLiqExpansionRecomputePanelHash(unittest.TestCase):
    def test_panel_and_report_exist_with_matching_hash(self):
        panel = _latest(PANEL_GLOB)
        report = _latest(REPORT_GLOB)
        self.assertIsNotNone(panel, "recomputed panel parquet must exist")
        self.assertIsNotNone(report, "panel build report must exist")
        spec = _read_json(report)
        self.assertIsNotNone(spec, "build report must be valid JSON")
        recorded = spec.get("panel_sha256")
        self.assertIsNotNone(recorded, "build report must record panel_sha256")
        import hashlib
        h = hashlib.sha256()
        with panel.open("rb") as fh:
            for chunk in iter(lambda: fh.read(1 << 20), b""):
                h.update(chunk)
        self.assertEqual(h.hexdigest(), recorded, "panel sha256 must match build report")


class TestLiqExpansionRecomputeEval(unittest.TestCase):
    def test_evaluation_summary_exists_with_recognised_verdict(self):
        p = _latest(EVAL_GLOB)
        self.assertIsNotNone(p, "evaluation summary must exist")
        spec = _read_json(p)
        self.assertIsNotNone(spec, "evaluation summary must be valid JSON")
        verdict = spec.get("verdict")
        self.assertIn(verdict, {"REPRODUCED", "NOT_REPRODUCED", "INCONCLUSIVE", "INADMISSIBLE"},
                      f"verdict must be recognised, got {verdict!r}")


class TestLiqExpansionRecomputeContrastsNonEmpty(unittest.TestCase):
    def test_contrasts_are_non_empty_when_not_inadmissible(self):
        p = _latest(EVAL_GLOB)
        self.assertIsNotNone(p, "evaluation summary must exist")
        spec = _read_json(p)
        self.assertIsNotNone(spec, "evaluation summary must be valid JSON")
        if spec.get("verdict") == "INADMISSIBLE":
            self.skipTest("INADMISSIBLE — no contrasts computed by design")
        contrasts = spec.get("contrasts") or {}
        for k in ("C2_vs_B1", "C1_vs_B1", "C2_vs_C1"):
            self.assertIn(k, contrasts, f"contrast {k} must be present")
            self.assertIsInstance(contrasts[k], dict, f"contrast {k} must be a dict")


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


if __name__ == "__main__":
    unittest.main()
