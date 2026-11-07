# Evaluation Summary - Funding Ablations (Gate 4, pilot)

**Generated:** 2026-11-07T01:14:21Z
**Git SHA:** 9ce75ad4fcd82fcff42950d1bfe85922019cb6e6
**Scope:** BTCUSDT, ETHUSDT, SOLUSDT, XRPUSDT, 2024-01-01 to 2024-03-31, 24h forward RV, 1 walk-forward split
**Model:** log-target ridge HAR (λ=0.001), predictions exp-transformed (positive). Train-only normalization, chronological splits, 7d purge/embargo.

## Aggregate (mean across splits)
| Ablation | QLIKE | MAE | RMSE | ΔQLIKE vs A | neg_pred |
|---|---|---|---|---|---|
| A_rv_only | 333293.4217179353 | 255952842.64419475 | 8236954326.140707 | 0.0 | 0.0 |
| B_rv_signed | 4847457.505402432 | 15955243.776873946 | 623478530.5448127 | 4514164.083684497 | 0.0 |
| C_rv_abs | 4847457.505402432 | 15955243.776873946 | 623478530.5448127 | 4514164.083684497 | 0.0 |
| D_rv_signed_abs | 4847468.957729966 | 15955229.924937373 | 623478010.2565118 | 4514175.536012031 | 0.0 |
| E_rv_funding_trails | 1.7172709452688984e+46 | 2.853194870747307e+90 | 1.6899008599432472e+92 | 1.7172709452688984e+46 | 0.0 |

## Split Details
- Split 0: test 2024-02-22..2024-03-31
  - A_rv_only: qlike=333293.4217179353, mae=255952842.64419475, rmse=8236954326.140707, n_feat=3, valid_n=3508, neg_pred=0
  - B_rv_signed: qlike=4847457.505402432, mae=15955243.776873946, rmse=623478530.5448127, n_feat=4, valid_n=3508, neg_pred=0
  - C_rv_abs: qlike=4847457.505402432, mae=15955243.776873946, rmse=623478530.5448127, n_feat=4, valid_n=3508, neg_pred=0
  - D_rv_signed_abs: qlike=4847468.957729966, mae=15955229.924937373, rmse=623478010.2565118, n_feat=5, valid_n=3508, neg_pred=0
  - E_rv_funding_trails: qlike=1.7172709452688984e+46, mae=2.853194870747307e+90, rmse=1.6899008599432472e+92, n_feat=11, valid_n=3508, neg_pred=0

## Leakage/Alignment Notes
- Funding (8h) aligned to 1h via last-known value at/before each hour (ffill). NaN if missing.
- Trailing funding pct/z computed over rolling windows on aligned series (past-only).
- Chronological splits, 7d purge/embargo, train-only normalization.
- Basis/premium not included in this run (no aligned series added); missing treated as NaN per policy.

## Caveats (non-negotiable)
- **Pilot only**: 1 split, 4 assets, Jan-Mar 2024. Not a sealed holdout result; no block-aware CIs; no multiple-comparison control applied.
- Funding ablations B/C/D/E show **worse QLIKE than RV-only (A)** in this pilot sample (possible overfit, regime, or feature construction). Do NOT interpret as evidence funding has no value; do NOT interpret as evidence of value.
- Gate 4 requires robust OOS evidence across adequate splits/assets before any claim. Next: expand splits/period, add basis/premium if available, add regularization tuning on train/val only, and pre-register contrasts.
