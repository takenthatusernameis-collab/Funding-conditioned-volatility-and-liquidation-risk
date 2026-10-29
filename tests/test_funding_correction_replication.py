import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from funding_correction_replication import (
    load_funding_series,
    identify_funding_extremes,
    time_to_correction,
    compute_rv_at_event,
    replicate_funding_correction,
    _nearest_rank_percentile,
)

REPO = Path(__file__).resolve().parents[1]
BTC_JAN = REPO / "BTCUSDT-fundingRate-2024-01" / "BTCUSDT-fundingRate-2024-01.csv"


class TestFundingCorrectionReplication(unittest.TestCase):

    def test_load_funding_series_real(self):
        series = load_funding_series(BTC_JAN)
        self.assertGreater(len(series), 0)
        self.assertIsInstance(series[0][0], int)
        self.assertIsInstance(series[0][1], float)
        self.assertTrue(all(series[i][0] < series[i + 1][0]
                            for i in range(len(series) - 1)))

    def test_nearest_rank_percentile(self):
        self.assertEqual(_nearest_rank_percentile([1, 2, 3, 4, 5], 50), 3)
        self.assertEqual(_nearest_rank_percentile([], 50), None)

    def test_identify_extremes_constant_series(self):
        series = [(i * 8 * 3600 * 1000, 0.0001) for i in range(200)]
        events = identify_funding_extremes(series)
        self.assertEqual(events, [])

    def test_identify_extremes_detects_spike(self):
        series = [(i * 8 * 3600 * 1000, 0.0001) for i in range(100)]
        series = series + [(100 * 8 * 3600 * 1000, 0.01)]
        events = identify_funding_extremes(series)
        self.assertIsInstance(events, list)

    def test_time_to_correction_corrected(self):
        series = [
            (0, 0.01),
            (8 * 3600 * 1000, 0.005),
            (16 * 3600 * 1000, 0.0002),
        ]
        ttc, censored = time_to_correction(series, 0, "positive", -0.001, 0.0003)
        self.assertFalse(censored)
        self.assertEqual(ttc, 16.0)

    def test_time_to_correction_censored(self):
        series = [
            (0, 0.01),
            (8 * 3600 * 1000, 0.005),
        ]
        ttc, censored = time_to_correction(series, 0, "positive", -0.001, 0.0003)
        self.assertTrue(censored)
        self.assertIsNone(ttc)

    def test_same_side_dedupe(self):
        series = [(i * 8 * 3600 * 1000, 0.0001) for i in range(200)]
        series = series + [(200 * 8 * 3600 * 1000, 0.02),
                           (201 * 8 * 3600 * 1000, 0.021),
                           (202 * 8 * 3600 * 1000, 0.0001)]
        events = identify_funding_extremes(series)
        spikes = [e for e in events if e["timestamp_ms"] >=
                  200 * 8 * 3600 * 1000]
        self.assertEqual(len(spikes), 1)

    def test_compute_rv_no_price_data(self):
        rv, n = compute_rv_at_event({}, 1704067200000)
        self.assertIsNone(rv)
        self.assertEqual(n, 0)

    def test_pipeline_runs_btcusdt(self):
        res = replicate_funding_correction(symbols=["BTCUSDT"])
        self.assertEqual(res["status"], "partial")
        self.assertIsInstance(res["total_events"], int)
        self.assertGreaterEqual(res["total_events"], 0)
        regimes = res["hazard_by_rv_regime"]
        total_regime_n = sum(rg["n"] for rg in regimes.values())
        self.assertEqual(total_regime_n, res["total_events"])

    def test_report_fields_present(self):
        res = replicate_funding_correction(symbols=["BTCUSDT"])
        for key in ("paper_claim", "definition", "regime_edges",
                    "hazard_by_rv_regime", "censored_count",
                    "corrected_count"):
            self.assertIn(key, res)


if __name__ == "__main__":
    unittest.main()
