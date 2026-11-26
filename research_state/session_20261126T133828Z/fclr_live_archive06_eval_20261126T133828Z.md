# FCLR-LIVE-ARCHIVE-06 Confirmatory Evaluation (20261126T133828Z)
**Experiment:** FCLR-LIVE-ARCHIVE-06
**Verdict:** `NOT_SUPPORTED`
**Source:** Binance public archive (unauthenticated), 5 symbols x 48 months (2021-2024), read-only verified cache.
## Design
- Target: next-24h downside realized-semivariance level D = log(RV_minus+1e-09), RV_minus sums squared negative 1h log-returns over the next 24 hours.
- B1: OLS on log RV1h/RV24h/RV168h + log RV_plus/RV_minus at 24h/168h (7 signed HAR features); C2: B1 + signed funding(24h) + trailing 90d |funding| pct + mark/index premium + mark/EMA24 distance (11 features).
- Splits 60/20/20 by unique UTC ts, 168h purge/embargo, test->3 blocks. train=103775 val=34870 test=35715.
## Results
| Model | MSE | R^2 | Sign accuracy |
|---|---|---|---|
| B1 | 8.506573e-01 | 0.2619 | 1.0000 |
| C2 | 8.445656e-01 | 0.2671 | 1.0000 |

**Primary C2 vs B1 relative test-MSE reduction: 0.716% (floor 2%).**
Bootstrap 2000 reps 95% CI relative MSE reduction: [0.419%, 1.020%].

## Per-block relative MSE reduction (C2 vs B1)
| Block | B1 MSE | C2 MSE | rel reduction |
|---|---|---|---|
| 1 | 8.503043e-01 | 8.443312e-01 | 0.702% |
| 2 | 8.521128e-01 | 8.461439e-01 | 0.700% |
| 3 | 8.495549e-01 | 8.432218e-01 | 0.745% |

## Leave-one-symbol-out (C2 vs B1)
| Symbol | n | rel MSE reduction | sign_acc B1 | sign_acc C2 |
|---|---|---|---|---|
| 1INCHUSDT | 7143 | 1.123% | 1.000 | 1.000 |
| AAVEUSDT | 7143 | 1.133% | 1.000 | 1.000 |
| ADAUSDT | 7143 | 0.239% | 1.000 | 1.000 |
| ALGOUSDT | 7143 | 0.666% | 1.000 | 1.000 |
| ALPHAUSDT | 7143 | 0.477% | 1.000 | 1.000 |

## Verdict: `NOT_SUPPORTED` — C2 vs B1 relative test-MSE reduction < 2% floor or CI includes 0.
