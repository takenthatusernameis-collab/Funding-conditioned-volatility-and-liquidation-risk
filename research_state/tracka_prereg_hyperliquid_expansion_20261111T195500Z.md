# Track A Symbol-Expansion Preregistration — GAP-TRACKA-SYMBOL-EXPANSION-2026M05M10

**Experiment ID:** TRACKA-HL-EXPANSION-20261111T195500Z
**Preregistered (UTC):** 2026-11-11T19:55:00Z
**Campaign:** GAP-TRACKA-SYMBOL-EXPANSION-2026M05M10 (pivot from GAP-TRACKA-EARLY-OBSERVED-2025H2_2026Q1, closed INADMISSIBLE with documented evidence)
**Track:** A
**Status:** PREREGISTERD_FROZEN_PRE_OUTCOMES — frozen BEFORE any outcome computation or forecast evaluation. JSON record is authoritative.

## Pivot rationale
GAP-TRACKA-EARLY-OBSERVED-2025H2_2026Q1 (TRACKA-HL-EARLY-20261111T191958Z) is closed INADMISSIBLE: bounded first-time unauthenticated Hyperliquid `candleSnapshot` acquisition for 2025-11..2026-04 x 9 coins completed with provenance (54 calls, HTTP 200), but candles/RV are absent for 2025-11..2026-03 (empty `[]` for all coins) and partial for 2026-04 (~327-328 rows); RV24h/B1 baseline not computable; pre-registered minima unsatisfiable. No outcome computation was performed for the early claim. Evidence: `research_state/evaluation_summary_TRACKA-HL-early-infeasible-20261111T193500Z.md`.

## Claim
Funding-conditioned features (C2) improve OOS forecasting of observed Hyperliquid perpetual liquidation intensity vs RV-only baseline (B1) on an EXPANDED-SYMBOL panel over 2026-05-01..2026-10-31 (or prereg subwindow), using a NEW symbol universe selected ex ante by frozen rules from cached ironflow observed labels. Different universe/design from closed NOT_MET `TRACKA-HL-S-20261111T133430Z` (9 symbols, same window); that panel is NOT relitigated.

## Data (admissible, unauthenticated, observed only)
- Observed labels: ironflow/hyperliquid-liquidations (CC BY 4.0), cached `research_state/data_cache/ironflow_events/2026-05..2026-10.parquet` (432 PERP markets cached). Label = notional_usd-weighted observed liquidation event count per symbol per 24h UTC bucket.
- Funding: cached `research_state/data_cache/hyperliquid_funding/*.json` for 9 coins (~2025-11-01..2026-10-30 hourly); candidates beyond 9 require bounded first-time unauthenticated fundingHistory fetch with provenance.
- Candles/RV: cached `research_state/data_cache/hyperliquid_candles/<COIN>/2026-05..2026-10.{json,accessed.json,sha256}` for 9 coins; candidates beyond 9 require bounded first-time candleSnapshot fetch with provenance. No re-fetch of cached data.

## Ex-ante symbol selection (frozen; no post-hoc/cherry-picked selection)
1. Rank candidate base symbols by ex-ante observed label notional_usd sum over cached ironflow 2026-05..2026-10 (label-only computation, not an outcome).
2. Universe candidates (frozen): ADA, LTC, DOT, TRX, ATOM, BCH, ETC, FIL, ICP, NEAR, ALGO, VET, HBAR, FTM, AAVE, UNI, CRV, SNX, COMP, MKR, SUSHI, 1INCH, BAL, BNT, CTSI, ENJ, IOTA, KSM, NU, OCEAN, OMG, ONT, QTUM, ZEC, ZIL, CELO, CHZ, IOST, HOT, MTL, NEXO, PNT, REN, RSR, STMX, TROY, WAN, WAVES, ZRX.
3. Exclude: closed 9 (BTC,ETH,BNB,SOL,XRP,AVAX,DOGE,LINK,SUI); prefixes cash:/flx:/hyna:/io:/km:/mkts:/para:/vntl:/xyz: and kBONK/kFLOKI/kLUNC/kNEIRO/kPEPE/kSHIB; stablecoin/fiat perps.
4. Include: >0 observed events in >=2 of 6 cached label months and nonzero label variance across test blocks (event-adequacy, label-only).
5. Final universe: >=5 symbols, selection fixed pre-outcomes subject to funding+candle acquirability via bounded first-time acquisition.

## Window and splits (frozen pre-outcomes)
- Window: 2026-05-01T00:00:00Z .. 2026-10-31T23:59:59Z; subwindow only if coverage incomplete after bounded acquisition (recorded in build report).
- Train: 2026-05-01 .. 2026-05-31; embargo 2026-06-01 .. 2026-06-06
- Validation: 2026-06-07 .. 2026-06-30; embargo 2026-07-01 .. 2026-07-06
- Test blocks: 2026-07-07..2026-08-06; 2026-08-13..2026-09-11; 2026-09-18..2026-10-17 (3 non-overlapping ~30d)
- Embargo: 7 days between partitions

## Evaluation (run only after freeze + acquisition + build)
- Primary contrast: C2 vs B1, QLIKE on next-24h observed liquidation intensity
- Materiality gate: >=2% relative QLIKE reduction, 95% CI excludes zero, >=5 paired instruments, >=3 test blocks (all required)
- Block-bootstrap CIs per pre-registered spec; no threshold-shopping; no sealed-holdout reuse; no Binance/2024 conflation; no modeled/proxy labels

## Infeasibility rule
If panel build yields <5 paired instruments, <3 test blocks with data, RV24h/B1 not computable, or zero label variance → INADMISSIBLE; documented infeasibility artifact + state update; pivot to GAP-VOLATILITY-UNTESTED-ADMISSIBLE-PANELS or hold (no unsupported claim).

## Gate 4 note
Branch 1 (Gate 4 / Track C confirmatory ablation) remains EXTERNAL_BLOCKED (human/legal Binance terms evidence; fabricated=false). Agent cannot set RESOLVED_VERIFIED. This prereg executes the symbol-expansion pivot only.

## Required sequence (heavy, no status-only)
1) Bounded first-time unauthenticated probe acquisition: fundingHistory + candleSnapshot 2026-05..2026-10 for top ex-ante candidates (excluding closed 9), provenance recorded; admissibility confirmed before build.
2) Apply ex-ante symbol selection; constitute final universe; document inclusion/exclusion.
3) Build deterministic RV-augmented panel; emit panel parquet + build report (hashes, coverage, leakage/embargo notes).
4) Run pre-registered C2 vs B1 evaluation; emit evaluation_summary verdict.
5) Atomic state updates (experiment_frontier.json, hypothesis_registry.json, run_manifest.json, final_confirmatory_verdict.md addendum); sealed 2024 H001 and closed Track A NOT_MET records preserved.
