# Evaluation Summary (FCLR-001)

Experiment: FCLR-002
Data range: 2024-01-01 .. 2024-06-30
Generated: 2026-10-26T12:19:30Z

## Splits (frozen)
- Train: 2024-01-02T00:00:00Z .. 2024-02-24T08:00:00Z
- Val: 2024-03-02T08:00:00Z .. 2024-03-20T02:00:00Z
- Test: 2024-03-27T02:00:00Z .. 2024-03-30T23:00:00Z (7d embargo)

## Test set QLIKE (lower is better)

- B0: mean_QLIKE=0.432319 (n=94)
- B1: mean_QLIKE=0.399218 (n=94)
- C1: mean_QLIKE=0.769779 (n=94)
- C2: mean_QLIKE=0.752404 (n=94)

## Paired comparisons (block bootstrap, ~24h blocks, 2000 replications)

### C2_vs_B1
- Paired n: 94
- Mean diff (modelA - modelB), QLIKE: 0.353186 (95% CI [-0.078192, 1.037320])
- Relative reduction (QLIKE): -88.47% (negative diff means improvement)

### C1_vs_B1
- Paired n: 94
- Mean diff (modelA - modelB), QLIKE: 0.370560 (95% CI [-0.084321, 1.085979])
- Relative reduction (QLIKE): -92.82% (negative diff means improvement)

### C2_vs_C1
- Paired n: 94
- Mean diff (modelA - modelB), QLIKE: -0.017375 (95% CI [-0.048658, 0.006128])
- Relative reduction (QLIKE): 2.26% (negative diff means improvement)

## Gate assessment (primary contrast C2 vs B1)

- Primary contrast C2 vs B1 meets >=2% relative QLIKE reduction: NOT_MET
- Relative reduction: -88.47%
- 95% CI for diff (C2-B1): [-0.078192, 1.037320]

## Notes
- All results use frozen splits only; no tuning on holdout.
- Features with missing values filled with 0.0 where protocol allows or rows dropped if core RV features missing.
- Mark/index premium not fully integrated where source missing; EMA distance computed from mark prices.
