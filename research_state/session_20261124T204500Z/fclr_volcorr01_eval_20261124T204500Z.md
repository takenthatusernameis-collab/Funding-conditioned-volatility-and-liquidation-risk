# FCLR-VOL-CORR-01 Evaluation — Funding-Extreme Correction-Time / Hazard Study

**Experiment ID:** FCLR-VOL-CORR-01
**Campaign:** FCLR-VOL-CORR-01-20261124T180000Z
**Session:** session_20261124T204500Z (20261124T204500Z)
**Phase:** HEAVY_CORRECTION_EVAL_AND_RECOMPUTE

## Design (outcome-blind, frozen before outcomes)
- Event: funding extreme is |funding_rate| >= q_t where q_t is an expanding, train-only quantile of |funding_rate| per coin (no future information).
- Correction: first subsequent hour the funding rate returns inside the pre-extreme band (|funding_rate| < q_t) within 168h; censored events recorded as censored, never as completed negatives.
- Regime split: realized-volatility tercile (high vs low) from trailing 24h close-to-close log returns, train-only thresholds.
- Design: chronological walk-forward, expanding train-only thresholds, PURGE_EMBARGO_H=48, no random split, no overlapping forward targets.
- Inference: cluster-robust (CR1) by coin AND Driscoll-Kraay HAC; Holm correction over declared family (regime contrast x estimand).
- Materiality floor (frozen): high-vs-low RV regime contrast in median correction time >= 10% relative.

## Results
- Total funding-extreme events (test period): 227023
- High-RV regime: n=25260, corrected=21646, censored=3614, median_correction_h=8.99999888888889, mean_correction_h=24.0866209896876
- Low-RV regime: n=25289, corrected=22989, censored=2300, median_correction_h=9.999990555555556, mean_correction_h=24.611466325633998
- Median correction-time contrast (high vs low): -10.00% relative
- Log-rank chi2: 3.9394446064005377, p_two_sided: 0.04716634712510681
- Holm-adjusted p (hazard): 0.09433269425021362
- Holm-adjusted p (median): 0.09433269425021362
- Materiality floor (10% relative): met=False
- Direction (slower correction / lower hazard in high-RV): False
- Verdict: NOT_SUPPORTED
- Status: CONFIRMATORY_COMPLETE

## Paper claim (Shek 2026, SSRN 7529458): median correction 27h high-RV vs 3h low-RV; lower correction hazard with higher RV.

## Conclusion
The broad-panel funding-extreme correction-time/hazard study returned verdict=NOT_SUPPORTED. The Shek (2026) correction-time pattern does not clear the frozen materiality floor at broad scale; a valid negative result (NOT_SUPPORTED) closes the correction-time arm.

Generated: 2026-11-24T21:23:28Z
