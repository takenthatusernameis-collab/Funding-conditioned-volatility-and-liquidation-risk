# Preregistration — TRACKA-HL-EARLY4H-2025H1-LIQ-GLM

**Campaign:** FCLR-EARLY4H-2025H1-LIQ-GLM v1
**Frozen (UTC):** 2026-11-12T16:48:38Z
**Status:** FROZEN BEFORE OUTCOMES
**Supersedes (estimator only):** TRACKA-HL-EARLY4H-2025H1 (sealed prereg `tracka_prereg_early2025h1_20261112T134503Z.json`, SHA-256 `fdd96bd1…`). The sealed `rv` NOT_MET result is **not** re-tested; the sealed prereg is not modified. Only the `liq` estimator/model form changes.

## Why this campaign exists

The corrected sealed eval (`...145537Z`) returned `liq = INCONCLUSIVE_NUMERICAL_INSTABILITY`: the frozen unregularized linear-in-log model with an exp() link extrapolated on the Oct-2025 funding spike (max per-row QLIKE 1.6e27). That is a model-form limitation, not a code bug. `liq` is therefore **open, not a null**.

This campaign answers `liq` with the QLIKE-consistent estimator — a Poisson / quasi-Poisson GLM with a **log link** fitted by IRLS — on the **same frozen panel, universe, and splits**. Only the estimator/model form is new.

## Window and labels

- Observed liquidation labels: 2025-05-25 .. 2025-10-31 (ironflow/hyperliquid-liquidations, CC BY 4.0, cached).
- Labels are observed events. No modeled, proxy, or synthetic labels.
- Universe: 9 named coins (AVAX, BNB, BTC, DOGE, ETH, LINK, SOL, SUI, XRP).
- BTC+ETH ≈ 63% of events and ≈ 84% of notional → per-coin and per-block reporting mandatory; a PASS driven by one coin or block is rejected.

## Reused frozen inputs (do not re-fetch, do not re-window)

- Panel: `research_state/tracka_hl_early2025h1_panel_20261112T145529Z.parquet`
- Panel SHA-256: `08c608035d179be8c274dd0b14386c5330893176c1b963048d09f82d98e3f958`
- Splits, minima, materiality: identical to `134503Z`.

## Target

- **T1_LIQ only:** next-24h observed liquidation notional USD (`t1_liq`), QLIKE loss.
- `rv` is **not** re-tested here.

## Models (frozen)

- **B1** = log RV4h, log RV24h, log RV168h (RV-only; no funding, no persistence lag).
- **C1** = B1 + signed funding (`fundingRate`) + 90-obs trailing abs-funding percentile (`abs_fund_pct`, ≥30 obs).
- **C2** = C1 + mark/index premium (`premium`) + mark/EMA24 distance (`ema_dist`).

Estimator: Poisson / quasi-Poisson GLM, **log link**, IRLS, **no regularization, no model search, no tuning**. Fit on the **train split only**; predict the conditional mean directly. Numerical safeguards only: eta clipped to [-30, 30], mu floored at 1e-12, IRLS ≤100 iterations with step-halving on deviance increase.

## Metric scope

QLIKE is evaluated on rows with `t1_liq > 0`, identical to the sealed `_design`/`evaluate` filtering and to `src/volatility/eval.py` (non-positive `y` or `yhat` are skipped). Zero-liq rows are excluded from both fitting and loss because QLIKE is undefined at `y = 0`.

## Primary contrast and gate

- Primary: `C2_vs_B1`; metric QLIKE (lower better). Secondary: `C1_vs_B1`, `C2_vs_C1`.
- Inference: block bootstrap over complete 30-day UTC blocks, 2000 reps, seed 20261112, 95% percentile CI, Holm across the declared family.
- PASS requires **≥ 2% relative QLIKE reduction AND 95% CI upper < 0** AND ≥ 5 paired instruments AND ≥ 3 test blocks, with Holm across the declared family and no single-coin driver.

## Numerical-stability acceptance

If any per-row QLIKE > 1e6, the target is `INCONCLUSIVE_NUMERICAL_INSTABILITY` (same guard as the corrected sealed eval). The exact max per-row QLIKE and offending rows/coins/blocks are reported.

## Concentration hazard

BTC+ETH are ~63% of events and ~84% of notional. Per-coin and per-block reporting is mandatory; a PASS driven by a single coin or block is rejected.

## Compliance

No outcome inspection before freeze; no threshold shopping; no sealed-holdout reuse; no Binance/2024 conflation; no modeled/proxy labels; Hyperliquid-only.