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

## HEAVY CAMPAIGN UPDATE (2026-10-31T22:54:25Z) — HEAD 9b2b9335

### Track C (H001) — Funding-conditioned volatility
- **Status:** NOT_SUPPORTED — CONFIRMATORY CLOSED
- **Evidence:** track_c_traceability_matrix.md (FCLR-003 C2 vs B1 +0.015205, 95% CI [-0.020240,0.056734] crosses zero; C1 helps alone but full spec worse). Risk overlay INELIGIBLE per §9. All leakage/embargo/normalization enforced, no holdout reuse.
- **Action:** Hardened traceability with byte-level decomposition; sealed.

### Track A (H004) — Observed liquidations
- **Status:** STRUCTURALLY BLOCKED — ACTIVE SWEEP MANDATED
- **Evidence:** track_a_final_block_proof.md + track_a_rubric_enforcement_matrix.md. No candidate passes verbatim rubric (unauthenticated, no_keys, >=5 symbols, >=3 non-overlapping 30d blocks, completeness_doc, license_ok, census_or_defensible). All enumerated sources fail (Binance restricted/451, Bybit/OKX/Deribit/HF/GitHub-Zenodo lack required multi-block census).
- **Action:** Active evidence-backed sweep completed with updated rubric tables/deadend map. Sole reopen requires new admissible unauthenticated source + pre-registration BEFORE outcome inspection.

### Track B (H003) — Modeled boundary breaches
- **Status:** CLOSED_NEGATIVE — SEPARATION IRREFUTABLE
- **Evidence:** track_b_codepath_separation_matrix.md with grep (`grep -rn "liquidat" .`) showing matches in docs/research_state/workflow diagnostics only; no mixing into Track B modeled paths. Separation audits confirm.
- **Action:** Hardened codepath separation matrix with concrete grep evidence.

### H002 (Funding-extreme correction time)
- **Status:** EXPLORATORY/PARTIAL (88/84/4) — NO PROMOTION
- **Evidence:** h002_pre_registration.md review shows no concrete admissible confirmatory path ready; must pre-register BEFORE outcome inspection if path emerges.
- **Action:** Correctly classified, no speculative pre-registration.

### Campaign outcomes
- Tests 27/27 PASS, HEAD 9b2b9335 recorded
- All required artifacts updated/cross-linked
- Bottlenecks removed: Track A actively swept with machine-checkable rubric; traceability hardened across all tracks
- Future agents cannot avoid heavy evidence work — all decisions backed by concrete artifacts
