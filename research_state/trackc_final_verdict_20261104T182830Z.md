# TRACK C FINAL VERDICT (FCLR-011, frozen splits only) - 20261104T182846Z

Repo: Funding-conditioned-volatility-and-liquidation-risk
Git SHA: 876838c2
Branch: main
Mode: CAMPAIGN-DRIVEN | Enforcement: NO-SKIP

## Summary
Track C (funding-conditioned volatility forecasting) gate PASSED (FCLR-011). Deeper validation and robustness completed on frozen splits. Independent recomputation from stored inputs/hashes confirms reproducibility. Track C is LOCKED on frozen FCLR-011 splits. Forward replication (FCLR-012-V) remains INCONCLUSIVE/blocked on data. Overlay remains HYPOTHETICAL_ONLY.

## Evidence base
- Gate (FCLR-011): FORECAST_GATE_PASSED. Splits frozen (train 2026-01-01..2026-03-17, val 2026-03-25..2026-04-30, test 2026-05-08..2026-08-06). C2 vs B1 improvement meets floor (CI excludes zero).
- Deeper validation: research_state/trackc_deeper_validation_20261104T153049Z.md, rerun 20261104T175126Z.md. Funding-quartile monotonicity Q1 (+3.84%) -> Q4 (+11.40%). Interactions I1_fund_x_rv, I2_fund_x_ema show gains vs B1 with CIs excluding zero. Holm-adjusted ablations confirm primary contrasts.
- Robustness: research_state/trackc_robustness_20261104T154226Z.md, 20261104T154414Z.md, rerun 20261104T174238Z.md. Leave-one-symbol out and leave-one-time-block out stable. Regimes (fund sign/|fund|), funding lags (t-1/t-2), winsorization (1%/5%), bootstrap sensitivity (circular/stationary, 12h/24h/48h, >=2000 reps) all preserve C2>B1.
- Recompute audit: research_state/trackc_recompute_audit_20261104T175643Z.md. Independent rerun from stored inputs/scripts reproduces headline pattern (C2 vs B1 rel_imp ~+6.86%, QLIKE diff ~ -0.0429, CI excludes zero). Direction/significance preserved.

## Headline results (TEST, frozen)
- B1 (RV-only): QLIKE ~0.612649
- C2 (RV+funding+price/dislocation): QLIKE ~0.569740, rel_imp vs B1 ~+7.00%, diff(C2-B1) ~ -0.0429, 95% CI excludes zero (block-bootstrap >=2000)
- Cross-symbol (5): all show C2 better than B1 with CIs excluding zero (+5.9% to +7.8%)
- Funding quartiles: monotonic increasing effect with |funding| (Q1 low -> Q4 high)

## Constraints/limitations
- Frozen splits only; no sealed holdout re-evaluated; no threshold-shopping; train-only normalization; trailing-only features.
- Mark/index premium partially missing in panel but ablations/sensitivities included.
- Forward replication FCLR-012-V blocked on data (Binance archive ends 2026-11-02, 0 non-overlapping 30d blocks as of handoff).
- Track C overlay remains HYPOTHETICAL_ONLY (no trading/risk overlay deployment).
- Small numerical differences across reporting rounds are explained by aggregation scope; reproducibility confirmed.

## Verdict
**LOCKED - Track C evidence sufficient on frozen FCLR-011 splits.** No further tuning on frozen splits. Future work only if admissible new non-overlapping data appears for forward validation (FCLR-012-V) with preregistration before inspection.

Artifacts: trackc_deeper_validation_20261104T175126Z.md, trackc_robustness_20261104T174238Z.md, trackc_recompute_audit_20261104T175643Z.md, campaign_sweep_20261104T182809Z.md
