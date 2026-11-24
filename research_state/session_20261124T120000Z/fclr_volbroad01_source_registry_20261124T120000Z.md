# FCLR-VOL-BROAD-01 Source Registry — ironflow_bulk on-disk panel

experiment_id: FCLR-VOL-BROAD-01
campaign: FCLR-VOL-BROAD-01-20261124T035500Z
session_utc: 20261124T120000Z
session_id: session_20261124T120000Z
phase: SOURCE_REGISTRY_ON_DISK
registry_kind: ironflow_bulk_on_disk_panel

Method: read-only enumeration of research_state/data_cache/ironflow_bulk/{candles_1h,funding,open_interest}.
Every .sha256 sidecar asserted before read; caches read-only, not mutated; no network.

Input integrity:
- sha256_sidecars_total: 54
- sha256_verified_ok: 54
- sha256_verified_bad: 0
- sha256_all_match: true
- panel_sha256: 8b414cc362bb76aa52e8d6bb639cf69c7934841d1e1bfb5552d18b0ac81a2fc9
- panel_hash_method: sha256 of concatenated dataset|month|sha256|rows across all parquet files (dataset|month sorted)

Coverage:
- month_span: 2025-05 .. 2026-10 (18 months)
- datasets: candles_1h, funding, open_interest
- n_distinct_coins_union: 886
- per_dataset_totals: candles_1h: 18 files / 3,643,742 rows; funding: 18 files / 4,104,648 rows; open_interest: 18 files / 3,977,432 rows
- note: candles_1h defines the 342-coin broad universe; funding and open_interest cover the 198 coins with funding/OI data; the volatility panel uses the intersection.

Schemas:
- candles_1h: timestamp, market, coin, dex, market_class, open, high, low, close, volume, trades
- funding: timestamp, market, coin, dex, funding_rate, premium
- open_interest: timestamp, market, coin, dex, mark_price, oracle_price, open_interest, open_interest_usd

Files: 54 parquet entries (18 per dataset), each with path, sha256, stored_sha256, sha_match, rows, schema, n_coins.

generated_utc: 2026-11-24T12:00:00Z
