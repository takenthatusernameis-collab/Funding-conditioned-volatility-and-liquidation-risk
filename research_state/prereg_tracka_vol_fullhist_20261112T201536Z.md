# Pre-registration — TRACKA-VOL-FULLHIST-20261112T201536Z (Arm A, P1 volatility)

**Frozen (UTC):** 2026-11-12T20:15:36Z
**Status:** `FROZEN_PRE_OUTCOMES` — no outcome, label, or target data has been read for this design.
**Campaign:** `FCLR-FULLHISTORY-VOL-LIQ-20261112T201536Z`
**Machine-readable twin:** `research_state/prereg_tracka_vol_fullhist_20261112T201536Z.json`

## Why this exists (bottleneck removal)

Every volatility verdict in this repository was produced on **one 6-month window**
(2026-05-01..2026-10-31), because the only admissible mark-price cache covered exactly those
months. `TRACKA-VOL-20261111T234918Z` (NOT_MET, 12-comparison Holm family) and
`TRACKA-ALT-VOL-20261112T020322Z` (NOT_MET, 5.77% materiality pass but CI crosses zero)
therefore share a single block structure and a single macro regime. FCLR-006/007 were also
underpowered by construction (<3 blocks).

`ironflow/hyperliquid-candles-1h` (CC BY 4.0, unauthenticated HF bulk parquet) supplies
complete hourly candles for **2025-05-25 .. 2026-10-31**. That converts
**2025-06-01 .. 2026-01-17 into a never-opened holdout** for the volatility target and lifts
per-block observations from 6,480 to ~6,960.

This is new forward-block evidence under `RESEARCH_PROMPT` §17, not a re-score: the sealed
2026-05..2026-10 verdicts are untouched and are excluded from every purpose below.

## Data (all unauthenticated, no key, no signup, no requester-pays)

| Dataset | Licence | Columns used | Verified coverage |
|---|---|---|---|
| `ironflow/hyperliquid-candles-1h` | CC-BY-4.0 | `timestamp, market, close` | exact hourly grid, 2025-06..2026-04 (row/coin == days×24) |
| `ironflow/hyperliquid-funding` | CC-BY-4.0 | `timestamp, market, funding_rate, premium` | exact hourly grid, same months |
| `ironflow/hyperliquid-open-interest` | CC-BY-4.0 | `timestamp, market, open_interest_usd, mark_price` | exact hourly grid, same months |

Acquisition: `python3 scripts/fclr_ironflow_bulk.py fetch --datasets candles_1h,funding,open_interest --months 2025-05..2026-04`
(cache-first, sha256 + provenance sidecars, fail-closed schema checks, no workflow edits).

**Not used:** any liquidation label (Arm A is volatility-only), the 2026-05..2026-10 caches,
and any Binance/2024 data.

## Universe (coverage-only rule, frozen ex ante)

Native perps (`market` ends with `-PERP`, no `:` dex prefix) with complete hourly
candle + funding + open-interest coverage over 2025-05-25..2026-04-30:

`BTC, ETH, SOL, HYPE, ENA, WLD, FARTCOIN, TRUMP, NEAR, XRP` — **10 coins**, ≥5 required.

The rule uses coverage only. It reads no outcome and no liquidation label. This is a different
universe arm from the closed 9-coin and 8-coin panels.

## Unit, targets, features

- **Unit:** coin × 1h decision point (hour start, UTC).
- **Primary target (T24):** forward 24h realized variance, `sum r²` over the 24 hourly log
  returns strictly after `t`. Secondary: T6, T72, T168.
- **Features (causal, `timestamp <= t` only):** `rv1h`, `rv24h`, `rv168h`, `funding_rate`,
  `abs_funding`, `premium`, `ema_dist` (EMA span 24).
- **Secondary-only features (never in the primary contrast):** `log_open_interest`,
  `dlog_open_interest_24h`.
- Warm-up: first usable row per coin is `2025-06-01T14:00Z` (complete 168h trailing RV).

## Models and estimand

| Model | Features |
|---|---|
| `B1` | `rv1h, rv24h, rv168h` |
| `C1` | `B1 + funding_rate, abs_funding` |
| `C2` | `C1 + premium, ema_dist` |
| `B2` (secondary) | `B1 + log_open_interest, dlog_open_interest_24h` |
| `C3` (secondary) | `C2 + log_open_interest, dlog_open_interest_24h` |

OLS on `log(target + 1e-12)`, fitted on the train split only, no regularization, no model
search, no tuning. Forecasts are `exp(Xβ)` floored at `1e-12`. Predictors are standardized with
**train-only** mean/std; zero-variance columns are dropped and logged.

**Primary contrast: `C2_vs_B1`. Metric: QLIKE (lower is better).**

## Splits (chronological, 7-day embargo)

| Region | Window | Use |
|---|---|---|
| Train | 2025-06-02 .. 2025-09-30 | fit |
| Embargo | 2025-10-01 .. 2025-10-07 | never scored |
| Test block 0 | 2025-10-08 .. 2025-11-06 | score |
| Test block 1 | 2025-11-13 .. 2025-12-12 | score |
| Test block 2 | 2025-12-19 .. 2026-01-17 | score |
| **Reserved untouched** | **2026-01-18 .. 2026-04-30** | **never read, ever** |
| Sealed (excluded) | 2026-05-01 .. 2026-10-31 | must not be read |

Decision points whose label horizon crosses a block end are dropped, so no scoring row reads the
reserved region. Expected ≈ 6,960 rows/block, ≈ 20,880 total.

## Gates

- Relative QLIKE reduction ≥ **2.0%**.
- 95% circular block-bootstrap CI (block 168h, 2000 reps, seed 20261112) excludes zero **in favour of C2**.
- ≥ **5** paired instruments and ≥ **3** test blocks with data.
- Holm across the declared primary family.

**Primary family (12):** 4 horizons × {`C2_vs_B1`, `C1_vs_B1`, `C2_vs_C1`}, Holm at α=0.05, every
cell reported including failures.

**Secondary family (8, non-promotable):** 4 horizons × {`B2_vs_B1`, `C3_vs_B1`}, Holm within that
family only, never pooled with the primary family.

## Promotion (RESEARCH_PROMPT §17) — all seven must be reported

data/label gates; frozen OOS beat vs RV-only baseline; materiality + multiplicity + uncertainty;
no single-coin / single-block / single-crisis domination (LOIO, per-coin, per-block); calibration
and subgroup diagnostics; independent recomputation from stored hashes; red-team + leakage audit.

Only a clean sweep yields `FORECAST_GATE_PASSED`. Otherwise `NOT_MET` (with exact failing minima)
or `INCONCLUSIVE` (with root cause). No variant may rescue a losing primary.

## Forbidden

Reading/scoring 2026-05-01..2026-10-31 or 2026-01-18..2026-04-30; reading liquidation labels in
Arm A; Binance/2024 or venue mixing; modeled/proxy/synthetic labels; any threshold/model/feature/
split tuning on test blocks; re-scoring the sealed volatility verdicts; promoting anything from the
secondary family; agent-set `RESOLVED_VERIFIED`/`fabricated=true`; `.github/workflows/*` edits;
committing raw bulk parquet or caches.

## Artifacts to emit

`tracka_vol_fullhist_panel_<UTC>.parquet`, `tracka_vol_fullhist_panel_build_report_<UTC>.json`,
`evaluation_summary_TRACKA-VOL-FULLHIST-<UTC>.{md,json}`, refreshed
`ironflow_bulk_manifest.json`.