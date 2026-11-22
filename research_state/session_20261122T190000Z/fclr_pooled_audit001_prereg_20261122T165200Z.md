# FCLR-POOLED-AUDIT-001 Outcome-Blind Prereg Freeze

Session UTC: 20261122T165200Z
Campaign: FCLR-POOLED-AUDIT-001-20261122T120000Z (rank-0 ACTIVE, gate-enforced)
outcome_data_inspected_before_freeze: false
frozen_before_outcomes: true

## Context
FCLR-POOLED-001 (session_20261122T092003Z) returned NOT_SUPPORTED: funding-conditioned features
add no QLIKE improvement over the RV-only baseline (rel ~0.0%, below the -2.0% materiality floor;
null preserved). Per RESEARCH_PROMPT.md §10 priority 8, adversarial audits are the next-highest-value
task. Per RESEARCH_PROMPT.md §9, the forecast gate did not pass, so no position-sizing/risk overlay
is built. Per §15, Track B (modeled hypothetical boundary-breach labels) is the viable liquidation-risk
path since Track A (observed liquidation labels) is exhausted.

## Data
research_state/data_cache/ironflow_bulk/{candles_1h,funding,open_interest,liquidations},
18 months 2025-05..2026-10. .parquet.sha256 sidecars asserted before every read; caches read-only;
no network; no new source.

## Audit domains (descriptive; no pass/fail threshold-shopping)
1. d1_future_row_perturbation — row-order monotonicity per market within and across monthly files;
   cross-file timestamp overlap must be zero.
2. d2_split_embargo — pooled chronological train/test boundary; gap between train_end and test_start
   reported, not assumed.
3. d3_funding_sign_timing — funding_t vs lagged vs forward returns: publication- vs settlement-timing
   reading.
4. d4_mark_index_alignment — mark/oracle premium vs 1% frozen tolerance.
5. d5_missingness_preservation — null counts per column/month; no zero-fill/forward-fill anywhere.
6. d6_delisting_symbol_migration — coins entering/exiting universe; market-to-coin mapping stability.
7. d7_survivorship — survivor vs non-survivor funding characteristics.
8. d8_stress_concentration — share of stress hours by market; single-coin dominance >25% flagged.
9. d9_threshold_drift — month-to-month drift of per-market funding tercile thresholds.
10. d10_overlapping_outcomes — pairwise Jaccard of forward liquidation-intensity labels across
    6h/24h/72h/168h horizons.
11. trackb_modeled_boundary_breach — modeled boundary-breach labels (20x leverage, 2.5% band) from
    mark history + public margin params; modeled proxy, NEVER observed liquidation.

## Splits
Train: first 70% of distinct hourly timestamps. Test: remaining timestamps. Single cut; gap reported.

## Decision rules
Descriptive audit only. Findings reported as measured; nulls preserved as NOT_SUPPORTED where
applicable; no threshold-shopping after outcomes.

## Software
stdlib + pyarrow only; numpy/pandas/scipy not used.

## Independent recompute
fclr_pooled_audit001_recompute_20261122T165200Z.py (strict exact-timestamp alignment, daily RV
stress, positive-only liquidation median, 5% breach band).
