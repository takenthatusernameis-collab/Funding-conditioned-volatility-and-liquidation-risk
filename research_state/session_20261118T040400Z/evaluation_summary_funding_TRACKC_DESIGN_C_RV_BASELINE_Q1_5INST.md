# Evaluation Summary - Funding Ablations (Gate 4, multi-split pilot)

**Generated:** 2026-11-18T04:04:56Z
**Git SHA:** ee75747a58d6fd323219dfd3a8d4de96ca690081
**Pre-registration:** `research_state/session_20261118T030427Z/trackc_extension_design_20261118T030427Z.json` (frozen before outcomes)
**Scope:** BTCUSDT, ETHUSDT, BNBUSDT, SOLUSDT, XRPUSDT, 2024-01-01 to 2024-03-31, 24h forward RV, 3 pre-registered walk-forward splits
**Model:** direct-variance OLS HAR (target = forward realized VARIANCE; train-only normalization per split; no log/exp transform)
**Verdict:** **PILOT/INCONCLUSIVE (data-sufficiency criteria not met; no claim-worthy inference)**

## Data Sufficiency (honest)
- instruments=5 (required >=5): MET
- claim-worthy: False
- shortfall: insufficient_30day_non_overlapping_test_blocks (ok_30d=0, required>=3, split_test_days=[14, 14, 14])

## Aggregate (mean across OK splits)
| Ablation | QLIKE | MAE | RMSE | ΔQLIKE vs A (pooled paired) | 95% block-bootstrap CI | n_obs/n_blocks |
|---|---|---|---|---|---|---|
| A_rv_only | 4.625433609263819 | 0.004631235750434722 | 0.006429035789836664 | — | — | — |
| B_rv_signed | 6.718025375768818 | 0.00465749725365644 | 0.006462666949358635 | 3.5695046296207704 | [-0.06268262865020797, 9.50578474788537] | 1361/34 |
| C_rv_abs | 6.718025375768818 | 0.00465749725365644 | 0.006462666949358635 | 3.5695046296207704 | [-0.06268262865020797, 9.50578474788537] | 1361/34 |
| D_rv_signed_abs | 6.718025375771593 | 0.004657497253656714 | 0.006462666949359058 | 3.5695046296250323 | [-0.06268262865088456, 9.505784747897291] | 1361/34 |
| E_rv_funding_trails | 14.083597328731557 | 0.005652535092293794 | 0.0076909971104951865 | -0.7248956182646947 | [-5.6899252020710325, 3.902201053908714] | 1277/33 |

## Per-Split Paired ΔQLIKE vs A (instability visibility)
| Contrast | Split 0 | Split 1 | Split 2 | n_obs (0/1/2) |
|---|---:|---:|---:|---|
| B_rv_signed vs A | 1.6103975340911942 | 7.133040284211373 | -0.017543422305700374 | 605/545/211 |
| C_rv_abs vs A | 1.6103975340911942 | 7.133040284211373 | -0.017543422305700374 | 605/545/211 |
| D_rv_signed_abs vs A | 1.6103975340929604 | 7.133040284220215 | -0.017543422306106185 | 605/545/211 |
| E_rv_funding_trails vs A | 0.39591094650176767 | -5.06603277965565 | 8.57310326157595 | 543/545/189 |

## Exploratory Sensitivity (NOT confirmatory; do not promote if unstable)
> Block-bootstrap block size sensitivity for paired ΔQLIKE vs A. Pre-registered primary remains block=24h, seed=12345, reps=2000.
| Contrast | block=12h CI | block=24h CI (primary) | block=48h CI |
|---|---|---|---|
| B_rv_signed vs A | [0.10185275212766766, 8.388979566525883] (pt=3.5695046296207704) | [-0.06268262865020797, 9.50578474788537] (pt=3.5695046296207704) | [-0.06318796159159461, 9.58123350563814] (pt=3.5695046296207704) |
| C_rv_abs vs A | [0.10185275212766766, 8.388979566525883] (pt=3.5695046296207704) | [-0.06268262865020797, 9.50578474788537] (pt=3.5695046296207704) | [-0.06318796159159461, 9.58123350563814] (pt=3.5695046296207704) |
| D_rv_signed_abs vs A | [0.10185275212738859, 8.388979566536097] (pt=3.5695046296250323) | [-0.06268262865088456, 9.505784747897291] (pt=3.5695046296250323) | [-0.06318796159230358, 9.581233505650506] (pt=3.5695046296250323) |
| E_rv_funding_trails vs A | [-4.629442765618857, 3.2800068713554253] (pt=-0.7248956182646947) | [-5.6899252020710325, 3.902201053908714] (pt=-0.7248956182646947) | [-5.661425856725503, 4.075356338453123] (pt=-0.7248956182646947) |

## Per-Split Details
- Split 0: train ('2024-01-01T00:00:00+00:00', '2024-01-28T23:59:59+00:00') | test ('2024-02-05T00:00:00+00:00', '2024-02-18T23:59:59+00:00') | purge/embargo=7d | n_train=1128 n_test=720
  - A_rv_only: qlike=1.9909523827678255, mae=0.00317006906475701, rmse=0.004111582218611315, n_feat=3, valid_n=608
  - B_rv_signed: qlike=2.4201715873103455, mae=0.003161490567381363, rmse=0.00407514611857067, n_feat=4, valid_n=677
  - C_rv_abs: qlike=2.4201715873103455, mae=0.003161490567381363, rmse=0.00407514611857067, n_feat=4, valid_n=677
  - D_rv_signed_abs: qlike=2.4201715873102354, mae=0.0031614905673814798, rmse=0.004075146118570424, n_feat=5, valid_n=677
  - E_rv_funding_trails: qlike=1.1955878018495358, mae=0.006144749471710704, rmse=0.007804837904864396, n_feat=11, valid_n=615
- Split 1: train ('2024-01-15T00:00:00+00:00', '2024-02-11T23:59:59+00:00') | test ('2024-02-19T00:00:00+00:00', '2024-03-03T23:59:59+00:00') | purge/embargo=7d | n_train=1128 n_test=624
  - A_rv_only: qlike=8.593195566957347, mae=0.003741471849975141, rmse=0.00658577109992757, n_feat=3, valid_n=545
  - B_rv_signed: qlike=15.72623585116872, mae=0.003852010740654159, rmse=0.006709707533259118, n_feat=4, valid_n=545
  - C_rv_abs: qlike=15.72623585116872, mae=0.003852010740654159, rmse=0.006709707533259118, n_feat=4, valid_n=545
  - D_rv_signed_abs: qlike=15.726235851177563, mae=0.0038520107406555316, rmse=0.006709707533260839, n_feat=5, valid_n=545
  - E_rv_funding_trails: qlike=30.286826906595696, mae=0.003870795103522907, rmse=0.006664242443567894, n_feat=11, valid_n=551
- Split 2: train ('2024-01-29T00:00:00+00:00', '2024-02-25T23:59:59+00:00') | test ('2024-03-04T00:00:00+00:00', '2024-03-17T23:59:59+00:00') | purge/embargo=7d | n_train=1320 n_test=600
  - A_rv_only: qlike=3.2921528780662856, mae=0.006982166336572015, rmse=0.008589754050971107, n_feat=3, valid_n=235
  - B_rv_signed: qlike=2.0076686888273882, mae=0.006958990452933797, rmse=0.008603147196246115, n_feat=4, valid_n=211
  - C_rv_abs: qlike=2.0076686888273882, mae=0.006958990452933797, rmse=0.008603147196246115, n_feat=4, valid_n=211
  - D_rv_signed_abs: qlike=2.007668688826983, mae=0.006958990452933131, rmse=0.00860314719624591, n_feat=5, valid_n=211
  - E_rv_funding_trails: qlike=10.768377277749433, mae=0.00694206070164777, rmse=0.008603910983053268, n_feat=11, valid_n=189

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
- **Data sufficiency:** instruments=5 (MET); ok_30day_splits=0 (required>=3) => meets_claim_worthy_data_sufficiency=False.
- **No economic value claim, no overlay, no Track A linkage.** Observed metrics are out-of-sample forecast evidence under pre-registered design; instability across splits/instrument sets must be reported honestly.
- If any leakage/alignment doubt exists, treat as non-confirmatory.
