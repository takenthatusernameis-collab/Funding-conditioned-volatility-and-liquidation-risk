# Track A Early 4h Liquidation Forecast Preregistration — TRACKA-HL-EARLY-4H-20261112T054737Z

**Timestamp (UTC):** 2026-11-12T05:47:37Z
**Experiment ID:** TRACKA-HL-EARLY-4H-20261112T054737Z
**Track:** A
**Campaign:** GAP-TRACKA-EARLY-OBSERVED-2025H2_2026Q1-4H
**Status:** PREREG_FROZEN_PRE_OUTCOMES

## 1. Purpose

Early 2025-11..2026-04 observed-liquidation+funding panel on **4h cadence**. Supersedes `TRACKA-HL-EARLY-20261111T191958Z` which was **INADMISSIBLE** because 1h `candleSnapshot` returned empty historical rows. 4h `candleSnapshot` returns **complete historical candles** (1086 bars/coin, 180 bars per 30-day block). This is a **NEW design/cadence**, not a reopening of sealed 1h outcomes (sealed record: `evaluation_summary_TRACKA-HL-early-infeasible-20261111T193500Z.md`).

## 2. Data Sources (All Cached + Provenanced)

| Source | Path | Coverage | Notes |
|--------|------|----------|-------|
| **Candles (4h)** | `research_state/data_cache/hyperliquid_candles_4h/<COIN>/<YYYY-MM>.json` | 2025-11-01 .. 2026-04-30, 9 coins, 1086 bars/coin | Hyperliquid `candleSnapshot` interval=4h; provenance: `.accessed.json` + `.sha256`; fetch report `tracka_hl_early_candle_fetch_4h_report_20261112T054104Z.json` |
| **Funding** | `research_state/data_cache/hyperliquid_funding/<COIN>.json` | 2025-11-01 .. 2026-10-30, ~8668 rows/coin (hourly) | Covers full window; unauthenticated |
| **Labels** | `research_state/data_cache/ironflow_events/<YYYY-MM>.parquet` | 2025-11-01 .. 2026-04-30, 9 `*-PERP` markets | ironflow/hyperliquid-liquidations (CC BY 4.0); **observed only** |

**Coins/Symbols (9):** BTC, ETH, BNB, SOL, XRP, AVAX, DOGE, LINK, SUI

## 3. Panel Construction

- **Unit:** symbol × 24h UTC bucket (aligned to 00:00 UTC)
- **Window:** 2025-11-01T00:00:00Z .. 2026-04-30T23:59:59Z
- **Target:** next-24h observed liquidation intensity = `liq_notional_usd` shifted -1 day (sum of notional_usd per symbol per 24h UTC bucket from ironflow events)
- **Baseline B1 (RV/context-only, 4h-derived):**
  - `rv_4h`: trailing 4h RV from 4h log returns (1 period)
  - `rv_24h`: trailing 24h RV from 4h log returns (6 periods)
  - `rv_168h`: trailing 168h RV from 4h log returns (42 periods)
  - `liq_intensity_lag1`: previous day's liquidation intensity (log)
  - `liq_intensity_lag7`: 7-day lag liquidation intensity (log)
- **Candidate C2 (B1 + funding-conditioned):**
  - `fundingRate`: latest funding rate at/before forecast origin (signed)
  - `abs_funding_90d_pct`: percentile rank of \|fundingRate\| vs prior 90 calendar days (min 30 obs)
  - `funding_premium`: mark/index premium at forecast origin
  - `funding_ema_dist`: mark/EMA24 distance at forecast origin
- **Model form (both):** OLS on `log(target + 1e-12)` with standardized predictors (training-only mean/std)

## 4. Splits (Chronological, Frozen Pre-Outcomes)

| Split | Start | End | Days |
|-------|-------|-----|------|
| **Train** | 2025-11-01 | 2026-01-31 | 92 |
| **Validation** | 2026-02-01 | 2026-02-28 | 28 |
| **Test Block 0** | 2026-03-07 | 2026-04-05 | 30 |
| **Test Block 1** | 2026-04-12 | 2026-05-11 | 30 |
| **Test Block 2** | 2026-05-18 | 2026-06-16 | 30 |

- **Embargo:** 7 calendar days between all split boundaries
- **Note:** Block 2 extends beyond 2026-04-30 window; data after 2026-04-30 excluded. Effective test blocks within window: **2 blocks (0 and 1)**. If <3 blocks feasible, record as **PILOT/INCONCLUSIVE** with exact shortfall.

## 5. Metrics & Gate

- **Primary metric:** QLIKE on next-24h liquidation intensity (lower better)
- **Materiality gate (ALL must pass for PASS):**
  1. Relative QLIKE reduction (C2 vs B1) ≥ 2%
  2. 95% CI for paired difference excludes zero (CI upper < 0 → C2 better)
  3. ≥ 5 paired instruments in test blocks
  4. ≥ 3 non-overlapping 30-day test blocks with data
- **Inference:** Block bootstrap (30-day blocks, joint across instruments), 2000 replications, seed=20261112
- **Paired comparisons:** C2_vs_B1 (primary), C1_vs_B1, C2_vs_C1

## 6. Inadmissibility Criteria (Any Triggers → INADMISSIBLE)

- Insufficient candles for RV computation (rv_24h needs 6 bars, rv_168h needs 42)
- Insufficient funding observations for 90d percentile (min 30)
- Insufficient label coverage (< 5 symbols with labels in test blocks)
- Insufficient test blocks (< 3 non-overlapping 30-day blocks within window)
- Data provenance/venue inconsistency detected

## 7. Compliance (Hard Bans)

- ✅ No outcome inspection before prereg freeze
- ✅ No threshold-shopping
- ✅ No sealed-holdout reuse (distinct window from FCLR-002/003/Track B)
- ✅ No Binance/2024 conflation (Hyperliquid-only)
- ✅ No modeled/proxy/synthetic liquidation labels (observed ironflow only)
- ✅ No `.github/workflows` edits
- ✅ No redundant network polling (all data cached)
- ✅ Venue-consistent artifacts only

## 8. Artifacts to Produce

| Artifact | Path |
|----------|------|
| Prereg JSON | `research_state/tracka_prereg_hyperliquid_early_4h_20261112T054737Z.json` |
| Prereg MD | `research_state/tracka_prereg_hyperliquid_early_4h_20261112T054737Z.md` |
| Panel Parquet | `research_state/tracka_hl_early_4h_panel_20261112T054737Z.parquet` |
| Panel Report JSON | `research_state/tracka_hl_early_4h_panel_build_report_20261112T054737Z.json` |
| Verdict MD | `research_state/evaluation_summary_TRACKA-HL-EARLY-4H-20261112T054737Z.md` |
| Verdict JSON | `research_state/evaluation_summary_TRACKA-HL-EARLY-4H-20261112T054737Z.json` |

---

**Frozen pre-outcomes.** This preregistration is immutable. Any changes require a new experiment ID.