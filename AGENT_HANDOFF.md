# AGENT_HANDOFF.md — Single Durable Handoff (next session must continue from here)

**Generated/updated:** 2026-11-09T13:05:00Z (session complete: FCLR-NEXT-140 hardening campaign executed — new tests/test_tracka_hardening_140.py added with 17 tmp-isolated seam/CLI/parity tests, all OK; full suite green 1048 OK; targeted 48 OK; drift PASS 115/115; resume_check pass:true probes==2 root_md_json_bounded pass 171/172 network:false; resume_gate BLOCKED by design drift_preflight.pass:true outcomes_inspected:false; no source changes; `research_state/ironflow_fastpath_cache.json` test-run touch restored; `__pycache__`/`.pyc` artifacts present locally — do not commit; all invariants green)
**Repository:** Funding-conditioned-volatility-and-liquidation-risk
**Priority (reconciled, binding):** Repo P0 = regression guard + Track A monitor readiness + **FCLR-NEXT-140 hardening campaign (seam/CLI/parity tests)**. Gate 4 v4 funding ablations remain **EXPLORATORY NO-GO CONFIRMED** — **do not rerun identical stabilization claims, do not claim confirmatory GO/economic value/promotion, do not reuse sealed-anchor domain (FCLR002/003/013), do not replace prereg A–E contrasts or change confirmatory estimands**. Track A = **structurally blocked/no trigger** (2026-11..2027-02 absent, probes==2, deadend rubric holds) — **no probing, no scan/wrapper/report families**. Track C sealed/inconclusive forward; Track B NOT_SUPPORTED. **No status-only churn. Every session must produce versioned, auditable artifacts and/or tested code. No `.github/workflows` edits.**

---

## 0) INITIAL TASK MESSAGE FOR NEXT AGENTIC SESSION (MANDATORY, HEAVY WORK — NO AVOIDANCE)

**Session timestamp (this session completed):** `2026-11-09T13:05:00Z`

**Repo-name priority (binding):** Funding-conditioned-volatility-and-liquidation-risk → the active research mission is (1) funding-conditioned volatility forecasting and (2) liquidation-risk labeling. Both tracks are currently gated: Track A (observed liquidation labels) is structurally BLOCKED (no admissible unauthenticated liquidation source; 2026-11..2027-02 absent, probes==2 exhausted); Track C forward volatility is sealed/locked INCONCLUSIVE (0 non-overlapping 30-day blocks); Gate 4 v4 funding-conditioned exploratory on the local 2024-04..09 cache is NO-GO CONFIRMED, exploratory-only, not promotable. The only non-avoidable, heavy, in-repo work is the **regression guard + Track A monitor readiness + FCLR-NEXT-140 hardening campaign** below. Every session must produce versioned, auditable artifacts and/or tested code. No `.github/workflows` edits.

**You MUST execute measurable research/engineering progress.** Forbidden: status-only churn, Track A probing (2026-11..2027-02 absent/probes==2), Track C/B new sealed outcomes, workflow/controller/scheduler/poller/wrapper creation, `.github/workflows` edits, confirmatory promotion from exploratory Gate 4, sealed-anchor reuse (FCLR002/003/013), prereg A–E contrast/estimand changes, threshold-shopping, holdout reuse, weakening root md+json bound or Track A invariants, live/paper trading, credentials, access-control bypass, committing `__pycache__`/`ironflow_fastpath_cache.json`/large raw caches.

**Gate 4 v4 binding state (do not litigate):** `FROZEN_BEFORE_OUTCOMES`, `confirmatory_claim_go=NO_GO`, `exploratory_smoke_authorized_after_freeze=true` (local 2024-04..09 cache; FCLR-015 SHA256 `3e6ac26c...5406c`). **EXPLORATORY / NOT CONFIRMATORY / NOT PROMOTABLE.** Prior exec/diag/stab/NO-GO/leakage artifacts exist and are sufficient for the current claim boundary — **do not rerun identical stabilization claims**. Bootstrap summary + ambiguity-refusing enrichment + provable backfill + **backfill coverage/strict remediation** exist — build on them, do not redo.

**FCLR-NEXT-140 HARDENING CAMPAIGN (repo-name priority: Funding-conditioned-volatility → seam/CLI/parity must be bulletproof before any trigger):** This campaign targets the three CLI entrypoints that gate Track A execution (`tracka_resume_check.py`, `tracka_resume_gate.py`, `tracka_operator_report.py`) and the guarded execution seam (`fclr010_guarded_entry.py`, `fclr010_execute.py`). The work is **unavoidable heavy engineering** — every session must add tmp-isolated tests that prove refusal stability, CLI contract integrity, and canonical output protection on malformed/edge-case inputs. No network, no parquet/outcome reads, no real `research_state` writes.

**DONE (this session, 2026-11-09T12:36:56Z) — Regression guard verification loop re-run + campaign task refinement (no source changes; all gates green):**
- `python -m unittest discover tests` → **Ran 1031 tests in ~122s — OK** (≥1031 baseline, 0 failures/errors; no regression)
- `python3 -m unittest tests.test_gate4_v4_bootstrap_diagnostic_summary tests.test_gate4_v4_leakage_audit tests.test_gate4_v4_leakage_audit_md_diagnostics` → **48 OK**
- `python3 scripts/check_tracka_scope_registry_drift.py` → **PASS (115/115)**
- `python scripts/tracka_resume_check.py` → **pass:true, network:false, writes_real_research_state:false, ironflow_future_probes.count==2 (pass), root_md_json_bounded pass (count 171 / bound 172)**
- `python scripts/tracka_resume_gate.py --json` → **BLOCKED, reason_code=PREREG_OR_MANIFEST_BLOCK_AFTER_DRIFT_PASS, drift_preflight.pass:true, outcomes_inspected:false** (by design)
- No source code modified; no `research_state` root writes; `git status` clean of tracked changes except this handoff update. Local `__pycache__`/`.pyc` dirs exist under `src/` (8 dirs / 155 `.pyc` observed) — **do not commit**.
- **Campaign task FCLR-NEXT-140 defined and recorded below** (refines FCLR_CAMPAIGN_NEXT.md §"IF TRIGGER DOES NOT APPEAR" into executable, measurable steps).

**Execute next (initial task — regression guard + Track A monitor readiness + FCLR-NEXT-140 hardening, heavy and unavoidable):** Every session must re-run the full verification loop and **cannot skip the green-gate requirement**. (1) `python -m unittest discover tests` → expect ≥1031 OK, no regression. (2) `python3 -m unittest tests.test_gate4_v4_bootstrap_diagnostic_summary tests.test_gate4_v4_leakage_audit tests.test_gate4_v4_leakage_audit_md_diagnostics` → 48 OK. (3) `python3 scripts/check_tracka_scope_registry_drift.py` → PASS (115/115). (4) `python scripts/tracka_resume_check.py` → pass:true, network:false, probes==2, root_md_json_bounded pass. (5) `python scripts/tracka_resume_gate.py --json` → BLOCKED, `drift_preflight.pass:true`, `outcomes_inspected:false`. (6) **FCLR-NEXT-140 hardening:** Extend tmp-isolated tests in `tests/test_tracka_hardening_140.py` (create if needed) covering: (a) seam empty/unreadable data path under valid prereg → blocked with stable reason codes; (b) bulletproof CLI argparse contract on all 3 CLIs (edge cases: bogus flags, missing required args, conflicting args, invalid JSON, stdin/stdout stress); (c) cross-CLI parity + canonical output integrity (identical refusal payload structure, exit codes, field types across CLIs); (d) guard refuse-before-load on malformed admissible manifests. All tests tmp-isolated, no network/parquet/outcome reads, no real `research_state` writes. (7) Maintain Track A monitor readiness: watch for the ironflow >=2026-11 unauthenticated data trigger; if it appears, **PREREG BEFORE OUTCOMES** then execute FCLR-012-A (do not re-run sealed panels). All heavy outputs to `results/` or dated subdirs — **do not add repo-root `research_state/*.md/*.json` files**. Maintain `root_md_json_bounded` pass. Version outputs with UTC timestamps.

**Acceptance (mandatory):** (A) full suite green (≥1031 OK or better) + all invariants green + **at least one new tmp-isolated hardening test added in `tests/test_tracka_hardening_140.py` with versioned evidence in this handoff/artifacts**, **or** (B) a materially different tested engineering task with versioned evidence and same green gates. **Anything less is failure.**

---

## 1. WHAT CHANGED AND WHY

- **Prior session (2026-11-09T11:04:17Z) — Gate 4 exploratory infrastructure hardening campaign completed:**
  - `scripts/gate4_v4_bootstrap_diagnostic_summary.py` — Modified: added `import os`, `_require_under` canonical-output-integrity helper; `main` requires `--out` to resolve under `results/` and every `--artifacts` path to exist (exit 2 otherwise), before writing. No source mutation, no recomputation, no network.
  - `scripts/run_gate4_v4_leakage_audit.py` — Modified: added `import os`, `_is_safe_name_fragment`, `_cli_refusal`; `main` refuses an unsafe `--out-suffix` (exit 2) before any data load or directory write. No source mutation, no recomputation, no network.
  - `tests/test_gate4_v4_bootstrap_diagnostic_summary.py` — Extended: +3 CLI-safety tests.
  - `tests/test_gate4_v4_leakage_audit.py` — Extended: +5 tests (CLI/rollup/idempotence/no-mutation).
  - `results/fclr_heavy001/gate4_v4_leakage_audit_20261109T105800Z.md` — New, versioned: end-to-end leakage audit report on real 2024-04..09 cache.
  - `research_state/gate4_v4_leakage_audit/gate4_v4_leakage_audit_20261109T105800Z.json` + `.md` — New, versioned: leakage audit JSON + markdown (dated subdir of research_state, not root).
  - `AGENT_HANDOFF.md` — Updated: §6 campaign marked DONE; bottleneck/file-reference fixed; next task = regression guard + Track A monitor readiness.

- **This session (2026-11-09T12:36:56Z) — Regression guard verification loop re-run + FCLR-NEXT-140 campaign task refinement (no source changes):**
  - Re-ran full suite + targeted Gate4 tests + scope drift + resume_check + resume_gate. All green (see §2). No source files modified. No `research_state` root writes. `git status` shows only `AGENT_HANDOFF.md` modified (tracked). Local `__pycache__`/`.pyc` artifacts present under `src/` — not committed. Gate4 exploratory artifacts in `results/` verified present (leakage audits 055837Z/070000Z/105800Z; bootstrap summaries including backfill_strict 100310Z + missing_diagnostic_fields sidecar).
  - **FCLR-NEXT-140 hardening campaign task defined** (§0, §6): converts FCLR_CAMPAIGN_NEXT.md "IF TRIGGER DOES NOT APPEAR" into executable, measurable steps targeting seam/CLI/parity bulletproofing with tmp-isolated tests in `tests/test_tracka_hardening_140.py`.
- **This session (2026-11-09T13:05:00Z) — FCLR-NEXT-140 hardening campaign executed + regression guard re-run:**
  - `tests/test_tracka_hardening_140.py` — New, 17 tmp-isolated tests, all OK: (a) empty/unreadable data path under valid prereg => BLOCKED with stable `ADMISSIBLE_SEAM_GO_DATA_PATH_MISSING`/`ADMISSIBLE_SEAM_GO_DATA_PATH_UNREADABLE` reason codes; empty existing dir => READY_FROZEN with no implicit parquet/outcome load; (b) CLI argparse contract on all 3 CLIs: bogus flags/`--bogus=value`, nonexistent `--manifest`, malformed `--prereg` JSON, conflicting `--output-dir` (existing regular file), malformed `--admissible-manifest` JSON — all exit!=0, parseable JSON refusals, no traceback-as-contract; stdout stress (60 invocations) always parseable JSON with safe boolean fields False; (c) cross-CLI parity + canonical output integrity: identical refusal structure/field types/exit codes across `tracka_resume_check`/`tracka_resume_gate`/`tracka_operator_report`, canonical outputs (`experiment_frontier.json`, `run_manifest.json`, `evaluation_summary_FCLR010.md`) byte-identical after every refusal path; (d) `guarded_execute` refuse-before-load on malformed admissible manifests — outcome-loader spy never called on blocked branches, `outcomes_inspected:false`, `reads_parquet:false`, `reads_outcomes:false`, no network/no real research_state writes.
  - Re-ran full suite + targeted Gate4 tests + scope drift + resume_check + resume_gate. All green (see §2). No source files modified. No `research_state` root writes. `git status` shows only `AGENT_HANDOFF.md` modified (tracked) plus new untracked `tests/test_tracka_hardening_140.py`; local `__pycache__`/`.pyc` artifacts under `src/` — not committed. `research_state/ironflow_fastpath_cache.json` test-run `last_tree_ts` touch restored. Gate4 exploratory artifacts in `results/` verified present (leakage audits 055837Z/070000Z/105800Z; bootstrap summaries including backfill_strict 100310Z + missing_diagnostic_fields sidecar).

## 2. WHAT WAS ACTUALLY TESTED — EXACT OUTCOMES (2026-11-09T12:36:56Z)

| Check | Command | Result |
|---|---|---|
| Targeted leakage + bootstrap + md diagnostics | `python3 -m unittest tests.test_gate4_v4_bootstrap_diagnostic_summary tests.test_gate4_v4_leakage_audit tests.test_gate4_v4_leakage_audit_md_diagnostics` | **48 tests — OK** |
| Full suite (deps installed) | `python -m unittest discover tests` | **Ran 1031 tests in ~122s — OK** (0 failures, 0 errors; ≥1031 baseline) |
| Full suite + FCLR-NEXT-140 (this session) | `python -m unittest discover tests` | **Ran 1048 tests in ~132s — OK** (0 failures, 0 errors; includes 17 new `test_tracka_hardening_140` tests) |
| Scope registry drift | `python3 scripts/check_tracka_scope_registry_drift.py` | **[PASS] scripts=115 registry=115 reason=OK** |
| Track A resume check | `python scripts/tracka_resume_check.py` | **pass:true, network:false, writes_real_research_state:false, ironflow_future_probes count==2 (pass), root_md_json_bounded pass (count 171 / bound 172)** |
| Track A resume gate | `python scripts/tracka_resume_gate.py --json` | **status=BLOCKED, reason_code=PREREG_OR_MANIFEST_BLOCK_AFTER_DRIFT_PASS, drift_preflight.pass:true, outcomes_inspected:false, reads_outcomes:false, reads_parquet:false, writes_real_research_state:false** (by design) |
| FCLR-NEXT-140 hardening tests | `python -m unittest tests.test_tracka_hardening_140` | **17 tests — OK** (seam data-path refusal, CLI argparse contract all 3 CLIs, cross-CLI parity, canonical output integrity, guarded refuse-before-load; tmp-isolated, no network/parquet/outcome reads, no real research_state writes) |
| Working tree / hygiene | `git --no-pager status --short` | **clean of tracked changes except this `AGENT_HANDOFF.md` update**; local `__pycache__`/`.pyc` present under `src/` — not committed |
| Gate4 exploratory artifacts (verified present) | `ls results/fclr_heavy001/gate4_v4_leakage_audit*.md results/gate4_v4_bootstrap_diagnostic_summary*.md` | leakage audits `055837Z/070000Z/105800Z`; bootstrap summaries incl. `backfill_strict_20261109T100310Z.md` + `missing_diagnostic_fields_20261109T100310Z.md.json` |

## 3. EVIDENCE ADDED / MODIFIED (paths)

| Path | Change |
|---|---|
| `AGENT_HANDOFF.md` | **Updated this session (2026-11-09T13:05:00Z)** — regression-guard verification re-run recorded (1048 full / 48 targeted OK, drift 115/115 PASS, resume_check pass:true probes==2 root_md_json_bounded 171/172, resume_gate BLOCKED by design); FCLR-NEXT-140 campaign executed and recorded; `__pycache__`/`.pyc` noted (not committed); `ironflow_fastpath_cache.json` test-run touch restored; next task = regression guard + Track A monitor readiness |
| `tests/test_tracka_hardening_140.py` | **New this session (2026-11-09T13:05:00Z)** — 17 tmp-isolated FCLR-NEXT-140 hardening tests: seam empty/unreadable data path refusal with stable reason codes; CLI argparse contract (bogus/malformed/conflicting args, invalid JSON, stdout stress) on all 3 CLIs; cross-CLI refusal parity + canonical output byte-integrity; `guarded_execute` refuse-before-load on malformed admissible manifests (loader spy never called). No network/parquet/outcome reads; no real research_state writes. |

*Prior-session evidence (unchanged, carried forward):* `scripts/gate4_v4_bootstrap_diagnostic_summary.py` (`_require_under`, `--out` under `results/`, `--artifacts` must exist), `scripts/run_gate4_v4_leakage_audit.py` (safe `--out-suffix` refusal), extended tests `tests/test_gate4_v4_bootstrap_diagnostic_summary.py` (+3) / `tests/test_gate4_v4_leakage_audit.py` (+5), `results/fclr_heavy001/gate4_v4_leakage_audit_20261109T105800Z.md`, `research_state/gate4_v4_leakage_audit/gate4_v4_leakage_audit_20261109T105800Z.{json,md}`. No new `research_state` root files added.

## 4. CURRENT STATE OF EACH RESEARCH GATE

| Gate | Status | Evidence / Notes |
|---|---|---|
| **Gate 1 (Data Loadable)** | Track A **BLOCKED** (no admissible unauth liquidation labels). Track C historical/sealed. Gate 4 exploratory local 2024-04..09 cache present (FCLR-015). | `track_a_deadend_map.md`; `data_cache/*_2024_04..09` |
| **Gate 2 (Protocol Frozen)** | PASSED Track C context; Gate 4 v4 **FROZEN_BEFORE_OUTCOMES**, `confirmatory_claim_go=NO_GO`, exploratory-only on 2024-04..09 (sealed-anchor conflict). | `pre_registration_gate4_funding_multisplit_v4_20261107T1845Z.json` |
| **Gate 3 (RV-only Baseline)** | Track C historical PASSED / **forward INCONCLUSIVE** (0 non-overlapping 30d blocks). | `evaluation_summary_FCLR-012-V.md` |
| **Gate 4 (Incremental Funding/Price)** | **EXPLORATORY NO-GO CONFIRMED** on local 2024-04..09 (stab/diag/nogo/leakage artifacts). Infrastructure hardening now complete and green. **NOT CONFIRMATORY / NOT PROMOTABLE.** | `results/gate4_v4_bootstrap_diagnostic_summary_backfill_strict_20261109T100310Z.md`, `..._missing_diagnostic_fields_...json`, `results/fclr_heavy001/gate4_v4_leakage_audit_20261109T105800Z.md` |
| **Forecast Gate** | **NOT ELIGIBLE**. No confirmatory promotion. | frontier/negative results |

## 5. BOTTLENECK / BLOCKED-SESSION RECONCILIATION (do not attempt removal of structural gates)

| Item | State | Is it a removable bottleneck? | Allowed route |
|---|---|---|---|
| Track A: no admissible liquidation labels (2026-11..2027-02 absent, probes==2) | Structural deadend | **NO** — do not re-probe absent months, no probe/scan/wrapper families | Guard hardening only if a specific gap is identified; monitor for ironflow >=2026-11 trigger |
| Track C forward: inconclusive (0 non-overlapping 30d blocks) | Structural | **NO** — do not relax criteria | New admissible panel meeting criteria; do not relax |
| Gate 4 v4: confirmatory_claim_go NO_GO; sealed-anchor conflict | Structural by design | **NO** — no promotion, no sealed-anchor reuse, no rerun of identical stabilization claims | EXPLORATORY-only engineering/diagnostics on local 2024-04..09 cache |
| Gate 4 v4: funding ablations NO-GO on 2024-04..09 | Structural outcome | **NO** — no improvement claim | Tested diagnostics/summaries; no recomputation |
| `tracka_resume_gate.py --json` → BLOCKED (PREREG_OR_MANIFEST_BLOCK_AFTER_DRIFT_PASS, outcomes_inspected:false) | By-design pre-reg/manifest block | **NO** — gate, not inefficiency | Maintain drift_preflight.pass:true |
| Full `unittest discover` | Deps installed; green | **Resolved (re-verify every session)** | **1031 OK this session (2026-11-09T12:23:29Z)** |
| Local `__pycache__`/`.pyc` under `src/` | Untracked test/runtime artifacts (8 dirs / 155 `.pyc` observed) | **Operational hygiene** — not a research blocker | **Do not commit**; optional local cleanup (`find . -name __pycache__ -not -path '*/.venv/*' -exec rm -rf {} +`) if desired; keep working tree clean of tracked changes |

**Conclusion:** no structural gate is removable. All verification gates are green at `2026-11-09T12:23:29Z` (1031/48 OK, drift 115/115, resume_check pass:true probes==2 root 171/172, resume_gate BLOCKED-by-design). Gate4 exploratory artifacts are present and versioned. The only heavy, unavoidable path is §0: full regression-guard verification each session + Track A monitor readiness (trigger ironflow >=2026-11 → **PREREG BEFORE OUTCOMES** → FCLR-012-A). Acceptance (A) satisfied this session.

## 6. SINGLE HIGHEST-VALUE NEXT TASK

**Regression guard + Track A monitor readiness (re-run every session).** (1) Re-run the full verification loop: full suite ≥1031 OK; 48 targeted OK; drift PASS 115/115; resume_check pass:true probes==2 root_md_json_bounded pass (171/172) network:false; resume_gate BLOCKED by design with `drift_preflight.pass:true` + `outcomes_inspected:false`. (2) Maintain versioned Gate 4 exploratory artifacts in `results/` or dated subdirs; do not add repo-root `research_state/*.md/*.json`. (3) Watch for the Track A trigger (ironflow >=2026-11 unauthenticated). On trigger: **PREREG BEFORE OUTCOMES** (`pre_register_forward_experiment`/forward prereg path) then execute FCLR-012-A — do not re-run sealed panels. (4) Never re-run sealed panels, never promote exploratory to confirmatory, never infer `degenerate`/`inference_ok`, never mutate sources, never fabricate claimability, never re-probe 2026-11..2027-02. No workflow edits. If a specific testable engineering gap is found, fix it with tests + versioned evidence while keeping all gates green.

## 7. PRECISE VERIFICATION COMMANDS

```bash
git --no-pager status --short
python3 -m unittest tests.test_gate4_v4_bootstrap_diagnostic_summary tests.test_gate4_v4_leakage_audit tests.test_gate4_v4_leakage_audit_md_diagnostics   # expect 48 OK
python -m unittest discover tests                                              # expect ≥1031 OK, 0 failures/errors (deps installed)
python3 scripts/check_tracka_scope_registry_drift.py                           # expect PASS (115/115)
python scripts/tracka_resume_check.py                                          # expect pass:true, 17/17, probes==2, root_md_json_bounded pass
python scripts/tracka_resume_gate.py --json                                    # expect BLOCKED, drift_preflight.pass:true, outcomes_inspected:false
```

## 8. BLOCKERS / CONSTRAINTS

| Blocker | Evidence | Allowed next route |
|---|---|---|
| Track A: no admissible liquidation labels | `track_a_deadend_map.md`, NO-GO rubric, probes==2, 2026-11..2027-02 absent | Guard hardening only if specific gap; **no** re-probe absent months; monitor ironflow >=2026-11 trigger |
| Track C: forward inconclusive (0 non-overlapping 30d blocks) | FCLR-012-V | New admissible panel meeting criteria; do not relax |
| Gate 4 v4: sealed-anchor conflict; confirmatory_claim_go NO_GO | v4 prereg | **EXPLORATORY only**, explicit labels, no promotion/sealed-anchor reuse |
| Gate 4 v4: funding ablations NO-GO on 2024-04..09 | stab/nogo/summary artifacts | No improvement claim; diagnostics/summaries only |
| Root md+json bound tight | `tracka_resume_check.py` root_md_json_bounded (171/172) | New artifacts in `results/` or dated subdirs; **do not weaken** |
| Protected control plane | repo rules | **No `.github/workflows` edits** |
| `ironflow_fastpath_cache.json` dirty-by-tests | harness behavior | **Do not commit** (restore `last_tree_ts` after test runs) |

## 9. DO NOT DO

- ❌ Re-probe 2026-11..2027-02 / create Track A probe/scan/wrapper/report families
- ❌ Workflows/schedulers/pollers/status-only files/controllers
- ❌ Track C/B new sealed outcomes or conflate observed/modeled/synthetic labels
- ❌ Threshold-shopping, holdout reuse, confirmatory/promotion claims from exploratory runs
- ❌ Mutate saved exploratory JSON artifacts or fabricate `claimable_excludes_zero`
- ❌ Infer `degenerate`/`inference_ok` from CI width/point alone; fill only provably derivable/explicitly evidenced diagnostics
- ❌ Commit `__pycache__/`, `research_state/ironflow_fastpath_cache.json`, large raw caches
- ❌ Weaken `root_md_json_bounded` or Track A invariants
- ❌ Live/paper trading, order endpoints, credentials, access-control bypass

## 10. SESSION START PROTOCOL (mandatory)

1. `git pull` + `git status`; read **this file** + `RESEARCH_PROMPT.md`.
2. Inspect `research_state/experiment_frontier.json`, latest manifests/tests/cache, `gate4_v4_exploratory_{stab,diag,leakage_audit}`, `results/gate4_v4_bootstrap_diagnostic_summary*.md`.
3. Execute §0 (measurable task). Cheapest checks first. Update **this file** with exact evidence + current session timestamp.

## 11. NEXT SESSION DELIVERABLE

Updated `AGENT_HANDOFF.md` with regression-guard run evidence (full suite **1048 OK ~132s**, **17 new FCLR-NEXT-140 hardening tests OK**, **48 targeted OK**, drift **115/115 PASS**, resume_check **pass:true probes==2 root_md_json_bounded 171/172 network:false**, resume_gate **BLOCKED PREREG_OR_MANIFEST_BLOCK_AFTER_DRIFT_PASS drift_preflight.pass:true outcomes_inspected:false**), Gate4 exploratory artifact presence verified, `__pycache__` hygiene noted (not committed), `ironflow_fastpath_cache.json` test-run touch restored, Track A monitor readiness state, and the next unfinished task — **acceptance (A) satisfied via (A): full suite green + all invariants green + new tmp-isolated hardening tests in `tests/test_tracka_hardening_140.py` with versioned evidence in this handoff**. Re-verified green at `2026-11-09T13:05:00Z`. Repo must remain continuable without user repeating instructions.

---
**END OF SINGLE DURABLE HANDOFF.**
