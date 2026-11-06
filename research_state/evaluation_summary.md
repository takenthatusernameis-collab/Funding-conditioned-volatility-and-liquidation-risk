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

## Funding Ablations (Gate 4)
**Updated:** 2026-11-06T23:17:27Z (pilot, 1 split, log-target ridge HAR; not a sealed claim)

| Ablation | QLIKE | ΔQLIKE vs A | MAE | neg_pred |
|---|---|---|---|---|
| A_rv_only | 2.5828046574874402e+25 | 0.0 | 2.3755417897490293e+30 | 0.0 |
| B_rv_signed | 6.221739678582001e+38 | 6.221739678581742e+38 | 6.121341638641806e+26 | 0.0 |
| C_rv_abs | 6.221739678582001e+38 | 6.221739678581742e+38 | 6.121341638641806e+26 | 0.0 |
| D_rv_signed_abs | 6.221835275107524e+38 | 6.221835275107265e+38 | 6.121321098222818e+26 | 0.0 |
| E_rv_funding_trails | 2.510636950488436e+154 | 2.510636950488436e+154 | 1.811528758046905e+248 | 0.0 |

> Pilot result: funding variants worse than RV-only on this split/sample. Inconclusive; expand splits and robustness before inference.
