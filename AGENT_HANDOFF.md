# AGENT_HANDOFF.md (SINGLE DURABLE HANDOFF)
Timestamp (UTC): 20261104T213200Z
Git SHA (HEAD): 346e063b
Branch: main
Repo: Funding-conditioned-volatility-and-liquidation-risk
Handoff ID: FCLR-HANDOFF-20261104T213200Z | Priority: P0 - REPO-NAME PRIORITIZED + BOTTLENECK REMOVAL FORCED | Mode: CAMPAIGN-DRIVEN | Enforcement: NO-SKIP

## REPO-NAME PRIORITIZATION (INFERRED)
Repository name: "Funding-conditioned-volatility-and-liquidation-risk"
- Funding-conditioned volatility component: Track C (FCLR-011) — LOCKED/PASSED on frozen splits (rel_imp ~+7.0%, CI excludes zero). No re-tuning.
- Liquidation risk component: Track A (FCLR-010) — BLOCKED on admissible unauthenticated liquidation data (ironflow latest 2026-10; no >=2026-11). Highest active priority.

## CURRENT VERIFIED STATE
- Tests: 166/166 pass. Working tree clean.
- Track C: SEALED/LOCKED (gate passed, robustness done). Track B: NOT_SUPPORTED.
- Track A: ON TRIGGER ONLY. Monitor active; no new data observed in latest probe.
- Bottlenecks exist in detection/hardening while blocked - must be removed every session.

## SINGLE INITIAL TASK MESSAGE FOR NEXT AGENTIC SESSION (COPY/PASTE VERBATIM)
```text
TASK ID: FCLR-NEXT-074-TRACK-A-FORCE-BOTTLENECKS-REMOVE-HEAVY
PRIORITY: P0 - REPO-NAME PRIORITIZED (Funding-conditioned volatility DONE; Liquidation risk NEXT - BLOCKED)
TIMESTAMP (UTC): 20261104T213200Z
CAMPAIGN: TRACK A BOTTLENECK REMOVAL + TRIGGER HARDENING (BLOCKED-DATA MODE - HEAVY WORK MANDATORY)

OBJECTIVE (INFERRED FROM REPO NAME): Funding-conditioned volatility is complete and locked. Focus ALL effort on liquidation risk (Track A). Data is blocked (ironflow data_through=2026-10, no >=2026-11). You CANNOT conclude "no data" and stop. While blocked, you MUST aggressively remove bottlenecks and harden automation so future agents can make immediate progress the moment data appears. Eliminate inefficiencies; do not add schedulers/pollers/status-only files.

CONSTRAINTS: No credentials/manual files/.github/workflows changes. Leakage-safe, preregister-before-outcomes. Track C/B remain locked/unsupported. Raw data out of git; only code/manifests/reports committed.

MANDATORY EXECUTION (IN ORDER, ALL REQUIRED - SESSION FAILS IF ANY SKIPPED):
1) STATE SWEEP (>=200 lines): Read RESEARCH_PROMPT.md, AGENT_HANDOFF.md, research_state/*, scripts/monitor_ironflow_liquidations.py, scripts/hunt_alternative_liquidation_sources.py, scripts/deep_review_alt_sources.py. Write research_state/campaign_sweep_tracka_$(date -u +%Y%m%dT%H%M%SZ).md with concrete evidence and diff vs prior sweep.
2) TRIGGER PROBE (FULL TABLES): Run scripts/monitor_ironflow_liquidations.py --quick, scripts/deep_review_alt_sources.py, scripts/hunt_alternative_liquidation_sources.py. Log EVERY checked URL/path/pattern, status/headers/mtime/body previews, ETag/TTL, cached hits. If >=2026-11 ironflow or rubric-GO alternative appears -> HALT inspection, PREREGISTER in research_state/fclr010_prereg_$(date -u +%Y%m%dT%H%M%SZ).json BEFORE inspecting outcomes (full hypothesis/frozen splits/metrics/stop rule), then run ONLY frozen FCLR-010 harness. Else write "NO NEW DATA - ON HOLD" with complete tables.
3) BOTTLENECK REMOVAL (CONCRETE): Find >=1 real bottleneck (duplication, slow probes, missing cache, weak classification, retry/backoff, I/O). Fix in scripts/ (prefer monitor_ironflow_liquidations.py, hunt_alternative_liquidation_sources.py, deep_review_alt_sources.py). Provide before/after evidence (diff + timing/behavior). Eliminate wasteful patterns.
4) TEST HARDENING: Add/extend tests in tests/test_monitor_ironflow.py or new targeted tests (state-diff, ETag/TTL, month-windowing, candidate classification, failure modes). Run python -m pytest tests/ -q (must remain >=166 passing).
5) BLOCKER+FRONTIER+HANDOFF: Write fresh research_state/liquidation_forward_validate_004_blocker_$(date -u +%Y%m%dT%H%M%SZ).md (full probe tables, ETag/cache, exact checkable resume conditions: paths/patterns/URLs/months >=2026-11, rubric-GO). Update/create experiment_frontier.json with precise resume triggers, last_checked UTC, blocked-cell status. Update AGENT_HANDOFF.md with timestamped next task.

RESUME CONDITION (ONLY UNBLOCK): ironflow data/events/YYYY-MM.parquet or data/fills/YYYY-MM.parquet for any month >=2026-11 returns HTTP 200 unauthenticated (via monitor) OR new admissible unauthenticated source passes strict GO rubric (>=5 symbols, >=1 complete month OR >=3x30d blocks, documented coverage/completeness, permissive license, no keys/signed/requester-pays, schema compatible with frozen FCLR-010). Hyperliquid-only for Track A.

STOP RULE: Complete ALL 5 steps + artifacts. Never stop early for "no data". Track C locked. No conflation of tracks.
```

## VERIFICATION
- `python -m pytest tests/ -q` (166 passed)
- `python scripts/monitor_ironflow_liquidations.py --quick`
- `python scripts/hunt_alternative_liquidation_sources.py`

## NEXT TASK (TIMESTAMPED)
20261104T213200Z: Execute campaign above. Remove bottlenecks while blocked; harden triggers so unblocking is instantaneous and correct.
