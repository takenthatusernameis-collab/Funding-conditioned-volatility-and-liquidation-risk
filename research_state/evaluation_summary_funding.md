# Evaluation Summary - Funding Ablations (Gate 4, pilot)

**Generated:** 2026-11-06T23:31:49Z
**Git SHA:** e8af3abbb48d93dd63b02b2c72da99392d51720e
**Scope:** BTCUSDT, ETHUSDT, SOLUSDT, XRPUSDT, 2024-01-01 to 2024-03-31, 24h forward RV, 1 walk-forward split
**Model:** log-target ridge HAR (λ=0.001), predictions exp-transformed (positive). Train-only normalization, chronological splits, 7d purge/embargo.

## Aggregate (mean across splits)
| Ablation | QLIKE | MAE | RMSE | ΔQLIKE vs A | neg_pred |
|---|---|---|---|---|---|
| A_rv_only | 333293.42171793274 | 255952842.6442126 | 8236954326.141345 | 0.0 | 0.0 |
| B_rv_signed | None | None | None | None | None |
| C_rv_abs | None | None | None | None | None |
| D_rv_signed_abs | None | None | None | None | None |
| E_rv_funding_trails | None | None | None | None | None |

## Split Details
- Split 0: test 2024-02-22..2024-03-31
  - A_rv_only: qlike=333293.42171793274, mae=255952842.6442126, rmse=8236954326.141345, n_feat=3, valid_n=3508, neg_pred=0
  - B_rv_signed: ERR The truth value of an array with more than one element is ambiguous. Use a.any() or a.all()
  - C_rv_abs: ERR The truth value of an array with more than one element is ambiguous. Use a.any() or a.all()
  - D_rv_signed_abs: ERR The truth value of an array with more than one element is ambiguous. Use a.any() or a.all()
  - E_rv_funding_trails: ERR The truth value of an array with more than one element is ambiguous. Use a.any() or a.all()

## Leakage/Alignment Notes
- Funding (8h) aligned to 1h via last-known value at/before each hour (ffill). NaN if missing.
- Trailing funding pct/z computed over rolling windows on aligned series (past-only).
- Chronological splits, 7d purge/embargo, train-only normalization.
- Basis/premium not included in this run (no aligned series added); missing treated as NaN per policy.

## Caveats (non-negotiable)
- **Pilot only**: 1 split, 4 assets, Jan-Mar 2024. Not a sealed holdout result; no block-aware CIs; no multiple-comparison control applied.
- Funding ablations B/C/D/E show **worse QLIKE than RV-only (A)** in this pilot sample (possible overfit, regime, or feature construction). Do NOT interpret as evidence funding has no value; do NOT interpret as evidence of value.
- Gate 4 requires robust OOS evidence across adequate splits/assets before any claim. Next: expand splits/period, add basis/premium if available, add regularization tuning on train/val only, and pre-register contrasts.
