# FCLR-020 Gate 4 readiness/action matrix (20261108T142025Z)

- method: deterministic read-only action mapping from FCLR-019; no network; no model-outcome computation
- draft_only: **True** | no_confirmatory_outcomes: **True** | exploratory_only: **True** | no_network: **True**
- not_go_for_confirmatory_outcomes: **True** | confirmatory_ready_now: **False** | confirmatory_outcomes_go: **False**

## Caveats
- draft_only_not_frozen_not_promoted: `True`
- no_confirmatory_outcomes_computed: `True`
- no_prerequisite_marked_satisfied: `True`
- no_satisfaction_inferred_from_absent_blocker: `True`
- lfs_pointer_treated_as_unavailable: `True`
- states_used: `['present_unverified', 'present_blocker', 'missing']`

## Global actions
- authorizes_confirmatory_outcomes=`False`
  - action: Keep v5 terms/admissibility fail-closed until verifiable human/legal evidence resolves blockers and package is GO.
  - action: Track A/H004 remains blocked; do not re-probe absent Hyperliquid months in a loop.
  - action: No .github/workflows edits; no sealed holdout/anchor overwrites; no competing handoff files.
  - verify: `python scripts/fclr016_v5_admissibility_report.py --bogus --json 2>&1 | head -c 200`
  - verify: `python scripts/tracka_resume_check.py | python3 -c "import sys,json; d=json.load(sys.stdin); print(d['pass'], d['network'])"`

## Per-window action matrices
### cand_2024_04_09_evidenced (2024-04-01..2024-09-30)
- fclr019_index_summary_state=**present_blocker** confirmatory_outcomes_go=**False**
#### identity_provenance_range — Identity/provenance range evidence (bounded)
- current_state=**present_unverified** read_state=`from_fclr018` authorizes_confirmatory_outcomes=`False` satisfied=`False` satisfaction_inferred=`False`
- blocker_or_missing_reason: IDENTITY_VERIFIED_BOUNDED_FCLR015 for window per fclr018; confirmatory still bounded by ranges/manifest/terms/fresh-frozen-prereg
- evidence_ref: `fclr018.window.provenance_status` snapshot=`missing`
- action_required: Human review required: verify cited provenance artifact is authentic, bounded, and sufficient for the intended confirmatory range.
- action_required: Confirm 2024-04..09 confirmatory use remains bounded by PROVENANCED_CONFIRMATORY_RANGES + manifest/terms/admissibility guards.
- action_required: Present-unverified is not satisfied; do not compute confirmatory outcomes on this basis alone.
- verification_command_or_check: `python -m unittest discover tests -q  # baseline regression (no confirmatory outcomes)`
- verification_command_or_check: `python scripts/check_tracka_scope_registry_drift.py  # read-only drift check`
- verification_command_or_check: `python scripts/tracka_resume_check.py  # read-only resume check (network:false)`
- verification_command_or_check: `python scripts/fclr015_gate4_cache_input_manifest.py --help >/dev/null 2>&1 || true  # read-only capability check (no confirmatory outcomes)`

#### manifest_terms_evidence — Manifest/terms evidence package
- current_state=**present_blocker** read_state=`from_fclr019_summary` authorizes_confirmatory_outcomes=`False` satisfied=`False` satisfaction_inferred=`False`
- blocker_or_missing_reason: provenance_manifest=present_blocker, terms_evidence=present_blocker
- action_required: Resolve manifest and terms evidence blockers before any confirmatory use (human/legal review required for terms).
- action_required: For v5 terms: produce verifiable RESOLVED_VERIFIED evidence only with fabricated=false and frozen scope; reconcile refs/hashes.
- action_required: Never fabricate terms/license/reviews or mark terms resolved without verifiable facts.
- verification_command_or_check: `python -m unittest discover tests -q  # baseline regression (no confirmatory outcomes)`
- verification_command_or_check: `python scripts/check_tracka_scope_registry_drift.py  # read-only drift check`
- verification_command_or_check: `python scripts/tracka_resume_check.py  # read-only resume check (network:false)`
- verification_command_or_check: `python scripts/fclr016_v5_admissibility_report.py --bogus --json 2>&1 | head -c 200  # refusal path must be parseable, exit!=0 expected`
- verification_command_or_check: `python scripts/fclr016_v5_promotion_dryrun.py --bogus --json 2>&1 | head -c 200  # refusal path must be parseable, exit!=0 expected`

#### manifest_terms_evidence.provenance_manifest — Provenance/license manifest artifact
- current_state=**present_blocker** read_state=`ok` authorizes_confirmatory_outcomes=`False` satisfied=`False` satisfaction_inferred=`False`
- blocker_or_missing_reason: confirmatory_provenance_go_false_or_missing
- evidence_ref: `research_state/fclr016_local_audit/fclr016_v5_provenance_license_manifest_20261108T014405Z.json` snapshot=`readable`
- action_required: Ensure provenance manifest exists, is readable, and states confirmatory_provenance_go/admissibility_complete/license_terms status with verifiable facts.
- action_required: Reconcile manifest refs/hashes after any legitimate evidence update; do not overwrite sealed artifacts.
- action_required: No confirmatory outcomes/freeze/promotion while this prerequisite is not concretely satisfied by verifiable evidence.
- verification_command_or_check: `test -f research_state/fclr016_local_audit/fclr016_v5_provenance_license_manifest_20261108T014405Z.json && sha256sum research_state/fclr016_local_audit/fclr016_v5_provenance_license_manifest_20261108T014405Z.json  # read-only existence/hash check`
- verification_command_or_check: `python3 -c "import json; json.load(open('research_state/fclr016_local_audit/fclr016_v5_provenance_license_manifest_20261108T014405Z.json')); print('json_ok')"  # read-only parse check`
- verification_command_or_check: `python -m unittest discover tests -q  # baseline regression (no confirmatory outcomes)`
- verification_command_or_check: `python scripts/check_tracka_scope_registry_drift.py  # read-only drift check`
- verification_command_or_check: `python scripts/tracka_resume_check.py  # read-only resume check (network:false)`

#### manifest_terms_evidence.terms_evidence — Terms/license evidence artifact (human/legal)
- current_state=**present_blocker** read_state=`ok` authorizes_confirmatory_outcomes=`False` satisfied=`False` satisfaction_inferred=`False`
- blocker_or_missing_reason: terms_status=EXPLICIT_BLOCKER_UNRESOLVED
- evidence_ref: `research_state/fclr016_local_audit/fclr016_v5_terms_evidence_BLOCKED_20261108T014835Z.json` snapshot=`readable`
- action_required: Human/legal action required: resolve EXPLICIT_BLOCKER_UNRESOLVED with verifiable evidence (fabricated=false).
- action_required: Do not create RESOLVED_VERIFIED without frozen scope and reconciled refs/hashes; do not edit .github/workflows.
- action_required: No confirmatory outcomes/freeze/promotion while this prerequisite is not concretely satisfied by verifiable evidence.
- verification_command_or_check: `test -f research_state/fclr016_local_audit/fclr016_v5_terms_evidence_BLOCKED_20261108T014835Z.json && sha256sum research_state/fclr016_local_audit/fclr016_v5_terms_evidence_BLOCKED_20261108T014835Z.json  # read-only existence/hash check`
- verification_command_or_check: `python3 -c "import json; json.load(open('research_state/fclr016_local_audit/fclr016_v5_terms_evidence_BLOCKED_20261108T014835Z.json')); print('json_ok')"  # read-only parse check`
- verification_command_or_check: `python -m unittest discover tests -q  # baseline regression (no confirmatory outcomes)`
- verification_command_or_check: `python scripts/check_tracka_scope_registry_drift.py  # read-only drift check`
- verification_command_or_check: `python scripts/tracka_resume_check.py  # read-only resume check (network:false)`

#### admissibility_package_status — Admissibility package status
- current_state=**present_blocker** read_state=`from_fclr019_summary` authorizes_confirmatory_outcomes=`False` satisfied=`False` satisfaction_inferred=`False`
- blocker_or_missing_reason: completeness=present_blocker, prereg_draft=None, v5_window=present_blocker
- action_required: Resolve completeness/leakage/admissibility blockers with verifiable local artifacts; keep v5 all_go=false handling fail-closed until resolved.
- action_required: Any confirmatory outcomes require real package all_go=true and fresh frozen prereg before outcomes.
- verification_command_or_check: `python -m unittest discover tests -q  # baseline regression (no confirmatory outcomes)`
- verification_command_or_check: `python scripts/check_tracka_scope_registry_drift.py  # read-only drift check`
- verification_command_or_check: `python scripts/tracka_resume_check.py  # read-only resume check (network:false)`

#### admissibility_package_status.completeness_leakage_audit — Completeness/leakage audit artifact
- current_state=**present_blocker** read_state=`ok` authorizes_confirmatory_outcomes=`False` satisfied=`False` satisfaction_inferred=`False`
- blocker_or_missing_reason: blockers_remaining_count=2
- evidence_ref: `research_state/fclr016_local_audit/fclr016_v5_completeness_leakage_audit_20261108T014405Z.json` snapshot=`readable`
- action_required: Address listed completeness/leakage blockers with verifiable evidence before confirmatory use.
- verification_command_or_check: `test -f research_state/fclr016_local_audit/fclr016_v5_completeness_leakage_audit_20261108T014405Z.json && sha256sum research_state/fclr016_local_audit/fclr016_v5_completeness_leakage_audit_20261108T014405Z.json  # read-only existence/hash check`
- verification_command_or_check: `python3 -c "import json; json.load(open('research_state/fclr016_local_audit/fclr016_v5_completeness_leakage_audit_20261108T014405Z.json')); print('json_ok')"  # read-only parse check`
- verification_command_or_check: `python -m unittest discover tests -q  # baseline regression (no confirmatory outcomes)`
- verification_command_or_check: `python scripts/check_tracka_scope_registry_drift.py  # read-only drift check`
- verification_command_or_check: `python scripts/tracka_resume_check.py  # read-only resume check (network:false)`

#### admissibility_package_status.confirmatory_prereg_draft_ref — Confirmatory prereg draft/ref artifact (not fresh frozen prereg)
- current_state=**present_blocker** read_state=`ok` authorizes_confirmatory_outcomes=`False` satisfied=`False` satisfaction_inferred=`False`
- blocker_or_missing_reason: prereg_draft_or_not_frozen_before_outcomes
- evidence_ref: `research_state/fclr016_local_audit/fclr016_v5_confirmatory_prereg_DRAFT_20261108T014835Z.json` snapshot=`readable`
- action_required: A DRAFT prereg skeleton/ref is not sufficient for confirmatory outcomes; fresh frozen prereg before outcomes is required.
- verification_command_or_check: `test -f research_state/fclr016_local_audit/fclr016_v5_confirmatory_prereg_DRAFT_20261108T014835Z.json && sha256sum research_state/fclr016_local_audit/fclr016_v5_confirmatory_prereg_DRAFT_20261108T014835Z.json  # read-only existence/hash check`
- verification_command_or_check: `python3 -c "import json; json.load(open('research_state/fclr016_local_audit/fclr016_v5_confirmatory_prereg_DRAFT_20261108T014835Z.json')); print('json_ok')"  # read-only parse check`
- verification_command_or_check: `python -m unittest discover tests -q  # baseline regression (no confirmatory outcomes)`
- verification_command_or_check: `python scripts/check_tracka_scope_registry_drift.py  # read-only drift check`
- verification_command_or_check: `python scripts/tracka_resume_check.py  # read-only resume check (network:false)`

#### admissibility_package_status.v5_window_terms_state_from_fclr018 — v5 window terms/admissibility state (from FCLR-018)
- current_state=**present_blocker** read_state=`from_fclr018` authorizes_confirmatory_outcomes=`False` satisfied=`False` satisfaction_inferred=`False`
- blocker_or_missing_reason: terms_status=EXPLICIT_BLOCKER_UNRESOLVED all_go=False confirmatory_outcomes_permitted=False
- evidence_ref: `fclr018.window.v5_terms_blocker_state` snapshot=`missing`
- action_required: Do not compute confirmatory outcomes while v5/window blocker state denies permission.
- verification_command_or_check: `python -m unittest discover tests -q  # baseline regression (no confirmatory outcomes)`
- verification_command_or_check: `python scripts/check_tracka_scope_registry_drift.py  # read-only drift check`
- verification_command_or_check: `python scripts/tracka_resume_check.py  # read-only resume check (network:false)`

#### fresh_frozen_prereg_before_outcomes_required — Fresh frozen prereg before outcomes (required)
- current_state=**missing** read_state=`policy_check` authorizes_confirmatory_outcomes=`False` satisfied=`False` satisfaction_inferred=`False`
- blocker_or_missing_reason: fresh frozen prereg before outcomes required = missing/not frozen (no concrete local frozen prereg artifact confirmed by this index)
- action_required: Create/freeze a fresh confirmatory preregistration BEFORE any confirmatory outcomes are computed (mandatory).
- action_required: Record frozen prereg hash/ref and ensure all admissibility/provenance/terms/leakage guards are green before outcomes.
- action_required: DRAFT prereg skeletons, FCLR-018 matrices, FCLR-019 indices, and FCLR-020 action matrices are NOT sufficient.
- action_required: Do not run or present v4/exploratory/confounded analyses as confirmatory claims.
- verification_command_or_check: `python -m unittest discover tests -q  # baseline regression (no confirmatory outcomes)`
- verification_command_or_check: `python scripts/check_tracka_scope_registry_drift.py  # read-only drift check`
- verification_command_or_check: `python scripts/tracka_resume_check.py  # read-only resume check (network:false)`
- verification_command_or_check: `test ! -f research_state/NO_SUCH_FRESH_FROZEN_PREREG  # placeholder reminder: a concrete frozen prereg artifact path must be supplied and verified before outcomes`

#### leakage_sufficiency_gates — Leakage controls and data sufficiency gates
- current_state=**present_unverified** read_state=`from_fclr018` authorizes_confirmatory_outcomes=`False` satisfied=`False` satisfaction_inferred=`False`
- blocker_or_missing_reason: local coverage/block-count feasibility fields present; leakage audit for any confirmatory run still requires fresh frozen prereg + admissibility package
- evidence_ref: `fclr018.window.coverage/block_fields` snapshot=`missing`
- action_required: Verify chronological leakage controls, purge/embargo as preregistered, and >=3 non-overlapping 30-day blocks / >=5 symbols for claim-worthy Gate 4 runs.
- action_required: Use only loader-compatible admissible local panel; do not threshold-shop or relax gates post-hoc.
- action_required: Local coverage/block feasibility is not a substitute for admissibility package GO + fresh frozen prereg.
- verification_command_or_check: `python -m unittest discover tests -q  # baseline regression (no confirmatory outcomes)`
- verification_command_or_check: `python scripts/check_tracka_scope_registry_drift.py  # read-only drift check`
- verification_command_or_check: `python scripts/tracka_resume_check.py  # read-only resume check (network:false)`
- verification_command_or_check: `python scripts/run_funding_ablations.py  # baseline pilot must run clean with honest verdict (no confirmatory claim from this command alone)`

### cand_2024_10_12_local_exploratory (2024-10-01..2024-12-31)
- fclr019_index_summary_state=**present_blocker** confirmatory_outcomes_go=**False**
#### identity_provenance_range — Identity/provenance range evidence (bounded)
- current_state=**present_blocker** read_state=`from_fclr018` authorizes_confirmatory_outcomes=`False` satisfied=`False` satisfaction_inferred=`False`
- blocker_or_missing_reason: provenance_status=UNVERIFIED; reasons=['v5_terms_blocker_unresolved_all_go_false', 'provenance_not_identity_verified_bounded_fclr015', 'calendar_coverage_incomplete_or_unverified', 'block_count_gate_lt_3']
- evidence_ref: `fclr018.window.provenance_status` snapshot=`missing`
- action_required: Provide verifiable bounded provenance/identity-range evidence for the candidate window (human/legal/repository evidence as applicable).
- action_required: Do not run confirmatory outcomes until provenance is identity-verified for bounded confirmatory ranges and all other guards pass.
- action_required: If FCLR-015 bounded context is claimed, ensure a readable local FCLR-015 artifact exists and is cited with hash/provenance facts (no fabrication).
- verification_command_or_check: `python -m unittest discover tests -q  # baseline regression (no confirmatory outcomes)`
- verification_command_or_check: `python scripts/check_tracka_scope_registry_drift.py  # read-only drift check`
- verification_command_or_check: `python scripts/tracka_resume_check.py  # read-only resume check (network:false)`
- verification_command_or_check: `python scripts/fclr015_gate4_cache_input_manifest.py --help >/dev/null 2>&1 || true  # read-only capability check (no confirmatory outcomes)`

#### manifest_terms_evidence — Manifest/terms evidence package
- current_state=**present_blocker** read_state=`from_fclr019_summary` authorizes_confirmatory_outcomes=`False` satisfied=`False` satisfaction_inferred=`False`
- blocker_or_missing_reason: provenance_manifest=present_blocker, terms_evidence=present_blocker
- action_required: Resolve manifest and terms evidence blockers before any confirmatory use (human/legal review required for terms).
- action_required: For v5 terms: produce verifiable RESOLVED_VERIFIED evidence only with fabricated=false and frozen scope; reconcile refs/hashes.
- action_required: Never fabricate terms/license/reviews or mark terms resolved without verifiable facts.
- verification_command_or_check: `python -m unittest discover tests -q  # baseline regression (no confirmatory outcomes)`
- verification_command_or_check: `python scripts/check_tracka_scope_registry_drift.py  # read-only drift check`
- verification_command_or_check: `python scripts/tracka_resume_check.py  # read-only resume check (network:false)`
- verification_command_or_check: `python scripts/fclr016_v5_admissibility_report.py --bogus --json 2>&1 | head -c 200  # refusal path must be parseable, exit!=0 expected`
- verification_command_or_check: `python scripts/fclr016_v5_promotion_dryrun.py --bogus --json 2>&1 | head -c 200  # refusal path must be parseable, exit!=0 expected`

#### manifest_terms_evidence.provenance_manifest — Provenance/license manifest artifact
- current_state=**present_blocker** read_state=`ok` authorizes_confirmatory_outcomes=`False` satisfied=`False` satisfaction_inferred=`False`
- blocker_or_missing_reason: confirmatory_provenance_go_false_or_missing
- evidence_ref: `research_state/fclr016_local_audit/fclr016_v5_provenance_license_manifest_20261108T014405Z.json` snapshot=`readable`
- action_required: Ensure provenance manifest exists, is readable, and states confirmatory_provenance_go/admissibility_complete/license_terms status with verifiable facts.
- action_required: Reconcile manifest refs/hashes after any legitimate evidence update; do not overwrite sealed artifacts.
- action_required: No confirmatory outcomes/freeze/promotion while this prerequisite is not concretely satisfied by verifiable evidence.
- verification_command_or_check: `test -f research_state/fclr016_local_audit/fclr016_v5_provenance_license_manifest_20261108T014405Z.json && sha256sum research_state/fclr016_local_audit/fclr016_v5_provenance_license_manifest_20261108T014405Z.json  # read-only existence/hash check`
- verification_command_or_check: `python3 -c "import json; json.load(open('research_state/fclr016_local_audit/fclr016_v5_provenance_license_manifest_20261108T014405Z.json')); print('json_ok')"  # read-only parse check`
- verification_command_or_check: `python -m unittest discover tests -q  # baseline regression (no confirmatory outcomes)`
- verification_command_or_check: `python scripts/check_tracka_scope_registry_drift.py  # read-only drift check`
- verification_command_or_check: `python scripts/tracka_resume_check.py  # read-only resume check (network:false)`

#### manifest_terms_evidence.terms_evidence — Terms/license evidence artifact (human/legal)
- current_state=**present_blocker** read_state=`ok` authorizes_confirmatory_outcomes=`False` satisfied=`False` satisfaction_inferred=`False`
- blocker_or_missing_reason: terms_status=EXPLICIT_BLOCKER_UNRESOLVED
- evidence_ref: `research_state/fclr016_local_audit/fclr016_v5_terms_evidence_BLOCKED_20261108T014835Z.json` snapshot=`readable`
- action_required: Human/legal action required: resolve EXPLICIT_BLOCKER_UNRESOLVED with verifiable evidence (fabricated=false).
- action_required: Do not create RESOLVED_VERIFIED without frozen scope and reconciled refs/hashes; do not edit .github/workflows.
- action_required: No confirmatory outcomes/freeze/promotion while this prerequisite is not concretely satisfied by verifiable evidence.
- verification_command_or_check: `test -f research_state/fclr016_local_audit/fclr016_v5_terms_evidence_BLOCKED_20261108T014835Z.json && sha256sum research_state/fclr016_local_audit/fclr016_v5_terms_evidence_BLOCKED_20261108T014835Z.json  # read-only existence/hash check`
- verification_command_or_check: `python3 -c "import json; json.load(open('research_state/fclr016_local_audit/fclr016_v5_terms_evidence_BLOCKED_20261108T014835Z.json')); print('json_ok')"  # read-only parse check`
- verification_command_or_check: `python -m unittest discover tests -q  # baseline regression (no confirmatory outcomes)`
- verification_command_or_check: `python scripts/check_tracka_scope_registry_drift.py  # read-only drift check`
- verification_command_or_check: `python scripts/tracka_resume_check.py  # read-only resume check (network:false)`

#### admissibility_package_status — Admissibility package status
- current_state=**present_blocker** read_state=`from_fclr019_summary` authorizes_confirmatory_outcomes=`False` satisfied=`False` satisfaction_inferred=`False`
- blocker_or_missing_reason: completeness=present_blocker, prereg_draft=None, v5_window=present_blocker
- action_required: Resolve completeness/leakage/admissibility blockers with verifiable local artifacts; keep v5 all_go=false handling fail-closed until resolved.
- action_required: Any confirmatory outcomes require real package all_go=true and fresh frozen prereg before outcomes.
- verification_command_or_check: `python -m unittest discover tests -q  # baseline regression (no confirmatory outcomes)`
- verification_command_or_check: `python scripts/check_tracka_scope_registry_drift.py  # read-only drift check`
- verification_command_or_check: `python scripts/tracka_resume_check.py  # read-only resume check (network:false)`

#### admissibility_package_status.completeness_leakage_audit — Completeness/leakage audit artifact
- current_state=**present_blocker** read_state=`ok` authorizes_confirmatory_outcomes=`False` satisfied=`False` satisfaction_inferred=`False`
- blocker_or_missing_reason: blockers_remaining_count=2
- evidence_ref: `research_state/fclr016_local_audit/fclr016_v5_completeness_leakage_audit_20261108T014405Z.json` snapshot=`readable`
- action_required: Address listed completeness/leakage blockers with verifiable evidence before confirmatory use.
- verification_command_or_check: `test -f research_state/fclr016_local_audit/fclr016_v5_completeness_leakage_audit_20261108T014405Z.json && sha256sum research_state/fclr016_local_audit/fclr016_v5_completeness_leakage_audit_20261108T014405Z.json  # read-only existence/hash check`
- verification_command_or_check: `python3 -c "import json; json.load(open('research_state/fclr016_local_audit/fclr016_v5_completeness_leakage_audit_20261108T014405Z.json')); print('json_ok')"  # read-only parse check`
- verification_command_or_check: `python -m unittest discover tests -q  # baseline regression (no confirmatory outcomes)`
- verification_command_or_check: `python scripts/check_tracka_scope_registry_drift.py  # read-only drift check`
- verification_command_or_check: `python scripts/tracka_resume_check.py  # read-only resume check (network:false)`

#### admissibility_package_status.confirmatory_prereg_draft_ref — Confirmatory prereg draft/ref artifact (not fresh frozen prereg)
- current_state=**present_blocker** read_state=`ok` authorizes_confirmatory_outcomes=`False` satisfied=`False` satisfaction_inferred=`False`
- blocker_or_missing_reason: prereg_draft_or_not_frozen_before_outcomes
- evidence_ref: `research_state/fclr016_local_audit/fclr016_v5_confirmatory_prereg_DRAFT_20261108T014835Z.json` snapshot=`readable`
- action_required: A DRAFT prereg skeleton/ref is not sufficient for confirmatory outcomes; fresh frozen prereg before outcomes is required.
- verification_command_or_check: `test -f research_state/fclr016_local_audit/fclr016_v5_confirmatory_prereg_DRAFT_20261108T014835Z.json && sha256sum research_state/fclr016_local_audit/fclr016_v5_confirmatory_prereg_DRAFT_20261108T014835Z.json  # read-only existence/hash check`
- verification_command_or_check: `python3 -c "import json; json.load(open('research_state/fclr016_local_audit/fclr016_v5_confirmatory_prereg_DRAFT_20261108T014835Z.json')); print('json_ok')"  # read-only parse check`
- verification_command_or_check: `python -m unittest discover tests -q  # baseline regression (no confirmatory outcomes)`
- verification_command_or_check: `python scripts/check_tracka_scope_registry_drift.py  # read-only drift check`
- verification_command_or_check: `python scripts/tracka_resume_check.py  # read-only resume check (network:false)`

#### admissibility_package_status.v5_window_terms_state_from_fclr018 — v5 window terms/admissibility state (from FCLR-018)
- current_state=**present_blocker** read_state=`from_fclr018` authorizes_confirmatory_outcomes=`False` satisfied=`False` satisfaction_inferred=`False`
- blocker_or_missing_reason: terms_status=EXPLICIT_BLOCKER_UNRESOLVED all_go=False confirmatory_outcomes_permitted=False
- evidence_ref: `fclr018.window.v5_terms_blocker_state` snapshot=`missing`
- action_required: Do not compute confirmatory outcomes while v5/window blocker state denies permission.
- verification_command_or_check: `python -m unittest discover tests -q  # baseline regression (no confirmatory outcomes)`
- verification_command_or_check: `python scripts/check_tracka_scope_registry_drift.py  # read-only drift check`
- verification_command_or_check: `python scripts/tracka_resume_check.py  # read-only resume check (network:false)`

#### fresh_frozen_prereg_before_outcomes_required — Fresh frozen prereg before outcomes (required)
- current_state=**missing** read_state=`policy_check` authorizes_confirmatory_outcomes=`False` satisfied=`False` satisfaction_inferred=`False`
- blocker_or_missing_reason: fresh frozen prereg before outcomes required = missing/not frozen (no concrete local frozen prereg artifact confirmed by this index)
- action_required: Create/freeze a fresh confirmatory preregistration BEFORE any confirmatory outcomes are computed (mandatory).
- action_required: Record frozen prereg hash/ref and ensure all admissibility/provenance/terms/leakage guards are green before outcomes.
- action_required: DRAFT prereg skeletons, FCLR-018 matrices, FCLR-019 indices, and FCLR-020 action matrices are NOT sufficient.
- action_required: Do not run or present v4/exploratory/confounded analyses as confirmatory claims.
- verification_command_or_check: `python -m unittest discover tests -q  # baseline regression (no confirmatory outcomes)`
- verification_command_or_check: `python scripts/check_tracka_scope_registry_drift.py  # read-only drift check`
- verification_command_or_check: `python scripts/tracka_resume_check.py  # read-only resume check (network:false)`
- verification_command_or_check: `test ! -f research_state/NO_SUCH_FRESH_FROZEN_PREREG  # placeholder reminder: a concrete frozen prereg artifact path must be supplied and verified before outcomes`

#### leakage_sufficiency_gates — Leakage controls and data sufficiency gates
- current_state=**present_blocker** read_state=`from_fclr018` authorizes_confirmatory_outcomes=`False` satisfied=`False` satisfaction_inferred=`False`
- blocker_or_missing_reason: calendar_coverage_incomplete_or_unverified;block_count_gate_lt_3
- evidence_ref: `fclr018.window.coverage/block_fields` snapshot=`missing`
- action_required: Verify chronological leakage controls, purge/embargo as preregistered, and >=3 non-overlapping 30-day blocks / >=5 symbols for claim-worthy Gate 4 runs.
- action_required: Use only loader-compatible admissible local panel; do not threshold-shop or relax gates post-hoc.
- action_required: Local coverage/block feasibility is not a substitute for admissibility package GO + fresh frozen prereg.
- verification_command_or_check: `python -m unittest discover tests -q  # baseline regression (no confirmatory outcomes)`
- verification_command_or_check: `python scripts/check_tracka_scope_registry_drift.py  # read-only drift check`
- verification_command_or_check: `python scripts/tracka_resume_check.py  # read-only resume check (network:false)`
- verification_command_or_check: `python scripts/run_funding_ablations.py  # baseline pilot must run clean with honest verdict (no confirmatory claim from this command alone)`

### cand_2024_04_12_mixed_evidenced_prefix (2024-04-01..2024-12-31)
- fclr019_index_summary_state=**present_blocker** confirmatory_outcomes_go=**False**
#### identity_provenance_range — Identity/provenance range evidence (bounded)
- current_state=**present_blocker** read_state=`from_fclr018` authorizes_confirmatory_outcomes=`False` satisfied=`False` satisfaction_inferred=`False`
- blocker_or_missing_reason: provenance_status=UNVERIFIED; reasons=['v5_terms_blocker_unresolved_all_go_false', 'provenance_not_identity_verified_bounded_fclr015', 'calendar_coverage_incomplete_or_unverified']
- evidence_ref: `fclr018.window.provenance_status` snapshot=`missing`
- action_required: Provide verifiable bounded provenance/identity-range evidence for the candidate window (human/legal/repository evidence as applicable).
- action_required: Do not run confirmatory outcomes until provenance is identity-verified for bounded confirmatory ranges and all other guards pass.
- action_required: If FCLR-015 bounded context is claimed, ensure a readable local FCLR-015 artifact exists and is cited with hash/provenance facts (no fabrication).
- verification_command_or_check: `python -m unittest discover tests -q  # baseline regression (no confirmatory outcomes)`
- verification_command_or_check: `python scripts/check_tracka_scope_registry_drift.py  # read-only drift check`
- verification_command_or_check: `python scripts/tracka_resume_check.py  # read-only resume check (network:false)`
- verification_command_or_check: `python scripts/fclr015_gate4_cache_input_manifest.py --help >/dev/null 2>&1 || true  # read-only capability check (no confirmatory outcomes)`

#### manifest_terms_evidence — Manifest/terms evidence package
- current_state=**present_blocker** read_state=`from_fclr019_summary` authorizes_confirmatory_outcomes=`False` satisfied=`False` satisfaction_inferred=`False`
- blocker_or_missing_reason: provenance_manifest=present_blocker, terms_evidence=present_blocker
- action_required: Resolve manifest and terms evidence blockers before any confirmatory use (human/legal review required for terms).
- action_required: For v5 terms: produce verifiable RESOLVED_VERIFIED evidence only with fabricated=false and frozen scope; reconcile refs/hashes.
- action_required: Never fabricate terms/license/reviews or mark terms resolved without verifiable facts.
- verification_command_or_check: `python -m unittest discover tests -q  # baseline regression (no confirmatory outcomes)`
- verification_command_or_check: `python scripts/check_tracka_scope_registry_drift.py  # read-only drift check`
- verification_command_or_check: `python scripts/tracka_resume_check.py  # read-only resume check (network:false)`
- verification_command_or_check: `python scripts/fclr016_v5_admissibility_report.py --bogus --json 2>&1 | head -c 200  # refusal path must be parseable, exit!=0 expected`
- verification_command_or_check: `python scripts/fclr016_v5_promotion_dryrun.py --bogus --json 2>&1 | head -c 200  # refusal path must be parseable, exit!=0 expected`

#### manifest_terms_evidence.provenance_manifest — Provenance/license manifest artifact
- current_state=**present_blocker** read_state=`ok` authorizes_confirmatory_outcomes=`False` satisfied=`False` satisfaction_inferred=`False`
- blocker_or_missing_reason: confirmatory_provenance_go_false_or_missing
- evidence_ref: `research_state/fclr016_local_audit/fclr016_v5_provenance_license_manifest_20261108T014405Z.json` snapshot=`readable`
- action_required: Ensure provenance manifest exists, is readable, and states confirmatory_provenance_go/admissibility_complete/license_terms status with verifiable facts.
- action_required: Reconcile manifest refs/hashes after any legitimate evidence update; do not overwrite sealed artifacts.
- action_required: No confirmatory outcomes/freeze/promotion while this prerequisite is not concretely satisfied by verifiable evidence.
- verification_command_or_check: `test -f research_state/fclr016_local_audit/fclr016_v5_provenance_license_manifest_20261108T014405Z.json && sha256sum research_state/fclr016_local_audit/fclr016_v5_provenance_license_manifest_20261108T014405Z.json  # read-only existence/hash check`
- verification_command_or_check: `python3 -c "import json; json.load(open('research_state/fclr016_local_audit/fclr016_v5_provenance_license_manifest_20261108T014405Z.json')); print('json_ok')"  # read-only parse check`
- verification_command_or_check: `python -m unittest discover tests -q  # baseline regression (no confirmatory outcomes)`
- verification_command_or_check: `python scripts/check_tracka_scope_registry_drift.py  # read-only drift check`
- verification_command_or_check: `python scripts/tracka_resume_check.py  # read-only resume check (network:false)`

#### manifest_terms_evidence.terms_evidence — Terms/license evidence artifact (human/legal)
- current_state=**present_blocker** read_state=`ok` authorizes_confirmatory_outcomes=`False` satisfied=`False` satisfaction_inferred=`False`
- blocker_or_missing_reason: terms_status=EXPLICIT_BLOCKER_UNRESOLVED
- evidence_ref: `research_state/fclr016_local_audit/fclr016_v5_terms_evidence_BLOCKED_20261108T014835Z.json` snapshot=`readable`
- action_required: Human/legal action required: resolve EXPLICIT_BLOCKER_UNRESOLVED with verifiable evidence (fabricated=false).
- action_required: Do not create RESOLVED_VERIFIED without frozen scope and reconciled refs/hashes; do not edit .github/workflows.
- action_required: No confirmatory outcomes/freeze/promotion while this prerequisite is not concretely satisfied by verifiable evidence.
- verification_command_or_check: `test -f research_state/fclr016_local_audit/fclr016_v5_terms_evidence_BLOCKED_20261108T014835Z.json && sha256sum research_state/fclr016_local_audit/fclr016_v5_terms_evidence_BLOCKED_20261108T014835Z.json  # read-only existence/hash check`
- verification_command_or_check: `python3 -c "import json; json.load(open('research_state/fclr016_local_audit/fclr016_v5_terms_evidence_BLOCKED_20261108T014835Z.json')); print('json_ok')"  # read-only parse check`
- verification_command_or_check: `python -m unittest discover tests -q  # baseline regression (no confirmatory outcomes)`
- verification_command_or_check: `python scripts/check_tracka_scope_registry_drift.py  # read-only drift check`
- verification_command_or_check: `python scripts/tracka_resume_check.py  # read-only resume check (network:false)`

#### admissibility_package_status — Admissibility package status
- current_state=**present_blocker** read_state=`from_fclr019_summary` authorizes_confirmatory_outcomes=`False` satisfied=`False` satisfaction_inferred=`False`
- blocker_or_missing_reason: completeness=present_blocker, prereg_draft=None, v5_window=present_blocker
- action_required: Resolve completeness/leakage/admissibility blockers with verifiable local artifacts; keep v5 all_go=false handling fail-closed until resolved.
- action_required: Any confirmatory outcomes require real package all_go=true and fresh frozen prereg before outcomes.
- verification_command_or_check: `python -m unittest discover tests -q  # baseline regression (no confirmatory outcomes)`
- verification_command_or_check: `python scripts/check_tracka_scope_registry_drift.py  # read-only drift check`
- verification_command_or_check: `python scripts/tracka_resume_check.py  # read-only resume check (network:false)`

#### admissibility_package_status.completeness_leakage_audit — Completeness/leakage audit artifact
- current_state=**present_blocker** read_state=`ok` authorizes_confirmatory_outcomes=`False` satisfied=`False` satisfaction_inferred=`False`
- blocker_or_missing_reason: blockers_remaining_count=2
- evidence_ref: `research_state/fclr016_local_audit/fclr016_v5_completeness_leakage_audit_20261108T014405Z.json` snapshot=`readable`
- action_required: Address listed completeness/leakage blockers with verifiable evidence before confirmatory use.
- verification_command_or_check: `test -f research_state/fclr016_local_audit/fclr016_v5_completeness_leakage_audit_20261108T014405Z.json && sha256sum research_state/fclr016_local_audit/fclr016_v5_completeness_leakage_audit_20261108T014405Z.json  # read-only existence/hash check`
- verification_command_or_check: `python3 -c "import json; json.load(open('research_state/fclr016_local_audit/fclr016_v5_completeness_leakage_audit_20261108T014405Z.json')); print('json_ok')"  # read-only parse check`
- verification_command_or_check: `python -m unittest discover tests -q  # baseline regression (no confirmatory outcomes)`
- verification_command_or_check: `python scripts/check_tracka_scope_registry_drift.py  # read-only drift check`
- verification_command_or_check: `python scripts/tracka_resume_check.py  # read-only resume check (network:false)`

#### admissibility_package_status.confirmatory_prereg_draft_ref — Confirmatory prereg draft/ref artifact (not fresh frozen prereg)
- current_state=**present_blocker** read_state=`ok` authorizes_confirmatory_outcomes=`False` satisfied=`False` satisfaction_inferred=`False`
- blocker_or_missing_reason: prereg_draft_or_not_frozen_before_outcomes
- evidence_ref: `research_state/fclr016_local_audit/fclr016_v5_confirmatory_prereg_DRAFT_20261108T014835Z.json` snapshot=`readable`
- action_required: A DRAFT prereg skeleton/ref is not sufficient for confirmatory outcomes; fresh frozen prereg before outcomes is required.
- verification_command_or_check: `test -f research_state/fclr016_local_audit/fclr016_v5_confirmatory_prereg_DRAFT_20261108T014835Z.json && sha256sum research_state/fclr016_local_audit/fclr016_v5_confirmatory_prereg_DRAFT_20261108T014835Z.json  # read-only existence/hash check`
- verification_command_or_check: `python3 -c "import json; json.load(open('research_state/fclr016_local_audit/fclr016_v5_confirmatory_prereg_DRAFT_20261108T014835Z.json')); print('json_ok')"  # read-only parse check`
- verification_command_or_check: `python -m unittest discover tests -q  # baseline regression (no confirmatory outcomes)`
- verification_command_or_check: `python scripts/check_tracka_scope_registry_drift.py  # read-only drift check`
- verification_command_or_check: `python scripts/tracka_resume_check.py  # read-only resume check (network:false)`

#### admissibility_package_status.v5_window_terms_state_from_fclr018 — v5 window terms/admissibility state (from FCLR-018)
- current_state=**present_blocker** read_state=`from_fclr018` authorizes_confirmatory_outcomes=`False` satisfied=`False` satisfaction_inferred=`False`
- blocker_or_missing_reason: terms_status=EXPLICIT_BLOCKER_UNRESOLVED all_go=False confirmatory_outcomes_permitted=False
- evidence_ref: `fclr018.window.v5_terms_blocker_state` snapshot=`missing`
- action_required: Do not compute confirmatory outcomes while v5/window blocker state denies permission.
- verification_command_or_check: `python -m unittest discover tests -q  # baseline regression (no confirmatory outcomes)`
- verification_command_or_check: `python scripts/check_tracka_scope_registry_drift.py  # read-only drift check`
- verification_command_or_check: `python scripts/tracka_resume_check.py  # read-only resume check (network:false)`

#### fresh_frozen_prereg_before_outcomes_required — Fresh frozen prereg before outcomes (required)
- current_state=**missing** read_state=`policy_check` authorizes_confirmatory_outcomes=`False` satisfied=`False` satisfaction_inferred=`False`
- blocker_or_missing_reason: fresh frozen prereg before outcomes required = missing/not frozen (no concrete local frozen prereg artifact confirmed by this index)
- action_required: Create/freeze a fresh confirmatory preregistration BEFORE any confirmatory outcomes are computed (mandatory).
- action_required: Record frozen prereg hash/ref and ensure all admissibility/provenance/terms/leakage guards are green before outcomes.
- action_required: DRAFT prereg skeletons, FCLR-018 matrices, FCLR-019 indices, and FCLR-020 action matrices are NOT sufficient.
- action_required: Do not run or present v4/exploratory/confounded analyses as confirmatory claims.
- verification_command_or_check: `python -m unittest discover tests -q  # baseline regression (no confirmatory outcomes)`
- verification_command_or_check: `python scripts/check_tracka_scope_registry_drift.py  # read-only drift check`
- verification_command_or_check: `python scripts/tracka_resume_check.py  # read-only resume check (network:false)`
- verification_command_or_check: `test ! -f research_state/NO_SUCH_FRESH_FROZEN_PREREG  # placeholder reminder: a concrete frozen prereg artifact path must be supplied and verified before outcomes`

#### leakage_sufficiency_gates — Leakage controls and data sufficiency gates
- current_state=**present_blocker** read_state=`from_fclr018` authorizes_confirmatory_outcomes=`False` satisfied=`False` satisfaction_inferred=`False`
- blocker_or_missing_reason: calendar_coverage_incomplete_or_unverified
- evidence_ref: `fclr018.window.coverage/block_fields` snapshot=`missing`
- action_required: Verify chronological leakage controls, purge/embargo as preregistered, and >=3 non-overlapping 30-day blocks / >=5 symbols for claim-worthy Gate 4 runs.
- action_required: Use only loader-compatible admissible local panel; do not threshold-shop or relax gates post-hoc.
- action_required: Local coverage/block feasibility is not a substitute for admissibility package GO + fresh frozen prereg.
- verification_command_or_check: `python -m unittest discover tests -q  # baseline regression (no confirmatory outcomes)`
- verification_command_or_check: `python scripts/check_tracka_scope_registry_drift.py  # read-only drift check`
- verification_command_or_check: `python scripts/tracka_resume_check.py  # read-only resume check (network:false)`
- verification_command_or_check: `python scripts/run_funding_ablations.py  # baseline pilot must run clean with honest verdict (no confirmatory claim from this command alone)`

### cand_2025_01_12_local_exploratory (2025-01-01..2025-12-31)
- fclr019_index_summary_state=**present_blocker** confirmatory_outcomes_go=**False**
#### identity_provenance_range — Identity/provenance range evidence (bounded)
- current_state=**present_blocker** read_state=`from_fclr018` authorizes_confirmatory_outcomes=`False` satisfied=`False` satisfaction_inferred=`False`
- blocker_or_missing_reason: provenance_status=UNVERIFIED; reasons=['v5_terms_blocker_unresolved_all_go_false', 'provenance_not_identity_verified_bounded_fclr015', 'calendar_coverage_incomplete_or_unverified']
- evidence_ref: `fclr018.window.provenance_status` snapshot=`missing`
- action_required: Provide verifiable bounded provenance/identity-range evidence for the candidate window (human/legal/repository evidence as applicable).
- action_required: Do not run confirmatory outcomes until provenance is identity-verified for bounded confirmatory ranges and all other guards pass.
- action_required: If FCLR-015 bounded context is claimed, ensure a readable local FCLR-015 artifact exists and is cited with hash/provenance facts (no fabrication).
- verification_command_or_check: `python -m unittest discover tests -q  # baseline regression (no confirmatory outcomes)`
- verification_command_or_check: `python scripts/check_tracka_scope_registry_drift.py  # read-only drift check`
- verification_command_or_check: `python scripts/tracka_resume_check.py  # read-only resume check (network:false)`
- verification_command_or_check: `python scripts/fclr015_gate4_cache_input_manifest.py --help >/dev/null 2>&1 || true  # read-only capability check (no confirmatory outcomes)`

#### manifest_terms_evidence — Manifest/terms evidence package
- current_state=**present_blocker** read_state=`from_fclr019_summary` authorizes_confirmatory_outcomes=`False` satisfied=`False` satisfaction_inferred=`False`
- blocker_or_missing_reason: provenance_manifest=present_blocker, terms_evidence=present_blocker
- action_required: Resolve manifest and terms evidence blockers before any confirmatory use (human/legal review required for terms).
- action_required: For v5 terms: produce verifiable RESOLVED_VERIFIED evidence only with fabricated=false and frozen scope; reconcile refs/hashes.
- action_required: Never fabricate terms/license/reviews or mark terms resolved without verifiable facts.
- verification_command_or_check: `python -m unittest discover tests -q  # baseline regression (no confirmatory outcomes)`
- verification_command_or_check: `python scripts/check_tracka_scope_registry_drift.py  # read-only drift check`
- verification_command_or_check: `python scripts/tracka_resume_check.py  # read-only resume check (network:false)`
- verification_command_or_check: `python scripts/fclr016_v5_admissibility_report.py --bogus --json 2>&1 | head -c 200  # refusal path must be parseable, exit!=0 expected`
- verification_command_or_check: `python scripts/fclr016_v5_promotion_dryrun.py --bogus --json 2>&1 | head -c 200  # refusal path must be parseable, exit!=0 expected`

#### manifest_terms_evidence.provenance_manifest — Provenance/license manifest artifact
- current_state=**present_blocker** read_state=`ok` authorizes_confirmatory_outcomes=`False` satisfied=`False` satisfaction_inferred=`False`
- blocker_or_missing_reason: confirmatory_provenance_go_false_or_missing
- evidence_ref: `research_state/fclr016_local_audit/fclr016_v5_provenance_license_manifest_20261108T014405Z.json` snapshot=`readable`
- action_required: Ensure provenance manifest exists, is readable, and states confirmatory_provenance_go/admissibility_complete/license_terms status with verifiable facts.
- action_required: Reconcile manifest refs/hashes after any legitimate evidence update; do not overwrite sealed artifacts.
- action_required: No confirmatory outcomes/freeze/promotion while this prerequisite is not concretely satisfied by verifiable evidence.
- verification_command_or_check: `test -f research_state/fclr016_local_audit/fclr016_v5_provenance_license_manifest_20261108T014405Z.json && sha256sum research_state/fclr016_local_audit/fclr016_v5_provenance_license_manifest_20261108T014405Z.json  # read-only existence/hash check`
- verification_command_or_check: `python3 -c "import json; json.load(open('research_state/fclr016_local_audit/fclr016_v5_provenance_license_manifest_20261108T014405Z.json')); print('json_ok')"  # read-only parse check`
- verification_command_or_check: `python -m unittest discover tests -q  # baseline regression (no confirmatory outcomes)`
- verification_command_or_check: `python scripts/check_tracka_scope_registry_drift.py  # read-only drift check`
- verification_command_or_check: `python scripts/tracka_resume_check.py  # read-only resume check (network:false)`

#### manifest_terms_evidence.terms_evidence — Terms/license evidence artifact (human/legal)
- current_state=**present_blocker** read_state=`ok` authorizes_confirmatory_outcomes=`False` satisfied=`False` satisfaction_inferred=`False`
- blocker_or_missing_reason: terms_status=EXPLICIT_BLOCKER_UNRESOLVED
- evidence_ref: `research_state/fclr016_local_audit/fclr016_v5_terms_evidence_BLOCKED_20261108T014835Z.json` snapshot=`readable`
- action_required: Human/legal action required: resolve EXPLICIT_BLOCKER_UNRESOLVED with verifiable evidence (fabricated=false).
- action_required: Do not create RESOLVED_VERIFIED without frozen scope and reconciled refs/hashes; do not edit .github/workflows.
- action_required: No confirmatory outcomes/freeze/promotion while this prerequisite is not concretely satisfied by verifiable evidence.
- verification_command_or_check: `test -f research_state/fclr016_local_audit/fclr016_v5_terms_evidence_BLOCKED_20261108T014835Z.json && sha256sum research_state/fclr016_local_audit/fclr016_v5_terms_evidence_BLOCKED_20261108T014835Z.json  # read-only existence/hash check`
- verification_command_or_check: `python3 -c "import json; json.load(open('research_state/fclr016_local_audit/fclr016_v5_terms_evidence_BLOCKED_20261108T014835Z.json')); print('json_ok')"  # read-only parse check`
- verification_command_or_check: `python -m unittest discover tests -q  # baseline regression (no confirmatory outcomes)`
- verification_command_or_check: `python scripts/check_tracka_scope_registry_drift.py  # read-only drift check`
- verification_command_or_check: `python scripts/tracka_resume_check.py  # read-only resume check (network:false)`

#### admissibility_package_status — Admissibility package status
- current_state=**present_blocker** read_state=`from_fclr019_summary` authorizes_confirmatory_outcomes=`False` satisfied=`False` satisfaction_inferred=`False`
- blocker_or_missing_reason: completeness=present_blocker, prereg_draft=None, v5_window=present_blocker
- action_required: Resolve completeness/leakage/admissibility blockers with verifiable local artifacts; keep v5 all_go=false handling fail-closed until resolved.
- action_required: Any confirmatory outcomes require real package all_go=true and fresh frozen prereg before outcomes.
- verification_command_or_check: `python -m unittest discover tests -q  # baseline regression (no confirmatory outcomes)`
- verification_command_or_check: `python scripts/check_tracka_scope_registry_drift.py  # read-only drift check`
- verification_command_or_check: `python scripts/tracka_resume_check.py  # read-only resume check (network:false)`

#### admissibility_package_status.completeness_leakage_audit — Completeness/leakage audit artifact
- current_state=**present_blocker** read_state=`ok` authorizes_confirmatory_outcomes=`False` satisfied=`False` satisfaction_inferred=`False`
- blocker_or_missing_reason: blockers_remaining_count=2
- evidence_ref: `research_state/fclr016_local_audit/fclr016_v5_completeness_leakage_audit_20261108T014405Z.json` snapshot=`readable`
- action_required: Address listed completeness/leakage blockers with verifiable evidence before confirmatory use.
- verification_command_or_check: `test -f research_state/fclr016_local_audit/fclr016_v5_completeness_leakage_audit_20261108T014405Z.json && sha256sum research_state/fclr016_local_audit/fclr016_v5_completeness_leakage_audit_20261108T014405Z.json  # read-only existence/hash check`
- verification_command_or_check: `python3 -c "import json; json.load(open('research_state/fclr016_local_audit/fclr016_v5_completeness_leakage_audit_20261108T014405Z.json')); print('json_ok')"  # read-only parse check`
- verification_command_or_check: `python -m unittest discover tests -q  # baseline regression (no confirmatory outcomes)`
- verification_command_or_check: `python scripts/check_tracka_scope_registry_drift.py  # read-only drift check`
- verification_command_or_check: `python scripts/tracka_resume_check.py  # read-only resume check (network:false)`

#### admissibility_package_status.confirmatory_prereg_draft_ref — Confirmatory prereg draft/ref artifact (not fresh frozen prereg)
- current_state=**present_blocker** read_state=`ok` authorizes_confirmatory_outcomes=`False` satisfied=`False` satisfaction_inferred=`False`
- blocker_or_missing_reason: prereg_draft_or_not_frozen_before_outcomes
- evidence_ref: `research_state/fclr016_local_audit/fclr016_v5_confirmatory_prereg_DRAFT_20261108T014835Z.json` snapshot=`readable`
- action_required: A DRAFT prereg skeleton/ref is not sufficient for confirmatory outcomes; fresh frozen prereg before outcomes is required.
- verification_command_or_check: `test -f research_state/fclr016_local_audit/fclr016_v5_confirmatory_prereg_DRAFT_20261108T014835Z.json && sha256sum research_state/fclr016_local_audit/fclr016_v5_confirmatory_prereg_DRAFT_20261108T014835Z.json  # read-only existence/hash check`
- verification_command_or_check: `python3 -c "import json; json.load(open('research_state/fclr016_local_audit/fclr016_v5_confirmatory_prereg_DRAFT_20261108T014835Z.json')); print('json_ok')"  # read-only parse check`
- verification_command_or_check: `python -m unittest discover tests -q  # baseline regression (no confirmatory outcomes)`
- verification_command_or_check: `python scripts/check_tracka_scope_registry_drift.py  # read-only drift check`
- verification_command_or_check: `python scripts/tracka_resume_check.py  # read-only resume check (network:false)`

#### admissibility_package_status.v5_window_terms_state_from_fclr018 — v5 window terms/admissibility state (from FCLR-018)
- current_state=**present_blocker** read_state=`from_fclr018` authorizes_confirmatory_outcomes=`False` satisfied=`False` satisfaction_inferred=`False`
- blocker_or_missing_reason: terms_status=EXPLICIT_BLOCKER_UNRESOLVED all_go=False confirmatory_outcomes_permitted=False
- evidence_ref: `fclr018.window.v5_terms_blocker_state` snapshot=`missing`
- action_required: Do not compute confirmatory outcomes while v5/window blocker state denies permission.
- verification_command_or_check: `python -m unittest discover tests -q  # baseline regression (no confirmatory outcomes)`
- verification_command_or_check: `python scripts/check_tracka_scope_registry_drift.py  # read-only drift check`
- verification_command_or_check: `python scripts/tracka_resume_check.py  # read-only resume check (network:false)`

#### fresh_frozen_prereg_before_outcomes_required — Fresh frozen prereg before outcomes (required)
- current_state=**missing** read_state=`policy_check` authorizes_confirmatory_outcomes=`False` satisfied=`False` satisfaction_inferred=`False`
- blocker_or_missing_reason: fresh frozen prereg before outcomes required = missing/not frozen (no concrete local frozen prereg artifact confirmed by this index)
- action_required: Create/freeze a fresh confirmatory preregistration BEFORE any confirmatory outcomes are computed (mandatory).
- action_required: Record frozen prereg hash/ref and ensure all admissibility/provenance/terms/leakage guards are green before outcomes.
- action_required: DRAFT prereg skeletons, FCLR-018 matrices, FCLR-019 indices, and FCLR-020 action matrices are NOT sufficient.
- action_required: Do not run or present v4/exploratory/confounded analyses as confirmatory claims.
- verification_command_or_check: `python -m unittest discover tests -q  # baseline regression (no confirmatory outcomes)`
- verification_command_or_check: `python scripts/check_tracka_scope_registry_drift.py  # read-only drift check`
- verification_command_or_check: `python scripts/tracka_resume_check.py  # read-only resume check (network:false)`
- verification_command_or_check: `test ! -f research_state/NO_SUCH_FRESH_FROZEN_PREREG  # placeholder reminder: a concrete frozen prereg artifact path must be supplied and verified before outcomes`

#### leakage_sufficiency_gates — Leakage controls and data sufficiency gates
- current_state=**present_blocker** read_state=`from_fclr018` authorizes_confirmatory_outcomes=`False` satisfied=`False` satisfaction_inferred=`False`
- blocker_or_missing_reason: calendar_coverage_incomplete_or_unverified
- evidence_ref: `fclr018.window.coverage/block_fields` snapshot=`missing`
- action_required: Verify chronological leakage controls, purge/embargo as preregistered, and >=3 non-overlapping 30-day blocks / >=5 symbols for claim-worthy Gate 4 runs.
- action_required: Use only loader-compatible admissible local panel; do not threshold-shop or relax gates post-hoc.
- action_required: Local coverage/block feasibility is not a substitute for admissibility package GO + fresh frozen prereg.
- verification_command_or_check: `python -m unittest discover tests -q  # baseline regression (no confirmatory outcomes)`
- verification_command_or_check: `python scripts/check_tracka_scope_registry_drift.py  # read-only drift check`
- verification_command_or_check: `python scripts/tracka_resume_check.py  # read-only resume check (network:false)`
- verification_command_or_check: `python scripts/run_funding_ablations.py  # baseline pilot must run clean with honest verdict (no confirmatory claim from this command alone)`

### cand_2024_01_12_local_exploratory (2024-01-01..2024-12-31)
- fclr019_index_summary_state=**present_blocker** confirmatory_outcomes_go=**False**
#### identity_provenance_range — Identity/provenance range evidence (bounded)
- current_state=**present_blocker** read_state=`from_fclr018` authorizes_confirmatory_outcomes=`False` satisfied=`False` satisfaction_inferred=`False`
- blocker_or_missing_reason: provenance_status=UNVERIFIED; reasons=['v5_terms_blocker_unresolved_all_go_false', 'provenance_not_identity_verified_bounded_fclr015', 'calendar_coverage_incomplete_or_unverified']
- evidence_ref: `fclr018.window.provenance_status` snapshot=`missing`
- action_required: Provide verifiable bounded provenance/identity-range evidence for the candidate window (human/legal/repository evidence as applicable).
- action_required: Do not run confirmatory outcomes until provenance is identity-verified for bounded confirmatory ranges and all other guards pass.
- action_required: If FCLR-015 bounded context is claimed, ensure a readable local FCLR-015 artifact exists and is cited with hash/provenance facts (no fabrication).
- verification_command_or_check: `python -m unittest discover tests -q  # baseline regression (no confirmatory outcomes)`
- verification_command_or_check: `python scripts/check_tracka_scope_registry_drift.py  # read-only drift check`
- verification_command_or_check: `python scripts/tracka_resume_check.py  # read-only resume check (network:false)`
- verification_command_or_check: `python scripts/fclr015_gate4_cache_input_manifest.py --help >/dev/null 2>&1 || true  # read-only capability check (no confirmatory outcomes)`

#### manifest_terms_evidence — Manifest/terms evidence package
- current_state=**present_blocker** read_state=`from_fclr019_summary` authorizes_confirmatory_outcomes=`False` satisfied=`False` satisfaction_inferred=`False`
- blocker_or_missing_reason: provenance_manifest=present_blocker, terms_evidence=present_blocker
- action_required: Resolve manifest and terms evidence blockers before any confirmatory use (human/legal review required for terms).
- action_required: For v5 terms: produce verifiable RESOLVED_VERIFIED evidence only with fabricated=false and frozen scope; reconcile refs/hashes.
- action_required: Never fabricate terms/license/reviews or mark terms resolved without verifiable facts.
- verification_command_or_check: `python -m unittest discover tests -q  # baseline regression (no confirmatory outcomes)`
- verification_command_or_check: `python scripts/check_tracka_scope_registry_drift.py  # read-only drift check`
- verification_command_or_check: `python scripts/tracka_resume_check.py  # read-only resume check (network:false)`
- verification_command_or_check: `python scripts/fclr016_v5_admissibility_report.py --bogus --json 2>&1 | head -c 200  # refusal path must be parseable, exit!=0 expected`
- verification_command_or_check: `python scripts/fclr016_v5_promotion_dryrun.py --bogus --json 2>&1 | head -c 200  # refusal path must be parseable, exit!=0 expected`

#### manifest_terms_evidence.provenance_manifest — Provenance/license manifest artifact
- current_state=**present_blocker** read_state=`ok` authorizes_confirmatory_outcomes=`False` satisfied=`False` satisfaction_inferred=`False`
- blocker_or_missing_reason: confirmatory_provenance_go_false_or_missing
- evidence_ref: `research_state/fclr016_local_audit/fclr016_v5_provenance_license_manifest_20261108T014405Z.json` snapshot=`readable`
- action_required: Ensure provenance manifest exists, is readable, and states confirmatory_provenance_go/admissibility_complete/license_terms status with verifiable facts.
- action_required: Reconcile manifest refs/hashes after any legitimate evidence update; do not overwrite sealed artifacts.
- action_required: No confirmatory outcomes/freeze/promotion while this prerequisite is not concretely satisfied by verifiable evidence.
- verification_command_or_check: `test -f research_state/fclr016_local_audit/fclr016_v5_provenance_license_manifest_20261108T014405Z.json && sha256sum research_state/fclr016_local_audit/fclr016_v5_provenance_license_manifest_20261108T014405Z.json  # read-only existence/hash check`
- verification_command_or_check: `python3 -c "import json; json.load(open('research_state/fclr016_local_audit/fclr016_v5_provenance_license_manifest_20261108T014405Z.json')); print('json_ok')"  # read-only parse check`
- verification_command_or_check: `python -m unittest discover tests -q  # baseline regression (no confirmatory outcomes)`
- verification_command_or_check: `python scripts/check_tracka_scope_registry_drift.py  # read-only drift check`
- verification_command_or_check: `python scripts/tracka_resume_check.py  # read-only resume check (network:false)`

#### manifest_terms_evidence.terms_evidence — Terms/license evidence artifact (human/legal)
- current_state=**present_blocker** read_state=`ok` authorizes_confirmatory_outcomes=`False` satisfied=`False` satisfaction_inferred=`False`
- blocker_or_missing_reason: terms_status=EXPLICIT_BLOCKER_UNRESOLVED
- evidence_ref: `research_state/fclr016_local_audit/fclr016_v5_terms_evidence_BLOCKED_20261108T014835Z.json` snapshot=`readable`
- action_required: Human/legal action required: resolve EXPLICIT_BLOCKER_UNRESOLVED with verifiable evidence (fabricated=false).
- action_required: Do not create RESOLVED_VERIFIED without frozen scope and reconciled refs/hashes; do not edit .github/workflows.
- action_required: No confirmatory outcomes/freeze/promotion while this prerequisite is not concretely satisfied by verifiable evidence.
- verification_command_or_check: `test -f research_state/fclr016_local_audit/fclr016_v5_terms_evidence_BLOCKED_20261108T014835Z.json && sha256sum research_state/fclr016_local_audit/fclr016_v5_terms_evidence_BLOCKED_20261108T014835Z.json  # read-only existence/hash check`
- verification_command_or_check: `python3 -c "import json; json.load(open('research_state/fclr016_local_audit/fclr016_v5_terms_evidence_BLOCKED_20261108T014835Z.json')); print('json_ok')"  # read-only parse check`
- verification_command_or_check: `python -m unittest discover tests -q  # baseline regression (no confirmatory outcomes)`
- verification_command_or_check: `python scripts/check_tracka_scope_registry_drift.py  # read-only drift check`
- verification_command_or_check: `python scripts/tracka_resume_check.py  # read-only resume check (network:false)`

#### admissibility_package_status — Admissibility package status
- current_state=**present_blocker** read_state=`from_fclr019_summary` authorizes_confirmatory_outcomes=`False` satisfied=`False` satisfaction_inferred=`False`
- blocker_or_missing_reason: completeness=present_blocker, prereg_draft=None, v5_window=present_blocker
- action_required: Resolve completeness/leakage/admissibility blockers with verifiable local artifacts; keep v5 all_go=false handling fail-closed until resolved.
- action_required: Any confirmatory outcomes require real package all_go=true and fresh frozen prereg before outcomes.
- verification_command_or_check: `python -m unittest discover tests -q  # baseline regression (no confirmatory outcomes)`
- verification_command_or_check: `python scripts/check_tracka_scope_registry_drift.py  # read-only drift check`
- verification_command_or_check: `python scripts/tracka_resume_check.py  # read-only resume check (network:false)`

#### admissibility_package_status.completeness_leakage_audit — Completeness/leakage audit artifact
- current_state=**present_blocker** read_state=`ok` authorizes_confirmatory_outcomes=`False` satisfied=`False` satisfaction_inferred=`False`
- blocker_or_missing_reason: blockers_remaining_count=2
- evidence_ref: `research_state/fclr016_local_audit/fclr016_v5_completeness_leakage_audit_20261108T014405Z.json` snapshot=`readable`
- action_required: Address listed completeness/leakage blockers with verifiable evidence before confirmatory use.
- verification_command_or_check: `test -f research_state/fclr016_local_audit/fclr016_v5_completeness_leakage_audit_20261108T014405Z.json && sha256sum research_state/fclr016_local_audit/fclr016_v5_completeness_leakage_audit_20261108T014405Z.json  # read-only existence/hash check`
- verification_command_or_check: `python3 -c "import json; json.load(open('research_state/fclr016_local_audit/fclr016_v5_completeness_leakage_audit_20261108T014405Z.json')); print('json_ok')"  # read-only parse check`
- verification_command_or_check: `python -m unittest discover tests -q  # baseline regression (no confirmatory outcomes)`
- verification_command_or_check: `python scripts/check_tracka_scope_registry_drift.py  # read-only drift check`
- verification_command_or_check: `python scripts/tracka_resume_check.py  # read-only resume check (network:false)`

#### admissibility_package_status.confirmatory_prereg_draft_ref — Confirmatory prereg draft/ref artifact (not fresh frozen prereg)
- current_state=**present_blocker** read_state=`ok` authorizes_confirmatory_outcomes=`False` satisfied=`False` satisfaction_inferred=`False`
- blocker_or_missing_reason: prereg_draft_or_not_frozen_before_outcomes
- evidence_ref: `research_state/fclr016_local_audit/fclr016_v5_confirmatory_prereg_DRAFT_20261108T014835Z.json` snapshot=`readable`
- action_required: A DRAFT prereg skeleton/ref is not sufficient for confirmatory outcomes; fresh frozen prereg before outcomes is required.
- verification_command_or_check: `test -f research_state/fclr016_local_audit/fclr016_v5_confirmatory_prereg_DRAFT_20261108T014835Z.json && sha256sum research_state/fclr016_local_audit/fclr016_v5_confirmatory_prereg_DRAFT_20261108T014835Z.json  # read-only existence/hash check`
- verification_command_or_check: `python3 -c "import json; json.load(open('research_state/fclr016_local_audit/fclr016_v5_confirmatory_prereg_DRAFT_20261108T014835Z.json')); print('json_ok')"  # read-only parse check`
- verification_command_or_check: `python -m unittest discover tests -q  # baseline regression (no confirmatory outcomes)`
- verification_command_or_check: `python scripts/check_tracka_scope_registry_drift.py  # read-only drift check`
- verification_command_or_check: `python scripts/tracka_resume_check.py  # read-only resume check (network:false)`

#### admissibility_package_status.v5_window_terms_state_from_fclr018 — v5 window terms/admissibility state (from FCLR-018)
- current_state=**present_blocker** read_state=`from_fclr018` authorizes_confirmatory_outcomes=`False` satisfied=`False` satisfaction_inferred=`False`
- blocker_or_missing_reason: terms_status=EXPLICIT_BLOCKER_UNRESOLVED all_go=False confirmatory_outcomes_permitted=False
- evidence_ref: `fclr018.window.v5_terms_blocker_state` snapshot=`missing`
- action_required: Do not compute confirmatory outcomes while v5/window blocker state denies permission.
- verification_command_or_check: `python -m unittest discover tests -q  # baseline regression (no confirmatory outcomes)`
- verification_command_or_check: `python scripts/check_tracka_scope_registry_drift.py  # read-only drift check`
- verification_command_or_check: `python scripts/tracka_resume_check.py  # read-only resume check (network:false)`

#### fresh_frozen_prereg_before_outcomes_required — Fresh frozen prereg before outcomes (required)
- current_state=**missing** read_state=`policy_check` authorizes_confirmatory_outcomes=`False` satisfied=`False` satisfaction_inferred=`False`
- blocker_or_missing_reason: fresh frozen prereg before outcomes required = missing/not frozen (no concrete local frozen prereg artifact confirmed by this index)
- action_required: Create/freeze a fresh confirmatory preregistration BEFORE any confirmatory outcomes are computed (mandatory).
- action_required: Record frozen prereg hash/ref and ensure all admissibility/provenance/terms/leakage guards are green before outcomes.
- action_required: DRAFT prereg skeletons, FCLR-018 matrices, FCLR-019 indices, and FCLR-020 action matrices are NOT sufficient.
- action_required: Do not run or present v4/exploratory/confounded analyses as confirmatory claims.
- verification_command_or_check: `python -m unittest discover tests -q  # baseline regression (no confirmatory outcomes)`
- verification_command_or_check: `python scripts/check_tracka_scope_registry_drift.py  # read-only drift check`
- verification_command_or_check: `python scripts/tracka_resume_check.py  # read-only resume check (network:false)`
- verification_command_or_check: `test ! -f research_state/NO_SUCH_FRESH_FROZEN_PREREG  # placeholder reminder: a concrete frozen prereg artifact path must be supplied and verified before outcomes`

#### leakage_sufficiency_gates — Leakage controls and data sufficiency gates
- current_state=**present_blocker** read_state=`from_fclr018` authorizes_confirmatory_outcomes=`False` satisfied=`False` satisfaction_inferred=`False`
- blocker_or_missing_reason: calendar_coverage_incomplete_or_unverified
- evidence_ref: `fclr018.window.coverage/block_fields` snapshot=`missing`
- action_required: Verify chronological leakage controls, purge/embargo as preregistered, and >=3 non-overlapping 30-day blocks / >=5 symbols for claim-worthy Gate 4 runs.
- action_required: Use only loader-compatible admissible local panel; do not threshold-shop or relax gates post-hoc.
- action_required: Local coverage/block feasibility is not a substitute for admissibility package GO + fresh frozen prereg.
- verification_command_or_check: `python -m unittest discover tests -q  # baseline regression (no confirmatory outcomes)`
- verification_command_or_check: `python scripts/check_tracka_scope_registry_drift.py  # read-only drift check`
- verification_command_or_check: `python scripts/tracka_resume_check.py  # read-only resume check (network:false)`
- verification_command_or_check: `python scripts/run_funding_ablations.py  # baseline pilot must run clean with honest verdict (no confirmatory claim from this command alone)`

Planning/draft action matrix only — not GO for confirmatory outcomes, not frozen/promoted, no prerequisite marked satisfied, no overlay/H001/Track A status change.
