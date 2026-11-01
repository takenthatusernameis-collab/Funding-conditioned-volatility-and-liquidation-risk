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
        # Normalize symbol for merge (panel symbols are like BTC-PERP)
        if funding_df is not None and not funding_df.empty:
            fund = funding_df.copy()
            # Ensure columns
            if 'hour' not in fund.columns and 'timestamp' in fund.columns:
                fund['hour'] = pd.to_datetime(fund['timestamp'], utc=True).dt.floor('h')
            # Map symbol
            if 'symbol_hl' not in fund.columns and 'coin' in fund.columns:
                fund['symbol_hl'] = fund['coin'].astype(str) + '-PERP'
            elif 'symbol' not in fund.columns and 'symbol_hl' in fund.columns:
                fund['symbol'] = fund['symbol_hl']
            # Aggregate to hourly if multiple per hour (Hyperliquid funding is typically once per interval; but just in case take last/mean)
            if 'hour' in fund.columns and 'symbol' in fund.columns and 'funding_rate' in fund.columns:
                fund_agg = fund.groupby(['symbol', 'hour'])['funding_rate'].mean().reset_index()
                panel = panel.merge(fund_agg, on=['symbol', 'hour'], how='left')
                panel['funding_rate'] = panel['funding_rate'].fillna(np.nan)
            else:
                panel['funding_rate'] = np.nan
        else:
            panel['funding_rate'] = np.nan

        # Compute derived features
        panel['funding_sign'] = np.sign(panel['funding_rate'].fillna(0.0))
        panel['funding_abs'] = panel['funding_rate'].abs()
        # Z-score by symbol, rolling window 90 days worth of hours ~ 2160, but use reasonable window with min_periods
        def _zscore(x):
            x = x.copy()
            # compute rolling zscore
            m = x.rolling(window=2160, min_periods=30).mean()
            s = x.rolling(window=2160, min_periods=30).std()
            z = (x - m) / s.replace(0, np.nan)
            return z
        try:
            panel['funding_zscore'] = panel.groupby('symbol')['funding_rate'].transform(lambda x: _zscore(x))
        except Exception:
            panel['funding_zscore'] = np.nan
        return panel

    def add_volatility_features(self, panel: pd.DataFrame, price_df: pd.DataFrame = None) -> pd.DataFrame:
        panel = panel.copy()
        if 'liq_count' in panel.columns:
            panel['rv_proxy'] = panel.groupby('symbol')['liq_count'].transform(lambda x: x.rolling(24, min_periods=1).std())
        else:
            panel['rv_proxy'] = 0.0
        try:
            panel['rv_proxy'] = panel['rv_proxy'].fillna(0)
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
        for col in panel.columns:
            if hasattr(panel[col], 'dtype') and panel[col].dtype.name == 'category':
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
            if hasattr(panel[col], 'dtype') and panel[col].dtype.name == 'category':
                panel[col] = panel[col].astype(object)
        return panel.fillna(0)
