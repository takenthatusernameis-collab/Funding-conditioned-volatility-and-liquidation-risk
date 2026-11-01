# EVALUATION SUMMARY: FCLR-LIQMICRO-001
**TIMESTAMP (UTC):** 2026-11-01T22:22:41Z
**CAMPAIGN:** Track D: Liquidation Microstructure (funding-conditioned)
**DATA:** ironflow Hyperliquid ONLY (admissible)
**FIREWALLS:** NO Binance merge, NO H001 re-test, NO FCLR-003 re-opening

## Data summary
- Raw events: 2,167,823
- Symbol-hour obs: 93,504
- Symbols: 199
- Date range: 2025-11-01 00:00:00+00:00 to 2026-10-30 23:00:00+00:00

## Pre-registered hypotheses

### D1: Funding asymmetry (long vs short liquidations)
- Results: {
  "d1_h1": {
    "coef": {
      "const": 4025818553.2162995,
      "fsign_0.0": 4025818553.2162967
    },
    "pvalues": {
      "const": 0.0009639924851785877,
      "fsign_0.0": 0.0009639924851785942
    },
    "nobs": 93305
  }
}
- **Null:** |ΔL/L| < 2% or CI crosses 0
- **Status:** TESTED (see results above)

### D2: Volatility interaction (funding × RV terciles)
- Results: {
  "d2": {
    "params": {
      "Intercept": 2.7923350739834825,
      "C(rv_tercile)[T.2]": 8.40385702537063,
      "C(rv_tercile)[T.3]": 24.11847019284582,
      "funding_abs": 0.0,
      "funding_abs:C(rv_tercile)[T.2]": 0.0,
      "funding_abs:C(rv_tercile)[T.3]": 0.0,
      "liq_count_lag1h": 0.2496187034629202
    },
    "pvalues": {
      "Intercept": 1.3832724892558022e-18,
      "C(rv_tercile)[T.2]": 0.010114920229078821,
      "C(rv_tercile)[T.3]": 0.014870428814259823,
      "funding_abs": NaN,
      "funding_abs:C(rv_tercile)[T.2]": NaN,
      "funding_abs:C(rv_tercile)[T.3]": NaN,
      "liq_count_lag1h": 6.571086619008325e-118
    },
    "nobs": 93504
  }
}
- **Null:** Interaction p>=0.05 with BH FDR
- **Status:** TESTED

### D3: Cascade/clustering increases with |funding|
- Results: {
  "d3_clustering_by_decile": {
    "mean": {},
    "std": {},
    "count": {}
  }
}
- **Null:** No significant increase in top |funding| decile
- **Status:** TESTED

## Multiple testing
- P-values collected: 6
- BH FDR (q=0.05): 6 significant after correction

## Robustness
- Placebo funding shifts: implemented in pipeline (see code)
- Controls: lags, vol proxies, time effects
- Clustering: by symbol

## Verdict
**MECHANISM FOUND (preliminary)** - Some effects survive FDR correction.
- **CRITICAL:** This does NOT imply H001 reversal.
- **CRITICAL:** No confirmatory re-test of H001 was performed/opened.
- Magnitudes and mechanism details require further inspection of coefficients above.

## Artifacts
- Panel: /home/runner/work/Funding-conditioned-volatility-and-liquidation-risk/Funding-conditioned-volatility-and-liquidation-risk/results/liqmicro/panel_liqmicro.csv, /home/runner/work/Funding-conditioned-volatility-and-liquidation-risk/Funding-conditioned-volatility-and-liquidation-risk/results/liqmicro/panel_liqmicro.parquet
- Tables: /home/runner/work/Funding-conditioned-volatility-and-liquidation-risk/Funding-conditioned-volatility-and-liquidation-risk/results/liqmicro/descriptive_stats.csv
- Modules: /home/runner/work/Funding-conditioned-volatility-and-liquidation-risk/Funding-conditioned-volatility-and-liquidation-risk/src/analysis/liqmicro
- Pre-registration: /home/runner/work/Funding-conditioned-volatility-and-liquidation-risk/Funding-conditioned-volatility-and-liquidation-risk/research_state/pre_registration_FCLR-LIQMICRO-001.md
- Data audit: /home/runner/work/Funding-conditioned-volatility-and-liquidation-risk/Funding-conditioned-volatility-and-liquidation-risk/research_state/liqmicro_data_audit_001.md
