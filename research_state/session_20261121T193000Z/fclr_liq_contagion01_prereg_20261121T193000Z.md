# FCLR-LIQ-CONTAGION-001 — Outcome-Blind Prereg Freeze

- **Experiment ID:** FCLR-LIQ-CONTAGION-001-20261121T193000Z
- **Campaign:** FCLR-LIQ-CONTAGION-001
- **Session:** session_20261121T193000Z
- **Generated (UTC):** 2026-11-21T19:30:00Z
- **Status:** FROZEN_PRE_OUTCOMES
- **frozen_before_outcomes:** **true**
- **outcome_data_inspected_before_freeze:** **false**

This prereg was frozen **before any contagion, lead-lag, Granger, permutation, funding-tercile, or temporal-stability statistic was computed**. The only prior inspection was metadata/coverage (row counts, null fractions, timestamp ranges, per-coin event counts, panel sha256) required to make the design executable. No target distribution, edge weight, causality p-value, or network metric was observed.

## Why this campaign (repository-name priority)

The repository is named *Funding-conditioned-volatility-and-liquidation-risk*, which mandates three pillars: **funding-conditioned**, **volatility**, and **liquidation risk**. No campaign to date has joined all three. FCLR-LIQ-CONTAGION-001 is the first:

- **Liquidation risk:** do liquidations in coin A predict liquidations in coin B (cross-coin contagion)?
- **Funding-conditioned:** do funding rate differentials between coins modulate that cross-coin prediction (funding-mediated spillover)?
- **Volatility:** does realized volatility in one coin predict liquidations in another (volatility spillover)?

The 1.74M event panel (15 coins, 2025-03-22 → 2026-10-31) carries `fundingRate`, `premium`, `mark`, `ema_dist`, `rv24h`, `rv168h`, `notional_usd`, `side` — everything needed, no external trigger, no paid data, no credentials.

## Frozen input (sha256 asserted in the eval script header before any read)

| Panel | Path | sha256 | Rows | Coins | Span |
|---|---|---|---|---|---|
| Combined liquidation (Track A observed) | `research_state/fclr_liq_combined_panel_20261115T181405Z.parquet` | `81a100d5…7f14` | 1,740,415 | 15 | 2025-03-22 → 2026-10-31 |

- `fundingRate`, `abs_fund_pct`, `notional_usd`, `rv24h`, `rv168h` are non-null on all rows.
- Coins: AAVE, ADA, AVAX, BNB, BTC, CRV, DOGE, ETH, LINK, LTC, NEAR, SOL, SUI, UNI, XRP.
- Sources: ironflow 1,555,142 + metpie 185,273.

## Hypotheses (frozen before outcomes)

- **H_contagion_liq:** Liquidation intensity in coin A at hour t predicts liquidation intensity in coin B at hour t+k (k=1..24h), controlling for coin B's own past liquidations and market-wide activity. Test via Granger causality on hourly aggregated counts; lead-lag cross-correlation at lags 1..24h.
- **H_contagion_funding:** Funding rate differential between coins modulates contagion strength. When funding(A) > funding(B) + threshold, liquidations in A more strongly predict liquidations in B (funding-mediated spillover). Test via funding-tercile split and interaction terms.

## Network construction

- 15×15 directed graph; nodes = coins; edge A→B present if Granger causality p < 0.01 after Bonferroni correction for 210 directed tests (alpha_adj = 0.01/210).
- Edge weight = Granger F-statistic or maximum absolute lead-lag correlation across lags 1..24h.
- Permutation test: 1000+ time-series permutations per directed pair for a null distribution of edge weights; empirical p = fraction of null weights ≥ observed weight.

## Funding conditioning

- Split each coin pair's funding rate differential into terciles (low / medium / high).
- Recompute the contagion network within each tercile.
- Test whether edge weights increase monotonically with funding differential.

## Temporal stability

- Rolling window: 90-day windows, 30-day step, over the full panel span.
- Report network density over time, edge persistence, regime-dependent contagion.

## Hourly aggregation

Collapse the event-level panel to (coin, UTC floor-hour) by event count and notional_usd sum. Build the COMPLETE hourly grid over each coin's observed span so zero-event hours are explicit zeros (flagged, not fabricated). Hourly funding = mean of fundingRate inside the hour; zero-event hours carry forward the most recent prior in-panel funding observation (funding forward-filled only, never the outcome), flagged. Hours with no prior funding are dropped and counted.

## Materiality floor

**2% relative**, frozen here, **not relaxed after outcomes**. Contagion effect must explain ≥ 2% of the variance in the target coin's liquidations; funding modulation must produce ≥ 2% relative difference between high- and low-differential terciles. A null is recorded as NOT_SUPPORTED.

## Inference

- Primary: permutation-based empirical p-values (1000+ permutations) per directed pair and edge weight.
- Multiple testing: Bonferroni across 210 directed Granger tests; Holm across the declared hypothesis family; raw and adjusted p-values both reported.
- Block bootstrap across contiguous UTC time blocks (jointly across coins), deterministic seed; leave-one-coin-out sensitivity reported.
- Strictly chronological; no random train/test split.

## Decision rule

Support for H_contagion_liq requires: (1) ≥1 directed edge significant at Bonferroni-adjusted p < 0.01; (2) signal clears the 2% materiality floor; (3) permutation null rejected (empirical p < 0.01); (4) not dominated by one coin or one time block.

Support for H_contagion_funding requires: (1) edge weight increases monotonically with funding-differential tercile; (2) interaction term significant after multiplicity correction; (3) ≥ 2% relative difference between high- and low-differential terciles.

No threshold shopping.

## Hard constraints honored

`outcome_data_inspected_before_freeze=false` · panel sha256 asserted before any read · materiality floor 0.02 frozen · observed liquidations distinct from modeled breaches · no external trigger · no network/paid data/credentials · no root-level md/json added · no `.github/workflows` modification · no overwrite of `research_state/research_protocol.md`.
