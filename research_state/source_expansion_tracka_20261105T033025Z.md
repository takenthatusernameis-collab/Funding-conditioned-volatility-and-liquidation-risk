# SOURCE EXPANSION + CLASSIFICATION HARDENING (STEP 4)
Timestamp (UTC): __TS__
Git SHA (HEAD): 83e151d03dc1046b9af405e8c26f2c6b94c7614b

## Caches (already hardened)
- hunt_alternative_liquidation_sources.py: HF search cache (SEARCH_CACHE_PATH, TTL 24h), URL probe cache (URL_CACHE_PATH, TTL 6h), POST cache keyed by URL+body, dedup across candidates
- monitor_ironflow_liquidations.py: ETag/tree cache, per-file caching, baseline-drift probe, consolidation
- deep_review_alt_sources.py: reuses shared URL probe cache (cache_hits observed)

## Rubric (strict, enforced)
From hunt/deep review: min_symbols>=5 OR >=1 complete month OR >=3x30d blocks; completeness_doc_required true; license_ok true; unauthenticated_only true; no_requester_pays true; schema_compatible_fclr010 true. Hyperliquid-only for Track A per experiment frontier.

## Current findings (from probes)
- Hyperliquid public API (/info) returns data but appears to be market metadata (universe/margin) not historical liquidation census parquet - needs schema compatibility check
- ironflow/hyperliquid-liquidations dataset exists on HF (metadata visible) but files/months need inspection; monitor will check
- Other venues (Bybit/OKX/Deribit/CoinAPI/Kaiko/Tardis/Coinglass) either require keys/auth, 404s, or not liquidation census data

## Classification hardening needed
- Distinguish liquidation events vs fills vs trades vs funding vs insurance fund vs ADL
- Schema mapping to FCLR-010 expected fields
- Fixture-based tests for classification edge cases
- Every probe cached (already implemented)

## Actions taken
- Reviewed existing hardening (caches/dedup/rubric). Existing implementation is already strong from 004i work.
- Will extend tests if needed in step 6.
