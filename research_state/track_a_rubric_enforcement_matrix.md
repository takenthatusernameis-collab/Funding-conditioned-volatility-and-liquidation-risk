# Track A Rubric Enforcement Matrix — Observed Liquidations (H004)

**Document type:** Decision-grade rubric enforcement matrix (heavy evidence artifact)
**Repository:** Funding-conditioned-volatility-and-liquidation-risk
**Generated:** 2026-10-31T14:16:58Z
**HEAD:** a915cd38 (main). Working tree clean except untracked `scripts/__pycache__/`, `tests/__pycache__/`.
**Hypothesis:** FCLR-H004 (Track A) — observed forced-liquidation labels improve forecasting.
**Status:** STRUCTURALLY BLOCKED — no admissible unauthenticated source passes ALL rubric items.
**Priority:** Track A is P1 per repo-name inference (Track C > Track A > Track B).

## Machine-checkable rubric (verbatim; ALL must pass, ANY failure → NO-GO)
`unauthenticated==true AND no_keys==true AND symbols>=5 AND blocks>=3 AND completeness_doc==true AND license_ok==true AND census_or_defensible==true`

Source: `research_state/track_a_final_block_proof.md:9-18, 50-51`; RESEARCH_PROMPT.md §16.

## Full candidate evaluation table (consolidated; all enumerated candidates)
| Candidate | unauth | no_keys | symbols>=5 | blocks>=3 | completeness_doc | license_ok | census/defensible | Result | Evidence artifacts |
|---|---|---|---|---|---|---|---|---|---|
| Binance forceOrders/fapi liquidation endpoints | false/blocked (451/restricted) | mixed | no/insufficient | no | unclear/partial | unclear/restricted | no (not full unauth census) | NO-GO | `research_state/binance_source_probe.md`; `research_state/liquidation_sources_enumeration.md` |
| Bybit public liquidation data | partial (no full unauth historical census) | mixed | insufficient | 1 window only (~30d) exhausted | unclear | unclear | incomplete | NO-GO | `research_state/evaluation_summary_FCLR005.md` (pilot, single window exhausted); `research_state/liquidation_source_campaign.md` |
| OKX/Deribit unauth liquidation history | no full census | unclear | no | <3 | no/unclear | unclear | not census | NO-GO | `research_state/liquidation_sources_enumeration.md` |
| HF/academic liquidation tick datasets (ochinimus-style) | sometimes unauth but limited access/range | varies | insufficient | 1 window exhausted (2026-07-08..2026-08-06) | partial | varies | no (single window) | NO-GO | `research_state/evaluation_summary_FCLR005.md`; `research_state/liquidation_source_campaign.md` |
| GitHub/Zenodo scraped liquidation datasets | unauth sometimes | yes | insufficient (<5 or incomplete) | <3 non-overlapping 30d blocks | missing | varies/unclear | no (not defensible census) | NO-GO | `research_state/liquidation_sources_enumeration.md` §84-92 |
| Aggregators/third-party APIs | auth/keys or restricted | no | N/A | N/A | no | restricted/unclear | no | NO-GO | probes/enumerations |

Sources: `research_state/track_a_final_block_proof.md:24-31, 71-78`; `research_state/track_a_deep_sweep.md`; `research_state/track_a_deadend_map.md`; `research_state/track_a_structural_block.md`.

## Result summary
- Candidates evaluated: 6 (all enumerated)
- Candidates passing ALL rubric items: 0
- Structural blockers: auth-required/451/geo-restricted endpoints; missing documented completeness across >=3 non-overlapping 30-day blocks for >=5 symbols; license/census indefensible; single-window exhaustion (FCLR-005 pilot).
- Track A status: **STRUCTURALLY BLOCKED**. Confirmatory Track A CLOSED without a new admissible source.

## Sole reopen condition (verbatim; strictly enforced)
A NEW admissible unauthenticated source (no keys) meeting ALL rubric items above with concrete machine-checkable evidence (endpoint/docs, coverage table, license, census definition). If such a candidate appears: FREEZE, pre-register experiment/protocol BEFORE any outcome inspection (RESEARCH_PROMPT.md §16), apply rubric strictly with evidence. Do not relax constraints. Source: `research_state/track_a_final_block_proof.md:36-43, 82-84`.

## Artifacts (traceability)
- `research_state/track_a_final_block_proof.md`
- `research_state/track_a_deadend_map.md` (MACHINE_CHECKABLE_FIREWALL_20261031)
- `research_state/track_a_structural_block.md`
- `research_state/track_a_deep_sweep.md`
- `research_state/liquidation_sources_enumeration.md`
- `research_state/binance_source_probe.md`
- `research_state/evaluation_summary_FCLR005.md` (pilot/exploratory only; confirms single-window exhaustion)

## Tests
`python -m unittest discover -s tests -v` → 27/27 PASS at HEAD a915cd38 (must remain green; Track A block is structural, not a test failure).
