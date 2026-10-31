# AGENT HANDOFF — SINGLE DURABLE HANDOFF (FINAL STATE)

UPDATED: 2026-10-31T00:18:08Z
HEAD: 7a036e8e
REPO: Funding-conditioned-volatility-and-liquidation-risk
PRIORITY_SOURCE: Repository name inference (funding-conditioned volatility and liquidation risk) — **PRIORITIZE: Track C (volatility) > Track A (observed liquidations) > Track B (modeled breaches)**
DURABLE_HANDOFF: SINGLE_SOURCE_OF_TRUTH
SESSION_GOAL: CAMPAIGN_FCLR007_MANDATORY_HEAVY_EXECUTION — CONFIRMATORY ON UNSEALED 2026-04-01..2026-07-31 PANEL + TRACK A SOURCE DISCOVERY IN PARALLEL

## INITIAL TASK MESSAGE FOR THE NEXT AGENTIC WORK SESSION (COPY AND EXECUTE THIS VERBATIM)

**TASK_ID:** `HND-20261031-FCLR007-HEAVY-001`
**PRIORITY:** P0
**TIMESTAMP:** 2026-10-31T00:18:08Z
**MODE:** HEAVY EXECUTION AUTHORIZED. PRE-REGISTER BEFORE ANY OUTCOME INSPECTION. NO THRESHOLD SHOPPING. NO HOLDOUT REUSE. NO NEW DATA DOWNLOADS UNLESS A SOURCE PASSES THE GO CHECKLIST IN `research_state/next_data_discovery_plan.md`.
**REPO:** Funding-conditioned-volatility-and-liquidation-risk

You are continuing from this SINGLE DURABLE handoff. **Prioritize strictly by repo name: Track C (volatility forecasting) FIRST, then Track A (observed liquidations), then Track B (modeled boundary breaches).**

### MISSION (NON-NEGOTIABLE)
This repo studies funding-conditioned volatility and liquidation risk. The cleanest claim-worthy path forward is **confirmatory testing of funding-conditioned volatility forecasting (FCLR-H001)** on unsealed data. A feasible confirmatory panel exists. **Do not wait. Do not defer to "verification only". Execute heavy work.**

### CURRENT DECISION-GRADE STATE

#### TRACK C — Volatility forecasting (H001 NOT_SUPPORTED so far; CONFIRMATORY PATH OPEN)
- **FCLR-003** (2024-10-02..2024-12-31, 3 blocks × 5 instruments, n=10796): C2 vs B1 +0.015205 QLIKE, CI [-0.020240, 0.056734] crosses zero, -3.78% rel → gate NOT_MET. COMPLETE_NEGATIVE. Byte-identical reproduction verified.
- **FCLR-006** (unsealed 2026-05-23..2026-08-06, 76 days = 2 blocks < 3, n=8987): C2 vs B1 significantly WORSE (+0.3686 QLIKE, CI entirely positive), -69.90% rel → gate NOT_MET. COMPLETE_NEGATIVE. Underpowered on blocks.
- **DATA-EXHAUSTION RETRACTED (2026-10-30T12:34:23Z):** `research_state/data_cache/` contains unsealed 2026 Apr-Jul markPriceKlines/indexPriceKlines/fundingRate for all 5 symbols (~122 days = 4 non-overlapping 30-day blocks, 3072 common UTC hours). **FEASIBLE:** ≥3 blocks × ≥5 instruments exists.
- **BOTTLENECK REMOVED:** Prior "campaign closure / no heavy execution" is SUPERSEDED. **CAMPAIGN FCLR-007 IS MANDATORY HEAVY EXECUTION.**

#### TRACK A — Observed liquidation labels (BLOCKED; MUST EXECUTE DISCOVERY)
- Binance liquidationSnapshot 404; fapi forceOrders 451; no admissible unauthenticated 2024 census.
- FCLR-005 pilot (2026-07-08..2026-08-06, 1 window < 3 blocks): no incremental skill; EXPLORATORY_ONLY.
- **BOTTLENECK REMOVED:** `research_state/next_data_discovery_plan.md` (FCLR-NEXT-001) exists but NOT executed. **EXECUTE IT NOW.** Probe ≥2 materially distinct source families. GO only if meets criteria; else document structural blockers with evidence. Default NO-GO.

#### TRACK B — Modeled boundary breaches (COMPLETE_NEGATIVE)
- FCLR-H003-EXT-001: no robust incremental skill after Holm correction across 16 cells. Track separation enforced.

### MANDATORY EXECUTION ORDER (DO NOT SKIP)

#### STEP 1: INTEGRITY CHECK (P0, ~2 min)
1. `python -m unittest discover -s tests -v` → **MUST PASS ALL 14 TESTS**
2. Verify artifacts exist: `research_state/hypothesis_registry.json`, `research_state/experiment_frontier.json`, `research_state/evaluation_summary_FCLR003.md`, `research_state/evaluation_summary_FCLR006.md`
3. Confirm sealed holds intact: no re-tuning, no holdout reuse, no workflow changes, no trading/paper-trading logic

#### STEP 2: TRACK A DISCOVERY (P0, PARALLEL WITH STEP 3 PREP)
Execute `research_state/next_data_discovery_plan.md` candidates in order (materially distinct families): (1) Binance alt paths (liquidations/, liquidationHistory/, forceLiquidation/), (2) OKX public archives, (3) Deribit, (4) Zenodo/OSF/arXiv, (5) GitHub raw CSV/Parquet, (6) Hugging Face, (7) CryptoDataDownload. Document EVERY probe in `research_state/liquidation_source_campaign.md`. **GO only if:** download path + ≥5 symbols + ≥3 non-overlapping 30-day blocks + documented completeness + license OK. **Pre-register NEW experiment BEFORE examining outcomes if GO.** Else document structural blocker per route.

#### STEP 3: CAMPAIGN FCLR-007 — CONFIRMATORY VOLATILITY (P0, HEAVY EXECUTION)
**Panel:** 2026-04-01..2026-07-31, all 5 symbols (BTCUSDT,ETHUSDT,BNBUSDT,SOLUSDT,XRPUSDT), ~122 days ≈ 4 blocks. Data VERIFIED present.
1. **Coverage audit (NO outcome inspection):** Create `research_state/fclr007_coverage_audit.md` with symbol-month coverage, common timestamp counts, frozen chronological 60/20/20 splits with 7-day purge/embargo, source file hashes.
2. **Pre-register BEFORE outcomes:** Create `research_state/research_protocol_fclr007.md` v1.0 copying FCLR-001/FCLR-006 design (B0 persistence, B1 RV-HAR, C1 funding-augmented, C2 combined; OLS on log RV + 1e-12, training-only standardization; primary contrast C2 vs B1 on 24h QLIKE; ≥2% relative QLIKE floor; Holm multiplicity; block bootstrap 2000 deterministic-seed replicates; ≥5 instruments; ≥3 non-overlapping 30-day blocks).
3. **Wire code:** Add FCLR-007 branch to `scripts/run_evaluation.py` (OUT `evaluation_summary_FCLR007.md`, SPLIT_KEY `split_boundaries_fclr007`, DATA_END 2026-07-31, START_ALL 2026-04-01). Code wiring only, no outcome logic changes.
4. **Execute:** `FCLR_EXPERIMENT=FCLR-007 python scripts/run_evaluation.py` → produces `research_state/evaluation_summary_FCLR007.md`, gate assessment, updates `run_manifest.json` with `split_boundaries_fclr007.frozen_before_outcomes: true`.
5. **Tests:** `python -m unittest discover -s tests -v` must still pass (14/14).
6. **Byte-identical repro:** Re-run FCLR-007; numbers identical (timestamp may differ). Document.
7. **Update registries:** Update `research_state/hypothesis_registry.json` (FCLR-H001 status), `research_state/experiment_frontier.json`, `run_manifest.json`.

#### STEP 4: VERDICT & CLEAN EXIT (P0)
- **If FCLR-007 gate NOT_MET:** H001 NOT_SUPPORTED confirmed on second unsealed panel. Preserve negative result. Risk overlay INELIGIBLE. No threshold shopping, no rescue on sealed holds.
- **If Track A finds GO source:** Pre-register new experiment BEFORE outcomes; reopen H004 only then.
- **If no GO + FCLR-007 negative:** Record structural closure with irrefutable evidence. Future work requires NEW admissible unauthenticated source (≥5 symbols, ≥3 blocks) per RESEARCH_PROMPT.md §16.

### HARD CONSTRAINTS (NEVER VIOLATE)
- **No credentials/manual inputs/paid data.** No workflow changes without explicit maintainer auth. No trading/paper-trading.
- **Track separation strict:** A observed, B modeled, C volatility. Never conflate modeled breaches with observed liquidations.
- **Preserve negatives/inconclusives.** No fabricated data/labels. No zero-fill of missing values.
- **Pre-registration mandatory** for FCLR-007 and any Track A GO experiment. **NO outcome inspection before pre-registration.**
- **No re-tuning on sealed holdouts. No threshold shopping. No unregistered feature/grid expansion.**

### SUCCESS CRITERIA
- [ ] All 14 tests pass
- [ ] FCLR-007 coverage audit + frozen protocol published BEFORE outcomes
- [ ] FCLR-007 executed, gate assessed, byte-identical repro verified
- [ ] Track A discovery executed with evidence for all probed routes (GO/NO-GO documented)
- [ ] Registries updated to reflect final state
- [ ] Handoff outcome clearly stated with evidence

**EXECUTE STEPS 1-4 IN ORDER. HEAVY EXECUTION IS AUTHORIZED AND EXPECTED. DO NOT STOP AT PLANNING.**
