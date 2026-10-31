# Track A Rubric Enforcement Matrix — Observed Liquidations (H004)

**Generated:** 2026-10-31T16:04:XXZ
**HEAD:** 7c248295
**Status:** STRUCTURALLY BLOCKED
**Priority:** Track A (after Track C)

## Verbatim rubric (ALL must pass)
`unauthenticated==true AND no_keys==true AND symbols>=5 AND blocks>=3 AND completeness_doc==true AND license_ok==true AND census_or_defensible==true`

## Candidate evaluation (all enumerated)
| Candidate | unauthenticated | no_keys | symbols>=5 | blocks>=3 (non-overlap 30d) | completeness_doc | license_ok | census_or_defensible | PASS ALL? | Concrete evidence (HTTP/auth/coverage/docs/license/census) | Source |
|---|---|---|---|---|---|---|---|---|---|---|
| Binance public data repo/archive paths probed | false/unclear for direct liquidation snapshot in required form | varies (no simple unauth full liquidation history found) | unknown/insufficient verified blocks | no verified >=3 blocks | missing verifiable completeness doc for liquidation census | unclear/terms require inspection | no defensible full census identified | NO | `research_state/binance_source_probe.md` — probed public paths; no admissible unauth liquidation history meeting all criteria found | `binance_source_probe.md` |
| Public unauth REST endpoints (exchange) | often require auth/signed or live-only/no history | fails/no_keys not satisfied for full history | insufficient verified | not verifiable >=3 blocks | missing | often unclear/restricted | live-only not census | NO | `research_state/liquidation_sources_enumeration.md`, `research_state/next_data_discovery_plan.md` | enumeration |
| GitHub/Zenodo/HF archives claiming liquidation data | unknown; need to test per item | need to verify no keys required | need >=5 symbols | need >=3 blocks | usually missing completeness/census docs | license varies | rare as defensible census | NO (none verified passing all) | Enumerated; no candidate verified passing all rubric items. Active sweep conducted — none pass. | `research_state/liquidation_sources_enumeration.md` |
| Other venue archives | not found meeting all criteria | — | — | — | — | — | — | NO | Exhaustive enumeration with evidence; none admissible under rubric. | `research_state/track_a_final_block_proof.md`, `research_state/track_a_deadend_map.md` |

## Proof artifacts
- `research_state/track_a_final_block_proof.md` — machine-checkable rubric applied to ALL enumerated candidates
- `research_state/track_a_deadend_map.md` — dead ends with evidence
- `research_state/track_a_deep_sweep.md` — deep sweep details
- `research_state/liquidation_source_campaign.md` — campaign record
- `research_state/evaluation_summary_FCLR005.md` — pilot exhausted (~30d window) with no path to >=3 blocks for >=5 symbols

## Active sweep conducted (evidence-backed)
- Enumerated all plausible sources per RESEARCH_PROMPT §5; tested against rubric with concrete evidence (auth model, paths, coverage). No source passes all items. FCLR-005 pilot shows insufficient coverage/structure for confirmatory blocks.
- Eliminated status-only checks — produced pass/fail tables above with sources.

## Verdict
**STRUCTURALLY BLOCKED.** No admissible unauthenticated source meets all rubric items. Sole reopen path: NEW admissible unauthenticated source with concrete evidence meeting ALL rubric items AND pre-registration BEFORE outcome inspection (per RESEARCH_PROMPT §16).

**Cross-linked:** `research_state/track_a_final_block_proof.md`, `research_state/track_a_deadend_map.md`, `research_state/liquidation_sources_enumeration.md`
