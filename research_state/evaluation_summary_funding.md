# Evaluation Summary - Funding Ablations (Gate 4, pilot)

**Generated:** 2026-11-07T02:22:15Z
**Git SHA:** ba03242224fa7bf1ada80211211e72324c899327
**Scope:** BTCUSDT, ETHUSDT, SOLUSDT, XRPUSDT, 2024-01-01 to 2024-03-31, 24h forward RV, 1 walk-forward split
**Model:** direct-variance OLS HAR (target = forward realized VARIANCE; train-only normalization). No log target, no exp transform.

## Aggregate (mean across splits)
| Ablation | QLIKE | MAE | RMSE | ΔQLIKE vs A | neg_pred |
|---|---|---|---|---|---|
| A_rv_only | 1.59541000261996 | 0.001682307260657039 | 0.0028922903876945506 | 0.0 | 342.0 |
| B_rv_signed | 1.4392367821430467 | 0.002343811776289131 | 0.003378589393046945 | -0.1561732204769133 | 188.0 |
| C_rv_abs | 1.4392367821430467 | 0.002343811776289131 | 0.003378589393046945 | -0.1561732204769133 | 188.0 |
| D_rv_signed_abs | 1.4392367821409628 | 0.0023438117762892034 | 0.003378589393047032 | -0.15617322047899718 | 188.0 |
| E_rv_funding_trails | 1.0644322409593807 | 0.0030111074589971904 | 0.004533937230615815 | -0.5309777616605793 | 675.0 |

## Split Details
- Split 0: test 2024-02-22..2024-03-31
  - A_rv_only: qlike=1.59541000261996, mae=0.001682307260657039, rmse=0.0028922903876945506, n_feat=3, valid_n=3166, neg_pred=342
  - B_rv_signed: qlike=1.4392367821430467, mae=0.002343811776289131, rmse=0.003378589393046945, n_feat=4, valid_n=3320, neg_pred=188
  - C_rv_abs: qlike=1.4392367821430467, mae=0.002343811776289131, rmse=0.003378589393046945, n_feat=4, valid_n=3320, neg_pred=188
  - D_rv_signed_abs: qlike=1.4392367821409628, mae=0.0023438117762892034, rmse=0.003378589393047032, n_feat=5, valid_n=3320, neg_pred=188
  - E_rv_funding_trails: qlike=1.0644322409593807, mae=0.0030111074589971904, rmse=0.004533937230615815, n_feat=11, valid_n=2834, neg_pred=675

## Leakage/Alignment Notes
- Funding (8h) aligned to 1h via last-known value at/before each hour (ffill). NaN if missing.
- Trailing funding pct/z computed over rolling windows on aligned series (past-only).
- Chronological splits, 7d purge/embargo, train-only normalization.
- Basis/premium not included in this run (no aligned series added); missing treated as NaN per policy.

## Caveats (non-negotiable)
- **Pilot only**: 1 split, 4 assets, Jan-Mar 2024. Not a sealed holdout result; no block-aware CIs; no multiple-comparison control applied.
- Funding ablations B/C/D/E show **worse QLIKE than RV-only (A)** in this pilot sample (possible overfit, regime, or feature construction). Do NOT interpret as evidence funding has no value; do NOT interpret as evidence of value.
- Gate 4 requires robust OOS evidence across adequate splits/assets before any claim. Next: expand splits/period, add basis/premium if available, add regularization tuning on train/val only, and pre-register contrasts.
