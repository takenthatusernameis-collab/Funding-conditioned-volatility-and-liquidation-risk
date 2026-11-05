# AGENT_HANDOFF.md (SINGLE DURABLE HANDOFF)
Timestamp (UTC): 20261105T131205Z
Git SHA (HEAD, baseline): c1a6cbf3 (working tree modified by 098 hardening; not committed)
Branch: main
Repo: Funding-conditioned-volatility-and-liquidation-risk
Handoff ID: FCLR-HANDOFF-20261105T131205Z | Priority: P0 - REPO-NAME PRIORITIZED + HEAVY WORK MANDATORY | Mode: CAMPAIGN-DRIVEN | Enforcement: NO-SKIP | Bottleneck-State: HARDENED-HEAVY-098-COMPLETE

## REPO-NAME PRIORITIZATION (INFERRED)
Repository name: "Funding-conditioned-volatility-and-liquidation-risk"
- Funding-conditioned VOLATILITY component = Track C (FCLR-011) — **SEALED/LOCKED**. Forecast gate PASSED. DO NOT retune/re-run sealed cells/conflate.
- LIQUIDATION RISK component = Track A (FCLR-010) — **ONLY UNFINISHED HALF**. BLOCKED on admissible unauthenticated liquidation data (Hyperliquid-only). Track B = **NOT_SUPPORTED**.
- BOTH components are core to repo identity. NO SCOPE DRIFT TO SEALED TRACKS.

## CURRENT VERIFIED STATE (098, MEASURABLE DELTA DELIVERED)
- Tests: `python -m unittest discover tests` — **261 tests, OK** (097 baseline 244; +17 via `tests/test_tracka_hardening_098.py`). MUST remain green.
- Track C: SEALED/LOCKED. Track B: NOT_SUPPORTED.
- Track A: ON-TRIGGER/MONITOR ONLY. Latest blocker: `research_state/liquidation_forward_validate_018_blocker_20261105T131205Z.md`. Latest sweep: `research_state/campaign_sweep_tracka_20261105T131205Z.md`. Frontier: `research_state/experiment_frontier.json` updated (`last_checked_utc` 20261105T131205Z, `track_a_blocked=true`, `artifact_churn_098`).
- Artifact churn (098, counted): root `research_state/*.md+*.json` = **161** (159 baseline + 2 required evidence: sweep+018 blocker, `<=161`). Ironflow probes = **2** (canonical digest + 1 live `ironflow_probe_20261105T130449Z.json`). No new recurring timestamped probe/scan families. Canonical alt outputs only.
- **Strict manifest gate integrated into harness/resume path (098, measurable):** `scripts/fclr010_harness.py` adds `evaluate_source_manifest` (default `strict=True` => `assess_strict_manifest`; explicit compat `strict=False` => `assess_minimal_fixture`) and rewrites `evaluate_forward` to enforce **PREREG-BEFORE-OUTCOMES always** plus **strict manifest GO gate by default when `source_manifest` is provided** (rejects minimal-only GO-shaped manifests; accepts full machine-verifiable manifest). Explicit compat fixture/test path: `strict_manifest_gate=False`. **Legacy callers without `source_manifest` preserve prior prereg/data-block behavior** (091/092/094/`test_fclr010_harness` green). Proofs: `test_tracka_hardening_098.py`.
- **Offline prereg-before-outcomes trigger simulation (098, deterministic):** 4 decision branches, tmp-only, no network, real `research_state` snapshot unchanged: (1) minimal-only manifest NO-GO blocks even with mocked 2026-11+ data+prereg, `outcomes_inspected=False`; (2) strict-GO manifest + no prereg => blocked, `prereg_required=True`, gate GO attached, no inspect; (3) strict-GO + missing prereg file => blocked/no inspect; (4) strict-GO + prereg present + mocked data present => `READY_FROZEN`, `outcomes_inspected=False`. <5s.
- **Alt/cache churn safety (098, deterministic tmp-isolated):** `deep_review`/`hunt` exercised with redirected tmp caches/paths and mocked hunt cache/probe interfaces produce canonical latest outputs only; **no recurring timestamped families**; repeated cache loads do not mutate real `research_state/url_probe_cache.json` (mtime/size snapshot unchanged).
- **Handoff drift audit/contract (098, tested):** single durable root handoff is `AGENT_HANDOFF.md` only. Repo-wide scan confirms no copies in `research_state/`, `scripts/`, `tests/`, `src/` (no stale copies found; no unsafe cleanup needed). Deterministic proof in `tests/test_tracka_hardening_098.py`.
- Resume gate: `scripts/tracka_resume_check.py` JSON `pass:true`, 8 checks, `<5s`, `network:false`, `writes_real_research_state:false` (strict rejects minimal-only GO-shaped, compat preserved, strict accepts full manifest + legacy checks).
- Trigger probe (20261105T130449Z): `monitor --quick` **NO RESUME TRIGGER** (`data_through=2026-10`; probed 2026-11..2027-02 absent; head_probes=8; probe_diff no change; baseline drift intact/content hash complete/18 pairs; kaggle mirror unchanged/triggered false). `deep_review`/`hunt` refreshed canonical latest; **no rubric-GO strict source**. No prereg created for real data; no outcome inspection.
- **NO COASTING.** Status-only output without measurable hardening delta is noncompliant.

## SINGLE INITIAL TASK MESSAGE FOR NEXT AGENTIC SESSION (COPY/PASTE VERBATIM)
```text
TASK ID: FCLR-NEXT-099-TRACK-A-NO-COAST-STRICT-TRIGGER-PATH-CLI-WIRING-AND-OUTCOME-ISOLATION-PROOF
PRIORITY: P0 - REPO-NAME PRIORITIZED (Volatility SEALED/LOCKED; Liquidation Risk = ONLY ACTIVE OBJECTIVE)
TIMESTAMP (UTC): 20261105T131205Z
CAMPAIGN: TRACK A LIQUIDATION RISK - IMPOSSIBLE-TO-COAST WHILE BLOCKED. MEASURABLE DELTA REQUIRED. ZERO CHURN. INSTANT IRREFUTABLE RESUME.
ENFORCEMENT: ALL STEPS MANDATORY. SESSION FAILS IF ONLY REPORTS/PROBES OR IF IT REPEATS 098 WITHOUT EXTENDING IT. PREREGISTER BEFORE INSPECTING OUTCOMES IF TRIGGERED. NO IDLE TURNS. NO STATUS-ONLY OUTPUT. NO NEW TIMESTAMPED PROBE/SWEEP/SCAN FAMILIES. NO SCHEDULERS/POLLERS/STATUS FILES/REPEATED WRAPPERS/AGENT-CONTROLLERS. NO WORKFLOW CHANGES.

OBJECTIVE (INFERRED): Complete liquidation-risk half of "Funding-conditioned-volatility-and-liquidation-risk". Data blocked (Hyperliquid data_through 2026-10; 2026-11.. absent). While blocked produce measurable hardening delta against 098 baseline (root md+json 161, probes 2, tests 261, strict gate integrated in harness with explicit compat, offline prereg-before-outcomes simulation 4 branches, alt/cache churn tmp-isolated proof, single durable handoff audited): (A) keep root md+json <=163 and ironflow probes == 2; no new recurring timestamped families, (B) wire strict manifest gate + prereg-before-outcomes into the actual operator/CLI resume path (e.g., `scripts/tracka_resume_check.py` and/or a dedicated `scripts/tracka_resume_gate.py`/monitor decision hook): default strict GO manifest + prereg-present check before any forward execution; explicit compat/test-fixture flag only; deterministic tests prove CLI/gate refuses to proceed without prereg and refuses minimal-only manifest on default path, (C) add outcome-isolation proof: tmp-isolated deterministic test that a mocked data path with synthetic "outcome" content is never read/parsed when prereg is absent or manifest is NO-GO (assert file reads/counts or monkeypatched loaders not called); no real data writes, (D) extend watch/handoff/alt contracts with machine-checkable invariants test (single root handoff, canonical alt outputs only, probe count==2, watch trigger_harden live<=1 and non-20261104T==0, no recurring timestamped probe/scan families in root) — fail-closed on drift, (E) exhaustive trigger probes; single canonical blocker/update with full before/after metrics. PREREGISTER BEFORE INSPECTING OUTCOMES IF TRIGGERED.

CONSTRAINTS: No credentials/manual files/.github/workflows changes. Leakage-safe, preregister-before-outcomes. Track C/B locked/unsupported. Raw data/caches out of git. Clean-clone reproducible. Hyperliquid-only for Track A. Never conflate observed/modeled liquidations. No threshold-shopping. Canonical outputs only (`ironflow_probe_digest_latest.json` + 1 live probe; `alt_source_scan_latest.json`; `alt_source_deep_review_latest.md`).

MANDATORY EXECUTION (ALL REQUIRED; CONCRETE METRICS):
1) ENTRY VERIFY: `python -m unittest discover tests` (>=261 green). Run `monitor --quick`, `deep_review`, `hunt`, `python scripts/tracka_resume_check.py`. Record exact root md+json, probes, tests, watch counts. If NO NEW DATA, continue to hardening.
2) CLI/OPERATOR STRICT RESUME GATE WIRING (MEASURABLE): Implement + deterministic tests. Prove default path blocks without prereg and blocks minimal-only manifest; accepts full strict manifest+prereg in tmp fixture; explicit compat flag only.
3) OUTCOME-ISOLATION PROOF (MEASURABLE): Tmp-isolated test proving no outcome/data content read/parsed when prereg absent or manifest NO-GO (monkeypatch/asserts). No network, no real research_state mutation.
4) MACHINE-CHECKABLE DRIFT INVARIANTS (MEASURABLE): Single fail-closed test/module covering handoff, canonical alt outputs, probe count, watch residue limits, and no recurring timestamped probe/scan families.
5) EVIDENCE, FRONTIER, HANDOFF (MANDATORY): Write `research_state/campaign_sweep_tracka_$(date -u +%Y%m%dT%H%M%SZ).md` and `research_state/liquidation_forward_validate_019_blocker_$(date -u +%Y%m%dT%H%M%SZ).md` with full before/after metrics, CLI wiring proof, outcome-isolation proof, invariant proof, probe evidence, concrete resume instructions. Update `research_state/experiment_frontier.json`. Update `AGENT_HANDOFF.md` with NEW stricter timestamped task FCLR-NEXT-100 naming exact uncovered gaps and not satisfiable by status reporting.

RESUME CONDITION (only): ironflow `data/events/YYYY-MM.parquet` or `data/fills/YYYY-MM.parquet` month>=2026-11 HTTP 200 unauthenticated OR admissible unauthenticated Hyperliquid source passes strict full-manifest GO gate (`assess_strict_manifest`/harness default). Hyperliquid-only. PREREGISTER BEFORE INSPECTING OUTCOMES.

STOP RULE: Complete ALL steps + artifacts with concrete metrics. Track C locked. Track B unsupported. No conflation. No workflow/scheduler/poller/status-only/repeated wrappers/agent-controllers/new recurring families. Blocked/no-data claims without measurable hardening delta are noncompliant. Leave state STRICTER than found.
```

## VERIFICATION COMMANDS (RUN ON ENTRY)
- `python -m unittest discover tests` (must be >=261, green)
- `python scripts/tracka_resume_check.py` (must print JSON with `"pass": true`, <5s, strict/compat/full-manifest checks)
- `python scripts/monitor_ironflow_liquidations.py --quick`
- `python scripts/deep_review_alt_sources.py`
- `python scripts/hunt_alternative_liquidation_sources.py`
- `python scripts/fclr010_harness.py` (frozen config, offline)

## NEXT TASK (TIMESTAMPED)
20261105T131205Z: Execute FCLR-NEXT-099. Volatility (Track C) SEALED/LOCKED. Liquidation Risk (Track A) = ONLY ACTIVE OBJECTIVE. 098 delivered: 261 tests green (+17); strict manifest gate integrated into `fclr010_harness` default manifest-bearing path (minimal-only rejected, full manifest accepted) with explicit compat/legacy preservation; offline prereg-before-outcomes trigger simulation proved 4 branches (tmp-only/no network/no real `research_state` mutation); alt/cache churn safety proved (tmp-isolated canonical outputs, no recurring families, no real cache mutation); handoff drift audited (single root `AGENT_HANDOFF.md`). Trigger NO DATA (probe 20261105T130449Z). PREREG BEFORE OUTCOMES if triggered. 099 must wire strict gate+prereg into CLI/operator resume path, add outcome-isolation proof (no outcome reads before prereg/GO), and add machine-checkable drift-invariant test with concrete metrics.
