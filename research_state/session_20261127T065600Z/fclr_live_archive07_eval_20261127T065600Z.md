# FCLR-LIVE-ARCHIVE-07 Confirmatory Evaluation (20261127T065600Z)
**Experiment:** FCLR-LIVE-ARCHIVE-07
**Verdict:** `NOT_SUPPORTED`
**Common support |S|:** 22608 (all-five mark-price, close>0)
## Design
- Target: next-24h mean log realized variance y = log(RV_24h_next + 1e-09), from 1h mark-price log-returns. Metric: QLIKE.
- B1: OLS on log RV1h/RV24h/RV168h + log RV_plus/RV_minus at 24h/168h (7 signed HAR features); C2: B1 + signed funding(24h) + trailing 90d |funding| pct + mark/index premium + mark/EMA24 distance (11 features).
- Declared Holm secondary (campaign-06 estimand): next-24h downside realized-semivariance level log(RV_minus+eps) on MSE, 2-family.
- Sequential confirmatory look k=2, alpha_2 = 0.008333.
- Splits 60/20/20 by unique UTC ts on S, 168h purge/embargo, test->3 blocks. train=66405 val=22415 test=23260.
## Results
| Model | QLIKE | MSE | R^2 |
|---|---|---|---|
| B1 | 4.266689e-01 | 7.377058e-01 | 0.2908 |
| C2 | 4.296724e-01 | 7.316783e-01 | 0.2966 |

**Primary C2 vs B1 relative test-QLIKE reduction: -0.704% (floor 2%).**
Bootstrap 2000 reps 95% CI relative QLIKE reduction: [-1.218%, -0.190%].

**Secondary (Holm, 2-family): downside-semivariance level MSE reduction 1.240%, direction consistent.**

## Per-block relative QLIKE reduction (C2 vs B1)
| Block | B1 QLIKE | C2 QLIKE | rel reduction |
|---|---|---|---|
| 1 | 4.271079e-01 | 4.300311e-01 | -0.684% |
| 2 | 4.270989e-01 | 4.301388e-01 | -0.712% |
| 3 | 4.258000e-01 | 4.288473e-01 | -0.716% |

## Leave-one-symbol-out (C2 vs B1)
| Symbol | n | rel QLIKE reduction |
|---|---|---|
| BNBUSDT | 4652 | 1.324% |
| BTCUSDT | 4652 | 0.371% |
| ETHUSDT | 4652 | -0.747% |
| SOLUSDT | 4652 | -1.546% |
| XRPUSDT | 4652 | -3.184% |

## Gaps: 0 unverified/missing cache entries disclosed (see JSON).

## Verdict: `NOT_SUPPORTED` — C2 vs B1 relative test-QLIKE reduction < 2% floor or CI includes 0.
