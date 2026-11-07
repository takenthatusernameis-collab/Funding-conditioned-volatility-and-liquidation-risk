"""Tests for the funding-conditioned volatility ablation pipeline.

These tests guard against regressions in scripts/run_funding_ablations.py:

1. Direct-variance OLS (not log-target ridge) matching the validated Gate 3
   RV-only baseline (QLIKE ~ 1.5954).
2. Funding alignment uses last-known value at/before each hour (no future
   leakage); trailing funding statistics are past-only.
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
    add_funding_to_panel,
    fit_predict_ols,
    load_funding_panel,
    load_kline_panel,
)
from src.eval.walkforward import (  # noqa: E402
    SplitBounds,
    _in_window,
    apply_train_only_normalization,
)
from src.features import funding as ff  # noqa: E402
from src.volatility import eval as veval  # noqa: E402

SYMBOLS = ["BTCUSDT", "ETHUSDT", "SOLUSDT", "XRPUSDT"]
BASE = ["rv_trail_24", "rv_trail_168", "rv_trail_6"]
SPLIT = SplitBounds(
    train=("2024-01-01T00:00:00+00:00", "2024-02-01T00:00:00+00:00"),
    validation=("2024-02-09T00:00:00+00:00", "2024-02-15T00:00:00+00:00"),
    test=("2024-02-22T00:00:00+00:00", "2024-03-31T00:00:00+00:00"),
    purge_days=7,
    embargo_days=7,
)


def _panel():
    kpanel = load_kline_panel(SYMBOLS, "2024-01-01", "2024-03-31", horizon=24)
    fpanel = load_funding_panel(SYMBOLS, "2024-01-01", "2024-03-31")
    return add_funding_to_panel(kpanel, fpanel)


def _split(panel):
    idx = panel.index.get_level_values("timestamp")
    train = panel.loc[_in_window(idx, SPLIT.train)]
    test = panel.loc[_in_window(idx, SPLIT.test)]
    return train, test


class TestFundingAblations(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.panel = _panel()

    def test_no_duplicate_columns_after_funding_merge(self):
        panel = self.__class__.panel
        funding_cols = [c for c in panel.columns if c.startswith("funding_")]
        assert funding_cols, "expected funding columns to be present"
        assert len(funding_cols) == len(set(funding_cols)), (
            f"duplicate funding columns: {[c for c in funding_cols if funding_cols.count(c) > 1]}"
        )

    def test_rv_only_baseline_reproduces_validated_gate3_value(self):
        """A_rv_only must reproduce the validated Gate 3 RV-only baseline exactly."""
        panel = self.__class__.panel
        train, test = _split(panel)
        train_n, _, test_n, _ = apply_train_only_normalization(train, test, test, BASE)
        p = fit_predict_ols(train_n, test_n, BASE)
        y = test_n["target_rv"].to_numpy(dtype=float)
        ql = veval.qlike(y.tolist(), p.tolist())
        assert ql is not None
        assert 1.0 < ql < 3.0, f"QLIKE {ql} outside plausible range for RV-only baseline"
        assert abs(ql - 1.5954100026198477) < 1e-6

    def test_funding_ablations_run_without_error(self):
        panel = self.__class__.panel
        train, test = _split(panel)
        trail = [c for c in panel.columns if c.startswith(("funding_pct_", "funding_z_"))]
        ablations = {
            "A_rv_only": BASE[:],
            "B_rv_signed": BASE + ["funding_signed"],
            "C_rv_abs": BASE + ["funding_abs"],
            "D_rv_signed_abs": BASE + ["funding_signed", "funding_abs"],
            "E_rv_funding_trails": BASE + ["funding_signed", "funding_abs"] + trail,
        }
        for name, fcols in ablations.items():
            fcols = [c for c in fcols if c in panel.columns]
            train_n, _, test_n, _ = apply_train_only_normalization(train, test, test, fcols)
            p = fit_predict_ols(train_n, test_n, fcols)
            y = test_n["target_rv"].to_numpy(dtype=float)
            m = veval.qlike(y.tolist(), p.tolist())
            assert m is not None, f"{name}: QLIKE was None"
            assert np.isfinite(m), f"{name}: QLIKE not finite ({m})"

    def test_predictions_are_bounded(self):
        """Direct-variance OLS must not produce astronomically large forecasts."""
        panel = self.__class__.panel
        train, test = _split(panel)
        train_n, _, test_n, _ = apply_train_only_normalization(train, test, test, BASE)
        p = fit_predict_ols(train_n, test_n, BASE)
        finite = p[np.isfinite(p)]
        assert finite.size > 0
        assert finite.min() >= 0.0, f"min prediction {finite.min()} is negative"
        assert finite.max() < 1.0, f"max prediction {finite.max()} far exceeds target scale"

    def test_funding_alignment_no_future_leakage(self):
        """A kline at time t must only see funding observed at or before t."""
        kindex = pd.DatetimeIndex([
            pd.Timestamp("2024-01-01T00:00:00", tz="UTC"),
            pd.Timestamp("2024-01-01T01:00:00", tz="UTC"),
            pd.Timestamp("2024-01-01T02:00:00", tz="UTC"),
        ])
        fdf = pd.DataFrame(
            {"last_funding_rate": [0.001, 0.002]},
            index=pd.DatetimeIndex([
                pd.Timestamp("2024-01-01T00:00:00", tz="UTC"),
                pd.Timestamp("2024-01-01T02:30:00", tz="UTC"),
            ]),
        )
        aligned = ff.resample_funding_to_hourly(fdf, kindex)
        vals = aligned.tolist()
        assert vals[0] == 0.001
        assert vals[1] == 0.001, f"t=01:00 must not see 02:30 funding, got {vals[1]}"
        assert vals[2] == 0.001, f"t=02:00 must not see 02:30 funding, got {vals[2]}"

    def test_trailing_funding_pct_is_past_only(self):
        """trailing_funding_pct must use only past observations (no lookahead)."""
        s = pd.Series([0.0, 0.1, 0.2, 0.3, 0.4], index=pd.RangeIndex(5))
        pct = ff.trailing_funding_pct(s, window=3)
        assert pct.iloc[2] == 1.0
        assert pct.iloc[3] == 1.0
        assert pd.isna(pct.iloc[0]) and pd.isna(pct.iloc[1])
