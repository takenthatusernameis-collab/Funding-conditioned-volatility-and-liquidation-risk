# TRACK C DEEPER VALIDATION (FCLR-011, frozen splits only) - 20261104T153054Z

## Context
- Panel: /home/runner/work/Funding-conditioned-volatility-and-liquidation-risk/Funding-conditioned-volatility-and-liquidation-risk/research_state/data_cache/fclr011_panel.json (FCLR-011)
- Experiment: FCLR-011 | Track C (funding-conditioned volatility) | Gate PASSED (per handoff)
- Symbols: ['BNBUSDT', 'BTCUSDT', 'ETHUSDT', 'SOLUSDT', 'XRPUSDT'] (n=5)
- Splits: {'train': ['2026-01-01T00:00:00Z', '2026-03-17T23:00:00Z'], 'val': ['2026-03-25T00:00:00Z', '2026-04-30T23:00:00Z'], 'test': ['2026-05-08T00:00:00Z', '2026-08-06T23:00:00Z']}
- Train/Val/Test: 8280/4440/10800
- Constraints: frozen FCLR-011 splits only, no sealed panel re-runs, no threshold-shop, no Binance/Hyperliquid merge, train-only normalization, trailing-only
- Bootstrap: block bootstrap >=2000 deterministic replicates (block_size=24h), Holm correction applied to family of ablation comparisons vs base

## 1) Ablations (QLIKE, lower better) - train/val/test
| Split | B1 | C1 (RV+fund) | C2 (RV+fund+price) | A1_fundpctz | A2_rvratios | A3_mark/ema | A4_mark/prem | A5_markema_sens | A6_markprem_sens |
|-------|-----|--------------|-------------------|-------------|-------------|-------------|--------------|-----------------|-----------------|
| TRAIN | 0.818770 | 0.797556 | 0.767879 | 0.773555 | 0.839068 | 0.790784 | 0.797556 | 0.784980 | 0.797556 |
| VAL | 0.574123 | 0.563487 | 0.547947 | 0.550200 | 0.589200 | 0.560652 | 0.563487 | 0.558091 | 0.563487 |
| TEST | 0.612649 | 0.594666 | 0.569740 | 0.572744 | 0.627220 | 0.590848 | 0.594666 | 0.587446 | 0.594666 |

## 2) Block-bootstrap vs B1 (TEST, block_size=24h, reps=2000, deterministic)
| Model | QLIKE | rel_imp_vs_B1(%) | diff(alt-base) | 95% CI (diff) | CI_excludes0 | raw_p_approx |
|-------|-------|-------------------|----------------|---------------|--------------|--------------|
| C1 | 0.594666 | +2.935 | -0.017982 | [-0.023456,-0.013085] | YES | 0.010 |
| C2 | 0.569740 | +7.004 | -0.042908 | [-0.057135,-0.030248] | YES | 0.010 |
| A1_fundpctz | 0.572744 | +6.513 | -0.039904 | [-0.052036,-0.028145] | YES | 0.010 |
| A2_rvratios | 0.627220 | -2.378 | 0.014571 | [0.011438,0.018083] | NO | 0.500 |
| A3_markema | 0.590848 | +3.558 | -0.021800 | [-0.028703,-0.015578] | YES | 0.010 |
| A4_markprem | 0.594666 | +2.935 | -0.017982 | [-0.023692,-0.012969] | YES | 0.010 |
| A5_markema_sens | 0.587446 | +4.114 | -0.025203 | [-0.032964,-0.017705] | YES | 0.010 |
| A6_markprem_sens | 0.594666 | +2.935 | -0.017982 | [-0.023709,-0.013100] | YES | 0.010 |

## 2b) Holm correction (family: ablations vs B1, TEST)
| Model | raw_p (approx) | holm_p |
|-------|-----------------|--------|
| C1 | 0.010 | 0.080 if ph is not None else 'NA' |
| C2 | 0.010 | 0.070 if ph is not None else 'NA' |
| A1_fundpctz | 0.010 | 0.060 if ph is not None else 'NA' |
| A2_rvratios | 0.500 | 0.500 if ph is not None else 'NA' |
| A3_markema | 0.010 | 0.050 if ph is not None else 'NA' |
| A4_markprem | 0.010 | 0.040 if ph is not None else 'NA' |
| A5_markema_sens | 0.010 | 0.030 if ph is not None else 'NA' |
| A6_markprem_sens | 0.010 | 0.020 if ph is not None else 'NA' |

## 3) Funding x RV / funding x dislocation interactions (TEST, block-bootstrap>=2000)
| Model | QLIKE | rel_imp_vs_B1(%) | diff vs C2 | 95% CI vs B1 (diff) | CI_excludes0 |
|-------|-------|-------------------|------------|---------------------|--------------|
| I1_fund_x_rv | 0.573305 | +6.422 | +0.003565 | [-0.051156,-0.027674] | YES |
| I2_fund_x_ema | 0.571641 | +6.693 | +0.001901 | [-0.054495,-0.029347] | YES |

## 4) Regime-stratified QLIKE by funding quartiles per symbol/time (TEST, descriptive)
- Funding |abs| quartiles (test): q1=1.691e-05, q2=3.916e-05, q3=6.572e-05

| Quartile | Range (|fund|) | n (test obs) | B1 QLIKE | C1 QLIKE | C2 QLIKE | rel_imp(C2 vs B1) |
|----------|-----------------|---------------|----------|----------|----------|-------------------|
| Q1_low | - | 2702 | 0.598741 | 0.592506 | 0.575755 | +3.839% |
| Q2 | - | 2699 | 0.587232 | 0.574724 | 0.552959 | +5.836% |
| Q3 | - | 2699 | 0.652332 | 0.633116 | 0.607770 | +6.831% |
| Q4_high | - | 2700 | 0.612306 | 0.578327 | 0.542480 | +11.404% |

## 5) Cross-symbol stability (TEST)
| Symbol | n | B1 QLIKE | C2 QLIKE | rel_imp(C2 vs B1) | diff(C2-B1) | 95% CI |
|--------|---|----------|----------|-------------------|--------------|-------|
| BNBUSDT | 2160 | 0.470067 | 0.433398 | +7.801% | -0.036669 | [-0.063398,-0.015566] |
| BTCUSDT | 2160 | 0.766094 | 0.709241 | +7.421% | -0.056853 | [-0.094754,-0.026784] |
| ETHUSDT | 2160 | 0.776777 | 0.720093 | +7.297% | -0.056684 | [-0.095739,-0.026313] |
| SOLUSDT | 2160 | 0.426227 | 0.398753 | +6.446% | -0.027474 | [-0.047858,-0.010415] |
| XRPUSDT | 2160 | 0.624077 | 0.587215 | +5.907% | -0.036861 | [-0.073257,-0.011224] |

## 6) Notes
- All on frozen FCLR-011 splits only (train 2026-01-01..2026-03-17, val 2026-03-25..2026-04-30, test 2026-05-08..2026-08-06).
- Train-only normalization for scalers; trailing-only features (funding percentiles/z computed from history before origin).
- Chronological, leakage-resistant. No tuning on test/holdout.
- Block bootstrap uses circular blocks of 24h, >=2000 reps where feasible (2000 for main, 1500 for per-symbol).
- Holm correction applied to ablation family vs B1 (raw_p approximated from CI direction; full per-contrast p computation possible but CI-exclusion is primary).
- Mark/index premium partially missing in panel (per eval summary) but EMA distance and funding features dominate; ablations include mark/index premium sensitivity.
- Forward replication FCLR-012-V blocked on data (Binance ends 2026-11-02, 0 blocks) - not addressed here.
- Track C overlay remains HYPOTHETICAL_ONLY per constraints.
