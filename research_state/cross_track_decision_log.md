# Cross-Track Decision Log — UPDATED

UPDATED: 2026-10-31T21:07:21Z
HEAD: 4000f272

## Decisions (by priority: C → A → B → H002)
| Track | Hypothesis | Status | Decision | Evidence |
|-------|-------------|--------|----------|----------|
| C (Funding-conditioned volatility) | FCLR-H001 | NOT_SUPPORTED — CONFIRMATORY CLOSED | No reopen without pre-registration + documented holdout discipline violations with concrete evidence. Risk overlay INELIGIBLE. | research_state/track_c_final_synthesis_dossier.md, research_state/evaluation_summary_FCLR003.md, research_state/track_c_traceability_matrix.md |
| A (Observed liquidations) | FCLR-H004 | STRUCTURALLY BLOCKED | Active sweep required. No candidate passes verbatim rubric (unauthenticated, no_keys, >=5 symbols, >=3 non-overlap 30d blocks, completeness_doc, license_ok, census_or_defensible). Sole reopen: new admissible unauthenticated source with concrete evidence + pre-registration before inspection. | research_state/track_a_final_block_proof.md, research_state/track_a_rubric_enforcement_matrix.md, research_state/track_a_deadend_map.md |
| B (Modeled boundary breaches) | FCLR-H003 | CLOSED_NEGATIVE | Strict separation from Track A proven via codepath grep; no robust incremental skill after Holm correction. | research_state/track_b_separation_proof_hardened.md, research_state/track_b_codepath_separation_matrix.md, research_state/evaluation_summary_FCLR-H003-EXT-001.md |
| H002 (Funding-extreme correction time) | FCLR-H002 | EXPLORATORY/PARTIAL (SEALED_PARTIAL) | 88 events, 84 corrected, 4 censored (Jan-Mar 2024). RV-regime contrast computed: high-RV median 16.0h vs low-RV 8.0h, log-rank p=0.0792 (direction matches paper, not significant). SSRN HTTP 403 blocks full methodology — cannot promote to exact replication/confirmatory/volatility-forecast-skill/liquidation evidence. No concrete confirmatory path exists per RESEARCH_PROMPT §16 without paper methodology; do NOT promote. Ruled out for promotion without new pre-registration + access to methodology. | research_state/h002_replication_report.md, research_state/hypothesis_registry.json, scripts/h002_download_2024_q1.py, tests/test_funding_correction_replication.py |

## H002 ruling
No pre-registration for promotion created because no admissible confirmatory path exists (methodology inaccessible). H002 remains exploratory/partial; must not be conflated with Track C/A/B. If SSRN becomes accessible, pre-register experiment BEFORE outcome inspection.


## SESSION_UPDATE_20261031T215333Z (THIS SESSION)
- Baseline verified: 27/27 tests PASS, HEAD 4000f272.
- Track C traceability hardened; remains NOT_SUPPORTED/CLOSED.
- Track A active sweep completed: no rubric-passing candidate found; block irrefutable.
- Track B separation hardened (grep evidence reviewed); remains CLOSED_NEGATIVE.
- H002: no concrete admissible confirmatory path; remains EXPLORATORY/PARTIAL, no promotion without pre-registration.
- All artifacts cross-linked per handoff.

## UPDATE 2026-10-31T22:04:30Z (HARDENING)
- Track C: NOT_SUPPORTED — CONFIRMATORY CLOSED. Traceability hardened (byte-level B0/B1/C1/C2, paired n/blocks/CIs, embargoes/leakage). Risk overlay INELIGIBLE (§9). No reopen without pre-registration + documented holdout discipline violations with evidence.
- Track A: STRUCTURALLY BLOCKED. Active sweep completed against verbatim rubric — no admissible unauthenticated candidate meets ALL items (>=5 symbols, >=3 non-overlapping 30d blocks, completeness/census/defensible, license/terms OK). New source requires pre-registration before inspection.
- Track B: CLOSED_NEGATIVE. Codepath separation hardened via grep (no mixing of observed liquidation labels into modeled Track B paths). Strict separation proven.
- H002: EXPLORATORY/PARTIAL (88/84/4). No promotion to volatility/boundary/observed liquidation without pre-registration per §16. If confirmatory path exists, pre-register FIRST.
