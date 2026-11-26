# FCLR-LIVE-ARCHIVE-01 Confirmatory Evaluation (20261126T042519Z)
**Experiment:** FCLR-LIVE-ARCHIVE-01
**Verdict:** `NOT_SUPPORTED`
**Source:** Binance public archive (unauthenticated S3), 5 symbols x 48 months (2021-2024).
## Design
- B0 RV24 persistence; B1 HAR OLS (log RV1h/24h/168h); C1 +signed funding +90d |funding| pct; C2 +mark/index premium +mark/EMA24 dist.
- Splits 60/20/20 by unique UTC ts, 168h purge/embargo, test->3 blocks. train=103775 val=34870 test=35715.
## Results (mean QLIKE, lower is better)
| Model | QLIKE |
|---|---|
| B0 | 0.508955 |
| B1 | 0.321497 |
| C1 | 0.318622 |
| C2 | 0.318796 |

**Primary C2 vs B1 relative QLIKE reduction: 0.840%** (floor 2%).
Bootstrap 2000 reps 95% CI relative reduction: [0.542%, 1.144%].

## Per-block QLIKE
| Block | B1 | C2 |
|---|---|---|
| 1 | 0.320867 | 0.318212 |
| 2 | 0.322918 | 0.320208 |
| 3 | 0.320705 | 0.317968 |

## Leave-one-symbol-out (C2 vs B1)
| Symbol | n | rel reduction |
|---|---|---|
| 1INCHUSDT | 7143 | 1.346% |
| AAVEUSDT | 7143 | 0.863% |
| ADAUSDT | 7143 | 0.401% |
| ALGOUSDT | 7143 | 0.683% |
| ALPHAUSDT | 7143 | 0.494% |

## Verdict: `NOT_SUPPORTED` — C2 vs B1 relative QLIKE reduction < 2% floor or CI includes 0.
