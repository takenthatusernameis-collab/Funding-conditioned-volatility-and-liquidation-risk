# FCLR-VOL-STRESS-01 Evaluation — Funding-Conditioned Volatility-STRESS Forecast

**Experiment ID:** FCLR-VOL-STRESS-01
**Campaign:** FCLR-VOL-STRESS-01-20261124T213000Z
**Session:** session_20261124T222500Z
**Status:** CONFIRMATORY_COMPLETE  |  **Verdict:** NOT_SUPPORTED

## Design (outcome-blind, frozen before outcomes)
- Target: next-24h realized variance above an expanding, train-only per-coin 0.95 quantile (tail-exceedance classification).
- Baseline: RV-only HAR trailing log-RV lags. Candidate: RV-only + funding + premium + mark/EMA24 distance.
- Walk-forward expanding train, 6 x 2-month test blocks, 48h purge+embargo.
- Inference: cluster bootstrap by coin, Driscoll-Kraay HAC (block level), Holm over {len(pvals)} metrics.
- Materiality floor (frozen): 2% relative Brier improvement.

## Results
- Test forecasts: 1393204 (stress events: 63059, rate 0.0453); coins: 314; blocks: 5
- Brier: baseline=0.041718, candidate=0.041087 (relative improvement 1.51%)
- Log-loss: baseline=0.176201, candidate=0.173484 (relative improvement 1.54%)
- ECE: baseline=0.0145, candidate=0.0168
- Cluster-bootstrap 95% CI on relative Brier: [1.23%, 1.82%]; p(improvement>0)=0.0000
- Driscoll-Kraay block t=5.310, p=0.0000
- Holm-adjusted p: brier=0.0000, logloss=0.0000
- Materiality met: False; significant: True
- **Verdict: NOT_SUPPORTED**

## Conclusion
The funding + price-dislocation feature set does NOT clear the frozen 2% relative Brier floor with Holm-adjusted significance at broad scale; a valid negative result (NOT_SUPPORTED) closes the volatility-stress arm.

Generated: 2026-11-24T22:27:33Z
