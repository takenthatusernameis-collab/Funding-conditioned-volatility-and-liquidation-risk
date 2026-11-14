#!/usr/bin/env python3
import hashlib
import json
import sys
import unittest
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
RS = ROOT / "research_state"
sys.path.insert(0, str(ROOT / "scripts"))

import fclr_fwd_vol_2024_disjoint_2024_06 as d24  # noqa: E402

PREREG = RS / "prereg_fclr_fwd_vol_2024_disjoint_2024_06_20261114T231100Z.json"
PREREG_MD = RS / "prereg_fclr_fwd_vol_2024_disjoint_2024_06_20261114T231100Z.md"


class TestFrozenPrereg(unittest.TestCase):
    def test_prereg_frozen_and_identity(self):
        self.assertTrue(PREREG.exists())
        self.assertTrue(PREREG_MD.exists())
        d = json.loads(PREREG.read_text())
        self.assertEqual(d["experiment_id"], d24.EXPERIMENT_ID)
        self.assertEqual(d["status"], "FROZEN_PRE_OUTCOMES")
        self.assertTrue(d["frozen_before_outcomes"])
        self.assertFalse(d["outcome_data_inspected_before_freeze"])
        self.assertFalse(d["status_rule"]["promotable"])
        self.assertEqual(d["status_rule"]["max_status"], "EXPLORATORY_ONLY")
        self.assertEqual(d["universe"]["symbols"], d24.SYMBOLS)
        b = d["splits"]["blocks"][0]
        self.assertEqual(b["train_start"], "2024-04-25T00:00:00Z")
        self.assertEqual(b["train_end"], "2024-05-24T23:00:00Z")
        self.assertEqual(b["test_start"], "2024-06-01T00:00:00Z")
        self.assertEqual(b["test_end"], "2024-06-30T23:00:00Z")
        self.assertEqual(d["splits"]["embargo_days"], 7)
        self.assertIn("sealed", d["estimator_arms"])
        self.assertIn("corrected", d["estimator_arms"])


class TestPanelBuild(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        panels = [d24.build_symbol(sym, d24.DATA_START, d24.BUFFER_END) for sym in d24.SYMBOLS]
        cls.panel = pd.concat(panels, ignore_index=True).sort_values(["symbol", "ts"]).reset_index(drop=True)
        cls.panel["ts"] = pd.to_datetime(cls.panel["ts"], utc=True)

    def test_panel_shape_and_keys(self):
        self.assertEqual(len(self.panel), 5 * len(pd.date_range(d24.DATA_START, d24.BUFFER_END, freq="1h", tz="UTC")))
        self.assertEqual(self.panel.duplicated(["symbol", "ts"]).sum(), 0)
        self.assertEqual(set(self.panel["symbol"].unique()), set(d24.SYMBOLS))
        self.assertEqual(self.panel["ts"].min(), d24.DATA_START)
        self.assertEqual(self.panel["ts"].max(), d24.BUFFER_END)

    def test_lineage_and_leakage_checks(self):
        lin = d24.lineage_check(self.panel)
        self.assertTrue(lin["pass"], lin)
        self.assertTrue(lin["per_cell_nonzero"])
        leak = d24.leakage_audit(self.panel)
        self.assertTrue(leak["pass"], leak)
        self.assertTrue(leak["embargo_enforced"])
        self.assertEqual(leak["embargo_days"], 7)

    def test_finite_row_masking_drop_only(self):
        train, test = d24.split_panel(self.panel)
        cols = d24.MODEL_FEATURES["C2"] + ["target_24h"]
        m = d24.finite_mask(train, cols)
        self.assertEqual(m.dtype, bool)
        self.assertTrue(m.sum() > 0)
        # rows with any non-finite excluded
        sub = train[~m]
        if len(sub):
            self.assertFalse(np.isfinite(sub[cols].values).all(axis=1).all())

    def test_train_only_scaling_and_smearing(self):
        train, test = d24.split_panel(self.panel)
        cols = d24.MODEL_FEATURES["C2"] + ["target_24h"]
        tr = train[d24.finite_mask(train, cols)].copy()
        te = test[d24.finite_mask(test, cols)].copy()
        fit_c = d24.fit_corrected(tr, d24.MODEL_FEATURES["C2"])
        self.assertIsNotNone(fit_c["mu"])
        self.assertIsNotNone(fit_c["sd"])
        self.assertGreater(fit_c["smear"], 0.0)
        self.assertTrue(np.allclose(fit_c["mu"], tr[d24.MODEL_FEATURES["C2"]].values.mean(axis=0)))
        fit_s = d24.fit_sealed(tr, d24.MODEL_FEATURES["C2"])
        self.assertIsNone(fit_s["mu"])
        self.assertEqual(fit_s["smear"], 1.0)
        # mutating test must not change corrected fit params (train-only)
        te2 = te.copy()
        te2[d24.MODEL_FEATURES["C2"]] = te2[d24.MODEL_FEATURES["C2"]] * 999.0
        fit_c2 = d24.fit_corrected(tr, d24.MODEL_FEATURES["C2"])
        self.assertTrue(np.allclose(fit_c["mu"], fit_c2["mu"]))
        self.assertTrue(np.allclose(fit_c["smear"], fit_c2["smear"]))


class TestDeterminismAndVerdict(unittest.TestCase):
    def test_bootstrap_deterministic(self):
        rng = np.random.default_rng(0)
        days = pd.date_range("2024-06-01", periods=10, freq="D", tz="UTC")
        rows = []
        for d in days:
            for i in range(20):
                rows.append({"ts": d + pd.Timedelta(hours=i), "symbol": "BTCUSDT", "diff": float(rng.normal()), "qb": 1.0})
        M = pd.DataFrame(rows)
        a = d24.bootstrap_diff(M, reps=50, seed=d24.BOOT_SEED)
        b = d24.bootstrap_diff(M, reps=50, seed=d24.BOOT_SEED)
        c = d24.bootstrap_diff(M, reps=50, seed=d24.BOOT_SEED + 1)
        self.assertEqual(a["ci_lo"], b["ci_lo"])
        self.assertEqual(a["mean_diff"], b["mean_diff"])
        self.assertNotEqual(a["ci_lo"], c["ci_lo"])

    def test_decide_verdict_rules(self):
        lin = {"pass": True}
        leak = {"pass": True}
        # estimator swing
        res = {
            "sealed": {"primary": {"rel_reduction_pct": -1.0, "n": 10}},
            "corrected": {"primary": {"rel_reduction_pct": 2.5, "n": 10}},
        }
        self.assertEqual(d24.decide_verdict(res, lin, leak), "EXPLAINED_BY_ESTIMATOR")
        # unexplained when consistent
        res2 = {
            "sealed": {"primary": {"rel_reduction_pct": -1.0, "n": 10}},
            "corrected": {"primary": {"rel_reduction_pct": -0.5, "n": 10}},
        }
        self.assertEqual(d24.decide_verdict(res2, lin, leak), "UNEXPLAINED")
        # inconclusive on bad lineage
        self.assertEqual(d24.decide_verdict(res2, {"pass": False}, leak), "INCONCLUSIVE")
        self.assertEqual(d24.decide_verdict(res2, lin, {"pass": False}), "INCONCLUSIVE")


if __name__ == "__main__":
    unittest.main()
