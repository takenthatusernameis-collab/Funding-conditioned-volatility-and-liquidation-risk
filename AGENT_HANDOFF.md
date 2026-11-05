# AGENT_HANDOFF.md (SINGLE DURABLE HANDOFF)
Timestamp (UTC): 20261105T014500Z
Git SHA (HEAD): 5f475208064b8281924d0542fd4801f71adc38fc
Branch: main
Repo: Funding-conditioned-volatility-and-liquidation-risk
Handoff ID: FCLR-HANDOFF-20261105T014500Z | Priority: P0 - REPO-NAME PRIORITIZED + HEAVY WORK ENFORCED | Mode: CAMPAIGN-DRIVEN | Enforcement: NO-SKIP

## REPO-NAME PRIORITIZATION (INFERRED)
Repository name: "Funding-conditioned-volatility-and-liquidation-risk"
- Funding-conditioned VOLATILITY component = Track C (FCLR-011) — SEALED/LOCKED. Forecast gate PASSED. DO NOT retune, re-run sealed cells, or conflate.
- Liquidation RISK component = Track A (FCLR-010) — UNFULFILLED HALF. THIS IS THE ONLY ACTIVE FOCUS. Currently BLOCKED on admissible unauthenticated liquidation data.
Inference: Volatility is complete. Liquidation risk is the repo's unfulfilled objective and must receive 100% of session effort until a valid resume condition is met.

## CURRENT VERIFIED STATE
- Tests: suite green (pytest), 180 passed (>=166 floor met). DO NOT regress.
- Bottlenecks already removed (consolidated alt-source artifacts, hardened caches/ETags/fast-paths, state-diffing). Treat these as hardened baselines, not finished work.
- Track C: SEALED/LOCKED. Track B: NOT_SUPPORTED. Track A: ON-TRIGGER/MONITOR ONLY, blocked on data.
- Last confirmed blocked (scripts/monitor_ironflow_liquidations.py --quick ~20261104T233118Z): data_through=2026-10; forward edge 2026-11..2027-02 head-probed absent; probe_diff added=0 changed=0 removed=0; baseline_drift intact.
- experiment_frontier.json: TRACK_A blocked, resume on ironflow data/events/YYYY-MM.parquet or data/fills/YYYY-MM.parquet >=2026-11 HTTP 200 unauthenticated OR rubric-GO alternative source. Track C blocked past 2026-11-02.

## SINGLE INITIAL TASK MESSAGE FOR NEXT AGENTIC SESSION (COPY/PASTE VERBATIM)
```text
TASK ID: FCLR-NEXT-080-TRACK-A-FORCE-HEAVY-PROGRESS-WHILE-BLOCKED
PRIORITY: P0 - REPO-NAME PRIORITIZED (Volatility DONE/LOCKED; Liquidation Risk ONLY)
TIMESTAMP (UTC): 20261105T014500Z
CAMPAIGN: TRACK A LIQUIDATION-RISK - GENERATE IRREFUTABLE PROGRESS WHILE DATA-BLOCKED. DO NOT COAST.
ENFORCEMENT: ALL STEPS MANDATORY. SESSION INCOMPLETE IF ANY SKIPPED.

OBJECTIVE (INFERRED FROM REPO NAME): With funding-conditioned volatility sealed, the liquidation-risk half is the sole unfinished objective. Data is currently blocked. You CANNOT conclude "no data" and stop. While blocked, you MUST force heavy, measurable work: expand admissible source coverage, harden triggers/classification/schema mapping, build a fixture-driven dry-run of the frozen FCLR-010 harness, and eliminate any remaining bottlenecks/duplication. Make it impossible for a future agent to avoid doing heavy work by leaving concrete, executable artifacts.

CONSTRAINTS: No credentials/manual files/.github/workflows changes. Leakage-safe, preregister-before-outcomes. Track C/B remain locked/unsupported. Raw data/caches out of git. Clean-clone reproducible. No schedulers/pollers/status-only files/repeated wrappers/agent-controllers.

MANDATORY EXECUTION (IN ORDER - ALL REQUIRED):
1) STATE SWEEP (>=250 lines): Read RESEARCH_PROMPT.md, AGENT_HANDOFF.md, research_state/experiment_frontier.json, research_state/run_manifest.json, scripts/monitor_ironflow_liquidations.py, scripts/hunt_alternative_liquidation_sources.py, scripts/deep_review_alt_sources.py, tests/test_monitor_ironflow.py. Write research_state/campaign_sweep_tracka_$(date -u +%Y%m%dT%H%M%SZ).md with concrete evidence, diff vs latest sweep, artifact count (ensure no new redundant status-only artifacts), and a "bottlenecks found" list with measurable fixes.
2) TRIGGER PROBE (FULL TABLES): Run scripts/monitor_ironflow_liquidations.py --quick, scripts/deep_review_alt_sources.py, scripts/hunt_alternative_liquidation_sources.py. Log EVERY checked URL/path/pattern, method, status/headers/ETag/Last-Modified/mtime, body preview, cache hit/miss/TTL, baseline-drift, probe_diff. If >=2026-11 ironflow OR rubric-GO alternative appears -> HALT inspection, PREREGISTER in research_state/fclr010_prereg_$(date -u +%Y%m%dT%H%M%SZ).json BEFORE inspecting outcomes (hypothesis, frozen splits, features/targets, metrics, stop rule, data hashes) and run ONLY the frozen FCLR-010 harness. Else write "NO NEW DATA - ON HOLD" with complete tables in research_state/trigger_probe_tracka_$(date -u +%Y%m%dT%H%M%SZ).md.
3) SOURCE EXPANSION + CLASSIFICATION HARDENING (HEAVY): Extend scripts/hunt_alternative_liquidation_sources.py to probe additional unauthenticated candidates with strict dedup, per-URL probe cache, and a hardened GO rubric (>=5 symbols OR >=1 complete month OR >=3x30d blocks, documented coverage/completeness, permissive/license-safe, no keys/signed/requester-pays, schema compatible with frozen FCLR-010; prefer Hyperliquid/venue-native public archives). Harden candidate classification (liquidation vs fills vs trades vs funding) with fixtures. Add/extend tests for rubric edge cases. Every new probe must be cached.
4) FIXTURE-DRIVEN DRY-RUN OF FCLR-010 (IRREFUTABLE PROGRESS): Create fixtures under tests/fixtures/tracka/ (minimal synthetic parquet/csv with required schema) and add a dry-run test path (or script) that validates: preregistration loading, frozen splits, feature computation with train-only normalization, leakage guards, and metric computation. Ensure the frozen harness can be invoked against fixtures without network. Document in research_state/tracka_fclr010_dryrun_$(date -u +%Y%m%dT%H%M%SZ).md with exact commands + pass/fail.
5) BOTTLENECK REMOVAL + TIMING (CONCRETE): Profile monitor/hunt/deep_review (timing before/after). Remove remaining duplication (URL lists, consolidation), unify caches, tighten backoff/retries, reduce redundant I/O. Fix at least ONE real bottleneck with before/after diff + timing/behavior evidence.
6) TEST HARDENING + EVIDENCE: Extend tests/test_monitor_ironflow.py and/or add targeted tests for rubric/classification/dry-run. Run python -m pytest tests/ -q (must remain >=180 passing; do NOT drop). Write research_state/liquidation_forward_validate_006_blocker_$(date -u +%Y%m%dT%H%M%SZ).md (full probe tables, caches/ETags, resume conditions, GO rubric, dry-run results). Update research_state/experiment_frontier.json with precise resume triggers, last_checked UTC, blocked status, and "next_action_heavy" pointing to artifacts. Update AGENT_HANDOFF.md with timestamped next task.

RESUME CONDITION (ONLY UNBLOCK): ironflow data/events/YYYY-MM.parquet or data/fills/YYYY-MM.parquet for any month >=2026-11 returns HTTP 200 unauthenticated (via monitor) OR new admissible unauthenticated source passes strict GO rubric. Hyperliquid-only for Track A.
STOP RULE: Complete ALL 6 steps + artifacts. Never stop early for "no data". Track C locked. No conflation. No schedulers/pollers/status-only files/wrappers/workflow changes. Preregister BEFORE inspecting outcomes if triggered.
```

## VERIFICATION
- `python -m pytest tests/ -q` (180 passed)
- `python scripts/monitor_ironflow_liquidations.py --quick` (blocked: data_through 2026-10)
- `python scripts/hunt_alternative_liquidation_sources.py`
- `python scripts/deep_review_alt_sources.py`

## NEXT TASK (TIMESTAMPED)
20261105T014500Z: Execute FCLR-NEXT-080 above in full. Prioritize liquidation risk (Track A) exclusively. Force heavy progress while blocked (source expansion + classification hardening + fixture-driven FCLR-010 dry-run + bottleneck removal). Keep artifacts consolidated. Do not touch Track C. If resume conditions met at any point, preregister BEFORE inspecting outcomes and run ONLY frozen FCLR-010 harness. Keep tests green (>=180). Leave concrete, executable evidence for the next session.
