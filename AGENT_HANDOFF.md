# AGENT_HANDOFF.md (SINGLE DURABLE HANDOFF)
Timestamp (UTC): 20261105T071103Z
Git SHA (HEAD): 69d08ad5
Branch: main
Repo: Funding-conditioned-volatility-and-liquidation-risk
Handoff ID: FCLR-HANDOFF-20261105T071103Z | Priority: P0 - REPO-NAME PRIORITIZED + HEAVY WORK MANDATORY | Mode: CAMPAIGN-DRIVEN | Enforcement: NO-SKIP | Bottleneck-State: MAXIMALLY-CONSOLIDATED-HEAVY

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
TASK ID: FCLR-NEXT-090-TRACK-A-HEAVY-WHILE-BLOCKED-DEMOLISH-ALL-BOTTLENECKS
PRIORITY: P0 - REPO-NAME PRIORITIZED (Volatility SEALED/LOCKED; Liquidation Risk = ONLY ACTIVE OBJECTIVE)
TIMESTAMP (UTC): 20261105T070937Z
CAMPAIGN: TRACK A LIQUIDATION RISK - MAXIMUM HEAVY PROGRESS WHILE BLOCKED. NO COASTING. ELIMINATE EVERY REMAINING BOTTLENECK. FORCE FUTURE AGENTS INTO HEAVY WORK.
ENFORCEMENT: ALL STEPS MANDATORY. SESSION INCOMPLETE IF ANY SKIPPED. PREREGISTER BEFORE INSPECTING OUTCOMES IF TRIGGERED. NO IDLE TURNS. NO "MONITOR ONLY" WITHOUT CONCRETE HARDENING.

OBJECTIVE (INFERRED): Complete the liquidation-risk half of "Funding-conditioned-volatility-and-liquidation-risk". Data blocked. While blocked you MUST create unavoidable heavy progress: aggressively consolidate artifacts to bare minimum (drive count down further), exhaust unauthenticated discovery (Hyperliquid-only), harden GO rubric to be maximally strict, extend adversarial tests, make FCLR-010 harness zero-latency for instant resume with <10s cold-start, eliminate ALL redundant wrappers/paths/duplicate docs, collapse any remaining sweeps, and leave the state STRICTER than you found it. Never stop for "no data". Future agents must NOT be able to coast.

CONSTRAINTS: No credentials/manual files/.github/workflows changes. Leakage-safe, preregister-before-outcomes. Track C/B locked/unsupported. Raw data/caches out of git. Clean-clone reproducible. No schedulers/pollers/status-only files/repeated wrappers/agent-controllers. Hyperliquid-only for Track A. Do not conflate observed/modelled liquidations. No threshold-shopping. No scope drift.

MANDATORY EXECUTION (IN ORDER - ALL REQUIRED):

1) ENTRY METRICS & BOTTLENECK BASELINE (IRREFUTABLE)
   - Count artifacts: ls -1 research_state/*.md research_state/*.json | wc -l
   - Count ironflow probes: find . -name '*ironflow*probe*' -not -path '*/\.git/*' | wc -l (MUST be <= 1 non-digest)
   - Measure I/O: time python scripts/monitor_ironflow_liquidations.py --quick >/dev/null 2>&1
   - Find redundancy: list timestamped duplicates, wrappers, status-only files
   - Record in research_state/campaign_sweep_tracka_$(date -u +%Y%m%dT%H%M%SZ).md with before/after targets (net -15 files minimum OR >=60% new artifacts consolidated).

2) TRIGGER PROBE (EXHAUSTIVE, HYPERLIQUID-ONLY - FAST PATH)
   - Run: python scripts/monitor_ironflow_liquidations.py --quick
   - Run: python scripts/deep_review_alt_sources.py
   - Run: python scripts/hunt_alternative_liquidation_sources.py
   - Log every URL/status/ETag/last-modified. IF trigger -> PREREGISTER before reading outcomes in research_state/tracka_fclr010_prereg_$(date -u +%Y%m%dT%H%M%SZ).md with frozen splits/rubric; run ONLY frozen FCLR-010 harness. ELSE write "NO NEW DATA - ON HOLD" with irrefutable evidence and IMMEDIATELY proceed to demolition (do not stop).

3) BOTTLENECK DEMOLITION (AGGRESSIVE - MANDATORY)
   - Merge ALL redundant timestamped artifacts into canonical docs. Delete/merge equivalents. Enforce EXACTLY 1 non-digest + digests for ironflow probe state.
   - Eliminate duplicate code paths/wrappers. Collapse similar scripts if safe and tested.
   - Remove any status-only/scheduler/poller files if they appeared. Kill repeated wrappers.
   - Target: net -15 files from entry baseline OR consolidate >=60% of timestamped files created recently. Document before/after with full file list in research_state/bottleneck_demolition_$(date -u +%Y%m%dT%H%M%SZ).md.

4) SOURCE HARDENING + MAXIMALLY STRICT RUBRIC
   - Tighten GO rubric (stricter than before). Harden classification with fixtures. Add/extend adversarial tests for rubric edges.
   - Cache probes with ETags/hashes; add fast-fail. Document in research_state/tracka_rubric_hardened_$(date -u +%Y%m%dT%H%M%SZ).md.

5) HARNESS HARDENING + OFFLINE DRY-RUN (ZERO-LATENCY RESUME)
   - Verify fixtures + FCLR-010 offline dry-run end-to-end. Fix any gaps (tests first). Make resume path trivial (<10s). Add fast-path checks. Document in research_state/tracka_fclr010_dryrun_hardened_$(date -u +%Y%m%dT%H%M%SZ).md.

6) TESTS, EVIDENCE, HANDOFF UPDATE (MANDATORY - LEAVE STRICTER STATE)
   - Run: python -m unittest discover tests (MUST stay green - 136 tests)
   - Write research_state/liquidation_forward_validate_010_blocker_$(date -u +%Y%m%dT%H%M%SZ).md with full evidence, metrics, bottlenecks removed, concrete resume instructions
   - Update research_state/experiment_frontier.json (last_checked now, track_a_blocked true, pointer to new blocker, notes more specific)
   - Update AGENT_HANDOFF.md with NEW stricter timestamped next task (cannot be coasted). Commit nothing just for activity.

RESUME CONDITION: ironflow data/events/YYYY-MM.parquet or data/fills/YYYY-MM.parquet for month>=2026-11 returns HTTP 200 unauthenticated OR admissible unauthenticated Hyperliquid source passes strict GO rubric. Hyperliquid-only.

STOP RULE: Complete ALL steps + ALL artifacts with concrete metrics. Track C locked. Track B unsupported. No conflation. No schedulers/pollers/status-only/repeated wrappers/agent-controllers/workflow changes. Preregister BEFORE outcomes if triggered. Heavy work mandatory while blocked. NO COASTING. Leave state stricter than found.
```

## VERIFICATION COMMANDS (RUN ON ENTRY)
- `python -m unittest discover tests` (must be green)
- `python scripts/monitor_ironflow_liquidations.py --quick`
- `python scripts/deep_review_alt_sources.py`
- `python scripts/hunt_alternative_liquidation_sources.py`
- `python scripts/generate_tracka_fixtures.py`

## NEXT TASK (TIMESTAMPED)
20261105T071103Z: Execute FCLR-NEXT-090 as above. Volatility SEALED/LOCKED. Liquidation Risk ONLY focus. Demolish ALL bottlenecks (net -15 files OR >=60% consolidated), probe exhaustively, harden rubric/fixtures/tests to MAXIMUM strictness, keep harness offline-ready zero-latency (<10s), tests green, write liquidation_forward_validate_010_blocker_*.md, update experiment_frontier.json and this handoff to be STRICTER. NO COASTING.
