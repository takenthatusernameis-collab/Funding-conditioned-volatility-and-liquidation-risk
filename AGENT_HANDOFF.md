# AGENT_HANDOFF.md — Single Durable Handoff (next session MUST continue from here)

**Updated:** 2026-11-09T17:52:40Z (message time) — handoff refresh after repo-state verification.
**Repo:** `Funding-conditioned-volatility-and-liquidation-risk` (repo-name priority: **funding-conditioned volatility** first — Track C is the only research track with admissible OOS evidence; Track A liquidation risk is structurally blocked). `git status --short`: clean (no uncommitted `run_manifest.json` LFS materialization, no `ironflow_fastpath_cache.json`, no `__pycache__` observed). Do **not** commit large raw caches/data zips, `__pycache__`, or workflow changes.
**Binding priority:** P0 = **Track C funding-conditioned volatility — next materially different heavy work** (not confirmatory on current data). `FUNDING_CONDITIONING_DEEPER_VALIDATION-002` = **COMPLETE_INCONCLUSIVE (EXPLORATORY_ONLY, 2026-11-09T16:39:00Z)**. Track B H003 = **COMPLETE_INCONCLUSIVE (2026-11-09T15:35:43Z)**. Track A = **STRUCTURALLY BLOCKED / NO TRIGGER** (ironflow `data_through=2026-10`; 2026-11..2027-02 absent; probes==2) — **no probing, no scan/wrapper/report families**. **No status-only churn. No `.github/workflows` edits. No confirmatory promotion from exploratory results. No sealed-holdout reuse, threshold shopping, or conflating observed/modeled/synthetic labels. Every session must produce versioned, auditable artifacts and/or tested code.**

---

## 0) INITIAL TASK MESSAGE — 2026-11-09T17:52:40Z — MANDATORY HEAVY WORK (DO NOT AVOID)

**Execute measurable research/engineering progress this session.** Forbidden: status-only churn; Track A probing/re-probe; FCLR-NEXT-14x-style guard-hardening substitution on legacy entrypoints; Track C/B new sealed outcomes without frozen prereg; conflating observed/modeled/synthetic labels; workflow/controller/scheduler/poller/wrapper creation; `.github/workflows` edits; confirmatory claims from exploratory runs; sealed-anchor reuse; prereg A–E/estimand changes; threshold-shopping/holdout reuse; weakening `root_md_json_bounded` or Track A invariants; fabricating outcomes; live/paper trading; credentials; access-control bypass.

### Verified state (2026-11-09T17:52:40Z)
| Item | Evidence |
|---|---|
| Track C deeper validation artifacts present | `research_state/evaluation_summary_STREAM_B_DEEP_ANALYSIS-001_20261109T162703Z.md`, `..._002_20261109T163517Z.md` |
| Decision recorded | `research_state/negative_results_report.md` Track C section (2026-11-09T16:39:00Z); `research_state/experiment_frontier.json` `FUNDING_CONDITIONING_DEEPER_VALIDATION-002` = `COMPLETE_INCONCLUSIVE` (exploratory) |
| Dep-light test gate | `python -m unittest tests.test_synthetic_boundary_labels` → **8/8 OK** (2026-11-09T17:52:40Z session verify). Full `discover` blocked by missing numpy/pandas/scipy in this runner; tmp-isolate heavy-dep tests; never fabricate. |
| Confirmatory blocker (structural) | FCLR-002 test 2024-07-23..2024-09-30 = 70 days = **2** non-overlapping 30-day blocks (<3). Binance archive ends **2026-11-02** (404 beyond). No cached >=3-block unsealed panel ready. 2024 partitions consumed (FCLR-004 BLOCKED). **Do not manufacture a confirmatory claim.** |

### Campaign result carried forward (do not relitigate without new admissible data)
- **STREAM_B_DEEP_ANALYSIS-001 (2026-11-09T16:27:03Z, frozen FCLR-002):** B1 0.662552, C2_all 0.632151 (**+4.588%** rel QLIKE, diff -0.030400, 95% CI [-0.044345,-0.018402], excludes 0 YES). C1 +0.972% (YES), A3_pricedisloc +2.255% (YES), A1_fundpctz +4.051% (YES), A2_rvratios -1.534%/A4_fund_rvrat -0.526% (NO). All 5 symbols +4.0%..+5.0%.
- **STREAM_B_DEEP_ANALYSIS-002 (2026-11-09T16:35:17Z):** regime-stratified QLIKE (train-only quartiles, no look-ahead, 2000 block-bootstrap reps). **Q1 extreme-funding skill robust (EXPLORATORY):** Q1_low_abs_pos CI excludes 0 YES for all 5 symbols (BNB +5.081%, BTC +4.374%, ETH +5.816%, SOL +6.923%, XRP +5.370%); Q1_low_abs_neg YES XRP (+9.192%); Q2_pos YES BTC/ETH/XRP. Aggregate: Q1_low_abs_neg **+4.890%** (YES), Q1_low_abs_pos **+5.346%** (YES), Q2_pos **+3.969%** (YES), Q2_neg -2.218% (NO), Q4_high_abs_neg -4.696% (NO). Q3/Q4_high_abs_pos = 0 rows (degenerate train boundaries). **Confirmatory gate NOT MET** (2 blocks < 3).

### Next unfinished heavy work (do in order — mandatory, measurable)
1. **Track C reproducibility + audit hardening (offline, bounded, no new outcomes):** create a versioned artifact `research_state/trackc_reproducibility_audit_<UTC>.md` (or timestamped) that (a) verifies SHA256/size/timestamps for the two STREAM_B summaries + `fclr002_panel.json`/manifest split refs used, (b) records exact rerun commands + environment deps present/missing, (c) restates the 2-block confirmatory blocker with `block_count_resolution_20261103T102000Z.md`/manifest evidence, and (d) lists the *single* next confirmatory path with a concrete prereg skeleton filename to create **before** any outcome inspection if/when a >=3-block admissible panel appears. Do not inspect new sealed outcomes.
2. **Test/engineering bottleneck (if actionable):** identify dep-light Track C/volatility tests runnable without numpy/pandas/scipy and get them green with tmp isolation; if none are actionable, add/extend a small stdlib-only unit test around existing volatility/metrics logic *only if* it exercises real code paths (no placeholder tests). Record exact test counts.
3. **Resume-trigger watchlist (evidence, no probing):** in the same reproducibility artifact, document the admissible confirmatory trigger: new unauthenticated Binance panel with >=5 symbols and >=3 non-overlapping 30-day OOS blocks (or equivalent pre-registered design), plus full preregistration frozen before outcomes; also Track A trigger rules unchanged. No network probing in this session unless performing a single bounded admissible check with provenance logged — default is no probe.
4. **Update this file** with exact evidence, commands run, test counts, timestamps, and the next unfinished task.

**Acceptance (mandatory):** (A) a new versioned `trackc_reproducibility_audit_*` artifact committed/ready with hashes, commands, blocker evidence, and next prereg path + updated `AGENT_HANDOFF.md` + green dep-light tests recorded, **or** (B) a materially different tested engineering/research task with same evidence discipline. **Anything less is failure.**

---

## 1) VERIFIED (2026-11-09T17:52:40Z session)

| Check | Result |
|---|---|
| `git status --short` | clean |
| `python -m unittest tests.test_synthetic_boundary_labels` | **8/8 OK** |
| STREAM_B artifacts | both summaries present (001/002 timestamps as above) |
| Frontier/negative report | `FUNDING_CONDITIONING_DEEPER_VALIDATION-002` COMPLETE_INCONCLUSIVE; Track C negative section present |
| Track A | no trigger; no re-probe performed |

---

## 2) DONE (carry forward)
- Volatility gate H001 closed NOT_SUPPORTED on claim-worthy panels (FCLR-001/002/003/008/v3/FCLR-013). Risk overlay INELIGIBLE.
- Track A structurally blocked; no admissible unauthenticated liquidation labels; ironflow probes==2 exhausted.
- Track B H003 **COMPLETE_INCONCLUSIVE** (2026-11-09T15:35:43Z).
- Track C `FUNDING_CONDITIONING_DEEPER_VALIDATION-002` **COMPLETE_INCONCLUSIVE (EXPLORATORY_ONLY)** (2026-11-09T16:39:00Z) — robust Q1 regime skill but 2 blocks < 3; not confirmatory.
- `test_synthetic_boundary_labels` dep-light: 8/8 OK.

---

## 3) GATE STATE (binding)
| Gate | Status |
|---|---|
| Gate 1 | Track A BLOCKED; Track C cache/manifests present |
| Gate 2 | Gate 4 v4 frozen-before-outcomes context preserved; no confirmatory claim |
| Gate 3 | Track C forward INCONCLUSIVE / 2-block limit on FCLR-002 |
| Gate 4 | EXPLORATORY evidence only; NOT CONFIRMATORY/NOT PROMOTABLE |
| Forecast Gate | NOT ELIGIBLE |
| Track B H003 | COMPLETE_INCONCLUSIVE |
| Track C deeper validation | COMPLETE_INCONCLUSIVE (EXPLORATORY_ONLY) |

---

## 4) BOTTLENECKS
| Bottleneck | Status | Action |
|---|---|---|
| Confirmatory Track C impossible on current data (2 blocks, archive ends 2026-11-02) | structural/data | Record reproducibly; define prereg-before-outcomes resume path; no fake confirmatory run |
| numpy/pandas/scipy missing in runner | env | Use stdlib/deplight tests + existing analysis artifacts; tmp-isolate heavy-dep tests |
| `root_md_json_bounded` / artifact churn | constraint | Put new artifacts under `research_state/` dated files sparingly or `results/` as appropriate; do not weaken guards |
| Track A no admissible labels | structural | No re-probe; trigger-only with prereg before outcomes |

---

## 5) KEY EVIDENCE PATHS
- `AGENT_HANDOFF.md` (this file, single durable)
- `RESEARCH_PROMPT.md`
- `research_state/experiment_frontier.json`
- `research_state/negative_results_report.md`
- `research_state/run_manifest.json` (LFS-tracked; materialize if pointer)
- `research_state/evaluation_summary_STREAM_B_DEEP_ANALYSIS-001_20261109T162703Z.md`
- `research_state/evaluation_summary_STREAM_B_DEEP_ANALYSIS-002_20261109T163517Z.md`
- `research_state/block_count_resolution_20261103T102000Z.md`
- `research_state/fclr_h003_pre_registration.md`, `research_state/evaluation_summary_h003_FCLR002.md`
- `scripts/synthetic_boundary_labels.py`, `tests/test_synthetic_boundary_labels.py`

---

## 6) DO NOT DO
- ❌ Track A probing / scan/wrapper/report/status-file families
- ❌ Confirmatory/promotion claims from exploratory runs; threshold shopping; sealed holdout reuse
- ❌ New sealed outcomes without frozen preregistration
- ❌ Conflate observed liquidations with modeled/synthetic boundary breaches
- ❌ `.github/workflows` edits; schedulers/pollers/controllers
- ❌ Commit raw caches/zips/`__pycache__`/`ironflow_fastpath_cache.json`
- ❌ Live/paper trading, order endpoints, credentials, access-control bypass

---

## 7) SESSION START (mandatory)
1. Read **this file** + `RESEARCH_PROMPT.md`; `git status --short`.
2. `git lfs pull` if `research_state/run_manifest.json` is a pointer (needed for split refs).
3. Run dep-light verification: `python -m unittest tests.test_synthetic_boundary_labels` (record count). Do not fabricate full-suite results if heavy deps missing.
4. Execute **§0 heavy work item 1** (reproducibility audit artifact) with hashes/timestamps/commands/blocker evidence/prereg resume path.
5. Update **this file** with exact evidence and next unfinished task.

---

**END OF SINGLE DURABLE HANDOFF. FUTURE AGENTS: START AT §0 — HEAVY WORK REQUIRED. (2026-11-09T17:52:40Z)**

---

## 1) VERIFIED THIS SESSION (2026-11-09T16:39:00Z)

| Check | Result |
|---|---|
| `git --no-pager status --short` | clean except uncommitted `research_state/run_manifest.json` (materialized LFS) + `research_state/ironflow_fastpath_cache.json` (cache) |
| `__pycache__` | removed from `scripts/` and `tests/` |
| Heavy deps | numpy/pandas/scipy **MISSING** in this runner → `python -m unittest discover tests` cannot complete (import errors); `src/volatility/*` is stdlib-only; deep-analysis scripts run on stdlib only |
| `python -m unittest tests.test_synthetic_boundary_labels` | **8/8 OK** (TestCase wrapper present; bottleneck resolved) |
| `PYTHONPATH=<repo> python scripts/run_stream_b_deep_analysis_001.py` | **RAN OK** → `evaluation_summary_STREAM_B_DEEP_ANALYSIS-001_20261109T162703Z.md` (TEST: B1 0.662552, C2_all 0.632151 +4.588%, CI excl 0 YES; all 5 symbols improve +4.0%..+5.0%) |
| `PYTHONPATH=<repo> python scripts/run_stream_b_deep_analysis_002.py` | **RAN OK** → `evaluation_summary_STREAM_B_DEEP_ANALYSIS-002_20261109T163517Z.md` (regime-stratified QLIKE; Q1_low_abs_pos CI excl 0 YES all 5 symbols; Q1_low_abs_neg YES XRP; Q2_pos YES BTC/ETH/XRP; aggregate Q1_low_abs_neg +4.890% YES, Q1_low_abs_pos +5.346% YES, Q2_pos +3.969% YES; 2 blocks < 3 → exploratory only) |
| `research_state/evaluation_summary_h003_FCLR002.md` | EXISTS (regenerated 2026-11-09T15:27:50Z, n=8274 test rows) |
| `research_state/experiment_frontier.json` | `FCLR-H003-FCLR-002` COMPLETE_INCONCLUSIVE (20261109T153543Z); `FUNDING_CONDITIONING_DEEPER_VALIDATION-002` → **COMPLETE_INCONCLUSIVE** (20261109T163900Z) |
| `research_state/negative_results_report.md` | Track B H003 FCLR-002 section (2026-11-09T15:27:50Z); **Track C section appended (2026-11-09T16:39:00Z)** with exact regime table, counts, timestamps |

---

## 2) DONE (carry forward)

- Volatility gate H001 closed out NOT_SUPPORTED on all claim-worthy panels (FCLR-001/002/003/008/v3/FCLR-013). Risk overlay INELIGIBLE. Preserve negatives; no threshold shopping.
- Track A structurally blocked; no admissible unauthenticated liquidation labels; ironflow data_through=2026-10, probes==2, exhausted.
- **Track B H003 COMPLETE_INCONCLUSIVE (2026-11-09T15:35:43Z)**: labels implemented; pre-registration frozen; FCLR-002 boundary-breach result computed, registered (FCLR-H003-FCLR-002), recorded in negative_results_report.md Track B section. Null result: no consistent incremental forecast skill of C2 over B0 across leverage/side scenarios.
- **Track C deeper validation COMPLETED (exploratory):** STREAM_B_DEEP_ANALYSIS-001 (2026-11-09T16:27:03Z) + STREAM_B_DEEP_ANALYSIS-002 (2026-11-09T16:35:17Z) executed on frozen FCLR-002 splits. Aggregate C2 vs B1 +4.588% test QLIKE (CI excl 0 YES). Regime-stratified: Q1 extreme-funding regimes show robust skill (CI excl 0 YES, rel_imp +4.374%..+9.192% per symbol), Q2_pos mostly YES, Q4/Q3 small/zero rows inconclusive. 2 blocks < 3 → NOT confirmatory, EXPLORATORY_ONLY, do NOT promote. Status decision recorded in negative_results_report.md Track C section + experiment_frontier.json COMPLETE_INCONCLUSIVE (2026-11-09T16:39:00Z).
- `test_synthetic_boundary_labels.py` bottleneck resolved: 8 tests collected, 8/8 OK.

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
| `test_synthetic_boundary_labels` collects 0 tests (not TestCase) | **YES — RESOLVED** | Already wrapped in TestCase; 8/8 OK (2026-11-09T16:39:00Z). |
| `run_manifest.json` was unmaterialized LFS pointer | **YES (done)** | Materialized via `git lfs pull` (uncommitted working tree). |
| H003 FCLR-002 result missing from frontier + negative report | **YES (done)** | Registered cell + appended Track B section (2026-11-09T15:35:43Z). |
| Track C regime-stratified QLIKE section-4 stub | **YES (done)** | Filled by STREAM_B_DEEP_ANALYSIS-002 (2026-11-09T16:35:17Z). |
| Track C status decision not recorded | **YES (done)** | Appended negative_results_report.md Track C section + frontier COMPLETE_INCONCLUSIVE (2026-11-09T16:39:00Z). |
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
- Negative report: `research_state/negative_results_report.md` (Track B section 2026-11-09T15:27:50Z; **Track C section 2026-11-09T16:39:00Z**)
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
4. **No new Track C confirmatory work possible on current data** (2 blocks < 3, archive ends 2026-11-02). Next materially different route: await new admissible Binance panel with >=3 non-overlapping 30-day blocks → build FCLR-008 with full preregistration before outcomes. Until then, Track C remains COMPLETE_INCONCLUSIVE (exploratory). Do not substitute status-only churn.
5. Update **this file** with exact evidence, test counts, timestamps, and next unfinished task.

---

**END OF SINGLE DURABLE HANDOFF. FUTURE AGENTS: START AT §0 — HEAVY WORK REQUIRED. (2026-11-09T16:39:00Z)**
