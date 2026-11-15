# FCLR-SHEK-SCALE Pre-Registration — Funding-Conditioned Correction Hazard Under RV Regimes

**Prereg ID:** `FCLR-SHEK-SCALE-20261115T063600Z`
**Campaign:** `FCLR-SHEK-SCALE-20261115T040843Z`
**Frozen at:** `2026-11-15T06:36:00Z` (BEFORE any scaled-sample correction-time outcome inspection)
**Class:** EXPLORATORY_ONLY · **promotable:** false · **sealed artifacts mutated:** false
**Network / paid / credentialed / manual data:** none (cache only)

## Scope
Scaled EXPLORATORY_ONLY partial replication of Shek (SSRN 7529458). Full methodology is not independently reconstructible (SSRN HTTP 403); this remains a partial, non-promotable replication. Correction time is a separate outcome from volatility-forecast skill and from observed-liquidation prediction; it is never relabelled.

## Frozen event definition (verbatim from `research_state/h002_pre_registration.md`)
- Two-sided nearest-rank 5th/95th percentile extremes on a trailing 90-day funding window.
- `>=30` valid funding observations in the trailing window (actual count recorded per event).
- Dedupe same-side clusters: keep the first extreme until funding re-enters the band.
- Correction = first strictly-later funding obs back inside `[p_low, p_high]`; censor at 168h or series end.
- RV regime = trailing 24h mark-price log-return realized vol; `>=23` valid hourly returns; else `missing`.

## Arms (frozen ex-ante)
**Arm A — Binance (primary, independent).** 5 symbols (BTC/ETH/BNB/SOL/XRP) × 31 months `2024-04..2026-10`. **Excludes `2024-01..2024-03`** already reported by the H002 partial (88 events) — this makes Arm A independent. Audit: 14,160 funding obs (84–93/symbol-month), mark price present in all 31 event-months (≥672 hourly rows/month).

**Arm B — ironflow cross-coin (secondary, never promotable).** Funding + candles 2025-05..2025-12 (observed months). Frozen thresholds: `≥1000` funding obs AND `≥5000` candle rows/coin → **160 coins qualify**. Separate secondary family; never merged into the primary Holm family.

## Inference (frozen)
- Kaplan–Meier medians per RV regime (reported, not headline-picking).
- Two-sided log-rank (1 df) high-RV vs low-RV, right-censoring respected.
- Median-difference 95% CI: **per-coin cluster + per-month block bootstrap**, 2000 reps, seed `20261115`.
- Multiplicity: **Holm** across the pre-specified primary family (pooled, positive-side, negative-side, per-symbol high-vs-low = 5 comparisons).
- Sensitivity grid (reported only, never optimises the headline): percentiles 1/99, 5/95, 10/90; censor 168h/336h; tercile vs median RV split.

## Headline cell (frozen)
`[5,95]` percentiles · `168h` censor · tercile split → high-RV vs low-RV correction-time hazard.

## Verdict rules (frozen)
`REPLICATES_DIRECTION` (high-RV KM median > low-RV AND `|median_diff| >= 0.5*min(medians)` AND Holm p<0.05) / `TAIL_SHAPE_EFFECT` (significant log-rank with the right direction but sub-material median gap — a distribution/tail difference, not a median replication) / `NULL` / `UNDERPOWERED` / `INCONCLUSIVE`. Materiality is judged on the **median contrast**, not the log-rank p alone: the 8h funding cadence quantises correction times, so a tiny median gap can be log-rank-significant without being economically material. No verdict promotes H2 out of EXPLORATORY_ONLY or into forecast/liquidation claims.

## Discipline
No early peek; no threshold tuning against outcomes; no new data; the frozen primary cell plus full sensitivity grid must be executed and a verdict recorded. "No trigger" is not a stop condition.