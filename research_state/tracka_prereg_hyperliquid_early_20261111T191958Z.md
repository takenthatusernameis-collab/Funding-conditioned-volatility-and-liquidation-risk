# Track A Early Observed-Liquidation Preregistration — GAP-TRACKA-EARLY-OBSERVED-2025H2_2026Q1

**Experiment ID:** TRACKA-HL-EARLY-20261111T191958Z
**Preregistered (UTC):** 2026-11-11T19:19:58Z
**Campaign:** GAP-TRACKA-EARLY-OBSERVED-2025H2_2026Q1 (Branch 2 default, mandatory while Gate 4 externally blocked)
**Track:** A
**Status:** PREREGISTERD_FROZEN_PRE_OUTCOMES — frozen BEFORE any outcome computation or panel alignment for the new claim. `research_state/tracka_prereg_hyperliquid_early_20261111T191958Z.json` is the authoritative frozen record.

## Claim
Funding-conditioned features (C2) improve out-of-sample forecasting of observed Hyperliquid perpetual liquidation intensity vs realized-volatility-only baseline (B1) on a new pre-registered admissible early window 2025-11-01..2026-04-30, disjoint from closed NOT_MET Track A 2026-05..2026-10.

## Data (admissible, unauthenticated, observed only)
- Observed labels: ironflow/hyperliquid-liquidations (CC BY 4.0), monthly parquets 2025-11..2026-04 in `research_state/data_cache/ironflow_events/`. Label = notional_usd-weighted observed liquidation event count per symbol per 24h UTC bucket.
- Funding context: cached `research_state/data_cache/hyperliquid_funding/*.json` (9 coins, ~2025-11-01..2026-10-30 hourly).
- Mark-price/RV context: NOT cached for 2025-11..2026-04 — bounded first-time unauthenticated Hyperliquid `candleSnapshot` 1h fetch for missing months only, cached under `research_state/data_cache/hyperliquid_candles/<COIN>/<YYYY-MM>.json` with `.accessed.json` + `.sha256` provenance. No re-fetch of 2026-05..2026-10.

## Window and splits (frozen pre-outcomes)
- Window: 2025-11-01T00:00:00Z .. 2026-04-30T23:59:59Z (9 symbols)
- Train: 2025-11-01 .. 2025-11-30; embargo 2025-12-01 .. 2025-12-07
- Validation: 2025-12-08 .. 2026-01-06; embargo 2026-01-07 .. 2026-01-13
- Test blocks (3 non-overlapping ~30d): 2026-01-14..2026-02-12; 2026-02-20..2026-03-21; 2026-03-29..2026-04-27
- Embargo between partitions: 7 days

## Evaluation (run only after freeze + acquisition + build)
- Primary contrast: C2 vs B1, QLIKE on next-24h observed liquidation intensity
- Materiality gate: >=2% relative QLIKE reduction, 95% CI excludes zero, >=5 paired instruments, >=3 test blocks (all required)
- Block-bootstrap CIs per pre-registered spec; no threshold-shopping; no sealed-holdout reuse; no Binance/2024 conflation; no modeled/proxy labels presented as observed

## Infeasibility rule
If panel build yields <5 paired instruments, <3 test blocks with data, or RV24h/B1 not computable → INADMISSIBLE; documented infeasibility artifact + state update; pivot to GAP-TRACKA-SYMBOL-EXPANSION-2026M05M10 under new prereg with frozen ex-ante symbol selection/event-adequacy rules.

## Gate 4 note
Branch 1 (Gate 4 / Track C confirmatory ablation) remains EXTERNAL_BLOCKED (no valid RESOLVED_VERIFIED terms evidence; human/legal review required, agent cannot set RESOLVED_VERIFIED). This prereg executes Branch 2 only.
