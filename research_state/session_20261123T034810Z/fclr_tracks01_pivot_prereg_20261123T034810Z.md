# FCLR-TRACKB-MODELED-BREACH-01 — Pivot Prereg (outcome-blind, frozen before outcomes)

## Campaign
FCLR-TRACKA-SOURCE-AUDIT-01-20261122T225107Z

## Session UTC
20261123T034810Z

## Experiment ID
FCLR-TRACKB-MODELED-BREACH-01 (new ID; NOT a re-run of any terminal campaign).

## Track
B — modeled boundary-breach proxy only, per RESEARCH_PROMPT.md section 15.
Does NOT reconstruct account-specific liquidation engines, cross/portfolio margin,
or actual forced liquidations. Never described as observed liquidations.

## Outcome-blind freeze
- `prereg_frozen_before_outcomes`: true
- `outcome_data_inspected_before_freeze`: false
- All input file hashes bound below; no outcome statistics inspected before this freeze.

## Label (modeled proxy ONLY)
For each coin and each forecast origin, take the observed mark-price path; compute a
hypothetical liquidation boundary from a frozen leverage/maintenance-margin scenario;
label `breach=1` if the forward mark price crosses the boundary within the horizon.
Long and short labels are kept strictly separate.

- Horizon: 24h
- Leverage: 5.0
- Maintenance margin rate: 0.0
- Entry price: mark_price at forecast origin t
- Boundary long: entry_price * (1 - 1/leverage + maintenance_margin_rate)
- Boundary short: entry_price * (1 + 1/leverage - maintenance_margin_rate)
- Crossed long: min(mark_price[t+1..t+horizon]) <= boundary_long
- Crossed short: max(mark_price[t+1..t+horizon]) >= boundary_short
- Label long: int(crossed_long); Label short: int(crossed_short)
- No leakage: only prices strictly after origin t (t+1..t+horizon)
- Primitive: scripts/synthetic_boundary_labels.py

## Data (on-disk, sha256-verified, caches not mutated)
research_state/data_cache/ironflow_bulk/
- open_interest/ (mark_price, oracle_price, open_interest) — mark_price used for boundary path
- funding/ (funding_rate, premium)
- candles_1h/ (OHLC)
- 18 monthly parquet 2025-05..2026-10, 342 coins
- All .parquet.sha256 sidecars asserted before every read

## Features (all known at origin, §7)
- Baseline B1 = trailing RV only: RV6/RV24/RV168 log-scaled, lagged-vol persistence
- Candidate C2 = B1 + signed funding + |funding| percentile (train-only rolling) + premium/mark-to-index dislocation + trailing MA deviation
- Features normalized with train-only parameters; no full-sample quantiles

## Model
- Simple calibrated logistic regression for P(breach)
- stdlib Newton/IRLS; linear-probability fallback if separation is severe
- No unconstrained ML

## Splits (§8)
- Chronological walk-forward (60/40 train/test)
- 48h purge + embargo
- Non-overlapping 168h (7-day) test blocks
- ≥3 non-overlapping test blocks required
- Features normalized with train-only parameters

## Metrics (§8 binary)
- Primary: Brier score + log loss
- Secondary: calibration slope/intercept; ROC-AUC; precision/recall at pre-specified alert budget
- Out-of-sample loss relative to RV-only baseline with block-aware (per-coin block bootstrap) CIs

## Materiality floor
- ≥ 2% relative Brier improvement (frozen; never relaxed after outcomes)

## Multiplicity
- Holm across declared family: primary count + long arm + short arm + survivor/exited arms
- Report raw and adjusted
- Sequential alpha-spending: alpha_k = 0.05 / (k * (k + 1)), k frozen

## Verdict rule (symmetric, frozen)
- SUPPORTED iff materiality met AND bootstrap CI excludes null in the favorable direction AND Holm-adjusted primary p < alpha_k
- Otherwise NOT_SUPPORTED (preserve the null honestly)
- No threshold-shopping

## Input hash binding
All 54 input parquet file hashes plus scripts/synthetic_boundary_labels.py are bound in
fclr_tracks01_pivot_prereg_20261123T034810Z.json. Any change to inputs invalidates this prereg.

## Generated
2026-11-23T03:48:10Z
