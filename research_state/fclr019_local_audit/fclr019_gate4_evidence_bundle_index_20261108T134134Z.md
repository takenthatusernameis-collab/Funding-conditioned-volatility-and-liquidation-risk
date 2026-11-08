# FCLR-019 Gate 4 evidence-bundle index (20261108T134134Z)

- method: deterministic local evidence read; read-only; no network; no model-outcome computation
- draft_only: **True** | no_confirmatory_outcomes: **True** | exploratory_only: **True** | no_network: **True**
- not_go_for_confirmatory_outcomes: **True**
- confirmatory_ready_now: **False** | confirmatory_outcomes_go: **False**

## Caveats
- draft_only_not_frozen_not_promoted: `True`
- no_confirmatory_outcomes_computed: `True`
- no_prerequisite_marked_satisfied: `True`
- states_used: `['present_unverified', 'present_blocker', 'missing']`
- lfs_pointer_treated_as_unavailable_pointer_missing_state: `True`
- v5_all_go_false_terms_explicit_blocker_unresolved_expected: `True`

## Global v5 evidence refs
- terms_evidence: state=**present_blocker** ref=`research_state/fclr016_local_audit/fclr016_v5_terms_evidence_BLOCKED_20261108T014835Z.json` read_state=`ok` note=`terms_status=EXPLICIT_BLOCKER_UNRESOLVED`
- provenance_manifest: state=**present_blocker** ref=`research_state/fclr016_local_audit/fclr016_v5_provenance_license_manifest_20261108T014405Z.json` read_state=`ok` note=`confirmatory_provenance_go_false_or_missing`
- completeness_leakage_audit: state=**present_blocker** ref=`research_state/fclr016_local_audit/fclr016_v5_completeness_leakage_audit_20261108T014405Z.json` read_state=`ok` note=`blockers_remaining_count=2`
- confirmatory_prereg_draft: state=**present_blocker** ref=`research_state/fclr016_local_audit/fclr016_v5_confirmatory_prereg_DRAFT_20261108T014835Z.json` read_state=`ok` note=`prereg_draft_or_not_frozen_before_outcomes`
- fresh_frozen_prereg_before_outcomes_required: state=**missing**

## Candidate window indices
### cand_2024_04_09_evidenced (2024-04-01..2024-09-30)
- fclr018_provenance_status=`IDENTITY_VERIFIED_BOUNDED_FCLR015` fclr018_confirmatory_eligibility=`INELIGIBLE_EXPLORATORY` index_summary_state=**present_blocker** confirmatory_outcomes_go=**False**
- identity_provenance_range: **present_unverified** `IDENTITY_VERIFIED_BOUNDED_FCLR015 for window per fclr018; confirmatory still bounded by ranges/manifest/terms/fresh-frozen-prereg`
- manifest_terms_evidence.summary: **present_blocker** (provenance_manifest=present_blocker, terms_evidence=present_blocker)
- admissibility_package_status.summary: **present_blocker** (completeness=present_blocker, v5_window_terms=present_blocker)
- fresh_frozen_prereg_before_outcomes_required: **missing**
- leakage_sufficiency_gates: **present_unverified** `local coverage/block-count feasibility fields present; leakage audit for any confirmatory run still requires fresh frozen prereg + admissibility package`

### cand_2024_10_12_local_exploratory (2024-10-01..2024-12-31)
- fclr018_provenance_status=`UNVERIFIED` fclr018_confirmatory_eligibility=`INELIGIBLE_EXPLORATORY` index_summary_state=**present_blocker** confirmatory_outcomes_go=**False**
- identity_provenance_range: **present_blocker** `provenance_status=UNVERIFIED; reasons=['v5_terms_blocker_unresolved_all_go_false', 'provenance_not_identity_verified_bounded_fclr015', 'calendar_coverage_incomplete_or_unverified', 'block_count_gate_lt_3']`
- manifest_terms_evidence.summary: **present_blocker** (provenance_manifest=present_blocker, terms_evidence=present_blocker)
- admissibility_package_status.summary: **present_blocker** (completeness=present_blocker, v5_window_terms=present_blocker)
- fresh_frozen_prereg_before_outcomes_required: **missing**
- leakage_sufficiency_gates: **present_blocker** `calendar_coverage_incomplete_or_unverified;block_count_gate_lt_3`

### cand_2024_04_12_mixed_evidenced_prefix (2024-04-01..2024-12-31)
- fclr018_provenance_status=`UNVERIFIED` fclr018_confirmatory_eligibility=`INELIGIBLE_EXPLORATORY` index_summary_state=**present_blocker** confirmatory_outcomes_go=**False**
- identity_provenance_range: **present_blocker** `provenance_status=UNVERIFIED; reasons=['v5_terms_blocker_unresolved_all_go_false', 'provenance_not_identity_verified_bounded_fclr015', 'calendar_coverage_incomplete_or_unverified']`
- manifest_terms_evidence.summary: **present_blocker** (provenance_manifest=present_blocker, terms_evidence=present_blocker)
- admissibility_package_status.summary: **present_blocker** (completeness=present_blocker, v5_window_terms=present_blocker)
- fresh_frozen_prereg_before_outcomes_required: **missing**
- leakage_sufficiency_gates: **present_blocker** `calendar_coverage_incomplete_or_unverified`

### cand_2025_01_12_local_exploratory (2025-01-01..2025-12-31)
- fclr018_provenance_status=`UNVERIFIED` fclr018_confirmatory_eligibility=`INELIGIBLE_EXPLORATORY` index_summary_state=**present_blocker** confirmatory_outcomes_go=**False**
- identity_provenance_range: **present_blocker** `provenance_status=UNVERIFIED; reasons=['v5_terms_blocker_unresolved_all_go_false', 'provenance_not_identity_verified_bounded_fclr015', 'calendar_coverage_incomplete_or_unverified']`
- manifest_terms_evidence.summary: **present_blocker** (provenance_manifest=present_blocker, terms_evidence=present_blocker)
- admissibility_package_status.summary: **present_blocker** (completeness=present_blocker, v5_window_terms=present_blocker)
- fresh_frozen_prereg_before_outcomes_required: **missing**
- leakage_sufficiency_gates: **present_blocker** `calendar_coverage_incomplete_or_unverified`

### cand_2024_01_12_local_exploratory (2024-01-01..2024-12-31)
- fclr018_provenance_status=`UNVERIFIED` fclr018_confirmatory_eligibility=`INELIGIBLE_EXPLORATORY` index_summary_state=**present_blocker** confirmatory_outcomes_go=**False**
- identity_provenance_range: **present_blocker** `provenance_status=UNVERIFIED; reasons=['v5_terms_blocker_unresolved_all_go_false', 'provenance_not_identity_verified_bounded_fclr015', 'calendar_coverage_incomplete_or_unverified']`
- manifest_terms_evidence.summary: **present_blocker** (provenance_manifest=present_blocker, terms_evidence=present_blocker)
- admissibility_package_status.summary: **present_blocker** (completeness=present_blocker, v5_window_terms=present_blocker)
- fresh_frozen_prereg_before_outcomes_required: **missing**
- leakage_sufficiency_gates: **present_blocker** `calendar_coverage_incomplete_or_unverified`

Planning/draft evidence only — not GO for confirmatory outcomes, not frozen/promoted, no prerequisite marked satisfied, no overlay/H001/Track A status change.
