# AGENT_HANDOFF.md (SINGLE DURABLE HANDOFF)
Timestamp (UTC): 20261105T061238Z
Git SHA (HEAD): 8e8b7e9091b1d89b1020761ffa0423b3d19983ef
Branch: main
Repo: Funding-conditioned-volatility-and-liquidation-risk
Handoff ID: FCLR-HANDOFF-20261105T051723Z | Priority: P0 - REPO-NAME PRIORITIZED + HEAVY WORK ENFORCED | Mode: CAMPAIGN-DRIVEN | Enforcement: NO-SKIP

## REPO-NAME PRIORITIZATION (INFERRED)
Repository name: "Funding-conditioned-volatility-and-liquidation-risk"
- Funding-conditioned VOLATILITY component = Track C (FCLR-011) — SEALED/LOCKED. Forecast gate PASSED. DO NOT retune, re-run sealed cells, or conflate.
- Liquidation RISK component = Track A (FCLR-010) — UNFULFILLED HALF. THIS IS THE ONLY ACTIVE FOCUS. Currently BLOCKED on admissible unauthenticated liquidation data.

## CURRENT VERIFIED STATE
- Tests: suite green (unittest discover tests) — 133 tests OK; adversarial tests added. DO NOT regress.
- FCLR-NEXT-084 (current heavy campaign) EXECUTED: full trigger probe (monitor/deep_review/hunt) — NO NEW DATA; bottlenecks demolished (ironflow_probe non-digest kept at 1, trends consolidated); FCLR-010 harness dry-run ready offline; source discovery hardened; evidence consolidated.
- Track C: SEALED/LOCKED. Track B: NOT_SUPPORTED. Track A: ON-TRIGGER/MONITOR ONLY, blocked on data.
- experiment_frontier.json updated with last_checked 2026-11-05T05:17:23Z pointing to liquidation_forward_validate_007_blocker_20261105T051723Z.md

## SINGLE INITIAL TASK MESSAGE FOR NEXT AGENTIC SESSION (COPY/PASTE VERBATIM)
```text
TASK ID: FCLR-NEXT-085-TRACK-A-MAINTAIN-HEAVY-WHILE-BLOCKED
PRIORITY: P0 - REPO-NAME PRIORITIZED (Volatility DONE/LOCKED; Liquidation Risk ONLY)
TIMESTAMP (UTC): 20261105T051723Z
CAMPAIGN: TRACK A LIQUIDATION-RISK - MAINTAIN HEAVY PROGRESS WHILE BLOCKED. DO NOT COAST.
ENFORCEMENT: ALL STEPS MANDATORY. SESSION INCOMPLETE IF ANY SKIPPED.

OBJECTIVE (INFERRED FROM REPO NAME): With funding-conditioned volatility sealed, liquidation risk is the sole unfinished objective. Data remains blocked. While blocked, you MUST create unavoidable progress: keep artifact churn minimal (enforce consolidation), exhaust unauthenticated source discovery, keep FCLR-010 harness zero-latency on resume, add tests, and leave undeniable executable evidence. If resume triggers appear at any point, PREREGISTER BEFORE INSPECTING OUTCOMES and run ONLY the frozen FCLR-010 harness.

CONSTRAINTS: No credentials/manual files/.github/workflows changes. Leakage-safe, preregister-before-outcomes. Track C/B remain locked/unsupported. Raw data/caches out of git. Clean-clone reproducible. No schedulers/pollers/status-only files/repeated wrappers/agent-controllers. Hyperliquid-only for Track A.

MANDATORY EXECUTION (IN ORDER - ALL REQUIRED):
1) BASELINE METRICS: Count ironflow_probe non-digest vs digest, trends, alt-source files, research_state size. Record in research_state/campaign_sweep_tracka_$(date -u +%Y%m%dT%H%M%SZ).md.
2) TRIGGER PROBE: Run monitor_ironflow_liquidations.py --quick, deep_review_alt_sources.py, hunt_alternative_liquidation_sources.py. Log full tables. If >=2026-11 ironflow OR rubric-GO alternative appears -> HALT, PREREGISTER in research_state/fclr010_prereg_$(date -u +%Y%m%dT%H%M%SZ).json BEFORE inspecting outcomes (hypothesis, frozen splits, features/targets, metrics, stop rule, data hashes), run ONLY frozen FCLR-010 harness. Else write "NO NEW DATA - ON HOLD" with complete tables.
3) BOTTLENECK DEMOLITION: If any new artifact churn appeared, consolidate aggressively (target >=40% reduction relative to new baseline). Fix >=1 concrete bottleneck with before/after diff/timings/counts/I-O. Document in research_state/bottleneck_demolition_$(date -u +%Y%m%dT%H%M%SZ).md.
4) SOURCE EXPANSION/HARDENING: Extend hunt/deep_review with unauthenticated candidates; enforce GO rubric; harden liquidation vs fills/trades/funding classification with fixtures; cache probes; add tests for rubric edge cases.
5) HARNESS HARDENING + DRY-RUN: Verify fixtures + FCLR-010 offline dry-run. Add adversarial tests if gaps found. Document in research_state/tracka_fclr010_dryrun_hardened_$(date -u +%Y%m%dT%H%M%SZ).md.
6) TESTS + FINAL EVIDENCE: Run python -m unittest discover tests (must stay green). Write research_state/liquidation_forward_validate_008_blocker_$(date -u +%Y%m%dT%H%M%SZ).md (full probe tables, bottleneck metrics, caches/ETags, resume conditions, GO rubric, dry-run results, next-action). Update research_state/experiment_frontier.json (last_checked UTC, blocked status, next_action_heavy). Update AGENT_HANDOFF.md with timestamped next task.

RESUME CONDITION (ONLY UNBLOCK): ironflow data/events/YYYY-MM.parquet or data/fills/YYYY-MM.parquet for any month >=2026-11 returns HTTP 200 unauthenticated (via monitor) OR new admissible unauthenticated source passes strict GO rubric. Hyperliquid-only for Track A.

STOP RULE: Complete ALL 6 steps + artifacts. Never stop early for "no data". Track C locked. No conflation. No schedulers/pollers/status-only files/wrappers/workflow changes. Preregister BEFORE inspecting outcomes if triggered.
```

## VERIFICATION
- `python -m unittest discover tests` (133 tests OK)
- `python scripts/monitor_ironflow_liquidations.py --quick` (blocked)
- `python scripts/hunt_alternative_liquidation_sources.py`
- `python scripts/deep_review_alt_sources.py`
- `python scripts/generate_tracka_fixtures.py`

## NEXT TASK (TIMESTAMPED)
20261105T061238Z: Execute FCLR-NEXT-086 (Track A liquidation-risk heavy maintenance while blocked). Volatility SEALED/LOCKED; Liquidation Risk sole active focus. NO NEW DATA expected. Run monitor_ironflow_liquidations.py --quick + deep_review + hunt; if trigger (ironflow>=2026-11 OR rubric-GO unauthenticated source) HALT + PREREGISTER before outcomes + run ONLY frozen FCLR-010 harness. Else consolidate artifacts (>=40% reduction), harden source rubric + fixtures, dry-run FCLR-010 offline, add tests, run unittest (stay green), write liquidation_forward_validate_009_blocker_$(date).md + update experiment_frontier.json + this handoff. Track C/B locked. No schedulers/pollers/status-only files/wrappers/workflow changes. Hyperliquid-only.
