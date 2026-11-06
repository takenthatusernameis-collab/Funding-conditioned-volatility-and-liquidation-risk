# AGENT_HANDOFF.md (SINGLE DURABLE HANDOFF) — READ THIS FILE FIRST
Timestamp (UTC): 20261106T114421Z
Handoff ID: FCLR-HANDOFF-20261106T114421Z
Baseline (prior session): FCLR-NEXT-127 COMPLETE (20261106T113316Z, G1-G3 evidenced in tests/test_tracka_hardening_127.py: seam detail parity + CLI, guarded_entry refusal reason/detail parity, READY writer scope + blocked no-loader; regression 154 OK: 120-127 + fclr010_harness). This session (20261106T114421Z): **ENTRY VERIFIED** — regression 161 OK pre/post-change (120-128 + harness), resume 17 checks pass (`pass:true`, `network:false`, `writes_real_research_state:false`), gate BLOCKED fail-closed (`drift_preflight.pass:true`, `PREREG_OR_MANIFEST_BLOCK_AFTER_DRIFT_PASS`, `outcomes_inspected:false`), scope drift `pass:true` (83/83). **NO TRIGGER; IRONFLOW PROBING EXHAUSTED — NO re-probing absent months.** FCLR-NEXT-128 delivered (G1-G3) as measurable dep-light/tmp-isolated code+tests (`tests/test_tracka_hardening_128.py`, 7 tests). Working tree clean (128 test committed-ready; no-commit-unless-asked applies). No new timestamped probe/sweep/scan/wrapper/report families in research_state. No schedulers/pollers/status files/repeated wrappers/agent-controllers. NO `.github/workflows` changes. Track C sealed/locked; Track B NOT_SUPPORTED.
Branch: main | Repo: Funding-conditioned-volatility-and-liquidation-risk
Priority: P0 — REPO-NAME PRIORITIZED (Track A liquidation risk is the ONLY active objective; Track C volatility sealed/locked; Track B NOT_SUPPORTED) | Mode: CAMPAIGN-DRIVEN | Enforcement: NO-SKIP/NO-COAST

## INITIAL TASK FOR NEXT AGENTIC SESSION (SINGLE, TIMESTAMPED, MANDATORY) — 20261106T114421Z
**Execute FCLR-NEXT-129.** ONLY active objective. **Heavy working required:** measurable code+test hardening when no trigger appears (G1-G3 below). Blocked/no-data claims without measurable hardening delta are noncompliant. No status-only loops. No re-probe absent months. No sealed Track C/B mutation.

TASK ID: FCLR-NEXT-129-FUSED-REFUSAL-MATRIX + OPERATOR-CLI-PARITY + REGISTRY-DRIFT-FAILS-CLOSED
PRIORITY: P0 — LIQUIDATION RISK (Track A) is the ONLY unfinished/active repo objective (Funding-conditioned VOLATILITY Track C sealed/locked; Track B NOT_SUPPORTED).
TIMESTAMP (UTC): 20261106T114421Z
ENFORCEMENT: ALL STEPS MANDATORY. NO STATUS-ONLY OUTPUT. NO NEW TIMESTAMPED PROBE/SWEEP/SCAN/WRAPPER/REPORT FAMILIES IN RESEARCH_STATE UNLESS STRICTLY ADMISSIBLE TRIGGER APPEARS (THEN: PREREG BEFORE INSPECTING OUTCOMES; blocker/prereg+result evidence only, ROOT BOUND PRESERVED). NO SCHEDULERS/POLLERS/STATUS FILES/REPEATED WRAPPERS/AGENT-CONTROLLERS. NO `.github/workflows` CHANGES. NO RE-IRONFLOW-PROBE OF ABSENT MONTHS. Hyperliquid-only for Track A observed-liquidation gate. NEVER conflate observed vs modeled liquidations. No threshold-shopping. Track C/B locked/unsupported.

### MANDATORY DELIVERABLES (G1-G3, ALL REQUIRED when no trigger)
1. **G1 (fused Track A blocked-branch refusal matrix):** dep-light tmp-isolated tests in `tests/test_tracka_hardening_129.py` asserting, for EVERY guarded Track A entrypoint (coupled_build_panel, fclr010_execute_fast, run_liqmicro, run_liqmicro_v2, fclr010_coverage_audit, liqmicro_audit, plus regression anchors fclr010_execute, coupled_robust_eval, overlay_quick, overlay_tracka_execute): mocked `guarded_execute` returns BLOCKED => `main()` rc=1, refusal payload `reason_code=PREREG_OR_MANIFEST_BLOCK_AFTER_DRIFT_PASS`, `canonical_outputs_mutated=false`, `outcomes_inspected=false`, `network=false`, `writes_real_research_state=false`, outcome loader never invoked, canonical snapshots (`research_state/experiment_frontier.json`, `research_state/run_manifest.json`, `research_state/evaluation_summary_FCLR010.md`, per-script summaries) unchanged. No script may be absent from the matrix.
2. **G2 (operator CLI parity):** `scripts.tracka_operator_report.main(argv)` exit 0 on pass / exit 1 on BLOCKED, stable JSON payload, drift-preflight-first fail-closed order, `--admissible-manifest` GO/NO-GO passthrough into `admissible_seam_wired` (pass/status/reason_code/failures/month/fail_closed/network/reads_outcomes/reads_parquet); dep-light test in `tests/test_tracka_hardening_129.py`.
3. **G3 (registry drift fails closed):** `scripts/check_tracka_scope_registry_drift.py --json` fails (`pass:false`) on scripts/*.py vs `research_state/tracka_script_scope_registry.json` drift: added/unregistered script, malformed entry (class/reason), or eval-summary writer left `unclassified_auxiliary`; asserted via tmp-isolated shadowing (no real research_state writes, no network), dep-light test in `tests/test_tracka_hardening_129.py`.

### CURRENT VERIFIED STATE (exit verify 20261106T114421Z)
- **Trigger:** NO TRIGGER. `ironflow_probe_20261105T200406Z.json` / `ironflow_probe_digest_latest.json` — `data_through=2026-10`; 2026-11..2027-02 absent. IRONFLOW PROBING EXHAUSTED (90+). **Do not re-probe.**
- **Resume:** `python scripts/tracka_resume_check.py` **17 checks PASS**, `pass:true`, `network:false`, `writes_real_research_state:false`. `--admissible-manifest` CLI: missing candidate => rc=1 NO-GO `ADMISSIBLE_CANDIDATE_PATH_MISSING`; valid GO manifest => rc=0 `ADMISSIBLE_SEAM_GO`.
- **Gate:** `python scripts/tracka_resume_gate.py --prereg /nonexistent` => `drift_preflight.pass:true`, `status=BLOCKED`, `reason_code=PREREG_OR_MANIFEST_BLOCK_AFTER_DRIFT_PASS`, `fail_closed_order=drift_preflight->manifest_prereg`, `outcomes_inspected:false`.
- **Scope drift:** `python scripts/check_tracka_scope_registry_drift.py --json` => `pass:true`, `scripts=83 registry=83 reason=OK`.
- **Regression (verified):** `python -m unittest tests.test_tracka_hardening_120 ... tests.test_tracka_hardening_128 tests.test_fclr010_harness` => **161 tests OK** (120-128 + harness; tmp-isolated, no network, no parquet/outcome reads, no real research_state writes).
- **Full-suite baseline (deps-present handoff):** 484 OK. **This environment:** numpy/pandas absent in legacy liqmicro/discovery paths; 120-128 deliverables dep-light.
- **Artifacts:** root `*.md+*.json` = **143** (<=163). `research_state` `ironflow_probe*` = **2** (1 live + 1 digest). No new timestamped probe/sweep/scan/wrapper/report families in research_state. No `.github/workflows` changes.

## FCLR-NEXT-128 DELIVERABLES (COMPLETE, EVIDENCED)
| Gap | Deliverable | Status | Evidence |
|---|---|---|---|
| G1 | `scripts.coupled_build_panel` main() blocked-refusal parity: rc=1, `reason_code=PREREG_OR_MANIFEST_BLOCK_AFTER_DRIFT_PASS`, `canonical_outputs_mutated=false`, outcome loader never invoked, canonical snapshots unchanged | COMPLETE | `tests/test_tracka_hardening_128.py::Test128G1*` (2 tests: loader-never-called + stable refusal shape) |
| G2 | `scripts.tracka_operator_report.compose_operator_report` stable seam-wired fields (`admissible_seam_wired` pass/status/reason_code/failures/month/fail_closed/network/reads_outcomes/reads_parquet), drift-preflight-first fail-closed order, missing candidate => fail-closed NO-GO `ADMISSIBLE_CANDIDATE_PATH_MISSING`, GO manifest => seam GO + gate BLOCKED prereg-required | COMPLETE | `tests/test_tracka_hardening_128.py::Test128G2*` (3 tests: no-candidate seam wired, missing candidate fail-closed, GO manifest seam) |
| G3 | Refusal-payload fail-closed matrix extended to `coupled_build_panel` + `fclr010_execute_fast` via `guarded_execute` mocks: rc=1, `canonical_outputs_mutated=false`, canonical snapshots unchanged | COMPLETE | `tests/test_tracka_hardening_128.py::Test128G3*` (2 tests: coupled matrix snapshots, fclr010_execute_fast blocked refusal + snapshots) |

## FCLR-NEXT-129 UNCOVERED GAPS (CODE+TEST ONLY — next session must not skip)
1. **G1:** fused blocked-branch refusal matrix across ALL guarded Track A entrypoints (none may be absent) in `tests/test_tracka_hardening_129.py`.
2. **G2:** `tracka_operator_report` CLI exit-code + JSON + drift-first + `--admissible-manifest` passthrough parity in `tests/test_tracka_hardening_129.py`.
3. **G3:** `check_tracka_scope_registry_drift.py` fails closed on registry/script drift in `tests/test_tracka_hardening_129.py`.

## BOTTLENECKS REMOVED / STILL HARD
- **Removed (this session):** stale initial task pointed at already-complete FCLR-NEXT-127 (entry verified; G1-G3 evidenced); replaced with FCLR-NEXT-128 then FCLR-NEXT-129 so the next session never repeats finished work or idles on a stale task. Absent-month probe churn (exhausted, enforced), status-only/no-delta loops (forbidden), unguarded canonical writes (guarded 120-128), missing gate/fclr010-execute/run_liqmicro refusal coverage (126), tracka_resume_check seam-detail + CLI parity (127), guarded_entry refusal parity (127), coupled/overlay READY writer scope + blocked no-loader (127), coupled_build_panel blocked-refusal parity + operator_report seam-wired + refusal-matrix extension (128). No bottleneck may be "worked around" by re-probing absent months or mutating sealed Track C/B.
- **Hard (do not fight with busywork):** post-2026-10 admissible Hyperliquid Track A liquidation data absent (`data_through=2026-10`). Only a **strictly admissible trigger** (real, documented, Hyperliquid observed, Hyperliquid-only) permits prereg->inspect path — and even then prereg BEFORE inspecting outcomes, root bound preserved.

## VERIFICATION COMMANDS (RUN ON ENTRY/NEXT)
- `python -m unittest tests.test_tracka_hardening_120 tests.test_tracka_hardening_121 tests.test_tracka_hardening_122 tests.test_tracka_hardening_123 tests.test_tracka_hardening_124 tests.test_tracka_hardening_125 tests.test_tracka_hardening_126 tests.test_tracka_hardening_127 tests.test_tracka_hardening_128 tests.test_fclr010_harness` (regression 161 OK, minimal env)
- `python scripts/tracka_resume_check.py` (17 checks, pass)
- `python scripts/tracka_resume_gate.py --prereg /nonexistent` (`drift_preflight.pass:true`, stable reason/order, `outcomes_inspected:false`)
- `python scripts/check_tracka_scope_registry_drift.py --json` (`pass:true`)
- `python -m unittest discover tests` (>=484 green in deps-present env; numpy/pandas import errors in legacy liqmicro tests are env constraints, not 120-128 regressions)

## STOP RULE
Complete ALL steps with concrete metrics. Track C locked. Track B unsupported. No conflation. No workflow/scheduler/poller/status-only/repeated wrappers/agent-controllers/new recurring families. Blocked/no-data claims without measurable hardening delta are noncompliant. Keep root md+json <=163 and probes==2. Leave state STRICTER than found.
