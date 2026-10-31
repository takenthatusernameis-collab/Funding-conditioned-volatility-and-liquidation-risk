# Cross-Track Decision Log — UPDATED

UPDATED: 2026-10-31T21:07:21Z
HEAD: e2f3f417f07ee62bcacefa2762effa2035ed0e55

## Decisions (by priority: C → A → B → H002)
| Track | Hypothesis | Status | Decision | Evidence |
|-------|-------------|--------|----------|----------|
| C (Funding-conditioned volatility) | FCLR-H001 | NOT_SUPPORTED — CONFIRMATORY CLOSED | No reopen without pre-registration + documented holdout discipline violations with concrete evidence. Risk overlay INELIGIBLE. | research_state/track_c_final_synthesis_dossier.md, research_state/evaluation_summary_FCLR003.md, research_state/track_c_traceability_matrix.md |
| A (Observed liquidations) | FCLR-H004 | STRUCTURALLY BLOCKED | Active sweep required. No candidate passes verbatim rubric (unauthenticated, no_keys, >=5 symbols, >=3 non-overlap 30d blocks, completeness_doc, license_ok, census_or_defensible). Sole reopen: new admissible unauthenticated source with concrete evidence + pre-registration before inspection. | research_state/track_a_final_block_proof.md, research_state/track_a_rubric_enforcement_matrix.md, research_state/track_a_deadend_map.md |
| B (Modeled boundary breaches) | FCLR-H003 | CLOSED_NEGATIVE | Strict separation from Track A proven via codepath grep; no robust incremental skill after Holm correction. | research_state/track_b_separation_proof_hardened.md, research_state/track_b_codepath_separation_matrix.md, research_state/evaluation_summary_FCLR-H003-EXT-001.md |
| H002 (Funding-extreme correction time) | FCLR-H002 | EXPLORATORY/PARTIAL (SEALED_PARTIAL) | 88 events, 84 corrected, 4 censored (Jan-Mar 2024). RV-regime contrast computed: high-RV median 16.0h vs low-RV 8.0h, log-rank p=0.0792 (direction matches paper, not significant). SSRN HTTP 403 blocks full methodology — cannot promote to exact replication/confirmatory/volatility-forecast-skill/liquidation evidence. No concrete confirmatory path exists per RESEARCH_PROMPT §16 without paper methodology; do NOT promote. Ruled out for promotion without new pre-registration + access to methodology. | research_state/h002_replication_report.md, research_state/hypothesis_registry.json, scripts/h002_download_2024_q1.py, tests/test_funding_correction_replication.py |

## H002 ruling
No pre-registration for promotion created because no admissible confirmatory path exists (methodology inaccessible). H002 remains exploratory/partial; must not be conflated with Track C/A/B. If SSRN becomes accessible, pre-register experiment BEFORE outcome inspection.
