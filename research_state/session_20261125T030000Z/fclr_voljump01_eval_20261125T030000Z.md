# FCLR-VOL-JUMP-01 Jump-Forecast Evaluation (20261125T030000Z)
- experiment_id: FCLR-VOL-JUMP-01
- session_id: session_20261125T030000Z
- status: CONFIRMATORY_COMPLETE
- verdict: NOT_SUPPORTED
- design: walk_forward_classification_signed_jump_semivariance_asymmetry
- universe: {'n_coins': 466, 'n_panel_rows': 3051819}
- n_forecasts: 1136222
- n_events: 39116
- n_coins: 454
- n_test_blocks: 4
- event_rate: 0.034426
- materiality_floor_rel: 0.02
- materiality_met: False
- significant: True

## Metrics (aggregate out-of-sample)
| model | brier | log_loss | ece |
|---|---|---|---|
| baseline (RV-only) | 0.033322 | 0.150536 | 0.012456 |
| candidate (RV+funding+price) | 0.033292 | 0.150112 | 0.012629 |

- relative Brier improvement: 0.0922%
- relative log-loss improvement: 0.2811%

## Inference
- cluster-bootstrap 95% CI (rel Brier): [7.252923103619278e-06, 5.425201268971311e-05]
- p(improvement>0): 0.993500
- Driscoll-Kraay block t=10.077899550027738 p=0.0 lag=2
- Holm adjusted p: [0.9935, 0.0] rejected=True

## Per-block results
| block | n_test | n_events | brier_base | brier_cand | rel_brier |
|---|---|---|---|---|---|
| 0 | 271150 | 11735 | 0.041320 | 0.041281 | 0.0949% |
| 1 | 267736 | 8339 | 0.030507 | 0.030476 | 0.1021% |
| 2 | 440993 | 15803 | 0.034532 | 0.034499 | 0.0944% |
| 3 | 156343 | 3239 | 0.020860 | 0.020850 | 0.0474% |

_Verdict: NOT_SUPPORTED. Relative Brier improvement 0.0922% vs frozen 2.00% floor; Holm-significant=True._
