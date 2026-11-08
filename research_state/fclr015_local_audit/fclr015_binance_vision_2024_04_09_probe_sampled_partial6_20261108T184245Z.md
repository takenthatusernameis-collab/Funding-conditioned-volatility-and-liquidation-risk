# FCLR-015 Binance Vision provenance probe 2024-04..09 (20261108T184245Z_sampled_partial6)

- method: bounded unauthenticated GET vs local cached zip sha256/etag (sampled days)
- source_base: https://data.binance.vision/
- cache_identity_vs_binance_vision: **GO_SAMPLED_OR_PARTIAL**
- confirmatory_claim_go: **NO_GO** (frozen prereg before outcomes + leakage/split controls still required)
- summary: {"match": 6, "mismatch": 0, "missing_local": 0, "missing_remote": 0, "new_checks_this_run": 6, "remote_error": 0, "total": 6}

## Notes
Binance Vision public historical market data; accessed unauthenticated via HTTPS. Verify Binance Vision/market-data terms before redistribution; checksums/provenance evidence only.
Sampling: day 1,15,28,last per month × 4 kline kinds × 5 symbols + monthly fundingRate (bounded). Use --full-days for exhaustive daily coverage.
MATCH means local cached zip sha256 == remote Binance Vision zip sha256 (HTTP 200/ETag recorded). Full-coverage manifest/hashes recommended before confirmatory Gate 4 rerun.

## Result counts
- MATCH: 6
