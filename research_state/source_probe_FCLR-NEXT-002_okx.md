# Source Probe: FCLR-NEXT-002 — Family #3 — OKX

**Probe date:** 2026-11-02T01:00:00Z
**Source family:** OKX public data endpoints and static.okx.com CDN
**Campaign:** FCLR-NEXT-002
**Rubric:** unauthenticated==true AND no_keys==true AND symbols>=5 AND blocks>=3 (non-overlapping 30-day blocks) AND completeness_doc==true AND license_ok==true AND census_or_defensible==true

## Endpoints tested

| Endpoint | HTTP status | Result |
|---|---|---|
| https://www.okx.com/ | 200 | Site accessible |
| https://static.okx.com/ | 403 | CDN access denied |
| https://www.okx.com/api/v5/public/data | 404 | No public bulk data endpoint |

## Fields
N/A — no downloadable liquidation data found.

## Coverage
- Symbols: 0 (no liquidation files)
- Blocks: 0 non-overlapping 30-day blocks
- Earliest/latest timestamp: N/A
- Cadence: N/A

## License / terms
Unclear — no liquidation product available to evaluate.

## Completeness
Cannot document — no historical liquidation census found.

## GO/NO-GO verdict
**NO-GO** — Rubric FAILS on: symbols>=5 (0), blocks>=3 (0), completeness_doc (false), census_or_defensible (false). OKX has no obvious public bulk liquidation history comparable to Binance's data.binance.vision; API requires auth for many endpoints; static CDN returns 403.

## Bottleneck / removal
OKX lacks an unauthenticated bulk liquidation census. This bottleneck cannot be removed within the admissible-source constraint.

## Next materially different route
None within OKX. Track A reopen requires a NEW admissible unauthenticated source outside OKX (e.g., Hyperliquid ironflow via HuggingFace, already admissible and used in FCLR-010).
