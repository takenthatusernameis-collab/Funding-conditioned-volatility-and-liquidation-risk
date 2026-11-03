# AGENT_HANDOFF.md (SINGLE DURABLE SOURCE OF TRUTH)

**TIMESTAMP:** 20261103T100705Z
**REPO:** Funding-conditioned-volatility-and-liquidation-risk
**PRIORITY (by repo name):** LIQUIDATION-FIRST + FUNDING-CONDITIONED-VOLATILITY. Both tracks named in repo. Maximize heavy computable work; eliminate idle-wait bottlenecks.

## SESSION GOAL
Do NOT passively poll. Build a self-driven campaign that produces verifiable artifacts every step. Remove bottlenecks so the next session cannot avoid doing heavy work. Every turn must produce a durable file/change.

## VERIFIED TRUTH (current)
- Track A (observed liquidations, ironflow/Hyperliquid): FCLR-010 COMPLETE, FORECAST_GATE_PASSED (C2 vs B1 Brier rel reduction 2.21%, CI [-0.004892,-0.001263] excludes zero, 199 instruments, 5x30-day blocks). SEALED. Forward months 2026-11,12,2027-01,02 all return 404 (consec_absent=3). All admissible unauthenticated alternatives deep-reviewed - NO-GO source found (track_a_final_block_proof.md, track_a_deadend_map.md). Structural data blocker: no new liquidation labels exist yet. Overlay executed (hypothetical only, no profitability claim).
- Track B (modeled boundary breaches/H003): CLOSED_NEGATIVE, NOT_SUPPORTED (sealed, no robust incremental skill after Holm m=16).
- Track C (volatility forecasting/H001): INCONCLUSIVE. All confirmatory panels exhausted:
  - FCLR-003 (sealed 2024, -3.78%, CI crosses zero) NOT_SUPPORTED
  - FCLR-006 (unsealed 2026 May-Aug, -69.90% worse) NOT_SUPPORTED
  - FCLR-007 (11-day, -3.42% worse) NOT_SUPPORTED
  - FCLR-008 (unsealed 2026 Jan-Aug, +4.30% but CI [-0.029938,0.000524] crosses zero) INCONCLUSIVE
- H002 (funding-extreme correction replication): PARTIAL_REPLICATION (direction matches paper, p=0.0792 not significant, SSRN HTTP 403 blocks exact replication).
- H004: SUPPORTED via FCLR-010 (Track A).
- **BOTTLENECK: FCLR-002 test split has only 2 non-overlapping 30-day blocks (<3 required) despite -9.28% QLIKE with CI excluding zero. Block-count resolution MANDATORY (find >=3 blocks config or document impossibility).**
- Tests: 117/117 PASS at HEAD (run `python -m unittest discover -s tests -v`). No workflow changes.
- Data exhaustion claim retracted: 2026 Jan-Aug mark-price data fully cached (FCLR-008 panel: 218 days, 7 blocks, 5 symbols, 5232 common timestamps, hashes in fclr008_coverage_audit.json). 2024 Q1 Binance data present in root zips/dirs.

## BOTTLENECK REMOVAL (executed this session; do not re-open)
- Track A forward-watch: ironflow returns 404 for >=2026-11. DO NOT poll. Probe once per session via --quick (<60s); resume only on HTTP 200 for YYYY-MM >= 2026-11.
- Sealed experiments frozen: FCLR-001/002/003/005/006/007/008/009/H003-EXT. Analysis-only allowed; no re-runs.
- FCLR-002 block-count bottleneck: not yet resolved. Must either find >=3 non-overlapping 30-day blocks on an unsealed panel or document structural impossibility with machine-checkable evidence.

## NEXT FOCUS CAMPAIGN (HEAVY WORK - execute in order, NO idle loops)

### CAMPAIGN 1: FUNDING-CONDITIONED VOLATILITY DEEP DIVE (repo-name primary, HIGH)
1. **BLOCK_COUNT_RESOLUTION**: Audit all available unsealed data windows for >=3 non-overlapping 30-day block configs on >=5 instruments. Check FCLR-002 test window extensions and any unsealed 2024 Q4/Q1 windows. Write `research_state/block_count_resolution_20261103T100705Z.md` with machine-checkable evidence (symbol counts, day counts, block counts, hash anchors). If impossible, document why with proof.
2. **Mechanism ablations on frozen FCLR-002 splits**: Decompose C2 into funding-only / basis-premium-only / smoothing-only vs B1 using cached panels only. Identify which component drives the -9.28% QLIKE point estimate. Write `research_state/fclr002_ablation_deep_dive_20261103T100705Z.md`.
3. **Regime-conditional analysis**: Vol regime x funding regime x cross-asset correlation on frozen FCLR-002 splits. Test if signal is regime-localized. Pre-register in note; do NOT change frozen protocols.
4. **Interaction forensics**: Funding x RV interaction terms, turning-point detection, lead-lag with censoring. Use cached FCLR-002 panel only.

### CAMPAIGN 2: TRACK A LIQUIDATION INTELLIGENCE (liquidation-first, HIGH - MONITOR ONLY)
1. **Consolidate FCLR-010 evidence bundle**: `research_state/track_a_fclr010_consolidated.md` - full run_manifest entries, evaluation_summary_FCLR010.md, gate assessment, content hashes, provenance. Make reproducible from cache.
2. **Build liquidation-feature pipeline**: Using cached ironflow data through 2026-10, construct funding-conditioned liquidation features (funding z-scores, funding-turning, basis/premium alignment, realized vol regimes) + leakage-audited feature table. Write `research_state/track_a_feature_build_20261103T100705Z.md` + cached parquet/npz.
3. **Forward-watch automation**: Enhance `scripts/monitor_ironflow_liquidations.py` to log structured probes (content-length/hash) to `research_state/ironflow_watch_log.jsonl` (append-only). Keep --quick <60s. NO cron/polling loops, NO retry storms.

### CAMPAIGN 3: INFRASTRUCTURE / BOTTLENECK REMOVAL (HIGH)
1. **Test coverage hardening**: Focused tests for liquidation feature builder and ironflow monitor (fast). Keep all tests passing (target >=117/117).
2. **Reproducibility**: Checksums, git SHA, timestamps on all heavy artifacts. Update run_manifest.json with campaign entries.
3. **Documentation**: research_protocol.md - add "data-exhaustion for confirmatory" note; gates stay frozen.

## EXECUTION RULES (strict)
- NO polling/waiting loops. Each action must produce a file/change.
- NO re-running sealed experiments. Analysis-only allowed.
- Track A resume ONLY on concrete data arrival (ironflow HTTP 200 for >=2026-11). If still 404, do NOT wait - run Campaigns 1-2-3.
- All code changes outside .github/workflows. Tests must pass (>=117/117).
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

# 3) START HEAVY WORK IMMEDIATELY - Campaign 1, step 1: block_count_resolution
# Do NOT wait. Produce artifacts.
```

## RESUME TRIGGERS (Track A only)
- Ironflow events/fills YYYY-MM >= 2026-11 return HTTP 200 (monitor writes evidence). If true: pre-register FCLR-011, run frozen Track A harness on new window, update evaluation_summary/gate.
- New admissible unauthenticated liquidation source passes full rubric (>=5 symbols, >=3x30d blocks OR complete month series, compatible schema) - document in blocker_evidence with evidence.

**DEFAULT MODE:** HEAVY_ANALYSIS_CAMPAIGN. No idle time. Every turn produces durable artifacts.