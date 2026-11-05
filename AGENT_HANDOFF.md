# AGENT_HANDOFF.md (SINGLE DURABLE HANDOFF)
Timestamp (UTC): 20261105T043559Z
Git SHA (HEAD): 8e8b7e9091b1d89b1020761ffa0423b3d19983ef
Branch: main
Repo: Funding-conditioned-volatility-and-liquidation-risk
Handoff ID: FCLR-HANDOFF-20261105T045000Z | Priority: P0 - REPO-NAME PRIORITIZED + HEAVY WORK ENFORCED | Mode: CAMPAIGN-DRIVEN | Enforcement: NO-SKIP

## REPO-NAME PRIORITIZATION (INFERRED)
Repository name: "Funding-conditioned-volatility-and-liquidation-risk"
- Funding-conditioned VOLATILITY component = Track C (FCLR-011) — SEALED/LOCKED. Forecast gate PASSED. DO NOT retune, re-run sealed cells, or conflate.
- Liquidation RISK component = Track A (FCLR-010) — UNFULFILLED HALF. THIS IS THE ONLY ACTIVE FOCUS. Currently BLOCKED on admissible unauthenticated liquidation data.
Inference: Volatility is complete. Liquidation risk is the repo's unfulfilled objective and must receive 100% of session effort until a valid resume condition is met.

## CURRENT VERIFIED STATE
- Tests: suite green (pytest), 180 passed (>=166 floor met). DO NOT regress. Verified at HEAD e5f060f9.
- FCLR-NEXT-083 (prior heavy campaign) COMPLETE: verified FCLR-NEXT-082 artifacts, ran full trigger probe (monitor --quick, deep_review, hunt), confirmed no resume trigger, verified FCLR-010 harness dry-run offline, extended source/rubric coverage paths, consolidated artifacts, tests green.
- Track C: SEALED/LOCKED. Track B: NOT_SUPPORTED. Track A: ON-TRIGGER/MONITOR ONLY, blocked on data.
- Last confirmed blocked (scripts/monitor_ironflow_liquidations.py --quick ~20261105T033318Z): data_through=2026-10; forward edge 2026-11..2027-02 head-probed absent; probe_diff added=0 changed=0 removed=0; baseline_drift intact.
- experiment_frontier.json: TRACK_A blocked, resume on ironflow data/events/YYYY-MM.parquet or data/fills/YYYY-MM.parquet >=2026-11 HTTP 200 unauthenticated OR rubric-GO alternative source. Track C blocked past 2026-11-02.
- Bottleneck: artifact churn — research_state/ironflow_probe_*.json still ~109 files (consolidation exists but not aggressively enforced/trimmed). This MUST be reduced measurably this session.

## SINGLE INITIAL TASK MESSAGE FOR NEXT AGENTIC SESSION (COPY/PASTE VERBATIM)
```text
TASK ID: FCLR-NEXT-084-TRACK-A-BOTTLENECK-DEMOLITION-AND-SOURCE-HARDENING
PRIORITY: P0 - REPO-NAME PRIORITIZED (Volatility DONE/LOCKED; Liquidation Risk ONLY)
TIMESTAMP (UTC): 20261105T045000Z
CAMPAIGN: TRACK A LIQUIDATION-RISK - DEMOLISH BOTTLENECKS WHILE BLOCKED; FORCE HEAVY, MEASURABLE PROGRESS. DO NOT COAST.
ENFORCEMENT: ALL STEPS MANDATORY. SESSION INCOMPLETE IF ANY SKIPPED.

OBJECTIVE (INFERRED FROM REPO NAME): With funding-conditioned volatility sealed, liquidation risk is the sole unfinished objective. Data remains blocked (ironflow through 2026-10; 2026-11+ absent). While blocked, you MUST create progress that CANNOT be avoided by future agents: aggressively reduce artifact churn, harden source discovery to the absolute maximum of unauthenticated venues, make the FCLR-010 harness zero-latency on resume, add adversarial tests, and leave undeniable executable evidence. If resume triggers appear at any point, PREREGISTER BEFORE INSPECTING OUTCOMES and run ONLY the frozen FCLR-010 harness.

CONSTRAINTS: No credentials/manual files/.github/workflows changes. Leakage-safe, preregister-before-outcomes. Track C/B remain locked/unsupported. Raw data/caches out of git. Clean-clone reproducible. No schedulers/pollers/status-only files/repeated wrappers/agent-controllers. Hyperliquid-only for Track A.

MANDATORY EXECUTION (IN ORDER - ALL REQUIRED):
1) BASELINE METRICS (MEASURABLE): Count ironflow_probe_*.json, trend files, alt-source caches, total research_state size. Record in research_state/campaign_sweep_tracka_$(date -u +%Y%m%dT%H%M%SZ).md with before-metrics. Time monitor --quick, hunt, deep_review. These numbers MUST improve.

2) TRIGGER PROBE (FULL TABLES): Run scripts/monitor_ironflow_liquidations.py --quick (must auto-consolidate), scripts/deep_review_alt_sources.py, scripts/hunt_alternative_liquidation_sources.py. Log EVERY checked URL/path/pattern, method, status/headers/ETag/Last-Modified/mtime, body preview, cache hit/miss/TTL, baseline-drift, probe_diff. If >=2026-11 ironflow OR rubric-GO alternative appears -> HALT, PREREGISTER in research_state/fclr010_prereg_$(date -u +%Y%m%dT%H%M%SZ).json BEFORE inspecting outcomes (hypothesis, frozen splits, features/targets, metrics, stop rule, data hashes), run ONLY frozen FCLR-010 harness. Else write "NO NEW DATA - ON HOLD" with complete tables in research_state/trigger_probe_tracka_$(date -u +%Y%m%dT%H%M%SZ).md.

3) BOTTLENECK DEMOLITION (HEAVY): Aggressively consolidate ironflow_probe_*.json (enforce consolidation on entry, deduplicate by content/hash, retire redundant trend snapshots, cap retention). Unify URL lists/caches across hunt/deep_review/monitor. Tighten backoff/retries. Remove duplication. Fix at least TWO concrete bottlenecks with before/after diff, timing (seconds), file counts, and I/O reduction. Target: ironflow_probe_*.json count reduced by >=40% from baseline. Document in research_state/bottleneck_demolition_$(date -u +%Y%m%dT%H%M%SZ).md.

4) SOURCE EXPANSION (EXHAUSTIVE): Extend scripts/hunt_alternative_liquidation_sources.py with additional unauthenticated candidates (venue-native archives, public mirrors). Harden GO rubric (>=5 symbols OR >=1 complete month OR >=3x30d blocks, documented coverage/completeness, permissive/license-safe, no keys/signed/requester-pays, schema compatible with frozen FCLR-010). Treat Kaggle metadata mirror as TRIGGER ONLY (never download). Harden liquidation vs fills vs trades vs funding classification with fixtures. Cache every probe. Add tests for rubric edge cases.

5) HARNESS HARDENING + DRY-RUN (HEAVY): Verify scripts/generate_tracka_fixtures.py produces fixtures and FCLR-010 can run fully offline. Add adversarial tests (leakage guards, frozen split enforcement, train-only normalization). Ensure prereg template is instantiable in <60s. Document in research_state/tracka_fclr010_dryrun_hardened_$(date -u +%Y%m%dT%H%M%SZ).md with exact commands + pass/fail.

6) TESTS + FINAL EVIDENCE (MANDATORY): Extend tests/test_monitor_ironflow.py and add targeted tests. Run python -m pytest tests/ -q (must remain >=180 passing; do NOT drop). Write research_state/liquidation_forward_validate_007_blocker_$(date -u +%Y%m%dT%H%M%SZ).md (full probe tables, bottleneck metrics before/after, caches/ETags, resume conditions, GO rubric, dry-run results, next-action). Update research_state/experiment_frontier.json with precise resume triggers, last_checked UTC, blocked status, "next_action_heavy" pointing to this artifact. Update AGENT_HANDOFF.md with timestamped next task.

RESUME CONDITION (ONLY UNBLOCK): ironflow data/events/YYYY-MM.parquet or data/fills/YYYY-MM.parquet for any month >=2026-11 returns HTTP 200 unauthenticated (via monitor) OR new admissible unauthenticated source passes strict GO rubric. Hyperliquid-only for Track A.
STOP RULE: Complete ALL 6 steps + artifacts. Never stop early for "no data". Track C locked. No conflation. No schedulers/pollers/status-only files/wrappers/workflow changes. Preregister BEFORE inspecting outcomes if triggered.
```

## VERIFICATION
- `python -m pytest tests/ -q` (180 passed)
- `python scripts/monitor_ironflow_liquidations.py --quick` (blocked: data_through 2026-10; auto-consolidates artifacts)
- `python scripts/hunt_alternative_liquidation_sources.py`
- `python scripts/deep_review_alt_sources.py`
- Dry-run offline: `python scripts/generate_tracka_fixtures.py` against tests/fixtures/tracka/

## NEXT TASK (TIMESTAMPED)
20261105T045000Z: Execute FCLR-NEXT-084 above in full. Liquidation risk (Track A) ONLY. Obligatorily demolish bottlenecks (target >=40% reduction in ironflow_probe_*.json), exhaust source discovery, harden FCLR-010 harness to zero-latency offline, add adversarial tests, keep tests green (>=180). Leave concrete before/after metrics and executable evidence. Do not touch Track C/B. Preregister BEFORE inspecting outcomes if triggered.

## HISTORY
- FCLR-NEXT-083 EXECUTED - 20261105T042119Z: Verified prior work, ran full probe, confirmed blocked, harness ready offline, tests green (180).
- FCLR-NEXT-082 EXECUTED - 20261105T033418Z: Full sweep, probe, dry-run, consolidation verified, evidence written.
