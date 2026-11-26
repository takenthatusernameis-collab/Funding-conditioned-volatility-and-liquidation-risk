# FCLR-LIVE-ARCHIVE-06 Evidence Audit (20261126T133828Z)

**Experiment:** FCLR-LIVE-ARCHIVE-06  **Session:** 20261126T133828Z  **Verdict:** `NOT_SUPPORTED`

**audit_pass:** true  **unresolved_blockers:** []

## Leakage controls
- outcome_data_inspected_before_freeze: false
- train_only_ols_fit: true
- train_only_scaling: true
- purge_embargo_hours: 168
- test_never_used_for_model_fitting: true
- hash_bound_prereg_to_source_registry: true

## Recompute
- all_checks_match: true
- mse_B1_match: true, mse_C2_match: true, r2_B1_match: true, r2_C2_match: true,
  rel_reduction_match: true, n_test_match: true, verdict_reproduced: true

## Source
- n_cache_entries: 1200, n_ok: 1200, n_missing: 0
- sha256_verified_all: true, read_only_reuse: true, network_used: false

## Verdict
- verdict: NOT_SUPPORTED
- reason: C2 vs B1 relative test-MSE reduction < 2% floor or CI includes 0
- relative_mse_reduction_C2_vs_B1: 0.007161214745326733 (0.716%, below the 2% floor)
- bootstrap_ci95_relative_mse_reduction: [0.00419, 0.01020] (lower bound > 0 but below 2% floor)
- materiality_floor: 0.02
- n_test: 35715, n_unique_timestamps: 34872

A valid null: the funding-conditioned downside realized-semivariance level arm does not
clear the frozen 2% relative test-MSE materiality floor. Stdlib only; no network;
read-only verified cache.
