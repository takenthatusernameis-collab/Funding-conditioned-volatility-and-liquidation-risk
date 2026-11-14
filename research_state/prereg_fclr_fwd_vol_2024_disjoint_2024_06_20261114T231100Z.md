# Preregistration — FCLR-FWD-VOL-2024-DISJOINT-2024-06-20261114T231100Z

- **Status:** FROZEN_PRE_OUTCOMES
- **Preregistered (UTC):** 2026-11-14T23:11:00Z
- **Frozen before outcomes:** true
- **Outcome data inspected before freeze:** false
- **Promotable:** false
- **Max status:** EXPLORATORY_ONLY
- **Singleton diagnostic only:** true (never a fresh three-block confirmation)

## Objective
Bounded singleton attribution diagnostic on cached Binance 2024-06 to test whether estimator behavior or data lineage explains sensitivity under the frozen B0/B1/C1/C2 24h QLIKE contract (primary C2 vs B1).

## Data (cached, no network)
- Symbols: BTCUSDT, ETHUSDT, BNBUSDT, SOLUSDT, XRPUSDT
- Months: 2024-04, 2024-05, 2024-06 (mark/premium/index klines + funding) from `research_state/data_cache/*_2024_{04,05,06}` and `data/raw/*-fundingRate-2024-0{4,5,6}.csv`
- Grid extended to 2024-07-07T23:00:00Z only to materialize strictly-forward 24h targets for test origins through 2024-06-30T23:00:00Z; test evaluation rows restricted to 2024-06-01..2024-06-30.

## Split (single block)
- Train: 2024-04-25T00:00:00Z .. 2024-05-24T23:00:00Z (30 days)
- Embargo: 2024-05-25T00:00:00Z .. 2024-05-31T23:00:00Z (7 days)
- Test: 2024-06-01T00:00:00Z .. 2024-06-30T23:00:00Z (30 days)

## Models/features (frozen)
- B0: [log_rv24h]
- B1: [log_rv1h, log_rv24h, log_rv168h]
- C1: [log_rv1h, log_rv24h, log_rv168h, signed_funding, abs_fund_pct]
- C2: [log_rv1h, log_rv24h, log_rv168h, signed_funding, abs_fund_pct, premium, ema_dist]

## Estimator arms (independently testable)
- **sealed:** raw features, no scaling, no smearing, finite-row masking/drop only, ridge-stabilized OLS on log(target+eps).
- **corrected:** train-only standardization, finite-row masking, train-only Duan log-target smearing, drop-only missingness, OLS on standardized design.

## Contrasts & inference
- Paired OOS QLIKE contrasts: C2 vs B1 (primary), C1 vs B1, C2 vs C1 (24h).
- Day-block bootstrap CIs (2000 reps, seed 20261114, deterministic), Holm-adjusted p-values, LOIO (leave-one-instrument-out of training), funding-permutation placebo (200 reps, seed 20261114).
- Leakage/causality: all features strictly causal at t; targets strictly forward; no future info for scaling/fitting/threshold/imputation; 7-day embargo enforced.

## Lineage/coverage requirements
- Record source sha256, row count, key count, symbol set, span; panel hash; per-cell coverage before outcome fitting.
- Any mismatch => `INCONCLUSIVE` (not numeric).

## Verdict space (all EXPLORATORY_ONLY, promotable=false)
`EXPLAINED_BY_ESTIMATOR` | `EXPLAINED_BY_DATA` | `UNEXPLAINED` | `INCONCLUSIVE`

## Forbidden
No mutation of sealed artifacts/verdicts; no tested disjoint months 2025-06/11/12; no fresh 3-block confirmation on 2024-06; no outcome inspection before freeze; no network/paid/manual data; no confirmatory/promotion claims.
