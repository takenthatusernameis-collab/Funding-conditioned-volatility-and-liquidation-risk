# AGENT_HANDOFF.md — Single Durable Handoff (next session must continue from here)

**Generated/updated:** 2026-11-09T06:27:55Z (session task timestamp `2026-11-09T06:05:59Z`)
**Repository:** Funding-conditioned-volatility-and-liquidation-risk
**Priority (reconciled):** Repo P0 = Gate 4 funding-conditioned volatility on local admissible 2024-04..09 cache remains **EXPLORATORY NO-GO CONFIRMED** (do not re-run identical stabilization claims). Next heavy work = measurable local engineering/hardening on Gate 4/Track C-adjacent infrastructure with versioned evidence and tests (no Track A probing, no sealed C/B new outcomes, no confirmatory promotion). Track A = structurally blocked / no trigger (lockdown hardening only if specific gap); Track C sealed/inconclusive forward; Track B NOT_SUPPORTED. **No status-only churn. Every session must produce versioned, auditable artifacts and/or tested code.**
**Verified this session (2026-11-09T06:05:59Z, post-state 2026-11-09T06:27:55Z):** Added **hardened block-bootstrap/inference diagnostics** as tested library code (synthetic, no network, no real `research_state` writes): `src/eval/inference.py` (`block_bootstrap_delta_ci_diagnostic`, `diagnose_block_bootstrap_inputs`) rejects non-finite diffs from CI accounting, reports `effective_block_count`/`n_blocks_nonempty_finite`, and flags degenerate/too-few-block/no-finite-block/low-effective-replicate regimes with additive fields while preserving legacy caller shape; `scripts/run_funding_ablations.py:block_bootstrap_delta_ci` delegates (backward-compatible). New tests: `tests/test_eval_inference_diagnostics.py` (5). Added versioned **EXPLORATORY diagnostic bundle index** in `results/` (no root `research_state` pressure): `results/fclr_heavy001/gate4_v4_diagnostic_bundle_index_20261109T061843Z.md`. Scope registry mirrors updated: `tests/test_tracka_hardening_117.py` SCRIPT_REGISTRY now includes `run_gate4_v4_leakage_audit.py` (reconciled with JSON + 118/119). Full suite: **971 tests in ~110s — OK**. `check_tracka_scope_registry_drift.py` → **[PASS] scripts=114 registry=114**. `tracka_resume_check.py` → **pass:true, 17/17, network:false, probes==2, writes_real_research_state:false, root_md_json_bounded pass**. `tracka_resume_gate.py --json` → **drift_preflight.pass:true, status:BLOCKED, reason_code:PREREG_OR_MANIFEST_BLOCK_AFTER_DRIFT_PASS, outcomes_inspected:false**. **All EXPLORATORY / NOT CONFIRMATORY / NOT PROMOTABLE where Gate 4 applies.** `research_state/ironflow_fastpath_cache.json` is modified locally — **do not commit**.

---

## 0) INITIAL TASK MESSAGE FOR NEXT AGENTIC SESSION (MANDATORY, HEAVY WORK)

**Session timestamp (initial task):** `2026-11-09T06:27:55Z`

**You MUST execute measurable research/engineering progress. No Track A probing (2026-11..2027-02 absent, probes==2, deadend rubric holds). No new Track C/B sealed outcomes. No workflows/schedulers/pollers/wrappers/controllers. No `.github/workflows` edits. No status-only churn. Every action must produce versioned, auditable artifacts and/or tested code.**

**Campaign (binding constraints):** Gate 4 v4 is `FROZEN_BEFORE_OUTCOMES`, `confirmatory_claim_go=NO_GO`, `exploratory_smoke_authorized_after_freeze=true` (local 2024-04..09 cache; FCLR-015 SHA256 `3e6ac26c...5406c`). **EXPLORATORY / NOT CONFIRMATORY / NOT PROMOTABLE.** Never claim confirmatory GO, economic value, or promotion. Never reuse sealed-anchor domain (FCLR002/003/013). Never replace prereg A–E contrasts or change confirmatory estimands.

**Completed — do not rerun identically:** v4 exec `20261109T004003Z`, diag `20261109T021456Z`, stab `20261109T045805Z` (**NO-GO**), NO-GO note `20261109T053308Z`, leakage audit `20261109T055837Z` (**PASS**, EXPLORATORY). Inference hardening delivered `20261109T061843Z`-session context: `src/eval/inference.py` + delegate in `scripts/run_funding_ablations.py` + `tests/test_eval_inference_diagnostics.py` (5 tests). Diagnostic bundle index: `results/fclr_heavy001/gate4_v4_diagnostic_bundle_index_20261109T061843Z.md`.

**Execute next (highest-value measurable engineering, not more status memos):**
1. **Propagate/use diagnostic fields in versioned Gate 4 exploratory reporting** (targeted, tested): ensure relevant exploratory runners (`run_gate4_v4_exploratory_{diag,stab,exec}`, leakage audit if applicable) persist `effective_block_count`/`regime_flags`/`ci_accounting_valid` in versioned outputs where they already emit bootstrap CIs — add/update **synthetic-safe unit tests** for any serializer/summary logic touched (no network, no real `research_state` writes). Do **not** change confirmatory estimands or prereg A–E contrasts.
2. **Keep diagnostic/index artifacts in `results/` or dated subdirs**; do not add root `research_state/*.md/*.json` files (bound 172). If a new script is added, register it in `research_state/tracka_script_scope_registry.json` and mirror in `tests/test_tracka_hardening_117.py` SCRIPT_REGISTRY; pass drift check.
3. **Targeted tests first**, then `python -m unittest discover tests` must remain **>=971 OK**. Verify: `check_tracka_scope_registry_drift.py` PASS; `tracka_resume_check.py` pass 17/17, probes==2, root bound pass; `tracka_resume_gate.py --json` BLOCKED, drift_preflight.pass:true, outcomes_inspected:false.
4. **Update this handoff** (§1–§10) with exact changes/commands/results/artifact paths/issues/next task. Record session timestamp `2026-11-09T06:27:55Z`.

**Acceptance (heavy work — at least one required):** (A) tested inference/diagnostic hardening or propagation merged as code + tests green + invariants green, or (B) a materially different tested engineering task with versioned evidence and suite/invariants green. Sessions without (A)/(B) fail the mandate.

---

## 1. WHAT CHANGED AND WHY (this session, 2026-11-09T06:05:59Z)
- **Hardened block-bootstrap/inference diagnostics (acceptance A):** Added `src/eval/__init__.py` and `src/eval/inference.py` with `diagnose_block_bootstrap_inputs` / `block_bootstrap_delta_ci_diagnostic`. Explicitly rejects non-finite diffs from CI accounting, reports effective/nonempty-finite block counts, and flags degenerate/too-few-block/no-finite-block/all-non-finite/low-effective-replicate regimes. Additive to legacy fields; preserves `point/ci_low/ci_high/n_obs/n_blocks/n_reps/seed/block_hours/alpha` for existing callers.
- **Integrated into existing path (backward-compatible):** `scripts/run_funding_ablations.py:block_bootstrap_delta_ci` now delegates to hardened diagnostics; behavior remains compatible with `tests/test_funding_ablations_multisplit.py` and Gate 4 callers.
- **Tests (synthetic, no network, no real `research_state` writes):** `tests/test_eval_inference_diagnostics.py` — 5 tests covering non-finite diff accounting, too-few-block degeneracy, no-finite-blocks, effective block count + legacy fields, fixed-seed determinism.
- **Versioned diagnostic bundle index (results/, no root pressure):** `results/fclr_heavy001/gate4_v4_diagnostic_bundle_index_20261109T061843Z.md` cross-links exec/diag/stab/nogo/leakage artifacts, commands, verdict, and hardening notes (**EXPLORATORY / NOT CONFIRMATORY / NOT PROMOTABLE**).
- **Scope registry reconciliation:** `tests/test_tracka_hardening_117.py` SCRIPT_REGISTRY gained `run_gate4_v4_leakage_audit.py` (`track_c_sealed_volatility`) to match canonical JSON registry and satisfy 117/118/119 drift guards. JSON registry already contained entry (script_count 114).
- **Cache hygiene:** `research_state/ironflow_fastpath_cache.json` modified by suite/check side effects — **do not commit**.

## 2. WHAT WAS ACTUALLY TESTED — EXACT OUTCOMES
| Check | Command | Result |
|---|---|---|
| Targeted inference diagnostics | `python -m unittest tests.test_eval_inference_diagnostics -v` (after float-assert fix) | **5 tests OK** |
| Targeted bootstrap/Gate 4 | `python -m unittest tests.test_eval_inference_diagnostics tests.test_funding_ablations_multisplit tests.test_gate4_v4_leakage_audit tests.test_gate4_v4_exploratory_diag tests.test_gate4_v4_exploratory_stab` | **25 tests OK** |
| Hardening registry tests | `python -m unittest tests.test_tracka_hardening_117 tests.test_tracka_hardening_118 tests.test_tracka_hardening_119` | **48 tests OK** |
| Full suite | `python -m unittest discover tests` | **Ran 971 tests in ~110s — OK** |
| Scope registry drift | `python scripts/check_tracka_scope_registry_drift.py` | **[PASS] scripts=114 registry=114 reason=OK** |
| Track A resume check | `python scripts/tracka_resume_check.py` | **pass:true, 17/17, network:false, probes==2, writes_real_research_state:false, root_md_json_bounded pass** |
| Track A resume gate | `python scripts/tracka_resume_gate.py --json` | **drift_preflight.pass:true, status:BLOCKED, reason_code:PREREG_OR_MANIFEST_BLOCK_AFTER_DRIFT_PASS, outcomes_inspected:false** |

## 3. EVIDENCE ADDED / MODIFIED (paths)
| Path | Change |
|---|---|
| `src/eval/__init__.py` | **Created** — eval package init |
| `src/eval/inference.py` | **Created** — hardened bootstrap diagnostics (`block_bootstrap_delta_ci_diagnostic`, `diagnose_block_bootstrap_inputs`) |
| `scripts/run_funding_ablations.py` | **Modified** — `block_bootstrap_delta_ci` delegates to hardened diagnostics (legacy shape preserved) |
| `tests/test_eval_inference_diagnostics.py` | **Created** — 5 synthetic diagnostic tests |
| `tests/test_tracka_hardening_117.py` | **Modified** — registered `run_gate4_v4_leakage_audit.py` in SCRIPT_REGISTRY (reconcile with JSON/118/119) |
| `results/fclr_heavy001/gate4_v4_diagnostic_bundle_index_20261109T061843Z.md` | **Created** — versioned EXPLORATORY diagnostic bundle index (no root pressure) |
| `AGENT_HANDOFF.md` | **Updated** — session `2026-11-09T06:05:59Z` / updated `2026-11-09T06:27:55Z`, acceptance (A) satisfied |
| `research_state/tracka_script_scope_registry.json` | **No change this session** (already contained leakage audit; verified PASS) |
| `research_state/ironflow_fastpath_cache.json` | **Modified locally by checks; do not commit** |

## 4. CURRENT STATE OF EACH RESEARCH GATE
| Gate | Status | Evidence / Notes |
|---|---|---|
| **Gate 1 (Data Loadable)** | Track A **BLOCKED** (no admissible unauth liquidation labels). Track C historical/sealed. Gate 4 exploratory local 2024-04..09 cache present (FCLR-015). | `track_a_deadend_map.md`; `data_cache/*_2024_04..09` |
| **Gate 2 (Protocol Frozen)** | PASSED Track C context; Gate 4 v4 **FROZEN_BEFORE_OUTCOMES**, `confirmatory_claim_go=NO_GO`, exploratory-only on 2024-04..09 (sealed-anchor conflict). | `pre_registration_gate4_funding_multisplit_v4_20261107T1845Z.json` |
| **Gate 3 (RV-only Baseline)** | Track C historical PASSED / **forward INCONCLUSIVE** (0 non-overlapping 30d blocks). | `evaluation_summary_FCLR-012-V.md` |
| **Gate 4 (Incremental Funding/Price)** | **EXPLORATORY NO-GO CONFIRMED** on local 2024-04..09 (stab `20261109T045805Z`, nogo `20261109T053308Z`). Leakage controls audited PASS (EXPLORATORY, `20261109T055837Z`). **Inference diagnostics hardened in code** (`src/eval/inference.py`, `2026-11-09T06:05:59Z` session) — **NOT CONFIRMATORY / NOT PROMOTABLE**. | `research_state/gate4_v4_exploratory_{stab,nogo,leakage_audit}/`, `results/fclr_heavy001/gate4_v4_diagnostic_bundle_index_20261109T061843Z.md` |
| **Forecast Gate** | **NOT ELIGIBLE**. No confirmatory promotion. | frontier/negative results |

## 5. SINGLE HIGHEST-VALUE NEXT TASK
**Propagate hardened bootstrap diagnostics into versioned exploratory outputs** (tested): update Gate 4 exploratory runner summary/serializer paths so saved JSON/MD include `effective_block_count`, `regime_flags`, and `ci_accounting_valid` where bootstrap CIs are reported; add synthetic unit tests for the touched serialization/reporting logic (no network, no real `research_state` writes). Keep confirmatory estimands/prereg contrasts unchanged. Keep artifacts in `results/` or dated subdirs; maintain root bound <=172 and suite >=971 OK.

## 6. PRECISE VERIFICATION COMMANDS
```bash
git --no-pager status --short
python -m unittest tests.test_eval_inference_diagnostics tests.test_funding_ablations_multisplit tests.test_gate4_v4_leakage_audit -v
python -m unittest discover tests                         # expect >=971 OK
python scripts/check_tracka_scope_registry_drift.py      # expect PASS
python scripts/tracka_resume_check.py                    # expect pass:true, 17/17, probes==2, root_md_json_bounded pass
python scripts/tracka_resume_gate.py --json              # expect BLOCKED, drift_preflight.pass:true, outcomes_inspected:false
ls results/fclr_heavy001/gate4_v4_diagnostic_bundle_index_*.md src/eval/inference.py tests/test_eval_inference_diagnostics.py
```

## 7. BLOCKERS / CONSTRAINTS
| Blocker | Evidence | Allowed next route |
|---|---|---|
| Track A: no admissible liquidation labels | `track_a_deadend_map.md`, NO-GO rubric, probes==2, 2026-11..2027-02 absent | Guard hardening only if specific gap; **no** re-probe absent months |
| Track C: forward inconclusive (0 non-overlapping 30d blocks) | FCLR-012-V | New admissible panel meeting criteria; do not relax |
| Gate 4 v4: sealed-anchor conflict; confirmatory_claim_go NO_GO | v4 prereg | **EXPLORATORY only**, explicit labels, no promotion/sealed-anchor reuse |
| Gate 4 v4: funding ablations NO-GO on 2024-04..09 | stab/nogo artifacts | No improvement claim; pivot to tested engineering/diagnostics |
| Root md+json bound 172 | `tracka_resume_check.py` | Put new artifacts in `results/` or dated subdirs; **do not weaken** |
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
2. Inspect `research_state/experiment_frontier.json`, latest manifests/tests/cache, `gate4_v4_exploratory_{stab,nogo}`, `gate4_v4_leakage_audit`, `results/fclr_heavy001/gate4_v4_diagnostic_bundle_index_*.md`.
3. Execute §0 (measurable task). Cheapest checks first. Update **this file** with exact evidence + current session timestamp.

## 10. NEXT SESSION DELIVERABLE
Updated `AGENT_HANDOFF.md` with tested inference-diagnostic propagation or materially different tested engineering + versioned artifacts, suite **>=971 OK**, scope drift PASS, Track A invariants green (17/17, probes==2, root bound pass), and the next unfinished task — **acceptance (A)/(B) satisfied**. Repo must remain continuable without user repeating instructions.

---
**END OF SINGLE DURABLE HANDOFF.**
