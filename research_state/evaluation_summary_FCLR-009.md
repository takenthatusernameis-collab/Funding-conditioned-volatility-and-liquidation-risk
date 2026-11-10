# Evaluation Summary (FCLR-009)

Experiment: FCLR-009
Data range: 2025-01-01 .. 2025-12-31
Generated: 2026-11-10T00:18:07Z

## Splits (frozen)
- Train: 2025-01-01T00:00:00Z .. 2025-04-05T23:00:00Z
- Val: 2025-04-13T00:00:00Z .. 2025-05-31T23:00:00Z
- Test: 2025-06-08T00:00:00Z .. 2025-12-31T23:00:00Z (7d embargo)

## Test set QLIKE (lower is better)

- B0: mean_QLIKE=0.367906 (n=24648)
- B1: mean_QLIKE=0.340756 (n=24495)
- C1: mean_QLIKE=0.339628 (n=24495)
- C2: mean_QLIKE=0.342205 (n=24495)

## Paired comparisons (block bootstrap, ~24h blocks, 2000 replications)

### C2_vs_B1
- Paired n: 24495
- Mean diff (modelA - modelB), QLIKE: 0.001449 (95% CI [-0.003120, 0.006165])
- Relative reduction (QLIKE): -0.43% (negative diff means improvement)

### C1_vs_B1
- Paired n: 24495
- Mean diff (modelA - modelB), QLIKE: -0.001128 (95% CI [-0.004738, 0.002440])
- Relative reduction (QLIKE): 0.33% (negative diff means improvement)

### C2_vs_C1
- Paired n: 24495
- Mean diff (modelA - modelB), QLIKE: 0.002577 (95% CI [-0.001426, 0.006739])
- Relative reduction (QLIKE): -0.76% (negative diff means improvement)

## Gate assessment (primary contrast C2 vs B1)

- Primary contrast C2 vs B1 meets >=2% relative QLIKE reduction: NOT_MET
- Relative reduction: -0.43%
- 95% CI for diff (C2-B1): [-0.003120, 0.006165] (excludes zero: no)
- Paired OOS instruments: 5 (BNBUSDT, BTCUSDT, ETHUSDT, SOLUSDT, XRPUSDT) -> >=5: PASS
- Test window: 2025-06-08 .. 2025-12-31 = 207 days = 6 non-overlapping 30-day block(s) -> >=3: PASS
- Forecast gate (all criteria): NOT_MET

## Notes
- All results use frozen splits only; no tuning on holdout.
- Features with missing values filled with 0.0 where protocol allows or rows dropped if core RV features missing.
- Mark/index premium not fully integrated where source missing; EMA distance computed from mark prices.
