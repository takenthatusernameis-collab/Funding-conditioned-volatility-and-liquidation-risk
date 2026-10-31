# AGENT HANDOFF — SINGLE DURABLE HANDOFF (PRIORITIZED BY REPO NAME)

UPDATED: 2026-10-31T07:19:00Z
HEAD: 7a3410a0
REPO: Funding-conditioned-volatility-and-liquidation-risk
PRIORITY_SOURCE: Repository name inference (funding-conditioned volatility and liquidation risk)
PRIORITY_ORDER: Track C (funding-conditioned volatility forecasting) > Track A (observed liquidations) > Track B (modeled boundary breaches)
DURABLE_HANDOFF: SINGLE_SOURCE_OF_TRUTH
SESSION_GOAL: HEAVY_EVIDENCE_CAMPAIGN — NO SHORTCUTS. FORCE AUDITABLE HEAVY WORK. MAXIMIZE DEFENSIBLE EVIDENCE.
BOTTLE_NECK_REMOVAL: MANDATORY — Remove any structural/efficiency blockers so significant progress continues. No status-only work.

## INITIAL TASK MESSAGE FOR THE NEXT AGENTIC WORK SESSION (COPY AND EXECUTE THIS VERBATIM)

**TASK_ID:** `HND-20261031-071900-HEAVY-FORCED-CAMPAIGN`
**PRIORITY:** P0
**TIMESTAMP:** 2026-10-31T07:19:00Z
**MODE:** FORCED HEAVY CAMPAIGN — EXPLICIT DIRECTIONS ABSENT, BUILD NEXT FOCUS CAMPAIGN SO FUTURE AGENTS CANNOT AVOID HEAVY WORK
**REPO:** Funding-conditioned-volatility-and-liquidation-risk
**MANDATE:** Leave the most relevant inferred timestamped clear initial task message for the next agentic work session in the single durable handoff. If multiple sessions blocked or inefficient, remove bottlenecks so significant progress continues. If explicit directions absent, build next focus campaign so future agents cannot avoid doing heavy work. Prioritize strictly by repo name.

You are continuing from this SINGLE DURABLE handoff. **Prioritize strictly by repo name: Track C (funding-conditioned volatility forecasting) FIRST, then Track A (observed liquidations), then Track B (modeled boundary breaches).**

### CURRENT KNOWN STATE (DO NOT TRUST BLINDLY - VERIFY)
- Tests: `python -m unittest discover -s tests -v` → **19/19 PASS** (verified 2026-10-31T07:19:00Z). Must stay green.
- HEAD: 7a3410a0 (main). Working tree clean except untracked `scripts/__pycache__/`, `tests/__pycache__/`.
- Track C (H001): NOT_SUPPORTED (SEALED_NEGATIVE). All confirmatory panels negative:
  - FCLR-003 (powered, 2024-10-02..2024-12-31, 3 blocks, n=10796): C2 vs B1 +0.015205 QLIKE, CI [-0.020240, 0.056734] crosses zero, -3.78% rel → gate NOT_MET → COMPLETE_NEGATIVE.
  - FCLR-006 (unsealed 2026-05-23..2026-08-06, 2 blocks <3, n=8987): C2 vs B1 +0.368588 QLIKE, CI entirely positive → WORSE, -69.90% rel → gate NOT_MET → COMPLETE_NEGATIVE.
  - FCLR-007 (unsealed 2026-07-21..2026-07-31, 0 blocks <3, n=1195): C2 vs B1 +0.010258 QLIKE, CI [0.001308, 0.019737] entirely positive → WORSE, -3.42% rel → gate NOT_MET → COMPLETE_NEGATIVE.
  - Risk overlay INELIGIBLE. No reopen path without violating pre-registration/holdout discipline.
- Track A (H004): BLOCKED/EXPLORATORY (STRUCTURALLY BLOCKED). No admissible unauthenticated observed-liquidation census with ≥5 symbols, ≥3 non-overlapping 30-day blocks, documented completeness, license OK. Sole reopen path: NEW admissible unauthenticated source per RESEARCH_PROMPT.md §16. FCLR-005 was exploratory-only on exhausted 2026-07-08..2026-08-06 window (0 blocks, no incremental skill).
- Track B (H003): COMPLETE_NEGATIVE (SEALED_NEGATIVE). 16 cells, Holm correction, no robust incremental skill. Strict separation from Track A proven (track_b_definitive_separation_audit.md).
- Forecast gate NOT_MET on every tested panel. Confirmatory program CLOSED. Heavy evidence work (forensic/synthesis/audit/source-discovery/hardening) is mandatory and unavoidable.

### BOTTLENECK REMOVAL MANDATE
If sessions are blocked/inefficient, REMOVE bottlenecks so significant progress continues:
1. **Data access bottlenecks**: Exhaust ALL admissible unauthenticated sources for Track A with machine-checkable GO/NO-GO. If no source qualifies, produce irrefutable dead-end evidence (URLs, HTTP codes, timestamps, coverage math, curl/probe attempts) and move to next materially different route - do NOT loop retries.
2. **Compute/analysis bottlenecks**: Leverage cached data in `research_state/data_cache/` and repo zips. Build restartable, incremental analyses. Avoid recomputing sealed results.
3. **Evidence bottlenecks**: Every claim needs provenance, hashes/splits, tests. Strengthen artifacts with concrete numbers.
4. **Handoff bottlenecks**: Keep this file as single source of truth. Make it impossible for next agent to do status-only work. If you are blocked, REMOVE the bottleneck or produce irrefutable evidence of why it cannot be removed. Do NOT report "blocked" without concrete evidence and attempted removals.

### MANDATORY HEAVY EVIDENCE CAMPAIGN (EXECUTE ALL - CANNOT SKIP)

**STEP 1: INTEGRITY CHECK (P0, ~2-5 min)**
1. `python -m unittest discover -s tests -v` → **MUST PASS ALL TESTS** (currently 19 tests). Verify and record timestamp.
2. Verify key artifacts exist and are cross-linked: `research_state/hypothesis_registry.json`, `research_state/experiment_frontier.json`, `research_state/track_c_consolidated_dossier.md`, `research_state/track_a_deadend_map.md`, `research_state/track_b_definitive_separation_audit.md`, `research_state/cross_track_decision_log.md`, `research_state/cross_track_decision_firewall.md`, `research_state/handoff_hardening_audit.md`, `research_state/negative_results_report.md`, `research_state/next_data_discovery_plan.md`, `research_state/final_confirmatory_verdict.md`, `research_state/structural_closure_verdict_heavy.md`.
3. Confirm constraints: no workflow changes, no trading logic, strict track separation, preserve negatives. Log integrity check in `research_state/AGENT_HANDOFF_OUTCOME.md`.

**STEP 2: FORCED HEAVY WORK (P0, PRIORITIZE BY REPO NAME)**

#### A. TRACK C - FUNDING-CONDITIONED VOLATILITY (FIRST - HIGHEST PRIORITY)
**Goal:** Squeeze every defensible ounce of evidence from existing cached data. Even though closed negative, do a deeper forensic re-analysis and meta-synthesis.

1. **Deep forensic audit** (HEAVY): Re-examine FCLR-003/006/007 with fresh eyes. For each, document: exact splits, embargoes, block structure, paired coverage, QLIKE decomposition, CI construction, feature availability, leakage checks. Update `research_state/track_c_consolidated_dossier.md` with a new "FORENSIC_REAUDIT_20261031" section with numbers.
2. **Alternative feature ablations** (HEAVY): Using cached data, test pre-registered but unexecuted ablations from protocols (e.g. different funding normalization windows, interaction terms, lag structures) - ONLY if they don't touch sealed holdouts. If any ablation would require reusing sealed holdouts, BLOCK and document with evidence.
3. **Robustness stress tests** (HEAVY): Time-varying effects, regime splits (volatility regimes), symbol concentration, look-ahead in features. Document all results (including nulls) with tables/numbers. Update `research_state/evaluation_summary.md` and `research_state/negative_results_report.md`.
4. **Meta-synthesis** (HEAVY): Write a tight synthesis tying funding/volatility/liquidation channels together. Be brutally honest about incremental value. Negative results are defensible evidence - make them unassailable.

#### B. TRACK A - OBSERVED LIQUIDATIONS (SECOND - REMOVE BOTTLENECKS)
**Goal:** Find ANY admissible unauthenticated source or prove beyond doubt it's impossible.

1. **Aggressive source sweep** (HEAVY): Probe all candidates in `research_state/liquidation_sources_enumeration.md` again with fresh checks. Check Binance public data repo paths, Bybit/OKX/Deribit public historical data, GitHub repos, HuggingFace datasets, Zenodo, academic archives. Try materially different routes; do not loop same probe.
2. **Machine-checkable firewall** (HEAVY): Harden `research_state/track_a_deadend_map.md` with executable-style rubric: `unauthenticated == true AND no_keys == true AND symbols>=5 AND blocks>=3 AND completeness_doc == true AND license_ok == true`. For EVERY probed source, fill all fields with evidence (URLs, HTTP codes, timestamps, coverage math, sizes, attempt logs).
3. **Bottleneck identification & removal** (HEAVY): If bottleneck is "need 2024" but only 2026 exists, test 2026 more rigorously under pre-registration. If bottleneck is format/ingestion, write robust parsers for found data. If truly no data exists, make dead-end UNFORGEABLE with irrefutable artifacts.
4. **Pre-register if GO** (HEAVY): If ANY source passes rubric, FREEZE protocol BEFORE examining outcomes, create pre-reg, then test. Never peek first. Document GO/NO-GO decision with evidence.

#### C. TRACK B - MODELED BREACHES (THIRD)
**Goal:** Strengthen separation evidence. Prove cross-contamination impossible.

1. **Separation audit** (HEAVY): Trace code paths - ensure Track B never uses Track A labels. Document concrete file paths/line references in `research_state/track_b_definitive_separation_audit.md`.
2. **Sensitivity analysis** (HEAVY): Vary margin assumptions, liquidation price models, funding assumptions. Document if any gives signal with numbers/tables, but NEVER conflate with observed liquidations.
3. **Firewall reinforcement** (HEAVY): Update `research_state/cross_track_decision_firewall.md` with explicit guards and verification checks.

**STEP 3: DOCUMENTATION & HARDENING (P0)**
1. Create/update `research_state/AGENT_HANDOFF_OUTCOME.md` with timestamp, HEAD (7a3410a0), detailed evidence summary of ALL heavy work done (artifacts modified/created, commands run, numbers).
2. Update `research_state/handoff_hardening_audit.md` proving bottlenecks removed and next agent CANNOT avoid heavy work (specific blockers identified+removed or irrefutable dead-ends).
3. Update `research_state/cross_track_decision_log.md` with new findings.
4. Ensure all artifacts cross-linked.
5. Run tests again: `python -m unittest discover -s tests -v` → MUST PASS. Record final test result with timestamp.

### HARD CONSTRAINTS (NEVER VIOLATE)
- No credentials/manual inputs/paid data. No `.github/workflows` changes without explicit maintainer auth. No trading/paper-trading/live orders.
- Strict track separation. Never conflate modeled breaches (B) with observed liquidations (A).
- Preserve negatives/inconclusives. No fabricated data/labels. No zero-fill of missing values.
- Pre-registration REQUIRED for any new experiment. NO outcome inspection before pre-registration.
- No re-tuning on sealed holdouts. No threshold shopping.
- Every iteration must create measurable research/data/testing/engineering progress. Status-only checks are FORBIDDEN.

### SUCCESS CRITERIA
- [ ] All tests pass (record timestamp/HEAD)
- [ ] Track C: Forensic re-audit complete with concrete tables/numbers in consolidated dossier (FORENSIC_REAUDIT_20261031)
- [ ] Track A: Machine-checkable firewall applied to ALL candidates in enumeration; dead-end evidence irrefutable OR GO experiment pre-registered and executed per rules with frozen protocol
- [ ] Track B: Separation proven with concrete code-path evidence (file paths/lines)
- [ ] Bottlenecks identified and removed (documented with evidence) - no unsubstantiated "blocked"
- [ ] `research_state/AGENT_HANDOFF_OUTCOME.md` created/updated with full evidence (artifacts, commands, numbers)
- [ ] `research_state/handoff_hardening_audit.md` proves heavy work unavoidable
- [ ] `research_state/cross_track_decision_log.md` updated
- [ ] This handoff remains single source of truth

**FORCED HEAVY CAMPAIGN. NO SHORTCUTS. BUILD EVIDENCE, NOT STATUS.**
