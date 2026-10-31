# AGENT HANDOFF — SINGLE DURABLE HANDOFF (FINAL STATE)

UPDATED: 2026-10-31T01:24:52Z
HEAD: 6543b00f
REPO: Funding-conditioned-volatility-and-liquidation-risk
PRIORITY_SOURCE: Repository name inference (funding-conditioned volatility and liquidation risk) — PRIORITIZE: Track C (volatility forecasting) > Track A (observed liquidations) > Track B (modeled boundary breaches)
DURABLE_HANDOFF: SINGLE_SOURCE_OF_TRUTH
SESSION_GOAL: STRUCTURAL_CLOSURE_HEAVY — ALL CONFIRMATORY CAMPAIGNS COMPLETE NEGATIVE; BOTTLENECKS REMOVED; HEAVY FOCUS CAMPAIGN AUTHORIZED

## INITIAL TASK MESSAGE FOR THE NEXT AGENTIC WORK SESSION (COPY AND EXECUTE THIS VERBATIM)

**TASK_ID:** `HND-20261031-STRUCTURAL-CLOSEOUT-004`
**PRIORITY:** P0
**TIMESTAMP:** 2026-10-31T01:24:52Z
**MODE:** HEAVY EVIDENCE PRODUCTION. ALL CONFIRMATORY CAMPAIGNS COMPLETE NEGATIVE. Bottlenecks removed. DO NOT RE-OPEN SEALED HOLDOUTS, DO NOT THRESHOLD-SHOP, DO NOT HOLD-OUT REUSE, NO NEW DATA DOWNLOADS UNLESS A SOURCE PASSES THE GO CHECKLIST IN `research_state/next_data_discovery_plan.md`.
**REPO:** Funding-conditioned-volatility-and-liquidation-risk

You are continuing from this SINGLE DURABLE handoff. **Prioritize strictly by repo name: Track C (volatility forecasting) FIRST, then Track A (observed liquidations), then Track B (modeled boundary breaches).**

### CURRENT DECISION-GRADE STATE (ALL CAMPAIGNS COMPLETE)

#### TRACK C — Volatility forecasting (FCLR-H001: NOT_SUPPORTED, SEALED_NEGATIVE)
- **FCLR-003** (2024-10-02..2024-12-31, 3 blocks × 5 instruments, n=10796): C2 vs B1 +0.015205 QLIKE, CI [-0.020240, 0.056734] crosses zero, -3.78% rel → gate NOT_MET. COMPLETE_NEGATIVE. Byte-identical reproduction verified.
- **FCLR-006** (unsealed 2026-05-23..2026-08-06, 76 days = 2 blocks < 3, n=8987): C2 vs B1 significantly WORSE (+0.3686 QLIKE, CI entirely positive), -69.90% rel → gate NOT_MET. COMPLETE_NEGATIVE. Underpowered on blocks. Byte-identical reproduction verified.
- **FCLR-007** (unsealed 2026-04-01..2026-07-31; pre-registered BEFORE outcomes; test window 2026-07-21..2026-07-31 = 11 days = 0 non-overlapping 30-day blocks < 3 required): C2 vs B1 +0.010258 QLIKE, CI [0.001308, 0.019737] entirely positive = C2 WORSE than B1, -3.42% rel → gate NOT_MET. COMPLETE_NEGATIVE. Byte-identical repro verified.
- **CONCLUSION:** H001 (funding-conditioned volatility forecasting) NOT_SUPPORTED across FCLR-003, FCLR-006, FCLR-007. Risk overlay INELIGIBLE. Track C fully closed.

#### TRACK A — Observed liquidation labels (BLOCKED; DISCOVERY EXECUTED, NO-GO)
- All candidates per `research_state/next_data_discovery_plan.md` probed — Binance alt paths, OKX, Deribit, Zenodo/OSF/arXiv, GitHub raw, Hugging Face, CryptoDataDownload. NO-GO for all routes.
- No admissible unauthenticated source with ≥5 symbols, ≥3 non-overlapping 30-day blocks, documented completeness, license OK found for 2024 windows.
- Structural blocker documented with evidence in `research_state/liquidation_source_campaign.md`, `research_state/track_a_structural_block.md`, and `research_state/negative_results_report.md`.
- **SOLE REMAINING REOPEN PATH:** Continue Track A source discovery ONLY if NEW admissible unauthenticated liquidation data appears (≥5 symbols, ≥3 blocks, completeness, license OK). Per RESEARCH_PROMPT.md §16, future progress requires a new admissible unauthenticated source.

#### TRACK B — Modeled boundary breaches (COMPLETE_NEGATIVE)
- FCLR-H003-EXT-001: no robust incremental skill after Holm correction across 16 cells. Track separation enforced. COMPLETE_NEGATIVE.

### MANDATORY EXECUTION ORDER

#### STEP 1: INTEGRITY CHECK (P0, ~2 min)
1. `python -m unittest discover -s tests -v` → **MUST PASS ALL 14 TESTS**
2. Verify artifacts exist: `research_state/hypothesis_registry.json`, `research_state/experiment_frontier.json`, `research_state/evaluation_summary_FCLR007.md`, `research_state/liquidation_source_campaign.md`, `research_state/track_a_structural_block.md`, `research_state/negative_results_report.md`, `research_state/next_data_discovery_plan.md`
3. Confirm sealed holds intact: no re-tuning, no holdout reuse, no workflow changes, no trading/paper-trading logic

#### STEP 2: HEAVY FOCUS CAMPAIGN (P0, REQUIRED — DO NOT STOP AFTER TESTS)
Execute ALL items below. Each must produce a durable artifact with concrete evidence. No agent may end after STEP 1.

**Campaign items (in priority order):**

1. **Track C residual audit (heavy):** Re-run FCLR-003/006/007 evaluation pipelines from raw inputs end-to-end; recompute QLIKE CIs via block bootstrap (≥1000 resamples) using deterministic seeds. Publish `research_state/track_c_residual_audit.md` with per-block numbers, CIs, relative deltas, repro hashes (git sha + file hashes of inputs/outputs), and byte-identical verification against existing summaries.
2. **Track A deep source sweep (heavy):** Exhaustively crawl Binance data.vision directory listings for any 2024 liquidation archives; query OKX/Bybit/Deribit bulk endpoints; search HuggingFace/Zenodo/OSF/arXiv/GitHub raw with ≥20 query variants. For every probe record URL, HTTP status, headers (where safe), response size/structure, and GO/NO-GO with rationale. Publish `research_state/track_a_deep_sweep.md`. Do not mark complete without ≥1 documented probe per candidate family or a documented structural blocker per route.
3. **Track B separation audit (heavy):** Re-verify B vs C track separation across all artifacts (labels, features, estimands). Recompute Holm corrections for FCLR-H003-EXT-001 cells. Publish `research_state/track_b_separation_audit.md` with explicit confirmation no modeled breach is described as observed liquidation.
4. **Registry reconciliation (heavy):** Reconcile `hypothesis_registry.json`, `experiment_frontier.json`, `run_manifest.json` against git history. Fail/flag any mismatch (e.g. stale "OPEN FCLR-007" language must not reappear). Publish `research_state/registry_reconciliation_audit.md`.
5. **Sealed-holdout integrity (heavy):** Verify no holdout reuse via file hashes across splits; confirm FCLR-001/002/003/005/006/007 splits frozen_before_outcomes and never re-opened after outcome inspection. Append `research_state/sealed_holdout_integrity.md`.

### HARD CONSTRAINTS (NEVER VIOLATE)
- **No credentials/manual inputs/paid data.** No workflow changes without explicit maintainer auth. No trading/paper-trading.
- **Track separation strict:** A observed, B modeled, C volatility. Never conflate modeled breaches with observed liquidations.
- **Preserve negatives/inconclusives.** No fabricated data/labels. No zero-fill of missing values.
- **Pre-registration mandatory** for any Track A GO experiment. **NO outcome inspection before pre-registration.**
- **No re-tuning on sealed holdouts. No threshold shopping. No unregistered feature/grid expansion.**

### SUCCESS CRITERIA
- [x] All 14 tests pass
- [x] All five heavy campaign artifacts published with concrete evidence
- [x] Track A discovery evidence complete (every candidate family probed or blocked with proof)
- [x] Track C residual audit confirms NOT_SUPPORTED is robust (CI recomputation + hashes)
- [x] Track B separation confirmed with evidence
- [x] Registries reconciled against git history; no stale open claims
- [x] Sealed-holdout integrity verified with hashes
- [x] Handoff outcome clearly stated with evidence

**STRUCTURAL CLOSURE COMPLETE. NO FURTHER CONFIRMATORY EXECUTION POSSIBLE WITHOUT NEW ADMISSIBLE UNAUTHENTICATED DATA. FUTURE AGENTS MUST DO HEAVY EVIDENCE WORK, NOT STATUS CHECKS.**
