# TRACKA-HL Alignment Blocker — Hyperliquid market/price context coverage
**Timestamp (UTC):** 2026-11-11T09:10:11Z
**Experiment:** TRACKA-HL-20261111T073000Z (prereg: research_state/tracka_prereg_hyperliquid_2026.json)
**Verdict:** BLOCKED — full 2025-06..2026-10 aligned panel NOT buildable from admissible unauthenticated Hyperliquid-native sources.

## Requirement (prereg panel)
Label: ironflow observed liquidation events, notional_usd-weighted per symbol per 24h UTC bucket, 2025-06-01..2026-10-31.
Context required per prereg Step 2: Hyperliquid mark price, index price, premium index, OHLCV klines for the SAME window and overlapping symbols, admissible = unauthenticated, Hyperliquid-native, no Binance/2024 conflation, provenance documented (URL, access date, hash/ETag, license, terms).

## Liquidation labels (NOT the bottleneck)
- Source: ironflow/hyperliquid-liquidations (CC BY 4.0, unauthenticated HF bulk parquet, GO).
- Local: research_state/data_cache/ironflow_events/ — 18 monthly parquet, 2025-05..2026-10, 2,848,413 rows, 468 distinct markets.
- Markets use `-PERP` naming (e.g. `BTC-PERP`, `ETH-PERP`, `SOL-PERP`, `XRP-PERP`). All 9 funded symbols present as `-PERP`.
- Symbols overlapping the 9 funded coins (BTC, ETH, BNB, SOL, XRP, AVAX, DOGE, LINK, SUI): BTC-PERP, ETH-PERP, BNB-PERP, SOL-PERP, XRP-PERP, AVAX-PERP, DOGE-PERP, LINK-PERP, SUI-PERP.

## Alignment data probed (admissible, unauthenticated, Hyperliquid-native)
API: https://api.hyperliquid.xyz/info (unauthenticated POST). Verified reachable 2026-11-11T09:10:11Z.

### 1) fundingHistory — type=fundingHistory
- Status: WORKS. Cached locally: research_state/data_cache/hyperliquid_funding/{BTC,ETH,BNB,SOL,XRP,AVAX,DOGE,LINK,SUI}.json
- Per file: 8,668 rows, range 2025-11-01T00:00:00Z .. 2026-10-30T23:00:00Z.
- Coverage gap: 2025-06 .. 2025-10 (5 months) NOT available. Panel needs 2025-06 start.

### 2) mark-price 1h candles — type=candleSnapshot with nested `req`
- Working payload: `{"type":"candleSnapshot","req":{"coin":"<COIN>","interval":"1h","startTime":<ms>,"endTime":<ms>}}`
  (Top-level coin/interval/startTime/endTime returns HTTP 422 "Failed to deserialize".)
- Returns 1h mark-price OHLCV (o,h,l,c,v,n). No separate historical index-price or premium-index endpoint identified; no OHLCV klines beyond mark-price candles.
- Depth probe (start=month-start, end=+7d):
  - BTC: 2025-06→0, 2025-09→0, 2025-12→0, 2026-03→0, 2026-05→169, 2026-06→169
  - ETH/SOL/XRP: identical pattern (2025-11→0, 2026-05→169, 2026-06→169)
- Inference: ~6–7 month lookback cap; mark-price candles available only ~2026-05 .. 2026-10.
- Coverage gap: 2025-06 .. 2026-04 mark price NOT available.

## Conclusion
Full 2025-06..2026-10 aligned panel CANNOT be built:
- mark price missing for 2025-06 .. 2026-04 (~11 months)
- funding missing for 2025-06 .. 2025-10 (5 months)
- index price / premium index historical: no admissible unauthenticated endpoint identified
Consequently the pre-registered splits (train 2025-06..2025-11, val 2025-12..2026-01, test 2026-02..2026-10) cannot be executed as prereg'd, and QLIKE C2-vs-B1 on the full panel is not computable.

## Paths forward (next agent must pick one and record it)
1. Extend coverage: find an additional admissible unauthenticated Hyperliquid-native source serving mark/index/premium/klines back to 2025-06 for the overlapping symbols; prove provenance+coverage; then build panel + run prereg evaluation + verdict artifact.
2. Scope-down: build panel on the overlap where all three exist (~2026-05..2026-10 candles / 2025-11..2026-10 funding), but this deviates from the frozen prereg window/splits and requires re-prereg before any outcome computation.
3. Close Track A panel as NOT_SUPPORTED due to inadmissible/missing alignment context, documenting this blocker as the terminal evidence.

Forbidden (still apply): no Binance/2024 conflation, no modeled/proxy/synthetic labels, no sealed-holdout reuse, no threshold-shopping, no outcome inspection before prereg freeze, no `.github/workflows` edits, no status-only output without this blocker or a verdict artifact.

## Evidence files
- research_state/tracka_prereg_hyperliquid_2026.json (prereg, frozen pre-outcomes)
- research_state/data_cache/ironflow_events/*.parquet (labels)
- research_state/data_cache/hyperliquid_funding/*.json (funding, 2025-11..2026-10)
- research_state/hl_coverage_probe.json (candle depth probe, 2026-11-01)
- research_state/ironflow_probe_digest_latest.json (ironflow provenance)
