# AGENT_HANDOFF.md (SINGLE DURABLE SOURCE OF TRUTH)

**TIMESTAMP:** 20261103T100500Z
**REPO:** Funding-conditioned-volatility-and-liquidation-risk
**PRIORITY (by repo name):** BOTH TRACKS ACTIVE. Track A (observed liquidations, funding-conditioned liquidation risk) = STRUCTURAL BLOCK (monitor-only). Track B (funding-conditioned volatility) = UNBLOCKED HEAVY CAMPAIGN. BOTH are core to repo name - do not neglect either.

## SESSION GOAL
Remove bottlenecks. Track A cannot proceed without new rubric-GO data (ironflow forward 404 through 2027-02). The bottleneck preventing new confirmatory Track B work is the FCLR-002 test split only having 2 non-overlapping 30-day blocks (<3 required). **Do NOT wait for perfect conditions.** Convert exploratory capacity into heavy evidence that can either (1) justify a new confirmatory split if structure exists elsewhere, or (2) produce a concrete pre-registration that meets protocol requirements. Never idle. Never re-run sealed FCLR-001..008.

## CRYSTAL-CLEAR INITIAL TASK (EXECUTE IMMEDIATELY, IN THIS ORDER)

```bash
# PHASE 1: VERIFY STATE (< 2 min) - MUST PASS
python scripts/monitor_ironflow_liquidations.py --quick
python scripts/monitor_ironflow_liquidations.py --verify
python -m unittest discover -s tests -v | tail -2   # MUST stay >=117/117 PASS

# PHASE 2: HEAVY WORK - FUNDING-CONDITIONED DEEP DIVE (PRIORITY - CANNOT SKIP)
# On frozen FCLR-002 splits ONLY (research_state/data_cache/fclr002_panel.json). Do NOT touch sealed panels.
# Goal: Understand funding-conditioning mechanism deeply enough to either expand to new confirmatory cell or harden existing results.

# 2a. Feature ablations (heavy)
# Drop each extended feature group individually (fund pct/z, RV ratios, price-disloc)
# Measure C2 vs B1 delta+CI (block=24, 2000 reps). Track if any single group kills improvement.
# Use: src/volatility/feature_engineering.py, src/volatility/block_bootstrap.py, scripts/run_stream_b_feature_extension.py

# 2b. Funding-conditioning interactions (heavy)
# Test fund×RV, fund×disloc, fund×RV regime interactions
# Keep train-only normalization, chronological splits, purge/embargo (leakage-resistant)

# 2c. Funding regime conditioning (heavy)
# Stratify by funding regime quartiles on TEST set only (descriptive, no re-split)
# Also test vol regime conditioning. Look for heterogeneity that explains mechanism.

# 2d. Cross-symbol stability (heavy)
# LOSO analysis already done, but dig deeper - coefficient stability, sign consistency
# Identify if funding effect is concentrated in specific symbols/regimes

# Output: research_state/evaluation_summary_STREAM_B_DEEP_ANALYSIS-001_<UTC>.md
# Include: tables of ablations, interaction coefficients, regime stratification, mechanism narrative

# PHASE 3: BOTTLENECK REMOVAL - FIND PATH TO CONFIRMATORY CELL (HEAVY)
# Blocker: FCLR-002 test has only 2 blocks. Need >=3.
# Actions:
# 1. Scan all cached panels for any configuration with >=5 symbols, >=3 non-overlapping 30-day blocks
# 2. Check if unsealed data has structure meeting criteria (without peeking at outcomes until pre-reg)
# 3. If found, DRAFT pre-registration (research_state/pre_registration_stream_b_funding_conditioned_*.md)
#    with full protocol details - DO NOT EXECUTE until split freeze documented
# 4. If NOT found, produce concrete analysis showing why impossible + alternative validation approach

# PHASE 4: TRACK A KEEP-ALIVE + AUTOMATION HARDENING (< 5 min)
# Strengthen monitor to catch 404->200 flip faster
# Ensure automation can resume instantly if data appears
# Evidence in research_state/ if improved

# PHASE 5: UPDATE HANDOFF (MANDATORY)
# Update AGENT_HANDOFF.md + research_state/experiment_frontier.json
# Record: bottlenecks removed, findings, next highest-value HEAVY task
# Make next session unable to avoid heavy work
```

## VERIFIED TRUTH (20261103T100500Z)
- **Track A (observed liquidations / funding-conditioned liquidation risk):** BLOCKED_ON_DATA (STRUCTURAL). Ironflow cached through 2026-10 intact. Forward 2026-11,12,2027-01,02 all 404; resume_trigger_met=false. FCLR-010 COMPLETE/PASSED (sealed). No admissible unauthenticated source. Sole reopen = NEW rubric-GO source (>=5 symbols, >=1 complete month OR >=3 non-overlapping 30-day blocks, documented completeness/coverage/license OK, unauthenticated only, schema compatible with frozen FCLR-010). Monitor-only.
- **Track B (funding-conditioned volatility):** STREAM_B_HEAVY_FEATURE_EXTENSION-001: C2 vs B1 +4.588% rel QLIKE, CI excludes zero. STREAM_B_ROBUSTNESS-002 COMPLETE: block sizes {12,24,48}, LOSO all symbols, scaling variants (robust/median-IQR/minmax), coef ±50% - ALL show consistent improvement with CIs excluding zero on frozen FCLR-002 splits (117/117 PASS). **BOTTLENECK:** FCLR-002 test split has only 2 non-overlapping 30-day blocks (<3 required for new confirmatory cell per protocol). Cannot run new confirmatory without meeting criteria.
- **Overlay:** INELIGIBLE. Microstructure D1-D3 tested (FCLR-LIQMICRO-002/003) - no H001 reversal.

## BOTTLENECKS REMOVED
1. Idle-wait eliminated - Track A monitor-only; 100% heavy work on Track B when blocked.
2. Shallow analysis eliminated - robustness across multiple dimensions complete.
3. Sealed-panel re-runs eliminated - frozen FCLR-002 splits only.
4. Unverifiable GO eliminated - strict rubric enforced.
5. **NEW:** Bottleneck of "only 2 blocks" now converted to explicit investigation task - must find alternative path or justify.

## REMAINING BOTTLENECKS
1. Track A data availability (structural, outside repo control) - only monitor + automation.
2. FCLR-002 test split has only 2 non-overlapping 30-day blocks (<3 required for new confirmatory cell per protocol). **MUST RESOLVE**: either find config meeting >=3 blocks on frozen/cached data, or produce detailed analysis showing impossibility + alternative validation that satisfies scientific rigor.

## FOCUS CAMPAIGN
**FUNDING_CONDITIONED_DEEP_DIVE-001 (HEAVY, MANDATORY):** Deepen understanding of funding-conditioning mechanism. This is core to repo name. Ablations, interactions, regime conditioning on frozen FCLR-002 splits. Simultaneously hunt for any cached panel meeting >=3 blocks. If funding effect is robust and path to confirmatory cell exists, draft pre-reg. If not, produce mechanism paper-quality analysis. This work CANNOT be avoided.

## MANDATORY DELIVERABLES THIS SESSION
- [ ] `python -m unittest discover -s tests -v` passes (117+)
- [ ] Track A keep-alive evidence (monitor --quick + --verify, <2 min)
- [ ] STREAM_B_DEEP_ANALYSIS-001 executed with ablations/interactions/regime analysis + cross-symbol stability
- [ ] **BOTTLENECK REPORT:** Explicit analysis of block-count issue - checked all cached panels for >=3 blocks config
- [ ] `research_state/evaluation_summary_STREAM_B_DEEP_ANALYSIS-001_<UTC>.md` written (comprehensive, mechanism-focused)
- [ ] If >=3-block config found: `research_state/pre_registration_stream_b_funding_conditioned_<UTC>.md` drafted (NOT executed). If not found: `research_state/block_count_resolution_001_<UTC>.md` explaining why and alternative validation
- [ ] AGENT_HANDOFF.md and research_state/experiment_frontier.json updated with successor task
- [ ] Evidence of heavy compute (block bootstraps 2000 reps, multiple ablations) recorded

## CRITICAL RULES
- Research only. No trading/paper/live/API orders. No credentials. Unauthenticated only.
- No .github/workflows changes.
- Modeled breaches != observed liquidations.
- Leakage-resistant: chronological splits, train-only normalization, purge/embargo.
- Never re-run sealed/exhausted confirmatory panels (FCLR-001..008). Fresh experiment ID only if protocol criteria met (>=5 symbols, >=3 blocks).
- **HEAVY WORK ALWAYS WHEN BLOCKED. NEVER IDLE.** Both tracks matter - funding conditions both volatility and liquidation risk.
- Do not peek at outcomes before pre-registration if creating new confirmatory cell.

## NEXT SESSION'S SINGLE HIGHEST-VALUE TASK
**HEAVY:** Based on this session's bottleneck report and deep analysis, either (a) execute pre-registered confirmatory cell if >=3 blocks found and pre-reg complete, OR (b) continue mechanism deepening with alternative validation approaches. Continue Track A monitor (<2 min). Keep all tests green. Focus relentlessly on funding-conditioning mechanism - it's the core of this repo. Do NOT do shallow analysis. Do NOT wait.
