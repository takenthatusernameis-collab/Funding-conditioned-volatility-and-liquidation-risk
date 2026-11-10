# Evaluation Summary (FCLR-014)

Experiment: FCLR-014
Data range: 2025-01-01 .. 2025-06-07
Generated: 2026-11-10T10:38:27Z

## Splits (frozen)
- Train: 2025-01-01T00:00:00Z .. 2025-04-05T23:00:00Z
- Val: 2025-04-13T00:00:00Z .. 2025-05-14T23:00:00Z
- Test: 2025-05-22T00:00:00Z .. 2025-06-07T23:00:00Z (7d embargo)

## Test set QLIKE (lower is better)

- B0: mean_QLIKE=0.373927 (n=1920)
- B1: mean_QLIKE=0.338659 (n=1918)
- C1: mean_QLIKE=0.334505 (n=1918)
- C2: mean_QLIKE=0.334792 (n=1918)

## Paired comparisons (block bootstrap, ~24h blocks, 2000 replications)

### C2_vs_B1
- Paired n: 1918
- Mean diff (modelA - modelB), QLIKE: -0.003867 (95% CI [-0.016361, 0.007728])
- Relative reduction (QLIKE): 1.14% (negative diff means improvement)

### C1_vs_B1
- Paired n: 1918
- Mean diff (modelA - modelB), QLIKE: -0.004154 (95% CI [-0.011299, 0.003046])
- Relative reduction (QLIKE): 1.23% (negative diff means improvement)

### C2_vs_C1
- Paired n: 1918
- Mean diff (modelA - modelB), QLIKE: 0.000287 (95% CI [-0.007433, 0.008595])
- Relative reduction (QLIKE): -0.09% (negative diff means improvement)

## Gate assessment (primary contrast C2 vs B1)

- Primary contrast C2 vs B1 meets >=2% relative QLIKE reduction: NOT_MET
- Relative reduction: 1.14%
- 95% CI for diff (C2-B1): [-0.016361, 0.007728] (excludes zero: no)
- Paired OOS instruments: 5 (BNBUSDT, BTCUSDT, ETHUSDT, SOLUSDT, XRPUSDT) -> >=5: PASS
- Test window: 2025-05-22 .. 2025-06-07 = 17 days = 0 non-overlapping 30-day block(s) -> >=3: NOT_MET
- Forecast gate (all criteria): NOT_MET

## Notes
- All results use frozen splits only; no tuning on holdout.
- Features with missing values filled with 0.0 where protocol allows or rows dropped if core RV features missing.
- Mark/index premium not fully integrated where source missing; EMA distance computed from mark prices.
