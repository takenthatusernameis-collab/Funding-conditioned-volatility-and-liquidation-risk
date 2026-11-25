# FCLR-VOL-JUMP-02 Evidence Audit (20261125T034400Z)

- experiment_id: FCLR-VOL-JUMP-02
- session_id: session_20261125T034400Z
- audit_pass: true
- verdict: NOT_SUPPORTED
- n_forecasts: 30284
- n_events: 1388
- n_coins: 202
- n_test_blocks: 3
- relative Brier improvement: 0.1510% (floor 2.00%)
- materiality_met: False
- significant: True
- recompute: all_checks_match=True n_checks=60

## Remediations applied (simultaneously)
- 48h purge+embargo
- non-overlapping forward-outcome windows (origin spacing >= 24h)
- mark/index tolerance filter (|mark/oracle - 1| <= 0.01)
- delisting-aware per-coin identity
- per-coin cluster bootstrap
- Holm across the declared family

## Notes
Leakage-hardened robustness RE-CONFIRMATION of the closed FCLR-VOL-JUMP-01 null. Relative Brier improvement 0.1510% is below the frozen 2% floor; the signed-jump / semivariance-asymmetry null SURVIVES non-overlapping forward windows, mark/index tolerance filtering, delisting-aware identity, per-coin block bootstrap and Holm correction. NOT_SUPPORTED is a valid, publishable negative result that closes the volatility-jump arm for good.
