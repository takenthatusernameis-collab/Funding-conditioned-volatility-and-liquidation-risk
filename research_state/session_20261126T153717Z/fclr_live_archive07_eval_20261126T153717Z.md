# FCLR-LIVE-ARCHIVE-07 Confirmatory Evaluation (20261126T153717Z)
**Experiment:** FCLR-LIVE-ARCHIVE-07
**Verdict:** `NOT_SUPPORTED`
**Source:** Binance public market-data archive (unauthenticated, free, no signup), 5 symbols x 31 months (2024-04..2026-10), read-only verified cache.
## Design
- Target: next-24h mean log realized variance y = log(RV_24h_next + 1e-09), from 1h mark-price log-returns. Metric: QLIKE.
- B1: OLS on log RV1h/RV24h/RV168h + log RV_plus/RV_minus at 24h/168h (7 signed HAR features); C2: B1 + signed funding(24h) + trailing 90d |funding| pct + mark/index premium + mark/EMA24 distance (11 features).
- Declared Holm secondary (campaign-06 estimand): next-24h downside realized-semivariance level log(RV_minus+eps) on MSE, 2-family.
- Sequential confirmatory look k=2, alpha_2 = 0.008333.
- Splits 60/20/20 by unique UTC ts, 168h purge/embargo, test->3 blocks. train=46896 val=11496 test=4368.
## Results
| Model | QLIKE | MSE | R^2 |
|---|---|---|---|
| B1 | -6.763766e+00 | 7.932604e-01 | 0.2022 |
| C2 | -6.754894e+00 | 7.911313e-01 | 0.2044 |

**Primary C2 vs B1 relative test-QLIKE reduction: 0.000% (floor 2%).**
Bootstrap 2000 reps 95% CI relative QLIKE reduction: [-1846721592840.218%, -51764024625.914%].

**Secondary (Holm, 2-family): downside-semivariance level MSE reduction -0.491%, direction inconsistent.**

## Per-block relative QLIKE reduction (C2 vs B1)
| Block | B1 QLIKE | C2 QLIKE | rel reduction |
|---|---|---|---|
| 1 | -6.762908e+00 | -6.753823e+00 | -908523370926.950% |
| 2 | -6.761247e+00 | -6.751971e+00 | -927577917061.484% |
| 3 | -6.767143e+00 | -6.758888e+00 | -825531929655.199% |

## Leave-one-symbol-out (C2 vs B1)
| Symbol | n | rel QLIKE reduction |
|---|---|---|
| BTCUSDT | 4368 | -304673851149.406% |

## Gaps: 3775 unverified/missing cache entries disclosed (see JSON).

## Verdict: `NOT_SUPPORTED` — C2 vs B1 relative test-QLIKE reduction < 2% floor or CI includes 0.
