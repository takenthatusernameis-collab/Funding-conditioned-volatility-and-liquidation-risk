# FCLR-VOL-CORR-01 Evidence Audit

**Experiment ID:** FCLR-VOL-CORR-01
**Campaign:** FCLR-VOL-CORR-01-20261124T180000Z
**Session:** session_20261124T204500Z
**Audit pass:** true
**Unresolved blockers:** none
**Verdict:** NOT_SUPPORTED (status CONFIRMATORY_COMPLETE)

## Summary

Broad-panel (342+ coin, 18-month `ironflow_bulk`) funding-extreme correction-time /
correction-hazard study executed confirmatory under an outcome-blind frozen prereg.
227,023 funding-extreme events in the test period. High-RV regime median correction
9.00h vs low-RV 10.00h (contrast -10.0% relative — NOT slower in high-RV); the frozen
>=10% relative slower-correction materiality floor was NOT met and the direction was
not slower. Verdict **NOT_SUPPORTED**: the Shek (2026) correction-time pattern does
not reconstruct at broad scale. This is a valid, publishable negative result that
closes the correction-time arm.

## Evidence chain

- Source registry: 54 parquet sha256-asserted (`bad=0`), `datasets` map with
  `candles_1h`/`funding`/`open_interest`.
- Prereg: `frozen_before_outcomes=true`, `outcome_data_inspected_before_freeze=false`,
  `design.kind=event_study_survival`, `materiality_floor_rel=0.10`, bound to the
  registry sha256.
- Eval: `status=CONFIRMATORY_COMPLETE`, `holdout_opened=true`, `n_events=227023`,
  numeric baseline/candidate `median_correction_h`, `materiality_met=false`,
  `verdict=NOT_SUPPORTED`.
- Recompute: independent stdlib recompute `all_checks_match=true`, `n_checks=29`.

## Leakage review

Expanding train-only quantile thresholds; 48h purge/embargo; no random split; censored
events recorded as censored (never completed negatives); no future information in
thresholds.

## Multiplicity

Holm step-down over the declared family (regime contrast x estimand).