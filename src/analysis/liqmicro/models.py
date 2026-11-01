#!/usr/bin/env python3
from typing import Dict, Tuple

import numpy as np
import pandas as pd
import statsmodels.api as sm
from statsmodels.formula.api import ols

class LiqMicroModels:
    def __init__(self):
        pass

    def d1_funding_asymmetry(self, panel: pd.DataFrame) -> Dict:
        results = {}
        # Test funding sign effect on liquidation asymmetry
        try:
            # Create long/short ratio if both exist
            if 'liq_count_long' in panel.columns and 'liq_count_short' in panel.columns:
                panel = panel.copy()
                panel['ls_ratio'] = (panel['liq_count_long'] + 1e-9) / (panel['liq_count_short'] + 1e-9)
                panel['funding_sign'] = np.sign(panel.get('funding_rate', 0))
                # Simple regression
                for h in [1, 2, 4]:
                    panel[f'ls_ratio_fwd{h}'] = panel.groupby('symbol')['ls_ratio'].shift(-h)
                # Try regression
                df_reg = panel.dropna(subset=['ls_ratio_fwd1'])
                if len(df_reg) > 100:
                    X = pd.get_dummies(df_reg['funding_sign'], prefix='fsign')
                    X = sm.add_constant(X)
                    y = df_reg['ls_ratio_fwd1']
                    try:
                        model = sm.OLS(y, X).fit(cov_type='cluster', cov_kwds={'groups': df_reg['symbol']})
                        results['d1_h1'] = {
                            'coef': model.params.to_dict(),
                            'pvalues': model.pvalues.to_dict(),
                            'nobs': int(model.nobs)
                        }
                    except:
                        pass
        except Exception as e:
            results['error'] = str(e)
        return results

    def d2_vol_interaction(self, panel: pd.DataFrame) -> Dict:
        results = {}
        try:
            panel = panel.copy()
            panel['funding_abs'] = np.abs(panel.get('funding_rate', 0))
            # Create interaction
            if 'rv_tercile' in panel.columns:
                df_reg = panel.dropna()
                if len(df_reg) > 100:
                    # Simple OLS with interaction
                    formula = 'liq_count ~ funding_abs * C(rv_tercile) + liq_count_lag1h'
                    try:
                        model = ols(formula, data=df_reg).fit(cov_type='cluster', cov_kwds={'groups': df_reg['symbol']})
                        results['d2'] = {
                            'params': model.params.to_dict(),
                            'pvalues': model.pvalues.to_dict(),
                            'nobs': int(model.nobs)
                        }
                    except:
                        pass
        except Exception as e:
            results['error'] = str(e)
        return results

    def d3_clustering(self, panel: pd.DataFrame) -> Dict:
        results = {}
        try:
            panel = panel.copy()
            panel['funding_abs'] = np.abs(panel.get('funding_rate', 0))
            # Bin by funding abs deciles
            try:
                panel['funding_decile'] = pd.qcut(panel['funding_abs'], q=10, labels=False, duplicates='drop')
            except:
                panel['funding_decile'] = 5
            # Compare clustering
            if 'liq_ar1' in panel.columns:
                clustering_by_decile = panel.groupby('funding_decile')['liq_ar1'].agg(['mean', 'std', 'count'])
                results['d3_clustering_by_decile'] = clustering_by_decile.to_dict()
        except Exception as e:
            results['error'] = str(e)
        return results
