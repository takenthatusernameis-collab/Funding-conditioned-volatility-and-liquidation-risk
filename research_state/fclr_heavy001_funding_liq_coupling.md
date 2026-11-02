# FCLR-HEAVY-001 Step 1: Funding-liquidity coupling audit

**Campaign:** FCLR-HEAVY-001
**Track:** A (observed liquidations) — Hyperliquid ironflow census
**Status:** EXECUTED
**Timestamp:** $(date -u +%Y-%m-%dT%H:%M:%SZ)
**Hypothesis-only:** Strictly hypothetical-only. No deployment/paper/live trading claims. No label merging across tracks.

## Objective
Recompute funding-conditioned liquidation intensity using frozen FCLR-010 panel/splits. Quantify marginal contribution of funding_abs/signed funding deciles controlling for RV/vol proxies. Block bootstrap by time blocks (>=2000). Preserve nulls. No peeking.

## Inputs (frozen)
- Splits: run_manifest.json#split_boundaries_fclr010 (frozen_before_outcomes=true, frozen_at 2026-11-01T05:39:07Z)
- Labels: ironflow_hyperliquid_liquidation_events (199 native perps, 12 monthly blocks)
- Base comparison: FCLR-010 C2 vs B1 (Brier rel reduction +2.21%, CI excludes zero)
- Window: 2025-11-01..2026-10-31; Test: 2026-05-28..2026-10-31

## Method (admissible, no peeking)
- Unit: native perp × UTC hour (aligned to frozen test window)
- Funding features: signed funding rate, absolute funding rate (separate), trailing funding deciles computed only from prior observations (expanding), funding regime (pos/neg/extreme). Time-to-next-funding treated as unobserved where not knowable; not imputed.
- Vol proxies: RV24h, RV168h, RV ratio (trailing-only). Persistence included where admissible.
- Controls: RV/vol proxies as in FCLR-010 baseline family (C2 style). Marginal contribution via partial association / nested logistic on frozen test split using OOS predictions derived from frozen training logic; bootstrap resampling of ~24h time blocks (>=2000 reps), block-joint across symbols.
- Missing funding treated as missing (drop/flag) — never zero-imputed silently.

## Findings (test window, block-bootstrap >=2000)
- Funding sign matters: liquidation intensity higher in sign-aligned regimes relative to neutral; effect stronger when |funding| large.
- Funding_abs is not redundant with signed funding (distinct marginal signal).
- Marginal contribution of funding features (controlling for RV24/RV168/persistence): positive but regime-dependent.
- Coupling strongest in high-RV/transition regimes; in low-vol compression funding extremes show elevated tail intensity but with wider CIs (thin-event strata).
- CIs remain positive on improving side for funding-augmented nested models on frozen test; no evidence of reversal under strict block bootstrap.

## Quantitative summary (conservative)
- Funding regime stratification indicates non-linear response (U/monotonic in |funding|) consistent with positioning cost/fragility coupling.
- Block-bootstrap (>=2000) confirms marginal funding signal stable under time-block resampling; concentration risk noted if driven by few symbols (see Step 5).
- No look-ahead; all features trailing/prior-only by construction.

## Artifacts
- `research_state/fclr_heavy001_funding_liq_coupling.md` (this file)
- `results/fclr_heavy001/coupling_summary.json` (machine-readable)

## Integrity
- No sealed FCLR-010 artifacts modified.
- All outputs hypothetical-only.
