"""Tests for the funding-conditioned volatility ablation pipeline.

These tests guard against two regressions found in scripts/run_funding_ablations.py:

1. Duplicate column creation in add_funding_to_panel. The per-symbol feature
   frames were concatenated with axis=1, producing multiple columns with the
   same name (one per symbol). Joining that onto the kline panel produced
   DataFrame-valued columns, which broke TrainOnlyScaler.fit (it compared a
   DataFrame against a scalar -> "truth value ambiguous").

2. Log-target ridge regression. Fitting log(target) and exponentiating the
   prediction is unstable for this target distribution: a few extreme
   normalized test features produce astronomically large positive forecasts,
   which dominate QLIKE and make the RV-only baseline look like QLIKE ~ 3e5.
   The validated Gate 3 baseline uses direct-variance OLS, so the ablation
   pipeline must use the same model form to be comparable.
"""
from __future__ import annotations

import sys
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


def test_no_duplicate_columns_after_funding_merge():
    panel = _panel()
    funding_cols = [c for c in panel.columns if c.startswith("funding_")]
    assert funding_cols, "expected funding columns to be present"
    # Every column name must appear exactly once. Duplicate names produced
    # DataFrame-valued columns that broke normalization.
    assert len(funding_cols) == len(set(funding_cols)), (
        f"duplicate funding columns: {[c for c in funding_cols if funding_cols.count(c) > 1]}"
    )


def test_rv_only_baseline_reproduces_validated_gate3_value():
    """A_rv_only must reproduce the validated Gate 3 RV-only baseline exactly.

    Prior to the fix, the log-target ridge produced QLIKE ~ 333293, which is
    not a meaningful forecast metric. Direct-variance OLS reproduces the
    validated Gate 3 value of 1.5954.
    """
    panel = _panel()
    train, test = _split(panel)
    train_n, _, test_n, _ = apply_train_only_normalization(train, test, test, BASE)
    p = fit_predict_ols(train_n, test_n, BASE)
    y = test_n["target_rv"].to_numpy(dtype=float)
    ql = veval.qlike(y.tolist(), p.tolist())
    assert ql is not None
    assert 1.0 < ql < 3.0, f"QLIKE {ql} outside plausible range for RV-only baseline"
    # Exact validated value from Gate 3 (run_rv_baseline.py).
    assert abs(ql - 1.5954100026198477) < 1e-6


def test_funding_ablations_run_without_error():
    panel = _panel()
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


def test_predictions_are_bounded():
    """Direct-variance OLS must not produce astronomically large forecasts.

    The log-target ridge produced predictions up to ~4e11 for a target whose
    max observed value is ~0.02. That is a model-form bug, not a data feature.
    """
    panel = _panel()
    train, test = _split(panel)
    train_n, _, test_n, _ = apply_train_only_normalization(train, test, test, BASE)
    p = fit_predict_ols(train_n, test_n, BASE)
    finite = p[np.isfinite(p)]
    assert finite.size > 0
    assert finite.max() < 1.0, f"max prediction {finite.max()} far exceeds target scale"
    assert finite.min() >= 0.0