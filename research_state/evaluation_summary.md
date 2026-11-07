# Evaluation Summary

**Status:** rv_baseline_complete
**Last Updated:** 2026-11-07T00:30:45Z
**Git SHA:** 9cf0778bdf591789b9df096115e17a4863d93481

## Scope
- Symbols: BTCUSDT, ETHUSDT, SOLUSDT, XRPUSDT
- Period: 2024-01-01 to 2024-03-31
- Horizon: 24h (forward RV)
- Walk-forward: chronological, purge/embargo >= 7d, train-only normalization

## Aggregate Metrics (mean across splits)
| Model | QLIKE (primary) | MAE | RMSE |
|---|---|---|---|
| Persistence (B1) | 0.6842911263640333 | 0.0017509493962043102 | 0.003220804505794008 |
| RV-HAR (B2, RV-only) | 1.59541000261996 | 0.0017367373032040807 | 0.0029209832907330377 |

## Split Details
- Split 0: test 2024-02-22T00:00:00+00:00..2024-03-31T00:00:00+00:00, n_train=2980, n_test=3600, n_models=4
  - persist: qlike=0.6842911263640333, mae=0.0017509493962043102, rmse=0.003220804505794008
  - rvhar: qlike=1.59541000261996, mae=0.0017367373032040807, rmse=0.0029209832907330377

## Notes
- Leakage-resistant: chronological splits only, purge/embargo applied, normalization fit on train only.
- Missing basis/spot treated as NaN (not zero).
- Funding ablations remain blocked until Gate 3 satisfied.