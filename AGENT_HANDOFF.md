# AGENT_HANDOFF.md (SINGLE DURABLE HANDOFF)
Timestamp (UTC): 20261105T061320Z
Git SHA (HEAD): 8e8b7e9091b1d89b1020761ffa0423b3d19983ef
Branch: main
Repo: Funding-conditioned-volatility-and-liquidation-risk
Handoff ID: FCLR-HANDOFF-20261105T061320Z | Priority: P0 - REPO-NAME PRIORITIZED + HEAVY WORK MANDATORY | Mode: CAMPAIGN-DRIVEN | Enforcement: NO-SKIP | Bottleneck-State: CONSOLIDATE-ON-ENTRY

## REPO-NAME PRIORITIZATION (INFERRED)
Repository name: "Funding-conditioned-volatility-and-liquidation-risk"
- Funding-conditioned VOLATILITY component = Track C (FCLR-011) — SEALED/LOCKED. Forecast gate PASSED. DO NOT retune/re-run sealed cells/conflate.
- LIQUIDATION RISK component = Track A (FCLR-010) — ONLY UNFINISHED HALF. BLOCKED on admissible unauthenticated liquidation data (Hyperliquid-only). Track B = NOT_SUPPORTED.

## CURRENT VERIFIED STATE (CLEAN BASELINE)
- Tests: `python -m unittest discover tests` — 133 tests OK (adversarial tests present). MUST remain green.
- Track C: SEALED/LOCKED. Track B: NOT_SUPPORTED.
- Track A: ON-TRIGGER/MONITOR ONLY. Last blocker: liquidation_forward_validate_008_blocker_20261105T061159Z.md. experiment_frontier.json points to liquidation_forward_validate_007_blocker_20261105T051723Z.md (update on entry).
- Artifact churn high (many timestamped files). Bottleneck: consolidation required. ironflow_probe non-digest artifacts proliferated previously; enforce 1 active non-digest path.
- Harness: FCLR-010 fixtures exist; dry-run capable offline. No schedulers/pollers/status-only files/agent-controllers/workflow changes permitted.

## SINGLE INITIAL TASK MESSAGE FOR NEXT AGENTIC SESSION (COPY/PASTE VERBATIM)
```text
TASK ID: FCLR-NEXT-086-TRACK-A-HEAVY-WHILE-BLOCKED-CONSOLIDATE
PRIORITY: P0 - REPO-NAME PRIORITIZED (Volatility SEALED/LOCKED; Liquidation Risk = ONLY ACTIVE OBJECTIVE)
TIMESTAMP (UTC): 20261105T061320Z
CAMPAIGN: TRACK A LIQUIDATION RISK - HEAVY PROGRESS WHILE BLOCKED. NO COASTING. ELIMINATE BOTTLENECKS.
ENFORCEMENT: ALL STEPS MANDATORY. SESSION INCOMPLETE IF ANY SKIPPED. PREREGISTER BEFORE INSPECTING OUTCOMES IF TRIGGERED.

OBJECTIVE (INFERRED): Complete the liquidation-risk half. Data blocked. While blocked you MUST create unavoidable heavy progress: consolidate artifact churn (>=40% net reduction of new timestamped research_state files created this session vs entry count), exhaust unauthenticated discovery (Hyperliquid-only), harden rubric/fixtures/tests, keep FCLR-010 harness zero-latency for resume, and produce concrete before/after metrics. Never stop for "no data".

CONSTRAINTS: No credentials/manual files/.github/workflows changes. Leakage-safe, preregister-before-outcomes. Track C/B locked/unsupported. Raw data/caches out of git. Clean-clone reproducible. No schedulers/pollers/status-only files/repeated wrappers/agent-controllers. Hyperliquid-only for Track A. Do not conflate observed/modelled liquidations.

MANDATORY EXECUTION (IN ORDER - ALL REQUIRED):

1) ENTRY METRICS & BOTTLENECK BASELINE
   - Count: ls -1 research_state/*.md research_state/*.json | wc -l; count ironflow_probe non-digest vs digest; list new files since last handoff by mtime.
   - Record baseline in research_state/campaign_sweep_tracka_$(date -u +%Y%m%dT%H%M%SZ).md with before-counts, largest sources of churn, I/O estimate.

2) TRIGGER PROBE (EXHAUSTIVE, FAST PATH)
   - Run: python scripts/monitor_ironflow_liquidations.py --quick
   - Run: python scripts/deep_review_alt_sources.py
   - Run: python scripts/hunt_alternative_liquidation_sources.py
   - Log full tables (URLs/endpoints, auth, history, ETags/hashes, rubric pass/fail).
   IF (ironflow events/YYYY-MM.parquet or data/fills/YYYY-MM.parquet for month>=2026-11 returns HTTP 200 unauthenticated via monitor) OR any candidate passes strict GO rubric (unauthenticated, Hyperliquid-only scope valid, provenance/revision limits acceptable) ->
     HALT exploration of outcomes. PREREGISTER in research_state/fclr010_prereg_$(date -u +%Y%m%dT%H%M%SZ).json BEFORE reading/parsing result tables (frozen: hypothesis/target/boundary, train/val/test splits by time, features/ablation, metrics+uncertainty, stop rule, data hashes). Run ONLY frozen FCLR-010 harness (fixtures allowed). ELSE write "NO NEW DATA - ON HOLD" with complete probe evidence.

3) BOTTLENECK DEMOLITION (CONSOLIDATE AGGRESSIVELY)
   - Identify >=1 concrete bottleneck (artifact churn / duplicate digests / redundant scans).
   - Consolidate: merge related timestamped artifacts into single consolidated docs where semantically equivalent; remove or archive redundant duplicates; enforce single source of truth for ironflow probe state (keep 1 non-digest + digests).
   - Target >=40% reduction of NEW timestamped files created this session (count before/after). Provide before/after diff, file-counts, I/O/timings if measurable. Document in research_state/bottleneck_demolition_$(date -u +%Y%m%dT%H%M%SZ).md.

4) SOURCE HARDENING + RUBRIC ENFORCEMENT
   - Tighten GO rubric (unauthenticated, no signup/key/payment, Hyperliquid-only, revision limits, classification tests).
   - Harden liquidation-vs-fills-trades-funding classification with fixtures; add/extend adversarial tests.
   - Cache probes with ETags/hashes; extend hunt/deep_review only if yields concrete unverifiable gaps (no speculative broad crawls). Add tests for rubric edge cases.

5) HARNESS HARDENING + OFFLINE DRY-RUN
   - Verify fixtures + FCLR-010 offline dry-run end-to-end. Fix any gaps found (tests first).
   - Document in research_state/tracka_fclr010_dryrun_hardened_$(date -u +%Y%m%dT%H%M%SZ).md (commands, results, hashes, resume readiness).

6) TESTS, EVIDENCE, HANDOFF UPDATE (MANDATORY)
   - Run: python -m unittest discover tests (MUST stay green; if any fail -> fix before closing).
   - Write research_state/liquidation_forward_validate_009_blocker_$(date -u +%Y%m%dT%H%M%SZ).md: entry/exit counts, probe tables, consolidation before/after (>=40%), bottleneck fix, rubric state, dry-run, caches/ETags, resume conditions, next concrete action (never "wait for data" alone).
   - Update research_state/experiment_frontier.json: last_checked (UTC now), track_a_blocked status, next_action_heavy, pointer to new blocker file.
   - Update AGENT_HANDOFF.md: new timestamped next task (FCLR-NEXT-087...) with same enforcement. Commit nothing just for activity; only meaningful artifacts.

RESUME CONDITION (ONLY UNBLOCK): ironflow data/events/YYYY-MM.parquet or data/fills/YYYY-MM.parquet for month>=2026-11 returns HTTP 200 unauthenticated (monitor_ironflow_liquidations.py) OR admissible unauthenticated Hyperliquid source passes strict GO rubric. Hyperliquid-only for Track A.

STOP RULE: Complete ALL 6 steps + ALL artifacts. Never stop early. Track C locked. Track B unsupported. No conflation of observed/modelled. No schedulers/pollers/status-only files/repeated wrappers/agent-controllers/workflow changes. Preregister BEFORE inspecting outcomes if triggered. Heavy work is mandatory while blocked.
```

## VERIFICATION COMMANDS (RUN ON ENTRY)
- `python -m unittest discover tests` (must be green)
- `python scripts/monitor_ironflow_liquidations.py --quick`
- `python scripts/deep_review_alt_sources.py`
- `python scripts/hunt_alternative_liquidation_sources.py`
- `python scripts/generate_tracka_fixtures.py`

## NEXT TASK (TIMESTAMPED)
20261105T061320Z: Execute FCLR-NEXT-086 as above. Volatility SEALED/LOCKED. Liquidation Risk ONLY focus. On entry compute baseline counts and consolidate aggressively (>=40% reduction of new files). Probe exhaustively; if trigger -> preregister before outcomes + run ONLY frozen FCLR-010. Else harden rubric/fixtures/tests, offline dry-run FCLR-010, keep tests green, write liquidation_forward_validate_009_blocker_*.md, update experiment_frontier.json and this handoff. No shortcuts.
