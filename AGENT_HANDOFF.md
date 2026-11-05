# AGENT_HANDOFF.md (SINGLE DURABLE HANDOFF)
Timestamp (UTC): 20261105T160711Z
Git SHA (HEAD, baseline): 46de9af8 (last commit; working tree modified by 101 hardening — uncommitted)
Branch: main
Repo: Funding-conditioned-volatility-and-liquidation-risk
Handoff ID: FCLR-HANDOFF-20261105T160711Z | Priority: P0 - REPO-NAME PRIORITIZED + HEAVY WORK MANDATORY | Mode: CAMPAIGN-DRIVEN | Enforcement: NO-SKIP | Bottleneck-State: HARDENED-101/CLI-DRIFT-INVARIANTS-WIRED-GATE-UNBUNDLED

## REPO-NAME PRIORITIZATION (INFERRED)
Repository name: "Funding-conditioned-volatility-and-liquidation-risk"
- Funding-conditioned VOLATILITY component = Track C (FCLR-011) — **SEALED/LOCKED**. Forecast gate PASSED. DO NOT retune/re-run sealed cells/conflate.
- LIQUIDATION RISK component = Track A (FCLR-010) — **ONLY UNFINISHED HALF**. BLOCKED on admissible unauthenticated liquidation data (Hyperliquid-only, `data_through=2026-10`; 2026-11..2027-02 absent). Track B = **NOT_SUPPORTED**.
- BOTH components core to repo identity. NO SCOPE DRIFT TO SEALED TRACKS.

## CURRENT VERIFIED STATE (20261105T160711Z)
- Tests: `python -m unittest discover tests` — **292 tests, OK** (+16 from 101). MUST remain green.
- Resume check (CLI, 101 wired): `python scripts/tracka_resume_check.py` — `pass:true`, **15 checks**, `<5s`, `network:false`, `writes_real_research_state:false`. Now includes wired drift invariants (machine-checkable, fail-closed): `handoff_single_root`, `probe_count_exactly_two` (1 live + 1 canonical digest), `root_md_json_bounded` (<=163), `canonical_alt_outputs_only`, `no_recurring_timestamped_probe_scan_families`, `watch_trigger_harden_invariant` (live<=1, non_20261104T==0), `no_root_trigger_harden_files`.
- CLI resume gate: `scripts/tracka_resume_gate.py` exists — strict default refuses minimal-only manifest / missing prereg; compat `--compat-fixture` only; outcome-isolation proven. **101 gap closed in resume_check; 102 gap: gate decision path not yet bundled with the same drift-preflight as a single operator gate.**
- Track C: SEALED/LOCKED. Track B: NOT_SUPPORTED.
- Track A: ON-TRIGGER/MONITOR ONLY. Latest blocker: `research_state/liquidation_forward_validate_020_blocker_20261105T160711Z.md`. Latest sweep: `research_state/campaign_sweep_tracka_20261105T160711Z.md`. Latest probe: `research_state/ironflow_probe_20261105T160637Z.json` — **NO RESUME TRIGGER** (`data_through=2026-10`, 2026-11..2027-02 absent; head_probes=8 cached_hits=0; baseline_drift intact; probe_diff 0/0/0). Deep review/hunt canonical latest refreshed (cache), no admissible strict GO source.
- Artifact state (verified): root `research_state/*.md+*.json` = **161** (099/101 invariant bound <=163). Ironflow probes = **2** (`ironflow_probe_20261105T160637Z.json` + `ironflow_probe_digest_latest.json`). Canonical alt outputs only (`alt_source_scan_latest.json`, `alt_source_deep_review_latest.md`). No new recurring timestamped probe/scan families in root. Watch `trigger_harden` live=1 (`trigger_harden_20261104T113550Z.json`), non-20261104T=0. No root trigger_harden files. 101 consolidated 4 unreferenced old blocker/sweep files with sha256 provenance into `research_state/tracka_bottleneck_history_090.md#101`.
- **NO COASTING.** Status-only output without measurable hardening delta is noncompliant.

## SINGLE INITIAL TASK MESSAGE FOR NEXT AGENTIC SESSION (COPY/PASTE VERBATIM)
```text
TASK ID: FCLR-NEXT-102-TRACK-A-NO-COAST-WIRE-DRIFT-PREFLIGHT-INTO-RESUME-GATE-AND-RUNTIME-CONSOLIDATION-ASSERT
PRIORITY: P0 - REPO-NAME PRIORITIZED (Volatility SEALED/LOCKED; Liquidation Risk = ONLY ACTIVE OBJECTIVE)
TIMESTAMP (UTC): 20261105T160711Z
CAMPAIGN: TRACK A LIQUIDATION RISK - IMPOSSIBLE-TO-COAST WHILE BLOCKED. MEASURABLE DELTA REQUIRED. ZERO CHURN. INSTANT IRREFUTABLE RESUME.
ENFORCEMENT: ALL STEPS MANDATORY. SESSION FAILS IF ONLY REPORTS/PROBES OR IF IT REPEATS 101 WITHOUT EXTENDING IT. PREREGISTER BEFORE INSPECTING OUTCOMES IF TRIGGERED. NO IDLE TURNS. NO STATUS-ONLY OUTPUT. NO NEW TIMESTAMPED PROBE/SWEEP/SCAN FAMILIES. NO SCHEDULERS/POLLERS/STATUS FILES/REPEATED WRAPPERS/AGENT-CONTROLLERS. NO WORKFLOW CHANGES.
OBJECTIVE (INFERRED): Complete liquidation-risk half of "Funding-conditioned-volatility-and-liquidation-risk". Data blocked (Hyperliquid data_through 2026-10; 2026-11.. absent). 101 wired 099 drift invariants into `scripts/tracka_resume_check.py` (15 checks, PASS, 292 tests). While blocked produce measurable hardening delta: (A) keep root md+json <=163 and ironflow probes == 2; no new recurring timestamped families. (B) Bundle the same drift preflight into `scripts/tracka_resume_gate.py` (or a single `scripts/tracka_resume_preflight.py` invoked by gate) so operator decision path fails-closed on drift BEFORE manifest/prereg decision logic that could be misread as GO-ready state; preserve strict-manifest/prereg/compat/outcome-isolation semantics and existing tests. JSON must expose drift_preflight pass/fail; <5s, network:false, no real research_state writes. (C) Add runtime consolidation post-condition assertion in `monitor_ironflow_liquidations` quick path (or a small exported `assert_probe_invariant(evidence_dir)` used by monitor/tests) so post-`--quick` state cannot silently violate probe==2/digest==1 invariant; keep monitor behavior/network profile unchanged except the assertion/fail-safe. (D) Deterministic tmp-only tests for gate+drift bundling and runtime assertion. (E) Exhaustive trigger probes; update frontier/handoff with full before/after metrics and NEW stricter timestamped task FCLR-NEXT-103 naming exact uncovered gaps. PREREGISTER BEFORE INSPECTING OUTCOMES IF TRIGGERED.
CONSTRAINTS: No credentials/manual files/.github/workflows changes. Leakage-safe, preregister-before-outcomes. Track C/B locked/unsupported. Raw data/caches out of git. Clean-clone reproducible. Hyperliquid-only for Track A. Never conflate observed/modeled liquidations. No threshold-shopping. Canonical outputs only (`ironflow_probe_digest_latest.json` + 1 live probe; `alt_source_scan_latest.json`; `alt_source_deep_review_latest.md`).
MANDATORY EXECUTION (ALL REQUIRED; CONCRETE METRICS):
1) ENTRY VERIFY: `python -m unittest discover tests` (>=292 green). `python scripts/tracka_resume_check.py` (must pass incl wired drift checks). `monitor --quick`, `deep_review`, `hunt`. Record exact root md+json, probes, tests, watch counts. If NO NEW DATA, continue to hardening.
2) WIRE DRIFT PREFLIGHT INTO GATE/OPERATOR DECISION (MEASURABLE): deterministic tests; preserve strict/prereg/compat/outcome-isolation; JSON exposes drift_preflight; <5s/no-network/no-real-writes.
3) RUNTIME CONSOLIDATION POST-CONDITION ASSERT (MEASURABLE): monitor cannot leave probe invariant violated; tmp-isolated proof; no behavior/network regression for blocked path.
4) EVIDENCE, FRONTIER, HANDOFF (MANDATORY): Write `research_state/campaign_sweep_tracka_$(date -u +%Y%m%dT%H%M%SZ).md` and `research_state/liquidation_forward_validate_021_blocker_$(date -u +%Y%m%dT%H%M%SZ).md` ONLY if root md+json bound allows without breaking <=163 — if not, consolidate unreferenced artifacts first with provenance, or record in frontier/handoff/tracka_bottleneck_history with preserved metrics. Update `research_state/experiment_frontier.json`. Update `AGENT_HANDOFF.md` with NEW stricter timestamped task FCLR-NEXT-103. PREREG BEFORE OUTCOMES IF TRIGGERED.
RESUME CONDITION (only): ironflow `data/events/YYYY-MM.parquet` or `data/fills/YYYY-MM.parquet` month>=2026-11 HTTP 200 unauthenticated OR admissible unauthenticated Hyperliquid source passes strict full-manifest GO gate (`assess_strict_manifest`/harness default). Hyperliquid-only. PREREGISTER BEFORE INSPECTING OUTCOMES.
STOP RULE: Complete ALL steps with concrete metrics. Track C locked. Track B unsupported. No conflation. No workflow/scheduler/poller/status-only/repeated wrappers/agent-controllers/new recurring families. Blocked/no-data claims without measurable hardening delta are noncompliant. Do NOT add root md+json files if it breaks the <=163 invariant — consolidate with provenance instead. Leave state STRICTER than found.
```

## VERIFICATION COMMANDS (RUN ON ENTRY)
- `python -m unittest discover tests` (must be >=292, green)
- `python scripts/tracka_resume_check.py` (must print JSON with `"pass": true`, <5s, `network:false`, `writes_real_research_state:false`, includes wired drift-invariant checks)
- `python scripts/tracka_resume_gate.py --help` (CLI exists)
- `python scripts/monitor_ironflow_liquidations.py --quick`
- `python scripts/deep_review_alt_sources.py`
- `python scripts/hunt_alternative_liquidation_sources.py`

## NEXT TASK (TIMESTAMPED)
20261105T160711Z: Execute FCLR-NEXT-102. Volatility (Track C) SEALED/LOCKED. Liquidation Risk (Track A) = ONLY ACTIVE OBJECTIVE. 101 wired 099/100 drift invariants into `tracka_resume_check.py` operator CLI (15 checks, fail-closed/<5s/no-network/no-real-writes) with 16 deterministic tmp-only tests and consolidation regression guards; 292 tests green. Remaining bottlenecks: drift preflight not bundled into `tracka_resume_gate.py` operator decision path; monitor quick-path lacks runtime post-condition assertion for probe invariant (unittest-only). 102 must close both while keeping root md+json <=163 and probes==2. Latest probe 20261105T160637Z shows **NO TRIGGER** (`data_through=2026-10`; 2026-11..2027-02 absent). PREREG BEFORE OUTCOMES if triggered.
