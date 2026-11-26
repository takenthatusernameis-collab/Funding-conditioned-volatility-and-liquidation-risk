# FCLR-LIVE-ARCHIVE-04 Confirmatory Evaluation (20261126T061929Z)
**Experiment:** FCLR-LIVE-ARCHIVE-04
**Verdict:** `NOT_SUPPORTED`
**Source:** Binance public archive (unauthenticated), 5 symbols x 48 months (2021-2024), read-only verified cache.
## Design
- Target: next-24h realized variance (continuous) as a predictive distribution at quantiles [0.1, 0.25, 0.5, 0.75, 0.9].
- B1: linear quantile regression on log RV1h/RV24h/RV168h (HAR); C2: B1 + funding(24h)+90d|funding|pct + mark/index premium + mark/EMA24 dist.
- Splits 60/20/20 by unique UTC ts, 168h purge/embargo, test->3 blocks. train=103775 val=34870 test=35715.
## Results
| Model | Avg pinball | Mean abs coverage error |
|---|---|---|
| B1 | 7.848803e-04 | 0.1292 |
| C2 | 7.935292e-04 | 0.1287 |

**Primary C2 vs B1 relative avg-pinball reduction: -1.102% (floor 2%).**
Bootstrap 2000 reps 95% CI relative avg-pinball reduction: [-1.233%, -0.969%].

### Per-quantile pinball loss
| tau | B1 | C2 |
|---|---|---|
| 0.10 | 2.631925e-04 | 2.663795e-04 |
| 0.25 | 6.326083e-04 | 6.396342e-04 |
| 0.50 | 1.120412e-03 | 1.120412e-03 |
| 0.75 | 1.084231e-03 | 1.104138e-03 |
| 0.90 | 8.239580e-04 | 8.370826e-04 |

### Empirical coverage (target = tau)
| tau | B1 | C2 |
|---|---|---|
| 0.10 | 0.2561 | 0.2601 |
| 0.25 | 0.5071 | 0.5060 |
| 0.50 | 0.6636 | 0.6636 |
| 0.75 | 0.7977 | 0.7890 |
| 0.90 | 0.9214 | 0.9246 |

## Per-block relative avg-pinball reduction (C2 vs B1)
| Block | B1 | C2 | rel reduction |
|---|---|---|---|
| 1 | 7.849891e-04 | 7.936646e-04 | -1.105% |
| 2 | 7.853039e-04 | 7.938379e-04 | -1.087% |
| 3 | 7.843481e-04 | 7.930852e-04 | -1.114% |

## Leave-one-symbol-out (C2 vs B1)
| Symbol | n | rel avg-pinball reduction |
|---|---|---|
| 1INCHUSDT | 7143 | 0.080% |
| AAVEUSDT | 7143 | 1.163% |
| ADAUSDT | 7143 | -3.184% |
| ALGOUSDT | 7143 | 3.296% |
| ALPHAUSDT | 7143 | -1.223% |

## Verdict: `NOT_SUPPORTED` — C2 vs B1 relative average pinball reduction < 2% floor or CI includes 0.
