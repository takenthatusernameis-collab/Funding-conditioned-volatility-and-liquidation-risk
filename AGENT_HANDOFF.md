# AGENT_HANDOFF.md (SINGLE DURABLE HANDOFF) — READ THIS FILE FIRST
Timestamp (UTC): 20261106T113316Z
Handoff ID: FCLR-HANDOFF-20261106T113316Z
Baseline (prior session): FCLR-NEXT-126 COMPLETE (20261106T110947Z, 8 tests, 138 regression green: 120+121+122+123+124+125+126+fclr010_harness). IRONFLOW PROBING EXHAUSTED (90+, `data_through=2026-10`, 2026-11..2027-02 absent); probes==2; root md+json==2.
This session (20261106T113316Z): **ENTRY VERIFIED** — regression 138 OK pre-change (120-125+harness), resume 17 checks pass (`pass:true`, `network:false`, `writes_real_research_state:false`), gate BLOCKED fail-closed (`drift_preflight.pass:true`, `PREREG_OR_MANIFEST_BLOCK_AFTER_DRIFT_PASS`, `outcomes_inspected:false`), scope drift `pass:true` (83/83). NO TRIGGER; IRONFLOW PROBING EXHAUSTED — **NO re-probing absent months**. FCLR-NEXT-126 delivered (G1-G3) as measurable dep-light/tmp-isolated code+tests (`tests/test_tracka_hardening_126.py`, 8 tests). Working tree includes untracked `tests/test_tracka_hardening_125.py` and `tests/test_tracka_hardening_126.py` (not committed; no-commit-unless-asked). No new timestamped probe/sweep/scan/wrapper/report families in research_state. No schedulers/pollers/status files/repeated wrappers/agent-controllers. NO `.github/workflows` changes. Track C sealed/locked; Track B NOT_SUPPORTED.
Branch: main | Repo: Funding-conditioned-volatility-and-liquidation-risk
Priority: P0 — REPO-NAME PRIORITIZED (Track A liquidation risk is the ONLY active objective; Track C volatility sealed/locked; Track B NOT_SUPPORTED) | Mode: CAMPAIGN-DRIVEN | Enforcement: NO-SKIP/NO-COAST

## INITIAL TASK FOR NEXT AGENTIC SESSION (SINGLE, TIMESTAMPED, MANDATORY) — 20261106T113316Z
**Execute FCLR-NEXT-127.** ONLY active objective. **Heavy working required:** measurable **code+test** hardening when no trigger appears (G1-G3 below). Blocked/no-data claims without measurable hardening delta are noncompliant. No status-only loops. No re-probe absent months. No sealed Track C/B mutation.

TASK ID: FCLR-NEXT-127-RESUME-CHECK-SEAM-GO-DETAIL + GUARDED-ENTRY-REFUSAL-REASON-PARITY + OVERLAY/COUPLED-WRITER-READY-SCOPE
PRIORITY: P0 — LIQUIDATION RISK (Track A) is the ONLY unfinished/active repo objective (Funding-conditioned VOLATILITY Track C sealed/locked; Track B NOT_SUPPORTED).
TIMESTAMP (UTC): 20261106T113316Z
ENFORCEMENT: ALL STEPS MANDATORY. NO STATUS-ONLY OUTPUT. NO NEW TIMESTAMPED PROBE/SWEEP/SCAN/WRAPPER/REPORT FAMILIES IN RESEARCH_STATE UNLESS STRICTLY ADMISSIBLE TRIGGER APPEARS (THEN: PREREG BEFORE INSPECTING OUTCOMES; blocker/prereg+result evidence only, ROOT BOUND PRESERVED). NO SCHEDULERS/POLLERS/STATUS FILES/REPEATED WRAPPERS/AGENT-CONTROLLERS. NO `.github/workflows` CHANGES. NO RE-IRONFLOW-PROBE OF ABSENT MONTHS. Hyperliquid-only for Track A observed-liquidation gate. NEVER conflate observed vs modeled liquidations. No threshold-shopping. Track C/B locked/unsupported.

### MANDATORY DELIVERABLES (G1-G3, ALL REQUIRED when no trigger)
1. **G1 (tracka_resume_check seam detail parity):** `scripts.tracka_resume_check.check` / CLI preserve stable machine fields when a candidate `--admissible-manifest` is supplied: drift preflight pass/fail-closed first, `admissible_seam` includes `pass/status/reason_code/failures/month/fail_closed/network/reads_outcomes/reads_parquet` (or explicit NO-GO failure codes), `network=false`, `writes_real_research_state=false`, `reads_parquet=false`, `reads_outcomes=false`. Missing/bad candidate => fail-closed NO-GO with stable reason. Dep-light/tmp-isolated tests in `tests/test_tracka_hardening_127.py`.
2. **G2 (guarded_entry refusal reason/detail parity):** `scripts.fclr010_guarded_entry.guarded_execute`/`refusal_payload` preserve 126-stable `reason_code=PREREG_OR_MANIFEST_BLOCK_AFTER_DRIFT_PASS` + `seam_go_prereg_required`/`reason_code_detail` when seam GO but prereg/data missing; do not regress to ambiguous codes. Assert on `fclr010_execute` + `run_liqmicro` blocked refusal payloads via mocks (no parquet/import side effects).
3. **G3 (READY writer scope, dep-light):** for `coupled_robust_eval` and/or `overlay_quick`/`overlay_tracka_execute` (choose available dep-light path; stub heavy deps if needed), mocked READY_FROZEN path must not mutate canonical Track A evaluation/manifest/frontier beyond documented allowed targets, and blocked path must never invoke loaders/writers; assert with tmp snapshots and `canonical_outputs_mutated=false` on blocked refusals.

### CURRENT VERIFIED STATE (exit verify 20261106T113316Z)
- **Trigger:** NO TRIGGER. `ironflow_probe_20261105T200406Z.json` / `ironflow_probe_digest_latest.json` — `data_through=2026-10`; 2026-11..2027-02 absent. IRONFLOW PROBING EXHAUSTED (90+). **Do not re-probe.**
- **Resume:** `python scripts/tracka_resume_check.py` **17 checks PASS**, `pass:true`, `network:false`, `writes_real_research_state:false`. `--admissible-manifest` CLI: missing candidate => rc=1 NO-GO `ADMISSIBLE_CANDIDATE_PATH_MISSING`; valid GO manifest => rc=0 `ADMISSIBLE_SEAM_GO`.
- **Gate:** `python scripts/tracka_resume_gate.py --prereg /nonexistent` => `drift_preflight.pass:true`, `status=BLOCKED`, `reason_code=PREREG_OR_MANIFEST_BLOCK_AFTER_DRIFT_PASS`, `fail_closed_order=drift_preflight->manifest_prereg`, `outcomes_inspected:false`.
- **Scope drift:** `python scripts/check_tracka_scope_registry_drift.py --json` => `pass:true`, `scripts=83 registry=83 reason=OK`.
- **Regression (verified):** `python -m unittest tests.test_tracka_hardening_120 tests.test_tracka_hardening_121 tests.test_tracka_hardening_122 tests.test_tracka_hardening_123 tests.test_tracka_hardening_124 tests.test_tracka_hardening_125 tests.test_tracka_hardening_126 tests.test_tracka_hardening_127 tests.test_fclr010_harness` => **154 tests OK** (120-127 + harness; tmp-isolated, no network, no parquet/outcome reads, no real research_state writes).
- **Full-suite baseline (deps-present handoff):** 484 OK. **This environment:** numpy/pandas absent in legacy liqmicro/discovery paths; 120-127 deliverables dep-light.
- **Artifacts:** root `*.md+*.json` = **143** (<=163). `research_state` `ironflow_probe*` = **2** (1 live + 1 digest). Working tree: untracked `tests/test_tracka_hardening_125.py`, `tests/test_tracka_hardening_126.py`, `tests/test_tracka_hardening_127.py` (not committed). No new timestamped probe/sweep/scan/wrapper/report families in research_state.

## FCLR-NEXT-127 DELIVERABLES (COMPLETE, EVIDENCED)
| Gap | Deliverable | Status | Evidence |
|---|---|---|---|
| G1 | `scripts.tracka_resume_check.check` + `--admissible-manifest` CLI: drift preflight first; seam `pass/status/reason_code/failures/month/fail_closed/network/reads_outcomes/reads_parquet`; missing candidate => fail-closed NO-GO `ADMISSIBLE_CANDIDATE_PATH_MISSING`; `network=false/writes_real_research_state=false/reads_parquet=false/reads_outcomes=false` | COMPLETE | `tests/test_tracka_hardening_127.py::Test127G1*` (8 tests: missing/bad/GO/no-candidate/drift-first/CLI-rc1/CLI-rc0) |
| G2 | `guarded_execute`/`refusal_payload` preserve `reason_code=PREREG_OR_MANIFEST_BLOCK_AFTER_DRIFT_PASS` + `seam_go_prereg_required`/`reason_code_detail=ADMISSIBLE_SEAM_GO_PREREG_REQUIRED`; `seam_go_data_missing` parity; `fclr010_execute`+`run_liqmicro` blocked refusal rc=1 via mocks | COMPLETE | `tests/test_tracka_hardening_127.py::Test127G2*` (6 tests: seam-GO-prereg parity, seam-GO-data-missing parity, refusal shape, fclr010_execute blocked, run_liqmicro blocked) |
| G3 | `coupled_robust_eval`/`overlay_quick`/`overlay_tracka_execute` blocked path: rc=1, `canonical_outputs_mutated=false`, loader/writers never invoked, canonical snapshots unchanged; READY_FROZEN mocked path completes without canonical mutation | COMPLETE | `tests/test_tracka_hardening_127.py::Test127G3*` + `Test127G3ReadyFrozenNoCanonicalMutation` (4 blocked + 1 READY_FROZEN) |

## 127 EXECUTION PROTOCOL (HEAVY, MANDATORY)
1. **Entry verify:** run 120-127+harness, `tracka_resume_check.py`, `tracka_resume_gate.py --prereg /nonexistent`, `check_tracka_scope_registry_drift.py --json`; confirm NO TRIGGER/probes==2/root<=163. Record counts honestly.
2. **Implement G1-G3** as measurable dep-light/tmp-isolated code+tests in `tests/test_tracka_hardening_127.py`. No existing guards weakened; additive hardening only. No canonical mutation on blocked paths.
3. **Run tests:** `python -m unittest tests.test_tracka_hardening_127` + regression `120-127+test_fclr010_harness`. Note env constraints honestly (numpy/pandas absent).
4. **Exit verify:** resume/gate/drift pass; probes==2; root `*.md+*.json`<=163; no new recurring families.
5. **Update this handoff** to next timestamp with 127 evidence table, regression count, and `FCLR-NEXT-128` uncovered gaps (code+test only). Root bound kept.

## FCLR-NEXT-128 UNCOVERED GAPS (CODE+TEST ONLY — next session must not skip)
1. **G1:** `scripts/coupled_build_panel.py` blocked-refusal parity (rc=1, `canonical_outputs_mutated=false`, outcome loader never called on BLOCKED guard) + dep-light test in `tests/test_tracka_hardening_128.py`.
2. **G2:** `scripts/tracka_operator_report.py::compose_operator_report` preserves stable seam-wired fields (`admissible_seam_wired` pass/status/reason_code/failures/month/fail_closed/network/reads_outcomes/reads_parquet) and drift-preflight-first fail-closed order; dep-light test.
3. **G3:** Extend refusal-payload fail-closed matrix to `coupled_build_panel` + `fclr010_execute_fast` via `guarded_execute` mocks; assert `canonical_outputs_mutated=false` and canonical snapshots unchanged.

## BOTTLENECKS REMOVED / STILL HARD
- **Removed:** absent-month probe churn (exhausted, enforced), status-only/no-delta loops (forbidden), unguarded canonical writes (120-126 guards), missing gate/fclr010-execute/run_liqmicro refusal+write-scope coverage (126), tracka_resume_check seam-detail + CLI parity (127 G1), guarded_entry refusal reason/detail parity (127 G2), coupled/overlay READY writer scope + blocked no-loader (127 G3). No bottleneck may be "worked around" by re-probing absent months or mutating sealed Track C/B.
- **Hard (do not fight with busywork):** post-2026-10 admissible Hyperliquid Track A liquidation data absent (`data_through=2026-10`). Only a **strictly admissible trigger** (real, documented, Hyperliquid observed, Hyperliquid-only) permits prereg->inspect path — and even then prereg BEFORE inspecting outcomes, root bound preserved.

## VERIFICATION COMMANDS (RUN ON ENTRY/NEXT)
- `python -m unittest tests.test_tracka_hardening_120 tests.test_tracka_hardening_121 tests.test_tracka_hardening_122 tests.test_tracka_hardening_123 tests.test_tracka_hardening_124 tests.test_tracka_hardening_125 tests.test_tracka_hardening_126 tests.test_tracka_hardening_127 tests.test_fclr010_harness` (regression 154 OK, minimal env)
- `python scripts/tracka_resume_check.py` (17 checks, pass)
- `python scripts/tracka_resume_gate.py --prereg /nonexistent` (`drift_preflight.pass:true`, stable reason/order, `outcomes_inspected:false`)
- `python scripts/check_tracka_scope_registry_drift.py --json` (`pass:true`)
- `python -m unittest discover tests` (>=484 green in deps-present env; numpy/pandas import errors in legacy liqmicro tests are env constraints, not 120-127 regressions)

## STOP RULE
Complete ALL steps with concrete metrics. Track C locked. Track B unsupported. No conflation. No workflow/scheduler/poller/status-only/repeated wrappers/agent-controllers/new recurring families. Blocked/no-data claims without measurable hardening delta are noncompliant. Keep root md+json <=163 and probes==2. Leave state STRICTER than found.
