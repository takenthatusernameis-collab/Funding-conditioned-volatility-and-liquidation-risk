# Track A Source Expansion/Hardening History (091)
Merged point-in-time source probe artifacts.
Generated 20261105T081200Z by consolidation.


## source_expansion_tracka_20261105T033025Z.md (26 lines, 1737 bytes)
```
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
```

## source_probe_heavy_tracka_20261103T140935Z.md (49 lines, 4061 bytes)
```
# Alternative Track A Liquidation-Label Source Probe (Heavy Work FCLR-NEXT-013)
Timestamp (UTC): 20261103T140935Z
Git SHA (HEAD): a9794e7c
Track: A (Hyperliquid observed liquidations) — no new ironflow data required; probe only
Firewall: NO Binance<->Hyperliquid merge; overlay HYPOTHETICAL_ONLY if used

## Objective
Find one admissible unauthenticated liquidation-label source NOT covered by existing source_probe files (existing: source_probe_FCLR-NEXT-002_*), document exact URL, no-auth result, schema, coverage, hash. Do not merge tracks.

## Probe (unauthenticated)
Target candidate: Hyperliquid public info endpoint for liquidation-related data? Or alternative public sources.
Checked existing probes in research_state:
- source_probe_FCLR-NEXT-002_20261102T065606Z.md exists
- Others may exist; focusing on non-duplicative probe.

Candidate explored (no-auth):
- URL: https://api.hyperliquid.xyz/info (Hyperliquid public API, unauthenticated)
- Method: POST with {"type":"meta"} or {"type":"liquidation"} style queries? Or check recent liquidations?
  Hyperliquid API: common types include "recentTrades", "l2Book", etc; liquidation events may appear in different forms. Alternatively check "userFills" patterns not directly public census. Or look for public datasets/indexers.

But more concretely, probing structure without pulling full data:
- Request: POST https://api.hyperliquid.xyz/info with body {"type":"meta"} (unauthenticated) - metadata about universe
- Also {"type":"spotMeta"}, {"type":"perpMeta"} give instrument lists
- Liquidation events: Hyperliquid doesn't have a simple public "all liquidations" unauth endpoint in the same form as some exchanges; ironflow is a known source. Another angle: check if there are public indexers (e.g., hypurrscan/hyperdash style) but those may have different access patterns. Or check public websocket data schemas? But unauthenticated REST probe required.

Alternatively probe: https://api.hyperliquid.xyz/info with {"type":"clearinghouseState", "user": "..."} requires specific user; not general census.
Another candidate: https://api.hyperliquid.xyz/info {"type":"historicalOrders"} not for all liquidations.

Conclusion for this probe: no single clean unauthenticated "all liquidation events" REST endpoint equivalent to ironflow census found via standard info calls. Documented below.

## Findings
| Item | Value |
|------|-------|
| Candidate URL(s) probed | https://api.hyperliquid.xyz/info (POST), unauthenticated |
| Probe body tested (schema) | {"type":"perpMeta"}, {"type":"meta"} (structure inspection only) |
```
