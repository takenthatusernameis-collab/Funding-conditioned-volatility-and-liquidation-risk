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

    def test_sensitivity_grid_shape_and_headline(self):
        """Frozen grid must be 12 cells with expected dimensions and headline flag."""
        sym_series = {}
        price_maps = {}
        per_sym = {}
        step = 8 * 3600 * 1000
        for sym in ["S1", "S2", "S3"]:
            rates = []
            for i in range(300):
                if i in (60, 180):
                    rates.append(0.02)
                elif i in (120, 240):
                    rates.append(-0.02)
                else:
                    rates.append(0.0001)
            sym_series[sym] = [(i * step, r) for i, r in enumerate(rates)]
            pm = {}
            price = 100.0
            for h in range(300 * 8):
                ts = h * 3600 * 1000
                vol = 0.001 if (h // 200) % 2 == 0 else 0.01
                price = price * (1.0 + (vol if h % 2 == 0 else -vol))
                pm[ts] = price
            price_maps[sym] = pm
            per_sym[sym] = {"m": len(rates)}
        cells = []
        for p_low, p_high in [(1.0, 99.0), (5.0, 95.0), (10.0, 90.0)]:
            for censor in (168, 336):
                for rv_split in ("tercile", "median"):
                    arm = self.shek._run_arm_a_impl(
                        sym_series, price_maps, per_sym, [],
                        p_low, p_high, censor, rv_split,
                        months=["m"], symbols=["S1", "S2", "S3"])
                    fam = self.shek._primary_family(arm["events"], arm["cluster_key"])
                    fam_valid = [f for f in fam if f.get("p_two_sided") is not None]
                    # re-run Holm on valid subset for verdict consistency
                    if fam_valid:
                        pvals = [f["p_two_sided"] for f in fam_valid]
                        import funding_correction_replication as fcr
                        adj = fcr.holm_bonferroni(pvals)
                        for f, a in zip(fam_valid, adj):
                            f["p_adj_holm"] = a
                    pooled = next((f for f in fam_valid if f["label"] == "pooled_high_vs_low"), None)
                    verdict = self.shek._verdict(fam_valid, pooled)
                    cells.append({
                        "percentiles": [p_low, p_high], "censor": censor,
                        "rv_split": rv_split, "verdict": verdict,
                        "n_events": len(arm["events"]),
                        "n_corrected": sum(1 for e in arm["events"] if not e["censored"]),
                        "n_censored": sum(1 for e in arm["events"] if e["censored"]),
                        "regime_counts": self.shek._regime_counts(arm["events"]),
                    })
        self.assertEqual(len(cells), 12)
        for c in cells:
            self.assertEqual(c["n_events"], c["n_corrected"] + c["n_censored"])
            self.assertIn(c["verdict"], {"REPLICATES_DIRECTION", "TAIL_SHAPE_EFFECT", "NULL", "UNDERPOWERED", "INCONCLUSIVE"})
        headline = [c for c in cells if c["percentiles"] == [5.0, 95.0] and c["censor"] == 168 and c["rv_split"] == "tercile"]
        self.assertEqual(len(headline), 1)

    def test_median_rv_split_and_censor_sensitivity(self):
        """Median split and longer censor should be accepted and produce valid regime accounting."""
        sym_series = {"X": [(i * 8 * 3600 * 1000, 0.02 if i == 50 else ( -0.02 if i == 100 else 0.0001)) for i in range(200)]}
        pm = {h * 3600 * 1000: 100.0 + (h % 5) for h in range(200 * 8)}
        per_sym = {"X": {"m": 200}}
        for rv_split in ("tercile", "median"):
            for censor in (168, 336):
                arm = self.shek._run_arm_a_impl(sym_series, {"X": pm}, per_sym, [],
                                                5.0, 95.0, censor, rv_split, months=["m"], symbols=["X"])
                rc = self.shek._regime_counts(arm["events"])
                total = sum(v["n"] for v in rc.values())
                self.assertEqual(total, len(arm["events"]))
                # rv_split recorded
                self.assertEqual(arm["rv_split"], rv_split)


if __name__ == "__main__":
    unittest.main()
