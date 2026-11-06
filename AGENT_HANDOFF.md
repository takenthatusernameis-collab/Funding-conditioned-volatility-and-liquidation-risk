# AGENT_HANDOFF.md (SINGLE DURABLE HANDOFF) — READ THIS FILE FIRST
Timestamp (UTC): 20261106T051000Z
Handoff ID: FCLR-HANDOFF-20261106T051000Z
Baseline (prior session): FCLR-NEXT-118 COMPLETE (20261106T035900Z). **This session (20261106T045619Z, FCLR-NEXT-119) delivered measurable code+test hardening (G1-G5, no trigger).** No new probes/families. Working tree may contain local modified `__pycache__` and `research_state/ironflow_fastpath_cache.json` — **do not commit**.
Branch: main | Repo: Funding-conditioned-volatility-and-liquidation-risk
Priority: P0 — REPO-NAME PRIORITIZED + HEAVY WORK MANDATORY | Mode: CAMPAIGN-DRIVEN | Enforcement: NO-SKIP/NO-COAST
Bottlenecks removed this session (measurable): (1) READY_FROZEN end-to-end testability added without real outcomes/network (G1). (2) h004 allowed-path Hyperliquid Track A canonical-target boundary machine-asserted (G2). (3) Repo-local script-scope registry drift check added + registry/117 reconciled incl. new script (G3). (4) `run_liqmicro_v2` top-level statsmodels import deferred to post-gate `_run_pipeline` (blocked/testable without statsmodels) + no-frontier-mutation parity asserted (G4). (5) Experiment-frontier mutation audit across blocked `run_liqmicro_v2` and all `guarded_tracka_ready_writing` scripts (G5). **Data bottleneck unchanged:** IRONFLOW PROBING EXHAUSTED (90+ CONFIRMED_ABSENT), `data_through=2026-10`, 2026-11..2027-02 absent. Do NOT re-probe absent months.

## INITIAL TASK FOR NEXT AGENTIC SESSION (SINGLE, TIMESTAMPED, MANDATORY) — 20261106T045619Z
**Execute FCLR-NEXT-120.** This is the ONLY active objective. Do not run status-only loops. Do not re-probe absent ironflow months (exhausted, 90+ CONFIRMED_ABSENT). Do not touch sealed Track C/B. Deliver measurable **code+test** hardening when no trigger appears. Blocked/no-data claims without measurable hardening delta are noncompliant.

TASK ID: FCLR-NEXT-120-HARNESS-EXPLICIT-SEAM-GO-MANIFEST-ONLY-READY-FROZEN-MATRIX + TRACKA-SCRIPT-REGISTRY-AUTO-DISCOVERY-GUARD-FROM-CODE + GUARDED-AUDIT-READY-WRITING-NO-READY-MATRIX + RUN_LIQMICRO_V2-READY-PIPELINE-CANONICAL-SURFACE-INVENTORY + H004-ALLOWED-PILOT-SANDBOX-PATH-ENFORCEMENT
PRIORITY: P0 — LIQUIDATION RISK (Track A) is the ONLY unfinished/active repo objective (Funding-conditioned VOLATILITY Track C sealed/locked).
TIMESTAMP (UTC): 20261106T045619Z
ENFORCEMENT: ALL STEPS MANDATORY. NO STATUS-ONLY OUTPUT. ENTRY VERIFY IS MANDATORY BUT INSUFFICIENT ALONE. NO NEW TIMESTAMPED PROBE/SWEEP/SCAN/WRAPPER/REPORT FAMILIES IN RESEARCH_STATE UNLESS A STRICTLY ADMISSIBLE TRIGGER APPEARS (THEN: PREREG BEFORE INSPECTING OUTCOMES; blocker/prereg+result evidence only, ROOT BOUND PRESERVED). NO SCHEDULERS/POLLERS/STATUS FILES/REPEATED WRAPPERS/AGENT-CONTROLLERS. NO `.github/workflows` CHANGES. NO RE-IRONFLOW-PROBE OF ABSENT MONTHS. Hyperliquid-only for Track A observed-liquidation gate. NEVER conflate observed vs modeled liquidations. No threshold-shopping. Track C/B locked/unsupported.

### MANDATORY DELIVERABLES (G1-G5, ALL REQUIRED when no trigger)
1. **G1 (harness READY_FROZEN with explicit admissible seam GO, manifest-only, tmp-isolated):** Add deterministic tmp-isolated tests that construct the *smallest* machine-verifiable manifest-only admissible candidate accepted by `tracka_resume_check.admissible_seam_check` / `fclr010_harness._evaluate_admissible_seam` (no network, no parquet/outcome reads) so `FCLR010Harness.execute_ready_data_load` reaches `READY_FROZEN` with an explicit outcome_loader and returns `data_loaded_implicitly:false`, `EXPLICIT_LOADER_AFTER_GATES`; assert no canonical `evaluation_summary*FCLR010`/`run_manifest.json`/`experiment_frontier.json`/`cross_track_decision_log.md` mutation. Also assert NO-GO seam refuses before loader. No real trigger data; use synthetic manifest fixtures only.
2. **G2 (scope registry auto-discovery guard from code, repo-local):** Strengthen `scripts/check_tracka_scope_registry_drift.py` and tests so drift fails not only on filename set mismatch but also when a registered class is inconsistent with cheap source heuristics for *guarded/liquidation-risk* classes (e.g., scripts classified `guarded_tracka*` must reference `guarded_execute`/`FCLR010Harness`/explicit refusal contract tokens; `raw_fetch_monitor_provenance` must not be `guarded_tracka_ready_writing`; `track_c_*`/`track_b_*` must not be labeled guarded Track A). Keep deterministic, no network, no imports that execute heavy deps. Preserve root<=163/probes==2.
3. **G3 (guarded_tracka_audit_ready_writing NO-READY refusal matrix):** Extend the 119/118-style matrix to `fclr010_coverage_audit.py` and `liqmicro_audit.py` (audit-ready-writing class) across missing prereg, NOGO seam, modeled/proxy, wrong venue states with tmp-isolated canonical target snapshots proving no canonical mutation and stable refusal payload/rc where applicable. No network/parquet/outcome reads.
4. **G4 (run_liqmicro_v2 READY-pipeline canonical-surface inventory, source + tmp contract):** Without executing real outcomes, add tests that inventory every `RESEARCH_STATE`/`RESULTS_DIR`/`evaluation_summary_FCLR-LIQMICRO-002` write in `_run_pipeline` and assert `_run_pipeline` is unreachable on all blocked guard states; add a READY-branch contract test that monkeypatches `guarded_execute` to return READY_FROZEN with synthetic loader outputs but patches/mocks downstream heavy deps (`LiqMicroFeatures/Models/Stats`, file writes) so the READY branch reaches `_run_pipeline` in a fully sandboxed temp dir (no real `research_state`/`results` writes) and no `experiment_frontier.json` mutation occurs. Document that v2 has no frontier writer by contract.
5. **G5 (h004 allowed-pilot sandbox path enforcement):** Add a machine-enforced test/guard proving that if `H004_ALLOW_FLAG`/env is set, any pilot output paths (`OUT_SUM`/`LIQ_ENUM`/`CKPT_PANEL`/`RUN_MANIFEST`/`HYP` module constants or computed write targets) must resolve under an explicit sandbox/temp root or be refused — *without running the pilot against real census data*. Implement the smallest code guard needed (refuse allowed mode unless sandbox env/arg is set, or redirect constants only in a testable hook) so allowed mode cannot accidentally write pilot artifacts into real `research_state/` during future hardening/tests. Preserve default refusal semantics and Hyperliquid canonical-target quarantine.

### MANDATORY EXECUTION (ALL REQUIRED; CONCRETE METRICS)
1) **ENTRY VERIFY** (record exact): `python -m unittest discover tests` (>=484 green). `python scripts/tracka_resume_check.py` (>=17 checks, incl. `probe_invariant_runtime_named`+`admissible_seam_wired`, pass). `python scripts/tracka_resume_gate.py --prereg /nonexistent` (`drift_preflight.pass:true`, stable reason/order, `outcomes_inspected:false`). `python scripts/tracka_operator_report.py; echo $?` (`pass:true`, exit 0). `python scripts/check_tracka_scope_registry_drift.py --json` (`pass:true`). Record root md+json (<=163) and probes (==2). Do NOT re-probe ironflow absent months.
2) **TRIGGER CHECK** (bounded, no new families): inspect latest monitor/probe state only (`research_state/ironflow_probe_20261105T200406Z.json` / `ironflow_probe_digest_latest.json`). No new recurring probe/scan files.
3) **NO-TRIGGER HEAVY-WORK HARDENING DELTA** (REQUIRED): deliver G1-G5 with `tests/test_tracka_hardening_120.py` (tmp-isolated, deterministic, no network, no parquet/outcome reads, no real `research_state` writes). Make refusal/guards machine-enforced in code only if needed.
4) **TRIGGER PATH** (only if appears): ironflow `data/events|data/fills/YYYY-MM.parquet` month>=2026-11 HTTP 200 unauthenticated OR admissible unauthenticated Hyperliquid source passes strict full-manifest GO gate => validate via seam (manifest-only) + **PREREGISTER BEFORE INSPECTING OUTCOMES**; execute forward validation through guarded data-load path only; Hyperliquid-only; separate observed vs modeled; canonical outputs; respect root bound.
5) **HANDOFF/FRONTIER** (required on completion): update `AGENT_HANDOFF.md` and `research_state/experiment_frontier.json` with concrete before/after metrics (suite count, changed files, reason-code table, G1-G5 status) and emit **FCLR-NEXT-121** (stricter, naming exact uncovered gaps). Run full `python -m unittest discover tests`; report before/after.

### ACCEPTANCE
- Full suite green (>=484 before, report after). Resume 17 PASS. Gate stable (`drift_preflight.pass:true`, `outcomes_inspected:false`). Operator `pass:true` exit 0. Drift check `pass:true`.
- G1-G5 covered by tmp-isolated deterministic tests; no network/parquet/outcome reads; no real `research_state` writes in tests.
- Root `research_state/*.md+*.json` <=163; probes==2. No `.github/workflows` changes. No `__pycache__`/`ironflow_fastpath_cache.json` committed.

RESUME/GO CONDITION (data trigger only): ironflow `data/events/YYYY-MM.parquet` or `data/fills/YYYY-MM.parquet` month>=2026-11 HTTP 200 unauthenticated OR admissible unauthenticated Hyperliquid source passes strict full-manifest GO gate. Hyperliquid-only. **PREREGISTER BEFORE INSPECTING OUTCOMES.**
STOP RULE: Complete ALL steps with concrete metrics. Track C locked. Track B unsupported. No conflation. No workflow/scheduler/poller/status-only/repeated wrappers/agent-controllers/new recurring families. Blocked/no-data claims without measurable hardening delta are noncompliant. Keep root md+json <=163 and probes==2. Leave state STRICTER than found.

## REPO-NAME PRIORITIZATION (INFERRED)
Repository: `Funding-conditioned-volatility-and-liquidation-risk`
- **Funding-conditioned VOLATILITY** = Track C (FCLR-011) — **SEALED/LOCKED**. Forecast gate PASSED. DO NOT retune/re-run/conflate.
- **LIQUIDATION RISK** = Track A (FCLR-010) — **ONLY UNFINISHED / ONLY ACTIVE OBJECTIVE**. BLOCKED on admissible unauthenticated liquidation data (Hyperliquid-only, `data_through=2026-10`; 2026-11..2027-02 absent). Track B = **NOT_SUPPORTED**.

## CURRENT VERIFIED STATE (entry verify + 119 completion, 20261106T045619Z)
- Tests: **484/484 OK** (`Ran 484 tests in 44.999s`, `OK`) — was 469 before 119.
- Resume: **17 checks PASS** (`tracka_resume_check`, incl. `probe_invariant_runtime_named` + `admissible_seam_wired`, `network:false`, `writes_real_research_state:false`).
- Gate: `drift_preflight.pass:true`, `status=BLOCKED`, `reason_code=PREREG_OR_MANIFEST_BLOCK_AFTER_DRIFT_PASS`, `fail_closed_order=drift_preflight->manifest_prereg`, `outcomes_inspected:false`.
- Operator: `pass:true`, exit `0`, `network:false`, `read_only:true`, `writes_real_research_state:false`.
- Scope drift check (new): `scripts/check_tracka_scope_registry_drift.py --json` `pass:true`, `scripts=83 registry=83 reason=OK`.
- Monitor/trigger: **NO TRIGGER**. `ironflow_probe_20261105T200406Z.json` (+ digest) — `data_through=2026-10`, 2026-11..2027-02 absent. **IRONFLOW PROBING EXHAUSTED (90+ CONFIRMED_ABSENT) — do not re-probe.**
- Artifacts: root `research_state/*.md+*.json` = **143** (<=163). Ironflow probes = **2**.
- Working-tree hygiene: local modified `__pycache__` and `research_state/ironflow_fastpath_cache.json` — **never commit**.

## FCLR-NEXT-119 DELIVERABLES (20261106T045619Z, COMPLETE, NO TRIGGER)
| Gap | Deliverable | Status | Evidence |
|---|---|---|---|
| G1 | READY_FROZEN end-to-end testability (no real outcomes/network): explicit loader invoked once only after gates; blocked never calls loader; source-order invariant (`evaluate_forward` precheck `outcome_loader=None`, `READY_FROZEN` gate before loader) | COMPLETE | `tests/test_tracka_hardening_119.py::Test119G1ReadyFrozenEndToEnd` (3 tests) |
| G2 | h004 allowed-path Hyperliquid Track A canonical-target boundary; default refused/no canonical mutation; allowed mode refuses if seam flag flipped; no `FCLR010Harness`/`fclr010_guarded_entry`/`guarded_execute(` tokens; canonical-target quarantine declared | COMPLETE | `Test119G2H004AllowedPathBoundary` (4 tests) |
| G3 | Repo-local scope-registry drift enforcement + reconciliation | COMPLETE | `scripts/check_tracka_scope_registry_drift.py` (new, read-only/deterministic), `research_state/tracka_script_scope_registry.json` (+`check_tracka_scope_registry_drift.py` entry, 83 scripts), `tests/test_tracka_hardening_117.py` SCRIPT_REGISTRY reconciled (83), `Test119G3ScopeRegistryDriftEnforcement` (4 tests) |
| G4 | `run_liqmicro_v2` no-frontier-mutation surface + blocked isolation | COMPLETE | deferred `models/stats` imports to post-gate `_run_pipeline` in `scripts/run_liqmicro_v2.py` (testable blocked path without statsmodels); source asserts no `experiment_frontier`/frontier writer and pipeline only after READY guard; `Test119G4RunLiqmicroV2NoFrontierMutation` (2 tests) |
| G5 | `experiment_frontier.json` mutation audit (blocked v2 + all `guarded_tracka_ready_writing`) | COMPLETE | `Test119G5ExperimentFrontierMutationAudit` (2 tests; audited 4 guarded ready-writing scripts: `coupled_robust_eval.py`, `fclr010_execute.py`, `overlay_quick.py`, `overlay_tracka_execute.py`) |

## CHANGED FILES (119)
- `scripts/check_tracka_scope_registry_drift.py` (new)
- `scripts/run_liqmicro_v2.py` (deferred heavy `liqmicro.models/stats` imports to post-gate `_run_pipeline`)
- `research_state/tracka_script_scope_registry.json` (+`check_tracka_scope_registry_drift.py`, count 83, generated 20261106T045619Z)
- `tests/test_tracka_hardening_117.py` (SCRIPT_REGISTRY reconciled +1)
- `tests/test_tracka_hardening_119.py` (new, 15 tests, tmp-isolated)
- `AGENT_HANDOFF.md` (this file)
- `research_state/experiment_frontier.json` (119/120 frontier update)

## 120 UNCOVERED GAPS (exact, code+tests required)
- Harness `READY_FROZEN` with an *explicit admissible seam GO* manifest (not legacy `seam=None`) is not yet exercised end-to-end with a machine-accepted minimal manifest fixture; current 119 G1 proves READY_FROZEN via `source_manifest=None/admissible_manifest=None`. Add manifest-only minimal GO fixture proving seam pass -> prereg/data -> explicit loader, and seam NO-GO -> refusal before loader.
- Drift check validates filename set + entry shape but not class/source semantic consistency (e.g., a guarded class missing `guarded_execute` tokens, or wrong track labels). Add cheap deterministic source-heuristic consistency checks for guarded/liquidation classes.
- `guarded_tracka_audit_ready_writing` scripts (`fclr010_coverage_audit.py`, `liqmicro_audit.py`) not covered by the 119 G5 frontier/writer refusal matrix across all non-READY states (missing prereg/NOGO seam/modeled/proxy/wrong venue).
- `run_liqmicro_v2` READY-pipeline canonical write surface (`_run_pipeline` writes to `RESEARCH_STATE`/`RESULTS_DIR`/`evaluation_summary_FCLR-LIQMICRO-002.md`) is only source-inventoried/blocked-proven; no sandboxed READY-branch contract test exercises `_run_pipeline` reachability with mocked heavy deps and temp write roots (cannot use real outcomes).
- `h004_fclr005_pipeline.py` allowed mode (`H004_ALLOW_FLAG`/env) has machine refusal/flag guards but no sandbox-root enforcement for pilot artifact constants/write targets; allowed mode could still target real `research_state/` paths if ever invoked with real data. Add smallest guard requiring explicit sandbox root (or test hook redirect) before allowed-mode writes, without running real census.

## VERIFICATION COMMANDS (RUN ON ENTRY)
- `python -m unittest discover tests` (>=484, green)
- `python scripts/tracka_resume_check.py` (>=17 checks, pass)
- `python scripts/tracka_resume_gate.py --prereg /nonexistent` (`drift_preflight.pass:true`, stable reason/order, `outcomes_inspected:false`)
- `python scripts/tracka_operator_report.py; echo $?` (`pass:true`, exit `0`)
- `python scripts/check_tracka_scope_registry_drift.py --json` (`pass:true`)

## STOP RULE
Complete ALL steps with concrete metrics. Track C locked. Track B unsupported. No conflation. No workflow/scheduler/poller/status-only/repeated wrappers/agent-controllers/new recurring families. Blocked/no-data claims without measurable hardening delta are noncompliant. Keep root md+json <=163 and probes==2. Leave state STRICTER than found.
