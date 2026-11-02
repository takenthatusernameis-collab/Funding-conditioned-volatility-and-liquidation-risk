# Source Probe: FCLR-NEXT-002 — Family #1 — Alternative Binance Paths

**Probe date:** 2026-11-02T01:00:00Z
**Source family:** Alternative Binance public data archive paths (data.binance.vision)
**Campaign:** FCLR-NEXT-002
**Rubric:** unauthenticated==true AND no_keys==true AND symbols>=5 AND blocks>=3 (non-overlapping 30-day blocks) AND completeness_doc==true AND license_ok==true AND census_or_defensible==true

## Endpoints tested

| Endpoint | HTTP status | Result |
|---|---|---|
| https://data.binance.vision/data/futures/um/daily/liquidationSnapshot/ | 404 | NoSuchKey — path does not exist |
| https://data.binance.vision/data/futures/um/daily/liquidations/ | 404 | NoSuchKey — path does not exist |
| https://data.binance.vision/data/futures/um/daily/liquidationHistory/ | 404 | NoSuchKey — path does not exist |
| https://data.binance.vision/data/futures/um/daily/forceLiquidation/ | 404 | NoSuchKey — path does not exist |
| https://data.binance.vision/data/futures/um/monthly/liquidationSnapshot/ | 404 | NoSuchKey — path does not exist |
| https://fapi.binance.com/fapi/v1/forceOrders | 451 | Geo-restricted / unavailable in this environment |

## Fields
N/A — no downloadable files found.

## Coverage
- Symbols: 0 (no files)
- Blocks: 0 non-overlapping 30-day blocks
- Earliest/latest timestamp: N/A
- Cadence: N/A

## License / terms
Unclear — required data not present, so license cannot be evaluated.

## Completeness
Cannot document — no archive exists at tested paths.

## GO/NO-GO verdict
**NO-GO** — Rubric FAILS on: symbols>=5 (0), blocks>=3 (0), completeness_doc (false), census_or_defensible (false). No Binance liquidation census archive exists at any tested unauthenticated path.

## Bottleneck / removal
Binance liquidation labels are structurally unavailable unauthenticated. This bottleneck cannot be removed within the admissible-source constraint. Prior probe (binance_source_probe.md, 2026-10-25) confirms: liquidationSnapshot 404, fapi forceOrders 451.

## Next materially different route
None within Binance. Track A reopen requires a NEW admissible unauthenticated source outside Binance (e.g., Hyperliquid ironflow via HuggingFace, already admissible and used in FCLR-010).
