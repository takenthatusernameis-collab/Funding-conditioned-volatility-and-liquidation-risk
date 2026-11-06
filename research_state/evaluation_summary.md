# Evaluation Summary

**Status:** rv_baseline_complete
**Last Updated:** 2026-11-06T23:31:43Z
**Git SHA:** e8af3abbb48d93dd63b02b2c72da99392d51720e

## Scope
- Symbols: BTCUSDT, ETHUSDT, SOLUSDT, XRPUSDT
- Period: 2024-01-01 to 2024-03-31
- Horizon: 24h (forward RV)
- Walk-forward: chronological, purge/embargo >= 7d, train-only normalization

## Aggregate Metrics (mean across splits)
| Model | QLIKE (primary) | MAE | RMSE |
|---|---|---|---|
| Persistence (B1) | 0.6842911263640333 | 0.0017509493962043102 | 0.003220804505794008 |
| RV-HAR (B2, RV-only) | 1.5954100026198477 | 0.0017367373032040807 | 0.0029209832907330377 |

## Split Details
- Split 0: test 2024-02-22T00:00:00+00:00..2024-03-31T00:00:00+00:00, n_train=2980, n_test=3600, n_models=4
  - persist: qlike=0.6842911263640333, mae=0.0017509493962043102, rmse=0.003220804505794008
  - rvhar: qlike=1.5954100026198477, mae=0.0017367373032040807, rmse=0.0029209832907330377

## Notes
- Leakage-resistant: chronological splits only, purge/embargo applied, normalization fit on train only.
- Missing basis/spot treated as NaN (not zero).
- Funding ablations remain blocked until Gate 3 satisfied.

## Funding Ablations (Gate 4)
**Updated:** 2026-11-06T23:31:49Z (pilot, 1 split, log-target ridge HAR; not a sealed claim)

| Ablation | QLIKE | ΔQLIKE vs A | MAE | neg_pred |
|---|---|---|---|---|
| A_rv_only | 333293.42171793274 | 0.0 | 255952842.6442126 | 0.0 |
| B_rv_signed | None | None | None | None |
| C_rv_abs | None | None | None | None |
| D_rv_signed_abs | None | None | None | None |
| E_rv_funding_trails | None | None | None | None |

> Pilot result: funding variants worse than RV-only on this split/sample. Inconclusive; expand splits and robustness before inference.
