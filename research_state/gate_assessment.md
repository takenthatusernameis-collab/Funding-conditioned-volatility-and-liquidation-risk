# Forecast Gate Assessment (FCLR-001)

Date: 2026-10-26

## Criteria (protocol §5)
- >=2% relative QLIKE reduction on primary contrast C2 vs B1: 2.50% -> met numerically.
- Two-sided 95% CI for paired loss difference must support improvement: CI [-0.123401, 0.158843] crosses zero -> NOT met.
- Minimum claim-worthy test: >=5 instruments (met: 5) AND >=3 non-overlapping 30-day evaluation blocks: NOT met (test span 2024-03-27..2024-03-30, ~4 days, single block).
- Multiplicity/uncertainty conditions: not satisfied.

## Conclusion
Forecast gate: NOT MET. Result is PILOT/INCONCLUSIVE. No significance claim. Risk-overlay phase remains INELIGIBLE. No tuning on holdout, no split changes.

## Next pre-registered action
Either (a) stop per protocol with inconclusive report, or (b) pre-register a follow-up protocol version extending the out-of-sample window to >=3 non-overlapping 30-day blocks before any further model changes; do not reuse current holdout for selection.


## FCLR-004 (2026-10-29T21:53:00Z)
- Pre-registered, pivoted to 6h primary due to 24h split reuse
- Timestamp audit shows only 1 unused day, no >=30-day window outside sealed partitions
- Cannot meet >=3 blocks requirement without reusing sealed holdouts -> BLOCKED
- Forecast gate: NOT_MET (blocked by data/split constraints, not by model performance)
- Risk-overlay: INELIGIBLE

## FCLR-008 (2026-11-01T00:54:34Z) — DECISIVE UNSEALED POWERED CONFIRMATORY
- Panel: 2026-01-01..2026-08-06, 5 symbols (BTCUSDT, ETHUSDT, BNBUSDT, SOLUSDT, XRPUSDT), 218 common days, 7 non-overlapping 30-day blocks, 5232 common hourly timestamps, n=10785 paired (C1/C2).
- Splits frozen BEFORE outcomes: train 2026-01-01..2026-03-17, val 2026-03-25..2026-04-30, test 2026-05-08..2026-08-06, 7-day embargoes. run_manifest.json#split_boundaries_fclr008 frozen_before_outcomes=true. Protocol research_state/research_protocol_fclr008.md v1.0 pre-registered before outcomes.
- Test QLIKE: B0=0.330127, B1=0.333314, C1=0.330164, C2=0.318996.
- Primary contrast C2 vs B1: mean diff -0.014318, 95% CI [-0.029938, 0.000524], relative reduction +4.30% (improvement).
- Criteria:
  - >=2% relative QLIKE reduction: PASS (4.30%).
  - Two-sided 95% CI supports improvement (excludes zero on improving side): FAIL — CI [-0.029938, 0.000524] crosses zero.
  - >=5 instruments: PASS (5).
  - >=3 non-overlapping 30-day blocks: PASS (test window 91 days = 3 blocks).
- Conclusion: Forecast gate NOT_MET. H001 INCONCLUSIVE — first unsealed panel with a positive direction (FCLR-006/007 were significantly worse), but the improvement is not statistically distinguishable from zero. Overlay remains INELIGIBLE. No tuning on holdout, no split changes, no threshold shopping. Byte-identical reproducibility re-run verified (only Generated timestamp and a corrected Data-range header line differ).
- All confirmatory panels now exhausted (FCLR-003 sealed 2024 -3.78%; FCLR-006 -69.90%; FCLR-007 -3.42%; FCLR-008 +4.30% but CI crosses zero). No further unsealed powered >=3-block >=5-symbol confirmatory cell exists without NEW admissible data + fresh pre-registered experiment ID.
