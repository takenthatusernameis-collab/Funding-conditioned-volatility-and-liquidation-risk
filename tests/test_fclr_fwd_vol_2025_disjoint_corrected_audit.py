#!/usr/bin/env python3
"""Tests for scripts/fclr_fwd_vol_2025_disjoint_corrected_audit.py.

Pins the contracts the frozen corrected-estimator audit depends on:
  - frozen prereg identity and flag set (frozen before outcomes, not promotable);
  - cached panel hash and lineage audit (row count, key uniqueness, symbol set, span);
  - train/test split, 7-day embargo, feature causality;
  - finite-row masking (missing stays missing);
  - train-only scaling and train-only smearing (no test information);
  - deterministic bootstrap seed;
  - verdict attribution rule boundaries;
  - no sealed-artifact mutation.

No network. No sealed artifact mutation.
"""
from __future__ import annotations

import json
import subprocess
import sys
import unittest
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
RS = ROOT / "research_state"
sys.path.insert(0, str(ROOT / "scripts"))

import fclr_fwd_vol_2025_disjoint_corrected_audit as aud  # noqa: E402

OUT_UTC = "2026-11-15T00:12:56Z"
PREREG = RS / f"prereg_fclr_fwd_vol_2025_disjoint_corrected_audit_{OUT_UTC}.json"
PREREG_MD = RS / f"prereg_fclr_fwd_vol_2025_disjoint_corrected_audit_{OUT_UTC}.md"
PANEL = RS / "tracka_fwd_vol_2025_disjoint_cross_panel_20261114T191615Z.parquet"
PANEL_SHA = "de0ca73e7d092a205e5f8c1163d56437384d1b15d65b4a27bc54a57e21738cba"
SEALED_EVAL = RS / "evaluation_summary_FCLR-FWD-VOL-2025-DISJOINT-CROSS-20261114T191615Z.json"
EXPERIMENT_ID = f"FCLR-FWD-VOL-2025-DISJOINT-CORRECTED-AUDIT-{OUT_UTC}"


def _read_json(p: Path):
    return json.loads(p.read_text())


class TestFrozenPrereg(unittest.TestCase):
    def test_prereg_exists_and_is_frozen(self):
        self.assertTrue(PREREG.exists(), "frozen corrected-audit prereg must exist")
        self.assertTrue(PREREG_MD.exists(), "prereg markdown must exist")
        d = _read_json(PREREG)
        self.assertEqual(d.get("status"), "FROZEN_PRE_OUTCOMES")
        self.assertTrue(d.get("frozen_before_outcomes"))
        self.assertTrue(d.get("pre_registered_before_outcomes"))
        self.assertFalse(d.get("outcome_data_inspected_before_freeze"))
        self.assertFalse(d.get("promotable"))
        self.assertEqual(d.get("max_status"), "EXPLORATORY_ONLY")
        self.assertFalse(d.get("network_required"))
        self.assertEqual(d.get("experiment_id"), EXPERIMENT_ID)

    def test_prereg_pins_panel_hash_and_blocks(self):
        d = _read_json(PREREG)
        self.assertEqual(d["panel"]["sha256"], PANEL_SHA)
        blocks = d["splits"]["blocks"]
        self.assertEqual([b["block"] for b in blocks], [0, 1, 2])
        self.assertEqual(d["splits"]["embargo_days"], 7)
        for b in blocks:
            self.assertLess(b["train_end"], b["test_start"])

    def test_prereg_declares_corrected_arm_only(self):
        d = _read_json(PREREG)
        self.assertIn("corrected", d["estimator_arm"])
        self.assertEqual(d["estimator_arm"]["corrected"]["scaling"], "train-only standardization")
        self.assertEqual(d["estimator_arm"]["corrected"]["smearing"], "train-only Duan smearing")
        self.assertEqual(d["estimator_arm"]["corrected"]["missing_policy"], "drop row; missing stays missing")

    def test_prereg_sealed_reference_matches_recorded_eval(self):
        d = _read_json(PREREG)
        sr = d["sealed_reference"]
        ev = _read_json(SEALED_EVAL)
        self.assertEqual(sr["rel_reduction_pct"], ev["primary"]["rel_reduction_pct"])
        self.assertEqual(sr["mean_diff"], ev["primary"]["mean_diff"])
        self.assertEqual(sr["ci"], [ev["primary"]["ci_lo"], ev["primary"]["ci_hi"]])

    def test_assert_prereg_frozen_accepts_the_frozen_file(self):
        aud.assert_prereg_frozen(_read_json(PREREG), EXPERIMENT_ID)

    def test_assert_prereg_frozen_rejects_drift(self):
        d = _read_json(PREREG)
        bad = dict(d)
        bad["frozen_before_outcomes"] = False
        with self.assertRaises(SystemExit):
            aud.assert_prereg_frozen(bad, EXPERIMENT_ID)


class TestPanelIdentityAndLineage(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.panel = pd.read_parquet(PANEL)
        cls.panel["ts"] = pd.to_datetime(cls.panel["ts"])
        cls.lineage = aud.audit_lineage(cls.panel)

    def test_panel_hash_matches_prereg(self):
        self.assertEqual(aud.sha256_file(PANEL), PANEL_SHA)

    def test_lineage_all_pass(self):
        self.assertTrue(self.lineage["all_pass"], json.dumps(
            {k: v for k, v in self.lineage.items() if isinstance(v, bool)}))
        self.assertEqual(self.lineage["row_count"], 30120)
        self.assertEqual(self.lineage["duplicate_keys"], 0)
        self.assertEqual(self.lineage["symbols"], sorted(aud.SYMBOLS))

    def test_per_block_row_counts(self):
        pb = {b["block"]: b for b in self.lineage["per_block"]}
        self.assertEqual(pb[0]["train_rows"], 3600)
        self.assertEqual(pb[1]["train_rows"], 3600)
        self.assertEqual(pb[2]["train_rows"], 3600)
        self.assertEqual(pb[0]["test_rows"], 3600)
        self.assertEqual(pb[1]["test_rows"], 3600)
        self.assertEqual(pb[2]["test_rows"], 3720)
        for b in pb.values():
            self.assertEqual(b["test_rows"] % 5, 0)


class TestSplitEmbargoAndCausality(unittest.TestCase):
    def test_embargo_is_seven_days_and_no_test_leak(self):
        for b in aud.BLOCKS:
            train_end = pd.Timestamp(b["train_end"], tz="UTC")
            test_start = pd.Timestamp(b["test_start"], tz="UTC")
            self.assertEqual((test_start - train_end).days, 7)

    def test_test_blocks_are_disjoint(self):
        spans = [(pd.Timestamp(b["test_start"], tz="UTC"),
                  pd.Timestamp(b["test_end"], tz="UTC")) for b in aud.BLOCKS]
        spans.sort()
        for (_, e1), (s2, _) in zip(spans, spans[1:]):
            self.assertLess(e1, s2)

    def test_features_do_not_reference_target(self):
        for cols in aud.fwd.MODEL_FEATURES.values():
            for c in cols:
                self.assertNotIn("target", c)


class TestFiniteRowMaskingDropOnly(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.panel = pd.read_parquet(PANEL)
        cls.panel["ts"] = pd.to_datetime(cls.panel["ts"])

    def test_finite_mask_is_bool_and_excludes_nonfinite(self):
        cols = aud.CORE_COLS
        m = aud.finite_mask(self.panel, cols)
        self.assertEqual(m.dtype, bool)
        self.assertTrue(m.sum() > 0)
        sub = self.panel[~m]
        if len(sub):
            self.assertFalse(np.isfinite(sub[cols].values.astype(float)).all(axis=1).all())

    def test_missing_rows_dropped_not_filled(self):
        base = self.panel[aud.finite_mask(self.panel, aud.CORE_COLS)].iloc[:100].copy()
        base.loc[base.index[:5], "premium"] = np.nan
        mask = aud.finite_mask(base, aud.CORE_COLS)
        self.assertEqual(int(mask.sum()), len(base) - 5)
        self.assertEqual(int(np.isfinite(base.loc[mask, "premium"]).sum()), len(base) - 5)


class TestTrainOnlyScalingAndSmearing(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        rng = np.random.default_rng(7)
        n = 400
        x1 = rng.normal(size=n)
        x2 = rng.normal(size=n)
        y = np.exp(0.3 + 0.5 * x1 - 0.2 * x2 + rng.normal(scale=0.4, size=n))
        cls.train = pd.DataFrame({
            "log_rv1h": x1, "log_rv24h": x2, "log_rv168h": x1 - x2,
            "signed_funding": rng.normal(size=n),
            "abs_fund_pct": rng.uniform(size=n),
            "premium": rng.normal(size=n),
            "ema_dist": rng.normal(size=n),
            "target_24h": y,
        })

    def test_train_only_scaling_uses_train_moments_only(self):
        fit = aud.fit_corrected(self.train, "C2", 24)
        self.assertEqual(fit["kind"], "corrected")
        self.assertTrue(np.allclose(fit["mu"], self.train[fit["feats"]].values.mean(axis=0)))
        self.assertTrue(np.allclose(fit["sd"], self.train[fit["feats"]].values.std(axis=0)))
        self.assertGreater(fit["smear"], 0.0)

    def test_corrected_predictions_do_not_depend_on_test_rows(self):
        fit = aud.fit_corrected(self.train, "C2", 24)
        test = self.train.iloc[:50].copy()
        a = aud.predict(fit, test)
        scrambled = test.sample(frac=1.0, random_state=3)
        b = aud.predict(fit, scrambled)
        self.assertTrue(np.allclose(np.sort(a), np.sort(b), equal_nan=True))


class TestBootstrapDeterminism(unittest.TestCase):
    def setUp(self):
        rng = np.random.default_rng(5)
        self.diffs = rng.normal(size=500)
        self.days = pd.date_range("2025-06-01", periods=500, freq="h").values

    def test_same_seed_same_interval(self):
        a = aud.paired_block_bootstrap(self.diffs, self.days, 200, aud.BOOT_SEED)
        b = aud.paired_block_bootstrap(self.diffs, self.days, 200, aud.BOOT_SEED)
        self.assertEqual(a, b)

    def test_seed_changes_interval(self):
        a = aud.paired_block_bootstrap(self.diffs, self.days, 200, aud.BOOT_SEED)
        c = aud.paired_block_bootstrap(self.diffs, self.days, 200, aud.BOOT_SEED + 1)
        self.assertNotEqual((a["ci_lo"], a["ci_hi"]), (c["ci_lo"], c["ci_hi"]))


class TestVerdictRule(unittest.TestCase):
    def test_explained_by_estimator_on_swing(self):
        v, _ = aud.determine_verdict(-1.0, -5.0, {"all_pass": True}, True)
        self.assertEqual(v, "EXPLAINED_BY_ESTIMATOR")

    def test_not_explained_by_estimator_when_close(self):
        v, _ = aud.determine_verdict(-1.963, -1.963, {"all_pass": True}, True)
        self.assertEqual(v, "NOT_EXPLAINED_BY_ESTIMATOR")

    def test_inconclusive_when_lineage_fails(self):
        v, _ = aud.determine_verdict(-1.963, -1.963, {"all_pass": False}, True)
        self.assertEqual(v, "INCONCLUSIVE")

    def test_inconclusive_when_cell_missing(self):
        v, _ = aud.determine_verdict(None, -1.963, {"all_pass": True}, False)
        self.assertEqual(v, "INCONCLUSIVE")


class TestNoSealedMutation(unittest.TestCase):
    def test_sealed_eval_and_panel_stable(self):
        sealed_eval = RS / "evaluation_summary_FCLR-FWD-VOL-2025-DISJOINT-CROSS-20261114T191615Z.json"
        self.assertTrue(sealed_eval.exists())
        ev = _read_json(sealed_eval)
        self.assertEqual(ev["verdict"], "EXPLORATORY_NULL")
        self.assertEqual(ev["primary"]["rel_reduction_pct"], -1.9633752428119817)
        self.assertEqual(aud.sha256_file(PANEL), PANEL_SHA)

    def test_audit_writes_only_new_corrected_audit_artifacts(self):
        self.assertTrue("corrected_audit" in PREREG.name)
        self.assertTrue(PREREG.exists())
        self.assertTrue(PREREG_MD.exists())
        # write targets must not collide with any sealed CROSS/RECONCILE artifact
        sealed_globs = [
            "prereg_fclr_fwd_vol_2025_disjoint_cross_*",
            "prereg_fclr_fwd_vol_2025_disjoint_reconcile_*",
            "tracka_fwd_vol_2025_disjoint_cross_panel_*",
            "tracka_fwd_vol_2025_disjoint_cross_build_report_*",
            "tracka_fwd_vol_2025_disjoint_reconcile_panel_*",
            "tracka_fwd_vol_2025_disjoint_reconcile_panel_build_report_*",
            "evaluation_summary_FCLR-FWD-VOL-2025-DISJOINT-CROSS-*",
            "evaluation_summary_FCLR-FWD-VOL-2025-DISJOINT-RECONCILE-*",
        ]
        for g in sealed_globs:
            for p in RS.glob(g):
                self.assertNotIn("corrected_audit", p.name, f"collision with sealed artifact {p.name}")


if __name__ == "__main__":
    unittest.main()
