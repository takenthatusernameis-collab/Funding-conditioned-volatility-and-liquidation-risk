# Source Probe: FCLR-NEXT-002 — Family #4 — Deribit

**Probe date:** 2026-11-02T01:00:00Z
**Source family:** Deribit historical data (historical.deribit.com)
**Campaign:** FCLR-NEXT-002
**Rubric:** unauthenticated==true AND no_keys==true AND symbols>=5 AND blocks>=3 (non-overlapping 30-day blocks) AND completeness_doc==true AND license_ok==true AND census_or_defensible==true

## Endpoints tested

| Endpoint | HTTP status | Result |
|---|---|---|
| https://historical.deribit.com/ | 000 | Connection failed (no response) |

## Fields
N/A — endpoint unreachable.

## Coverage
- Symbols: 0
- Blocks: 0 non-overlapping 30-day blocks
- Earliest/latest timestamp: N/A
- Cadence: N/A

## License / terms
Unclear — endpoint unreachable, cannot evaluate.

## Completeness
Cannot document — endpoint unreachable.

## GO/NO-GO verdict
**NO-GO** — Rubric FAILS: endpoint unreachable (connection error), symbols>=5 (0), blocks>=3 (0), completeness_doc (false), census_or_defensible (false). No admissible unauthenticated Deribit perp liquidation history accessible.

## Bottleneck / removal
Deribit historical endpoint unreachable in this environment. This bottleneck cannot be removed within the admissible-source constraint.

## Next materially different route
None within Deribit. Track A reopen requires a NEW admissible unauthenticated source outside Deribit (e.g., Hyperliquid ironflow via HuggingFace, already admissible and used in FCLR-010).
