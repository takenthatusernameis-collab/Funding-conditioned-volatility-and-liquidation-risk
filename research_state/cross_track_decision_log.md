# CROSS-TRACK DECISION LOG (PRIORITIZED BY REPO NAME: C → A → B → H002)

UPDATED: 2026-10-31T17:18:44Z
HEAD: 12b0bb93

## Priority order (enforced)
1. Track C (funding-conditioned volatility) - repo name priority
2. Track A (observed liquidations)
3. Track B (modeled boundary breaches)
4. H002 (funding-extreme correction time)

## Decisions

### Track C (H001) - P1
- **Status:** NOT_SUPPORTED — CONFIRMATORY CLOSED
- **Evidence:** FCLR-003 C2 vs B1 ΔQLIKE +0.015205, 95% CI [-0.020240,0.056734] crosses zero (-3.78% worse). C1 (+funding only) shows improvement; adding price-dislocation features degrades below RV-only. FCLR-006/FCLR-007 worse/underpowered.
- **Gate:** Risk overlay INELIGIBLE per RESEARCH_PROMPT §9.
- **Traceability:** research_state/track_c_traceability_matrix.md (full decomposition), research_state/track_c_final_synthesis_dossier.md, research_state/evaluation_summary_FCLR003.md, research_state/leakage_audit.md
- **Decision:** CLOSED. No reopen without pre-registration + documented holdout discipline violations with concrete evidence.

### Track A (H004) - P2
- **Status:** STRUCTURALLY BLOCKED
- **Rubric (verbatim):** unauthenticated==true AND no_keys==true AND symbols>=5 AND blocks>=3 AND completeness_doc==true AND license_ok==true AND census_or_defensible==true
- **Sweep:** ALL enumerated candidates tested with concrete evidence (auth/HTTP/coverage/census/docs/license). None pass ALL items. Binance probed (no admissible unauth liquidation census), public REST live-only/no history, GitHub/Zenodo/HF insufficient coverage/completeness, FCLR-005 pilot exhausted single window.
- **Evidence:** research_state/track_a_rubric_enforcement_matrix.md, research_state/track_a_final_block_proof.md, research_state/track_a_deadend_map.md, research_state/binance_source_probe.md, research_state/liquidation_sources_enumeration.md, research_state/evaluation_summary_FCLR005.md
- **Decision:** BLOCKED. Sole reopen requires NEW admissible unauthenticated source meeting ALL rubric items with concrete evidence AND pre-registration BEFORE outcome inspection per RESEARCH_PROMPT §16.

### Track B (H003) - P3
- **Status:** CLOSED_NEGATIVE
- **Evidence:** FCLR-H003-EXT-001 no robust incremental skill after Holm correction across 16 cells. Strict separation from Track A proven; no mixing detected via codepath grep.
- **Evidence:** research_state/track_b_codepath_separation_matrix.md, research_state/track_b_separation_proof_hardened.md, research_state/track_b_definitive_separation_audit.md, research_state/evaluation_summary_FCLR-H003-EXT-001.md
- **Decision:** CLOSED_NEGATIVE. Separation enforced and locked.

### H002 (funding-extreme correction time) - P4
- **Status:** EXPLORATORY/PARTIAL
- **Evidence:** 88 events, 84 corrected, 4 censored (recorded). Pre-registered in research_state/h002_pre_registration.md BEFORE outcome inspection.
- **Constraints:** Do NOT promote to volatility skill/boundary breaches/observed liquidations. No concrete admissible path to confirmatory under current constraints; any confirmatory work requires new pre-registration per RESEARCH_PROMPT §16.
- **Decision:** Remain exploratory/partial. No automatic promotion.

## Integration notes
- All decisions prioritize repo name (funding-conditioned volatility first). Bottlenecks removed with heavy evidence. Tests remain 27/27 PASS at HEAD 12b0bb93.
