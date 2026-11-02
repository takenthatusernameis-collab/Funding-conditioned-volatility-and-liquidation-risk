# Source Probe: FCLR-NEXT-002 — Family #2 — Bybit

**Probe date:** 2026-11-02T01:00:00Z
**Source family:** Bybit public archive (public.bybit.com)
**Campaign:** FCLR-NEXT-002
**Rubric:** unauthenticated==true AND no_keys==true AND symbols>=5 AND blocks>=3 (non-overlapping 30-day blocks) AND completeness_doc==true AND license_ok==true AND census_or_defensible==true

## Endpoints tested

| Endpoint | HTTP status | Result |
|---|---|---|
| https://public.bybit.com/ | 200 | Site accessible |
| https://public.bybit.com/linear/liquidation/ | 404 | No liquidation directory |
| https://public.bybit.com/spot/liquidation/ | 404 | No liquidation directory |
| https://public.bybit.com/archive/linear/liquidation/ | 404 | No liquidation directory |

## Fields
N/A — no liquidation data directory found.

## Coverage
- Symbols: 0 usable for liquidation census (trade CSVs exist but are not liquidation events)
- Blocks: 0 non-overlapping 30-day liquidation blocks
- Earliest/latest timestamp: N/A
- Cadence: N/A

## License / terms
Public data terms checked; no liquidation census product available in required form.

## Completeness
Cannot document — trades are not liquidation events; trade→liquidation conversion requires venue rules not published as a census.

## GO/NO-GO verdict
**NO-GO** — Rubric FAILS on: symbols>=5 (insufficient), blocks>=3 (0), completeness_doc (false — trades != census), census_or_defensible (false). Bybit public archive provides trade-level CSVs only; no unauthenticated complete liquidation event census archive surfaced.

## Bottleneck / removal
Bybit lacks a published unauthenticated liquidation census. This bottleneck cannot be removed within the admissible-source constraint. Prior sweep (track_a_deadend_map.md) confirms: no `liquidation/` directory; trades cannot be converted to a complete liquidation census without venue rules.

## Next materially different route
None within Bybit public archive. Track A reopen requires a NEW admissible unauthenticated source outside Bybit (e.g., Hyperliquid ironflow via HuggingFace, already admissible and used in FCLR-010).
