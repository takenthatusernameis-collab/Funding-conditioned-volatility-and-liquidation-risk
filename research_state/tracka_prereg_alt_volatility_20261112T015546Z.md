# TRACKA-ALT-VOL-20261112T015546Z — Preregistration (Frozen Pre-Outcomes)

**Preregistered UTC:** 2026-11-12T01:55:46Z
**Campaign:** GAP-VOLATILITY-ALTERNATE-DESIGN
**Track:** A
**Status:** PREREGISTERED_FROZEN_PRE_OUTCOMES

**Pivoted from:** `TRACKA-EXP-ROBUST-20261112T015119Z` FRAGILE (LOIO FAIL, Placebo/Permutation FAIL). Volatility family `TRACKA-VOL-FAMILY-20261112T005111Z` completed NOT_MET (Holm across 12 comparisons). Sealed PASS `TRACKA-HL-EXPANSION-20261111T195500Z` preserved.

**Claim:** An alternate volatility forecast design on the cached Hyperliquid panel (2025-11..2026-10, 9 core coins) with a DIFFERENT pre-specified horizon, feature set, and/or split structure from the NOT_MET `TRACKA-VOL-FAMILY-20261112T005111Z` will demonstrate incremental forecast skill of funding-conditioned features (C2) over RV-only baseline (B1) for realized variance forecasting.

**Hypothesis ID:** `H_tracka_hl_alt_volatility_forecast` (primary_tracka_alt_volatility)
**Venue:** hyperliquid_perpetuals
**Data Source:** Hyperliquid API (unauthenticated) — fundingHistory + candleSnapshot 1h, cached with provenance, 9 coins, 2025-11..2026-10, observed_only=true, modeled_or_proxy=false

## Panel Construction
- **Source Artifacts:** `research_state/data_cache/hyperliquid_funding/` (9 coins, ~2025-11..2026-10) + `research_state/data_cache/hyperliquid_candles/` (9 coins, 2025-11..2026-10)
- **Coins:** AVAX, BNB, BTC, DOGE, ETH, LINK, SOL, SUI, XRP
- **Time Window:** 2025-11-01T00:00:00Z .. 2026-10-31T23:59:59Z
- **Target Horizon:** 6h (DIFFERENT from prior family's primary 24h)
- **Target Definition:** Realized variance over next 6 hours (6 x 1h log returns squared sum)
- **RV Features:** RV1h, RV24h, RV72h, RV168h computed from 1h candles (causal, trailing-only)
- **Funding Features:** fundingRate, abs_fund_pct (trailing 90-day percentile)
- **Price Features:** premium (mark/index), ema_dist (24-period EMA distance)
- **Merge:** Causal merge_asof on 1h grid, then aggregate to 6h horizon buckets

### Feature Sets
| Model | Features |
|-------|----------|
| B1 | log(rv1h), log(rv24h), log(rv168h) |
| C1 | B1 + fundingRate, abs_fund_pct |
| C2 | C1 + premium, ema_dist, rv72h |

### Split Boundaries (FROZEN, DIFFERENT from TRACKA-VOL-FAMILY)
- **Embargo:** 7 days between partitions
- **Train:** 2025-11-01T00:00:00Z .. 2026-02-28T23:00:00Z
- **Validation:** 2026-03-07T00:00:00Z .. 2026-04-30T23:00:00Z
- **Test Blocks (5 × 30-day, non-overlapping):**
  1. 2026-05-07T00:00:00Z .. 2026-06-06T23:00:00Z
  2. 2026-06-13T00:00:00Z .. 2026-07-13T23:00:00Z
  3. 2026-07-20T00:00:00Z .. 2026-08-19T23:00:00Z
  4. 2026-08-26T00:00:00Z .. 2026-09-25T23:00:00Z
  5. 2026-10-02T00:00:00Z .. 2026-10-31T23:00:00Z
- **n_test_blocks:** 5 (vs 3 in prior volatility family)
- **Note:** DIFFERENT split structure from TRACKA-VOL-FAMILY (which used 2026-05..2026-10). This uses full cached window 2025-11..2026-10 with 5 test blocks. Target horizon 6h (vs 24h primary in prior family).

## Models & Contrast
- **Baselines:** B1 (RV-only)
- **Models:** C2 (full funding + price + RV)
- **Primary Contrast:** C2 vs B1
- **Primary Target:** next-6h realized variance
- **Metric:** QLIKE (lower is better)

## Materiality Gate (Identical to Prior Volatility Family)
- min_relative_reduction_pct: 2.0
- ci_excludes_zero: true
- min_paired_instruments: 5
- min_test_blocks: 3
- all_required: true

## Event Adequacy Rule
Claim-worthy only if after deterministic panel build: ≥5 paired instruments with RV/target coverage in test blocks, ≥3 non-overlapping 30-day test blocks with data, RV features computable for test blocks, target variance >0 across test blocks; otherwise INADMISSIBLE → emit documented infeasibility + state update.

## Multiplicity
Single primary contrast (C2 vs B1) on single pre-specified horizon (6h). No family-wise correction needed. Secondary contrasts (C1 vs B1, C2 vs C1) reported but not gated.

## Forbidden (Binding)
- No outcome inspection before preregistration freeze
- No threshold-shopping on test set
- No sealed-holdout reuse (FCLR-002/FCLR-003/Track B/C/Track A volatility family test sets sealed)
- No Binance/2024 conflation (Hyperliquid only)
- No modeled/proxy/synthetic labels (observed mark prices only)
- No redundant network polling (all data cached with provenance)
- No post-hoc horizon/feature/split selection based on outcomes
- No agent-set RESOLVED_VERIFIED/fabricated=true; no Gate 4 bypass
- No mutation of sealed/closed verdicts (TRACKA-VOL-FAMILY-20261112T005111Z, TRACKA-HL-EXPANSION-20261111T195500Z, etc.)

## Atomic State Updates Required (Mandatory)
1. `research_state/experiment_frontier.json`
2. `research_state/hypothesis_registry.json` (add `H_tracka_hl_alt_volatility_forecast` status)
3. `research_state/run_manifest.json` (run `ALT-VOL-20261112T015546Z`)
4. `research_state/final_confirmatory_verdict.md` (append addendum)

## Gate 4 Note
Gate 4 Branch 1 remains EXTERNAL_BLOCKED (no valid RESOLVED_VERIFIED terms evidence; human/legal review required; agent cannot set RESOLVED_VERIFIED). This prereg executes the alternate volatility design only.