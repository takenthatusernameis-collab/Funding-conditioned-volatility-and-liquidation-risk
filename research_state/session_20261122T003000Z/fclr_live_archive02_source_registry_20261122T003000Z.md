# FCLR-LIVE-ARCHIVE-02 Source Registry — Binance Public Archive (data.binance.vision)

**Campaign:** FCLR-LIVE-ARCHIVE-02 (rank-0, gate-enforced)
**Session UTC:** 2026-11-22T00:30:00Z
**Artifact:** `fclr_live_archive02_source_registry_20261122T003000Z.{json,md}`

## Source (verified reachable 2026-11-22T00:25:00Z)

| Field | Value |
|-------|-------|
| Venue | Binance (public market-data archive) |
| Base URL | https://data.binance.vision |
| S3 bucket | s3-ap-northeast-1.amazonaws.com/data.binance.vision |
| Access | Unauthenticated HTTPS GET (no API key, no signed request, no account, no payment, no signup) |
| REST api.binance.com | HTTP 451 blocked — not used |
| Re-verified | root HTTP 200; metrics prefix listing HTTP 200; fundingRate zip HTTP 200; S3 list-type=2 on metrics/BTCUSDT = 2272 keys (2020-09-01 .. 2026-11-20) |

## Datasets downloaded (session window 2025-06-01 .. 2025-08-18, BTCUSDT)

| Dataset | Archive path | Files downloaded | Sample sha256 | Use |
|---------|-------------|------------------|---------------|-----|
| futures/um/daily/metrics | `data/futures/um/daily/metrics/BTCUSDT/` | 79 daily zips (2025-06-01 .. 2025-08-18) | `BTCUSDT-metrics-2025-06-15.zip` = `8f6627d5...` (10,955 B, 288 rows, 5-min cadence) | Open interest + taker long/short volume ratio (liquidation-risk proxy) |
| futures/um/monthly/fundingRate | `data/futures/um/monthly/fundingRate/BTCUSDT/` | 3 monthly zips (2025-06 .. 2025-08) | `BTCUSDT-fundingRate-2025-06.zip` = `d611a863...` (946 B) | Signed funding rate feature |
| futures/um/monthly/markPriceKlines/1h | `data/futures/um/monthly/markPriceKlines/BTCUSDT/1h/` | 3 monthly zips (2025-06 .. 2025-08) | `BTCUSDT-1h-2025-06.zip` = `af4ef458...` (20,653 B) | Forward realized-variance target |

## Liquidation-risk proxy (never observed liquidations)

This archive has NO `liquidationSnapshot` dataset (Binance discontinued public liquidation snapshots). Liquidation risk is therefore PROXIED, causally, as: elevated open interest + extreme taker long/short volume imbalance + mark-to-index dislocation. Every proxy result is labeled `LIQUIDATION_RISK_PROXY` and is never represented as observed liquidations. Track A (observed liquidation labels) is NOT_SUPPORTED on this source.

## Admissibility

- Unauthenticated: yes
- No credentials/keys: yes
- No payment/signup: yes
- Historical depth: yes (2020 onward)
- Schema verified by real download: yes
- Admissible for research (Track C volatility + proxy liquidation-risk): yes
- Admissible for Track A observed liquidations: no

## Manifest and raw extracts

- Download manifest: `research_state/session_20261122T003000Z/download_manifest.json`
- Raw extracts: `research_state/session_20261122T003000Z/raw/`
- Machine-readable registry: `fclr_live_archive02_source_registry_20261122T003000Z.json` (same directory)
