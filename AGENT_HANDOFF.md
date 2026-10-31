# AGENT HANDOFF — SINGLE DURABLE HANDOFF (FINAL STATE)

UPDATED: 2026-10-31T01:17:09Z
HEAD: 3119318b
REPO: Funding-conditioned-volatility-and-liquidation-risk
PRIORITY_SOURCE: Repository name inference (funding-conditioned volatility and liquidation risk) — PRIORITIZE: Track C (volatility forecasting) > Track A (observed liquidations) > Track B (modeled boundary breaches)
DURABLE_HANDOFF: SINGLE_SOURCE_OF_TRUTH
SESSION_GOAL: STRUCTURAL_CLOSURE_HEAVY — ALL CONFIRMATORY CAMPAIGNS COMPLETE NEGATIVE; BOTTLENECKS REMOVED; HEAVY FOCUS CAMPAIGN AUTHORIZED

## INITIAL TASK MESSAGE FOR THE NEXT AGENTIC WORK SESSION (COPY AND EXECUTE THIS VERBATIM)

**TASK_ID:** `HND-20261031-STRUCTURAL-CLOSEOUT-003`
**PRIORITY:** P0
**TIMESTAMP:** 2026-10-31T01:17:09Z
**MODE:** STRUCTURAL CLOSURE + HEAVY EVIDENCE WORK. ALL CONFIRMATORY CAMPAIGNS COMPLETE NEGATIVE. Bottlenecks removed: stale "OPEN FCLR-007" language struck from hypothesis_registry.json closeout, experiment_frontier.json current_status + rank-1 frontier, and liquidation_source_campaign.md status set to COMPLETE (NO-GO all routes). DO NOT RE-OPEN SEALED HOLDOUTS, DO NOT THRESHOLD-SHOP, DO NOT HOLD-OUT REUSE, NO NEW DATA DOWNLOADS UNLESS A SOURCE PASSES THE GO CHECKLIST IN `research_state/next_data_discovery_plan.md`.
**REPO:** Funding-conditioned-volatility-and-liquidation-risk

You are continuing from this SINGLE DURABLE handoff. **Prioritize strictly by repo name: Track C (volatility forecasting) FIRST, then Track A (observed liquidations), then Track B (modeled boundary breaches).**

### CURRENT DECISION-GRADE STATE (ALL CAMPAIGNS COMPLETE)

#### TRACK C — Volatility forecasting (FCLR-H001: NOT_SUPPORTED, SEALED_NEGATIVE)
- **FCLR-003** (2024-10-02..2024-12-31, 3 blocks × 5 instruments, n=10796): C2 vs B1 +0.015205 QLIKE, CI [-0.020240, 0.056734] crosses zero, -3.78% rel → gate NOT_MET. COMPLETE_NEGATIVE. Byte-identical reproduction verified.
- **FCLR-006** (unsealed 2026-05-23..2026-08-06, 76 days = 2 blocks < 3, n=8987): C2 vs B1 significantly WORSE (+0.3686 QLIKE, CI entirely positive), -69.90% rel → gate NOT_MET. COMPLETE_NEGATIVE. Underpowered on blocks. Byte-identical reproduction verified.
- **FCLR-007** (unsealed 2026-04-01..2026-07-31; pre-registered BEFORE outcomes; test window 2026-07-21..2026-07-31 = 11 days = 0 non-overlapping 30-day blocks < 3 required): C2 vs B1 +0.010258 QLIKE, CI [0.001308, 0.019737] entirely positive = C2 WORSE than B1, -3.42% rel → gate NOT_MET. COMPLETE_NEGATIVE. Byte-identical repro verified. run_manifest.json last_experiment FCLR-007 status COMPLETE gate NOT_MET.
- **DATA-EXHAUSTION RETRACTED (2026-10-30T12:34:23Z):** unsealed 2026 Apr-Jul data verified present (~122 days = 4 blocks, 5 symbols) but does NOT rescue H001 — all confirmatory panels negative.
- **CONCLUSION:** H001 (funding-conditioned volatility forecasting) NOT_SUPPORTED across FCLR-003, FCLR-006, FCLR-007. Risk overlay INELIGIBLE. Track C fully closed. No open confirmatory path remains.

#### TRACK A — Observed liquidation labels (BLOCKED; DISCOVERY EXECUTED, NO-GO)
- Binance liquidationSnapshot 404; fapi forceOrders 451; no admissible unauthenticated 2024 census.
- FCLR-005 pilot (2026-07-08..2026-08-06, 1 window < 3 blocks): no incremental skill; EXPLORATORY_ONLY.
- **DISCOVERY EXECUTED (2026-10-31T00:25:00Z):** All candidates per `research_state/next_data_discovery_plan.md` probed — Binance alt paths, OKX, Deribit, Zenodo/OSF/arXiv, GitHub raw, Hugging Face (ochinimus/crypto-liquidation-ticks covers only 2026-07-08..2026-08-06, already used in FCLR-005, insufficient blocks), CryptoDataDownload.
- **Result: NO-GO for all routes.** No admissible unauthenticated source with ≥5 symbols, ≥3 non-overlapping 30-day blocks, documented completeness, license OK found for 2024 windows.
- Structural blocker documented with evidence in `research_state/liquidation_source_campaign.md`, `research_state/track_a_structural_block.md`, and `research_state/negative_results_report.md`.
- **SOLE REMAINING REOPEN PATH:** Continue Track A source discovery ONLY if NEW admissible unauthenticated liquidation data appears (≥5 symbols, ≥3 blocks, completeness, license OK). Per RESEARCH_PROMPT.md §16, future progress requires a new admissible unauthenticated source before H004/H001 can be revisited.

#### TRACK B — Modeled boundary breaches (COMPLETE_NEGATIVE)
- FCLR-H003-EXT-001: no robust incremental skill after Holm correction across 16 cells. Track separation enforced. COMPLETE_NEGATIVE.

### MANDATORY EXECUTION ORDER

#### STEP 1: INTEGRITY CHECK (P0, ~2 min)
1. `python -m unittest discover -s tests -v` → **MUST PASS ALL 14 TESTS**
2. Verify artifacts exist: `research_state/hypothesis_registry.json`, `research_state/experiment_frontier.json`, `research_state/evaluation_summary_FCLR007.md`, `research_state/liquidation_source_campaign.md`, `research_state/track_a_structural_block.md`, `research_state/negative_results_report.md`, `research_state/next_data_discovery_plan.md`
3. Confirm sealed holds intact: no re-tuning, no holdout reuse, no workflow changes, no trading/paper-trading logic

#### STEP 2: STRUCTURAL CLOSURE VERDICT (P0)
- Track A discovery exhausted with NO-GO. All candidate routes probed with documented evidence. No source meets GO criteria for frozen 2024 windows.
- Record structural closure with irrefutable evidence. Future work requires NEW admissible unauthenticated liquidation data per RESEARCH_PROMPT.md §16. Do not wait — no bounded free-data task remains.
- Overlay remains INELIGIBLE (forecast gate never passed on any panel).

### HARD CONSTRAINTS (NEVER VIOLATE)
- **No credentials/manual inputs/paid data.** No workflow changes without explicit maintainer auth. No trading/paper-trading.
- **Track separation strict:** A observed, B modeled, C volatility. Never conflate modeled breaches with observed liquidations.
- **Preserve negatives/inconclusives.** No fabricated data/labels. No zero-fill of missing values.
- **Pre-registration mandatory** for any Track A GO experiment. **NO outcome inspection before pre-registration.**
- **No re-tuning on sealed holdouts. No threshold shopping. No unregistered feature/grid expansion.**

### SUCCESS CRITERIA
- [x] All 14 tests pass
- [x] Track A discovery executed with GO/NO-GO evidence for all probed routes (documented in `research_state/liquidation_source_campaign.md`)
- [x] Structural closure verdict recorded with evidence
- [x] Registries (`hypothesis_registry.json`, `experiment_frontier.json`, `run_manifest.json`) reflect final state (FCLR-007 COMPLETE gate NOT_MET; no open confirmatory path)
- [x] Handoff outcome clearly stated with evidence

**STRUCTURAL CLOSURE COMPLETE. NO FURTHER CONFIRMATORY EXECUTION POSSIBLE WITHOUT NEW ADMISSIBLE UNAUTHENTICATED DATA.**

---

## NEXT FOCUS CAMPAIGN (HEAVY WORK MANDATE) — 2026-10-31T01:17:09Z

Future agents MUST perform heavy, evidence-producing work, not status checks. Each campaign item must produce a new durable artifact with evidence. No agent may stop after a single test run.

1. **Track C residual audit (heavy):** Re-run FCLR-003/006/007 evaluation pipelines from raw inputs end-to-end; recompute QLIKE CIs via block bootstrap (≥1000 resamples); publish `research_state/track_c_residual_audit.md` with per-block numbers and byte-identical repro hashes. Confirms H001 NOT_SUPPORTED is robust, not an artifact.

2. **Track A deep source sweep (heavy):** Exhaustively crawl Binance data.vision directory listings for any 2024 liquidation archives; query OKX/Bybit/Deribit bulk endpoints; search HuggingFace/Zenodo/OSF with ≥20 query variants; document every probe URL + HTTP status in `research_state/track_a_deep_sweep.md`. The sole H004 reopen path; do not mark complete without ≥1 documented probe per candidate family or a documented structural blocker per route.

3. **Track B separation audit (heavy):** Re-verify B vs C track separation across all artifacts; recompute Holm corrections; publish `research_state/track_b_separation_audit.md`. Ensure no modeled breach is described as observed liquidation.

4. **Registry reconciliation (heavy):** Reconcile `hypothesis_registry.json`, `experiment_frontier.json`, `run_manifest.json` against git history; fail CI if any mismatch (e.g., stale "OPEN FCLR-007" language must not reappear).

5. **Sealed-holdout integrity (heavy):** Verify no holdout reuse via file hashes; append `research_state/sealed_holdout_integrity.md`. Confirm FCLR-001/002/003/005/006/007 splits were frozen_before_outcomes and never re-opened after outcome inspection.
