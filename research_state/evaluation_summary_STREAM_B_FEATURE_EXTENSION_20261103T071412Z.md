# STREAM_B_HEAVY_FEATURE_EXTENSION-001 - 20261103T071412Z

## Objective
Extend Track B volatility features on frozen splits (FCLR-002 panel):
- Funding percentiles/zscore (trailing-only)
- RV ratios 6h/24h/7d
- Price-dislocation MA/EMA deviation
- Train-only normalized models
- Block-bootstrap CIs (circular blocks)
- Full ablations

## Data
- Panel: /home/runner/work/Funding-conditioned-volatility-and-liquidation-risk/Funding-conditioned-volatility-and-liquidation-risk/research_state/data_cache/fclr002_panel.json
- Total rows: 19488
- Symbols: ['BNBUSDT', 'BTCUSDT', 'ETHUSDT', 'SOLUSDT', 'XRPUSDT']
- Splits (frozen): {'train': ['2024-04-01T00:00:00Z', '2024-06-08T23:00:00Z'], 'val': ['2024-06-16T00:00:00Z', '2024-07-15T23:00:00Z'], 'test': ['2024-07-23T00:00:00Z', '2024-09-30T23:00:00Z']}
- Note: Does NOT re-run sealed FCLR-001..008 panels

## Split sizes
- Train: 7608
- Val: 3600
- Test: 8280

## Evaluation (QLIKE, lower better; block-bootstrap 2000 reps, block size 24)

### TRAIN
| Model | n | QLIKE | MSE | MAE |
|------|---|-------|-----|-----|
| B1 | 7608 | 0.764720 | 8.067e-06 | 0.001061 |
| C1 | 7608 | 0.747116 | 8.232e-06 | 0.001074 |
| A1_fundpctz | 7608 | 0.728082 | 8.571e-06 | 0.001094 |
| A2_rvratios | 7608 | 0.774523 | 8.677e-06 | 0.001079 |
| A3_pricedisloc | 7608 | 0.755506 | 9.141e-06 | 0.001108 |
| A4_fund_rvrat | 7608 | 0.756523 | 8.860e-06 | 0.001092 |
| C2 | 7608 | 0.730045 | 1.048e-05 | 0.001162 |

### VAL
| Model | n | QLIKE | MSE | MAE |
|------|---|-------|-----|-----|
| B1 | 3600 | 0.838717 | 2.997e-06 | 0.000997 |
| C1 | 3600 | 0.828255 | 3.057e-06 | 0.001004 |
| A1_fundpctz | 3600 | 0.802143 | 3.185e-06 | 0.001019 |
| A2_rvratios | 3600 | 0.849885 | 3.174e-06 | 0.001014 |
| A3_pricedisloc | 3600 | 0.817460 | 3.162e-06 | 0.001019 |
| A4_fund_rvrat | 3600 | 0.839157 | 3.238e-06 | 0.001021 |
| C2 | 3600 | 0.793902 | 3.571e-06 | 0.001058 |

### TEST
| Model | n | QLIKE | MSE | MAE |
|------|---|-------|-----|-----|
| B1 | 8280 | 0.662552 | 8.916e-06 | 0.001167 |
| C1 | 8280 | 0.656112 | 9.066e-06 | 0.001177 |
| A1_fundpctz | 8280 | 0.635709 | 9.516e-06 | 0.001205 |
| A2_rvratios | 8280 | 0.672714 | 9.480e-06 | 0.001190 |
| A3_pricedisloc | 8280 | 0.647610 | 1.022e-05 | 0.001212 |
| A4_fund_rvrat | 8280 | 0.666040 | 9.640e-06 | 0.001199 |
| C2 | 8280 | 0.632151 | 1.163e-05 | 0.001276 |

#### Block-bootstrap CIs (C2 vs B1, TEST)
- QLIKE(B1)=0.662552, QLIKE(C2)=0.632151, rel. improvement=4.588%
- diff(QLIKE_C2 - QLIKE_B1) = -0.030400, 95% CI [-0.044418, -0.017603] (negative = C2 better)
- CI crosses zero: NO

## Ablation summary
- A1_fundpctz: adds trailing funding percentiles/z-scores (train-only normalized)
- A2_rvratios: adds RV ratios (6h/24h/7d style)
- A3_pricedisloc: adds price-dislocation MA/EMA deviation
- A4_fund_rvrat: funding + RV ratios combined
- C2: all features combined

## Notes
- All features are trailing-only (no lookahead). Normalization fitted on TRAIN only.
- Chronological splits preserved (frozen). No tuning on test set.
- Does NOT re-run sealed FCLR-001..008 confirmatory panels.
- Block-bootstrap uses circular blocks of size 24 hours.
- Leakage-resistant by construction.