# FCLR-VOL-JUMP-03 Multi-Estimator x Multi-Horizon Jump-Forecast Robustness Evaluation (20261125T045000Z)

- experiment_id: FCLR-VOL-JUMP-03
- session_id: session_20261125T045000Z
- status: CONFIRMATORY_COMPLETE
- verdict: NOT_SUPPORTED
- design: walk_forward_classification_signed_jump_semivariance_asymmetry_multi_estimator_multi_horizon_nonoverlapping_leakage_hardened
- estimators: ['bipower', 'threshold_bipower']
- horizons_h: [24, 48]
- remediations: ['48h purge+embargo', 'non-overlapping forward-outcome windows (origin spacing >= H)', 'mark/index tolerance filter (|mark/oracle - 1| <= 0.01)', 'delisting-aware per-coin identity', 'per-coin cluster bootstrap', 'Holm across the declared estimator x horizon x metric family']
- universe coins (intersection): 466
- aggregate n_forecasts: 87162
- aggregate n_events: 4235
- materiality_floor_rel: 0.02
- materiality_met: False
- significant: True

## Per-config results (aggregate out-of-sample, leakage-hardened)
| estimator | H | n_fc | n_ev | coins | brier_base | brier_cand | rel_brier | rel_logloss | p_boot | p_dk |
|---|---|---|---|---|---|---|---|---|---|---|
| bipower | 24 | 30284 | 1388 | 202 | 0.043611 | 0.043545 | 0.1510% | 0.4134% | 0.9290 | 0.0000 |
| bipower | 48 | 13297 | 642 | 202 | 0.045779 | 0.045734 | 0.0991% | 0.2525% | 0.7165 | 0.0000 |
| threshold_bipower | 24 | 30284 | 1476 | 202 | 0.046045 | 0.045797 | 0.5386% | 1.1523% | 1.0000 | 0.0000 |
| threshold_bipower | 48 | 13297 | 729 | 202 | 0.051717 | 0.051565 | 0.2949% | 0.6389% | 0.9450 | 0.0000 |

## Aggregate (pooled across configs)
- Brier baseline=0.046024 candidate=0.045885 rel=0.3025%
- log-loss baseline=0.191776 candidate=0.190466 rel=0.6829%
- Holm family size=8 rejected=True

_Verdict: NOT_SUPPORTED. Best-config relative Brier improvement vs frozen 2.00% floor; Holm-significant=True. A null that survives across ALL estimators and horizons closes the volatility-jump arm for good._
