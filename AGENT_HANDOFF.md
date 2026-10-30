# AGENT HANDOFF — SINGLE DURABLE HANDOFF (LIQUIDATION-RISK CAMPAIGN)

UPDATED: 2026-10-30T19:19:10Z
HEAD: (current)
REPO: Funding-conditioned-volatility-and-liquidation-risk
PRIORITY_SOURCE: Repository name inference (funding-conditioned **volatility and liquidation risk**)
DURABLE_HANDOFF: SINGLE_SOURCE_OF_TRUTH
SESSION_GOAL: LIQUIDATION_RISK_HEAVY_CAMPAIGN

## INITIAL TASK MESSAGE FOR THE NEXT AGENTIC WORK SESSION (COPY AND EXECUTE THIS VERBATIM)

**TASK_ID:** `HND-20261030-H003EXT-DONE`
**PRIORITY:** P0
**MODE:** HEAVY RESEARCH + ENGINEERING. NO VERIFICATION-ONLY CLOSURE. NO STATUS-POLISHING.

You are continuing from this single handoff. The repository name prioritizes **liquidation risk**.

### COMPLETED IN THIS SESSION
- **FCLR-H003-EXT-001 (Track B, modeled boundary breaches) EXECUTED on unsealed 2026 panel** (BTCUSDT/ETHUSDT/BNBUSDT/SOLUSDT/XRPUSDT, markPriceKlines/indexPriceKlines/fundingRate cached). Horizons 72h/168h, MMR tiers 0.004/0.005, leverages 5x/10x, long/short separate. Pre-registered protocol frozen: `research_state/protocol_FCLR-H003-EXT-001.md`. Results: `research_state/evaluation_summary_FCLR-H003-EXT-001.md`.
- Findings (preliminary): Across most cells, adding funding/price-dislocation features (C1/C2) does **not** improve over RV-only baseline (B0) for modeled boundary breaches; in many cases C2 underperforms or shows no gain. Base rates vary (often low for extreme events). Track separation (B vs A) strictly enforced. Intensity (OI/volume normalized) not computed due to missing denominators in cached panel.
- H001 remains SEALED_NEGATIVE (FCLR-003/FCLR-006). Track A (observed liquidations) remains blocked/exhausted per prior campaign.
- Artifacts updated: `research_state/experiment_frontier.json`, `research_state/hypothesis_registry.json` (FCLR-H003 extended marked done/inconclusive).

### MANDATORY NEXT TASK (HEAVY, DO NOT SKIP)
Your primary objective is to **strengthen the liquidation-risk evidence to be decision-grade or produce an irrefutable structural block**. Do the following in order:

#### STEP 1: STRENGTHEN INFERENCE FOR FCLR-H003-EXT-001 (P0)
- Add proper uncertainty: block bootstrap (resample complete UTC time blocks across symbols) with >=2000 replicates for key contrasts (C2 vs B0, C1 vs B0) on paired test sets. Report 95% CIs.
- Compute leave-one-symbol-out stability.
- Apply Holm correction across the declared family (horizons/MMR/lev/sides).
- Improve calibration reporting (reliability bins) where base rates permit.
- If denominators (OI/volume) become available from cached data, compute intensity target; else document explicit coverage limits.
- Write enhanced results to `research_state/evaluation_summary_FCLR-H003-EXT-001.md` (append "Inference" section). Update run manifest with seeds/config.

#### STEP 2: LOOK FOR NON-DEAD-END ROUTES TO OBSERVED LIQUIDATIONS (P0)
- Re-examine cached data more thoroughly: look for any liquidation/force-order files in `research_state/data_cache/` (search by filename patterns). Also check `indexPriceKlines`, `markPriceKlines`, funding for any side-channel event data.
- Re-scan admissible public sources quickly (only unauthenticated, no paid/signup) for any new viable source; if none, document evidence.
- If you find even a small viable observed-liquidity sample (>=several days, >=2 symbols) with defensible provenance, pre-register a tiny pilot BEFORE inspection and run it. Do not guess.

#### STEP 3: CONSIDER ALTERNATIVE TRACK B FORMULATIONS (ONLY IF JUSTIFIED)
- If STEP 1 shows no signal but you have concrete hypothesis for regime-dependent effect (e.g., funding regime split), pre-register a new experiment ID before any outcome inspection and test narrowly. Do not grid-search.
- Do not build trading/risk overlay. Remains ineligible.

#### STEP 4: DURABLE HANDOFF UPDATE (MANDATORY)
Update `AGENT_HANDOFF.md` with exact next task, commands to verify, and summary of changes. Update `experiment_frontier.json` and relevant registries. Run tests: `python -m unittest discover -s tests -v`. Commit nothing unnecessarily.

### HARD CONSTRAINTS
- No credentials/manual inputs. No workflow changes without explicit maintainer auth. No trading. Track separation enforced. Pre-register before holdout inspection. Preserve negative results.

### SUCCESS CRITERIA
Significant progress = stronger decision-grade evidence on liquidation risk (Track A or improved Track B inference) OR irrefutable structural block with concrete executable next route.

**START NOW. DO HEAVY WORK ON LIQUIDATION RISK.**
