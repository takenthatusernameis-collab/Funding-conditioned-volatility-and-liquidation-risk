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
**Updated:** 2026-11-07T02:35:06Z (multi-split pilot, 3 splits, direct-variance OLS HAR; NOT claim-worthy)
**Verdict:** PILOT/INCONCLUSIVE (data-sufficiency criteria not met; no claim-worthy inference)

| Ablation | QLIKE (mean) | ΔQLIKE vs A (pooled) | 95% block-bootstrap CI |
|---|---|---|---|
| A_rv_only | 7.4632551696362475 | — | — |
| B_rv_signed | 16.987894189880944 | 8.4009401155691 | [-0.12384387819312244, 24.20983559161728] |
| C_rv_abs | 16.987894189880944 | 8.4009401155691 | [-0.12384387819312244, 24.20983559161728] |
| D_rv_signed_abs | 16.987894191103717 | 8.400940116333015 | [-0.12384387813653992, 24.20983559418449] |
| E_rv_funding_trails | 5.543607735488995 | 4.6124034791315704 | [-0.1288482496015316, 13.12243540310433] |

> Shortfalls: instruments=4 < 5; no_30day_non_overlapping_test_blocks (pre-reg uses 14-day windows; Q1 2024 local data insufficient for >=3 x 30-day); q1_2024_only_local_data. No confirmatory claim; no economic value claim.
