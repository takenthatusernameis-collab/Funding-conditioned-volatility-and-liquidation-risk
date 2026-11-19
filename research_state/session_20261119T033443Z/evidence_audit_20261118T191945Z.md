# Evidence Audit — FCLR-LIQ-RISK-RECALIBRATION-07

**Session:** `session_20261118T191945Z`
**Campaign:** `FCLR-LIQ-RISK-RECALIBRATION-07-20261118T191714Z`
**Timestamp UTC:** 20261118T191945Z

## Summary
RISK-07 executed end-to-end on cached 2024-04..09 data. Train-only recalibration (Platt / PAVA isotonic / prior-offset) fitted on 5-fold out-of-fold train scores across three chronological holdouts with 7-day purge/embargo.

**Verdict:** `HONEST_NEGATIVE_OR_INCONCLUSIVE` — materiality floor NOT met.
**Floor met:** `false`

## Materiality floor (C1_platt / C3_prior_offset)
| Calibrator | ΔBrier sig. holdouts (>=2/3) | ΔECE>=0.005 holdouts (>=2/3) | real mean ΔBrier | placebo p95 mean | criterion_3 beats placebo | floor_met |
|---|---|---|---|---|---|---|
| C1_platt | 1 | 0 | -7.63e-05 | -4.37e-04 | true | false |
| C3_prior_offset | 1 | 0 | -6.09e-06 | -6.09e-06 | false | false |

Real mean ΔBrier (primary L10|long|H24): C1_platt -7.63e-05, C2_isotonic -2.85e-04, C3_prior_offset -6.09e-06. All at or below zero — the recalibration layer did not materially improve out-of-sample Brier/ECE beyond the label-permutation placebo.

## Primary scenario `L10|long|H24`
| Holdout | n | n_pos | C0 brier | C1 Δbrier | C2 Δbrier | C3 Δbrier | C1 ece | C2 ece | C3 ece |
|---|---|---|---|---|---|---|---|---|---|
| 2024-07 | 3720 | 78 | 0.020497 | -2.03e-04 | -4.1e-05 | -1e-06 | 0.023228 | 0.018817 | 0.021618 |
| 2024-08 | 3720 | 129 | 0.034902 | 1.17e-03 | -3.38e-03 | 1.24e-04 | 0.027562 | 0.043594 | 0.023059 |
| 2024-09 | 3480 | 2 | 0.000992 | -3.3e-05 | -4.3e-05 | 2.1e-05 | 0.021214 | 0.021338 | 0.019776 |

## Recompute
Independent re-derivation from stored per-scenario metrics: `n_discrepancies = 0`, status `RECONCILED_ZERO_DISCREPANCIES`.

## Prohibitions respected
- no sealed rescore: true
- no sealed month read: true
- no network: true
- no root research_state additions: true
- no sealed artifact mutation: true
- no workflow edits: true
- no Track C QLIKE rerun: true
- no zero-byte artifacts: true

## Honest status
EXPLORATORY/PILOT. Modeled boundary breaches only; not observed liquidations. No confirmatory claim. The RV-only baseline recalibration did not clear the pre-registered materiality floor; reported as an honest negative/inconclusive.
