# STREAM_B_ROBUSTNESS-002 - 20261103T101627Z

## Objective
Heavy robustness on extended features (fund pct/z, RV ratios, price-disloc) on frozen FCLR-002 splits.
- Circular block bootstrap: block sizes {12, 24, 48}
- Leave-one-symbol-out (5 symbols)
- Train-only scaling variants (robust/median-IQR, standardization)
- Coefficient sensitivity ±50%
- C2 vs B1 QLIKE deltas + CIs
- Leakage-resistant: chronological splits, train-only normalization, purge/embargo preserved
- No re-run of sealed FCLR-001..008 panels

## Data
- Panel: /home/runner/work/Funding-conditioned-volatility-and-liquidation-risk/Funding-conditioned-volatility-and-liquidation-risk/research_state/data_cache/fclr002_panel.json
- Total rows: 19488
- Symbols: ['BNBUSDT', 'BTCUSDT', 'ETHUSDT', 'SOLUSDT', 'XRPUSDT']
- Splits (frozen): {'train': ['2024-04-01T00:00:00Z', '2024-06-08T23:00:00Z'], 'val': ['2024-06-16T00:00:00Z', '2024-07-15T23:00:00Z'], 'test': ['2024-07-23T00:00:00Z', '2024-09-30T23:00:00Z']}

## Split sizes
- Train: 7608
- Val: 3600
- Test: 8280

## 1) Circular block bootstrap by block size (TEST)
| Block size | QLIKE(B1) | QLIKE(C2) | rel. imp (%) | diff(C2-B1) | 95% CI | crosses zero |
|-----------|-----------|-----------|--------------|--------------|---------|--------------|
| 12 | 0.662552 | 0.632151 | 4.588 | -0.030400 | [-0.041736, -0.020385] | NO |
| 24 | 0.662552 | 0.632151 | 4.588 | -0.030400 | [-0.045284, -0.017665] | NO |
| 48 | 0.662552 | 0.632151 | 4.588 | -0.030400 | [-0.044491, -0.017702] | NO |

## 2) Leave-one-symbol-out (TEST, block=24)
| Left out | n | QLIKE(B1) | QLIKE(C2) | rel. imp (%) | diff(C2-B1) | 95% CI | crosses zero |
|----------|---|-----------|-----------|--------------|--------------|---------|--------------|
| BNBUSDT | 6624 | 0.692764 | 0.660854 | 4.606 | -0.031911 | [-0.048001, -0.017541] | NO |
| BTCUSDT | 6624 | 0.639983 | 0.609548 | 4.756 | -0.030436 | [-0.046348, -0.016220] | NO |
| ETHUSDT | 6624 | 0.628324 | 0.599921 | 4.520 | -0.028402 | [-0.042402, -0.015905] | NO |
| SOLUSDT | 6624 | 0.738186 | 0.704215 | 4.602 | -0.033971 | [-0.050965, -0.019039] | NO |
| XRPUSDT | 6624 | 0.613502 | 0.586219 | 4.447 | -0.027282 | [-0.043303, -0.014160] | NO |

## 3) Train-only scaling variants (TEST, block=24)
| Variant | QLIKE(B1) | QLIKE(C2) | rel. imp (%) | diff(C2-B1) | 95% CI | crosses zero |
|---------|-----------|-----------|--------------|--------------|---------|--------------|
| standard (z-score) | 0.662552 | 0.632151 | 4.588 | -0.030400 | [-0.045498, -0.018123] | NO |
| robust (median-IQR) | 0.662552 | 0.632151 | 4.588 | -0.030400 | [-0.044475, -0.018267] | NO |
| minmax_train | 0.662552 | 0.632151 | 4.588 | -0.030400 | [-0.044470, -0.018172] | NO |

## 4) Coefficient sensitivity ±50% (TEST, block=24)
| Scale | QLIKE(B1) | QLIKE(C2) | rel. imp (%) | diff(C2-B1) | 95% CI | crosses zero |
|-------|-----------|-----------|--------------|--------------|---------|--------------|
| 0.5x | 0.662552 | 0.645856 | 2.520 | -0.016696 | [-0.024369, -0.009822] | NO |
| 1.0x | 0.662552 | 0.632151 | 4.588 | -0.030400 | [-0.044963, -0.017205] | NO |
| 1.5x | 0.662552 | 0.620876 | 6.290 | -0.041676 | [-0.062483, -0.022819] | NO |

## Summary
- Extended features show consistent improvement over RV-only baseline across robustness checks.
- CIs remain below zero across block sizes and leave-one-symbol-out in tested configurations.
- Coefficient scaling preserves direction of improvement.
- Train-only normalization and chronological splits maintained throughout.

## Notes
- Does NOT re-run sealed FCLR-001..008 confirmatory panels.
- Heavy robustness on frozen FCLR-002 splits only.
- Leakage-resistant by construction.