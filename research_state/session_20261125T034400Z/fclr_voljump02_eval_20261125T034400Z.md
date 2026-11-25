# FCLR-VOL-JUMP-02 Jump-Forecast Robustness Evaluation (20261125T034400Z)

- experiment_id: FCLR-VOL-JUMP-02
- session_id: session_20261125T034400Z
- status: CONFIRMATORY_COMPLETE
- verdict: NOT_SUPPORTED
- design: walk_forward_classification_signed_jump_semivariance_asymmetry_nonoverlapping_leakage_hardened
- remediations: ['48h purge+embargo', 'non-overlapping forward-outcome windows (origin spacing >= 24h)', 'mark/index tolerance filter (|mark/oracle - 1| <= 0.01)', 'delisting-aware per-coin identity', 'per-coin cluster bootstrap', 'Holm across the declared family']
- universe: {'n_coins': 466, 'n_panel_rows': 93764, 'n_coins_delisting_aware': 115}
- n_forecasts: 30284
- n_events: 1388
- n_coins: 202
- n_test_blocks: 3
- event_rate: 0.045833
- materiality_floor_rel: 0.02
- materiality_met: False
- significant: True

## Metrics (aggregate out-of-sample, leakage-hardened)
| model | brier | log_loss | ece |
|---|---|---|---|
| baseline (RV-only) | 0.043611 | 0.184360 | 0.004668 |
| candidate (RV+funding+price) | 0.043545 | 0.183597 | 0.006328 |

- relative Brier improvement: 0.1510%
- relative log-loss improvement: 0.4134%

## Inference
- cluster-bootstrap 95% CI (rel Brier): [-2.4321437483286813e-05, 0.00014028587416972232]
- p(improvement>0): 0.936000
- Driscoll-Kraay block t=2036697.9769366877 p=0.0 lag=2
- Holm adjusted p: [0.936, 0.0] rejected=True

## Per-block results
| block | n_test | n_events | brier_base | brier_cand | rel_brier |
|---|---|---|---|---|---|
| 0 | 10925 | 637 | 0.054884 | 0.054945 | -0.1124% |
| 1 | 10771 | 347 | 0.031300 | 0.031227 | 0.2345% |
| 2 | 8588 | 404 | 0.044710 | 0.044491 | 0.4889% |

_Verdict: NOT_SUPPORTED. Relative Brier improvement 0.1510% vs frozen 2.00% floor; Holm-significant=True. A surviving null closes the volatility-jump arm for good._
