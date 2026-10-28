# Evaluation Summary (FCLR-002)

Experiment: FCLR-002
Data range: 2024-01-01 .. 2024-09-30
Generated: 2026-10-28T15:55:10Z

## Splits (frozen)
- Train: 2024-04-01T00:00:00Z .. 2024-06-08T23:00:00Z
- Val: 2024-06-16T00:00:00Z .. 2024-07-15T23:00:00Z
- Test: 2024-07-23T00:00:00Z .. 2024-09-30T23:00:00Z (7d embargo)

## Test set QLIKE (lower is better)

- B0: mean_QLIKE=0.543471 (n=8280)
- B1: mean_QLIKE=0.487438 (n=8274)
- C1: mean_QLIKE=0.487455 (n=8274)
- C2: mean_QLIKE=0.442223 (n=8274)

## Paired comparisons (block bootstrap, ~24h blocks, 2000 replications)

### C2_vs_B1
- Paired n: 8274
- Mean diff (modelA - modelB), QLIKE: -0.045215 (95% CI [-0.097648, -0.008788])
- Relative reduction (QLIKE): 9.28% (negative diff means improvement)

### C1_vs_B1
- Paired n: 8274
- Mean diff (modelA - modelB), QLIKE: 0.000017 (95% CI [-0.005982, 0.006047])
- Relative reduction (QLIKE): -0.00% (negative diff means improvement)

### C2_vs_C1
- Paired n: 8274
- Mean diff (modelA - modelB), QLIKE: -0.045232 (95% CI [-0.098089, -0.009173])
- Relative reduction (QLIKE): 9.28% (negative diff means improvement)

## Gate assessment (primary contrast C2 vs B1)

- Primary contrast C2 vs B1 meets >=2% relative QLIKE reduction: PASS
- Relative reduction: 9.28%
- 95% CI for diff (C2-B1): [-0.097648, -0.008788]

## Notes
- All results use frozen splits only; no tuning on holdout.
- Features with missing values filled with 0.0 where protocol allows or rows dropped if core RV features missing.
- Mark/index premium not fully integrated where source missing; EMA distance computed from mark prices.
