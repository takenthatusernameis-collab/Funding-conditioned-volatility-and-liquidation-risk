# Cross-Track Decision Log (C → A → B → H002)

UPDATED: 2026-10-31T18:59:09Z
HEAD: cee31508
PRIORITY: Repo-name driven (funding-conditioned volatility first)

## Decisions
| Track | Decision | Rationale (evidence) | Artifacts |
|---|---|---|---|
| C (H001/FCLR) | NOT_SUPPORTED — CONFIRMATORY CLOSED. Risk overlay INELIGIBLE (§9). | FCLR-003 powered: C2 vs B1 ΔQLIKE=+0.015205, 95% CI [-0.020240,0.056734] crosses zero (-3.78% worse). C1 helps alone but full spec degrades; FCLR-006/007 worse/underpowered. Leakage controls passed, gates enforced. | `research_state/track_c_traceability_matrix.md`, `research_state/track_c_final_synthesis_dossier.md`, `research_state/evaluation_summary_FCLR003.md`, `research_state/leakage_audit.md` |
| A (H004) | STRUCTURALLY BLOCKED. | Verbatim rubric applied to ALL enumerated candidates; no candidate passes all items (unauthenticated/no_keys/symbols>=5/blocks>=3/completeness_doc/license_ok/census_or_defensible). FCLR-005 pilot exhausted. | `research_state/track_a_rubric_enforcement_matrix.md`, `research_state/track_a_final_block_proof.md`, `research_state/track_a_deadend_map.md`, `research_state/liquidation_sources_enumeration.md`, `research_state/evaluation_summary_FCLR005.md` |
| B (H003) | CLOSED_NEGATIVE. Strict separation proven. | FCLR-H003-EXT-001: no robust incremental skill after Holm correction across 16 cells. Codepath grep shows `liquidat*` isolated to Track A (h004*) vs Track B (synthetic_boundary_labels/run_h003*) with explicit non-conflation; no mixing. | `research_state/track_b_codepath_separation_matrix.md`, `research_state/track_b_separation_proof_hardened.md`, `research_state/track_b_definitive_separation_audit.md`, `research_state/evaluation_summary_FCLR-H003-EXT-001.md` |
| H002 | EXPLORATORY/PARTIAL only. No promotion. | 88 events, 84 corrected, 4 censored. Pre-registered BEFORE outcome inspection in `research_state/h002_pre_registration.md`. No concrete admissible path to confirmatory per RESEARCH_PROMPT §16 identified; do not conflate with volatility skill/boundary breaches/observed liquidations. | `research_state/h002_pre_registration.md` |

## Cross-links
All artifacts above cross-linked. HEAD consistent at cee31508. Tests 27/27 PASS.

## Synthesis
Priority order strictly followed (C→A→B→H002). Bottlenecks removed with concrete evidence. No reopen paths without meeting strict pre-registration/gate constraints.
