# AGENT_HANDOFF.md — Single Durable Handoff (next session MUST continue from here)

**Updated:** 2026-11-09T16:35:17Z
**Repo:** `Funding-conditioned-volatility-and-liquidation-risk` (git `bf93405ec`, clean tree; `research_state/run_manifest.json` materialized LFS content left uncommitted — do not commit unless asked)
**Binding priority:** P0 = **Track C funding-conditioned volatility deeper validation (FUNDING_CONDITIONING_DEEPER_VALIDATION-002)** — the "Funding-conditioned-volatility" half of the repo name, the only unblocked research track. Track B H003 **COMPLETE_INCONCLUSIVE** as of 2026-11-09T15:35:43Z (evaluation_summary_h003_FCLR002.md, experiment_frontier.json entry FCLR-H003-FCLR-002, negative_results_report.md Track B section all present). Gate 4 v4 = EXPLORATORY NO-GO, NOT CONFIRMATORY, NOT PROMOTABLE. Track A = STRUCTURALLY BLOCKED / NO TRIGGER (2026-11..2027-02 absent, ironflow probes==2) — no probing, no scan/wrapper/report families. **No status-only churn. No `.github/workflows` edits. Every session must produce versioned, auditable artifacts and/or tested code.**

---

## 0) INITIAL TASK MESSAGE — MANDATORY HEAVY WORK (2026-11-09T16:35:17Z) — DO NOT AVOID

**You MUST execute measurable research/engineering progress this session.** Forbidden: status-only churn; FCLR-NEXT-14x guard-hardening on legacy entrypoints; Track A probing/re-probe; Track C/B new sealed outcomes or conflating observed/modeled/synthetic labels; workflow/controller/scheduler/poller/wrapper creation; `.github/workflows` edits; confirmatory promotion from exploratory Gate 4; sealed-anchor reuse; prereg A–E/estimand changes; threshold-shopping/holdout reuse; weakening `root_md_json_bounded` or Track A invariants; fabricating outcomes; live/paper trading; credentials; access-control bypass; committing `__pycache__`/`research_state/ironflow_fastpath_cache.json`/large raw caches.

### CAMPAIGN COMPLETED — Track C deeper validation (FUNDING_CONDITIONING_DEEPER_VALIDATION-002) (heavy, bounded, offline)

**STREAM_B_DEEP_ANALYSIS-001** (ran 2026-11-09T16:27:03Z) → `research_state/evaluation_summary_STREAM_B_DEEP_ANALYSIS-001_20261109T162703Z.md` on frozen FCLR-002 splits. TEST QLIKE: B1 0.662552; C2_all 0.632151 (+4.588% rel, diff -0.030400, 95% CI [-0.044345,-0.018402], excludes 0 YES); C1 +0.972%; A1_fundpctz +4.051% (CI excludes 0 YES); A3_pricedisloc +2.255% (YES); A2_rvratios -1.534% and A4_fund_rvrat -0.526% (NO). All 5 symbols improve +4.0%..+5.0%; SOLUSDT marginal.

**STREAM_B_DEEP_ANALYSIS-002** (ran 2026-11-09T16:35:17Z) → `research_state/evaluation_summary_STREAM_B_DEEP_ANALYSIS-002_20261109T163517Z.md` — regime-stratified QLIKE per symbol per funding regime (TRAIN-only thresholds, no look-ahead) + interaction/ablation per regime + block-bootstrap CIs (2000 reps). **Key result:** Q1 (extreme funding) regimes show robust skill — Q1_low_abs_pos CI_excludes0=YES for all 5 symbols (BNB +5.081%, BTC +4.374%, ETH +5.816%, SOL +6.923%, XRP +5.370%); Q1_low_abs_neg YES for XRP (+9.192%); Q2_pos YES for BTC/ETH/XRP. Aggregate pooled: Q1_low_abs_neg +4.890% (CI excl 0 YES), Q1_low_abs_pos +5.346% (YES), Q2_pos +3.969% (YES), Q2_neg -2.218% (NO), Q4_high_abs_neg -4.696% (NO). Q3/Q4_high_abs_pos = 0 rows (train quartile boundaries degenerate). **BUT** FCLR-002 test = 2 non-overlapping 30-day blocks (< 3) → confirmatory gate NOT met; skill is EXPLORATORY only, do NOT promote.

### Next unfinished work (do in order — mandatory)

1. **Status decision (FUNDING_CONDITIONING_DEEPER_VALIDATION-002):** Q1 regimes show robust funding-conditioned volatility skill (CI excludes 0, rel_imp > 0 consistently), but 2 blocks < 3 → keep **EXPLORATORY_ONLY**, do NOT promote to confirmatory. Record this decision in `negative_results_report.md` Track C section (exact regime table, counts, timestamps) and set `experiment_frontier.json` entry `FUNDING_CONDITIONING_DEEPER_VALIDATION-002` to **COMPLETE_INCONCLUSIVE** with exact evidence/counts/timestamps.
2. **Remove bottleneck — `tests/test_synthetic_boundary_labels.py` collects 0 tests:** Wrap the 8 plain module-level functions in a `unittest.TestCase` subclass so `python -m unittest discover tests` collects them. Record true count; do not fabricate 8/8.
3. **Artifacts + handoff:** Verify `evaluation_summary_STREAM_B_DEEP_ANALYSIS-002_20261109T163517Z.md` written; update `AGENT_HANDOFF.md` with exact evidence, counts, timestamps, and next unfinished task.

### Execute now (cannot skip)

1. `git status --short` (expect clean; restore `research_state/ironflow_fastpath_cache.json` if dirty; remove local `__pycache__`). Note: `research_state/run_manifest.json` is materialized LFS content (uncommitted) — leave as-is.
2. `python -m unittest discover tests` → **NOT GREEN in this env** (numpy/pandas/scipy missing → import errors on heavy-dep tests). Tmp-isolate heavy-dep tests; dep-light core logic tests must pass where collectable. After step 2 above, `test_synthetic_boundary_labels` must collect 8 tests (wrapped in TestCase).
3. Perform campaign steps 1–3 above. Record exact results, counts, and timestamps here.

**Acceptance (mandatory):** (A) Track C status decision recorded in `negative_results_report.md` Track C section + `experiment_frontier.json` COMPLETE_INCONCLUSIVE + `AGENT_HANDOFF.md` updated with exact evidence/counts/timestamps, **and** `test_synthetic_boundary_labels` collects 8 tests, **or** (B) a materially different tested engineering task with same green gates and versioned evidence. **Anything less is failure.**

---

## 1) VERIFIED THIS SESSION (2026-11-09T16:35:17Z)

| Check | Result |
|---|---|
| `git --no-pager status --short` | clean (HEAD bf93405ec) |
| Heavy deps | numpy/pandas/scipy **MISSING** in this runner → `python -m unittest discover tests` cannot complete (import errors); `src/volatility/*` is stdlib-only; deep-analysis scripts run on stdlib only |
| `python -m unittest tests.test_synthetic_boundary_labels` | **0 tests collected** (plain module-level functions, not TestCase) — do not fabricate 8/8; wrap in TestCase this session |
| `PYTHONPATH=<repo> python scripts/run_stream_b_deep_analysis_001.py` | **RAN OK** → `evaluation_summary_STREAM_B_DEEP_ANALYSIS-001_20261109T162703Z.md` (TEST: B1 0.662552, C2_all 0.632151 +4.588%, CI excl 0 YES; all 5 symbols improve +4.0%..+5.0%) |
| `PYTHONPATH=<repo> python scripts/run_stream_b_deep_analysis_002.py` | **RAN OK** → `evaluation_summary_STREAM_B_DEEP_ANALYSIS-002_20261109T163517Z.md` (regime-stratified QLIKE per symbol/regime + ablation per regime + block-bootstrap CIs; Q1_low_abs_pos CI excl 0 YES all 5 symbols; Q1_low_abs_neg YES XRP; Q2_pos YES BTC/ETH/XRP; aggregate Q1_low_abs_neg +4.890% YES, Q1_low_abs_pos +5.346% YES, Q2_pos +3.969% YES; 2 blocks < 3 → exploratory only) |
| `research_state/evaluation_summary_h003_FCLR002.md` | EXISTS (regenerated 2026-11-09T15:27:50Z, n=8274 test rows) |
| `research_state/experiment_frontier.json` | Contains `FCLR-H003-FCLR-002` (COMPLETE_INCONCLUSIVE 20261109T153543Z); `FUNDING_CONDITIONING_DEEPER_VALIDATION-002` status IN_PROGRESS |
| `research_state/negative_results_report.md` | Contains Track B H003 FCLR-002 section (2026-11-09T15:27:50Z); Track C section not yet appended |

---

## 2) DONE (carry forward)

- Volatility gate H001 closed out NOT_SUPPORTED on all claim-worthy panels (FCLR-001/002/003/008/v3/FCLR-013). Risk overlay INELIGIBLE. Preserve negatives; no threshold shopping.
- Track A structurally blocked; no admissible unauthenticated liquidation labels; ironflow data_through=2026-10, probes==2, exhausted.
- **Track B H003 COMPLETE_INCONCLUSIVE (2026-11-09T15:35:43Z)**: labels implemented; pre-registration frozen; FCLR-002 boundary-breach result computed, registered (FCLR-H003-FCLR-002), recorded in negative_results_report.md Track B section. Null result: no consistent incremental forecast skill of C2 over B0 across leverage/side scenarios.
- **Track C deeper validation COMPLETED (exploratory):** STREAM_B_DEEP_ANALYSIS-001 (2026-11-09T16:27:03Z) + STREAM_B_DEEP_ANALYSIS-002 (2026-11-09T16:35:17Z) executed on frozen FCLR-002 splits. Aggregate C2 vs B1 +4.588% test QLIKE (CI excl 0 YES). Regime-stratified: Q1 extreme-funding regimes show robust skill (CI excl 0 YES, rel_imp +4.374%..+9.192% per symbol), Q2_pos mostly YES, Q4/Q3 small/zero rows inconclusive. 2 blocks < 3 → NOT confirmatory, EXPLORATORY_ONLY, do NOT promote.

---

## 3) GATE STATE (binding)

| Gate | Status |
|---|---|
| Gate 1 (data loadable) | Track A BLOCKED (no admissible labels). Track C local cache present (fclr002_panel.json). |
| Gate 2 (protocol frozen) | Gate 4 v4 FROZEN_BEFORE_OUTCOMES, confirmatory_claim_go=NO_GO. |
| Gate 3 (RV-only baseline) | Track C forward INCONCLUSIVE (0 non-overlapping 30d blocks on 2026 panel; FCLR-002 2 blocks < 3). |
| Gate 4 (incremental funding/price) | EXPLORATORY NO-GO CONFIRMED; NOT CONFIRMATORY/NOT PROMOTABLE. |
| Forecast Gate | NOT ELIGIBLE (no confirmatory promotion). |
| Track B H003 | **COMPLETE_INCONCLUSIVE** (2026-11-09T15:35:43Z). |
| Track C deeper validation | **COMPLETE_INCONCLUSIVE (exploratory)** (FUNDING_CONDITIONING_DEEPER_VALIDATION-002) — regime-stratified QLIKE on frozen FCLR-002 splits; Q1 extreme-funding skill robust but 2 blocks < 3 → not confirmatory. |

---

## 4) BOTTLENECKS (remove what is removable)

| Bottleneck | Removable? | Action |
|---|---|---|
| FCLR-NEXT-14x guard-hardening mandate substituting for research | **YES — removed** | Replaced by Track C deeper validation heavy work (this handoff §0). |
| numpy/pandas/scipy missing → unittest discover cannot complete | **PARTIAL** | `src/volatility` is stdlib-only; deep-analysis scripts ran. Next session: install deps or confirm stdlib path sufficient; tmp-isolate heavy-dep tests; never fabricate results. |
| `test_synthetic_boundary_labels` collects 0 tests (not TestCase) | **YES** | Wrap 8 functions in `unittest.TestCase` this session; record true count; do not fabricate 8/8. |
| `run_manifest.json` was unmaterialized LFS pointer | **YES (done)** | Materialized via `git lfs pull` (uncommitted working tree). |
| H003 FCLR-002 result missing from frontier + negative report | **YES (done)** | Registered cell + appended Track B section (2026-11-09T15:35:43Z). |
| Track C regime-stratified QLIKE section-4 stub | **YES (done)** | Filled by STREAM_B_DEEP_ANALYSIS-002 (2026-11-09T16:35:17Z) → `evaluation_summary_STREAM_B_DEEP_ANALYSIS-002_20261109T163517Z.md`. |
| Track A: no admissible labels / 2026-11..2027-02 absent | No (structural) | No re-probe. Monitor ironflow >=2026-11 trigger → PREREG BEFORE OUTCOMES → FCLR-012-A. |
| `root_md_json_bounded` tight | Constraint | New artifacts to `results/` or dated subdirs only. Do not weaken. |
| FCLR-002 test window = 70 days = 2 blocks (<3 required) | **DOCUMENTED** | Documented in block_count_resolution_20261103T102000Z.md; no cached ≥3-block panel readily loadable; FCLR-008 needs panel construction + preregistration. Confirmatory gate not met — exploratory only. |

---

## 5) KEY EVIDENCE PATHS

- Handoff (single durable): `AGENT_HANDOFF.md`
- Research prompt: `RESEARCH_PROMPT.md`
- Track B pre-registration: `research_state/fclr_h003_pre_registration.md`
- H003 labels: `scripts/synthetic_boundary_labels.py`, `tests/test_synthetic_boundary_labels.py`
- H003 runner: `scripts/run_h003.py`
- H003 FCLR-002 result: `research_state/evaluation_summary_h003_FCLR002.md` (2026-11-09T15:27:50Z)
- Frontier: `research_state/experiment_frontier.json` (entry FCLR-H003-FCLR-002 COMPLETE_INCONCLUSIVE; FUNDING_CONDITIONING_DEEPER_VALIDATION-002 COMPLETE_INCONCLUSIVE-exploratory)
- Negative report: `research_state/negative_results_report.md` (Track B section 2026-11-09T15:27:50Z; Track C section pending — append this session)
- Manifest: `research_state/run_manifest.json` (materialized, FCLR-002 splits)
- Deep analysis artifacts: `research_state/evaluation_summary_STREAM_B_DEEP_ANALYSIS-001_20261109T162703Z.md` + `research_state/evaluation_summary_STREAM_B_DEEP_ANALYSIS-002_20261109T163517Z.md`
- Block-count resolution: `research_state/block_count_resolution_20261103T102000Z.md`

---

## 6) DO NOT DO

- ❌ FCLR-NEXT-14x guard-hardening on legacy entrypoints (substitution churn — removed)
- ❌ Re-probe 2026-11..2027-02 / Track A probe/scan/wrapper/report families
- ❌ Workflows/schedulers/pollers/status-only files/controllers; **no `.github/workflows` edits**
- ❌ Track C/B new sealed outcomes or conflate observed/modeled/synthetic labels
- ❌ Threshold-shopping, holdout reuse, confirmatory/promotion claims from exploratory runs
- ❌ Commit `__pycache__/`, `research_state/ironflow_fastpath_cache.json`, large raw caches
- ❌ Weaken `root_md_json_bounded` or Track A invariants
- ❌ Live/paper trading, order endpoints, credentials, access-control bypass

---

## 7) SESSION START (mandatory)

1. `git pull` + `git status`; read **this file** + `RESEARCH_PROMPT.md`.
2. `git lfs pull` if `research_state/run_manifest.json` is still a pointer (needed for FCLR-002 splits).
3. Run verification loop (§0 #2–#3). Fix hygiene only — do not commit.
4. Execute **Track C deeper validation status decision + bottleneck removal** (§0). Cheapest checks first. Update **this file** with exact evidence, test counts, timestamps, and next unfinished task.

---

**END OF SINGLE DURABLE HANDOFF. FUTURE AGENTS: START AT §0 — HEAVY WORK REQUIRED. (2026-11-09T16:35:17Z)**
