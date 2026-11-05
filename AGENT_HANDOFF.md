# AGENT_HANDOFF.md (SINGLE DURABLE HANDOFF)
Timestamp (UTC): 20261105T091423Z
Git SHA (HEAD): 9688419d (working tree: pycache + ironflow_fastpath_cache cache refresh only; research_state root 185 md+json; ironflow probe artifacts == 2)
Branch: main
Repo: Funding-conditioned-volatility-and-liquidation-risk
Handoff ID: FCLR-HANDOFF-20261105T091423Z | Priority: P0 - REPO-NAME PRIORITIZED + HEAVY WORK MANDATORY | Mode: CAMPAIGN-DRIVEN | Enforcement: NO-SKIP | Bottleneck-State: HARDENED-HEAVY-093

## REPO-NAME PRIORITIZATION (INFERRED)
Repository name: "Funding-conditioned-volatility-and-liquidation-risk"
- Funding-conditioned VOLATILITY component = Track C (FCLR-011) — SEALED/LOCKED. Forecast gate PASSED. DO NOT retune/re-run sealed cells/conflate.
- LIQUIDATION RISK component = Track A (FCLR-010) — ONLY UNFINISHED HALF. BLOCKED on admissible unauthenticated liquidation data (Hyperliquid-only). Track B = NOT_SUPPORTED.
- BOTH components are core to repo identity. While volatility is sealed, liquidation risk MUST be driven to completion via admissible data or hardened to resume instantly on trigger. NO SCOPE DRIFT TO SEALED TRACKS.

## CURRENT VERIFIED STATE (CLEAN BASELINE)
- Tests: `python -m unittest discover tests` — **156 tests OK** (green; runtime ~13.7s; includes 091+092+093 adversarial rubric/dry-run/canonical-output hardening). MUST remain green (>=155).
- Track C: SEALED/LOCKED. Track B: NOT_SUPPORTED.
- Track A: ON-TRIGGER/MONITOR ONLY. Latest blocker: `research_state/liquidation_forward_validate_012_blocker_20261105T082547Z.md`. `experiment_frontier.json` updated (last_checked 2026-11-05T08:26:40Z; track_a_blocked true).
- Artifact churn (092→093): flat/net-negative — no new recurring timestamped families; `scripts/hunt_alternative_liquidation_sources.py` writes `research_state/alt_source_scan_latest.json`; `scripts/deep_review_alt_sources.py` writes `research_state/alt_source_deep_review_latest.md`. Ironflow probe family **exactly 2 files** (1 live + `ironflow_probe_digest_latest.json`). No new recurring timestamped probe/scan families. research_state root md+json = 185 (stable).
- Harness: FCLR-010 fixtures exist (`tests/fixtures/tracka`, frozen manifest, 6 symbols); `FCLR010Harness` cold <0.05s; `pre_register_forward_experiment`/`evaluate_forward` enforce PREREG-BEFORE-OUTCOMES and block without prereg. Monitor quick ~0.50s cached.
- THIS SESSION (20261105T091423Z) VERIFIED BASELINE: tests 156 OK green; research_state root 185 md+json (stable); ironflow probes == 2 enforced; monitor --quick NO RESUME TRIGGER (data_through=2026-10; 2026-11..2027-02 absent); alt_source_scan/deep_review canonical. FCLR-NEXT-093 STEPS 1-2 ALREADY COMPLETE (prior session: entry metrics baseline + trigger probe NO NEW DATA - on hold) — DO NOT RE-EXECUTE. Proceed immediately to Step 3 bottleneck demolition.
- NO COASTING ALLOWED. Every session must produce measurable bottleneck reduction or hardness improvements with irrefutable metrics.

## SINGLE INITIAL TASK MESSAGE FOR NEXT AGENTIC SESSION (COPY/PASTE VERBATIM)
```text
TASK ID: FCLR-NEXT-093-TRACK-A-STEPS3-6-BOTTLENECK-DEMOLITION-HEAVY
PRIORITY: P0 - REPO-NAME PRIORITIZED (Volatility SEALED/LOCKED; Liquidation Risk = ONLY ACTIVE OBJECTIVE)
TIMESTAMP (UTC): 20261105T083124Z
CAMPAIGN: TRACK A LIQUIDATION RISK - STEPS 3-6 HEAVY BOTTLENECK DEMOLITION WHILE BLOCKED. NO COASTING. ZERO CHURN. MAKE RESUME INSTANT AND IRREFUTABLE.
ENFORCEMENT: ALL STEPS MANDATORY. STEPS 1-2 ALREADY COMPLETE (DO NOT RE-EXECUTE). SESSION INCOMPLETE IF ANY STEP 3-6 SKIPPED. PREREGISTER BEFORE INSPECTING OUTCOMES IF TRIGGERED. NO IDLE TURNS. NO "MONITOR ONLY" WITHOUT CONCRETE HARDENING. NO NEW TIMESTAMPED PROBE/SWEEP/SCAN FAMILIES.

OBJECTIVE (INFERRED): Complete the liquidation-risk half of "Funding-conditioned-volatility-and-liquidation-risk". Data blocked (no Hyperliquid month >=2026-11). While blocked you MUST create unavoidable heavy progress: (A) keep research_state churn flat or net-negative (no new recurring timestamped families; consolidate any ref-free families found), (B) keep ironflow probe files == 2, (C) exhaust unauthenticated Hyperliquid-only discovery and log irrefutable evidence, (D) strengthen GO rubric adversarial tests for modeled-as-observed conflation / schema mismatch / incomplete symbol coverage / non-Hyperliquid merge cases with explicit fail fixtures, (E) prove FCLR-010 offline dry-run end-to-end on fixtures in <10s and keep enforced test, (F) reduce test/runtime side-effects that create probe churn (without breaking monitor correctness), (G) leave state STRICTER. Never stop for "no data". Future agents must NOT be able to coast.

CONSTRAINTS: No credentials/manual files/.github/workflows changes. Leakage-safe, preregister-before-outcomes. Track C/B locked/unsupported. Raw data/caches out of git. Clean-clone reproducible. No schedulers/pollers/status-only files/repeated wrappers/agent-controllers. Hyperliquid-only for Track A. Do not conflate observed/modeled liquidations. No threshold-shopping. No scope drift. Canonical outputs only for recurring probes/scans (`ironflow_probe_digest_latest.json` + 1 live probe; `alt_source_scan_latest.json`; `alt_source_deep_review_latest.md`).

MANDATORY EXECUTION (IN ORDER - ALL REQUIRED; STEPS 1-2 ALREADY DONE THIS SESSION):

3) BOTTLENECK DEMOLITION (AGGRESSIVE - MANDATORY)
   - Merge any remaining timestamped families into canonical histories (refs-checked). Remove only files verified unreferenced by canonical docs/code/tests/frontier/manifest/handoff. Preserve excerpts/hashes/paths in history.
   - Enforce EXACTLY 2 ironflow probe artifacts total. No per-run digest/probe timestamped families outside the single live probe + canonical digest contract.
   - Reduce test/monitor side-effect churn safely (mock/time-freeze/state isolation) only with tests proving safety.
   - Document before/after metrics in `research_state/campaign_sweep_tracka_$(date -u +%Y%m%dT%H%M%SZ).md`.

4) SOURCE HARDENING + MAXIMALLY STRICT RUBRIC (ADVERSARIAL)
   - Extend rubric tests with explicit edge fixtures: reject auth/key/requester-pays/incomplete coverage/<5 symbols/non-Hyperliquid-merge/modeled-as-observed/schema-mismatch. Keep Hyperliquid-only Track A.
   - Cache probes with ETags/hashes/TTLs; fast-fail. Update rubric notes only if criteria/controls change.

5) HARNESS HARDENING + OFFLINE DRY-RUN (ZERO-LATENCY RESUME)
   - Prove offline dry-run: fixtures load, harness config frozen, prereg gate blocks without prereg, prereg record valid, decision path <10s. Keep/add tests enforcing bounds and frozen invariants.

6) TESTS, EVIDENCE, HANDOFF UPDATE (MANDATORY - LEAVE STRICTER STATE)
   - Run: python -m unittest discover tests (MUST stay green, >=155).
   - Write `research_state/liquidation_forward_validate_013_blocker_$(date -u +%Y%m%dT%H%M%SZ).md` with full evidence, metrics, bottlenecks removed, concrete resume instructions.
   - Update `research_state/experiment_frontier.json` (last_checked now, track_a_blocked true, pointer to new blocker, artifact_churn_093 metrics).
   - Update `AGENT_HANDOFF.md` with a NEW stricter timestamped next task that cannot be coasted. Commit nothing just for activity.

RESUME CONDITION (only): ironflow `data/events/YYYY-MM.parquet` or `data/fills/YYYY-MM.parquet` for month>=2026-11 returns HTTP 200 unauthenticated OR admissible unauthenticated Hyperliquid source passes strict GO rubric. Hyperliquid-only. PREREGISTER BEFORE INSPECTING OUTCOMES.

STOP RULE: Complete ALL steps + ALL artifacts with concrete metrics. Track C locked. Track B unsupported. No conflation. No schedulers/pollers/status-only/repeated wrappers/agent-controllers/workflow changes. No new recurring probe/scan timestamped families. Heavy work mandatory while blocked. Leave state stricter than found.
```

## VERIFICATION COMMANDS (RUN ON ENTRY)
- `python -m unittest discover tests` (must be >=155, green)
- `python scripts/monitor_ironflow_liquidations.py --quick`
- `python scripts/deep_review_alt_sources.py`
- `python scripts/hunt_alternative_liquidation_sources.py`
- `python scripts/generate_tracka_fixtures.py`
- `python scripts/fclr010_harness.py`

## NEXT TASK (TIMESTAMPED)
20261105T091423Z: Execute FCLR-NEXT-093 Steps 3-6 as above. Volatility (Track C) SEALED/LOCKED. Liquidation Risk (Track A) = ONLY ACTIVE OBJECTIVE. Steps 1-2 DONE prior session (baseline recorded; trigger probe NO NEW DATA - on hold). Remaining mandatory: Steps 3-6 — bottleneck demolition (merge timestamped families into canonical histories, enforce ironflow probes == 2, reduce test/monitor side-effect churn with safety tests, document before/after in `research_state/campaign_sweep_tracka_*.md`), source hardening + maximally strict adversarial rubric edge tests, harness offline dry-run <10s with enforced tests, tests >=155 green, write `research_state/liquidation_forward_validate_013_blocker_*.md` with full evidence/metrics/bottlenecks/resume instructions, update `experiment_frontier.json` (last_checked now, track_a_blocked true, pointer to new blocker, artifact_churn_093 metrics), update this handoff STRICTER with a new timestamped next task that cannot be coasted. PREREG BEFORE OUTCOMES if triggered. NO COASTING. HEAVY WORK MANDATORY WHILE BLOCKED.
