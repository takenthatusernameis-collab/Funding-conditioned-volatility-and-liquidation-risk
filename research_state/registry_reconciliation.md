# Registry Reconciliation (Heavy Evidence)
Generated: 2026-10-31T01:21:34Z
HEAD: 3119318b

## hypothesis_registry.json
- entries: 6
- contains "OPEN FCLR-007": False
- contains "FCLR-007": True

## experiment_frontier.json
- keys: ['registry_version', 'generated', 'protocol_ref', 'current_status', 'summary', 'frontier', 'coverage', 'blocked_cells', 'untested_cells', 'experiments']
- contains "OPEN FCLR-007": False

## run_manifest.json
- last_experiment: FCLR-007
- FCLR-007: {'status': 'COMPLETE', 'gate': 'NOT_MET', 'split_boundaries_fclr007': {'frozen_before_outcomes': True}}
- contains "OPEN FCLR-007": False

## Reconciliation verdict
- PASS: No stale "OPEN FCLR-007" language found in registries.
- State consistent with handoff: FCLR-007 COMPLETE gate NOT_MET; no open confirmatory path.

## Recommendation
- CI check should grep for "OPEN FCLR-007" across research_state/*.json and fail if found.