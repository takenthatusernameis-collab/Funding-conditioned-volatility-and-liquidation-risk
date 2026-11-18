# Evaluation Summary - Funding Ablations (Gate 4, multi-split pilot)

**Generated:** 2026-11-18T04:04:37Z
**Git SHA:** ee75747a58d6fd323219dfd3a8d4de96ca690081
**Pre-registration:** `research_state/session_20261118T030427Z/trackc_extension_design_20261118T030427Z.json` (frozen before outcomes)
**Scope:** BTCUSDT, ETHUSDT, BNBUSDT, SOLUSDT, XRPUSDT, 2024-04-01 to 2024-09-30, 24h forward RV, 4 pre-registered walk-forward splits
**Model:** direct-variance OLS HAR (target = forward realized VARIANCE; train-only normalization per split; no log/exp transform)
**Verdict:** **DATA-SUFFICIENT PILOT / INCONCLUSIVE ON PRIMARY CONTRAST (pre-registered 30-day blocks met; E vs A CI spans 0; no improvement claim)**

## Data Sufficiency (honest)
- instruments=5 (required >=5): MET
- claim-worthy: True

## Aggregate (mean across OK splits)
| Ablation | QLIKE | MAE | RMSE | ΔQLIKE vs A (pooled paired) | 95% block-bootstrap CI | n_obs/n_blocks |
|---|---|---|---|---|---|---|
| A_rv_only | 0.7983190184128208 | 0.001092547506261916 | 0.001820474515849786 | — | — | — |
| B_rv_signed | 12.183624174308331 | 0.0010651273940529746 | 0.0018516401463693946 | 11.110522829146998 | [0.4805228898957609, 32.3125828515638] | 13620/120 |
| C_rv_abs | 0.8459619410133365 | 0.0010629048565582034 | 0.0018097508718590376 | -0.024710146016497722 | [-0.37159501419708163, 0.27079878707767846] | 13985/120 |
| D_rv_signed_abs | 3.449289460975088 | 0.001050373352226502 | 0.0018152243676412955 | 2.4219181112117916 | [-0.25396005567146496, 7.5122025661868825] | 13269/120 |
| E_rv_funding_trails | 1.2417017959530712 | 0.0011413909374884416 | 0.0020142809604019674 | 0.48790231255149863 | [-0.04216077732786338, 1.197337930020189] | 12969/120 |

## Per-Split Paired ΔQLIKE vs A (instability visibility)
| Contrast | Split 0 | Split 1 | Split 2 | Split 3 | n_obs (0/1/2/3) |
|---|---:|---:|---:|---:|---|
| B_rv_signed vs A | -0.061106742794621895 | 0.25349446480151794 | 1.1548593949118886 | 44.687585138480266 | 3600/3508/3224/3288 |
| C_rv_abs vs A | 0.17994478420132368 | 0.47175737511347055 | -0.13235454649684109 | -0.6223803025087525 | 3600/3534/3272/3579 |
| D_rv_signed_abs vs A | -0.15012945352330515 | 0.3434145020264318 | 0.11962413470124396 | 10.334492139205738 | 3600/3502/3158/3009 |
| E_rv_funding_trails vs A | 0.038332194318153365 | 0.3091646988024407 | 1.091563230503703 | 0.5675604566952663 | 3417/3422/3167/2963 |

## Exploratory Sensitivity (NOT confirmatory; do not promote if unstable)
> Block-bootstrap block size sensitivity for paired ΔQLIKE vs A. Pre-registered primary remains block=24h, seed=12345, reps=2000.
| Contrast | block=12h CI | block=24h CI (primary) | block=48h CI |
|---|---|---|---|
| B_rv_signed vs A | [0.5266085816583637, 32.18840371111218] (pt=11.110522829146998) | [0.4805228898957609, 32.3125828515638] (pt=11.110522829146998) | [0.4058656653327767, 32.60508037969851] (pt=11.110522829146998) |
| C_rv_abs vs A | [-0.36057948893636405, 0.2257158959121775] (pt=-0.024710146016497722) | [-0.37159501419708163, 0.27079878707767846] (pt=-0.024710146016497722) | [-0.40088615334803396, 0.33608036349810444] (pt=-0.024710146016497722) |
| D_rv_signed_abs vs A | [-0.2355623445428459, 7.487533305290891] (pt=2.4219181112117916) | [-0.25396005567146496, 7.5122025661868825] (pt=2.4219181112117916) | [-0.2546603803850073, 7.50438072872261] (pt=2.4219181112117916) |
| E_rv_funding_trails vs A | [-0.060998468201770954, 1.1937063856668433] (pt=0.48790231255149863) | [-0.04216077732786338, 1.197337930020189] (pt=0.48790231255149863) | [-0.057616502335751156, 1.1925841627410696] (pt=0.48790231255149863) |

## Per-Split Details
- Split 0: train ('2024-04-01T00:00:00+00:00', '2024-05-07T23:59:59+00:00') | test ('2024-05-15T00:00:00+00:00', '2024-06-13T23:59:59+00:00') | purge/embargo=7d | n_train=4440 n_test=3600
  - A_rv_only: qlike=0.8626811370032493, mae=0.0012746358204607645, rmse=0.0015144217419927775, n_feat=3, valid_n=3600
  - B_rv_signed: qlike=0.8015743942086275, mae=0.0011996210577740161, rmse=0.00151474453076059, n_feat=4, valid_n=3600
  - C_rv_abs: qlike=1.042625921204573, mae=0.0011491246857054116, rmse=0.001424882556487399, n_feat=4, valid_n=3600
  - D_rv_signed_abs: qlike=0.7125516834799442, mae=0.0011395718194704904, rmse=0.001474879320037505, n_feat=5, valid_n=3600
  - E_rv_funding_trails: qlike=0.9076205756285074, mae=0.0014190130539747745, rmse=0.0020762664831524896, n_feat=11, valid_n=3417
- Split 1: train ('2024-04-01T00:00:00+00:00', '2024-06-06T23:59:59+00:00') | test ('2024-06-14T00:00:00+00:00', '2024-07-13T23:59:59+00:00') | purge/embargo=7d | n_train=8040 n_test=3600
  - A_rv_only: qlike=0.5659745411011408, mae=0.000951182441203342, rmse=0.001400211363165027, n_feat=3, valid_n=3534
  - B_rv_signed: qlike=0.8234824385538435, mae=0.0009049818039712985, rmse=0.0013974288794576545, n_feat=4, valid_n=3508
  - C_rv_abs: qlike=1.0377319162146112, mae=0.0009415837676613198, rmse=0.001413867909140677, n_feat=4, valid_n=3534
  - D_rv_signed_abs: qlike=0.9107351246475898, mae=0.0008821210619056325, rmse=0.0013529741673883847, n_feat=5, valid_n=3502
  - E_rv_funding_trails: qlike=0.8440924294293792, mae=0.0009571337453320328, rmse=0.0015014998687560227, n_feat=11, valid_n=3422
- Split 2: train ('2024-04-01T00:00:00+00:00', '2024-07-06T23:59:59+00:00') | test ('2024-07-14T00:00:00+00:00', '2024-08-12T23:59:59+00:00') | purge/embargo=7d | n_train=11640 n_test=3600
  - A_rv_only: qlike=0.7899274264265308, mae=0.001553709581784163, rmse=0.0035934330265396794, n_feat=3, valid_n=3274
  - B_rv_signed: qlike=2.109066706258309, mae=0.0015637439207339735, rmse=0.0036666937168248408, n_feat=4, valid_n=3252
  - C_rv_abs: qlike=0.9182121380529652, mae=0.001539815849595868, rmse=0.0035924230585261878, n_feat=4, valid_n=3302
  - D_rv_signed_abs: qlike=0.8885053521462463, mae=0.0014997875132487675, rmse=0.0035673006620722744, n_feat=5, valid_n=3329
  - E_rv_funding_trails: qlike=1.713050622842053, mae=0.0015181393696574379, rmse=0.0035906090639651763, n_feat=11, valid_n=3338
- Split 3: train ('2024-04-01T00:00:00+00:00', '2024-08-05T23:59:59+00:00') | test ('2024-08-13T00:00:00+00:00', '2024-09-11T23:59:59+00:00') | purge/embargo=7d | n_train=15240 n_test=3600
  - A_rv_only: qlike=0.9746929691203629, mae=0.0005906621815993943, rmse=0.0007738319317016594, n_feat=3, valid_n=3579
  - B_rv_signed: qlike=45.00037315821255, mae=0.0005921627937326103, rmse=0.0008276934584344938, n_feat=4, valid_n=3288
  - C_rv_abs: qlike=0.385277788581197, mae=0.0006210951232702145, rmse=0.0008078299632818869, n_feat=4, valid_n=3594
  - D_rv_signed_abs: qlike=11.285365683626573, mae=0.0006800130142811173, rmse=0.0008657433210670183, n_feat=5, valid_n=3024
  - E_rv_funding_trails: qlike=1.5020435559123453, mae=0.0006712775809895216, rmse=0.0008887484257341813, n_feat=11, valid_n=2978

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
