# AGENT_HANDOFF.md (SINGLE DURABLE HANDOFF)
Timestamp (UTC): 20261104T223906Z
Git SHA (HEAD): 3be0f274
Branch: main
Repo: Funding-conditioned-volatility-and-liquidation-risk
Handoff ID: FCLR-HANDOFF-20261104T223906Z | Priority: P0 - REPO-NAME PRIORITIZED + BOTTLENECKS REMOVED | Mode: CAMPAIGN-DRIVEN | Enforcement: NO-SKIP

## REPO-NAME PRIORITIZATION (INFERRED)
Repository name: "Funding-conditioned-volatility-and-liquidation-risk"
- Funding-conditioned VOLATILITY component = Track C (FCLR-011) — COMPLETE/LOCKED, forecast gate PASSED on frozen splits (rel_imp ~+7.0%, CI excludes zero). No re-tuning, no re-run of sealed cells.
- Liquidation RISK component = Track A (FCLR-010) — BLOCKED on admissible unauthenticated liquidation data (ironflow data_through=2026-10; no month >=2026-11 returns HTTP 200). HIGHEST ACTIVE PRIORITY. All unfinished work concentrates here.
Inference: volatility is done; liquidation risk is the repo-name's unfulfilled half and is the sole focus of the next session.

## CURRENT VERIFIED STATE
- Tests: suite green (pytest), 179 passed (>=166 floor met). Staged diff is __pycache__ de-tracking (git rm --cached, NOT committed — commit only on explicit request).
- Bottlenecks removed (already done, do NOT regress): 18 near-duplicate alt_source_scan_*.json -> 1 (latest kept); 12 near-duplicate alt_source_deep_review_*.md -> 1 (latest kept). Scripts hardened: monitor_ironflow_liquidations.py (ETag tree cache, HEAD-404 fast path, forward-edge-only resume probe, baseline-drift state-only skip when tree 304, per-file ETag/LM caching), hunt_alternative_liquidation_sources.py (24h HF search cache, 6h per-URL probe cache, URL dedup, merged DEEP_REVIEW_URLS), deep_review_alt_sources.py (reuses hunt's shared URL probe cache instead of re-GETting). Pure status-only repetition eliminated per RESEARCH_PROMPT constraint #23. Do NOT re-add schedulers/pollers/status-only files/repeated wrappers.
- Track C: SEALED/LOCKED. Track B: NOT_SUPPORTED. Track A: ON TRIGGER/MONITOR ONLY, blocked on data.
- Track A last confirmed blocked via scripts/monitor_ironflow_liquidations.py --quick (20261104T223659Z): data_through=2026-10; forward edge 2026-11..2027-02 head-probed absent (404/EntryNotFound); probe_diff added=0 changed=0 removed=0; baseline_drift intact; kaggle_mirror triggered=False. Evidence: research_state/ironflow_probe_20261104T223638Z.json (and prior probes 213437Z/214306Z/214647Z/214814Z).
- Frontier/blocked cells: research_state/experiment_frontier.json (TRACK_A blocked: resume on ironflow data/events/YYYY-MM.parquet or data/fills/YYYY-MM.parquet >=2026-11 HTTP 200 unauthenticated, OR rubric-GO alternative source). last_checked 2026-11-04T21:32:54Z.

## SINGLE INITIAL TASK MESSAGE FOR NEXT AGENTIC SESSION (COPY/PASTE VERBATIM)
```text
TASK ID: FCLR-NEXT-076-TRACK-A-FORCE-BOTTLENECKS-REMOVE-HEAVY
PRIORITY: P0 - REPO-NAME PRIORITIZED (Funding-conditioned volatility DONE/LOCKED; Liquidation risk NEXT - BLOCKED)
TIMESTAMP (UTC): 20261104T223906Z
CAMPAIGN: TRACK A LIQUIDATION-RISK BOTTLENECK REMOVAL + TRIGGER HARDENING (BLOCKED-DATA MODE - HEAVY WORK MANDATORY)

OBJECTIVE (INFERRED FROM REPO NAME): Funding-conditioned volatility is complete and locked. Focus ALL effort on liquidation risk (Track A). Data is blocked (ironflow data_through=2026-10, no >=2026-11). You CANNOT conclude "no data" and stop. While blocked, you MUST aggressively remove bottlenecks and harden automation so future agents make immediate progress the moment data appears. Eliminate inefficiencies; do NOT add schedulers/pollers/status-only files/repeated wrappers. The prior session already removed 18 alt_source_scan + 12 alt_source_deep_review duplicates and added ETag/HEAD caches — start from that hardened baseline, do not regress it.

CONSTRAINTS: No credentials/manual files/.github/workflows changes. Leakage-safe, preregister-before-outcomes. Track C/B remain locked/unsupported. Raw data/caches out of git; only code/manifests/reports committed. Clean-clone reproduction possible.

MANDATORY EXECUTION (IN ORDER, ALL REQUIRED - SESSION FAILS IF ANY SKIPPED):
1) STATE SWEEP (>=200 lines): Read RESEARCH_PROMPT.md, AGENT_HANDOFF.md, research_state/experiment_frontier.json, research_state/run_manifest.json, scripts/monitor_ironflow_liquidations.py, scripts/hunt_alternative_liquidation_sources.py, scripts/deep_review_alt_sources.py. Write research_state/campaign_sweep_tracka_$(date -u +%Y%m%dT%H%M%SZ).md with concrete evidence and diff vs prior sweep. Confirm no new redundant status-only files were added.
2) TRIGGER PROBE (FULL TABLES): Run scripts/monitor_ironflow_liquidations.py --quick, scripts/deep_review_alt_sources.py, scripts/hunt_alternative_liquidation_sources.py. Log EVERY checked URL/path/pattern, status/headers/mtime/body previews, ETag/TTL, cached hits. If >=2026-11 ironflow or rubric-GO alternative appears -> HALT inspection, PREREGISTER in research_state/fclr010_prereg_$(date -u +%Y%m%dT%H%M%SZ).json BEFORE inspecting outcomes (full hypothesis/frozen splits/metrics/stop rule), then run ONLY frozen FCLR-010 harness. Else write "NO NEW DATA - ON HOLD" with complete tables.
3) BOTTLENECK REMOVAL (CONCRETE, >=1 real fix): Find a real bottleneck (duplication, slow probes, missing cache, weak classification, retry/backoff, I/O). Fix in scripts/ (prefer monitor_ironflow_liquidations.py, hunt_alternative_liquidation_sources.py, deep_review_alt_sources.py). Provide before/after evidence (diff + timing/behavior). Eliminate wasteful/redundant patterns; consolidate near-duplicate artifacts keeping latest.
4) TEST HARDENING: Add/extend tests in tests/test_monitor_ironflow.py or new targeted tests (state-diff, ETag/TTL, month-windowing, candidate classification, failure modes). Run python -m pytest tests/ -q (must remain green; >=166 passing).
5) BLOCKER+FRONTIER+HANDOFF: Write fresh research_state/liquidation_forward_validate_004_blocker_$(date -u +%Y%m%dT%H%M%SZ).md (full probe tables, ETag/cache, exact checkable resume conditions: paths/patterns/URLs/months >=2026-11, rubric-GO). Update/create experiment_frontier.json with precise resume triggers, last_checked UTC, blocked-cell status. Update AGENT_HANDOFF.md with timestamped next task.

RESUME CONDITION (ONLY UNBLOCK): ironflow data/events/YYYY-MM.parquet or data/fills/YYYY-MM.parquet for any month >=2026-11 returns HTTP 200 unauthenticated (via monitor) OR new admissible unauthenticated source passes strict GO rubric (>=5 symbols, >=1 complete month OR >=3x30d blocks, documented coverage/completeness, permissive license, no keys/signed/requester-pays, schema compatible with frozen FCLR-010). Hyperliquid-only for Track A.

STOP RULE: Complete ALL 5 steps + artifacts. Never stop early for "no data". Track C locked. No conflation of tracks.
```

## VERIFICATION
- `python -m pytest tests/ -q` (suite green; 179 passed)
- `python scripts/monitor_ironflow_liquidations.py --quick` (confirms blocked: data_through=2026-10, no >=2026-11)
- `python scripts/hunt_alternative_liquidation_sources.py`
- `python scripts/deep_review_alt_sources.py`

## NEXT TASK (TIMESTAMPED)
20261104T223906Z: Execute campaign FCLR-NEXT-076 above. Remove bottlenecks while blocked; harden triggers so unblocking is instantaneous and correct.
