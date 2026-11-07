"""Tests for Gate 4 multi-split, leakage-resistant funding ablations.

Guards (P0, no network, fixture-friendly where possible):
- Pre-registered 3-split walk-forward with purge/embargo and train-only normalization
- Block bootstrap ΔQLIKE CI is deterministic (seeded) and resamples UTC time blocks jointly
- A_rv_only regression remains stable on the original single-split Gate 3 setup
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
    PRE_REG_SPLITS,
    PURGE_DAYS,
    EMBARGO_DAYS,
    BOOTSTRAP_SEED,
    BOOTSTRAP_REPS,
    add_funding_to_panel,
    block_bootstrap_delta_ci,
    build_prereg_splits,
    fit_predict_ols,
    load_funding_panel,
    load_kline_panel,
    paired_qlike_by_time,
    run_multisplit,
)
from src.eval.walkforward import _in_window, apply_train_only_normalization  # noqa: E402
from src.volatility import eval as veval  # noqa: E402

SYMBOLS = ["BTCUSDT", "ETHUSDT", "SOLUSDT", "XRPUSDT"]
BASE = ["rv_trail_24", "rv_trail_168", "rv_trail_6"]
LEGACY_SPLIT_TRAIN = ("2024-01-01T00:00:00+00:00", "2024-02-01T00:00:00+00:00")
LEGACY_SPLIT_TEST = ("2024-02-22T00:00:00+00:00", "2024-03-31T00:00:00+00:00")
GATE3_A_QLIKE = 1.5954100026198477


def _panel():
    kpanel = load_kline_panel(SYMBOLS, "2024-01-01", "2024-03-31", horizon=24)
    fpanel = load_funding_panel(SYMBOLS, "2024-01-01", "2024-03-31")
    return add_funding_to_panel(kpanel, fpanel)


class TestFundingMultisplit(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.panel = _panel()

    def test_prereg_splits_chronological_with_purge_embargo(self):
        splits = build_prereg_splits()
        self.assertEqual(len(splits), 3)
        for i, sp in enumerate(splits):
            self.assertEqual(sp.purge_days, PURGE_DAYS)
            self.assertEqual(sp.embargo_days, EMBARGO_DAYS)
            train_end = pd.Timestamp(PRE_REG_SPLITS[i]["train"][1])
            test_start = pd.Timestamp(PRE_REG_SPLITS[i]["test"][0])
            gap = test_start - train_end
            self.assertGreaterEqual(gap, pd.Timedelta(days=PURGE_DAYS - 1))
            self.assertEqual(sp.test, PRE_REG_SPLITS[i]["test"])
        idx = self.panel.index.get_level_values("timestamp")
        for s in PRE_REG_SPLITS:
            self.assertGreater(_in_window(idx, s["train"]).sum(), 0)
            self.assertGreater(_in_window(idx, s["test"]).sum(), 0)

    def test_multisplit_runs_and_reports_per_split(self):
        panel = self.panel
        ablations = {"A_rv_only": BASE, "B_rv_signed": BASE + ["funding_signed"]}
        res, pooled = run_multisplit(panel, ablations)
        ok = [r for r in res if r.get("status") == "OK"]
        self.assertEqual(len(ok), 3)
        for r in ok:
            self.assertIn("ablations", r)
            for ab in ablations:
                self.assertIn(ab, r["ablations"])
                self.assertIn("qlike", r["ablations"][ab])
                self.assertIsNotNone(r["ablations"][ab]["qlike"])
        self.assertIn("B_rv_signed", pooled)
        self.assertGreater(len(pooled["B_rv_signed"]), 0)

    def test_a_rv_only_legacy_gate3_regression_stable(self):
        panel = self.panel
        idx = panel.index.get_level_values("timestamp")
        train = panel.loc[_in_window(idx, LEGACY_SPLIT_TRAIN)]
        test = panel.loc[_in_window(idx, LEGACY_SPLIT_TEST)]
        train_n, _, test_n, _ = apply_train_only_normalization(train, test, test, BASE)
        p = fit_predict_ols(train_n, test_n, BASE)
        y = test_n["target_rv"].to_numpy(dtype=float)
        ql = veval.qlike(y.tolist(), p.tolist())
        self.assertIsNotNone(ql)
        self.assertAlmostEqual(ql, GATE3_A_QLIKE, places=6)

    def test_block_bootstrap_ci_deterministic(self):
        ts = pd.date_range("2024-02-05", periods=240, freq="h", tz="UTC")
        rng = np.random.default_rng(7)
        y = np.abs(rng.normal(0.001, 0.0002, size=(240, 3))) + 1e-6
        pb = y + rng.normal(0, 0.00005, size=y.shape)
        pa = pb - 0.00001
        parts = []
        for sym_i in range(3):
            t = pd.DatetimeIndex(ts)
            df = pd.DataFrame({"timestamp": t, "ql_base": np.abs(pb[:, sym_i]), "ql_alt": np.abs(pa[:, sym_i])})
            df["diff"] = df["ql_alt"] - df["ql_base"]
            parts.append(df[["timestamp", "ql_base", "ql_alt", "diff"]])
        paired = pd.concat(parts, ignore_index=True)
        a = block_bootstrap_delta_ci(paired, block_hours=24, n_reps=200, seed=BOOTSTRAP_SEED)
        b = block_bootstrap_delta_ci(paired, block_hours=24, n_reps=200, seed=BOOTSTRAP_SEED)
        c = block_bootstrap_delta_ci(paired, block_hours=24, n_reps=200, seed=BOOTSTRAP_SEED + 1)
        self.assertEqual(a["point"], b["point"])
        self.assertEqual(a["ci_low"], b["ci_low"])
        self.assertEqual(a["ci_high"], b["ci_high"])
        self.assertEqual(a["n_reps"], 200)
        self.assertGreater(a["n_blocks"], 1)
        self.assertEqual(c["n_reps"], 200)
        # different seed may coincide on this synthetic sample; determinism is the invariant

    def test_block_bootstrap_resamples_time_blocks_jointly(self):
        # two instruments share timestamps; per timestamp block appears together
        ts = pd.date_range("2024-02-05", periods=48, freq="h", tz="UTC")
        rows = []
        for sym in ["A", "B"]:
            for i, t in enumerate(ts):
                rows.append({"timestamp": t, "ql_base": 1.0 + 0.01 * i, "ql_alt": 0.9 + 0.01 * i, "diff": -0.1})
        paired = pd.DataFrame(rows)
        ci = block_bootstrap_delta_ci(paired, block_hours=24, n_reps=100, seed=123)
        self.assertAlmostEqual(ci["point"], -0.1, places=12)
        self.assertAlmostEqual(ci["ci_low"], -0.1, places=12)
        self.assertAlmostEqual(ci["ci_high"], -0.1, places=12)
        self.assertEqual(ci["n_blocks"], 2)


if __name__ == "__main__":
    unittest.main()
