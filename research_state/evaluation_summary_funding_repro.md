# Evaluation Summary - Funding Ablations (Gate 4, multi-split pilot)

**Generated:** 2026-11-07T10:20:41Z
**Git SHA:** c1696f3fbf77fdf52053048eca8dd3a2f1518453
**Pre-registration:** `research_state/pre_registration_gate4_funding_multisplit_v3_30d_20261107T033500Z.md` (frozen before outcomes)
**Scope:** BTCUSDT, ETHUSDT, SOLUSDT, XRPUSDT, BNBUSDT, 2024-04-01 to 2024-09-30, 24h forward RV, 4 pre-registered walk-forward splits
**Model:** direct-variance OLS HAR (target = forward realized VARIANCE; train-only normalization per split; no log/exp transform)
**Verdict:** **DATA-SUFFICIENT PILOT / INCONCLUSIVE ON PRIMARY CONTRAST (pre-registered 30-day blocks met; E vs A CI spans 0; no improvement claim)**

## Data Sufficiency (honest)
- instruments=5 (required >=5): MET
- claim-worthy: True

## Aggregate (mean across OK splits)
| Ablation | QLIKE | MAE | RMSE | ΔQLIKE vs A (pooled paired) | 95% block-bootstrap CI | n_obs/n_blocks |
|---|---|---|---|---|---|---|
| A_rv_only | 0.798319018412711 | 0.0010925475062619158 | 0.0018204745158497855 | — | — | — |
| B_rv_signed | 12.183624184348375 | 0.0010651273940529746 | 0.0018516401463693957 | 11.110522838842066 | [0.4805228898986025, 32.31258288091912] | 13620/120 |
| C_rv_abs | 0.845961941013358 | 0.0010629048565582034 | 0.0018097508718590376 | -0.024710146016338065 | [-0.37159501419674296, 0.2707987870777943] | 13985/120 |
| D_rv_signed_abs | 3.4492894649959656 | 0.0010503733522264976 | 0.0018152243676412922 | 2.4219181148773314 | [-0.25396005567122193, 7.512202577246805] | 13269/120 |
| E_rv_funding_trails | 1.2417017959574312 | 0.001141390937488439 | 0.0020142809604019665 | 0.4879023125556385 | [-0.042160777324701186, 1.1973379300276015] | 12969/120 |

## Per-Split Paired ΔQLIKE vs A (instability visibility)
| Contrast | Split 0 | Split 1 | Split 2 | Split 3 | n_obs (0/1/2/3) |
|---|---:|---:|---:|---:|---|
| B_rv_signed vs A | -0.0611067427946213 | 0.25349446480150833 | 1.1548593949123356 | 44.687585178640056 | 3600/3508/3224/3288 |
| C_rv_abs vs A | 0.17994478420129137 | 0.47175737511369054 | -0.13235454649685044 | -0.6223803025083052 | 3600/3534/3272/3579 |
| D_rv_signed_abs vs A | -0.1501294535233037 | 0.34341450202666923 | 0.11962413470120653 | 10.334492155369691 | 3600/3502/3158/3009 |
| E_rv_funding_trails vs A | 0.038332194318099165 | 0.30916469880287895 | 1.0915632305039822 | 0.5675604567126445 | 3417/3422/3167/2963 |

## Exploratory Sensitivity (NOT confirmatory; do not promote if unstable)
> Block-bootstrap block size sensitivity for paired ΔQLIKE vs A. Pre-registered primary remains block=24h, seed=12345, reps=2000.
| Contrast | block=12h CI | block=24h CI (primary) | block=48h CI |
|---|---|---|---|
| B_rv_signed vs A | [0.5266085816588382, 32.18840374035179] (pt=11.110522838842066) | [0.4805228898986025, 32.31258288091912] (pt=11.110522838842066) | [0.40586566533404206, 32.605080409251165] (pt=11.110522838842066) |
| C_rv_abs vs A | [-0.3605794889360364, 0.22571589591222574] (pt=-0.024710146016338065) | [-0.37159501419674296, 0.2707987870777943] (pt=-0.024710146016338065) | [-0.40088615334780414, 0.33608036349812537] (pt=-0.024710146016338065) |
| D_rv_signed_abs vs A | [-0.2355623445423137, 7.487533316310916] (pt=2.4219181148773314) | [-0.25396005567122193, 7.512202577246805] (pt=2.4219181148773314) | [-0.2546603803841484, 7.5043807399390925] (pt=2.4219181148773314) |
| E_rv_funding_trails vs A | [-0.0609984682010953, 1.193706385672306] (pt=0.4879023125556385) | [-0.042160777324701186, 1.1973379300276015] (pt=0.4879023125556385) | [-0.05761650233457378, 1.1925841627481637] (pt=0.4879023125556385) |

## Per-Split Details
- Split 0: train ('2024-04-01T00:00:00+00:00', '2024-05-07T23:59:59+00:00') | test ('2024-05-15T00:00:00+00:00', '2024-06-13T23:59:59+00:00') | purge/embargo=7d | n_train=4440 n_test=3600
  - A_rv_only: qlike=0.8626811370032491, mae=0.0012746358204607643, rmse=0.0015144217419927773, n_feat=3, valid_n=3600
  - B_rv_signed: qlike=0.8015743942086277, mae=0.0011996210577740172, rmse=0.0015147445307605908, n_feat=4, valid_n=3600
  - C_rv_abs: qlike=1.0426259212045406, mae=0.0011491246857054118, rmse=0.0014248825564873993, n_feat=4, valid_n=3600
  - D_rv_signed_abs: qlike=0.7125516834799456, mae=0.0011395718194704932, rmse=0.0014748793200375068, n_feat=5, valid_n=3600
  - E_rv_funding_trails: qlike=0.907620575628453, mae=0.0014190130539747782, rmse=0.0020762664831524935, n_feat=11, valid_n=3417
- Split 1: train ('2024-04-01T00:00:00+00:00', '2024-06-06T23:59:59+00:00') | test ('2024-06-14T00:00:00+00:00', '2024-07-13T23:59:59+00:00') | purge/embargo=7d | n_train=8040 n_test=3600
  - A_rv_only: qlike=0.5659745411011408, mae=0.0009511824412033422, rmse=0.001400211363165027, n_feat=3, valid_n=3534
  - B_rv_signed: qlike=0.8234824385538339, mae=0.0009049818039712993, rmse=0.0013974288794576545, n_feat=4, valid_n=3508
  - C_rv_abs: qlike=1.0377319162148315, mae=0.0009415837676613192, rmse=0.001413867909140677, n_feat=4, valid_n=3534
  - D_rv_signed_abs: qlike=0.910735124647827, mae=0.0008821210619056322, rmse=0.0013529741673883845, n_feat=5, valid_n=3502
  - E_rv_funding_trails: qlike=0.8440924294298177, mae=0.0009571337453320313, rmse=0.001501499868756022, n_feat=11, valid_n=3422
- Split 2: train ('2024-04-01T00:00:00+00:00', '2024-07-06T23:59:59+00:00') | test ('2024-07-14T00:00:00+00:00', '2024-08-12T23:59:59+00:00') | purge/embargo=7d | n_train=11640 n_test=3600
  - A_rv_only: qlike=0.7899274264265382, mae=0.0015537095817841626, rmse=0.003593433026539679, n_feat=3, valid_n=3274
  - B_rv_signed: qlike=2.109066706258703, mae=0.001563743920733972, rmse=0.0036666937168248408, n_feat=4, valid_n=3252
  - C_rv_abs: qlike=0.9182121380528623, mae=0.0015398158495958682, rmse=0.003592423058526187, n_feat=4, valid_n=3302
  - D_rv_signed_abs: qlike=0.8885053521462617, mae=0.0014997875132487654, rmse=0.0035673006620722736, n_feat=5, valid_n=3329
  - E_rv_funding_trails: qlike=1.713050622842332, mae=0.0015181393696574353, rmse=0.0035906090639651763, n_feat=11, valid_n=3338
- Split 3: train ('2024-04-01T00:00:00+00:00', '2024-08-05T23:59:59+00:00') | test ('2024-08-13T00:00:00+00:00', '2024-09-11T23:59:59+00:00') | purge/embargo=7d | n_train=15240 n_test=3600
  - A_rv_only: qlike=0.9746929691199161, mae=0.0005906621815993942, rmse=0.0007738319317016594, n_feat=3, valid_n=3579
  - B_rv_signed: qlike=45.00037319837234, mae=0.0005921627937326104, rmse=0.0008276934584344959, n_feat=4, valid_n=3288
  - C_rv_abs: qlike=0.3852777885811977, mae=0.0006210951232702147, rmse=0.0008078299632818869, n_feat=4, valid_n=3594
  - D_rv_signed_abs: qlike=11.285365699709828, mae=0.0006800130142810995, rmse=0.0008657433210670043, n_feat=5, valid_n=3024
  - E_rv_funding_trails: qlike=1.5020435559291225, mae=0.0006712775809895116, rmse=0.0008887484257341734, n_feat=11, valid_n=2978

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
