# FCLR-VOL-LIQ-ROBUST-04 — Prereg (frozen before outcomes)

**Session:** `session_20261118T132800Z`
**Campaign:** `FCLR-VOL-LIQ-ROBUST-04-20261118T120000Z`
**Timestamp (UTC):** 2026-11-18T13:28:00Z
**Label:** EXPLORATORY/PILOT — not confirmatory, no forecast-gate pass claim.
**Network:** none. **Parquet:** none. **numpy/pandas/scipy:** none (stdlib only).

## Frozen ex ante (before touching evaluation)

- `outcome_data_inspected_before_freeze = false`; `preregistered_before_outcomes = true`.
- **Research question:** does the Track C Design A funding-trail QLIKE improvement over RV-only (headline E = −0.3579, `session_20261118T093031Z`) hold under an alternative chronological holdout (test 2024-09, train 2024-04..08) on the cached 2024-04..09 panel?
- **Instruments:** BTC/ETH/SOL/XRP/BNB (5).
- **Windows:** train 2024-04-01..2024-08-24; embargo 2024-08-25..2024-08-31 (7d); test 2024-09-01..2024-09-30.
- **Target:** next-24h realized variance (sum of 24 hourly squared log returns t+1..t+24, dimensionless).
- **Features (causal at t):** `lrv1, lrv24, lrv168, fund, fund_abs, fmean, fewma`.
- **Models:** A_rv_only, B_rv_signed, C_rv_abs, D_rv_signed_abs, E_rv_funding_trails.
- **Estimation:** stdlib OLS on log RV + Duan smearing; train-only standardization.
- **Metric:** QLIKE (primary), MAE, RMSE; paired ΔQLIKE vs A.
- **Uncertainty:** UTC-day block bootstrap, jointly across instruments, seed 12345, 2000 reps, percentile CI95; LOIO.
- **Materiality floor:** mean ΔQLIKE (A − E) > 0 with CI95 lower bound > 0 on the 2024-09 holdout.

## Prohibitions
No future bars, no full-sample normalization, no sealed months, no look-ahead, no funding/threshold tuning on test, no observed-liquidation labeling, no sealed confirmatory re-score. All artifacts live in this session dir (root `research_state/` is at 500/500).