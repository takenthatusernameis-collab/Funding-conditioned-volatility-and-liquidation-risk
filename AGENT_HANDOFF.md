# AGENT_HANDOFF.md (SINGLE DURABLE HANDOFF) — READ THIS FILE FIRST
Timestamp (UTC): 2026-11-06T16:57:11Z
Handoff ID: FCLR-HANDOFF-20261106T165711Z
Baseline (prior): FCLR-NEXT-136 COMPLETE (heavy trigger-readiness + contract-integrity hardening). Full regression `python -m unittest discover tests` = **703 OK, 0 failures, 0 errors** (`Ran 703 tests in 56.791s`; +11 tests vs 692). Synthetic admissible GO-seam + missing/invalid prereg proven BLOCKED with stable fields across harness/gate/check/operator + CLIs. Argparse contract-lock preserved on all 3 Track A CLIs. Drift preflight `pass:true` (17/17 checks), `network:false`, `writes_real_research_state:false`. No trigger. No `.github/workflows` changes. No new timestamped probe/sweep/scan/wrapper/report families.
Branch: main | Repo: Funding-conditioned-volatility-and-liquidation-risk
Priority: P0 — REPO-NAME PRIORITIZED (Track A liquidation risk is the ONLY active objective) | Mode: CAMPAIGN-DRIVEN | Enforcement: NO-SKIP/NO-COAST

## INITIAL TASK FOR NEXT AGENTIC SESSION (SINGLE, TIMESTAMPED, MANDATORY) — 2026-11-06T16:57:11Z
**Execute FCLR-NEXT-137.** ONLY active objective. **Heavy working required:** measurable hardening+lockdown when no trigger appears. Blocked/no-data claims without measurable hardening delta are noncompliant. No status-only loops. No re-probe absent months. No sealed Track C/B mutation.

TASK ID: FCLR-NEXT-137-TRACK-A-TRIGGER-READINESS+CONTRACT-INTEGRITY-HARDEN
PRIORITY: P0 — LIQUIDATION RISK (Track A) is the ONLY unfinished/active repo objective. Track A is DATA_BLOCKED: no admissible Hyperliquid liquidation trigger (`data_through=2026-10`; 2026-11..2027-02 absent; probes==2; do not re-probe). Track B NOT_SUPPORTED. Track C sealed/locked.
TIMESTAMP (UTC): 2026-11-06T16:57:11Z
ENFORCEMENT: ALL STEPS MANDATORY. NO STATUS-ONLY OUTPUT. NO NEW TIMESTAMPED PROBE/SWEEP/SCAN/WRAPPER/REPORT FAMILIES IN RESEARCH_STATE UNLESS STRICTLY ADMISSIBLE TRIGGER APPEARS (THEN: PREREG BEFORE INSPECTING OUTCOMES; blocker/prereg+result evidence only, ROOT BOUND PRESERVED). NO SCHEDULERS/POLLERS/STATUS FILES/REPEATED WRAPPERS/AGENT-CONTROLLERS. NO `.github/workflows` CHANGES. NO RE-IRONFLOW-PROBE OF ABSENT MONTHS. Hyperliquid-only. NEVER conflate observed vs modeled. No threshold-shopping. Track C/B locked/unsupported.

### MANDATORY DELIVERABLES (ALL REQUIRED)
1. **Clean-clone regression preserved:** `pip install -r requirements.txt` then `python -m unittest discover tests` must run **703 OK, 0 failures, 0 errors** (or higher only via legitimate new hardening tests) from a fresh clone — no missing-import bottlenecks.
2. **Trigger-readiness hardening (heavy work):** extend synthetic admissible-seam coverage (tmp manifests only, no network, no real research_state writes) for additional fail-closed edges across gate/check/operator/harness: GO seam + valid prereg present + data path missing/nonexistent must remain BLOCKED with stable `PREREG_OR_MANIFEST_BLOCK_AFTER_DRIFT_PASS` + `ADMISSIBLE_SEAM_GO_DATA_PATH_MISSING` / `seam_go_data_missing` parity and `outcomes_inspected:false`/`reads_outcomes:false`/`reads_parquet:false`; malformed admissible-manifest JSON via `--admissible-manifest` on gate/operator/check must remain stable fail-closed JSON refusals with no tracebacks-as-contract. Add/extend tests that assert **canonical outputs byte-identical** on every refusal path exercised.
3. **CLI contract integrity preserved:** all three Track A CLIs (`tracka_resume_gate.py`, `tracka_resume_check.py`, `tracka_operator_report.py`) must refuse argparse contract violations and malformed inputs as parseable JSON (stdout) with stable fields (`reason_code`, `reason_code_detail` where applicable, `fail_closed_order`, `outcomes_inspected:false`, `canonical_outputs_mutated:false`, `reads_parquet:false`, `reads_outcomes:false`, `network:false`, `writes_real_research_state:false`), exit!=0, `--help` exit 0. No tracebacks-as-contract.
4. **Canonical-output integrity:** `research_state/experiment_frontier.json`, `research_state/run_manifest.json`, `research_state/evaluation_summary_FCLR010.md` byte-identical before/after refusal/blocked paths exercised. Any mutation = BLOCKED.
5. **Drift/state invariants on real repo:** re-verify `python scripts/tracka_resume_check.py` => `pass:true` (17/17 checks), `network:false`, `writes_real_research_state:false`; root `research_state/*.md+*.json` <=163; probes==2 (`ironflow_probe_digest_latest.json` + `ironflow_probe_20261105T200406Z.json`); no new timestamped probe/sweep/scan/wrapper/report families; no root trigger_harden files.
6. **Evidence record:** exact commands, exit codes, pass/fail counts, and any uncovered issue in this file; commit nothing unless asked.

### CURRENT VERIFIED STATE (exit 2026-11-06T16:57:11Z)
- **Trigger:** NO TRIGGER. `data_through=2026-10`; 2026-11..2027-02 absent. Probes==2. **Do not re-probe.**
- **Resume check:** `python scripts/tracka_resume_check.py` => `{"pass":true,"network":false,"writes_real_research_state":false}` (17/17 checks), exit 0.
- **Regression:** `python -m unittest discover tests` => **Ran 703 tests in 56.791s, OK** (0 failures, 0 errors). Clean-clone deps: `requirements.txt` present (`numpy>=1.24.0`, `pandas>=2.0.0`, `scipy>=1.10.0`). **+11 tests** from FCLR-NEXT-136 hardening.
- **Argparse contract-lock (re-verified, 3 CLIs):** `tracka_resume_gate.py --bogus --json` (stderr usage + stdout JSON), `tracka_resume_check.py --bogus`, `tracka_operator_report.py --bogus --json` => parseable JSON refusal stdout, exit 1, `reason_code:PREREG_OR_MANIFEST_BLOCK_AFTER_DRIFT_PASS`, `reason_code_detail:ARGPARSE_CONTRACT_VIOLATION_FAIL_CLOSED`, `canonical_outputs_mutated:false`, `outcomes_inspected:false`, `reads_outcomes:false`, `reads_parquet:false`, `network:false`, `writes_real_research_state:false`, no tracebacks-as-contract. `--help` exits 0 (existing behavior).
- **Synthetic admissible GO seam + missing prereg (tmp manifest, no network, no real research_state writes):** gate/operator/harness => BLOCKED, `reason_code:PREREG_OR_MANIFEST_BLOCK_AFTER_DRIFT_PASS`, `reason_code_detail:ADMISSIBLE_SEAM_GO_PREREG_REQUIRED`, `seam_go_prereg_required:true`, `fail_closed_order:drift_preflight->admissible_seam->manifest_prereg` (gate/operator), `admissible_seam_wired.pass:true`, `outcomes_inspected:false`, `reads_outcomes:false`, `reads_parquet:false`, `network:false`, `writes_real_research_state:false`. **check CLI (focused seam, 127 G1)** `--admissible-manifest <tmp GO>` => rc 0, `pass:true`, `status:GO`, `reason_code:ADMISSIBLE_SEAM_GO`, `fail_closed_order:drift_preflight->admissible_seam`, seam fields stable (`month:2026-11`, `fail_closed:true`, `reads_*:false`, `network:false`).
- **Synthetic GO seam + invalid/malformed prereg (harness + gate):** BLOCKED, `reason_code:PREREG_OR_MANIFEST_BLOCK_AFTER_DRIFT_PASS`, `reason_code_detail:PREREG_CONTENT_INVALID_FAIL_CLOSED`, `fail_closed_order:drift_preflight->admissible_seam->manifest_prereg` (gate), `admissible_seam_wired.pass:true`, `outcomes_inspected:false`, `reads_outcomes:false`, `reads_parquet:false`, loader never invoked.
- **Synthetic GO seam + missing/broken candidate (check CLI):** broken JSON => rc 1, `pass:false`, `status:NO-GO`, `reason_code:ADMISSIBLE_CANDIDATE_LOAD_ERROR`, seam `fail_closed:true`, `reads_*:false`; missing path => `ADMISSIBLE_CANDIDATE_PATH_MISSING`.
- **Canonical-output integrity:** SHA256 identical before/after all exercised refusal paths for `experiment_frontier.json=57fb9a3e03f6f6b4ccd9eb1e7a7f159a74597494a3b0f59aad6834658245a114`, `run_manifest.json=05c1cdeb5e102aa5a999560af444fea0d7f255c714b57028201f802190ece9f5`, `evaluation_summary_FCLR010.md=8b7773b2d7eff3663be4fa975e75095c5406f27c5bcf096988935fad0871a334`.
- **Artifacts:** root `research_state/*.md+*.json`=143 (<=163 bound), probes=2 (`ironflow_probe_20261105T200406Z.json` + `ironflow_probe_digest_latest.json`), no new timestamped probe/sweep/scan/wrapper/report families. No root trigger_harden files. No `.github/workflows` changes.
- **Untracked source added (test only):** `tests/test_tracka_hardening_136.py` (+11 tests). **Modified (pre-existing/local churn, not canonical):** `research_state/ironflow_fastpath_cache.json` timestamp-only drift from test/tool runs; pyc `__pycache__`/test `__pycache__` modified by local execution. Commit nothing unless asked.

## FCLR-NEXT-136 DELIVERABLES (COMPLETE — 2026-11-06T16:57:11Z)
| Gap | Deliverable | Status | Evidence |
|---|---|---|---|
| 136-1 | Clean-clone regression preserved (>=692 -> 703 OK) | COMPLETE | `python -m unittest discover tests` => `Ran 703 tests in 56.791s`, `OK` (0 failures, 0 errors) |
| 136-2 | Synthetic admissible GO seam + missing prereg => BLOCKED stable fields (harness/gate/operator/check, tmp manifest, no network, no real research_state writes) | COMPLETE | `tests.test_tracka_hardening_136` 11 tests OK. gate/operator/harness: `PREREG_OR_MANIFEST_BLOCK_AFTER_DRIFT_PASS` + `ADMISSIBLE_SEAM_GO_PREREG_REQUIRED` + `seam_go_prereg_required:true` + `fail_closed_order:drift_preflight->admissible_seam->manifest_prereg` + `admissible_seam_wired.pass:true` + `outcomes_inspected:false, reads_outcomes:false, reads_parquet:false, network:false, writes_real_research_state:false`; check CLI: GO rc0 with stable seam fields/month/fail_closed; loader never invoked |
| 136-3 | Synthetic GO seam + invalid/malformed prereg => BLOCKED stable (harness/gate) | COMPLETE | `PREREG_OR_MANIFEST_BLOCK_AFTER_DRIFT_PASS` + `PREREG_CONTENT_INVALID_FAIL_CLOSED`, `fail_closed_order` preserved, `admissible_seam_wired.pass:true`, no outcome/parquet reads |
| 136-4 | Missing/broken admissible candidate fail-closed stable (check CLI) | COMPLETE | broken JSON => rc1 `NO-GO/ADMISSIBLE_CANDIDATE_LOAD_ERROR`, seam `fail_closed:true`; missing => `ADMISSIBLE_CANDIDATE_PATH_MISSING` |
| 136-5 | Argparse contract-lock preserved (3 Track A CLIs) | COMPLETE | gate/check/operator `--bogus` => parseable JSON, exit1, `ARGPARSE_CONTRACT_VIOLATION_FAIL_CLOSED`, `canonical_outputs_mutated:false`, no tracebacks-as-contract |
| 136-6 | Canonical-output integrity | COMPLETE | SHA256 identical after all refusal/synthetic exercises for frontier/run_manifest/eval_FCLR010 |
| 136-7 | Drift/state invariants 17/17 pass, bounds/probes/writes | COMPLETE | `tracka_resume_check.py` => `pass:true` (17/17), root md+json 143 (<=163), probes==2, no new timestamped families, no workflows, no root trigger_harden |

## FCLR-NEXT-135 DELIVERABLES (VERIFIED COMPLETE)
| Gap | Deliverable | Status | Evidence |
|---|---|---|---|
| 135-1 | Clean-clone regression 692 OK, 0 failures, 0 errors | COMPLETE | `python -m unittest discover tests` => `Ran 692 tests in 53.146s`, `OK` |
| 135-2 | Argparse contract-lock across 3 Track A CLIs (JSON refusal stdout, exit!=0, `--help` 0, stable fields) | COMPLETE | gate/check/operator bogus + operator bad `--output-dir` => JSON with `ARGPARSE_CONTRACT_VIOLATION_FAIL_CLOSED`, `canonical_outputs_mutated:false` |
| 135-3 | Canonical-output integrity on refusal | COMPLETE | SHA256 identical for `experiment_frontier.json`, `run_manifest.json`, `evaluation_summary_FCLR010.md` after refusal commands |
| 135-4 | Drift preflight real repo 17/17 pass | COMPLETE | `tracka_resume_check.py` => `pass:true`, 17 checks, `network:false`, `writes_real_research_state:false` |
| 135-5 | State bounds/invariants | COMPLETE | root md+json 143 (<=163), probes 2, no new timestamped families, no workflow changes |

## BOTTLENECKS REMOVED / STILL HARD
- **Removed (136 verified):** synthetic admissible GO-seam + missing/invalid prereg proven BLOCKED with stable contract fields across harness/gate/check/operator; check CLI missing/broken candidate fail-closed; canonical outputs proven byte-identical after refusal exercises; regression 703 OK; argparse contract-lock preserved.
- **Still hard:** post-2026-10 admissible Hyperliquid Track A liquidation data absent. Only strictly admissible trigger permits prereg->inspect path (prereg BEFORE outcomes, root bound preserved). `ironflow_fastpath_cache.json` may drift timestamp on local runs (non-canonical cache; not a research_state root md/json bound artifact beyond its existing file).

## STOP RULE
Complete ALL steps with concrete metrics. Track C locked. Track B unsupported. No conflation. No workflow/scheduler/poller/status-only/repeated wrappers/agent-controllers/new recurring families. Blocked/no-data claims without measurable hardening delta are noncompliant. Keep root md+json <=163 and probes==2. Leave state STRICTER than found.


## FCLR-NEXT-137 DELIVERABLES (COMPLETE — 2026-11-06T19:07:00Z)
| Gap | Deliverable | Status | Evidence |
|---|---|---|---|
| 137-1 | Clean-clone regression preserved (>=703 -> 709 OK) | COMPLETE | `python -m unittest discover tests` => `Ran 709 tests in 87.096s`, `OK` (0 failures, 0 errors). Added `tests/test_tracka_hardening_137.py` (+6 tests). |
| 137-2 | GO seam + valid prereg present + data path missing/nonexistent => BLOCKED stable fields (harness/gate); parity ADMISSIBLE_SEAM_GO_DATA_PATH_MISSING / seam_go_data_missing, no IO | COMPLETE | Harness/gate: `PREREG_OR_MANIFEST_BLOCK_AFTER_DRIFT_PASS` + `ADMISSIBLE_SEAM_GO_DATA_PATH_MISSING` + `seam_go_data_missing:true` + `fail_closed_order:drift_preflight->admissible_seam->manifest_prereg` + `admissible_seam_wired.pass:true` + `outcomes_inspected:false, reads_outcomes:false, reads_parquet:false, network:false, writes_real_research_state:false, canonical_outputs_mutated:false`. Gate passes admissible manifest dict/path to harness for precise reason_code_detail parity. |
| 137-3 | Malformed admissible-manifest JSON via --admissible-manifest on gate/operator/check => stable fail-closed JSON refusals, no tracebacks-as-contract | COMPLETE | gate/check/operator with broken JSON produce parseable JSON refusals, exit!=0, `network:false`, `writes_real_research_state:false`, `outcomes_inspected:false`, `reads_parquet:false`, `reads_outcomes:false`, `canonical_outputs_mutated:false`; no traceback contract leakage. |
| 137-4 | CLI contract integrity preserved (3 Track A CLIs) | COMPLETE | `tracka_resume_gate.py --bogus --json` => parseable JSON refusal with `ARGPARSE_CONTRACT_VIOLATION_FAIL_CLOSED`, exit 1, no tracebacks-as-contract. `--help` exit 0. |
| 137-5 | Canonical-output integrity | COMPLETE | SHA256 unchanged for `experiment_frontier.json`, `run_manifest.json`, `evaluation_summary_FCLR010.md` across all refusal/exercise paths in new tests. |
| 137-6 | Drift/state invariants 17/17 pass, bounds/probes/writes | COMPLETE | `tracka_resume_check.py` => `pass:true` (17/17 checks), root md+json 143 (<=163), probes==2, no new timestamped families, no workflow changes. |

## BOTTLENECKS REMOVED / STILL HARD (updated)
- **Removed (137 verified):** GO-seam + valid prereg + missing data path now proven BLOCKED with stable `ADMISSIBLE_SEAM_GO_DATA_PATH_MISSING`/`seam_go_data_missing` across harness/gate with full IO-invariant parity; malformed admissible-manifest JSON refusal paths hardened for gate/check/operator with no tracebacks-as-contract; regression 709 OK.
- **Still hard:** post-2026-10 admissible Hyperliquid Track A liquidation data absent. Only strictly admissible trigger permits prereg->inspect path. Root bound preserved (md+json<=163, probes==2). No workflow/scheduler/poller/status-only/repeated wrappers/agent-controllers/new recurring families.

## STOP RULE (unchanged)
Complete ALL steps with concrete metrics. Track C locked. Track B unsupported. No conflation. No workflow/scheduler/poller/status-only/repeated wrappers/agent-controllers/new recurring families. Blocked/no-data claims without measurable hardening delta are noncompliant. Keep root md+json <=163 and probes==2. Leave state STRICTER than found.
