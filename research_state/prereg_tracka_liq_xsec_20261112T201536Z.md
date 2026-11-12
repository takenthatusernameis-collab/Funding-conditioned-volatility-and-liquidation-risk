# Pre-registration — TRACKA-LIQ-XSEC-20261112T201536Z (Arm B, P2, EXPLORATORY)

**Frozen (UTC):** 2026-11-12T20:15:36Z
**Status:** `FROZEN_PRE_OUTCOMES` — no outcome data read for this design.
**Maximum attainable status:** `EXPLORATORY_ONLY`. **Not promotable.**
**Machine-readable twin:** `research_state/prereg_tracka_liq_xsec_20261112T201536Z.json`

## Why this is exploratory and not confirmatory

There is **no unopened label window left** inside the ironflow coverage range
2025-05-25..2026-10-31:

| Region | Opened by |
|---|---|
| 2025-05-25..2025-10-31 | `TRACKA-HL-EARLY4H-2025H1` (NOT_MET, robust estimator) |
| 2025-11-01..2026-04-30 | `TRACKA-HL-EARLY-4H-20261112T054737Z` (INCONCLUSIVE_PILOT_SHORTFALL, 2 blocks) |
| 2026-05-01..2026-10-31 | `TRACKA-HL-S-20261111T133430Z` (NOT_MET) and the 8-coin expansion PASS (not promotable) |

`RESEARCH_PROMPT` §17 forbids calling an inspected holdout untouched evidence. This arm therefore
changes the **estimand** (cross-sectional ranking) and the **universe arm** (full native-perp
cross-section, ~150-200 coins, instead of 8-9 hand-picked coins), declares itself exploratory, and
cannot alter any sealed verdict.

## Claim

On the full Hyperliquid native-perp cross-section, a funding-conditioned cross-sectional score
carries information about the **relative ordering** of next-24h observed liquidation intensity
across coins.

## Data

| Dataset | Licence | Columns | Months |
|---|---|---|---|
| `ironflow/hyperliquid-liquidations` | CC-BY-4.0 | `timestamp, market, notional_usd` | 2025-05..2025-10 (already cached, 2.85M rows verified) |
| `ironflow/hyperliquid-candles-1h` | CC-BY-4.0 | `timestamp, market, close` | 2025-05..2025-10 |
| `ironflow/hyperliquid-funding` | CC-BY-4.0 | `timestamp, market, funding_rate, premium` | 2025-05..2025-10 |

All observed labels only. No modeled, proxy, or synthetic liquidation data. No venue mixing.

## Universe (coverage-only rule, frozen ex ante)

Native perps (`market` ends `-PERP`, no `:`) with, over the test window 2025-10-08..2026-01-17:

- ≥ **20** observed liquidation-days, and
- ≥ **100** observed liquidation events, and
- complete hourly candle + funding coverage.

Eligibility uses label **existence/coverage** only — never magnitude, direction, or timing.
Expected size ~150-200 coins; hard floor 5.

## Unit, features, score

- **Unit:** coin × 24h UTC bucket.
- **Causal features:** `rv24h` (trailing, from hourly closes), `funding_rate`, `abs_funding`,
  `premium` (all as-of at or before bucket start).
- **Score:** within-bucket cross-sectional z-score of `funding_rate` plus cross-sectional z-score
  of `abs_funding`. No time-series fitting, no information flow across buckets.

## Estimand and inference

- **Primary:** Spearman rank IC between the score at bucket *t* and next-24h observed liquidation
  event count at *t+1*, per 30-day block, on the pooled cross-section.
- **Secondary:** top-k minus bottom-k mean next-24h liquidation notional spread (k = 10% of the
  universe, floor 5), per block.
- **Null:** within each 24h bucket, permute the score across coins; 1,000 reps; seed 20261112;
  two-sided.
- **Materiality floor:** |mean IC| ≥ 0.05 **and** spread sign consistent in ≥ 2 of 3 blocks.
- **Unit of inference:** the 30-day block, not the coin-day.

## Splits

| Region | Window | Use |
|---|---|---|
| Burn-in | 2025-05-25 .. 2025-10-07 | feature warm-up + universe eligibility only, never scored |
| Test block 0 | 2025-10-08 .. 2025-11-06 | score |
| Test block 1 | 2025-11-13 .. 2025-12-12 | score |
| Test block 2 | 2025-12-19 .. 2026-01-17 | score |
| Reserved untouched | 2026-01-18 .. 2026-04-30 | never read |
| Sealed | 2026-05-01 .. 2026-10-31 | never read |

Same block skeleton as Arm A; the arms are scored and reported separately.

## Decision rule

- `EXPLORATORY_SIGNAL` — criteria met: report with full diagnostics, no promotion; a confirmatory
  test would require a newly preregistered, unopened forward window.
- `EXPLORATORY_NULL` — criteria not met: preserve the null with exact failing minima.
- `INADMISSIBLE` — <5 coins or <3 blocks with data: emit infeasibility with exact minima, stop.

## Forbidden

Any promotion or re-labelling of a sealed hypothesis; reading the reserved or sealed windows;
liquidation labels in Arm A; venue mixing; modeled/synthetic labels; tuning the score, k, or floor
on test blocks; `.github/workflows/*` edits; committing raw parquet or caches.

## Artifacts

`tracka_liq_xsec_panel_<UTC>.parquet`, `tracka_liq_xsec_panel_build_report_<UTC>.json`,
`evaluation_summary_TRACKA-LIQ-XSEC-<UTC>.{md,json}`.