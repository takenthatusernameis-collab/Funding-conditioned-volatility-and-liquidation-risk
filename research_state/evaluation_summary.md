# Evaluation Summary (FCLR-004)

Experiment: FCLR-004
Data range: 2024-01-01 .. 2024-03-31
Generated: 2026-10-29T21:13:51Z

## Splits (frozen)
- Train: 2024-04-01T00:00:00Z .. 2024-06-08T23:00:00Z
- Val: 2024-06-16T00:00:00Z .. 2024-07-15T23:00:00Z
- Test: 2024-07-23T00:00:00Z .. 2024-09-30T23:00:00Z (7d embargo)

## Test set QLIKE (lower is better)

- B0: mean_QLIKE=N/A (no test rows) (n=0)
- B1: mean_QLIKE=N/A (no test rows) (n=0)
- C1: mean_QLIKE=N/A (no test rows) (n=0)
- C2: mean_QLIKE=N/A (no test rows) (n=0)

## Paired comparisons (block bootstrap, ~24h blocks, 2000 replications)

## Gate assessment (primary contrast C2 vs B1)

- Primary contrast: NOT_EVALUABLE
- Paired OOS instruments: 0 () -> >=5: NOT_MET
- Test window: 2024-07-23 .. 2024-09-30 = 70 days = 2 non-overlapping 30-day block(s) -> >=3: NOT_MET
- Forecast gate (all criteria): NOT_MET

## Notes
- All results use frozen splits only; no tuning on holdout.
- Features with missing values filled with 0.0 where protocol allows or rows dropped if core RV features missing.
- Mark/index premium not fully integrated where source missing; EMA distance computed from mark prices.
