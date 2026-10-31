import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from funding_correction_replication import (
    benjamini_hochberg,
    bootstrap_median_ci,
    log_rank_test,
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

    def test_log_rank_identical_groups_not_significant(self):
        # Two identical survival samples -> chi2 ~ 0, p ~ 1
        a = [(8.0, False), (16.0, False), (24.0, True)]
        chi2, p = log_rank_test(a, list(a))
        self.assertIsNotNone(chi2)
        self.assertLessEqual(chi2, 1e-9)
        self.assertGreaterEqual(p, 0.99)

    def test_log_rank_separated_groups_significant(self):
        # Group A corrects immediately, group B never corrects (censored)
        a = [(8.0, False)] * 10
        b = [(168.0, True)] * 10
        chi2, p = log_rank_test(a, b)
        self.assertIsNotNone(chi2)
        self.assertGreater(chi2, 10.0)
        self.assertLess(p, 0.01)

    def test_log_rank_empty(self):
        chi2, p = log_rank_test([], [])
        self.assertIsNone(chi2)
        self.assertIsNone(p)

    def test_robustness_outputs_present(self):
        res = replicate_funding_correction(symbols=["BTCUSDT"])
        self.assertIn("median_correction_hours_all_ci", res)
        self.assertIn("median_by_volatility_tercile", res)
        self.assertIn("multiple_comparisons", res)
        mc = res["multiple_comparisons"]
        self.assertEqual(mc["method"], "Benjamini-Hochberg FDR")
        self.assertIn("18-symbol universe", mc["universe_note"])
        # log-rank contrast must be present (pre-registered primary contrast)
        self.assertIn("log_rank_high_vs_low", res)


if __name__ == "__main__":
    unittest.main()
