# AGENT_HANDOFF.md (SINGLE DURABLE SOURCE OF TRUTH)

**TIMESTAMP:** 20261103T060500Z
**REPO:** Funding-conditioned-volatility-and-liquidation-risk
**PRIORITY:** BOTH TRACKS MANDATORY - Track A liquidation forward-validation (IRONFLOW BLOCKED_ON_DATA) + Track B volatility forecasting (UNBLOCKED) in parallel HEAVY CAMPAIGN
**CAMPAIGN:** LIQUIDATION_FCVR_HEAVY-005 - DUAL-TRACK MAXIMUM THROUGHPUT (NO IDLE TIME)

## SESSION GOAL FOR NEXT AGENT
DO NOT COAST. Ironflow forward edge structurally blocked (2026-11,12,2027-01,02 all 404; consec_absent>=3; data_through 2026-10). 12 REVIEW_REQUIRED sources need deep verification against strict FCLR rubric. Repository has MASSIVE unexploited data for Track B (BTC/ETH/SOL/XRP klines 1h, funding, mark/index/premium Jan-Mar 2024; also broader cached data).
MANDATE: Run BOTH tracks concurrently at all times. Every action must produce measurable progress. Eliminate bottlenecks. Never wait for data - build infrastructure, verify sources deeply, and advance Track B to production quality.

## CRYSTAL-CLEAR INITIAL TASK (EXECUTE IMMEDIATELY IN THIS ORDER)

```bash
# PHASE 1: VERIFY CURRENT STATE (5 min)
python scripts/monitor_ironflow_liquidations.py --verify
python scripts/monitor_ironflow_liquidations.py --quick
python scripts/monitor_ironflow_liquidations.py --decision
python -m unittest discover -s tests -v

# PHASE 2: ASSESS TRACK B READINESS (10 min)
ls data/ research_state/data_cache/ src/ scripts/ | head -40
find . -name "*feature*eng*" -not -path "*/__pycache__/*" | head -15
find . -name "*volatil*forecast*" -not -path "*/__pycache__/*" | head -15

# PHASE 3: DEEP REVIEW OF ALTERNATIVE SOURCES (START IN PARALLEL)
python scripts/hunt_alternative_liquidation_sources.py
# Then deep-verify each REVIEW_REQUIRED against FCLR rubric
```

## VERIFIED BASELINE (20261103T060500Z)
- **Ironflow (Track A):** Cached through 2026-10 intact (18 month pairs). Forward 2026-11,12,2027-01,02 all 404, consec_absent=3. Baseline drift intact, content_hash_complete=True. resume_trigger_met=false.
- **Tests:** 111/111 PASS (14.725s). verify_heavy_work_004i passes.
- **Alt hunt:** Multiple scans done; 12 REVIEW_REQUIRED identified, 0 GO, many NO-GO. Need DEEP rubric verification with concrete evidence.
- **Track B data:** BTC/ETH/SOL/XRP klines (1h), funding rates, mark/index/premium prices present for Jan-Mar 2024 + broader cache. Fully viable NOW.
- **Infrastructure:** Rich codebase (scripts/, src/, tests/, research_state/). All automation in place.

## DUAL-TRACK HEAVY WORKSTREAMS (RUN IN PARALLEL)

### STREAM A: LIQUIDATION DATA ACQUISITION (AGGRESSIVE - BLOCKED BUT NEVER IDLE)
- [ ] **A1) Ironflow monitoring hardening** - Enhance `scripts/monitor_ironflow_liquidations.py` with faster diff detection, probe history tracking, alerting logic. Add tests.
- [ ] **A2) DEEP-VERIFY all REVIEW_REQUIRED** - For each candidate from alt scans, apply full FCLR rubric: unauthenticated path exists, >=5 symbols OR broad coverage, >=1 complete month OR >=3x30d blocks, schema mappable to liquidation events/fills, no keys/signed/requester-pays, license OK. Document pass/fail with exact URLs, status codes, headers, body samples in `research_state/alt_source_deep_review_YYYYMMDDTHHMMSSZ.md`.
- [ ] **A3) Expand hunt aggressively** - Search IPFS/Arweave, academic repos (Zenodo/OSF), data commons, GitHub for liquidation datasets, HF beyond current. Test every plausible unauthenticated path. No credentials.
- [ ] **A4) Probe any promising candidate** - Write concrete probe script, test against rubric, add to tests if logic changes. Only GO if passes ALL criteria.
- [ ] **A5) Fresh blocker evidence** - Create `research_state/blocker_evidence_YYYYMMDDTHHMMSSZ.md` with ALL command outputs, timestamps, URLs probed.

### STREAM B: VOLATILITY FORECASTING (UNBLOCKED - BUILD TO PRODUCTION QUALITY NOW)
- [ ] **B1) Audit existing volatility/feature code** - Explore `src/`, find feature engineering, models, evaluation. Understand current state vs RESEARCH_PROMPT requirements.
- [ ] **B2) Build complete feature pipeline** - Implement funding-conditioned features (signed/abs funding, trailing percentiles, time-to-funding), RV features (6h/24h/7d, ratios), price-dislocation (premium/basis/mark-index, MA/EMA deviations). All trailing-only, no leakage.
- [ ] **B3) Leakage-resistant evaluation** - Chronological splits only, freeze protocol before holdout, purge/embargo horizons, normalize on train only. Follow RESEARCH_PROMPT strictly.
- [ ] **B4) Baselines + ablations** - Persistence, RV-only (HAR-style), RV+funding, RV+funding+price features. Compare rigorously with block bootstrap, proper metrics (QLIKE/MSE).
- [ ] **B5) Run full evaluation** - Execute on available data (Jan-Mar 2024 + cached), document in `research_state/evaluation_summary_VOLATILITY_YYYYMMDDTHHMMSSZ.md`. Create reusable modules in `src/` with unit tests.
- [ ] **B6) Extend to all available symbols/periods** - Maximize use of cached data across all venues/time ranges present.

### STREAM C: INFRASTRUCTURE & TESTING (PARALLEL HARDENING)
- [ ] **C1) Strengthen ironflow/alt-hunt tests** - Add regression tests for probe logic, diff detection, rubric validation.
- [ ] **C2) Pipeline robustness** - Improve caching, checkpointing, resume logic. Make everything restartable/idempotent.
- [ ] **C3) Update all research_state artifacts** - Refresh run_manifest.json, hypothesis_registry.json, experiment_frontier.json with current truth.
- [ ] **C4) Maintain test suite** - Keep ALL tests green (target >=111, add tests for new code). Run frequently.

### STREAM D: DOCUMENTATION & CONTINUITY (PARALLEL)
- [ ] **D1) Update experiment_frontier.json** - Reflect dual-track campaign, concrete next actions, accurate blockers/resume triggers.
- [ ] **D2) Update this AGENT_HANDOFF.md** - Leave crystal-clear next task for successor with specific commands and priorities.
- [ ] **D3) Create continuity artifacts** - Deep review notes, Track B progress doc, updated manifests. Ensure root and research_state copies consistent.
- [ ] **D4) Evidence trail** - Timestamp everything, document all probes/decisions with commands/outputs.

## BOTTLENECKS TO ELIMINATE IMMEDIATELY
1. **Idle waiting** - Split every session across A and B. If A blocked, B must run at full throttle.
2. **Shallow source review** - Deep-verify each REVIEW_REQUIRED with actual probing and rubric checks, not just reading JSON.
3. **Track B underutilized** - Repo has tons of data. Build production-quality pipeline NOW.
4. **Manual steps** - Automate everything. All scripts must be resumable/checkpointable.
5. **Stale artifacts** - Keep manifests/handoffs current in real-time.

## RESUME CONDITIONS (AUTO-TRIGGER FOR TRACK A)
1. **Ironflow**: YYYY-MM >= 2026-11 returns 200 on unauthenticated probe AND contains liquidation events/fills with schema compatible with FCLR-010 (Hyperliquid). Verify via `python scripts/monitor_ironflow_liquidations.py --quick`.
2. **Alt source**: New admissible unauthenticated source passing FULL rubric (>=5 symbols OR equivalent coverage, >=1 complete month OR >=3 non-overlapping 30-day blocks, completeness/coverage/license documented OK, no keys/signed/requester-pays, schema mappable to FCLR-010 liquidation events/fills).

## MANDATORY ARTIFACTS TO LEAVE BEHIND
- [ ] `research_state/blocker_evidence_YYYYMMDDTHHMMSSZ.md` - Fresh comprehensive blocker evidence
- [ ] `research_state/alt_source_deep_review_YYYYMMDDTHHMMSSZ.md` - Deep verification of ALL REVIEW_REQUIRED with pass/fail + evidence
- [ ] `research_state/volatility_track_progress_YYYYMMDDTHHMMSSZ.md` - Track B pipeline, baselines, results
- [ ] `research_state/evaluation_summary_VOLATILITY_*.md` - Concrete evaluation results if run
- [ ] Updated `research_state/experiment_frontier.json` - Accurate dual-track state
- [ ] Updated `AGENT_HANDOFF.md` (root) - Crystal-clear next task for successor
- [ ] Updated `research_state/run_manifest.json`, `research_state/hypothesis_registry.json` if changed
- [ ] All tests passing (>=111). Add tests for any new functionality.

## CRITICAL RULES
- **Follow RESEARCH_PROMPT strictly** - Chronological splits, freeze protocol before holdout, no leakage, separate tracks, preserve negative results
- **No trading** - Research only, never simulate/live/paper trade
- **No credentials** - Only unauthenticated public sources
- **No .github/workflows changes** - Protected
- **Track separation** - Don't conflate modeled boundary breaches with observed liquidations
- **Heavy work always** - If blocked on A, 3x effort on B. Never idle.
- **Evidence-based** - Every claim needs commands/outputs/timestamps


## UPDATE (20261103T060801Z) - DUAL-TRACK EXECUTION STARTED
- Created fresh blocker evidence for Track A
- Deep-reviewed alternative sources (no new GO found; ironflow remains sole path)
- Started Track B infrastructure (src/volatility/* modules created)
- All tests still passing (111/111)
- Both tracks running in parallel as mandated
