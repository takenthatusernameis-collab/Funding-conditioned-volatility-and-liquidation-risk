# FCLR-VOL-JUMP-04 Multi-Estimator x Multi-Horizon DIRECTIONAL (Sign) Jump-Forecast Robustness Evaluation (20261125T054500Z)

- experiment_id: FCLR-VOL-JUMP-04
- session_id: session_20261125T054500Z
- status: CONFIRMATORY_COMPLETE
- verdict: NOT_SUPPORTED
- design: walk_forward_classification_directional_signed_jump_semivariance_asymmetry_sign_multi_estimator_multi_horizon_nonoverlapping_leakage_hardened
- target: next-H signed-jump DIRECTION / SIGN (downside-dominant: J^{(H)} < 0, RS- > RS+)
- estimators: ['bipower', 'threshold_bipower']
- horizons_h: [24, 48]
- remediations: ['48h purge+embargo', 'non-overlapping forward-outcome windows (origin spacing >= H)', 'mark/index tolerance filter (|mark/oracle - 1| <= 0.01)', 'delisting-aware per-coin identity', 'per-coin cluster bootstrap', 'Holm across the declared estimator x horizon x metric family']
- universe coins (intersection): 466
- aggregate n_forecasts: 110914
- aggregate n_events: 57354
- materiality_floor_rel: 0.02
- materiality_met: False
- significant: True

## Per-config results (aggregate out-of-sample, leakage-hardened)
| estimator | H | n_fc | n_ev | coins | brier_base | brier_cand | rel_brier | rel_logloss | p_boot | p_dk |
|---|---|---|---|---|---|---|---|---|---|---|
| bipower | 24 | 38259 | 19785 | 367 | 0.250034 | 0.249799 | 0.0942% | 0.0671% | 0.9910 | 0.0000 |
| bipower | 48 | 17198 | 9010 | 367 | 0.250010 | 0.249755 | 0.1020% | 0.0017% | 0.9110 | 0.0000 |
| threshold_bipower | 24 | 38259 | 19647 | 367 | 0.250226 | 0.250144 | 0.0328% | 0.0240% | 0.8240 | 0.0000 |
| threshold_bipower | 48 | 17198 | 8912 | 367 | 0.250434 | 0.250630 | -0.0785% | -0.1773% | 0.2095 | 0.0000 |

## Aggregate (pooled across configs)
- Brier baseline=0.250159 candidate=0.250040 rel=0.0474%
- log-loss baseline=0.693471 candidate=0.693442 rel=0.0042%
- Holm family size=8 rejected=True

_Verdict: NOT_SUPPORTED. Best-config relative Brier improvement vs frozen 2.00% floor; Holm-significant=True. A null that survives across ALL estimators and horizons closes the funding-conditioned volatility-jump family for good._
