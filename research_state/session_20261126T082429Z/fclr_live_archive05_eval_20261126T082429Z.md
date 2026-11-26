# FCLR-LIVE-ARCHIVE-05 Confirmatory Evaluation (20261126T082429Z)
**Experiment:** FCLR-LIVE-ARCHIVE-05
**Verdict:** `NOT_SUPPORTED`
**Source:** Binance public archive (unauthenticated), 5 symbols x 48 months (2021-2024), read-only verified cache.
## Design
- Target: next-24h realized-semivariance asymmetry A = log((RV_plus+1e-09)/(RV_minus+1e-09)), RV_plus/RV_minus sum squared positive/negative 1h log-returns over the next 24 hours.
- B1: OLS on log RV1h/RV24h/RV168h + log RV_plus/RV_minus at 24h/168h (7 signed HAR features); C2: B1 + signed funding(24h) + trailing 90d |funding| pct + mark/index premium + mark/EMA24 distance (11 features).
- Splits 60/20/20 by unique UTC ts, 168h purge/embargo, test->3 blocks. train=103775 val=34870 test=35715.
## Results
| Model | MSE | R^2 | Sign accuracy |
|---|---|---|---|
| B1 | 9.355263e-01 | -0.0181 | 0.5016 |
| C2 | 9.342108e-01 | -0.0167 | 0.5031 |

**Primary C2 vs B1 relative test-MSE reduction: 0.141% (floor 2%).**
Bootstrap 2000 reps 95% CI relative MSE reduction: [-0.032%, 0.315%].

## Per-block relative MSE reduction (C2 vs B1)
| Block | B1 MSE | C2 MSE | rel reduction |
|---|---|---|---|
| 1 | 9.346000e-01 | 9.333012e-01 | 0.139% |
| 2 | 9.353948e-01 | 9.339722e-01 | 0.152% |
| 3 | 9.365840e-01 | 9.353592e-01 | 0.131% |

## Leave-one-symbol-out (C2 vs B1)
| Symbol | n | rel MSE reduction | sign_acc B1 | sign_acc C2 |
|---|---|---|---|---|
| 1INCHUSDT | 7143 | 0.770% | 0.517 | 0.521 |
| AAVEUSDT | 7143 | 0.225% | 0.490 | 0.484 |
| ADAUSDT | 7143 | 0.107% | 0.500 | 0.506 |
| ALGOUSDT | 7143 | -0.032% | 0.513 | 0.513 |
| ALPHAUSDT | 7143 | -0.026% | 0.483 | 0.486 |

## Verdict: `NOT_SUPPORTED` — C2 vs B1 relative test-MSE reduction < 2% floor or CI includes 0.
