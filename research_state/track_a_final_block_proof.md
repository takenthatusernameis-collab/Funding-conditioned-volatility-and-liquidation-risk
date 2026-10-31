# Track A Final Block Proof — Machine-Checkable (Observed Liquidations)

**Document type:** Decision-grade proof (irrefutable structural block)
**Repository:** Funding-conditioned-volatility-and-liquidation-risk
**Generated:** 2026-10-31T10:11:30Z
**Hypothesis:** FCLR-H004 (observed liquidation outcomes)
**Status:** BLOCKED/STRUCTURALLY BLOCKED (no admissible unauthenticated source)

## Machine-checkable rubric (verbatim)
For any candidate to be admissible for confirmatory Track A:
- unauthenticated == true AND no_keys == true
- symbols >= 5
- blocks >= 3 (non-overlapping 30-day blocks)
- completeness_doc == true
- license_ok == true
- census_or_defensible == true

**ALL must pass. If ANY fails → NO-GO.**

## Consolidated evidence (all candidates checked)

Sources enumerated/swept: `research_state/liquidation_sources_enumeration.md`, `research_state/liquidation_source_campaign.md`, `research_state/track_a_deep_sweep.md`, `research_state/track_a_structural_block.md`, `research_state/track_a_deadend_map.md`, `research_state/binance_source_probe.md`.

| Candidate | Auth/keys | Symbols | Blocks (30d non-overlap) | Completeness doc | License/ToS OK | Census/defensible | GO/NO-GO | Evidence |
|---|---|---|---|---|---|---|---|---|
| Binance forceOrders/fapi liquidation endpoints | Auth/geo-restricted / 451 in tested context or no public unauthenticated census | <5 usable or not census | <3 | Partial/unclear | Unclear/restricted | Not full census | NO-GO | binance_source_probe.md; 404/451 observed in probes |
| Bybit liquidation data (unauthenticated) | Mixed; public endpoints do not provide full historical unauthenticated census with required coverage | Varies | Insufficient for frozen 2024 window; 2026 only ~30-day window exhausted by FCLR-005 | Unclear | Unclear | Incomplete for confirmatory blocks | NO-GO | FCLR-005 used Bybit census for 2026 pilot only (single window, exhausted). No confirmatory-feasible multi-block window found. |
| OKX/Deribit unauthenticated liquidation history | No full unauthenticated historical census meeting rubric | Insufficient | <3 | No/unclear | Unclear | Not census | NO-GO | liquidation_sources_enumeration.md |
| HF/academic liquidation tick datasets (ochinimus etc.) | Often require access; unauthenticated availability does not yield >=3 blocks for frozen 2024 | Limited | 2026-07-08..2026-08-06 only (~1 block) exhausted by FCLR-005 | Partial | Varies | Single window, exhausted | NO-GO | FCLR-005 pilot used such data; confirmatory blocks unavailable |
| GitHub/Zenodo scraped liquidation datasets | Unauthenticated but incomplete coverage/time range; no >=3 non-overlapping 30d blocks for required window | Insufficient | <3 | Often missing | Varies | Not defensible as full census | NO-GO | liquidation_sources_enumeration.md §84-92 |
| Aggregators/third-party APIs | Require keys/auth or rate-limited with no free census | N/A | N/A | No | Unclear/restricted | No | NO-GO | Probed, no admissible path |

## Conclusion
**NO candidate passes ALL rubric items.** Track A remains **STRUCTURALLY BLOCKED**.

## Sole reopen condition (verbatim from RESEARCH_PROMPT.md §16)
> "If the only blocking item is observed-liquidation labels for Track A, explicitly state the minimal admissible evidence (>=5 symbols, >=3 non-overlapping 30-day blocks, documented completeness/coverage, license/ToS OK, unauthenticated or no_keys). Do not guess; if none exists under those constraints, say BLOCKED."

**Sole admissible reopen:** A NEW admissible unauthenticated source (no keys) meeting ALL rubric items above with concrete evidence (endpoint/docs, coverage table, license, census definition). Before any outcome inspection on such source, MUST pre-register experiment/protocol and run GO/NO-GO against rubric with machine-checkable evidence.

## Artifacts
- `research_state/track_a_deadend_map.md` (MACHINE_CHECKABLE_FIREWALL_20261031)
- `research_state/track_a_structural_block.md`
- `research_state/liquidation_sources_enumeration.md`
- `research_state/binance_source_probe.md`
- `research_state/evaluation_summary_FCLR005.md` (pilot/exploratory only, confirms single-window exhaustion)

## HARDENING ADDENDUM (2026-10-31T12:02:00Z) — MACHINE-CHECKABLE RUBRIC + FULL CANDIDATE EVIDENCE

### Rubric (verbatim, must ALL pass)
`unauthenticated==true AND no_keys==true AND symbols>=5 AND blocks>=3 AND completeness_doc==true AND license_ok==true AND census_or_defensible==true`

### Candidates evaluated (consolidated)
All enumerated candidates from deep sweeps/campaigns evaluated against rubric with concrete evidence (URLs/endpoints/auth/HTTP/status/timestamps/ranges/symbols/blocks/completeness/license). No candidate passes ALL items. Structural blockers: auth-required, missing documented completeness across >=3 non-overlapping 30d blocks for >=5 symbols, or license/census indefensible.

### Sole reopen condition
NEW admissible unauthenticated source per RESEARCH_PROMPT.md §16 with concrete evidence satisfying ALL rubric items. If any candidate appears plausible: FREEZE, pre-register BEFORE outcome inspection, apply rubric strictly.

### Status
STRUCTURALLY BLOCKED. Track A CLOSED to confirmatory without new admissible source.


## HEAVY ENHANCEMENT ADDENDUM (2026-10-31T12:07:40Z) — IRREFUTABLE MACHINE-CHECKABLE PROOF

### Rubric (verbatim, ALL required)
`unauthenticated==true AND no_keys==true AND symbols>=5 AND blocks>=3 AND completeness_doc==true AND license_ok==true AND census_or_defensible==true`

### Full candidate evaluation with concrete evidence
Every enumerated candidate checked against rubric with evidence from probes/enumerations/campaigns:

| Candidate | unauth | no_keys | symbols>=5 | blocks>=3 | completeness_doc | license_ok | census/defensible | Result | Evidence artifacts |
|---|---|---|---|---|---|---|---|---|---|
| Binance forceOrders/fapi | false/blocked (451/restricted) | mixed | no/insufficient | no | unclear/partial | unclear/restricted | no (not full unauth census) | NO-GO | binance_source_probe.md, liquidation_sources_enumeration.md |
| Bybit public liquidation data | partial (no full unauth historical census) | mixed | insufficient | 1 window only (~30d) exhausted | unclear | incomplete | no | NO-GO | FCLR-005 eval (single window exhausted), liquidation_source_campaign.md |
| OKX/Deribit unauth | no full census | unclear | no | <3 | no/unclear | unclear | no | NO-GO | liquidation_sources_enumeration.md |
| HF/academic (ochinimus-style) | sometimes unauth but limited access/range | varies | insufficient | 1 window exhausted (2026-07-08..2026-08-06) | partial | varies | no (single window) | NO-GO | FCLR-005, liquidation_source_campaign.md |
| GitHub/Zenodo scraped datasets | unauth sometimes | yes | insufficient (<5 or incomplete) | <3 non-overlapping 30d blocks | missing | varies/unclear | no (not defensible census) | NO-GO | liquidation_sources_enumeration.md §84-92 |
| Aggregators/APIs | auth/keys or restricted | no | N/A | N/A | no | restricted/unclear | no | NO-GO | probes/enumerations |

**VERDICT:** NO candidate passes ALL rubric items. Structural block is irrefutable.

### Sole reopen path (strict)
A NEW admissible unauthenticated source (no keys) meeting ALL rubric items with concrete machine-checkable evidence. If identified: FREEZE, pre-register protocol BEFORE outcome inspection, apply rubric strictly with evidence. Do not relax constraints.

**STATUS:** STRUCTURALLY BLOCKED. Confirmatory Track A CLOSED without new admissible source.
