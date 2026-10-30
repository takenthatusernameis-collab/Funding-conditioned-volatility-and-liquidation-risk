# Evaluation Summary (FCLR-006)

Experiment: FCLR-006
Data range: 2024-01-01 .. 2026-08-06
Generated: 2026-10-30T13:47:31Z

## Splits (frozen)
- Train: 2026-04-01T00:00:00Z .. 2026-04-24T23:00:00Z
- Val: 2026-05-02T00:00:00Z .. 2026-05-15T23:00:00Z
- Test: 2026-05-23T00:00:00Z .. 2026-08-06T23:00:00Z (7d embargo)

## Test set QLIKE (lower is better)

- B0: mean_QLIKE=0.518169 (n=9000)
- B1: mean_QLIKE=0.527290 (n=8987)
- C1: mean_QLIKE=0.626463 (n=8987)
- C2: mean_QLIKE=0.895879 (n=8987)

## Paired comparisons (block bootstrap, ~24h blocks, 2000 replications)

### C2_vs_B1
- Paired n: 8987
- Mean diff (modelA - modelB), QLIKE: 0.368588 (95% CI [0.173748, 0.615614])
- Relative reduction (QLIKE): -69.90% (negative diff means improvement)

### C1_vs_B1
- Paired n: 8987
- Mean diff (modelA - modelB), QLIKE: 0.099173 (95% CI [0.040500, 0.173461])
- Relative reduction (QLIKE): -18.81% (negative diff means improvement)

### C2_vs_C1
- Paired n: 8987
- Mean diff (modelA - modelB), QLIKE: 0.269416 (95% CI [0.117749, 0.462135])
- Relative reduction (QLIKE): -43.01% (negative diff means improvement)

## Gate assessment (primary contrast C2 vs B1)

- Primary contrast C2 vs B1 meets >=2% relative QLIKE reduction: NOT_MET
- Relative reduction: -69.90%
- 95% CI for diff (C2-B1): [0.173748, 0.615614] (excludes zero: no)
- Paired OOS instruments: 5 (BNBUSDT, BTCUSDT, ETHUSDT, SOLUSDT, XRPUSDT) -> >=5: PASS
- Test window: 2026-05-23 .. 2026-08-06 = 76 days = 2 non-overlapping 30-day block(s) -> >=3: NOT_MET
- Forecast gate (all criteria): NOT_MET

## Notes
- All results use frozen splits only; no tuning on holdout.
- Features with missing values filled with 0.0 where protocol allows or rows dropped if core RV features missing.
- Mark/index premium not fully integrated where source missing; EMA distance computed from mark prices.
