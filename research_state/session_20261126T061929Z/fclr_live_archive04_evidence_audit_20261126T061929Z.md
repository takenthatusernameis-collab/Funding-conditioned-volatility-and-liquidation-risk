# FCLR-LIVE-ARCHIVE-04 Evidence Audit (20261126T061929Z)
**Experiment:** FCLR-LIVE-ARCHIVE-04
**Verdict:** `NOT_SUPPORTED`
**Audit pass:** `True`
**Unresolved blockers:** none
## Leakage controls
- outcome_data_inspected_before_freeze: False
- train_only_quantile_fit: True
- train_only_scaling: True
- purge_embargo_hours: 168
- test_never_used_for_quantile_estimation: True
- hash_bound_prereg_to_source_registry: True
## Recompute cross-check
- all_checks_match: True
- avg_pinball_B1_match: True
- avg_pinball_C2_match: True
- rel_reduction_match: True
- n_test_match: True
- verdict_reproduced: True
## Source integrity
- cache entries 1200/1200 ok, missing=0, sha256_verified_all=True
- network used: False; read-only reuse: True
## Headline
- relative avg-pinball reduction C2 vs B1: -1.102% (floor 2%)
- bootstrap 95% CI relative: [-1.233%, -0.969%]

**Verdict: `NOT_SUPPORTED` — C2 vs B1 relative average pinball reduction < 2% floor or CI includes 0.**
