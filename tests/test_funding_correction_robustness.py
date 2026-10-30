import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from funding_correction_replication import (
    benjamini_hochberg,
    bootstrap_median_ci,
    replicate_funding_correction,
)


class TestFundingCorrectionRobustness(unittest.TestCase):

    def test_benjamini_hochberg_empty(self):
        self.assertEqual(benjamini_hochberg([]), [])

    def test_benjamini_hochberg_monotonic(self):
        pvals = [0.01, 0.04, 0.03]
        adj = benjamini_hochberg(pvals)
        self.assertEqual(len(adj), 3)
        # adjusted p-values should be in [0,1]
        for a in adj:
            self.assertGreaterEqual(a, 0.0)
            self.assertLessEqual(a, 1.0)

    def test_bootstrap_median_ci(self):
        times = [1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0]
        lo, hi = bootstrap_median_ci(times, n_boot=100, seed=123)
        self.assertIsNotNone(lo)
        self.assertIsNotNone(hi)
        self.assertLessEqual(lo, hi)

    def test_robustness_outputs_present(self):
        res = replicate_funding_correction(symbols=["BTCUSDT"])
        self.assertIn("median_correction_hours_all_ci", res)
        self.assertIn("median_by_volatility_tercile", res)
        self.assertIn("multiple_comparisons", res)
        mc = res["multiple_comparisons"]
        self.assertEqual(mc["method"], "Benjamini-Hochberg FDR")
        self.assertIn("18-symbol universe", mc["universe_note"])


if __name__ == "__main__":
    unittest.main()
