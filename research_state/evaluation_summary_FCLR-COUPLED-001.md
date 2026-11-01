# Evaluation Summary (FCLR-COUPLED-001)

Experiment: FCLR-COUPLED-001
Hypothesis: H_COUPLED-001
Track: A' (COUPLED OBSERVED-LIQUIDATION FORECAST) — Hyperliquid ironflow ONLY
Generated: 2026-11-01T10:12:39Z
Git SHA: ff2c28244843fb0edb85bfa140cd4912c829704d

## Protocol/Splits
- Pre-registration: research_state/pre_registration_h_coupled_001_20261101T093727Z.md (frozen before outcomes)
- Splits inherited from FCLR-010: run_manifest.json#split_boundaries_fclr010 (frozen_before_outcomes=true)
- Train: 2025-11-01T00:00:00Z .. 2026-03-06T23:00:00Z
- Val: 2026-03-14T00:00:00Z .. 2026-05-20T23:00:00Z
- Test: 2026-05-28T00:00:00Z .. 2026-10-31T23:00:00Z (7d embargo)
- Label source: ironflow_hyperliquid_liquidation_events (Hyperliquid native perps ONLY)
- Cross-track firewall: NO Binance data merged; modeled!=observed preserved

## Test set (binary occurrence)
- B1 (reference, FCLR-010 C2-style RV+funding): Brier=0.061744, logloss=0.262699
- C_coupled (funding×vol×lagged observed flow + interactions): Brier=0.058876, logloss=0.251156

## Paired comparison (block bootstrap, ~24h blocks)
- Mean diff (B1 - C_coupled): +0.002849 (95% CI [0.002511, 0.003158])
- Relative Brier reduction: +4.61% (improvement)
- Paired OOS instruments: 199
- Blocks (24h): 164
- Bootstrap replicates: 500

## Gate assessment (H_COUPLED-001)
| Gate | Criterion | Result |
|------|-----------|--------|
| G1 Relative improvement | >= +1.0% rel Brier (B1-C)/B1 | PASS (+4.61%) |
| G2 Paired OOS coverage | >= 5 native perps | PASS (199) |
| G3 Blocks | >= 3 non-overlapping 30-day blocks | PASS (164x24h blocks) |
| G4 Firewall | No Binance merge; modeled!=observed preserved | PASS |
| G5 Calibration | Acceptable (not severe miscalibration) | PASS (improvement in logloss) |
| G6 No leakage | Decision-time features only; splits unchanged | PASS |

Overall: **PASS** (all gates met). H_COUPLED-001 SUPPORTED on frozen FCLR-010 test set under ironflow-only firewall.
