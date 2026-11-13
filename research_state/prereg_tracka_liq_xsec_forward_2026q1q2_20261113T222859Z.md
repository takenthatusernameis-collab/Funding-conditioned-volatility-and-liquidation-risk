# Preregistration — TRACKA-LIQ-XSEC-FORWARD-20261113T222859Z

- **Experiment:** `TRACKA-LIQ-XSEC-FORWARD-20261113T222859Z`
- **Campaign:** `FCLR-FORWARD-LIQ-2026Q1Q2`
- **Arm/Track:** B / `A_liquidation`
- **Status:** `FROZEN_PRE_OUTCOMES`
- **Preregistered (UTC):** 2026-11-13T22:28:59Z
- **Flags:** `pre_registered_before_outcomes=true`, `frozen_before_outcomes=true`, `outcome_data_inspected_before_freeze=false`, `promotable=false`

## Claim (exploratory, max EXPLORATORY_ONLY)
On the unopened forward Hyperliquid native-perp cross-section (2026-01-18..2026-04-30), a funding-conditioned score carries information about the RELATIVE ordering of next-24h observed liquidation intensity across coins (cross-sectional rank IC and top-minus-bottom spread), using the same estimand/inference as Arm B `TRACKA-LIQ-XSEC-20261112T201536Z`.

## Data (on-disk, offline, no network/credentials)
- Liquidations (observed only, CC-BY-4.0): `research_state/data_cache/ironflow_bulk/liquidations/<2026-01..2026-04>.parquet`
- Candles 1h: `research_state/data_cache/ironflow_bulk/candles_1h/<2025-12,2026-01..2026-04>.parquet` (2025-12 tail for 24h rv warm-up only)
- Funding: `research_state/data_cache/ironflow_bulk/funding/<2025-12,2026-01..2026-04>.parquet`
- No venue mixing; no modeled/proxy/synthetic labels; no May 2026 or sealed windows.

## Universe (coverage-only, frozen ex ante)
Native perps (`market` ends `-PERP`, no `:`) with >=20 observed liquidation-days and >=100 observed liquidation events over 2026-01-18..2026-04-30, and complete hourly candle+funding coverage over test window 2026-02-10..2026-04-30. Selection uses only label existence/coverage (not magnitude/direction/timing/result). Pre-coverage eligible: 113 coins / 192 native perps; final universe <=113 (coverage filter only). Min 5.

## Splits (exact; 7-day embargo preserved)
- Burn-in (never scored): 2026-01-18T00:00:00Z..2026-02-02T23:59:59Z (16 days)
- Embargo 7d: 2026-02-03..2026-02-09
- Block 0 target: 2026-02-10T00:00:00Z..2026-03-11T23:00:00Z (scored decision days 02-10..03-10 = 29)
- Embargo 7d: 2026-03-12..2026-03-18
- Block 1 target: 2026-03-19T00:00:00Z..2026-04-03T23:00:00Z (scored decision days 03-19..04-02 = 15)
- Embargo 7d: 2026-04-04..2026-04-10
- Block 2 target: 2026-04-11T00:00:00Z..2026-04-30T23:00:00Z (scored decision days 04-11..04-29 = 19)
- Total 16+7+30+7+16+7+20 = **103 days**. Block end is target horizon (builder scores start..end-1 day). Scored decision days = 63, last 2026-04-29 targeting [2026-04-30,2026-05-01). d=2026-04-30 forbidden. Labels end 2026-04-30T23:48:51Z.

## Features / Score (identical to Arm B)
At bucket start d (data at/before d only): `rv24h` (trailing 24h realized variance from hourly closes), `funding_rate`, `abs_funding`, `premium` (as-of latest). Score = within-bucket z(funding_rate) + z(abs_funding).

## Estimand / Inference (identical to Arm B)
- Primary: Spearman rank IC of score vs next-24h observed liquidation event count per 30-day block on pooled cross-section.
- Secondary: top-k minus bottom-k next-24h notional spread (k=10% of universe, floor 5).
- Inference: within-bucket permutation 1000 reps, seed 20261112; null 5th/95th percentiles and empirical p per block/pooled.
- Materiality: |mean IC| >= 0.05 AND spread sign consistent >=2/3 blocks.

## Decision rule
- `EXPLORATORY_SIGNAL`: criteria met -> EXPLORATORY_ONLY, never promoted.
- `EXPLORATORY_NULL`: criteria not met -> null with exact failing minima.
- `INADMISSIBLE`: <5 coins or <3 blocks -> infeasibility with exact minima (do not weaken MIN_COINS).

## Forbidden
No promotion/confirmation claims; no May 2026/sealed/earlier-than-2025-12 reads (except 2025-12 warm-up); no venue mixing; no modeled/proxy/synthetic labels; no threshold shopping/tuning; no .github/workflows edits; no raw parquet commits.
