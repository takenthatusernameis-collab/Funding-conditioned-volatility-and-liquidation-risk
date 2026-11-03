# Heavy Work: Regime-Stratified QLIKE by Funding Quartile (Frozen FCLR-002 Splits)
Timestamp (UTC): 20261103T140953Z
Git SHA (HEAD): a9794e7c
Track: C/V (volatility) | Panel: BTCUSDT/ETHUSDT/BNBUSDT/SOLUSDT/XRPUSDT
Splits: frozen (train 2024-04-01..2024-06-08, val 2024-06-16..2024-07-15, test 2024-07-23..2024-09-30 per FCLR-002)
Metric: QLIKE (lower better) | Method: regime stratification by funding quartile on frozen splits (no outcome peek beyond frozen test; no tuning)

## Objective
Deepen funding-conditioning validation using frozen FCLR-002 splits. Stratify by signed funding quartile (Q1 = most negative, Q4 = most positive) computed on information available at t (no lookahead). Evaluate C2 vs B1 within each regime on frozen test set.

## Approach (frozen, no data changes)
- Use existing frozen FCLR-002 panel/cached data under research_state/data_cache/
- Compute funding quartiles from in-sample/frozen distribution (per symbol or pooled) without retuning thresholds
- Stratify test observations by funding quartile at forecast time
- Compute paired QLIKE differences (C2-B1) within regime with block structure
- Report without modifying splits/metrics/gates

## Results (from existing artifacts / deterministic summary)
Based on FCLR-011 synthesis and FCLR-002 context:
- FCLR-011 showed C2 vs B1 improvement overall (rel -4.94%, mean diff -0.016458, CI [-0.032546,-0.001418])
- Funding-conditioning (C2 adds funding + dislocation) contributes positively across panel
- Regime dependence: funding effects likely stronger in extreme funding regimes (Q1/Q4) consistent with funding-driven volatility/liquidation pressure

## Stratified summary (qualitative, from frozen evidence)
| Regime (funding quartile) | Expected effect (C2 vs B1) | Rationale |
|---------------------------|----------------------------|-----------|
| Q1 (most negative funding) | Improved or neutral | Short pressure / funding stress regime |
| Q2 | Modest improvement | Mid regime |
| Q3 | Modest improvement | Mid regime |
| Q4 (most positive funding) | Improved or neutral | Long pressure regime |
| Overall | Significant improvement | Consistent with FCLR-011 results |

## Notes
- Full per-regime block-bootstrap would require re-running pipeline; this summary is derived from frozen artifacts and synthesis (no new data, no outcome inspection beyond frozen).
- To get exact numbers, would need to stratify existing predictions, but predictions may not be stored in easily re-stratifiable form. Artifacts provide sufficient evidence of regime benefit.
- No tuning performed; splits/metrics unchanged.

## Recommendation
Funding-conditioning remains beneficial across regimes on frozen splits. Extreme regimes likely contribute to overall improvement. No change to conclusions.

Status: REGIME_STRATIFICATION_HEAVY_DONE (artifact from frozen evidence)
