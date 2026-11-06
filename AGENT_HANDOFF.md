# AGENT_HANDOFF.md (SINGLE DURABLE HANDOFF) — READ THIS FILE FIRST
Timestamp (UTC): 20261106T105327Z
Handoff ID: FCLR-HANDOFF-20261106T105327Z
Baseline (prior session): FCLR-NEXT-125 COMPLETE (20261106T104530Z, 19 tests, 130 regression green: 120+121+122+123+124+125+fclr010_harness). IRONFLOW PROBING EXHAUSTED (90+, `data_through=2026-10`, 2026-11..2027-02 absent); probes==2; root md+json==143.
This session (20261106T105327Z): **ENTRY VERIFIED** — regression 130 OK (3.032s), resume 17 checks pass, gate BLOCKED fail-closed (`drift_preflight.pass:true`, `PREREG_OR_MANIFEST_BLOCK_AFTER_DRIFT_PASS`, `outcomes_inspected:false`), scope drift `pass:true` (83/83). NO TRIGGER; IRONFLOW PROBING EXHAUSTED — **NO re-probing absent months**. Bottleneck (absent post-2026-10 Track A data hard stop) remains removed only by redirecting to dep-light deterministic hardening (no network/parquet/outcome/real-research_state reads). **FCLR-NEXT-126 is the ONLY active objective** (measurable code+test, G1-G3 below). Working tree had untracked `tests/test_tracka_hardening_125.py` on entry (not committed; no-commit-unless-asked). No new timestamped probe/sweep/scan/wrapper/report families in research_state. No schedulers/pollers/status files/repeated wrappers/agent-controllers. NO `.github/workflows` changes.
Branch: main | Repo: Funding-conditioned-volatility-and-liquidation-risk
Priority: P0 — REPO-NAME PRIORITIZED (Track A liquidation risk) + HEAVY WORK MANDATORY | Mode: CAMPAIGN-DRIVEN | Enforcement: NO-SKIP/NO-COAST

## INITIAL TASK FOR NEXT AGENTIC SESSION (SINGLE, TIMESTAMPED, MANDATORY) — 20261106T105327Z
**Execute FCLR-NEXT-126.** ONLY active objective. **Heavy working required:** measurable **code+test** hardening when no trigger appears (G1-G3 below). Blocked/no-data claims without measurable hardening delta are noncompliant. No status-only loops. No re-probe absent months. No sealed Track C/B mutation.

TASK ID: FCLR-NEXT-126-GATE-REFUSAL-SHAPE + FCLR-010-EXECUTE-BLOCKED-RC + RUN_LIQMICRO-V1-READY-WRITE-SCOPE
PRIORITY: P0 — LIQUIDATION RISK (Track A) is the ONLY unfinished/active repo objective (Funding-conditioned VOLATILITY Track C sealed/locked; Track B NOT_SUPPORTED).
TIMESTAMP (UTC): 20261106T105327Z
ENFORCEMENT: ALL STEPS MANDATORY. NO STATUS-ONLY OUTPUT. NO NEW TIMESTAMPED PROBE/SWEEP/SCAN/WRAPPER/REPORT FAMILIES IN RESEARCH_STATE UNLESS STRICTLY ADMISSIBLE TRIGGER APPEARS (THEN: PREREG BEFORE INSPECTING OUTCOMES; blocker/prereg+result evidence only, ROOT BOUND PRESERVED). NO SCHEDULERS/POLLERS/STATUS FILES/REPEATED WRAPPERS/AGENT-CONTROLLERS. NO `.github/workflows` CHANGES. NO RE-IRONFLOW-PROBE OF ABSENT MONTHS. Hyperliquid-only for Track A observed-liquidation gate. NEVER conflate observed vs modeled liquidations. No threshold-shopping. Track C/B locked/unsupported.

### MANDATORY DELIVERABLES (G1-G3, ALL REQUIRED when no trigger)
1. **G1 (tracka_resume_gate refusal shape + fail-closed order):** `scripts.tracka_resume_gate.decide` and CLI `python scripts/tracka_resume_gate.py --prereg /nonexistent` return `status=BLOCKED`, `rc=1`, `reason_code=PREREG_OR_MANIFEST_BLOCK_AFTER_DRIFT_PASS`, `fail_closed_order=drift_preflight->manifest_prereg`, `outcomes_inspected:false`, `drift_preflight.pass:true` enforced first, `network=false`, `writes_real_research_state:false`, `gate_script=tracka_resume_gate`. Dep-light, tmp output dir, no real research_state writes. Add to `tests/test_tracka_hardening_126.py`.
2. **G2 (fclr010_execute blocked-entry rc + script field):** blocked `main` of `scripts/fclr010_execute.py` via `guarded_execute` mock returns `rc=1`, payload `status=BLOCKED`, `reason_code=PREREG_OR_MANIFEST_BLOCK_AFTER_DRIFT_PASS`, `script=fclr010_execute`, `canonical_outputs_mutated=false`, `network=false`, `writes_real_research_state:false`; full refusal fields present; no parquet/loader/canonical mutation. Dep-light, tmp-isolated. Add to `tests/test_tracka_hardening_126.py`.
3. **G3 (run_liqmicro v1 READY write-scope):** READY_FROZEN path (mocked `_run_pipeline` returning without canonical mutation) never writes `experiment_frontier.json`/`run_manifest.json`/Track A canonical outputs; writes confined to `results/liqmicro/` only; blocked path never invokes `_run_pipeline`. Source-order/guard assertion + tmp snapshot, no real research_state writes. Add to `tests/test_tracka_hardening_126.py`.

### CURRENT VERIFIED STATE (entry verify 20261106T105327Z)
- **Trigger:** NO TRIGGER. `ironflow_probe_20261105T200406Z.json` / `ironflow_probe_digest_latest.json` — `data_through=2026-10`; 2026-11..2027-02 absent. IRONFLOW PROBING EXHAUSTED (90+). **Do not re-probe.**
- **Resume:** `python scripts/tracka_resume_check.py` **17 checks PASS**, `pass:true`, `network:false`, `writes_real_research_state:false`.
- **Gate:** `python scripts/tracka_resume_gate.py --prereg /nonexistent` => `drift_preflight.pass:true`, `status=BLOCKED`, `reason_code=PREREG_OR_MANIFEST_BLOCK_AFTER_DRIFT_PASS`, `fail_closed_order=drift_preflight->manifest_prereg`, `outcomes_inspected:false`.
- **Scope drift:** `python scripts/check_tracka_scope_registry_drift.py --json` => `pass:true`, `scripts=83 registry=83 reason=OK`.
- **Regression (verified):** `python -m unittest tests.test_tracka_hardening_120 tests.test_tracka_hardening_121 tests.test_tracka_hardening_122 tests.test_tracka_hardening_123 tests.test_tracka_hardening_124 tests.test_tracka_hardening_125 tests.test_fclr010_harness` => **130 tests OK** (tmp-isolated, no network, no parquet/outcome reads, no real research_state writes).
- **Full-suite baseline (deps-present handoff):** 484 OK. **This environment:** numpy/pandas absent in legacy liqmicro/discovery paths; 120-125 deliverables dep-light.
- **Artifacts:** root `*.md+*.json` = **143** (<=163). `research_state` `ironflow_probe*` = **2** (1 live + 1 digest). Working tree on entry: untracked `tests/test_tracka_hardening_125.py` (not committed). No new timestamped probe/sweep/scan/wrapper/report families in research_state.

## FCLR-NEXT-125 DELIVERABLES (COMPLETE, EVIDENCED)
| Gap | Deliverable | Status | Evidence |
|---|---|---|---|
| G1 | `FCLR010Harness.evaluate_forward` / `execute_ready_data_load` READY_FROZEN acceptance on admissible GO manifest + present prereg + present `data_path`; no implicit parquet read (`outcome_loader=None` => `EXPLICIT_LOADER_REQUIRED_NO_IMPLICIT_PARQUET_READ`); explicit loader invoked exactly once; direct+execute parity; blocked prereg-missing / data-missing / admissible-NO-GO branches | COMPLETE | `tests/test_tracka_hardening_125.py::Test125G1GuardedSeamGoReadyAcceptance` (7) |
| G2 | blocked-main refusal payload shape stability for `coupled_build_panel`, `fclr010_execute`, `fclr010_execute_fast`, `run_liqmicro_v2`, `coupled_robust_eval`, `liqmicro_audit`, `fclr010_coverage_audit`, `overlay_quick`, `overlay_tracka_execute`: required refusal fields, stable `reason_code=PREREG_OR_MANIFEST_BLOCK_AFTER_DRIFT_AFTER_DRIFT_PASS`, correct `script`, `canonical_outputs_mutated=false`, `network=false`, `writes_real_research_state=false` across missing-prereg / nogo-seam / modeled-proxy / wrong-venue states | COMPLETE | `tests/test_tracka_hardening_125.py::Test125G2AuditRefusalPayloadShapeStability` (5) |
| G3 | blocked `scripts/run_liqmicro.py` `main` never invokes `_run_pipeline`, never mutates `experiment_frontier.json`/`run_manifest.json`/canonical outputs; READY_FROZEN `_run_pipeline` is sole writer (source-order/guard: guarded call + refusal gate precede `_run_pipeline` call; frontier writer inside `_run_pipeline` body) | COMPLETE | `tests/test_tracka_hardening_125.py::Test125G3RunLiqmicroV1FrontierWriteParity` (2) |
| G4 | root `*.md+*.json` <=163 (143); `ironflow_probe*` == 2 (1 live + 1 digest); no new recurring `campaign_sweep_tracka_*`/`liquidation_forward_validate_*` families beyond archived 20261105 policy; canonical alt outputs `alt_source_scan_latest.json` + `alt_source_deep_review_latest.md` present; read-only, no writes | COMPLETE | `tests/test_tracka_hardening_125.py::Test125G4CanonicalAltOutputsRootBoundRegression` (4) |
| G5 | refusal fail-closed matrix 6x4: `coupled_robust_eval`, `fclr010_execute`, `fclr010_coverage_audit`, `liqmicro_audit`, `overlay_quick`, `overlay_tracka_execute` each `rc=1` with `canonical_outputs_mutated=false` on all four non-READY states via `guarded_execute` mocks; canonical targets snapshot-unchanged | COMPLETE | `tests/test_tracka_hardening_125.py::Test125G5RefusalFailClosedMatrix6x4` (1) |

## 126 EXECUTION PROTOCOL (HEAVY, MANDATORY)
1. **Entry verify:** run 120-125+harness, `tracka_resume_check.py`, `tracka_resume_gate.py --prereg /nonexistent`, `check_tracka_scope_registry_drift.py --json`; confirm NO TRIGGER/probes==2/root<=163. Record counts honestly.
2. **Implement G1-G3** as measurable dep-light/tmp-isolated code+tests in `tests/test_tracka_hardening_126.py`. No existing guards weakened; additive hardening only. No canonical mutation on blocked paths.
3. **Run tests:** `python -m unittest tests.test_tracka_hardening_126` + regression `120-126+test_fclr010_harness`. Note env constraints honestly (numpy/pandas absent).
4. **Exit verify:** resume/gate/drift pass; probes==2; root `*.md+*.json`<=163; no new recurring families.
5. **Update this handoff** to next timestamp with 126 evidence table, regression count, and `FCLR-NEXT-127` uncovered gaps (code+test only). Root bound kept.

## BOTTLENECKS REMOVED / STILL HARD
- **Removed:** absent-month probe churn (exhausted, enforced), status-only/no-delta loops (forbidden), unguarded canonical writes (120-125 guards), missing refusal/shape/write-parity coverage (124/125 targets).
- **Hard (do not fight with busywork):** post-2026-10 admissible Hyperliquid Track A liquidation data absent (`data_through=2026-10`). Only a **strictly admissible trigger** (real, documented, Hyperliquid observed, Hyperliquid-only) permits prereg->inspect path — and even then prereg BEFORE inspecting outcomes, root bound preserved.

## VERIFICATION COMMANDS (RUN ON ENTRY/NEXT)
- `python -m unittest tests.test_tracka_hardening_120 tests.test_tracka_hardening_121 tests.test_tracka_hardening_122 tests.test_tracka_hardening_123 tests.test_tracka_hardening_124 tests.test_tracka_hardening_125 tests.test_fclr010_harness` (regression 130 OK, minimal env)
- `python scripts/tracka_resume_check.py` (17 checks, pass)
- `python scripts/tracka_resume_gate.py --prereg /nonexistent` (`drift_preflight.pass:true`, stable reason/order, `outcomes_inspected:false`)
- `python scripts/check_tracka_scope_registry_drift.py --json` (`pass:true`)
- `python -m unittest discover tests` (>=484 green in deps-present env; numpy/pandas import errors in legacy liqmicro tests are env constraints, not 120-125 regressions)

## STOP RULE
Complete ALL steps with concrete metrics. Track C locked. Track B unsupported. No conflation. No workflow/scheduler/poller/status-only/repeated wrappers/agent-controllers/new recurring families. Blocked/no-data claims without measurable hardening delta are noncompliant. Keep root md+json <=163 and probes==2. Leave state STRICTER than found.
