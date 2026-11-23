# FCLR-TRACKA-SOURCE-AUDIT-01 — Source Enumeration Probe Report

**Session UTC:** 20261123T014600Z
**Campaign:** FCLR-TRACKA-SOURCE-AUDIT-01-20261122T225107Z
**Phase:** SOURCE_ENUMERATION_PROBE
**Method:** bounded unauthenticated GET/HEAD probes; stdlib urllib; no auth; no payment; no manual download
**Generated UTC:** 2026-11-23T01:49:35Z

## Summary
- Candidates enumerated: 6
- Admissible Track A complete census: 0 of 6
- Admissible Track B mark-price/funding sources: 2 (Binance public archive, OKX public REST)

## Per-Source Access Table

| # | Source | Family | Track A admissible? | Rejection / Access Reason |
|---|--------|--------|---------------------|---------------------------|
| 1 | Binance public market-data archive | exchange_official_archive | No | No public liquidation endpoint returned 200; observed-liquidation history not served. |
| 2 | Bybit public REST API (v5, linear) | exchange_public_rest | No | Endpoint reachable but forbidden (403) without credentials; not an unauthenticated source. |
| 3 | OKX public REST API (v5) | exchange_public_rest | No | No public liquidation endpoint returned 200; observed-liquidation history not served. |
| 4 | Hyperliquid public API | exchange_public_rest | No | Unreachable / errored: HTTPError 405: Method Not Allowed |
| 5 | Ironflow / Hugging Face liquidations archive | institutional_archive | Yes | access verified |
| 6 | Public GitHub / Zenodo / Hugging Face institutional archives (generic) | public_archive | No | No verified unauthenticated historical observed-liquidation path with defensible coverage. |

## Endpoint Detail

### Binance public market-data archive
- **Family:** exchange_official_archive
- **Base URL:** https://data.binance.vision
- **Probed UTC:** 2026-11-23T01:49:26Z
- **Purpose:** observed liquidation labels (liquidationSnapshot) + mark-price/funding/OI for Track B features
- **Track A admissible:** False
- **Rejection reason:** No public liquidation endpoint returned 200; observed-liquidation history not served.

### Bybit public REST API (v5, linear)
- **Family:** exchange_public_rest
- **Base URL:** https://api.bybit.com
- **Probed UTC:** 2026-11-23T01:49:28Z
- **Purpose:** historical funding, klines, and any public liquidation history
- **Track A admissible:** False
- **Rejection reason:** Endpoint reachable but forbidden (403) without credentials; not an unauthenticated source.

### OKX public REST API (v5)
- **Family:** exchange_public_rest
- **Base URL:** https://www.okx.com
- **Probed UTC:** 2026-11-23T01:49:28Z
- **Purpose:** historical funding, candles, and any public liquidation history
- **Track A admissible:** False
- **Rejection reason:** No public liquidation endpoint returned 200; observed-liquidation history not served.

### Hyperliquid public API
- **Family:** exchange_public_rest
- **Base URL:** https://api.hyperliquid.xyz
- **Probed UTC:** 2026-11-23T01:49:29Z
- **Purpose:** any unauthenticated historical liquidation endpoint with deep history
- **Track A admissible:** False
- **Rejection reason:** Unreachable / errored: HTTPError 405: Method Not Allowed

### Ironflow / Hugging Face liquidations archive
- **Family:** institutional_archive
- **Base URL:** https://huggingface.co/datasets/ironflow/hyperliquid-liquidations
- **Probed UTC:** 2026-11-23T01:49:35Z
- **Purpose:** observed liquidation events (Hyperliquid), CC BY 4.0; on-disk ironflow bulk is the capped-sample feed
- **Track A admissible:** True

### Public GitHub / Zenodo / Hugging Face institutional archives (generic)
- **Family:** public_archive
- **Base URL:** n/a
- **Probed UTC:** 2026-11-23T01:49:35Z
- **Purpose:** downloadable historical liquidation/event records without signup or keys
- **Track A admissible:** False
- **Rejection reason:** No verified unauthenticated historical observed-liquidation path with defensible coverage.

## Frozen Viability Decision
- Decision: TRACK_A_STRUCTURALLY_BLOCKED
- outcome_data_inspected_before_freeze: false
- Structural-impossibility basis: three+ distinct blocked routes spanning two+ source families
- See fclr_tracks01_viability_decision_20261123T014600Z.json for the full decision record.

## Track B Pivot
- Pivot to Track B modeled boundary-breach protocol FCLR-TRACKB-MODELED-BREACH-01
- See fclr_tracks01_pivot_prereg_20261123T043600Z.{json,md} for the frozen prereg.
