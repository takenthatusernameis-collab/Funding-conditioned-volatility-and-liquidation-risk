# FCLR-TRACKA-SOURCE-AUDIT-01 — Source Registry (observed liquidation)

**Campaign:** FCLR-TRACKA-SOURCE-AUDIT-01-20261122T225107Z
**Session UTC:** 20261123T014600Z
**Phase:** SOURCE_ENUMERATION_PROBE
**Method:** bounded unauthenticated GET probes (stdlib urllib); no auth; no payment; no signup; no manual download; bounded retry budget with exponential backoff. Live endpoints probed 2026-11-23T01:49:35Z.

## Conclusion

No free, unauthenticated source provides a complete observed-liquidation census with defensible provenance and adequate coverage.

| Measure | Value |
|---|---|
| Candidates enumerated | 6 |
| Admissible Track A complete census | 0 |
| Admissible Track B mark-price + funding | 2 (Binance archive, OKX public REST) |
| Inadmissible Track A | 6 |

## Per-source findings

### 1. Binance public market-data archive — https://data.binance.vision
- **Access proof:** unauthenticated HTTP 200 on root and on real zip payloads (`BTCUSDT-metrics-2026-01-01.zip`, `BTCUSDT-fundingRate-2026-01.zip`); `liquidationSnapshot` daily and monthly directories return S3 `NoSuchKey` (HTTP 404).
- **History depth:** metrics 2020-09 .. 2026-11; fundingRate 2020-01 .. 2026-10; klines/markPriceKlines/indexPriceKlines/premiumIndexKlines deep (on-disk inputs table).
- **Track A (observed liquidation):** INADMISSIBLE — no liquidationSnapshot exists in the public archive. Observed-liquidation labels cannot be constructed from Binance archive alone.
- **Track B (modeled breach):** ADMISSIBLE for mark-price/index/premium/funding/OI features.

### 2. Bybit public REST API (v5, linear) — https://api.bybit.com
- **Access proof:** all probed endpoints (kline, funding history, liquidation) return HTTP 403 (CloudFront blocks the distribution in this environment).
- **Track A:** INADMISSIBLE — not an unauthenticated source in this environment; no credentials requested (RESEARCH_PROMPT.md §1).

### 3. OKX public REST API (v5) — https://www.okx.com
- **Access proof:** candles (HTTP 200) and funding rate (HTTP 200) return JSON; `/api/v5/public/liquidation` returns HTTP 404.
- **Track A:** INADMISSIBLE — no public liquidation endpoint.

### 4. Hyperliquid public API — https://api.hyperliquid.xyz
- **Access proof:** GET `/info` returns HTTP 405 Method Not Allowed (POST with JSON body required). No historical liquidation endpoint discovered in bounded probe.
- **Track A:** INADMISSIBLE — no verified unauthenticated historical liquidation endpoint with deep history.

### 5. Ironflow / Hugging Face liquidations archive
- **Access proof:** unauthenticated HTTP 200 on `.../data/events/2025-05.parquet?download=true` returning real PAR1 parquet bytes. On-disk accessed.json sidecar: license CC BY 4.0, unauthenticated, requester_pays=false.
- **History depth:** on-disk ironflow bulk liquidations, 18 monthly parquet, 2025-05 .. 2026-10, 2.85M rows.
- **Track A:** INADMISSIBLE as a complete census — this is a **capped-sample feed** (RESEARCH_PROMPT.md §15). It serves real observed liquidation events but is not a complete liquidation census; absence from the feed cannot be labeled "no liquidation." At most a partial positive signal under an explicit incomplete-label design.

### 6. Public GitHub / Zenodo / Hugging Face / institutional archives (generic)
- **Access proof:** candidate family enumerated per RESEARCH_PROMPT.md §5; no specific URL verified admissible in this session.
- **Track A:** INADMISSIBLE — no verified unauthenticated historical observed-liquidation path with defensible coverage.

## On-disk ironflow bulk note

`research_state/data_cache/ironflow_bulk/liquidations/` (18 monthly parquet, 2.85M rows, 2025-05 .. 2026-10) is the capped-sample feed above. It is NOT substituted for a complete census. sha256 sidecars verified; caches not mutated. Schema: `timestamp,market,issuer,wallet,position_side,size,notional_usd,avg_price,fills,block,tx_hash`.

## Decision

Track A observed-liquidation labeling is **structurally blocked**. See `fclr_tracks01_viability_decision_20261123T014600Z.json` for the frozen viability decision and the Track B (modeled boundary-breach) pivot, frozen before any outcome inspection.

**Generated:** 2026-11-23T01:49:35Z
