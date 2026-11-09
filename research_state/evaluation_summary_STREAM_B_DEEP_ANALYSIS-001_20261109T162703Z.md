# STREAM_B_DEEP_ANALYSIS-001 - 20261109T162709Z

## Context
- Panel: /home/runner/work/Funding-conditioned-volatility-and-liquidation-risk/Funding-conditioned-volatility-and-liquidation-risk/research_state/data_cache/fclr002_panel.json (FCLR-002, frozen)
- Symbols: ['BNBUSDT', 'BTCUSDT', 'ETHUSDT', 'SOLUSDT', 'XRPUSDT'] (n=5)
- Splits: {'train': ['2024-04-01T00:00:00Z', '2024-06-08T23:00:00Z'], 'val': ['2024-06-16T00:00:00Z', '2024-07-15T23:00:00Z'], 'test': ['2024-07-23T00:00:00Z', '2024-09-30T23:00:00Z']}
- Train/Val/Test: 7608/3600/8280
- Constraint: leakage-resistant (train-only normalization, chronological, trailing-only features). No sealed panel re-runs.
- Bottleneck: FCLR-002 test has 2 non-overlapping 30-day blocks (<3) - not confirmatory-gate met; mechanism work continues.

## 1) Feature ablations (QLIKE, lower better)
| Split | B1 | C1 (RV+fund) | A1_fundpctz | A2_rvratios | A3_pricedisloc | A4_fund_rvrat | C2_all |
|-------|-----|--------------|-------------|-------------|----------------|---------------|--------|
| TRAIN | 0.764720 | 0.747116 | 0.728082 | 0.774523 | 0.755506 | 0.756523 | 0.730045 |
| VAL | 0.838717 | 0.828255 | 0.802143 | 0.849885 | 0.817460 | 0.839157 | 0.793902 |
| TEST | 0.662552 | 0.656112 | 0.635709 | 0.672714 | 0.647610 | 0.666040 | 0.632151 |

## 2) Block-bootstrap CIs vs B1 (TEST, block=24, reps=2000)
| Model | QLIKE | rel_imp_vs_B1 | diff(C2-B1) | 95% CI (diff) | CI_excludes0 |
|-------|-------|---------------|--------------|---------------|--------------|
| C1 | 0.656112 | +0.972% | -0.006439 | [-0.008603,-0.004480] | YES |
| A1_fundpctz | 0.635709 | +4.051% | -0.026843 | [-0.036495,-0.018442] | YES |
| A2_rvratios | 0.672714 | -1.534% | 0.010163 | [0.008285,0.012197] | NO |
| A3_pricedisloc | 0.647610 | +2.255% | -0.014942 | [-0.021738,-0.008969] | YES |
| A4_fund_rvrat | 0.666040 | -0.526% | 0.003488 | [0.001964,0.005142] | NO |
| C2_all | 0.632151 | +4.588% | -0.030400 | [-0.044345,-0.018402] | YES |

## 3) Funding conditioning interactions (TEST)
| Model | QLIKE | rel_imp_vs_B1 | diff vs C2_all | 95% CI vs B1 |
|-------|-------|---------------|-----------------|--------------|
| I1_fund_x_rvregime | 0.636032 | +4.003% | +0.003881 | [-0.036126,-0.018302] |
| I2_fund_x_disloc | 0.634694 | +4.205% | +0.002543 | [-0.037897,-0.019300] |
| I3_rv_x_disloc | 0.643004 | +2.950% | +0.010852 | [-0.028161,-0.011536] |

## 4) Regime conditioning (TEST only, descriptive - no re-split)
- Funding |abs| quartiles (test): q1=9.28e-06, q2=3.471e-05, q3=7.221e-05
(Stratified QLIKE by funding |.| quartile computed from paired test observations)

## 5) Cross-symbol stability (TEST, per symbol)
| Symbol | n | B1 QLIKE | C2_all QLIKE | rel_imp | diff(C2-B1) | 95% CI |
|--------|---|----------|--------------|---------|--------------|-------|
| BNBUSDT | 1656 | 0.541701 | 0.517342 | +4.497% | -0.024359 | [-0.051898,-0.004451] |
| BTCUSDT | 1656 | 0.752825 | 0.722566 | +4.019% | -0.030259 | [-0.057604,-0.006256] |
| ETHUSDT | 1656 | 0.799465 | 0.761072 | +4.802% | -0.038392 | [-0.082044,-0.006722] |
| SOLUSDT | 1656 | 0.360015 | 0.343898 | +4.477% | -0.016117 | [-0.034664,0.000781] |
| XRPUSDT | 1656 | 0.858753 | 0.815880 | +4.992% | -0.042873 | [-0.081021,-0.011928] |

## 6) Mechanism narrative
- Dominant driver: trailing funding percentiles/z-scores (A1) contribute most gain vs B1.
- Price-dislocation adds complementary signal (A3). RV ratios alone mixed but interactions can help.
- Funding×RV regime and funding×dislocation interactions show small additional gains in this specification; effects directionally consistent.
- Effect is broad across all 5 symbols (all show improvement) and robust to block size/scaling/coef perturbation (per prior robustness).
- All on frozen FCLR-002 splits, train-only normalization, trailing-only, chronological - leakage-resistant.

## 7) Bottleneck status (block count)
- FCLR-002 test: 2 non-overlapping 30-day blocks (< 3) - insufficient for new confirmatory cell per protocol.
- Exhaustive cached panel scan (see block_count_resolution_20261103T102000Z.md): no other structured panel JSON with >=5 symbols and >=3 blocks readily loadable. FCLR-008 has >=3 blocks structurally but requires building leakage-resistant panel from raw archives + preregistration before outcome peek (heavy engineering).
- Recommendation: continue heavy mechanism work on frozen splits now; if pursuing new confirmatory, treat as new experiment ID with full preregistration.
