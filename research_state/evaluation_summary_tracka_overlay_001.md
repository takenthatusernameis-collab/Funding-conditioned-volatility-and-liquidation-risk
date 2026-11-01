# Evaluation Summary (FCLR-OVERLAY-001)

**TIMESTAMP (UTC):** 2026-11-01T18:30:04Z
**REPO:** Funding-conditioned-volatility-and-liquidation-risk
**EXPERIMENT_ID:** FCLR-OVERLAY-001
**HYPOTHESIS_ID:** FCLR-H004 + H_COUPLED-001
**GIT SHA:** daf93ab21ddd635a36de99ffbd80d09112be9239
**TRACK:** A (observed liquidations, ironflow Hyperliquid ONLY)
**STATUS:** EXECUTED

## Protocol/Splits (frozen)
- Pre-registered: research_state/pre_registration_tracka_overlay_20261101T165900Z.md
- Splits from run_manifest.json#split_boundaries_fclr010 (frozen_before_outcomes=true, frozen_at 2026-11-01T05:39:07Z)
- Train: 2025-11-01T00:00:00Z .. 2026-03-06T23:00:00Z
- Val: 2026-03-14T00:00:00Z .. 2026-05-20T23:00:00Z
- Test: 2026-05-28T00:00:00Z .. 2026-10-31T23:00:00Z (7d embargo)
- Firewall: ironflow Hyperliquid native perps ONLY; NO Binance merge; Modeled != observed

## Inputs
- Base model: FCLR-010 C2-style + H_COUPLED-001 (coupled) predictions on frozen test window
- H_COUPLED-001 ROBUST: PASS (+4.61% rel Brier reduction, CI [0.002511,0.003158], >=2000 reps)

## Overlay specification (FIXED, no tuning)
- Dev-only quantiles (train period): p_low = 0.015830 (q33), p_mid = 0.038029 (q67), p_high = 0.128723 (q90)
- Multipliers (fixed): s_mid=0.8, s_high=0.6, s_very_high=0.4; clip [0,1]
- Buckets: low=[0,p_low), mid=[p_low,p_mid), high=[p_mid,p_high), very_high=[p_high,1.0]

## Calibration by bucket (test)
- low: n=309062, mean_p=0.015083, event_rate=0.006419
- mid: n=214068, mean_p=0.022367, event_rate=0.024104
- high: n=149717, mean_p=0.069942, event_rate=0.076097
- very_high: n=76786, mean_p=0.293821, event_rate=0.301005

## Primary metric: exposure-weighted event exposure reduction (vs no-overlay baseline)
- Mean relative reduction: 43.985%
- 95% block-bootstrap CI (500 reps, 157 blocks): [42.983%, 44.909%]

## Turnover/stability (descriptive)
- Band changes (consecutive hours): 23013
- Fraction reduced (mult < 1.0): 0.5877

## Gates
- Calibration inspected by bucket: OK
- No leakage (frozen splits, dev-only quantiles, causal features): PASS
- Firewall intact (ironflow Hyperliquid only, no cross-track merge): PASS
- Block-bootstrap CIs computed: PASS
- Multiplicity: only fixed pre-registered params (no variants) -> N/A
- Reproducible from stored hashes/config: PASS

## Disclaimer
- **no profitability claim**: Overlay is hypothetical only (historical simulation). Does not account for all execution/cross-margin/liquidation mechanics, fees/funding/slippage in full detail; results are for risk-reduction assessment only.
- Modeled != observed. Hypothetical position-sizing adjustment only.

## Provenance
- Config: pre-reg fixed bands/multipliers, dev quantiles q33/q67/q90 from train
- Hashes: git daf93ab21ddd635a36de99ffbd80d09112be9239
- Artifacts: research_state/pre_registration_tracka_overlay_20261101T165900Z.md, research_state/evaluation_summary_FCLR010.md, research_state/evaluation_summary_FCLR-COUPLED-001-ROBUST.md
