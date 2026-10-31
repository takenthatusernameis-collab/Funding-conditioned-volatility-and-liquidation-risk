# AGENT HANDOFF — SINGLE DURABLE HANDOFF (PRIORITIZED BY REPO NAME)

UPDATED: 2026-10-31T06:07:36Z
HEAD: 2327c91c9e965886e4f64da0ce678220ba40d2c8
REPO: Funding-conditioned-volatility-and-liquidation-risk
PRIORITY_SOURCE: Repository name inference (funding-conditioned volatility and liquidation risk)
PRIORITY_ORDER: Track C (funding-conditioned volatility forecasting) > Track A (observed liquidations) > Track B (modeled boundary breaches)
DURABLE_HANDOFF: SINGLE_SOURCE_OF_TRUTH
SESSION_GOAL: HEAVY_EVIDENCE_CAMPAIGN — NO SHORTCUTS. FORCE AUDITABLE HEAVY WORK. MAXIMIZE DEFENSIBLE EVIDENCE.

## INITIAL TASK MESSAGE FOR THE NEXT AGENTIC WORK SESSION (COPY AND EXECUTE THIS VERBATIM)

**TASK_ID:** `HND-20261031-060736-HEAVY-FORCED`
**PRIORITY:** P0
**TIMESTAMP:** 2026-10-31T06:07:36Z
**MODE:** FORCED HEAVY CAMPAIGN — EXPLICIT DIRECTIONS ABSENT, BUILD NEXT FOCUS CAMPAIGN SO FUTURE AGENTS CANNOT AVOID HEAVY WORK
**REPO:** Funding-conditioned-volatility-and-liquidation-risk

You are continuing from this SINGLE DURABLE handoff. **Prioritize strictly by repo name: Track C (funding-conditioned volatility forecasting) FIRST, then Track A (observed liquidations), then Track B (modeled boundary breaches).**

### CURRENT KNOWN STATE (DO NOT TRUST BLINDLY - VERIFY)
- Track C (H001): NOT_SUPPORTED across FCLR-003/006/007. All confirmatory panels negative; forecast gate NOT_MET. Risk overlay INELIGIBLE. See `research_state/track_c_consolidated_dossier.md`, `research_state/hypothesis_registry.json`.
- Track A (H004): BLOCKED/EXPLORATORY. No admissible unauthenticated 2024 liquidation census found; only small exploratory 2026 window (FCLR-005). See `research_state/track_a_deadend_map.md`, `research_state/liquidation_source_campaign.md`, `research_state/next_data_discovery_plan.md`.
- Track B (H003): COMPLETE_NEGATIVE after Holm correction across 16 cells. Strictly separated from observed liquidations. See `research_state/track_b_definitive_separation_audit.md`.

### BOTTLENECK REMOVAL MANDATE
If sessions are blocked/inefficient, REMOVE bottlenecks so significant progress continues:
1. **Data access bottlenecks**: Exhaust ALL admissible unauthenticated sources for Track A with machine-checkable GO/NO-GO. If no source qualifies, produce irrefutable dead-end evidence (URLs, HTTP codes, timestamps, coverage math) and move to next materially different route - do NOT loop retries.
2. **Compute/analysis bottlenecks**: Leverage cached data in `research_state/data_cache/` and repo zips. Build restartable, incremental analyses. Avoid recomputing sealed results.
3. **Evidence bottlenecks**: Every claim needs provenance, hashes/splits, tests. Strengthen artifacts with concrete numbers.
4. **Handoff bottlenecks**: Keep this file as single source of truth. Make it impossible for next agent to do status-only work.

### MANDATORY HEAVY EVIDENCE CAMPAIGN (EXECUTE ALL - CANNOT SKIP)

**STEP 1: INTEGRITY CHECK (P0, ~2-5 min)**
1. `python -m unittest discover -s tests -v` → **MUST PASS ALL TESTS**
2. Verify key artifacts exist and are cross-linked: `research_state/hypothesis_registry.json`, `research_state/experiment_frontier.json`, `research_state/track_c_consolidated_dossier.md`, `research_state/track_a_deadend_map.md`, `research_state/track_b_definitive_separation_audit.md`, `research_state/cross_track_decision_log.md`, `research_state/cross_track_decision_firewall.md`, `research_state/handoff_hardening_audit.md`, `research_state/negative_results_report.md`, `research_state/next_data_discovery_plan.md`
3. Confirm constraints: no workflow changes, no trading logic, strict track separation, preserve negatives.

**STEP 2: FORCED HEAVY WORK (P0, PRIORITIZE BY REPO NAME)**

#### A. TRACK C - FUNDING-CONDITIONED VOLATILITY (FIRST - HIGHEST PRIORITY)
**Goal:** Squeeze every defensible ounce of evidence from existing cached data. Even if closed negative, do a deeper forensic re-analysis.

1. **Deep forensic audit** (HEAVY): Re-examine FCLR-003/006/007 with fresh eyes. For each, document: exact splits, embargoes, block structure, paired coverage, QLIKE decomposition, CI construction, feature availability, leakage checks. Update `research_state/track_c_consolidated_dossier.md` with a new "FORENSIC_REAUDIT_20261031" section with numbers.
2. **Alternative feature ablations** (HEAVY): Using cached data, test pre-registered but unexecuted ablations from protocols (e.g. different funding normalization windows, interaction terms, lag structures) - ONLY if they don't touch sealed holdouts. If any ablation would require reusing sealed holdouts, BLOCK and document.
3. **Robustness stress tests** (HEAVY): Time-varying effects, regime splits (volatility regimes), symbol concentration, look-ahead in features. Document all results (including nulls). Update `research_state/evaluation_summary.md` and `research_state/negative_results_report.md`.
4. **Meta-synthesis** (HEAVY): Write a tight synthesis tying funding/volatility/liquidation channels together. Be brutally honest about incremental value.

#### B. TRACK A - OBSERVED LIQUIDATIONS (SECOND - REMOVE BOTTLENECKS)
**Goal:** Find ANY admissible unauthenticated source or prove beyond doubt it's impossible.

1. **Aggressive source sweep** (HEAVY): Probe all candidates in `research_state/liquidation_sources_enumeration.md` again with fresh checks. Check Binance public data repo paths, Bybit/OKX/Deribit public historical data, CoinAPI alternatives? No - must be free/unauthenticated/no keys. Check GitHub repos, HuggingFace datasets, Zenodo, academic archives, data.commoncrawl style? Or exchange data archives.
2. **Machine-checkable firewall** (HEAVY): Harden `research_state/track_a_deadend_map.md` with executable-style rubric: `unauthenticated == true AND no_keys == true AND symbols>=5 AND blocks>=3 AND completeness_doc == true AND license_ok == true`. For EVERY probed source, fill all fields with evidence (curl-like behavior, dates, sizes).
3. **Bottleneck identification & removal** (HEAVY): If the bottleneck is "need 2024" but only 2026 exists, test 2026 more rigorously under pre-registration. If bottleneck is format/ingestion, write robust parsers for found data. If truly no data exists, make dead-end UNFORGEABLE.
4. **Pre-register if GO** (HEAVY): If ANY source passes rubric, FREEZE protocol BEFORE examining outcomes, create pre-reg, then test. Never peek first.

#### C. TRACK B - MODELED BREACHES (THIRD)
**Goal:** Strengthen separation evidence. Prove cross-contamination impossible.

1. **Separation audit** (HEAVY): Trace code paths - ensure Track B never uses Track A labels. Document in `research_state/track_b_definitive_separation_audit.md`.
2. **Sensitivity analysis** (HEAVY): Vary margin assumptions, liquidation price models, funding assumptions. Document if any gives signal, but NEVER conflate with observed liquidations.
3. **Firewall reinforcement** (HEAVY): Update `research_state/cross_track_decision_firewall.md` with explicit guards.

**STEP 3: DOCUMENTATION & HARDENING (P0)**
1. Create/update `research_state/AGENT_HANDOFF_OUTCOME.md` with timestamp, HEAD, detailed evidence summary of ALL heavy work done.
2. Update `research_state/handoff_hardening_audit.md` proving bottlenecks removed and next agent CANNOT avoid heavy work.
3. Update `research_state/cross_track_decision_log.md` with new findings.
4. Ensure all artifacts cross-linked.
5. Run tests again: `python -m unittest discover -s tests -v` → MUST PASS

### HARD CONSTRAINTS (NEVER VIOLATE)
- No credentials/manual inputs/paid data. No `.github/workflows` changes without explicit maintainer auth. No trading/paper-trading/live orders.
- Strict track separation. Never conflate modeled breaches (B) with observed liquidations (A).
- Preserve negatives/inconclusives. No fabricated data/labels. No zero-fill of missing values.
- Pre-registration REQUIRED for any new experiment. NO outcome inspection before pre-registration.
- No re-tuning on sealed holdouts. No threshold shopping.
- Every iteration must create measurable research/data/testing/engineering progress. Status-only checks are FORBIDDEN.

### SUCCESS CRITERIA
- [ ] All tests pass
- [ ] Track C: Forensic re-audit complete with concrete tables/numbers in consolidated dossier
- [ ] Track A: Machine-checkable firewall applied to ALL candidates; dead-end evidence irrefutable OR GO experiment pre-registered and executed per rules
- [ ] Track B: Separation proven with code-path evidence
- [ ] Bottlenecks identified and removed (documented)
- [ ] `research_state/AGENT_HANDOFF_OUTCOME.md` created/updated with full evidence
- [ ] `research_state/handoff_hardening_audit.md` proves heavy work unavoidable
- [ ] This handoff remains single source of truth

**FORCED HEAVY CAMPAIGN. NO SHORTCUTS. BUILD EVIDENCE, NOT STATUS.**
