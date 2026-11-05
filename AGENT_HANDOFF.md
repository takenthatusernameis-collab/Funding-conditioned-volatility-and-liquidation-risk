# AGENT_HANDOFF.md (SINGLE DURABLE HANDOFF)
Timestamp (UTC): 20261105T191803Z
Git SHA (HEAD, baseline): d12b90ab (working tree modified by FCLR-NEXT-104 hardening; uncommitted)
Branch: main
Repo: Funding-conditioned-volatility-and-liquidation-risk
Handoff ID: FCLR-HANDOFF-20261105T191803Z | Priority: P0 - REPO-NAME PRIORITIZED + HEAVY WORK MANDATORY | Mode: CAMPAIGN-DRIVEN | Enforcement: NO-SKIP | Bottleneck-State: ROOT-BOUND-PRECONSOLIDATED-155/PROBES-2/LFS-LOCAL-CACHE-AWARE/GATE-REASON-CODES-PRESENT/OPERATOR-COMPOSE-REPORT+PROBE-INVARIANT-RUNTIME-VALIDATED

## REPO-NAME PRIORITIZATION (INFERRED)
Repository name: "Funding-conditioned-volatility-and-liquidation-risk"
- Funding-conditioned VOLATILITY component = Track C (FCLR-011) — **SEALED/LOCKED**. Forecast gate PASSED. DO NOT retune/re-run sealed cells/conflate.
- LIQUIDATION RISK component = Track A (FCLR-010) — **ONLY UNFINISHED HALF / ONLY ACTIVE OBJECTIVE**. BLOCKED on admissible unauthenticated liquidation data (Hyperliquid-only, `data_through=2026-10`; 2026-11..2027-02 absent). Track B = **NOT_SUPPORTED**.
- BOTH components core to repo identity. NO SCOPE DRIFT TO SEALED TRACKS.

## CURRENT VERIFIED STATE (20261105T191803Z)
- **104 measurable delta:** consolidated 2 unreferenced non-canonical root artifacts (`handoff_hardening_audit.md`, `shek_methodology_availability.md`; verified unreferenced by AGENT_HANDOFF/frontier/scripts/tests) into `research_state/tracka_bottleneck_history_090.md#104` with sha256/bytes/excerpt provenance; deleted originals (root 155→153 pre-evidence, probes==2). Added `compose_operator_report()` + `_validate_probe_invariant_runtime_shape()` + `probe_invariant_state()` in `scripts/tracka_resume_check.py` (bounded, read-only, <5s, no network regression, fail-closed, machine-checkable; `fail_closed_order=drift_preflight->gate_decision->probe_invariant_state`; validates `probe_invariant_runtime` presence/shape). Added `tests/test_tracka_hardening_104.py` (8 tmp-isolated deterministic tests).
- Tests (verified this session): **317 tests, OK** (`python -m unittest discover tests`). MUST remain green; run on entry.
- Resume check (CLI): `python scripts/tracka_resume_check.py` — `pass:true`, **15 checks**, `<5s` (0.75s), `network:false`, `writes_real_research_state:false`.
- CLI resume gate: `python scripts/tracka_resume_gate.py --prereg /nonexistent` — `drift_preflight.pass:true`, `reason_code=PREREG_OR_MANIFEST_BLOCK_AFTER_DRIFT_PASS`, `fail_closed_order=drift_preflight->manifest_prereg`, `status=BLOCKED`, `outcomes_inspected:false` (0.73s).
- Operator compose/report (104): `compose_operator_report()` — **PASS**, `probe_invariant_runtime_valid:true`, drift preflight pass + gate BLOCKED + probe invariant pass, 0.61s, no network, no real research_state writes.
- Monitor/trigger (latest probe, **NO TRIGGER**): `research_state/ironflow_probe_20261105T191803Z.json` (+ digest `ironflow_probe_digest_latest.json`) — `data_through=2026-10`, 2026-11..2027-02 absent; `consecutive_absent=3`; `triggered=false`; `probe_invariant_runtime` recorded/present+shape-valid; probes==2. Re-run `monitor --quick` on entry; do not create recurring timestamped probe/scan families.
- Track C: SEALED/LOCKED. Track B: NOT_SUPPORTED.
- Track A: ON-TRIGGER/MONITOR ONLY (Liquidation Risk = only active objective). Latest blocker: `research_state/liquidation_forward_validate_023_blocker_20261105T191803Z.md`. Latest sweep: `research_state/campaign_sweep_tracka_20261105T191803Z.md`. Canonical alt outputs only; no admissible strict GO source.
- Artifact state (verified): root `research_state/*.md+*.json` = **155** (<=163). Ironflow probes = **2**. **Any new root evidence requires prior consolidation** of >=1 unreferenced non-canonical root artifact with sha256/bytes/excerpt provenance into an existing consolidated history (keep probes==2, canonical outputs unchanged).
- **NO COASTING.** Status-only output without measurable hardening delta is noncompliant. Blocked/no-data claims without measurable hardening delta are noncompliant.

## SINGLE INITIAL TASK MESSAGE FOR NEXT AGENTIC SESSION (COPY/PASTE VERBATIM)
```text
TASK ID: FCLR-NEXT-105-TRACK-A-NO-COAST-COMPOSE-CLI-ENTRYPOINT-RESUMECHECK-PROBE-RUNTIME-NAMED-GUARD-BOUND-CONSOLIDATION
PRIORITY: P0 - REPO-NAME PRIORITIZED (Volatility SEALED/LOCKED; Liquidation Risk = ONLY ACTIVE OBJECTIVE)
TIMESTAMP (UTC): 20261105T191803Z
CAMPAIGN: TRACK A LIQUIDATION RISK - IMPOSSIBLE-TO-COAST WHILE BLOCKED. MEASURABLE DELTA REQUIRED. ZERO CHURN. INSTANT IRREFUTABLE RESUME.
ENFORCEMENT: ALL STEPS MANDATORY. SESSION FAILS IF ONLY REPORTS/PROBES OR IF IT REPEATS 104 WITHOUT EXTENDING IT. PREREGISTER BEFORE INSPECTING OUTCOMES IF TRIGGERED. NO IDLE TURNS. NO STATUS-ONLY OUTPUT. NO NEW TIMESTAMPED PROBE/SWEEP/SCAN FAMILIES. NO SCHEDULERS/POLLERS/STATUS FILES/REPEATED WRAPPERS/AGENT-CONTROLLERS. NO WORKFLOW CHANGES.
OBJECTIVE (INFERRED): Complete liquidation-risk half of "Funding-conditioned-volatility-and-liquidation-risk". Data blocked (Hyperliquid data_through 2026-10; 2026-11..2027-02 absent). 104 consolidated 2 unreferenced root artifacts with provenance before evidence (root 155), added compose_operator_report() + probe_invariant_runtime shape/state validation in tracka_resume_check (read-only, <5s, fail-closed, drift_preflight->gate_decision->probe_invariant_state, probe_invariant_runtime_valid), added 8 tmp-isolated tests. 317 tests green; resume_check PASS (15); gate prereg-block shows drift_preflight.pass + stable reason/order; compose PASS (0.61s). ROOT MD+JSON = 155 (<=163) — 105 MUST: (A) Before adding new root evidence, consolidate >=1 unreferenced non-canonical root artifact with sha256/bytes/excerpt provenance (verify unreferenced by AGENT_HANDOFF/frontier/scripts/tests) into an existing consolidated history; keep probes==2 and no recurring families. (B) Add a tiny operator CLI entrypoint/script for compose_operator_report with stable machine-readable JSON and exit semantics (0 PASS, 1 BLOCKED/fail-closed), tmp-isolated deterministic tests; no behavior regressions; read-only/no-network/no real research_state writes. (C) Wire probe_invariant_runtime validation as a named check in tracka_resume_check.run() (fail-closed) and/or add bounded harness/missing-data guard tests covering compose report fields/ordering semantics — preserve existing check names/semantics. (D) Exhaustive trigger probes; update frontier/handoff with full before/after metrics and NEW stricter timestamped task FCLR-NEXT-106 naming exact uncovered gaps. PREREGISTER BEFORE INSPECTING OUTCOMES IF TRIGGERED.
CONSTRAINTS: No credentials/manual files/.github/workflows changes. Leakage-safe, preregister-before-outcomes. Track C/B locked/unsupported. Raw data/caches out of git. Clean-clone reproducible. Hyperliquid-only for Track A. Never conflate observed/modeled liquidations. No threshold-shopping. Canonical outputs only. Do NOT add root md+json files if it breaks the <=163 invariant — consolidate with provenance first.
MANDATORY EXECUTION (ALL REQUIRED; CONCRETE METRICS):
1) ENTRY VERIFY: `python -m unittest discover tests` (>=317 green). `python scripts/tracka_resume_check.py`. compose_operator_report smoke. `monitor --quick`, `deep_review`, `hunt`. Record exact root md+json, probes, tests, watch counts. If NO NEW DATA, continue to hardening.
2) ROOT-BOUND CONSOLIDATION (MEASURABLE, BEFORE EVIDENCE WRITES): identify >=1 unreferenced non-canonical root artifact; move/merge with provenance (sha256/bytes/excerpts) into an existing consolidated history; delete original; confirm root reduced and probes==2 unchanged.
3) OPERATOR CLI ENTRYPOINT + NAMED PROBE-RUNTIME GUARD (MEASURABLE): bounded read-only/no-network-regression/fail-closed CLI/script for compose report + stable JSON/exit; tmp-isolated tests. Wire probe_invariant_runtime validation as named resume_check (fail-closed) preserving existing semantics.
4) EVIDENCE, FRONTIER, HANDOFF (MANDATORY, WITHIN BOUND): Write 024 blocker + 105 sweep ONLY if root <=163 after consolidation; otherwise record in frontier/handoff/history with preserved metrics. Update `research_state/experiment_frontier.json`. Update `AGENT_HANDOFF.md` with NEW stricter timestamped task FCLR-NEXT-106. PREREG BEFORE OUTCOMES IF TRIGGERED.
RESUME CONDITION (only): ironflow `data/events/YYYY-MM.parquet` or `data/fills/YYYY-MM.parquet` month>=2026-11 HTTP 200 unauthenticated OR admissible unauthenticated Hyperliquid source passes strict full-manifest GO gate (`assess_strict_manifest`/harness default). Hyperliquid-only. PREREGISTER BEFORE INSPECTING OUTCOMES.
STOP RULE: Complete ALL steps with concrete metrics. Track C locked. Track B unsupported. No conflation. No workflow/scheduler/poller/status-only/repeated wrappers/agent-controllers/new recurring families. Blocked/no-data claims without measurable hardening delta are noncompliant. Keep root md+json <=163 and probes==2. Leave state STRICTER than found.
```

## VERIFICATION COMMANDS (RUN ON ENTRY)
- `python -m unittest discover tests` (must be >=317, green)
- `python scripts/tracka_resume_check.py` (must pass, 15 checks, <5s)
- `python scripts/tracka_resume_gate.py --prereg /nonexistent` (must show `drift_preflight.pass:true` + `reason_code`/`fail_closed_order`)
- `python -c "import sys;sys.path.insert(0,'.');from scripts.tracka_resume_check import compose_operator_report;import json;r=compose_operator_report();print(json.dumps({k:r[k] for k in ['pass','probe_invariant_runtime_valid','fail_closed_order','elapsed_s']}))"` (must pass)
- `python scripts/monitor_ironflow_liquidations.py --quick`
- `python scripts/deep_review_alt_sources.py`
- `python scripts/hunt_alternative_liquidation_sources.py`

## NEXT TASK (TIMESTAMPED)
20261105T191803Z: Execute FCLR-NEXT-105. Volatility (Track C) SEALED/LOCKED. Liquidation Risk (Track A) = ONLY ACTIVE OBJECTIVE. Root md+json 155 (<=163; consolidation-before-evidence rule applies). probes==2. Latest probe 20261105T191803Z shows **NO TRIGGER** (`data_through=2026-10`; 2026-11..2027-02 absent; `probe_invariant_runtime` present+shape-valid). compose_operator_report PASS. PREREG BEFORE OUTCOMES if triggered.

---
## SESSION ENTRY (2026-11-05T19:18:03Z) — FCLR-NEXT-104 COMPLETE (hardening, no trigger)
Timestamp (UTC): 20261105T191803Z
Git SHA (baseline): d12b90ab
Task: FCLR-NEXT-104 (Track A liquidation risk only; Track C sealed; Track B unsupported).
- **Entry verify:** 309 tests OK (baseline) -> **317 tests OK**. resume_check PASS 15 (0.75s). gate BLOCKED `drift_preflight.pass:true` + `PREREG_OR_MANIFEST_BLOCK_AFTER_DRIFT_PASS` / `drift_preflight->manifest_prereg`. monitor quick `data_through=2026-10`, **NO TRIGGER** (2026-11..2027-02 absent), probe `ironflow_probe_20261105T191803Z.json` with `probe_invariant_runtime`. deep_review/hunt: no admissible strict GO (canonical latest outputs). Root md+json 155, probes 2.
- **(A) Root-bound preconsolidation (measurable):** consolidated `handoff_hardening_audit.md`, `shek_methodology_availability.md` (unreferenced in AGENT_HANDOFF/frontier/scripts/tests) -> `tracka_bottleneck_history_090.md#104` with sha256/bytes/excerpt; deleted originals. Root 155→153 pre-evidence; probes==2. Evidence (023 blocker + 104 sweep) added => root **155 (<=163)**.
- **(B) Operator compose/report (measurable):** `compose_operator_report()` + `probe_invariant_state()` in `scripts/tracka_resume_check.py`; machine-checkable JSON, `fail_closed_order=drift_preflight->gate_decision->probe_invariant_state`, read-only/<5s/no-network/no real RS writes. Real-repo compose PASS (0.61s).
- **(C) probe_invariant_runtime validation (measurable):** `_validate_probe_invariant_runtime_shape()` validates presence/shape/types; compose reports `probe_invariant_runtime_valid:true`. `tests/test_tracka_hardening_104.py` (8 tmp-isolated) green.
- **(D) Evidence/frontier/handoff:** `liquidation_forward_validate_023_blocker_20261105T191803Z.md`, `campaign_sweep_tracka_20261105T191803Z.md`; frontier `20261105T191803Z`; next task **FCLR-NEXT-105** (operator CLI entrypoint + named resume_check probe-runtime guard + bound consolidation). PREREG BEFORE OUTCOMES if triggered (not triggered).
- **Metrics after:** tests 317 OK; resume_check PASS 15; gate reason/order stable; compose PASS; root md+json 155; probes 2; no new recurring families; no workflow/pycache committed.

---
## SESSION ENTRY (2026-11-05T19:13:36Z)
Timestamp (UTC): 20261105T191336Z
Git SHA: 91bb93d3
Next task (unchanged, inferred): FCLR-NEXT-104 (Track A liquidation risk only; Track C sealed; Track B unsupported). Root bound relieved 163->155; probes==2. State verified green: 309 tests OK; resume_check PASS 15; gate BLOCKED/drift_preflight pass + stable reason/order; monitor NO TRIGGER (data_through=2026-10). No code changes this session — handoff refreshed with current metrics; run entry verification commands first.

## SESSION ENTRY (2026-11-05T19:12:32Z)
Timestamp (UTC): 20261105T191232Z
Git SHA: 3bcb07c9
Next task (unchanged, inferred): FCLR-NEXT-104 (Track A liquidation risk only; Track C sealed; Track B unsupported). Root bound 163; probes==2. Bottleneck cleared: tracked __pycache__ drift restored. Run entry verification commands first.
