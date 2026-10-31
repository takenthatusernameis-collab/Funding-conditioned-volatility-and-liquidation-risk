# Evaluation Summary (FCLR-007)

Experiment: FCLR-007
Data range: 2024-01-01 .. 2026-07-31
Generated: 2026-10-31T00:21:05Z

## Splits (frozen)
- Train: 2026-04-01T00:00:00Z .. 2026-06-12T23:00:00Z
- Val: 2026-06-20T00:00:00Z .. 2026-07-13T23:00:00Z
- Test: 2026-07-21T00:00:00Z .. 2026-07-31T23:00:00Z (7d embargo)

## Test set QLIKE (lower is better)

- B0: mean_QLIKE=0.296547 (n=1200)
- B1: mean_QLIKE=0.300377 (n=1195)
- C1: mean_QLIKE=0.302530 (n=1195)
- C2: mean_QLIKE=0.310635 (n=1195)

## Paired comparisons (block bootstrap, ~24h blocks, 2000 replications)

### C2_vs_B1
- Paired n: 1195
- Mean diff (modelA - modelB), QLIKE: 0.010258 (95% CI [0.001308, 0.019737])
- Relative reduction (QLIKE): -3.42% (negative diff means improvement)

### C1_vs_B1
- Paired n: 1195
- Mean diff (modelA - modelB), QLIKE: 0.002153 (95% CI [-0.012934, 0.018661])
- Relative reduction (QLIKE): -0.72% (negative diff means improvement)

### C2_vs_C1
- Paired n: 1195
- Mean diff (modelA - modelB), QLIKE: 0.008106 (95% CI [-0.006195, 0.022205])
- Relative reduction (QLIKE): -2.68% (negative diff means improvement)

## Gate assessment (primary contrast C2 vs B1)

- Primary contrast C2 vs B1 meets >=2% relative QLIKE reduction: NOT_MET
- Relative reduction: -3.42%
- 95% CI for diff (C2-B1): [0.001308, 0.019737] (excludes zero: no)
- Paired OOS instruments: 5 (BNBUSDT, BTCUSDT, ETHUSDT, SOLUSDT, XRPUSDT) -> >=5: PASS
- Test window: 2026-07-21 .. 2026-07-31 = 11 days = 0 non-overlapping 30-day block(s) -> >=3: NOT_MET
- Forecast gate (all criteria): NOT_MET

## Notes
- All results use frozen splits only; no tuning on holdout.
- Features with missing values filled with 0.0 where protocol allows or rows dropped if core RV features missing.
- Mark/index premium not fully integrated where source missing; EMA distance computed from mark prices.
