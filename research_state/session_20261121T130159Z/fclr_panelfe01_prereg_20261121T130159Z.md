# FCLR-PANEL-FE-001 — Outcome-Blind Prereg Freeze

- **Experiment ID:** FCLR-PANEL-FE-001-20261121T130159Z
- **Session:** session_20261121T130159Z
- **Generated (UTC):** 2026-11-21T13:01:59Z
- **Status:** FROZEN_PRE_OUTCOMES
- **outcome_data_inspected_before_freeze:** **false**
- **frozen_before_outcomes:** true

This prereg was frozen **before any RV or liquidation outcome statistic was computed**. The only prior inspection was metadata/coverage (row counts, null fractions, timestamp ranges, per-coin event counts) needed to make the design executable. No target distribution, coefficient, or forecast metric was observed.

## Why this campaign (repository-name priority)

The repository is named *Funding-conditioned-volatility-and-liquidation-risk* — two scientific halves reconciled by funding conditioning:

- **Half (a):** does the funding rate **condition volatility (RV)**?
- **Half (b):** does it **condition liquidation risk/intensity**?

Every prior campaign answered these with **pooled cross-sectional regime contrasts** or a **3-block time-series confirmation**. Both routes are exhausted or underpowered on the frozen panels (`next_campaign_status.py` → `NO_FEASIBLE_3_BLOCK_DESIGN_IN_ANY_DOMAIN`). This campaign attacks the same two halves with a **materially different, feasible design**: a two-way (coin + hour) fixed-effects panel on the full frozen panels, exploiting within-coin, within-hour variation. It therefore does **not** need the 3 mutually non-overlapping ≥127-day contiguous blocks.

## Frozen inputs (sha256 asserted in the eval script)

| Panel | Path | sha256 | Rows | Coins | Span |
|---|---|---|---|---|---|
| FCLR-001 (primary) | `research_state/fclr011_recompute_panel_20261115T234700Z.parquet` | `41962f82…c1f4` | 29,136 | 5 | 2026-01-01 → 2026-08-31 |
| Combined liquidation (Track A observed) | `research_state/fclr_liq_combined_panel_20261115T181405Z.parquet` | `81a100d5…7f14` | 1,740,415 | 15 | 2025-03-22 → 2026-10-31 |

**Critical data notes:**
- `premium` is **100% null** (`NOT_COMPUTABLE_WITHOUT_INDEX_PRICE`) — never used.
- `funding_asof_lag_h` is **hours-since-last-funding** (values ~1,2,3,…), **NOT** a funding rate. The signed funding rate is `signed_funding`.
- Frozen split boundaries carry a 7-day embargo: train `01-01→03-17`, validation `03-25→04-30`, test `05-08→08-06`.

## Hypotheses (frozen before outcomes)

- **H_panelfe_vol (half a):** two-way (coin + hour) FE on FCLR-001; coefficient on `signed_funding` in a regression of **next-hour log_rv1h** is non-zero and economically material (≥2% relative effect per 1-SD funding shock). Robustness: `target_rv24h`; sign-blind `abs_funding_pct_trail`.
- **H_panelfe_liq (half b):** two-way (coin + hour) FE on the hourly-aggregated combined liquidation panel; coefficient on `fundingRate` (hourly mean) in regressions of `log(1+liq_count)` and `log(1+notional_usd)` is non-zero and material (≥2% per 1-SD shock). Robustness: `abs_fund_pct` (hourly mean).

**Materiality floor = 2% relative**, frozen here, **not** relaxed after outcomes. A null is recorded as `NOT_SUPPORTED`.

## Inference (all three reported)

1. **Primary:** cluster-robust (CR1) by coin.
2. **Secondary:** Driscoll-Kraay HAC (Bartlett) on `h_t = Σ_i x_it e_it`.
3. **Tertiary:** Newey-West HAC on the stacked within-transformed series.

Only 5 coins in FCLR-001, so cluster-robust inference with G=5 is reported but the HAC time-series SE are the more reliable dependence-robust measures. Holm familywise correction across primary contrasts within each half; raw and Holm-adjusted p-values both reported.

## Walk-forward OOS (strictly chronological)

Expanding-window one-step-ahead; re-fit at each daily origin (00:00 UTC) using only data ≤ origin; forecast the next day. No random split; frozen split boundaries respected as a minimum; 7-day embargo.

- **Half a:** funding-conditioned FE vs no-funding FE baseline on `rv1h` level; **QLIKE**; Diebold-Mariano (HAC) on daily-mean QLIKE loss differential; relative reduction reported.
- **Half b:** funding-conditioned FE vs no-funding FE baseline on hourly `notional` intensity; **QLIKE** (+ Poisson deviance robustness); Diebold-Mariano.

## Regime cuts (pre-registered secondary)

- Half a: trailing-`rv24h` tercile (low/mid/high); UTC session bucket (Asia/EU/US).
- Half b: UTC session bucket of the liquidation hour.

## Decision rule

Support requires: (1) HAC 95% CI excludes 0; (2) 1-SD implied effect ≥ 2%; (3) Holm-adjusted p < 0.05; (4) walk-forward QLIKE relative reduction > 0 with DM not rejecting in the wrong direction; (5) not dominated by one coin or one time block. No threshold shopping.

## Hard constraints honored

`outcome_data_inspected_before_freeze=false` · both panel sha256 asserted · `premium` never used · `funding_asof_lag_h` not used as a rate · no random split · 2% floor frozen · observed liquidations kept distinct from modeled breaches.