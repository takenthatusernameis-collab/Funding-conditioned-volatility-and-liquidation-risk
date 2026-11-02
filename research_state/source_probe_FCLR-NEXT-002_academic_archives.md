# Source Probe: FCLR-NEXT-002 — Family #5 — Academic / Institutional Archives

**Probe date:** 2026-11-02T01:00:00Z
**Source family:** Zenodo, OSF, arXiv supplements (dataset files, unauthenticated GET)
**Campaign:** FCLR-NEXT-002
**Rubric:** unauthenticated==true AND no_keys==true AND symbols>=5 AND blocks>=3 (non-overlapping 30-day blocks) AND completeness_doc==true AND license_ok==true AND census_or_defensible==true

## Endpoints tested

| Endpoint | HTTP status | Result |
|---|---|---|
| https://zenodo.org/api/ | 404 | API path not found at root |
| https://osf.io/api/v1/ | 404 | API path not found |
| https://arxiv.org/api/ | 302 | Redirect (not a direct dataset API) |

## Fields
N/A — no dataset files found.

## Coverage
- Symbols: 0 (no crypto perpetual liquidation datasets found)
- Blocks: 0 non-overlapping 30-day blocks
- Earliest/latest timestamp: N/A
- Cadence: N/A

## License / terms
Varies by dataset; no suitable dataset found to evaluate.

## Completeness
Cannot document — no matching dataset found.

## GO/NO-GO verdict
**NO-GO** — Rubric FAILS on: symbols>=5 (0), blocks>=3 (0), completeness_doc (false), census_or_defensible (false). No crypto perpetual liquidation event datasets found on Zenodo/OSF/arXiv with required coverage and license. Prior sweep (liquidation_sources_enumeration.md §84-92) confirms no match.

## Bottleneck / removal
Academic archives do not host crypto perpetual liquidation census datasets meeting the rubric. This bottleneck cannot be removed within the admissible-source constraint.

## Next materially different route
None within academic archives. Track A reopen requires a NEW admissible unauthenticated source outside academic archives (e.g., Hyperliquid ironflow via HuggingFace, already admissible and used in FCLR-010).
