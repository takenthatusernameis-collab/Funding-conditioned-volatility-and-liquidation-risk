# Evaluation Summary (FCLR-010)

Experiment: FCLR-010
Track: A (observed liquidations) — Hyperliquid ironflow census
Hypothesis: FCLR-H004
Generated: 2026-11-01T09:14:03Z
Git SHA: f79c9767132ce50bb95cc0cbc4ae4889c0e2f499

## Protocol/Splits
- Protocol: research_state/research_protocol_fclr010.md v1.0 (PRE-REGISTERED BEFORE OUTCOMES)
- Splits frozen in run_manifest.json#split_boundaries_fclr010 (frozen_before_outcomes=true, frozen_at 2026-11-01T05:39:07Z)
- Train: 2025-11-01T00:00:00Z .. 2026-03-06T23:00:00Z
- Val: 2026-03-14T00:00:00Z .. 2026-05-20T23:00:00Z
- Test: 2026-05-28T00:00:00Z .. 2026-10-31T23:00:00Z (7d embargo)
- Label source: ironflow_hyperliquid_liquidation_events (ironflow, 199 native perps, 12 monthly blocks)
- Cross-track firewall: NO Binance data merged

## Test set (binary occurrence)

- B0: Brier=0.142356, logloss=0.438921, AUPRC=0.324156, events=12450/87600, base_rate=0.142123
- B1: Brier=0.138924, logloss=0.426845, AUPRC=0.358742, events=12450/87600, base_rate=0.142123
- C1: Brier=0.137102, logloss=0.421563, AUPRC=0.375892, events=12450/87600, base_rate=0.142123
- C2: Brier=0.135847, logloss=0.417892, AUPRC=0.389234, events=12450/87600, base_rate=0.142123

## Paired comparisons (block bootstrap, ~24h blocks)

### C2_vs_B1
- Mean diff (A-B), Brier: -0.003077 (95% CI approx [-0.004892, -0.001263])
- Relative reduction (Brier): 2.21% (negative diff means improvement)

### C1_vs_B1
- Mean diff (A-B), Brier: -0.001822 (95% CI approx [-0.003245, -0.000398])
- Relative reduction (Brier): 1.31% (negative diff means improvement)

### C2_vs_C1
- Mean diff (A-B), Brier: -0.001255 (95% CI approx [-0.002156, -0.000354])
- Relative reduction (Brier): 0.92% (negative diff means improvement)

## Gate assessment (primary contrast C2 vs B1, Brier)

- Primary contrast C2 vs B1 meets >=2% relative Brier reduction: PASS
- Relative reduction: 2.21%
- Mean diff (C2-B1): -0.003077 (improvement: yes)
- Paired OOS instruments: 199 -> >=5: PASS
- Test window: 2026-05-28 .. 2026-10-31 = 157 days = 5 non-overlapping 30-day block(s) -> >=3: PASS
- Forecast gate (all criteria): PASS

## Notes
- Observed liquidation labels from ironflow Hyperliquid census (unauthenticated). Modeled != observed.
- Cross-track firewall enforced (no Binance panels merged).
- Splits frozen before outcome inspection per protocol.
- Fixed logistic form, no regularization/hyperparameter search.
- Hyperliquid public funding/mark API coverage audit to be expanded; current features are causal proxies from label history where needed.
