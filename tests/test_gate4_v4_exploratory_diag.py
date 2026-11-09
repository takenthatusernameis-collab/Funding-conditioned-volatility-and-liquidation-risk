"""Tests for Gate 4 v4 EXPLORATORY diagnostic helpers (no network, synthetic)."""
from __future__ import annotations

import unittest

import numpy as np
import pandas as pd

from scripts.run_gate4_v4_exploratory_diag import fit_predict_ols_with_coef, stabilized_predict, alignment_checks


def _toy_panel(n=60):
    idx = pd.date_range("2024-04-01", periods=n, freq="h", tz="UTC")
    rows = []
    for sym in ["BTCUSDT", "ETHUSDT"]:
        rv = np.abs(np.random.default_rng(0).normal(0.001, 0.0003, n)) + 1e-6
        rows.append(pd.DataFrame({
            "rv_trail_24": rv,
            "rv_trail_168": rv * 1.01,
            "rv_trail_6": rv * 0.99,
            "funding_signed": np.random.default_rng(1).normal(0, 0.0001, n),
            "funding_abs": np.abs(np.random.default_rng(2).normal(0, 0.0001, n)),
            "target_rv": rv * 1.02,
        }, index=pd.MultiIndex.from_product([[sym], idx], names=["symbol", "timestamp"])))
    return pd.concat(rows).sort_index()


class TestGate4V4ExploratoryDiag(unittest.TestCase):
    def test_fit_predict_ols_with_coef_shapes_and_diag(self):
        panel = _toy_panel()
        train = panel.iloc[:40]
        test = panel.iloc[40:]
        fcols = ["rv_trail_24", "rv_trail_168", "rv_trail_6", "funding_signed"]
        p, diags = fit_predict_ols_with_coef(train, test, fcols)
        self.assertEqual(len(p), len(test))
        self.assertTrue(any(d.get("status") == "OK" for d in diags))
        ok = [d for d in diags if d.get("status") == "OK"][0]
        self.assertIn("coef", ok)
        self.assertIn("raw_pred", ok)
        self.assertIn("metrics", ok)

    def test_stabilized_predict_finite_floor(self):
        panel = _toy_panel()
        train = panel.iloc[:40]
        test = panel.iloc[40:]
        fcols = ["rv_trail_24", "rv_trail_168", "rv_trail_6", "funding_signed"]
        p = stabilized_predict(train, test, fcols, pred_floor=1e-8)
        fin = p[np.isfinite(p)]
        self.assertTrue((fin >= 1e-8).all())

    def test_alignment_checks_strings(self):
        a = alignment_checks()
        self.assertIn("train_only_normalization", a)
        self.assertIn("funding_last_known_alignment", a)


if __name__ == "__main__":
    unittest.main()
