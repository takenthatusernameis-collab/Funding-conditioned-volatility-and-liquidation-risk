# AGENT_HANDOFF.md (SINGLE DURABLE HANDOFF)
Timestamp (UTC): 20261105T032100Z
Git SHA (HEAD): 83e151d03dc1046b9af405e8c26f2c6b94c7614b
Branch: main
Repo: Funding-conditioned-volatility-and-liquidation-risk
Handoff ID: FCLR-HANDOFF-20261105T032100Z | Priority: P0 - REPO-NAME PRIORITIZED + HEAVY WORK ENFORCED | Mode: CAMPAIGN-DRIVEN | Enforcement: NO-SKIP

## REPO-NAME PRIORITIZATION (INFERRED)
Repository name: "Funding-conditioned-volatility-and-liquidation-risk"
- Funding-conditioned VOLATILITY component = Track C (FCLR-011) — SEALED/LOCKED. Forecast gate PASSED. DO NOT retune, re-run sealed cells, or conflate.
- Liquidation RISK component = Track A (FCLR-010) — UNFULFILLED HALF. THIS IS THE ONLY ACTIVE FOCUS. Currently BLOCKED on admissible unauthenticated liquidation data.
Inference: Volatility is complete. Liquidation risk is the repo's unfulfilled objective and must receive 100% of session effort until a valid resume condition is met.

## CURRENT VERIFIED STATE
- Tests: suite green (pytest), 180 passed (>=166 floor met). DO NOT regress. Verified at HEAD bff485f5.
- FCLR-NEXT-080 (prior heavy campaign) COMPLETE across checkpoint commits 5f475208..bff485f5: source expansion+classification hardening (scripts/hunt_alternative_liquidation_sources.py +446), fixture-driven FCLR-010 dry-run (scripts/generate_tracka_fixtures.py +130, tests/fixtures/tracka/), monitor hardening (scripts/monitor_ironflow_liquidations.py +115), test hardening (tests/test_monitor_ironflow.py +25, 179->180), bottleneck consolidation (monitor auto-consolidates ironflow_probe_*/trend reports).
- Track C: SEALED/LOCKED. Track B: NOT_SUPPORTED. Track A: ON-TRIGGER/MONITOR ONLY, blocked on data.
- Last confirmed blocked (scripts/monitor_ironflow_liquidations.py --quick ~20261105T012638Z): data_through=2026-10; forward edge 2026-11..2027-02 head-probed absent; probe_diff added=0 changed=0 removed=0; baseline_drift intact.
- experiment_frontier.json: TRACK_A blocked, resume on ironflow data/events/YYYY-MM.parquet or data/fills/YYYY-MM.parquet >=2026-11 HTTP 200 unauthenticated OR rubric-GO alternative source. Track C blocked past 2026-11-02.
- Bottleneck: artifact churn — research_state/ironflow_probe_*.json still ~109 files (down from ~326; consolidation added but must run on monitor entry). treat consolidation as required before declaring step 5 done.

## SINGLE INITIAL TASK MESSAGE FOR NEXT AGENTIC SESSION (COPY/PASTE VERBATIM)
```text
TASK ID: FCLR-NEXT-082-TRACK-A-VERIFY-AND-HOLD-WHILE-BLOCKED
PRIORITY: P0 - REPO-NAME PRIORITIZED (Volatility DONE/LOCKED; Liquidation Risk ONLY)
TIMESTAMP (UTC): 20261105T032100Z
CAMPAIGN: TRACK A LIQUIDATION-RISK - VERIFY PRIOR HEAVY WORK + KEEP FCLR-010 HARNESS READY; FORCE HEAVY, MEASURABLE PROGRESS WHILE DATA-BLOCKED. DO NOT COAST.
ENFORCEMENT: ALL STEPS MANDATORY. SESSION INCOMPLETE IF ANY SKIPPED.

OBJECTIVE (INFERRED FROM REPO NAME): With funding-conditioned volatility sealed, the liquidation-risk half is the sole unfinished objective. Data is currently blocked. You CANNOT conclude "no data" and stop. While blocked, you MUST force heavy, measurable work: verify all prior FCLR-NEXT-080 artifacts are present and non-redundant, run the full trigger probe to confirm/resume, keep the frozen FCLR-010 harness invocation-ready against fixtures offline (zero decision latency when data appears), extend the GO rubric/source coverage, remove the remaining artifact-churn bottleneck, and leave concrete executable evidence. Make it impossible for a future agent to avoid doing heavy work.

CONSTRAINTS: No credentials/manual files/.github/workflows changes. Leakage-safe, preregister-before-outcomes. Track C/B remain locked/unsupported. Raw data/caches out of git. Clean-clone reproducible. No schedulers/pollers/status-only files/repeated wrappers/agent-controllers.

MANDATORY EXECUTION (IN ORDER - ALL REQUIRED):
1) STATE SWEEP (>=250 lines): Read RESEARCH_PROMPT.md, AGENT_HANDOFF.md, research_state/experiment_frontier.json, research_state/run_manifest.json, scripts/monitor_ironflow_liquidations.py, scripts/hunt_alternative_liquidation_sources.py, scripts/deep_review_alt_sources.py, scripts/generate_tracka_fixtures.py, tests/test_monitor_ironflow.py. Confirm FCLR-NEXT-080 steps 1-6 are complete and artifact locations. Write research_state/campaign_sweep_tracka_$(date -u +%Y%m%dT%H%M%SZ).md with concrete evidence, artifact count (ensure no new redundant status-only artifacts), diff vs latest sweep, and a "bottlenecks found" list with measurable fixes (include ironflow_probe_*.json churn count).
2) TRIGGER PROBE (FULL TABLES): Run scripts/monitor_ironflow_liquidations.py --quick (this auto-consolidates ironflow probe/trend artifacts), scripts/deep_review_alt_sources.py, scripts/hunt_alternative_liquidation_sources.py. Log EVERY checked URL/path/pattern, method, status/headers/ETag/Last-Modified/mtime, body preview, cache hit/miss/TTL, baseline-drift, probe_diff. If >=2026-11 ironflow OR rubric-GO alternative appears -> HALT inspection, PREREGISTER in research_state/fclr010_prereg_$(date -u +%Y%m%dT%H%M%SZ).json BEFORE inspecting outcomes (hypothesis, frozen splits, features/targets, metrics, stop rule, data hashes) and run ONLY the frozen FCLR-010 harness. Else write "NO NEW DATA - ON HOLD" with complete tables in research_state/trigger_probe_tracka_$(date -u +%Y%m%dT%H%M%SZ).md.
3) HARNESS READINESS (HEAVY): Verify scripts/generate_tracka_fixtures.py dry-run path validates FCLR-010 against tests/fixtures/tracka/ fixtures WITHOUT network: preregistration loading, frozen splits, feature computation with train-only normalization, leakage guards, metric computation. Confirm the frozen harness can be invoked offline so zero latency on resume. Document pass/fail + exact commands in research_state/tracka_fclr010_dryrun_$(date -u +%Y%m%dT%H%M%SZ).md. Pre-write a fclr010 preregistration template (hypothesis/frozen splits/features/targets/metrics/stop rule) ready to instantiate on trigger.
4) SOURCE EXPANSION + CLASSIFICATION HARDENING (HEAVY): Extend scripts/hunt_alternative_liquidation_sources.py to probe additional unauthenticated candidates with strict dedup, per-URL probe cache, and hardened GO rubric (>=5 symbols OR >=1 complete month OR >=3x30d blocks, documented coverage/completeness, permissive/license-safe, no keys/signed/requester-pays, schema compatible with frozen FCLR-010; prefer Hyperliquid/venue-native public archives). Harden candidate classification (liquidation vs fills vs trades vs funding) with fixtures. Add/extend tests for rubric edge cases. Every new probe cached.
5) BOTTLENECK REMOVAL + TIMING (CONCRETE): Run monitor (auto-consolidates ironflow_probe_*/trend reports). Profile monitor/hunt/deep_review timing before/after. Remove remaining duplication (URL lists, consolidation), unify caches, tighten backoff/retries, reduce redundant I/O. Fix at least ONE real bottleneck with before/after diff + timing/behavior evidence (target: reduce ironflow_probe_*.json count materially).
6) TEST HARDENING + EVIDENCE: Extend tests/test_monitor_ironflow.py and/or add targeted tests for rubric/classification/dry-run/consolidation. Run python -m pytest tests/ -q (must remain >=180 passing; do NOT drop). Write research_state/liquidation_forward_validate_006_blocker_$(date -u +%Y%m%dT%H%M%SZ).md (full probe tables, caches/ETags, resume conditions, GO rubric, dry-run results). Update research_state/experiment_frontier.json with precise resume triggers, last_checked UTC, blocked status, and "next_action_heavy" pointing to artifacts. Update AGENT_HANDOFF.md with timestamped next task.

RESUME CONDITION (ONLY UNBLOCK): ironflow data/events/YYYY-MM.parquet or data/fills/YYYY-MM.parquet for any month >=2026-11 returns HTTP 200 unauthenticated (via monitor) OR new admissible unauthenticated source passes strict GO rubric. Hyperliquid-only for Track A.
STOP RULE: Complete ALL 6 steps + artifacts. Never stop early for "no data". Track C locked. No conflation. No schedulers/pollers/status-only files/wrappers/workflow changes. Preregister BEFORE inspecting outcomes if triggered.
```

## VERIFICATION
- `python -m pytest tests/ -q` (180 passed)
- `python scripts/monitor_ironflow_liquidations.py --quick` (blocked: data_through 2026-10; auto-consolidates artifacts)
- `python scripts/hunt_alternative_liquidation_sources.py`
- `python scripts/deep_review_alt_sources.py`
- Dry-run offline: scripts/generate_tracka_fixtures.py against tests/fixtures/tracka/ (no network)

## NEXT TASK (TIMESTAMPED)
20261105T032100Z: Execute FCLR-NEXT-082 above in full. Prioritize liquidation risk (Track A) exclusively. Verify prior heavy work (FCLR-NEXT-080 complete), run full trigger probe, keep FCLR-010 harness invocation-ready offline, extend rubric/source coverage, remove artifact-churn bottleneck (ironflow_probe_*.json), keep tests green (>=180). Leave concrete, executable evidence for the next session. Do not touch Track C. If resume conditions met at any point, preregister BEFORE inspecting outcomes and run ONLY frozen FCLR-010 harness.
