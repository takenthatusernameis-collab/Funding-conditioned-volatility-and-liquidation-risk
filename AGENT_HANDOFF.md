# AGENT_HANDOFF.md (SINGLE DURABLE SOURCE OF TRUTH)

**TIMESTAMP:** 20261103T100321Z
**REPO:** Funding-conditioned-volatility-and-liquidation-risk
**PRIORITY (by repo name):** BOTH TRACKS ACTIVE. Track A (observed liquidations) = STRUCTURAL BLOCK (monitor-only, heavy automation complete). Track B (funding-conditioned volatility) = HEAVY CAMPAIGN READY (STREAM_B_ROBUSTNESS-002 complete with consistent gains).

## SESSION GOAL
Remove bottlenecks. Track A cannot proceed without new rubric-GO data (ironflow forward 404 through 2027-02). All heavy Track B robustness done on frozen FCLR-002 splits. Next agent MUST do heavy work: expand Stream B analysis on frozen FCLR-002 splits (new ablations/feature combinations) or harden Track A detection automation. Do NOT idle. Do NOT re-run sealed FCLR-001..008.

## CRYSTAL-CLEAR INITIAL TASK (EXECUTE IMMEDIATELY, IN THIS ORDER)

```bash
# PHASE 1: VERIFY STATE (< 2 min)
python scripts/monitor_ironflow_liquidations.py --quick
python scripts/monitor_ironflow_liquidations.py --verify
python -m unittest discover -s tests -v | tail -2   # MUST stay >=117/117 PASS

# PHASE 2: HEAVY WORK - STREAM_B_DEEP_ANALYSIS-001 (PRIORITY)
# On frozen FCLR-002 splits (research_state/data_cache/fclr002_panel.json), do NOT touch sealed panels.
# Extend STREAM_B_ROBUSTNESS-002 findings:
# 1. Feature ablations: drop each extended feature group (fund pct/z, RV ratios, price-disloc) individually; measure C2 vs B1 delta+CI (block=24, 2000 reps)
# 2. Interaction tests: fund×RV, fund×disloc interactions; keep train-only normalization, chronological splits, purge/embargo
# 3. Regime conditioning: by vol regime / funding regime quartiles on test set (descriptive only, no re-split)
# 4. Model stability: check coefficient signs/magnitudes across LOSO and bootstraps
# Preserve leakage resistance. Write artifact: research_state/evaluation_summary_STREAM_B_DEEP_ANALYSIS-001_<UTC>.md
# Use: src/volatility/feature_engineering.py, src/volatility/block_bootstrap.py, scripts/run_stream_b_feature_extension.py

# PHASE 3: TRACK A HEAVY AUTOMATION (PARALLEL IF TIME, ELSE AFTER PHASE 2)
# Strengthen resume detection: ensure monitor scripts can catch 404->200 flip instantly.
# Add/extend tests for probe diff/resume trigger. Keep <10 min total for Track A automation.
# Evidence: update automation notes in research_state/ if improved.

# PHASE 4: UPDATE HANDOFF
# Write successor task to AGENT_HANDOFF.md + research_state/experiment_frontier.json
# Record key findings, next highest-value heavy task, bottlenecks removed/remaining
```

## VERIFIED TRUTH (20261103T100321Z)
- **Track A (observed liquidations):** BLOCKED_ON_DATA (STRUCTURAL). Ironflow cached through 2026-10 intact. Forward 2026-11,12,2027-01,02 all 404; resume_trigger_met=false. FCLR-010 COMPLETE/PASSED (sealed). No admissible unauthenticated source. Sole reopen = NEW rubric-GO source (>=5 symbols, >=1 complete month OR >=3 non-overlapping 30-day blocks, documented completeness/coverage/license OK, unauthenticated only, schema compatible with frozen FCLR-010).
- **Track B (funding-conditioned volatility):** STREAM_B_HEAVY_FEATURE_EXTENSION-001: C2 vs B1 +4.588% rel QLIKE, CI [-0.044418,-0.017603] excludes zero (117/117 PASS). STREAM_B_ROBUSTNESS-002 (COMPLETED 20261103T090636Z): block sizes {12,24,48}, LOSO all symbols, scaling variants (robust/median-IQR/minmax), coef ±50% - ALL show consistent improvement with CIs excluding zero on frozen FCLR-002 splits. No sealed panels re-run.
- **Overlay:** INELIGIBLE. Microstructure D1-D3 tested (FCLR-LIQMICRO-002/003) - no H001 reversal.

## BOTTLENECKS REMOVED
1. Idle-wait eliminated - Track A monitor-only; 100% heavy work on Track B when blocked.
2. Shallow analysis eliminated - robustness across multiple dimensions complete.
3. Sealed-panel re-runs eliminated - frozen FCLR-002 splits only.
4. Unverifiable GO eliminated - strict rubric enforced.

## REMAINING BOTTLENECKS
1. Track A data availability (structural, outside repo control) - only monitor + automation.
2. FCLR-002 test split has only 2 non-overlapping 30-day blocks (<3 required for new confirmatory cell per protocol). Cannot pre-register new confirmatory cell on current split without violating protocol. Must either (a) find configuration meeting >=3 blocks on frozen data, or (b) do heavy exploratory/robustness work that doesn't require new confirmatory cell.

## FOCUS CAMPAIGN
**STREAM_B_DEEP_ANALYSIS-001 (HEAVY, REQUIRED):** Deepen understanding of why extended features help. Ablations, interactions, regime conditioning on frozen FCLR-002 splits. This is heavy work that must be done regardless of explicit directions. If ablations show specific feature groups drive gains, document for future pre-registration. Keep tests green (117+). Do NOT re-run sealed FCLR-001..008.

## MANDATORY DELIVERABLES THIS SESSION
- [ ] `python -m unittest discover -s tests -v` passes (117+)
- [ ] Track A keep-alive evidence (monitor --quick + --verify, <1 min)
- [ ] STREAM_B_DEEP_ANALYSIS-001 executed with ablations/interactions/regime analysis
- [ ] `research_state/evaluation_summary_STREAM_B_DEEP_ANALYSIS-001_<UTC>.md` written
- [ ] AGENT_HANDOFF.md and research_state/experiment_frontier.json updated with successor task

## CRITICAL RULES
- Research only. No trading/paper/live/API orders. No credentials. Unauthenticated only.
- No .github/workflows changes.
- Modeled breaches != observed liquidations.
- Leakage-resistant: chronological splits, train-only normalization, purge/embargo.
- Never re-run sealed/exhausted confirmatory panels (FCLR-001..008). Fresh experiment ID only if protocol criteria met (>=5 symbols, >=3 blocks).
- Heavy work always when blocked. Never idle.

## NEXT SESSION'S SINGLE HIGHEST-VALUE TASK
**HEAVY:** Complete STREAM_B_DEEP_ANALYSIS-001 ablations/interactions on frozen FCLR-002 splits. If feature groups identified as key drivers with stable gains across LOSO/bootstraps, prepare a detailed pre-registration draft (research_state/pre_registration_stream_b_*.md) that would satisfy protocol criteria - but do NOT execute confirmatory run unless split structure meets >=3 blocks. Continue Track A monitor (<1 min). Keep all tests green. Do NOT re-run sealed panels.
