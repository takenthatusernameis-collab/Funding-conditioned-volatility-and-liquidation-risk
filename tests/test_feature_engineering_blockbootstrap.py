from __future__ import annotations

import unittest
from src.volatility import feature_engineering as fe
from src.volatility import block_bootstrap as bb


class TestFeatureEngineering(unittest.TestCase):
    def test_trailing_percentile_zscore(self):
        vals = [1.0, 2.0, 3.0, 4.0]
        p = fe.trailing_percentile(vals, 3.0)
        self.assertIsNotNone(p)
        self.assertGreaterEqual(p, 0.0)
        self.assertLessEqual(p, 1.0)
        z = fe.trailing_zscore(vals, 5.0)
        self.assertIsNotNone(z)

    def test_rv_ratio(self):
        self.assertIsNotNone(fe.rv_ratio(0.01, 0.02))
        self.assertIsNone(fe.rv_ratio(0.01, 0.0))
        self.assertIsNone(fe.rv_ratio(None, 0.02))

    def test_price_dislocation(self):
        self.assertAlmostEqual(fe.price_dislocation_ma_deviation(110.0, 100.0), 0.1)
        self.assertIsNone(fe.price_dislocation_ma_deviation(110.0, 0.0))

    def test_train_only_scaler(self):
        scaler = fe.TrainOnlyScaler().fit([1.0, 2.0, 3.0, 4.0])
        self.assertIsNotNone(scaler.mean_)
        out = scaler.transform([2.0])
        self.assertEqual(len(out), 1)


class TestBlockBootstrap(unittest.TestCase):
    def test_circular_blocks(self):
        reps = bb.circular_block_bootstrap_indices(10, 3, 5, seed=123)
        self.assertEqual(len(reps), 5)
        for r in reps:
            self.assertEqual(len(r), 10)

    def test_block_bootstrap_ci(self):
        y = [0.01] * 50
        yhat_b = [0.012] * 50
        yhat_a = [0.011] * 50
        def qlike_fn(yy, yh):
            import math
            s = 0.0
            for a,b in zip(yy,yh):
                if a>0 and b>0:
                    s += a/b - math.log(a/b) - 1.0
            return s/len(yy) if yy else float('nan')
        diff, lo, hi = bb.block_bootstrap_ci(y, yhat_b, yhat_a, qlike_fn, block_size=6, num_reps=100, seed=5)
        self.assertIsInstance(diff, float)
        self.assertIsInstance(lo, float)
        self.assertIsInstance(hi, float)


if __name__ == '__main__':
    unittest.main()
