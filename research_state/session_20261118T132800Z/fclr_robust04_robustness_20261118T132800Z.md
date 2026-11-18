# FCLR-VOL-LIQ-ROBUST-04 — Track C Funding-Trail QLIKE Robustness (stdlib OLS HAR)

**Session:** session_20261118T132800Z
**Campaign:** FCLR-VOL-LIQ-ROBUST-04-20261118T120000Z
**Timestamp (UTC):** 20261118T132800Z
**Label:** EXPLORATORY/PILOT — not confirmatory, no forecast-gate pass claim.
**Network:** none. **Parquet:** none. **numpy/pandas/scipy:** none (stdlib only).

## Design
- Alternative chronological holdout: **test 2024-09**, train **2024-04..08**, 7d purge/embargo (2024-08-25..2024-08-31).
- Instruments: BTCUSDT, ETHUSDT, SOLUSDT, XRPUSDT, BNBUSDT
- Target: next-24h realized variance (sum of 24 hourly squared log returns t+1..t+24).
- Features (causal at t): lrv1, lrv24, lrv168, fund, fund_abs, fmean, fewma.
- Estimation: stdlib OLS on log RV, Duan smearing, train-only standardization.
- Uncertainty: UTC-day block bootstrap, seed 12345, 2000 reps; LOIO.

### Split 1: train 2024-04-01..2024-08-24, embargo 2024-08-25..2024-08-31, test 2024-09-01..2024-09-30
- train origins: {'BTCUSDT': 3312, 'ETHUSDT': 3312, 'SOLUSDT': 3312, 'XRPUSDT': 3312, 'BNBUSDT': 3312}
- test origins: {'BTCUSDT': 696, 'ETHUSDT': 696, 'SOLUSDT': 696, 'XRPUSDT': 696, 'BNBUSDT': 696}
- common test timestamps: 696
- A_rv_only: fit_ok={'BTCUSDT': True, 'ETHUSDT': True, 'SOLUSDT': True, 'XRPUSDT': True, 'BNBUSDT': True}, smearing=1.000000, n_pts=3480, mean_qlike=-6.110056052214218
- B_rv_signed: fit_ok={'BTCUSDT': True, 'ETHUSDT': True, 'SOLUSDT': True, 'XRPUSDT': True, 'BNBUSDT': True}, smearing=1.000000, n_pts=3480, mean_qlike=-6.108779175888441
- C_rv_abs: fit_ok={'BTCUSDT': True, 'ETHUSDT': True, 'SOLUSDT': True, 'XRPUSDT': True, 'BNBUSDT': True}, smearing=1.000000, n_pts=3480, mean_qlike=-6.106848782979606
- D_rv_signed_abs: fit_ok={'BTCUSDT': True, 'ETHUSDT': True, 'SOLUSDT': True, 'XRPUSDT': True, 'BNBUSDT': True}, smearing=1.000000, n_pts=3480, mean_qlike=-6.103127697637085
- E_rv_funding_trails: fit_ok={'BTCUSDT': True, 'ETHUSDT': True, 'SOLUSDT': True, 'XRPUSDT': True, 'BNBUSDT': True}, smearing=1.000000, n_pts=3480, mean_qlike=-6.0806380469802095

## Cross-split summary (ΔQLIKE = A − model; QLIKE lower = better; negative = model WORSE)
- A_rv_only: n=3480, mean_qlike=-6.110056052214218, mean_mae=0.0004376187154664991, mean_rmse=0.000732274837432504, mean_delta_qlike_vs_A=0.0
- B_rv_signed: n=3480, mean_qlike=-6.108779175888441, mean_mae=0.00043677219716584033, mean_rmse=0.0007322104742737242, mean_delta_qlike_vs_A=-0.0012768763257773091
  - bootstrap (A − model): mean=-0.001233, CI95=[-0.005123, 0.002913], reps=2000
- C_rv_abs: n=3480, mean_qlike=-6.106848782979606, mean_mae=0.00043671516119569255, mean_rmse=0.0007325181290869478, mean_delta_qlike_vs_A=-0.0032072692346130803
  - bootstrap (A − model): mean=-0.003218, CI95=[-0.006205, -0.000058], reps=2000
- D_rv_signed_abs: n=3480, mean_qlike=-6.103127697637085, mean_mae=0.0004355309053368119, mean_rmse=0.000733121148962697, mean_delta_qlike_vs_A=-0.006928354577132994
  - bootstrap (A − model): mean=-0.006913, CI95=[-0.011328, -0.002013], reps=2000
- E_rv_funding_trails: n=3480, mean_qlike=-6.0806380469802095, mean_mae=0.0004318623380859807, mean_rmse=0.0007404857354865178, mean_delta_qlike_vs_A=-0.029418005234008757
  - bootstrap (A − model): mean=-0.029233, CI95=[-0.042126, -0.015872], reps=2000

## Materiality floor (pre-registered; QLIKE lower = better)
- mean QLIKE A (RV-only) = -6.110056052214218
- mean QLIKE E (funding trails) = -6.0806380469802095
- ΔQLIKE (A − E) = -0.029418005234008757  (positive = E improves; negative = E is WORSE)
- bootstrap mean (A − E) = -0.029232628974225856, CI95 = [-0.04212624249173988, -0.015872221477403303]
- better model by mean QLIKE = **A_rv_only**
- **materiality_floor_met = False**
- LOIO E all positive = False

## Sign-convention audit (important)
- delta convention: mean_delta_qlike_vs_A = mean(QLIKE_A - QLIKE_model); QLIKE is a loss, lower is better
- negative delta means: model has HIGHER QLIKE = WORSE than RV-only
- prior headline check: session_20261118T093031Z reported E=-0.3579 as an improvement; under the same convention that is A - E = -0.3579, i.e. E is WORSE by 0.3579. The prior 'funding-trail improves QLIKE' claim is a SIGN INVERSION.
- prior headline corrected: RV-only (A) has lower QLIKE than funding-trail (E) in every split of session_20261118T093031Z and on the 2024-09 holdout here.
- robust04 finding: On the 2024-09 alternative holdout the funding-trail model E is worse than RV-only (A - E < 0, CI95 strictly below 0); the pre-registered improvement floor is NOT met.

## Leave-one-instrument-out mean ΔQLIKE vs A (A − model; negative = model worse)
- B_rv_signed: BTCUSDT=-0.0008196499668790649, ETHUSDT=-0.002488452849506735, SOLUSDT=0.0019329382559212997, XRPUSDT=-0.0036723126033795595, BNBUSDT=-0.0013369044650424864
- C_rv_abs: BTCUSDT=-0.0026537031688730877, ETHUSDT=-0.005253128584987887, SOLUSDT=-0.001714855989267968, XRPUSDT=-0.00400811126830414, BNBUSDT=-0.0024065471616323175
- D_rv_signed_abs: BTCUSDT=-0.007390217766098037, ETHUSDT=-0.009803642462229971, SOLUSDT=-0.005283433729547265, XRPUSDT=-0.0062810763520046555, BNBUSDT=-0.005883402575785035
- E_rv_funding_trails: BTCUSDT=-0.03107260210396559, ETHUSDT=-0.02692488094295342, SOLUSDT=-0.030697509745834146, XRPUSDT=-0.015080852057603648, BNBUSDT=-0.043314181319686985

## Honest status
- EXPLORATORY/PILOT. Alternative-holdout robustness confirmation of an exploratory Track C result; no confirmatory promotion claimed.
- No sealed months touched. No look-ahead; train-only standardization.
