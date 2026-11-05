# Track A Campaign Sweep (Step 1)
Timestamp (UTC): 20261105T002951Z
Git SHA: 089dff74a2e868044e36e65d0af7dacfbc284be7

## Evidence

### RESEARCH_PROMPT.md - key constraints
- Track A is liquidation risk; Track C is volatility (forecast gate passed, sealed/locked)
- Must not conflate observed vs modeled liquidations
- Cannot stop for lack of data; must find alternatives while blocked
- Ironflow is HF dataset ironflow/hyperliquid-liquidations

### AGENT_HANDOFF.md (current)
Handoff ID: FCLR-HANDOFF-20261105T001706Z | Priority: P0 - REPO-NAME PRIORITIZED + BOTTLENECKS REMOVED | Mode: CAMPAIGN-DRIVEN | Enforcement: NO-SKIP
- Funding-conditioned VOLATILITY component = Track C (FCLR-011) — COMPLETE/SEALED/LOCKED. Forecast gate PASSED on frozen splits. DO NOT retune/re-run sealed cells.
- Liquidation RISK component = Track A (FCLR-010) — BLOCKED on admissible unauthenticated liquidation data (ironflow data_through=2026-10; no month >=2026-11 returns HTTP 200). THIS IS THE UNFULFILLED HALF - HIGHEST ACTIVE PRIORITY.
- Bottlenecks removed (hardened baseline, DO NOT regress): consolidated alt_source_scan_*.json to single latest; consolidated alt_source_deep_review_*.md to single latest. monitor_ironflow_liquidations.py has ETag/tree cache, HEAD-404 fast path, forward-edge-only resume probe, baseline-drift state-only skip on 304, per-file ETag/LM caching. hunt_alternative_liquidation_sources.py has 24h HF search cache, 6h per-URL probe cache, URL dedup, merged DEEP_REVIEW_URLS. deep_review_alt_sources.py reuses hunt's shared URL probe cache. No schedulers/pollers/status-only files/repeated wrappers.
- Track C: SEALED/LOCKED. Track B: NOT_SUPPORTED. Track A: ON TRIGGER/MONITOR ONLY, blocked on data.
- Last confirmed blocked via scripts/monitor_ironflow_liquidations.py --quick (20261104T233118Z context): data_through=2026-10; forward edge 2026-11..2027-02 head-probed absent; probe_diff added=0 changed=0 removed=0; baseline_drift intact.
TASK ID: FCLR-NEXT-079-TRACK-A-HEAVY-BOTTLENECK-CAMPAIGN
PRIORITY: P0 - REPO-NAME PRIORITIZED (Funding-conditioned volatility DONE/LOCKED; Liquidation risk ONLY ACTIVE FOCUS - BLOCKED ON DATA)
CAMPAIGN: TRACK A LIQUIDATION-RISK - FORCE HEAVY BOTTLENECK REMOVAL WHILE BLOCKED, HARDEN TRIGGERS, NEVER CONCLUDE "NO DATA"
OBJECTIVE (INFERRED FROM REPO NAME): Funding-conditioned volatility is complete/locked. ALL effort must go to liquidation risk (Track A). Data blocked (ironflow data_through=2026-10, no >=2026-11). You CANNOT stop because "no data". While blocked, you MUST aggressively find and remove real bottlenecks, harden automation/triggers/caches/classification so the moment data appears, an agent can resume FCLR-010 with zero wasted time. Eliminate inefficiencies. Do NOT add schedulers/pollers/status-only files/repeated wrappers.
CONSTRAINTS: No credentials/manual files/.github/workflows changes. Leakage-safe, preregister-before-outcomes. Track C/B remain locked/unsupported. Raw data/caches out of git. Clean-clone reproducible.
2) TRIGGER PROBE (FULL TABLES): Run scripts/monitor_ironflow_liquidations.py --quick, scripts/deep_review_alt_sources.py, scripts/hunt_alternative_liquidation_sources.py. Log EVERY checked URL/path/pattern, status/headers/mtime/body previews, ETag/TTL, cached hits, baseline-drift. If >=2026-11 ironflow OR rubric-GO alternative appears -> HALT inspection, PREREGISTER in research_state/fclr010_prereg_$(date -u +%Y%m%dT%H%M%SZ).json BEFORE inspecting outcomes (hypothesis/frozen splits/metrics/stop rule), run ONLY frozen FCLR-010 harness. Else write "NO NEW DATA - ON HOLD" with complete tables.
5) BLOCKER+FRONTIER+HANDOFF: Write fresh research_state/liquidation_forward_validate_005_blocker_$(date -u +%Y%m%dT%H%M%SZ).md (full probe tables, ETag/cache, exact checkable resume conditions). Update/create research_state/experiment_frontier.json with precise resume triggers, last_checked UTC, blocked status. Update AGENT_HANDOFF.md with timestamped next task.
RESUME CONDITION (ONLY UNBLOCK): ironflow data/events/YYYY-MM.parquet or data/fills/YYYY-MM.parquet for any month >=2026-11 returns HTTP 200 unauthenticated (via monitor) OR new admissible unauthenticated source passes strict GO rubric (>=5 symbols, >=1 complete month OR >=3x30d blocks, documented coverage/completeness, permissive license, no keys/signed/requester-pays, schema compatible with frozen FCLR-010). Hyperliquid-only for Track A.
STOP RULE: Complete ALL 5 steps + artifacts. Never stop early for "no data". Track C locked. No conflation of tracks. No schedulers/pollers/status-only files/wrappers/workflow changes.
- `python scripts/monitor_ironflow_liquidations.py --quick` (blocked: data_through 2026-10)
20261105T001706Z: Execute FCLR-NEXT-079 above in full. Prioritize liquidation risk (Track A). Remove bottlenecks while blocked, harden triggers, keep artifacts consolidated. Do not touch Track C. If resume conditions met at any point, preregister before inspecting outcomes.

### experiment_frontier.json (relevant)
{"rank": 0, "task": "FCLR-NEXT-012: CONSOLIDATE-TRACKA-AND-FUNDING-INCREMENTAL \u2014 forward validation pre-registered (FCLR-012-A Track A ironflow beyond 2026-10-31; FCLR-012-V funding-conditioned volatility on new 2026 panel). Frozen splits/metrics/gates/embargo/block-bootstrap; no holdout reuse; NO overlay changes.", "prerequisite": "tests/test_fclr010_harness.py passes; fclr010_harness.py pre_register_forward_experiment() + evaluate_forward() hardened; run_manifest.json experiments map updated; consolidated + synthesis artifacts written.", "acceptance": "experiment_frontier.json contains FCLR-012; track_a_fclr010_consolidated.md and funding_incremental_synthesis_20261103T115630Z.md and forward_campaign_fclr012_prereg.md present; AGENT_HANDOFF.md single durable handoff with FORWARD CAMPAIGN; pytest green.", "blockers": "Forward runs blocked unless NEW admissible unauthenticated data appears (new ironflow monthly parquet >2026-10-31 for Track A; new unsealed 2026 Binance panel beyond 2026-11-02 for volatility). Do not relax thresholds or re-run sealed panels.", "do_not": "Do not re-run sealed FCLR-001/002/003/006/007/008/010/011. Do not threshold-shop. Do not merge tracks. Do not build live/paper trading.", "status": "PREREGISTERED", "resume_triggers": ["new ironflow parquet >2026-10-31 -> execute FCLR-012-A", "new unsealed 2026 Binance panel >2026-11-02 -> execute FCLR-012-V v2"], "generated": "20261103T120041Z"}
{"rank": 0.1, "task": "TRACK_A_LIQUIDATION_RISK_MONITOR: Keep alive until rubric-GO data appears", "prerequisite": "monitor_ironflow_liquidations --quick/--verify", "acceptance": "Evidence logged each session, automation hardened, resume only on rubric-GO data with preregistration", "blockers": "Structural - no data (2026-10 latest); monitor hardened in 004i", "status": "MONITOR_ONLY", "resume_triggers": ["ironflow >=2026-11 parquet appears (events or fills HTTP 200 unauthenticated)", "rubric-GO alternative unauthenticated source passes strict criteria"], "generated": "20261104T192914Z", "last_checked": "2026-11-04T23:31:18Z", "notes": "Hardened: ETag/tree cache, HEAD-404 fast path, baseline-drift probe, per-file ETag/LM caching, alt source consolidation automated"}

### blocked_cells
{"hypothesis": "FCLR-H004", "reason": "Direct liquidation labels unavailable from admissible public sources", "status": "BLOCKED"}
{"track": "TRACK_A", "reason": "No ironflow month >=2026-11 (data_through=2026-10)", "resume_trigger": "data/events/YYYY-MM.parquet or data/fills/YYYY-MM.parquet >=2026-11 appears (unauthenticated HF) with HTTP 200; OR rubric-GO alternative source passes strict criteria", "last_checked": "2026-11-04T23:31:18Z"}

### run_manifest.json (relevant)
FCLR-010: {"status": "COMPLETE_SEALED", "gate": "FORECAST_GATE_PASSED", "track": "A", "primary_contrast": "C2_vs_B1", "primary_metric": "brier", "rel_reduction": 0.0221, "ci": [-0.004892, -0.001263], "instrumen

### ironflow_monitor_state.json (summary)
last_check: 2026-11-02T05:59:46Z
data_through: 2026-10
consecutive_absent: 3
events_months_present (last 5): ['2026-06', '2026-07', '2026-08', '2026-09', '2026-10'] (total 18)
resume_trigger.currently_fired: False
last_scan.go: False

### Scripts examined
- scripts/monitor_ironflow_liquidations.py: exists (96627 bytes)
- scripts/hunt_alternative_liquidation_sources.py: exists (40586 bytes)
- scripts/deep_review_alt_sources.py: exists (10243 bytes)

### Redundant artifact check
alt_source_scan_*.json count: 1
alt_source_deep_review_*.md count: 1
  latest: /home/runner/work/Funding-conditioned-volatility-and-liquidation-risk/Funding-conditioned-volatility-and-liquidation-risk/research_state/alt_source_scan_20261105T001950Z.json
  latest: /home/runner/work/Funding-conditioned-volatility-and-liquidation-risk/Funding-conditioned-volatility-and-liquidation-risk/research_state/alt_source_deep_review_20261105T002000Z.md
- Handoff says consolidated to single latest; current matches.