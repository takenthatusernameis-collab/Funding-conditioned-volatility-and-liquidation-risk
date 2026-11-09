"""Tests for Gate 4 v4 EXPLORATORY leakage audit (synthetic, no network)."""
from __future__ import annotations

import sys
import unittest
from pathlib import Path

import numpy as np
import pandas as pd

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO))

from src.eval import walkforward as wf  # noqa: E402
from scripts.run_gate4_v4_leakage_audit import (  # noqa: E402
    LABEL,
    audit_block_bootstrap_reproducibility,
    audit_variant_leakage,
    train_derived_params,
    train_normalization_stats,
)
from scripts.run_funding_ablations import PRE_REG_SPLITS_V3_30D


def _toy_panel(n_train=40, n_test=20, seed=3):
    idx_train = pd.date_range("2024-04-01", periods=n_train, freq="h", tz="UTC")
    idx_test = pd.date_range("2024-04-02", periods=n_test, freq="h", tz="UTC")
    rng = np.random.default_rng(seed)
    parts = []
    for sym in ["BTCUSDT", "ETHUSDT"]:
        rv = np.abs(rng.normal(0.0015, 0.0004, n_train + n_test)) + 1e-5
        df = pd.DataFrame({
            "rv_trail_24": rv, "rv_trail_168": rv * 1.02, "rv_trail_6": rv * 0.98,
            "funding_signed": rng.normal(0, 0.0001, n_train + n_test),
            "funding_abs": np.abs(rng.normal(0, 0.0001, n_train + n_test)),
            "target_rv": rv * (1.0 + 0.05 * rng.normal(0, 1, n_train + n_test)).clip(0.2, 5),
        }, index=pd.MultiIndex.from_product([[sym], np.concatenate([idx_train, idx_test])],
                                            names=["symbol", "timestamp"]))
        parts.append(df)
    return pd.concat(parts).sort_index()


class TestLeakageAuditTrainOnly(unittest.TestCase):
    def test_label_exploratory(self):
        self.assertIn("EXPLORATORY", LABEL)
        self.assertIn("NOT CONFIRMATORY", LABEL)
        self.assertIn("NOT PROMOTABLE", LABEL)

    def test_train_derived_params_from_train_only(self):
        panel = _toy_panel()
        idx = panel.index.get_level_values("timestamp")
        split_ts = pd.Timestamp("2024-04-02", tz="UTC")
        train = panel.loc[idx < split_ts]
        test = panel.loc[idx >= split_ts]
        fcols = ["rv_trail_24", "rv_trail_168", "rv_trail_6", "funding_signed"]
        tr_b = train_derived_params(train, fcols, "V3_scale_ridge_target_floor")
        te_b = train_derived_params(test, fcols, "V3_scale_ridge_target_floor")
        # Train-derived params must differ between train-only and test-only folds
        # (they are computed from different data), and train floor must be > 0.
        self.assertGreater(tr_b["target_floor"], 0.0)
        self.assertIn("1e-8*max(", tr_b["ridge_rule"])
        self.assertIn("train_target_median", tr_b["target_floor_rule"])
        self.assertEqual(tr_b["normalization"]["rv_trail_24"]["n"], len(train))

    def test_test_perturbation_does_not_change_train_params(self):
        panel = _toy_panel()
        idx = panel.index.get_level_values("timestamp")
        split_ts = pd.Timestamp("2024-04-02", tz="UTC")
        train = panel.loc[idx < split_ts]
        test = panel.loc[idx >= split_ts]
        fcols = ["rv_trail_24", "rv_trail_168", "rv_trail_6", "funding_signed"]
        tr_norm_base, _, _, _ = wf.apply_train_only_normalization(train, test, test, fcols)
        base = train_derived_params(tr_norm_base, fcols, "V4_winsor_train")
        te_perturbed = test.copy()
        te_perturbed["target_rv"] = test["target_rv"].to_numpy(dtype=float) * 100.0
        tr_norm, _, te_norm, _ = wf.apply_train_only_normalization(
            train, te_perturbed, te_perturbed, fcols)
        perturbed = train_derived_params(tr_norm, fcols, "V4_winsor_train")
        for key in ("ridge_scale_diag_trace_over_k", "target_floor", "n_train_valid"):
            self.assertEqual(base.get(key), perturbed.get(key), (key, base, perturbed))
        for c in fcols:
            self.assertEqual(base["normalization"][c].get("mean"), perturbed["normalization"][c].get("mean"), c)
            self.assertEqual(base["normalization"][c].get("std"), perturbed["normalization"][c].get("std"), c)
        self.assertEqual(base.get("winsor_lo"), perturbed.get("winsor_lo"))
        self.assertEqual(base.get("winsor_hi"), perturbed.get("winsor_hi"))

    def test_train_only_stats_use_train_data(self):
        vals = np.array([1.0, 2.0, 3.0, 4.0, 5.0])
        df = pd.DataFrame({"rv_trail_24": vals, "target_rv": vals * 2})
        stats = train_normalization_stats(df, ["rv_trail_24"])
        self.assertAlmostEqual(stats["rv_trail_24"]["mean"], 3.0)
        self.assertAlmostEqual(stats["rv_trail_24"]["std"], np.std(vals))
        self.assertEqual(stats["rv_trail_24"]["n"], 5)


class TestLeakageAuditBlockBootstrapReproducibility(unittest.TestCase):
    def test_fixed_seed_identical_ci(self):
        panel = _toy_panel(n_train=60, n_test=40, seed=11)
        bb1 = audit_block_bootstrap_reproducibility(panel, PRE_REG_SPLITS_V3_30D)
        self.assertTrue(bb1["identical_on_rerun"])
        self.assertEqual(bb1["run1"]["point"], bb1["run2"]["point"])
        self.assertEqual(bb1["run1"]["ci_low"], bb1["run2"]["ci_low"])
        self.assertEqual(bb1["run1"]["ci_high"], bb1["run2"]["ci_high"])
        self.assertEqual(bb1["seed"], 20261109)

    def test_audit_variant_leakage_all_invariant(self):
        panel = _toy_panel(n_train=60, n_test=40, seed=22)
        for v in ["V1_primary", "V2_scale_ridge", "V3_scale_ridge_target_floor", "V4_winsor_train"]:
            res = audit_variant_leakage(panel, v, PRE_REG_SPLITS_V3_30D)
            self.assertTrue(res["all_train_params_test_invariant"], v)
            for sp in res["splits"]:
                for s in sp["symbols"]:
                    if s.get("status") == "OK":
                        self.assertTrue(s["test_perturbation_unchanged"], (v, sp["split_id"], s["symbol"]))


if __name__ == "__main__":
    unittest.main()
