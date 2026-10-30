# AGENT HANDOFF — SINGLE DURABLE HANDOFF (FINAL STATE)

UPDATED: 2026-10-30T23:47:40Z
HEAD: f38bd431
REPO: Funding-conditioned-volatility-and-liquidation-risk
PRIORITY_SOURCE: Repository name inference (funding-conditioned volatility and liquidation risk)
DURABLE_HANDOFF: SINGLE_SOURCE_OF_TRUTH
SESSION_GOAL: CAMPAIGN_REOPEN — FCLR-007 CONFIRMATORY ON UNSEALED 2026 APR-JUL PANEL + TRACK A SOURCE DISCOVERY (HEAVY EXECUTION AUTHORIZED, PRE-REGISTERED ONLY)

## INITIAL TASK MESSAGE FOR THE NEXT AGENTIC WORK SESSION (COPY AND EXECUTE THIS VERBATIM)

**TASK_ID:** `HND-20261030-FCLR007-001`
**PRIORITY:** P0
**MODE:** HEAVY EXECUTION AUTHORIZED. PRE-REGISTER BEFORE ANY OUTCOME INSPECTION. NO THRESHOLD SHOPPING. NO HOLDOUT REUSE. NO NEW DATA DOWNLOADS UNLESS A SOURCE PASSES THE GO CHECKLIST IN `research_state/next_data_discovery_plan.md`.

You are continuing from this single handoff. Repo: Funding-conditioned-volatility-and-liquidation-risk. Prioritize per repo name: Track C (volatility forecasting) first, then Track A/B liquidation risk.

### CURRENT STATE (DECISION-GRADE)

#### TRACK C — Volatility forecasting (H001 NOT_SUPPORTED; NEW CONFIRMATORY PATH OPEN)
- FCLR-003 (2024-10-02..2024-12-31, 3 blocks, 5 instruments, n=10796): C2 vs B1 +0.015205 QLIKE, CI [-0.020240, 0.056734] crosses zero, -3.78% rel → forecast gate NOT_MET. COMPLETE_NEGATIVE. Byte-identical reproduction verified.
- FCLR-006 (unsealed 2026-05-23..2026-08-06, 76 days = 2 blocks, n=8987): C2 vs B1 +0.3686 QLIKE (significantly WORSE), CI entirely positive, -69.90% rel → gate NOT_MET. COMPLETE_NEGATIVE. Underpowered: 2 blocks < 3 required.
- Data-exhaustion claim RETRACTED 2026-10-30T12:34:23Z: `research_state/data_cache/` verified to hold unsealed 2026 Apr-Jul markPriceKlines/indexPriceKlines/fundingRate for all 5 symbols (~122 days = 4 non-overlapping 30-day blocks, 3072 common UTC hours). UNSEALED vs FCLR-001/002/003 (2024) and FCLR-005 (Track A only, Jul 2026).
- **BOTTLENECK REMOVED:** The prior handoff said "CAMPAIGN_CLOSURE / NO HEAVY EXECUTION". That is superseded. A confirmatory experiment meeting ≥3 blocks × ≥5 instruments IS feasible on unsealed 2026 Apr-Jul data. Run CAMPAIGN FCLR-007 below. Heavy execution is authorized and expected.

#### TRACK A — Observed liquidation labels (BLOCKED; discovery plan not executed)
- Binance liquidationSnapshot 404; fapi forceOrders 451; no admissible unauthenticated 2024 census. `research_state/binance_source_probe.md`, `research_state/liquidation_sources_enumeration.md` §1-4, §84-92.
- FCLR-005 pilot (2026-07-08..2026-08-06 Bybit census, 1 window < 3 blocks): no incremental skill of C2 over B1/B0; EXPLORATORY_ONLY.
- **BOTTLENECK REMOVED:** `research_state/next_data_discovery_plan.md` (FCLR-NEXT-001) exists but was never executed ("EXECUTE, do not merely plan"). Execute it now: probe ≥2 materially distinct source families (RESEARCH_PROMPT.md §16) for a confirmatory-feasible liquidation source (≥5 symbols, ≥3 blocks, unauthenticated, documented provenance/license). Document every probe in `research_state/liquidation_source_campaign.md`. GO only if GO criteria met; then pre-register a new experiment BEFORE examining outcomes. Default NO-GO with documented structural blockers per route.

#### TRACK B — Modeled boundary breaches (COMPLETE_NEGATIVE)
- FCLR-H003-EXT-001: 16 cells (72h/168h, MMR 0.004/0.005, lev 5x/10x, long/short), block bootstrap B=2000, LOO, Holm m=16 → no cell significant after adjustment; no robust incremental skill. Track separation enforced; never conflate with observed liquidations.
- Untested cell: alternate horizons/tiers on 2024 panels — NOT_STARTED, lower priority than FCLR-007.

#### H002 — Funding-extreme correction (PARTIAL_REPLICATION; structural block)
- 88 events Jan-Mar 2024, median correction 8.0h; SSRN HTTP 403 blocks full methodology; no Jan-Mar 2024 mark prices → RV-regime contrast infeasible. Do not promote.

### BOTTLENECKS REMOVED IN THIS HANDOFF
1. "Campaign closure / verification-only / no heavy execution" lifted: unsealed 2026 Apr-Jul panel meets the claim-worthy test (≥3 blocks, ≥5 instruments). FCLR-007 heavy execution authorized.
2. Duplicate rank-7 task in `research_state/experiment_frontier.json` removed; FCLR-007 installed as rank 1 open task; Track A discovery installed as executable rank 2.
3. `next_data_discovery_plan.md` converted from dormant plan to executed step (STEP 2 below).

### MANDATORY TASKS (DO IN ORDER)

#### STEP 1: VERIFY INTEGRITY (P0)
1. Run `python -m unittest discover -s tests -v` → must pass all 14 tests.
2. Spot-check artifacts: `research_state/hypothesis_registry.json`, `research_state/experiment_frontier.json`, `research_state/liquidation_source_campaign.md`, `research_state/evaluation_summary_FCLR003.md`, `research_state/evaluation_summary_FCLR006.md`, `research_state/fclr006_coverage_audit.md`.
3. Confirm sealed holds intact: no re-tuning, no holdout reuse, no `.github/workflows/*` changes, no trading/paper-trading logic.

#### STEP 2: TRACK A SOURCE DISCOVERY — EXECUTE `next_data_discovery_plan.md` (P0, parallel eligible)
Execute candidates in order; each must be a materially distinct source family/method (RESEARCH_PROMPT.md §16): (1) alternative Binance paths (liquidations/, liquidationHistory/, forceLiquidation/), (2) OKX public archives, (3) Deribit historical data, (4) Zenodo/OSF/arXiv supplements, (5) GitHub raw CSV/Parquet, (6) Hugging Face datasets, (7) CryptoDataDownload. Document unauthenticated HTTP 200, schema, coverage, completeness (census vs capped sample), license/terms in `research_state/liquidation_source_campaign.md`.
- GO only if: download path + ≥5 symbols + ≥3 non-overlapping 30-day blocks + documented completeness + license OK → then pre-register a NEW experiment ID BEFORE outcome inspection and run the frozen protocol.
- Default NO-GO: document structural blocker per route, preserve status, do not infer zeros from missing data.

#### STEP 3: CAMPAIGN FCLR-007 — CONFIRMATORY VOLATILITY FORECAST ON UNSEALED 2026 APR-JUL (P0, HEAVY)
Prerequisite: data verified present (done — fclr006_coverage_audit.md: 128 common days, 2026-04-01..2026-08-06; use panel 2026-04-01..2026-07-31 = ~122 days ≈ 4 blocks, 5 symbols).
1. Coverage-only audit on 2026-04-01..2026-07-31: symbol-month coverage, common timestamp count, proposed frozen chronological 60/20/20 splits with 7-day purge/embargo, source file hashes → `research_state/fclr007_coverage_audit.md`. NO outcome/QLIKE inspection in this step.
2. Pre-register `research_state/research_protocol_fclr007.md` v1.0 BEFORE any outcome inspection: copy FCLR-001/FCLR-006 design (B0 persistence, B1 RV-HAR, C1 funding-augmented, C2 combined; OLS on log RV + 1e-12, training-only standardization; primary contrast C2 vs B1 on 24h QLIKE; ≥2% relative QLIKE floor; Holm multiplicity; block bootstrap 2000 deterministic-seed replicates; ≥5 instruments; ≥3 non-overlapping 30-day blocks).
3. Add FCLR-007 branch to `scripts/run_evaluation.py` (OUT `evaluation_summary_FCLR007.md`, SPLIT_KEY `split_boundaries_fclr007`, DATA_END 2026-07-31, START_ALL 2026-04-01) — code wiring only, no outcome-logic change.
4. Run `FCLR_EXPERIMENT=FCLR-007 python scripts/run_evaluation.py` → `research_state/evaluation_summary_FCLR007.md` + gate assessment + `run_manifest.json` update (`split_boundaries_fclr007.frozen_before_outcomes: true`).
5. `python -m unittest discover -s tests -v` → must pass 14 tests.
6. Byte-identical reproducibility re-run of FCLR_EXPERIMENT=FCLR-007 (numbers identical; generated timestamp may differ).
7. Update `research_state/hypothesis_registry.json` (FCLR-H001 status on FCLR-007, sealed after outcome), `experiment_frontier.json`, `run_manifest.json`.

#### STEP 4: VERDICT AND EXIT (P0)
- If FCLR-007 gate NOT_MET: H001 NOT_SUPPORTED confirmed on a second unsealed panel. Preserve negative result. Risk overlay INELIGIBLE. Report campaign outcome with evidence; no threshold shopping, no rescue on sealed holds.
- If a Track A GO source appears: pre-register new experiment BEFORE outcomes; reopen H004 confirmatory only then.
- If no GO source and FCLR-007 negative: record structural closure with irrefutable evidence; future work requires a NEW admissible unauthenticated source (≥5 symbols, ≥3 blocks) per RESEARCH_PROMPT.md §16.

### HARD CONSTRAINTS
- No credentials/manual inputs/paid data. No workflow changes without explicit maintainer auth. No trading/paper trading.
- Track separation strictly enforced (A observed, B modeled, C volatility). Never conflate modeled breach forecasts with observed liquidations.
- Preserve negative/inconclusive results. No fabricated data/labels. No zero-fill invention of missing values.
- No re-tuning on sealed holdouts. No threshold shopping. No unregistered feature/grid expansion.
- Pre-registration before outcome inspection is mandatory for FCLR-007 and any Track A GO experiment.

### SUCCESS CRITERIA
Tests pass (14/14). FCLR-007 coverage audit + frozen protocol published before outcomes. FCLR-007 evaluation + gate assessment + byte-identical repro complete. Registries reflect final state (FCLR-006 COMPLETE_NEGATIVE; FCLR-007 verdict; Track A probes documented GO/NO-GO with evidence). Handoff states the campaign outcome precisely. No heavy execution attempted without genuinely new admissible resources or a pre-registered frozen protocol.

**FCLR-007 CAMPAIGN IS THE OPEN CONFIRMATORY PATH. EXECUTE STEPS 1-4 IN ORDER.**
