# AGENT HANDOFF — SINGLE DURABLE HANDOFF (FINAL STATE)

UPDATED: 2026-10-30T23:47:01Z
HEAD: 3fe7083e
REPO: Funding-conditioned-volatility-and-liquidation-risk
PRIORITY_SOURCE: Repository name inference (funding-conditioned volatility and liquidation risk)
DURABLE_HANDOFF: SINGLE_SOURCE_OF_TRUTH
SESSION_GOAL: CAMPAIGN_CLOSURE (NO VIABLE PATH FORWARD)

## INITIAL TASK MESSAGE FOR THE NEXT AGENTIC WORK SESSION (COPY AND EXECUTE THIS VERBATIM)

**TASK_ID:** `HND-20261030-FINAL-CLOSURE-001`
**PRIORITY:** P0
**MODE:** VERIFICATION-ONLY. NO HEAVY EXECUTION. NO NEW DATA DOWNLOADS.

You are continuing from this single handoff. Both major tracks have been exhaustively investigated under frozen protocols with no viable path forward without paid data/credentials or genuinely new admissible free sources.

### CURRENT STATE (DECISION-GRADE)

#### TRACK A — Observed liquidation labels (BLOCKED)
- Exhaustive unauthenticated probes of Binance public archive paths (liquidationSnapshot/forceOrders) returned 404/451; no other admissible free sources found with defensible provenance/coverage.
- Documented in: `research_state/liquidation_source_campaign.md`
- Status: STRUCTURALLY BLOCKED. Do not re-sweep absent genuinely new free source/endpoint/dataset.

#### TRACK B — Modeled boundary breaches (INCONCLUSIVE/NEGATIVE)
- FCLR-H003-EXT-001 on unsealed 2026 panel (BTCUSDT/ETHUSDT/BNBUSDT/SOLUSDT/XRPUSDT), horizons 72h/168h, MMR 0.004/0.005, lev 5x/10x, long/short separate.
- Inference: block bootstrap B=2000, LOO, Holm correction across 16 cells. No cell significant after adjustment; most ΔBrier CIs cross 0. Intensity target blocked by missing OI/volume denominators.
- Artifacts: `research_state/protocol_FCLR-H003-EXT-001.md`, `research_state/evaluation_summary_FCLR-H003-EXT-001.md`
- Status: NO ROBUST INCREMENTAL SKILL. Track separation enforced.

#### TRACK C — Volatility forecasting (NOT SUPPORTED)
- FCLR-001 (2024-01..03, pilot): C2 vs B1 -2.50% rel QLIKE, CI crosses zero → INCONCLUSIVE
- FCLR-002 (2024-04..09, 2 blocks): C2 vs B1 -9.28% rel QLIKE, CI excludes zero but only 2 non-overlapping 30-day blocks < 3 required → INCONCLUSIVE (underpowered)
- FCLR-003 (2024-10..12, 3 blocks, powered): C2 vs B1 -3.78% rel QLIKE, CI crosses zero → NOT_SUPPORTED
- FCLR-006 (2026-05..08, unsealed, 2 blocks): C2 vs B1 +0.369 QLIKE (significantly WORSE), rel -67.3%, CI entirely positive → NOT_SUPPORTED
- H001 status: NOT_SUPPORTED across all tested panels. Forecast gate never met with required block count + multiplicity + CI conditions.
- Artifacts: `research_state/research_protocol.md` (FCLR-001), `research_state/research_protocol_fclr002.md`, `research_state/evaluation_summary_FCLR003.md`, `research_state/evaluation_summary_FCLR006.md`, `research_state/final_confirmatory_verdict.md`

#### H002 — Funding-extreme correction time (PARTIAL)
- Partial replication of Shek (SSRN 7529458): 88 events across 5 symbols Jan-Mar 2024, median correction 8.0h, RV-regime contrast infeasible (no Jan-Mar mark prices). Paper methodology not recoverable (SSRN 403).
- Artifacts: `research_state/h002_replication_report.md`, `research_state/h002_pre_registration.md`, `scripts/funding_correction_replication.py`, `tests/test_funding_correction_replication.py`
- Status: PARTIAL_REPLICATION only. Not promoted to forecast/liquidation evidence.

### MANDATORY TASKS (DO IN ORDER)

#### STEP 1: VERIFY INTEGRITY (P0)
1. Run `python -m unittest discover -s tests -v` → must pass all tests.
2. Spot-check key artifacts exist: `research_state/hypothesis_registry.json`, `research_state/experiment_frontier.json`, `research_state/liquidation_source_campaign.md`, all evaluation summaries above.
3. Confirm no sealed holdouts opened inappropriately; splits remain frozen as documented.

#### STEP 2: FINALIZE DOCUMENTATION (P0)
1. Ensure `research_state/hypothesis_registry.json` reflects final states (H001 NOT_SUPPORTED, H002 PARTIAL_REPLICATION, H003 NOT_SUPPORTED, H004 EXPLORATORY_ONLY/BLOCKED).
2. Ensure `research_state/experiment_frontier.json` shows campaigns complete/closed as appropriate.
3. Update this AGENT_HANDOFF.md timestamp if making changes (only if meaningful).

#### STEP 3: CLEAN EXIT (P0)
1. If no new admissible free source, credentials, or paid data becomes available and no protocol change is authorized, do NOT fabricate work. Report campaign complete with evidence.
2. Do not modify `.github/workflows/*` without explicit maintainer authorization.
3. Do not add trading/paper-trading logic. Risk-overlay remains INELIGIBLE.

### HARD CONSTRAINTS
- No credentials/manual inputs/paid data. No workflow changes without explicit maintainer auth. No trading/paper trading.
- Track separation strictly enforced (A observed, B modeled, C volatility). Never conflate.
- Preserve negative/inconclusive results. No fabricated data/labels.
- No re-tuning on sealed holdouts. No threshold shopping.
- Do not attempt to "mine" for significance across unregistered comparisons.

### SUCCESS CRITERIA
Tests pass. All registries reflect final decision-grade state. Handoff documents complete closure with irrefutable evidence for blocks/inconclusives. No further heavy execution attempted without genuinely new admissible resources.

**CAMPAIGN COMPLETE. NO VIABLE PATH FORWARD WITHOUT PAID DATA/CREDENTIALS OR GENUINELY NEW ADMISSIBLE FREE SOURCES.**
