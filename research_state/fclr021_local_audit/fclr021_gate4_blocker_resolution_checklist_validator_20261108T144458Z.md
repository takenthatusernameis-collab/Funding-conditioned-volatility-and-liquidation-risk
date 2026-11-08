# FCLR-021 Gate 4 blocker-resolution checklist validator (20261108T144458Z)

- method: deterministic read-only coverage check of FCLR-020 action/check text vs Gate 4 prerequisite gate set; no network; no model-outcome computation
- draft_only: **True** | no_confirmatory_outcomes: **True** | exploratory_only: **True** | no_network: **True**
- not_go_for_confirmatory_outcomes: **True** | confirmatory_ready_now: **False** | confirmatory_outcomes_go: **False**

## Caveats
- draft_only_not_frozen_not_promoted: `True`
- no_confirmatory_outcomes_computed: `True`
- no_prerequisite_marked_satisfied: `True`
- no_satisfaction_inferred_from_absent_blocker: `True`
- coverage_ok_is_text_coverage_not_resolution: `True`
- lfs_pointer_treated_as_unavailable: `True`
- states_used: `['present_unverified', 'present_blocker', 'missing']`

## Coverage summary
- total_rows=**50** covered_rows=**5** gap_rows=**45**

## Global actions
- authorizes_confirmatory_outcomes=`False`
  - action: Keep v5 terms/admissibility fail-closed until verifiable human/legal evidence resolves blockers and package is GO.
  - action: Track A/H004 remains blocked; do not re-probe absent Hyperliquid months in a loop.
  - action: No .github/workflows edits; no sealed holdout/anchor overwrites; no competing handoff files.
  - action: coverage_ok references action/check text only; it does not resolve a blocker or mark a prerequisite satisfied.
  - verify: `python scripts/fclr016_v5_admissibility_report.py --bogus --json 2>&1 | head -c 200`
  - verify: `python scripts/tracka_resume_check.py | python3 -c "import sys,json; d=json.load(sys.stdin); print(d['pass'], d['network'])"`

## Missing-action warnings (coverage gaps)
- window=`cand_2024_04_09_evidenced` prerequisite=`identity_provenance_range` current_state=`present_unverified` gate_class=`provenance_manifest_evidence` missing_action_class=`provenance_manifest_evidence` missing_markers=`['action:hash', 'action:identity-verified', 'check:sha256sum', 'check:test -f', 'check:json_ok']`
  - warning: coverage gap: cand_2024_04_09_evidenced/identity_provenance_range gate_class=provenance_manifest_evidence missing=['action:hash', 'action:identity-verified', 'check:sha256sum', 'check:test -f', 'check:json_ok']
- window=`cand_2024_04_09_evidenced` prerequisite=`manifest_terms_evidence` current_state=`present_blocker` gate_class=`terms_legal_evidence_resolution` missing_action_class=`terms_legal_evidence_resolution` missing_markers=`['action:verifiable evidence']`
  - warning: coverage gap: cand_2024_04_09_evidenced/manifest_terms_evidence gate_class=terms_legal_evidence_resolution missing=['action:verifiable evidence']
- window=`cand_2024_04_09_evidenced` prerequisite=`manifest_terms_evidence.provenance_manifest` current_state=`present_blocker` gate_class=`provenance_manifest_evidence` missing_action_class=`provenance_manifest_evidence` missing_markers=`['action:identity-verified', 'action:bounded', 'check:fclr015']`
  - warning: coverage gap: cand_2024_04_09_evidenced/manifest_terms_evidence.provenance_manifest gate_class=provenance_manifest_evidence missing=['action:identity-verified', 'action:bounded', 'check:fclr015']
- window=`cand_2024_04_09_evidenced` prerequisite=`manifest_terms_evidence.terms_evidence` current_state=`present_blocker` gate_class=`terms_legal_evidence_resolution` missing_action_class=`terms_legal_evidence_resolution` missing_markers=`['action:terms', 'check:fclr016_v5_admissibility_report', 'check:fclr016_v5_promotion_dryrun']`
  - warning: coverage gap: cand_2024_04_09_evidenced/manifest_terms_evidence.terms_evidence gate_class=terms_legal_evidence_resolution missing=['action:terms', 'check:fclr016_v5_admissibility_report', 'check:fclr016_v5_promotion_dryrun']
- window=`cand_2024_04_09_evidenced` prerequisite=`admissibility_package_status.completeness_leakage_audit` current_state=`present_blocker` gate_class=`admissibility_completeness_leakage_evidence` missing_action_class=`admissibility_completeness_leakage_evidence` missing_markers=`['action:admissibility']`
  - warning: coverage gap: cand_2024_04_09_evidenced/admissibility_package_status.completeness_leakage_audit gate_class=admissibility_completeness_leakage_evidence missing=['action:admissibility']
- window=`cand_2024_04_09_evidenced` prerequisite=`admissibility_package_status.confirmatory_prereg_draft_ref` current_state=`present_blocker` gate_class=`fresh_frozen_prereg_before_outcomes` missing_action_class=`fresh_frozen_prereg_before_outcomes` missing_markers=`['action:fresh frozen preregistration', 'action:before any confirmatory outcomes', 'check:run_funding_ablations']`
  - warning: coverage gap: cand_2024_04_09_evidenced/admissibility_package_status.confirmatory_prereg_draft_ref gate_class=fresh_frozen_prereg_before_outcomes missing=['action:fresh frozen preregistration', 'action:before any confirmatory outcomes', 'check:run_funding_ablations']
- window=`cand_2024_04_09_evidenced` prerequisite=`admissibility_package_status.v5_window_terms_state_from_fclr018` current_state=`present_blocker` gate_class=`terms_legal_evidence_resolution` missing_action_class=`terms_legal_evidence_resolution` missing_markers=`['action:terms', 'action:human/legal', 'action:fabricated=false', 'action:verifiable evidence', 'check:fclr016_v5_admissibility_report', 'check:fclr016_v5_promotion_dryrun']`
  - warning: coverage gap: cand_2024_04_09_evidenced/admissibility_package_status.v5_window_terms_state_from_fclr018 gate_class=terms_legal_evidence_resolution missing=['action:terms', 'action:human/legal', 'action:fabricated=false', 'action:verifiable evidence', 'check:fclr016_v5_admissibility_report', 'check:fclr016_v5_promotion_dryrun']
- window=`cand_2024_04_09_evidenced` prerequisite=`fresh_frozen_prereg_before_outcomes_required` current_state=`missing` gate_class=`fresh_frozen_prereg_before_outcomes` missing_action_class=`fresh_frozen_prereg_before_outcomes` missing_markers=`['action:fresh frozen preregistration', 'check:run_funding_ablations']`
  - warning: coverage gap: cand_2024_04_09_evidenced/fresh_frozen_prereg_before_outcomes_required gate_class=fresh_frozen_prereg_before_outcomes missing=['action:fresh frozen preregistration', 'check:run_funding_ablations']
- window=`cand_2024_04_09_evidenced` prerequisite=`leakage_sufficiency_gates` current_state=`present_unverified` gate_class=`leakage_sufficiency_gates` missing_action_class=`leakage_sufficiency_gates` missing_markers=`['action:sufficiency']`
  - warning: coverage gap: cand_2024_04_09_evidenced/leakage_sufficiency_gates gate_class=leakage_sufficiency_gates missing=['action:sufficiency']
- window=`cand_2024_10_12_local_exploratory` prerequisite=`identity_provenance_range` current_state=`present_blocker` gate_class=`provenance_manifest_evidence` missing_action_class=`provenance_manifest_evidence` missing_markers=`['action:manifest', 'check:sha256sum', 'check:test -f', 'check:json_ok']`
  - warning: coverage gap: cand_2024_10_12_local_exploratory/identity_provenance_range gate_class=provenance_manifest_evidence missing=['action:manifest', 'check:sha256sum', 'check:test -f', 'check:json_ok']
- window=`cand_2024_10_12_local_exploratory` prerequisite=`manifest_terms_evidence` current_state=`present_blocker` gate_class=`terms_legal_evidence_resolution` missing_action_class=`terms_legal_evidence_resolution` missing_markers=`['action:verifiable evidence']`
  - warning: coverage gap: cand_2024_10_12_local_exploratory/manifest_terms_evidence gate_class=terms_legal_evidence_resolution missing=['action:verifiable evidence']
- window=`cand_2024_10_12_local_exploratory` prerequisite=`manifest_terms_evidence.provenance_manifest` current_state=`present_blocker` gate_class=`provenance_manifest_evidence` missing_action_class=`provenance_manifest_evidence` missing_markers=`['action:identity-verified', 'action:bounded', 'check:fclr015']`
  - warning: coverage gap: cand_2024_10_12_local_exploratory/manifest_terms_evidence.provenance_manifest gate_class=provenance_manifest_evidence missing=['action:identity-verified', 'action:bounded', 'check:fclr015']
- window=`cand_2024_10_12_local_exploratory` prerequisite=`manifest_terms_evidence.terms_evidence` current_state=`present_blocker` gate_class=`terms_legal_evidence_resolution` missing_action_class=`terms_legal_evidence_resolution` missing_markers=`['action:terms', 'check:fclr016_v5_admissibility_report', 'check:fclr016_v5_promotion_dryrun']`
  - warning: coverage gap: cand_2024_10_12_local_exploratory/manifest_terms_evidence.terms_evidence gate_class=terms_legal_evidence_resolution missing=['action:terms', 'check:fclr016_v5_admissibility_report', 'check:fclr016_v5_promotion_dryrun']
- window=`cand_2024_10_12_local_exploratory` prerequisite=`admissibility_package_status.completeness_leakage_audit` current_state=`present_blocker` gate_class=`admissibility_completeness_leakage_evidence` missing_action_class=`admissibility_completeness_leakage_evidence` missing_markers=`['action:admissibility']`
  - warning: coverage gap: cand_2024_10_12_local_exploratory/admissibility_package_status.completeness_leakage_audit gate_class=admissibility_completeness_leakage_evidence missing=['action:admissibility']
- window=`cand_2024_10_12_local_exploratory` prerequisite=`admissibility_package_status.confirmatory_prereg_draft_ref` current_state=`present_blocker` gate_class=`fresh_frozen_prereg_before_outcomes` missing_action_class=`fresh_frozen_prereg_before_outcomes` missing_markers=`['action:fresh frozen preregistration', 'action:before any confirmatory outcomes', 'check:run_funding_ablations']`
  - warning: coverage gap: cand_2024_10_12_local_exploratory/admissibility_package_status.confirmatory_prereg_draft_ref gate_class=fresh_frozen_prereg_before_outcomes missing=['action:fresh frozen preregistration', 'action:before any confirmatory outcomes', 'check:run_funding_ablations']
- window=`cand_2024_10_12_local_exploratory` prerequisite=`admissibility_package_status.v5_window_terms_state_from_fclr018` current_state=`present_blocker` gate_class=`terms_legal_evidence_resolution` missing_action_class=`terms_legal_evidence_resolution` missing_markers=`['action:terms', 'action:human/legal', 'action:fabricated=false', 'action:verifiable evidence', 'check:fclr016_v5_admissibility_report', 'check:fclr016_v5_promotion_dryrun']`
  - warning: coverage gap: cand_2024_10_12_local_exploratory/admissibility_package_status.v5_window_terms_state_from_fclr018 gate_class=terms_legal_evidence_resolution missing=['action:terms', 'action:human/legal', 'action:fabricated=false', 'action:verifiable evidence', 'check:fclr016_v5_admissibility_report', 'check:fclr016_v5_promotion_dryrun']
- window=`cand_2024_10_12_local_exploratory` prerequisite=`fresh_frozen_prereg_before_outcomes_required` current_state=`missing` gate_class=`fresh_frozen_prereg_before_outcomes` missing_action_class=`fresh_frozen_prereg_before_outcomes` missing_markers=`['action:fresh frozen preregistration', 'check:run_funding_ablations']`
  - warning: coverage gap: cand_2024_10_12_local_exploratory/fresh_frozen_prereg_before_outcomes_required gate_class=fresh_frozen_prereg_before_outcomes missing=['action:fresh frozen preregistration', 'check:run_funding_ablations']
- window=`cand_2024_10_12_local_exploratory` prerequisite=`leakage_sufficiency_gates` current_state=`present_blocker` gate_class=`leakage_sufficiency_gates` missing_action_class=`leakage_sufficiency_gates` missing_markers=`['action:sufficiency']`
  - warning: coverage gap: cand_2024_10_12_local_exploratory/leakage_sufficiency_gates gate_class=leakage_sufficiency_gates missing=['action:sufficiency']
- window=`cand_2024_04_12_mixed_evidenced_prefix` prerequisite=`identity_provenance_range` current_state=`present_blocker` gate_class=`provenance_manifest_evidence` missing_action_class=`provenance_manifest_evidence` missing_markers=`['action:manifest', 'check:sha256sum', 'check:test -f', 'check:json_ok']`
  - warning: coverage gap: cand_2024_04_12_mixed_evidenced_prefix/identity_provenance_range gate_class=provenance_manifest_evidence missing=['action:manifest', 'check:sha256sum', 'check:test -f', 'check:json_ok']
- window=`cand_2024_04_12_mixed_evidenced_prefix` prerequisite=`manifest_terms_evidence` current_state=`present_blocker` gate_class=`terms_legal_evidence_resolution` missing_action_class=`terms_legal_evidence_resolution` missing_markers=`['action:verifiable evidence']`
  - warning: coverage gap: cand_2024_04_12_mixed_evidenced_prefix/manifest_terms_evidence gate_class=terms_legal_evidence_resolution missing=['action:verifiable evidence']
- window=`cand_2024_04_12_mixed_evidenced_prefix` prerequisite=`manifest_terms_evidence.provenance_manifest` current_state=`present_blocker` gate_class=`provenance_manifest_evidence` missing_action_class=`provenance_manifest_evidence` missing_markers=`['action:identity-verified', 'action:bounded', 'check:fclr015']`
  - warning: coverage gap: cand_2024_04_12_mixed_evidenced_prefix/manifest_terms_evidence.provenance_manifest gate_class=provenance_manifest_evidence missing=['action:identity-verified', 'action:bounded', 'check:fclr015']
- window=`cand_2024_04_12_mixed_evidenced_prefix` prerequisite=`manifest_terms_evidence.terms_evidence` current_state=`present_blocker` gate_class=`terms_legal_evidence_resolution` missing_action_class=`terms_legal_evidence_resolution` missing_markers=`['action:terms', 'check:fclr016_v5_admissibility_report', 'check:fclr016_v5_promotion_dryrun']`
  - warning: coverage gap: cand_2024_04_12_mixed_evidenced_prefix/manifest_terms_evidence.terms_evidence gate_class=terms_legal_evidence_resolution missing=['action:terms', 'check:fclr016_v5_admissibility_report', 'check:fclr016_v5_promotion_dryrun']
- window=`cand_2024_04_12_mixed_evidenced_prefix` prerequisite=`admissibility_package_status.completeness_leakage_audit` current_state=`present_blocker` gate_class=`admissibility_completeness_leakage_evidence` missing_action_class=`admissibility_completeness_leakage_evidence` missing_markers=`['action:admissibility']`
  - warning: coverage gap: cand_2024_04_12_mixed_evidenced_prefix/admissibility_package_status.completeness_leakage_audit gate_class=admissibility_completeness_leakage_evidence missing=['action:admissibility']
- window=`cand_2024_04_12_mixed_evidenced_prefix` prerequisite=`admissibility_package_status.confirmatory_prereg_draft_ref` current_state=`present_blocker` gate_class=`fresh_frozen_prereg_before_outcomes` missing_action_class=`fresh_frozen_prereg_before_outcomes` missing_markers=`['action:fresh frozen preregistration', 'action:before any confirmatory outcomes', 'check:run_funding_ablations']`
  - warning: coverage gap: cand_2024_04_12_mixed_evidenced_prefix/admissibility_package_status.confirmatory_prereg_draft_ref gate_class=fresh_frozen_prereg_before_outcomes missing=['action:fresh frozen preregistration', 'action:before any confirmatory outcomes', 'check:run_funding_ablations']
- window=`cand_2024_04_12_mixed_evidenced_prefix` prerequisite=`admissibility_package_status.v5_window_terms_state_from_fclr018` current_state=`present_blocker` gate_class=`terms_legal_evidence_resolution` missing_action_class=`terms_legal_evidence_resolution` missing_markers=`['action:terms', 'action:human/legal', 'action:fabricated=false', 'action:verifiable evidence', 'check:fclr016_v5_admissibility_report', 'check:fclr016_v5_promotion_dryrun']`
  - warning: coverage gap: cand_2024_04_12_mixed_evidenced_prefix/admissibility_package_status.v5_window_terms_state_from_fclr018 gate_class=terms_legal_evidence_resolution missing=['action:terms', 'action:human/legal', 'action:fabricated=false', 'action:verifiable evidence', 'check:fclr016_v5_admissibility_report', 'check:fclr016_v5_promotion_dryrun']
- window=`cand_2024_04_12_mixed_evidenced_prefix` prerequisite=`fresh_frozen_prereg_before_outcomes_required` current_state=`missing` gate_class=`fresh_frozen_prereg_before_outcomes` missing_action_class=`fresh_frozen_prereg_before_outcomes` missing_markers=`['action:fresh frozen preregistration', 'check:run_funding_ablations']`
  - warning: coverage gap: cand_2024_04_12_mixed_evidenced_prefix/fresh_frozen_prereg_before_outcomes_required gate_class=fresh_frozen_prereg_before_outcomes missing=['action:fresh frozen preregistration', 'check:run_funding_ablations']
- window=`cand_2024_04_12_mixed_evidenced_prefix` prerequisite=`leakage_sufficiency_gates` current_state=`present_blocker` gate_class=`leakage_sufficiency_gates` missing_action_class=`leakage_sufficiency_gates` missing_markers=`['action:sufficiency']`
  - warning: coverage gap: cand_2024_04_12_mixed_evidenced_prefix/leakage_sufficiency_gates gate_class=leakage_sufficiency_gates missing=['action:sufficiency']
- window=`cand_2025_01_12_local_exploratory` prerequisite=`identity_provenance_range` current_state=`present_blocker` gate_class=`provenance_manifest_evidence` missing_action_class=`provenance_manifest_evidence` missing_markers=`['action:manifest', 'check:sha256sum', 'check:test -f', 'check:json_ok']`
  - warning: coverage gap: cand_2025_01_12_local_exploratory/identity_provenance_range gate_class=provenance_manifest_evidence missing=['action:manifest', 'check:sha256sum', 'check:test -f', 'check:json_ok']
- window=`cand_2025_01_12_local_exploratory` prerequisite=`manifest_terms_evidence` current_state=`present_blocker` gate_class=`terms_legal_evidence_resolution` missing_action_class=`terms_legal_evidence_resolution` missing_markers=`['action:verifiable evidence']`
  - warning: coverage gap: cand_2025_01_12_local_exploratory/manifest_terms_evidence gate_class=terms_legal_evidence_resolution missing=['action:verifiable evidence']
- window=`cand_2025_01_12_local_exploratory` prerequisite=`manifest_terms_evidence.provenance_manifest` current_state=`present_blocker` gate_class=`provenance_manifest_evidence` missing_action_class=`provenance_manifest_evidence` missing_markers=`['action:identity-verified', 'action:bounded', 'check:fclr015']`
  - warning: coverage gap: cand_2025_01_12_local_exploratory/manifest_terms_evidence.provenance_manifest gate_class=provenance_manifest_evidence missing=['action:identity-verified', 'action:bounded', 'check:fclr015']
- window=`cand_2025_01_12_local_exploratory` prerequisite=`manifest_terms_evidence.terms_evidence` current_state=`present_blocker` gate_class=`terms_legal_evidence_resolution` missing_action_class=`terms_legal_evidence_resolution` missing_markers=`['action:terms', 'check:fclr016_v5_admissibility_report', 'check:fclr016_v5_promotion_dryrun']`
  - warning: coverage gap: cand_2025_01_12_local_exploratory/manifest_terms_evidence.terms_evidence gate_class=terms_legal_evidence_resolution missing=['action:terms', 'check:fclr016_v5_admissibility_report', 'check:fclr016_v5_promotion_dryrun']
- window=`cand_2025_01_12_local_exploratory` prerequisite=`admissibility_package_status.completeness_leakage_audit` current_state=`present_blocker` gate_class=`admissibility_completeness_leakage_evidence` missing_action_class=`admissibility_completeness_leakage_evidence` missing_markers=`['action:admissibility']`
  - warning: coverage gap: cand_2025_01_12_local_exploratory/admissibility_package_status.completeness_leakage_audit gate_class=admissibility_completeness_leakage_evidence missing=['action:admissibility']
- window=`cand_2025_01_12_local_exploratory` prerequisite=`admissibility_package_status.confirmatory_prereg_draft_ref` current_state=`present_blocker` gate_class=`fresh_frozen_prereg_before_outcomes` missing_action_class=`fresh_frozen_prereg_before_outcomes` missing_markers=`['action:fresh frozen preregistration', 'action:before any confirmatory outcomes', 'check:run_funding_ablations']`
  - warning: coverage gap: cand_2025_01_12_local_exploratory/admissibility_package_status.confirmatory_prereg_draft_ref gate_class=fresh_frozen_prereg_before_outcomes missing=['action:fresh frozen preregistration', 'action:before any confirmatory outcomes', 'check:run_funding_ablations']
- window=`cand_2025_01_12_local_exploratory` prerequisite=`admissibility_package_status.v5_window_terms_state_from_fclr018` current_state=`present_blocker` gate_class=`terms_legal_evidence_resolution` missing_action_class=`terms_legal_evidence_resolution` missing_markers=`['action:terms', 'action:human/legal', 'action:fabricated=false', 'action:verifiable evidence', 'check:fclr016_v5_admissibility_report', 'check:fclr016_v5_promotion_dryrun']`
  - warning: coverage gap: cand_2025_01_12_local_exploratory/admissibility_package_status.v5_window_terms_state_from_fclr018 gate_class=terms_legal_evidence_resolution missing=['action:terms', 'action:human/legal', 'action:fabricated=false', 'action:verifiable evidence', 'check:fclr016_v5_admissibility_report', 'check:fclr016_v5_promotion_dryrun']
- window=`cand_2025_01_12_local_exploratory` prerequisite=`fresh_frozen_prereg_before_outcomes_required` current_state=`missing` gate_class=`fresh_frozen_prereg_before_outcomes` missing_action_class=`fresh_frozen_prereg_before_outcomes` missing_markers=`['action:fresh frozen preregistration', 'check:run_funding_ablations']`
  - warning: coverage gap: cand_2025_01_12_local_exploratory/fresh_frozen_prereg_before_outcomes_required gate_class=fresh_frozen_prereg_before_outcomes missing=['action:fresh frozen preregistration', 'check:run_funding_ablations']
- window=`cand_2025_01_12_local_exploratory` prerequisite=`leakage_sufficiency_gates` current_state=`present_blocker` gate_class=`leakage_sufficiency_gates` missing_action_class=`leakage_sufficiency_gates` missing_markers=`['action:sufficiency']`
  - warning: coverage gap: cand_2025_01_12_local_exploratory/leakage_sufficiency_gates gate_class=leakage_sufficiency_gates missing=['action:sufficiency']
- window=`cand_2024_01_12_local_exploratory` prerequisite=`identity_provenance_range` current_state=`present_blocker` gate_class=`provenance_manifest_evidence` missing_action_class=`provenance_manifest_evidence` missing_markers=`['action:manifest', 'check:sha256sum', 'check:test -f', 'check:json_ok']`
  - warning: coverage gap: cand_2024_01_12_local_exploratory/identity_provenance_range gate_class=provenance_manifest_evidence missing=['action:manifest', 'check:sha256sum', 'check:test -f', 'check:json_ok']
- window=`cand_2024_01_12_local_exploratory` prerequisite=`manifest_terms_evidence` current_state=`present_blocker` gate_class=`terms_legal_evidence_resolution` missing_action_class=`terms_legal_evidence_resolution` missing_markers=`['action:verifiable evidence']`
  - warning: coverage gap: cand_2024_01_12_local_exploratory/manifest_terms_evidence gate_class=terms_legal_evidence_resolution missing=['action:verifiable evidence']
- window=`cand_2024_01_12_local_exploratory` prerequisite=`manifest_terms_evidence.provenance_manifest` current_state=`present_blocker` gate_class=`provenance_manifest_evidence` missing_action_class=`provenance_manifest_evidence` missing_markers=`['action:identity-verified', 'action:bounded', 'check:fclr015']`
  - warning: coverage gap: cand_2024_01_12_local_exploratory/manifest_terms_evidence.provenance_manifest gate_class=provenance_manifest_evidence missing=['action:identity-verified', 'action:bounded', 'check:fclr015']
- window=`cand_2024_01_12_local_exploratory` prerequisite=`manifest_terms_evidence.terms_evidence` current_state=`present_blocker` gate_class=`terms_legal_evidence_resolution` missing_action_class=`terms_legal_evidence_resolution` missing_markers=`['action:terms', 'check:fclr016_v5_admissibility_report', 'check:fclr016_v5_promotion_dryrun']`
  - warning: coverage gap: cand_2024_01_12_local_exploratory/manifest_terms_evidence.terms_evidence gate_class=terms_legal_evidence_resolution missing=['action:terms', 'check:fclr016_v5_admissibility_report', 'check:fclr016_v5_promotion_dryrun']
- window=`cand_2024_01_12_local_exploratory` prerequisite=`admissibility_package_status.completeness_leakage_audit` current_state=`present_blocker` gate_class=`admissibility_completeness_leakage_evidence` missing_action_class=`admissibility_completeness_leakage_evidence` missing_markers=`['action:admissibility']`
  - warning: coverage gap: cand_2024_01_12_local_exploratory/admissibility_package_status.completeness_leakage_audit gate_class=admissibility_completeness_leakage_evidence missing=['action:admissibility']
- window=`cand_2024_01_12_local_exploratory` prerequisite=`admissibility_package_status.confirmatory_prereg_draft_ref` current_state=`present_blocker` gate_class=`fresh_frozen_prereg_before_outcomes` missing_action_class=`fresh_frozen_prereg_before_outcomes` missing_markers=`['action:fresh frozen preregistration', 'action:before any confirmatory outcomes', 'check:run_funding_ablations']`
  - warning: coverage gap: cand_2024_01_12_local_exploratory/admissibility_package_status.confirmatory_prereg_draft_ref gate_class=fresh_frozen_prereg_before_outcomes missing=['action:fresh frozen preregistration', 'action:before any confirmatory outcomes', 'check:run_funding_ablations']
- window=`cand_2024_01_12_local_exploratory` prerequisite=`admissibility_package_status.v5_window_terms_state_from_fclr018` current_state=`present_blocker` gate_class=`terms_legal_evidence_resolution` missing_action_class=`terms_legal_evidence_resolution` missing_markers=`['action:terms', 'action:human/legal', 'action:fabricated=false', 'action:verifiable evidence', 'check:fclr016_v5_admissibility_report', 'check:fclr016_v5_promotion_dryrun']`
  - warning: coverage gap: cand_2024_01_12_local_exploratory/admissibility_package_status.v5_window_terms_state_from_fclr018 gate_class=terms_legal_evidence_resolution missing=['action:terms', 'action:human/legal', 'action:fabricated=false', 'action:verifiable evidence', 'check:fclr016_v5_admissibility_report', 'check:fclr016_v5_promotion_dryrun']
- window=`cand_2024_01_12_local_exploratory` prerequisite=`fresh_frozen_prereg_before_outcomes_required` current_state=`missing` gate_class=`fresh_frozen_prereg_before_outcomes` missing_action_class=`fresh_frozen_prereg_before_outcomes` missing_markers=`['action:fresh frozen preregistration', 'check:run_funding_ablations']`
  - warning: coverage gap: cand_2024_01_12_local_exploratory/fresh_frozen_prereg_before_outcomes_required gate_class=fresh_frozen_prereg_before_outcomes missing=['action:fresh frozen preregistration', 'check:run_funding_ablations']
- window=`cand_2024_01_12_local_exploratory` prerequisite=`leakage_sufficiency_gates` current_state=`present_blocker` gate_class=`leakage_sufficiency_gates` missing_action_class=`leakage_sufficiency_gates` missing_markers=`['action:sufficiency']`
  - warning: coverage gap: cand_2024_01_12_local_exploratory/leakage_sufficiency_gates gate_class=leakage_sufficiency_gates missing=['action:sufficiency']

## Coverage matrix (per window / prerequisite)
### cand_2024_04_09_evidenced — identity_provenance_range (Identity/provenance range evidence (bounded))
- current_state=**present_unverified** gate_class=`provenance_manifest_evidence` coverage_ok=`False` missing_action_class=`provenance_manifest_evidence` missing_markers=`['action:hash', 'action:identity-verified', 'check:sha256sum', 'check:test -f', 'check:json_ok']`
- blocker_or_missing_reason: IDENTITY_VERIFIED_BOUNDED_FCLR015 for window per fclr018; confirmatory still bounded by ranges/manifest/terms/fresh-frozen-prereg
- evidence_ref: `fclr018.window.provenance_status` snapshot=`missing`
- verification_command_or_check: `test -f fclr018.window.provenance_status && sha256sum fclr018.window.provenance_status  # read-only existence/hash check`
- verification_command_or_check: `python -m unittest discover tests -q  # baseline regression (no confirmatory outcomes)`
- verification_command_or_check: `python scripts/check_tracka_scope_registry_drift.py  # read-only drift check`
- verification_command_or_check: `python scripts/tracka_resume_check.py  # read-only resume check (network:false)`
- verification_command_or_check: `python -m unittest discover tests -q  # baseline regression (no confirmatory outcomes)`
- verification_command_or_check: `python scripts/check_tracka_scope_registry_drift.py  # read-only drift check`
- verification_command_or_check: `python scripts/tracka_resume_check.py  # read-only resume check (network:false)`
- verification_command_or_check: `python scripts/fclr015_gate4_cache_input_manifest.py --help >/dev/null 2>&1 || true  # read-only capability check (no confirmatory outcomes)`

### cand_2024_04_09_evidenced — manifest_terms_evidence (Manifest/terms evidence package)
- current_state=**present_blocker** gate_class=`terms_legal_evidence_resolution` coverage_ok=`False` missing_action_class=`terms_legal_evidence_resolution` missing_markers=`['action:verifiable evidence']`
- blocker_or_missing_reason: provenance_manifest=present_blocker, terms_evidence=present_blocker
- verification_command_or_check: `python -m unittest discover tests -q  # baseline regression (no confirmatory outcomes)`
- verification_command_or_check: `python scripts/check_tracka_scope_registry_drift.py  # read-only drift check`
- verification_command_or_check: `python scripts/tracka_resume_check.py  # read-only resume check (network:false)`
- verification_command_or_check: `python -m unittest discover tests -q  # baseline regression (no confirmatory outcomes)`
- verification_command_or_check: `python scripts/check_tracka_scope_registry_drift.py  # read-only drift check`
- verification_command_or_check: `python scripts/tracka_resume_check.py  # read-only resume check (network:false)`
- verification_command_or_check: `python scripts/fclr016_v5_admissibility_report.py --bogus --json 2>&1 | head -c 200  # refusal path must be parseable, exit!=0 expected`
- verification_command_or_check: `python scripts/fclr016_v5_promotion_dryrun.py --bogus --json 2>&1 | head -c 200  # refusal path must be parseable, exit!=0 expected`

### cand_2024_04_09_evidenced — manifest_terms_evidence.provenance_manifest (Provenance/license manifest artifact)
- current_state=**present_blocker** gate_class=`provenance_manifest_evidence` coverage_ok=`False` missing_action_class=`provenance_manifest_evidence` missing_markers=`['action:identity-verified', 'action:bounded', 'check:fclr015']`
- blocker_or_missing_reason: confirmatory_provenance_go_false_or_missing
- evidence_ref: `research_state/fclr016_local_audit/fclr016_v5_provenance_license_manifest_20261108T014405Z.json` snapshot=`readable`
- verification_command_or_check: `test -f research_state/fclr016_local_audit/fclr016_v5_provenance_license_manifest_20261108T014405Z.json && sha256sum research_state/fclr016_local_audit/fclr016_v5_provenance_license_manifest_20261108T014405Z.json  # read-only existence/hash check`
- verification_command_or_check: `python3 -c "import json; json.load(open('research_state/fclr016_local_audit/fclr016_v5_provenance_license_manifest_20261108T014405Z.json')); print('json_ok')"  # read-only parse check`
- verification_command_or_check: `python -m unittest discover tests -q  # baseline regression (no confirmatory outcomes)`
- verification_command_or_check: `python scripts/check_tracka_scope_registry_drift.py  # read-only drift check`
- verification_command_or_check: `python scripts/tracka_resume_check.py  # read-only resume check (network:false)`
- verification_command_or_check: `test -f research_state/fclr016_local_audit/fclr016_v5_provenance_license_manifest_20261108T014405Z.json && sha256sum research_state/fclr016_local_audit/fclr016_v5_provenance_license_manifest_20261108T014405Z.json  # read-only existence/hash check`
- verification_command_or_check: `python3 -c "import json; json.load(open('research_state/fclr016_local_audit/fclr016_v5_provenance_license_manifest_20261108T014405Z.json')); print('json_ok')"  # read-only parse check`
- verification_command_or_check: `python -m unittest discover tests -q  # baseline regression (no confirmatory outcomes)`
- verification_command_or_check: `python scripts/check_tracka_scope_registry_drift.py  # read-only drift check`
- verification_command_or_check: `python scripts/tracka_resume_check.py  # read-only resume check (network:false)`

### cand_2024_04_09_evidenced — manifest_terms_evidence.terms_evidence (Terms/license evidence artifact (human/legal))
- current_state=**present_blocker** gate_class=`terms_legal_evidence_resolution` coverage_ok=`False` missing_action_class=`terms_legal_evidence_resolution` missing_markers=`['action:terms', 'check:fclr016_v5_admissibility_report', 'check:fclr016_v5_promotion_dryrun']`
- blocker_or_missing_reason: terms_status=EXPLICIT_BLOCKER_UNRESOLVED
- evidence_ref: `research_state/fclr016_local_audit/fclr016_v5_terms_evidence_BLOCKED_20261108T014835Z.json` snapshot=`readable`
- verification_command_or_check: `test -f research_state/fclr016_local_audit/fclr016_v5_terms_evidence_BLOCKED_20261108T014835Z.json && sha256sum research_state/fclr016_local_audit/fclr016_v5_terms_evidence_BLOCKED_20261108T014835Z.json  # read-only existence/hash check`
- verification_command_or_check: `python3 -c "import json; json.load(open('research_state/fclr016_local_audit/fclr016_v5_terms_evidence_BLOCKED_20261108T014835Z.json')); print('json_ok')"  # read-only parse check`
- verification_command_or_check: `python -m unittest discover tests -q  # baseline regression (no confirmatory outcomes)`
- verification_command_or_check: `python scripts/check_tracka_scope_registry_drift.py  # read-only drift check`
- verification_command_or_check: `python scripts/tracka_resume_check.py  # read-only resume check (network:false)`
- verification_command_or_check: `test -f research_state/fclr016_local_audit/fclr016_v5_terms_evidence_BLOCKED_20261108T014835Z.json && sha256sum research_state/fclr016_local_audit/fclr016_v5_terms_evidence_BLOCKED_20261108T014835Z.json  # read-only existence/hash check`
- verification_command_or_check: `python3 -c "import json; json.load(open('research_state/fclr016_local_audit/fclr016_v5_terms_evidence_BLOCKED_20261108T014835Z.json')); print('json_ok')"  # read-only parse check`
- verification_command_or_check: `python -m unittest discover tests -q  # baseline regression (no confirmatory outcomes)`
- verification_command_or_check: `python scripts/check_tracka_scope_registry_drift.py  # read-only drift check`
- verification_command_or_check: `python scripts/tracka_resume_check.py  # read-only resume check (network:false)`

### cand_2024_04_09_evidenced — admissibility_package_status (Admissibility package status)
- current_state=**present_blocker** gate_class=`admissibility_completeness_leakage_evidence` coverage_ok=`True` missing_action_class=`None` missing_markers=`[]`
- blocker_or_missing_reason: completeness=present_blocker, prereg_draft=None, v5_window=present_blocker
- verification_command_or_check: `python -m unittest discover tests -q  # baseline regression (no confirmatory outcomes)`
- verification_command_or_check: `python scripts/check_tracka_scope_registry_drift.py  # read-only drift check`
- verification_command_or_check: `python scripts/tracka_resume_check.py  # read-only resume check (network:false)`
- verification_command_or_check: `python -m unittest discover tests -q  # baseline regression (no confirmatory outcomes)`
- verification_command_or_check: `python scripts/check_tracka_scope_registry_drift.py  # read-only drift check`
- verification_command_or_check: `python scripts/tracka_resume_check.py  # read-only resume check (network:false)`

### cand_2024_04_09_evidenced — admissibility_package_status.completeness_leakage_audit (Completeness/leakage audit artifact)
- current_state=**present_blocker** gate_class=`admissibility_completeness_leakage_evidence` coverage_ok=`False` missing_action_class=`admissibility_completeness_leakage_evidence` missing_markers=`['action:admissibility']`
- blocker_or_missing_reason: blockers_remaining_count=2
- evidence_ref: `research_state/fclr016_local_audit/fclr016_v5_completeness_leakage_audit_20261108T014405Z.json` snapshot=`readable`
- verification_command_or_check: `test -f research_state/fclr016_local_audit/fclr016_v5_completeness_leakage_audit_20261108T014405Z.json && sha256sum research_state/fclr016_local_audit/fclr016_v5_completeness_leakage_audit_20261108T014405Z.json  # read-only existence/hash check`
- verification_command_or_check: `python3 -c "import json; json.load(open('research_state/fclr016_local_audit/fclr016_v5_completeness_leakage_audit_20261108T014405Z.json')); print('json_ok')"  # read-only parse check`
- verification_command_or_check: `python -m unittest discover tests -q  # baseline regression (no confirmatory outcomes)`
- verification_command_or_check: `python scripts/check_tracka_scope_registry_drift.py  # read-only drift check`
- verification_command_or_check: `python scripts/tracka_resume_check.py  # read-only resume check (network:false)`
- verification_command_or_check: `test -f research_state/fclr016_local_audit/fclr016_v5_completeness_leakage_audit_20261108T014405Z.json && sha256sum research_state/fclr016_local_audit/fclr016_v5_completeness_leakage_audit_20261108T014405Z.json  # read-only existence/hash check`
- verification_command_or_check: `python3 -c "import json; json.load(open('research_state/fclr016_local_audit/fclr016_v5_completeness_leakage_audit_20261108T014405Z.json')); print('json_ok')"  # read-only parse check`
- verification_command_or_check: `python -m unittest discover tests -q  # baseline regression (no confirmatory outcomes)`
- verification_command_or_check: `python scripts/check_tracka_scope_registry_drift.py  # read-only drift check`
- verification_command_or_check: `python scripts/tracka_resume_check.py  # read-only resume check (network:false)`

### cand_2024_04_09_evidenced — admissibility_package_status.confirmatory_prereg_draft_ref (Confirmatory prereg draft/ref artifact (not fresh frozen prereg))
- current_state=**present_blocker** gate_class=`fresh_frozen_prereg_before_outcomes` coverage_ok=`False` missing_action_class=`fresh_frozen_prereg_before_outcomes` missing_markers=`['action:fresh frozen preregistration', 'action:before any confirmatory outcomes', 'check:run_funding_ablations']`
- blocker_or_missing_reason: prereg_draft_or_not_frozen_before_outcomes
- evidence_ref: `research_state/fclr016_local_audit/fclr016_v5_confirmatory_prereg_DRAFT_20261108T014835Z.json` snapshot=`readable`
- verification_command_or_check: `test -f research_state/fclr016_local_audit/fclr016_v5_confirmatory_prereg_DRAFT_20261108T014835Z.json && sha256sum research_state/fclr016_local_audit/fclr016_v5_confirmatory_prereg_DRAFT_20261108T014835Z.json  # read-only existence/hash check`
- verification_command_or_check: `python3 -c "import json; json.load(open('research_state/fclr016_local_audit/fclr016_v5_confirmatory_prereg_DRAFT_20261108T014835Z.json')); print('json_ok')"  # read-only parse check`
- verification_command_or_check: `python -m unittest discover tests -q  # baseline regression (no confirmatory outcomes)`
- verification_command_or_check: `python scripts/check_tracka_scope_registry_drift.py  # read-only drift check`
- verification_command_or_check: `python scripts/tracka_resume_check.py  # read-only resume check (network:false)`
- verification_command_or_check: `test -f research_state/fclr016_local_audit/fclr016_v5_confirmatory_prereg_DRAFT_20261108T014835Z.json && sha256sum research_state/fclr016_local_audit/fclr016_v5_confirmatory_prereg_DRAFT_20261108T014835Z.json  # read-only existence/hash check`
- verification_command_or_check: `python3 -c "import json; json.load(open('research_state/fclr016_local_audit/fclr016_v5_confirmatory_prereg_DRAFT_20261108T014835Z.json')); print('json_ok')"  # read-only parse check`
- verification_command_or_check: `python -m unittest discover tests -q  # baseline regression (no confirmatory outcomes)`
- verification_command_or_check: `python scripts/check_tracka_scope_registry_drift.py  # read-only drift check`
- verification_command_or_check: `python scripts/tracka_resume_check.py  # read-only resume check (network:false)`

### cand_2024_04_09_evidenced — admissibility_package_status.v5_window_terms_state_from_fclr018 (v5 window terms/admissibility state (from FCLR-018))
- current_state=**present_blocker** gate_class=`terms_legal_evidence_resolution` coverage_ok=`False` missing_action_class=`terms_legal_evidence_resolution` missing_markers=`['action:terms', 'action:human/legal', 'action:fabricated=false', 'action:verifiable evidence', 'check:fclr016_v5_admissibility_report', 'check:fclr016_v5_promotion_dryrun']`
- blocker_or_missing_reason: terms_status=EXPLICIT_BLOCKER_UNRESOLVED all_go=False confirmatory_outcomes_permitted=False
- evidence_ref: `fclr018.window.v5_terms_blocker_state` snapshot=`missing`
- verification_command_or_check: `test -f fclr018.window.v5_terms_blocker_state && sha256sum fclr018.window.v5_terms_blocker_state  # read-only existence/hash check`
- verification_command_or_check: `python -m unittest discover tests -q  # baseline regression (no confirmatory outcomes)`
- verification_command_or_check: `python scripts/check_tracka_scope_registry_drift.py  # read-only drift check`
- verification_command_or_check: `python scripts/tracka_resume_check.py  # read-only resume check (network:false)`
- verification_command_or_check: `python -m unittest discover tests -q  # baseline regression (no confirmatory outcomes)`
- verification_command_or_check: `python scripts/check_tracka_scope_registry_drift.py  # read-only drift check`
- verification_command_or_check: `python scripts/tracka_resume_check.py  # read-only resume check (network:false)`

### cand_2024_04_09_evidenced — fresh_frozen_prereg_before_outcomes_required (Fresh frozen prereg before outcomes (required))
- current_state=**missing** gate_class=`fresh_frozen_prereg_before_outcomes` coverage_ok=`False` missing_action_class=`fresh_frozen_prereg_before_outcomes` missing_markers=`['action:fresh frozen preregistration', 'check:run_funding_ablations']`
- blocker_or_missing_reason: fresh frozen prereg before outcomes required = missing/not frozen (no concrete local frozen prereg artifact confirmed by this index)
- verification_command_or_check: `python -m unittest discover tests -q  # baseline regression (no confirmatory outcomes)`
- verification_command_or_check: `python scripts/check_tracka_scope_registry_drift.py  # read-only drift check`
- verification_command_or_check: `python scripts/tracka_resume_check.py  # read-only resume check (network:false)`
- verification_command_or_check: `python -m unittest discover tests -q  # baseline regression (no confirmatory outcomes)`
- verification_command_or_check: `python scripts/check_tracka_scope_registry_drift.py  # read-only drift check`
- verification_command_or_check: `python scripts/tracka_resume_check.py  # read-only resume check (network:false)`
- verification_command_or_check: `test ! -f research_state/NO_SUCH_FRESH_FROZEN_PREREG  # placeholder reminder: a concrete frozen prereg artifact path must be supplied and verified before outcomes`

### cand_2024_04_09_evidenced — leakage_sufficiency_gates (Leakage controls and data sufficiency gates)
- current_state=**present_unverified** gate_class=`leakage_sufficiency_gates` coverage_ok=`False` missing_action_class=`leakage_sufficiency_gates` missing_markers=`['action:sufficiency']`
- blocker_or_missing_reason: local coverage/block-count feasibility fields present; leakage audit for any confirmatory run still requires fresh frozen prereg + admissibility package
- evidence_ref: `fclr018.window.coverage/block_fields` snapshot=`missing`
- verification_command_or_check: `test -f fclr018.window.coverage/block_fields && sha256sum fclr018.window.coverage/block_fields  # read-only existence/hash check`
- verification_command_or_check: `python -m unittest discover tests -q  # baseline regression (no confirmatory outcomes)`
- verification_command_or_check: `python scripts/check_tracka_scope_registry_drift.py  # read-only drift check`
- verification_command_or_check: `python scripts/tracka_resume_check.py  # read-only resume check (network:false)`
- verification_command_or_check: `python -m unittest discover tests -q  # baseline regression (no confirmatory outcomes)`
- verification_command_or_check: `python scripts/check_tracka_scope_registry_drift.py  # read-only drift check`
- verification_command_or_check: `python scripts/tracka_resume_check.py  # read-only resume check (network:false)`
- verification_command_or_check: `python scripts/run_funding_ablations.py  # baseline pilot must run clean with honest verdict (no confirmatory claim from this command alone)`

### cand_2024_10_12_local_exploratory — identity_provenance_range (Identity/provenance range evidence (bounded))
- current_state=**present_blocker** gate_class=`provenance_manifest_evidence` coverage_ok=`False` missing_action_class=`provenance_manifest_evidence` missing_markers=`['action:manifest', 'check:sha256sum', 'check:test -f', 'check:json_ok']`
- blocker_or_missing_reason: provenance_status=UNVERIFIED; reasons=['v5_terms_blocker_unresolved_all_go_false', 'provenance_not_identity_verified_bounded_fclr015', 'calendar_coverage_incomplete_or_unverified', 'block_count_gate_lt_3']
- evidence_ref: `fclr018.window.provenance_status` snapshot=`missing`
- verification_command_or_check: `test -f fclr018.window.provenance_status && sha256sum fclr018.window.provenance_status  # read-only existence/hash check`
- verification_command_or_check: `python -m unittest discover tests -q  # baseline regression (no confirmatory outcomes)`
- verification_command_or_check: `python scripts/check_tracka_scope_registry_drift.py  # read-only drift check`
- verification_command_or_check: `python scripts/tracka_resume_check.py  # read-only resume check (network:false)`
- verification_command_or_check: `python -m unittest discover tests -q  # baseline regression (no confirmatory outcomes)`
- verification_command_or_check: `python scripts/check_tracka_scope_registry_drift.py  # read-only drift check`
- verification_command_or_check: `python scripts/tracka_resume_check.py  # read-only resume check (network:false)`
- verification_command_or_check: `python scripts/fclr015_gate4_cache_input_manifest.py --help >/dev/null 2>&1 || true  # read-only capability check (no confirmatory outcomes)`

### cand_2024_10_12_local_exploratory — manifest_terms_evidence (Manifest/terms evidence package)
- current_state=**present_blocker** gate_class=`terms_legal_evidence_resolution` coverage_ok=`False` missing_action_class=`terms_legal_evidence_resolution` missing_markers=`['action:verifiable evidence']`
- blocker_or_missing_reason: provenance_manifest=present_blocker, terms_evidence=present_blocker
- verification_command_or_check: `python -m unittest discover tests -q  # baseline regression (no confirmatory outcomes)`
- verification_command_or_check: `python scripts/check_tracka_scope_registry_drift.py  # read-only drift check`
- verification_command_or_check: `python scripts/tracka_resume_check.py  # read-only resume check (network:false)`
- verification_command_or_check: `python -m unittest discover tests -q  # baseline regression (no confirmatory outcomes)`
- verification_command_or_check: `python scripts/check_tracka_scope_registry_drift.py  # read-only drift check`
- verification_command_or_check: `python scripts/tracka_resume_check.py  # read-only resume check (network:false)`
- verification_command_or_check: `python scripts/fclr016_v5_admissibility_report.py --bogus --json 2>&1 | head -c 200  # refusal path must be parseable, exit!=0 expected`
- verification_command_or_check: `python scripts/fclr016_v5_promotion_dryrun.py --bogus --json 2>&1 | head -c 200  # refusal path must be parseable, exit!=0 expected`

### cand_2024_10_12_local_exploratory — manifest_terms_evidence.provenance_manifest (Provenance/license manifest artifact)
- current_state=**present_blocker** gate_class=`provenance_manifest_evidence` coverage_ok=`False` missing_action_class=`provenance_manifest_evidence` missing_markers=`['action:identity-verified', 'action:bounded', 'check:fclr015']`
- blocker_or_missing_reason: confirmatory_provenance_go_false_or_missing
- evidence_ref: `research_state/fclr016_local_audit/fclr016_v5_provenance_license_manifest_20261108T014405Z.json` snapshot=`readable`
- verification_command_or_check: `test -f research_state/fclr016_local_audit/fclr016_v5_provenance_license_manifest_20261108T014405Z.json && sha256sum research_state/fclr016_local_audit/fclr016_v5_provenance_license_manifest_20261108T014405Z.json  # read-only existence/hash check`
- verification_command_or_check: `python3 -c "import json; json.load(open('research_state/fclr016_local_audit/fclr016_v5_provenance_license_manifest_20261108T014405Z.json')); print('json_ok')"  # read-only parse check`
- verification_command_or_check: `python -m unittest discover tests -q  # baseline regression (no confirmatory outcomes)`
- verification_command_or_check: `python scripts/check_tracka_scope_registry_drift.py  # read-only drift check`
- verification_command_or_check: `python scripts/tracka_resume_check.py  # read-only resume check (network:false)`
- verification_command_or_check: `test -f research_state/fclr016_local_audit/fclr016_v5_provenance_license_manifest_20261108T014405Z.json && sha256sum research_state/fclr016_local_audit/fclr016_v5_provenance_license_manifest_20261108T014405Z.json  # read-only existence/hash check`
- verification_command_or_check: `python3 -c "import json; json.load(open('research_state/fclr016_local_audit/fclr016_v5_provenance_license_manifest_20261108T014405Z.json')); print('json_ok')"  # read-only parse check`
- verification_command_or_check: `python -m unittest discover tests -q  # baseline regression (no confirmatory outcomes)`
- verification_command_or_check: `python scripts/check_tracka_scope_registry_drift.py  # read-only drift check`
- verification_command_or_check: `python scripts/tracka_resume_check.py  # read-only resume check (network:false)`

### cand_2024_10_12_local_exploratory — manifest_terms_evidence.terms_evidence (Terms/license evidence artifact (human/legal))
- current_state=**present_blocker** gate_class=`terms_legal_evidence_resolution` coverage_ok=`False` missing_action_class=`terms_legal_evidence_resolution` missing_markers=`['action:terms', 'check:fclr016_v5_admissibility_report', 'check:fclr016_v5_promotion_dryrun']`
- blocker_or_missing_reason: terms_status=EXPLICIT_BLOCKER_UNRESOLVED
- evidence_ref: `research_state/fclr016_local_audit/fclr016_v5_terms_evidence_BLOCKED_20261108T014835Z.json` snapshot=`readable`
- verification_command_or_check: `test -f research_state/fclr016_local_audit/fclr016_v5_terms_evidence_BLOCKED_20261108T014835Z.json && sha256sum research_state/fclr016_local_audit/fclr016_v5_terms_evidence_BLOCKED_20261108T014835Z.json  # read-only existence/hash check`
- verification_command_or_check: `python3 -c "import json; json.load(open('research_state/fclr016_local_audit/fclr016_v5_terms_evidence_BLOCKED_20261108T014835Z.json')); print('json_ok')"  # read-only parse check`
- verification_command_or_check: `python -m unittest discover tests -q  # baseline regression (no confirmatory outcomes)`
- verification_command_or_check: `python scripts/check_tracka_scope_registry_drift.py  # read-only drift check`
- verification_command_or_check: `python scripts/tracka_resume_check.py  # read-only resume check (network:false)`
- verification_command_or_check: `test -f research_state/fclr016_local_audit/fclr016_v5_terms_evidence_BLOCKED_20261108T014835Z.json && sha256sum research_state/fclr016_local_audit/fclr016_v5_terms_evidence_BLOCKED_20261108T014835Z.json  # read-only existence/hash check`
- verification_command_or_check: `python3 -c "import json; json.load(open('research_state/fclr016_local_audit/fclr016_v5_terms_evidence_BLOCKED_20261108T014835Z.json')); print('json_ok')"  # read-only parse check`
- verification_command_or_check: `python -m unittest discover tests -q  # baseline regression (no confirmatory outcomes)`
- verification_command_or_check: `python scripts/check_tracka_scope_registry_drift.py  # read-only drift check`
- verification_command_or_check: `python scripts/tracka_resume_check.py  # read-only resume check (network:false)`

### cand_2024_10_12_local_exploratory — admissibility_package_status (Admissibility package status)
- current_state=**present_blocker** gate_class=`admissibility_completeness_leakage_evidence` coverage_ok=`True` missing_action_class=`None` missing_markers=`[]`
- blocker_or_missing_reason: completeness=present_blocker, prereg_draft=None, v5_window=present_blocker
- verification_command_or_check: `python -m unittest discover tests -q  # baseline regression (no confirmatory outcomes)`
- verification_command_or_check: `python scripts/check_tracka_scope_registry_drift.py  # read-only drift check`
- verification_command_or_check: `python scripts/tracka_resume_check.py  # read-only resume check (network:false)`
- verification_command_or_check: `python -m unittest discover tests -q  # baseline regression (no confirmatory outcomes)`
- verification_command_or_check: `python scripts/check_tracka_scope_registry_drift.py  # read-only drift check`
- verification_command_or_check: `python scripts/tracka_resume_check.py  # read-only resume check (network:false)`

### cand_2024_10_12_local_exploratory — admissibility_package_status.completeness_leakage_audit (Completeness/leakage audit artifact)
- current_state=**present_blocker** gate_class=`admissibility_completeness_leakage_evidence` coverage_ok=`False` missing_action_class=`admissibility_completeness_leakage_evidence` missing_markers=`['action:admissibility']`
- blocker_or_missing_reason: blockers_remaining_count=2
- evidence_ref: `research_state/fclr016_local_audit/fclr016_v5_completeness_leakage_audit_20261108T014405Z.json` snapshot=`readable`
- verification_command_or_check: `test -f research_state/fclr016_local_audit/fclr016_v5_completeness_leakage_audit_20261108T014405Z.json && sha256sum research_state/fclr016_local_audit/fclr016_v5_completeness_leakage_audit_20261108T014405Z.json  # read-only existence/hash check`
- verification_command_or_check: `python3 -c "import json; json.load(open('research_state/fclr016_local_audit/fclr016_v5_completeness_leakage_audit_20261108T014405Z.json')); print('json_ok')"  # read-only parse check`
- verification_command_or_check: `python -m unittest discover tests -q  # baseline regression (no confirmatory outcomes)`
- verification_command_or_check: `python scripts/check_tracka_scope_registry_drift.py  # read-only drift check`
- verification_command_or_check: `python scripts/tracka_resume_check.py  # read-only resume check (network:false)`
- verification_command_or_check: `test -f research_state/fclr016_local_audit/fclr016_v5_completeness_leakage_audit_20261108T014405Z.json && sha256sum research_state/fclr016_local_audit/fclr016_v5_completeness_leakage_audit_20261108T014405Z.json  # read-only existence/hash check`
- verification_command_or_check: `python3 -c "import json; json.load(open('research_state/fclr016_local_audit/fclr016_v5_completeness_leakage_audit_20261108T014405Z.json')); print('json_ok')"  # read-only parse check`
- verification_command_or_check: `python -m unittest discover tests -q  # baseline regression (no confirmatory outcomes)`
- verification_command_or_check: `python scripts/check_tracka_scope_registry_drift.py  # read-only drift check`
- verification_command_or_check: `python scripts/tracka_resume_check.py  # read-only resume check (network:false)`

### cand_2024_10_12_local_exploratory — admissibility_package_status.confirmatory_prereg_draft_ref (Confirmatory prereg draft/ref artifact (not fresh frozen prereg))
- current_state=**present_blocker** gate_class=`fresh_frozen_prereg_before_outcomes` coverage_ok=`False` missing_action_class=`fresh_frozen_prereg_before_outcomes` missing_markers=`['action:fresh frozen preregistration', 'action:before any confirmatory outcomes', 'check:run_funding_ablations']`
- blocker_or_missing_reason: prereg_draft_or_not_frozen_before_outcomes
- evidence_ref: `research_state/fclr016_local_audit/fclr016_v5_confirmatory_prereg_DRAFT_20261108T014835Z.json` snapshot=`readable`
- verification_command_or_check: `test -f research_state/fclr016_local_audit/fclr016_v5_confirmatory_prereg_DRAFT_20261108T014835Z.json && sha256sum research_state/fclr016_local_audit/fclr016_v5_confirmatory_prereg_DRAFT_20261108T014835Z.json  # read-only existence/hash check`
- verification_command_or_check: `python3 -c "import json; json.load(open('research_state/fclr016_local_audit/fclr016_v5_confirmatory_prereg_DRAFT_20261108T014835Z.json')); print('json_ok')"  # read-only parse check`
- verification_command_or_check: `python -m unittest discover tests -q  # baseline regression (no confirmatory outcomes)`
- verification_command_or_check: `python scripts/check_tracka_scope_registry_drift.py  # read-only drift check`
- verification_command_or_check: `python scripts/tracka_resume_check.py  # read-only resume check (network:false)`
- verification_command_or_check: `test -f research_state/fclr016_local_audit/fclr016_v5_confirmatory_prereg_DRAFT_20261108T014835Z.json && sha256sum research_state/fclr016_local_audit/fclr016_v5_confirmatory_prereg_DRAFT_20261108T014835Z.json  # read-only existence/hash check`
- verification_command_or_check: `python3 -c "import json; json.load(open('research_state/fclr016_local_audit/fclr016_v5_confirmatory_prereg_DRAFT_20261108T014835Z.json')); print('json_ok')"  # read-only parse check`
- verification_command_or_check: `python -m unittest discover tests -q  # baseline regression (no confirmatory outcomes)`
- verification_command_or_check: `python scripts/check_tracka_scope_registry_drift.py  # read-only drift check`
- verification_command_or_check: `python scripts/tracka_resume_check.py  # read-only resume check (network:false)`

### cand_2024_10_12_local_exploratory — admissibility_package_status.v5_window_terms_state_from_fclr018 (v5 window terms/admissibility state (from FCLR-018))
- current_state=**present_blocker** gate_class=`terms_legal_evidence_resolution` coverage_ok=`False` missing_action_class=`terms_legal_evidence_resolution` missing_markers=`['action:terms', 'action:human/legal', 'action:fabricated=false', 'action:verifiable evidence', 'check:fclr016_v5_admissibility_report', 'check:fclr016_v5_promotion_dryrun']`
- blocker_or_missing_reason: terms_status=EXPLICIT_BLOCKER_UNRESOLVED all_go=False confirmatory_outcomes_permitted=False
- evidence_ref: `fclr018.window.v5_terms_blocker_state` snapshot=`missing`
- verification_command_or_check: `test -f fclr018.window.v5_terms_blocker_state && sha256sum fclr018.window.v5_terms_blocker_state  # read-only existence/hash check`
- verification_command_or_check: `python -m unittest discover tests -q  # baseline regression (no confirmatory outcomes)`
- verification_command_or_check: `python scripts/check_tracka_scope_registry_drift.py  # read-only drift check`
- verification_command_or_check: `python scripts/tracka_resume_check.py  # read-only resume check (network:false)`
- verification_command_or_check: `python -m unittest discover tests -q  # baseline regression (no confirmatory outcomes)`
- verification_command_or_check: `python scripts/check_tracka_scope_registry_drift.py  # read-only drift check`
- verification_command_or_check: `python scripts/tracka_resume_check.py  # read-only resume check (network:false)`

### cand_2024_10_12_local_exploratory — fresh_frozen_prereg_before_outcomes_required (Fresh frozen prereg before outcomes (required))
- current_state=**missing** gate_class=`fresh_frozen_prereg_before_outcomes` coverage_ok=`False` missing_action_class=`fresh_frozen_prereg_before_outcomes` missing_markers=`['action:fresh frozen preregistration', 'check:run_funding_ablations']`
- blocker_or_missing_reason: fresh frozen prereg before outcomes required = missing/not frozen (no concrete local frozen prereg artifact confirmed by this index)
- verification_command_or_check: `python -m unittest discover tests -q  # baseline regression (no confirmatory outcomes)`
- verification_command_or_check: `python scripts/check_tracka_scope_registry_drift.py  # read-only drift check`
- verification_command_or_check: `python scripts/tracka_resume_check.py  # read-only resume check (network:false)`
- verification_command_or_check: `python -m unittest discover tests -q  # baseline regression (no confirmatory outcomes)`
- verification_command_or_check: `python scripts/check_tracka_scope_registry_drift.py  # read-only drift check`
- verification_command_or_check: `python scripts/tracka_resume_check.py  # read-only resume check (network:false)`
- verification_command_or_check: `test ! -f research_state/NO_SUCH_FRESH_FROZEN_PREREG  # placeholder reminder: a concrete frozen prereg artifact path must be supplied and verified before outcomes`

### cand_2024_10_12_local_exploratory — leakage_sufficiency_gates (Leakage controls and data sufficiency gates)
- current_state=**present_blocker** gate_class=`leakage_sufficiency_gates` coverage_ok=`False` missing_action_class=`leakage_sufficiency_gates` missing_markers=`['action:sufficiency']`
- blocker_or_missing_reason: calendar_coverage_incomplete_or_unverified;block_count_gate_lt_3
- evidence_ref: `fclr018.window.coverage/block_fields` snapshot=`missing`
- verification_command_or_check: `test -f fclr018.window.coverage/block_fields && sha256sum fclr018.window.coverage/block_fields  # read-only existence/hash check`
- verification_command_or_check: `python -m unittest discover tests -q  # baseline regression (no confirmatory outcomes)`
- verification_command_or_check: `python scripts/check_tracka_scope_registry_drift.py  # read-only drift check`
- verification_command_or_check: `python scripts/tracka_resume_check.py  # read-only resume check (network:false)`
- verification_command_or_check: `python -m unittest discover tests -q  # baseline regression (no confirmatory outcomes)`
- verification_command_or_check: `python scripts/check_tracka_scope_registry_drift.py  # read-only drift check`
- verification_command_or_check: `python scripts/tracka_resume_check.py  # read-only resume check (network:false)`
- verification_command_or_check: `python scripts/run_funding_ablations.py  # baseline pilot must run clean with honest verdict (no confirmatory claim from this command alone)`

### cand_2024_04_12_mixed_evidenced_prefix — identity_provenance_range (Identity/provenance range evidence (bounded))
- current_state=**present_blocker** gate_class=`provenance_manifest_evidence` coverage_ok=`False` missing_action_class=`provenance_manifest_evidence` missing_markers=`['action:manifest', 'check:sha256sum', 'check:test -f', 'check:json_ok']`
- blocker_or_missing_reason: provenance_status=UNVERIFIED; reasons=['v5_terms_blocker_unresolved_all_go_false', 'provenance_not_identity_verified_bounded_fclr015', 'calendar_coverage_incomplete_or_unverified']
- evidence_ref: `fclr018.window.provenance_status` snapshot=`missing`
- verification_command_or_check: `test -f fclr018.window.provenance_status && sha256sum fclr018.window.provenance_status  # read-only existence/hash check`
- verification_command_or_check: `python -m unittest discover tests -q  # baseline regression (no confirmatory outcomes)`
- verification_command_or_check: `python scripts/check_tracka_scope_registry_drift.py  # read-only drift check`
- verification_command_or_check: `python scripts/tracka_resume_check.py  # read-only resume check (network:false)`
- verification_command_or_check: `python -m unittest discover tests -q  # baseline regression (no confirmatory outcomes)`
- verification_command_or_check: `python scripts/check_tracka_scope_registry_drift.py  # read-only drift check`
- verification_command_or_check: `python scripts/tracka_resume_check.py  # read-only resume check (network:false)`
- verification_command_or_check: `python scripts/fclr015_gate4_cache_input_manifest.py --help >/dev/null 2>&1 || true  # read-only capability check (no confirmatory outcomes)`

### cand_2024_04_12_mixed_evidenced_prefix — manifest_terms_evidence (Manifest/terms evidence package)
- current_state=**present_blocker** gate_class=`terms_legal_evidence_resolution` coverage_ok=`False` missing_action_class=`terms_legal_evidence_resolution` missing_markers=`['action:verifiable evidence']`
- blocker_or_missing_reason: provenance_manifest=present_blocker, terms_evidence=present_blocker
- verification_command_or_check: `python -m unittest discover tests -q  # baseline regression (no confirmatory outcomes)`
- verification_command_or_check: `python scripts/check_tracka_scope_registry_drift.py  # read-only drift check`
- verification_command_or_check: `python scripts/tracka_resume_check.py  # read-only resume check (network:false)`
- verification_command_or_check: `python -m unittest discover tests -q  # baseline regression (no confirmatory outcomes)`
- verification_command_or_check: `python scripts/check_tracka_scope_registry_drift.py  # read-only drift check`
- verification_command_or_check: `python scripts/tracka_resume_check.py  # read-only resume check (network:false)`
- verification_command_or_check: `python scripts/fclr016_v5_admissibility_report.py --bogus --json 2>&1 | head -c 200  # refusal path must be parseable, exit!=0 expected`
- verification_command_or_check: `python scripts/fclr016_v5_promotion_dryrun.py --bogus --json 2>&1 | head -c 200  # refusal path must be parseable, exit!=0 expected`

### cand_2024_04_12_mixed_evidenced_prefix — manifest_terms_evidence.provenance_manifest (Provenance/license manifest artifact)
- current_state=**present_blocker** gate_class=`provenance_manifest_evidence` coverage_ok=`False` missing_action_class=`provenance_manifest_evidence` missing_markers=`['action:identity-verified', 'action:bounded', 'check:fclr015']`
- blocker_or_missing_reason: confirmatory_provenance_go_false_or_missing
- evidence_ref: `research_state/fclr016_local_audit/fclr016_v5_provenance_license_manifest_20261108T014405Z.json` snapshot=`readable`
- verification_command_or_check: `test -f research_state/fclr016_local_audit/fclr016_v5_provenance_license_manifest_20261108T014405Z.json && sha256sum research_state/fclr016_local_audit/fclr016_v5_provenance_license_manifest_20261108T014405Z.json  # read-only existence/hash check`
- verification_command_or_check: `python3 -c "import json; json.load(open('research_state/fclr016_local_audit/fclr016_v5_provenance_license_manifest_20261108T014405Z.json')); print('json_ok')"  # read-only parse check`
- verification_command_or_check: `python -m unittest discover tests -q  # baseline regression (no confirmatory outcomes)`
- verification_command_or_check: `python scripts/check_tracka_scope_registry_drift.py  # read-only drift check`
- verification_command_or_check: `python scripts/tracka_resume_check.py  # read-only resume check (network:false)`
- verification_command_or_check: `test -f research_state/fclr016_local_audit/fclr016_v5_provenance_license_manifest_20261108T014405Z.json && sha256sum research_state/fclr016_local_audit/fclr016_v5_provenance_license_manifest_20261108T014405Z.json  # read-only existence/hash check`
- verification_command_or_check: `python3 -c "import json; json.load(open('research_state/fclr016_local_audit/fclr016_v5_provenance_license_manifest_20261108T014405Z.json')); print('json_ok')"  # read-only parse check`
- verification_command_or_check: `python -m unittest discover tests -q  # baseline regression (no confirmatory outcomes)`
- verification_command_or_check: `python scripts/check_tracka_scope_registry_drift.py  # read-only drift check`
- verification_command_or_check: `python scripts/tracka_resume_check.py  # read-only resume check (network:false)`

### cand_2024_04_12_mixed_evidenced_prefix — manifest_terms_evidence.terms_evidence (Terms/license evidence artifact (human/legal))
- current_state=**present_blocker** gate_class=`terms_legal_evidence_resolution` coverage_ok=`False` missing_action_class=`terms_legal_evidence_resolution` missing_markers=`['action:terms', 'check:fclr016_v5_admissibility_report', 'check:fclr016_v5_promotion_dryrun']`
- blocker_or_missing_reason: terms_status=EXPLICIT_BLOCKER_UNRESOLVED
- evidence_ref: `research_state/fclr016_local_audit/fclr016_v5_terms_evidence_BLOCKED_20261108T014835Z.json` snapshot=`readable`
- verification_command_or_check: `test -f research_state/fclr016_local_audit/fclr016_v5_terms_evidence_BLOCKED_20261108T014835Z.json && sha256sum research_state/fclr016_local_audit/fclr016_v5_terms_evidence_BLOCKED_20261108T014835Z.json  # read-only existence/hash check`
- verification_command_or_check: `python3 -c "import json; json.load(open('research_state/fclr016_local_audit/fclr016_v5_terms_evidence_BLOCKED_20261108T014835Z.json')); print('json_ok')"  # read-only parse check`
- verification_command_or_check: `python -m unittest discover tests -q  # baseline regression (no confirmatory outcomes)`
- verification_command_or_check: `python scripts/check_tracka_scope_registry_drift.py  # read-only drift check`
- verification_command_or_check: `python scripts/tracka_resume_check.py  # read-only resume check (network:false)`
- verification_command_or_check: `test -f research_state/fclr016_local_audit/fclr016_v5_terms_evidence_BLOCKED_20261108T014835Z.json && sha256sum research_state/fclr016_local_audit/fclr016_v5_terms_evidence_BLOCKED_20261108T014835Z.json  # read-only existence/hash check`
- verification_command_or_check: `python3 -c "import json; json.load(open('research_state/fclr016_local_audit/fclr016_v5_terms_evidence_BLOCKED_20261108T014835Z.json')); print('json_ok')"  # read-only parse check`
- verification_command_or_check: `python -m unittest discover tests -q  # baseline regression (no confirmatory outcomes)`
- verification_command_or_check: `python scripts/check_tracka_scope_registry_drift.py  # read-only drift check`
- verification_command_or_check: `python scripts/tracka_resume_check.py  # read-only resume check (network:false)`

### cand_2024_04_12_mixed_evidenced_prefix — admissibility_package_status (Admissibility package status)
- current_state=**present_blocker** gate_class=`admissibility_completeness_leakage_evidence` coverage_ok=`True` missing_action_class=`None` missing_markers=`[]`
- blocker_or_missing_reason: completeness=present_blocker, prereg_draft=None, v5_window=present_blocker
- verification_command_or_check: `python -m unittest discover tests -q  # baseline regression (no confirmatory outcomes)`
- verification_command_or_check: `python scripts/check_tracka_scope_registry_drift.py  # read-only drift check`
- verification_command_or_check: `python scripts/tracka_resume_check.py  # read-only resume check (network:false)`
- verification_command_or_check: `python -m unittest discover tests -q  # baseline regression (no confirmatory outcomes)`
- verification_command_or_check: `python scripts/check_tracka_scope_registry_drift.py  # read-only drift check`
- verification_command_or_check: `python scripts/tracka_resume_check.py  # read-only resume check (network:false)`

### cand_2024_04_12_mixed_evidenced_prefix — admissibility_package_status.completeness_leakage_audit (Completeness/leakage audit artifact)
- current_state=**present_blocker** gate_class=`admissibility_completeness_leakage_evidence` coverage_ok=`False` missing_action_class=`admissibility_completeness_leakage_evidence` missing_markers=`['action:admissibility']`
- blocker_or_missing_reason: blockers_remaining_count=2
- evidence_ref: `research_state/fclr016_local_audit/fclr016_v5_completeness_leakage_audit_20261108T014405Z.json` snapshot=`readable`
- verification_command_or_check: `test -f research_state/fclr016_local_audit/fclr016_v5_completeness_leakage_audit_20261108T014405Z.json && sha256sum research_state/fclr016_local_audit/fclr016_v5_completeness_leakage_audit_20261108T014405Z.json  # read-only existence/hash check`
- verification_command_or_check: `python3 -c "import json; json.load(open('research_state/fclr016_local_audit/fclr016_v5_completeness_leakage_audit_20261108T014405Z.json')); print('json_ok')"  # read-only parse check`
- verification_command_or_check: `python -m unittest discover tests -q  # baseline regression (no confirmatory outcomes)`
- verification_command_or_check: `python scripts/check_tracka_scope_registry_drift.py  # read-only drift check`
- verification_command_or_check: `python scripts/tracka_resume_check.py  # read-only resume check (network:false)`
- verification_command_or_check: `test -f research_state/fclr016_local_audit/fclr016_v5_completeness_leakage_audit_20261108T014405Z.json && sha256sum research_state/fclr016_local_audit/fclr016_v5_completeness_leakage_audit_20261108T014405Z.json  # read-only existence/hash check`
- verification_command_or_check: `python3 -c "import json; json.load(open('research_state/fclr016_local_audit/fclr016_v5_completeness_leakage_audit_20261108T014405Z.json')); print('json_ok')"  # read-only parse check`
- verification_command_or_check: `python -m unittest discover tests -q  # baseline regression (no confirmatory outcomes)`
- verification_command_or_check: `python scripts/check_tracka_scope_registry_drift.py  # read-only drift check`
- verification_command_or_check: `python scripts/tracka_resume_check.py  # read-only resume check (network:false)`

### cand_2024_04_12_mixed_evidenced_prefix — admissibility_package_status.confirmatory_prereg_draft_ref (Confirmatory prereg draft/ref artifact (not fresh frozen prereg))
- current_state=**present_blocker** gate_class=`fresh_frozen_prereg_before_outcomes` coverage_ok=`False` missing_action_class=`fresh_frozen_prereg_before_outcomes` missing_markers=`['action:fresh frozen preregistration', 'action:before any confirmatory outcomes', 'check:run_funding_ablations']`
- blocker_or_missing_reason: prereg_draft_or_not_frozen_before_outcomes
- evidence_ref: `research_state/fclr016_local_audit/fclr016_v5_confirmatory_prereg_DRAFT_20261108T014835Z.json` snapshot=`readable`
- verification_command_or_check: `test -f research_state/fclr016_local_audit/fclr016_v5_confirmatory_prereg_DRAFT_20261108T014835Z.json && sha256sum research_state/fclr016_local_audit/fclr016_v5_confirmatory_prereg_DRAFT_20261108T014835Z.json  # read-only existence/hash check`
- verification_command_or_check: `python3 -c "import json; json.load(open('research_state/fclr016_local_audit/fclr016_v5_confirmatory_prereg_DRAFT_20261108T014835Z.json')); print('json_ok')"  # read-only parse check`
- verification_command_or_check: `python -m unittest discover tests -q  # baseline regression (no confirmatory outcomes)`
- verification_command_or_check: `python scripts/check_tracka_scope_registry_drift.py  # read-only drift check`
- verification_command_or_check: `python scripts/tracka_resume_check.py  # read-only resume check (network:false)`
- verification_command_or_check: `test -f research_state/fclr016_local_audit/fclr016_v5_confirmatory_prereg_DRAFT_20261108T014835Z.json && sha256sum research_state/fclr016_local_audit/fclr016_v5_confirmatory_prereg_DRAFT_20261108T014835Z.json  # read-only existence/hash check`
- verification_command_or_check: `python3 -c "import json; json.load(open('research_state/fclr016_local_audit/fclr016_v5_confirmatory_prereg_DRAFT_20261108T014835Z.json')); print('json_ok')"  # read-only parse check`
- verification_command_or_check: `python -m unittest discover tests -q  # baseline regression (no confirmatory outcomes)`
- verification_command_or_check: `python scripts/check_tracka_scope_registry_drift.py  # read-only drift check`
- verification_command_or_check: `python scripts/tracka_resume_check.py  # read-only resume check (network:false)`

### cand_2024_04_12_mixed_evidenced_prefix — admissibility_package_status.v5_window_terms_state_from_fclr018 (v5 window terms/admissibility state (from FCLR-018))
- current_state=**present_blocker** gate_class=`terms_legal_evidence_resolution` coverage_ok=`False` missing_action_class=`terms_legal_evidence_resolution` missing_markers=`['action:terms', 'action:human/legal', 'action:fabricated=false', 'action:verifiable evidence', 'check:fclr016_v5_admissibility_report', 'check:fclr016_v5_promotion_dryrun']`
- blocker_or_missing_reason: terms_status=EXPLICIT_BLOCKER_UNRESOLVED all_go=False confirmatory_outcomes_permitted=False
- evidence_ref: `fclr018.window.v5_terms_blocker_state` snapshot=`missing`
- verification_command_or_check: `test -f fclr018.window.v5_terms_blocker_state && sha256sum fclr018.window.v5_terms_blocker_state  # read-only existence/hash check`
- verification_command_or_check: `python -m unittest discover tests -q  # baseline regression (no confirmatory outcomes)`
- verification_command_or_check: `python scripts/check_tracka_scope_registry_drift.py  # read-only drift check`
- verification_command_or_check: `python scripts/tracka_resume_check.py  # read-only resume check (network:false)`
- verification_command_or_check: `python -m unittest discover tests -q  # baseline regression (no confirmatory outcomes)`
- verification_command_or_check: `python scripts/check_tracka_scope_registry_drift.py  # read-only drift check`
- verification_command_or_check: `python scripts/tracka_resume_check.py  # read-only resume check (network:false)`

### cand_2024_04_12_mixed_evidenced_prefix — fresh_frozen_prereg_before_outcomes_required (Fresh frozen prereg before outcomes (required))
- current_state=**missing** gate_class=`fresh_frozen_prereg_before_outcomes` coverage_ok=`False` missing_action_class=`fresh_frozen_prereg_before_outcomes` missing_markers=`['action:fresh frozen preregistration', 'check:run_funding_ablations']`
- blocker_or_missing_reason: fresh frozen prereg before outcomes required = missing/not frozen (no concrete local frozen prereg artifact confirmed by this index)
- verification_command_or_check: `python -m unittest discover tests -q  # baseline regression (no confirmatory outcomes)`
- verification_command_or_check: `python scripts/check_tracka_scope_registry_drift.py  # read-only drift check`
- verification_command_or_check: `python scripts/tracka_resume_check.py  # read-only resume check (network:false)`
- verification_command_or_check: `python -m unittest discover tests -q  # baseline regression (no confirmatory outcomes)`
- verification_command_or_check: `python scripts/check_tracka_scope_registry_drift.py  # read-only drift check`
- verification_command_or_check: `python scripts/tracka_resume_check.py  # read-only resume check (network:false)`
- verification_command_or_check: `test ! -f research_state/NO_SUCH_FRESH_FROZEN_PREREG  # placeholder reminder: a concrete frozen prereg artifact path must be supplied and verified before outcomes`

### cand_2024_04_12_mixed_evidenced_prefix — leakage_sufficiency_gates (Leakage controls and data sufficiency gates)
- current_state=**present_blocker** gate_class=`leakage_sufficiency_gates` coverage_ok=`False` missing_action_class=`leakage_sufficiency_gates` missing_markers=`['action:sufficiency']`
- blocker_or_missing_reason: calendar_coverage_incomplete_or_unverified
- evidence_ref: `fclr018.window.coverage/block_fields` snapshot=`missing`
- verification_command_or_check: `test -f fclr018.window.coverage/block_fields && sha256sum fclr018.window.coverage/block_fields  # read-only existence/hash check`
- verification_command_or_check: `python -m unittest discover tests -q  # baseline regression (no confirmatory outcomes)`
- verification_command_or_check: `python scripts/check_tracka_scope_registry_drift.py  # read-only drift check`
- verification_command_or_check: `python scripts/tracka_resume_check.py  # read-only resume check (network:false)`
- verification_command_or_check: `python -m unittest discover tests -q  # baseline regression (no confirmatory outcomes)`
- verification_command_or_check: `python scripts/check_tracka_scope_registry_drift.py  # read-only drift check`
- verification_command_or_check: `python scripts/tracka_resume_check.py  # read-only resume check (network:false)`
- verification_command_or_check: `python scripts/run_funding_ablations.py  # baseline pilot must run clean with honest verdict (no confirmatory claim from this command alone)`

### cand_2025_01_12_local_exploratory — identity_provenance_range (Identity/provenance range evidence (bounded))
- current_state=**present_blocker** gate_class=`provenance_manifest_evidence` coverage_ok=`False` missing_action_class=`provenance_manifest_evidence` missing_markers=`['action:manifest', 'check:sha256sum', 'check:test -f', 'check:json_ok']`
- blocker_or_missing_reason: provenance_status=UNVERIFIED; reasons=['v5_terms_blocker_unresolved_all_go_false', 'provenance_not_identity_verified_bounded_fclr015', 'calendar_coverage_incomplete_or_unverified']
- evidence_ref: `fclr018.window.provenance_status` snapshot=`missing`
- verification_command_or_check: `test -f fclr018.window.provenance_status && sha256sum fclr018.window.provenance_status  # read-only existence/hash check`
- verification_command_or_check: `python -m unittest discover tests -q  # baseline regression (no confirmatory outcomes)`
- verification_command_or_check: `python scripts/check_tracka_scope_registry_drift.py  # read-only drift check`
- verification_command_or_check: `python scripts/tracka_resume_check.py  # read-only resume check (network:false)`
- verification_command_or_check: `python -m unittest discover tests -q  # baseline regression (no confirmatory outcomes)`
- verification_command_or_check: `python scripts/check_tracka_scope_registry_drift.py  # read-only drift check`
- verification_command_or_check: `python scripts/tracka_resume_check.py  # read-only resume check (network:false)`
- verification_command_or_check: `python scripts/fclr015_gate4_cache_input_manifest.py --help >/dev/null 2>&1 || true  # read-only capability check (no confirmatory outcomes)`

### cand_2025_01_12_local_exploratory — manifest_terms_evidence (Manifest/terms evidence package)
- current_state=**present_blocker** gate_class=`terms_legal_evidence_resolution` coverage_ok=`False` missing_action_class=`terms_legal_evidence_resolution` missing_markers=`['action:verifiable evidence']`
- blocker_or_missing_reason: provenance_manifest=present_blocker, terms_evidence=present_blocker
- verification_command_or_check: `python -m unittest discover tests -q  # baseline regression (no confirmatory outcomes)`
- verification_command_or_check: `python scripts/check_tracka_scope_registry_drift.py  # read-only drift check`
- verification_command_or_check: `python scripts/tracka_resume_check.py  # read-only resume check (network:false)`
- verification_command_or_check: `python -m unittest discover tests -q  # baseline regression (no confirmatory outcomes)`
- verification_command_or_check: `python scripts/check_tracka_scope_registry_drift.py  # read-only drift check`
- verification_command_or_check: `python scripts/tracka_resume_check.py  # read-only resume check (network:false)`
- verification_command_or_check: `python scripts/fclr016_v5_admissibility_report.py --bogus --json 2>&1 | head -c 200  # refusal path must be parseable, exit!=0 expected`
- verification_command_or_check: `python scripts/fclr016_v5_promotion_dryrun.py --bogus --json 2>&1 | head -c 200  # refusal path must be parseable, exit!=0 expected`

### cand_2025_01_12_local_exploratory — manifest_terms_evidence.provenance_manifest (Provenance/license manifest artifact)
- current_state=**present_blocker** gate_class=`provenance_manifest_evidence` coverage_ok=`False` missing_action_class=`provenance_manifest_evidence` missing_markers=`['action:identity-verified', 'action:bounded', 'check:fclr015']`
- blocker_or_missing_reason: confirmatory_provenance_go_false_or_missing
- evidence_ref: `research_state/fclr016_local_audit/fclr016_v5_provenance_license_manifest_20261108T014405Z.json` snapshot=`readable`
- verification_command_or_check: `test -f research_state/fclr016_local_audit/fclr016_v5_provenance_license_manifest_20261108T014405Z.json && sha256sum research_state/fclr016_local_audit/fclr016_v5_provenance_license_manifest_20261108T014405Z.json  # read-only existence/hash check`
- verification_command_or_check: `python3 -c "import json; json.load(open('research_state/fclr016_local_audit/fclr016_v5_provenance_license_manifest_20261108T014405Z.json')); print('json_ok')"  # read-only parse check`
- verification_command_or_check: `python -m unittest discover tests -q  # baseline regression (no confirmatory outcomes)`
- verification_command_or_check: `python scripts/check_tracka_scope_registry_drift.py  # read-only drift check`
- verification_command_or_check: `python scripts/tracka_resume_check.py  # read-only resume check (network:false)`
- verification_command_or_check: `test -f research_state/fclr016_local_audit/fclr016_v5_provenance_license_manifest_20261108T014405Z.json && sha256sum research_state/fclr016_local_audit/fclr016_v5_provenance_license_manifest_20261108T014405Z.json  # read-only existence/hash check`
- verification_command_or_check: `python3 -c "import json; json.load(open('research_state/fclr016_local_audit/fclr016_v5_provenance_license_manifest_20261108T014405Z.json')); print('json_ok')"  # read-only parse check`
- verification_command_or_check: `python -m unittest discover tests -q  # baseline regression (no confirmatory outcomes)`
- verification_command_or_check: `python scripts/check_tracka_scope_registry_drift.py  # read-only drift check`
- verification_command_or_check: `python scripts/tracka_resume_check.py  # read-only resume check (network:false)`

### cand_2025_01_12_local_exploratory — manifest_terms_evidence.terms_evidence (Terms/license evidence artifact (human/legal))
- current_state=**present_blocker** gate_class=`terms_legal_evidence_resolution` coverage_ok=`False` missing_action_class=`terms_legal_evidence_resolution` missing_markers=`['action:terms', 'check:fclr016_v5_admissibility_report', 'check:fclr016_v5_promotion_dryrun']`
- blocker_or_missing_reason: terms_status=EXPLICIT_BLOCKER_UNRESOLVED
- evidence_ref: `research_state/fclr016_local_audit/fclr016_v5_terms_evidence_BLOCKED_20261108T014835Z.json` snapshot=`readable`
- verification_command_or_check: `test -f research_state/fclr016_local_audit/fclr016_v5_terms_evidence_BLOCKED_20261108T014835Z.json && sha256sum research_state/fclr016_local_audit/fclr016_v5_terms_evidence_BLOCKED_20261108T014835Z.json  # read-only existence/hash check`
- verification_command_or_check: `python3 -c "import json; json.load(open('research_state/fclr016_local_audit/fclr016_v5_terms_evidence_BLOCKED_20261108T014835Z.json')); print('json_ok')"  # read-only parse check`
- verification_command_or_check: `python -m unittest discover tests -q  # baseline regression (no confirmatory outcomes)`
- verification_command_or_check: `python scripts/check_tracka_scope_registry_drift.py  # read-only drift check`
- verification_command_or_check: `python scripts/tracka_resume_check.py  # read-only resume check (network:false)`
- verification_command_or_check: `test -f research_state/fclr016_local_audit/fclr016_v5_terms_evidence_BLOCKED_20261108T014835Z.json && sha256sum research_state/fclr016_local_audit/fclr016_v5_terms_evidence_BLOCKED_20261108T014835Z.json  # read-only existence/hash check`
- verification_command_or_check: `python3 -c "import json; json.load(open('research_state/fclr016_local_audit/fclr016_v5_terms_evidence_BLOCKED_20261108T014835Z.json')); print('json_ok')"  # read-only parse check`
- verification_command_or_check: `python -m unittest discover tests -q  # baseline regression (no confirmatory outcomes)`
- verification_command_or_check: `python scripts/check_tracka_scope_registry_drift.py  # read-only drift check`
- verification_command_or_check: `python scripts/tracka_resume_check.py  # read-only resume check (network:false)`

### cand_2025_01_12_local_exploratory — admissibility_package_status (Admissibility package status)
- current_state=**present_blocker** gate_class=`admissibility_completeness_leakage_evidence` coverage_ok=`True` missing_action_class=`None` missing_markers=`[]`
- blocker_or_missing_reason: completeness=present_blocker, prereg_draft=None, v5_window=present_blocker
- verification_command_or_check: `python -m unittest discover tests -q  # baseline regression (no confirmatory outcomes)`
- verification_command_or_check: `python scripts/check_tracka_scope_registry_drift.py  # read-only drift check`
- verification_command_or_check: `python scripts/tracka_resume_check.py  # read-only resume check (network:false)`
- verification_command_or_check: `python -m unittest discover tests -q  # baseline regression (no confirmatory outcomes)`
- verification_command_or_check: `python scripts/check_tracka_scope_registry_drift.py  # read-only drift check`
- verification_command_or_check: `python scripts/tracka_resume_check.py  # read-only resume check (network:false)`

### cand_2025_01_12_local_exploratory — admissibility_package_status.completeness_leakage_audit (Completeness/leakage audit artifact)
- current_state=**present_blocker** gate_class=`admissibility_completeness_leakage_evidence` coverage_ok=`False` missing_action_class=`admissibility_completeness_leakage_evidence` missing_markers=`['action:admissibility']`
- blocker_or_missing_reason: blockers_remaining_count=2
- evidence_ref: `research_state/fclr016_local_audit/fclr016_v5_completeness_leakage_audit_20261108T014405Z.json` snapshot=`readable`
- verification_command_or_check: `test -f research_state/fclr016_local_audit/fclr016_v5_completeness_leakage_audit_20261108T014405Z.json && sha256sum research_state/fclr016_local_audit/fclr016_v5_completeness_leakage_audit_20261108T014405Z.json  # read-only existence/hash check`
- verification_command_or_check: `python3 -c "import json; json.load(open('research_state/fclr016_local_audit/fclr016_v5_completeness_leakage_audit_20261108T014405Z.json')); print('json_ok')"  # read-only parse check`
- verification_command_or_check: `python -m unittest discover tests -q  # baseline regression (no confirmatory outcomes)`
- verification_command_or_check: `python scripts/check_tracka_scope_registry_drift.py  # read-only drift check`
- verification_command_or_check: `python scripts/tracka_resume_check.py  # read-only resume check (network:false)`
- verification_command_or_check: `test -f research_state/fclr016_local_audit/fclr016_v5_completeness_leakage_audit_20261108T014405Z.json && sha256sum research_state/fclr016_local_audit/fclr016_v5_completeness_leakage_audit_20261108T014405Z.json  # read-only existence/hash check`
- verification_command_or_check: `python3 -c "import json; json.load(open('research_state/fclr016_local_audit/fclr016_v5_completeness_leakage_audit_20261108T014405Z.json')); print('json_ok')"  # read-only parse check`
- verification_command_or_check: `python -m unittest discover tests -q  # baseline regression (no confirmatory outcomes)`
- verification_command_or_check: `python scripts/check_tracka_scope_registry_drift.py  # read-only drift check`
- verification_command_or_check: `python scripts/tracka_resume_check.py  # read-only resume check (network:false)`

### cand_2025_01_12_local_exploratory — admissibility_package_status.confirmatory_prereg_draft_ref (Confirmatory prereg draft/ref artifact (not fresh frozen prereg))
- current_state=**present_blocker** gate_class=`fresh_frozen_prereg_before_outcomes` coverage_ok=`False` missing_action_class=`fresh_frozen_prereg_before_outcomes` missing_markers=`['action:fresh frozen preregistration', 'action:before any confirmatory outcomes', 'check:run_funding_ablations']`
- blocker_or_missing_reason: prereg_draft_or_not_frozen_before_outcomes
- evidence_ref: `research_state/fclr016_local_audit/fclr016_v5_confirmatory_prereg_DRAFT_20261108T014835Z.json` snapshot=`readable`
- verification_command_or_check: `test -f research_state/fclr016_local_audit/fclr016_v5_confirmatory_prereg_DRAFT_20261108T014835Z.json && sha256sum research_state/fclr016_local_audit/fclr016_v5_confirmatory_prereg_DRAFT_20261108T014835Z.json  # read-only existence/hash check`
- verification_command_or_check: `python3 -c "import json; json.load(open('research_state/fclr016_local_audit/fclr016_v5_confirmatory_prereg_DRAFT_20261108T014835Z.json')); print('json_ok')"  # read-only parse check`
- verification_command_or_check: `python -m unittest discover tests -q  # baseline regression (no confirmatory outcomes)`
- verification_command_or_check: `python scripts/check_tracka_scope_registry_drift.py  # read-only drift check`
- verification_command_or_check: `python scripts/tracka_resume_check.py  # read-only resume check (network:false)`
- verification_command_or_check: `test -f research_state/fclr016_local_audit/fclr016_v5_confirmatory_prereg_DRAFT_20261108T014835Z.json && sha256sum research_state/fclr016_local_audit/fclr016_v5_confirmatory_prereg_DRAFT_20261108T014835Z.json  # read-only existence/hash check`
- verification_command_or_check: `python3 -c "import json; json.load(open('research_state/fclr016_local_audit/fclr016_v5_confirmatory_prereg_DRAFT_20261108T014835Z.json')); print('json_ok')"  # read-only parse check`
- verification_command_or_check: `python -m unittest discover tests -q  # baseline regression (no confirmatory outcomes)`
- verification_command_or_check: `python scripts/check_tracka_scope_registry_drift.py  # read-only drift check`
- verification_command_or_check: `python scripts/tracka_resume_check.py  # read-only resume check (network:false)`

### cand_2025_01_12_local_exploratory — admissibility_package_status.v5_window_terms_state_from_fclr018 (v5 window terms/admissibility state (from FCLR-018))
- current_state=**present_blocker** gate_class=`terms_legal_evidence_resolution` coverage_ok=`False` missing_action_class=`terms_legal_evidence_resolution` missing_markers=`['action:terms', 'action:human/legal', 'action:fabricated=false', 'action:verifiable evidence', 'check:fclr016_v5_admissibility_report', 'check:fclr016_v5_promotion_dryrun']`
- blocker_or_missing_reason: terms_status=EXPLICIT_BLOCKER_UNRESOLVED all_go=False confirmatory_outcomes_permitted=False
- evidence_ref: `fclr018.window.v5_terms_blocker_state` snapshot=`missing`
- verification_command_or_check: `test -f fclr018.window.v5_terms_blocker_state && sha256sum fclr018.window.v5_terms_blocker_state  # read-only existence/hash check`
- verification_command_or_check: `python -m unittest discover tests -q  # baseline regression (no confirmatory outcomes)`
- verification_command_or_check: `python scripts/check_tracka_scope_registry_drift.py  # read-only drift check`
- verification_command_or_check: `python scripts/tracka_resume_check.py  # read-only resume check (network:false)`
- verification_command_or_check: `python -m unittest discover tests -q  # baseline regression (no confirmatory outcomes)`
- verification_command_or_check: `python scripts/check_tracka_scope_registry_drift.py  # read-only drift check`
- verification_command_or_check: `python scripts/tracka_resume_check.py  # read-only resume check (network:false)`

### cand_2025_01_12_local_exploratory — fresh_frozen_prereg_before_outcomes_required (Fresh frozen prereg before outcomes (required))
- current_state=**missing** gate_class=`fresh_frozen_prereg_before_outcomes` coverage_ok=`False` missing_action_class=`fresh_frozen_prereg_before_outcomes` missing_markers=`['action:fresh frozen preregistration', 'check:run_funding_ablations']`
- blocker_or_missing_reason: fresh frozen prereg before outcomes required = missing/not frozen (no concrete local frozen prereg artifact confirmed by this index)
- verification_command_or_check: `python -m unittest discover tests -q  # baseline regression (no confirmatory outcomes)`
- verification_command_or_check: `python scripts/check_tracka_scope_registry_drift.py  # read-only drift check`
- verification_command_or_check: `python scripts/tracka_resume_check.py  # read-only resume check (network:false)`
- verification_command_or_check: `python -m unittest discover tests -q  # baseline regression (no confirmatory outcomes)`
- verification_command_or_check: `python scripts/check_tracka_scope_registry_drift.py  # read-only drift check`
- verification_command_or_check: `python scripts/tracka_resume_check.py  # read-only resume check (network:false)`
- verification_command_or_check: `test ! -f research_state/NO_SUCH_FRESH_FROZEN_PREREG  # placeholder reminder: a concrete frozen prereg artifact path must be supplied and verified before outcomes`

### cand_2025_01_12_local_exploratory — leakage_sufficiency_gates (Leakage controls and data sufficiency gates)
- current_state=**present_blocker** gate_class=`leakage_sufficiency_gates` coverage_ok=`False` missing_action_class=`leakage_sufficiency_gates` missing_markers=`['action:sufficiency']`
- blocker_or_missing_reason: calendar_coverage_incomplete_or_unverified
- evidence_ref: `fclr018.window.coverage/block_fields` snapshot=`missing`
- verification_command_or_check: `test -f fclr018.window.coverage/block_fields && sha256sum fclr018.window.coverage/block_fields  # read-only existence/hash check`
- verification_command_or_check: `python -m unittest discover tests -q  # baseline regression (no confirmatory outcomes)`
- verification_command_or_check: `python scripts/check_tracka_scope_registry_drift.py  # read-only drift check`
- verification_command_or_check: `python scripts/tracka_resume_check.py  # read-only resume check (network:false)`
- verification_command_or_check: `python -m unittest discover tests -q  # baseline regression (no confirmatory outcomes)`
- verification_command_or_check: `python scripts/check_tracka_scope_registry_drift.py  # read-only drift check`
- verification_command_or_check: `python scripts/tracka_resume_check.py  # read-only resume check (network:false)`
- verification_command_or_check: `python scripts/run_funding_ablations.py  # baseline pilot must run clean with honest verdict (no confirmatory claim from this command alone)`

### cand_2024_01_12_local_exploratory — identity_provenance_range (Identity/provenance range evidence (bounded))
- current_state=**present_blocker** gate_class=`provenance_manifest_evidence` coverage_ok=`False` missing_action_class=`provenance_manifest_evidence` missing_markers=`['action:manifest', 'check:sha256sum', 'check:test -f', 'check:json_ok']`
- blocker_or_missing_reason: provenance_status=UNVERIFIED; reasons=['v5_terms_blocker_unresolved_all_go_false', 'provenance_not_identity_verified_bounded_fclr015', 'calendar_coverage_incomplete_or_unverified']
- evidence_ref: `fclr018.window.provenance_status` snapshot=`missing`
- verification_command_or_check: `test -f fclr018.window.provenance_status && sha256sum fclr018.window.provenance_status  # read-only existence/hash check`
- verification_command_or_check: `python -m unittest discover tests -q  # baseline regression (no confirmatory outcomes)`
- verification_command_or_check: `python scripts/check_tracka_scope_registry_drift.py  # read-only drift check`
- verification_command_or_check: `python scripts/tracka_resume_check.py  # read-only resume check (network:false)`
- verification_command_or_check: `python -m unittest discover tests -q  # baseline regression (no confirmatory outcomes)`
- verification_command_or_check: `python scripts/check_tracka_scope_registry_drift.py  # read-only drift check`
- verification_command_or_check: `python scripts/tracka_resume_check.py  # read-only resume check (network:false)`
- verification_command_or_check: `python scripts/fclr015_gate4_cache_input_manifest.py --help >/dev/null 2>&1 || true  # read-only capability check (no confirmatory outcomes)`

### cand_2024_01_12_local_exploratory — manifest_terms_evidence (Manifest/terms evidence package)
- current_state=**present_blocker** gate_class=`terms_legal_evidence_resolution` coverage_ok=`False` missing_action_class=`terms_legal_evidence_resolution` missing_markers=`['action:verifiable evidence']`
- blocker_or_missing_reason: provenance_manifest=present_blocker, terms_evidence=present_blocker
- verification_command_or_check: `python -m unittest discover tests -q  # baseline regression (no confirmatory outcomes)`
- verification_command_or_check: `python scripts/check_tracka_scope_registry_drift.py  # read-only drift check`
- verification_command_or_check: `python scripts/tracka_resume_check.py  # read-only resume check (network:false)`
- verification_command_or_check: `python -m unittest discover tests -q  # baseline regression (no confirmatory outcomes)`
- verification_command_or_check: `python scripts/check_tracka_scope_registry_drift.py  # read-only drift check`
- verification_command_or_check: `python scripts/tracka_resume_check.py  # read-only resume check (network:false)`
- verification_command_or_check: `python scripts/fclr016_v5_admissibility_report.py --bogus --json 2>&1 | head -c 200  # refusal path must be parseable, exit!=0 expected`
- verification_command_or_check: `python scripts/fclr016_v5_promotion_dryrun.py --bogus --json 2>&1 | head -c 200  # refusal path must be parseable, exit!=0 expected`

### cand_2024_01_12_local_exploratory — manifest_terms_evidence.provenance_manifest (Provenance/license manifest artifact)
- current_state=**present_blocker** gate_class=`provenance_manifest_evidence` coverage_ok=`False` missing_action_class=`provenance_manifest_evidence` missing_markers=`['action:identity-verified', 'action:bounded', 'check:fclr015']`
- blocker_or_missing_reason: confirmatory_provenance_go_false_or_missing
- evidence_ref: `research_state/fclr016_local_audit/fclr016_v5_provenance_license_manifest_20261108T014405Z.json` snapshot=`readable`
- verification_command_or_check: `test -f research_state/fclr016_local_audit/fclr016_v5_provenance_license_manifest_20261108T014405Z.json && sha256sum research_state/fclr016_local_audit/fclr016_v5_provenance_license_manifest_20261108T014405Z.json  # read-only existence/hash check`
- verification_command_or_check: `python3 -c "import json; json.load(open('research_state/fclr016_local_audit/fclr016_v5_provenance_license_manifest_20261108T014405Z.json')); print('json_ok')"  # read-only parse check`
- verification_command_or_check: `python -m unittest discover tests -q  # baseline regression (no confirmatory outcomes)`
- verification_command_or_check: `python scripts/check_tracka_scope_registry_drift.py  # read-only drift check`
- verification_command_or_check: `python scripts/tracka_resume_check.py  # read-only resume check (network:false)`
- verification_command_or_check: `test -f research_state/fclr016_local_audit/fclr016_v5_provenance_license_manifest_20261108T014405Z.json && sha256sum research_state/fclr016_local_audit/fclr016_v5_provenance_license_manifest_20261108T014405Z.json  # read-only existence/hash check`
- verification_command_or_check: `python3 -c "import json; json.load(open('research_state/fclr016_local_audit/fclr016_v5_provenance_license_manifest_20261108T014405Z.json')); print('json_ok')"  # read-only parse check`
- verification_command_or_check: `python -m unittest discover tests -q  # baseline regression (no confirmatory outcomes)`
- verification_command_or_check: `python scripts/check_tracka_scope_registry_drift.py  # read-only drift check`
- verification_command_or_check: `python scripts/tracka_resume_check.py  # read-only resume check (network:false)`

### cand_2024_01_12_local_exploratory — manifest_terms_evidence.terms_evidence (Terms/license evidence artifact (human/legal))
- current_state=**present_blocker** gate_class=`terms_legal_evidence_resolution` coverage_ok=`False` missing_action_class=`terms_legal_evidence_resolution` missing_markers=`['action:terms', 'check:fclr016_v5_admissibility_report', 'check:fclr016_v5_promotion_dryrun']`
- blocker_or_missing_reason: terms_status=EXPLICIT_BLOCKER_UNRESOLVED
- evidence_ref: `research_state/fclr016_local_audit/fclr016_v5_terms_evidence_BLOCKED_20261108T014835Z.json` snapshot=`readable`
- verification_command_or_check: `test -f research_state/fclr016_local_audit/fclr016_v5_terms_evidence_BLOCKED_20261108T014835Z.json && sha256sum research_state/fclr016_local_audit/fclr016_v5_terms_evidence_BLOCKED_20261108T014835Z.json  # read-only existence/hash check`
- verification_command_or_check: `python3 -c "import json; json.load(open('research_state/fclr016_local_audit/fclr016_v5_terms_evidence_BLOCKED_20261108T014835Z.json')); print('json_ok')"  # read-only parse check`
- verification_command_or_check: `python -m unittest discover tests -q  # baseline regression (no confirmatory outcomes)`
- verification_command_or_check: `python scripts/check_tracka_scope_registry_drift.py  # read-only drift check`
- verification_command_or_check: `python scripts/tracka_resume_check.py  # read-only resume check (network:false)`
- verification_command_or_check: `test -f research_state/fclr016_local_audit/fclr016_v5_terms_evidence_BLOCKED_20261108T014835Z.json && sha256sum research_state/fclr016_local_audit/fclr016_v5_terms_evidence_BLOCKED_20261108T014835Z.json  # read-only existence/hash check`
- verification_command_or_check: `python3 -c "import json; json.load(open('research_state/fclr016_local_audit/fclr016_v5_terms_evidence_BLOCKED_20261108T014835Z.json')); print('json_ok')"  # read-only parse check`
- verification_command_or_check: `python -m unittest discover tests -q  # baseline regression (no confirmatory outcomes)`
- verification_command_or_check: `python scripts/check_tracka_scope_registry_drift.py  # read-only drift check`
- verification_command_or_check: `python scripts/tracka_resume_check.py  # read-only resume check (network:false)`

### cand_2024_01_12_local_exploratory — admissibility_package_status (Admissibility package status)
- current_state=**present_blocker** gate_class=`admissibility_completeness_leakage_evidence` coverage_ok=`True` missing_action_class=`None` missing_markers=`[]`
- blocker_or_missing_reason: completeness=present_blocker, prereg_draft=None, v5_window=present_blocker
- verification_command_or_check: `python -m unittest discover tests -q  # baseline regression (no confirmatory outcomes)`
- verification_command_or_check: `python scripts/check_tracka_scope_registry_drift.py  # read-only drift check`
- verification_command_or_check: `python scripts/tracka_resume_check.py  # read-only resume check (network:false)`
- verification_command_or_check: `python -m unittest discover tests -q  # baseline regression (no confirmatory outcomes)`
- verification_command_or_check: `python scripts/check_tracka_scope_registry_drift.py  # read-only drift check`
- verification_command_or_check: `python scripts/tracka_resume_check.py  # read-only resume check (network:false)`

### cand_2024_01_12_local_exploratory — admissibility_package_status.completeness_leakage_audit (Completeness/leakage audit artifact)
- current_state=**present_blocker** gate_class=`admissibility_completeness_leakage_evidence` coverage_ok=`False` missing_action_class=`admissibility_completeness_leakage_evidence` missing_markers=`['action:admissibility']`
- blocker_or_missing_reason: blockers_remaining_count=2
- evidence_ref: `research_state/fclr016_local_audit/fclr016_v5_completeness_leakage_audit_20261108T014405Z.json` snapshot=`readable`
- verification_command_or_check: `test -f research_state/fclr016_local_audit/fclr016_v5_completeness_leakage_audit_20261108T014405Z.json && sha256sum research_state/fclr016_local_audit/fclr016_v5_completeness_leakage_audit_20261108T014405Z.json  # read-only existence/hash check`
- verification_command_or_check: `python3 -c "import json; json.load(open('research_state/fclr016_local_audit/fclr016_v5_completeness_leakage_audit_20261108T014405Z.json')); print('json_ok')"  # read-only parse check`
- verification_command_or_check: `python -m unittest discover tests -q  # baseline regression (no confirmatory outcomes)`
- verification_command_or_check: `python scripts/check_tracka_scope_registry_drift.py  # read-only drift check`
- verification_command_or_check: `python scripts/tracka_resume_check.py  # read-only resume check (network:false)`
- verification_command_or_check: `test -f research_state/fclr016_local_audit/fclr016_v5_completeness_leakage_audit_20261108T014405Z.json && sha256sum research_state/fclr016_local_audit/fclr016_v5_completeness_leakage_audit_20261108T014405Z.json  # read-only existence/hash check`
- verification_command_or_check: `python3 -c "import json; json.load(open('research_state/fclr016_local_audit/fclr016_v5_completeness_leakage_audit_20261108T014405Z.json')); print('json_ok')"  # read-only parse check`
- verification_command_or_check: `python -m unittest discover tests -q  # baseline regression (no confirmatory outcomes)`
- verification_command_or_check: `python scripts/check_tracka_scope_registry_drift.py  # read-only drift check`
- verification_command_or_check: `python scripts/tracka_resume_check.py  # read-only resume check (network:false)`

### cand_2024_01_12_local_exploratory — admissibility_package_status.confirmatory_prereg_draft_ref (Confirmatory prereg draft/ref artifact (not fresh frozen prereg))
- current_state=**present_blocker** gate_class=`fresh_frozen_prereg_before_outcomes` coverage_ok=`False` missing_action_class=`fresh_frozen_prereg_before_outcomes` missing_markers=`['action:fresh frozen preregistration', 'action:before any confirmatory outcomes', 'check:run_funding_ablations']`
- blocker_or_missing_reason: prereg_draft_or_not_frozen_before_outcomes
- evidence_ref: `research_state/fclr016_local_audit/fclr016_v5_confirmatory_prereg_DRAFT_20261108T014835Z.json` snapshot=`readable`
- verification_command_or_check: `test -f research_state/fclr016_local_audit/fclr016_v5_confirmatory_prereg_DRAFT_20261108T014835Z.json && sha256sum research_state/fclr016_local_audit/fclr016_v5_confirmatory_prereg_DRAFT_20261108T014835Z.json  # read-only existence/hash check`
- verification_command_or_check: `python3 -c "import json; json.load(open('research_state/fclr016_local_audit/fclr016_v5_confirmatory_prereg_DRAFT_20261108T014835Z.json')); print('json_ok')"  # read-only parse check`
- verification_command_or_check: `python -m unittest discover tests -q  # baseline regression (no confirmatory outcomes)`
- verification_command_or_check: `python scripts/check_tracka_scope_registry_drift.py  # read-only drift check`
- verification_command_or_check: `python scripts/tracka_resume_check.py  # read-only resume check (network:false)`
- verification_command_or_check: `test -f research_state/fclr016_local_audit/fclr016_v5_confirmatory_prereg_DRAFT_20261108T014835Z.json && sha256sum research_state/fclr016_local_audit/fclr016_v5_confirmatory_prereg_DRAFT_20261108T014835Z.json  # read-only existence/hash check`
- verification_command_or_check: `python3 -c "import json; json.load(open('research_state/fclr016_local_audit/fclr016_v5_confirmatory_prereg_DRAFT_20261108T014835Z.json')); print('json_ok')"  # read-only parse check`
- verification_command_or_check: `python -m unittest discover tests -q  # baseline regression (no confirmatory outcomes)`
- verification_command_or_check: `python scripts/check_tracka_scope_registry_drift.py  # read-only drift check`
- verification_command_or_check: `python scripts/tracka_resume_check.py  # read-only resume check (network:false)`

### cand_2024_01_12_local_exploratory — admissibility_package_status.v5_window_terms_state_from_fclr018 (v5 window terms/admissibility state (from FCLR-018))
- current_state=**present_blocker** gate_class=`terms_legal_evidence_resolution` coverage_ok=`False` missing_action_class=`terms_legal_evidence_resolution` missing_markers=`['action:terms', 'action:human/legal', 'action:fabricated=false', 'action:verifiable evidence', 'check:fclr016_v5_admissibility_report', 'check:fclr016_v5_promotion_dryrun']`
- blocker_or_missing_reason: terms_status=EXPLICIT_BLOCKER_UNRESOLVED all_go=False confirmatory_outcomes_permitted=False
- evidence_ref: `fclr018.window.v5_terms_blocker_state` snapshot=`missing`
- verification_command_or_check: `test -f fclr018.window.v5_terms_blocker_state && sha256sum fclr018.window.v5_terms_blocker_state  # read-only existence/hash check`
- verification_command_or_check: `python -m unittest discover tests -q  # baseline regression (no confirmatory outcomes)`
- verification_command_or_check: `python scripts/check_tracka_scope_registry_drift.py  # read-only drift check`
- verification_command_or_check: `python scripts/tracka_resume_check.py  # read-only resume check (network:false)`
- verification_command_or_check: `python -m unittest discover tests -q  # baseline regression (no confirmatory outcomes)`
- verification_command_or_check: `python scripts/check_tracka_scope_registry_drift.py  # read-only drift check`
- verification_command_or_check: `python scripts/tracka_resume_check.py  # read-only resume check (network:false)`

### cand_2024_01_12_local_exploratory — fresh_frozen_prereg_before_outcomes_required (Fresh frozen prereg before outcomes (required))
- current_state=**missing** gate_class=`fresh_frozen_prereg_before_outcomes` coverage_ok=`False` missing_action_class=`fresh_frozen_prereg_before_outcomes` missing_markers=`['action:fresh frozen preregistration', 'check:run_funding_ablations']`
- blocker_or_missing_reason: fresh frozen prereg before outcomes required = missing/not frozen (no concrete local frozen prereg artifact confirmed by this index)
- verification_command_or_check: `python -m unittest discover tests -q  # baseline regression (no confirmatory outcomes)`
- verification_command_or_check: `python scripts/check_tracka_scope_registry_drift.py  # read-only drift check`
- verification_command_or_check: `python scripts/tracka_resume_check.py  # read-only resume check (network:false)`
- verification_command_or_check: `python -m unittest discover tests -q  # baseline regression (no confirmatory outcomes)`
- verification_command_or_check: `python scripts/check_tracka_scope_registry_drift.py  # read-only drift check`
- verification_command_or_check: `python scripts/tracka_resume_check.py  # read-only resume check (network:false)`
- verification_command_or_check: `test ! -f research_state/NO_SUCH_FRESH_FROZEN_PREREG  # placeholder reminder: a concrete frozen prereg artifact path must be supplied and verified before outcomes`

### cand_2024_01_12_local_exploratory — leakage_sufficiency_gates (Leakage controls and data sufficiency gates)
- current_state=**present_blocker** gate_class=`leakage_sufficiency_gates` coverage_ok=`False` missing_action_class=`leakage_sufficiency_gates` missing_markers=`['action:sufficiency']`
- blocker_or_missing_reason: calendar_coverage_incomplete_or_unverified
- evidence_ref: `fclr018.window.coverage/block_fields` snapshot=`missing`
- verification_command_or_check: `test -f fclr018.window.coverage/block_fields && sha256sum fclr018.window.coverage/block_fields  # read-only existence/hash check`
- verification_command_or_check: `python -m unittest discover tests -q  # baseline regression (no confirmatory outcomes)`
- verification_command_or_check: `python scripts/check_tracka_scope_registry_drift.py  # read-only drift check`
- verification_command_or_check: `python scripts/tracka_resume_check.py  # read-only resume check (network:false)`
- verification_command_or_check: `python -m unittest discover tests -q  # baseline regression (no confirmatory outcomes)`
- verification_command_or_check: `python scripts/check_tracka_scope_registry_drift.py  # read-only drift check`
- verification_command_or_check: `python scripts/tracka_resume_check.py  # read-only resume check (network:false)`
- verification_command_or_check: `python scripts/run_funding_ablations.py  # baseline pilot must run clean with honest verdict (no confirmatory claim from this command alone)`

Planning/draft coverage validation only — not GO for confirmatory outcomes, not frozen/promoted, no prerequisite marked satisfied, no overlay/H001/Track A status change.
