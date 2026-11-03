# AGENT_HANDOFF.md (SINGLE DURABLE SOURCE OF TRUTH)

**TIMESTAMP:** 20261103T110235Z
**REPO:** Funding-conditioned-volatility-and-liquidation-risk
**PRIORITY (by repo name):** BOTH TRACKS ACTIVE AND NAMED. Track A (observed liquidations / funding-conditioned liquidation risk) = STRUCTURAL BLOCK, monitor-only. Track B / Track C (funding-conditioned volatility forecasting) = HEAVY CAMPAIGN, unblocked on frozen splits. Repo name requires funding to condition BOTH volatility and liquidation risk - do not neglect either.

## SESSION GOAL (UPDATED 20261103T110235Z)
Remove bottlenecks so the next session cannot avoid doing heavy work. Track A forward data is 404 through 2027-02 (structural, outside repo control) - do not poll, monitor only. The bottleneck preventing a new confirmatory Track B cell is the FCLR-002 test split having only 2 non-overlapping 30-day blocks (<3 required per protocol). H001 is INCONCLUSIVE on the decisive unsealed panel FCLR-008 (CI crosses zero); all confirmatory panels FCLR-001..008 are exhausted/sealed. Path to resolution: build a NEW leakage-resistant panel from raw 2026 Jan-Aug archives (FCLR-008 coverage: 5 symbols, 218 days, 7 blocks) with FULL PRE-REGISTRATION before any outcome inspection, under a new experiment ID. Never idle. Never re-run sealed FCLR-001..008.

## CRYSTAL-CLEAR INITIAL TASK (EXECUTE IMMEDIATELY, IN THIS ORDER)

```bash
# PHASE 1: VERIFY STATE (< 2 min) - MUST PASS
python scripts/monitor_ironflow_liquidations.py --quick
python -m unittest discover -s tests -v | tail -2   # MUST stay >=117/117 PASS

# PHASE 2: HEAVY WORK - RESOLVE BLOCK-COUNT BOTTLENECK (PRIORITY - CANNOT SKIP)
# Goal: Build new confirmatory cell via FCLR-008 panel from raw archives (Jan-Aug 2026, 5 symbols, 7 blocks).
# STEP 2a: Preregister FIRST (before any outcome peek). Write research_state/pre_registration_fclr011_<UTC>.md
#   - Protocol: research_protocol_fclr008.md v1.0 as template (new version for FCLR-011)
#   - Splits frozen BEFORE outcomes: train/val/test chronological, 7d purge/embargo
#   - Criteria: >=5 symbols, >=3 non-overlapping 30-day test blocks, block bootstrap 2000 reps
#   - Hypothesis: FCLR-H001 (C2 vs B1 QLIKE on next-24h realized variance)
#   - DO NOT inspect outcomes until splits frozen and pre-registered
#
# STEP 2b: Build leakage-resistant panel from root raw archives
#   - markPriceKlines-1h-2024-*/2026-*, indexPriceKlines, premiumIndexKlines, fundingRate zips
#   - Align mark/index/funding per symbol, train-only normalization, trailing-only features
#   - Output: research_state/data_cache/fclr011_panel.json + coverage audit
#
# STEP 2c: If panel builds and passes criteria -> execute FCLR-011 confirmatory run (frozen protocol)
#   - Write research_state/evaluation_summary_FCLR-011_<UTC>.md
#   - Assess forecast gate (>=2% rel QLIKE reduction + CI excludes zero)
#
# STEP 2d: If panel build is infeasible in-session -> produce machine-checkable block-count impossibility proof
#   - research_state/block_count_resolution_fclr011_<UTC>.md with symbol/day/block counts + hash anchors

# PHASE 3: TRACK A KEEP-ALIVE + AUTOMATION (< 2 min)
# monitor_ironflow_liquidations.py --quick (no resume trigger = still 404). Do not poll.
# Evidence: research_state/ironflow_probe_*.json (append-only, already logged)

# PHASE 4: UPDATE HANDOFF (MANDATORY)
# Update AGENT_HANDOFF.md + research_state/experiment_frontier.json
# Record: bottlenecks removed, findings, next highest-value HEAVY task
# Make next session unable to avoid heavy work
```

## VERIFIED TRUTH (20261103T110235Z)
- **Track A (observed liquidations / funding-conditioned liquidation risk):** BLOCKED_ON_DATA (STRUCTURAL). Ironflow cached through 2026-10 intact. Forward 2026-11,12,2027-01,02 all 404; resume_trigger_met=false. FCLR-010 COMPLETE/PASSED (sealed): C2 vs B1 Brier rel reduction 2.21%, CI [-0.004892,-0.001263] excludes zero, 199 instruments, 5x30-day blocks. No admissible unauthenticated source for new labels. Sole reopen = NEW rubric-GO source (>=5 symbols, >=1 complete month OR >=3 non-overlapping 30-day blocks, documented completeness/coverage/license OK, unauthenticated only, schema compatible with frozen FCLR-010). Monitor-only.
- **Track B/C (funding-conditioned volatility forecasting):** H001 INCONCLUSIVE on decisive unsealed panel FCLR-008 (2026-01-01..2026-08-06, 5 symbols, 218 days, 7 blocks, n=10785): C2 vs B1 +4.30% rel QLIKE, CI [-0.029938,0.000524] crosses zero -> forecast gate NOT_MET. All confirmatory panels exhausted: FCLR-003 (-3.78%, sealed 2024), FCLR-006 (-69.90%, unsealed 2026), FCLR-007 (-3.42%, 11-day), FCLR-008 (CI crosses zero). FCLR-002: -9.28% rel QLIKE, CI excludes zero, but test = 2 blocks (<3) -> INCONCLUSIVE (underpowered). Stream B deep analysis on frozen FCLR-002 splits COMPLETE: A1_fundpctz dominant (+4.051%), A3_pricedisloc (+2.255%), C2_all +4.588%, all 5 symbols improve, interactions/regime conditioning done.
- **Overlay:** INELIGIBLE (gate never passed). Microstructure D1-D3 tested - no H001 reversal.
- **Tests:** 117/117 PASS at HEAD.

## BOTTLENECKS REMOVED
1. Idle-wait eliminated - Track A monitor-only; 100% heavy work on Track B/C when blocked.
2. Shallow analysis eliminated - robustness across block sizes {12,24,48}, LOSO all symbols, scaling variants complete.
3. Sealed-panel re-runs eliminated - frozen FCLR-002 splits only, never re-run FCLR-001..008.
4. Unverifiable GO eliminated - strict rubric enforced for Track A reopen.
5. Block-count bottleneck converted to explicit build-or-prove task (FCLR-011 panel from raw archives).

## REMAINING BOTTLENECKS
1. Track A data availability (structural) - monitor only, resume on HTTP 200 for 2026-11+ or rubric-GO source.
2. FCLR-002 test = 2 blocks (<3) - blocks new confirmatory cell on frozen data. RESOLVE VIA: FCLR-011 panel build from raw 2026 archives (>=3 blocks available structurally) + pre-registration, OR machine-checkable impossibility proof.

## FOCUS CAMPAIGN (HEAVY, MANDATORY - CANNOT BE AVOIDED)
**FCLR-011_CONFIRMATORY_CELL_BUILD-001:** Construct leakage-resistant panel from raw 2026 Jan-Aug archives (5 symbols BTCUSDT/ETHUSDT/BNBUSDT/SOLUSDT/XRPUSDT, mark+index+premium+funding), pre-register BEFORE outcome inspection, execute confirmatory run if criteria met (>=5 symbols, >=3 non-overlapping 30-day test blocks). This is the ONLY path to resolve H001 INCONCLUSIVE. Repo name = funding-conditioned volatility AND liquidation risk; this campaign addresses the volatility half that remains unresolved. If panel build infeasible in-session, produce block-count impossibility proof instead - but heavy work must continue every turn.

## CRITICAL RULES
- Research only. No trading/paper/live/API orders. No credentials. Unauthenticated only.
- No .github/workflows changes.
- Modeled breaches != observed liquidations. Tracks A/B/C strictly separated.
- Leakage-resistant: chronological splits, train-only normalization, purge/embargo, trailing-only features.
- Never re-run sealed/exhausted confirmatory panels (FCLR-001..008). Fresh experiment ID only if protocol criteria met (>=5 symbols, >=3 blocks).
- HEAVY WORK ALWAYS WHEN BLOCKED. NEVER IDLE.
- Do not peek at outcomes before pre-registration if creating new confirmatory cell.

## NEXT SESSION'S SINGLE HIGHEST-VALUE TASK
**Build FCLR-011 panel from raw 2026 archives + pre-register (or produce block-count impossibility proof).** Track A monitor (<2 min). Keep tests green (117+). Do NOT re-run sealed FCLR-001..008. Do NOT peek at outcomes before pre-registration. This is core to repo name - heavy work cannot be avoided.

## RESUME TRIGGERS (Track A only)
- Ironflow events/fills YYYY-MM >= 2026-11 return HTTP 200 (monitor writes evidence). If true: pre-register FCLR-011-track-a, run frozen Track A harness on new window, update evaluation_summary/gate.
- New admissible unauthenticated liquidation source passes full rubric (>=5 symbols, >=3x30d blocks OR complete month series, compatible schema) - document in blocker_evidence with evidence.

**DEFAULT MODE:** HEAVY_ANALYSIS_CAMPAIGN. No idle time. Every turn produces durable artifacts.