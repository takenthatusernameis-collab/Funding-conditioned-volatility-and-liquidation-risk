# Preregistration — TRACKA-HL-EARLY4H-2025H1-LIQ-GLM-ROBUST

**Campaign:** FCLR-EARLY4H-2025H1-LIQ-GLM-ROBUST v1
**Frozen (UTC):** 2026-11-12T16:52:34Z
**Status:** FROZEN BEFORE OUTCOMES
**Successor to:** TRACKA-HL-EARLY4H-2025H1-LIQ-GLM (parent verdict `INCONCLUSIVE_NUMERICAL_INSTABILITY`)

## Why

The parent `liq` GLM was unstable in exactly one place: **test block 3 (Oct-2025 funding spike)**, where `fundingRate` / `premium` / `ema_dist` are 27.7× / 12.5× / 4.5× outside the training range. Blocks 0-2 are stable. The fix is a bounded-feature re-specification of the **same** Poisson/quasi-Poisson log-link estimator.

## Reused frozen inputs

- Panel: `research_state/tracka_hl_early2025h1_panel_20261112T145529Z.parquet` (SHA-256 `08c60803…`)
- Splits, universe, minima, materiality: identical to `134503Z`.
- Diagnostic: `research_state/tracka_liq_glm_step5_power_coverage_20261112T165210Z.md`

## Target

`t1_liq` only (next-24h observed liquidation notional USD), QLIKE on positive rows. `rv` is not re-tested.

## Models (frozen)

- **B1** = log RV4h, log RV24h, log RV168h.
- **C1** = B1 + `fundingRate_clipped` + `abs_fund_pct`.
- **C2** = C1 + `premium_clipped` + `ema_dist_clipped`.

## Feature transform (frozen)

For `fundingRate`, `abs_fund_pct`, `premium`, `ema_dist`: compute observed `[min, max]` on the **train split** (positive `t1_liq` rows), clip to that range, then standardize by train mean/std. RV log features unchanged. No outcome-dependent selection.

## Estimator

Poisson / quasi-Poisson GLM, log link, IRLS, no regularization, no model search, no tuning. Fit on train only; predict conditional mean directly. Numerical safeguards only: eta ∈ [-30, 30], mu ≥ 1e-12, IRLS ≤ 100 iterations with step-halving.

## Gate

- Primary contrast `C2_vs_B1`; block bootstrap over 30-day blocks, 2000 reps, seed 20261112, 95% percentile CI, Holm across the family.
- PASS requires ≥ 2% relative QLIKE reduction AND 95% CI upper < 0 AND ≥ 5 paired instruments AND ≥ 3 test blocks AND Holm AND no single-coin driver AND max row QLIKE ≤ 1e6.
- If `INCONCLUSIVE_NUMERICAL_INSTABILITY` fires again: emit a timestamped evidenced structural-blocker document with the exact failing minima and stop; do not iterate estimator forms without a materially new source or a new preregistered design.

## Compliance

No outcome inspection before freeze; no threshold shopping; no sealed-holdout reuse; no Binance/2024 conflation; no modeled/proxy labels; Hyperliquid-only.