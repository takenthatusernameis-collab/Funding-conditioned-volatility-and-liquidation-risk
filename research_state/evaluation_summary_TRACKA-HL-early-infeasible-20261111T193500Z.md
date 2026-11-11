# Documented Infeasibility — GAP-TRACKA-EARLY-OBSERVED-2025H2_2026Q1

**Experiment ID:** TRACKA-HL-EARLY-20261111T191958Z
**Campaign:** GAP-TRACKA-EARLY-OBSERVED-2025H2_2026Q1 (Branch 2 default)
**Track:** A
**Determination:** INADMISSIBLE — pre-registered claim-worthy minima cannot be satisfied on audited cached + bounded first-time acquirable data.
**Determined (UTC):** 2026-11-11T19:19:58Z (acquisition completed 2026-11-11T19:31:40Z)
**Prereg (frozen pre-outcomes):** research_state/tracka_prereg_hyperliquid_early_20261111T191958Z.json/.md
**Gate 4:** EXTERNAL_BLOCKED (no RESOLVED_VERIFIED terms evidence) — Branch 2 executed; Branch 1 not triggered.

## Evidence (exact, verifiable)
1. **Observed labels (ironflow, Hyperliquid, observed only):** cached `research_state/data_cache/ironflow_events/2025-11.parquet .. 2026-04.parquet` — label coverage present for all 6 months of the prereg window 2025-11-01..2026-04-30 for 468 markets incl. all 9 *-PERP symbols. PASS.
2. **Funding context (cached):** `research_state/data_cache/hyperliquid_funding/{9 coins}.json`, 8668 hourly records each, coverage ~2025-11-01T00:00:00Z .. 2026-10-30T23:00:00Z (first_ms 1761955200078, last_ms 1793401200078 per coin). Covers the full prereg window. PASS.
3. **Mark-price/RV context (candles):** NOT cached for 2025-11..2026-04. Bounded first-time unauthenticated Hyperliquid `candleSnapshot` 1h acquisition executed for all 9 coins x months 2025-11..2026-04 (54 calls, report `research_state/tracka_hl_early_candle_fetch_report_20261111T193140Z.json`, 0 errors, all HTTP 200). Result:
   - 2025-11, 2025-12, 2026-01, 2026-02, 2026-03: empty list `[]` for all 9 coins — no candle data available from the exchange for this window.
   - 2026-04: partial only, ~327-328 rows per coin (e.g., BTC first t=1776412800000, last t=1777590000000; ~45% of month hours).
   - RV24h requires 168 hourly closes; cannot be computed across the window; B1 RV-only baseline NOT computable for 2025-11..2026-03 and only partially for 2026-04.
4. **Pre-registered minima (all required):**
   - >=5 paired instruments: labels+funding exist for 9, but RV/B1 computability fails.
   - >=3 non-overlapping 30-day test blocks with data: NOT satisfiable (candles absent 5 of 6 months; April partial).
   - RV24h/B1 baseline computable: NO.
   - Materiality gate (>=2% relative QLIKE reduction, CI excludes zero): cannot be evaluated — no OOS test set with RV context.

## Determination
Claim INADMISSIBLE under prereg infeasibility rule. No outcome computation was performed for this claim (prereg frozen pre-outcomes; no panel alignment/outcome inspection occurred). No Binance/2024 conflation; Hyperliquid only; observed ironflow labels only; no modeled/proxy labels presented as observed; no redundant polling (bounded first-time acquisition, cached+provenanced).

## Pivot
Next candidate per gap audit: `GAP-TRACKA-SYMBOL-EXPANSION-2026M05M10` — expand symbol universe on 2026-05..2026-10 (or subwindow) for observed liquidation-intensity forecasting using additional liquid Hyperliquid markets present in ironflow (432 PERP markets cached for 2026-05..2026-10 vs 9 in the closed NOT_MET panel) with matching funding+candle predictors. Requires NEW prereg with frozen ex-ante symbol selection rule + event-adequacy checks BEFORE outcomes; bounded first-time unauthenticated fundingHistory/candleSnapshot acquisition for candidate symbols as needed; no cherry-picking; no sealed-holdout reuse; Track A 2026-05..2026-10 9-symbol panel remains closed NOT_MET and is not relitigated — expansion is a different universe/design.

## Artifacts
- Prereg: research_state/tracka_prereg_hyperliquid_early_20261111T191958Z.json + .md
- Acquisition report: research_state/tracka_hl_early_candle_fetch_report_20261111T193140Z.json
- Candle cache: research_state/data_cache/hyperliquid_candles/<COIN>/2025-11..2026-04.{json,accessed.json,sha256}
- This document: research_state/evaluation_summary_TRACKA-HL-early-infeasible-20261111T<UTC>.md
