# FCLR-LIQ-CONTAGION-002 Prereg Freeze (Outcome-Blind)

**Experiment ID:** FCLR-LIQ-CONTAGION-002-20261121T210000Z
**Campaign:** FCLR-LIQ-CONTAGION-002
**Session:** `research_state/session_20261121T210000Z/`
**Generated UTC:** 2026-11-21T21:00:00Z
**Status:** FROZEN_PRE_OUTCOMES
**outcome_data_inspected_before_freeze:** false

## Rationale
FCLR-LIQ-CONTAGION-001 (session_20261121T193000Z, COMPLETE) disclosed an unresolved methodological discrepancy:
- eval edge set = 11 edges (Granger-Bonferroni INTERSECT permutation-Bonferroni, density 0.0524)
- independent recompute edge set = 58 edges (empirical-p only, density 0.2762)
- the two edge sets disagree on 47 of 210 directed pairs
- the declared 2% per-edge materiality floor was asserted True but never actually computed (no per-edge variance-explained field)
- funding-tercile and temporal-stability results were never reconciled against the primary edge set

FCLR-LIQ-CONTAGION-002 reuses the SAME frozen panel (no new data, no external trigger, no credentials) to compute per-edge materiality and reconcile edge-set criteria. This prereg is frozen BEFORE any reconciliation statistic is computed.

## Frozen inputs
- Combined liquidation panel: `research_state/fclr_liq_combined_panel_20261115T181405Z.parquet`
- sha256: `81a100d5d0625832bebabaabea13b786e15319577721cfe8507da5b779ec7f14`
- rows: 1,740,415; n_coins: 15; span: 2025-03-22T19:00:18Z .. 2026-10-31T22:02:10Z
- coins: AAVE, ADA, AVAX, BNB, BTC, CRV, DOGE, ETH, LINK, LTC, NEAR, SOL, SUI, UNI, XRP (210 directed pairs)
- sources: ironflow 1,555,142; metpie 185,273
- label kind: observed liquidation events (Track A)

## Hypotheses (frozen, outcome-blind)

**H_recon_materiality (recon_materiality):** When the 2% per-edge variance-explained floor is actually computed within each VAR(6) Granger regression, the number of contagion edges clearing it is reported with a confidence interval, and the claim "contagion is material" is promoted or demoted accordingly.
- Estimand: partial R-squared / variance explained in coin B's hourly liquidation intensity attributable to coin A's lagged liquidations, beyond coin B's own lags, per directed (A->B) pair.
- Materiality floor: 0.02 (2%). Frozen; not relaxed after outcomes.

**H_recon_robustness (recon_robustness):** The contagion edge set is characterised across raw p<0.01, Bonferroni (alpha=0.01/210), Benjamini-Hochberg FDR q=0.05, and permutation-empirical (1000 permutations/pair) criteria; cross-criterion Jaccard agreement is reported; edges present under only one criterion are flagged fragile. The eval-vs-recompute disagreement (47 of 210 pairs) is quantified.
- Materiality floor: 0.02 (jointly with robustness).

**H_recon_stability (recon_stability):** Block-bootstrap edge-set stability (per-edge selection frequency over 1000+ moving-block resamples) and tercile/temporal-stability reconciliation are reported against each primary criterion's edge set; an edge is "stable" only if it survives the bootstrap AND the criterion ladder.
- Materiality floor: 0.02 (stability requires bootstrap >= 0.5 median AND variance_explained >= 0.02).

## Estimator definitions
- VAR order: 6
- Model: for each directed pair (A->B), regress B's hourly liquidation count on B's own lags (1..6) plus A's lagged liquidation counts (1..6), with intercept. Restricted model: B's own lags + intercept only.
- Partial variance explained: `variance_explained = 1 - SSR_unrestricted / SSR_restricted`. This is the per-edge materiality quantity CONTAGION-001 never computed.
- Granger F-test: joint F-test of the 6 source-lag coefficients; p-value from F(6, df_resid).
- Raw p criterion: edge if Granger p < 0.01 (uncorrected).
- Bonferroni criterion: edge if Granger p < 0.01 / 210.
- BH-FDR criterion: edge if Granger p passes Benjamini-Hochberg step-up at q=0.05 across 210 tests.
- Permutation-empirical criterion: 1000 time-series permutations per pair; shuffle source series, recompute Granger F; empirical p = fraction of null F >= observed F; edge if empirical p < 0.01.
- Jaccard: |A ∩ B| / |A ∪ B| over directed-pair edge sets.
- Funding tercile: split hours by pair-level funding-rate differential into low/medium/high; recompute network within each tercile; Jaccard vs each primary criterion.
- Temporal stability: rolling 90-day and 30-day windows, 30-day step; Jaccard vs each primary criterion.
- Block bootstrap: 1000+ moving-block resamples of the hourly panel (contiguous UTC blocks, jointly across coins), deterministic seed 20261121; per-edge selection frequency + 95% stability interval.

## Hourly aggregation
Collapse the event-level panel to (coin, UTC floor-hour) by count of events and sum of notional_usd. Build the complete hourly grid so zero-event hours are explicit zeros (has_event=False; never silently fabricated). Funding predictor = mean fundingRate within the hour; zero-event hours use forward-fill of funding only (never of the outcome), flagged funding_is_ffill=True. Hours with no prior funding are dropped and counted. Inputs: notional_usd (count+sum), fundingRate (hourly mean), rv24h, rv168s, mark, ema_dist. Expected ~50,000 hourly coin-observations (~14,000 per coin).

## Inference
- Primary SE: analytical F-test p-values plus permutation-empirical p-values (1000 permutations/pair).
- Multiple testing: Bonferroni across 210 directed Granger tests; BH-FDR q=0.05; raw p<0.01; permutation-empirical p<0.01. All four reported with edge-set sizes and pairwise Jaccard.
- Block bootstrap: contiguous UTC blocks jointly across coins; deterministic seed; per-edge selection frequency + 95% interval.
- No random train/test split; strictly chronological.

## Decision rules
- H_recon_materiality SUPPORTED only if per-edge variance_explained is computed for all 210 pairs, the count clearing the 0.02 floor is reported with a bootstrap CI, and that count > 0; otherwise NOT_SUPPORTED.
- H_recon_robustness SUPPORTED only if edge-set size and pairwise Jaccard are reported for all four criteria, the 47-of-210 eval-vs-recompute disagreement is quantified, and single-criterion edges are flagged fragile.
- H_recon_stability SUPPORTED only if per-edge bootstrap selection frequency + 95% interval and tercile/rolling Jaccard are reported, and stability requires bootstrap + ladder + materiality jointly.
- A null is recorded as NOT_SUPPORTED. No threshold shopping. Materiality floor not relaxed after outcomes.

## Hard constraints honored
- outcome_data_inspected_before_freeze=false; panel sha256 asserted in script headers before any read.
- No random train/test split; strictly chronological.
- Materiality floor 0.02 frozen; nulls preserved as NOT_SUPPORTED.
- Observed liquidations distinct from modeled boundary breaches (Track A observed events only).
- No external trigger; frozen panel sole input; no network/paid data/credentials/new data acquisition.
- No root-level research_state/*.md|*.json (root churn cap 499/500); all artifacts under `research_state/session_20261121T210000Z/`.
- No .github/workflows modification; no overwrite of research_state/research_protocol.md.
- No zero-byte placeholder files; no empty session directory.
- Recompute is a separate stdlib/numpy code path (no shared helpers with recon script).
