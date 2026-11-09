"""Unit tests for hardened block-bootstrap/inference diagnostics.

Synthetic only: no network, no real research_state writes.
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

from scripts.run_funding_ablations import block_bootstrap_delta_ci  # noqa: E402
from src.eval.inference import block_bootstrap_delta_ci_diagnostic  # noqa: E402


def _paired(ts, diffs, *, copies=1):
    parts = []
    for c in range(copies):
        t = pd.DatetimeIndex(ts) + pd.Timedelta(minutes=c)
        df = pd.DataFrame({"timestamp": t, "ql_base": 1.0, "ql_alt": 1.0 + np.asarray(diffs, dtype=float), "diff": np.asarray(diffs, dtype=float)})
        parts.append(df[["timestamp", "ql_base", "ql_alt", "diff"]])
    return pd.concat(parts, ignore_index=True)


class TestEvalInferenceDiagnostics(unittest.TestCase):
    def test_rejects_non_finite_diffs_and_reports_accounting(self):
        ts = pd.date_range("2024-02-05", periods=96, freq="h", tz="UTC")
        diffs = np.full(96, -0.1)
        diffs[5] = np.nan
        diffs[9] = np.inf
        diffs[12] = -np.inf
        out = block_bootstrap_delta_ci(_paired(ts, diffs, copies=2), block_hours=24, n_reps=120, seed=123)
        self.assertIn("n_obs_nonfinite", out)
        self.assertGreaterEqual(out["n_obs_nonfinite"], 3)
        self.assertEqual(out["n_obs_finite"], 93 * 2)
        self.assertTrue(np.isfinite(out["point"]))
        self.assertTrue(out["ci_accounting_valid"])
        self.assertIn("effective_block_count", out)
        self.assertEqual(out["effective_block_count"], out["n_blocks"])
        self.assertNotIn("all_diffs_non_finite", out["regime_flags"])

    def test_flags_too_few_blocks_and_degenerate_regime(self):
        ts = pd.date_range("2024-02-05", periods=6, freq="h", tz="UTC")
        diffs = np.array([-0.2, -0.2, -0.2, -0.2, -0.2, -0.2])
        out = block_bootstrap_delta_ci(_paired(ts, diffs), block_hours=24, n_reps=80, seed=7)
        self.assertLess(out["n_blocks"], 3)
        self.assertIn("too_few_blocks", out["regime_flags"])
        self.assertTrue(out["degenerate"])
        self.assertFalse(out["inference_ok"])
        self.assertAlmostEqual(out["point"], -0.2, places=12)

    def test_flags_no_finite_blocks(self):
        ts = pd.date_range("2024-02-05", periods=24, freq="h", tz="UTC")
        diffs = np.full(24, np.nan)
        out = block_bootstrap_delta_ci_diagnostic(_paired(ts, diffs), block_hours=24, n_reps=50, seed=1)
        self.assertIn("no_finite_blocks", out["regime_flags"])
        self.assertIn("all_diffs_non_finite", out["regime_flags"])
        self.assertTrue(out["degenerate"])
        self.assertIsNone(out["point"])
        self.assertFalse(out["ci_accounting_valid"])

    def test_reports_effective_block_count_and_legacy_fields(self):
        ts = pd.date_range("2024-02-05", periods=240, freq="h", tz="UTC")
        rng = np.random.default_rng(11)
        diffs = rng.normal(-0.01, 0.001, size=240)
        out = block_bootstrap_delta_ci(_paired(ts, diffs, copies=2), block_hours=24, n_reps=150, seed=99)
        for k in ("point", "ci_low", "ci_high", "n_obs", "n_blocks", "n_reps", "seed", "block_hours"):
            self.assertIn(k, out)
        self.assertGreater(out["effective_block_count"], 1)
        self.assertEqual(out["n_reps"], 150)
        self.assertEqual(out["seed"], 99)
        self.assertIn("regime_flags", out)
        self.assertTrue(out["ci_low"] <= out["ci_high"])

    def test_deterministic_with_fixed_seed(self):
        ts = pd.date_range("2024-02-05", periods=120, freq="h", tz="UTC")
        diffs = np.linspace(-0.05, 0.02, 120)
        a = block_bootstrap_delta_ci(_paired(ts, diffs, copies=2), block_hours=24, n_reps=100, seed=20261109)
        b = block_bootstrap_delta_ci(_paired(ts, diffs, copies=2), block_hours=24, n_reps=100, seed=20261109)
        self.assertEqual(a["point"], b["point"])
        self.assertEqual(a["ci_low"], b["ci_low"])
        self.assertEqual(a["ci_high"], b["ci_high"])
        self.assertEqual(a["effective_block_count"], b["effective_block_count"])
        self.assertEqual(a["regime_flags"], b["regime_flags"])


if __name__ == "__main__":
    unittest.main()
