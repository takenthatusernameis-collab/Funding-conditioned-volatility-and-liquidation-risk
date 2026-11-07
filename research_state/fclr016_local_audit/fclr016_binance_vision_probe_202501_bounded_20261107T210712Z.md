# FCLR-016 Binance Vision provenance probe 2025+ (20261107T210712Z_202501_bounded)

- method: bounded unauthenticated GET vs local cached zip sha256/etag (FCLR-016, 2025+ probe)
- cache_identity_vs_binance_vision: **NO_GO**
- confirmatory_claim_go: **NO_GO** (identity evidence only; prereg/leakage/license/completeness required)
- summary: `{"match": 2, "mismatch": 4, "missing_local": 0, "missing_remote": 0, "new_this_run": 6, "remote_error": 0, "total": 6}`

## FCLR-014 context
2025+ cache provenance UNVERIFIED per fclr014_provenance_decision_20261107T133102Z.md; identity match is necessary but not sufficient (license/terms/completeness/leakage/prereg still required).

## Result counts
- MATCH: 2
- MISMATCH: 4

## Non-MATCH (first 60)
- MISMATCH BTCUSDT 2025-01 klines 2025-01-01 local=1ab87f7ca2a54d08 remote=5076115def7504d4
- MISMATCH BTCUSDT 2025-01 klines 2025-01-31 local=c1e5a5a1eb03acb0 remote=583eb6a6e0e1a579
- MISMATCH ETHUSDT 2025-01 klines 2025-01-01 local=dac481802308a61e remote=ce3c5c3518034814
- MISMATCH ETHUSDT 2025-01 klines 2025-01-31 local=cab349faf9727c6d remote=a96cd7b865d74a0b
