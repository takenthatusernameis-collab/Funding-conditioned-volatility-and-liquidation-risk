# FCLR-VOL-JUMP-03 Prereg (frozen before outcomes) — 20261125T045000Z

- experiment_id: FCLR-VOL-JUMP-03
- session_id: session_20261125T045000Z
- frozen_before_outcomes: true
- outcome_data_inspected_before_freeze: false
- source_registry_sha256: 0970a0a7752f0909a8c201f9ce0a5529a30e5fa6eebc05cfba57a1b9a55a2e44
- design.kind: walk_forward_classification_signed_jump_semivariance_asymmetry_multi_estimator_multi_horizon_nonoverlapping_leakage_hardened
- estimators: bipower, threshold_bipower
- horizons_h: 24, 48
- materiality_floor_rel: 0.02 (frozen; not relaxed after outcomes)

## Question
Does the funding + price-dislocation feature set improve out-of-sample forecasts of a signed-jump / semivariance-asymmetry tail event beyond an RV-only baseline, clearing a frozen 2% materiality floor with Holm-adjusted uncertainty, when the jump estimator (bipower vs threshold-bipower) AND the forecast horizon ({24h, 48h}) are varied and all FCLR-POOLED-AUDIT-001 leakage remediations are applied simultaneously?

## Remediations (applied simultaneously)
48h purge+embargo; non-overlapping forward-outcome windows (origin spacing >= H); mark/index tolerance filter (|mark/oracle - 1| <= 0.01); delisting-aware per-coin identity; per-coin cluster bootstrap; Holm across the declared estimator x horizon x metric family.

## Verdict rule (symmetric)
PROMOTED if materiality_met AND Holm-significant; NOT_SUPPORTED if the 2% floor is not met in any config (valid, publishable negative result); INCONCLUSIVE on degenerate metrics. A null that survives across ALL estimators and horizons closes the volatility-jump arm for good.