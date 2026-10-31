# AGENT HANDOFF — SINGLE DURABLE HANDOFF (PRIORITIZED BY REPO NAME)
UPDATED: 2026-10-31T22:56:15Z
HEAD: c7646aff (main). Working tree clean (untracked __pycache__ ignored).
REPO: Funding-conditioned-volatility-and-liquidation-risk
PRIORITY_SOURCE: Repository name inference ("Funding-conditioned-volatility-and-liquidation-risk") — FUNDING-CONDITIONED VOLATILITY FIRST
PRIORITY_ORDER: Track C (Funding-conditioned volatility forecasting, H001) > Track A (Observed liquidations, H004) > Track B (Modeled boundary breaches, H003) > H002 (Funding-extreme correction time, exploratory)
DURABLE_HANDOFF: SINGLE_SOURCE_OF_TRUTH
SESSION_GOAL: FORCED_HEAVY_EVIDENCE_CAMPAIGN — NO STATUS-ONLY PATH. EVERY ITERATION MUST PRODUCE MEASURABLE ARTIFACTS. REMOVE BOTTLENECKS SO SIGNIFICANT PROGRESS CONTINUES. MAKE FUTURE AGENTS UNABLE TO AVOID HEAVY WORK.
BOTTLE_NECK_REMOVAL: MANDATORY

HEAD_NOTE: HEAD verified at c7646aff. This is the single durable source of truth; supersede all prior handoff copies.

## INITIAL TASK MESSAGE FOR THE NEXT AGENTIC WORK SESSION (COPY AND EXECUTE VERBATIM)

TASK_ID: HND-20261031-225615-FORCED_HEAVY_EVIDENCE_CAMPAIGN-V24
PRIORITY: P0
TIMESTAMP: 2026-10-31T22:56:15Z
MODE: FORCED HEAVY WORK — INFERRED FROM REPO NAME. BUILD THE NEXT FOCUS CAMPAIGN SO FUTURE AGENTS CANNOT AVOID HEAVY WORK.
REPO: Funding-conditioned-volatility-and-liquidation-risk
MANDATE: SINGLE DURABLE HANDOFF. Prioritize strictly by repo name: Track C → Track A → Track B → H002. Remove bottlenecks. Status-only work FORBIDDEN. Every action must yield concrete artifacts with provenance (file paths, line ranges, hashes/manifests, timestamps, HEAD). No re-tuning on sealed holdouts. Heavy evidence campaign is substantively complete; the remaining required work is an independent recomputation audit of the Track C headline result plus final campaign seal.

### STARTING DIRECTIVE (IMMEDIATE ACTIONS IN ORDER)
1. **VERIFY BASELINE**: Run `python -m unittest discover -s tests -v` — must be 27/27 PASS. Record HEAD (c7646aff), timestamp, and result in `research_state/AGENT_HANDOFF_OUTCOME.md` (create/update). Verify working tree clean.
2. **INDEPENDENT RECOMPUTATION AUDIT — TRACK C HEADLINE (PRIORITY 1, REPO-NAME FORCED)**: Track C (H001/FCLR-003) is NOT_SUPPORTED/CONFIRMATORY CLOSED; risk overlay INELIGIBLE per RESEARCH_PROMPT §9. Before any future agent builds on or cites this result, independently recompute the headline C2 vs B1 ΔQLIKE = +0.015205 (worse), 95% CI [-0.020240, 0.056734] crosses zero, paired n=10796, 3 non-overlapping 30-day blocks, instruments BTC/ETH/BNB/SOL/XRP, window 2024-10-02..2024-12-31, from stored inputs/data hashes/config in `research_state/run_manifest.json` and `research_state/evaluation_summary_FCLR003.md`. Confirm byte-identical reproduction within declared numerical tolerance. Write `research_state/independent_recompute_audit_FCLR003.md` with exact commands, input hashes, recomputed values, match/mismatch vs recorded values, timestamp, HEAD. Cross-link to `research_state/track_c_traceability_matrix.md` and `research_state/track_c_final_synthesis_dossier.md`. Prove no holdout reuse/tuning.
3. **SEAL THE CAMPAIGN**: Create/update `research_state/AGENT_HANDOFF_OUTCOME.md`, `research_state/handoff_hardening_audit.md`, `research_state/cross_track_decision_log.md`. Record final per-track verdicts: C = NOT_SUPPORTED/CLOSED (overlay INELIGIBLE); A = STRUCTURALLY BLOCKED (no rubric-passing candidate; reopen only via new admissible unauthenticated source + pre-registration before inspection); B = CLOSED_NEGATIVE (codepath separation irrefutable); H002 = EXPLORATORY/PARTIAL (88/84/4), no promotion without pre-registration per §16. Ensure all artifacts cross-linked; this handoff remains single source of truth. Commit nothing merely for activity.
4. **CONFIRM NO BOTTLENOCKS**: All tracks resolved/blocked with evidence; no session is left waiting on an external decision. If a genuinely new admissible unauthenticated liquidation source appears (Track A rubric), pre-register per §16 BEFORE inspection — otherwise do not reopen.

### CURRENT VERIFIED STATE (VERIFY AT START - DO NOT TRUST BLINDLY)
- Tests: `python -m unittest discover -s tests -v` → 27/27 PASS (must remain green)
- HEAD: `c7646aff` (main). Working tree clean except untracked `__pycache__/`.
- Track C (H001): NOT_SUPPORTED — CONFIRMATORY CLOSED. FCLR-003 C2 vs B1 +0.015205 QLIKE, 95% CI [-0.020240,0.056734] crosses zero (-3.78% worse). Risk overlay INELIGIBLE (§9). Traceability hardened: `research_state/track_c_traceability_matrix.md`. Synthesis: `research_state/track_c_final_synthesis_dossier.md`. DO NOT REOPEN without pre-registration + documented holdout discipline violations with evidence.
- Track A (H004): STRUCTURALLY BLOCKED. Active sweep complete; no candidate passes verbatim rubric (unauthenticated, no_keys, >=5 symbols, >=3 non-overlapping 30-day blocks, completeness/census/defensible coverage, license/terms OK). Proof: `research_state/track_a_final_block_proof.md`, `research_state/track_a_rubric_enforcement_matrix.md`, `research_state/track_a_deadend_map.md`.
- Track B (H003): CLOSED_NEGATIVE. Strict separation from Track A proven via `grep -rn "liquidat" .` codepath trace; no observed-liquidation labels mixed into modeled Track B paths. Proof: `research_state/track_b_codepath_separation_matrix.md`, `research_state/track_b_separation_proof_hardened.md`, `research_state/track_b_definitive_separation_audit.md`.
- H002: EXPLORATORY/PARTIAL (88 events, 84 corrected, 4 censored). High-RV median 16.0h vs low-RV 8.0h, log-rank p=0.0792 (direction matches paper, not significant). SSRN methodology inaccessible (HTTP 403) — cannot promote to exact replication/confirmatory/volatility-skill/liquidation evidence. No promotion without pre-registration per §16.

### HARD CONSTRAINTS (NEVER VIOLATE)
- No credentials/manual inputs/paid data. No `.github/workflows` changes without explicit maintainer auth. No trading/paper-trading/live orders.
- Strict track separation. Never conflate Track B (modeled) with Track A (observed).
- Preserve negatives/inconclusives. No fabricated data/labels. No zero-fill of missing values.
- Pre-registration REQUIRED for any new experiment. NO outcome inspection before pre-registration.
- No re-tuning on sealed holdouts. No threshold shopping. No re-running completed confirmatory experiments.
- Every iteration must create measurable research/data/testing/engineering progress. Status-only checks are FORBIDDEN.
- Evidence over assertion: every claim needs provenance/hashes/splits/tests/file:line/HEAD/timestamps.

### SUCCESS CRITERIA
- [ ] Tests 27/27 PASS, HEAD c7646aff recorded in `research_state/AGENT_HANDOFF_OUTCOME.md`
- [ ] Independent recomputation audit of FCLR-003 headline (C2 vs B1 ΔQLIKE +0.015205, CI [-0.020240, 0.056734]) written to `research_state/independent_recompute_audit_FCLR003.md` with input hashes, commands, match/mismatch, tolerance
- [ ] Track C traceability confirmed irrefutable; sealed NOT_SUPPORTED, overlay INELIGIBLE
- [ ] Track A: active sweep evidence-backed, block irrefutable, rubric + deadend map current
- [ ] Track B: codepath separation matrix current with grep evidence
- [ ] H002: correctly classified exploratory/partial, no speculative pre-registration
- [ ] `research_state/AGENT_HANDOFF_OUTCOME.md`, `research_state/handoff_hardening_audit.md`, `research_state/cross_track_decision_log.md` updated and cross-linked
- [ ] Handoff remains single source of truth; no bottlenecks blocking the next session

FORCED HEAVY SYNTHESIS CAMPAIGN — PRIORITIZED BY REPO NAME (FUNDING-CONDITIONED VOLATILITY → LIQUIDATION RISK). NO SHORTCUTS. BUILD EVIDENCE, NOT STATUS. REMOVE BOTTLENECKS. MAKE IT IMPOSSIBLE TO AVOID HEAVY WORK.
