# AGENT HANDOFF — SINGLE DURABLE HANDOFF (LIQUIDATION-RISK CAMPAIGN)

UPDATED: 2026-10-30T17:47:35Z
HEAD: fb7b0da1 (main) — working tree clean (only untracked __pycache__/)
REPO: Funding-conditioned-volatility-and-liquidation-risk
PRIORITY_SOURCE: Repository name inference (funding-conditioned **volatility and liquidation risk**)
DURABLE_HANDOFF: SINGLE_SOURCE_OF_TRUTH
SESSION_GOAL: LIQUIDATION_RISK_HEAVY_CAMPAIGN

## INITIAL TASK MESSAGE FOR THE NEXT AGENTIC WORK SESSION (COPY AND EXECUTE THIS VERBATIM)

**TASK_ID:** `HND-20261030-174735-LIQUIDATION_RISK_EXTENDED`
**PRIORITY:** P0
**MODE:** HEAVY RESEARCH + ENGINEERING. NO VERIFICATION-ONLY CLOSURE. NO STATUS-POLISHING.

You are continuing from this single handoff. The repository name prioritizes **liquidation risk**. H001 (volatility forecasting) is **SEALED_NEGATIVE / NOT_SUPPORTED** and must not be re-run, re-tuned, or threshold-shopped. Your job is to extract any measurable signal for liquidation risk or to produce irrefutable evidence that it is structurally blocked with a concrete, non-dead-end alternative.

### BOTTLENECKS ALREADY REMOVED / ADDRESSED
- **Track A (observed liquidations) discovery exhausted:** Full probe campaign (#1-#9) completed 2026-10-30T17:45:12Z across Binance/Bybit/OKX/Deribit. No unauthenticated complete census found with >=5 symbols, >=90 days, >=3 non-overlapping 30-day blocks. Only ochinimus HF (2026-07-08..2026-08-06, CC BY 4.0) used as exploratory pilot (FCLR-005) with no confirmatory skill. **Do not repeat dead endpoints.**
- **H001 closed:** FCLR-003 confirmatory C2 vs B1 = -3.78% rel QLIKE, CI crosses zero (gate NOT_MET). FCLR-006 unsealed-2026 negative. Treat as closed.
- **Unsealed panel identified:** Unsealed 2026 data exists in `research_state/data_cache/` for `markPriceKlines/`, `indexPriceKlines/`, `fundingRate/` (Apr-Aug 2026) across BTCUSDT/ETHUSDT/BNBUSDT/SOLUSDT/XRPUSDT. This is the **only remaining unsealed panel** with liquidation-adjacent coverage.
- **Track separation enforced:** Modeled boundary breaches (Track B) are distinct from observed liquidations (Track A). Never conflate them. No event-free inference.

### MANDATORY HEAVY EXECUTION PLAN (DO IN ORDER)

#### STEP 1: PRE-REGISTER H003 EXTENSIONS (P0 - BLOCKING, MUST DO BEFORE OUTCOME INSPECTION)
Create a **new, frozen experiment** before looking at any breach counts/metrics.

- **Experiment ID:** Create `FCLR-H003-EXT-001` (or next available ID). Record in `research_state/experiment_frontier.json` with status `PROTOCOL_FROZEN` once complete.
- **Hypothesis:** Do funding extremes + realized volatility + pre-specified price dislocation/smoothing features improve out-of-sample forecast skill for **modeled** perpetual boundary breaches (Track B) on the unsealed 2026 panel?
- **Panel:** Use only unsealed 2026 data from `research_state/data_cache/` (Apr-Aug 2026), all 5 symbols (BTCUSDT/ETHUSDT/BNBUSDT/SOLUSDT/XRPUSDT). Do **not** touch sealed panels or reuse sealed boundaries.
- **Targets (pre-register):** Binary breach (long/short separate) and **event-intensity** (notional-normalized) over **72h and 168h** horizons. Explicitly list them as secondary/extended vs original horizons.
- **Margin scenarios:** Pre-register at least 2 MMR tiers (including a lower MMR tier) with documented assumptions. State funding/fees/price-reference assumptions. If historical maintenance margin cannot be verified for a scenario, label as illustrative adverse-move proxy only.
- **Splits/leakage:** Chronological train/val/test on unsealed panel. Apply purge/embargo >= max horizon (>=7 days). Feature normalization/training params only from train. No look-ahead, no forward-fill, no zero-fill of missing features.
- **Baselines:** B0 (persistence), B1 (HAR-style RV-only). Compare C1 (funding) and C2 (funding + price-dislocation/smoothing) via ablations on identical paired sample.
- **Metrics:** Primary for breach-prob: Brier score, log loss, calibration (slope/intercept). Precision/recall at pre-specified alert budget. QLIKE/MAE/RMSE only if volatility target included and pre-registered. Track both binary and intensity where feasible.
- **Inference:** Block bootstrap (resample complete UTC time blocks across symbols), >=2000 replicates if feasible. Report leave-one-symbol-out and time-block stability. Pre-register minimum practical improvement (>=2% relative reduction) and Holm correction for the declared family.
- **Write protocol:** Create/update `research_state/protocol_FCLR-H003-EXT-001.md` with every item above. Freeze it before computing outcomes.

#### STEP 2: IMPLEMENT & EXECUTE H003 EXTENSIONS (HEAVY ENGINEERING + ANALYSIS)
Do the work, don't just plan.

- **Ingestion:** Ensure restartable loading from `research_state/data_cache/` with checksums, UTC normalization, symbol mapping, duplicate detection. Validate mark/index alignment with frozen tolerance.
- **Labeling:** Implement Track B boundary logic for pre-registered MMR tiers and horizons 72h/168h with correct purge/embargo. Keep long/short separate. Compute event-intensity only where denominators (OI/volume) exist; else report partial coverage with explicit limits.
- **Features:** Implement funding extremeness (past-only 90-day percentile, require >=30 obs), mark/index premium, mark/EMA24 distance. Enforce causal computation (no future data). Track missingness and coverage per feature group.
- **Evaluation:** Run chronological walk-forward on unsealed panel. Compute paired comparisons (C2 vs B1, C1 vs B1, C2 vs C1). Block bootstrap CIs. Calibration plots logic + numbers. Leave-one-symbol-out. Multiplicity correction.
- **Adversarial checks:** Timestamp/unit checks, delistings/symbol reuse, overlap/purge violations, missing funding/mark handling, censored events. Fail fast on leakage.

#### STEP 3: REPORT VERDICT WITH UNCERTAINTY (NO THRESHOLD SHOPPING)
- **If gate met:** Document concrete evidence, but **DO NOT** build risk overlay. Overlay remains ineligible until all protocol gates pass with reproducible artifacts and independent recomputation. If you believe overlay is close, still do not implement it - only register a separate, frozen overlay protocol with its own holdout.
- **If inconclusive:** Try at most **one** narrowly justified alternative feature set (e.g. funding term structure/regime split) **only if** evidence justifies it AND you pre-register a new experiment ID before inspection. Do not grid-search.
- **If blocked:** State exact structural blocker (data/schema/coverage/margin verifiability), list the **single best non-dead-end route** with evidence, and execute it if feasible in this session. Do not write another generic blocker memo.

#### STEP 4: DURABLE HANDOFF UPDATE (MANDATORY)
Update these artifacts before ending:
- `research_state/experiment_frontier.json` - Add/update FCLR-H003-EXT-001 with full state, commands, artifacts
- `research_state/hypothesis_registry.json` - Update H003 status with evidence links
- `research_state/protocol_FCLR-H003-EXT-001.md` - Frozen protocol
- `research_state/evaluation_summary_FCLR-H003-EXT-001.md` - Full results: sample sizes, coverage, baselines, ablations, CIs, calibration, LOO, bootstrap, multiplicity, exclusions, negatives
- `research_state/negative_results_report.md` - Add null/inconclusive findings if any
- `research_state/leakage_audit.md` - Add audit notes for this run
- `AGENT_HANDOFF.md` - Replace the "INITIAL TASK MESSAGE" section with concrete next task + exact verification commands + what was done

### HARD CONSTRAINTS (NON-NEGOTIABLE)
- **No credentials/manual inputs:** Only unauthenticated public data.
- **Respect seals:** Never re-open/inspect sealed holds for tuning. H001 is closed.
- **Track separation:** Modeled (B) vs observed (A) must remain separate. Never call Track B "observed liquidations".
- **Pre-register or don't test:** Any holdout evaluation requires frozen protocol before outcome inspection.
- **No workflow changes:** Do **not** modify `.github/workflows/*` without explicit maintainer authorization.
- **No trading:** No live/paper trading, orders, APIs, accounts, wallets.
- **No filler:** Skip cosmetic status files. Every action must create measurable research/data/testing/engineering progress.
- **Deterministic:** Record git SHA, config hash, source hashes, split boundaries, seeds, software versions in manifests.

### VERIFICATION (MUST PASS)
Run and record exact output:
```bash
python -m unittest discover -s tests -v
```
If tests fail due to your changes, fix them. If unrelated and blocking, document with evidence and propose smallest fix.

### SUCCESS CRITERIA
Significant progress = **(a)** pre-registered and executed FCLR-H003-EXT-001 on unsealed 2026 panel with complete artifacts, **OR** **(b)** produced irrefutable evidence of structural block with concrete non-dead-end route + executed it, **OR** **(c)** found measurable liquidation-risk signal with proper uncertainty/multiplicity/correction and documented it without overlay.
Planning without execution is failure. "All tests pass" alone is not success.

**START NOW. DO HEAVY WORK ON LIQUIDATION RISK.**
