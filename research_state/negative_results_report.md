# Negative Results Report — FCLR-001

Date: 2026-10-26
Protocol: research_state/research_protocol.md v1.0 (FCLR-001, FROZEN)

This report preserves null, failed, and inconclusive outcomes with explanations.
No result below was obtained by tuning, threshold-shopping, or reuse of the sealed
holdout for selection. All outcomes use the frozen train/val/test split with a
7-calendar-day embargo.

## 1. Primary forecast test (FCLR-H001)

- **Outcome:** INCONCLUSIVE (PILOT). Forecast gate NOT MET.
- **Contrast:** C2 vs B1 on next-24-hour realized variance, out-of-sample QLIKE.
- **Point estimate:** 2.50% relative QLIKE reduction (favors C2).
- **Uncertainty:** paired block bootstrap (2000 reps, ~24h blocks) 95% CI
  [-0.123401, 0.158843] crosses zero.
- **Block requirement:** NOT MET. Test window is a single ~4-day block
  (2024-03-27..2024-03-30) versus the protocol requirement of >=3 non-overlapping
  30-day evaluation blocks across >=5 instruments.
- **Interpretation:** The numerical improvement is not distinguishable from noise
  given the dependence-aware uncertainty, and the evaluation window is too short
  and too concentrated to support a claim. Retain the null.

Secondary contrasts (also inconclusive, CIs cross zero):
- C1 vs B1: -1.84% (95% CI [-0.134702, 0.175329]).
- C2 vs C1: -0.67% (95% CI [-0.016485, 0.011301]).

## 2. Baselines

- B0 (persistence) test QLIKE = 0.140791, lower than B1 (0.147800). The simple
  persistence baseline outperforms the HAR-style volatility baseline on this
  short test window. This is a null/negative finding for the B1 model form on the
  frozen panel and is preserved rather than omitted.

## 3. Funding-correction replication (FCLR-H002)

- **Outcome:** PARTIAL replication, not a confirmatory result.
- **Finding:** 445 funding-extreme events across 5 symbols (Jan-Mar 2024); median
  correction time 8.0h, mean 12.6h among corrected events.
- **Limitation:** The working paper's full methodology (event definition, censoring
  rules, volatility-regime split, contract set) is not independently
  reconstructible from admissible public sources alone. The reconstructed numbers
  are therefore not an exact replication and cannot be promoted to a confirmatory
  claim. Correction time is not evidence on volatility forecast skill, boundary
  breaches, or observed liquidations.

## 4. Hypothetical boundary-breach forecast (FCLR-H003)

- **Outcome:** NOT STARTED. Labels are implemented
  (scripts/synthetic_boundary_labels.py, 5/5 tests passed) but no out-of-sample
  breach evaluation has been run. No margin/leverage scenario has been registered
  before outcome inspection, as required. This cell must not be reported as a null
  result; it is untested.

## 5. Observed liquidation outcomes (FCLR-H004)

- **Outcome:** BLOCKED. Direct historical liquidation labels are unavailable from
  admissible public sources.
- **Evidence:** research_state/binance_source_probe.md. No liquidationSnapshot
  archive found under data/futures/um or cm (HTTP 404). Binance fapi forceOrders
  endpoint returns 451 restricted location in this environment.
- **Handling:** Absence of data is NOT evidence of zero liquidations. Track A is
  not viable for a binary absence/presence target. Track B (modeled boundary
  breaches) and Track C (volatility/stress outcomes) proceed independently and
  must never be described as observed-liquidation validation.

## 6. Exclusions and known shortfalls

- Test window is a single ~4-day block; protocol requires >=3 non-overlapping
  30-day blocks across >=5 instruments. The frozen 2024-01-01..2024-03-31
  coverage does not support the required block structure at the frozen split rule.
- Direct liquidation labels unavailable.
- No claim of forecast skill, edge, or economic benefit is supported by any
  result in this report.

## 7. What must not be repeated

- Do not reuse the sealed holdout for model selection, threshold choice, or
  re-evaluation.
- Do not relax the block/multiplicity/uncertainty gates after seeing outcomes.
- Do not relabel exploratory or partial results as confirmatory.
- Do not report unexecuted cells (H003, H004) as completed or null.