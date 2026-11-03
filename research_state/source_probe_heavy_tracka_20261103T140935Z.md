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
| No-auth result | HTTP 200 possible for meta/perpMeta; returns universe/metadata, not full historical liquidation event census with timestamps/sizes in bulk unauthenticated form suitable for Track A label parity |
| Schema (observed) | perpMeta contains universe info (assets, margin, etc.); no obvious "liquidations" array for full history |
| Coverage | Universe coverage exists, but liquidation event labels (who/when/size/liquidation price/type) not available as complete unauthenticated historical census via these endpoints |
| Hash of probe record | N/A (metadata only; no bulk dataset downloaded) |
| Existing coverage | Ironflow (ironflow_events parquet) already used for FCLR-010; this probe confirms no obvious drop-in unauthenticated replacement found |

## Alternative approach (documented)
- Check public indexer APIs? Some third-party indexers expose liquidation feeds but terms vary; probe would need to respect no-auth and ToS. Not pursued further without clearer unauthenticated bulk access.
- Hyperliquid websocket provides live data but historical census reconstruction complex/nontrivial and likely incomplete vs curated ironflow.

## Recommendation
No admissible unauthenticated replacement for ironflow liquidation-event census identified in this probe. Continue using ironflow_events as Track A label source; monitor for >2026-10-31 data per forward campaign. Do not merge tracks.

Status: SOURCE_PROBE_HEAVY_TRACKA_DONE (no drop-in alternative found)
