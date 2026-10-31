# Track A Rubric Enforcement Matrix — ACTIVE SWEEP (HARDENED)

UPDATED: 2026-10-31T21:06:41Z
HEAD: e2f3f417f07ee62bcacefa2762effa2035ed0e55
HYPOTHESIS: FCLR-H004 (observed liquidation outcomes)
STATUS: STRUCTURALLY BLOCKED — ACTIVE SWEEP MANDATED

## Verbatim rubric (ALL must pass)
`unauthenticated==true AND no_keys==true AND symbols>=5 AND blocks>=3 (non-overlapping 30-day blocks) AND completeness_doc==true AND license_ok==true AND census_or_defensible==true`

If ANY item fails → NO-GO. No relaxation without concrete evidence and pre-registration.

## Active sweep log (concrete probes)
| Candidate (source/endpoint) | unauthenticated | no_keys | symbols>=5 | blocks>=3 (30d non-overlap) | completeness_doc | license_ok | census_or_defensible | Auth/HTTP/probe notes | GO/NO-GO | Evidence (file:line/probe) |
|---|---|---|---|---|---|---|---|---|---|---|
| Binance fapi forceOrders/liquidation endpoints | false/restricted (451 observed in probes) | mixed/unclear | insufficient for confirmatory census | <3 / no documented multi-block census | partial/unclear | unclear/restricted | no (not full unauth census) | See binance_source_probe.md; 404/451 in tested contexts | NO-GO | research_state/binance_source_probe.md |
| Bybit public liquidation data | partial (no full unauth historical census) | mixed | insufficient for frozen 2024; 2026 only | 1 window (~30d) exhausted by FCLR-005 | unclear/missing for confirmatory scope | unclear | incomplete census | Used only for FCLR-005 pilot (single window exhausted) | NO-GO | research_state/evaluation_summary_FCLR005.md, research_state/liquidation_source_campaign.md |
| OKX/Deribit unauthenticated history | no full unauth census found | unclear | insufficient | <3 | no/unclear | unclear | no | Enumerated, no admissible path | NO-GO | research_state/liquidation_sources_enumeration.md |
| HF/academic datasets (ochinimus-style) | unauth sometimes but access/range limited | varies | insufficient for >=3 blocks in required windows | 1 window (2026-07-08..2026-08-06) exhausted | partial | varies/unclear | no (single window, exhausted) | FCLR-005 pilot only | NO-GO | research_state/liquidation_source_campaign.md, research_state/evaluation_summary_FCLR005.md |
| GitHub/Zenodo scraped liquidation datasets | unauth sometimes | yes | <5 or incomplete coverage | <3 non-overlapping 30d blocks | missing documented completeness | varies/unclear | not defensible as full census | §84-92 enumeration | NO-GO | research_state/liquidation_sources_enumeration.md §84-92 |
| Aggregators/third-party APIs | restricted/auth/keys or rate-limited | no | N/A | N/A | no | restricted/unclear | no | Probed, inadmissible | NO-GO | research_state/liquidation_sources_enumeration.md |

## Deadend map (updated)
See research_state/track_a_deadend_map.md (MACHINE_CHECKABLE_FIREWALL_20261031, hardened). All routes exhausted for confirmatory requirements.

## Sole reopen condition
NEW admissible unauthenticated source (no keys) meeting ALL rubric items with concrete evidence:
- documented endpoint/docs showing unauthenticated access
- full census definition (what is included/excluded, coverage completeness)
- >=5 symbols with historical depth
- >=3 non-overlapping 30-day blocks with dates/timestamps
- license/ToS allowing research use
- concrete HTTP/probe results, sample data, coverage table, hashes if files

If found: pre-register experiment/protocol BEFORE outcome inspection per RESEARCH_PROMPT §16, run rubric enforcement, record in this matrix with file:line evidence.

## Status
STRUCTURALLY BLOCKED — ACTIVE SWEEP REQUIRED. No candidate passes rubric. Continue enumeration but do not relax constraints.
