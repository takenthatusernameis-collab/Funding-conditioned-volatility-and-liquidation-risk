# AGENT_HANDOFF.md (SINGLE DURABLE SOURCE OF TRUTH)

**TIMESTAMP:** 20261103T110235Z
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
- **BOTTLENECK: FCLR-002 test split has only 2 non-overlapping 30-day blocks (<3 required) despite -9.28% QLIKE with CI excluding zero. Block-count resolution MANDATORY: build FCLR-011 panel from raw 2026 archives (>=3 blocks structurally available) + pre-registration, OR produce machine-checkable impossibility proof.**
- Tests: 117/117 PASS at HEAD (run `python -m unittest discover -s tests -v`). No workflow changes.
- Data exhaustion claim retracted: 2026 Jan-Aug mark-price data fully cached (FCLR-008 panel: 218 days, 7 blocks, 5 symbols, 5232 common timestamps, hashes in fclr008_coverage_audit.json). 2024 Q1 Binance data present in root zips/dirs.

## BOTTLENECK REMOVAL (executed; do not re-open)
- Track A forward-watch: ironflow returns 404 for >=2026-11. DO NOT poll. Probe once per session via --quick (<60s); resume only on HTTP 200 for YYYY-MM >= 2026-11.
- Sealed experiments frozen: FCLR-001/002/003/005/006/007/008/009/H003-EXT. Analysis-only allowed; no re-runs.
- FCLR-002 block-count bottleneck: convert to FCLR-011 panel build from raw archives OR impossibility proof.

## NEXT FOCUS CAMPAIGN (HEAVY WORK - execute in order, NO idle loops)

### CAMPAIGN 1: FCLR-011 CONFIRMATORY CELL BUILD (repo-name primary, HIGH)
1. **PRE-REGISTER FIRST** (before any outcome peek): `research_state/pre_registration_fclr011_<UTC>.md` using research_protocol_fclr008.md v1.0 as template (new version). Splits frozen BEFORE outcomes. Criteria: >=5 symbols, >=3 non-overlapping 30-day test blocks, block bootstrap 2000 reps, hypothesis FCLR-H001.
2. **BUILD PANEL**: leakage-resistant panel from root raw archives (markPriceKlines, indexPriceKlines, premiumIndexKlines, fundingRate zips, 2026 Jan-Aug). Train-only normalization, trailing-only, chronological, purge/embargo. Output: `research_state/data_cache/fclr011_panel.json` + coverage audit.
3. **EXECUTE** (if criteria met): FCLR-011 confirmatory run, `research_state/evaluation_summary_FCLR-011_<UTC>.md`, assess forecast gate (>=2% rel QLIKE + CI excludes zero).
4. **IF INFEASIBLE**: `research_state/block_count_resolution_fclr011_<UTC>.md` with machine-checkable symbol/day/block counts + hash anchors.

### CAMPAIGN 2: TRACK A LIQUIDATION INTELLIGENCE (liquidation-first, HIGH - MONITOR ONLY)
1. Consolidate FCLR-010 evidence bundle: `research_state/track_a_fclr010_consolidated.md`.
2. Build liquidation-feature pipeline from cached ironflow data through 2026-10.
3. Forward-watch: `monitor_ironflow_liquidations.py --quick` (<60s), append-only log to `research_state/ironflow_watch_log.jsonl`. NO cron/polling loops.

### CAMPAIGN 3: INFRASTRUCTURE / BOTTLENECK REMOVAL (HIGH)
1. Test coverage hardening (fast). Keep all tests passing (>=117/117).
2. Reproducibility: checksums, git SHA, timestamps on all heavy artifacts. Update run_manifest.json.
3. Documentation: research_protocol.md data-exhaustion note; gates stay frozen.

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

# 2) Quick health (non-polling)
python scripts/monitor_ironflow_liquidations.py --quick
python -m unittest discover -s tests -v 2>&1 | tail -3

# 3) START HEAVY WORK IMMEDIATELY - Campaign 1, step 1: pre-register FCLR-011
# Do NOT wait. Produce artifacts.
```

## RESUME TRIGGERS (Track A only)
- Ironflow events/fills YYYY-MM >= 2026-11 return HTTP 200 (monitor writes evidence). If true: pre-register FCLR-011-track-a, run frozen Track A harness on new window, update evaluation_summary/gate.
- New admissible unauthenticated liquidation source passes full rubric (>=5 symbols, >=3x30d blocks OR complete month series, compatible schema) - document in blocker_evidence with evidence.

**DEFAULT MODE:** HEAVY_ANALYSIS_CAMPAIGN. No idle time. Every turn produces durable artifacts.