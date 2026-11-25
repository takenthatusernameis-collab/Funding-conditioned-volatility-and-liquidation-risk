# FCLR-VOL-JUMP-03 Evidence Audit — 20261125T045000Z

- experiment_id: FCLR-VOL-JUMP-03
- session_id: session_20261125T045000Z
- audit_pass: true
- unresolved_blockers: []
- verdict: NOT_SUPPORTED
- eval_status: CONFIRMATORY_COMPLETE
- holdout_opened: true
- recompute_all_checks_match: true (76 checks)
- materiality_floor_rel: 0.02 (frozen)
- materiality_met: false
- significant: true (Holm; economic materiality governs)

## Universe & scale
- 466 coins in the candles/funding/open_interest intersection; 202 coins with sufficient trailing history per config.
- 87,162 non-overlapping forecasts; 4,235 jump events; 4 (estimator x horizon) configs.

## Per-config relative Brier improvement (candidate vs RV-only baseline)
| estimator | H | rel Brier |
|---|---|---|
| bipower | 24 | 0.1510% |
| bipower | 48 | 0.0991% |
| threshold_bipower | 24 | 0.5386% |
| threshold_bipower | 48 | 0.2949% |

All below the frozen 2% floor; aggregate 0.3025%.

## Checks
- eval candidate metrics numeric (not NaN)
- independent stdlib recompute all_checks_match=true (76 checks)
- materiality floor applied as frozen (2% relative Brier)
- verdict symmetric and consistent with frozen prereg rule
- all FCLR-POOLED-AUDIT-001 leakage remediations applied simultaneously
- jump estimator varied (bipower vs threshold-bipower); horizon varied ({24h, 48h})
- bipower/24h reproduces the closed jump02 result (0.1510%) as a pipeline sanity check
- no external trigger required or fired on frozen data

## Notes
The signed-jump / semivariance-asymmetry null SURVIVES variation of the jump estimator AND the forecast horizon under full leakage remediation. NOT_SUPPORTED is a valid, publishable negative result that closes the funding-conditioned volatility-jump arm for good.