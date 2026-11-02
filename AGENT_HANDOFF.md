# AGENT_HANDOFF.md (DURABLE — SINGLE SOURCE OF TRUTH)
**TIMESTAMP (UTC):** 2026-11-02T03:05:25Z
**INITIAL TASK (NEXT SESSION):** EXECUTE CAMPAIGN FCLR-HEAVY-001 — Funding-conditioned liquidation-risk deepening (Track A operational hardening). START AT STEP 1 IMMEDIATELY. DO HEAVY WORK. Do not stop until ALL 6 steps produce artifacts + `python -m unittest discover -s tests -v` returns 27/27. NO confirmatory outcome inspection for sealed panels. Treat all outputs as hypothetical-only.
**REPO:** Funding-conditioned-volatility-and-liquidation-risk
**REPO PRIORITIZATION (INFERRED):** Funding-conditioned volatility → liquidation risk (name is directive). Priority order: (1) Track A operational hardening on frozen ironflow Hyperliquid census (gate PASSED, overlay EXECUTED) — exhaust this before anything else → (2) nothing else until heavy Track A analysis is fully exhausted. Track C sealed (NOT_SUPPORTED), Track B closed (CLOSED_NEGATIVE), H002 permanently blocked.
**BRANCH/HEAD:** main @ d7243ea2
**HANDOFF ID:** FCLR-HANDOFF-080-20261102T030525Z
**SUPERSEDES:** FCLR-HANDOFF-079-20261102T022615Z

## BOTTLENECKS REMOVED (this session)
- **State clean:** Tests 27/27 PASS. No workflow edits needed. No open forks. All discovery exhausted (FCLR-NEXT-002 COMPLETE_NO-GO).
- **Path unambiguous:** The only admissible Track A path (ironflow Hyperliquid census) is already exploited (FCLR-010 PASSED). The highest value left is deepening, not reopening.
- **Ambiguity eliminated:** FCLR-HEAVY-001 is NOT STARTED. No artifacts exist under `research_state/fclr_heavy001_*` or `results/fclr_heavy001/`. Step 1 is the immediate, unblocked action.
- **No dead-ends left open:** H001 inconclusive but not reopenable without new admissible data; Track B/C closed; H002 blocked. No parallel "discovery" loops to chase.

## STATUS (CURRENT - FROZEN)
- Track A (FCLR-010): GATE PASSED on Hyperliquid ironflow census (199 perps, Nov 2025–Oct 2026, 12 blocks). C2 vs B1 Brier rel -2.21%, CI [-0.004892,-0.001263] excludes zero. Overlay FCLR-OVERLAY-001 executed (HYPOTHETICAL ONLY). Splits frozen 2026-11-01T05:39:07Z.
- Track C (H001): NOT_SUPPORTED — CONFIRMATORY CLOSED.
- Track B (H003): CLOSED_NEGATIVE (extended grid no robust skill).
- H002: PERMANENT BLOCK (SSRN HTTP 403).
- FCLR-LIQMICRO-002/003 COMPLETE. No new admissible unauthenticated liquidation source found.

## CAMPAIGN FCLR-HEAVY-001 (HEAVY — future agents CANNOT avoid doing heavy working)
**OBJECTIVE:** Extract maximum admissible value from frozen Track A without crossing deployment/trading claims. All outputs hypothetical-only. No label merging across tracks. Every step must be executed with rigor; do not summarize away the work.

### EXECUTE IN ORDER (each step MANDATORY - produce artifacts or precise blocker + continue)
1. **Funding-liquidity coupling audit** (HEAVY)
   - Create: `research_state/fclr_heavy001_funding_liq_coupling.md`, `results/fclr_heavy001/coupling_summary.json`
   - Recompute funding-conditioned liquidation intensity using frozen FCLR-010 panel/splits. Quantify marginal contribution of funding_abs/signed funding deciles controlling for RV/vol proxies. Block bootstrap by time blocks (>=2000). Preserve nulls. No peeking.

2. **Regime stratification (adversarial)** (HEAVY)
   - Create: `research_state/fclr_heavy001_regime_strat.md`, `results/fclr_heavy001/regime_strat.json`
   - Stratify by realized vol terciles, funding regime (pos/neg/extreme), funding cycle/time-of-day if knowable. Report event counts, Brier/logloss, calibration, block-bootstrap CIs for C2 vs B1 per stratum. Flag thin strata (< threshold events) without imputing.

3. **Lead/lag & censoring robustness** (HEAVY)
   - Create: `research_state/fclr_heavy001_leadlag_censor.md`, `results/fclr_heavy001/leadlag_censor.json`
   - Test alternative lead windows/censoring consistent with frozen protocol. No re-tuning to holdout. Document any non-conforming rule changes as REJECTED if peeking required.

4. **Feature ablation hardening (funding-focused)** (HEAVY)
   - Create: `research_state/fclr_heavy001_ablation_funding.md`, `results/fclr_heavy001/ablation_funding.json`
   - Isolate funding alone vs RV-only vs combined; include funding sign/abs interactions. Same frozen splits/blocks/bootstrap. Report raw + Holm-adjusted across registered comparisons.

5. **Cross-symbol concentration & stability** (HEAVY)
   - Create: `research_state/fclr_heavy001_concentration.md`, `results/fclr_heavy001/concentration.json`
   - Leave-one-symbol-out, symbol-cluster stability. Identify concentration; if improvement driven by <20% symbols with wide CIs, call out instability explicitly.

6. **Reproducibility + integrity lock-in** (MANDATORY)
   - Re-verify sealed FCLR-010 artifacts untouched (hashes/mtimes). Write `research_state/fclr_heavy001_integrity.md`.
   - Run `python -m unittest discover -s tests -v` → must be 27/27.
   - Update `research_state/experiment_frontier.json` (FCLR-HEAVY-001 status per step) and append to `research_state/cross_track_decision_log.md`.

### ACCEPTANCE CRITERIA (HARD)
- All 6 steps produce artifacts. No step skipped.
- Tests: 27/27 PASS.
- No sealed panel modified. All new outputs under `results/fclr_heavy001/` and `research_state/fclr_heavy001_*.md/json`.
- Strictly hypothetical-only. No trading/paper/live claims. No label merging.
- If peeking/re-tuning sealed splits or unregistered comparisons required → STOP, document blocker in handoff/log, continue to next step if possible or report blocked with evidence.

## PARALLEL READINESS (NON-BLOCKING)
Keep `scripts/reopen_probe.py` functional per FCLR-REOPEN-READY-001. Only if NEW admissible unauthenticated liquidation source passes rubric (>=5 symbols, >=3 non-overlapping 30-day blocks, documented completeness, license OK) OR SSRN H002 accessible → pre-register new experiment BEFORE outcome inspection.

## HARD CONSTRAINTS
- NO Binance merge. NO reopening H001/FCLR-003/FCLR-008/FCLR-010 without trigger + pre-registration + split freeze.
- ALL 27 tests MUST PASS. NO changes to `.github/workflows/`.
- Only admissible: ironflow Hyperliquid liquidations + Hyperliquid fundingHistory API.
- Never silently zero missing funding — drop/flag with justification.
- Sealed artifacts unchanged. Track A/B/C never merged; modeled != observed.
- No risk-overlay promotion beyond hypothetical.

## SINGLE HIGHEST-VALUE NEXT TASK
**START NOW: CAMPAIGN FCLR-HEAVY-001 Step 1.** Do heavy, rigorous analysis on frozen Track A. Be exhaustive. Produce concrete artifacts future agents cannot ignore. If any subanalysis blocked by data, write precise evidence + smallest verifiable alternative and proceed. Do not idle. Do not pivot to closed tracks.
