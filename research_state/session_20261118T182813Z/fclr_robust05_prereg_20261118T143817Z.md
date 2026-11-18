# FCLR-VOL-LIQ-ROBUST-05 — Prereg (frozen before outcomes)

**Session:** `session_20261118T143817Z`
**Campaign:** `FCLR-VOL-LIQ-ROBUST-05-20261118T132800Z`
**Timestamp (UTC):** 2026-11-18T14:38:17Z
**Label:** EXPLORATORY/PILOT — not confirmatory, no forecast-gate pass claim.
**Network:** none. **Parquet:** none. **numpy/pandas/scipy:** none (stdlib only).

## Frozen ex ante (before touching evaluation)

- `outcome_data_inspected_before_freeze = false`; `preregistered_before_outcomes = true`.
- **Research question:** under the corrected QLIKE sign convention, does **any** funding-conditioned model (B/C/D/E) beat RV-only (A) across **multiple chronological holdouts**, and is the effect distinguishable from a **placebo** permutation null?
- **Instruments:** BTC/ETH/SOL/XRP/BNB (5).
- **Holdouts / expanding train (7-day purge/embargo):**
  - `2024-06`: train 2024-04-01..2024-05-24, embargo 05-25..05-31, test 06-01..06-30
  - `2024-07`: train 2024-04-01..2024-06-23, embargo 06-24..06-30, test 07-01..07-31
  - `2024-08`: train 2024-04-01..2024-07-24, embargo 07-25..07-31, test 08-01..08-31
  - `2024-09`: train 2024-04-01..2024-08-24, embargo 08-25..08-31, test 09-01..09-30
- **Target:** next-24h realized variance (sum of 24 hourly squared log returns t+1..t+24, dimensionless).
- **Features (causal at t):** `lrv1, lrv24, lrv168, fund, fund_abs, fmean, fewma`.
- **Models:** A_rv_only, B_rv_signed, C_rv_abs, D_rv_signed_abs, E_rv_funding_trails.
- **Estimation:** stdlib OLS on log RV + Duan smearing; train-only standardization.
- **Metric:** QLIKE (primary, lower is better), MAE, RMSE; paired ΔQLIKE vs A = `QLIKE_A − QLIKE_model` (**positive = model better**).
- **Uncertainty:** UTC-day block bootstrap, jointly across instruments, seed 12345, 2000 reps, percentile CI95; LOIO per holdout.
- **Placebo:** deterministic permutation of the funding observation series (seed 12345) through the identical pipeline; report its ΔQLIKE distribution for E.
- **Materiality floor:** E beats A (mean ΔQLIKE > 0 with bootstrap CI95 lower bound > 0) in **≥3 of 4** holdouts **and** real funding-trail `|mean ΔQLIKE|` exceeds placebo `|mean ΔQLIKE|`. Otherwise: honest negative result.

## Prior state carried in

- ROBUST-04 (2024-09 holdout): A − E = **−0.029418**, CI95 `[−0.042126, −0.015872]` → RV-only better; floor not met.
- The earlier "funding-trail improves QLIKE" headline was a **sign inversion** and must not be repeated.

## Prohibitions

No future bars, no full-sample normalization, no sealed months, no look-ahead, no funding/threshold tuning on test, no observed-liquidation labeling, no sealed confirmatory re-score. All artifacts live in this session dir.
