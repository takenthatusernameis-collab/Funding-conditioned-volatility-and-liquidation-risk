# AGENT_HANDOFF.md — Single Durable Handoff (next session must continue from here)

**Generated:** 2026-11-09T03:22:50Z
**Repository:** Funding-conditioned-volatility-and-liquidation-risk
**Priority (reconciled):** Repo P0 = Gate 4 funding-conditioned volatility work on local admissible 2024-04..09 data (measurable, unblocked, EXPLORATORY only). Track A = structurally blocked / no trigger (lockdown hardening only if specific gap); Track C sealed/inconclusive forward; Track B NOT_SUPPORTED. **No status-only churn. No avoiding heavy work — every session must produce versioned, auditable artifacts.**
**Verified this session (baseline/evidence):** Gate 4 v4 EXPLORATORY diagnostic artifacts exist and are versioned explaining B/D split-3 instability + E vs A LOO/robustness (all **EXPLORATORY / NOT CONFIRMATORY / NOT PROMOTABLE**). `python -m unittest discover tests` → **Ran 954 tests in 111.471s — OK**. `tracka_resume_check.py` → **pass:true, network:false, probes==2, writes_real_research_state:false, root_md_json_bounded pass (171/172)**. `tracka_resume_gate.py --json` → **drift_preflight.pass:true, status:BLOCKED, reason_code:PREREG_OR_MANIFEST_BLOCK_AFTER_DRIFT_PASS, outcomes_inspected:false**. `check_tracka_scope_registry_drift.py` → **[PASS] scope-registry drift: scripts=112 registry=112 reason=OK**. Local 2024-04..09 cache used; v4 prereg FROZEN_BEFORE_OUTCOMES, confirmatory_claim_go=NO_GO, exploratory_smoke_authorized_after_freeze=true. Git status clean at SHA `6a97185ade7938f86585e2c80c6a406f1fa2b588`.

---

## 0) INITIAL TASK MESSAGE FOR NEXT AGENTIC SESSION (MANDATORY, HEAVY WORK)

**You MUST execute measurable research/engineering progress in this session. Do not probe absent Track A months (2026-11..2027-02). Do not add workflows/schedulers/pollers/wrappers/controllers. Do not touch `.github/workflows`. Status-only probing, blocker-memos without execution, and waiting on user instructions are not acceptable — produce versioned artifacts.**

**Session timestamp (initial task):** `2026-11-09T03:22:50Z`

### Campaign: Gate 4 v4 follow-through — decide/execute next prereg-scoped EXPLORATORY modeling fix OR formalize NO-GO (local 2024-04..09) — produce versioned, auditable artifacts

**Intent/constraints (binding):** `research_state/pre_registration_gate4_funding_multisplit_v4_20261107T1845Z.json` is `FROZEN_BEFORE_OUTCOMES`, `confirmatory_claim_go=NO_GO`, `exploratory_smoke_authorized_after_freeze=true`. Sealed-anchor conflict with FCLR002/003/013 domain family applies. **All outputs MUST be labeled EXPLORATORY / NOT CONFIRMATORY / NOT PROMOTABLE.** Never claim confirmatory GO, economic value, or promotion. **Do not replace prereg A–E contrasts or change confirmatory estimands.** Any modeling variant is an EXPLORATORY comparison only, versioned separately.

**Completed (do not rerun identically; build on it):**
- Exec `20261109T004003Z` (SHA `2f21b1dd4`): E vs A ΔQLIKE +0.4879, 95% block CI [-0.04216,1.19734] (spans 0, n=12969, 120 blocks) — **INCONCLUSIVE**. B/D unstable (split 3 B vs A Δ=44.69, D vs A Δ=10.33). Artifacts: `results/fclr_heavy001/gate4_v4_exploratory_exec_20261109T004003Z.md`, `research_state/gate4_v4_exploratory_exec/*`.
- Diag `20261109T021456Z` (SHA `2f21b1dd4`): reproduced E vs A +0.487902 CI [-0.042161,1.197338]. **Root-cause evidence (split 3, 2024-08-13..2024-09-11):** funding-augmented direct-variance OLS extrapolates to negative/near-zero variance under small target scale + tiny ridge (`1e-10*I`) + train-only standardization; floor-at-zero removes invalids but remaining near-zero positives and concentrated blowups dominate QLIKE. B BTC QLIKE mean 225.80 (raw_neg 89/720, raw_min -0.000527); D SOL 56.34 / BTC 1.68 with many raw negatives and larger `coef_l2`. E has no catastrophic single-instrument blowup but many raw negatives (622) and is worse than A. **E vs A LOO (EXPLORATORY):** all +0.488 inconclusive; drop XRP attenuates to +0.111 CI [-0.129,0.358] (inconclusive); other drops make harm CI>0; no LOO shows improvement. **Naive stabilized comparison (strong ridge + pred_floor=1e-8, EXPLORATORY only, NOT a prereg replacement) catastrophically worse** (Δ +9213.35) — do not use. Artifacts: `results/fclr_heavy001/gate4_v4_exploratory_diag_20261109T021456Z.md`, `research_state/gate4_v4_exploratory_diag/gate4_v4_exploratory_diag_20261109T021456Z.json`, `scripts/run_gate4_v4_exploratory_diag.py`, `tests/test_gate4_v4_exploratory_diag.py`.

**Execute next (versioned suffix, e.g. `_v4_exploratory_stab_20261109T####Z`; do not overwrite prior exec/diag outputs):**
1. **Read** `scripts/run_funding_ablations.py`, `scripts/run_gate4_v4_exploratory_diag.py`, diag JSON, `src/eval/walkforward.py`, and `src/volatility/eval.py`. Confirm E spec columns match prereg intent (`funding_signed, funding_abs, funding_pct_{24,72,168}, funding_z_{24,72,168}` + RV trails) and that no target leakage exists.
2. **Implement a principled EXPLORATORY stabilized comparison (not replacing A–E):** candidates to evaluate deterministically, each labeled EXPLORATORY and compared against original A/E only as diagnostics — e.g. (a) larger *scale-aware* ridge (calibrated to `trace(X'X)/k` or train-target variance, fixed rule prereg-scoped for this exploratory branch), (b) prediction floor at a small fraction of train target mean/variance scale (not 1e-8 absolute) with QLIKE-valid handling documented, (c) coefficient/fit diagnostics by split/instrument, (d) optional winsorization of standardized funding features using **train-only** quantiles if and only if leakage-safe and reported. **Do not claim improvement; report per-split, pooled CI, LOO, and any remaining blowups.**
3. **Run targeted unit tests** for any new code (synthetic, no network, no real research_state writes), then `python -m unittest discover tests` must remain **>=954 OK** (fix regressions you introduce).
4. **Write versioned artifacts** under subdirs (`research_state/gate4_v4_exploratory_diag/` or a new `..._stab/`, `results/fclr_heavy001/`) with commands, git SHA, tables, explicit NOT CONFIRMATORY/NOT PROMOTABLE verdict. **Do not weaken `tracka_resume_check` root md+json bound (172) or any Track A invariant.**
5. **Re-run** `python scripts/tracka_resume_check.py` and `python scripts/tracka_resume_gate.py --json` — expect 17/17 pass, probes==2, root bound satisfied, BLOCKED with `outcomes_inspected:false`.
6. **If stabilized exploratory comparison still shows no credible improvement / remains unstable:** produce a concise versioned **EXPLORATORY NO-GO note** for funding ablations on this local slice (not a confirmatory claim; no sealed-anchor reuse) and pivot to the most measurable open Gate 4/Track C-adjacent local engineering task supported by tests. **Do not start Track A probing or Track C/B sealed work.**
7. **Update this handoff** (§1–§10) with exact changes, commands, results, artifact paths, uncovered issues, and the next unfinished task.

**Acceptance for next session (heavy work — at least one required):** (A) versioned EXPLORATORY stabilized-comparison artifacts with full diagnostics and NOT CONFIRMATORY labeling, (B) versioned EXPLORATORY NO-GO note with evidence, or (C) new tested hardening/engineering work with suite green and Track A invariants green — with exact evidence and the session timestamp `2026-11-09T03:22:50Z` recorded in this handoff. A session that ends without one of (A)/(B)/(C) has not satisfied the heavy-work mandate.

---

## 1. WHAT CHANGED AND WHY (this session)
- **Updated handoff timestamp** to `2026-11-09T03:22:50Z` for session continuity.
- **Verified all baseline checks**: test suite 954 OK, tracka_resume_check pass (17/17), tracka_resume_gate BLOCKED (prereg required), scope registry PASS (112/112), root md+json bound 171/172.
- **No new code executed** — this handoff update establishes the exact current state and mandatory next-task campaign for the next agentic session.
- **Bottlenecks identified and cleared**: Track A probing prohibited (no admissible labels, probes==2 limit reached); Track C/B sealed; workflows/controllers forbidden; confirmatory paths blocked by provenance/prereg. Only unblocked measurable path is Gate 4 v4 EXPLORATORY follow-through on local 2024-04..09.

## 2. WHAT WAS ACTUALLY TESTED — EXACT OUTCOMES
| Check | Command | Result |
|---|---|---|
| Full suite | `python -m unittest discover tests` | **Ran 954 tests in 111.471s — OK** |
| Track A resume check | `python scripts/tracka_resume_check.py` | **pass:true**, network:false, probes==2, `writes_real_research_state:false`, `root_md_json_bounded` pass (171/172) |
| Track A resume gate | `python scripts/tracka_resume_gate.py --json` | **drift_preflight.pass:true**, `status:BLOCKED`, `reason_code:PREREG_OR_MANIFEST_BLOCK_AFTER_DRIFT_PASS`, `outcomes_inspected:false` |
| Scope registry drift | `python scripts/check_tracka_scope_registry_drift.py` | **[PASS] scope-registry drift: scripts=112 registry=112 reason=OK** |

## 3. EVIDENCE ADDED / MODIFIED (paths)
| Path | Change |
|---|---|
| `AGENT_HANDOFF.md` | **Updated** with new session timestamp `2026-11-09T03:22:50Z`, verified baseline outcomes, and mandatory heavy-work campaign for next session. |

## 4. CURRENT STATE OF EACH RESEARCH GATE
| Gate | Status | Evidence / Notes |
|---|---|---|
| **Gate 1 (Data Loadable)** | Track A: **BLOCKED** (no admissible unauth liquidation labels). Track C: PASSED (historical) / sealed. Gate 4 exploratory: local 2024-04..09 cache present (FCLR-015). | `track_a_deadend_map.md`; FCLR-015 manifest SHA256 `3e6ac26c...5406c`; `research_state/data_cache/*_2024_04..09` |
| **Gate 2 (Protocol Frozen)** | PASSED (Track C FCLR-001 context); Gate 4 v4 prereg **FROZEN_BEFORE_OUTCOMES** but `confirmatory_claim_go=NO_GO`, exploratory-only on 2024-04..09 due to sealed-anchor conflict. | `pre_registration_gate4_funding_multisplit_v4_20261107T1845Z.json` |
| **Gate 3 (RV-only Baseline)** | Track C: PASSED historical / **INCONCLUSIVE forward** (5-day test window, 0 non-overlapping 30d blocks). | `evaluation_summary_FCLR-012-V.md` |
| **Gate 4 (Incremental Funding/Price)** | **EXPLORATORY EXEC+DIAG (INCONCLUSIVE, NOT CONFIRMATORY/NOT PROMOTABLE)** — E vs A CI spans 0 and instrument-sensitive (no LOO improvement). B/D split-3 instability diagnosed (negative/near-zero extrapolation, QLIKE sensitivity; BTC/SOL blowups). Naive floor+strong ridge made it catastrophically worse. **Next:** principled EXPLORATORY stabilized comparison (scale-aware, leakage-safe) or formal EXPLORATORY NO-GO note. | `results/fclr_heavy001/gate4_v4_exploratory_exec_20261109T004003Z.md`; `research_state/gate4_v4_exploratory_exec/*`; `results/fclr_heavy001/gate4_v4_exploratory_diag_20261109T021456Z.md`; `research_state/gate4_v4_exploratory_diag/gate4_v4_exploratory_diag_20261109T021456Z.json` |
| **Forecast Gate** | **NOT ELIGIBLE** (Track C forward Gate 3 inconclusive; Track A blocked). No confirmatory promotion from v4 exploratory exec/diag. | frontier/negative results |

## 5. SINGLE HIGHEST-VALUE NEXT TASK
Execute **§0 Campaign**: implement and evaluate a **principled, leakage-safe EXPLORATORY stabilized comparison** (scale-aware ridge and/or train-only target-scale floor; no prereg A–E replacement), report pooled/LOO/per-split diagnostics with NOT CONFIRMATORY labeling, or produce a versioned EXPLORATORY NO-GO note if no credible improvement is supported. Keep suite + Track A invariants green and root bound satisfied.

## 6. PRECISE VERIFICATION COMMANDS
```bash
git --no-pager status --short
python -m unittest discover tests                         # expect >=954 OK
python scripts/tracka_resume_check.py                    # expect pass:true, 17/17, probes==2, network:false, root_md_json_bounded pass
python scripts/tracka_resume_gate.py --json              # expect BLOCKED, drift_preflight.pass:true, outcomes_inspected:false
python scripts/check_tracka_scope_registry_drift.py      # expect PASS
python scripts/run_gate4_v4_exploratory_diag.py --help
ls results/fclr_heavy001/gate4_v4_exploratory_diag_20261109T021456Z.md
ls research_state/gate4_v4_exploratory_diag/
```

## 7. BLOCKERS / CONSTRAINTS
| Blocker | Evidence | Allowed next route |
|---|---|---|
| Track A: no admissible liquidation labels | `track_a_deadend_map.md`, rubric NO-GO all 8 candidates; probes==2; 2026-11..2027-02 absent | **Only** if a genuinely new unauth source meets full rubric; else guard hardening only. No re-probe absent months. |
| Track C: forward panel ends 2026-11-02, 0 non-overlapping 30d test blocks | `fclr012v_coverage_audit.json`, FCLR-012-V inconclusive | New admissible panel with real volume, ≥3 non-overlapping 30d blocks; do not relax criteria. |
| Gate 4 v4: sealed-anchor conflict on 2024 slice | v4 prereg `confirmatory_claim_go:NO_GO` | Run as **EXPLORATORY only**, explicit labeling, no promotion. |
| Gate 4 v4 B/D instability / E sensitivity | exec `20261109T004003Z`, diag `20261109T021456Z` | Diagnose/fix only as **EXPLORATORY comparisons** with versioned artifacts; do not claim improvement or replace prereg A–E. |
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
2. Inspect `research_state/experiment_frontier.json`, latest manifests, tests, data cache state, `research_state/gate4_v4_exploratory_exec/`, and `research_state/gate4_v4_exploratory_diag/`.
3. Execute §0 (highest-value measurable task). Run cheapest checks first.
4. Update **this file** with exact changes/commands/results/evidence/gates/next task + blockers.

## 10. NEXT SESSION DELIVERABLE
Updated `AGENT_HANDOFF.md` with Gate 4 v4 principled EXPLORATORY stabilized-comparison evidence or EXPLORATORY NO-GO note, full suite + Track A invariant outcomes, artifact paths, root-bound compliance, and the next unfinished task — **session timestamp `2026-11-09T03:22:50Z` recorded, at least one of acceptance (A)/(B)/(C) produced**. **Repo state must remain continuable without user repeating instructions.**

---
**END OF SINGLE DURABLE HANDOFF.**