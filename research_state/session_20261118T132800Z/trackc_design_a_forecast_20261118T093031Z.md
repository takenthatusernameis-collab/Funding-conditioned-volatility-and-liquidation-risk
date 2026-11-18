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
  - train origins: {'BTCUSDT': 888, 'ETHUSDT': 888, 'SOLUSDT': 888, 'XRPUSDT': 888, 'BNBUSDT': 888}
  - common test timestamps: 696
  - A_rv_only: fit_ok={'BTCUSDT': True, 'ETHUSDT': True, 'SOLUSDT': True, 'XRPUSDT': True, 'BNBUSDT': True}, smearing=1.000000, n_pts=3480, mean_qlike=-6.377520157117973
  - B_rv_signed: fit_ok={'BTCUSDT': True, 'ETHUSDT': True, 'SOLUSDT': True, 'XRPUSDT': True, 'BNBUSDT': True}, smearing=1.000000, n_pts=3480, mean_qlike=-6.374083397980691
  - C_rv_abs: fit_ok={'BTCUSDT': True, 'ETHUSDT': True, 'SOLUSDT': True, 'XRPUSDT': True, 'BNBUSDT': True}, smearing=1.000000, n_pts=3480, mean_qlike=-6.3750187883759075
  - D_rv_signed_abs: fit_ok={'BTCUSDT': True, 'ETHUSDT': True, 'SOLUSDT': True, 'XRPUSDT': True, 'BNBUSDT': True}, smearing=1.000000, n_pts=3480, mean_qlike=-6.377462790648988
  - E_rv_funding_trails: fit_ok={'BTCUSDT': True, 'ETHUSDT': True, 'SOLUSDT': True, 'XRPUSDT': True, 'BNBUSDT': True}, smearing=1.000000, n_pts=3480, mean_qlike=-6.2654924664359655
### Split 2: train 2024-04-01..2024-06-21, test 2024-06-29..2024-07-28
  - train origins: {'BTCUSDT': 1776, 'ETHUSDT': 1776, 'SOLUSDT': 1776, 'XRPUSDT': 1776, 'BNBUSDT': 1776}
  - common test timestamps: 696
  - A_rv_only: fit_ok={'BTCUSDT': True, 'ETHUSDT': True, 'SOLUSDT': True, 'XRPUSDT': True, 'BNBUSDT': True}, smearing=1.000000, n_pts=3480, mean_qlike=-5.677729356730936
  - B_rv_signed: fit_ok={'BTCUSDT': True, 'ETHUSDT': True, 'SOLUSDT': True, 'XRPUSDT': True, 'BNBUSDT': True}, smearing=1.000000, n_pts=3480, mean_qlike=-5.666847521519
  - C_rv_abs: fit_ok={'BTCUSDT': True, 'ETHUSDT': True, 'SOLUSDT': True, 'XRPUSDT': True, 'BNBUSDT': True}, smearing=1.000000, n_pts=3480, mean_qlike=-5.648584190940997
  - D_rv_signed_abs: fit_ok={'BTCUSDT': True, 'ETHUSDT': True, 'SOLUSDT': True, 'XRPUSDT': True, 'BNBUSDT': True}, smearing=1.000000, n_pts=3480, mean_qlike=-5.635539501874077
  - E_rv_funding_trails: fit_ok={'BTCUSDT': True, 'ETHUSDT': True, 'SOLUSDT': True, 'XRPUSDT': True, 'BNBUSDT': True}, smearing=1.000000, n_pts=3480, mean_qlike=-5.456050272659691
### Split 3: train 2024-04-01..2024-07-28, test 2024-08-05..2024-09-03
  - train origins: {'BTCUSDT': 2664, 'ETHUSDT': 2664, 'SOLUSDT': 2664, 'XRPUSDT': 2664, 'BNBUSDT': 2664}
  - common test timestamps: 696
  - A_rv_only: fit_ok={'BTCUSDT': True, 'ETHUSDT': True, 'SOLUSDT': True, 'XRPUSDT': True, 'BNBUSDT': True}, smearing=1.000000, n_pts=3480, mean_qlike=-5.595179511925172
  - B_rv_signed: fit_ok={'BTCUSDT': True, 'ETHUSDT': True, 'SOLUSDT': True, 'XRPUSDT': True, 'BNBUSDT': True}, smearing=1.000000, n_pts=3480, mean_qlike=-5.585817528927316
  - C_rv_abs: fit_ok={'BTCUSDT': True, 'ETHUSDT': True, 'SOLUSDT': True, 'XRPUSDT': True, 'BNBUSDT': True}, smearing=1.000000, n_pts=3480, mean_qlike=-5.581749335979045
  - D_rv_signed_abs: fit_ok={'BTCUSDT': True, 'ETHUSDT': True, 'SOLUSDT': True, 'XRPUSDT': True, 'BNBUSDT': True}, smearing=1.000000, n_pts=3480, mean_qlike=-5.468893198327585
  - E_rv_funding_trails: fit_ok={'BTCUSDT': True, 'ETHUSDT': True, 'SOLUSDT': True, 'XRPUSDT': True, 'BNBUSDT': True}, smearing=1.000000, n_pts=3480, mean_qlike=-4.85509733516823

## Cross-split summary
- A_rv_only: n=10440, mean_qlike=-5.883476341924694, mean_mae=0.0007336421160083371, mean_rmse=0.0018337429412740535, mean_delta_qlike_vs_A=0.0
- B_rv_signed: n=10440, mean_qlike=-5.8755828161423365, mean_mae=0.0007320754362837464, mean_rmse=0.0018378593825363588, mean_delta_qlike_vs_A=-0.00789352578235788
  - bootstrap: mean_improvement=-0.007848, CI95=[-0.012060, -0.003309], reps=2000
- C_rv_abs: n=10440, mean_qlike=-5.868450771765316, mean_mae=0.000734507421117885, mean_rmse=0.0018434420664812567, mean_delta_qlike_vs_A=-0.015025570159377938
  - bootstrap: mean_improvement=-0.015156, CI95=[-0.023771, -0.005336], reps=2000
- D_rv_signed_abs: n=10440, mean_qlike=-5.827298496950217, mean_mae=0.0007435155426744584, mean_rmse=0.001856796851649257, mean_delta_qlike_vs_A=-0.05617784497447741
  - bootstrap: mean_improvement=-0.055803, CI95=[-0.081117, -0.028348], reps=2000
- E_rv_funding_trails: n=10440, mean_qlike=-5.525546691421296, mean_mae=0.0007493718223208351, mean_rmse=0.0019331492918881056, mean_delta_qlike_vs_A=-0.3579296505033986
  - bootstrap: mean_improvement=-0.359576, CI95=[-0.498033, -0.193188], reps=2000

## Leave-one-instrument-out mean delta QLIKE vs A
- B_rv_signed: BTCUSDT=-0.009472870802366898, ETHUSDT=-0.010223316007104903, SOLUSDT=-0.006940966765301951, XRPUSDT=-0.006779864022229473, BNBUSDT=-0.006050611314786176
- C_rv_abs: BTCUSDT=-0.018332272215423998, ETHUSDT=-0.01883462755525592, SOLUSDT=-0.0156749524516042, XRPUSDT=-0.013184656383514676, BNBUSDT=-0.009101342191090886
- D_rv_signed_abs: BTCUSDT=-0.06899562348434797, ETHUSDT=-0.02411615574340625, SOLUSDT=-0.06675155101095061, XRPUSDT=-0.06446689307883846, BNBUSDT=-0.0565590015548438
- E_rv_funding_trails: BTCUSDT=-0.4197320577225743, ETHUSDT=-0.17863826651254266, SOLUSDT=-0.4307574008325463, XRPUSDT=-0.3328444624847273, BNBUSDT=-0.42767606496460214

## Honest status
- EXPLORATORY/PILOT. Smallest training window (45d) in split 1 is a pilot-quality risk.
- No sealed months (2024-10..12, 2025+) touched. No confirmatory promotion claimed.
- Missing numpy/pandas/scipy runtime is an environment constraint; stdlib fallback used.
