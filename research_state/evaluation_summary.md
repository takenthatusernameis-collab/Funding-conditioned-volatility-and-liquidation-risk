# Evaluation Summary

**Status:** rv_baseline_complete
**Last Updated:** 2026-11-07T01:14:16Z
**Git SHA:** 9ce75ad4fcd82fcff42950d1bfe85922019cb6e6

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

## Funding Ablations (Gate 4)
**Updated:** 2026-11-07T01:24:13Z (pilot, 1 split, direct-variance OLS HAR; not a sealed claim)

| Ablation | QLIKE | ΔQLIKE vs A | MAE | neg_pred |
|---|---|---|---|---|
| A_rv_only | 1.59541000261996 | 0.0 | 0.001682307260657039 | 342.0 |
| B_rv_signed | 1.4392367821430467 | -0.1561732204769133 | 0.002343811776289131 | 188.0 |
| C_rv_abs | 1.4392367821430467 | -0.1561732204769133 | 0.002343811776289131 | 188.0 |
| D_rv_signed_abs | 1.4392367821409628 | -0.15617322047899718 | 0.0023438117762892034 | 188.0 |
| E_rv_funding_trails | 1.0644322409593807 | -0.5309777616605793 | 0.0030111074589971904 | 675.0 |

> Pilot result: funding-augmented variants (B/C/D) improve QLIKE vs RV-only (A) by ~0.16; adding trailing funding percentiles/zscores (E) improves further to QLIKE 1.0644 (Δ ≈ -0.53 vs A). Single split, 4 assets, Jan-Mar 2024; not a sealed holdout result, no block-aware CIs, no multiple-comparison control. Label PILOT/INCONCLUSIVE; expand splits and robustness before inference.
