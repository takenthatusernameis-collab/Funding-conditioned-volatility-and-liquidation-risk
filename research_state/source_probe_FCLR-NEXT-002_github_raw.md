# Source Probe: FCLR-NEXT-002 — Family #6 — GitHub Raw

**Probe date:** 2026-11-02T01:00:00Z
**Source family:** Public GitHub repos containing CSV/Parquet liquidation or perp mark-price data (raw content, unauthenticated)
**Campaign:** FCLR-NEXT-002
**Rubric:** unauthenticated==true AND no_keys==true AND symbols>=5 AND blocks>=3 (non-overlapping 30-day blocks) AND completeness_doc==true AND license_ok==true AND census_or_defensible==true

## Endpoints tested

| Endpoint | HTTP status | Result |
|---|---|---|
| https://api.github.com/search/repositories?q=crypto+liquidation+data&per_page=10 | 200 (rate-limited search) | Repos found but code search requires auth (401) |
| https://raw.githubusercontent.com/ | 301 | Redirect (raw content accessible) |

## Repos surfaced (not liquidation census datasets)

| Repo | Stars | Description | Assessment |
|---|---|---|---|
| SpiralDevelopment/crypto-hft-data | 78 | WebSocket HFT data collector | Real-time collector, not historical census |
| ruleaker/awesome-derivatives-data | 3 | Curated list of crypto derivatives data resources | Index/link list, not a dataset |
| Co-Messi/HyperData-Terminal | 26 | Trading terminal for multiple venues | Tool, not a dataset |
| DevAkhil/Crypto-Liquidation-API | 2 | .NET Core API via Selenium | Requires scraping, not a census archive |
| afelder11/crypto-liquidation-datastream | 0 | Live liquidation datastream | Live stream, not historical census |

## Fields
N/A — no raw CSV/Parquet liquidation census files found.

## Coverage
- Symbols: 0 (no census dataset with ≥5 symbols)
- Blocks: 0 non-overlapping 30-day blocks
- Earliest/latest timestamp: N/A
- Cadence: N/A

## License / terms
Varies by repo; no suitable dataset found to evaluate.

## Completeness
Cannot document — no curated liquidation label set found.

## GO/NO-GO verdict
**NO-GO** — Rubric FAILS on: symbols>=5 (0), blocks>=3 (0), completeness_doc (false), census_or_defensible (false). GitHub code search requires authentication (401); raw content is accessible but no public repo with ≥5 symbols, ≥3 non-overlapping 30-day blocks, documented completeness liquidation census surfaced.

## Bottleneck / removal
GitHub lacks a curated unauthenticated liquidation census dataset meeting the rubric. This bottleneck cannot be removed within the admissible-source constraint.

## Next materially different route
None within GitHub raw. Track A reopen requires a NEW admissible unauthenticated source outside GitHub (e.g., Hyperliquid ironflow via HuggingFace, already admissible and used in FCLR-010).
