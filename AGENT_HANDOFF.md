# AGENT_HANDOFF.md (SINGLE DURABLE HANDOFF) — READ THIS FILE FIRST
Timestamp (UTC): 20261106T090232Z
Handoff ID: FCLR-HANDOFF-20261106T090232Z
Baseline (prior session): FCLR-NEXT-122 COMPLETE (20261106T085555Z, 21 tests, 66 regression green). IRONFLOW PROBING EXHAUSTED (90+, `data_through=2026-10`, 2026-11..2027-02 absent); probes==2; root md+json==2.
This session (20261106T090232Z): entry verify re-confirmed; **NO TRIGGER**; IRONFLOW PROBING EXHAUSTED — **NO re-probing absent months**. Bottleneck absent post-2026-10 Track A data hard stop remains removed by redirecting to dep-light deterministic hardening (no network/parquet/outcome/real-research_state reads). **FCLR-NEXT-123 G1-G5 COMPLETE** (measurable code+test): `tests/test_tracka_hardening_123.py` **18 tests OK** (tmp-isolated). Regression: `test_tracka_hardening_120 + test_tracka_hardening_121 + test_tracka_hardening_122 + test_fclr010_harness` = **66 tests OK**. Entry/exit verify: `tracka_resume_check.py` **17 checks PASS**, `pass:true`, `network:false`, `writes_real_research_state:false`; `tracka_resume_gate.py --prereg /nonexistent` => `drift_preflight.pass:true`, `status=BLOCKED`, `reason_code=PREREG_OR_MANIFEST_BLOCK_AFTER_DRIFT_PASS`, `fail_closed_order=drift_preflight->manifest_prereg`, `outcomes_inspected:false`; `check_tracka_scope_registry_drift.py --json` => `pass:true scripts=83 registry=83 reason=OK`. No new timestamped probe/sweep/scan/wrapper/report families in research_state. No schedulers/pollers/status files/repeated wrappers/agent-controllers. NO `.github/workflows` changes.
Branch: main | Repo: Funding-conditioned-volatility-and-liquidation-risk
Priority: P0 — REPO-NAME PRIORITIZED (Track A liquidation risk) + HEAVY WORK MANDATORY | Mode: CAMPAIGN-DRIVEN | Enforcement: NO-SKIP/NO-COAST

## INITIAL TASK FOR NEXT AGENTIC SESSION (SINGLE, TIMESTAMPED, MANDATORY) — 20261106T090232Z
**Execute FCLR-NEXT-124.** ONLY active objective. **Heavy working required:** measurable **code+test** hardening when no trigger appears (G1-G5 below). Blocked/no-data claims without measurable hardening delta are noncompliant. No status-only loops. No re-probe absent months. No sealed Track C/B mutation.

TASK ID: FCLR-NEXT-124-COUPLED-BUILD-PANEL-READY-PATH-WRITE-SCOPE-GUARD-FOR-CACHE/PARQUET-ARTIFACTS + EVALUATE_FORWARD-MANIFEST-ONLY-SEAM-GO-WITH-DATA-MISSING-STABLE-REASON/PAYLOAD-PARITY + H004-CENSUS-INPUT-PATH-TRAVERSAL/SYMLINK-ESCAPE-FAILCLOSED-MATRIX + GUARDED-SOURCE-CONTRACT-AUDIT-ENSURE-COUPLED-BUILD-PANEL-EMITS-FULL-REFUSAL-FIELDS-RUNTIME (NO REAL WRITES) + REGRESSION-MATRIX-COVERAGE-FOR-122/123-WRITE-GUARD-ARGS-DIVERGENCE-ACROSS-MONKEYPATCHED-CONSTANTS (READINESS-PRESERVED)
PRIORITY: P0 — LIQUIDATION RISK (Track A) is the ONLY unfinished/active repo objective (Funding-conditioned VOLATILITY Track C sealed/locked).
TIMESTAMP (UTC): 20261106T090232Z
ENFORCEMENT: ALL STEPS MANDATORY. NO STATUS-ONLY OUTPUT. NO NEW TIMESTAMPED PROBE/SWEEP/SCAN/WRAPPER/REPORT FAMILIES IN RESEARCH_STATE UNLESS STRICTLY ADMISSIBLE TRIGGER APPEARS (THEN: PREREG BEFORE INSPECTING OUTCOMES; blocker/prereg+result evidence only, ROOT BOUND PRESERVED). NO SCHEDULERS/POLLERS/STATUS FILES/REPEATED WRAPPERS/AGENT-CONTROLLERS. NO `.github/workflows` CHANGES. NO RE-IRONFLOW-PROBE OF ABSENT MONTHS. Hyperliquid-only for Track A observed-liquidation gate. NEVER conflate observed vs modeled liquidations. No threshold-shopping. Track C/B locked/unsupported.

### MANDATORY DELIVERABLES (G1-G5, ALL REQUIRED when no trigger)
1. **G1 (coupled_build_panel READY-path/cache write-scope guard):** Add a machine-enforced write-scope allowlist for `coupled_build_panel` canonical cache/parquet artifacts (`RESEARCH_STATE/.cache/fclr_coupled_panel.parquet` scope only, no dir-wide research_state/repo-root/wildcards, no Hyperliquid canonical output mutation). Fail closed before any cache write on READY path violations; blocked NO-READY path must not invoke cache writes. Add tmp-sandboxed tests (no real research_state writes).
2. **G2 (evaluate_forward manifest-only seam-GO with data missing parity):** Seam-GO + prereg present but `data_path` missing must return stable BLOCKED payload parity (no outcomes inspected, no loader, stable reason/fields) consistent with guarded surfaces; matrix test direct `evaluate_forward` + `execute_ready_data_load`/`guarded_execute`. No data/parquet read.
3. **G3 (h004 census/input path traversal/symlink-escape fail-closed):** In allowed sandbox mode, required census/input resolution must reject path traversal (`..`) and symlink targets escaping sandbox/root policy before heavy work; stable `reason_code`/payload. Tmp-isolated, no real research_state writes, no network.
4. **G4 (coupled_build_panel refusal payload runtime emission audit):** Prove runtime blocked NO-READY refusal emits full required fields (`status,outcomes_inspected,canonical_outputs_mutated,network,writes_real_research_state,script,reason_code`) via dep-light mock path where safe; fix emission only if absent. No parquet/loader/canonical mutation.
5. **G5 (123/122 write-guard divergence regression matrix preserved):** Add/strengthen regression cases proving liqmicro_v2 write-guard catches constant/arg divergence, repo-root/RS-dir-wide/wildcard, and denied-target contamination while policy roots remain pass; ensure no bypass via `results_dir`/`research_state` args alone. Deterministic, no writes.

### CURRENT VERIFIED STATE (exit verify this session, 20261106T090232Z)
- **Trigger:** NO TRIGGER. `ironflow_probe_20261105T200406Z.json` / `ironflow_probe_digest_latest.json` — `data_through=2026-10`; 2026-11..2027-02 absent. IRONFLOW PROBING EXHAUSTED (90+). **Do not re-probe.**
- **Resume:** `python scripts/tracka_resume_check.py` **17 checks PASS**, `pass:true`, `network:false`, `writes_real_research_state:false`.
- **Gate:** `python scripts/tracka_resume_gate.py --prereg /nonexistent` => `drift_preflight.pass:true`, `status=BLOCKED`, `reason_code=PREREG_OR_MANIFEST_BLOCK_AFTER_DRIFT_PASS`, `fail_closed_order=drift_preflight->manifest_prereg`, `outcomes_inspected:false`.
- **Scope drift:** `python scripts/check_tracka_scope_registry_drift.py --json` => `pass:true`, `scripts=83 registry=83 reason=OK`.
- **123 tests (this session, deterministic/minimal env):** `python -m unittest tests.test_tracka_hardening_123` => **18 tests OK**. `test_tracka_hardening_120 + 121 + 122 + test_fclr010_harness` => **66 tests OK** (tmp-isolated, no network, no parquet/outcome reads, no real research_state writes).
- **Full-suite baseline (prior deps-present handoff):** 484 OK. **This environment:** numpy/pandas absent in legacy liqmicro/discovery paths; 120/121/122/123/harness deliverables dep-light verified here.
- **Artifacts:** root `*.md+*.json` = **2** (<=163). `research_state` probes = **2**. Working tree: `scripts/fclr010_harness.py`, `scripts/run_liqmicro_v2.py`, `scripts/h004_fclr005_pipeline.py`, `scripts/coupled_robust_eval.py`, `scripts/coupled_build_panel.py`, `tests/test_tracka_hardening_123.py` modified/added (uncommitted); `AGENT_HANDOFF.md` updated.

## FCLR-NEXT-123 DELIVERABLES (COMPLETE, NO TRIGGER)
| Gap | Deliverable | Status | Evidence |
|---|---|---|---|
| G1 | `FCLR010Harness.evaluate_forward` direct seam-GO + prereg missing/nonexistent => stable `reason_code=PREREG_OR_MANIFEST_BLOCK_AFTER_DRIFT_PASS`, `seam_go_prereg_required=true`, `reason_code_detail=ADMISSIBLE_SEAM_GO_PREREG_REQUIRED`, `status=BLOCKED`, `prereg_required:true`, `outcomes_inspected:false`; no loader invoked | COMPLETE | `scripts/fclr010_harness.py`, `tests/test_tracka_hardening_123.py::Test123G1EvaluateForwardSeamGoPreregParity` (3) |
| G2 | `_guard_liqmicro_v2_write_targets` validates effective allowed roots (arg or monkeypatched constant), fails closed on policy divergence / repo escape / RS dir-wide / repo root / wildcard / arbitrary repo dirs / denied targets; `results_dir/research_state` args cannot bypass; blocked main never invokes guard/pipeline | COMPLETE | `scripts/run_liqmicro_v2.py`, `tests/test_tracka_hardening_123.py::Test123G2LiqmicroV2WriteGuardArgsBound` (5); 121/122 liqmicro write-guard tests remain green |
| G3 | h004 sandbox guard fail-closed on missing sandbox root, **file-not-dir** root, nonexistent/unusable root before census/heavy work; stable reason codes `H004_ALLOWED_MODE_REQUIRES_SANDBOX_ROOT`, `H004_SANDBOX_ROOT_NOT_DIRECTORY`, `H004_SANDBOX_ROOT_UNUSABLE`; census absent detail stable; `main` refuses file sandbox before heavy work; no real RS writes | COMPLETE | `scripts/h004_fclr005_pipeline.py`, `tests/test_tracka_hardening_123.py::Test123G3H004SandboxRootNondirUnusable` (5) |
| G4 | Guarded ready-writing refusal payload field audit for execute/execute_fast/run_liqmicro_v2 runtime and coupled_build_panel runtime/source emission (`network`,`writes_real_research_state`,`canonical_outputs_mutated` set where needed); JSON-extract tolerant to leading banners; no loader/canonical mutation | COMPLETE | `scripts/coupled_build_panel.py`, `scripts/coupled_robust_eval.py` (typing import), `tests/test_tracka_hardening_123.py::Test123G4GuardedRefusalPayloadNetworkWrsAudit` (2) |
| G5 | `coupled_robust_eval` guarded-class source contract + runtime blocked-path refusal with heavy mocks; required refusal fields emitted; no canonical mutation; registry drift passes | COMPLETE | `scripts/coupled_robust_eval.py`, `tests/test_tracka_hardening_123.py::Test123G5CoupledRobustEvalGuardedBlockedPath` (3) |

## 124 UNCOVERED GAPS (exact, code+tests required)
- **G1**: `coupled_build_panel` READY-path/cache write-scope allowlist + blocked-path nonwrite proof (specific cache artifact root only; tmp sandbox).
- **G2**: `evaluate_forward` seam-GO + prereg present + `data_path` missing stable BLOCKED parity across direct/execute/guarded surfaces (no loader/outcome read).
- **G3**: h004 allowed-sandbox census/input path traversal (`..`) and symlink-escape fail-closed matrix before heavy work.
- **G4**: `coupled_build_panel` runtime blocked NO-READY refusal full-field emission (dep-light) with no parquet/loader/canonical mutation.
- **G5**: liqmicro_v2 write-guard divergence regression matrix preserved/extended (constant+arg+`results_dir/research_state` arg bypass attempts).

## VERIFICATION COMMANDS (RUN ON ENTRY)
- `python -m unittest tests.test_tracka_hardening_120 tests.test_tracka_hardening_121 tests.test_tracka_hardening_122 tests.test_tracka_hardening_123 tests.test_fclr010_harness` (must be green in minimal env)
- `python scripts/tracka_resume_check.py` (17 checks, pass)
- `python scripts/tracka_resume_gate.py --prereg /nonexistent` (`drift_preflight.pass:true`, stable reason/order, `outcomes_inspected:false`)
- `python scripts/check_tracka_scope_registry_drift.py --json` (`pass:true`)
- `python -m unittest discover tests` (>=484 green in deps-present env; numpy/pandas import errors in legacy liqmicro tests are env constraints, not 120–123 regressions)

## STOP RULE
Complete ALL steps with concrete metrics. Track C locked. Track B unsupported. No conflation. No workflow/scheduler/poller/status-only/repeated wrappers/agent-controllers/new recurring families. Blocked/no-data claims without measurable hardening delta are noncompliant. Keep root md+json <=163 and probes==2. Leave state STRICTER than found.
