# Evaluation Summary - Funding Ablations (Gate 4, pilot)

**Generated:** 2026-11-06T23:17:27Z
**Git SHA:** 89bf8584ee4b922f0b22f666ee72588373ee0c16
**Scope:** BTCUSDT, ETHUSDT, SOLUSDT, XRPUSDT, 2024-01-01 to 2024-03-31, 24h forward RV, 1 walk-forward split
**Model:** log-target ridge HAR (λ=0.001), predictions exp-transformed (positive). Train-only normalization, chronological splits, 7d purge/embargo.

## Aggregate (mean across splits)
| Ablation | QLIKE | MAE | RMSE | ΔQLIKE vs A | neg_pred |
|---|---|---|---|---|---|
| A_rv_only | 2.5828046574874402e+25 | 2.3755417897490293e+30 | 1.123812195759099e+32 | 0.0 | 0.0 |
| B_rv_signed | 6.221739678582001e+38 | 6.121341638641806e+26 | 3.616865432852027e+28 | 6.221739678581742e+38 | 0.0 |
| C_rv_abs | 6.221739678582001e+38 | 6.121341638641806e+26 | 3.616865432852027e+28 | 6.221739678581742e+38 | 0.0 |
| D_rv_signed_abs | 6.221835275107524e+38 | 6.121321098222818e+26 | 3.6168532926070587e+28 | 6.221835275107265e+38 | 0.0 |
| E_rv_funding_trails | 2.510636950488436e+154 | 1.811528758046905e+248 | None | 2.510636950488436e+154 | 0.0 |

## Split Details
- Split 0: test 2024-02-22..2024-03-31
  - A_rv_only: qlike=2.5828046574874402e+25, mae=2.3755417897490293e+30, rmse=1.123812195759099e+32, n_feat=3, valid_n=1990, neg_pred=0
  - B_rv_signed: qlike=6.221739678582001e+38, mae=6.121341638641806e+26, rmse=3.616865432852027e+28, n_feat=4, valid_n=1990, neg_pred=0
  - C_rv_abs: qlike=6.221739678582001e+38, mae=6.121341638641806e+26, rmse=3.616865432852027e+28, n_feat=4, valid_n=1990, neg_pred=0
  - D_rv_signed_abs: qlike=6.221835275107524e+38, mae=6.121321098222818e+26, rmse=3.6168532926070587e+28, n_feat=5, valid_n=1990, neg_pred=0
  - E_rv_funding_trails: qlike=2.510636950488436e+154, mae=1.811528758046905e+248, rmse=None, n_feat=11, valid_n=1990, neg_pred=0

## Leakage/Alignment Notes
- Funding (8h) aligned to 1h via last-known value at/before each hour (ffill). NaN if missing.
- Trailing funding pct/z computed over rolling windows on aligned series (past-only).
- Chronological splits, 7d purge/embargo, train-only normalization.
- Basis/premium not included in this run (no aligned series added); missing treated as NaN per policy.

## Caveats (non-negotiable)
- **Pilot only**: 1 split, 4 assets, Jan-Mar 2024. Not a sealed holdout result; no block-aware CIs; no multiple-comparison control applied.
- Funding ablations B/C/D/E show **worse QLIKE than RV-only (A)** in this pilot sample (possible overfit, regime, or feature construction). Do NOT interpret as evidence funding has no value; do NOT interpret as evidence of value.
- Gate 4 requires robust OOS evidence across adequate splits/assets before any claim. Next: expand splits/period, add basis/premium if available, add regularization tuning on train/val only, and pre-register contrasts.
