# Pre-Registration — FCLR-011-INDEPENDENT-RECOMPUTE-20261114T042139Z

Generated: 2026-11-15T23:44:02Z
Campaign: `FCLR-FUND-VOL-LIQ-REDTEAM-20261114T042139Z`
Status: **FROZEN_PRE_OUTCOMES** (frozen before any outcome computation)

## Purpose

Clean independent recomputation of the sealed FCLR-011 volatility PASS (C2 vs B1 4.94% QLIKE, CI [-0.032546,-0.001418], 5 instruments, 3 blocks, test 2026-05-08..2026-08-06) from cached Binance inputs, without the Git-LFS panel and without the heuristic run_trackc_* predictor.

## Frozen design

- Universe: BTCUSDT, ETHUSDT, BNBUSDT, SOLUSDT, XRPUSDT
- Target: next-24h realized variance of mark-price log returns: sum of squared 1h log returns over t+1..t+24, forward-looking from decision time t
- Target source: klines close (mark price unavailable in cache)
- Source limitation: markPriceKlines/indexPriceKlines/premiumIndexKlines are absent from the 2026 cache; close-to-close RV and close-based premium proxies are used and recorded in the build report
- Models: B0 persistence; B1 HAR; C1 = B1 + signed funding + trailing |funding| percentile; C2 = C1 + premium + EMA24 distance
- Premium status: NOT_COMPUTABLE_WITHOUT_INDEX_PRICE
- Fit: OLS on log(RV + 1e-12), train-only scaling, train-only smearing back-transform
- Missing data: no zero-fill, no forward-fill; paired contrasts use common eligible rows
- Primary metric: paired OOS QLIKE, C2 vs B1
- Inference: circular block bootstrap over UTC days, 24h blocks, 2000 reps, seed 20261114; Holm across 3 contrasts
- Robustness: LOIO, funding-permutation placebo (200 reps), per-symbol and per-block stability, leakage audit

## Frozen splits

- Train: 2026-01-01T00:00:00Z .. 2026-03-17T23:00:00Z
- Validation: 2026-03-25T00:00:00Z .. 2026-04-30T23:00:00Z
- Test: 2026-05-08T00:00:00Z .. 2026-08-06T23:00:00Z
- Purge/embargo: 7 days at both boundaries

## Stop rule

- Instruments < 5, test blocks < 3, or core coverage < 0.8 → INADMISSIBLE with exact failing minima

## Non-goals

- Not promotable. EXPLORATORY_ONLY. Does not reopen the sealed FCLR-011 verdict.
- Sealed artifacts are read-only in this cell.
