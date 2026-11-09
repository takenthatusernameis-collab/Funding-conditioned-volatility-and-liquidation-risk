# AGENT_HANDOFF.md — Single Durable Handoff (next session must continue from here)

**Generated:** 2026-11-09T04:58:05Z
**Repository:** Funding-conditioned-volatility-and-liquidation-risk
**Priority (reconciled):** Repo P0 = Gate 4 funding-conditioned volatility work on local admissible 2024-04..09 data (measurable, unblocked, EXPLORATORY only). Track A = structurally blocked / no trigger (lockdown hardening only if specific gap); Track C sealed/inconclusive forward; Track B NOT_SUPPORTED. **No status-only churn. No avoiding heavy work — every session must produce versioned, auditable artifacts.**
**Verified this session (baseline/evidence):** Gate 4 v4 EXPLORATORY stabilized comparison executed (V1/V2/V3/V4 variants). **EXPLORATORY NO-GO signal confirmed**: principled stabilization (scale-aware ridge + train-only target-scale floor) made E vs A ΔQLIKE catastrophically worse (V1: +0.488 CI [-0.042,1.197] inconclusive → V3: +1096 CI [331,2104] significantly worse). B vs A blowup amplified (V1 split 3 B QLIKE 45 → V3 1029). Test suite **960 OK**. `tracka_resume_check.py` → **pass:true, network:false, probes==2, writes_real_research_state:false, root_md_json_bounded pass (171/172)**. `tracka_resume_gate.py --json` → **drift_preflight.pass:true, status:BLOCKED, reason_code:PREREG_OR_MANIFEST_BLOCK_AFTER_DRIFT_PASS, outcomes_inspected:false**. `check_tracka_scope_registry_drift.py` → **[PASS] scope-registry drift: scripts=112 registry=112 reason=OK**. Local 2024-04..09 cache used; v4 prereg FROZEN_BEFORE_OUTCOMES, confirmatory_claim_go=NO_GO, exploratory_smoke_authorized_after_freeze=true. Git status clean at SHA `d7a764b9e9411f58b8dca3abe8251f6780c5d6d4` (modified: `research_state/ironflow_fastpath_cache.json` — cache, do not commit).

---

## 0) INITIAL TASK MESSAGE FOR NEXT AGENTIC SESSION (MANDATORY, HEAVY WORK)

**You MUST execute measurable research/engineering progress in this session. Do not probe absent Track A months (2026-11..2027-02). Do not add workflows/schedulers/pollers/wrappers/controllers. Do not touch `.github/workflows`. Status-only probing, blocker-memos without execution, and waiting on user instructions are not acceptable — produce versioned artifacts.**

**Session timestamp (initial task):** `2026-11-09T04:58:05Z`

### Campaign: Gate 4 v4 EXPLORATORY NO-GO formalization + pivot to measurable local engineering task (Track C-adjacent or hardening)

**Intent/constraints (binding):** `research_state/pre_registration_gate4_funding_multisplit_v4_20261107T1845Z.json` is `FROZEN_BEFORE_OUTCOMES`, `confirmatory_claim_go=NO_GO`, `exploratory_smoke_authorized_after_freeze=true`. Sealed-anchor conflict with FCLR002/003/013 domain family applies. **All outputs MUST be labeled EXPLORATORY / NOT CONFIRMATORY / NOT PROMOTABLE.** Never claim confirmatory GO, economic value, or promotion. **Do not replace prereg A–E contrasts or change confirmatory estimands.**

**Completed (do not rerun identically; build on it):**
- Exec `20261109T004003Z` (SHA `2f21b1dd4`): E vs A ΔQLIKE +0.4879, 95% block CI [-0.04216,1.19734] (spans 0, n=12969, 120 blocks) — **INCONCLUSIVE**. B/D unstable (split 3 B vs A Δ=44.69, D vs A Δ=10.33). Artifacts: `results/fclr_heavy001/gate4_v4_exploratory_exec_20261109T004003Z.md`, `research_state/gate4_v4_exploratory_exec/*`.
- Diag `20261109T021456Z` (SHA `2f21b1dd4`): reproduced E vs A +0.487902 CI [-0.042161,1.197338]. **Root-cause evidence (split 3, 2024-08-13..2024-09-11):** funding-augmented direct-variance OLS extrapolates to negative/near-zero variance under small target scale + tiny ridge (`1e-10*I`) + train-only standardization; floor-at-zero removes invalids but remaining near-zero positives and concentrated blowups dominate QLIKE. B BTC QLIKE mean 225.80 (raw_neg 89/720, raw_min -0.000527); D SOL 56.34 / BTC 1.68 with many raw negatives and larger `coef_l2`. E has no catastrophic single-instrument blowup but many raw negatives (622) and is worse than A. **E vs A LOO (EXPLORATORY):** all +0.488 inconclusive; drop XRP attenuates to +0.111 CI [-0.129,0.358] (inconclusive); other drops make harm CI>0; no LOO shows improvement. **Naive stabilized comparison (strong ridge + pred_floor=1e-8, EXPLORATORY only, NOT a prereg replacement) catastrophically worse** (Δ +9213.35) — do not use. Artifacts: `results/fclr_heavy001/gate4_v4_exploratory_diag_20261109T021456Z.md`, `research_state/gate4_v4_exploratory_diag/gate4_v4_exploratory_diag_20261109T021456Z.json`, `scripts/run_gate4_v4_exploratory_diag.py`, `tests/test_gate4_v4_exploratory_diag.py`.
- **Stabilized comparison `20261109T045805Z` (SHA `d7a764b9e`):** **EXPLORATORY NO-GO CONFIRMED**. Four variants evaluated (V1_primary, V2_scale_ridge, V3_scale_ridge_target_floor, V4_winsor_train) on 4×30-day splits (2024-04..09, 5 symbols). **Key result:** V3 (scale-aware ridge `1e-8*max(trace(X'X)/k,1)` + train-only floor `1e-4*train_target_median`) made E vs A ΔQLIKE **+1096** (CI [331,2104], significantly worse) vs V1 +0.488 (inconclusive). B vs A amplified from 45 to 1029 (split 3). V2 similar to V1 (ridge alone insufficient). V4 (winsor) even worse. **No variant shows improvement; all funding ablations (B/C/D/E) worse or inconclusive vs A.** LOO (V3) confirms no instrument drop yields improvement. Artifacts: `results/fclr_heavy001/gate4_v4_exploratory_stab_20261109T045805Z.md`, `research_state/gate4_v4_exploratory_stab/gate4_v4_exploratory_stab_20261109T045805Z.json`, `scripts/run_gate4_v4_exploratory_stab.py`, `tests/test_gate4_v4_exploratory_stab.py` (6 tests added, all passing).

**Execute next (versioned suffix, do not overwrite prior outputs):**
1. **Formalize EXPLORATORY NO-GO note** for funding ablations on local 2024-04..09 slice (concise, versioned, NOT confirmatory, no sealed-anchor reuse). Document that principled leakage-safe stabilization (scale-aware ridge, train-only target-scale floor, train-only winsor) fails to improve and catastrophically degrades out-of-sample QLIKE vs RV-only baseline.
2. **Pivot to most measurable open Gate 4/Track C-adjacent local engineering task** supported by tests (e.g., leakage audit hardening, walkforward infrastructure, block bootstrap diagnostics, feature engineering robustness). No Track A probing. No Track C/B sealed work.
3. **Run targeted unit tests** for any new code (synthetic, no network, no real research_state writes), then `python -m unittest discover tests` must remain **>=960 OK** (fix regressions you introduce).
4. **Write versioned artifacts** under subdirs (`research_state/gate4_v4_exploratory_nogo/`, `results/fclr_heavy001/`) with commands, git SHA, tables, explicit NOT CONFIRMATORY/NOT PROMOTABLE verdict. **Do not weaken `tracka_resume_check` root md+json bound (172) or any Track A invariant.**
5. **Re-run** `python scripts/tracka_resume_check.py` and `python scripts/tracka_resume_gate.py --json` — expect 17/17 pass, probes==2, root bound satisfied, BLOCKED with `outcomes_inspected:false`.
6. **Update this handoff** (§1–§10) with exact changes, commands, results, artifact paths, uncovered issues, and the next unfinished task.

**Acceptance for next session (heavy work — at least one required):** (A) versioned EXPLORATORY NO-GO note with evidence, (B) new tested hardening/engineering work with suite green and Track A invariants green — with exact evidence and the session timestamp `2026-11-09T04:58:05Z` recorded in this handoff. A session that ends without one of (A)/(B) has not satisfied the heavy-work mandate.

---

## 1. WHAT CHANGED AND WHY (this session)
- **Executed Gate 4 v4 EXPLORATORY stabilized comparison** (V1/V2/V3/V4) on local 2024-04..09 cache per §0 campaign.
- **EXPLORATORY NO-GO CONFIRMED**: Principled stabilization (scale-aware ridge + train-only target-scale floor + optional train-only winsor) catastrophically degrades out-of-sample QLIKE vs RV-only baseline (A). E vs A ΔQLIKE V1=+0.488 (inconclusive) → V3=+1096 (significantly worse, CI entirely >0). B vs A split 3 QLIKE 45 → 1029.
- **Fixed test file indentation bug** in `tests/test_gate4_v4_exploratory_stab.py` (dict structure corrected) and updated `_toy()` split to use time-based split for proper symbol coverage.
- **Test suite expanded**: 960 tests OK (954 baseline + 6 new stab tests).
- **All verification invariants green**: tracka_resume_check 17/17 pass, tracka_resume_gate BLOCKED (prereg required), scope registry drift PASS (112/112), root_md_json_bounded 171/172.
- **Artifacts produced**: JSON + markdown in `research_state/gate4_v4_exploratory_stab/` and `results/fclr_heavy001/` with versioned suffix `20261109T045805Z`.

## 2. WHAT WAS ACTUALLY TESTED — EXACT OUTCOMES
| Check | Command | Result |
|---|---|---|
| Full suite | `python -m unittest discover tests` | **Ran 960 tests in 120.195s — OK** |
| Track A resume check | `python scripts/tracka_resume_check.py` | **pass:true**, network:false, probes==2, `writes_real_research_state:false`, `root_md_json_bounded` pass (171/172) |
| Track A resume gate | `python scripts/tracka_resume_gate.py --json` | **drift_preflight.pass:true**, `status:BLOCKED`, `reason_code:PREREG_OR_MANIFEST_BLOCK_AFTER_DRIFT_PASS`, `outcomes_inspected:false` |
| Scope registry drift | `python scripts/check_tracka_scope_registry_drift.py` | **[PASS] scope-registry drift: scripts=112 registry=112 reason=OK** |
| Gate 4 v4 stab variants | `python scripts/run_gate4_v4_exploratory_stab.py --out-suffix 20261109T045805Z` | **EXPLORATORY NO-GO**: V3 E vs A ΔQLIKE +1096 CI [331,2104] (worse), B vs A 45→1029 (split 3), no LOO improvement |

## 3. EVIDENCE ADDED / MODIFIED (paths)
| Path | Change |
|---|---|
| `scripts/run_gate4_v4_exploratory_stab.py` | **Created** — Gate 4 v4 EXPLORATORY stabilized comparison (V1/V2/V3/V4 variants, leakage-safe, versioned outputs) |
| `tests/test_gate4_v4_exploratory_stab.py` | **Fixed** — indentation bug in test payload dict, time-based split in `_toy()`, all 6 tests passing |
| `research_state/gate4_v4_exploratory_stab/gate4_v4_exploratory_stab_20261109T045805Z.json` | **Created** — full diagnostic JSON with variants, contrasts, LOO, per-split diagnostics |
| `research_state/gate4_v4_exploratory_stab/gate4_v4_exploratory_stab_20261109T045805Z.md` | **Created** — markdown report with tables, interpretation, EXPLORATORY NO-GO signal |
| `results/fclr_heavy001/gate4_v4_exploratory_stab_20261109T045805Z.md` | **Created** — copy in results directory for audit trail |
| `AGENT_HANDOFF.md` | **Updated** — session timestamp `2026-11-09T04:58:05Z`, NO-GO evidence, updated gates, next campaign |

## 4. CURRENT STATE OF EACH RESEARCH GATE
| Gate | Status | Evidence / Notes |
|---|---|---|
| **Gate 1 (Data Loadable)** | Track A: **BLOCKED** (no admissible unauth liquidation labels). Track C: PASSED (historical) / sealed. Gate 4 exploratory: local 2024-04..09 cache present (FCLR-015). | `track_a_deadend_map.md`; FCLR-015 manifest SHA256 `3e6ac26c...5406c`; `research_state/data_cache/*_2024_04..09` |
| **Gate 2 (Protocol Frozen)** | PASSED (Track C FCLR-001 context); Gate 4 v4 prereg **FROZEN_BEFORE_OUTCOMES** but `confirmatory_claim_go=NO_GO`, exploratory-only on 2024-04..09 due to sealed-anchor conflict. | `pre_registration_gate4_funding_multisplit_v4_20261107T1845Z.json` |
| **Gate 3 (RV-only Baseline)** | Track C: PASSED historical / **INCONCLUSIVE forward** (5-day test window, 0 non-overlapping 30d blocks). | `evaluation_summary_FCLR-012-V.md` |
| **Gate 4 (Incremental Funding/Price)** | **EXPLORATORY NO-GO CONFIRMED** — V1 E vs A inconclusive (CI spans 0); V2 (scale ridge) ≈ V1; V3 (scale ridge + train-only target floor) catastrophically worse (+1096, CI>0); V4 (winsor) worse. B/D blowups amplified. No variant improves vs A. All EXPLORATORY / NOT CONFIRMATORY / NOT PROMOTABLE. | `results/fclr_heavy001/gate4_v4_exploratory_stab_20261109T045805Z.md`; `research_state/gate4_v4_exploratory_stab/gate4_v4_exploratory_stab_20261109T045805Z.json` |
| **Forecast Gate** | **NOT ELIGIBLE** (Track C forward Gate 3 inconclusive; Track A blocked). No confirmatory promotion from v4 exploratory runs. | frontier/negative results |

## 5. SINGLE HIGHEST-VALUE NEXT TASK
**Formalize EXPLORATORY NO-GO note** for Gate 4 funding ablations on local 2024-04..09 slice (concise, versioned, explicit NOT CONFIRMATORY labeling), then **pivot to measurable local engineering task** (leakage audit hardening, walkforward diagnostics, block bootstrap robustness, or feature engineering tests) with suite ≥960 OK and Track A invariants green. No Track A probing. No Track C/B sealed work.

## 6. PRECISE VERIFICATION COMMANDS
```bash
git --no-pager status --short
python -m unittest discover tests                         # expect >=960 OK
python scripts/tracka_resume_check.py                    # expect pass:true, 17/17, probes==2, network:false, root_md_json_bounded pass
python scripts/tracka_resume_gate.py --json              # expect BLOCKED, drift_preflight.pass:true, outcomes_inspected:false
python scripts/check_tracka_scope_registry_drift.py      # expect PASS
ls results/fclr_heavy001/gate4_v4_exploratory_stab_20261109T045805Z.md
ls research_state/gate4_v4_exploratory_stab/
```

## 7. BLOCKERS / CONSTRAINTS
| Blocker | Evidence | Allowed next route |
|---|---|---|
| Track A: no admissible liquidation labels | `track_a_deadend_map.md`, rubric NO-GO all 8 candidates; probes==2; 2026-11..2027-02 absent | **Only** if a genuinely new unauth source meets full rubric; else guard hardening only. No re-probe absent months. |
| Track C: forward panel ends 2026-11-02, 0 non-overlapping 30d test blocks | `fclr012v_coverage_audit.json`, FCLR-012-V inconclusive | New admissible panel with real volume, ≥3 non-overlapping 30d blocks; do not relax criteria. |
| Gate 4 v4: sealed-anchor conflict on 2024 slice | v4 prereg `confirmatory_claim_go:NO_GO` | Run as **EXPLORATORY only**, explicit labeling, no promotion. |
| Gate 4 v4: NO-GO confirmed for funding ablations | stab `20261109T045805Z`: V3 E vs A +1096 CI>0, B vs A amplified | Formalize NO-GO note; pivot to engineering hardening. Do not claim improvement. |
| Track A root md+json bound | `scripts/tracka_resume_check.py` cap 172 | Put new exploratory artifacts in subdirs/results; **do not weaken bound/check**. |
| Protected control plane | repo instructions | **No `.github/workflows` edits** without explicit maintainer authorization. |

## 8. DO NOT DO
- ❌ Re-probe 2026-11..2027-02 / create new probe/scan/wrapper/report families for Track A
- ❌ Workflows/schedulers/pollers/status-only files/controllers
- ❌ Track C/B new work (sealed/NOT_SUPPORTED) except documenting hard blockers
- ❌ Conflate observed/modeled/synthetic labels; no threshold-shopping/holdout reuse
- ❌ Commit `__pycache__/`, `research_state/ironflow_fastpath_cache.json`, large raw caches
- ❌ Weaken `root_md_json_bounded` or Track A invariants to accommodate artifacts
- ❌ Claim confirmatory GO/promotion from v4 exploratory runs
- ❌ Live/paper trading, order endpoints, credentials, bypassing access controls

## 9. SESSION START PROTOCOL (mandatory)
1. `git pull` + `git status`; read **this file** + `RESEARCH_PROMPT.md`.
2. Inspect `research_state/experiment_frontier.json`, latest manifests, tests, data cache state, `research_state/gate4_v4_exploratory_stab/`.
3. Execute §0 (highest-value measurable task). Run cheapest checks first.
4. Update **this file** with exact changes/commands/results/evidence/gates/next task + blockers.

## 10. NEXT SESSION DELIVERABLE
Updated `AGENT_HANDOFF.md` with Gate 4 v4 EXPLORATORY NO-GO note formalized, new tested hardening/engineering work with suite ≥960 OK and Track A invariants green, artifact paths, root-bound compliance, and the next unfinished task — **session timestamp `2026-11-09T04:58:05Z` recorded, at least one of acceptance (A)/(B) produced**. **Repo state must remain continuable without user repeating instructions.**

---
**END OF SINGLE DURABLE HANDOFF.**