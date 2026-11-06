# AGENT_HANDOFF.md (SINGLE DURABLE HANDOFF) — READ THIS FILE FIRST
Timestamp (UTC): 20261106T133740Z
Handoff ID: FCLR-HANDOFF-20261106T133740Z
Baseline (prior): FCLR-NEXT-130 COMPLETE (20261106T133530Z, regression 178 OK 120-130+harness). This session (20261106T133740Z): **FCLR-NEXT-131 COMPLETE** — entry verified 178 OK; exit regression **193 OK** (120-131 + harness, +15, tmp-isolated, no network, no parquet/outcome reads, no real research_state writes). Resume 17 PASS (`pass:true`,`network:false`,`writes_real_research_state:false`). Gate BLOCKED fail-closed (`drift_preflight.pass:true`,`PREREG_OR_MANIFEST_BLOCK_AFTER_DRIFT_PASS`,`fail_closed_order=drift_preflight->manifest_prereg`,`outcomes_inspected:false`). Scope drift `pass:true` (83/83). **NO TRIGGER; IRONFLOW PROBING EXHAUSTED — NO re-probing absent months** (`data_through=2026-10`, probes==2). **131 hardenings delivered:** `scripts/fclr010_harness.py` evaluate_forward/execute_ready_data_load now emit stable fail-closed refusal fields on manifest-gate NO-GO, seam NO-GO before outcomes, data-missing, and precheck/seam exceptions (`canonical_outputs_mutated:false`,`network:false`,`writes_real_research_state:false`,`reads_parquet:false`,`reads_outcomes:false` where applicable); new dep-light matrix `tests/test_tracka_hardening_131.py` (15 tests) proves G1 harness/guarded exception+invalid-manifest/prereg-no-outcome paths, G2 operator/gate/check malformed admissible-manifest JSON refusals (parseable, exit!=0, stable fail-closed fields, no traceback contract), G3 refusal_payload/guard snapshot stability + guarded_execute BLOCKED boolean normalization for absent/truthy safety fields. `scripts/tracka_resume_check|gate|operator_report` already had 131-era JSON refusal handling (verified parseable on malformed admissible manifests). Working tree dirty (no-commit-unless-asked): `scripts/fclr010_harness.py`, `tests/test_tracka_hardening_131.py`, `AGENT_HANDOFF.md`. No new timestamped probe/sweep/scan/wrapper/report families in research_state. No schedulers/pollers/status files/repeated wrappers/agent-controllers. NO `.github/workflows` changes. Track C sealed/locked; Track B NOT_SUPPORTED. Hyperliquid-only observed liquidation gate; modeled!=observed.
Branch: main | Repo: Funding-conditioned-volatility-and-liquidation-risk
Priority: P0 — REPO-NAME PRIORITIZED (Track A liquidation risk is the ONLY active objective) | Mode: CAMPAIGN-DRIVEN | Enforcement: NO-SKIP/NO-COAST

## INITIAL TASK FOR NEXT AGENTIC SESSION (SINGLE, TIMESTAMPED, MANDATORY) — 20261106T133740Z
**Execute FCLR-NEXT-132.** ONLY active objective. **Heavy working required:** measurable code+test hardening when no trigger appears (G1-G3). Blocked/no-data claims without measurable hardening delta are noncompliant. No status-only loops. No re-probe absent months. No sealed Track C/B mutation.

TASK ID: FCLR-NEXT-132-EVALUATE_FORWARD-PREREG-CONTENT-FAILCLOSED + ADMISSIBLE-SEAM-EXCEPTION-CODE-PARITY + CLI-MALFORMED-MANIFEST-SCHEMA-STABILITY
PRIORITY: P0 — LIQUIDATION RISK (Track A) is the ONLY unfinished/active repo objective.
TIMESTAMP (UTC): 20261106T133740Z
ENFORCEMENT: ALL STEPS MANDATORY. NO STATUS-ONLY OUTPUT. NO NEW TIMESTAMPED PROBE/SWEEP/SCAN/WRAPPER/REPORT FAMILIES IN RESEARCH_STATE UNLESS STRICTLY ADMISSIBLE TRIGGER APPEARS (THEN: PREREG BEFORE INSPECTING OUTCOMES; blocker/prereg+result evidence only, ROOT BOUND PRESERVED). NO SCHEDULERS/POLLERS/STATUS FILES/REPEATED WRAPPERS/AGENT-CONTROLLERS. NO `.github/workflows` CHANGES. NO RE-IRONFLOW-PROBE OF ABSENT MONTHS. Hyperliquid-only. NEVER conflate observed vs modeled. No threshold-shopping. Track C/B locked/unsupported.

### MANDATORY DELIVERABLES (G1-G3, ALL REQUIRED when no trigger)
1. **G1 (evaluate_forward prereg-content fail-closed, minimal semantics-safe):** `FCLR010Harness.evaluate_forward` currently reaches READY_FROZEN when `pre_reg_path` exists but contains malformed/unreadable JSON (131 observed) and does not invoke explicit loader unless caller requests it — acceptable only if the contract is explicit. Add/extend `tests/test_tracka_hardening_132.py` (dep-light, tmp-isolated, no network, no parquet/outcome reads, no real research_state writes) to assert the exact current contract: malformed existing prereg must NOT inspect outcomes, must NOT read parquet implicitly, must return stable machine fields (`outcomes_inspected:false`, `reads_parquet/reads_outcomes` false or explicit no-implicit-load flags). If the contract is ambiguous/unsafe, harden minimally to fail closed as BLOCKED with `reason_code=PREREG_OR_MANIFEST_BLOCK_AFTER_DRIFT_PASS`/detail `PREREG_CONTENT_INVALID_FAIL_CLOSED` (no outcome inspection) while preserving READY+valid-prereg behavior.
2. **G2 (admissible-seam exception reason-code parity across harness/check/gate/operator):** normalize `admissible_seam_check`/harness `_evaluate_admissible_seam` exception and malformed-shape surfaces to stable machine fields where feasible (`pass:false`, `status:NO-GO|BLOCKED` as context-appropriate, stable `reason_code`/`failures`, `fail_closed:true`, `network:false`, `reads_outcomes:false`, `reads_parquet:false`), without changing drift-first ordering or converting valid NO-GO semantics into crashes. Add `tests/test_tracka_hardening_132.py` matrix for check CLI, gate CLI, operator CLI, harness method on mocked exceptions/malformed candidate manifests (tmp files).
3. **G3 (CLI refusal schema stability matrix):** all Track A operator/check/gate CLIs touched by 131/132 must emit parseable JSON refusals (no traceback contract) on malformed `--admissible-manifest`/`--manifest`/bad temp-path edge cases covered by tests, with stable required safety fields present (`status` or `pass:false` context, `fail_closed`/blocked semantics, `network:false`, `reads_outcomes:false`/`reads_parquet:false` or `outcomes_inspected:false` as applicable). Extend `tests/test_tracka_hardening_132.py`; harden only if missing.

### CURRENT VERIFIED STATE (exit 20261106T133740Z)
- **Trigger:** NO TRIGGER. `data_through=2026-10`; 2026-11..2027-02 absent. Probes==2. **Do not re-probe.**
- **Resume:** 17 checks PASS, `pass:true`, `network:false`, `writes_real_research_state:false`.
- **Gate:** `--prereg /nonexistent` => BLOCKED, `drift_preflight.pass:true`, `PREREG_OR_MANIFEST_BLOCK_AFTER_DRIFT_PASS`, `fail_closed_order=drift_preflight->manifest_prereg`, `outcomes_inspected:false`.
- **Operator/Gate/Check malformed admissible manifest:** parseable JSON refusals, exit!=0, fail-closed, no outcomes/parquet reads (verified).
- **Scope drift:** `pass:true` (83/83).
- **Regression:** **193 OK** (`120-131` + `fclr010_harness`, tmp-isolated).
- **Artifacts:** root `*.md+*.json`=2, probes=2, no new timestamped probe/sweep/scan/wrapper/report families. No `.github/workflows` changes.

## FCLR-NEXT-131 DELIVERABLES (COMPLETE)
| Gap | Deliverable | Status | Evidence |
|---|---|---|---|
| G1 | Harness/guarded exception+invalid-manifest fail-closed matrix; stable refusal fields on seam/manifest/precheck exceptions and manifest-gate NO-GO/data-missing/seam NO-GO branches; no outcome inspection | COMPLETE | `scripts/fclr010_harness.py` (evaluate_forward/execute_ready_data_load hardened), `tests/test_tracka_hardening_131.py` (6 tests) |
| G2 | Operator/gate/check malformed admissible-manifest JSON refusal parity (parseable, exit!=0, stable fail-closed fields, no traceback contract) | COMPLETE | `tests/test_tracka_hardening_131.py` (4 tests); verified CLI outputs for gate/operator/check |
| G3 | `refusal_payload`/guard snapshot stability + `guarded_execute` BLOCKED boolean normalization (absent/truthy safety fields -> false), no canonical mutation | COMPLETE | `tests/test_tracka_hardening_131.py` (5 tests); `scripts/fclr010_guarded_entry.py` existing normalization verified |

## FCLR-NEXT-132 UNCOVERED GAPS (CODE+TEST ONLY)
1. **G1:** malformed existing prereg content in `evaluate_forward` — make contract explicit/fail-closed without outcome inspection (`tests/test_tracka_hardening_132.py`).
2. **G2:** admissible-seam exception/malformed-shape reason-code parity across harness/check/gate/operator (`tests/test_tracka_hardening_132.py`).
3. **G3:** CLI malformed-manifest refusal schema stability matrix for covered Track A CLIs (`tests/test_tracka_hardening_132.py`).

## BOTTLENECKS REMOVED / STILL HARD
- **Removed:** 131 harness/CLI/guard refusal hardening + 15 dep-light tests; regression 178->193. 120-130 intact.
- **Hard:** post-2026-10 admissible Hyperliquid Track A liquidation data absent. Only strictly admissible trigger permits prereg->inspect path (prereg BEFORE outcomes, root bound preserved).

## STOP RULE
Complete ALL steps with concrete metrics. Track C locked. Track B unsupported. No conflation. No workflow/scheduler/poller/status-only/repeated wrappers/agent-controllers/new recurring families. Blocked/no-data claims without measurable hardening delta are noncompliant. Keep root md+json <=163 and probes==2. Leave state STRICTER than found.
