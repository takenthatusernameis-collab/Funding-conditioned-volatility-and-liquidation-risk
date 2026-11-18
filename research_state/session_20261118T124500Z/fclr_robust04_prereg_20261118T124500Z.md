# FCLR-VOL-LIQ-ROBUST-04 — Track C Robustness Confirmation Prereg (FROZEN)

**Campaign:** FCLR-VOL-LIQ-ROBUST-04-20261118T120000Z
**Session:** session_20261118T124500Z
**Timestamp (UTC):** 20261118T124500Z
**Frozen before evaluation:** TRUE — `outcome_data_inspected_before_freeze=false`
**Label:** EXPLORATORY/PILOT — not confirmatory, no forecast-gate pass claim.

## Research question
Does the Track C Design A funding-trail QLIKE improvement (model E = `lrv1,lrv24,lrv168,fund,fund_abs,fmean,fewma` vs RV-only model A, originally mean ΔQLIKE = −0.3579 in `session_20261118T093031Z`) hold under an **alternative chronological holdout** (test month **2024-09**, train **2024-04..08**) on the cached 2024-04..09 panel?

## Design (fixed ex ante)
- Instruments: BTCUSDT, ETHUSDT, SOLUSDT, XRPUSDT, BNBUSDT
- Train window: 2024-04-01..2024-08-31
- Holdout test window: 2024-09-01..2024-09-30
- Origin rule: bar t eligible iff trailing 168h history present and next-24h horizon bars t+1..t+24 all inside the window
- Horizon: next-24h realized variance = Σ 24 hourly squared close-to-close log returns
- Mark field: close (markPriceKlines 1h), units USDT
- Features (causal-at-t): lrv1, lrv24, lrv168, fund, fund_abs, fmean, fewma
- Model family: stdlib OLS HAR (log-RV), Duan smearing
- Baseline A: RV-only; Candidate E: RV + funding trails
- Metrics: ΔQLIKE vs A (primary), MAE, RMSE
- Bootstrap: 2000 reps, seed 12345, UTC-day blocks resampled jointly across instruments
- LOIO: leave-one-instrument-out mean ΔQLIKE vs A
- Materiality floor: bootstrap mean improvement (A−E) > 0 **and** CI95 lower bound > 0; LOIO majority-positive

## Leakage controls
- Train-only standardization; no full-sample normalization; no future bars; 7d purge/embargo; no sealed months (2024-10+).

## Interpretation (ex ante)
- If E materially improves QLIKE with CI95 lower bound > 0 → the Track C funding-trail result is **robust to holdout choice** (still EXPLORATORY/PILOT).
- If not → the original result is **holdout-specific** and must be reported as such.

## Prohibitions
No outcome inspection before freeze; no network; no sealed months; no confirmatory promotion.