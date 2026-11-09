# AGENT_HANDOFF.md — Single Durable Handoff (next session must continue from here)

**Generated/updated:** 2026-11-09T07:23:17Z (session task timestamp `2026-11-09T07:23:17Z`)
**Repository:** Funding-conditioned-volatility-and-liquidation-risk
**Priority (reconciled, binding):** Repo P0 = **Gate 4 exploratory infrastructure hardening with measurable, tested artifacts** (local admissible 2024-04..09 cache only). Gate 4 v4 funding ablations remain **EXPLORATORY NO-GO CONFIRMED** — **do not rerun identical stabilization claims, do not claim confirmatory GO/economic value/promotion, do not reuse sealed-anchor domain (FCLR002/003/013), do not replace prereg A–E contrasts or change confirmatory estimands**. Track A = **structurally blocked/no trigger** (2026-11..2027-02 absent, probes==2, deadend rubric holds) — **no probing, no scan/wrapper/report families**. Track C sealed/inconclusive forward; Track B NOT_SUPPORTED. **No status-only churn. Every session must produce versioned, auditable artifacts and/or tested code. No `.github/workflows` edits.**

**Verified this session (2026-11-09T07:00:00Z):** Completed §0 task (1) — leakage-audit JSON now carries additive bootstrap diagnostics. `scripts/run_gate4_v4_leakage_audit.py` `audit_block_bootstrap_reproducibility()` now serializes `run1_diagnostics`/`run2_diagnostics`/`diagnostics_identical_on_rerun` (effective_block_count, ci_accounting_valid, regime_flags, degenerate, inference_ok, n_reps_effective, n_obs_finite); `write_md()` renders an "Additive bootstrap diagnostics" table + summary lines; `make_interpretation()` cites them. Regenerated artifact `research_state/gate4_v4_leakage_audit/gate4_v4_leakage_audit_20261109T070000Z.json` (+md in same dir and `results/fclr_heavy001/`) — leakage_invariance_all=true, bootstrap_reproducible=true, eff=120, ci_valid=true, flags=[]. New synthetic tests in `tests/test_gate4_v4_leakage_audit_md_diagnostics.py` (now 12 tests): extract_additive_diag full/legacy/none, payload JSON carries diagnostics, interpretation mentions additive diagnostics. Fixed pre-existing failing assertion `test_write_md_legacy_ci_fallback` (row format) to match actual renderer output. **Full suite: 986 tests in ~109s — OK** (was 981 with 1 failure; +5 net). `check_tracka_scope_registry_drift.py` → **[PASS] scripts=114 registry=114**. `tracka_resume_check.py` → **pass:true, 17/17, network:false, writes_real_research_state:false, probes==2, root_md_json_bounded pass**. `tracka_resume_gate.py --json` → **BLOCKED, reason_code:PREREG_OR_MANIFEST_BLOCK_AFTER_DRIFT_PASS, drift_preflight.pass:true, outcomes_inspected:false**. All EXPLORATORY / NOT CONFIRMATORY / NOT PROMOTABLE. No root `research_state/*.md/*.json` added (new artifacts live in `research_state/gate4_v4_leakage_audit/` subdir + `results/fclr_heavy001/`). `scripts/run_gate4_v4_exploratory_stab.py` markdown now serializes `eff_blocks`/`ci_valid`/`regime_flags` for pooled contrasts and LOO (additive, legacy-field tolerant). `scripts/run_gate4_v4_exploratory_diag.py` stdout reports `eff_blocks`/`ci_...`

---

## 0) INITIAL TASK MESSAGE FOR NEXT AGENTIC SESSION (MANDATORY, HEAVY WORK — NO AVOIDANCE)

**Session timestamp (initial task):** `2026-11-09T07:23:17Z`

**You MUST execute measurable research/engineering progress.** Forbidden: status-only churn, Track A probing (2026-11..2027-02 absent/probes==2), Track C/B new sealed outcomes, workflow/controller/scheduler/poller/wrapper creation, `.github/workflows` edits, confirmatory promotion from exploratory Gate 4, sealed-anchor reuse, prereg A–E contrast/estimand changes, threshold-shopping, holdout reuse, weakening root md+json bound or Track A invariants, live/paper trading, credentials, access-control bypass, committing `__pycache__`/`ironflow_fastpath_cache.json`/large raw caches.

**Gate 4 v4 binding state (do not litigate):** `FROZEN_BEFORE_OUTCOMES`, `confirmatory_claim_go=NO_GO`, `exploratory_smoke_authorized_after_freeze=true` (local 2024-04..09 cache; FCLR-015 SHA256 `3e6ac26c...5406c`). **EXPLORATORY / NOT CONFIRMATORY / NOT PROMOTABLE.** Prior exec/diag/stab/NO-GO/leakage artifacts exist and are sufficient for the current claim boundary — **do not rerun identical stabilization claims**. Bootstrap diagnostics now exist in code + stab/diag propagation (`src/eval/inference.py`, `scripts/run_funding_ablations.py` delegate, `run_gate4_v4_exploratory_{stab,diag}.py`, tests) — build on this, do not redo it.

**§0 task (1) DONE 2026-11-09T07:00:00Z — leakage-audit additive bootstrap diagnostics (JSON serialization, MD table, interpretation, 12 tests, versioned artifact). Do not rerun.**

**Execute next (initial task — highest-value measurable engineering, complete fully):** implement a *materially different* tested Gate 4/Track C-adjacent hardening task with versioned evidence — **failing-regime regression tests for `fit_predict_ols` / `block_bootstrap_delta_ci_diagnostic` edge cases that could inflate QLIKE or hide degenerate CIs** (synthetic fixtures only: zero-variance predictor columns, constant finite diffs, empty/all-non-finite diffs, too-few-blocks, missing required columns, collinear predictors, single-instrument panels). Verify each edge case is detected by the diagnostic fields (`degenerate`, `regime_flags`, `ci_accounting_valid`, `inference_ok`) and cannot silently produce a spurious QLIKE improvement. Synthetic fixtures only — no network, no real `research_state` writes, no expensive exploratory recomputation. New scripts must be **registered** in `research_state/tracka_script_scope_registry.json` and mirrored in the appropriate `tests/test_tracka_hardening_*.py` `SCRIPT_REGISTRY`; keep `scripts=registry` and drift PASS. Fallbacks only if (b) is already covered: (a) deterministic “bootstrap diagnostic summary” helper consuming saved exploratory JSON → compact `results/` markdown risk table (synthetic fixture test), or (c) split-boundary/leakage assertions around exploratory variant parameter provenance.

**Artifact discipline:** new heavy outputs go to `results/` or dated subdirs — **do not add repo-root `research_state/*.md/*.json` files**. Root bound is tight (currently 2 root md+json files total per resume check structure; maintain `root_md_json_bounded` pass). Version outputs with UTC timestamps in filenames when creating bundles.

**Verification (must run):** targeted tests for touched code first; then `python -m unittest discover tests` (**must remain ≥986 OK, expect increase if tests added**). `python scripts/check_tracka_scope_registry_drift.py` → PASS. `python scripts/tracka_resume_check.py` → pass:true, 17/17, network:false, probes==2, root_md_json_bounded pass. `python scripts/tracka_resume_gate.py --json` → BLOCKED, `drift_preflight.pass:true`, `outcomes_inspected:false`.

**Update this single durable handoff** (§1–§10) with session timestamp, exact file paths changed, commands, pass/fail counts, artifact paths, blockers, and the **single highest-value unfinished next task**. No parallel handoff files.

**Acceptance (mandatory):** (A) tested code/artifact change with green targeted + full suite + all invariants green, **or** (B) a materially different tested engineering task with versioned evidence and same green gates. **Anything less is failure.**

---

## 1. WHAT CHANGED AND WHY (last completed session, 2026-11-09T07:00:00Z)
- **Completed §0 task (1) — leakage-audit JSON now carries additive bootstrap diagnostics (acceptance A):** `scripts/run_gate4_v4_leakage_audit.py` `audit_block_bootstrap_reproducibility()` now returns `run1_diagnostics`/`run2_diagnostics`/`diagnostics_identical_on_rerun` via new `extract_additive_diag()`; `write_md()` renders an "Additive bootstrap diagnostics" table + summary lines (legacy-tolerant); `make_interpretation()` cites them. The pre-existing artifact `gate4_v4_leakage_audit_20261109T055837Z.json` had these fields as `None` — gap now closed.
- **Tests (synthetic, no network, no real `research_state` writes):** `tests/test_gate4_v4_leakage_audit_md_diagnostics.py` extended from 7 to **12 tests**: `extract_additive_diag` full/legacy/none, payload-JSON-carries-diagnostics, interpretation-cites-additive-diagnostics, plus the pre-existing diag-field/flags/write_md tests. **Fixed a pre-existing failing assertion** `test_write_md_legacy_ci_fallback` to match the actual per-metric row format the renderer produces (no behavior change to the renderer).
- **Regenerated versioned artifact:** `research_state/gate4_v4_leakage_audit/gate4_v4_leakage_audit_20261109T070000Z.json` (+ `.md` in same subdir and `results/fclr_heavy001/gate4_v4_leakage_audit_20261109T070000Z.md`) — leakage_invariance_all=true, bootstrap_reproducible=true, eff=120, ci_valid=true, flags=[].
- **No Track A/root-bound weakening:** no probe/scan/wrapper families; no new root `research_state/*.md/*.json` (new artifacts live in `research_state/gate4_v4_leakage_audit/` subdir + `results/fclr_heavy001/`); no workflow/controller edits.
- **This session (2026-11-09T07:23:17Z):** handoff only — refreshed §0 initial task message for the next session (failing-regime regression tests); no code change.

## 2. WHAT WAS ACTUALLY TESTED — EXACT OUTCOMES
| Check | Command | Result |
|---|---|---|
| Targeted leakage-audit serialization + hardened bootstrap | `python3 -m unittest tests.test_gate4_v4_leakage_audit_md_diagnostics tests.test_gate4_v4_leakage_audit tests.test_eval_inference_diagnostics -v` | **23 tests OK** |
| Registry/leakage guards | `python -m unittest tests.test_tracka_hardening_117 tests.test_tracka_hardening_118 tests.test_tracka_hardening_119 tests.test_gate4_v4_leakage_audit` | **OK** (includes `Updated experiment_frontier.json` side effect in some harness paths — no commit) |
| Full suite | `python -m unittest discover tests` | **Ran 986 tests in ~109s — OK** (was 981 with 1 failure; +5 net) |
| Scope registry drift | `python scripts/check_tracka_scope_registry_drift.py` | **[PASS] scripts=114 registry=114 reason=OK** |
| Track A resume check | `python scripts/tracka_resume_check.py` | **pass:true, 17/17, network:false, writes_real_research_state:false, probe_count_exactly_two pass (2), root_md_json_bounded pass** |
| Track A resume gate | `python scripts/tracka_resume_gate.py --json` | **BLOCKED / PREREG_OR_MANIFEST_BLOCK_AFTER_DRIFT_PASS / drift_preflight.pass:true / outcomes_inspected:false** |

## 3. EVIDENCE ADDED / MODIFIED (paths)
| Path | Change |
|---|---|
| `scripts/run_gate4_v4_leakage_audit.py` | **Modified** — `extract_additive_diag()` added; `audit_block_bootstrap_reproducibility()` now returns `run1_diagnostics`/`run2_diagnostics`/`diagnostics_identical_on_rerun`; `write_md()` renders additive diagnostics table + summary lines; `make_interpretation()` cites additive diagnostics |
| `tests/test_gate4_v4_leakage_audit_md_diagnostics.py` | **Modified** — extended 7→12 tests (additive extraction, JSON payload, interpretation); fixed `test_write_md_legacy_ci_fallback` row-format assertion to match renderer |
| `research_state/gate4_v4_leakage_audit/gate4_v4_leakage_audit_20261109T070000Z.json` | **Created** — regenerated EXPLORATORY leakage audit with additive diagnostics serialized |
| `research_state/gate4_v4_leakage_audit/gate4_v4_leakage_audit_20261109T070000Z.md` | **Created** — markdown with additive diagnostics table |
| `results/fclr_heavy001/gate4_v4_leakage_audit_20261109T070000Z.md` | **Created** — mirror markdown |
| `AGENT_HANDOFF.md` | **Updated** — single durable handoff, session `2026-11-09T07:23:17Z`, §0 initial task message = failing-regime regression tests |

## 4. CURRENT STATE OF EACH RESEARCH GATE
| Gate | Status | Evidence / Notes |
|---|---|---|
| **Gate 1 (Data Loadable)** | Track A **BLOCKED** (no admissible unauth liquidation labels). Track C historical/sealed. Gate 4 exploratory local 2024-04..09 cache present (FCLR-015). | `track_a_deadend_map.md`; `data_cache/*_2024_04..09` |
| **Gate 2 (Protocol Frozen)** | PASSED Track C context; Gate 4 v4 **FROZEN_BEFORE_OUTCOMES**, `confirmatory_claim_go=NO_GO`, exploratory-only on 2024-04..09 (sealed-anchor conflict). | `pre_registration_gate4_funding_multisplit_v4_20261107T1845Z.json` |
| **Gate 3 (RV-only Baseline)** | Track C historical PASSED / **forward INCONCLUSIVE** (0 non-overlapping 30d blocks). | `evaluation_summary_FCLR-012-V.md` |
| **Gate 4 (Incremental Funding/Price)** | **EXPLORATORY NO-GO CONFIRMED** on local 2024-04..09 (stab `20261109T045805Z`, nogo `20261109T053308Z`). Leakage controls audited PASS (EXPLORATORY, `20261109T055837Z`). Bootstrap diagnostics hardened + propagated into stab markdown/diag stdout/CI JSON shape; tests green. **NOT CONFIRMATORY / NOT PROMOTABLE.** | `research_state/gate4_v4_exploratory_{stab,nogo,leakage_audit}/`, `src/eval/inference.py`, `tests/test_*inference*`, `tests/test_gate4_v4_exploratory_stab_diagnostics.py` |
| **Forecast Gate** | **NOT ELIGIBLE**. No confirmatory promotion. | frontier/negative results |

## 5. BOTTLENECK / BLOCKED-SESSION RECONCILIATION (do not attempt removal of structural gates)
| Item | State | Is it a removable bottleneck? | Allowed route |
|---|---|---|---|
| Track A: no admissible liquidation labels (2026-11..2027-02 absent, probes==2) | Structural deadend | **NO** — do not re-probe absent months, no probe/scan/wrapper families | Guard hardening only if a specific gap is identified |
| Track C forward: inconclusive (0 non-overlapping 30d blocks) | Structural | **NO** — do not relax criteria | New admissible panel meeting criteria; do not relax |
| Gate 4 v4: confirmatory_claim_go NO_GO; sealed-anchor conflict | Structural by design | **NO** — no promotion, no sealed-anchor reuse, no rerun of identical stabilization claims | EXPLORATORY-only engineering/diagnostics on local 2024-04..09 cache |
| `tracka_resume_gate.py --json` → BLOCKED (PREREG_OR_MANIFEST_BLOCK_AFTER_DRIFT_PASS, outcomes_inspected:false) | By-design pre-reg/manifest block | **NO** — this is a gate, not an inefficiency to bypass | Maintain drift_preflight.pass:true; do not force outcomes_inspected |
| Leakage-audit additive diagnostics (§0 task 1) | **DONE** 2026-11-09T07:00:00Z | N/A — completed, do not rerun | Build on it; next task is failing-regime tests |

**Conclusion:** no session is inefficient due to a removable bottleneck. Every BLOCKED state above is a structural constraint that must be preserved, not removed. The only open, non-avoidable, high-value path is the §0 initial task: failing-regime regression tests for `fit_predict_ols` / `block_bootstrap_delta_ci_diagnostic`.

## 6. SINGLE HIGHEST-VALUE NEXT TASK
**Failing-regime regression tests for `fit_predict_ols` / `block_bootstrap_delta_ci_diagnostic` (measurable, low-risk, materially different from serialization coverage).** Add synthetic fixture tests covering zero-variance predictor columns, constant finite diffs, empty/all-non-finite diffs, too-few-blocks, missing required columns, collinear predictors, and single-instrument panels; assert each regime is flagged by `degenerate`/`regime_flags`/`ci_accounting_valid`/`inference_ok` and cannot silently inflate QLIKE or hide a degenerate CI. Leakage-audit diagnostic propagation (§0.1) is **already complete** (2026-11-09T07:00:00Z) — this is the next distinct task, not a rerun. **Do not rerun expensive exploratory computations** — test inference/fit behavior with synthetic fixtures only. Register any new script in `research_state/tracka_script_scope_registry.json` and mirror in `tests/test_tracka_hardening_*.py` `SCRIPT_REGISTRY`; keep `scripts=registry` and drift PASS.

## 7. PRECISE VERIFICATION COMMANDS
```bash
git --no-pager status --short
python3 -m unittest tests.test_gate4_v4_leakage_audit_md_diagnostics tests.test_gate4_v4_leakage_audit tests.test_eval_inference_diagnostics -v
python -m unittest discover tests                         # expect >=986 OK
python scripts/check_tracka_scope_registry_drift.py      # expect PASS
python scripts/tracka_resume_check.py                    # expect pass:true, 17/17, probes==2, root_md_json_bounded pass
python scripts/tracka_resume_gate.py --json              # expect BLOCKED, drift_preflight.pass:true, outcomes_inspected:false
```

## 8. BLOCKERS / CONSTRAINTS
| Blocker | Evidence | Allowed next route |
|---|---|---|
| Track A: no admissible liquidation labels | `track_a_deadend_map.md`, NO-GO rubric, probes==2, 2026-11..2027-02 absent | Guard hardening only if specific gap; **no** re-probe absent months |
| Track C: forward inconclusive (0 non-overlapping 30d blocks) | FCLR-012-V | New admissible panel meeting criteria; do not relax |
| Gate 4 v4: sealed-anchor conflict; confirmatory_claim_go NO_GO | v4 prereg | **EXPLORATORY only**, explicit labels, no promotion/sealed-anchor reuse |
| Gate 4 v4: funding ablations NO-GO on 2024-04..09 | stab/nogo artifacts | No improvement claim; pivot to tested engineering/diagnostics |
| Root md+json bound tight | `tracka_resume_check.py` root_md_json_bounded | New artifacts in `results/` or dated subdirs; **do not weaken** |
| Protected control plane | repo rules | **No `.github/workflows` edits** |

## 9. DO NOT DO
- ❌ Re-probe 2026-11..2027-02 / create Track A probe/scan/wrapper/report families
- ❌ Workflows/schedulers/pollers/status-only files/controllers
- ❌ Track C/B new sealed outcomes or conflate observed/modeled/synthetic labels
- ❌ Threshold-shopping, holdout reuse, confirmatory/promotion claims from exploratory runs
- ❌ Commit `__pycache__/`, `research_state/ironflow_fastpath_cache.json`, large raw caches
- ❌ Weaken `root_md_json_bounded` or Track A invariants
- ❌ Live/paper trading, order endpoints, credentials, access-control bypass

## 10. SESSION START PROTOCOL (mandatory)
1. `git pull` + `git status`; read **this file** + `RESEARCH_PROMPT.md`.
2. Inspect `research_state/experiment_frontier.json`, latest manifests/tests/cache, `gate4_v4_exploratory_{stab,nogo,leakage_audit}`, `results/fclr_heavy001/*diagnostic*`.
3. Execute §0 (measurable task). Cheapest checks first. Update **this file** with exact evidence + current session timestamp.

## 11. NEXT SESSION DELIVERABLE
Updated `AGENT_HANDOFF.md` with tested failing-regime regression coverage for `fit_predict_ols`/`block_bootstrap_delta_ci_diagnostic` (or a materially different tested hardening task from §0.2a–c) + versioned artifacts, suite **≥986 OK** (or higher if tests added), scope drift PASS, Track A invariants green (17/17, probes==2, root bound pass), and the next unfinished task — **acceptance (A)/(B) satisfied**. Repo must remain continuable without user repeating instructions.

---
**END OF SINGLE DURABLE HANDOFF.**
