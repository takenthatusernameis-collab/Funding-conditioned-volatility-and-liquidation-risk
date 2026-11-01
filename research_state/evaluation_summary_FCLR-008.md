# Evaluation Summary (FCLR-008)

Experiment: FCLR-008
Data range: 2026-01-01 .. 2026-08-06
Generated: 2026-11-01T00:54:34Z

## Splits (frozen)
- Train: 2026-01-01T00:00:00Z .. 2026-03-17T23:00:00Z
- Val: 2026-03-25T00:00:00Z .. 2026-04-30T23:00:00Z
- Test: 2026-05-08T00:00:00Z .. 2026-08-06T23:00:00Z (7d embargo)

## Test set QLIKE (lower is better)

- B0: mean_QLIKE=0.330127 (n=10800)
- B1: mean_QLIKE=0.333314 (n=10785)
- C1: mean_QLIKE=0.330164 (n=10785)
- C2: mean_QLIKE=0.318996 (n=10785)

## Paired comparisons (block bootstrap, ~24h blocks, 2000 replications)

### C2_vs_B1
- Paired n: 10785
- Mean diff (modelA - modelB), QLIKE: -0.014318 (95% CI [-0.029938, 0.000524])
- Relative reduction (QLIKE): 4.30% (negative diff means improvement)

### C1_vs_B1
- Paired n: 10785
- Mean diff (modelA - modelB), QLIKE: -0.003150 (95% CI [-0.010051, 0.003832])
- Relative reduction (QLIKE): 0.94% (negative diff means improvement)

### C2_vs_C1
- Paired n: 10785
- Mean diff (modelA - modelB), QLIKE: -0.011168 (95% CI [-0.026088, 0.002175])
- Relative reduction (QLIKE): 3.38% (negative diff means improvement)

## Gate assessment (primary contrast C2 vs B1)

- Primary contrast C2 vs B1 meets >=2% relative QLIKE reduction: PASS
- Relative reduction: 4.30%
- 95% CI for diff (C2-B1): [-0.029938, 0.000524] (excludes zero: no)
- Paired OOS instruments: 5 (BNBUSDT, BTCUSDT, ETHUSDT, SOLUSDT, XRPUSDT) -> >=5: PASS
- Test window: 2026-05-08 .. 2026-08-06 = 91 days = 3 non-overlapping 30-day block(s) -> >=3: PASS
- Forecast gate (all criteria): NOT_MET

## Notes
- All results use frozen splits only; no tuning on holdout.
- Features with missing values filled with 0.0 where protocol allows or rows dropped if core RV features missing.
- Mark/index premium not fully integrated where source missing; EMA distance computed from mark prices.
