# Evidence Audit — FCLR-VOL-LIQ-ROBUST-04

**Session:** session_20261118T132800Z
**Campaign:** FCLR-VOL-LIQ-ROBUST-04-20261118T120000Z
**Network:** none. **Parquet:** none. **numpy/pandas/scipy:** none (stdlib only).

## Tracks completed
- **Track C (carried forward from `session_20261118T093031Z`):** `trackc_design_a_forecast_20261118T093031Z.{py,json,md}`. NOTE: the prior headline E=-0.3579 was reported as an improvement, but under the same delta convention (mean QLIKE_A − QLIKE_model) it means E is WORSE by 0.3579 — a sign inversion.
- **Track B (carried forward from `session_20261118T093031Z`):** `trackb_breach_labels_20261118T093031Z.{py,json,md}`; synthetic modeled boundary-breach labels (rows 41760, breached 1418, observed_liquidation_labels=false).
- **Breach forecast (carried forward from `session_20261118T114500Z`):** `trackbc_breach_prereg_20261118T114500Z.json`, `trackbc_breach_forecast_20261118T114500Z.{py,json,md}`; pooled mean ΔAUC −0.0661, materiality floor NOT met.
- **Robust-04 (executed this session):** `fclr_robust04_prereg_20261118T132800Z.{json,md}`, `fclr_robust04_robustness_20261118T132800Z.{py,json,md}`; alternative holdout 2024-09 (train 2024-04..08); mean QLIKE A=-6.110056 vs E=-6.080638; A − E = -0.029418, CI95 [-0.04212624249173988, -0.015872221477403303]; materiality floor NOT met; RV-only better.

## Sign-convention audit (important)
- mean_delta_qlike_vs_A = mean(QLIKE_A - QLIKE_model); QLIKE is a loss, lower is better
- session_20261118T093031Z reported E=-0.3579 as an improvement; under the same convention that is A - E = -0.3579, i.e. E is WORSE by 0.3579. The prior 'funding-trail improves QLIKE' claim is a SIGN INVERSION.
- On the 2024-09 alternative holdout the funding-trail model E is worse than RV-only (A - E < 0, CI95 strictly below 0); the pre-registered improvement floor is NOT met.

## Trigger check
- `trigger_check_20261118T132800Z.json`: all 4 reopen triggers OPEN; none fired.

## Honest status
- EXPLORATORY/PILOT. Robustness confirmation executed with substantive artifacts. The pre-registered funding-trail improvement floor is NOT met on 2024-09; the prior Track C headline is corrected as a sign inversion. No confirmatory promotion claimed.
