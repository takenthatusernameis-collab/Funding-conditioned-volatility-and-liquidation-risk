# FCLR-LIQ-XSEC-BROAD-01 — Outcome-Blind Prereg Freeze

**Experiment ID:** FCLR-LIQ-XSEC-BROAD-01
**Campaign:** FCLR-LIQ-XSEC-BROAD-01-20261123T080000Z
**Session UTC:** 20261123T085507Z
**Phase:** PREREG_FREEZE_ON_BROAD_UNIVERSE
**Outcome data inspected before freeze:** false
**Decision frozen before outcomes:** true

## Estimand

Out-of-sample, regime-conditioned, cross-sectional association between a funding feature and NEXT-HOUR observed liquidation intensity, tested for GENERALIZATION from the 15-coin combined metpie+ironflow panel (FCLR-XSEC-004/005/006, promotable=false) to the full on-disk ironflow_bulk liquidation universe.

This is a cross-sectional/ordering claim, NOT a time-series forecast gate. Reported as such; never as an observed-liquidation forecast gate pass.

## Label construct (observed ironflow liquidations, capped-sample feed — NOT a complete census)

Per-coin per-hour observed liquidation intensity = event count and notional_usd sum from `ironflow_bulk/liquidations` (columns: timestamp[ms], market, coin, position_side, size, notional_usd, avg_price, ...). Long/short sides kept separate. Absence from this feed is NOT zero; claims restricted to presence/intensity ordering, never a binary absence/presence census.

Targets: next_hour_count, next_hour_notional. Sides: long, short. Horizon: 1h.

## Universe

Full 342+ coin ironflow_bulk liquidation universe for 2025-05..2026-10. Do NOT restrict to the 15-coin combined panel and do NOT substitute present-day survivors for the historical universe; report per-coin coverage and the exited/survivor split.

## Features (all known at origin)

- Primary: signed funding rate (latest observation available by origin hour t, retaining sign separately)
- Secondary: abs_funding_percentile (train-only rolling), mark/oracle premium dislocation, trailing RV24/RV168, trailing MA deviation
- Sources: ironflow_bulk/funding (funding_rate, premium), ironflow_bulk/open_interest (mark_price, oracle_price), ironflow_bulk/candles_1h (close)
- Normalization: train-only means and standard deviations; no full-sample quantiles

## Regime variable (frozen)

RV-tercile (low/mid/high) AND UTC-session bucket (Asian/European/US) — the SAME regime conditioning that produced the SUPPORTED narrow-universe findings. Computed with EXPANDING train-only thresholds so no future information leaks into the regime label.

UTC buckets: Asian [0,8), European [8,16), US [16,24).

## Design

Chronological walk-forward. Train on the earlier portion (60%); evaluate on non-overlapping forward test blocks (168h; >=3 non-overlapping test blocks required across the forward span; 48h purge+embargo; features normalized with train-only parameters; no full-sample quantiles).

## Metrics

Primary: cross-sectional Spearman rank-IC, mean rank-IC across test blocks.
Secondary: top-decile precision, top-decile recall, alert-budget precision-recall.
Contrast: cross-sectional ordering of predicted vs realized next-hour intensity across coins within each test block.

## Uncertainty

- Per-coin block bootstrap: >=2,000 deterministic-seed replicates; resample complete UTC time blocks jointly across coins; CI95 percentile [2.5, 97.5].
- Leave-one-instrument-out: >=6/8 held-out subsets pass (reproduce narrow-universe sign/direction).
- Placebo/permutation null: permute the funding feature within each test block; >=1,000 replicates; the true effect must exceed the 95th percentile of the null to be credible.

## Materiality floor

Frozen pre-specified effect size: narrow-universe sign/direction must be reproduced at broad breadth. Never relaxed after outcomes. The primary question is GENERALIZATION, not a new threshold to shop.

## Multiplicity

Holm step-down across declared family: RV_tercile_arm, UTC_bucket_arm, count_target, notional_target, long_side, short_side. Report raw and Holm-adjusted p-values.

## Verdict rule (symmetric, frozen)

SUPPORTED_GENERALIZATION iff:
1. narrow-universe sign/direction reproduced at broad breadth, AND
2. block-bootstrap CI95 excludes the null in the favorable direction, AND
3. Holm-adjusted primary p < alpha_k;

Otherwise NOT_SUPPORTED (null preserved honestly; a broad-universe failure to generalize is itself the durable finding). No threshold shopping; no relabeling.

## Sign convention (EVIDENCE NOTE compliance)

`relative_improvement = (baseline - candidate) / baseline`, positive = candidate better. Used identically in the eval AND the recompute. The recompute asserts `all_checks_match:true` against the eval.

## Input hash assertions

- Panel SHA-256: `09377b01aeebdf6a6dca527f1298586d441f65b6648b81178e28523e0e3e2923`
- Panel hash method: SHA-256 of concatenated `path|sha256|rows` across all 72 ironflow_bulk parquet files (dataset|month sorted)
- SHA-256 sidecars asserted before every read; caches read-only, not mutated; no network for heavy evaluation

## Status vocabulary

SUPPORTED_GENERALIZATION / NOT_SUPPORTED (symmetric, frozen)

**Generated UTC:** 2026-11-23T08:55:07Z
