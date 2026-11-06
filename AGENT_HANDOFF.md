# AGENT_HANDOFF.md (SINGLE DURABLE HANDOFF) — READ THIS FILE FIRST
Timestamp (UTC): 20261106T041556Z
Handoff ID: FCLR-HANDOFF-20261106T041556Z
Baseline (prior session commit): abcada7c (`chore(kilo): checkpoint agent session`). FCLR-NEXT-118 COMPLETE (20261106T035900Z, no trigger). **This session (20261106T041556Z) performed entry verify only and refreshed the single durable handoff; no research code changes, no trigger, no new probes/families.** Working tree may contain local modified `__pycache__` and `research_state/ironflow_fastpath_cache.json` — **do not commit**.
Branch: main | Repo: Funding-conditioned-volatility-and-liquidation-risk
Priority: P0 — REPO-NAME PRIORITIZED + HEAVY WORK MANDATORY | Mode: CAMPAIGN-DRIVEN | Enforcement: NO-SKIP/NO-COAST
Bottlenecks removed this session: none data-side (IRONFLOW PROBING EXHAUSTED 90+, data_through=2026-10, 2026-11..2027-02 absent). Handoff bottleneck removed: single timestamped initial task for next session made explicit below. **Next session must deliver measurable code+test hardening (FCLR-NEXT-119 G1-G5) — status-only output is noncompliant.**

## INITIAL TASK FOR NEXT AGENTIC SESSION (SINGLE, TIMESTAMPED, MANDATORY) — 20261106T041556Z
**Execute FCLR-NEXT-119.** This is the ONLY active objective. Do not run status-only loops. Do not re-probe absent ironflow months (exhausted, 90+ CONFIRMED_ABSENT). Do not touch sealed Track C/B. Deliver measurable **code+test** hardening when no trigger appears.

TASK ID: FCLR-NEXT-119-FCLR010-READY-FROZEN-END-TO-END-PATH + H004-ALLOWED-PILOT-ARTIFACT-BOUNDARY + CI-ENFORCED-SCOPE-REGISTRY-DRIFT + RUN_LIQMICRO_V2-NO-FRONTIER-MUTATION-SURFACE + EXPERIMENT_FRONTIER-MUTATION-AUDIT
PRIORITY: P0 — LIQUIDATION RISK (Track A) is the ONLY unfinished/active repo objective (Funding-conditioned VOLATILITY Track C sealed/locked).
TIMESTAMP (UTC): 20261106T041556Z
ENFORCEMENT: ALL STEPS MANDATORY. NO STATUS-ONLY OUTPUT. ENTRY VERIFY IS MANDATORY BUT INSUFFICIENT ALONE. NO NEW TIMESTAMPED PROBE/SWEEP/SCAN/WRAPPER/REPORT FAMILIES IN RESEARCH_STATE UNLESS A STRICTLY ADMISSIBLE TRIGGER APPEARS (THEN: PREREG BEFORE INSPECTING OUTCOMES; blocker/prereg+result evidence only, ROOT BOUND PRESERVED). NO SCHEDULERS/POLLERS/STATUS FILES/REPEATED WRAPPERS/AGENT-CONTROLLERS. NO `.github/workflows` CHANGES. NO RE-IRONFLOW-PROBE OF ABSENT MONTHS. Hyperliquid-only for Track A observed-liquidation gate. NEVER conflate observed vs modeled liquidations. No threshold-shopping. Track C/B locked/unsupported.

### MANDATORY DELIVERABLES (G1-G5, ALL REQUIRED when no trigger)
1. **G1 (READY_FROZEN end-to-end testability, no real outcomes):** Deterministic tmp-isolated tests proving READY_FROZEN branch is reached only via `guarded_execute` READY_FROZEN (source order + branch-order asserted), and that no canonical `evaluation_summary*`/`run_manifest.json`/`experiment_frontier.json` mutation occurs when trigger absent. No real outcome data/network.
2. **G2 (h004 allowed-path pilot artifact boundary):** Tmp-isolated tests proving allowed historical-pilot path writes target only non-canonical pilot artifacts and cannot touch Hyperliquid Track A canonical targets/frontier/run_manifest/cross-track liquidation gate fields; assert no `FCLR010Harness`/`fclr010_guarded_entry` invocation from allowed path.
3. **G3 (scope-registry drift, repo-local enforcement):** Add repo-local drift check (script and/or test; **do NOT modify `.github/workflows`**) that fails on `scripts/*.py` additions/removals not reflected in `research_state/tracka_script_scope_registry.json` (and keeps it reconciled with `test_tracka_hardening_117.SCRIPT_REGISTRY`). Preserve root<=163/probes==2.
4. **G4 (run_liqmicro_v2 no-frontier-mutation surface):** Regression test asserting `run_liqmicro_v2` never mutates `experiment_frontier.json` under any state (blocked/ready/refused); confirm no future v2 frontier mutation surface is added unguarded.
5. **G5 (experiment_frontier mutation audit):** Tmp-isolated tests proving blocked `main()` of `run_liqmicro_v2` + all `guarded_tracka_ready_writing` scripts never mutate `experiment_frontier.json` (snapshot before/after, no diff). No network/parquet/outcome reads, no real `research_state` writes.

### MANDATORY EXECUTION (ALL REQUIRED; CONCRETE METRICS)
1) **ENTRY VERIFY** (record exact): `python -m unittest discover tests` (>=469 green). `python scripts/tracka_resume_check.py` (>=17 checks, incl. `probe_invariant_runtime_named`+`admissible_seam_wired`, pass). `python scripts/tracka_resume_gate.py --prereg /nonexistent` (`drift_preflight.pass:true`, stable reason/order, `outcomes_inspected:false`). `python scripts/tracka_operator_report.py; echo $?` (`pass:true`, exit 0). Record root md+json (<=163) and probes (==2). Do NOT re-probe ironflow absent months.
2) **TRIGGER CHECK** (bounded, no new families): inspect latest monitor/probe state only (`research_state/ironflow_probe_20261105T200406Z.json` / `ironflow_probe_digest_latest.json`). No new recurring probe/scan files.
3) **NO-TRIGGER HEAVY-WORK HARDENING DELTA** (REQUIRED): deliver G1-G5 with `tests/test_tracka_hardening_119.py` (tmp-isolated, deterministic, no network, no parquet/outcome reads, no real `research_state` writes). Make refusal/guards machine-enforced in code only if needed.
4) **TRIGGER PATH** (only if appears): ironflow `data/events|data/fills/YYYY-MM.parquet` month>=2026-11 HTTP 200 unauthenticated OR admissible unauthenticated Hyperliquid source passes strict full-manifest GO gate => validate via seam (manifest-only) + **PREREGISTER BEFORE INSPECTING OUTCOMES**; execute forward validation through guarded data-load path only; Hyperliquid-only; separate observed vs modeled; canonical outputs; respect root bound.
5) **HANDOFF/FRONTIER** (required on completion): update `AGENT_HANDOFF.md` and `research_state/experiment_frontier.json` with concrete before/after metrics (suite count, changed files, reason-code table, G1-G5 status) and emit **FCLR-NEXT-120** (stricter, naming exact uncovered gaps). Run full `python -m unittest discover tests`; report before/after.

### ACCEPTANCE
- Full suite green (>=469 before, report after). Resume 17 PASS. Gate stable (`drift_preflight.pass:true`, `outcomes_inspected:false`). Operator `pass:true` exit 0.
- G1-G5 covered by tmp-isolated deterministic tests; no network/parquet/outcome reads; no real `research_state` writes in tests.
- Root `research_state/*.md+*.json` <=163; probes==2. No `.github/workflows` changes. No `__pycache__`/`ironflow_fastpath_cache.json` committed.

RESUME/GO CONDITION (data trigger only): ironflow `data/events/YYYY-MM.parquet` or `data/fills/YYYY-MM.parquet` month>=2026-11 HTTP 200 unauthenticated OR admissible unauthenticated Hyperliquid source passes strict full-manifest GO gate. Hyperliquid-only. **PREREGISTER BEFORE INSPECTING OUTCOMES.**
STOP RULE: Complete ALL steps with concrete metrics. Track C locked. Track B unsupported. No conflation. No workflow/scheduler/poller/status-only/repeated wrappers/agent-controllers/new recurring families. Blocked/no-data claims without measurable hardening delta are noncompliant. Keep root md+json <=163 and probes==2. Leave state STRICTER than found.

## REPO-NAME PRIORITIZATION (INFERRED)
Repository: `Funding-conditioned-volatility-and-liquidation-risk`
- **Funding-conditioned VOLATILITY** = Track C (FCLR-011) — **SEALED/LOCKED**. Forecast gate PASSED. DO NOT retune/re-run/conflate.
- **LIQUIDATION RISK** = Track A (FCLR-010) — **ONLY UNFINISHED / ONLY ACTIVE OBJECTIVE**. BLOCKED on admissible unauthenticated liquidation data (Hyperliquid-only, `data_through=2026-10`; 2026-11..2027-02 absent). Track B = **NOT_SUPPORTED**.

## CURRENT VERIFIED STATE (entry verify 20261106T041556Z, read-only, no trigger)
- Tests: **469/469 OK** (`Ran 469 tests`, `OK`).
- Resume: **17 checks PASS** (`tracka_resume_check`, incl. `probe_invariant_runtime_named` + `admissible_seam_wired`, <5s, `network:false`, `writes_real_research_state:false`).
- Gate: `drift_preflight.pass:true`, `status=BLOCKED`, `reason_code=PREREG_OR_MANIFEST_BLOCK_AFTER_DRIFT_PASS`, `fail_closed_order=drift_preflight->manifest_prereg`, `outcomes_inspected:false`.
- Operator: `pass:true`, exit `0`, `network:false`, `read_only:true`, `writes_real_research_state:false`.
- Monitor/trigger: **NO TRIGGER**. `ironflow_probe_20261105T200406Z.json` (+ digest) — `data_through=2026-10`, 2026-11..2027-02 absent. **IRONFLOW PROBING EXHAUSTED (90+ CONFIRMED_ABSENT) — do not re-probe.**
- Artifacts: root `research_state/*.md+*.json` = **143** (<=163). Ironflow probes = **2**.
- Working-tree hygiene: local modified `__pycache__` and `research_state/ironflow_fastpath_cache.json` — **never commit**.

## VERIFICATION COMMANDS (RUN ON ENTRY)
- `python -m unittest discover tests` (>=469, green)
- `python scripts/tracka_resume_check.py` (>=17 checks, pass)
- `python scripts/tracka_resume_gate.py --prereg /nonexistent` (`drift_preflight.pass:true`, stable reason/order, `outcomes_inspected:false`)
- `python scripts/tracka_operator_report.py; echo $?` (`pass:true`, exit `0`)

## 119 UNCOVERED GAPS (close with code+tests)
- READY_FROZEN end-to-end path cannot be exercised without admissible trigger data. Add deterministic tmp-isolated test proving READY_FROZEN branch reached only via guarded_execute READY_FROZEN (source order + branch-order asserted) and no canonical summary/manifest/frontier write when trigger absent.
- h004 allowed path still writes its own pilot artifacts (evaluation_summary_FCLR005.md, LIQ_ENUM, CKPT_PANEL) by design. Add tmp-isolated test proving allowed-path writes target non-canonical paths only and cannot touch Hyperliquid Track A canonical targets; assert no FCLR010Harness/fclr010_guarded_entry invocation from allowed path.
- Registry drift check is static (test-time only). Add repo-local drift check (script/test; do NOT modify .github/workflows) that fails on scripts/*.py additions/removals not reflected in research_state/tracka_script_scope_registry.json; preserve root<=163/probes==2.
- run_liqmicro_v2 does not write experiment_frontier.json (by design; only run_liqmicro v1 does). Add regression test asserting run_liqmicro_v2 never mutates experiment_frontier.json under any state; confirm no future v2 frontier mutation surface is added unguarded.
- experiment_frontier.json mutation audit: tmp-isolated test proving blocked main() of run_liqmicro_v2 + all guarded_tracka_ready_writing scripts never mutates experiment_frontier.json (snapshot before/after, no diff).
