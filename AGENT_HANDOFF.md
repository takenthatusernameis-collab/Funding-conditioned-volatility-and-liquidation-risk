# AGENT_HANDOFF.md — Single Durable Handoff (next session must continue from here)

**Generated/updated:** 2026-11-09T06:29:33Z (session task timestamp `2026-11-09T06:29:33Z`)
**Repository:** Funding-conditioned-volatility-and-liquidation-risk
**Priority (reconciled, binding):** Repo P0 = **Gate 4 exploratory infrastructure hardening with measurable, tested artifacts** (local admissible 2024-04..09 cache only). Gate 4 v4 funding ablations remain **EXPLORATORY NO-GO CONFIRMED** — **do not rerun identical stabilization claims, do not claim confirmatory GO/economic value/promotion, do not reuse sealed-anchor domain (FCLR002/003/013), do not replace prereg A–E contrasts or change confirmatory estimands**. Track A = **structurally blocked/no trigger** (2026-11..2027-02 absent, probes==2, deadend rubric holds) — **no probing, no scan/wrapper/report families**. Track C sealed/inconclusive forward; Track B NOT_SUPPORTED. **No status-only churn. Every session must produce versioned, auditable artifacts and/or tested code. No `.github/workflows` edits.**

**Verified this session (2026-11-09T06:29:33Z):** Propagated hardened bootstrap diagnostics into Gate 4 exploratory reporting paths (acceptance A, tested). `scripts/run_gate4_v4_exploratory_stab.py` markdown now serializes `eff_blocks`/`ci_valid`/`regime_flags` for pooled contrasts and LOO (additive, legacy-field tolerant). `scripts/run_gate4_v4_exploratory_diag.py` stdout reports `eff_blocks`/`ci_valid`/`flags` for E vs A. Bootstrap delegate (`scripts/run_funding_ablations.py:block_bootstrap_delta_ci` → `src/eval/inference.diagnostic`) confirmed to return additive fields: `effective_block_count`, `regime_flags`, `ci_accounting_valid`, `degenerate`, `inference_ok`, `n_obs_*`, `n_blocks_*`, `n_reps_effective`. New synthetic test: `tests/test_gate4_v4_exploratory_stab_diagnostics.py` (3). Existing hardened stack green: `src/eval/inference.py`, `tests/test_eval_inference_diagnostics.py` (5). **Targeted:** `test_gate4_v4_exploratory_stab_diagnostics`, `test_eval_inference_diagnostics`, `test_funding_ablations_multisplit`, `test_gate4_v4_exploratory_diag`, `test_gate4_v4_exploratory_stab` → **22 tests OK**. **Full suite:** **974 tests in ~110s — OK**. `check_tracka_scope_registry_drift.py` → **[PASS] scripts=114 registry=114**. `tracka_resume_check.py` → **pass:true, 17/17 checks pass, network:false, writes_real_research_state:false, probes_count_exactly_two pass (count=2), root_md_json_bounded pass**. `tracka_resume_gate.py --json` → **status:BLOCKED, reason_code:PREREG_OR_MANIFEST_BLOCK_AFTER_DRIFT_PASS, drift_preflight.pass:true, outcomes_inspected:false**. **All EXPLORATORY / NOT CONFIRMATORY / NOT PROMOTABLE for Gate 4.** `research_state/ironflow_fastpath_cache.json` modified locally — **do not commit**.

---

## 0) INITIAL TASK MESSAGE FOR NEXT AGENTIC SESSION (MANDATORY, HEAVY WORK — NO AVOIDANCE)

**Session timestamp (initial task):** `2026-11-09T06:29:33Z`

**You MUST execute measurable research/engineering progress.** Forbidden: status-only churn, Track A probing (2026-11..2027-02 absent/probes==2), Track C/B new sealed outcomes, workflow/controller/scheduler/poller/wrapper creation, `.github/workflows` edits, confirmatory promotion from exploratory Gate 4, sealed-anchor reuse, prereg A–E contrast/estimand changes, threshold-shopping, holdout reuse, weakening root md+json bound or Track A invariants, live/paper trading, credentials, access-control bypass, committing `__pycache__`/`ironflow_fastpath_cache.json`/large raw caches.

**Gate 4 v4 binding state (do not litigate):** `FROZEN_BEFORE_OUTCOMES`, `confirmatory_claim_go=NO_GO`, `exploratory_smoke_authorized_after_freeze=true` (local 2024-04..09 cache; FCLR-015 SHA256 `3e6ac26c...5406c`). **EXPLORATORY / NOT CONFIRMATORY / NOT PROMOTABLE.** Prior exec/diag/stab/NO-GO/leakage artifacts exist and are sufficient for the current claim boundary — **do not rerun identical stabilization claims**. Bootstrap diagnostics now exist in code + stab/diag propagation (`src/eval/inference.py`, `scripts/run_funding_ablations.py` delegate, `run_gate4_v4_exploratory_{stab,diag}.py`, tests) — build on this, do not redo it.

**Execute next (highest-value measurable engineering — choose ≥1, complete fully):**

1. **Persist diagnostic fields in exploratory JSON summaries for leakage audit + any remaining exploratory serializers (tested).** `run_gate4_v4_leakage_audit.py` reports bootstrap reproducibility; ensure its saved JSON/MD carries additive `effective_block_count`/`regime_flags`/`ci_accounting_valid` where bootstrap CIs appear (the delegate already returns them — verify serialization/markdown). Add **synthetic** unit tests for touched serialization/report logic (no network, no real `research_state` writes, use temp dirs). **Do not rerun heavy exploratory data passes unless required by a new tested code path; prefer serializer/unit-test coverage.**
2. **If (1) is already complete after inspection, implement a *materially different* tested Gate 4/Track C-adjacent hardening task with versioned evidence** (examples, pick one and do it end-to-end): (a) add a deterministic “bootstrap diagnostic summary” helper that consumes saved exploratory JSON and emits a compact `results/` markdown risk table (synthetic fixture test), (b) add failing-regime regression tests for `fit_predict_ols`/`block_bootstrap_delta_ci_diagnostic` edge cases that could inflate QLIKE or hide degenerate CIs (synthetic), or (c) harden split-boundary/leakage assertions around exploratory variant parameter provenance with fixture tests. **New scripts must be registered** in `research_state/tracka_script_scope_registry.json` and mirrored in `tests/test_tracka_hardening_117.py` `SCRIPT_REGISTRY` (and pass 118/119 checks); keep `scripts=registry` and drift PASS.
3. **Artifact discipline:** new heavy outputs go to `results/` or dated subdirs — **do not add repo-root `research_state/*.md/*.json` files**. Root bound is tight (currently 2 root md+json files total per resume check structure; maintain `root_md_json_bounded` pass). Version outputs with UTC timestamps in filenames when creating bundles.
4. **Verification (must run):** targeted tests for touched code first; then `python -m unittest discover tests` (**must remain ≥974 OK, expect increase if tests added**). `python scripts/check_tracka_scope_registry_drift.py` → PASS. `python scripts/tracka_resume_check.py` → pass:true, 17/17, network:false, probes==2, root_md_json_bounded pass. `python scripts/tracka_resume_gate.py --json` → BLOCKED, `drift_preflight.pass:true`, `outcomes_inspected:false`.
5. **Update this single durable handoff** (§1–§10) with session timestamp, exact file paths changed, commands, pass/fail counts, artifact paths, blockers, and the **single highest-value unfinished next task**. No parallel handoff files.

**Acceptance (mandatory):** (A) tested code/artifact change with green targeted + full suite + all invariants green, **or** (B) a materially different tested engineering task with versioned evidence and same green gates. **Anything less is failure.**

---

## 1. WHAT CHANGED AND WHY (this session, 2026-11-09T06:29:33Z)
- **Propagated bootstrap diagnostics into exploratory reporting (acceptance A):** `scripts/run_gate4_v4_exploratory_stab.py` `write_md()` now renders additive CI diagnostics (`eff_blocks`, `ci_valid`, `regime_flags`) in pooled contrast and V3 E-vs-A LOO tables; legacy CI dicts without new fields remain readable (`effective_block_count` falls back to `n_blocks`, flags render `ok`). `scripts/run_gate4_v4_exploratory_diag.py` stdout now prints `eff_blocks`/`ci_valid`/`flags` for E vs A. JSON outputs already carry additive fields because `block_bootstrap_delta_ci` delegates to `src/eval.inference.block_bootstrap_delta_ci_diagnostic`.
- **Tests (synthetic, no network, no real `research_state` writes):** added `tests/test_gate4_v4_exploratory_stab_diagnostics.py` (3 tests): markdown includes diagnostic columns/flags; markdown tolerates legacy CI dicts; additive CI JSON shape keys present. Confirmed existing hardened coverage remains green (`tests/test_eval_inference_diagnostics.py`, `tests/test_funding_ablations_multisplit.py`, diag/stab tests).
- **No Track A/root-bound weakening:** no probe/scan/wrapper families; no new root `research_state/*.md/*.json`; no workflow/controller edits. `research_state/ironflow_fastpath_cache.json` local side effect — **do not commit**.

## 2. WHAT WAS ACTUALLY TESTED — EXACT OUTCOMES
| Check | Command | Result |
|---|---|---|
| Targeted propagation + hardened bootstrap | `python3 -m unittest tests.test_gate4_v4_exploratory_stab_diagnostics tests.test_eval_inference_diagnostics tests.test_funding_ablations_multisplit tests.test_gate4_v4_exploratory_diag tests.test_gate4_v4_exploratory_stab -v` | **22 tests OK** |
| Registry/leakage guards | `python -m unittest tests.test_tracka_hardening_117 tests.test_tracka_hardening_118 tests.test_tracka_hardening_119 tests.test_gate4_v4_leakage_audit` | **OK** (includes `Updated experiment_frontier.json` side effect in some harness paths — no commit) |
| Full suite | `python -m unittest discover tests` | **Ran 974 tests in ~110s — OK** |
| Scope registry drift | `python scripts/check_tracka_scope_registry_drift.py` | **[PASS] scripts=114 registry=114 reason=OK** |
| Track A resume check | `python scripts/tracka_resume_check.py` | **pass:true, 17/17, network:false, writes_real_research_state:false, probe_count_exactly_two pass (2), root_md_json_bounded pass** |
| Track A resume gate | `python scripts/tracka_resume_gate.py --json` | **BLOCKED / PREREG_OR_MANIFEST_BLOCK_AFTER_DRIFT_PASS / drift_preflight.pass:true / outcomes_inspected:false** |

## 3. EVIDENCE ADDED / MODIFIED (paths)
| Path | Change |
|---|---|
| `scripts/run_gate4_v4_exploratory_stab.py` | **Modified** — markdown tables include `eff_blocks`/`ci_valid`/`regime_flags` (pooled + LOO), legacy-field tolerant |
| `scripts/run_gate4_v4_exploratory_diag.py` | **Modified** — stdout includes `eff_blocks`/`ci_valid`/`flags` for E vs A |
| `tests/test_gate4_v4_exploratory_stab_diagnostics.py` | **Created (untracked/new test)** — 3 synthetic propagation tests |
| `AGENT_HANDOFF.md` | **Updated** — single durable handoff, session `2026-11-09T06:29:33Z` |
| `src/eval/inference.py`, `scripts/run_funding_ablations.py`, `tests/test_eval_inference_diagnostics.py`, `tests/test_tracka_hardening_117.py` | **Present/hardened from prior session context** — verified compatible by targeted/full suite (no regression) |
| `results/fclr_heavy001/gate4_v4_diagnostic_bundle_index_20261109T061843Z.md` | **Pre-existing versioned EXPLORATORY index** — reference only |
| `research_state/ironflow_fastpath_cache.json` | **Modified locally by checks; do not commit** |

## 4. CURRENT STATE OF EACH RESEARCH GATE
| Gate | Status | Evidence / Notes |
|---|---|---|
| **Gate 1 (Data Loadable)** | Track A **BLOCKED** (no admissible unauth liquidation labels). Track C historical/sealed. Gate 4 exploratory local 2024-04..09 cache present (FCLR-015). | `track_a_deadend_map.md`; `data_cache/*_2024_04..09` |
| **Gate 2 (Protocol Frozen)** | PASSED Track C context; Gate 4 v4 **FROZEN_BEFORE_OUTCOMES**, `confirmatory_claim_go=NO_GO`, exploratory-only on 2024-04..09 (sealed-anchor conflict). | `pre_registration_gate4_funding_multisplit_v4_20261107T1845Z.json` |
| **Gate 3 (RV-only Baseline)** | Track C historical PASSED / **forward INCONCLUSIVE** (0 non-overlapping 30d blocks). | `evaluation_summary_FCLR-012-V.md` |
| **Gate 4 (Incremental Funding/Price)** | **EXPLORATORY NO-GO CONFIRMED** on local 2024-04..09 (stab `20261109T045805Z`, nogo `20261109T053308Z`). Leakage controls audited PASS (EXPLORATORY, `20261109T055837Z`). Bootstrap diagnostics hardened + propagated into stab markdown/diag stdout/CI JSON shape; tests green. **NOT CONFIRMATORY / NOT PROMOTABLE.** | `research_state/gate4_v4_exploratory_{stab,nogo,leakage_audit}/`, `src/eval/inference.py`, `tests/test_*inference*`, `tests/test_gate4_v4_exploratory_stab_diagnostics.py` |
| **Forecast Gate** | **NOT ELIGIBLE**. No confirmatory promotion. | frontier/negative results |

## 5. SINGLE HIGHEST-VALUE NEXT TASK
**Leakage-audit diagnostic propagation + synthetic serializer test (measurable, low-risk).** Inspect `scripts/run_gate4_v4_leakage_audit.py` output JSON/MD paths and ensure additive bootstrap diagnostics (`effective_block_count`/`regime_flags`/`ci_accounting_valid`) are surfaced wherever bootstrap CIs/reproducibility summaries are serialized; add synthetic tests for the touched serializer/report logic (temp dirs, no network, no real `research_state` writes). **Do not rerun expensive exploratory computations** — test serializer behavior with fixture payloads. If leakage audit already surfaces fields completely, pick a *different* tested hardening task from §0(2a–c) and record why (1) was skipped.

## 6. PRECISE VERIFICATION COMMANDS
```bash
git --no-pager status --short
python3 -m unittest tests.test_gate4_v4_exploratory_stab_diagnostics tests.test_eval_inference_diagnostics tests.test_funding_ablations_multisplit tests.test_gate4_v4_exploratory_diag tests.test_gate4_v4_exploratory_stab -v
python -m unittest discover tests                         # expect >=974 OK
python scripts/check_tracka_scope_registry_drift.py      # expect PASS
python scripts/tracka_resume_check.py                    # expect pass:true, 17/17, probes==2, root_md_json_bounded pass
python scripts/tracka_resume_gate.py --json              # expect BLOCKED, drift_preflight.pass:true, outcomes_inspected:false
```

## 7. BLOCKERS / CONSTRAINTS
| Blocker | Evidence | Allowed next route |
|---|---|---|
| Track A: no admissible liquidation labels | `track_a_deadend_map.md`, NO-GO rubric, probes==2, 2026-11..2027-02 absent | Guard hardening only if specific gap; **no** re-probe absent months |
| Track C: forward inconclusive (0 non-overlapping 30d blocks) | FCLR-012-V | New admissible panel meeting criteria; do not relax |
| Gate 4 v4: sealed-anchor conflict; confirmatory_claim_go NO_GO | v4 prereg | **EXPLORATORY only**, explicit labels, no promotion/sealed-anchor reuse |
| Gate 4 v4: funding ablations NO-GO on 2024-04..09 | stab/nogo artifacts | No improvement claim; pivot to tested engineering/diagnostics |
| Root md+json bound tight | `tracka_resume_check.py` root_md_json_bounded | New artifacts in `results/` or dated subdirs; **do not weaken** |
| Protected control plane | repo rules | **No `.github/workflows` edits** |

## 8. DO NOT DO
- ❌ Re-probe 2026-11..2027-02 / create Track A probe/scan/wrapper/report families
- ❌ Workflows/schedulers/pollers/status-only files/controllers
- ❌ Track C/B new sealed outcomes or conflate observed/modeled/synthetic labels
- ❌ Threshold-shopping, holdout reuse, confirmatory/promotion claims from exploratory runs
- ❌ Commit `__pycache__/`, `research_state/ironflow_fastpath_cache.json`, large raw caches
- ❌ Weaken `root_md_json_bounded` or Track A invariants
- ❌ Live/paper trading, order endpoints, credentials, access-control bypass

## 9. SESSION START PROTOCOL (mandatory)
1. `git pull` + `git status`; read **this file** + `RESEARCH_PROMPT.md`.
2. Inspect `research_state/experiment_frontier.json`, latest manifests/tests/cache, `gate4_v4_exploratory_{stab,nogo,leakage_audit}`, `results/fclr_heavy001/*diagnostic*`.
3. Execute §0 (measurable task). Cheapest checks first. Update **this file** with exact evidence + current session timestamp.

## 10. NEXT SESSION DELIVERABLE
Updated `AGENT_HANDOFF.md` with tested leakage-audit diagnostic propagation (or a materially different tested hardening task from §0.2a–c) + versioned artifacts, suite **≥974 OK** (or higher if tests added), scope drift PASS, Track A invariants green (17/17, probes==2, root bound pass), and the next unfinished task — **acceptance (A)/(B) satisfied**. Repo must remain continuable without user repeating instructions.

---
**END OF SINGLE DURABLE HANDOFF.**
