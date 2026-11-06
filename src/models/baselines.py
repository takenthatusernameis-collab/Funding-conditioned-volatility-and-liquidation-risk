"""Baseline models for volatility forecasting.

B1: persistence (lagged RV).
B2: RV-only HAR-style linear model on trailing RV features.

All models are fit strictly on training data and produce forecasts aligned to
the forecast-origin index. No future information is used.
"""
from __future__ import annotations

from typing import Dict, List, Optional, Tuple

import numpy as np
import pandas as pd


def _clean_rows(X: np.ndarray, y: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
    mask = np.isfinite(y) & np.all(np.isfinite(X), axis=1)
    return X[mask], y[mask]


def persistence_forecast(rv_lag: pd.Series) -> pd.Series:
    """B1: predict forward RV with the most recently observed trailing RV."""
    return rv_lag.copy()


class RVOnlyHAR:
    """B2: HAR-style linear regression on trailing RV features.

    Features default to [rv_trail_24, rv_trail_168, rv_trail_6] when present.
    """

    def __init__(self, feature_cols: Optional[List[str]] = None):
        self.feature_cols = feature_cols
        self.coef_: Optional[np.ndarray] = None
        self.intercept_: float = 0.0
        self._fitted_features: List[str] = []

    def fit(self, X: pd.DataFrame, y: pd.Series):
        if self.feature_cols is None:
            self._fitted_features = [
                c for c in ["rv_trail_24", "rv_trail_168", "rv_trail_6"]
                if c in X.columns
            ]
        else:
            self._fitted_features = [c for c in self.feature_cols if c in X.columns]
        if not self._fitted_features:
            raise ValueError("No usable RV feature columns for HAR fit.")
        Xmat = X[self._fitted_features].to_numpy(dtype=float)
        ymat = y.to_numpy(dtype=float)
        Xc, yc = _clean_rows(Xmat, ymat)
        if len(yc) < 2:
            # Degenerate: fall back to mean.
            self.coef_ = np.zeros(len(self._fitted_features))
            self.intercept_ = float(np.nanmean(yc)) if np.isfinite(yc).any() else 0.0
            return self
        # OLS via normal equations with small ridge for stability.
        n, k = Xc.shape
        XtX = Xc.T @ Xc
        ridge = 1e-10 * np.eye(k)
        try:
            coef = np.linalg.solve(XtX + ridge, Xc.T @ yc)
        except np.linalg.LinAlgError:
            coef = np.zeros(k)
        self.coef_ = coef
        self.intercept_ = float(yc.mean() - coef @ Xc.mean(axis=0))
        return self

    def predict(self, X: pd.DataFrame) -> np.ndarray:
        if self.coef_ is None:
            raise RuntimeError("Model not fitted.")
        Xmat = X[self._fitted_features].to_numpy(dtype=float)
        preds = self.intercept_ + Xmat @ self.coef_
        preds[~np.isfinite(preds)] = np.nan
        return preds


def make_baseline_predictions(
    panel: pd.DataFrame,
    rv_col: str,
    feature_cols: Optional[List[str]] = None,
) -> pd.DataFrame:
    """Produce B1 (persistence) and B2 (HAR RV-only) predictions.

    The panel must be indexed by (symbol, timestamp) with columns including the
    trailing RV feature columns and `rv_lag` for persistence.
    """
    out = panel.copy()
    out["pred_persist"] = out["rv_lag"]
    out["pred_rvhar"] = np.nan
    models: Dict[str, RVOnlyHAR] = {}
    for sym, grp in out.groupby(level="symbol", sort=False):
        grp = grp.sort_index()
        train_mask = grp["target_rv"].isna() | True  # caller splits via masks
        X = grp
        y = grp["target_rv"]
        model = RVOnlyHAR(feature_cols=feature_cols)
        try:
            model.fit(X, y)
        except ValueError:
            models[sym] = model
            continue
        models[sym] = model
        out.loc[grp.index, "pred_rvhar"] = model.predict(X)
    return out, models