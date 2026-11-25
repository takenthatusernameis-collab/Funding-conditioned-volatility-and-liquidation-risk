# FCLR-VOL-JUMP-01 Evidence Audit (20261125T030000Z)

- experiment_id: FCLR-VOL-JUMP-01
- session_id: session_20261125T030000Z
- audit_pass: True
- unresolved_blockers: []
- verdict: NOT_SUPPORTED

## Result
- status: CONFIRMATORY_COMPLETE
- n_forecasts: 1136222
- n_events: 39116
- n_coins: 454
- n_test_blocks: 4
- baseline brier: 0.033322
- candidate brier: 0.033292
- relative Brier improvement: 0.0922% (floor 2.00%)
- materiality_met: False
- significant (Holm): True

## Recompute
- independent stdlib recompute all_checks_match: True (60 checks)

## Checks
- eval candidate metrics are numeric (not NaN)
- independent stdlib recompute all_checks_match=true
- materiality floor applied as frozen (2% relative Brier)
- verdict symmetric and consistent with frozen prereg rule
- no external trigger required or fired on frozen data

## Notes
Candidate relative Brier improvement 0.0922% is statistically distinguishable from zero (Holm) but far below the frozen 2% materiality floor; NOT_SUPPORTED closes the signed-jump / semivariance-asymmetry arm at broad scale.
