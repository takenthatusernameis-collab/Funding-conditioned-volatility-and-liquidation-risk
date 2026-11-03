# AGENT_HANDOFF.md (SINGLE DURABLE SOURCE OF TRUTH)

**TIMESTAMP:** 20261103T050500Z
**REPO:** Funding-conditioned-volatility-and-liquidation-risk
**PRIORITY:** Track A liquidation forward-validation (IRONFLOW) — BLOCKED_ON_DATA (STRUCTURAL); CONTINUOUS HEAVY CAMPAIGN - eliminate bottlenecks, force forward progress.
**CAMPAIGN:** LIQUIDATION_FORWARD_VALIDATE_HEAVY-004j — BLOCKED_ON_DATA (HEAVY-WORK-CONTINUOUS)

## SESSION GOAL FOR NEXT AGENT
DO NOT COAST. Data path is structurally blocked on Ironflow forward edge (2026-11..2027-02 all 404, consecutive_absent>=3, data_through 2026-10). All prior sources NO-GO under strict FCLR rubric. 12 REVIEW_REQUIRED sources need deep verification. MANDATORY HEAVY WORK A-F. Primary mission: remove bottlenecks and maximize heavy execution across BOTH tracks (A - liquidation forward validation; B - volatility forecasting with available data). Never wait idle - always have parallel heavy workstreams running.

## CLEAR INITIAL TASK (EXECUTE IN ORDER - START NOW)
```bash
# 1) Verify current state
python scripts/monitor_ironflow_liquidations.py --verify
python scripts/monitor_ironflow_liquidations.py --quick
python scripts/monitor_ironflow_liquidations.py --decision
python scripts/monitor_ironflow_liquidations.py --scan

# 2) Hunt alternatives
python scripts/hunt_alternative_liquidation_sources.py

# 3) Validate framework
python scripts/verify_heavy_work_004i.py
python -m unittest discover -s tests -v

# 4) Review state
cat research_state/AGENT_HANDOFF.md
ls -lt research_state/alt_source_scan_*.json | head -2
cat research_state/experiment_frontier.json | head -120
```

## VERIFIED BASELINE (20261103T050500Z)
- **Ironflow**: cached through 2026-10 intact. Forward 2026-11,12,2027-01,02 all 404 (consec_absent=3). Baseline drift intact. content_hash_complete=True.
- **Tests**: 111/111 PASS (13.847s)
- **verify_heavy_work_004i**: ALL CHECKS PASSED
- **Alt hunt**: 12 REVIEW_REQUIRED identified, 0 GO, multiple NO-GO. Needs deep rubric verification.
- **Codebase**: Rich infrastructure - scripts/, src/, tests/ all present. Data directories have extensive BTC/ETH/SOL/XRP klines, funding rates, index/mark/premium prices (Jan-Mar 2024). RESEARCH_PROMPT.md has full protocol.

## MANDATORY HEAVY WORK (PARALLEL STREAMS)

### STREAM A: Ironflow/Data Acquisition (BLOCKED - but aggressive monitoring)
- [ ] **A1)** Enhance ironflow monitoring - add faster cadence logic, diff detection, any change alerts
- [ ] **A2)** Deep-verify each REVIEW_REQUIRED from alt scans against FCLR rubric (unauthenticated, >=5 symbols or broad coverage, >=1 full month OR >=3x30d blocks, schema compatible with liquidation events/fills, no keys/signed/requester-pays, license OK)
- [ ] **A3)** Expand hunt to new surfaces (IPFS/Arweave, academic repos, public archives, data commons) without credentials
- [ ] **A4)** For any promising candidate, write concrete probe script + tests, validate strictly

### STREAM B: Volatility Forecasting Track (UNBLOCKED - HEAVY EXECUTION)
- [ ] **B1)** Build/complete feature engineering pipeline using available data (klines 1h, funding rates, mark/index/premium). All 4 symbols Jan-Mar 2024 present.
- [ ] **B2)** Implement leakage-resistant chronological split, frozen protocol per RESEARCH_PROMPT
- [ ] **B3)** Baseline: realized-vol-only forecast. Add funding + price features. Compare rigorously.
- [ ] **B4)** Run full evaluation suite, document results in research_state/
- [ ] **B5)** Create reusable, tested modules in src/ with unit tests

### STREAM C: Infrastructure/Testing (PARALLEL)
- [ ] **C1)** Strengthen tests - add regression tests for ironflow monitoring, alt-hunt logic
- [ ] **C2)** Improve data pipeline robustness, caching, checkpointing
- [ ] **C3)** Update research_state artifacts (run_manifest, hypothesis_registry, etc.) with current state
- [ ] **C4)** Keep all tests green, add new tests for new functionality

### STREAM D: Documentation/Continuity (PARALLEL)
- [ ] **D1)** Fresh blocker evidence doc with commands/outputs/timestamps
- [ ] **D2)** Update experiment_frontier.json with concrete resume triggers and next actions
- [ ] **D3)** Update THIS handoff with precise next task for successor
- [ ] **D4)** Ensure AGENT_HANDOFF.md in research_state/ and root both current

## RESUME CONDITIONS (AUTO-TRIGGER)
1. **Ironflow**: YYYY-MM >= 2026-11 returns 200 on unauthenticated probe AND contains liquidation events/fills with compatible schema
2. **Alt source**: New admissible unauthenticated source passing full FCLR rubric (>=5 symbols OR equivalent coverage, >=1 complete month OR >=3 non-overlapping 30-day blocks, completeness/coverage/license acceptable, no keys/signed/requester-pays, schema mappable to FCLR-010 liquidation events/fills)

## BOTTLENECKS TO ELIMINATE
- Avoid idle time waiting for data - split effort across A and B tracks constantly
- Deep-verify REVIEW_REQUIRED properly (don't just list them)
- Build Track B to production quality even while Track A blocked
- Make everything resumable, tested, checkpointed
- Remove any manual steps, ensure fully automated

## ARTIFACTS TO LEAVE BEHIND (MANDATORY)
- [ ] Fresh blocker evidence: `research_state/blocker_evidence_YYYYMMDDTHHMMSSZ.md` with full command outputs
- [ ] Updated ironflow probe history scan
- [ ] Deep review notes for all REVIEW_REQUIRED with pass/fail + evidence
- [ ] Track B progress: working pipeline, baseline results, tests
- [ ] `research_state/experiment_frontier.json` refreshed with concrete actions
- [ ] Updated `AGENT_HANDOFF.md` (root) with crystal-clear next task
- [ ] All tests passing (maintain 111+)
- [ ] `research_state/run_manifest.json` updated

## CRITICAL NOTES
- Repository has MASSIVE data already present (klines, funding, index/mark/premium for BTC/ETH/SOL/XRP Jan-Mar 2024). Track B is fully viable NOW.
- Don't conflate funding-correction time with liquidation prediction per paper - follow RESEARCH_PROMPT strictly
- Chronological splits only, freeze protocol before holdout, preserve negative results
- No trading simulation/order placement
- Everything must be automatable without credentials
