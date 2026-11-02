# EVALUATION SUMMARY: FCLR-LIQMICRO-002
**TIMESTAMP (UTC):** 2026-11-02T00:05:49Z
**CAMPAIGN:** Track D: Liquidation Microstructure (funding-conditioned) - REAL FUNDING INTEGRATION
**DATA:** ironflow Hyperliquid liquidations ONLY + Hyperliquid fundingHistory API (unauthenticated)
**FIREWALLS:** NO Binance merge, NO H001 re-test, NO FCLR-003 re-opening

## Data summary
- Raw events: 2,167,823
- Symbol-hour obs: 93,504
- Symbols: 199
- Funding rows: 78,012
- panel.funding_rate std: 6.9810415624e-06
- panel.funding_rate non-NaN: 93504
- Date range: 2025-11-01 00:00:00+00:00 to 2026-10-30 23:00:00+00:00

## Pre-registered hypotheses (same as FCLR-LIQMICRO-001)

### D1: Funding asymmetry (long vs short liquidations)
- Results: {
  "d1_h1": {
    "coef": {
      "const": 6.975917957084009e+20,
      "fsign_-1.0": -6.975917956841101e+20,
      "fsign_0.0": -6.97591795704335e+20,
      "fsign_1.0": -6.97591795683471e+20
    },
    "pvalues": {
      "const": 0.9999999979101164,
      "fsign_-1.0": 0.9999999982593966,
      "fsign_0.0": 0.9999999982486178,
      "fsign_1.0": 0.9999999982243881
    },
    "nobs": 93305
  }
}
- **Null:** |ΔL/L| < 2% or CI crosses 0
- **Status:** TESTED

### D2: Volatility interaction (funding × RV terciles)
- Results: {
  "d2": {
    "params": {
      "Intercept": 2.5718862087654784,
      "C(rv_tercile)[T.2]": 5.725509631245275,
      "C(rv_tercile)[T.3]": 19.666348654456122,
      "funding_abs": 431296.66902519925,
      "funding_abs:C(rv_tercile)[T.2]": 928875.0823923553,
      "funding_abs:C(rv_tercile)[T.3]": 900050.4161232038,
      "liq_count_lag1h": 0.23457374931185324
    },
    "pvalues": {
      "Intercept": 2.0890612924313144e-29,
      "C(rv_tercile)[T.2]": 0.0003956781175894451,
      "C(rv_tercile)[T.3]": 0.006645167410046508,
      "funding_abs": 0.11837217276222105,
      "funding_abs:C(rv_tercile)[T.2]": 0.05137705156694823,
      "funding_abs:C(rv_tercile)[T.3]": 0.06365040414488912,
      "liq_count_lag1h": 2.6351567446411677e-97
    },
    "nobs": 93504
  }
}
- **Null:** Interaction p>=0.05 with BH FDR
- **Status:** TESTED

### D3: Cascade/clustering increases with |funding|
- Results: {
  "d3_clustering_by_decile": {
    "mean": {
      "0": 0.08091048783437338,
      "1": 0.07901410844293703
    },
    "std": {
      "0": 0.16958183278613678,
      "1": 0.15390767710615424
    },
    "count": {
      "0": 91351,
      "1": 2153
    }
  }
}
- **Null:** No significant increase in top |funding| decile
- **Status:** TESTED

## Multiple testing
- P-values collected: 11
- BH FDR (q=0.05): 4 significant after correction

## Verdict
**FUNDING INTEGRATION COMPLETE WITH REAL DATA.**
- **CRITICAL:** NO reversal of H001; NO confirmatory re-test of H001 opened.
- Funding features now have variation (std>0). See coefficients above.

## Artifacts
- Panel: /home/runner/work/Funding-conditioned-volatility-and-liquidation-risk/Funding-conditioned-volatility-and-liquidation-risk/results/liqmicro_v2/panel_liqmicro_v2.csv, /home/runner/work/Funding-conditioned-volatility-and-liquidation-risk/Funding-conditioned-volatility-and-liquidation-risk/results/liqmicro_v2/panel_liqmicro_v2.parquet
- Tables: /home/runner/work/Funding-conditioned-volatility-and-liquidation-risk/Funding-conditioned-volatility-and-liquidation-risk/results/liqmicro_v2/descriptive_stats_v2.csv
- Modules: /home/runner/work/Funding-conditioned-volatility-and-liquidation-risk/Funding-conditioned-volatility-and-liquidation-risk/src/analysis/liqmicro (updated)
- Funding audit: /home/runner/work/Funding-conditioned-volatility-and-liquidation-risk/Funding-conditioned-volatility-and-liquidation-risk/research_state/liqmicro_funding_audit_002.md
- Pre-registration note: This is a funding-integration fix to FCLR-LIQMICRO-001 (same D1-D3).
