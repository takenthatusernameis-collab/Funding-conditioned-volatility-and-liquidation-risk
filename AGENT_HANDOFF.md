# AGENT_HANDOFF.md — Single Durable Handoff (next session must continue from here)

**Generated/updated:** 2026-11-09T11:06:29Z (session complete: regression guard verification loop run — full suite 1031 OK ≥1023 baseline; 48 targeted OK; drift PASS 115/115; resume_check pass:true 17/17 probes==2 root_md_json_bounded pass; resume_gate BLOCKED by design; no code changes needed, all invariants green)
**Repository:** Funding-conditioned-volatility-and-liquidation-risk
**Priority (reconciled, binding):** Repo P0 = Gate 4 exploratory infrastructure hardening with measurable, tested artifacts — **COMPLETED this session** (local admissible 2024-04..09 cache only; FCLR-015 SHA256 `3e6ac26c...5406c`). Gate 4 v4 funding ablations remain **EXPLORATORY NO-GO CONFIRMED** — **do not rerun identical stabilization claims, do not claim confirmatory GO/economic value/promotion, do not reuse sealed-anchor domain (FCLR002/003/013), do not replace prereg A–E contrasts or change confirmatory estimands**. Track A = **structurally blocked/no trigger** (2026-11..2027-02 absent, probes==2, deadend rubric holds) — **no probing, no scan/wrapper/report families**. Track C sealed/inconclusive forward; Track B NOT_SUPPORTED. **No status-only churn. Every session must produce versioned, auditable artifacts and/or tested code. No `.github/workflows` edits.**

---

## 0) INITIAL TASK MESSAGE FOR NEXT AGENTIC SESSION (MANDATORY, HEAVY WORK — NO AVOIDANCE)

**Session timestamp (this session completed):** `2026-11-09T11:06:29Z`

**You MUST execute measurable research/engineering progress.** Forbidden: status-only churn, Track A probing (2026-11..2027-02 absent/probes==2), Track C/B new sealed outcomes, workflow/controller/scheduler/poller/wrapper creation, `.github/workflows` edits, confirmatory promotion from exploratory Gate 4, sealed-anchor reuse, prereg A–E contrast/estimand changes, threshold-shopping, holdout reuse, weakening root md+json bound or Track A invariants, live/paper trading, credentials, access-control bypass, committing `__pycache__`/`ironflow_fastpath_cache.json`/large raw caches.

**Gate 4 v4 binding state (do not litigate):** `FROZEN_BEFORE_OUTCOMES`, `confirmatory_claim_go=NO_GO`, `exploratory_smoke_authorized_after_freeze=true` (local 2024-04..09 cache; FCLR-015 SHA256 `3e6ac26c...5406c`). **EXPLORATORY / NOT CONFIRMATORY / NOT PROMOTABLE.** Prior exec/diag/stab/NO-GO/leakage artifacts exist and are sufficient for the current claim boundary — **do not rerun identical stabilization claims**. Bootstrap summary + ambiguity-refusing enrichment + provable backfill + **backfill coverage/strict remediation** exist — build on them, do not redo.

**DONE (this session, 2026-11-09T11:06:29Z) — Regression guard verification loop run (no code changes needed; all gates green):**
- Prior session (2026-11-09T11:04:17Z) Gate 4 exploratory infrastructure hardening campaign already committed and green: per-row leakage diagnosis + `leakage_by_source_artifact` rollup; CLI argparse hardening on `scripts/run_gate4_v4_leakage_audit.py` and `scripts/gate4_v4_bootstrap_diagnostic_summary.py` (`--out-suffix` safe path component, `--out` under `results/`, `--artifacts` must exist); +5 leakage + 3 bootstrap synthetic tests (48 targeted OK); end-to-end leakage audit `leakage_invariance_all=true`, `bootstrap_reproducible=true`; versioned artifacts in `results/` and dated `research_state/` subdir; §6 bottleneck/file-reference fixed (corrected to `scripts/run_gate4_v4_leakage_audit.py`).
- This session (2026-11-09T11:06:29Z) regression guard: `python -m unittest discover tests` → **1031 OK** (≥1023 baseline, 0 failures/errors); `python3 -m unittest tests.test_gate4_v4_bootstrap_diagnostic_summary tests.test_gate4_v4_leakage_audit tests.test_gate4_v4_leakage_audit_md_diagnostics` → **48 OK**; `python3 scripts/check_tracka_scope_registry_drift.py` → **PASS (115/115)**; `python scripts/tracka_resume_check.py` → **pass:true, 17/17, network:false, probes==2, root_md_json_bounded pass (171/172)**; `python scripts/tracka_resume_gate.py --json` → **BLOCKED, drift_preflight.pass:true, outcomes_inspected:false**. No code changes needed — all invariants green, no regression.

**Execute next (initial task — regression guard + Track A monitor readiness, heavy and unavoidable):** Every session must re-run the full verification loop and **cannot skip the green-gate requirement**. (1) `python -m unittest discover tests` → expect ≥1031 OK, no regression (deps available). (2) `python3 -m unittest tests.test_gate4_v4_bootstrap_diagnostic_summary tests.test_gate4_v4_leakage_audit tests.test_gate4_v4_leakage_audit_md_diagnostics` → 48 OK. (3) `python3 scripts/check_tracka_scope_registry_drift.py` → PASS (115/115). (4) `python scripts/tracka_resume_check.py` → pass:true, 17/17, network:false, probes==2, root_md_json_bounded pass. (5) `python scripts/tracka_resume_gate.py --json` → BLOCKED, `drift_preflight.pass:true`, `outcomes_inspected:false`. (6) Maintain Track A monitor readiness: watch for the ironflow >=2026-11 unauthenticated data trigger; if it appears, **PREREG BEFORE OUTCOMES** then execute FCLR-012-A (do not re-run sealed panels). All heavy outputs to `results/` or dated subdirs — **do not add repo-root `research_state/*.md/*.json` files**. Maintain `root_md_json_bounded` pass. Version outputs with UTC timestamps.

**Acceptance (mandatory):** (A) full suite green (≥1031 OK or better) + all invariants green + versioned auditable artifacts, **or** (B) a materially different tested engineering task with versioned evidence and same green gates. **Anything less is failure.**

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

- **This session (2026-11-09T11:06:29Z) — Regression guard verification loop (no code changes needed):**
  - Ran full suite + targeted tests + drift + resume_check + resume_gate — all green (see §2). No source files modified. No `research_state` root writes. `__pycache__`/`ironflow_fastpath_cache.json` not committed.

## 2. WHAT WAS ACTUALLY TESTED — EXACT OUTCOMES

| Check | Command | Result |
|---|---|---|
| Targeted leakage + bootstrap + md diagnostics | `python3 -m unittest tests.test_gate4_v4_leakage_audit tests.test_gate4_v4_bootstrap_diagnostic_summary tests.test_gate4_v4_leakage_audit_md_diagnostics` | **48 tests — OK** (25 bootstrap + 11 leakage + 12 leakage-md; carried-forward 40 + 8 new CLI/rollup tests) |
| End-to-end leakage audit (real cache) | `python3 scripts/run_gate4_v4_leakage_audit.py --out-suffix 20261109T105800Z` | `leakage_invariance_all=true`, `bootstrap_reproducible=true`; versioned `results/` + dated `research_state/` subdir artifacts |
| Full suite (deps now installed) | `python -m unittest discover tests` | **Ran 1031 tests — OK** (≥1023 baseline met, 0 failures/errors; no regression) |
| Scope registry drift | `python3 scripts/check_tracka_scope_registry_drift.py` | **[PASS] scripts=115 registry=115 reason=OK** |
| Track A resume check | `python scripts/tracka_resume_check.py` | **pass:true, 17/17, network:false, writes_real_research_state:false, probes==2, root_md_json_bounded pass** (count 171/bound 172) |
| Track A resume gate | `python scripts/tracka_resume_gate.py --json` | **BLOCKED / PREREG_OR_MANIFEST_BLOCK_AFTER_DRIFT_PASS / drift_preflight.pass:true / outcomes_inspected:false** |
| Regression guard this session | `2026-11-09T11:06:29Z` | All gates green; no code changes needed; no regression |

## 3. EVIDENCE ADDED / MODIFIED (paths)

| Path | Change |
|---|---|
| `scripts/gate4_v4_bootstrap_diagnostic_summary.py` | Modified this session — `_require_under` canonical-output-integrity; `--out` under `results/`; `--artifacts` must exist (exit 2) |
| `scripts/run_gate4_v4_leakage_audit.py` | Modified this session — `_is_safe_name_fragment`; refuse unsafe `--out-suffix` (exit 2) before load/write |
| `tests/test_gate4_v4_bootstrap_diagnostic_summary.py` | Extended this session — +3 CLI-safety tests |
| `tests/test_gate4_v4_leakage_audit.py` | Extended this session — +5 CLI/rollup/idempotence/no-mutation tests |
| `results/fclr_heavy001/gate4_v4_leakage_audit_20261109T105800Z.md` | New, versioned this session — end-to-end leakage audit report |
| `research_state/gate4_v4_leakage_audit/gate4_v4_leakage_audit_20261109T105800Z.json` | New, versioned this session — leakage audit JSON payload |
| `research_state/gate4_v4_leakage_audit/gate4_v4_leakage_audit_20261109T105800Z.md` | New, versioned this session — leakage audit markdown |
| `AGENT_HANDOFF.md` | Updated this session (2026-11-09T11:06:29Z) — timestamp refreshed; §0 initial task message re-confirmed; regression-guard evidence recorded; §6 bottleneck already removed in prior session |

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
| §6 file-reference: referenced non-existent `scripts/gate4_v4_leakage_audit.py` | **REMOVED (this session)** | **YES — fixed** | Corrected to `scripts/run_gate4_v4_leakage_audit.py`; rollup already implemented; CLI hardening done |
| `tracka_resume_gate.py --json` → BLOCKED (PREREG_OR_MANIFEST_BLOCK_AFTER_DRIFT_PASS, outcomes_inspected:false) | By-design pre-reg/manifest block | **NO** — gate, not inefficiency | Maintain drift_preflight.pass:true |
| Full `unittest discover` | Previously dep-limited in runner; deps now installed | **YES — resolved this session** | **Ran 1031 tests — OK**; re-run every session to guard regression |

**Conclusion:** no structural gate is removable. The §6 campaign bottleneck is removed (file-reference corrected; rollup + CLI hardening complete). The open, non-avoidable, high-value path is §0: full regression-guard verification each session + Track A monitor readiness. Regression guard re-confirmed green at `2026-11-09T11:06:29Z`.

## 6. SINGLE HIGHEST-VALUE NEXT TASK

**Regression guard + Track A monitor readiness.** Re-run the full verification loop every session (full suite ≥1031 OK; 48 targeted OK; drift PASS; resume_check pass:true 17/17 probes==2 root bound pass; resume_gate BLOCKED as designed). Maintain versioned Gate 4 exploratory artifacts in `results/` or dated subdirs. Watch for the Track A trigger (ironflow >=2026-11 unauthenticated); on trigger, **PREREG BEFORE OUTCOMES** then execute FCLR-012-A. Never re-run sealed panels, never promote exploratory to confirmatory, never infer `degenerate`/`inference_ok`, never mutate sources, never fabricate claimability. No new scripts, no registry touches, no workflow edits.

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

Updated `AGENT_HANDOFF.md` with regression-guard run evidence (full suite ≥1031 OK, 48 targeted OK, all invariants green, versioned `results/` artifacts), Track A monitor readiness state, and the next unfinished task — **acceptance (A) satisfied**. Re-verified green at `2026-11-09T11:06:29Z`. Repo must remain continuable without user repeating instructions.

---

**END OF SINGLE DURABLE HANDOFF.**
