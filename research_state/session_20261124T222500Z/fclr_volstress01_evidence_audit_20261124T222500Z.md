# FCLR-VOL-STRESS-01 Evidence Audit

**Experiment ID:** FCLR-VOL-STRESS-01
**Session:** session_20261124T222500Z
**Audit pass:** True
**Verdict:** NOT_SUPPORTED
**Unresolved blockers:** none

## Reconciliation
- Eval verdict: NOT_SUPPORTED
- Recompute verdict: None (all_checks_match=True, n_checks=31)
- Materiality met: False (floor 0.02, relative Brier improvement 0.015120837271339846)
- Events: 1393204 across 314 coins / 5 test blocks

## Notes
- Outcome-blind prereg frozen before outcomes and bound to the source-registry sha256.
- Every source parquet .sha256 sidecar recomputed and matched (bad=0).
- Independent stdlib recompute reproduces the headline Brier relative improvement, materiality, and verdict.
- Verdict is a valid, publishable negative result (NOT_SUPPORTED): the funding + price feature set does not clear the frozen 2% relative Brier floor at broad scale.
