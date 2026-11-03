# AGENT_HANDOFF.md (SINGLE DURABLE SOURCE OF TRUTH)

**TIMESTAMP:** 20261103T100254Z
**REPO:** Funding-conditioned-volatility-and-liquidation-risk
**PRIORITY (by repo name):** LIQUIDATION-FIRST. Maximize heavy computable work now; eliminate idle-wait bottlenecks.

## SESSION GOAL
Do NOT passively poll. Build a self-driven campaign that produces verifiable artifacts every step. Remove bottlenecks so the next session cannot avoid doing heavy work. Every turn must produce a durable file/change.

## VERIFIED TRUTH (current)
- Track A (observed liquidations): FCLR-010 COMPLETE, FORECAST_GATE_PASSED (Hyperliquid ironflow census 2025-11..2026-10, 199 instruments, 5x30-day blocks, C2 vs B1 Brier rel reduction 2.21%, CI excludes zero). Sealed. Forward months 2026-11,12,2027-01,02 all return 404 (consec_absent=3). All admissible unauthenticated alternatives deep-reviewed - NO GO source found (blocker_evidence_20261103T070800Z.md). Structural data blocker: no new liquidation labels exist yet.
- Track B (volatility forecasting): H001 INCONCLUSIVE. All confirmatory panels exhausted (FCLR-003 sealed -3.78%, FCLR-006 -69.90% worse, FCLR-007 -3.42% worse, FCLR-008 +4.30% but CI crosses zero). Overlay INELIGIBLE. All tests 111/111 PASS.
- H002: PARTIAL_REPLICATION (direction matches paper, p=0.0792 not significant, SSRN HTTP 403 blocks exact replication).
- H003: NOT_SUPPORTED (sealed).

## BOTTLENECK REMOVAL (executed this session; do not re-open)
- Data exhaustion claim retracted: 2026 Apr-Jul all 5 symbols present in data_cache (markPriceKlines, indexPriceKlines, fundingRate). Track C data is NOT exhausted; Track A labels are.
- Track A forward-watch: ironflow returns 404 for >=2026-11. DO NOT poll. Probe once per session via --quick (<60s) only; resume only on HTTP 200 for YYYY-MM >= 2026-11.
- Sealed experiments frozen: FCLR-001/002/003/005/006/007/008/009/H003-EXT. Analysis-only allowed; no re-runs.

## NEXT FOCUS CAMPAIGN (HEAVY WORK - execute in order, NO idle loops)

### CAMPAIGN 1: TRACK A LIQUIDATION INTELLIGENCE (LIQUIDATION-FIRST, HIGH)
1. **Consolidate FCLR-010 evidence bundle**: `research_state/track_a_fclr010_consolidated.md` - full run_manifest entries, evaluation_summary_FCLR010.md, gate assessment, content hashes, provenance. Make reproducible from cache.
2. **Build liquidation-feature pipeline**: Using cached ironflow data through 2026-10, construct funding-conditioned liquidation features (funding z-scores, funding-turning, basis/premium alignment, realized vol regimes) + leakage-audited feature table. Write `research_state/track_a_feature_build_20261103T095405Z.md` + cached parquet/npz.
3. **Forward-watch automation**: Enhance `scripts/monitor_ironflow_liquidations.py` to log structured probes (content-length/hash) to `research_state/ironflow_watch_log.jsonl` (append-only). Keep --quick <60s. NO cron/polling loops, NO retry storms.

### CAMPAIGN 2: VOLATILITY FORECASTING DEEPENING (squeeze exhausted data, HIGH)
1. **FCLR-008 robustness deep-dive**: Alternative blockings (calendar vs 24h), wild bootstrap sensitivity, subperiod stability by quarter/regime, symbol-wise LOO with CIs. Write `research_state/fclr008_robustness_deep_20261103T095405Z.md`.
2. **Feature ablation forensics**: Decompose C2 into funding-only / basis-premium-only / smoothing-only vs B1. Identify which component drives +4.30% point estimate. Use cached panels only.
3. **Regime-conditional analysis**: Vol regime x funding regime x cross-asset correlation. Test if signal is regime-localized. Pre-register in note; do NOT change frozen protocols.

### CAMPAIGN 3: INFRASTRUCTURE / BOTTLENECK REMOVAL (HIGH)
1. **Test coverage hardening**: Focused tests for liquidation feature builder and ironflow monitor (fast). Keep all tests passing.
2. **Reproducibility**: Checksums, git SHA, timestamps on all heavy artifacts. Update run_manifest.json with campaign entries.
3. **Documentation**: research_protocol.md - add "data-exhaustion for confirmatory" note; gates stay frozen.

## EXECUTION RULES (strict)
- NO polling/waiting loops. Each action must produce a file/change.
- NO re-running sealed experiments. Analysis-only allowed.
- Track A resume ONLY on concrete data arrival (ironflow HTTP 200 for >=2026-11). If still 404, do NOT wait - run Campaigns 1-2-3.
- All code changes outside .github/workflows. Tests must pass (111/111).
- Commit nothing merely for activity; commit only coherent units of progress.
- Every session must leave AGENT_HANDOFF.md updated with concrete next actions + evidence.

## NEXT SESSION START (MANDATORY)
```bash
# 1) Read truth
cat research_state/AGENT_HANDOFF.md | head -80
cat research_state/hypothesis_registry.json | grep -B2 -A30 '"FCLR-H001"' | head -40
cat research_state/hypothesis_registry.json | grep -B2 -A40 '"FCLR-H004"' | head -50

# 2) Quick health (non-polling)
python scripts/monitor_ironflow_liquidations.py --quick
python -m unittest discover -s tests -v 2>&1 | tail -3

# 3) START HEAVY WORK IMMEDIATELY - pick first unstarted from Campaign 1
# Do NOT wait. Produce artifacts.
```

## RESUME TRIGGERS (Track A only)
- Ironflow events/fills YYYY-MM >= 2026-11 return HTTP 200 (monitor writes evidence). If true: pre-register FCLR-011, run frozen Track A harness on new window, update evaluation_summary/gate.
- New admissible unauthenticated liquidation source passes full rubric (>=5 symbols, >=3x30d blocks OR complete month series, compatible schema) - document in blocker_evidence with evidence.

**DEFAULT MODE:** HEAVY_ANALYSIS_CAMPAIGN. No idle time. Every turn produces durable artifacts.
