# AGENT_HANDOFF.md (SINGLE DURABLE HANDOFF) — READ THIS FILE FIRST
Timestamp (UTC): 20261106T133530Z
Handoff ID: FCLR-HANDOFF-20261106T133530Z
Baseline (prior session): FCLR-NEXT-129 COMPLETE (20261106T124035Z, regression 169 OK 120-129+harness). This session (20261106T133530Z): **ENTRY VERIFIED** — regression **178 OK** pre/post (120-130 + harness, tmp-isolated, no network, no parquet/outcome reads, no real research_state writes), resume 17 checks pass (`pass:true`,`network:false`,`writes_real_research_state:false`), gate BLOCKED fail-closed (`drift_preflight.pass:true`,`PREREG_OR_MANIFEST_BLOCK_AFTER_DRIFT_PASS`,`outcomes_inspected:false`,`fail_closed_order=drift_preflight->manifest_prereg`), scope drift `pass:true` (83/83). **NO TRIGGER; IRONFLOW PROBING EXHAUSTED — NO re-probing absent months.** FCLR-NEXT-130 delivered (G1-G3) with small fail-closed hardenings: `fclr010_harness.execute_ready_data_load` loader-exception now emits stable refusal fields/reason_code; `tracka_resume_gate` CLI now returns machine-readable JSON refusal on malformed manifest/decision exceptions (no traceback contract). Working tree dirty: `AGENT_HANDOFF.md`, `scripts/fclr010_harness.py`, `scripts/tracka_resume_gate.py`, `tests/test_tracka_hardening_130.py` (no-commit-unless-asked). No new timestamped probe/sweep/scan/wrapper/report families in research_state. No schedulers/pollers/status files/repeated wrappers/agent-controllers. NO `.github/workflows` changes. Track C sealed/locked; Track B NOT_SUPPORTED.
Branch: main | Repo: Funding-conditioned-volatility-and-liquidation-risk
Priority: P0 — REPO-NAME PRIORITIZED (Track A liquidation risk is the ONLY active objective; Track C volatility sealed/locked; Track B NOT_SUPPORTED) | Mode: CAMPAIGN-DRIVEN | Enforcement: NO-SKIP/NO-COAST

## INITIAL TASK FOR NEXT AGENTIC SESSION (SINGLE, TIMESTAMPED, MANDATORY) — 20261106T133530Z
**Execute FCLR-NEXT-131.** ONLY active objective. **Heavy working required:** measurable code+test hardening when no trigger appears (G1-G3 below). Blocked/no-data claims without measurable hardening delta are noncompliant. No status-only loops. No re-probe absent months. No sealed Track C/B mutation.

TASK ID: FCLR-NEXT-131-HARNESS-SEAM-EXCEPTION-MATRIX + OPERATOR/CLI-JSON-REFUSAL-PARITY + GUARD-SNAPSHOT-FIELD-STABILITY
PRIORITY: P0 — LIQUIDATION RISK (Track A) is the ONLY unfinished/active repo objective (Funding-conditioned VOLATILITY Track C sealed/locked; Track B NOT_SUPPORTED).
TIMESTAMP (UTC): 20261106T133530Z
ENFORCEMENT: ALL STEPS MANDATORY. NO STATUS-ONLY OUTPUT. NO NEW TIMESTAMPED PROBE/SWEEP/SCAN/WRAPPER/REPORT FAMILIES IN RESEARCH_STATE UNLESS STRICTLY ADMISSIBLE TRIGGER APPEARS (THEN: PREREG BEFORE INSPECTING OUTCOMES; blocker/prereg+result evidence only, ROOT BOUND PRESERVED). NO SCHEDULERS/POLLERS/STATUS FILES/REPEATED WRAPPERS/AGENT-CONTROLLERS. NO `.github/workflows` CHANGES. NO RE-IRONFLOW-PROBE OF ABSENT MONTHS. Hyperliquid-only for Track A observed-liquidation gate. NEVER conflate observed vs modeled liquidations. No threshold-shopping. Track C/B locked/unsupported.

### MANDATORY DELIVERABLES (G1-G3, ALL REQUIRED when no trigger)
1. **G1 (harness seam/guard exception fail-closed matrix):** dep-light tmp-isolated tests in `tests/test_tracka_hardening_131.py` asserting `FCLR010Harness.evaluate_forward`/`execute_ready_data_load`/`guarded_execute` paths fail closed with stable refusal fields (`status=BLOCKED`,`reason_code=PREREG_OR_MANIFEST_BLOCK_AFTER_DRIFT_PASS` or explicit stable detail as applicable, `outcomes_inspected:false`,`canonical_outputs_mutated:false`,`network:false`,`writes_real_research_state:false`,`reads_parquet:false`,`reads_outcomes:false`) when: admissible seam check raises/returns malformed shape (mocked), manifest evaluator raises, and prereg read path is invalid but must not inspect outcomes. No parquet/outcome reads, no network, no real research_state writes. Harden only if current behavior is not already stable/fail-closed.
2. **G2 (operator/CLI JSON refusal parity on machine contracts):** `scripts.tracka_operator_report` and `scripts.tracka_resume_gate` (and `tracka_resume_check` if it emits JSON on blocked paths) must return parseable JSON refusals (no traceback-as-contract) on malformed admissible-manifest JSON/path shapes where feasible, with stable required fields and exit!=0; extend dep-light tmp-isolated tests in `tests/test_tracka_hardening_131.py`. Preserve existing drift-first/admissible-seam semantics; do not loosen BLOCKED behavior.
3. **G3 (guard snapshot / refusal_payload field stability):** `scripts.fclr010_guarded_entry.refusal_payload` + guard snapshots must always include required boolean/type-stable fields and tolerate missing/extra guard keys without raising; `guarded_execute` must normalize absent booleans to safe defaults on BLOCKED. Add focused dep-light tests in `tests/test_tracka_hardening_131.py`.

### CURRENT VERIFIED STATE (exit verify 20261106T133530Z)
- **Trigger:** NO TRIGGER. `ironflow_probe_20251105T200406Z.json` / `ironflow_probe_digest_latest.json` — `data_through=2026-10`; 2026-11..2027-02 absent. IRONFLOW PROBING EXHAUSTED. **Do not re-probe.**
- **Resume:** `python scripts/tracka_resume_check.py` **17 checks PASS**, `pass:true`, `network:false`, `writes_real_research_state:false`.
- **Gate:** `python scripts/tracka_resume_gate.py --prereg /nonexistent` => `drift_preflight.pass:true`, `status=BLOCKED`, `reason_code=PREREG_OR_MANIFEST_BLOCK_AFTER_DRIFT_PASS`, `fail_closed_order=drift_preflight->manifest_prereg`, `outcomes_inspected:false`. Malformed manifest CLI now returns JSON refusal (130 G2 hardening).
- **Operator CLI:** `--admissible-manifest /nonexistent` / malformed JSON => fail-closed NO-GO/load-error, drift-first, stable seam fields, no outcomes.
- **Scope drift:** `python scripts/check_tracka_scope_registry_drift.py --json` => `pass:true`, `scripts=83 registry=83 reason=OK`.
- **Regression (verified):** `python -m unittest tests.test_tracka_hardening_120 ... tests.test_tracka_hardening_130 tests.test_fclr010_harness` => **178 tests OK** (tmp-isolated, no network, no parquet/outcome reads, no real research_state writes).
- **Artifacts:** root `*.md+*.json` = **2** (bound <=163). `research_state` `ironflow_probe*` = **2**. No new timestamped probe/sweep/scan/wrapper/report families in research_state. No `.github/workflows` changes.

## FCLR-NEXT-130 DELIVERABLES (COMPLETE, EVIDENCED)
| Gap | Deliverable | Status | Evidence |
|---|---|---|---|
| G1 | `guarded_execute`/loader refusal contract: READY path with absent loader + `allow_default_loader=false` performs no parquet/outcome reads (safe explicit-loader-required state); loader exception and invalid-payload-shape paths fail closed BLOCKED with stable refusal flags and no reads/writes/network; default loader never invoked when not explicitly enabled | COMPLETE | `tests/test_tracka_hardening_130.py::Test130G1GuardedEntryLoaderContract` (4 tests); `scripts/fclr010_harness.py` loader-exception refusal fields hardened |
| G2 | `tracka_resume_gate` CLI blocked-matrix parity (missing prereg, malformed prereg fixture, malformed manifest JSON refusal, valid prereg + missing data) stable JSON/exit/reason/order, no outcomes/network/writes | COMPLETE | `tests/test_tracka_hardening_130.py::Test130G2ResumeGateCLIMatrix` (4 tests); `scripts/tracka_resume_gate.py` machine-readable refusal on malformed manifest/decision exceptions |
| G3 | Cross-entrypoint refusal payload schema parity/types for all 10 guarded Track A entrypoints on BLOCKED (required fields present, `status/reason_code` stable, required booleans false, canonical snapshots unchanged) | COMPLETE | `tests/test_tracka_hardening_130.py::Test130G3RefusalPayloadSchemaParity` (1 matrix test, 10 subtests) |

## FCLR-NEXT-131 UNCOVERED GAPS (CODE+TEST ONLY — next session must not skip)
1. **G1:** harness seam/manifest-evaluator/prereg exception matrix => fail-closed stable refusal fields, no outcomes/parquet reads/network/writes (`tests/test_tracka_hardening_131.py`; harden only if needed).
2. **G2:** operator/gate/check CLI JSON refusal parity on malformed admissible-manifest contracts where feasible (parseable JSON, no traceback contract, stable fields/exit!=0, semantics preserved) (`tests/test_tracka_hardening_131.py`).
3. **G3:** `refusal_payload`/guard snapshot field stability + safe boolean normalization on BLOCKED for missing/extra guard keys (`tests/test_tracka_hardening_131.py`; harden only if needed).

## BOTTLENECKS REMOVED / STILL HARD
- **Removed (this session):** 130 G1-G3 delivered (loader/default-loader/exception/invalid-payload contracts, gate CLI malformed-manifest JSON refusal, 10-entrypoint refusal schema parity). Harness loader-exception payload now carries stable refusal flags. Prior 120-129 hardening remains green. No workaround via re-probing absent months or mutating sealed Track C/B.
- **Hard (do not fight with busywork):** post-2026-10 admissible Hyperliquid Track A liquidation data absent (`data_through=2026-10`, probes==2). Only a **strictly admissible trigger** (real, documented, Hyperliquid observed, Hyperliquid-only) permits prereg->inspect path — prereg BEFORE inspecting outcomes, root bound preserved.

## VERIFICATION COMMANDS (RUN ON ENTRY/NEXT)
- `python -m unittest tests.test_tracka_hardening_120 tests.test_tracka_hardening_121 tests.test_tracka_hardening_122 tests.test_tracka_hardening_123 tests.test_tracka_hardening_124 tests.test_tracka_hardening_125 tests.test_tracka_hardening_126 tests.test_tracka_hardening_127 tests.test_tracka_hardening_128 tests.test_tracka_hardening_129 tests.test_tracka_hardening_130 tests.test_fclr010_harness` (regression **178 OK**, minimal env)
- `python scripts/tracka_resume_check.py` (17 checks, pass)
- `python scripts/tracka_resume_gate.py --prereg /nonexistent` (`drift_preflight.pass:true`, `PREREG_OR_MANIFEST_BLOCK_AFTER_DRIFT_PASS`, `fail_closed_order=drift_preflight->manifest_prereg`, `outcomes_inspected:false`)
- `python scripts/tracka_operator_report.py --json --admissible-manifest /nonexistent` (drift-first, fail-closed NO-GO seam, gate blocked)
- `python scripts/check_tracka_scope_registry_drift.py --json` (`pass:true`, 83/83)
- `python -m unittest discover tests` (>=501 green in deps-present env expected from 178+323 baseline; numpy/pandas import errors in legacy liqmicro tests are env constraints, not 120-130 regressions)

## STOP RULE
Complete ALL steps with concrete metrics. Track C locked. Track B unsupported. No conflation. No workflow/scheduler/poller/status-only/repeated wrappers/agent-controllers/new recurring families. Blocked/no-data claims without measurable hardening delta are noncompliant. Keep root md+json <=163 and probes==2. Leave state STRICTER than found.
