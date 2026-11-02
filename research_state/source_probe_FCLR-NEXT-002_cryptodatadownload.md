# Source Probe: FCLR-NEXT-002 — Family #8 — CryptoDataDownload / Venue-Native Archives

**Probe date:** 2026-11-02T01:00:00Z
**Source family:** CryptoDataDownload and other venue-native archives (all products, unauthenticated downloads)
**Campaign:** FCLR-NEXT-002
**Rubric:** unauthenticated==true AND no_keys==true AND symbols>=5 AND blocks>=3 (non-overlapping 30-day blocks) AND completeness_doc==true AND license_ok==true AND census_or_defensible==true

## Endpoints tested

| Endpoint | HTTP status | Result |
|---|---|---|
| https://www.cryptodatadownload.com/ | 200 | Site accessible |
| (scanned 170 links on homepage) | — | 0 liquidation links, 0 futures/perpetual links |

## Fields
N/A — no liquidation product found.

## Coverage
- Symbols: 0 (no liquidation product)
- Blocks: 0 non-overlapping 30-day blocks
- Earliest/latest timestamp: N/A
- Cadence: N/A

## License / terms
Unclear — no liquidation product available to evaluate.

## Completeness
Cannot document — no liquidation-label product found.

## GO/NO-GO verdict
**NO-GO** — Rubric FAILS on: symbols>=5 (0), blocks>=3 (0), completeness_doc (false), census_or_defensible (false). CryptoDataDownload homepage has no liquidation links and no futures/perpetual product links. No unauthenticated bulk liquidation census available.

## Bottleneck / removal
CryptoDataDownload does not offer liquidation-event data. This bottleneck cannot be removed within the admissible-source constraint.

## Next materially different route
None within CryptoDataDownload. Track A reopen requires a NEW admissible unauthenticated source outside CryptoDataDownload (e.g., Hyperliquid ironflow via HuggingFace, already admissible and used in FCLR-010).
