# FCLR-VOL-JUMP-04 Evidence Audit (20261125T054500Z)

- experiment_id: FCLR-VOL-JUMP-04
- session_id: session_20261125T054500Z
- audit_pass: true
- unresolved_blockers: []
- verdict: NOT_SUPPORTED
- eval_status: CONFIRMATORY_COMPLETE
- holdout_opened: true
- recompute_all_checks_match: true (76 checks)

## Headline
Directional / SIGN jump-forecast robustness study (target `J^{(H)} < 0`, downside-dominant
RS- > RS+), crossing the jump estimator (bipower vs threshold-bipower) with the forecast
horizon ({24h, 48h}) under the full FCLR-POOLED-AUDIT-001 leakage-hardened pipeline.

- n_forecasts: 110,914 (non-overlapping)
- n_events: 57,354 (downside-dominance; base rate ~51.7%)
- n_coins: 367
- aggregate Brier: baseline 0.250159 vs candidate 0.250040 (rel 0.0474%)
- aggregate log-loss: baseline 0.693471 vs candidate 0.693442 (rel 0.0042%)
- materiality_floor_rel: 0.02 -> materiality_met: false
- Holm-significant: true (but economically immaterial)

## Per-config relative Brier improvement
| estimator | H | rel_brier |
|---|---|---|
| bipower | 24 | 0.0942% |
| bipower | 48 | 0.1020% |
| threshold_bipower | 24 | 0.0328% |
| threshold_bipower | 48 | -0.0785% |

## Checks
- eval candidate metrics numeric (not NaN)
- independent stdlib recompute all_checks_match=true (76 checks)
- materiality floor applied as frozen (2% relative Brier)
- verdict symmetric and consistent with frozen prereg rule
- all FCLR-POOLED-AUDIT-001 leakage remediations applied simultaneously
- jump estimator varied (bipower vs threshold-bipower)
- forecast horizon varied ({24h, 48h})
- target is the DIRECTIONAL / SIGN of the signed jump, materially different from jump01/02/03 magnitude-exceedance
- base rate estimated train-only (binary sign target; no quantile threshold)
- no external trigger required or fired on frozen data

## Notes
The directional (sign) jump null SURVIVES variation of the jump estimator AND the forecast
horizon under full leakage remediation. NOT_SUPPORTED is a valid, publishable negative
result that closes the funding-conditioned volatility-jump family (magnitude AND direction)
for good.