#!/usr/bin/env python3
from pathlib import Path
from typing import Dict

import numpy as np
import pandas as pd

class LiqMicroFeatures:
    def __init__(self):
        pass

    def add_funding_features(self, panel: pd.DataFrame, funding_df: pd.DataFrame = None) -> pd.DataFrame:
        panel = panel.copy()
        if funding_df is not None and not funding_df.empty:
            pass
        else:
            panel['funding_rate'] = 0.0
            panel['funding_sign'] = 0
            panel['funding_abs'] = 0.0
            panel['funding_zscore'] = 0.0
        return panel

    def add_volatility_features(self, panel: pd.DataFrame, price_df: pd.DataFrame = None) -> pd.DataFrame:
        panel = panel.copy()
        if 'liq_count' in panel.columns:
            panel['rv_proxy'] = panel.groupby('symbol')['liq_count'].transform(lambda x: x.rolling(24, min_periods=1).std())
        else:
            panel['rv_proxy'] = 0.0
        try:
            panel['rv_proxy'] = panel['rv_proxy'].fillna(0)
            # Create terciles without categorical issues
            panel['rv_tercile'] = 2
            try:
                ranks = panel.groupby(panel['hour'].dt.date)['rv_proxy'].transform(lambda x: x.rank(method='first'))
                terciles = pd.qcut(ranks, q=3, labels=False, duplicates='drop') + 1
                panel['rv_tercile'] = terciles.fillna(2).astype(int)
            except Exception:
                pass
        except Exception:
            panel['rv_tercile'] = 2
        return panel

    def add_lag_features(self, panel: pd.DataFrame) -> pd.DataFrame:
        panel = panel.copy().sort_values(['symbol', 'hour'])
        for lag in [1, 4, 24]:
            if 'liq_count' in panel.columns:
                panel[f'liq_count_lag{lag}h'] = panel.groupby('symbol')['liq_count'].shift(lag)
        # Fill NaN safely
        for col in panel.columns:
            if panel[col].dtype.name == 'category':
                panel[col] = panel[col].astype(object)
        panel = panel.fillna(0)
        return panel

    def add_clustering_features(self, panel: pd.DataFrame) -> pd.DataFrame:
        panel = panel.copy().sort_values(['symbol', 'hour'])
        if 'liq_count' in panel.columns:
            try:
                panel['liq_ar1'] = panel.groupby('symbol')['liq_count'].transform(
                    lambda x: x.rolling(48, min_periods=10).apply(lambda y: y.autocorr(lag=1) if len(y.dropna()) > 5 else 0, raw=False)
                )
            except Exception:
                panel['liq_ar1'] = 0.0
        for col in panel.columns:
            if panel[col].dtype.name == 'category':
                panel[col] = panel[col].astype(object)
        return panel.fillna(0)
