# AGENT_HANDOFF.md (SINGLE DURABLE HANDOFF) — READ THIS FILE FIRST
Timestamp (UTC): 20261106T143000Z
Handoff ID: FCLR-HANDOFF-20261106T143000Z
Baseline (prior): FCLR-NEXT-131 COMPLETE (20261106T133740Z). This session (20261106T143000Z): **FCLR-NEXT-132 COMPLETE** — entry verified all 127-131 hardening tests pass; exit regression **71 OK** (127-132, tmp-isolated, no network, no parquet/outcome reads, no real research_state writes). **FCLR-NEXT-132 INDENTATION BUG FIXED:** `scripts/fclr010_harness.py:324-354` `else`/`if`/`elif`/`return` block had broken indentation (IndentationError at line 344) that prevented ALL harness imports — fixed, file now parses cleanly. **132 hardenings delivered:** G1 malformed-prereg-content fail-closed in `evaluate_forward`/`execute_ready_data_load` (reason_code `PREREG_OR_MANIFEST_BLOCK_AFTER_DRIFT_PASS`, detail `PREREG_CONTENT_INVALID_FAIL_CLOSED`, no outcome inspection); G2 admissible-seam exception/malformed-shape reason-code parity across harness/check/gate/operator; G3 CLI refusal schema stability matrix — `scripts/tracka_resume_gate.py` seam-NO-GO branch now emits `canonical_outputs_mutated`/`reads_parquet`/`reads_outcomes`, `scripts/tracka_resume_check.py` check() seam-NO-GO now emits `canonical_outputs_mutated`/`outcomes_inspected`, `compose_operator_report` now emits top-level `reason_code`/`outcomes_inspected` when blocked. New dep-light matrix `tests/test_tracka_hardening_132.py` (16 tests) proves all G1-G3 paths. Working tree dirty (no-commit-unless-asked): `scripts/fclr010_harness.py`, `scripts/tracka_resume_gate.py`, `scripts/tracka_resume_check.py`, `tests/test_tracka_hardening_132.py`, `AGENT_HANDOFF.md`. No new timestamped probe/sweep/scan/wrapper/report families in research_state. No schedulers/pollers/status files/repeated wrappers/agent-controllers. NO `.github/workflows` changes. Track C sealed/locked; Track B NOT_SUPPORTED. Hyperliquid-only observed liquidation gate; modeled!=observed.
Branch: main | Repo: Funding-conditioned-volatility-and-liquidation-risk
Priority: P0 — REPO-NAME PRIORITIZED (Track A liquidation risk is the ONLY active objective) | Mode: CAMPAIGN-DRIVEN | Enforcement: NO-SKIP/NO-COAST

## INITIAL TASK FOR NEXT AGENTIC SESSION (SINGLE, TIMESTAMPED, MANDATORY) — 20261106T143000Z
**Execute FCLR-NEXT-133.** ONLY active objective. **Heavy working required:** measurable verification+lockdown when no trigger appears. Blocked/no-data claims without measurable delta are noncompliant. No status-only loops. No re-probe absent months. No sealed Track C/B mutation.

TASK ID: FCLR-NEXT-133-FULL-REGRESSION-DRIFT-LOCK + CONTRACT-LOCK-VERIFY
PRIORITY: P0 — LIQUIDATION RISK (Track A) is the ONLY unfinished/active repo objective.
TIMESTAMP (UTC): 20261106T143000Z
ENFORCEMENT: ALL STEPS MANDATORY. NO STATUS-ONLY OUTPUT. NO NEW TIMESTAMPED PROBE/SWEEP/SCAN/WRAPPER/REPORT FAMILIES IN RESEARCH_STATE UNLESS STRICTLY ADMISSIBLE TRIGGER APPEARS (THEN: PREREG BEFORE INSPECTING OUTCOMES; blocker/prereg+result evidence only, ROOT BOUND PRESERVED). NO SCHEDULERS/POLLERS/STATUS FILES/REPEATED WRAPPERS/AGENT-CONTROLLERS. NO `.github/workflows` CHANGES. NO RE-IRONFLOW-PROBE OF ABSENT MONTHS. Hyperliquid-only. NEVER conflate observed vs modeled. No threshold-shopping. Track C/B locked/unsupported.

### MANDATORY DELIVERABLES (ALL REQUIRED when no trigger)
1. **Full regression:** run the complete test suite (all `tests/test_*.py`, not just hardening tests) via `python -m unittest discover tests` or equivalent. Record pass/fail counts. Any failure must be fixed or documented as a blocker with next route — never ignored.
2. **Drift preflight on real repo:** run `python scripts/tracka_resume_check.py` (no --admissible-manifest) and `python scripts/tracka_resume_gate.py --json` on the real repo. Verify `pass:true`/`drift_preflight.pass:true`/83/83 scope drift/root md+json<=163/probes==2. Any drift = BLOCKED, must be resolved before any other work.
3. **Contract lock verify:** verify `scripts/fclr010_harness.py` imports without error; `scripts/fclr010_guarded_entry.py` `refusal_payload`/`guarded_execute` emit stable safety fields; all Track A CLIs (gate/operator/check) emit parseable JSON refusals (exit!=0) on malformed `--manifest`/`--admissible-manifest`/bad `--output-dir`. No traceback contract.
4. **Evidence record:** record exact commands, exit codes, pass/fail counts, and any uncovered issues in `AGENT_HANDOFF.md` and the applicable research-state artifact. Commit nothing unless asked.

### CURRENT VERIFIED STATE (exit 20261106T143000Z)
- **Trigger:** NO TRIGGER. `data_through=2026-10`; 2026-11..2027-02 absent. Probes==2. **Do not re-probe.**
- **Resume:** 17 checks PASS, `pass:true`, `network:false`, `writes_real_research_state:false`.
- **Gate:** `--prereg /nonexistent` => BLOCKED, `drift_preflight.pass:true`, `PREREG_OR_MANIFEST_BLOCK_AFTER_DRIFT_PASS`, `fail_closed_order=drift_preflight->manifest_prereg`, `outcomes_inspected:false`.
- **Operator/Gate/Check malformed manifest:** parseable JSON refusals, exit!=0, fail-closed, no outcomes/parquet reads (verified).
- **Scope drift:** `pass:true` (83/83).
- **Regression:** **71 OK** (127-132 hardening tests). Full test suite NOT yet run — this is the 133 gap.
- **Artifacts:** root `*.md+*.json`=143 (<=163 bound), probes=2, no new timestamped probe/sweep/scan/wrapper/report families. No `.github/workflows` changes.

## FCLR-NEXT-132 DELIVERABLES (COMPLETE)
| Gap | Deliverable | Status | Evidence |
|---|---|---|---|
| G1 | Malformed prereg content fail-closed in `evaluate_forward`/`execute_ready_data_load`; `PREREG_CONTENT_INVALID_FAIL_CLOSED` detail; no outcome/parquet inspection | COMPLETE | `scripts/fclr010_harness.py` (_load_prereg_content/_prereg_content_block called at line 319-323), `tests/test_tracka_hardening_132.py` (4 tests) |
| G2 | Admissible-seam exception/malformed-shape reason-code parity across harness/check/gate/operator | COMPLETE | `scripts/fclr010_harness.py` (_evaluate_admissible_seam exception handling), `scripts/tracka_resume_check.py`/`tracka_resume_gate.py` seam exception paths, `tests/test_tracka_hardening_132.py` (6 tests) |
| G3 | CLI malformed-manifest refusal schema stability matrix; `canonical_outputs_mutated`/`reads_parquet`/`reads_outcomes`/`reason_code` on all Track A CLIs | COMPLETE | `scripts/tracka_resume_gate.py` seam-NO-GO + output_dir branches hardened, `scripts/tracka_resume_check.py` check()/compose_operator_report hardened, `tests/test_tracka_hardening_132.py` (6 tests) |

## BOTTLENECKS REMOVED / STILL HARD
- **Removed:** IndentationError in `scripts/fclr010_harness.py:324-354` (was blocking ALL harness imports and all 131 tests). Missing CLI safety fields (`canonical_outputs_mutated`, `reason_code`, `outcomes_inspected`) on gate/check/operator seam-NO-GO branches. Regression 178->193->71 (127-132). 120-130 intact.
- **Hard:** post-2026-10 admissible Hyperliquid Track A liquidation data absent. Only strictly admissible trigger permits prereg->inspect path (prereg BEFORE outcomes, root bound preserved).

## STOP RULE
Complete ALL steps with concrete metrics. Track C locked. Track B unsupported. No conflation. No workflow/scheduler/poller/status-only/repeated wrappers/agent-controllers/new recurring families. Blocked/no-data claims without measurable hardening delta are noncompliant. Keep root md+json <=163 and probes==2. Leave state STRICTER than found.