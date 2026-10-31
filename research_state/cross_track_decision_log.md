# Cross-Track Decision Log (C → A → B → H002)

**Generated:** 2026-10-31T16:04:XXZ
**HEAD:** 7c248295
**Priority (repo name):** Track C > Track A > Track B > H002

## Decisions
| Track | Status | Decision | Evidence |
|---|---|---|---|
| **Track C (H001, funding-conditioned volatility)** | NOT_SUPPORTED — CONFIRMATORY CLOSED | C2 vs B1 fails gate in powered window (CI crosses zero, worse). C1 helps alone but full price+funding degrades. Risk overlay INELIGIBLE (§9). No reopen without pre-registration + holdout discipline violations with evidence. | `research_state/track_c_traceability_matrix.md`, `research_state/evaluation_summary_FCLR003.md`, `research_state/track_c_final_synthesis_dossier.md` |
| **Track A (H004, observed liquidations)** | STRUCTURALLY BLOCKED | No admissible unauthenticated source passes all rubric items (unauth+no_keys+symbols>=5+blocks>=3+completeness_doc+license_ok+census_or_defensible). Active evidence-backed sweep completed with pass/fail tables. | `research_state/track_a_rubric_enforcement_matrix.md`, `research_state/track_a_final_block_proof.md`, `research_state/track_a_deadend_map.md` |
| **Track B (H003, modeled boundary breaches)** | CLOSED_NEGATIVE | No robust incremental skill after Holm across 16 cells; strict separation from Track A proven via grep-traced codepaths and explicit firewall statements. Results are synthetic/model-proxy only. | `research_state/track_b_codepath_separation_matrix.md`, `research_state/track_b_separation_proof_hardened.md`, `research_state/evaluation_summary_FCLR-H003-EXT-001.md` |
| **H002 (funding-extreme correction time)** | EXPLORATORY/PARTIAL | 88 events, 84 corrected, 4 censored. No concrete admissible confirmatory path evidenced. Must pre-register BEFORE outcome inspection if advanced to confirmatory; do not conflate with other tracks. | `research_state/h002_pre_registration.md`, `research_state/h002_replication_report.md` |

## Synthesis
Funding-conditioned volatility (C) first — closed negative in powered confirmatory with full traceability. Observed liquidations (A) blocked by data access firewall (machine-checkable). Modeled boundary breaches (B) closed negative with proven separation. H002 remains exploratory only with strict discipline.
