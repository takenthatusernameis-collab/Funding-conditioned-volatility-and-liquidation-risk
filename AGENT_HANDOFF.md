# AGENT_HANDOFF.md (SINGLE DURABLE HANDOFF)
Timestamp (UTC): 20261105T081715Z
Git SHA (HEAD): 69d08ad5
Branch: main
Repo: Funding-conditioned-volatility-and-liquidation-risk
Handoff ID: FCLR-HANDOFF-20261105T081715Z | Priority: P0 - REPO-NAME PRIORITIZED + HEAVY WORK MANDATORY | Mode: CAMPAIGN-DRIVEN | Enforcement: NO-SKIP | Bottleneck-State: HARDENED-HEAVY-091

## REPO-NAME PRIORITIZATION (INFERRED)
Repository name: "Funding-conditioned-volatility-and-liquidation-risk"
- Funding-conditioned VOLATILITY component = Track C (FCLR-011) — SEALED/LOCKED. Forecast gate PASSED. DO NOT retune/re-run sealed cells/conflate.
- LIQUIDATION RISK component = Track A (FCLR-010) — ONLY UNFINISHED HALF. BLOCKED on admissible unauthenticated liquidation data (Hyperliquid-only). Track B = NOT_SUPPORTED.
- BOTH components are core to repo identity. While volatility is sealed, liquidation risk MUST be driven to completion via admissible data or hardened to resume instantly on trigger. NO SCOPE DRIFT TO SEALED TRACKS.

## CURRENT VERIFIED STATE (CLEAN BASELINE)
- Tests: `python -m unittest discover tests` — **146 tests OK** (adversarial + rubric/prereg/latency hardening). MUST remain green.
- Track C: SEALED/LOCKED. Track B: NOT_SUPPORTED.
- Track A: ON-TRIGGER/MONITOR ONLY. Latest blocker: `research_state/liquidation_forward_validate_011_blocker_20261105T081715Z.md`. `experiment_frontier.json` updated (last_checked 2026-11-05T08:17:15Z).
- Artifact churn (091): `research_state` *.md+*.json 191 -> 179 (**net -12**); removed 6 unreferenced temp diag scripts + 2 zero-ref fast variants; consolidated 9 ref-free timestamped artifacts into 3 canonical histories (content preserved); removed 6 ref-free transient snapshots + 2 duplicates + 1 merged snapshot. Ironflow probe family **exactly 2 files** (1 live + `ironflow_probe_digest_latest.json`). No new recurring timestamped probe families.
- Harness: FCLR-010 fixtures exist (`tests/fixtures/tracka`, frozen manifest, 6 symbols); `FCLR010Harness` cold load <0.05s; `pre_register_forward_experiment`/`evaluate_forward` enforce PREREG-BEFORE-OUTCOMES and block without prereg/data. Monitor quick ~0.46s cached.
- NO COASTING ALLOWED. Every session must produce measurable bottleneck reduction or hardness improvements with irrefutable metrics.

## SINGLE INITIAL TASK MESSAGE FOR NEXT AGENTIC SESSION (COPY/PASTE VERBATIM)
```text
TASK ID: FCLR-NEXT-092-TRACK-A-HEAVY-WHILE-BLOCKED-ZERO-CHURN-RESUME
PRIORITY: P0 - REPO-NAME PRIORITIZED (Volatility SEALED/LOCKED; Liquidation Risk = ONLY ACTIVE OBJECTIVE)
TIMESTAMP (UTC): 20261105T081715Z
CAMPAIGN: TRACK A LIQUIDATION RISK - MAXIMUM HEAVY PROGRESS WHILE BLOCKED. NO COASTING. ELIMINATE REMAINING CHURN. MAKE RESUME INSTANT AND IRREFUTABLE.
ENFORCEMENT: ALL STEPS MANDATORY. SESSION INCOMPLETE IF ANY SKIPPED. PREREGISTER BEFORE INSPECTING OUTCOMES IF TRIGGERED. NO IDLE TURNS. NO "MONITOR ONLY" WITHOUT CONCRETE HARDENING. NO NEW TIMESTAMPED PROBE/SWEEP FAMILIES.

OBJECTIVE (INFERRED): Complete the liquidation-risk half of "Funding-conditioned-volatility-and-liquidation-risk". Data blocked. While blocked you MUST create unavoidable heavy progress: (A) drive research_state net down by >=12 files OR consolidate >=70% of remaining timestamped families into canonical histories with refs-checked deletions, (B) keep ironflow probe files == 2, (C) exhaust unauthenticated Hyperliquid-only discovery and log irrefutable evidence, (D) make GO rubric + classification adversarial-tested with failing-edge fixtures, (E) prove FCLR-010 offline dry-run end-to-end on fixtures in <10s and add a test that enforces the <10s bound, (F) remove/merge remaining duplicate script paths only if tests prove safety, (G) leave state STRICTER. Never stop for "no data". Future agents must NOT be able to coast.

CONSTRAINTS: No credentials/manual files/.github/workflows changes. Leakage-safe, preregister-before-outcomes. Track C/B locked/unsupported. Raw data/caches out of git. Clean-clone reproducible. No schedulers/pollers/status-only files/repeated wrappers/agent-controllers. Hyperliquid-only for Track A. Do not conflate observed/modeled liquidations. No threshold-shopping. No scope drift. No new recurring timestamped families for probes/sweeps/blockers - append to canonical histories or overwrite canonical pointers where safe.

MANDATORY EXECUTION (IN ORDER - ALL REQUIRED):

1) ENTRY METRICS & BOTTLENECK BASELINE (IRREFUTABLE)
   - Record: research_state md+json count, ironflow probe file count/names, timestamped-family count, tests count, monitor --quick time.
   - Identify remaining churn sources (timestamped families, duplicate scripts, wrappers). Set measurable targets: net -12 files OR >=70% remaining timestamped families consolidated; ironflow probes == 2; tests >=146 and green.

2) TRIGGER PROBE (EXHAUSTIVE, HYPERLIQUID-ONLY - FAST PATH)
   - Run: python scripts/monitor_ironflow_liquidations.py --quick
   - Run: python scripts/deep_review_alt_sources.py
   - Run: python scripts/hunt_alternative_liquidation_sources.py
   - Log every URL/status/ETag/last-modified/classification. IF trigger -> HALT outcome inspection; PREREGISTER BEFORE reading outcomes in `research_state/fclr010_prereg_$(date -u +%Y%m%dT%H%M%SZ).json` with frozen hypothesis/splits/features/targets/metrics/gates/stop rule/data hashes; run ONLY frozen FCLR-010 harness. ELSE write "NO NEW DATA - ON HOLD" with irrefutable evidence and IMMEDIATELY proceed to demolition.

3) BOTTLENECK DEMOLITION (AGGRESSIVE - MANDATORY)
   - Merge timestamped families into canonical histories (refs-checked). Remove only files verified unreferenced by canonical docs/code/tests/frontier/manifest/handoff. Preserve excerpts/hashes/paths in history.
   - Enforce EXACTLY 2 ironflow probe artifacts total. No per-run digest/probe timestamped families.
   - Eliminate duplicate code paths/wrappers only with tests proving safety. Remove status-only/scheduler/poller files if any appear.
   - Document before/after metrics in `research_state/campaign_sweep_tracka_$(date -u +%Y%m%dT%H%M%SZ).md` (net delta, families consolidated, refs checked).

4) SOURCE HARDENING + MAXIMALLY STRICT RUBRIC (ADVERSARIAL)
   - Extend rubric tests with edge fixtures: reject auth/key/requester-pays/incomplete coverage/<5 symbols/non-Hyperliquid-merge/modeled-as-observed/schema-mismatch. Keep Hyperliquid-only Track A.
   - Cache probes with ETags/hashes/TTLs; fast-fail. Update `research_state/tracka_rubric_hardened_$(date -u +%Y%m%dT%H%M%SZ).md` only if criteria/controls change; otherwise append a short delta to canonical history.

5) HARNESS HARDENING + OFFLINE DRY-RUN (ZERO-LATENCY RESUME)
   - Prove offline dry-run: fixtures load, harness config frozen, prereg gate blocks without prereg, prereg record valid, decision path <10s. Add/keep tests enforcing bounds and frozen invariants.
   - Document in `research_state/tracka_fclr010_dryrun_hardened_$(date -u +%Y%m%dT%H%M%SZ).md` (or append canonical delta).

6) TESTS, EVIDENCE, HANDOFF UPDATE (MANDATORY - LEAVE STRICTER STATE)
   - Run: python -m unittest discover tests (MUST stay green, >=146).
   - Write `research_state/liquidation_forward_validate_012_blocker_$(date -u +%Y%m%dT%H%M%SZ).md` with full evidence, metrics, bottlenecks removed, concrete resume instructions.
   - Update `research_state/experiment_frontier.json` (last_checked now, track_a_blocked true, pointer to new blocker, artifact_churn_092 metrics).
   - Update `AGENT_HANDOFF.md` with a NEW stricter timestamped next task that cannot be coasted. Commit nothing just for activity.

RESUME CONDITION (only): ironflow `data/events/YYYY-MM.parquet` or `data/fills/YYYY-MM.parquet` for month>=2026-11 returns HTTP 200 unauthenticated OR admissible unauthenticated Hyperliquid source passes strict GO rubric. Hyperliquid-only. PREREGISTER BEFORE INSPECTING OUTCOMES.

STOP RULE: Complete ALL steps + ALL artifacts with concrete metrics. Track C locked. Track B unsupported. No conflation. No schedulers/pollers/status-only/repeated wrappers/agent-controllers/workflow changes. No new recurring probe timestamped families. Heavy work mandatory while blocked. Leave state stricter than found.
```

## VERIFICATION COMMANDS (RUN ON ENTRY)
- `python -m unittest discover tests` (must be >=146, green)
- `python scripts/monitor_ironflow_liquidations.py --quick`
- `python scripts/deep_review_alt_sources.py`
- `python scripts/hunt_alternative_liquidation_sources.py`
- `python scripts/generate_tracka_fixtures.py`
- `python scripts/fclr010_harness.py`

## NEXT TASK (TIMESTAMPED)
20261105T081715Z: Execute FCLR-NEXT-092 as above. Volatility SEALED/LOCKED. Liquidation Risk ONLY focus. Demolish remaining churn (net -12 research_state files OR >=70% timestamped families consolidated, refs-checked), keep ironflow probes==2, probe exhaustively, add adversarial rubric edge tests, keep harness offline-ready <10s with enforced tests, tests >=146 green, write `liquidation_forward_validate_012_blocker_*.md`, update `experiment_frontier.json` and this handoff STRICTER. PREREG BEFORE OUTCOMES if triggered. NO COASTING.
