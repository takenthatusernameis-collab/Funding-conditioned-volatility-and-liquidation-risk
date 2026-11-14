#!/usr/bin/env python3
"""Tests for scripts/fclr_fwd_vol_2025_disjoint_reconcile.py.

Pins the contracts the frozen reconciliation depends on:
  - frozen prereg identity and flag set (frozen before outcomes, not promotable);
  - panel hash and lineage audit (row count, key uniqueness, symbol set, span);
  - the corrupt-day detection and the cleaned-panel build (row/key/lineage);
  - train/test embargo arithmetic and feature causality;
  - finite-row masking (missing stays missing);
  - train-only scaling and train-only smearing (no test information);
  - deterministic bootstrap seed and placebo seed;
  - verdict attribution rule boundaries.

No network. No sealed artifact mutation.
"""
from __future__ import annotations

import json
import sys
import unittest
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
RS = ROOT / "research_state"
sys.path.insert(0, str(ROOT / "scripts"))

import fclr_fwd_vol_2025_disjoint_reconcile as rec  # noqa: E402

PREREG = RS / "prereg_fclr_fwd_vol_2025_disjoint_reconcile_20261114T193000Z.json"
PREREG_MD = RS / "prereg_fclr_fwd_vol_2025_disjoint_reconcile_20261114T193000Z.md"
PANEL = RS / "tracka_fwd_vol_2025_disjoint_cross_panel_20261114T191615Z.parquet"
PANEL_SHA = "de0ca73e7d092a205e5f8c1163d56437384d1b15d65b4a27bc54a57e21738cba"
EVAL_JSON = RS / "evaluation_summary_FCLR-FWD-VOL-2025-DISJOINT-RECONCILE-20261114T193000Z.json"
EVAL_MD = RS / "evaluation_summary_FCLR-FWD-VOL-2025-DISJOINT-RECONCILE-20261114T193000Z.md"


def _read_json(p: Path):
    return json.loads(p.read_text())


class TestFrozenPrereg(unittest.TestCase):
    def test_prereg_exists_and_is_frozen(self):
        self.assertTrue(PREREG.exists(), "frozen reconciliation prereg must exist")
        self.assertTrue(PREREG_MD.exists(), "prereg markdown must exist")
        d = _read_json(PREREG)
        self.assertEqual(d.get("status"), "FROZEN_PRE_OUTCOMES")
        self.assertTrue(d.get("frozen_before_outcomes"))
        self.assertTrue(d.get("pre_registered_before_outcomes"))
        self.assertFalse(d.get("outcome_data_inspected_before_freeze"))
        self.assertFalse(d.get("promotable"))
        self.assertEqual(d.get("max_status"), "EXPLORATORY_ONLY")
        self.assertFalse(d.get("network_required"))
        self.assertEqual(d.get("experiment_id"), rec.EXPERIMENT_ID)

    def test_prereg_pins_panel_hash_and_blocks(self):
        d = _read_json(PREREG)
        self.assertEqual(d["panel"]["sha256"], PANEL_SHA)
        blocks = d["splits"]["blocks"]
        self.assertEqual([b["block"] for b in blocks], [0, 1, 2])
        self.assertEqual(d["splits"]["embargo_days"], 7)
        for b in blocks:
            self.assertLess(b["train_end"], b["test_start"])

    def test_prereg_declares_both_arms(self):
        d = _read_json(PREREG)
        self.assertIn("sealed", d["estimator_arms"])
        self.assertIn("corrected", d["estimator_arms"])
        self.assertIn("existing", d["panel_arms"])
        self.assertIn("cleaned", d["panel_arms"])
        self.assertEqual(d["panel_arms"]["cleaned"]["corrupt_day"], "2025-10-19")
        self.assertEqual(d["panel_arms"]["cleaned"]["corrupt_symbol"], "XRPUSDT")

    def test_assert_prereg_frozen_accepts_the_frozen_file(self):
        rec.assert_prereg_frozen(_read_json(PREREG))

    def test_assert_prereg_frozen_rejects_drift(self):
        d = _read_json(PREREG)
        bad = dict(d)
        bad["frozen_before_outcomes"] = False
        with self.assertRaises(SystemExit):
            rec.assert_prereg_frozen(bad)


class TestPanelIdentityAndLineage(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.panel = pd.read_parquet(PANEL)
        cls.panel["ts"] = pd.to_datetime(cls.panel["ts"])
        cls.lineage = rec.audit_lineage(cls.panel)

    def test_panel_hash_matches_prereg(self):
        self.assertEqual(rec.sha256_file(PANEL), PANEL_SHA)

    def test_lineage_all_pass(self):
        self.assertTrue(self.lineage["all_pass"], json.dumps(
            {k: v for k, v in self.lineage.items() if isinstance(v, bool)}))
        self.assertEqual(self.lineage["row_count"], 30120)
        self.assertEqual(self.lineage["duplicate_keys"], 0)
        self.assertEqual(self.lineage["symbols"], sorted(rec.fwd.SYMBOLS))

    def test_corrupt_day_is_detected_by_value_scale(self):
        self.assertEqual(self.lineage["corrupt_day_rows"], 24)
        self.assertTrue(self.lineage["corrupt_day_all_nonpositive"])
        self.assertTrue((ROOT / rec.CORRUPT_FILE).exists())

    def test_only_one_corrupt_mark_day_in_whole_cache(self):
        cache = RS / "data_cache"
        bad = []
        for sym_dir in sorted(p for p in cache.iterdir() if p.is_dir()):
            for kdir in sorted(sym_dir.glob("markPriceKlines-*")):
                for csv in sorted(kdir.glob("*.csv")):
                    c = pd.read_csv(csv, usecols=["close"])["close"]
                    if (c <= 0).any():
                        bad.append(str(csv.relative_to(ROOT)))
        self.assertEqual(bad, [rec.CORRUPT_FILE])

    def test_per_block_row_counts(self):
        pb = {b["block"]: b for b in self.lineage["per_block"]}
        self.assertEqual(pb[0]["train_rows"], 3600)
        self.assertEqual(pb[1]["train_rows"], 3600)
        self.assertEqual(pb[2]["train_rows"], 3600)
        for b in pb.values():
            self.assertEqual(b["test_rows"] % 5, 0)


class TestCleanedPanelBuild(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.panel = pd.read_parquet(PANEL)
        cls.panel["ts"] = pd.to_datetime(cls.panel["ts"])
        cls.cleaned, cls.report = rec.build_cleaned_panel(cls.panel)

    def test_build_report_checks_pass(self):
        for k, v in self.report["checks"].items():
            self.assertTrue(v, f"cleaned-panel check failed: {k}")
        self.assertEqual(self.report["removed_rows"], 24)
        self.assertFalse(self.report["imputation_used"])
        self.assertFalse(self.report["forward_fill_used"])

    def test_row_and_key_counts(self):
        self.assertEqual(len(self.cleaned), len(self.panel) - 24)
        self.assertEqual(self.cleaned.duplicated(["symbol", "ts"]).sum(), 0)
        self.assertEqual(sorted(self.cleaned["symbol"].unique()), sorted(rec.fwd.SYMBOLS))

    def test_no_nonpositive_mark_remains(self):
        self.assertTrue((self.cleaned["mark"] > 0).all())

    def test_other_symbols_bytewise_unchanged(self):
        a = (self.panel[self.panel["symbol"] != rec.CORRUPT_SYMBOL]
             .sort_values(["symbol", "ts"], kind="stable").reset_index(drop=True))
        b = (self.cleaned[self.cleaned["symbol"] != rec.CORRUPT_SYMBOL]
             .sort_values(["symbol", "ts"], kind="stable").reset_index(drop=True))
        pd.testing.assert_frame_equal(a, b)

    def test_repair_restores_xrp_returns_after_the_removed_day(self):
        x = self.cleaned[self.cleaned["symbol"] == rec.CORRUPT_SYMBOL].sort_values("ts")
        after = x[x["ts"] >= pd.Timestamp("2025-10-20", tz="UTC")]
        self.assertTrue(np.isfinite(after["ret"]).all())
        self.assertTrue(np.isfinite(after["rv24h"].iloc[30:]).all())
        corrupt = x[(x["ts"] >= pd.Timestamp("2025-10-19", tz="UTC"))
                    & (x["ts"] < pd.Timestamp("2025-10-20", tz="UTC"))]
        self.assertEqual(len(corrupt), 0)


class TestEmbargoAndCausality(unittest.TestCase):
    def test_embargo_is_seven_days_and_no_test_leak(self):
        for b in rec.BLOCKS:
            train_end = pd.Timestamp(b["train_end"], tz="UTC")
            test_start = pd.Timestamp(b["test_start"], tz="UTC")
            self.assertEqual((test_start - train_end).days, 7)
            self.assertEqual(rec.EMBARGO_DAYS, 7)

    def test_test_blocks_are_disjoint(self):
        spans = [(pd.Timestamp(b["test_start"], tz="UTC"),
                  pd.Timestamp(b["test_end"], tz="UTC")) for b in rec.BLOCKS]
        spans.sort()
        for (_, e1), (s2, _) in zip(spans, spans[1:]):
            self.assertLess(e1, s2)

    def test_features_are_causal_columns_only(self):
        for cols in rec.fwd.MODEL_FEATURES.values():
            for c in cols:
                self.assertIn(c, rec.CORE_COLS + ["log_rv24h", "signed_funding",
                                                  "abs_fund_pct", "premium", "ema_dist",
                                                  "log_rv1h", "log_rv168h"])
                self.assertNotIn("target", c)


class TestEstimatorArms(unittest.TestCase):
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
        cls.test = cls.train.iloc[:50].copy()

    def test_train_only_scaling_uses_train_moments_only(self):
        fit = rec.fit_corrected(self.train, "C2", 24)
        self.assertEqual(fit["kind"], "corrected")
        self.assertTrue(np.allclose(fit["mu"], self.train[fit["feats"]].values.mean(axis=0)))
        self.assertGreater(fit["smear"], 0.0)

    def test_sealed_arm_has_no_scaling_and_no_smearing(self):
        fit = rec.fit_sealed(self.train, "C2", 24)
        self.assertIsNone(fit["mu"])
        self.assertIsNone(fit["sd"])
        self.assertEqual(fit["smear"], 1.0)

    def test_corrected_predictions_do_not_depend_on_test_rows(self):
        a = rec.predict(rec.fit_corrected(self.train, "C2", 24), self.test)
        scrambled = self.test.sample(frac=1.0, random_state=3)
        b = rec.predict(rec.fit_corrected(self.train, "C2", 24), scrambled)
        self.assertTrue(np.allclose(np.sort(a), np.sort(b), equal_nan=True))

    def test_missing_rows_are_dropped_not_filled(self):
        df = self.test.copy()
        df.loc[df.index[:5], "premium"] = np.nan
        mask = rec.finite_mask(df, rec.CORE_COLS)
        self.assertEqual(int(mask.sum()), len(df) - 5)
        self.assertEqual(int(np.isfinite(df.loc[mask, "premium"]).sum()), len(df) - 5)

    def test_qlike_zero_when_prediction_is_perfect(self):
        y = np.array([1.0, 2.0, 3.0])
        q = rec.qlike(y, y.copy())
        self.assertTrue(np.allclose(q, 0.0))

    def test_qlike_nonnegative(self):
        rng = np.random.default_rng(11)
        y = rng.uniform(0.1, 5.0, 200)
        p = rng.uniform(0.1, 5.0, 200)
        self.assertTrue((rec.qlike(y, p) >= -1e-12).all())


class TestBootstrapDeterminism(unittest.TestCase):
    def setUp(self):
        rng = np.random.default_rng(5)
        self.diffs = rng.normal(size=500)
        self.days = pd.date_range("2025-06-01", periods=500, freq="h").values

    def test_same_seed_same_interval(self):
        a = rec.paired_block_bootstrap(self.diffs, self.days, 200, rec.BOOT_SEED)
        b = rec.paired_block_bootstrap(self.diffs, self.days, 200, rec.BOOT_SEED)
        self.assertEqual(a, b)

    def test_seed_changes_interval(self):
        a = rec.paired_block_bootstrap(self.diffs, self.days, 200, rec.BOOT_SEED)
        c = rec.paired_block_bootstrap(self.diffs, self.days, 200, rec.BOOT_SEED + 1)
        self.assertNotEqual((a["ci_lo"], a["ci_hi"]), (c["ci_lo"], c["ci_hi"]))

    def test_holm_is_monotone_and_bounded(self):
        p = {"a": 0.01, "b": 0.04, "c": 0.5}
        adj = rec.holm(p)
        self.assertLessEqual(adj["a"], adj["b"])
        self.assertLessEqual(adj["b"], adj["c"])
        self.assertTrue(all(0.0 <= v <= 1.0 for v in adj.values()))


class TestVerdictRule(unittest.TestCase):
    def _cells(self, es, ec, cs, cc):
        out = {}
        for panel_name, sealed, corrected in (("existing", es, ec), ("cleaned", cs, cc)):
            for est, val in (("sealed", sealed), ("corrected", corrected)):
                out[f"{panel_name}+{est}"] = {"primary": {"rel_reduction_pct": val}}
        return out

    def test_explained_by_estimator(self):
        v, _ = rec.determine_verdict(self._cells(-1.0, -5.0, -1.2, -5.2))
        self.assertEqual(v, "EXPLAINED_BY_ESTIMATOR")

    def test_explained_by_data(self):
        v, _ = rec.determine_verdict(self._cells(-1.0, -1.2, -5.0, -5.2))
        self.assertEqual(v, "EXPLAINED_BY_DATA")

    def test_unexplained_for_mixed_swing(self):
        v, _ = rec.determine_verdict(self._cells(-3.165, -1.963, -5.396, -3.269))
        self.assertEqual(v, "UNEXPLAINED")

    def test_inconclusive_when_a_cell_is_missing(self):
        v, _ = rec.determine_verdict(self._cells(-1.0, None, -1.2, -1.3))
        self.assertEqual(v, "INCONCLUSIVE")

    def test_frozen_result_is_unexplained(self):
        d = _read_json(EVAL_JSON)
        self.assertEqual(d["verdict"], "UNEXPLAINED")
        self.assertEqual(d["status"], "VALID_EXPLORATORY")
        self.assertFalse(d["promotable"])
        self.assertAlmostEqual(d["cells"]["existing+corrected"]["primary"]["rel_reduction_pct"],
                               -1.9633752428119817, places=10)


class TestEmittedArtifacts(unittest.TestCase):
    def test_evaluation_files_exist(self):
        self.assertTrue(EVAL_JSON.exists())
        self.assertTrue(EVAL_MD.exists())

    def test_evaluation_records_prereg_hash_and_lineage(self):
        d = _read_json(EVAL_JSON)
        self.assertTrue(d["prereg_sha256"])
        self.assertTrue(d["lineage_audit"]["all_pass"])
        self.assertEqual(d["lineage_audit"]["corrupt_day_rows"], 24)

    def test_evaluation_has_four_cells(self):
        d = _read_json(EVAL_JSON)
        self.assertEqual(set(d["cells"]), {"existing+sealed", "existing+corrected",
                                          "cleaned+sealed", "cleaned+corrected"})
        for name, c in d["cells"].items():
            self.assertEqual(c["status"], "VALID_EXPLORATORY", name)
            self.assertEqual(len(c["instruments"]), 5, name)
            self.assertEqual(len(c["per_block"]), 3, name)

    def test_cleaned_panel_artifact_matches_report_hash(self):
        d = _read_json(EVAL_JSON)
        rep = d["cleaned_panel_report"]
        p = RS / Path(rep["panel_path"]).name
        self.assertTrue(p.exists())
        self.assertEqual(rec.sha256_file(p), rep["panel_sha256"])
        self.assertEqual(rep["row_count"], 30096)


if __name__ == "__main__":
    unittest.main()