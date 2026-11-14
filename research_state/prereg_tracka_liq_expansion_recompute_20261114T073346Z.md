# Pre-Registration — FCLR-LIQ-EXPANSION-RECOMPUTE-20261114T073346Z

Generated: 2026-11-14T08:29:35Z
Campaign: `FCLR-FUND-VOL-LIQ-REDTEAM-20261114T042139Z`
Status: **FROZEN_PRE_OUTCOMES** (frozen before any outcome computation)

## Purpose

Independent recomputation of the sealed Track A liquidation expansion PASS TRACKA-HL-EXPANSION-20261111T195500Z (C2 vs B1 +19.04% QLIKE rel reduction, CI [-5.088102,-0.477660], 8 instruments, 593 paired rows, 3 test blocks, window 2026-05-01..2026-10-31) from cached observed ironflow liquidation labels + Hyperliquid funding + mark-price candles, without reading the sealed panel parquet. All results EXPLORATORY_ONLY, promotable=false.

## Frozen design

- Universe: AAVE, ADA, BCH, CRV, LTC, NEAR, UNI, ZEC
- Markets: AAVE-PERP, ADA-PERP, BCH-PERP, CRV-PERP, LTC-PERP, NEAR-PERP, UNI-PERP, ZEC-PERP
- Label: sum(notional_usd) of observed Hyperliquid liquidation events per symbol per 24h UTC bucket (observed liquidations only; no modeled/proxy/synthetic)
- Target: next-24h observed ironflow liquidation intensity per symbol per 24h UTC bucket: sum(notional_usd) of observed liquidation events over t+1..t+24h, strictly forward from decision time t
- Target source: ironflow_events observed liquidation labels (notional_usd)
- Models: B0 persistence; B1 HAR (log RV1h/RV24h/RV168h); C1 = B1 + signed funding + trailing |funding| percentile; C2 = C1 + mark/index premium + mark/EMA24 distance
- Fit: OLS on log(target + 1e-12), train-only scaling, train-only smearing back-transform
- Missing data: no zero-fill, no forward-fill; paired contrasts use common eligible rows
- Primary metric: paired OOS QLIKE, C2 vs B1
- Inference: circular block bootstrap over complete UTC days, 1-day blocks, 2000 reps, seed 20261114; Holm across 3 contrasts
- Robustness: LOIO, funding-permutation placebo (200 reps), per-symbol and per-block stability, leakage audit

## Frozen splits

- Train: 2026-05-01T00:00:00Z .. 2026-05-31T23:00:00Z
- Validation: 2026-06-07T00:00:00Z .. 2026-06-30T23:00:00Z
- Test blocks: 2026-07-07T00:00:00Z .. 2026-08-06T23:00:00Z; 2026-08-13T00:00:00Z .. 2026-09-11T23:00:00Z; 2026-09-18T00:00:00Z .. 2026-10-17T23:00:00Z
- Purge/embargo: 7 days at both boundaries

## Stop rule

- Instruments < 5, test blocks < 3, or core coverage < 0.8 → INADMISSIBLE with exact failing minima

## Non-goals

- Not promotable. EXPLORATORY_ONLY. Does not reopen the sealed expansion verdict.
- Sealed artifacts are read-only in this cell.
