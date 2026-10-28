# Evaluation Summary (FCLR-001)

Experiment: FCLR-001
Data range: 2024-01-01 .. 2024-03-31
Generated: 2026-10-28T07:49:27Z

## Splits (frozen)
- Train: 2024-01-02T00:00:00Z .. 2024-02-24T08:00:00Z
- Val: 2024-03-02T08:00:00Z .. 2024-03-20T02:00:00Z
- Test: 2024-03-27T02:00:00Z .. 2024-03-30T23:00:00Z (7d embargo)

## Test set QLIKE (lower is better)

- B0: mean_QLIKE=0.140791 (n=70)
- B1: mean_QLIKE=0.147800 (n=70)
- C1: mean_QLIKE=0.145083 (n=70)
- C2: mean_QLIKE=0.144105 (n=70)

## Paired comparisons (block bootstrap, ~24h blocks, 2000 replications)

### C2_vs_B1
- Paired n: 70
- Mean diff (modelA - modelB), QLIKE: -0.003695 (95% CI [-0.123401, 0.158843])
- Relative reduction (QLIKE): 2.50% (negative diff means improvement)

### C1_vs_B1
- Paired n: 70
- Mean diff (modelA - modelB), QLIKE: -0.002717 (95% CI [-0.134702, 0.175329])
- Relative reduction (QLIKE): 1.84% (negative diff means improvement)

### C2_vs_C1
- Paired n: 70
- Mean diff (modelA - modelB), QLIKE: -0.000979 (95% CI [-0.016485, 0.011301])
- Relative reduction (QLIKE): 0.67% (negative diff means improvement)

## Gate assessment (primary contrast C2 vs B1)

- Primary contrast C2 vs B1 meets >=2% relative QLIKE reduction: NOT_MET
- Relative reduction: 2.50%
- 95% CI for diff (C2-B1): [-0.123401, 0.158843]

## Notes
- All results use frozen splits only; no tuning on holdout.
- Features with missing values filled with 0.0 where protocol allows or rows dropped if core RV features missing.
- Mark/index premium not fully integrated where source missing; EMA distance computed from mark prices.
