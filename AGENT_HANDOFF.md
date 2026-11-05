# AGENT_HANDOFF.md (SINGLE DURABLE HANDOFF)
Timestamp (UTC): 20261105T062115Z
Git SHA (HEAD): f936bc00
Branch: main
Repo: Funding-conditioned-volatility-and-liquidation-risk
Handoff ID: FCLR-HANDOFF-20261105T062115Z | Priority: P0 - REPO-NAME PRIORITIZED + HEAVY WORK MANDATORY | Mode: CAMPAIGN-DRIVEN | Enforcement: NO-SKIP | Bottleneck-State: CONSOLIDATED-AGGRESSIVE

## REPO-NAME PRIORITIZATION (INFERRED)
Repository name: "Funding-conditioned-volatility-and-liquidation-risk"
- Funding-conditioned VOLATILITY component = Track C (FCLR-011) — SEALED/LOCKED. Forecast gate PASSED. DO NOT retune/re-run sealed cells/conflate.
- LIQUIDATION RISK component = Track A (FCLR-010) — ONLY UNFINISHED HALF. BLOCKED on admissible unauthenticated liquidation data (Hyperliquid-only). Track B = NOT_SUPPORTED.
- BOTH components are core to repo identity. While volatility is sealed, liquidation risk MUST be driven to completion via admissible data or hardened to resume instantly on trigger. NO SCOPE DRIFT TO SEALED TRACKS.

## CURRENT VERIFIED STATE (CLEAN BASELINE)
- Tests: `python -m unittest discover tests` — 136 tests OK (adversarial tests present). MUST remain green.
- Track C: SEALED/LOCKED. Track B: NOT_SUPPORTED.
- Track A: ON-TRIGGER/MONITOR ONLY. Last blocker: liquidation_forward_validate_009_blocker_20261105T061930Z.md. experiment_frontier.json updated.
- Artifact churn reduced: 244 -> 230 files in research_state (-5.7%); bottlenecks consolidated (sweeps/dryruns/bottlenecks/alt-sources merged). 1 non-digest ironflow probe path enforced.
- Harness: FCLR-010 fixtures exist; dry-run capable offline. No schedulers/pollers/status-only files/agent-controllers/workflow changes permitted.
- NO COASTING ALLOWED. Every session must produce measurable bottleneck reduction or hardness improvements.

## SINGLE INITIAL TASK MESSAGE FOR NEXT AGENTIC SESSION (COPY/PASTE VERBATIM)
```text
TASK ID: FCLR-NEXT-089-TRACK-A-HEAVY-WHILE-BLOCKED-DEMOLISH-BOTTLENECKS
PRIORITY: P0 - REPO-NAME PRIORITIZED (Volatility SEALED/LOCKED; Liquidation Risk = ONLY ACTIVE OBJECTIVE)
TIMESTAMP (UTC): 20261105T062115Z
CAMPAIGN: TRACK A LIQUIDATION RISK - MAXIMUM HEAVY PROGRESS WHILE BLOCKED. NO COASTING. ELIMINATE EVERY BOTTLENECK.
ENFORCEMENT: ALL STEPS MANDATORY. SESSION INCOMPLETE IF ANY SKIPPED. PREREGISTER BEFORE INSPECTING OUTCOMES IF TRIGGERED. NO IDLE TURNS.

OBJECTIVE (INFERRED): Complete the liquidation-risk half of "Funding-conditioned-volatility-and-liquidation-risk". Data blocked. While blocked you MUST create unavoidable heavy progress: aggressively consolidate artifacts (drive down count), exhaust unauthenticated discovery (Hyperliquid-only), harden rubric/fixtures/adversarial tests, make FCLR-010 harness zero-latency for instant resume, eliminate redundant wrappers/paths, and produce concrete before/after metrics. Never stop for "no data". Force future agents to work hard by leaving a stricter, cleaner state.

CONSTRAINTS: No credentials/manual files/.github/workflows changes. Leakage-safe, preregister-before-outcomes. Track C/B locked/unsupported. Raw data/caches out of git. Clean-clone reproducible. No schedulers/pollers/status-only files/repeated wrappers/agent-controllers. Hyperliquid-only for Track A. Do not conflate observed/modelled liquidations. No threshold-shopping.

MANDATORY EXECUTION (IN ORDER - ALL REQUIRED):

1) ENTRY METRICS & BOTTLENECK BASELINE
   - Count: ls -1 research_state/*.md research_state/*.json | wc -l; find . -name '*ironflow*probe*' -not -path '*/\.git/*' | wc -l; count non-digest vs digest
   - Measure I/O: time python scripts/monitor_ironflow_liquidations.py --quick >/dev/null 2>&1 | tail -1
   - Record baseline in research_state/campaign_sweep_tracka_$(date -u +%Y%m%dT%H%M%SZ).md with before-counts, churn sources, redundant files, I/O estimate, concrete targets.

2) TRIGGER PROBE (EXHAUSTIVE, FAST PATH - HYPERLIQUID-ONLY)
   - Run: python scripts/monitor_ironflow_liquidations.py --quick
   - Run: python scripts/deep_review_alt_sources.py
   - Run: python scripts/hunt_alternative_liquidation_sources.py
   - Log full tables with URLs/status/ETags. IF trigger -> PREREGISTER before reading outcomes in research_state/tracka_fclr010_prereg_$(date -u +%Y%m%dT%H%M%SZ).md; run ONLY frozen FCLR-010 harness. ELSE write "NO NEW DATA - ON HOLD" with irrefutable evidence.

3) BOTTLENECK DEMOLITION (CONSOLIDATE AGGRESSIVELY - MANDATORY)
   - Merge ALL redundant timestamped artifacts into canonical docs. Delete/merge equivalents. Enforce EXACTLY 1 non-digest + digests for ironflow probe state.
   - Eliminate duplicate code paths/wrappers. Collapse similar scripts if safe and tested.
   - Target >=50% reduction of NEW timestamped files created this session vs entry count OR net -10 more files from entry baseline (whichever harder). Document before/after in research_state/bottleneck_demolition_$(date -u +%Y%m%dT%H%M%SZ).md with file list.

4) SOURCE HARDENING + RUBRIC ENFORCEMENT
   - Tighten GO rubric to be stricter; harden classification with fixtures; add/extend adversarial tests for rubric edges. Cache probes with ETags/hashes. Document in research_state/tracka_rubric_hardened_$(date -u +%Y%m%dT%H%M%SZ).md

5) HARNESS HARDENING + OFFLINE DRY-RUN (ZERO-LATENCY RESUME)
   - Verify fixtures + FCLR-010 offline dry-run end-to-end. Fix any gaps (tests first). Make resume path trivial. Document in research_state/tracka_fclr010_dryrun_hardened_$(date -u +%Y%m%dT%H%M%SZ).md

6) TESTS, EVIDENCE, HANDOFF UPDATE (MANDATORY)
   - Run: python -m unittest discover tests (MUST stay green - 136 tests)
   - Write research_state/liquidation_forward_validate_010_blocker_$(date -u +%Y%m%dT%H%M%SZ).md with full evidence, metrics, bottlenecks removed
   - Update research_state/experiment_frontier.json (last_checked now, track_a_blocked true, pointer to new blocker)
   - Update AGENT_HANDOFF.md with new timestamped next task (stricter). Commit nothing just for activity.

RESUME CONDITION: ironflow data/events/YYYY-MM.parquet or data/fills/YYYY-MM.parquet for month>=2026-11 returns HTTP 200 unauthenticated OR admissible unauthenticated Hyperliquid source passes strict GO rubric. Hyperliquid-only.

STOP RULE: Complete ALL steps + ALL artifacts with concrete metrics. Track C locked. Track B unsupported. No conflation. No schedulers/pollers/status-only/repeated wrappers/agent-controllers/workflow changes. Preregister BEFORE outcomes if triggered. Heavy work mandatory while blocked. NO COASTING.
```

## VERIFICATION COMMANDS (RUN ON ENTRY)
- `python -m unittest discover tests` (must be green)
- `python scripts/monitor_ironflow_liquidations.py --quick`
- `python scripts/deep_review_alt_sources.py`
- `python scripts/hunt_alternative_liquidation_sources.py`
- `python scripts/generate_tracka_fixtures.py`

## NEXT TASK (TIMESTAMPED)
20261105T062115Z: Execute FCLR-NEXT-089 as above. Volatility SEALED/LOCKED. Liquidation Risk ONLY focus. Demolish bottlenecks aggressively (>=50% new artifacts or net -10), probe exhaustively, harden rubric/fixtures/tests, keep harness offline-ready zero-latency, tests green, write liquidation_forward_validate_010_blocker_*.md, update experiment_frontier.json and this handoff. NO COASTING.
