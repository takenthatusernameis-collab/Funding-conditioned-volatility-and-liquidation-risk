# Evaluation Summary - Funding Ablations (Gate 4, multi-split pilot)

**Generated:** 2026-11-07T03:29:01Z
**Git SHA:** ff3476d62c37ea88356dda8aec8dec455acaec45
**Pre-registration:** `research_state/pre_registration_gate4_funding_multisplit_v2_5sym_20261107T032439Z.md` (frozen before outcomes)
**Scope:** BTCUSDT, ETHUSDT, SOLUSDT, XRPUSDT, BNBUSDT, 2024-01-01 to 2024-03-31, 24h forward RV, 3 pre-registered walk-forward splits
**Model:** direct-variance OLS HAR (target = forward realized VARIANCE; train-only normalization per split; no log/exp transform)
**Verdict:** **PILOT/INCONCLUSIVE (data-sufficiency criteria not met; no claim-worthy inference)**

## Data Sufficiency (honest)
- instruments=5 (required >=5): MET
- claim-worthy: False
- shortfall: no_30day_non_overlapping_test_blocks (pre-reg uses 14-day windows; Q1 2024 local data insufficient for >=3 x 30-day)
- shortfall: q1_2024_only_local_data

## Aggregate (mean across OK splits)
| Ablation | QLIKE | MAE | RMSE | ΔQLIKE vs A (pooled paired) | 95% block-bootstrap CI | n_obs/n_blocks |
|---|---|---|---|---|---|---|
| A_rv_only | 5.803459241308542 | 0.0015476623369448418 | 0.002193820812879932 | — | — | — |
| B_rv_signed | 2.555662519851302 | 0.0018372928671238978 | 0.0027867642164398506 | -3.612970687166556 | [-8.3592449399975, -0.5741679858769428] | 3740/42 |
| C_rv_abs | 17.1533038908623 | 0.001670581976203579 | 0.002387632427975753 | -1.0069368263879108 | [-2.9312299631824406, 0.32131520531886587] | 2838/42 |
| D_rv_signed_abs | 13.181698445411909 | 0.0013900489678615867 | 0.0022405850586437142 | -1.836905919269446 | [-3.8751409395276157, -0.18230594904579703] | 3334/42 |
| E_rv_funding_trails | 5.78538142648025 | 0.0017395959151952668 | 0.0031356718246800183 | -1.6489202390149797 | [-3.9918278213500464, 0.30332204461053297] | 2920/42 |

## Per-Split Paired ΔQLIKE vs A (instability visibility)
| Contrast | Split 0 | Split 1 | Split 2 | n_obs (0/1/2) |
|---|---:|---:|---:|---|
| B_rv_signed vs A | -0.09334819149262734 | -8.10745714593373 | -3.0735782366253237 | 1676/1393/671 |
| C_rv_abs vs A | 0.7631801936874046 | -4.956969291572084 | -1.6549298069211646 | 1629/636/573 |
| D_rv_signed_abs vs A | -0.2934188607191063 | -3.840328332943686 | -2.6161504346630307 | 1664/1035/635 |
| E_rv_funding_trails vs A | 0.1812727189915471 | -3.6027369611810673 | -3.347491072915515 | 1465/822/633 |

## Exploratory Sensitivity (NOT confirmatory; do not promote if unstable)
> Block-bootstrap block size sensitivity for paired ΔQLIKE vs A. Pre-registered primary remains block=24h, seed=12345, reps=2000.
| Contrast | block=12h CI | block=24h CI (primary) | block=48h CI |
|---|---|---|---|
| B_rv_signed vs A | [-7.323234619374838, -0.9127789109979318] (pt=-3.612970687166556) | [-8.3592449399975, -0.5741679858769428] (pt=-3.612970687166556) | [-8.737291477548604, -0.38087293819917456] (pt=-3.612970687166556) |
| C_rv_abs vs A | [-2.8757177684382724, 0.25956011449551175] (pt=-1.0069368263879108) | [-2.9312299631824406, 0.32131520531886587] (pt=-1.0069368263879108) | [-3.203044103396538, 0.41003325685913533] (pt=-1.0069368263879108) |
| D_rv_signed_abs vs A | [-3.635746261676863, -0.4546287683218925] (pt=-1.836905919269446) | [-3.8751409395276157, -0.18230594904579703] (pt=-1.836905919269446) | [-4.119482557484368, -0.10380119603380476] (pt=-1.836905919269446) |
| E_rv_funding_trails vs A | [-3.8495068645188666, 0.038849308388191665] (pt=-1.6489202390149797) | [-3.9918278213500464, 0.30332204461053297] (pt=-1.6489202390149797) | [-4.321445776769727, 0.47278075528159563] (pt=-1.6489202390149797) |

## Per-Split Details
- Split 0: train ('2024-01-01T00:00:00+00:00', '2024-01-28T23:59:59+00:00') | test ('2024-02-05T00:00:00+00:00', '2024-02-18T23:59:59+00:00') | purge/embargo=7d | n_train=3360 n_test=1680
  - A_rv_only: qlike=0.5681709135016833, mae=0.0008201025957951973, rmse=0.0009193618781201634, n_feat=3, valid_n=1680
  - B_rv_signed: qlike=0.46919716407591694, mae=0.0007237660874617642, rmse=0.0009021092609663269, n_feat=4, valid_n=1676
  - C_rv_abs: qlike=1.2760644590625874, mae=0.0009059345197376927, rmse=0.0010202215607098592, n_feat=4, valid_n=1629
  - D_rv_signed_abs: qlike=0.2720178036908581, mae=0.000524948125256614, rmse=0.0007633328508814865, n_feat=5, valid_n=1664
  - E_rv_funding_trails: qlike=0.7395698618485672, mae=0.0015227563520679803, rmse=0.0034738676519242844, n_feat=11, valid_n=1465
- Split 1: train ('2024-01-15T00:00:00+00:00', '2024-02-11T23:59:59+00:00') | test ('2024-02-19T00:00:00+00:00', '2024-03-03T23:59:59+00:00') | purge/embargo=7d | n_train=3360 n_test=1680
  - A_rv_only: qlike=9.168852899764632, mae=0.001014938845139822, rmse=0.001557611847137627, n_feat=3, valid_n=1468
  - B_rv_signed: qlike=1.3603924331119952, mae=0.002144671673752494, rmse=0.0036050060209781086, n_feat=4, valid_n=1605
  - C_rv_abs: qlike=1.50953172077206, mae=0.0012569873229138022, rmse=0.0020167046850794053, n_feat=4, valid_n=639
  - D_rv_signed_abs: qlike=2.3010361711208436, mae=0.0011009140339018801, rmse=0.0018940797371413075, n_feat=5, valid_n=1103
  - E_rv_funding_trails: qlike=5.320762912859348, mae=0.001182944117911432, rmse=0.0019645956083874524, n_feat=11, valid_n=893
- Split 2: train ('2024-01-29T00:00:00+00:00', '2024-02-25T23:59:59+00:00') | test ('2024-03-04T00:00:00+00:00', '2024-03-17T23:59:59+00:00') | purge/embargo=7d | n_train=3360 n_test=1680
  - A_rv_only: qlike=7.673353910659311, mae=0.002807945569899506, rmse=0.004104488713382006, n_feat=3, valid_n=710
  - B_rv_signed: qlike=5.837397962365994, mae=0.0026434408401574353, rmse=0.003853177367375116, n_feat=4, valid_n=1106
  - C_rv_abs: qlike=48.67431549275226, mae=0.0028488240859592426, rmse=0.0041259710381379945, n_feat=4, valid_n=611
  - D_rv_signed_abs: qlike=36.972041361424026, mae=0.002544284744426266, rmse=0.004064342587908349, n_feat=5, valid_n=1343
  - E_rv_funding_trails: qlike=11.295811504732837, mae=0.002513087275606388, rmse=0.003968552213728319, n_feat=11, valid_n=1098

## Bootstrap (pre-registered)
- Paired ΔQLIKE (alt-base; negative = better for QLIKE) with circular block bootstrap on whole UTC time blocks, jointly across instruments.
- seed=12345, reps=2000, block_hours=24, alpha=0.05, two-sided percentile CI.

## Leakage/Alignment Notes
- Funding (8h) aligned to 1h via last-known value at/before each hour (ffill). NaN if missing.
- Trailing funding pct/z computed over rolling windows on aligned series (past-only).
- Chronological splits, 7d purge/embargo, train-only normalization per split.
- Basis/premium not included (no aligned admissible local series verified); missing treated as NaN per policy.

## Caveats (non-negotiable)
- **Pilot/inconclusive (v2, 5 symbols):** instruments=5 MET for pilot set, but Q1-2024-only local data and 14-day test windows still do NOT satisfy claim-worthy criteria (>=3 non-overlapping 30-day blocks, robust uncertainty under sufficient data coverage). No 30-day block criterion met.
- **Do NOT promote to confirmatory, do NOT claim economic value, do NOT build any overlay.** Point estimates/CIs are pilot evidence only.
- Direction/magnitude can change with more data, more splits, and claim-worthy instrument/block coverage.
