# Final Inconclusive Report — FCLR-001

Date: 2026-10-26
Repository: funding-conditioned-volatility-and-liquidation-risk
Protocol: research_state/research_protocol.md v1.0 (FROZEN)
Decision: Stop with inconclusive report (option a). No risk-overlay phase.

## 1. Gates and status

| Gate | Status | Evidence |
|------|--------|----------|
| Coverage audit (>=5 instruments) | MET | 5 instruments (BTCUSDT, ETHUSDT, BNBUSDT, SOLUSDT, XRPUSDT); 2136 common hourly timestamps, 2024-01-01..2024-03-31 |
| Frozen split boundaries | MET | research_state/run_manifest.json; train 2024-01-02T00:00:00Z..2024-02-24T08:00:00Z, val 2024-03-02T08:00:00Z..2024-03-20T02:00:00Z, test 2024-03-27T02:00:00Z..2024-03-30T23:00:00Z, embargo 7d |
| Frozen research protocol | MET | research_state/research_protocol.md v1.0 |
| Direct liquidation labels | NOT VERIFIED | unavailable from public sources |
| Synthetic hypothetical mark-price boundary labels | IMPLEMENTED (5/5 tests passed) | scripts/synthetic_boundary_labels.py |
| Future realized-volatility target | IMPLEMENTED (7/7 tests passed) | scripts/forecast_pipeline.py |
| Funding-correction replication | IMPLEMENTED/PARTIAL (4/4 tests passed) | scripts/funding_correction_replication.py; 445 funding-extreme events across 5 symbols; median correction time 8.0h, mean 12.6h |
| Out-of-sample forecast gate | NOT MET (PILOT/INCONCLUSIVE) | research_state/evaluation_summary.md; research_state/gate_assessment.md |
| Risk-overlay phase | INELIGIBLE | forecast gate not met |

## 2. Tests executed

- tests/test_synthetic_boundary_labels.py: 5/5 passed
- tests/test_forecast_pipeline.py: 7/7 passed
- tests/test_funding_correction_replication.py: 4/4 passed
- Controller progress accounting: 6/6 passed

## 3. Evidence

Out-of-sample test QLIKE (lower better), n=70 per model:
- B0 = 0.140791
- B1 = 0.147800
- C1 = 0.145083
- C2 = 0.144105

Paired block bootstrap (2000 reps, ~24h blocks):
- C2 vs B1: mean diff -0.003695, 95% CI [-0.123401, 0.158843], relative reduction 2.50%
- C1 vs B1: mean diff -0.002717, 95% CI [-0.134702, 0.175329], relative reduction 1.84%
- C2 vs C1: mean diff -0.000979, 95% CI [-0.016485, 0.011301], relative reduction 0.67%

Gate criteria (protocol §5):
1. >=2% relative QLIKE reduction on primary contrast C2 vs B1: met numerically (2.50%).
2. Two-sided 95% CI for paired loss difference must support improvement: NOT met (CI crosses zero).
3. Minimum claim-worthy test: >=5 instruments (met) AND >=3 non-overlapping 30-day evaluation blocks: NOT met (test span 2024-03-27..2024-03-30, ~4 days, single block).
4. Multiplicity/uncertainty conditions: not satisfied.

## 4. Conclusion

Forecast gate: NOT MET. Result is PILOT/INCONCLUSIVE. No significance claim. Forecast improvement did not meet uncertainty/block requirements: although C2 vs B1 shows a 2.50% relative QLIKE reduction numerically, the 95% CI crosses zero and the test window is a single ~4-day block versus the protocol requirement of >=3 non-overlapping 30-day blocks. Direct liquidation labels remain unavailable. Risk-overlay phase remains INELIGIBLE.

No tuning on holdout, no split/protocol changes were made.

## 5. Blockers (unresolved)

- Direct liquidation labels unavailable.
- Forecast gate not met (PILOT/INCONCLUSIVE): CI crosses zero; insufficient test blocks per protocol requirements.

## 6. Next pre-registered action

Either (a) stop per protocol with inconclusive report (chosen), or (b) pre-register a follow-up protocol version extending the out-of-sample window to >=3 non-overlapping 30-day blocks before any further model changes; do not reuse current holdout for selection. No further model changes or OOS extension attempted without new pre-registered protocol and sufficient data.
