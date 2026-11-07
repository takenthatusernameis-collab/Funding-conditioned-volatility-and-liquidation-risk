# Evaluation Summary - Funding Ablations (Gate 4, multi-split pilot)

**Generated:** 2026-11-07T02:35:06Z
**Git SHA:** 3aa41592dd20cebc22497c8a6d4a0ce2ff2da6f7
**Pre-registration:** `research_state/pre_registration_gate4_funding_multisplit_20261107.md` (frozen before outcomes)
**Scope:** BTCUSDT, ETHUSDT, SOLUSDT, XRPUSDT, 2024-01-01 to 2024-03-31, 24h forward RV, 3 pre-registered walk-forward splits
**Model:** direct-variance OLS HAR (target = forward realized VARIANCE; train-only normalization per split; no log/exp transform)
**Verdict:** **PILOT/INCONCLUSIVE (data-sufficiency criteria not met; no claim-worthy inference)**

## Data Sufficiency (honest)
- instruments=4 (required >=5): NOT MET
- claim-worthy: False
- shortfall: instruments=4 < 5
- shortfall: no_30day_non_overlapping_test_blocks (pre-reg uses 14-day windows; Q1 2024 local data insufficient for >=3 x 30-day)
- shortfall: q1_2024_only_local_data

## Aggregate (mean across OK splits)
| Ablation | QLIKE | MAE | RMSE | ΔQLIKE vs A (pooled paired) | 95% block-bootstrap CI | n_obs/n_blocks |
|---|---|---|---|---|---|---|
| A_rv_only | 7.4632551696362475 | 0.001575245819844309 | 0.002279117352787852 | — | — | — |
| B_rv_signed | 16.987894189880944 | 0.0016771724880907523 | 0.0024518364960988983 | 8.4009401155691 | [-0.12384387819312244, 24.20983559161728] | 2605/42 |
| C_rv_abs | 16.987894189880944 | 0.0016771724880907523 | 0.0024518364960988983 | 8.4009401155691 | [-0.12384387819312244, 24.20983559161728] | 2605/42 |
| D_rv_signed_abs | 16.987894191103717 | 0.0016771724880907841 | 0.0024518364960989243 | 8.400940116333015 | [-0.12384387813653992, 24.20983559418449] | 2605/42 |
| E_rv_funding_trails | 5.543607735488995 | 0.002022002371623597 | 0.0031514411874857535 | 4.6124034791315704 | [-0.1288482496015316, 13.12243540310433] | 1819/41 |

## Per-Split Details
- Split 0: train ('2024-01-01T00:00:00+00:00', '2024-01-28T23:59:59+00:00') | test ('2024-02-05T00:00:00+00:00', '2024-02-18T23:59:59+00:00') | purge/embargo=7d | n_train=2688 n_test=1344
  - A_rv_only: qlike=0.6883380538890281, mae=0.0008245528915028976, rmse=0.0009221269311027606, n_feat=3, valid_n=1344
  - B_rv_signed: qlike=3.2430660310433765, mae=0.0009131619934817238, rmse=0.0010493431229244023, n_feat=4, valid_n=1267
  - C_rv_abs: qlike=3.2430660310433765, mae=0.0009131619934817238, rmse=0.0010493431229244023, n_feat=4, valid_n=1267
  - D_rv_signed_abs: qlike=3.243066031078264, mae=0.0009131619934817304, rmse=0.0010493431229244151, n_feat=5, valid_n=1267
  - E_rv_funding_trails: qlike=7.90803649349073, mae=0.0016748163359833674, rmse=0.0029411807736853877, n_feat=11, valid_n=1091
- Split 1: train ('2024-01-15T00:00:00+00:00', '2024-02-11T23:59:59+00:00') | test ('2024-02-19T00:00:00+00:00', '2024-03-03T23:59:59+00:00') | purge/embargo=7d | n_train=2688 n_test=1344
  - A_rv_only: qlike=2.5833688902330016, mae=0.0011163836239120016, rmse=0.0016972839145703966, n_feat=3, valid_n=1139
  - B_rv_signed: qlike=2.102867852632694, mae=0.0013002584302867638, rmse=0.002093846496068847, n_feat=4, valid_n=1059
  - C_rv_abs: qlike=2.102867852632694, mae=0.0013002584302867638, rmse=0.002093846496068847, n_feat=4, valid_n=1059
  - D_rv_signed_abs: qlike=2.102867852697096, mae=0.001300258430286846, rmse=0.0020938464960689085, n_feat=5, valid_n=1059
  - E_rv_funding_trails: qlike=3.852543947938043, mae=0.0014289206635841104, rmse=0.0022080612595874027, n_feat=11, valid_n=374
- Split 2: train ('2024-01-29T00:00:00+00:00', '2024-02-25T23:59:59+00:00') | test ('2024-03-04T00:00:00+00:00', '2024-03-17T23:59:59+00:00') | purge/embargo=7d | n_train=2688 n_test=1344
  - A_rv_only: qlike=19.11805856478671, mae=0.002784800944118028, rmse=0.0042179412126903985, n_feat=3, valid_n=558
  - B_rv_signed: qlike=45.61774868596677, mae=0.0028180970405037695, rmse=0.004212319869303446, n_feat=4, valid_n=506
  - C_rv_abs: qlike=45.61774868596677, mae=0.0028180970405037695, rmse=0.004212319869303446, n_feat=4, valid_n=506
  - D_rv_signed_abs: qlike=45.617748689535794, mae=0.002818097040503776, rmse=0.004212319869303449, n_feat=5, valid_n=506
  - E_rv_funding_trails: qlike=4.870242765038211, mae=0.0029622701153033137, rmse=0.004305081529184469, n_feat=11, valid_n=418

## Bootstrap (pre-registered)
- Paired ΔQLIKE (alt-base; negative = better for QLIKE) with circular block bootstrap on whole UTC time blocks, jointly across instruments.
- seed=12345, reps=2000, block_hours=24, alpha=0.05, two-sided percentile CI.

## Leakage/Alignment Notes
- Funding (8h) aligned to 1h via last-known value at/before each hour (ffill). NaN if missing.
- Trailing funding pct/z computed over rolling windows on aligned series (past-only).
- Chronological splits, 7d purge/embargo, train-only normalization per split.
- Basis/premium not included (no aligned admissible local series verified); missing treated as NaN per policy.

## Caveats (non-negotiable)
- **Pilot/inconclusive:** 4 instruments (<5), Q1-2024-only local data, 14-day test windows — does not satisfy FCLR-001 claim-worthy criteria (>=5 instruments, >=3 non-overlapping 30-day blocks, robust uncertainty).
- **Do NOT promote to confirmatory, do NOT claim economic value, do NOT build any overlay.** Point estimates/CIs are pilot evidence only.
- Direction/magnitude can change with more data, more splits, and claim-worthy instrument/block coverage.
