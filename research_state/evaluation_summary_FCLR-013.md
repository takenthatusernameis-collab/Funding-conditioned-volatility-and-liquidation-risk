# Evaluation Summary (FCLR-013)

Experiment: FCLR-013
Data range: 2026-07-01 .. 2026-09-30
Generated: 2026-11-07T11:07:34Z

## Splits (frozen)
- Train: 2026-07-01T00:00:00Z .. 2026-08-05T23:00:00Z
- Val: 2026-08-06T00:00:00Z .. 2026-08-25T23:00:00Z
- Test: 2026-08-26T00:00:00Z .. 2026-09-30T23:00:00Z (7d embargo)

## Test set QLIKE (lower is better)

- B0: mean_QLIKE=0.694317 (n=4200)
- B1: mean_QLIKE=0.452171 (n=4199)
- C1: mean_QLIKE=0.437154 (n=4199)
- C2: mean_QLIKE=0.458124 (n=4199)

## Paired comparisons (block bootstrap, ~24h blocks, 2000 replications)

### C2_vs_B1
- Paired n: 4199
- Mean diff (modelA - modelB), QLIKE: 0.005953 (95% CI [-0.011716, 0.022101])
- Relative reduction (QLIKE): -1.32% (negative diff means improvement)

### C1_vs_B1
- Paired n: 4199
- Mean diff (modelA - modelB), QLIKE: -0.015018 (95% CI [-0.030304, -0.003729])
- Relative reduction (QLIKE): 3.32% (negative diff means improvement)

### C2_vs_C1
- Paired n: 4199
- Mean diff (modelA - modelB), QLIKE: 0.020971 (95% CI [0.003206, 0.039391])
- Relative reduction (QLIKE): -4.80% (negative diff means improvement)

## Gate assessment (primary contrast C2 vs B1)

- Primary contrast C2 vs B1 meets >=2% relative QLIKE reduction: NOT_MET
- Relative reduction: -1.32%
- 95% CI for diff (C2-B1): [-0.011716, 0.022101] (excludes zero: no)
- Paired OOS instruments: 5 (BNBUSDT, BTCUSDT, ETHUSDT, SOLUSDT, XRPUSDT) -> >=5: PASS
- Test window: 2026-08-26 .. 2026-09-30 = 36 days = 1 non-overlapping 30-day block(s) -> >=3: NOT_MET
- Forecast gate (all criteria): NOT_MET

## Notes
- All results use frozen splits only; no tuning on holdout.
- Features with missing values filled with 0.0 where protocol allows or rows dropped if core RV features missing.
- Mark/index premium not fully integrated where source missing; EMA distance computed from mark prices.
