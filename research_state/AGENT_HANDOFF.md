# AGENT_HANDOFF.md (SINGLE DURABLE SOURCE OF TRUTH)

**TIMESTAMP:** 20261103T095342Z
**REPO:** Funding-conditioned-volatility-and-liquidation-risk
**PRIORITY (by repo name):** LIQUIDATION-FIRST. Maximize heavy computable work now; eliminate idle-wait bottlenecks.

## SESSION GOAL
Do NOT passively poll. Build a self-driven campaign that produces verifiable artifacts every step. Remove blockers so next session cannot avoid doing heavy work.

## VERIFIED TRUTH (current)
- Track A (observed liquidations): FCLR-010 COMPLETE (Hyperliquid ironflow census 2025-11..2026-10). Gate PASSED, sealed. Forward months 2026-11,12,2027-01,02 return 404 (consec_absent=3). All admissible unauthenticated alternatives deep-reviewed - NO GO sources found. Structural blocker (data not yet published).
- Track B (volatility forecasting): H001 INCONCLUSIVE. All confirmatory panels exhausted (FCLR-003 sealed negative, FCLR-006 negative, FCLR-007 underpowered negative, FCLR-008 unsealed decisive but CI crosses zero [+4.30%, 95% CI crosses zero]). Overlay INELIGIBLE. All tests 111/111 PASS.
- H002: PARTIAL_REPLICATION (direction matches paper but not significant; SSRN blocked).
- H003: NOT_SUPPORTED (sealed).

## IMMEDIATE HEAVY CAMPAIGN (execute in order, NO idle loops)

### CAMPAIGN 1: LIQUIDATION INTELLIGENCE (Track A hardening) - HIGH
1. **Strengthen FCLR-010 artifacts**: Generate consolidated Track A evidence bundle (run_manifest entries, evaluation_summary, gate assessment) into `research_state/track_a_fclr010_consolidated.md` with full hashes/provenance. Make reproducible from cache.
2. **Build liquidation-feature pipeline**: Using cached ironflow data through 2026-10, construct funding-conditioned liquidation features (funding z-scores, funding-turning, basis/premium alignment, realized vol regimes) and produce a leakage-audited feature table for future use. Write to `research_state/track_a_feature_build_20261103T072021Z.md` + cached parquet/npz if needed.
3. **Forward-watch automation**: Enhance `scripts/monitor_ironflow_liquidations.py` to log structured probes with content-length/hash, write to `research_state/ironflow_watch_log.jsonl` (append-only). Keep `--quick` <60s. DO NOT add cron/polling loops or retry storms.

### CAMPAIGN 2: VOLATILITY FORECASTING DEEPENING (squeeze more from exhausted data) - HIGH
Despite H001 inconclusive and panels exhausted, extract maximum insight:
1. **Robustness mining**: Re-examine FCLR-008 with alternative blockings (calendar blocks vs 24h), wild bootstrap sensitivity, subperiod stability (by quarter/regime), symbol-wise leave-one-out with CIs. Write `research_state/fclr008_robustness_deep_20261103T072021Z.md`.
2. **Feature ablation forensics**: Systematically decompose C2 into components (funding-only, basis/premium-only, smoothing-only) vs B1 to identify which component drives the +4.30% point estimate. Use existing cached panels.
3. **Regime-conditional analysis**: Vol regime, funding regime (signed/abs), cross-asset correlation regimes. Test if signal is regime-localized. Pre-register analysis in note but don't change frozen protocols.

### CAMPAIGN 3: INFRASTRUCTURE/BOTTLENECK REMOVAL - HIGH
1. **Test coverage hardening**: Add focused tests for liquidation feature builder and ironflow monitor if missing. Keep tests fast.
2. **Reproducibility**: Ensure all heavy artifacts have checksums, git SHA, timestamps. Update run_manifest with campaign entries.
3. **Documentation**: Update research_protocol with "data-exhaustion for confirmatory" note but leave gates frozen.

## EXECUTION RULES (strict)
- NO polling/waiting loops. Each action must produce a file/change.
- NO re-running sealed experiments (FCLR-001/002/003/005/006/007/008 gates frozen). Analysis-only allowed.
- Track A resume only on concrete data arrival (ironflow returns 200 for >=2026-11). If still 404, do NOT wait - do Campaigns 1-2-3.
- All code changes outside .github/workflows. Tests must pass.
- Commit nothing just for activity; commit only if coherent unit of progress.
- Every session must leave AGENT_HANDOFF.md updated with concrete next actions and evidence.

## NEXT SESSION START (MANDATORY)
```bash
# 1) Read truth
cat research_state/AGENT_HANDOFF.md | head -80
cat research_state/hypothesis_registry.json | grep -B2 -A30 '"FCLR-H001"' | head -40
cat research_state/hypothesis_registry.json | grep -B2 -A40 '"FCLR-H004"' | head -50

# 2) Quick health
python scripts/monitor_ironflow_liquidations.py --quick
python -m unittest discover -s tests -v 2>&1 | tail -3

# 3) START HEAVY WORK IMMEDIATELY - pick first unstarted from Campaign 1
# Do NOT wait. Produce artifacts.
```

## RESUME TRIGGERS (Track A only)
- Ironflow events/fills YYYY-MM >= 2026-11 return HTTP 200 (monitor writes evidence). If true: pre-register FCLR-011, run frozen Track A harness on new window, update evaluation_summary/gate.
- New admissible unauthenticated liquidation source passes full rubric (>=5 symbols, >=3x30d blocks OR complete month series, compatible schema) - document in blocker_evidence with evidence.

**DEFAULT MODE:** HEAVY_ANALYSIS_CAMPAIGN. No idle time. Every turn produces durable artifacts.
