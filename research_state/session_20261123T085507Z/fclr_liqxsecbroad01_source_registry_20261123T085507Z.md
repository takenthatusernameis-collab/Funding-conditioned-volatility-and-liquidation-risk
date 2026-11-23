# FCLR-LIQ-XSEC-BROAD-01 — On-Disk Source Registry

**Experiment ID:** FCLR-LIQ-XSEC-BROAD-01
**Campaign:** FCLR-LIQ-XSEC-BROAD-01-20261123T080000Z
**Session UTC:** 20261123T085507Z
**Phase:** SOURCE_REGISTRY_ON_DISK

## Registry kind

ironflow_bulk_on_disk_panel — read-only enumeration of
`research_state/data_cache/ironflow_bulk/{candles_1h,funding,open_interest,liquidations}`.

## Method

- SHA-256 sidecar asserted for every parquet before read; all 72 sidecars verified OK, 0 bad.
- Caches read-only, not mutated. No network used for the heavy evaluation.
- Panel hash = SHA-256 of concatenated `path|sha256|rows` across all 72 parquet files (dataset|month sorted).

## Input integrity

| Check | Value |
|---|---|
| SHA-256 sidecars total | 72 |
| SHA-256 verified OK | 72 |
| SHA-256 verified bad | 0 |
| SHA-256 all match | true |
| Panel SHA-256 | `09377b01aeebdf6a6dca527f1298586d441f65b6648b81178e28523e0e3e2923` |

## Coverage

| Item | Value |
|---|---|
| Month span | 2025-05 .. 2026-10 (18 months) |
| Distinct markets in liquidations | 468 (market is the instrument key; no `coin` column in liquidations) |
| Distinct coins (market stripped of exchange prefix + `-PERP`) | 393 |
| Liquidation row total | 2,849,452 |
| candles_1h rows | 3,643,742 (18 files) |
| funding rows | 4,104,648 (18 files) |
| open_interest rows | 3,977,432 (18 files) |

## Schemas

- `liquidations`: timestamp, market, issuer, wallet, position_side, size, notional_usd, avg_price, fills, block, tx_hash
- `funding`: timestamp, market, coin, dex, funding_rate, premium
- `open_interest`: timestamp, market, coin, dex, mark_price, oracle_price, open_interest, open_interest_usd
- `candles_1h`: timestamp, market, coin, dex, market_class, open, high, low, close, volume, trades

Note: `liquidations` has NO `coin` column — the instrument key is `market`. Per-coin identity is derived by stripping the exchange prefix and `-PERP` suffix from `market`.

## Capped-sample caveat

ironflow liquidations are a capped-sample feed (RESEARCH_PROMPT.md section 15), not a complete census. Absence from this feed is NOT zero; claims are restricted to presence/intensity ordering, never a binary absence/presence census.

## File inventory

See `fclr_liqxsecbroad01_source_registry_20261123T085507Z.json` for the per-file entry list (path, sha256, stored sha256, sha_match, rows).

**Generated UTC:** 2026-11-23T08:55:07Z
