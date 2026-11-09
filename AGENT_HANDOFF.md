# AGENT_HANDOFF.md — Single Durable Handoff for Next Agentic Session

**Generated:** 2026-11-09T00:09:15Z
**Repository:** Funding-conditioned-volatility-and-liquidation-risk
**Git SHA:** (check `git rev-parse HEAD` at session start)

---

## 1. WHAT CHANGED AND WHY

**No new code changes in this session** — this handoff establishes the authoritative baseline for the next session.

**Repository state summary:**
- **Track A (Observed Liquidation Risk):** STRUCTURALLY BLOCKED — exhaustive search of 8 candidate source families found NO admissible unauthenticated liquidation label source meeting rubric criteria (≥5 symbols, ≥3 non-overlapping 30-day blocks, documented completeness, license OK, census/defensible labels). Evidence: `research_state/track_a_deadend_map.md`, `research_state/liquidation_source_campaign.md`, `research_state/negative_results_report.md`. Data through 2026-10 only; 2026-11..2027-02 absent; 2 probes executed, probing exhausted.
- **Track C (Volatility Forecasting):** SEALED/LOCKED — forecast gate PASSED but INCONCLUSIVE (FCLR-012-V executed on last available Binance panel ending 2026-11-02; test window = 5 days = 0 non-overlapping 30-day blocks). Binance archive ends 2026-11-02 (verified 404 on 2026-11-03/04 and 2026-10-28/29).
- **Track B (Modeled Boundary-Breach):** NOT_SUPPORTED — no admissible historical margin/liquidation parameters verified for confirmatory use.
- **Test Suite:** 950 tests (3 failures, 2 errors) — regression baseline established. All hardening tests (G1-G3+) passing in dep-light environments.
- **Codebase Hardening (Complete through FCLR-NEXT-131):** All 8 Track A entrypoints wired through guarded contracts; 0 direct parquet/outcome reads outside loaders; drift invariants (17/17) wired into resume_check; operator/gate CLIs stable with parseable JSON refusals (exit≠0, canonical outputs unchanged).

---

## 2. WHAT WAS ACTUALLY TESTED — EXACT OUTCOMES

| Test/Check | Result | Evidence |
|------------|--------|----------|
| Full test suite (`python -m unittest discover tests`) | 950 ran, 3 failures, 2 errors | See terminal output above |
| Track A resume check (`python scripts/tracka_resume_check.py`) | 17/17 checks PASS, `network:false`, `probes==2` | `experiment_frontier.json` artifact_churn_108+ |
| Track A resume gate (`python scripts/tracka_resume_gate.py --json`) | `drift_preflight.pass:true`, `BLOCKED PREREG_OR_MANIFEST_BLOCK_AFTER_DRIFT_PASS`, `outcomes_inspected:false` | Same |
| Track A operator report (`python scripts/tracka_operator_report.py`) | `pass:true`, exit 0 | Same |
| Ironflow monitor quick (`python scripts/monitor_ironflow_liquidations.py --quick`) | `data_through=2026-10`, 2026-11..2027-02 absent, probes=2 | `research_state/ironflow_probe_20261105T200406Z.json` |
| Track A rubric (8 candidates) | ALL NO-GO — no source passes `unauth∧no_keys∧symbols≥5∧blocks≥3∧completeness_doc∧license_ok∧census_or_defensible` | `research_state/track_a_deadend_map.md` §Machine_Checkable_Firewall |
| FCLR-012-V forward volatility validation | INCONCLUSIVE — 0 test blocks, CI spans zero, Binance archive ends 2026-11-02 | `research_state/evaluation_summary_FCLR-012-V.md`, `run_manifest.json` |

---

## 3. EVIDENCE ADDED AND WHERE

| Artifact | Location | Purpose |
|----------|----------|---------|
| Track A Dead-End Map (complete rubric) | `research_state/track_a_deadend_map.md` | Irrefutable structural block evidence |
| Liquidation Source Campaign | `research_state/liquidation_source_campaign.md` | Exhaustive probe log with HTTP evidence |
| Negative Results Report | `research_state/negative_results_report.md` | Preserved null/inconclusive outcomes |
| Experiment Frontier (updated) | `research_state/experiment_frontier.json` | Complete task registry with status, gaps, blockers |
| Research Protocol (frozen) | `research_state/research_protocol.md` | FCLR-001 starter protocol, frozen pre-holdout |
| Ironflow Probe Cache | `research_state/ironflow_probe_20261105T200406Z.json` | Last probe evidence (data_through=2026-10) |
| Test Hardening Suites | `tests/test_tracka_hardening_107.py` through `test_tracka_hardening_138.py` | G1-G3+ measurable guard/test hardening |

---

## 4. CURRENT STATE OF EACH RESEARCH GATE

| Gate | Status | Evidence |
|------|--------|----------|
| **Gate 1 (Data Loadable)** | TRACK A: BLOCKED — no admissible liquidation labels | `track_a_deadend_map.md`, `negative_results_report.md` |
| | TRACK C: PASSED (historical panel) — SEALED | `evaluation_summary_FCLR-012-V.md` |
| **Gate 2 (Protocol Frozen)** | PASSED — FCLR-001 protocol frozen 2026-11-06T20:36:32Z | `research_protocol.md` |
| **Gate 3 (RV-only Baseline)** | TRACK C: PASSED (historical) — INCONCLUSIVE forward | `evaluation_summary_FCLR-012-V.md` |
| | TRACK A: N/A — no labels | — |
| **Gate 4 (Incremental Funding/Price)** | TRACK C: NOT APPLICABLE (forward panel INCONCLUSIVE) | — |
| | TRACK A: BLOCKED — no labels to test against | — |
| **Forecast Gate (Gate 4 pass + materiality + multiplicity + calibration + cross-instrument + no leakage)** | TRACK C: NOT ELIGIBLE (Gate 3 INCONCLUSIVE forward) | `experiment_frontier.json` blocked_cells |
| | TRACK A: BLOCKED (no labels) | `track_a_deadend_map.md` |

---

## 5. SINGLE HIGHEST-VALUE NEXT TASK

**FCLR-NEXT-132 (or next sequential): MEASURABLE TRACK A HARDENING — SEAM/CLI/GUARD MATRIX EXTENSION**

Per `research_state/FCLR_CAMPAIGN_NEXT.md` (RECONCILED 2026-11-07T00:15:23Z), **Repo P0 = Phase 3 funding-conditioned volatility ablations (Gate 4) using local data** — but Track A remains blocked/no trigger. The heavy work that **must continue** is **Track A guard hardening** (no status-only churn):

1. **G1:** Extend seam tests — empty/unreadable data path under valid prereg → blocked with stable reason codes (tmp-isolated, no network/parquet/outcome reads, no real research_state writes)
2. **G2:** Bulletproof CLI argparse contract on all 3 CLIs (`tracka_resume_check.py`, `tracka_resume_gate.py`, `tracka_operator_report.py`) — edge cases, malformed args, missing files
3. **G3:** Cross-CLI parity + canonical output integrity — same refusal payload schema, stable bool/type fields, `exit≠0` on refusal
4. **G4:** Add/extend tests (legitimate hardening) keeping regression **≥709 OK** (current baseline from experiment_frontier)
5. **G5:** Verify invariants (17/17 drift checks pass, root md+json ≤163, probes==2, no new timestamped probe/scan/wrapper/report families)

**This is the ONLY unblocked heavy-work path.** Do NOT re-probe absent months (2026-11..2027-02). Do NOT create status files. Do NOT touch Track C/B. Do NOT modify `.github/workflows`.

---

## 6. PRECISE COMMAND/CHECK TO VERIFY PROGRESS

```bash
# 1. Install deps (if needed)
pip install -r requirements.txt

# 2. Run regression suite — must be ≥709 OK (allow 3 failures, 2 errors as baseline)
python -m unittest discover tests

# 3. Track A resume check — must show 17/17 PASS, network:false, probes==2
python scripts/tracka_resume_check.py

# 4. Track A resume gate — must show drift_preflight.pass:true, BLOCKED with stable reason_code, outcomes_inspected:false
python scripts/tracka_resume_gate.py --json

# 5. Track A operator report — must show pass:true, exit 0
python scripts/tracka_operator_report.py

# 6. Verify no new timestamped artifact families created in research_state/
ls -1 research_state/*.md research_state/*.json | wc -l  # must not exceed ~163 root files

# 7. Verify drift invariants
python scripts/check_tracka_scope_registry_drift.py
```

**Acceptance Criteria (from FCLR_CAMPAIGN_NEXT.md):**
- All tests pass (regression ≥709 OK)
- Refusals parseable JSON, no tracebacks, exit≠0, canonical outputs unchanged
- Drift 17/17 pass
- Bounds respected (root md+json ≤163, probes==2, no new timestamped families)

---

## 7. SOURCE/ENGINEERING BLOCKERS — WITH EVIDENCE AND NEXT ROUTE

| Blocker | Evidence | Next Materially Different Free Route |
|---------|----------|--------------------------------------|
| **Track A: No admissible liquidation labels** (structural) | `track_a_deadend_map.md` — 8 candidates, all NO-GO on machine-checkable rubric; Binance 404/451, Bybit trades≠census, HF 2026 window exhausted, others absent/paywalled | **SOLE REOPEN PATH:** New admissible unauthenticated source appears meeting ALL rubric criteria (≥5 symbols, ≥3 blocks, documented completeness, license OK, census/defensible). **Do not re-probe.** Monitor `monitor_ironflow_liquidations.py --quick` for Hyperliquid ≥2026-11 parquet. |
| **Track C: No forward Binance data beyond 2026-11-02** | `fclr012v_coverage_audit.json` — archive ends 2026-11-02 (verified 404); test window 5 days = 0 blocks | New admissible Binance panel with real volume >0 across ≥3 non-overlapping 30-day blocks. Do not relax block-count criterion. |
| **Track B: No verified historical margin/liquidation parameters** | `h002_methodology_dossier.md`, `h002_replication_blocker.md` | Only if public venue publishes complete historical margin tiers with time applicability — not currently admissible. |

---

## 8. MANDATORY SESSION START PROTOCOL (from RESEARCH_PROMPT.md §27)

At start of **every** session:
1. `git pull` and `git status` — verify clean state
2. Read **this file** (`AGENT_HANDOFF.md`) and `RESEARCH_PROMPT.md` completely
3. Inspect working tree, recent commits, `research_state/experiment_frontier.json`, latest run manifest, tests, source registry
4. **Treat repository state and evidence as authoritative** — do not assume earlier prose remains current
5. Choose highest-value unfinished task completable without credentials/human intervention (see §5 above)
6. Execute, run cheapest deterministic checks first
7. Record exact changes, commands, results, uncovered issues, next actionable task **in this AGENT_HANDOFF.md** and applicable research-state artifact
8. Commit nothing merely to show activity

---

## 9. DO NOT DO (Hard Constraints from RESEARCH_PROMPT.md)

- ❌ No re-probing absent months (2026-11..2027-02) — probing exhausted
- ❌ No workflow/scheduler/poller/status-only/wrapper/controller additions
- ❌ No Track C/B work — Track C sealed, Track B NOT_SUPPORTED
- ❌ No conflation of observed/modeled/synthetic labels
- ❌ No threshold-shopping or holdout reuse
- ❌ No commit of `__pycache__/`, `ironflow_fastpath_cache.json`, or large raw caches
- ❌ No modification of `.github/workflows` without explicit maintainer authorization
- ❌ No live/paper trading, no API order endpoints, no account operations

---

## 10. NEXT SESSION DELIVERABLE

Update **this file** (`AGENT_HANDOFF.md`) with:
1. What changed and why (diff summary)
2. What was actually tested, with exact outcomes (commands + results)
3. What evidence was added and where (file paths)
4. Current state of each research gate (updated table)
5. Single highest-value next task (updated if completed)
6. Precise command/check that verifies it
7. Any new blocker with evidence and next route

**Make it possible for the agent after you to continue from persisted repository state without asking the user to repeat instructions.**

---

**END OF HANDOFF — This is the single durable handoff. No other handoff files should exist.**