# FCLR-VOL-JUMP-01 Source Registry (20261125T030000Z)

- experiment_id: FCLR-VOL-JUMP-01
- session_id: session_20261125T030000Z
- source: ironflow_bulk (frozen on-disk cache; read-only; no network)
- cache_root: research_state/data_cache/ironflow_bulk
- month_span: ['2025-05', '2026-10'] (18 months)
- universe intersection coins: 466
- sha256_all_match: True
- sha256_verified_bad: 0
- n_files: 54

## Datasets

| dataset | files |
|---|---|
| candles_1h | {'months': ['2025-05', '2025-06', '2025-07', '2025-08', '2025-09', '2025-10', '2025-11', '2025-12', '2026-01', '2026-02', '2026-03', '2026-04', '2026-05', '2026-06', '2026-07', '2026-08', '2026-09', '2026-10'], 'n_months': 18, 'total_rows': 3643742, 'schema': ['timestamp', 'market', 'coin', 'dex', 'market_class', 'open', 'high', 'low', 'close', 'volume', 'trades'], 'parquet_count': 18} |
| funding | {'months': ['2025-05', '2025-06', '2025-07', '2025-08', '2025-09', '2025-10', '2025-11', '2025-12', '2026-01', '2026-02', '2026-03', '2026-04', '2026-05', '2026-06', '2026-07', '2026-08', '2026-09', '2026-10'], 'n_months': 18, 'total_rows': 4104648, 'schema': ['timestamp', 'market', 'coin', 'dex', 'funding_rate', 'premium'], 'parquet_count': 18} |
| open_interest | {'months': ['2025-05', '2025-06', '2025-07', '2025-08', '2025-09', '2025-10', '2025-11', '2025-12', '2026-01', '2026-02', '2026-03', '2026-04', '2026-05', '2026-06', '2026-07', '2026-08', '2026-09', '2026-10'], 'n_months': 18, 'total_rows': 3977432, 'schema': ['timestamp', 'market', 'coin', 'dex', 'mark_price', 'oracle_price', 'open_interest', 'open_interest_usd'], 'parquet_count': 18} |

_Source registry sha256: `046d98225067c3dbdf86c94cd47eb4f3de60e33a8cfec370b758fa636e7c2d75`_
