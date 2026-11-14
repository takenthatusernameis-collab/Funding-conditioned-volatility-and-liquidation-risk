# FCLR-018 Gate 4 prereg-readiness matrix (20261114T173656Z)

- method: deterministic local evidence read; read-only; no network; no model-outcome computation
- prereg_status: **DRAFT_NOT_FROZEN** (NOT FROZEN / NOT PROMOTED / NOT EXECUTABLE AS CONFIRMATORY)
- no_confirmatory_outcomes: **True**
- exploratory_only: **True**
- no_network: **True**
- not_go_for_confirmatory_outcomes: **True**
- confirmatory_ready_now: **False**

## Caveats / gates
- draft_only_not_frozen_not_promoted: `True`
- no_confirmatory_outcomes_computed: `True`
- v5_terms_explicit_blocker_unresolved: `True`
- fclr015_identity_verified_slice_only_where_evidenced: `2024-04..09`
- unprovenanced_windows_are_exploratory: `True`
- sealed_artifacts_untouched: `['research_state/evaluation_summary_funding_v3_30d.md', 'research_state/run_manifest_funding_v3_30d.json', 'research_state/pre_registration_gate4_funding_multisplit_v3_30d_20261107T033500Z.md']`
- confirmatory_requires_fresh_frozen_prereg_before_outcomes: `True`
- v5_terms_blocker_state: `{"all_go": false, "confirmatory_outcomes_permitted": false, "fabricated": false, "terms_status": "EXPLICIT_BLOCKER_UNRESOLVED"}`
- provenanced_confirmatory_ranges_note: 2024-04-01..2024-09-30 identity-verified bounded (FCLR-015 context) only; confirmatory bounded by PROVENANCED_CONFIRMATORY_RANGES + manifest/terms evidence + admissibility guards.

## Candidate windows
### cand_2024_04_09_evidenced (2024-04-01..2024-09-30)
- basis: `fclr015_evidenced_bounded` | span_days=183 | months=6
- max_non_overlapping_30d_blocks_with_7d_purge: 5 | block_count_gate_ge_3: **True**
- calendar_coverage_all_symbols_complete: **True**
- provenance_status: **IDENTITY_VERIFIED_BOUNDED_FCLR015**
- confirmatory_eligibility: **INELIGIBLE_EXPLORATORY** | confirmatory_eligible_now: **False**
- confirmatory_ineligibility_reasons: `['v5_terms_blocker_unresolved_all_go_false']`

### cand_2024_10_12_local_exploratory (2024-10-01..2024-12-31)
- basis: `local_cache_contiguous_unprovenanced` | span_days=92 | months=3
- max_non_overlapping_30d_blocks_with_7d_purge: 2 | block_count_gate_ge_3: **False**
- calendar_coverage_all_symbols_complete: **False**
- provenance_status: **UNVERIFIED**
- confirmatory_eligibility: **INELIGIBLE_EXPLORATORY** | confirmatory_eligible_now: **False**
- confirmatory_ineligibility_reasons: `['v5_terms_blocker_unresolved_all_go_false', 'provenance_not_identity_verified_bounded_fclr015', 'calendar_coverage_incomplete_or_unverified', 'block_count_gate_lt_3']`

### cand_2024_04_12_mixed_evidenced_prefix (2024-04-01..2024-12-31)
- basis: `local_cache_mixed_evidenced_prefix_unprovenanced_suffix` | span_days=275 | months=9
- max_non_overlapping_30d_blocks_with_7d_purge: 7 | block_count_gate_ge_3: **True**
- calendar_coverage_all_symbols_complete: **False**
- provenance_status: **UNVERIFIED**
- confirmatory_eligibility: **INELIGIBLE_EXPLORATORY** | confirmatory_eligible_now: **False**
- confirmatory_ineligibility_reasons: `['v5_terms_blocker_unresolved_all_go_false', 'provenance_not_identity_verified_bounded_fclr015', 'calendar_coverage_incomplete_or_unverified']`

### cand_2025_01_12_local_exploratory (2025-01-01..2025-12-31)
- basis: `local_cache_contiguous_unprovenanced` | span_days=365 | months=12
- max_non_overlapping_30d_blocks_with_7d_purge: 10 | block_count_gate_ge_3: **True**
- calendar_coverage_all_symbols_complete: **False**
- provenance_status: **UNVERIFIED**
- confirmatory_eligibility: **INELIGIBLE_EXPLORATORY** | confirmatory_eligible_now: **False**
- confirmatory_ineligibility_reasons: `['v5_terms_blocker_unresolved_all_go_false', 'provenance_not_identity_verified_bounded_fclr015', 'calendar_coverage_incomplete_or_unverified']`

### cand_2024_01_12_local_exploratory (2024-01-01..2024-12-31)
- basis: `local_cache_contains_evidenced_but_entire_window_not_verified` | span_days=366 | months=12
- max_non_overlapping_30d_blocks_with_7d_purge: 10 | block_count_gate_ge_3: **True**
- calendar_coverage_all_symbols_complete: **False**
- provenance_status: **UNVERIFIED**
- confirmatory_eligibility: **INELIGIBLE_EXPLORATORY** | confirmatory_eligible_now: **False**
- confirmatory_ineligibility_reasons: `['v5_terms_blocker_unresolved_all_go_false', 'provenance_not_identity_verified_bounded_fclr015', 'calendar_coverage_incomplete_or_unverified']`

## DRAFT prereg skeleton (NOT FROZEN)
```json
{
  "acceptance_stop_rules_draft": [
    "Claim-worthy only if fresh frozen prereg before outcomes, admissibility gates green, provenance/terms resolved as required, >=5 instruments, >=3 non-overlapping 30d blocks, leakage audit clean, stable pre-registered uncertainty.",
    "If any sufficiency/coverage/leakage/provenance/terms criterion fails: PILOT/INCONCLUSIVE or INELIGIBLE; no confirmatory claim.",
    "No threshold shopping; no H001/economic/overlay/Track A status change without separate evidence."
  ],
  "based_on_candidate": "cand_2024_04_09_evidenced",
  "confirmatory_gate_note": "2024-04..09 confirmatory bounded by PROVENANCED_CONFIRMATORY_RANGES + manifest/terms evidence + admissibility guards; v5 terms EXPLICIT_BLOCKER_UNRESOLVED/all_go=false blocks confirmatory outcomes.",
  "freeze_promotion_authorized": false,
  "hypotheses": {
    "H0": "DRAFT: No incremental forecast skill beyond RV-only baseline.",
    "H1_primary": "DRAFT: RV+funding features vs RV-only baseline improve 24h forward realized-variance forecast loss (QLIKE) out-of-sample; direction/magnitude not pre-claimed."
  },
  "not_executable_as_confirmatory": true,
  "primary_contrast_candidates": [
    "E_rv_signed_abs_roll vs A_rv_only (candidate, subject to frozen prereg)",
    "D/B/C vs A secondary/reporting-only unless separately frozen"
  ],
  "requires_fresh_frozen_prereg_before_outcomes": true,
  "split_block_bootstrap_params_draft": {
    "block_days": 30,
    "bootstrap": "block bootstrap over UTC day blocks (draft; seed/reps fixed only at freeze)",
    "chronological": true,
    "leakage_controls": [
      "chronological splits",
      "train-only normalization",
      "funding merge last-known<=hour",
      "forward targets not used in train",
      "no random splits",
      "no test tuning"
    ],
    "min_non_overlapping_blocks": 3,
    "purge_embargo_days": 7,
    "walk_forward_non_overlapping_test_blocks": true
  },
  "status": "DRAFT_NOT_FROZEN"
}
```

Planning/draft evidence only — not GO for confirmatory outcomes, not frozen/promoted, no overlay/H001/Track A status change.
