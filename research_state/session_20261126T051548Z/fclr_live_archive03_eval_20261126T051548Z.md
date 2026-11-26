# FCLR-LIVE-ARCHIVE-03 Confirmatory Evaluation (20261126T051548Z)
**Experiment:** FCLR-LIVE-ARCHIVE-03
**Verdict:** `NOT_SUPPORTED`
**Source:** Binance public archive (unauthenticated), 5 symbols x 48 months (2021-2024), read-only verified cache.
## Design
- Target: next-24h RV > train-only 95th percentile (binary stress/tail exceedance).
- B1: logistic HAR on log RV1h/RV24h/RV168h; C2: B1 + funding(24h)+90d|funding|pct +mark/index premium +mark/EMA24 dist.
- Splits 60/20/20 by unique UTC ts, 168h purge/embargo, test->3 blocks. train=103775 val=34870 test=35715.
- Stress threshold (train-only 95th pct RV): 1.660156e-02; stress events in test: 748/35715 (2.09%).
## Results
| Model | Brier | Log-loss | ECE |
|---|---|---|---|
| B1 | 0.018753 | 0.083699 | 0.002439 |
| C2 | 0.018667 | 0.083128 | 0.003372 |

**Primary C2 vs B1 relative Brier reduction: 0.458% (floor 2%).**
Log-loss relative reduction: 0.682%.
Bootstrap 2000 reps 95% CI relative Brier reduction: [-0.966%, 1.972%].

## Per-block relative Brier reduction (C2 vs B1)
| Block | Brier B1 | Brier C2 | rel reduction |
|---|---|---|---|
| 1 | 0.018802 | 0.018765 | 0.194% |
| 2 | 0.018768 | 0.018695 | 0.388% |
| 3 | 0.018689 | 0.018541 | 0.794% |

## Leave-one-symbol-out (C2 vs B1)
| Symbol | n | stress | rel Brier reduction |
|---|---|---|---|
| 1INCHUSDT | 7143 | 73 | 1.178% |
| AAVEUSDT | 7143 | 62 | 3.618% |
| ADAUSDT | 7143 | 122 | 0.697% |
| ALGOUSDT | 7143 | 280 | -1.701% |
| ALPHAUSDT | 7143 | 190 | 2.399% |

## Verdict: `NOT_SUPPORTED` — C2 vs B1 relative Brier reduction < 2% floor or CI includes 0.
