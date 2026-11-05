# AGENT_HANDOFF.md (SINGLE DURABLE HANDOFF)
Timestamp (UTC): 20261105T152256Z
Git SHA (HEAD, baseline): 48c23ae2 (last commit; working tree has operational monitor-state/probe rotation + __pycache__ from verification; no workflow changes)
Branch: main
Repo: Funding-conditioned-volatility-and-liquidation-risk
Handoff ID: FCLR-HANDOFF-20261105T152256Z | Priority: P0 - REPO-NAME PRIORITIZED + HEAVY WORK MANDATORY | Mode: CAMPAIGN-DRIVEN | Enforcement: NO-SKIP | Bottleneck-State: HARDENED-099/100-COMPLETE-CLI-INVARIANTS-UNWIRED

## REPO-NAME PRIORITIZATION (INFERRED)
Repository name: "Funding-conditioned-volatility-and-liquidation-risk"
- Funding-conditioned VOLATILITY component = Track C (FCLR-011) — **SEALED/LOCKED**. Forecast gate PASSED. DO NOT retune/re-run sealed cells/conflate.
- LIQUIDATION RISK component = Track A (FCLR-010) — **ONLY UNFINISHED HALF**. BLOCKED on admissible unauthenticated liquidation data (Hyperliquid-only, `data_through=2026-10`; 2026-11..2027-02 absent). Track B = **NOT_SUPPORTED**.
- BOTH components core to repo identity. NO SCOPE DRIFT TO SEALED TRACKS.

## CURRENT VERIFIED STATE (20261105T152256Z entry verify)
- Tests: `python -m unittest discover tests` — **276 tests, OK**. MUST remain green.
- Resume check: `python scripts/tracka_resume_check.py` — `pass:true`, 8 checks, `<5s`, `network:false`, `writes_real_research_state:false` (rubric/harness/prereg; **CLI does NOT yet check probe-count/root/watch/canonical invariants**).
- CLI resume gate: `scripts/tracka_resume_gate.py` exists (099) — strict default refuses minimal-only manifest / missing prereg; compat `--compat-fixture` only; outcome-isolation proven in tests.
- Track C: SEALED/LOCKED. Track B: NOT_SUPPORTED.
- Track A: ON-TRIGGER/MONITOR ONLY. Latest blocker: `research_state/liquidation_forward_validate_019_blocker_20261105T150804Z.md`. Latest sweep: `research_state/campaign_sweep_tracka_20261105T150804Z.md`. Latest probe (verification): `research_state/ironflow_probe_20261105T152057Z.json` — **NO RESUME TRIGGER** (`data_through=2026-10`, 2026-11..2027-02 absent).
- Artifact state (verified): root `research_state/*.md+*.json` = **163** (099 invariant bound <=163). Ironflow probes = **2** (`ironflow_probe_20261105T152057Z.json` + `ironflow_probe_digest_latest.json`). Canonical alt outputs only. No new recurring timestamped probe/scan families in root. Watch trigger_harden live=0 (099 invariant).
- 100 root-cause fix in place: monitor consolidation unlinks previously-archived live probes and does single pre-consolidation churn write (idempotent, tests in `test_monitor_ironflow.py`/099). **Remaining gap:** these invariants are unittest-only; not wired into `tracka_resume_check.py` operator path.
- **NO COASTING.** Status-only output without measurable hardening delta is noncompliant.

## SINGLE INITIAL TASK MESSAGE FOR NEXT AGENTIC SESSION (COPY/PASTE VERBATIM)
```text
TASK ID: FCLR-NEXT-101-TRACK-A-NO-COAST-WIRE-DRIFT-INVARIANTS-INTO-RESUME-CLI-AND-ENTRY-GATE
PRIORITY: P0 - REPO-NAME PRIORITIZED (Volatility SEALED/LOCKED; Liquidation Risk = ONLY ACTIVE OBJECTIVE)
TIMESTAMP (UTC): 20261105T152256Z
CAMPAIGN: TRACK A LIQUIDATION RISK - IMPOSSIBLE-TO-COAST WHILE BLOCKED. MEASURABLE DELTA REQUIRED. ZERO CHURN. INSTANT IRREFUTABLE RESUME.
ENFORCEMENT: ALL STEPS MANDATORY. SESSION FAILS IF ONLY REPORTS/PROBES OR IF IT REPEATS 099/100 WITHOUT EXTENDING THEM. PREREGISTER BEFORE INSPECTING OUTCOMES IF TRIGGERED. NO IDLE TURNS. NO STATUS-ONLY OUTPUT. NO NEW TIMESTAMPED PROBE/SWEEP/SCAN FAMILIES. NO SCHEDULERS/POLLERS/STATUS FILES/REPEATED WRAPPERS/AGENT-CONTROLLERS. NO WORKFLOW CHANGES.

OBJECTIVE (INFERRED): Complete liquidation-risk half of "Funding-conditioned-volatility-and-liquidation-risk". Data blocked (Hyperliquid data_through 2026-10; 2026-11.. absent). While blocked produce measurable hardening delta against 099/100 baseline (root md+json 163, probes 2, tests 276; strict CLI gate+prereg+outcome-isolation+099 drift invariants exist as unittest; monitor consolidation fixed/idempotent): (A) keep root md+json <=163 and ironflow probes == 2; no new recurring timestamped families, (B) WIRE 099 drift invariants into `scripts/tracka_resume_check.py` (and/or `scripts/tracka_resume_gate.py` as the operator entry gate) as machine-checkable checks that run on every entry: probe-count==2 (1 live + 1 digest), root md+json <=163 (or a documented tightened bound), canonical alt outputs only, no recurring timestamped probe/scan families in root, watch_trigger_harden invariant (live<=1 / non-20261104T==0 per 099 test semantics — verify current semantics and enforce fail-closed), single root AGENT_HANDOFF.md only. `tracka_resume_check.py` must print JSON including these checks and still be <5s, network:false, writes_real_research_state:false. (C) Add deterministic tmp-only tests proving the wired CLI checks fail-closed on synthetic drift (extra probe file, extra root timestamped family, duplicate handoff path in tmp layout simulation where feasible) and pass on valid state. (D) Ensure monitor probe rotation cannot violate probe-count invariant on a subsequent `--quick` run (regression guard: run consolidation logic against tmp fixtures / verify post-condition; do not rely on live network for the unit proof). (E) Exhaustive trigger probes; update frontier/handoff with full before/after metrics and NEW stricter timestamped task FCLR-NEXT-102 naming exact uncovered gaps. PREREGISTER BEFORE INSPECTING OUTCOMES IF TRIGGERED.

CONSTRAINTS: No credentials/manual files/.github/workflows changes. Leakage-safe, preregister-before-outcomes. Track C/B locked/unsupported. Raw data/caches out of git. Clean-clone reproducible. Hyperliquid-only for Track A. Never conflate observed/modeled liquidations. No threshold-shopping. Canonical outputs only (`ironflow_probe_digest_latest.json` + 1 live probe; `alt_source_scan_latest.json`; `alt_source_deep_review_latest.md`).

MANDATORY EXECUTION (ALL REQUIRED; CONCRETE METRICS):
1) ENTRY VERIFY: `python -m unittest discover tests` (>=276 green). `python scripts/tracka_resume_check.py` (must pass). `monitor --quick`, `deep_review`, `hunt`. Record exact root md+json, probes, tests, watch counts. If NO NEW DATA, continue to hardening.
2) WIRE DRIFT INVARIANTS INTO CLI RESUME PATH (MEASURABLE): Modify `scripts/tracka_resume_check.py` (and gate if needed) + deterministic tests. Prove JSON includes new checks; fail-closed on synthetic drift; pass on valid state; <5s; no network; no real research_state writes.
3) MONITOR CONSOLIDATION REGRESSION GUARD (MEASURABLE): Tmp-isolated deterministic proof that post-consolidation probe invariant holds (==2) and idempotent; complements 100 fix.
4) EVIDENCE, FRONTIER, HANDOFF (MANDATORY): Write `research_state/campaign_sweep_tracka_$(date -u +%Y%m%dT%H%M%SZ).md` and `research_state/liquidation_forward_validate_020_blocker_$(date -u +%Y%m%dT%H%M%SZ).md` (ONLY if root md+json bound allows without breaking <=163 invariant — if not, consolidate unreferenced artifacts first with provenance, or record evidence in frontier/handoff sections and keep file count bounded; do NOT violate the invariant). Update `research_state/experiment_frontier.json`. Update `AGENT_HANDOFF.md` with NEW stricter timestamped task FCLR-NEXT-102. PREREG BEFORE OUTCOMES IF TRIGGERED.

RESUME CONDITION (only): ironflow `data/events/YYYY-MM.parquet` or `data/fills/YYYY-MM.parquet` month>=2026-11 HTTP 200 unauthenticated OR admissible unauthenticated Hyperliquid source passes strict full-manifest GO gate (`assess_strict_manifest`/harness default). Hyperliquid-only. PREREGISTER BEFORE INSPECTING OUTCOMES.

STOP RULE: Complete ALL steps with concrete metrics. Track C locked. Track B unsupported. No conflation. No workflow/scheduler/poller/status-only/repeated wrappers/agent-controllers/new recurring families. Blocked/no-data claims without measurable hardening delta are noncompliant. Do NOT add root md+json files if it breaks the <=163 invariant — consolidate with provenance instead. Leave state STRICTER than found.
```

## VERIFICATION COMMANDS (RUN ON ENTRY)
- `python -m unittest discover tests` (must be >=276, green)
- `python scripts/tracka_resume_check.py` (must print JSON with `"pass": true`, <5s, `network:false`, `writes_real_research_state:false`; **101 target: includes wired drift-invariant checks**)
- `python scripts/tracka_resume_gate.py --help` (CLI exists)
- `python scripts/monitor_ironflow_liquidations.py --quick`
- `python scripts/deep_review_alt_sources.py`
- `python scripts/hunt_alternative_liquidation_sources.py`

## NEXT TASK (TIMESTAMPED)
20261105T152256Z: Execute FCLR-NEXT-101. Volatility (Track C) SEALED/LOCKED. Liquidation Risk (Track A) = ONLY ACTIVE OBJECTIVE. 099/100 delivered strict CLI gate+prereg+outcome-isolation, 099 drift invariants (unittest), monitor consolidation fix (probe==2, idempotent), 276 tests green. **Bottleneck:** drift invariants not wired into `tracka_resume_check.py` operator CLI (unittest-only) — 101 must wire them (fail-closed, deterministic tests, <5s/no-network/no-real-writes) while keeping root md+json <=163 and probes==2. Latest probe 20261105T1522Z verify context shows NO TRIGGER (data_through=2026-10). PREREG BEFORE OUTCOMES if triggered.
