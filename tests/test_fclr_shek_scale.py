"""FCLR-SHEK-SCALE deterministic fixture tests (no network, cache-independent).

Validates frozen event-definition primitives and scaled-pipeline helpers:
correction vs censoring, same-side dedupe, RV-regime assignment, KM median
not-reached semantics, materiality/verdict classification, and per-coin/coin
regime counting. Uses synthetic series only; does not read research_state.
"""
from __future__ import annotations

import importlib.util
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))


def _load_shek():
    spec = importlib.util.spec_from_file_location(
        "fclr_shek_scale_test", ROOT / "scripts" / "fclr_shek_scale.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


class TestFclrShekScale(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.shek = _load_shek()
        import funding_correction_replication as fcr
        cls.fcr = fcr

    def _series(self, rates, start_ms=0, step_ms=8 * 3600 * 1000):
        return [(start_ms + i * step_ms, r) for i, r in enumerate(rates)]

    def test_correction_and_censoring(self):
        # correction: extreme -> still outside -> returns inside band at +16h
        base = [0.0001] * 100
        rates = base + [0.02, 0.01, 0.0]
        series = self._series(rates)
        evs = self.fcr.identify_funding_extremes(series)
        self.assertTrue(evs)
        ev = [e for e in evs if e["timestamp_ms"] == 100 * 8 * 3600 * 1000][-1]
        ttc, cens = self.fcr.time_to_correction(
            series, ev["timestamp_ms"], ev["side"],
            ev["threshold_low"], ev["threshold_high"])
        self.assertFalse(cens)
        self.assertEqual(ttc, 16.0)
        # censored: never returns inside band before end
        rates2 = base + [0.02, 0.015, 0.012]
        series2 = self._series(rates2)
        evs2 = self.fcr.identify_funding_extremes(series2)
        ev2 = [e for e in evs2 if e["timestamp_ms"] == 100 * 8 * 3600 * 1000][-1]
        ttc2, cens2 = self.fcr.time_to_correction(
            series2, ev2["timestamp_ms"], ev2["side"],
            ev2["threshold_low"], ev2["threshold_high"])
        self.assertTrue(cens2)
        self.assertIsNone(ttc2)

    def test_same_side_dedupe_keeps_first(self):
        base = [0.0001] * 120
        rates = base + [0.03, 0.031, 0.0001] + [0.0001] * 40
        series = self._series(rates)
        evs = self.fcr.identify_funding_extremes(series)
        spike_ts = {120 * 8 * 3600 * 1000, 121 * 8 * 3600 * 1000}
        spikes = [e for e in evs if e["timestamp_ms"] in spike_ts]
        self.assertEqual(len(spikes), 1)
        self.assertEqual(spikes[0]["timestamp_ms"], 120 * 8 * 3600 * 1000)

    def test_rv_regime_assignment_and_counts(self):
        events = []
        rvs = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]
        for i, rv in enumerate(rvs):
            events.append({
                "symbol": "BTCUSDT",
                "side": "positive",
                "rv_24h": rv,
                "rv_n_returns": 24,
                "time_to_correction_hours": 8.0 + i,
                "censored": False,
                "timestamp_ms": 1_700_000_000_000 + i * 8 * 3600 * 1000,
            })
        vals = sorted(e["rv_24h"] for e in events)
        low_edge = self.fcr._nearest_rank_percentile(vals, 33.33)
        high_edge = self.fcr._nearest_rank_percentile(vals, 66.67)
        for ev in events:
            if ev["rv_24h"] <= low_edge:
                ev["rv_regime"] = "low"
            elif ev["rv_24h"] >= high_edge:
                ev["rv_regime"] = "high"
            else:
                ev["rv_regime"] = "middle"
        counts = self.shek._regime_counts(events)
        self.assertEqual(counts["low"]["n"] + counts["middle"]["n"] + counts["high"]["n"], 9)
        self.assertEqual(sum(v["n"] for v in counts.values()), 9)

    def test_km_median_not_reached(self):
        recs = [{"t": 168.0, "censored": True}, {"t": 168.0, "censored": True}]
        self.assertIsNone(self.shek._km_median(recs))
        recs2 = [{"t": 8.0, "censored": False}, {"t": 8.0, "censored": False},
                 {"t": 16.0, "censored": False}, {"t": 24.0, "censored": False}]
        self.assertEqual(self.shek._km_median(recs2), 8.0)

    def test_verdict_tail_shape_vs_replicates(self):
        pooled_tail = {
            "materiality_base_high": 8.000000277777778,
            "materiality_base_low": 8.0,
            "material": False,
            "median_diff_ci": {"lo": -1.0, "hi": 1.0},
            "p_adj_holm": 0.001,
        }
        self.assertEqual(self.shek._verdict([pooled_tail], pooled_tail), "TAIL_SHAPE_EFFECT")
        pooled_rep = {
            "materiality_base_high": 16.0,
            "materiality_base_low": 8.0,
            "material": True,
            "median_diff_ci": {"lo": 4.0, "hi": 12.0},
            "p_adj_holm": 0.001,
        }
        self.assertEqual(self.shek._verdict([pooled_rep], pooled_rep), "REPLICATES_DIRECTION")
        pooled_null = {
            "materiality_base_high": 8.0,
            "materiality_base_low": 8.0,
            "material": False,
            "median_diff_ci": {"lo": -0.1, "hi": -0.01},
            "p_adj_holm": 0.5,
        }
        self.assertEqual(self.shek._verdict([pooled_null], pooled_null), "NULL")
        self.assertEqual(self.shek._verdict([], None), "INCONCLUSIVE")


if __name__ == "__main__":
    unittest.main()
