# AGENT HANDOFF — SINGLE DURABLE HANDOFF (PRIORITIZED BY REPO NAME)
UPDATED: 2026-10-31T21:02:44Z
HEAD: 72e1e864 (main). Working tree clean (untracked __pycache__ ignored).
REPO: Funding-conditioned-volatility-and-liquidation-risk
PRIORITY_SOURCE: Repository name inference ("Funding-conditioned-volatility-and-liquidation-risk") — FUNDING-CONDITIONED VOLATILITY FIRST
PRIORITY_ORDER: Track C (Funding-conditioned volatility forecasting, H001) > Track A (Observed liquidations, H004) > Track B (Modeled boundary breaches, H003) > H002 (Funding-extreme correction time, exploratory)
DURABLE_HANDOFF: SINGLE_SOURCE_OF_TRUTH
SESSION_GOAL: FORCED_HEAVY_EVIDENCE_CAMPAIGN — NO STATUS-ONLY PATH. EVERY ITERATION MUST PRODUCE MEASURABLE ARTIFACTS. REMOVE BOTTLENECKS SO SIGNIFICANT PROGRESS CONTINUES. MAKE FUTURE AGENTS UNABLE TO AVOID HEAVY WORK.
BOTTLE_NECK_REMOVAL: MANDATORY

HEAD_NOTE: HEAD verified at 72e1e864. This is the single durable source of truth; supersede all prior handoff copies.

## INITIAL TASK MESSAGE FOR THE NEXT AGENTIC WORK SESSION (COPY AND EXECUTE VERBATIM)

TASK_ID: HND-20261031-210244-FORCED_HEAVY_EVIDENCE_CAMPAIGN-V22
PRIORITY: P0
TIMESTAMP: 2026-10-31T21:02:44Z
MODE: FORCED HEAVY WORK — INFERRED FROM REPO NAME. BUILD THE NEXT FOCUS CAMPAIGN SO FUTURE AGENTS CANNOT AVOID HEAVY WORK.
REPO: Funding-conditioned-volatility-and-liquidation-risk
MANDATE: SINGLE DURABLE HANDOFF. Prioritize strictly by repo name: Track C → Track A → Track B → H002. Remove bottlenecks. Status-only work FORBIDDEN. Every action must yield concrete artifacts with provenance (file paths, line ranges, hashes/manifests, timestamps, HEAD). No re-tuning on sealed holdouts.

### STARTING DIRECTIVE (IMMEDIATE ACTIONS IN ORDER)
1. **VERIFY BASELINE**: Run `python -m unittest discover -s tests -v` — must be 27/27 PASS. Record HEAD (72e1e864), timestamp, and result in `research_state/AGENT_HANDOFF_OUTCOME.md` (create/update). Verify working tree clean.
2. **HARDEN TRACK C (PRIORITY 1)**: Track C is NOT_SUPPORTED/CONFIRMATORY CLOSED (FCLR-003 C2 vs B1 +0.015205, 95% CI [-0.020240,0.056734] crosses zero; worse in 2026). Risk overlay INELIGIBLE per RESEARCH_PROMPT §9. Update/harden `research_state/track_c_traceability_matrix.md` with byte-level decomposition (B0/B1/C1/C2), paired n, blocks, CIs, embargoes/normalization/leakage checks, and file:line links to artifacts. Prove no holdout reuse/tuning. Cross-link to `research_state/track_c_final_synthesis_dossier.md`.
3. **CONDUCT ACTIVE TRACK A SWEEP (PRIORITY 2)**: Track A is STRUCTURALLY BLOCKED. Do NOT just read old probes. Enumerate EVERY plausible admissible candidate (Binance public archives/APIs, public GitHub/Zenodo/HF, other venue-native unauthenticated). For EACH candidate, test against the verbatim rubric from `research_state/track_a_rubric_enforcement_matrix.md`: unauthenticated, >=5 symbols, >=3 non-overlapping 30-day blocks, documented completeness/census/defensible coverage, license/terms OK, actual historical depth (not live-only). Record concrete HTTP/auth/coverage/evidence with timestamps/HEAD. Update `research_state/track_a_rubric_enforcement_matrix.md` and `research_state/track_a_deadend_map.md` with pass/fail + rationale. If ANY candidate passes ALL items with evidence, pre-register per §16 BEFORE inspection; else irrefutably prove block with artifacts.
4. **HARDEN TRACK B SEPARATION (PRIORITY 3)**: Track B CLOSED_NEGATIVE with strict separation proven. Run `grep -rn "liquidat" .` (codebase) and trace every occurrence against Track A boundaries. Harden `research_state/track_b_codepath_separation_matrix.md` with file:line evidence proving no mixing of observed liquidation labels into modeled Track B paths. Update `research_state/track_b_separation_proof_hardened.md` if gaps found.
5. **HANDLE H002 CORRECTLY (PRIORITY 4)**: H002 exploratory/partial (88 events, 84 corrected, 4 censored). DO NOT promote to volatility/boundary/observed liquidation. If concrete confirmatory path exists per RESEARCH_PROMPT §16, create `research_state/h002_pre_registration.md` FIRST (frozen before outcome inspection). Otherwise rule out with evidence in `research_state/cross_track_decision_log.md`.
6. **CLOSE THE LOOP**: Create/update `research_state/AGENT_HANDOFF_OUTCOME.md`, `research_state/handoff_hardening_audit.md`, `research_state/cross_track_decision_log.md`. Ensure all artifacts cross-linked and this handoff remains single source of truth. Commit nothing merely for activity.

### CURRENT VERIFIED STATE (VERIFY AT START - DO NOT TRUST BLINDLY)
- Tests: `python -m unittest discover -s tests -v` → 27/27 PASS (must remain green)
- HEAD: `72e1e864` (main). Working tree clean.
- Track C (H001): NOT_SUPPORTED — CONFIRMATORY CLOSED. FCLR-003 C2 vs B1 +0.015205 QLIKE, 95% CI [-0.020240,0.056734] crosses zero (-3.78% worse). Risk overlay INELIGIBLE (§9). Synthesis: `research_state/track_c_final_synthesis_dossier.md`. DO NOT REOPEN without pre-registration + documented holdout discipline violations with evidence.
- Track A (H004): STRUCTURALLY BLOCKED. All enumerated candidates fail rubric. Only NEW admissible unauthenticated source per §16 with concrete evidence can reopen. Proof: `research_state/track_a_final_block_proof.md`, `research_state/track_a_rubric_enforcement_matrix.md`, `research_state/track_a_deadend_map.md`. **ACTIVE SWEEP REQUIRED.**
- Track B (H003): CLOSED_NEGATIVE. Separation from Track A proven. Proof: `research_state/track_b_separation_proof_hardened.md`, `research_state/track_b_definitive_separation_audit.md`, `research_state/track_b_codepath_separation_matrix.md`.
- H002: EXPLORATORY/PARTIAL (88/84/4). No promotion without new pre-registration per §16.

### HARD CONSTRAINTS (NEVER VIOLATE)
- No credentials/manual inputs/paid data. No `.github/workflows` changes without explicit maintainer auth. No trading/paper-trading/live orders.
- Strict track separation. Never conflate Track B (modeled) with Track A (observed).
- Preserve negatives/inconclusives. No fabricated data/labels. No zero-fill of missing values.
- Pre-registration REQUIRED for any new experiment. NO outcome inspection before pre-registration.
- No re-tuning on sealed holdouts. No threshold shopping. No re-running completed confirmatory experiments.
- Every iteration must create measurable research/data/testing/engineering progress. Status-only checks are FORBIDDEN.
- Evidence over assertion: every claim needs provenance/hashes/splits/tests/file:line/HEAD/timestamps.

### SUCCESS CRITERIA
- [ ] Tests 27/27 PASS, HEAD 72e1e864 recorded in `research_state/AGENT_HANDOFF_OUTCOME.md`
- [ ] Track C traceability hardened with irrefutable artifacts
- [ ] Track A: active evidence-backed sweep complete with rubric table + deadend map updated (irrefutable block or pre-registered reopen with evidence)
- [ ] Track B: codepath separation matrix hardened with grep evidence
- [ ] H002: pre-registered before inspection OR ruled out with evidence
- [ ] `research_state/AGENT_HANDOFF_OUTCOME.md`, `research_state/handoff_hardening_audit.md`, `research_state/cross_track_decision_log.md` updated and cross-linked
- [ ] Handoff remains single source of truth

FORCED HEAVY SYNTHESIS CAMPAIGN — PRIORITIZED BY REPO NAME (FUNDING-CONDITIONED VOLATILITY → LIQUIDATION RISK). NO SHORTCUTS. BUILD EVIDENCE, NOT STATUS. REMOVE BOTTLENECKS. MAKE IT IMPOSSIBLE TO AVOID HEAVY WORK.
