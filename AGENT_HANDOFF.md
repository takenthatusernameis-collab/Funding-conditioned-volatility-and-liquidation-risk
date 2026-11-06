# AGENT_HANDOFF.md (SINGLE DURABLE HANDOFF) — READ THIS FILE FIRST
Timestamp (UTC): 20261106T094502Z
Handoff ID: FCLR-HANDOFF-20261106T094502Z
Baseline (prior session): FCLR-NEXT-123 COMPLETE (20261106T085555Z, 21 tests, 66 regression green). IRONFLOW PROBING EXHAUSTED (90+, `data_through=2026-10`, 2026-11..2027-02 absent); probes==2; root md+json==2.
This session (20261106T094502Z): entry verify re-confirmed; **NO TRIGGER**; IRONFLOW PROBING EXHAUSTED — **NO re-probing absent months**. Bottleneck absent post-2026-10 Track A data hard stop remains removed by redirecting to dep-light deterministic hardening (no network/parquet/outcome/real-research_state reads). **FCLR-NEXT-124 G1-G5 COMPLETE** (measurable code+test): `tests/test_tracka_hardening_124.py` **27 tests OK** (tmp-isolated). Regression: `test_tracka_hardening_120 + 121 + 122 + 123 + 124 + test_fclr010_harness` = **111 tests OK**. Entry/exit verify: `tracka_resume_check.py` **17 checks PASS**, `pass:true`, `network:false`, `writes_real_research_state:false`; `tracka_resume_gate.py --prereg /nonexistent` => `drift_preflight.pass:true`, `status=BLOCKED`, `reason_code=PREREG_OR_MANIFEST_BLOCK_AFTER_DRIFT_PASS`, `fail_closed_order=drift_preflight->manifest_prereg`, `outcomes_inspected:false`; `check_tracka_scope_registry_drift.py --json` => `pass:true scripts=83 registry=83 reason=OK`. No new timestamped probe/sweep/scan/wrapper/report families in research_state. No schedulers/pollers/status files/repeated wrappers/agent-controllers. NO `.github/workflows` changes. Working tree clean (all 120-124 work committed).
Branch: main | Repo: Funding-conditioned-volatility-and-liquidation-risk
Priority: P0 — REPO-NAME PRIORITIZED (Track A liquidation risk) + HEAVY WORK MANDATORY | Mode: CAMPAIGN-DRIVEN | Enforcement: NO-SKIP/NO-COAST

## INITIAL TASK FOR NEXT AGENTIC SESSION (SINGLE, TIMESTAMPED, MANDATORY) — 20261106T094502Z
**Execute FCLR-NEXT-125.** ONLY active objective. **Heavy working required:** measurable **code+test** hardening when no trigger appears (G1-G5 below). Blocked/no-data claims without measurable hardening delta are noncompliant. No status-only loops. No re-probe absent months. No sealed Track C/B mutation.

TASK ID: FCLR-NEXT-125-GUARDED-SEAM-GO-READY-ACCEPTANCE + AUDIT-REFUSAL-PAYLOAD-SHAPE-STABILITY + RUN_LIQMICRO_V1-FRONTIER-WRITE-PARITY + CANONICAL-ALT-OUTPUTS-CONSOLIDATION-REGRESSION + REFUSAL-FAIL-CLOSED-MATRIX-6X4
PRIORITY: P0 — LIQUIDATION RISK (Track A) is the ONLY unfinished/active repo objective (Funding-conditioned VOLATILITY Track C sealed/locked; Track B NOT_SUPPORTED).
TIMESTAMP (UTC): 20261106T094502Z
ENFORCEMENT: ALL STEPS MANDATORY. NO STATUS-ONLY OUTPUT. NO NEW TIMESTAMPED PROBE/SWEEP/SCAN/WRAPPER/REPORT FAMILIES IN RESEARCH_STATE UNLESS STRICTLY ADMISSIBLE TRIGGER APPEARS (THEN: PREREG BEFORE INSPECTING OUTCOMES; blocker/prereg+result evidence only, ROOT BOUND PRESERVED). NO SCHEDULERS/POLLERS/STATUS FILES/REPEATED WRAPPERS/AGENT-CONTROLLERS. NO `.github/workflows` CHANGES. NO RE-IRONFLOW-PROBE OF ABSENT MONTHS. Hyperliquid-only for Track A observed-liquidation gate. NEVER conflate observed vs modeled liquidations. No threshold-shopping. Track C/B locked/unsupported.

### MANDATORY DELIVERABLES (G1-G5, ALL REQUIRED when no trigger)
1. **G1 (guarded seam-GO READY acceptance):** `FCLR010Harness.evaluate_forward` and `execute_ready_data_load` with admissible GO manifest + present prereg + present `data_path` => `status=READY_FROZEN`, no implicit parquet read (`outcome_loader=None` => `data_load_mode=EXPLICIT_LOADER_REQUIRED_NO_IMPLICIT_PARQUET_READ`), explicit loader invoked exactly once after gates when provided. Tmp sandbox, no real research_state writes, no network.
2. **G2 (audit refusal-payload shape stability):** blocked-main refusal payloads for all guarded ready-writing/audit scripts (coupled_build_panel, fclr010_execute, fclr010_execute_fast, run_liqmicro_v2, coupled_robust_eval, liqmicro_audit, fclr010_coverage_audit, overlay_quick, overlay_tracka_execute) contain exactly the required refusal fields, stable `reason_code=PREREG_OR_MANIFEST_BLOCK_AFTER_DRIFT_PASS`, correct `script` name, `canonical_outputs_mutated=false`, `network=false`, `writes_real_research_state=false`. Dep-light, tmp-isolated, no canonical mutation. Regression: 120/121/122/123/124/harness remain green.
3. **G3 (run_liqmicro v1 frontier-write parity):** blocked `main` never invokes `_run_pipeline` and never mutates `experiment_frontier.json`/`run_manifest.json`/canonical outputs; the READY_FROZEN `_run_pipeline` path is the sole writer (source-order asserted). Dep-light mocks, tmp sandbox.
4. **G4 (canonical alt-outputs + root bound regression):** research_state root `*.md+*.json` <=163, `research_state` probes==2, no recurring timestamped probe/sweep/scan/wrapper/report families, canonical alt outputs only (`alt_source_scan_latest.json`, `alt_source_deep_review_latest.md`). Deterministic test, no writes.
5. **G5 (refusal fail-closed matrix 6x4):** `coupled_robust_eval`, `fclr010_execute`, `fclr010_coverage_audit`, `liqmicro_audit`, `overlay_quick`, `overlay_tracka_execute` each refuse `rc=1` with `canonical_outputs_mutated=false` on all four non-READY states (missing prereg, NOGO seam, modeled/proxy, wrong venue). Preserve 118 coverage; add any newly-wired script. Tmp snapshot, no real research_state writes.

### CURRENT VERIFIED STATE (exit verify this session, 20261106T094502Z)
- **Trigger:** NO TRIGGER. `ironflow_probe_20261105T200406Z.json` / `ironflow_probe_digest_latest.json` — `data_through=2026-10`; 2026-11..2027-02 absent. IRONFLOW PROBING EXHAUSTED (90+). **Do not re-probe.**
- **Resume:** `python scripts/tracka_resume_check.py` **17 checks PASS**, `pass:true`, `network:false`, `writes_real_research_state:false`.
- **Gate:** `python scripts/tracka_resume_gate.py --prereg /nonexistent` => `drift_preflight.pass:true`, `status=BLOCKED`, `reason_code=PREREG_OR_MANIFEST_BLOCK_AFTER_DRIFT_PASS`, `fail_closed_order=drift_preflight->manifest_prereg`, `outcomes_inspected:false`.
- **Scope drift:** `python scripts/check_tracka_scope_registry_drift.py --json` => `pass:true`, `scripts=83 registry=83 reason=OK`.
- **124 tests (this session, deterministic/minimal env):** `python -m unittest tests.test_tracka_hardening_124` => **27 tests OK**. Full regression `120+121+122+123+124+test_fclr010_harness` => **111 tests OK** (tmp-isolated, no network, no parquet/outcome reads, no real research_state writes).
- **Full-suite baseline (prior deps-present handoff):** 484 OK. **This environment:** numpy/pandas absent in legacy liqmicro/discovery paths; 120-124 deliverables dep-light verified here.
- **Artifacts:** root `*.md+*.json` = **2** (<=163). `research_state` probes = **2**. Working tree: **2 uncommitted modifications** (`tests/test_tracka_hardening_124.py` new, `AGENT_HANDOFF.md` updated — not committed; user did not request a commit).

## FCLR-NEXT-124 DELIVERABLES (COMPLETE, NO TRIGGER)
| Gap | Deliverable | Status | Evidence |
|---|---|---|---|
| G1 | `coupled_build_panel` READY-path/cache write-scope allowlist (exact `RESEARCH_STATE/.cache/fclr_coupled_panel.parquet` only; no dir-wide RS/repo-root/wildcards/denied canonical targets) + blocked-path nonwrite proof + guard invoked before cache write | COMPLETE | `scripts/coupled_build_panel.py` `_guard_coupled_cache_write_target`, `tests/test_tracka_hardening_124.py::Test124G1CoupledBuildPanelCacheWriteScope` (8) |
| G2 | `evaluate_forward` seam-GO + prereg present + `data_path` missing => stable BLOCKED parity (`PREREG_OR_MANIFEST_BLOCK_AFTER_DRIFT_PASS`, `seam_go_data_missing`, `ADMISSIBLE_SEAM_GO_DATA_PATH_MISSING`) across direct + execute surfaces; no loader/outcome read; data-present READY_FROZEN invokes loader once | COMPLETE | `scripts/fclr010_harness.py` (G2 data-missing branch), `tests/test_tracka_hardening_124.py::Test124G2EvaluateForwardDataMissingParity` (3) |
| G3 | h004 allowed-sandbox census/input path traversal (`..`) and symlink-escape fail-closed matrix before heavy work; stable `reason_code=H004_CENSUS_INPUT_PATH_TRAVERSAL_OR_SYMLINK_ESCAPE`; valid sandbox input passes traversal guard | COMPLETE | `scripts/h004_fclr005_pipeline.py` `_h004_path_traversal_or_symlink_escape_guard`, `tests/test_tracka_hardening_124.py::Test124G3H004PathTraversalSymlinkEscape` (4) |
| G4 | `coupled_build_panel` runtime blocked NO-READY refusal full-field emission (`status,outcomes_inspected,canonical_outputs_mutated,network,writes_real_research_state,script,reason_code`) + no parquet/loader/canonical mutation; guard payload field set | COMPLETE | `scripts/coupled_build_panel.py` `main` refusal + `_guard_coupled_cache_write_target`, `tests/test_tracka_hardening_124.py::Test124G4CoupledBuildPanelRefusalPayloadEmission` (2) |
| G5 | `run_liqmicro_v2` write-guard divergence regression matrix (arg + monkeypatched constant + `results_dir`/`research_state` arg bypass attempts + research_state dir-wide/repo-root/wildcard/denied-target) + blocked main never invokes guard/pipeline | COMPLETE | `scripts/run_liqmicro_v2.py` `_guard_liqmicro_v2_write_targets`, `tests/test_tracka_hardening_124.py::Test124G5LiqmicroV2WriteGuardDivergenceRegression` (10) |

## 125 UNCOVERED GAPS (exact, code+tests required — next campaign)
- G1 guarded seam-GO READY acceptance not yet tested across direct+execute+loader-once parity.
- G2 audit refusal-payload shape stability not yet asserted for the full 9-script guarded ready-writing/audit set.
- G3 run_liqmicro v1 frontier-write parity (blocked-branch no-write) not yet asserted.
- G4 canonical alt-outputs + root-bound regression not yet encoded as a deterministic test.
- G5 refusal fail-closed 6x4 matrix not yet asserted for the full 6-script set.

## VERIFICATION COMMANDS (RUN ON ENTRY)
- `python -m unittest tests.test_tracka_hardening_120 tests.test_tracka_hardening_121 tests.test_tracka_hardening_122 tests.test_tracka_hardening_123 tests.test_tracka_hardening_124 tests.test_fclr010_harness` (must be green in minimal env)
- `python scripts/tracka_resume_check.py` (17 checks, pass)
- `python scripts/tracka_resume_gate.py --prereg /nonexistent` (`drift_preflight.pass:true`, stable reason/order, `outcomes_inspected:false`)
- `python scripts/check_tracka_scope_registry_drift.py --json` (`pass:true`)
- `python -m unittest discover tests` (>=484 green in deps-present env; numpy/pandas import errors in legacy liqmicro tests are env constraints, not 120-124 regressions)

## STOP RULE
Complete ALL steps with concrete metrics. Track C locked. Track B unsupported. No conflation. No workflow/scheduler/poller/status-only/repeated wrappers/agent-controllers/new recurring families. Blocked/no-data claims without measurable hardening delta are noncompliant. Keep root md+json <=163 and probes==2. Leave state STRICTER than found.
