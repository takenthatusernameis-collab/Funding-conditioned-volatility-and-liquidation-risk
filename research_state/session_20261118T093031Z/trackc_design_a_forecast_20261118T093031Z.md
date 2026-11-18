# Track C — Design A Exploratory Volatility Forecast (stdlib OLS HAR)

**Session:** session_20261118T093031Z
**Timestamp (UTC):** 20261118T093031Z
**Track:** C — volatility/stress forecasting (Track C Design A)
**Label:** EXPLORATORY/PILOT — not confirmatory, no forecast-gate pass claim.
**Network:** none. **Parquet:** none. **numpy/pandas/scipy:** none (stdlib only).

## Design
- Instruments: BTCUSDT, ETHUSDT, SOLUSDT, XRPUSDT, BNBUSDT
- Window: 2024-04-01..2024-09-09 (provenanced confirmatory subset)
- Horizon: next-24h realized variance from 1h mark-price close-to-close log returns t+1..t+24
- Mark field: close (markPriceKlines 1h), units USDT
- Target units: squared log-return (dimensionless); sum of 24 hourly squared log returns
- Epsilon: 1e-12
- Models: A_rv_only, B_rv_signed, C_rv_abs, D_rv_signed_abs, E_rv_funding_trails
- Estimation: OLS via normal equations + Gaussian elimination with partial pivoting
- Standardization: train-only means/stds; zero-variance columns dropped
- Back-transformation: Duan smearing factor on train residuals
- Metrics: QLIKE (primary), MAE, RMSE; paired delta QLIKE vs model A
- Bootstrap: 2000 reps, seed 12345, UTC day blocks resampled jointly across instruments
- Splits: 3 chronological non-overlapping 30d test blocks with 7d purge/embargo, expanding train

### Split 1: train 2024-04-01..2024-05-15, test 2024-05-23..2024-06-21
  - train origins: {'BTCUSDT': 0, 'ETHUSDT': 0, 'SOLUSDT': 0, 'XRPUSDT': 0, 'BNBUSDT': 0}
  - common test timestamps: 0
  - A_rv_only: fit_ok={'BTCUSDT': True, 'ETHUSDT': True, 'SOLUSDT': True, 'XRPUSDT': True, 'BNBUSDT': True}, smearing=1.000000, n_pts=0, mean_qlike=None
  - B_rv_signed: fit_ok={'BTCUSDT': True, 'ETHUSDT': True, 'SOLUSDT': True, 'XRPUSDT': True, 'BNBUSDT': True}, smearing=1.000000, n_pts=0, mean_qlike=None
  - C_rv_abs: fit_ok={'BTCUSDT': True, 'ETHUSDT': True, 'SOLUSDT': True, 'XRPUSDT': True, 'BNBUSDT': True}, smearing=1.000000, n_pts=0, mean_qlike=None
  - D_rv_signed_abs: fit_ok={'BTCUSDT': True, 'ETHUSDT': True, 'SOLUSDT': True, 'XRPUSDT': True, 'BNBUSDT': True}, smearing=1.000000, n_pts=0, mean_qlike=None
  - E_rv_funding_trails: fit_ok={'BTCUSDT': True, 'ETHUSDT': True, 'SOLUSDT': True, 'XRPUSDT': True, 'BNBUSDT': True}, smearing=1.000000, n_pts=0, mean_qlike=None
### Split 2: train 2024-04-01..2024-06-21, test 2024-06-29..2024-07-28
  - train origins: {'BTCUSDT': 0, 'ETHUSDT': 0, 'SOLUSDT': 0, 'XRPUSDT': 0, 'BNBUSDT': 0}
  - common test timestamps: 0
  - A_rv_only: fit_ok={'BTCUSDT': True, 'ETHUSDT': True, 'SOLUSDT': True, 'XRPUSDT': True, 'BNBUSDT': True}, smearing=1.000000, n_pts=0, mean_qlike=None
  - B_rv_signed: fit_ok={'BTCUSDT': True, 'ETHUSDT': True, 'SOLUSDT': True, 'XRPUSDT': True, 'BNBUSDT': True}, smearing=1.000000, n_pts=0, mean_qlike=None
  - C_rv_abs: fit_ok={'BTCUSDT': True, 'ETHUSDT': True, 'SOLUSDT': True, 'XRPUSDT': True, 'BNBUSDT': True}, smearing=1.000000, n_pts=0, mean_qlike=None
  - D_rv_signed_abs: fit_ok={'BTCUSDT': True, 'ETHUSDT': True, 'SOLUSDT': True, 'XRPUSDT': True, 'BNBUSDT': True}, smearing=1.000000, n_pts=0, mean_qlike=None
  - E_rv_funding_trails: fit_ok={'BTCUSDT': True, 'ETHUSDT': True, 'SOLUSDT': True, 'XRPUSDT': True, 'BNBUSDT': True}, smearing=1.000000, n_pts=0, mean_qlike=None
### Split 3: train 2024-04-01..2024-07-28, test 2024-08-05..2024-09-03
  - train origins: {'BTCUSDT': 0, 'ETHUSDT': 0, 'SOLUSDT': 0, 'XRPUSDT': 0, 'BNBUSDT': 0}
  - common test timestamps: 0
  - A_rv_only: fit_ok={'BTCUSDT': True, 'ETHUSDT': True, 'SOLUSDT': True, 'XRPUSDT': True, 'BNBUSDT': True}, smearing=1.000000, n_pts=0, mean_qlike=None
  - B_rv_signed: fit_ok={'BTCUSDT': True, 'ETHUSDT': True, 'SOLUSDT': True, 'XRPUSDT': True, 'BNBUSDT': True}, smearing=1.000000, n_pts=0, mean_qlike=None
  - C_rv_abs: fit_ok={'BTCUSDT': True, 'ETHUSDT': True, 'SOLUSDT': True, 'XRPUSDT': True, 'BNBUSDT': True}, smearing=1.000000, n_pts=0, mean_qlike=None
  - D_rv_signed_abs: fit_ok={'BTCUSDT': True, 'ETHUSDT': True, 'SOLUSDT': True, 'XRPUSDT': True, 'BNBUSDT': True}, smearing=1.000000, n_pts=0, mean_qlike=None
  - E_rv_funding_trails: fit_ok={'BTCUSDT': True, 'ETHUSDT': True, 'SOLUSDT': True, 'XRPUSDT': True, 'BNBUSDT': True}, smearing=1.000000, n_pts=0, mean_qlike=None

## Cross-split summary
- A_rv_only: n=0, mean_qlike=None, mean_mae=None, mean_rmse=None, mean_delta_qlike_vs_A=None
- B_rv_signed: n=0, mean_qlike=None, mean_mae=None, mean_rmse=None, mean_delta_qlike_vs_A=None
- C_rv_abs: n=0, mean_qlike=None, mean_mae=None, mean_rmse=None, mean_delta_qlike_vs_A=None
- D_rv_signed_abs: n=0, mean_qlike=None, mean_mae=None, mean_rmse=None, mean_delta_qlike_vs_A=None
- E_rv_funding_trails: n=0, mean_qlike=None, mean_mae=None, mean_rmse=None, mean_delta_qlike_vs_A=None

## Leave-one-instrument-out mean delta QLIKE vs A
- B_rv_signed: BTCUSDT=None, ETHUSDT=None, SOLUSDT=None, XRPUSDT=None, BNBUSDT=None
- C_rv_abs: BTCUSDT=None, ETHUSDT=None, SOLUSDT=None, XRPUSDT=None, BNBUSDT=None
- D_rv_signed_abs: BTCUSDT=None, ETHUSDT=None, SOLUSDT=None, XRPUSDT=None, BNBUSDT=None
- E_rv_funding_trails: BTCUSDT=None, ETHUSDT=None, SOLUSDT=None, XRPUSDT=None, BNBUSDT=None

## Honest status
- EXPLORATORY/PILOT. Smallest training window (45d) in split 1 is a pilot-quality risk.
- No sealed months (2024-10..12, 2025+) touched. No confirmatory promotion claimed.
- Missing numpy/pandas/scipy runtime is an environment constraint; stdlib fallback used.
