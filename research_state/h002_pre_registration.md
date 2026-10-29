# H002 Pre-Registration — Funding-Extreme Correction-Time Partial Replication

Frozen: 2026-10-29T22:48:55Z
Campaign: H002-PARTIAL-REPLICA-v1
Hypothesis: FCLR-H002 (status: PARTIAL_REPLICATION)
Source claim: Helvin Shek, "Limits to Coordination: Funding Drag in Crypto Perpetual Funding Rates," SSRN abstract 7529458, posted 2026-09-29 (abstract page and PDF delivery returned HTTP 403 in this environment; full methodology not independently recoverable — see research_state/shek_methodology_availability.md).

## Paper claim being assessed (cited, not treated as established truth)
- 1,696 funding-extreme events across 18 Binance perpetual contracts.
- Median time to funding-extreme correction: 27 h in high-realized-volatility (RV) conditions vs 3 h in low-RV conditions.
- Lower correction hazard with higher RV.

## Scope and limits
- Partial reconstruction only, from admissible cached public data (no new downloads; no sealed holdouts; no forecast gate; no risk overlay; no trading/simulation).
- Correction time is a separate outcome from volatility forecast skill and from observed liquidation; results must not be conflated with either.
- If any element below cannot be computed from available data, record it as a limitation and keep the replication PARTIAL.

## 1. Data
- Venue: Binance USDⓈ-M perpetual funding rates, cached at repo root: `{SYMBOL}-fundingRate-2024-01/2024-02/2024-03.csv`.
- Symbols (eligible universe): BTCUSDT, ETHUSDT, BNBUSDT, SOLUSDT, XRPUSDT (5 contracts; matches reconstructed sample).
- Period: 2024-01-01T00:00:00Z .. 2024-03-31T23:59:59Z (Jan–Mar 2024).
- Cadence: 8-hourly funding (calc_time, epoch ms; funding_interval_hours = 8).
- Price series for RV: cached mark-price/klines where present under research_state/data_cache/{SYMBOL}_2024_0{1..3}; if mark price unavailable for an hour, that return is missing (never zero-filled).

## 2. Frozen event definition (extreme detection)
- Per symbol, per funding observation in chronological order.
- Trailing normalization window: preceding 90 calendar days of funding observations for that symbol (rolling, pre-event only).
- Minimum history: at least 30 valid funding observations within the trailing 90-day window before an extreme can be emitted; record actual count per event.
- Extreme: funding rate at or below the 5th percentile OR at or above the 95th percentile of the trailing window (two-sided; retain positive and negative sides separately).
- Percentile computed via nearest-rank on sorted trailing values.
- Events in consecutive funding observations on the same side: dedupe by keeping the most extreme observation and skipping subsequent same-side observations until funding crosses back within [p_low, p_high].
- Thresholds used at event time (p_low, p_high) are frozen with the event and used for its correction test.

## 3. Frozen correction definition
- Correction: the first subsequent funding observation (strictly after the event timestamp) whose funding rate moves back inside the normalization band:
  - Positive extreme: funding <= p_high.
  - Negative extreme: funding >= p_low.
- Time to correction = (correction_ts - event_ts) in hours (8-hour grid multiples).
- Censoring (uncorrected): no correction within the maximum follow-up window of 168 hours (7 days), or series ends before 168 hours. Censored events are reported, never counted as completed negatives.
- If the event observation itself is the last available observation, it is censored.

## 4. Frozen RV regime split
- RV regime for an event: trailing 24-hour realized volatility of mark-price log returns ending at the event timestamp (returns over hourly closes up to and including the event hour).
- Require at least 23 valid hourly returns; otherwise regime = missing (event excluded from regime split, retained in overall counts).
- RV bins (pre-registered): low = bottom tercile of per-symbol event RV distribution; high = top tercile; middle excluded from the high/low contrast but reported.
- Regime computed from the full Jan–Mar sample per symbol before the contrast; record bin edges per symbol.
- Primary contrast: median time to correction in high-RV vs low-RV events (Kaplan-Meier style medians with censoring), and hazard direction (lower hazard with higher RV per paper claim).

## 5. Exclusions and eligibility
- Symbols with fewer than 30 total funding observations in Jan–Mar: exclude symbol (record reason).
- Events missing regime RV: excluded from high/low contrast only.
- Duplicate timestamps: dedupe keeping first; record count.
- Non-finite funding rates: excluded (record count).

## 6. Outputs required by this campaign
- research_state/h002_pre_registration.md (this file) — frozen before computation.
- scripts/funding_correction_replication.py extended to: emit per-symbol event lists, correction times, censoring flags, RV regime assignment, hazard-by-RV-regime table, censoring summary.
- research_state/h002_replication_report.md — reconstructed medians/hazard vs paper claim; explicit PARTIAL statement; separates correction time from volatility forecast/liquidation.
- tests/test_funding_correction_replication.py — hazard regime logic + censoring tests; run via `python -m unittest tests/test_funding_correction_replication.py -v` (pytest unavailable in this environment).
- research_state/hypothesis_registry.json — H002 evidence updated.
- research_state/run_manifest.json — run record appended.
- research_state/negative_results_report.md — updated only if null/inconclusive findings arise.

## 7. Acceptance
- Pre-registration exists and is frozen before any computation in this session.
- Hazard-by-RV-regime table with censoring counts by symbol/regime computed from cached Jan–Mar 2024 data only.
- Report states PARTIAL and does not claim exact replication or forecast/liquidation skill.
- Tests pass.
- No sealed holdouts reused; no forecast-gate runs; no downloads.
