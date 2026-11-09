# AGENT_HANDOFF.md — Single Durable Handoff (next session must continue from here)

**Generated:** 2026-11-09T06:05:59Z
**Repository:** Funding-conditioned-volatility-and-liquidation-risk
**Priority (reconciled):** Repo P0 = Gate 4 funding-conditioned volatility on local admissible 2024-04..09 cache remains **EXPLORATORY NO-GO CONFIRMED** (do not re-run identical stabilization claims). Next heavy work = measurable local engineering/hardening on Gate 4/Track C-adjacent infrastructure with versioned evidence and tests (no Track A probing, no sealed C/B new outcomes, no confirmatory promotion). Track A = structurally blocked / no trigger (lockdown hardening only if specific gap); Track C sealed/inconclusive forward; Track B NOT_SUPPORTED. **No status-only churn. Every session must produce versioned, auditable artifacts.**
**Verified this session (2026-11-09T06:05:59Z, baseline SHA `14f08775e`):** Gate 4 v4 EXPLORATORY **leakage audit PASS** (train-only provenance of ridge scale, winsor bounds, target floor, normalization mean/std invariant to test-fold perturbation across V1–V4, 4 prereg v3_30d splits × 5 symbols; block-bootstrap CI deterministic/reproducible with fixed seed 20261109). New artifacts: `research_state/gate4_v4_leakage_audit/gate4_v4_leakage_audit_20261109T055837Z.{json,md}`, `results/fclr_heavy001/gate4_v4_leakage_audit_20261109T055837Z.md` (EXPLORATORY / NOT CONFIRMATORY / NOT PROMOTABLE). New/updated code (registered, tested): `scripts/run_gate4_v4_leakage_audit.py`, `tests/test_gate4_v4_leakage_audit.py` (6 synthetic tests OK), `research_state/tracka_script_scope_registry.json` (+`run_gate4_v4_leakage_audit.py`, `script_count` 114, scope drift PASS). Full suite: **960 tests in 120.0s — OK** (ran after stash/restore of `ironflow_fastpath_cache.json`). `tracka_resume_check.py` → **pass:true, 17/17, network:false, probes==2, writes_real_research_state:false, root_md_json_bounded pass (171/172)**. `tracka_resume_gate.py --json` → **drift_preflight.pass:true, status:BLOCKED, reason_code:PREREG_OR_MANIFEST_BLOCK_AFTER_DRIFT_PASS, outcomes_inspected:false**. `check_tracka_scope_registry_drift.py` → **[PASS] scripts=114 registry=114**. NO-GO formalization present: `research_state/gate4_v4_exploratory_nogo/gate4_v4_exploratory_nogo_20261109T053308Z.{json,md}`, `results/fclr_heavy001/gate4_v4_exploratory_nogo_20261109T053308Z.md`. `research_state/ironflow_fastpath_cache.json` is a local cache mutation — **do not commit**.

---

## 0) INITIAL TASK MESSAGE FOR NEXT AGENTIC SESSION (MANDATORY, HEAVY WORK)

**Session timestamp (initial task):** `2026-11-09T06:05:59Z`

**You MUST execute measurable research/engineering progress. No Track A probing (2026-11..2027-02 absent, probes==2, deadend rubric holds). No new Track C/B sealed outcomes. No workflows/schedulers/pollers/wrappers/controllers. No `.github/workflows` edits. No status-only churn. Every action must produce versioned, auditable artifacts and/or tested code.**

**Campaign (binding constraints):** Gate 4 v4 is `FROZEN_BEFORE_OUTCOMES`, `confirmatory_claim_go=NO_GO`, `exploratory_smoke_authorized_after_freeze=true` (local 2024-04..09 cache; FCLR-015 SHA256 `3e6ac26c...5406c`). **EXPLORATORY / NOT CONFIRMATORY / NOT PROMOTABLE.** Never claim confirmatory GO, economic value, or promotion. Never reuse sealed-anchor domain (FCLR002/003/013). Never replace prereg A–E contrasts or change confirmatory estimands.

**Completed — do not rerun identically:** v4 exec `20261109T004003Z` (inconclusive E vs A, split-3 B/D blowup), diag `20261109T021456Z` (root cause), stab `20261109T045805Z` (**NO-GO**: V3 E vs A +1096 CI [331,2104] worse; B amplified 45→1029; V4 worse; no LOO improvement), NO-GO note `20261109T053308Z`, leakage audit `20261109T055837Z` (**PASS**: train-only provenance invariant, bootstrap deterministic). Artifacts in `research_state/gate4_v4_exploratory_{exec,diag,stab,nogo}/`, `research_state/gate4_v4_leakage_audit/`, `results/fclr_heavy001/`.

**Execute next (highest-value measurable engineering, not more status memos):**
1. **Harden block-bootstrap / inference diagnostics** as tested library code (synthetic only): add explicit checks/tests that CI accounting rejects non-finite diffs, reports effective block count, and flags degenerate/too-few-block regimes — integrate into `scripts/run_funding_ablations.py` helpers or a small `src/eval/` utility with unit tests (no network, no real `research_state` writes). Keep behavior compatible with existing callers.
2. **Add a versioned EXPLORATORY “diagnostic bundle index”** (single markdown under `results/fclr_heavy001/`) that cross-links v4 exec/diag/stab/nogo/leakage artifacts, commands, SHAs, and the explicit no-promotion verdict — **not** a new root `research_state/*.md/json` file if it would pressure the 172 bound (use `results/` or dated subdir only).
3. **Targeted tests first**, then `python -m unittest discover tests` must remain **>=960 OK**. Register any new `scripts/*.py` in `research_state/tracka_script_scope_registry.json` and pass `check_tracka_scope_registry_drift.py`.
4. **Verify invariants:** `python scripts/tracka_resume_check.py` (17/17 pass, probes==2, network:false, root_md_json_bounded pass), `python scripts/tracka_resume_gate.py --json` (BLOCKED, drift_preflight.pass:true, outcomes_inspected:false). **Do not weaken root md+json bound (172).**
5. **Update this handoff** (§1–§10) with exact changes/commands/results/artifact paths/issues/next task. Record session timestamp `2026-11-09T06:05:59Z`.

**Acceptance (heavy work — at least one required):** (A) tested inference/diagnostic hardening merged as code + tests green + invariants green, or (B) a materially different tested engineering task with versioned evidence and suite/invariants green. Sessions without (A)/(B) fail the mandate.

---

## 1. WHAT CHANGED AND WHY (this session, 2026-11-09T06:05:59Z)
- **Added Gate 4 v4 EXPLORATORY leakage audit** (measurable hardening, not status-only): `scripts/run_gate4_v4_leakage_audit.py` verifies train-only provenance of ridge scale, winsor bounds, target floor, and normalization mean/std by perturbing test-fold targets and asserting train-derived params unchanged; also checks block-bootstrap CI reproducibility with fixed deterministic seed (20261109). **All EXPLORATORY / NOT CONFIRMATORY / NOT PROMOTABLE.**
- **Executed audit** on local 2024-04..09 cache (FCLR-015, 5 symbols, prereg v3_30d 4 splits, V1–V4): **leakage_invariance_all=true, bootstrap_reproducible=true**. Versioned artifacts: `research_state/gate4_v4_leakage_audit/gate4_v4_leakage_audit_20261109T055837Z.{json,md}`, `results/fclr_heavy001/gate4_v4_leakage_audit_20261109T055837Z.md`.
- **Added/validated tests**: `tests/test_gate4_v4_leakage_audit.py` (6 synthetic, no network, no real `research_state` writes) — covers label guard, train-only params, test perturbation invariance on normalized-train path, normalization stats, fixed-seed bootstrap reproducibility, all-variant invariance.
- **Scope registry updated**: registered `run_gate4_v4_leakage_audit.py` as `track_c_sealed_volatility` in `research_state/tracka_script_scope_registry.json` (script_count 114); `check_tracka_scope_registry_drift.py` PASS.
- **NO-GO formalization confirmed present** (from prior work, not rerun): `research_state/gate4_v4_exploratory_nogo/gate4_v4_exploratory_nogo_20261109T053308Z.{json,md}`, `results/fclr_heavy001/gate4_v4_exploratory_nogo_20261109T053308Z.md`.
- **Cache hygiene**: `research_state/ironflow_fastpath_cache.json` mutated by test discovery side effects during checks; restored/stashed during verification — **do not commit**.

## 2. WHAT WAS ACTUALLY TESTED — EXACT OUTCOMES
| Check | Command | Result |
|---|---|---|
| Targeted leakage audit | `python -m unittest tests.test_gate4_v4_leakage_audit -v` | **6 tests OK** |
| Targeted Gate 4 v4 suite | `python -m unittest tests.test_gate4_v4_leakage_audit tests.test_gate4_v4_exploratory_stab tests.test_gate4_v4_exploratory_diag -v` | **15 tests OK** |
| Full suite | `python -m unittest discover tests` | **Ran 960 tests in 120.0s — OK** |
| Leakage audit execution | `python scripts/run_gate4_v4_leakage_audit.py --out-suffix 20261109T055837Z` | **EXPLORATORY; leakage_invariance_all:true; bootstrap_reproducible:true** |
| Track A resume check | `python scripts/tracka_resume_check.py` | **pass:true, 17/17, network:false, probes==2, writes_real_research_state:false, root_md_json_bounded pass (171/172)** |
| Track A resume gate | `python scripts/tracka_resume_gate.py --json` | **drift_preflight.pass:true, status:BLOCKED, reason_code:PREREG_OR_MANIFEST_BLOCK_AFTER_DRIFT_PASS, outcomes_inspected:false** |
| Scope registry drift | `python scripts/check_tracka_scope_registry_drift.py` | **[PASS] scripts=114 registry=114 reason=OK** |

## 3. EVIDENCE ADDED / MODIFIED (paths)
| Path | Change |
|---|---|
| `scripts/run_gate4_v4_leakage_audit.py` | **Created** — EXPLORATORY leakage-audit harness (train-only provenance + bootstrap reproducibility, versioned outputs) |
| `tests/test_gate4_v4_leakage_audit.py` | **Created** — 6 synthetic tests (no network, no real research_state writes) |
| `research_state/gate4_v4_leakage_audit/gate4_v4_leakage_audit_20261109T055837Z.json` | **Created** — full audit JSON (all V1–V4 × 4 splits × 5 symbols invariant) |
| `research_state/gate4_v4_leakage_audit/gate4_v4_leakage_audit_20261109T055837Z.md` | **Created** — markdown audit report |
| `results/fclr_heavy001/gate4_v4_leakage_audit_20261109T055837Z.md` | **Created** — results copy for audit trail |
| `research_state/tracka_script_scope_registry.json` | **Modified** — registered `run_gate4_v4_leakage_audit.py` (`track_c_sealed_volatility`, script_count 114) |
| `AGENT_HANDOFF.md` | **Updated** — session `2026-11-09T06:05:59Z`, evidence, gates, next campaign |
| `research_state/gate4_v4_exploratory_nogo/gate4_v4_exploratory_nogo_20261109T053308Z.{json,md}` | **Present (prior)** — EXPLORATORY NO-GO formalization (not rerun) |
| `research_state/ironflow_fastpath_cache.json` | **Cache mutation observed during checks; do not commit** |

## 4. CURRENT STATE OF EACH RESEARCH GATE
| Gate | Status | Evidence / Notes |
|---|---|---|
| **Gate 1 (Data Loadable)** | Track A **BLOCKED** (no admissible unauth liquidation labels). Track C historical/sealed. Gate 4 exploratory local 2024-04..09 cache present (FCLR-015). | `track_a_deadend_map.md`; `data_cache/*_2024_04..09` |
| **Gate 2 (Protocol Frozen)** | PASSED Track C context; Gate 4 v4 **FROZEN_BEFORE_OUTCOMES**, `confirmatory_claim_go=NO_GO`, exploratory-only on 2024-04..09 (sealed-anchor conflict). | `pre_registration_gate4_funding_multisplit_v4_20261107T1845Z.json` |
| **Gate 3 (RV-only Baseline)** | Track C historical PASSED / **forward INCONCLUSIVE** (0 non-overlapping 30d blocks). | `evaluation_summary_FCLR-012-V.md` |
| **Gate 4 (Incremental Funding/Price)** | **EXPLORATORY NO-GO CONFIRMED** on local 2024-04..09 (stab `20261109T045805Z`: V3 E vs A +1096 CI [331,2104] worse; B amplified; V4 worse; no LOO improvement). **Leakage controls audited PASS (EXPLORATORY diagnostic)** — leakage audit `20261109T055837Z`. All **NOT CONFIRMATORY / NOT PROMOTABLE**. | `research_state/gate4_v4_exploratory_stab/*`, `research_state/gate4_v4_exploratory_nogo/*`, `research_state/gate4_v4_leakage_audit/*` |
| **Forecast Gate** | **NOT ELIGIBLE**. No confirmatory promotion. | frontier/negative results |

## 5. SINGLE HIGHEST-VALUE NEXT TASK
**Harden block-bootstrap/inference diagnostics as tested code** (synthetic, no network, no real `research_state` writes): make `block_bootstrap_delta_ci`/paired helpers explicitly reject non-finite diffs, surface effective block count, and flag degenerate/too-few-block regimes with unit tests; keep existing-caller behavior compatible. Add a **versioned diagnostic bundle index** in `results/fclr_heavy001/` (no root `research_state` md/json pressure). Register any new script, keep suite **>=960 OK**, and keep all Track A/root-bound invariants green.

## 6. PRECISE VERIFICATION COMMANDS
```bash
git --no-pager status --short
python -m unittest tests.test_gate4_v4_leakage_audit -v
python -m unittest discover tests                         # expect >=960 OK
python scripts/run_gate4_v4_leakage_audit.py --out-suffix <TS>  # EXPLORATORY; expect leakage_invariance_all true, bootstrap_reproducible true
python scripts/tracka_resume_check.py                    # expect pass:true, 17/17, probes==2, root_md_json_bounded pass (<=172)
python scripts/tracka_resume_gate.py --json              # expect BLOCKED, drift_preflight.pass:true, outcomes_inspected:false
python scripts/check_tracka_scope_registry_drift.py      # expect PASS
ls research_state/gate4_v4_leakage_audit/ results/fclr_heavy001/gate4_v4_leakage_audit_*.md
```

## 7. BLOCKERS / CONSTRAINTS
| Blocker | Evidence | Allowed next route |
|---|---|---|
| Track A: no admissible liquidation labels | `track_a_deadend_map.md`, NO-GO rubric, probes==2, 2026-11..2027-02 absent | Guard hardening only if specific gap; **no** re-probe absent months |
| Track C: forward inconclusive (0 non-overlapping 30d blocks) | FCLR-012-V | New admissible panel meeting criteria; do not relax |
| Gate 4 v4: sealed-anchor conflict; confirmatory_claim_go NO_GO | v4 prereg | **EXPLORATORY only**, explicit labels, no promotion/sealed-anchor reuse |
| Gate 4 v4: funding ablations NO-GO on 2024-04..09 | stab `20261109T045805Z`, nogo `20261109T053308Z` | No improvement claim; pivot to tested engineering/diagnostics |
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
2. Inspect `research_state/experiment_frontier.json`, latest manifests/tests/cache, `gate4_v4_exploratory_{stab,nogo}`, `gate4_v4_leakage_audit`.
3. Execute §0 (measurable task). Cheapest checks first. Update **this file** with exact evidence + session timestamp `2026-11-09T06:05:59Z`.

## 10. NEXT SESSION DELIVERABLE
Updated `AGENT_HANDOFF.md` with tested inference/diagnostic hardening (or materially different tested engineering) + versioned artifacts, suite **>=960 OK**, scope drift PASS, Track A invariants green (17/17, probes==2, root bound <=172), and the next unfinished task — **session timestamp `2026-11-09T06:05:59Z` recorded, acceptance (A)/(B) satisfied**. Repo must remain continuable without user repeating instructions.

---
**END OF SINGLE DURABLE HANDOFF.**