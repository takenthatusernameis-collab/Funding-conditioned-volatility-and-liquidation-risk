# AGENT_HANDOFF.md (SINGLE DURABLE HANDOFF)
Timestamp (UTC): 20261105T122444Z
Git SHA (HEAD, baseline): c1a6cbf3 (working tree modified by 097 hardening; not committed)
Branch: main
Repo: Funding-conditioned-volatility-and-liquidation-risk
Handoff ID: FCLR-HANDOFF-20261105T122444Z | Priority: P0 - REPO-NAME PRIORITIZED + HEAVY WORK MANDATORY | Mode: CAMPAIGN-DRIVEN | Enforcement: NO-SKIP | Bottleneck-State: HARDENED-HEAVY-097-COMPLETE

## REPO-NAME PRIORITIZATION (INFERRED)
Repository name: "Funding-conditioned-volatility-and-liquidation-risk"
- Funding-conditioned VOLATILITY component = Track C (FCLR-011) — **SEALED/LOCKED**. Forecast gate PASSED. DO NOT retune/re-run sealed cells/conflate.
- LIQUIDATION RISK component = Track A (FCLR-010) — **ONLY UNFINISHED HALF**. BLOCKED on admissible unauthenticated liquidation data (Hyperliquid-only). Track B = **NOT_SUPPORTED**.
- BOTH components are core to repo identity. NO SCOPE DRIFT TO SEALED TRACKS.

## CURRENT VERIFIED STATE (097, MEASURABLE DELTA DELIVERED)
- Tests: `python -m unittest discover tests` — **244 tests, OK** (096 baseline 226; +18). MUST remain green.
- Track C: SEALED/LOCKED. Track B: NOT_SUPPORTED.
- Track A: ON-TRIGGER/MONITOR ONLY. Latest blocker: `research_state/liquidation_forward_validate_017_blocker_20261105T122444Z.md`. Latest sweep: `research_state/campaign_sweep_tracka_20261105T122444Z.md`. Frontier: `research_state/experiment_frontier.json` updated (`last_checked_utc` 2026-11-05T12:24:44Z, `track_a_blocked=true`, `artifact_churn_097`).
- Artifact churn (097, counted): root `research_state/*.md+*.json` = **159** (157 baseline + 2 required evidence: sweep+017 blocker). Ironflow probes = **2** (canonical digest + 1 live). No new recurring timestamped probe/scan families. Canonical alt outputs only.
- Strict-manifest defaults + compat (097, measurable): `scripts/tracka_rubric.py` adds strict full-manifest default path (`assess_strict_manifest` / `strict_tracka_manifest=True`) and `minimal_fixture_compat=True` legacy path. **Strict mode fail-closes** for GO-shaped observed Hyperliquid claims that satisfy only minimal fields but lack machine-verifiable access/dataset provenance, label definition, and required evidence (months/blocks/symbol proof/raw-epoch normalization where claimed). **Compat/default legacy preserved** (093-096 suites remain green: 67 tests). Rubric adversarial 093-097 = **79 tests green** (+12, `tests/test_tracka_adversarial_rubric_097.py`).
- Resume gate (097): `scripts/tracka_resume_check.py` validates strict rejects minimal-only GO-shaped, compat preserved, strict accepts full machine-verifiable manifest (+legacy checks) — **8 checks, PASS <5s, offline/no-network/no-real-writes**, JSON contract intact.
- Monitor network-isolation proof (097): `tests/test_monitor_network_isolation_097.py` = **6 tests green** (tmp dirs + mocks/patches) proving `verify_state`, `check_baseline_drift`, `evaluate_resume_decision`, `simulate_resume`, and isolated CLI `--verify`/`--decision` do **not** call network primitives in tested state-only/decision paths and do **not** mutate real `research_state`. (`--quick`/`--scan` remain network probes by design.)
- Watch residue consolidation/audit (097, safe/generator-compatible): all `trigger_harden_*` live in watch root = **1** (`trigger_harden_20261104T113550Z.json`); **non-20261104T live residue = 0**. 096 archive preserved (27 files + provenance manifest). No unsafe moves. Read-only compatibility proof: non-recursive generator globs in `scripts/write_trigger_harden_successor.py` and `scripts/track_c_inventory_harden.py` resolve previous snapshot to kept live file; archive excluded. No generators broken.
- Trigger probe (20261105T121645Z): `monitor --quick` **NO RESUME TRIGGER** (`data_through=2026-10`; probed 2026-11..2027-02 absent; probe_diff no change; baseline drift intact; kaggle mirror unchanged/triggered false). `deep_review`/`hunt` refreshed canonical latest; **no rubric-GO (strict or legacy) source**. No prereg created; no outcome inspection.
- **NO COASTING.** Status-only output without measurable hardening delta is noncompliant.

## SINGLE INITIAL TASK MESSAGE FOR NEXT AGENTIC SESSION (COPY/PASTE VERBATIM)
```text
TASK ID: FCLR-NEXT-098-TRACK-A-NO-COAST-STRICT-GATE-HARNESS-INTEGRATION-AND-TRIGGER-PATH-PROOF
PRIORITY: P0 - REPO-NAME PRIORITIZED (Volatility SEALED/LOCKED; Liquidation Risk = ONLY ACTIVE OBJECTIVE)
TIMESTAMP (UTC): 20261105T122444Z
CAMPAIGN: TRACK A LIQUIDATION RISK - IMPOSSIBLE-TO-COAST WHILE BLOCKED. MEASURABLE DELTA REQUIRED. ZERO CHURN. INSTANT IRREFUTABLE RESUME.
ENFORCEMENT: ALL STEPS MANDATORY. SESSION FAILS IF ONLY REPORTS/PROBES OR IF IT REPEATS 097 WITHOUT EXTENDING IT. PREREGISTER BEFORE INSPECTING OUTCOMES IF TRIGGERED. NO IDLE TURNS. NO STATUS-ONLY OUTPUT. NO NEW TIMESTAMPED PROBE/SWEEP/SCAN FAMILIES. NO SCHEDULERS/POLLERS/STATUS FILES/REPEATED WRAPPERS/AGENT-CONTROLLERS. NO WORKFLOW CHANGES.

OBJECTIVE (INFERRED): Complete liquidation-risk half of "Funding-conditioned-volatility-and-liquidation-risk". Data blocked (Hyperliquid data_through 2026-10; 2026-11.. absent). While blocked produce measurable hardening delta against 097 baseline (root md+json 159, probes 2, tests 244, rubric 093-097=79, resume 8 checks PASS <5s, watch live 1/non-20261104T 0): (A) keep root md+json <=161 and ironflow probes == 2; no new recurring timestamped families, (B) **integrate strict-manifest rubric into the actual Track A resume/forward-experiment gate path**: make `fclr010_harness` (and/or a dedicated gate used by resume flow) evaluate candidate manifests with `assess_strict_manifest` by default for GO decisions, reject minimal-only GO-shaped manifests, preserve explicit compat/test-fixture path where needed; add deterministic tests proving harness/gate path rejects minimal-only and accepts full manifest, (C) add **offline trigger-simulation proof** (deterministic, no network, tmp-only) that a synthetic rubric-GO strict manifest + mocked/fixture 2026-11+ availability path would produce a PREREG-BEFORE-OUTCOMES resume decision (blocked until prereg written; no outcome inspection), covering the exact handoff decision branches, (D) **reduce `research_state/url_probe_cache.json`/alt cache churn risk**: add a deterministic test or mechanism proving deep_review/hunt in cache-only/test mode does not create new recurring timestamped artifacts and does not grow real cache beyond bounded/expected behavior when inputs unchanged (tmp-isolated), (E) audit `AGENT_HANDOFF.md`/frontier/handoff drift: ensure only `AGENT_HANDOFF.md` is the single durable root handoff and no stale handoff copies cause confusion; if cleanup is safe and provenance-preserving do it with tests/evidence, else provide tested incompatibility proof and exact references, (F) exhaustive trigger probes; single canonical blocker/update with full before/after metrics. PREREGISTER BEFORE INSPECTING OUTCOMES IF TRIGGERED. Never stop for "no data".

CONSTRAINTS: No credentials/manual files/.github/workflows changes. Leakage-safe, preregister-before-outcomes. Track C/B locked/unsupported. Raw data/caches out of git. Clean-clone reproducible. Hyperliquid-only for Track A. Never conflate observed/modeled liquidations. No threshold-shopping. Canonical outputs only (`ironflow_probe_digest_latest.json` + 1 live probe; `alt_source_scan_latest.json`; `alt_source_deep_review_latest.md`).

MANDATORY EXECUTION (ALL REQUIRED; CONCRETE METRICS):
1) ENTRY VERIFY: `python -m unittest discover tests` (>=244 green). Run `monitor --quick`, `deep_review`, `hunt`, `python scripts/tracka_resume_check.py`. Record exact root md+json, probes, tests, watch counts. If NO NEW DATA, continue to hardening.
2) HARNESS/GATE STRICT INTEGRATION (MEASURABLE): Implement + tests. Prove minimal-only manifest cannot pass GO gate in default/strict path; full manifest can pass gate checks (deterministic fixtures, no network).
3) OFFLINE PREREG-BEFORE-OUTCOMES RESUME SIMULATION (MEASURABLE): Deterministic test/fixture proving trigger path requires prereg before outcomes; blocked/no-inspection otherwise. No network, tmp-only, no real research_state mutation.
4) ALT/CACHE CHURN SAFETY (MEASURABLE): Deterministic proof (tmp-isolated, mocked/fixture) for deep_review/hunt cache behavior; no new recurring timestamped families; bounded/no unexpected real-file mutation.
5) HANDOFF DRIFT AUDIT/CLEANUP (MEASURABLE OR TESTED INCOMPATIBILITY): Document exact durable handoff contract; safe cleanup only with evidence/tests.
6) EVIDENCE, FRONTIER, HANDOFF (MANDATORY): Write `research_state/campaign_sweep_tracka_$(date -u +%Y%m%dT%H%M%SZ).md` and `research_state/liquidation_forward_validate_018_blocker_$(date -u +%Y%m%dT%H%M%SZ).md` with full before/after metrics, strict gate integration proof, prereg-before-outcomes simulation proof, alt/cache churn proof, handoff-drift proof, probe evidence, concrete resume instructions. Update `research_state/experiment_frontier.json`. Update `AGENT_HANDOFF.md` with NEW stricter timestamped task FCLR-NEXT-099 naming exact uncovered gaps and not satisfiable by status reporting.

RESUME CONDITION (only): ironflow `data/events/YYYY-MM.parquet` or `data/fills/YYYY-MM.parquet` month>=2026-11 HTTP 200 unauthenticated OR admissible unauthenticated Hyperliquid source passes strict GO rubric/full-manifest gate. Hyperliquid-only. PREREGISTER BEFORE INSPECTING OUTCOMES.

STOP RULE: Complete ALL steps + artifacts with concrete metrics. Track C locked. Track B unsupported. No conflation. No workflow/scheduler/poller/status-only/repeated wrappers/agent-controllers/new recurring families. Blocked/no-data claims without measurable hardening delta are noncompliant. Leave state STRICTER than found.
```

## VERIFICATION COMMANDS (RUN ON ENTRY)
- `python -m unittest discover tests` (must be >=244, green)
- `python scripts/tracka_resume_check.py` (must print JSON with `"pass": true`, <5s, includes strict/compat/full-manifest checks)
- `python scripts/monitor_ironflow_liquidations.py --quick`
- `python scripts/deep_review_alt_sources.py`
- `python scripts/hunt_alternative_liquidation_sources.py`
- `python scripts/fclr010_harness.py` (frozen config, offline)

## NEXT TASK (TIMESTAMPED)
20261105T122444Z: Execute FCLR-NEXT-098. Volatility (Track C) SEALED/LOCKED. Liquidation Risk (Track A) = ONLY ACTIVE OBJECTIVE. 097 delivered: 244 tests green (+18); rubric 093-097=79 (+12) with strict full-manifest defaults + minimal_fixture_compat (093-096 preserved); resume 8 checks PASS <5s/offline/no-network/no-real-writes proving strict rejects minimal-only GO-shaped, compat preserved, strict accepts full manifest; monitor network-isolation proofs +6 (state-only/decision/simulate/--verify/--decision tmp-isolated, network mocked not called, real `research_state` unchanged); watch live 1/non-20261104T 0 with generator-compatible audit; root md+json 159, probes 2, no new recurring families. Trigger NO DATA. PREREG BEFORE OUTCOMES if triggered. 098 must integrate strict gate into harness/resume path, add offline prereg-before-outcomes trigger simulation, and prove alt/cache churn safety + handoff-drift audit/cleanup with concrete metrics.
