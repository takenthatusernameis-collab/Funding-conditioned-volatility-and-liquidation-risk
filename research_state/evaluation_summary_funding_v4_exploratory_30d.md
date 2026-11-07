# Evaluation Summary - Funding Ablations (Gate 4, multi-split pilot)

**Generated:** 2026-11-07T20:54:37Z
**Git SHA:** 37f2dc8ca8397da688cfec0d7bf83a3e9de06c53
**Pre-registration:** `research_state/pre_registration_gate4_funding_multisplit_v4_20261107T1845Z.md` (frozen before outcomes)
**Scope:** BTCUSDT, ETHUSDT, SOLUSDT, XRPUSDT, BNBUSDT, 2024-04-01 to 2024-09-30, 24h forward RV, 4 pre-registered walk-forward splits
**Model:** direct-variance OLS HAR (target = forward realized VARIANCE; train-only normalization per split; no log/exp transform)
**Verdict:** **DATA-SUFFICIENT PILOT / INCONCLUSIVE ON PRIMARY CONTRAST (pre-registered 30-day blocks met; E vs A CI spans 0; no improvement claim)**

## Data Sufficiency (honest)
- instruments=5 (required >=5): MET
- claim-worthy: True

## Aggregate (mean across OK splits)
| Ablation | QLIKE | MAE | RMSE | ΔQLIKE vs A (pooled paired) | 95% block-bootstrap CI | n_obs/n_blocks |
|---|---|---|---|---|---|---|
| A_rv_only | 0.7983190184126631 | 0.0010925475062619158 | 0.0018204745158497855 | — | — | — |
| B_rv_signed | 12.183624182224962 | 0.0010651273940529746 | 0.0018516401463693957 | 11.110522836791604 | [0.48052288989834724, 32.31258287470994] | 13620/120 |
| C_rv_abs | 0.8459619410133684 | 0.0010629048565582036 | 0.0018097508718590374 | -0.024710146016296737 | [-0.37159501419659596, 0.2707987870777838] | 13985/120 |
| D_rv_signed_abs | 3.4492894624624917 | 0.0010503733522264959 | 0.0018152243676412916 | 2.421918112567877 | [-0.2539600556711275, 7.512202570277498] | 13269/120 |
| E_rv_funding_trails | 1.241701795957689 | 0.0011413909374884345 | 0.0020142809604019557 | 0.48790231255595967 | [-0.04216077732537772, 1.1973379300280491] | 12969/120 |

## Per-Split Paired ΔQLIKE vs A (instability visibility)
| Contrast | Split 0 | Split 1 | Split 2 | Split 3 | n_obs (0/1/2/3) |
|---|---:|---:|---:|---:|---|
| B_rv_signed vs A | -0.061106742794619445 | 0.2534944648015296 | 1.1548593949122556 | 44.687585170146406 | 3600/3508/3224/3288 |
| C_rv_abs vs A | 0.17994478420127102 | 0.4717573751136753 | -0.1323545464968529 | -0.622380302508106 | 3600/3534/3272/3579 |
| D_rv_signed_abs vs A | -0.15012945352330412 | 0.3434145020268775 | 0.11962413470115817 | 10.334492145185333 | 3600/3502/3158/3009 |
| E_rv_funding_trails vs A | 0.03833219431819898 | 0.30916469880312913 | 1.0915632305047063 | 0.5675604567128726 | 3417/3422/3167/2963 |

## Exploratory Sensitivity (NOT confirmatory; do not promote if unstable)
> Block-bootstrap block size sensitivity for paired ΔQLIKE vs A. Pre-registered primary remains block=24h, seed=12345, reps=2000.
| Contrast | block=12h CI | block=24h CI (primary) | block=48h CI |
|---|---|---|---|
| B_rv_signed vs A | [0.5266085816589288, 32.188403734167316] (pt=11.110522836791604) | [0.48052288989834724, 32.31258287470994] (pt=11.110522836791604) | [0.40586566533389123, 32.60508040300046] (pt=11.110522836791604) |
| C_rv_abs vs A | [-0.3605794889358921, 0.22571589591221194] (pt=-0.024710146016296737) | [-0.37159501419659596, 0.2707987870777838] (pt=-0.024710146016296737) | [-0.4008861533477015, 0.3360803634981003] (pt=-0.024710146016296737) |
| D_rv_signed_abs vs A | [-0.23556234454215058, 7.487533309366848] (pt=2.421918112567877) | [-0.2539600556711275, 7.512202570277498] (pt=2.421918112567877) | [-0.25466038038354727, 7.504380732871568] (pt=2.421918112567877) |
| E_rv_funding_trails vs A | [-0.060998468201006344, 1.1937063856735863] (pt=0.48790231255595967) | [-0.04216077732537772, 1.1973379300280491] (pt=0.48790231255595967) | [-0.057616502333888174, 1.1925841627453069] (pt=0.48790231255595967) |

## Per-Split Details
- Split 0: train ('2024-04-01T00:00:00+00:00', '2024-05-07T23:59:59+00:00') | test ('2024-05-15T00:00:00+00:00', '2024-06-13T23:59:59+00:00') | purge/embargo=7d | n_train=4440 n_test=3600
  - A_rv_only: qlike=0.8626811370032509, mae=0.001274635820460764, rmse=0.001514421741992777, n_feat=3, valid_n=3600
  - B_rv_signed: qlike=0.8015743942086314, mae=0.0011996210577740172, rmse=0.001514744530760591, n_feat=4, valid_n=3600
  - C_rv_abs: qlike=1.0426259212045217, mae=0.001149124685705412, rmse=0.0014248825564873993, n_feat=4, valid_n=3600
  - D_rv_signed_abs: qlike=0.7125516834799468, mae=0.0011395718194704885, rmse=0.0014748793200375031, n_feat=5, valid_n=3600
  - E_rv_funding_trails: qlike=0.9076205756285542, mae=0.001419013053974758, rmse=0.002076266483152447, n_feat=11, valid_n=3417
- Split 1: train ('2024-04-01T00:00:00+00:00', '2024-06-06T23:59:59+00:00') | test ('2024-06-14T00:00:00+00:00', '2024-07-13T23:59:59+00:00') | purge/embargo=7d | n_train=8040 n_test=3600
  - A_rv_only: qlike=0.5659745411011431, mae=0.0009511824412033422, rmse=0.001400211363165027, n_feat=3, valid_n=3534
  - B_rv_signed: qlike=0.8234824385538575, mae=0.0009049818039712994, rmse=0.0013974288794576547, n_feat=4, valid_n=3508
  - C_rv_abs: qlike=1.0377319162148184, mae=0.0009415837676613193, rmse=0.001413867909140677, n_feat=4, valid_n=3534
  - D_rv_signed_abs: qlike=0.9107351246480376, mae=0.000882121061905631, rmse=0.0013529741673883847, n_feat=5, valid_n=3502
  - E_rv_funding_trails: qlike=0.8440924294300697, mae=0.0009571337453320289, rmse=0.00150149986875602, n_feat=11, valid_n=3422
- Split 2: train ('2024-04-01T00:00:00+00:00', '2024-07-06T23:59:59+00:00') | test ('2024-07-14T00:00:00+00:00', '2024-08-12T23:59:59+00:00') | purge/embargo=7d | n_train=11640 n_test=3600
  - A_rv_only: qlike=0.7899274264265418, mae=0.0015537095817841624, rmse=0.0035934330265396785, n_feat=3, valid_n=3274
  - B_rv_signed: qlike=2.1090667062586594, mae=0.0015637439207339715, rmse=0.0036666937168248403, n_feat=4, valid_n=3252
  - C_rv_abs: qlike=0.9182121380529361, mae=0.001539815849595868, rmse=0.0035924230585261865, n_feat=4, valid_n=3302
  - D_rv_signed_abs: qlike=0.8885053521462225, mae=0.0014997875132487651, rmse=0.003567300662072274, n_feat=5, valid_n=3329
  - E_rv_funding_trails: qlike=1.713050622843014, mae=0.001518139369657435, rmse=0.0035906090639651767, n_feat=11, valid_n=3338
- Split 3: train ('2024-04-01T00:00:00+00:00', '2024-08-05T23:59:59+00:00') | test ('2024-08-13T00:00:00+00:00', '2024-09-11T23:59:59+00:00') | purge/embargo=7d | n_train=15240 n_test=3600
  - A_rv_only: qlike=0.9746929691197167, mae=0.0005906621815993943, rmse=0.0007738319317016595, n_feat=3, valid_n=3579
  - B_rv_signed: qlike=45.0003731898787, mae=0.0005921627937326104, rmse=0.0008276934584344959, n_feat=4, valid_n=3288
  - C_rv_abs: qlike=0.38527778858119693, mae=0.0006210951232702149, rmse=0.0008078299632818871, n_feat=4, valid_n=3594
  - D_rv_signed_abs: qlike=11.285365689575759, mae=0.0006800130142810992, rmse=0.0008657433210670041, n_feat=5, valid_n=3024
  - E_rv_funding_trails: qlike=1.502043555929118, mae=0.0006712775809895154, rmse=0.000888748425734179, n_feat=11, valid_n=2978

## Bootstrap (pre-registered)
- Paired ΔQLIKE (alt-base; negative = better for QLIKE) with circular block bootstrap on whole UTC time blocks, jointly across instruments.
- seed=12345, reps=2000, block_hours=24, alpha=0.05, two-sided percentile CI.

## Leakage/Alignment Notes
- Funding (8h) aligned to 1h via last-known value at/before each hour (ffill). NaN if missing.
- Trailing funding pct/z computed over rolling windows on aligned series (past-only).
- Chronological splits, 7d purge/embargo, train-only normalization per split.
- Basis/premium not included (no aligned admissible local series verified); missing treated as NaN per policy.

## Caveats (non-negotiable)
- **Verdict:** DATA-SUFFICIENT PILOT / INCONCLUSIVE ON PRIMARY CONTRAST (pre-registered 30-day blocks met; E vs A CI spans 0; no improvement claim)
- **Data sufficiency:** instruments=5 (MET); ok_30day_splits=4 (required>=3) => meets_claim_worthy_data_sufficiency=True.
- **No economic value claim, no overlay, no Track A linkage.** Observed metrics are out-of-sample forecast evidence under pre-registered design; instability across splits/instrument sets must be reported honestly.
- If any leakage/alignment doubt exists, treat as non-confirmatory.
