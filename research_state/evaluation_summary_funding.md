# Evaluation Summary - Funding Ablations (Gate 4, multi-split pilot)

**Generated:** 2026-11-08T16:37:31Z
**Git SHA:** daa559aa065313e5396c91153c85e1b470b4a033
**Pre-registration:** `research_state/pre_registration_gate4_funding_multisplit_20261107.md` (frozen before outcomes)
**Scope:** BTCUSDT, ETHUSDT, SOLUSDT, XRPUSDT, 2024-01-01 to 2024-03-31, 24h forward RV, 3 pre-registered walk-forward splits
**Model:** direct-variance OLS HAR (target = forward realized VARIANCE; train-only normalization per split; no log/exp transform)
**Verdict:** **PILOT/INCONCLUSIVE (data-sufficiency criteria not met; no claim-worthy inference)**

## Data Sufficiency (honest)
- instruments=4 (required >=5): NOT MET
- claim-worthy: False
- shortfall: instruments=4 < 5
- shortfall: insufficient_30day_non_overlapping_test_blocks (ok_30d=0, required>=3, split_test_days=[14, 14, 14])

## Aggregate (mean across OK splits)
| Ablation | QLIKE | MAE | RMSE | ΔQLIKE vs A (pooled paired) | 95% block-bootstrap CI | n_obs/n_blocks |
|---|---|---|---|---|---|---|
| A_rv_only | 7.463255169636498 | 0.0015752458198443093 | 0.0022791173527878517 | — | — | — |
| B_rv_signed | 16.987894189915938 | 0.0016771724880907514 | 0.0024518364960988983 | 8.400940115566256 | [-0.12384387819379696, 24.209835591605284] | 2605/42 |
| C_rv_abs | 16.987894189915938 | 0.0016771724880907514 | 0.0024518364960988983 | 8.400940115566256 | [-0.12384387819379696, 24.209835591605284] | 2605/42 |
| D_rv_signed_abs | 16.98789419113723 | 0.0016771724880907833 | 0.0024518364960989234 | 8.40094011632883 | [-0.12384387813694987, 24.209835594169473] | 2605/42 |
| E_rv_funding_trails | 5.543607735698287 | 0.0020220023716236127 | 0.0031514411874857488 | 4.612403479236548 | [-0.1288482496006673, 13.122435403144543] | 1819/41 |

## Per-Split Paired ΔQLIKE vs A (instability visibility)
| Contrast | Split 0 | Split 1 | Split 2 | n_obs (0/1/2) |
|---|---:|---:|---:|---|
| B_rv_signed vs A | 2.763598178916185 | -0.8255528770169275 | 39.77353016009128 | 1267/858/480 |
| C_rv_abs vs A | 2.763598178916185 | -0.8255528770169275 | 39.77353016009128 | 1267/858/480 |
| D_rv_signed_abs vs A | 2.7635981789493456 | -0.8255528769369784 | 39.77353016399939 | 1267/858/480 |
| E_rv_funding_trails vs A | 7.225674132254077 | 1.6403717666397328 | -0.1451845857541486 | 1091/343/385 |

## Exploratory Sensitivity (NOT confirmatory; do not promote if unstable)
> Block-bootstrap block size sensitivity for paired ΔQLIKE vs A. Pre-registered primary remains block=24h, seed=12345, reps=2000.
| Contrast | block=12h CI | block=24h CI (primary) | block=48h CI |
|---|---|---|---|
| B_rv_signed vs A | [0.031670973142356305, 24.113780756853075] (pt=8.400940115566256) | [-0.12384387819379696, 24.209835591605284] (pt=8.400940115566256) | [-0.43468610877959035, 24.013335755908027] (pt=8.400940115566256) |
| C_rv_abs vs A | [0.031670973142356305, 24.113780756853075] (pt=8.400940115566256) | [-0.12384387819379696, 24.209835591605284] (pt=8.400940115566256) | [-0.43468610877959035, 24.013335755908027] (pt=8.400940115566256) |
| D_rv_signed_abs vs A | [0.0316709732001089, 24.113780759314004] (pt=8.40094011632883) | [-0.12384387813694987, 24.209835594169473] (pt=8.40094011632883) | [-0.43468610877488, 24.01333575822119] (pt=8.40094011632883) |
| E_rv_funding_trails vs A | [-0.09514734553286228, 13.357421456243788] (pt=4.612403479236548) | [-0.1288482496006673, 13.122435403144543] (pt=4.612403479236548) | [-0.11736393726757173, 12.70339880368411] (pt=4.612403479236548) |

## Per-Split Details
- Split 0: train ('2024-01-01T00:00:00+00:00', '2024-01-28T23:59:59+00:00') | test ('2024-02-05T00:00:00+00:00', '2024-02-18T23:59:59+00:00') | purge/embargo=7d | n_train=2688 n_test=1344
  - A_rv_only: qlike=0.6883380538890281, mae=0.0008245528915028976, rmse=0.0009221269311027606, n_feat=3, valid_n=1344
  - B_rv_signed: qlike=3.2430660310459682, mae=0.0009131619934817241, rmse=0.001049343122924403, n_feat=4, valid_n=1267
  - C_rv_abs: qlike=3.2430660310459682, mae=0.0009131619934817241, rmse=0.001049343122924403, n_feat=4, valid_n=1267
  - D_rv_signed_abs: qlike=3.2430660310791284, mae=0.0009131619934817306, rmse=0.0010493431229244155, n_feat=5, valid_n=1267
  - E_rv_funding_trails: qlike=7.908036493435277, mae=0.0016748163359833687, rmse=0.0029411807736853565, n_feat=11, valid_n=1091
- Split 1: train ('2024-01-15T00:00:00+00:00', '2024-02-11T23:59:59+00:00') | test ('2024-02-19T00:00:00+00:00', '2024-03-03T23:59:59+00:00') | purge/embargo=7d | n_train=2688 n_test=1344
  - A_rv_only: qlike=2.583368890233034, mae=0.0011163836239120016, rmse=0.0016972839145703964, n_feat=3, valid_n=1139
  - B_rv_signed: qlike=2.102867852631954, mae=0.0013002584302867618, rmse=0.0020938464960688456, n_feat=4, valid_n=1059
  - C_rv_abs: qlike=2.102867852631954, mae=0.0013002584302867618, rmse=0.0020938464960688456, n_feat=4, valid_n=1059
  - D_rv_signed_abs: qlike=2.1028678526966598, mae=0.001300258430286844, rmse=0.002093846496068907, n_feat=5, valid_n=1059
  - E_rv_funding_trails: qlike=3.8525439486119373, mae=0.0014289206635841527, rmse=0.002208061259587419, n_feat=11, valid_n=374
- Split 2: train ('2024-01-29T00:00:00+00:00', '2024-02-25T23:59:59+00:00') | test ('2024-03-04T00:00:00+00:00', '2024-03-17T23:59:59+00:00') | purge/embargo=7d | n_train=2688 n_test=1344
  - A_rv_only: qlike=19.118058564787432, mae=0.002784800944118029, rmse=0.0042179412126903985, n_feat=3, valid_n=558
  - B_rv_signed: qlike=45.617748686069895, mae=0.0028180970405037686, rmse=0.004212319869303446, n_feat=4, valid_n=506
  - C_rv_abs: qlike=45.617748686069895, mae=0.0028180970405037686, rmse=0.004212319869303446, n_feat=4, valid_n=506
  - D_rv_signed_abs: qlike=45.6177486896359, mae=0.002818097040503775, rmse=0.004212319869303448, n_feat=5, valid_n=506
  - E_rv_funding_trails: qlike=4.870242765047645, mae=0.0029622701153033167, rmse=0.004305081529184471, n_feat=11, valid_n=418

## Bootstrap (pre-registered)
- Paired ΔQLIKE (alt-base; negative = better for QLIKE) with circular block bootstrap on whole UTC time blocks, jointly across instruments.
- seed=12345, reps=2000, block_hours=24, alpha=0.05, two-sided percentile CI.

## Leakage/Alignment Notes
- Funding (8h) aligned to 1h via last-known value at/before each hour (ffill). NaN if missing.
- Trailing funding pct/z computed over rolling windows on aligned series (past-only).
- Chronological splits, 7d purge/embargo, train-only normalization per split.
- Basis/premium not included (no aligned admissible local series verified); missing treated as NaN per policy.

## Caveats (non-negotiable)
- **Verdict:** PILOT/INCONCLUSIVE (data-sufficiency criteria not met; no claim-worthy inference)
- **Data sufficiency:** instruments=4 (NOT MET; required >=5); ok_30day_splits=0 (required>=3) => meets_claim_worthy_data_sufficiency=False.
- **No economic value claim, no overlay, no Track A linkage.** Observed metrics are out-of-sample forecast evidence under pre-registered design; instability across splits/instrument sets must be reported honestly.
- If any leakage/alignment doubt exists, treat as non-confirmatory.
