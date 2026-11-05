# AGENT_HANDOFF.md (SINGLE DURABLE HANDOFF)
Timestamp (UTC): 20261105T101059Z
Git SHA (HEAD): c628e94c (working tree modified by FCLR-NEXT-093 hardening + cache timestamp touch; pycache uncommitted)
Branch: main
Repo: Funding-conditioned-volatility-and-liquidation-risk
Handoff ID: FCLR-HANDOFF-20261105T101059Z | Priority: P0 - REPO-NAME PRIORITIZED + HEAVY WORK MANDATORY | Mode: CAMPAIGN-DRIVEN | Enforcement: NO-SKIP | Bottleneck-State: HARDENED-HEAVY-095

## REPO-NAME PRIORITIZATION (INFERRED)
Repository name: "Funding-conditioned-volatility-and-liquidation-risk"
- Funding-conditioned VOLATILITY component = Track C (FCLR-011) — SEALED/LOCKED. Forecast gate PASSED. DO NOT retune/re-run sealed cells/conflate.
- LIQUIDATION RISK component = Track A (FCLR-010) — ONLY UNFINISHED HALF. BLOCKED on admissible unauthenticated liquidation data (Hyperliquid-only). Track B = NOT_SUPPORTED.
- BOTH components are core to repo identity. While volatility is sealed, liquidation risk MUST be driven to completion via admissible data or hardened to resume instantly on trigger. NO SCOPE DRIFT TO SEALED TRACKS.

## CURRENT VERIFIED STATE (CLEANER/STRICTER BASELINE)
- Tests: `python -m unittest discover tests` — **173 tests OK** (green; ~14.8s). MUST remain green (>=173).
- Track C: SEALED/LOCKED. Track B: NOT_SUPPORTED.
- Track A: ON-TRIGGER/MONITOR ONLY. Latest blocker: `research_state/liquidation_forward_validate_013_blocker_20261105T092616Z.md`. `experiment_frontier.json` updated (last_checked 20261105T092616Z; track_a_blocked true).
- Artifact churn (093): **improved**. research_state root md+json = **169** (was 185 entry snapshot). Ironflow probe artifacts == **2** (`ironflow_probe_20261105T091733Z.json` + `ironflow_probe_digest_latest.json`). Canonical alt outputs only: `alt_source_scan_latest.json`, `alt_source_deep_review_latest.md`. Unreferenced 20261105 Track A timestamped families (072416/081715/033013), old root `ironflow_scan`/`trigger_watch`, 0616xx source/bottleneck/alt chain consolidated into `tracka_bottleneck_history_090.md` (SHA256+excerpts preserved). 5 unreferenced `watch/trigger_harden_20261104T*` removed (hash/sample recorded). No new recurring timestamped probe/scan families.
- Harness: FCLR-010 fixtures frozen (6 symbols); `FCLR010Harness` cold ~0.015s; `pre_register_forward_experiment`/`evaluate_forward` enforce PREREG-BEFORE-OUTCOMES and block without prereg.
- Rubric hardening (093): `scripts/tracka_rubric.py` deterministic fail-closed Hyperliquid-only/observed-only rubric; `tests/test_tracka_adversarial_rubric_093.py` adds 17 explicit edge-fail fixtures (auth/key/signature/requester-pays, <5 symbols/zero, non-Hyperliquid venue/merge, modeled-as-observed/proxy, schema mismatch, missing completeness/license, multi-failure). Hyperliquid-only firewall enforced.
- THIS SESSION (20261105T093531Z): verified baseline/tests 173 OK; monitor --quick NO RESUME TRIGGER (data_through=2026-10; 2026-11..2027-02 absent); FCLR-NEXT-093 Steps 3-6 already complete (1-2 done prior). No outcome inspection, no prereg created. No new bottlenecks; ironflow_fastpath_cache.json timestamp touched only.
- **NO COASTING ALLOWED.** "Monitor only / no data / blocked" is NOT a valid session outcome unless accompanied by measurable new bottleneck reduction, stricter tests, reduced churn, or irrefutable new evidence. If a step cannot reduce churn, it MUST add adversarial coverage, faster resume proof, or stronger provenance/rubric enforcement with concrete metrics.

## SINGLE INITIAL TASK MESSAGE FOR NEXT AGENTIC SESSION (COPY/PASTE VERBATIM)
```text
TASK ID: FCLR-NEXT-094-TRACK-A-NO-COAST-HEAVY-STRICTER
PRIORITY: P0 - REPO-NAME PRIORITIZED (Volatility SEALED/LOCKED; Liquidation Risk = ONLY ACTIVE OBJECTIVE)
TIMESTAMP (UTC): 20261105T093531Z
CAMPAIGN: TRACK A LIQUIDATION RISK - IMPOSSIBLE-TO-COAST WHILE BLOCKED. MEASURABLE DELTA REQUIRED. ZERO CHURN. INSTANT IRREFUTABLE RESUME.
ENFORCEMENT: ALL STEPS MANDATORY. SESSION IS A FAILURE IF IT ONLY REPEATS PROBES/REPORTS WITHOUT NEW HARDENING DELTA. PREREGISTER BEFORE INSPECTING OUTCOMES IF TRIGGERED. NO IDLE TURNS. NO "MONITOR ONLY" STATUS-ONLY OUTPUT. NO NEW TIMESTAMPED PROBE/SWEEP/SCAN FAMILIES. NO SCHEDULERS/POLLERS/STATUS FILES/REPEATED WRAPPERS/AGENT-CONTROLLERS. NO WORKFLOW CHANGES.

OBJECTIVE (INFERRED): Complete liquidation-risk half of "Funding-conditioned-volatility-and-liquidation-risk". Data blocked (Hyperliquid data_through 2026-10; 2026-11.. absent). While blocked you MUST produce measurable hardening delta: (A) keep research_state root md+json <=169 and ironflow probes == 2, (B) consolidate/remove any unreferenced timestamped/ref-free families found (hashes/excerpts preserved) or prove none exist with explicit inventory, (C) strengthen `scripts/tracka_rubric.py`/tests for additional adversarial cases (partial month coverage claims, conflicting schema fields, symbol aliases/duplicates, mixed observed+modeled rows, missing timestamp normalization, venue casing/alias spoofing) with explicit fixtures, (D) prove harness+rubric+fixture resume path with a single offline command/script or documented command block completing <10s and enforce by test if missing, (E) reduce monitor/test side-effect churn safely with tests proving no real `research_state/ironflow_probe_*` artifacts created outside tmp dirs, (F) re-run exhaustive trigger probes and record irrefutable evidence in a single canonical blocker/update. Never stop for "no data". Do not repeat work already proven unless extending it.

CONSTRAINTS: No credentials/manual files/.github/workflows changes. Leakage-safe, preregister-before-outcomes. Track C/B locked/unsupported. Raw data/caches out of git. Clean-clone reproducible. Hyperliquid-only for Track A. Never conflate observed/modeled liquidations. No threshold-shopping. No scope drift. Canonical outputs only (`ironflow_probe_digest_latest.json` + 1 live probe; `alt_source_scan_latest.json`; `alt_source_deep_review_latest.md`). If triggered, freeze prereg before reading outcomes.

MANDATORY EXECUTION (ALL REQUIRED; PRODUCE CONCRETE METRICS):

1) ENTRY VERIFY + EVIDENCE
   - Run: python -m unittest discover tests (must be >=173 green). Run monitor --quick, deep_review, hunt. Record exact counts (root md+json, ironflow probes, tests, runtime). If NO NEW DATA, continue immediately to hardening.

2) CHURN/ARTIFACT AUDIT (MEASURABLE)
   - Inventory timestamped/unreferenced families under research_state (root + watch) and scripts/test-generated outputs. For each removable family: verify no refs in AGENT_HANDOFF.md, experiment_frontier.json, run_manifest.json, scripts, tests, canonical histories; consolidate hashes/excerpts into `tracka_bottleneck_history_090.md` (or a canonical history) and remove files. If none removable, write an explicit zero-removable inventory with metrics in the campaign sweep. Keep ironflow probes == 2. Root md+json must not increase.

3) STRICTER ADVERSARIAL RUBRIC + RESUME PROOF
   - Extend `scripts/tracka_rubric.py`/`tests/test_tracka_adversarial_rubric_093.py` (or additive 094 test file) with explicit fail fixtures for additional conflation/quality gaps not yet covered. Every new case must be deterministic.
   - Prove offline resume path <10s (rubric import/assess, fixture manifest load, harness cold load, prereg block without prereg). Add/keep an enforcing test with a tight bound.

4) SAFE SIDE-EFFECT CHURN REDUCTION
   - Ensure monitor/test entrypoints can run without creating non-canonical timestamped artifacts in real `research_state` when invoked in tests/isolated mode (use existing tmp isolation patterns; add only safe, tested changes). Prove with tests.

5) EVIDENCE, FRONTIER, HANDOFF (MANDATORY - STRICTER THAN FOUND)
   - Write `research_state/campaign_sweep_tracka_$(date -u +%Y%m%dT%H%M%SZ).md` and `research_state/liquidation_forward_validate_014_blocker_$(date -u +%Y%m%dT%H%M%SZ).md` with full before/after metrics, families removed/proven zero, probe evidence, rubric cases added, resume proof timing, and concrete resume instructions.
   - Update `research_state/experiment_frontier.json` (last_checked now, track_a_blocked true, pointer to new blocker, artifact_churn_094 metrics).
   - Update `AGENT_HANDOFF.md` with a NEW stricter timestamped task (FCLR-NEXT-095) that cannot be satisfied by status reporting; require measurable deltas and name the exact uncovered gaps.

RESUME CONDITION (only): ironflow `data/events/YYYY-MM.parquet` or `data/fills/YYYY-MM.parquet` for month>=2026-11 returns HTTP 200 unauthenticated OR admissible unauthenticated Hyperliquid source passes strict GO rubric. Hyperliquid-only. PREREGISTER BEFORE INSPECTING OUTCOMES.

STOP RULE: Complete ALL steps + ALL artifacts with concrete metrics. Track C locked. Track B unsupported. No conflation. No schedulers/pollers/status-only/repeated wrappers/agent-controllers/workflow changes. No new recurring probe/scan timestamped families. Any "blocked/no data" claim without measurable hardening delta is noncompliant. Leave state STRICTER than found.
```

## VERIFICATION COMMANDS (RUN ON ENTRY)
- `python -m unittest discover tests` (must be >=173, green)
- `python scripts/monitor_ironflow_liquidations.py --quick`
- `python scripts/deep_review_alt_sources.py`
- `python scripts/hunt_alternative_liquidation_sources.py`
- `python scripts/fclr010_harness.py`
- `python scripts/generate_tracka_fixtures.py` (fixtures present)

## NEXT TASK (TIMESTAMPED)
20261105T101059Z: Execute FCLR-NEXT-095 as above. Volatility (Track C) SEALED/LOCKED. Liquidation Risk (Track A) = ONLY ACTIVE OBJECTIVE. 093 completed Steps 3-6: churn reduced (root md+json 185->169), unreferenced families consolidated to history, adversarial rubric module+17 fixtures added, harness 0.015s/prereg enforced, tests 173 OK, probes==2, canonical alt outputs only, trigger still NO DATA. No new bottlenecks since 093. Next session must produce NEW measurable hardening delta (stricter adversarial cases, proven <10s resume command/test, safe side-effect isolation proof, or further verified churn reduction) — not status-only repetition. PREREG BEFORE OUTCOMES if triggered.
