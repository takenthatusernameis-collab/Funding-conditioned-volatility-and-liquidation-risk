# FCLR-TRACKB-MODELED-BREACH-01 — Pivot Prereg (Track B, Modeled Boundary-Breach)

**Campaign:** FCLR-TRACKA-SOURCE-AUDIT-01-20261122T225107Z
**Session UTC:** 20261123T043600Z
**Phase:** PIVOT_PREREG_TRACKB_MODELED_BREACH
**Outcome data inspected before freeze:** false
**Decision frozen before outcomes:** true

## Rationale

Track A observed-liquidation labels are TRACK_A_STRUCTURALLY_BLOCKED: no free, unauthenticated source provides a complete observed-liquidation census with defensible provenance and adequate coverage (six candidate source families enumerated and probed; zero admissible Track A complete census). Per RESEARCH_PROMPT.md section 16 (three blocked routes spanning two+ source families → new experiment), pivot to Track B modeled hypothetical liquidation-boundary breach on the best available free mark-price + margin data.

This is a **modeled proxy only**. It does not reconstruct account-specific liquidation mechanics, portfolio/cross margin, liquidation engine execution, or actual forced liquidations. Long and short outcomes are kept strictly separate. It is never described or reported as observed liquidation (RESEARCH_PROMPT.md sections 15, 95-97).

## Data Sources (on-disk, sha256-verified, read-only, no network)

| Source | Path | Span | Use |
|--------|------|------|-----|
| ironflow_bulk candles_1h | research_state/data_cache/ironflow_bulk/candles_1h/ | 2025-05 .. 2026-10 (18 monthly parquet) | mark_price := close for modeled breach path |
| ironflow_bulk funding | research_state/data_cache/ironflow_bulk/funding/ | 2025-05 .. 2026-10 (18 monthly parquet) | signed funding_rate, premium features |
| ironflow_bulk open_interest | research_state/data_cache/ironflow_bulk/open_interest/ | 2025-05 .. 2026-10 (18 monthly parquet) | mark_price/oracle_price cross-check, open_interest context |

Every parquet has a .sha256 sidecar asserted before read. Caches are read-only, not mutated.

## Label Construct (Modeled Breach Proxy Only)

- **Kind:** modeled hypothetical liquidation-boundary breach (NOT observed liquidation)
- **Boundary rule:** `liquidation_boundary_price(entry_price, leverage, side, maintenance_margin_rate)`:
  - Long: entry × (1 − 1/leverage + mmr)
  - Short: entry × (1 + 1/leverage − mmr)
- **Crossed rule:** `boundary_crossed_future(mark_closes, t_index, boundary, side, horizon)` — uses only prices strictly after t_index (t+1..t+horizon); **no leakage**
- **Horizon:** 24 hours
- **Leverage:** 5.0
- **Maintenance margin rate:** 0.0
- **Entry price:** mark_price at origin t
- **Sides:** long and short, kept strictly separate
- **Label source:** `scripts/synthetic_boundary_labels.py` (synthetic_boundary_label, liquidation_boundary_price, boundary_crossed_future)

## Features (all known at origin)

| Feature group | Features |
|---------------|----------|
| Baseline B1 | RV6, RV24, RV168 (trailing realized volatility from hourly mark-price log returns, log-scaled, lagged persistence) |
| Candidate C2 additions | signed funding, abs funding percentile (train-only rolling, ≥30 observations), premium/mark-to-index dislocation, trailing MA deviation (mark/EMA24 − 1) |
| Normalization | train-only means/stds; no full-sample quantiles |

## Model

- **Family:** calibrated logistic regression for P(breach)
- **Fitting:** stdlib Newton/IRLS; linear-probability fallback if separation is severe
- **Regularization:** none; simple constrained model; no unconstrained ML

## Splits

- **Kind:** chronological walk-forward
- **Train fraction:** 60%
- **Purge + embargo:** 48 hours
- **Test blocks:** non-overlapping 168-hour (7-day) blocks; ≥3 required
- **Normalization:** train-only parameters

## Metrics

- **Primary:** Brier score, log loss (out-of-sample vs RV-only baseline B1)
- **Secondary:** calibration slope/intercept, ROC-AUC, precision/recall at pre-specified alert budget
- **Uncertainty:** block-aware per-coin block bootstrap CIs

## Materiality Floor

- **Threshold:** ≥2% relative Brier improvement vs RV-only baseline
- **Frozen:** never relaxed after outcomes

## Multiplicity

- **Method:** Holm step-down across declared family
- **Family:** primary arm, long arm, short arm, survivor arm, exited arm
- **Alpha spending:** alpha_k = 0.05 / (k × (k + 1)), k frozen
- **Report:** raw and adjusted p-values

## Verdict Rule (Symmetric, Frozen)

- **SUPPORTED iff:** materiality met AND bootstrap CI95 excludes null in favorable direction AND Holm-adjusted primary p < alpha_k
- **Otherwise:** NOT_SUPPORTED (null preserved honestly)
- **No threshold shopping:** true
- **Best model in losing family is not a proven edge:** true

## Input Hash Assertions

SHA-256 sidecars asserted for every parquet read; caches not mutated; no network for heavy evaluation.

## Status Vocabulary

NOT_SUPPORTED / SUPPORTED (symmetric, frozen).

**Generated UTC:** 2026-11-23T04:36:00Z
