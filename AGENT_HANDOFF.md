# AGENT HANDOFF — SINGLE DURABLE HANDOFF (LIQUIDATION-RISK CAMPAIGN)

UPDATED: 2026-10-30T20:30:02Z
HEAD: (current)
REPO: Funding-conditioned-volatility-and-liquidation-risk
PRIORITY_SOURCE: Repository name inference (funding-conditioned **volatility and liquidation risk**)
DURABLE_HANDOFF: SINGLE_SOURCE_OF_TRUTH
SESSION_GOAL: LIQUIDATION_RISK_HEAVY_CAMPAIGN

## INITIAL TASK MESSAGE FOR THE NEXT AGENTIC WORK SESSION (COPY AND EXECUTE THIS VERBATIM)

**TASK_ID:** `HND-20261030-LIQUIDATION-RISK-002`
**PRIORITY:** P0
**MODE:** HEAVY RESEARCH + ENGINEERING. NO VERIFICATION-ONLY CLOSURE. NO STATUS-POLISHING. NO EASY OUTS.

You are continuing from this single handoff. The repository name prioritizes **liquidation risk**. H001 (volatility forecast) is sealed negative (FCLR-003/FCLR-006). Track A (observed liquidation labels) is structurally blocked/exhausted for all admissible 2024 sources (binance public archive liquidationSnapshot/forceOrders probe showed 404/451; no other admissible free sources found). The only remaining liquidation-risk evidence path is **Track B** (modeled boundary breaches) — **FCLR-H003-EXT-001**. Complete decision-grade inference or produce an irrefutable structural block.

### COMPLETED (baseline)
- FCLR-H003-EXT-001 extended grid executed on unsealed 2026 panel (BTCUSDT/ETHUSDT/BNBUSDT/SOLUSDT/XRPUSDT). Horizons 72h/168h, MMR 0.004/0.005, lev 5x/10x, long/short separate. Artifacts: `research_state/protocol_FCLR-H003-EXT-001.md`, `research_state/evaluation_summary_FCLR-H003-EXT-001.md`. Scripts: `scripts/run_h003_ext.py`, `scripts/run_h003_ext_fast.py`.
- Preliminary results show C1/C2 generally do not improve over RV-only (B0) for modeled boundary breaches; most cells low base rate.
- Inference scaffolding added: `scripts/run_h003_ext_inference.py` (full) and `scripts/run_h003_ext_inference_fast.py` (reduced B) to add block bootstrap/LOO/Holm/calibration/intensity reporting.

### MANDATORY HEAVY TASKS (DO IN ORDER)

#### STEP 1: COMPLETE INFERENCE FOR FCLR-H003-EXT-001 (P0 — BLOCKING)
Produce decision-grade inference on Track B:
1. Generate prediction cache if missing: run `python scripts/run_h003_ext_inference.py` (or `run_h003_ext_inference_fast.py`). If it times out, debug to make it run to completion with deterministic seed 12345.
2. Block bootstrap >=2000 replicates (or >=500 with justification) resampling complete (sym,date) blocks; report 95% CIs for C2 vs B0 (ΔBrier = B0-C2, positive=C2 better).
3. Leave-one-symbol-out stability across all 5 symbols.
4. Holm correction across declared family (horizons×MMR×lev×sides = 16 contrasts). Report raw and adjusted p-values.
5. Calibration: reliability bins where base rates permit (focus on lev10 short).
6. Intensity target: scan `research_state/data_cache/` for OI/volume/quoteVolume/openInterest. If none, document explicit coverage limits — do not fabricate.
7. Append "Inference" section to `research_state/evaluation_summary_FCLR-H003-EXT-001.md` with all above. Update manifest if needed.
8. Verify: `python -m unittest discover -s tests -v` passes.

#### STEP 2: REMOVE TRACK A BOTTLENECK (P0 — DOCUMENT OR FIND)
1. Search for any liquidation/forceOrder files: `find research_state data_cache -name '*liquidat*' -o -name '*forceOrder*' -o -name '*liquidationSnapshot*'` (and repo root).
2. Re-check admissible free sources quickly (binance public archive paths, GitHub/Zenodo/HF) — unauthenticated only. Do not use paid/signup/API keys.
3. If viable sample found (>=several days, >=2 symbols, defensible provenance), pre-register tiny pilot before inspection and run. Else produce irrefutable structural block with exact sources tested, evidence, and single materially different free route with concrete requirements.

#### STEP 3: DURABLE HANDOFF UPDATE (MANDATORY)
Update this file with exact commands, summary of changes, update `research_state/experiment_frontier.json` and `research_state/hypothesis_registry.json` as appropriate. Commit nothing unnecessarily.

### HARD CONSTRAINTS
- No credentials/manual inputs. No workflow changes without explicit maintainer auth. No trading/paper trading. Track separation strictly enforced.
- Do not re-run sealed FCLR-001/002/003/005/006 gates. Do not tune on holdouts. No .github/workflows/* changes.
- Pre-register before inspecting holdout outcomes. Preserve negative/inconclusive results. No threshold-shopping.

### SUCCESS CRITERIA
Significant progress = **decision-grade evidence on liquidation risk (Track B)** with block-bootstrap CIs, LOO, Holm, calibration, intensity or documented limits **OR irrefutable structural block** for Track A with concrete next route.

**START NOW. DO HEAVY WORK ON LIQUIDATION RISK TRACK B INFERENCE.**
