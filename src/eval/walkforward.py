"""Leakage-resistant walk-forward evaluation for volatility forecasts.

Splits are chronological. Purge/embargo separate train from test to prevent
autocorrelation bleed. Normalization is train-only. No random splits.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Dict, List, Optional, Tuple

import numpy as np
import pandas as pd

from src.volatility.feature_engineering import TrainOnlyScaler
from src.volatility.eval import qlike, mae, mse


def parse_iso(s: str) -> datetime:
    if s.endswith("Z"):
        s = s[:-1] + "+00:00"
    dt = datetime.fromisoformat(s)
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return dt


@dataclass
class SplitBounds:
    train: Tuple[str, str]
    validation: Tuple[str, str]
    test: Tuple[str, str]
    purge_days: int = 7
    embargo_days: int = 7


def _expand_bounds(bounds: Tuple[str, str], days: int) -> Tuple[datetime, datetime]:
    lo = parse_iso(bounds[0])
    hi = parse_iso(bounds[1])
    return lo, hi


def build_walkforward_splits(
    start: str,
    end: str,
    train_months: int = 6,
    val_months: int = 2,
    test_months: int = 2,
    purge_days: int = 7,
    embargo_days: int = 7,
) -> List[SplitBounds]:
    """Construct overlapping chronological walk-forward splits.

    The window slides forward in test-month steps. Each split has train/val/test
    with purge/embargo gaps.
    """
    lo = parse_iso(start)
    hi = parse_iso(end)
    splits: List[SplitBounds] = []
    t_train_end = lo + pd.DateOffset(months=train_months)
    t_val_end = t_train_end + pd.DateOffset(months=val_months)
    t_test_end = t_val_end + pd.DateOffset(months=test_months)
    while t_test_end <= hi:
        train_start = lo
        train_end = t_train_end - pd.Timedelta(days=purge_days)
        val_start = t_train_end + pd.Timedelta(days=embargo_days)
        val_end = t_val_end - pd.Timedelta(days=purge_days)
        test_start = t_val_end + pd.Timedelta(days=embargo_days)
        test_end = t_test_end
        splits.append(SplitBounds(
            train=(train_start.isoformat(), train_end.isoformat()),
            validation=(val_start.isoformat(), val_end.isoformat()),
            test=(test_start.isoformat(), test_end.isoformat()),
            purge_days=purge_days,
            embargo_days=embargo_days,
        ))
        # slide
        lo = t_test_end
        t_train_end = lo + pd.DateOffset(months=train_months)
        t_val_end = t_train_end + pd.DateOffset(months=val_months)
        t_test_end = t_val_end + pd.DateOffset(months=test_months)
    return splits


def _in_window(ts: pd.DatetimeIndex, bounds: Tuple[str, str]) -> np.ndarray:
    lo, hi = _expand_bounds(bounds, 0)
    return (ts >= lo) & (ts <= hi)


def apply_train_only_normalization(
    train: pd.DataFrame,
    val: pd.DataFrame,
    test: pd.DataFrame,
    feature_cols: List[str],
) -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, Dict[str, TrainOnlyScaler]]:
    scalers: Dict[str, TrainOnlyScaler] = {}
    train_out = train.copy()
    val_out = val.copy()
    test_out = test.copy()
    for col in feature_cols:
        sc = TrainOnlyScaler()
        sc.fit(train[col].to_numpy(dtype=float))
        scalers[col] = sc
        train_out[col] = sc.transform(train[col].to_numpy(dtype=float))
        val_out[col] = sc.transform(val[col].to_numpy(dtype=float))
        test_out[col] = sc.transform(test[col].to_numpy(dtype=float))
    return train_out, val_out, test_out, scalers


def evaluate_split(
    panel: pd.DataFrame,
    split: SplitBounds,
    feature_cols: List[str],
    horizon: int,
) -> Dict[str, object]:
    """Run one walk-forward split: fit RV-only HAR on train, predict test."""
    idx = panel.index.get_level_values("timestamp")
    train_mask = _in_window(idx, split.train)
    val_mask = _in_window(idx, split.validation)
    test_mask = _in_window(idx, split.test)
    train = panel.loc[train_mask]
    val = panel.loc[val_mask]
    test = panel.loc[test_mask]
    if train.empty or test.empty:
        return {"status": "INSUFFICIENT_DATA", "n_test": int(test_mask.sum())}
    train_n, val_n, test_n, _ = apply_train_only_normalization(
        train, val, test, feature_cols
    )
    from src.models.baselines import RVOnlyHAR

    preds: Dict[str, pd.Series] = {}
    models: Dict[str, object] = {}
    test_out = test_n.copy()
    test_out["pred_persist"] = test_n["rv_lag"]
    test_out["pred_rvhar"] = np.nan
    for sym, grp in test_n.groupby(level="symbol", sort=False):
        train_sym = train_n.loc[train_n.index.get_level_values("symbol") == sym]
        if len(train_sym) < 10:
            continue
        Xtr = train_sym[feature_cols]
        ytr = train_sym["target_rv"]
        m = RVOnlyHAR(feature_cols=feature_cols)
        try:
            m.fit(Xtr, ytr)
        except Exception:
            continue
        models[sym] = m
        Xte = grp[feature_cols]
        test_out.loc[grp.index, "pred_rvhar"] = m.predict(Xte)
    y = test_out["target_rv"].to_numpy(dtype=float)
    p_persist = test_out["pred_persist"].to_numpy(dtype=float)
    p_har = test_out["pred_rvhar"].to_numpy(dtype=float)
    out: Dict[str, object] = {
        "status": "OK",
        "n_test": int(test_mask.sum()),
        "n_train": int(train_mask.sum()),
        "test_window": (split.test[0], split.test[1]),
        "metrics": {
            "persist": {
                "qlike": qlike(y.tolist(), p_persist.tolist()),
                "mae": mae(y.tolist(), p_persist.tolist()),
                "rmse": float(np.sqrt(mse(y.tolist(), p_persist.tolist()) or np.nan)),
            },
            "rvhar": {
                "qlike": qlike(y.tolist(), p_har.tolist()),
                "mae": mae(y.tolist(), p_har.tolist()),
                "rmse": float(np.sqrt(mse(y.tolist(), p_har.tolist()) or np.nan)),
            },
        },
        "n_models": len(models),
    }
    return out