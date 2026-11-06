# Evaluation Summary

**Status:** rv_baseline_complete
**Last Updated:** 2026-11-06T23:10:18Z
**Git SHA:** 47ad0cfacaa0d8be5e9fccc9700e750acd290148

## Scope
- Symbols: BTCUSDT, ETHUSDT, SOLUSDT, XRPUSDT
- Period: 2024-01-01 to 2024-03-31
- Horizon: 24h (forward RV)
- Walk-forward: chronological, purge/embargo >= 7d, train-only normalization

## Aggregate Metrics (mean across splits)
| Model | QLIKE (primary) | MAE | RMSE |
|---|---|---|---|
| Persistence (B1) | 40.42013461318862 | 0.031230921391122834 | 0.04309956336610376 |
| RV-HAR (B2, RV-only) | 35.21029512275652 | 0.03303496936401546 | 0.04517362255282348 |

## Split Details
- Split 0: test 2024-02-22T00:00:00+00:00..2024-03-31T00:00:00+00:00, n_train=2980, n_test=3600, n_models=4
  - persist: qlike=40.42013461318862, mae=0.031230921391122834, rmse=0.04309956336610376
  - rvhar: qlike=35.21029512275652, mae=0.03303496936401546, rmse=0.04517362255282348

## Notes
- Leakage-resistant: chronological splits only, purge/embargo applied, normalization fit on train only.
- Missing basis/spot treated as NaN (not zero).
- Funding ablations remain blocked until Gate 3 satisfied.