# Pre-Registration — FCLR-LIQ-EXPANSION-RECONCILIATION-20261114T083642Z

Generated: 2026-11-14T11:19:38Z
Campaign: `FCLR-LIQ-EXPANSION-RECONCILIATION-20261114T083642Z`
Status: **FROZEN_PRE_OUTCOMES** (frozen before any outcome computation)

## Purpose

2×2 reconciliation audit for the 19.04% vs 6.19% C2_vs_B1 QLIKE gap between the sealed Track A liquidation expansion (TRACKA-HL-EXPANSION-20261111T195500Z, PASS, +19.04% QLIKE rel reduction) and its independent recompute (FCLR-LIQ-EXPANSION-RECOMPUTE-20261114T073346Z, INCONCLUSIVE, +6.19% QLIKE rel reduction). Both share 1,472 (coin, ts) keys over 2026-05-01..2026-10-31. Cells: {Sealed panel, Recompute panel} × {Sealed estimator, Recompute estimator}. Verdict in {EXPLAINED_BY_ESTIMATOR, EXPLAINED_BY_DATA, UNEXPLAINED, INCONCLUSIVE}. All results EXPLORATORY_ONLY, promotable=false. Does not reopen sealed verdict.

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
