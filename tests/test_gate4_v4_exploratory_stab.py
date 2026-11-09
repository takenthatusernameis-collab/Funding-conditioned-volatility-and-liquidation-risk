"""Tests for Gate 4 v4 EXPLORATORY stabilized comparison (synthetic, no network)."""
from __future__ import annotations

import json
import sys
import unittest
from pathlib import Path

import numpy as np
import pandas as pd

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO))

from scripts.run_gate4_v4_exploratory_stab import (  # noqa: E402
    LABEL,
    fit_predict_variant,
    make_interpretation,
    train_only_winsor,
)


def _toy():
    idx = pd.date_range("2024-04-01", periods=80, freq="h", tz="UTC")
    rng = np.random.default_rng(7)
    parts = []
    for sym in ["BTCUSDT", "ETHUSDT"]:
        rv = np.abs(rng.normal(0.0015, 0.0004, len(idx))) + 1e-5
        df = pd.DataFrame({
            "rv_trail_24": rv, "rv_trail_168": rv * 1.02, "rv_trail_6": rv * 0.98,
            "funding_signed": rng.normal(0, 0.0001, len(idx)),
            "funding_abs": np.abs(rng.normal(0, 0.0001, len(idx))),
            "funding_pct_24": rng.normal(0, 1, len(idx)), "funding_pct_72": rng.normal(0, 1, len(idx)),
            "funding_pct_168": rng.normal(0, 1, len(idx)), "funding_z_24": rng.normal(0, 1, len(idx)),
            "funding_z_72": rng.normal(0, 1, len(idx)), "funding_z_168": rng.normal(0, 1, len(idx)),
            "target_rv": rv * (1.0 + 0.05 * rng.normal(0, 1, len(idx))).clip(0.2, 5),
        }, index=pd.MultiIndex.from_product([[sym], idx], names=["symbol", "timestamp"]))
        parts.append(df)
    panel = pd.concat(parts).sort_index()
    # Split by time (first 40 hours for train, last 40 for test) for each symbol
    split_ts = idx[40]
    train = panel.loc[panel.index.get_level_values("timestamp") < split_ts]
    test = panel.loc[panel.index.get_level_values("timestamp") >= split_ts]
    return train, test


class TestGate4V4ExploratoryStab(unittest.TestCase):
    def test_label_exploratory(self):
        self.assertIn("EXPLORATORY", LABEL)
        self.assertIn("NOT CONFIRMATORY", LABEL)
        self.assertIn("NOT PROMOTABLE", LABEL)

    def test_train_only_winsor_uses_train_bounds(self):
        rng = np.random.default_rng(0)
        Xtr = rng.normal(0, 1, (200, 3))
        Xte = rng.normal(0, 5, (50, 3))
        Xtrw, Xtew, meta = train_only_winsor(Xtr, Xte, 0.05, 0.95)
        self.assertEqual(meta["bounds_from"], "train_only")
        lo = np.nanquantile(Xtr, 0.05, axis=0)
        hi = np.nanquantile(Xtr, 0.95, axis=0)
        self.assertTrue(np.all(Xtew >= lo - 1e-12))
        self.assertTrue(np.all(Xtew <= hi + 1e-12))

    def test_v1_primary_floors_at_zero(self):
        train, test = _toy()
        fcols = ["rv_trail_24", "rv_trail_168", "rv_trail_6"]
        p, diags = fit_predict_variant(train, test, fcols, "V1_primary")
        fin = p[np.isfinite(p)]
        self.assertTrue((fin >= 0).all())
        ok = [d for d in diags if d["status"] == "OK"]
        self.assertTrue(ok)
        self.assertIn("1e-10", ok[0]["ridge_rule"])

    def test_v3_applies_train_only_target_floor(self):
        train, test = _toy()
        fcols = ["rv_trail_24", "rv_trail_168", "rv_trail_6", "funding_signed"]
        p, diags = fit_predict_variant(train, test, fcols, "V3_scale_ridge_target_floor")
        fin = p[np.isfinite(p)]
        self.assertTrue((fin > 0).all())
        ok = [d for d in diags if d["status"] == "OK"][0]
        self.assertIn("train_target_median", ok["floor_rule"])
        self.assertIn("trace(XtX)/k", ok["ridge_rule"])

    def test_v4_winsor_meta_present(self):
        train, test = _toy()
        fcols = ["rv_trail_24", "rv_trail_168", "rv_trail_6", "funding_signed"]
        _, diags = fit_predict_variant(train, test, fcols, "V4_winsor_train")
        ok = [d for d in diags if d["status"] == "OK"][0]
        self.assertIsNotNone(ok["winsor"])
        self.assertEqual(ok["winsor"]["bounds_from"], "train_only")

    def test_make_interpretation_exploratory_nogo_signal(self):
        payload = {
            "variants": {
                "V1_primary": {"contrasts_vs_A": {"E_rv_funding_trails": {"point": 0.5, "ci_low": -0.1, "ci_high": 1.0}, "B_rv_signed": {"point": 10, "ci_low": 1, "ci_high": 20}}, "split_results": [{"split_id": 3, "ablations": {"B_rv_signed": {"metrics": {"qlike": 45.0}}}}]},
                "V3_scale_ridge_target_floor": {"contrasts_vs_A": {"E_rv_funding_trails": {"point": 0.4, "ci_low": -0.2, "ci_high": 0.9}, "B_rv_signed": {"point": 2.0, "ci_low": -1, "ci_high": 5}}, "split_results": [{"split_id": 3, "ablations": {"B_rv_signed": {"metrics": {"qlike": 3.0}}}}]},
            },
            "loo_e_vs_a_v3": {"all": {"point": 0.4, "ci_low": -0.2, "ci_high": 0.9}, "drop_BTCUSDT": {"point": 0.1, "ci_low": -0.1, "ci_high": 0.3}},
        }
        txt = make_interpretation(payload)
        self.assertIn("EXPLORATORY", txt)
        self.assertIn("not confirmatory", txt.lower())


if __name__ == "__main__":
    unittest.main()
