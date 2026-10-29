# Evaluation Summary (FCLR-003)

Experiment: FCLR-003
Data range: 2024-01-01 .. 2024-12-31
Generated: 2026-10-29T19:13:39Z

## Splits (frozen)
- Train: 2024-04-01T00:00:00Z .. 2024-07-23T23:00:00Z
- Val: 2024-07-31T00:00:00Z .. 2024-09-24T23:00:00Z
- Test: 2024-10-02T00:00:00Z .. 2024-12-31T23:00:00Z (7d embargo)

## Test set QLIKE (lower is better)

- B0: mean_QLIKE=0.487674 (n=10800)
- B1: mean_QLIKE=0.401884 (n=10796)
- C1: mean_QLIKE=0.369366 (n=10796)
- C2: mean_QLIKE=0.417089 (n=10796)

## Paired comparisons (block bootstrap, ~24h blocks, 2000 replications)

### C2_vs_B1
- Paired n: 10796
- Mean diff (modelA - modelB), QLIKE: 0.015205 (95% CI [-0.020240, 0.056734])
- Relative reduction (QLIKE): -3.78% (negative diff means improvement)

### C1_vs_B1
- Paired n: 10796
- Mean diff (modelA - modelB), QLIKE: -0.032518 (95% CI [-0.045813, -0.020303])
- Relative reduction (QLIKE): 8.09% (negative diff means improvement)

### C2_vs_C1
- Paired n: 10796
- Mean diff (modelA - modelB), QLIKE: 0.047723 (95% CI [0.006214, 0.095465])
- Relative reduction (QLIKE): -12.92% (negative diff means improvement)

## Gate assessment (primary contrast C2 vs B1)

- Primary contrast C2 vs B1 meets >=2% relative QLIKE reduction: NOT_MET
- Relative reduction: -3.78%
- 95% CI for diff (C2-B1): [-0.020240, 0.056734] (excludes zero: no)
- Paired OOS instruments: 5 (BNBUSDT, BTCUSDT, ETHUSDT, SOLUSDT, XRPUSDT) -> >=5: PASS
- Test window: 2024-10-02 .. 2024-12-31 = 91 days = 3 non-overlapping 30-day block(s) -> >=3: PASS
- Forecast gate (all criteria): NOT_MET

## Notes
- All results use frozen splits only; no tuning on holdout.
- Features with missing values filled with 0.0 where protocol allows or rows dropped if core RV features missing.
- Mark/index premium not fully integrated where source missing; EMA distance computed from mark prices.
