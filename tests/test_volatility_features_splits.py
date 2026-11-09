"""Stdlib-only tests for src.volatility.features and .splits (dep-light gate)."""
import unittest
from datetime import datetime, timezone

from src.volatility.features import log_returns, realized_variance, trailing_rv, forward_rv
from src.volatility.splits import parse_iso, in_split


class TestLogReturns(unittest.TestCase):
    def test_basic(self):
        import math
        r = log_returns([100.0, 110.0, 99.0])
        self.assertEqual(len(r), 2)
        self.assertAlmostEqual(r[0], math.log(1.1))
        self.assertAlmostEqual(r[1], math.log(99.0 / 110.0))

    def test_invalid_prices(self):
        r = log_returns([100.0, None, 99.0, 0.0, 50.0])
        self.assertIsNone(r[0])
        self.assertIsNone(r[1])
        self.assertIsNone(r[2])
        self.assertIsNone(r[3])


class TestRealizedVariance(unittest.TestCase):
    def test_sum_of_squares(self):
        self.assertAlmostEqual(realized_variance([0.1, -0.2, 0.3]), 0.14)

    def test_empty(self):
        self.assertIsNone(realized_variance([]))
        self.assertIsNone(realized_variance([None, None]))


class TestTrailingForwardRV(unittest.TestCase):
    def test_trailing_rv_bounds(self):
        prices = [100, 101, 102, 103, 104]
        self.assertIsNone(trailing_rv(prices, 1, 2))
        rv = trailing_rv(prices, 2, 2)
        self.assertIsNotNone(rv)
        self.assertGreater(rv, 0)

    def test_forward_rv_bounds(self):
        prices = [100, 101, 102, 103, 104]
        self.assertIsNone(forward_rv(prices, 3, 2))
        rv = forward_rv(prices, 2, 2)
        self.assertIsNotNone(rv)
        self.assertGreater(rv, 0)


class TestSplits(unittest.TestCase):
    def test_parse_iso_z(self):
        dt = parse_iso("2024-04-01T00:00:00Z")
        self.assertEqual(dt.tzinfo, timezone.utc)
        self.assertEqual(dt.year, 2024)
        self.assertEqual(dt.month, 4)

    def test_in_split(self):
        bounds = ("2024-04-01T00:00:00Z", "2024-06-08T23:00:00Z")
        self.assertTrue(in_split(parse_iso("2024-05-01T00:00:00Z"), bounds))
        self.assertTrue(in_split(parse_iso("2024-04-01T00:00:00Z"), bounds))
        self.assertFalse(in_split(parse_iso("2024-06-09T00:00:00Z"), bounds))
        self.assertFalse(in_split(parse_iso("2024-03-31T23:00:00Z"), bounds))


if __name__ == "__main__":
    unittest.main()
