# AGENT_HANDOFF.md (SINGLE DURABLE HANDOFF)
Timestamp (UTC): 20261105T011841Z
Git SHA (HEAD): 5f475208064b8281924d0542fd4801f71adc38fc
Branch: main
Repo: Funding-conditioned-volatility-and-liquidation-risk
Handoff ID: FCLR-HANDOFF-20261105T011841Z | Priority: P0 - REPO-NAME PRIORITIZED + BOTTLENECKS REMOVED | Mode: CAMPAIGN-DRIVEN | Enforcement: NO-SKIP

## REPO-NAME PRIORITIZATION (INFERRED)
Repository name: "Funding-conditioned-volatility-and-liquidation-risk"
- Funding-conditioned VOLATILITY component = Track C (FCLR-011) — COMPLETE/SEALED/LOCKED. Forecast gate PASSED on frozen splits. DO NOT retune/re-run sealed cells.
- Liquidation RISK component = Track A (FCLR-010) — BLOCKED on admissible unauthenticated liquidation data (ironflow data_through=2026-10; no month >=2026-11 returns HTTP 200). THIS IS THE UNFULFILLED HALF - HIGHEST ACTIVE PRIORITY.
Inference: Volatility done; liquidation risk is the repo's unfulfilled half and must be the sole focus.

## CURRENT VERIFIED STATE
- Tests: suite green (pytest), 179 passed (>=166 floor met). REGRESSION FIXED this session: commits after f15adc3f gutted scripts/hunt_alternative_liquidation_sources.py (34 stub lines, dropped _cache_save/_cache_load/_cache_fresh/http_probe/http_probe_cached/SEARCH_TTL_SECONDS/etc.) and scripts/monitor_ironflow_liquidations.py (dropped FAST_PATH_STATE/load_fastpath_cache/save_fastpath_cache/tree_get_cached), dropping the suite to 165 passed / 14 failed. Restored the cache API to both scripts; suite back to 179 passed. Do NOT regress.
- Bottlenecks removed (hardened baseline, DO NOT regress): consolidated alt_source_scan_*.json to single latest; consolidated alt_source_deep_review_*.md to single latest. monitor_ironflow_liquidations.py has ETag/tree cache, HEAD-404 fast path, forward-edge-only resume probe, baseline-drift state-only skip on 304, per-file ETag/LM caching, fastpath cache. hunt_alternative_liquidation_sources.py has 24h HF search cache, 6h per-URL probe cache, URL dedup, merged DEEP_REVIEW_URLS. deep_review_alt_sources.py reuses hunt's shared URL probe cache. No schedulers/pollers/status-only files/repeated wrappers.
- Track C: SEALED/LOCKED. Track B: NOT_SUPPORTED. Track A: ON TRIGGER/MONITOR ONLY, blocked on data.
- Last confirmed blocked via scripts/monitor_ironflow_liquidations.py --quick (20261104T233118Z context): data_through=2026-10; forward edge 2026-11..2027-02 head-probed absent; probe_diff added=0 changed=0 removed=0; baseline_drift intact.
- experiment_frontier.json (20261104T233118Z last_checked): TRACK_A blocked, resume on ironflow data/events/YYYY-MM.parquet or data/fills/YYYY-MM.parquet >=2026-11 HTTP 200 unauthenticated OR rubric-GO alternative source. Track C blocked past 2026-11-02 (Binance archive ends). FCLR-010 gate PASSED (sealed), FCLR-011 gate PASSED (sealed), FCLR-012-V INCONCLUSIVE (0 test blocks, CI spans zero).

## SINGLE INITIAL TASK MESSAGE FOR NEXT AGENTIC SESSION (COPY/PASTE VERBATIM)
```text
TASK ID: FCLR-NEXT-079-TRACK-A-HEAVY-BOTTLENECK-CAMPAIGN
PRIORITY: P0 - REPO-NAME PRIORITIZED (Funding-conditioned volatility DONE/LOCKED; Liquidation risk ONLY ACTIVE FOCUS - BLOCKED ON DATA)
TIMESTAMP (UTC): 20261105T011841Z
CAMPAIGN: TRACK A LIQUIDATION-RISK - FORCE HEAVY BOTTLENECK REMOVAL WHILE BLOCKED, HARDEN TRIGGERS, NEVER CONCLUDE "NO DATA"

OBJECTIVE (INFERRED FROM REPO NAME): Funding-conditioned volatility is complete/locked. ALL effort must go to liquidation risk (Track A). Data blocked (ironflow data_through=2026-10, no >=2026-11). You CANNOT stop because "no data". While blocked, you MUST aggressively find and remove real bottlenecks, harden automation/triggers/caches/classification so the moment data appears, an agent can resume FCLR-010 with zero wasted time. Eliminate inefficiencies. Do NOT add schedulers/pollers/status-only files/repeated wrappers.

CONSTRAINTS: No credentials/manual files/.github/workflows changes. Leakage-safe, preregister-before-outcomes. Track C/B remain locked/unsupported. Raw data/caches out of git. Clean-clone reproducible.

MANDATORY EXECUTION (IN ORDER - ALL REQUIRED, SESSION INCOMPLETE IF ANY SKIPPED):
1) STATE SWEEP (>=200 lines): Read RESEARCH_PROMPT.md, AGENT_HANDOFF.md, research_state/experiment_frontier.json, research_state/run_manifest.json, scripts/monitor_ironflow_liquidations.py, scripts/hunt_alternative_liquidation_sources.py, scripts/deep_review_alt_sources.py. Write research_state/campaign_sweep_tracka_$(date -u +%Y%m%dT%H%M%SZ).md with concrete evidence, diff vs latest sweep, confirm no new redundant status-only artifacts added.
2) TRIGGER PROBE (FULL TABLES): Run scripts/monitor_ironflow_liquidations.py --quick, scripts/deep_review_alt_sources.py, scripts/hunt_alternative_liquidation_sources.py. Log EVERY checked URL/path/pattern, status/headers/mtime/body previews, ETag/TTL, cached hits, baseline-drift. If >=2026-11 ironflow OR rubric-GO alternative appears -> HALT inspection, PREREGISTER in research_state/fclr010_prereg_$(date -u +%Y%m%dT%H%M%SZ).json BEFORE inspecting outcomes (hypothesis/frozen splits/metrics/stop rule), run ONLY frozen FCLR-010 harness. Else write "NO NEW DATA - ON HOLD" with complete tables.
3) BOTTLENECK REMOVAL (CONCRETE, >=1 REAL FIX): Find real bottlenecks (duplication, slow probes, missing cache, weak classification, retry/backoff, I/O, redundant artifact churn). Fix in scripts/ (prefer monitor_ironflow_liquidations.py, hunt_alternative_liquidation_sources.py, deep_review_alt_sources.py). Provide before/after evidence (diff + timing/behavior). Consolidate duplicates keeping latest. Remove wasteful patterns.
4) TEST HARDENING: Add/extend targeted tests in tests/test_monitor_ironflow.py or new tests (ETag/TTL, state-diff, month-windowing, candidate classification, failure modes, baseline-drift). Run python -m pytest tests/ -q (must remain green; >=166 passing).
5) BLOCKER+FRONTIER+HANDOFF: Write fresh research_state/liquidation_forward_validate_005_blocker_$(date -u +%Y%m%dT%H%M%SZ).md (full probe tables, ETag/cache, exact checkable resume conditions). Update/create research_state/experiment_frontier.json with precise resume triggers, last_checked UTC, blocked status. Update AGENT_HANDOFF.md with timestamped next task.

RESUME CONDITION (ONLY UNBLOCK): ironflow data/events/YYYY-MM.parquet or data/fills/YYYY-MM.parquet for any month >=2026-11 returns HTTP 200 unauthenticated (via monitor) OR new admissible unauthenticated source passes strict GO rubric (>=5 symbols, >=1 complete month OR >=3x30d blocks, documented coverage/completeness, permissive license, no keys/signed/requester-pays, schema compatible with frozen FCLR-010). Hyperliquid-only for Track A.
STOP RULE: Complete ALL 5 steps + artifacts. Never stop early for "no data". Track C locked. No conflation of tracks. No schedulers/pollers/status-only files/wrappers/workflow changes.
```

## VERIFICATION
- `python -m pytest tests/ -q` (179 passed)
- `python scripts/monitor_ironflow_liquidations.py --quick` (blocked: data_through 2026-10)
- `python scripts/hunt_alternative_liquidation_sources.py`
- `python scripts/deep_review_alt_sources.py`

## NEXT TASK (TIMESTAMPED)
20261105T011841Z: Execute FCLR-NEXT-079 above in full. Prioritize liquidation risk (Track A). Remove bottlenecks while blocked, harden triggers, keep artifacts consolidated. Do not touch Track C. If resume conditions met at any point, preregister before inspecting outcomes. Confirm tests stay green (>=166) before ending the session.
