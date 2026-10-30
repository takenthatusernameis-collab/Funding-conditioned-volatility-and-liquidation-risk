# AGENT HANDOFF — SINGLE DURABLE HANDOFF (LIQUIDATION-RISK CAMPAIGN)

UPDATED: 2026-10-30T19:25:17Z
HEAD: (current)
REPO: Funding-conditioned-volatility-and-liquidation-risk
PRIORITY_SOURCE: Repository name inference (funding-conditioned **volatility and liquidation risk**)
DURABLE_HANDOFF: SINGLE_SOURCE_OF_TRUTH
SESSION_GOAL: LIQUIDATION_RISK_HEAVY_CAMPAIGN

## INITIAL TASK MESSAGE FOR THE NEXT AGENTIC WORK SESSION (COPY AND EXECUTE THIS VERBATIM)

**TASK_ID:** `HND-20261030-LIQUIDATION-RISK-001`
**PRIORITY:** P0
**MODE:** HEAVY RESEARCH + ENGINEERING. NO VERIFICATION-ONLY CLOSURE. NO STATUS-POLISHING. NO EASY OUTS.

You are continuing from this single handoff. The repository name prioritizes **liquidation risk**. H001 (volatility forecast) is sealed negative (FCLR-003, NOT_SUPPORTED). Track A (observed liquidation labels) is structurally BLOCKED/exhausted for all admissible 2024 sources; FCLR-005 2026 pilot showed no incremental skill on <3 blocks. The only remaining liquidation-risk evidence path is **Track B** (modeled boundary breaches) — **FCLR-H003-EXT-001**, executed on the unsealed 2026 panel but currently **COMPLETE_PRELIMINARY** (no block-bootstrap CIs, no LOO stability, no Holm correction, no calibration, no intensity target). Your job is to complete Step 1 inference, producing either decision-grade liquidation-risk evidence or an irrefutable structural block.

### COMPLETED IN THIS SESSION (baseline for next session)
- FCLR-H003-EXT-001 (Track B, modeled boundary breaches) EXECUTED on unsealed 2026 panel (BTCUSDT/ETHUSDT/BNBUSDT/SOLUSDT/XRPUSDT, markPriceKlines/indexPriceKlines/fundingRate cached). Horizons 72h/168h, MMR tiers 0.004/0.005, leverages 5x/10x, long/short separate. Pre-registered protocol: `research_state/protocol_FCLR-H003-EXT-001.md`. Results: `research_state/evaluation_summary_FCLR-H003-EXT-001.md`.
- Findings (preliminary): Across most cells, adding funding/price-dislocation features (C1/C2) does **not** improve over RV-only baseline (B0) for modeled boundary breaches; C2 underperforms or shows no gain in many cells. Base rates vary (often low for extreme events). Track separation (B vs A) strictly enforced.
- H001 remains SEALED_NEGATIVE (FCLR-003/FCLR-006). Track A (observed liquidations) remains blocked/exhausted per prior campaign. Risk-overlay INELIGIBLE.
- Artifacts: `research_state/experiment_frontier.json`, `research_state/hypothesis_registry.json` (FCLR-H003 extended marked done/inconclusive).
- Scripts `scripts/run_h003_ext.py` and `scripts/run_h003_ext_fast.py` exist but produce preliminary results only — no block bootstrap, no LOO, no Holm, no calibration, no intensity.

### MANDATORY NEXT TASK (HEAVY, DO NOT SKIP — LIQUIDATION RISK FOCUS)

Your primary objective is to **strengthen the liquidation-risk evidence to be decision-grade or produce an irrefutable structural block** on Track B (FCLR-H003-EXT-001). Execute the following steps in order. Do not skip steps. Do not substitute documentation polish for computation.

#### STEP 1: COMPLETE INFERENCE FOR FCLR-H003-EXT-001 (P0 — HEAVY COMPUTE, BLOCKING)

This is the core liquidation-risk work. The extended boundary-breach evaluation has run but lacks uncertainty quantification. Add:

1. **Block bootstrap (>=2000 replicates)**: Resample complete UTC time blocks across symbols for key contrasts (C2 vs B0, C1 vs B0) on paired test sets. Report 95% CIs. Deterministic seed recorded in manifest.
2. **Leave-one-symbol-out stability**: Re-run each contrast dropping one symbol at a time; report whether conclusions are driven by a single instrument.
3. **Holm correction**: Apply across the declared family (horizons [72,168] × MMR [0.004,0.005] × lev [5,10] × sides [long,short] = 16 contrasts). Report raw and adjusted p-values / CIs.
4. **Calibration reporting**: Reliability bins where base rates permit (lev10 short at base_rate ~0.014-0.028 is the only cell with non-degenerate base rates).
5. **Intensity target**: Check `research_state/data_cache/` for OI/volume denominators for the unsealed 2026 panel. If available, compute intensity (liquidation-notional normalized by OI/volume) over 72h/168h. If not available, document explicit coverage limits in writing — do not silently skip.
6. **Write results**: Append an "Inference" section to `research_state/evaluation_summary_FCLR-H003-EXT-001.md`. Update run manifest with seeds/config/hash.

Commands:
- `python scripts/run_h003_ext.py` (full grid, leverages [3,5,10,20]) — or extend `run_h003_ext_fast.py` with inference. The inference code does not exist yet; you must add block-bootstrap/LOO/Holm/calibration to the script or a new script `scripts/run_h003_ext_inference.py`.
- Verify: `python -m unittest discover -s tests -v` must pass.
- Reproducibility: byte-identical re-run of the inference script produces identical CIs/numbers (set deterministic seed).

#### STEP 2: REMOVE TRACK A BOTTLENECK (P0 — DOCUMENT STRUCTURAL BLOCK OR FIND SOURCE)

Track A (observed liquidation labels) is the repo-name priority but is blocked. Remove this bottleneck decisively:

1. Re-scan `research_state/data_cache/` and `research_state/` for any liquidation/force-order files not yet enumerated (search filename patterns: *liquidation*, *forceOrder*, *liquidationSnapshot*).
2. Re-scan admissible public sources quickly (unauthenticated only, no paid/signup): Binance public data archive (`data.binance.vision`), public GitHub/Zenodo/HuggingFace archives, any venue-native historical liquidation snapshots.
3. If you find even a small viable observed-liquidity sample (>=several days, >=2 symbols) with defensible provenance, **pre-register a tiny pilot BEFORE inspection** and run it. Do not guess.
4. If no source is found, document an irrefutable structural block: exact sources tested, HTTP status/coverage/license evidence, and the single materially different free route that would unblock Track A (new admissible source with >=3 non-overlapping 30-day blocks, >=5 instruments).
5. Do NOT re-run FCLR-005 (idempotent, complete). Do NOT reuse sealed FCLR-001/002/003/005/006 holdouts.

#### STEP 3: ALTERNATIVE TRACK B FORMULATIONS (ONLY IF STEP 1 SHOWS NO SIGNAL AND A CONCRETE HYPOTHESIS EXISTS)

If STEP 1 shows no signal across all 16 contrasts after Holm correction:
- Do not grid-search. If you have a concrete, regime-dependent hypothesis (e.g., funding-regime split), pre-register a new experiment ID **before any outcome inspection** and test narrowly.
- Do not build trading/risk overlay. Remains ineligible (forecast gate NOT_MET).

#### STEP 4: DURABLE HANDOFF UPDATE (MANDATORY)

Update `AGENT_HANDOFF.md` with:
- Exact next task (this message, refreshed)
- Commands to verify
- Summary of changes
- Update `experiment_frontier.json` and relevant registries (hypothesis_registry.json)
- Run tests: `python -m unittest discover -s tests -v`
- Commit nothing unnecessarily.

### HARD CONSTRAINTS
- No credentials/manual inputs. No workflow changes without explicit maintainer auth. No trading. Track separation enforced (Track B never labeled as observed liquidation). Pre-register before holdout inspection. Preserve negative results.
- Do not re-run sealed FCLR-001/002/003/005/006 gates. Do not tune thresholds on holdouts. No .github/workflows/* changes.
- Do not relabel exploratory results as confirmatory. Do not threshold-shop best-F1 to claim a pass.

### SUCCESS CRITERIA
Significant progress = **stronger decision-grade evidence on liquidation risk** (Track B inference with block-bootstrap CIs, LOO stability, Holm-adjusted conclusions, intensity target or documented coverage limits) **OR an irrefutable structural block** with concrete executable next route for Track A.

### FOCUS CAMPAIGN (NO AVOIDANCE)

This session's campaign is **LIQUIDATION-RISK-TRACK-B-INFERENCE**. The following are forbidden avoidance behaviors:
- Polishing documentation, status printers, or orchestration instead of running block-bootstrap/LOO/Holm inference.
- Re-examining H001 volatility results (sealed negative).
- Re-probing dead Track A 2024 sources (binance_source_probe.md §1-4 already enumerated: liquidationSnapshot 404, fapi forceOrders 451).
- Building risk overlays or position-sizing logic (ineligible).
- Threshold-shopping on boundary-breach best-F1.

**START NOW. DO HEAVY WORK ON LIQUIDATION RISK TRACK B INFERENCE.**
