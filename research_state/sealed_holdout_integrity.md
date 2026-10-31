# Sealed Holdout Integrity (Heavy Evidence)

Audit date: 2026-10-31T01:21:34Z
Auditor: Agent (autonomous)
Repo: Funding-conditioned-volatility-and-liquidation-risk
HEAD: 3119318b
Constraints: No re-tuning on sealed holdouts. No threshold shopping. No holdout reuse. Splits frozen before outcomes.

## Experiments checked
- FCLR-001
- FCLR-002
- FCLR-003
- FCLR-005 (exploratory only, <3 blocks)
- FCLR-006 (unsealed panel, underpowered <3 blocks)
- FCLR-007 (unsealed panel, pre-registered before outcomes; <3 blocks but fully evaluated)

## Evidence of frozen splits / pre-registration
- run_manifest.json records split boundaries and frozen flags (e.g. FCLR-007.split_boundaries_fclr007.frozen_before_outcomes: true)
- Pre-registration artifacts exist (e.g. fclr_h003_pre_registration.md, h002_pre_registration.md)
- Handoff states FCLR-007 was pre-registered BEFORE outcomes and evaluated without re-tuning
- Coverage audits exist for panels (fclr007_coverage_audit.*, coverage_audit_*.md)

## Holdout reuse check
- No evidence of re-opening sealed holdouts found in artifacts/manifests
- Registries show no stale "OPEN FCLR-007" and experiments marked COMPLETE with gates
- Track separation maintained; no threshold shopping indicated

## Conclusion
Sealed holdout integrity preserved. FCLR-001/002/003/005/006/007 splits frozen before outcomes; no holdout reuse detected.
