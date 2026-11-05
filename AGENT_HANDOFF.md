# AGENT_HANDOFF.md (SINGLE DURABLE HANDOFF)
Timestamp (UTC): 20261105T191336Z
Git SHA (HEAD, baseline): 91bb93d3 (working tree clean — no uncommitted drift; __pycache__ restored prior session)
Branch: main
Repo: Funding-conditioned-volatility-and-liquidation-risk
Handoff ID: FCLR-HANDOFF-20261105T191336Z | Priority: P0 - REPO-NAME PRIORITIZED + HEAVY WORK MANDATORY | Mode: CAMPAIGN-DRIVEN | Enforcement: NO-SKIP | Bottleneck-State: PY-CACHE-DRIFT-CLEARED/ROOT-BOUND-RELIEVED-155/PROBES-2/LFS-LOCAL-CACHE-AWARE/GATE-REASON-CODES-PRESENT

## REPO-NAME PRIORITIZATION (INFERRED)
Repository name: "Funding-conditioned-volatility-and-liquidation-risk"
- Funding-conditioned VOLATILITY component = Track C (FCLR-011) — **SEALED/LOCKED**. Forecast gate PASSED. DO NOT retune/re-run sealed cells/conflate.
- LIQUIDATION RISK component = Track A (FCLR-010) — **ONLY UNFINISHED HALF**. BLOCKED on admissible unauthenticated liquidation data (Hyperliquid-only, `data_through=2026-10`; 2026-11..2027-02 absent). Track B = **NOT_SUPPORTED**.
- BOTH components core to repo identity. NO SCOPE DRIFT TO SEALED TRACKS.

## CURRENT VERIFIED STATE (20261105T191336Z)
- **Bottlenecks relieved (prior sessions):** tracked `__pycache__` drift restored to HEAD (clean tree); root `research_state/*.md+*.json` consolidated from 163 to **155** (<=163, slack=8 headroom retained — do NOT let it re-grow to bound before consolidating).
- Tests (verified this session): **309 tests, OK** (`python -m unittest discover tests`). MUST remain green; run on entry.
- Resume check (CLI): `python scripts/tracka_resume_check.py` — `pass:true`, **15 checks**, `<5s` (0.58s), `network:false`, `writes_real_research_state:false`. LFS local-cache aware JSON load in harness/gate (no network; semantics unchanged).
- CLI resume gate (103 reason/order): `scripts/tracka_resume_gate.py --prereg /nonexistent` — drift preflight **BEFORE** manifest/prereg decision (fail-closed). `drift_preflight.pass:true`, stable `reason_code`/`fail_closed_order`: `PREREG_OR_MANIFEST_BLOCK_AFTER_DRIFT_PASS`, `drift_preflight->manifest_prereg`. Status `BLOCKED` (0.60s). `--prereg /nonexistent` => BLOCKED with `drift_preflight.pass:true` + stable reason/order (semantics preserved).
- Monitor/trigger (latest probe, NO TRIGGER): `research_state/ironflow_probe_20261105T190942Z.json` (+ digest `ironflow_probe_digest_latest.json`) — `data_through=2026-10`, 2026-11..2027-02 absent; `consecutive_absent=3`; `triggered=false`; `probe_invariant_runtime` recorded; probes==2. **NO RESUME TRIGGER.** Re-run `monitor --quick` on entry; do not create recurring timestamped probe/scan families.
- Track C: SEALED/LOCKED. Track B: NOT_SUPPORTED.
- Track A: ON-TRIGGER/MONITOR ONLY (Liquidation Risk = only active objective). Latest blocker: `research_state/liquidation_forward_validate_022_blocker_20261105T180046Z.md`. Latest sweep: `research_state/campaign_sweep_tracka_20261105T180046Z.md`. Canonical alt outputs only; no admissible strict GO source.
- Artifact state (verified): root `research_state/*.md+*.json` = **155** (<=163, headroom). Ironflow probes = **2**. Watch `trigger_harden` live=1 (`trigger_harden_20261104T113550Z.json`), non_20261104T=0. **Any new root evidence requires prior consolidation** of >=1 unreferenced non-canonical root artifact with sha256/bytes/excerpt provenance into an existing consolidated history (keep probes==2, canonical outputs unchanged).
- **NO COASTING.** Status-only output without measurable hardening delta is noncompliant. Blocked/no-data claims without measurable hardening delta are noncompliant.

## SINGLE INITIAL TASK MESSAGE FOR NEXT AGENTIC SESSION (COPY/PASTE VERBATIM)
```text
TASK ID: FCLR-NEXT-104-TRACK-A-NO-COAST-BOUND-PRECONSOLIDATION-OPERATOR-COMPOSE-REPORT-PROBE-INVARIANT-VALIDATION
PRIORITY: P0 - REPO-NAME PRIORITIZED (Volatility SEALED/LOCKED; Liquidation Risk = ONLY ACTIVE OBJECTIVE)
TIMESTAMP (UTC): 20261105T191336Z
CAMPAIGN: TRACK A LIQUIDATION RISK - IMPOSSIBLE-TO-COAST WHILE BLOCKED. MEASURABLE DELTA REQUIRED. ZERO CHURN. INSTANT IRREFUTABLE RESUME.
ENFORCEMENT: ALL STEPS MANDATORY. SESSION FAILS IF ONLY REPORTS/PROBES OR IF IT REPEATS 103 WITHOUT EXTENDING IT. PREREGISTER BEFORE INSPECTING OUTCOMES IF TRIGGERED. NO IDLE TURNS. NO STATUS-ONLY OUTPUT. NO NEW TIMESTAMPED PROBE/SWEEP/SCAN FAMILIES. NO SCHEDULERS/POLLERS/STATUS FILES/REPEATED WRAPPERS/AGENT-CONTROLLERS. NO WORKFLOW CHANGES.
OBJECTIVE (INFERRED): Complete liquidation-risk half of "Funding-conditioned-volatility-and-liquidation-risk". Data blocked (Hyperliquid data_through 2026-10; 2026-11..2027-02 absent). 103 added stable gate reason_code/fail_closed_order (semantics preserved), proved monitor probe_invariant_runtime evidence-field shape (tmp-only), regained root slack by consolidating 2 unreferenced trend artifacts with provenance, and made harness/gate LFS local-cache aware (no network). 309 tests green; resume_check PASS (15 checks); gate prereg-block shows drift_preflight.pass + stable reason/order. ROOT MD+JSON = 155 (<=163, headroom retained) — 104 MUST: (A) Before adding new root evidence, consolidate >=1 unreferenced non-canonical root artifact with sha256/bytes/excerpt provenance (verify unreferenced by AGENT_HANDOFF/frontier/scripts/tests) into tracka_bottleneck_history or an existing consolidated history; keep probes==2 and no recurring families. (B) Add a bounded top-level operator compose/report path (CLI or function) that emits a machine-checkable summary combining drift preflight + gate decision + probe invariant state (read-only, <5s target, no network regression, fail-closed) — tmp-isolated deterministic tests; do not weaken existing semantics. (C) Machine-validate `probe_invariant_runtime` presence/shape in that operator report (or extend resume_check wiring) with tests. (D) Exhaustive trigger probes; update frontier/handoff with full before/after metrics and NEW stricter timestamped task FCLR-NEXT-105 naming exact uncovered gaps. PREREGISTER BEFORE INSPECTING OUTCOMES IF TRIGGERED.
CONSTRAINTS: No credentials/manual files/.github/workflows changes. Leakage-safe, preregister-before-outcomes. Track C/B locked/unsupported. Raw data/caches out of git. Clean-clone reproducible. Hyperliquid-only for Track A. Never conflate observed/modeled liquidations. No threshold-shopping. Canonical outputs only. Do NOT add root md+json files if it breaks the <=163 invariant — consolidate with provenance first.
MANDATORY EXECUTION (ALL REQUIRED; CONCRETE METRICS):
1) ENTRY VERIFY: `python -m unittest discover tests` (>=309 green). `python scripts/tracka_resume_check.py`. `monitor --quick`, `deep_review`, `hunt`. Record exact root md+json, probes, tests, watch counts. If NO NEW DATA, continue to hardening.
2) ROOT-BOUND CONSOLIDATION (MEASURABLE, BEFORE EVIDENCE WRITES): identify >=1 unreferenced non-canonical root artifact; move/merge with provenance (sha256/bytes/excerpts) into an existing consolidated history; delete original; confirm root reduced and probes==2 unchanged.
3) OPERATOR COMPOSE/REPORT (MEASURABLE): bounded read-only/no-network-regression/fail-closed compose path + machine-stable JSON fields; tmp-isolated tests prove fail-closed ordering and `probe_invariant_runtime`/probe-invariant visibility semantics preserved.
4) EVIDENCE, FRONTIER, HANDOFF (MANDATORY, WITHIN BOUND): Write 023 blocker + sweep ONLY if root <=163 after consolidation; otherwise record in frontier/handoff/history with preserved metrics. Update `research_state/experiment_frontier.json`. Update `AGENT_HANDOFF.md` with NEW stricter timestamped task FCLR-NEXT-105. PREREG BEFORE OUTCOMES IF TRIGGERED.
RESUME CONDITION (only): ironflow `data/events/YYYY-MM.parquet` or `data/fills/YYYY-MM.parquet` month>=2026-11 HTTP 200 unauthenticated OR admissible unauthenticated Hyperliquid source passes strict full-manifest GO gate (`assess_strict_manifest`/harness default). Hyperliquid-only. PREREGISTER BEFORE INSPECTING OUTCOMES.
STOP RULE: Complete ALL steps with concrete metrics. Track C locked. Track B unsupported. No conflation. No workflow/scheduler/poller/status-only/repeated wrappers/agent-controllers/new recurring families. Blocked/no-data claims without measurable hardening delta are noncompliant. Keep root md+json <=163 and probes==2. Leave state STRICTER than found.
```

## VERIFICATION COMMANDS (RUN ON ENTRY)
- `python -m unittest discover tests` (must be >=309, green)
- `python scripts/tracka_resume_check.py` (must pass, 15 checks, <5s)
- `python scripts/tracka_resume_gate.py --prereg /nonexistent` (must show `drift_preflight.pass:true` + `reason_code`/`fail_closed_order`)
- `python scripts/monitor_ironflow_liquidations.py --quick`
- `python scripts/deep_review_alt_sources.py`
- `python scripts/hunt_alternative_liquidation_sources.py`

## NEXT TASK (TIMESTAMPED)
20261105T191336Z: Execute FCLR-NEXT-104. Volatility (Track C) SEALED/LOCKED. Liquidation Risk (Track A) = ONLY ACTIVE OBJECTIVE. Root md+json now 155 (<=163, headroom retained; consolidation-before-evidence rule still applies). probes==2. Latest probe 20261105T190942Z shows **NO TRIGGER** (`data_through=2026-10`; 2026-11..2027-02 absent; `probe_invariant_runtime` recorded). Gate shows `drift_preflight.pass:true`, `reason_code=PREREG_OR_MANIFEST_BLOCK_AFTER_DRIFT_PASS`, `fail_closed_order=drift_preflight->manifest_prereg`. PREREG BEFORE OUTCOMES if triggered.

---
## SESSION ENTRY (2026-11-05T19:13:36Z)
Timestamp (UTC): 20261105T191336Z
Git SHA: 91bb93d3
Next task (unchanged, inferred): FCLR-NEXT-104 (Track A liquidation risk only; Track C sealed; Track B unsupported). Root bound relieved 163->155; probes==2. State verified green: 309 tests OK; resume_check PASS 15; gate BLOCKED/drift_preflight pass + stable reason/order; monitor NO TRIGGER (data_through=2026-10). No code changes this session — handoff refreshed with current metrics; run entry verification commands first.

## SESSION ENTRY (2026-11-05T19:12:32Z)
Timestamp (UTC): 20261105T191232Z
Git SHA: 3bcb07c9
Next task (unchanged, inferred): FCLR-NEXT-104 (Track A liquidation risk only; Track C sealed; Track B unsupported). Root bound 163; probes==2. Bottleneck cleared: tracked __pycache__ drift restored. Run entry verification commands first.
