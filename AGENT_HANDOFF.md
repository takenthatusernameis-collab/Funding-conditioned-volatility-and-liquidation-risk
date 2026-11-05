# AGENT_HANDOFF.md (SINGLE DURABLE HANDOFF)
Timestamp (UTC): 20261105T162400Z
Git SHA (HEAD, baseline): 46de9af8 (last commit; working tree modified by 101+102 hardening — uncommitted)
Branch: main
Repo: Funding-conditioned-volatility-and-liquidation-risk
Handoff ID: FCLR-HANDOFF-20261105T162400Z | Priority: P0 - REPO-NAME PRIORITIZED + HEAVY WORK MANDATORY | Mode: CAMPAIGN-DRIVEN | Enforcement: NO-SKIP | Bottleneck-State: HARDENED-102/GATE-DRIFT-PREFLIGHT-BUNDLED+MONITOR-RUNTIME-INVARIANT-ROOT-AT-BOUND

## REPO-NAME PRIORITIZATION (INFERRED)
Repository name: "Funding-conditioned-volatility-and-liquidation-risk"
- Funding-conditioned VOLATILITY component = Track C (FCLR-011) — **SEALED/LOCKED**. Forecast gate PASSED. DO NOT retune/re-run sealed cells/conflate.
- LIQUIDATION RISK component = Track A (FCLR-010) — **ONLY UNFINISHED HALF**. BLOCKED on admissible unauthenticated liquidation data (Hyperliquid-only, `data_through=2026-10`; 2026-11..2027-02 absent). Track B = **NOT_SUPPORTED**.
- BOTH components core to repo identity. NO SCOPE DRIFT TO SEALED TRACKS.

## CURRENT VERIFIED STATE (20261105T162400Z)
- Tests: `python -m unittest discover tests` — **303 tests, OK** (+11 from 102). MUST remain green.
- Resume check (CLI): `python scripts/tracka_resume_check.py` — `pass:true`, **15 checks**, `<5s`, `network:false`, `writes_real_research_state:false`. Includes wired drift invariants (fail-closed/read-only).
- CLI resume gate (102 bundled): `scripts/tracka_resume_gate.py` — drift preflight runs **BEFORE** manifest/prereg decision (fail-closed; cannot be misread as GO-ready). JSON exposes `drift_preflight`. Preserves strict-manifest/prereg/compat/outcome-isolation semantics. `--skip-drift-preflight` only for controlled tmp-isolated tests (default off). Real-repo `--prereg /nonexistent` => BLOCKED with `drift_preflight.pass:true`.
- Monitor (102 runtime assert): `monitor_ironflow_liquidations.py --quick` enforces `assert_probe_invariant()` post-consolidation (fail-safe; records `probe_invariant_runtime`); no blocked-path behavior/network regression.
- Track C: SEALED/LOCKED. Track B: NOT_SUPPORTED.
- Track A: ON-TRIGGER/MONITOR ONLY. Latest blocker: `research_state/liquidation_forward_validate_021_blocker_20261105T162400Z.md`. Latest sweep: `research_state/campaign_sweep_tracka_20261105T162400Z.md`. Latest probe: `research_state/ironflow_probe_20261105T162945Z.json` — **NO RESUME TRIGGER** (`data_through=2026-10`, 2026-11..2027-02 absent; head_probes=8 cached_hits=0; baseline_drift intact; probe_diff 0/0/0). Deep review/hunt canonical latest refreshed (cache), no admissible strict GO source.
- Artifact state (verified): root `research_state/*.md+*.json` = **163** (099/101 invariant bound <=163 — **AT BOUND**; 103 must consolidate unreferenced artifacts with provenance before adding new evidence). Ironflow probes = **2** (`ironflow_probe_20261105T162945Z.json` + `ironflow_probe_digest_latest.json`). Canonical alt outputs only. No new recurring timestamped probe/scan families in root. Watch `trigger_harden` live=1 (`trigger_harden_20261104T113550Z.json`), non_20261104T=0. No root trigger_harden files.
- **NO COASTING.** Status-only output without measurable hardening delta is noncompliant.

## SINGLE INITIAL TASK MESSAGE FOR NEXT AGENTIC SESSION (COPY/PASTE VERBATIM)
```text
TASK ID: FCLR-NEXT-103-TRACK-A-NO-COAST-ROOT-BOUND-CONSOLIDATION-GATE-REASONCODES-MONITOR-EVIDENCE-FIELD-PROOF
PRIORITY: P0 - REPO-NAME PRIORITIZED (Volatility SEALED/LOCKED; Liquidation Risk = ONLY ACTIVE OBJECTIVE)
TIMESTAMP (UTC): 20261105T162400Z
CAMPAIGN: TRACK A LIQUIDATION RISK - IMPOSSIBLE-TO-COAST WHILE BLOCKED. MEASURABLE DELTA REQUIRED. ZERO CHURN. INSTANT IRREFUTABLE RESUME.
ENFORCEMENT: ALL STEPS MANDATORY. SESSION FAILS IF ONLY REPORTS/PROBES OR IF IT REPEATS 102 WITHOUT EXTENDING IT. PREREGISTER BEFORE INSPECTING OUTCOMES IF TRIGGERED. NO IDLE TURNS. NO STATUS-ONLY OUTPUT. NO NEW TIMESTAMPED PROBE/SWEEP/SCAN FAMILIES. NO SCHEDULERS/POLLERS/STATUS FILES/REPEATED WRAPPERS/AGENT-CONTROLLERS. NO WORKFLOW CHANGES.
OBJECTIVE (INFERRED): Complete liquidation-risk half of "Funding-conditioned-volatility-and-liquidation-risk". Data blocked (Hyperliquid data_through 2026-10; 2026-11.. absent). 102 bundled drift preflight into tracka_resume_gate (fail-closed before manifest/prereg, drift_preflight JSON, <5s/no-network/no-real-writes, strict/prereg/compat preserved) and added monitor runtime assert_probe_invariant quick-path post-condition; 303 tests green. ROOT MD+JSON IS AT BOUND (163==163) — 103 MUST create measurable hardening delta: (A) Consolidate >=2 unreferenced superseded blocker/sweep artifacts with sha256/bytes/excerpt provenance into tracka_bottleneck_history (verify unreferenced by AGENT_HANDOFF/frontier) to regain root slack BEFORE writing 103 evidence; keep probes==2, no recurring families. (B) Add machine-stable gate reason codes / fail-closed ordering proof in JSON+tests (e.g. drift_fail_before_prereg_fail vs prereg_fail_after_drift_pass) without changing semantics. (C) Add deterministic tmp-only proof that monitor quick-path evidence includes probe_invariant_runtime (mocked quick execution path or extracted helper used by quick path) — no network regression. (D) Exhaustive trigger probes; update frontier/handoff with full before/after metrics and NEW stricter timestamped task FCLR-NEXT-104 naming exact uncovered gaps. PREREGISTER BEFORE INSPECTING OUTCOMES IF TRIGGERED.
CONSTRAINTS: No credentials/manual files/.github/workflows changes. Leakage-safe, preregister-before-outcomes. Track C/B locked/unsupported. Raw data/caches out of git. Clean-clone reproducible. Hyperliquid-only for Track A. Never conflate observed/modeled liquidations. No threshold-shopping. Canonical outputs only. Do NOT add root md+json files if it breaks the <=163 invariant — consolidate with provenance first.
MANDATORY EXECUTION (ALL REQUIRED; CONCRETE METRICS):
1) ENTRY VERIFY: `python -m unittest discover tests` (>=303 green). `python scripts/tracka_resume_check.py`. `monitor --quick`, `deep_review`, `hunt`. Record exact root md+json, probes, tests, watch counts. If NO NEW DATA, continue to hardening.
2) ROOT-BOUND CONSOLIDATION (MEASURABLE, BEFORE EVIDENCE WRITES): identify >=2 unreferenced superseded blocker/sweep root files (verify not referenced by AGENT_HANDOFF.md or experiment_frontier.json); move/merge with provenance (sha256/bytes/excerpts) into research_state/tracka_bottleneck_history_090.md section; delete originals; confirm root count reduced and probes==2 unchanged.
3) GATE REASON-CODE/ORDER HARDENING (MEASURABLE): JSON includes stable reason_code or equivalent ordering marker for drift_preflight failure vs prereg failure path; deterministic tmp-only tests prove fail-closed order and preserved semantics.
4) MONITOR EVIDENCE-FIELD PROOF (MEASURABLE): deterministic tmp-only test proves probe_invariant_runtime appears in quick-path evidence structure (no network; mock/extracted helper).
5) EVIDENCE, FRONTIER, HANDOFF (MANDATORY, WITHIN BOUND): Write 022 blocker + sweep ONLY if root <=163 after consolidation; otherwise record in frontier/handoff/history with preserved metrics. Update `research_state/experiment_frontier.json`. Update `AGENT_HANDOFF.md` with NEW stricter timestamped task FCLR-NEXT-104. PREREG BEFORE OUTCOMES IF TRIGGERED.
RESUME CONDITION (only): ironflow `data/events/YYYY-MM.parquet` or `data/fills/YYYY-MM.parquet` month>=2026-11 HTTP 200 unauthenticated OR admissible unauthenticated Hyperliquid source passes strict full-manifest GO gate (`assess_strict_manifest`/harness default). Hyperliquid-only. PREREGISTER BEFORE INSPECTING OUTCOMES.
STOP RULE: Complete ALL steps with concrete metrics. Track C locked. Track B unsupported. No conflation. No workflow/scheduler/poller/status-only/repeated wrappers/agent-controllers/new recurring families. Blocked/no-data claims without measurable hardening delta are noncompliant. Keep root md+json <=163 and probes==2. Leave state STRICTER than found.
```

## VERIFICATION COMMANDS (RUN ON ENTRY)
- `python -m unittest discover tests` (must be >=303, green)
- `python scripts/tracka_resume_check.py` (must pass, <5s, wired drift invariants)
- `python scripts/tracka_resume_gate.py --prereg /nonexistent` (must show `drift_preflight.pass:true` on clean repo)
- `python scripts/monitor_ironflow_liquidations.py --quick`
- `python scripts/deep_review_alt_sources.py`
- `python scripts/hunt_alternative_liquidation_sources.py`

## NEXT TASK (TIMESTAMPED)
20261105T162400Z: Execute FCLR-NEXT-103. Volatility (Track C) SEALED/LOCKED. Liquidation Risk (Track A) = ONLY ACTIVE OBJECTIVE. 102 bundled drift preflight into `tracka_resume_gate.py` (fail-closed before manifest/prereg, `drift_preflight` JSON, strict/prereg/compat/outcome-isolation preserved) and added `monitor.assert_probe_invariant()` runtime post-condition in quick path; 303 tests green. **Root md+json at bound (163)** — 103 must consolidate >=2 unreferenced superseded blocker/sweep artifacts with provenance before adding evidence, add machine-stable gate reason-code/order tests, and prove monitor quick evidence contains `probe_invariant_runtime` (tmp-only/no-network). Latest probe 20261105T161729Z shows **NO TRIGGER** (`data_through=2026-10`; 2026-11..2027-02 absent). PREREG BEFORE OUTCOMES if triggered.
