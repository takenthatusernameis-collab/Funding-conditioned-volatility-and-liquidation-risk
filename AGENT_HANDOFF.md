# AGENT_HANDOFF.md (SINGLE DURABLE HANDOFF) — READ THIS FILE FIRST
Timestamp (UTC): 2026-11-06T15:54:39Z
Handoff ID: FCLR-HANDOFF-20261106T155439Z
Baseline (prior): FCLR-NEXT-134 COMPLETE (20261106T155000Z; 687->692 OK). **This session (2026-11-06T15:54Z): FCLR-NEXT-135 VERIFIED COMPLETE** — full regression `python -m unittest discover tests` = **692 OK, 0 failures, 0 errors** (`Ran 692 tests in 53.146s`). Contract-lock phase 2 re-verified on all 3 Track A CLIs. Drift preflight `pass:true` (17/17 checks), `network:false`, `writes_real_research_state:false`, `elapsed_s`~0.39. No trigger. No `.github/workflows` changes. No new timestamped probe/sweep/scan/wrapper/report families.
Branch: main | Repo: Funding-conditioned-volatility-and-liquidation-risk
Priority: P0 — REPO-NAME PRIORITIZED (Track A liquidation risk is the ONLY active objective) | Mode: CAMPAIGN-DRIVEN | Enforcement: NO-SKIP/NO-COAST

## INITIAL TASK FOR NEXT AGENTIC SESSION (SINGLE, TIMESTAMPED, MANDATORY) — 2026-11-06T15:54:39Z
**Execute FCLR-NEXT-136.** ONLY active objective. **Heavy working required:** measurable hardening+lockdown when no trigger appears. Blocked/no-data claims without measurable hardening delta are noncompliant. No status-only loops. No re-probe absent months. No sealed Track C/B mutation.

TASK ID: FCLR-NEXT-136-TRACK-A-TRIGGER-READINESS+CONTRACT-INTEGRITY-HARDEN
PRIORITY: P0 — LIQUIDATION RISK (Track A) is the ONLY unfinished/active repo objective. Track A is DATA_BLOCKED: no admissible Hyperliquid liquidation trigger (`data_through=2026-10`; 2026-11..2027-02 absent; probes==2; do not re-probe). Track B NOT_SUPPORTED. Track C sealed/locked.
TIMESTAMP (UTC): 2026-11-06T15:54:39Z
ENFORCEMENT: ALL STEPS MANDATORY. NO STATUS-ONLY OUTPUT. NO NEW TIMESTAMPED PROBE/SWEEP/SCAN/WRAPPER/REPORT FAMILIES IN RESEARCH_STATE UNLESS STRICTLY ADMISSIBLE TRIGGER APPEARS (THEN: PREREG BEFORE INSPECTING OUTCOMES; blocker/prereg+result evidence only, ROOT BOUND PRESERVED). NO SCHEDULERS/POLLERS/STATUS FILES/REPEATED WRAPPERS/AGENT-CONTROLLERS. NO `.github/workflows` CHANGES. NO RE-IRONFLOW-PROBE OF ABSENT MONTHS. Hyperliquid-only. NEVER conflate observed vs modeled. No threshold-shopping. Track C/B locked/unsupported.

### MANDATORY DELIVERABLES (ALL REQUIRED)
1. **Clean-clone regression preserved:** `pip install -r requirements.txt` then `python -m unittest discover tests` must run **692 OK, 0 failures, 0 errors** from a fresh clone — no missing-import bottlenecks.
2. **Trigger-readiness hardening (heavy work):** strengthen the admissible-trigger -> prereg -> outcome-inspection seam so an admissible candidate cannot advance without: (a) prereg present/valid, (b) admissible-manifest GO from `src.analysis.tracka_admissible` seam, (c) `outcomes_inspected:false` on any refusal/block, (d) no parquet/outcome reads before prereg, (e) canonical outputs byte-identical on refusal. Add/extend tests that exercise a **synthetic admissible tmp manifest** (no network, no real research_state writes) and prove GO-seam + missing/invalid prereg => BLOCKED with stable `reason_code`/`fail_closed_order`/`outcomes_inspected:false`/`reads_outcomes:false`/`reads_parquet:false` across gate/check/operator paths.
3. **CLI contract integrity preserved:** all three Track A CLIs (`tracka_resume_gate.py`, `tracka_resume_check.py`, `tracka_operator_report.py`) must refuse argparse contract violations and malformed inputs as parseable JSON (stdout) with stable fields (`reason_code`, `reason_code_detail`/detail where applicable, `fail_closed_order`, `outcomes_inspected:false`, `canonical_outputs_mutated:false`, `reads_parquet:false`, `reads_outcomes:false`, `network:false`, `writes_real_research_state:false`), exit!=0, `--help` exit 0. No tracebacks-as-contract.
4. **Canonical-output integrity:** `research_state/experiment_frontier.json`, `research_state/run_manifest.json`, `research_state/evaluation_summary_FCLR010.md` byte-identical before/after refusal/blocked paths exercised (argparse, bad output-dir, malformed manifest/prereg, missing prereg). Any mutation = BLOCKED.
5. **Drift/state invariants on real repo:** re-verify `python scripts/tracka_resume_check.py` => `pass:true` (17/17 checks), `network:false`, `writes_real_research_state:false`; root `research_state/*.md+*.json` <=163; probes==2 (`ironflow_probe_digest_latest.json` + `ironflow_probe_20261105T200406Z.json`); no new timestamped probe/sweep/scan/wrapper/report families; no root trigger_harden files.
6. **Evidence record:** exact commands, exit codes, pass/fail counts, and any uncovered issue in this file; commit nothing unless asked.

### CURRENT VERIFIED STATE (exit 2026-11-06T15:54:39Z)
- **Trigger:** NO TRIGGER. `data_through=2026-10`; 2026-11..2027-02 absent. Probes==2. **Do not re-probe.**
- **Resume check:** `{"pass":true,"network":false,"writes_real_research_state":false,"elapsed_s":~0.387}` (17/17 checks).
- **Gate (`--prereg /nonexistent --json`):** BLOCKED, `drift_preflight.pass:true`, `reason_code:PREREG_OR_MANIFEST_BLOCK_AFTER_DRIFT_PASS`, `fail_closed_order:drift_preflight->manifest_prereg`, `outcomes_inspected:false`, `reads_parquet:false`, `reads_outcomes:false`, exit 1.
- **Argparse contract-lock (re-verified):** `tracka_resume_gate.py --bogus --json`, `tracka_resume_check.py --bogus`, `tracka_operator_report.py --bogus --json`, `tracka_operator_report.py --output-dir /nonexistent/zzz --json` => parseable JSON stdout, exit!=0 (2), `reason_code:PREREG_OR_MANIFEST_BLOCK_AFTER_DRIFT_PASS`, `reason_code_detail:ARGPARSE_CONTRACT_VIOLATION_FAIL_CLOSED`, `canonical_outputs_mutated:false`, `outcomes_inspected:false`, no tracebacks-as-contract. `--help` exits 0 on all 3.
- **Canonical-output integrity:** frontier/run_manifest/eval_FCLR010 byte-identical after argparse-refusal commands (IDENTICAL True).
- **Regression:** **692 OK, 0 failures, 0 errors** (`python -m unittest discover tests`, 53.146s). `requirements.txt` (numpy, pandas, scipy) present.
- **Artifacts:** root `research_state/*.md+*.json`=143 (<=163 bound), probes=2, no new timestamped probe/sweep/scan/wrapper/report families. No `.github/workflows` changes. `git status` shows pre-existing modified pyc/cache artifacts from local test execution (untracked/dirty state not created by this session's source edits; commit nothing unless asked).

## FCLR-NEXT-135 DELIVERABLES (VERIFIED COMPLETE)
| Gap | Deliverable | Status | Evidence |
|---|---|---|---|
| 135-1 | Clean-clone regression 692 OK, 0 failures, 0 errors | COMPLETE | `python -m unittest discover tests` => `Ran 692 tests in 53.146s`, `OK` |
| 135-2 | Argparse contract-lock across 3 Track A CLIs (JSON refusal stdout, exit!=0, `--help` 0, stable fields) | COMPLETE | gate/check/operator bogus + operator bad `--output-dir` => JSON with `ARGPARSE_CONTRACT_VIOLATION_FAIL_CLOSED`, `canonical_outputs_mutated:false` |
| 135-3 | Canonical-output integrity on refusal | COMPLETE | SHA256 identical for `experiment_frontier.json`, `run_manifest.json`, `evaluation_summary_FCLR010.md` after refusal commands |
| 135-4 | Drift preflight real repo 17/17 pass | COMPLETE | `tracka_resume_check.py` => `pass:true`, 17 checks, `network:false`, `writes_real_research_state:false` |
| 135-5 | State bounds/invariants | COMPLETE | root md+json 143 (<=163), probes 2, no new timestamped families, no workflow changes |

## BOTTLENECKS REMOVED / STILL HARD
- **Removed (134/135 verified):** argparse contract violations refuse as parseable JSON on all 3 CLIs; `canonical_outputs_mutated` parity present; regression 692 OK stable; clean-clone `requirements.txt` present.
- **Hard:** post-2026-10 admissible Hyperliquid Track A liquidation data absent. Only strictly admissible trigger permits prereg->inspect path (prereg BEFORE outcomes, root bound preserved).

## STOP RULE
Complete ALL steps with concrete metrics. Track C locked. Track B unsupported. No conflation. No workflow/scheduler/poller/status-only/repeated wrappers/agent-controllers/new recurring families. Blocked/no-data claims without measurable hardening delta are noncompliant. Keep root md+json <=163 and probes==2. Leave state STRICTER than found.
