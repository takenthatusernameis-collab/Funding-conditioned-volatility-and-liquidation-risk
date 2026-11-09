"""Failing-regime regression tests for fit_predict_ols and block_bootstrap_delta_ci_diagnostic.

Synthetic fixtures only: no network, no real research_state writes, no exploratory
recomputation. Covers zero-variance predictor columns, constant finite diffs,
empty/all-non-finite diffs, too-few-blocks, missing required columns, collinear
predictors, and single-instrument panels. Each regime must be detected by the
diagnostic fields (degenerate / regime_flags / ci_accounting_valid /
inference_ok) and must not silently inflate QLIKE or hide a degenerate CI.
"""
from __future__ import annotations

import sys
import unittest
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "scripts"))

from scripts.run_funding_ablations import (  # noqa: E402
    fit_predict_ols,
    paired_qlike_by_time,
)
from src.eval.inference import block_bootstrap_delta_ci_diagnostic  # noqa: E402

BASE = ["rv_trail_24", "rv_trail_168", "rv_trail_6"]


def _ts(n, start="2024-04-01"):
    return pd.date_range(start, periods=n, freq="h", tz="UTC")


def _panel(symbols, n=336, seed=3):
    rows = []
    rng = np.random.default_rng(seed)
    for sym in symbols:
        rv = np.abs(rng.normal(0.001, 0.0003, n)) + 1e-6
        idx = pd.MultiIndex.from_product([[sym], _ts(n)], names=["symbol", "timestamp"])
        rows.append(
            pd.DataFrame(
                {
                    "rv_trail_24": rv,
                    "rv_trail_168": rv * 1.01 + 1e-6,
                    "rv_trail_6": rv * 0.99 + 1e-6,
                    "funding_signed": rng.normal(0.0, 0.0001, n),
                    "target_rv": rv * 1.02 + 1e-6,
                },
                index=idx,
            )
        )
    return pd.concat(rows).sort_index()


def _split(panel, cutoff="2024-04-08T12:00"):
    cut = pd.Timestamp(cutoff, tz="UTC")
    ts = panel.index.get_level_values("timestamp")
    train = panel.loc[ts < cut]
    test = panel.loc[ts >= cut]
    return train, test


def _paired(ts, diffs, copies=2):
    parts = []
    for _ in range(copies):
        t = pd.DatetimeIndex(ts) + pd.Timedelta(minutes=_)
        parts.append(
            pd.DataFrame(
                {
                    "timestamp": t,
                    "ql_base": 1.0,
                    "ql_alt": 1.0 + np.asarray(diffs, dtype=float),
                    "diff": np.asarray(diffs, dtype=float),
                }
            )[["timestamp", "ql_base", "ql_alt", "diff"]]
        )
    return pd.concat(parts, ignore_index=True)


class TestFitPredictOlsFailingRegimes(unittest.TestCase):
    def test_zero_variance_column_does_not_inflate_predictions(self):
        panel = _panel(["BTCUSDT", "ETHUSDT"])
        train, test = _split(panel)
        train = train.copy()
        test = test.copy()
        train["const_col"] = 7.0
        test["const_col"] = 7.0
        full = fit_predict_ols(train, test, BASE + ["const_col"])
        reduced = fit_predict_ols(train, test, BASE)
        finite = full[np.isfinite(full)]
        self.assertGreater(finite.size, 0)
        self.assertTrue(np.allclose(full, reduced, equal_nan=True))
        self.assertTrue(np.all(np.isfinite(full[np.isfinite(full)])))
        self.assertLess(float(np.max(finite)), 0.01)

    def test_collinear_predictors_finite_no_crash(self):
        panel = _panel(["BTCUSDT", "ETHUSDT", "SOLUSDT"])
        train, test = _split(panel)
        train = train.copy()
        test = test.copy()
        train["dup"] = train["rv_trail_24"]
        test["dup"] = test["rv_trail_24"]
        p = fit_predict_ols(train, test, BASE + ["dup"])
        fin = p[np.isfinite(p)]
        self.assertGreater(fin.size, 0)
        self.assertTrue(np.all(fin >= 0.0))
        self.assertTrue(np.all(np.isfinite(fin)))

    def test_missing_required_column_fail_closed(self):
        panel = _panel(["BTCUSDT"])
        train, test = _split(panel)
        with self.assertRaises(ValueError):
            fit_predict_ols(train, test, BASE + ["does_not_exist"])

    def test_single_instrument_panel_produces_finite_predictions(self):
        panel = _panel(["XRPUSDT"])
        train, test = _split(panel)
        p = fit_predict_ols(train, test, BASE)
        fin = p[np.isfinite(p)]
        self.assertGreater(fin.size, 0)
        self.assertTrue(np.all(np.isfinite(fin)))
        self.assertTrue(np.all(fin >= 0.0))

    def test_insufficient_training_graceful_all_nan(self):
        idx = pd.date_range("2024-04-01", periods=1, freq="h", tz="UTC")
        mi = pd.MultiIndex.from_product([["BTCUSDT"], idx], names=["symbol", "timestamp"])
        train = pd.DataFrame(
            {"rv_trail_24": [0.001], "rv_trail_168": [0.001], "rv_trail_6": [0.001], "target_rv": [0.001]},
            index=mi,
        )
        test = train.copy()
        p = fit_predict_ols(train, test, BASE)
        self.assertEqual(len(p), 1)
        self.assertTrue(np.all(np.isnan(p)))

    def test_target_scale_qlike_finite(self):
        panel = _panel(["BTCUSDT", "ETHUSDT"])
        train, test = _split(panel)
        p = fit_predict_ols(train, test, BASE)
        y = test["target_rv"].to_numpy(dtype=float)
        mask = np.isfinite(y) & np.isfinite(p) & (y > 0) & (p > 0)
        self.assertGreater(mask.sum(), 0)
        ql = float(np.mean(y[mask] / p[mask] - np.log(y[mask] / p[mask]) - 1.0))
        self.assertTrue(np.isfinite(ql) and ql >= 0.0)


class TestBlockBootstrapDiagnosticFailingRegimes(unittest.TestCase):
    def test_constant_finite_diffs_flagged_zero_width_ci(self):
        ts = _ts(120)
        out = block_bootstrap_delta_ci_diagnostic(_paired(ts, np.full(120, -0.1)), block_hours=24, n_reps=200, seed=5)
        self.assertIn("constant_finite_diffs", out["regime_flags"])
        self.assertIsNotNone(out["point"])
        self.assertEqual(out["ci_low"], out["ci_high"])
        self.assertEqual(out["point"], out["ci_low"])

    def test_empty_input_degenerate_no_ci(self):
        out = block_bootstrap_delta_ci_diagnostic(
            _paired(_ts(0), np.array([])), block_hours=24, n_reps=50, seed=1,
        )
        self.assertIn("empty_input", out["regime_flags"])
        self.assertTrue(out["degenerate"])
        self.assertFalse(out["inference_ok"])
        self.assertFalse(out["ci_accounting_valid"])
        self.assertIsNone(out["point"])

    def test_all_non_finite_diffs_degenerate_no_point(self):
        ts = _ts(48)
        out = block_bootstrap_delta_ci_diagnostic(
            _paired(ts, np.full(48, np.nan)), block_hours=24, n_reps=50, seed=2,
        )
        self.assertIn("all_diffs_non_finite", out["regime_flags"])
        self.assertTrue(out["degenerate"])
        self.assertFalse(out["inference_ok"])
        self.assertFalse(out["ci_accounting_valid"])
        self.assertIsNone(out["point"])

    def test_too_few_blocks_flagged_degenerate(self):
        ts = _ts(6)
        out = block_bootstrap_delta_ci_diagnostic(
            _paired(ts, np.full(6, -0.2)), block_hours=24, n_reps=80, seed=7,
        )
        self.assertIn("too_few_blocks", out["regime_flags"])
        self.assertTrue(out["degenerate"])
        self.assertFalse(out["inference_ok"])
        self.assertEqual(out["ci_low"], out["ci_high"])

    def test_missing_required_columns_flagged(self):
        bad = _paired(_ts(48), np.full(48, -0.1)).drop(columns=["diff"])
        out = block_bootstrap_delta_ci_diagnostic(bad, block_hours=24, n_reps=50, seed=3)
        self.assertIn("missing_required_columns", out["regime_flags"])
        self.assertTrue(out["degenerate"])
        self.assertFalse(out["inference_ok"])
        self.assertFalse(out["ci_accounting_valid"])

    def test_normal_input_valid_ci(self):
        ts = _ts(240)
        rng = np.random.default_rng(11)
        out = block_bootstrap_delta_ci_diagnostic(
            _paired(ts, rng.normal(-0.01, 0.001, size=240)), block_hours=24, n_reps=150, seed=99,
        )
        self.assertTrue(out["inference_ok"])
        self.assertTrue(out["ci_accounting_valid"])
        self.assertTrue(np.isfinite(out["point"]))
        self.assertTrue(out["ci_low"] <= out["ci_high"])
        self.assertGreater(out["effective_block_count"], 1)

    def test_deterministic_with_fixed_seed(self):
        ts = _ts(120)
        diffs = np.linspace(-0.05, 0.02, 120)
        a = block_bootstrap_delta_ci_diagnostic(_paired(ts, diffs), block_hours=24, n_reps=100, seed=20261109)
        b = block_bootstrap_delta_ci_diagnostic(_paired(ts, diffs), block_hours=24, n_reps=100, seed=20261109)
        self.assertEqual(a, b)


class TestFailingRegimeQlikeInflationGuard(unittest.TestCase):
    def test_identical_predictions_cannot_claim_improvement(self):
        ts = _ts(96)
        diffs = np.zeros(96)
        out = block_bootstrap_delta_ci_diagnostic(_paired(ts, diffs), block_hours=24, n_reps=100, seed=4)
        self.assertIn("constant_finite_diffs", out["regime_flags"])
        self.assertEqual(out["ci_low"], out["ci_high"])
        improvement_claimable = bool(
            out["inference_ok"] and not out["degenerate"] and out["ci_accounting_valid"] and out["ci_low"] < out["ci_high"]
        )
        self.assertFalse(improvement_claimable)

    def test_zero_variance_feature_ablation_no_spurious_qlike_edge(self):
        panel = _panel(["BTCUSDT", "ETHUSDT"])
        train, test = _split(panel)
        train = train.copy()
        test = test.copy()
        train["const_col"] = 3.0
        test["const_col"] = 3.0
        p_base = fit_predict_ols(train, test, BASE)
        p_alt = fit_predict_ols(train, test, BASE + ["const_col"])
        y = test["target_rv"].to_numpy(dtype=float)
        ts = test.index.get_level_values("timestamp")
        paired = paired_qlike_by_time(y, p_base, p_alt, ts)
        if len(paired):
            out = block_bootstrap_delta_ci_diagnostic(
                paired, block_hours=24, n_reps=100, seed=6,
            )
            claimable = bool(
                out["inference_ok"] and not out["degenerate"] and out["ci_accounting_valid"] and out["ci_low"] < out["ci_high"]
            )
            self.assertFalse(claimable)


if __name__ == "__main__":
    unittest.main()
