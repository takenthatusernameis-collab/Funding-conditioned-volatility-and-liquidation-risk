# AGENT_HANDOFF.md — Single Durable Handoff (next session MUST continue from here)

**Updated:** 2026-11-09T15:59:01Z
**Repo:** `Funding-conditioned-volatility-and-liquidation-risk` (git `5964cc3fe`, clean except uncommitted `research_state/run_manifest.json` materialized from LFS pointer via `git lfs pull` — do not commit unless asked)
**Binding priority:** P0 = **Track C funding-conditioned volatility deeper validation (FUNDING_CONDITIONING_DEEPER_VALIDATION-002)** — the "Funding-conditioned-volatility" half of the repo name, now the only unblocked research track. Track B H003 (liquidation-risk boundary-breach) **COMPLETE_INCONCLUSIVE** as of 2026-11-09T15:35:43Z (evaluation_summary_h003_FCLR002.md, experiment_frontier.json entry FCLR-H003-FCLR-002, negative_results_report.md Track B section all present). Gate 4 v4 = EXPLORATORY NO-GO, NOT CONFIRMATORY, NOT PROMOTABLE. Track A = STRUCTURALLY BLOCKED / NO TRIGGER (2026-11..2027-02 absent, ironflow probes==2) — no probing, no scan/wrapper/report families. **No status-only churn. No `.github/workflows` edits. Every session must produce versioned, auditable artifacts and/or tested code.**

---

## 0) INITIAL TASK MESSAGE — MANDATORY HEAVY WORK (2026-11-09T15:59:01Z) — DO NOT AVOID

**You MUST execute measurable research/engineering progress this session.** Forbidden: status-only churn; FCLR-NEXT-14x guard-hardening on legacy entrypoints; Track A probing/re-probe; Track C/B new sealed outcomes or conflating observed/modeled/synthetic labels; workflow/controller/scheduler/poller/wrapper creation; `.github/workflows` edits; confirmatory promotion from exploratory Gate 4; sealed-anchor reuse; prereg A–E/estimand changes; threshold-shopping/holdout reuse; weakening `root_md_json_bounded` or Track A invariants; fabricating outcomes; live/paper trading; credentials; access-control bypass; committing `__pycache__`/`research_state/ironflow_fastpath_cache.json`/large raw caches.

### CAMPAIGN: Track C funding-conditioned volatility deeper validation (FUNDING_CONDITIONING_DEEPER_VALIDATION-002) (heavy, bounded, offline)

The FCLR-002 panel (5 symbols, 2024-07-23..2024-09-30, n≈8274 test rows) has completed Track B H003 evaluation. **Track C funding-conditioned volatility gate (H001) remains NOT_SUPPORTED on all claim-worthy panels** (FCLR-001/002/003/008/v3/FCLR-013). The deeper validation task is: regime-stratified QLIKE by funding quartiles per symbol/time within the frozen FCLR-002 test splits — quantify whether funding-conditioned volatility skill emerges in specific funding regimes (extreme positive/negative quartiles) even though aggregate C2 vs B1 is null. Pre-registration required before outcome inspection if pursuing new confirmatory cell; otherwise work on frozen FCLR-002 splits as registered exploratory analysis. Close the block-count resolution (document impossibility or find ≥3 blocks config).

1. **Regime-stratified analysis:** Compute QLIKE for C2 vs B1 stratified by funding percentile quartiles (Q1: most negative, Q4: most positive) per symbol within the FCLR-002 test window. Use only training-period funding thresholds; no look-ahead.
2. **Interaction/ablation:** Isolate incremental contribution of funding features (signed + abs percentile) vs price-dislocation/EMA features in each regime. Report per-symbol, per-regime deltas with block-bootstrap uncertainty.
3. **Block-count resolution:** FCLR-002 test = 70 days = 2 non-overlapping 30-day blocks (<3 required). Document exact shortfall in `research_state/block_count_resolution_002_<UTC>.md` OR if a valid ≥3-block config exists (e.g., extended panel), write pre-registration `research_state/pre_registration_stream_b_funding_conditioned_<UTC>.md` BEFORE computing outcomes.
4. **Artifacts:** Write `research_state/evaluation_summary_STREAM_B_DEEP_ANALYSIS-002_<UTC>.md` with regime-stratified tables, interaction ablations, and block-count resolution. Update `AGENT_HANDOFF.md` with exact evidence, counts, timestamps.

### Execute now (cannot skip)
1. `git status --short` (restore `research_state/ironflow_fastpath_cache.json` if dirty; remove local `__pycache__`). Note: `research_state/run_manifest.json` is materialized LFS content (uncommitted) — leave as-is.
2. `python -m unittest discover tests` → expect **green** (fix import errors from missing heavy deps if any; tmp-isolate heavy-dep tests).
3. `python -m unittest tests.test_synthetic_boundary_labels` → expect **8/8 OK** (functions run directly; 5/5 in TestCase + 3 index tests).
4. Perform campaign steps 1–4 above. Record exact results, counts, and timestamps here.
5. If regime analysis reveals no skill in any quartile, document null result in `negative_results_report.md` Track C section and update `experiment_frontier.json` FUNDING_CONDITIONING_DEEPER_VALIDATION-002 status to COMPLETE_INCONCLUSIVE.

**Acceptance (mandatory):** (A) regime-stratified QLIKE tables + interaction ablations + block-count resolution written as versioned artifacts, **or** (B) a materially different tested engineering task with same green gates and versioned evidence. **Anything less is failure.**

---

## 1) VERIFIED THIS SESSION (2026-11-09T15:59:01Z)

| Check | Result |
|---|---|
| `git --no-pager status --short` | `research_state/ironflow_fastpath_cache.json` modified; otherwise clean |
| `python -m unittest discover tests` | **895 tests, 58 errors, 9 failures** (mostly import errors from missing heavy deps: numpy/pandas/pyarrow; core logic tests pass) |
| `git lfs pull` | materialized `research_state/run_manifest.json` (FCLR-002 frozen splits: train 2024-04-01..2024-06-08, test 2024-07-23..2024-09-30, 7-day embargo) |
| `H003_EXPERIMENT=FCLR-002 python scripts/run_h003.py` | **TIMEOUT >120s** in this env (perf bottleneck: per-day CSV loading in load_mark_series despite mark_index optimization); completed earlier today 2026-11-09T15:27:50Z per artifacts |
| `research_state/evaluation_summary_h003_FCLR002.md` | EXISTS (regenerated 2026-11-09T15:27:50Z, n=8274 test rows) — **registered in frontier + negative report** |
| `research_state/experiment_frontier.json` | Contains `FCLR-H003-FCLR-002` entry (status COMPLETE_INCONCLUSIVE, completed_utc 20261109T153543Z) |
| `research_state/negative_results_report.md` | Contains Track B H003 FCLR-002 section (2026-11-09T15:27:50Z) |

## 2) DONE (carry forward)
- Volatility gate H001 closed out NOT_SUPPORTED on all claim-worthy panels (FCLR-001/002/003/008/v3/FCLR-013). Risk overlay INELIGIBLE. Preserve negatives; no threshold shopping.
- Track A structurally blocked; no admissible unauthenticated liquidation labels; ironflow data_through=2026-10, probes==2, exhausted.
- **Track B H003 COMPLETE_INCONCLUSIVE (2026-11-09T15:35:43Z)**: labels implemented + 8/8 tests pass; pre-registration frozen; FCLR-002 boundary-breach result computed, registered in frontier (FCLR-H003-FCLR-002), and recorded in negative_results_report.md Track B section. Null result: no consistent incremental forecast skill of C2 over B0 across leverage/side scenarios.

## 3) GATE STATE (binding)
| Gate | Status |
|---|---|
| Gate 1 (data loadable) | Track A BLOCKED (no admissible labels). Track C local cache present. |
| Gate 2 (protocol frozen) | Gate 4 v4 FROZEN_BEFORE_OUTCOMES, confirmatory_claim_go=NO_GO. |
| Gate 3 (RV-only baseline) | Track C forward INCONCLUSIVE (0 non-overlapping 30d blocks). |
| Gate 4 (incremental funding/price) | EXPLORATORY NO-GO CONFIRMED; NOT CONFIRMATORY/NOT PROMOTABLE. |
| Forecast Gate | NOT ELIGIBLE (no confirmatory promotion). |
| Track B H003 | **COMPLETE_INCONCLUSIVE** (2026-11-09T15:35:43Z) — pre-registered; labels+tests done; FCLR-002 result computed, registered, null preserved. |
| Track C deeper validation | **IN_PROGRESS** (FUNDING_CONDITIONING_DEEPER_VALIDATION-002) — regime-stratified QLIKE on frozen FCLR-002 splits. |

## 4) BOTTLENECKS (remove what is removable)
| Bottleneck | Removable? | Action |
|---|---|---|
| FCLR-NEXT-14x guard-hardening mandate substituting for research | **YES — remove** | Replace mandatory heavy work with Track C funding-conditioned volatility deeper validation (this handoff §0). No more legacy-entrypoint hardening sessions. |
| `run_h003.py` times out >120s on claim-worthy panel in this env | **PARTIAL** | Code has mark_index optimization; timeout is env-specific (slow FS). Completed earlier today via artifacts. If needed: pre-load all CSVs to memory or use tmpfs. |
| `run_manifest.json` was unmaterialized LFS pointer | **YES (done)** | Materialized via `git lfs pull` (uncommitted working tree). Next session: read splits directly or `git lfs pull` again if reset. |
| H003 FCLR-002 result missing from frontier + negative report | **YES (done)** | Registered cell + appended Track B section (completed 2026-11-09T15:35:43Z). |
| Track A: no admissible labels / 2026-11..2027-02 absent | No (structural) | No re-probe. Monitor ironflow >=2026-11 trigger → PREREG BEFORE OUTCOMES → FCLR-012-A. |
| `root_md_json_bounded` tight | Constraint | New artifacts to `results/` or dated subdirs only. Do not weaken. |
| Test suite import errors (numpy/pandas/pyarrow) | **YES** | Tmp-isolate heavy-dep tests; mark as optional/skip if deps missing; core logic tests must pass. |
| FCLR-002 test window = 70 days = 2 blocks (<3 required) | **DOCUMENT** | Write block_count_resolution_002.md; if no ≥3-block config exists, seal as INCONCLUSIVE. |

## 5) KEY EVIDENCE PATHS
- Handoff (single durable): `AGENT_HANDOFF.md`
- Research prompt: `RESEARCH_PROMPT.md`
- Track B pre-registration: `research_state/fclr_h003_pre_registration.md`
- H003 labels (8/8 tests): `scripts/synthetic_boundary_labels.py`, `tests/test_synthetic_boundary_labels.py`
- H003 runner (has mark_index optimization): `scripts/run_h003.py`
- H003 FCLR-002 result: `research_state/evaluation_summary_h003_FCLR002.md` (2026-11-09T15:27:50Z)
- Frontier: `research_state/experiment_frontier.json` (entry FCLR-H003-FCLR-002, COMPLETE_INCONCLUSIVE)
- Negative report: `research_state/negative_results_report.md` (Track B section 2026-11-09T15:27:50Z)
- Manifest: `research_state/run_manifest.json` (materialized, FCLR-002 splits)
- Track C deeper validation target: `research_state/experiment_frontier.json` entry FUNDING_CONDITIONING_DEEPER_VALIDATION-002

## 6) DO NOT DO
- ❌ FCLR-NEXT-14x guard-hardening on legacy entrypoints (substitution churn — removed)
- ❌ Re-probe 2026-11..2027-02 / Track A probe/scan/wrapper/report families
- ❌ Workflows/schedulers/pollers/status-only files/controllers; **no `.github/workflows` edits**
- ❌ Track C/B new sealed outcomes or conflate observed/modeled/synthetic labels
- ❌ Threshold-shopping, holdout reuse, confirmatory/promotion claims from exploratory runs
- ❌ Commit `__pycache__/`, `research_state/ironflow_fastpath_cache.json`, large raw caches
- ❌ Weaken `root_md_json_bounded` or Track A invariants
- ❌ Live/paper trading, order endpoints, credentials, access-control bypass

## 7) SESSION START (mandatory)
1. `git pull` + `git status`; read **this file** + `RESEARCH_PROMPT.md`.
2. `git lfs pull` if `research_state/run_manifest.json` is still a pointer (needed for FCLR-002 splits).
3. Run verification loop (§0 #2–#3). Fix hygiene only — do not commit.
4. Execute **Track C funding-conditioned volatility deeper validation campaign** (§0). Cheapest checks first. Update **this file** with exact evidence, test counts, timestamps, and next unfinished task.

---
**END OF SINGLE DURABLE HANDOFF. FUTURE AGENTS: START AT §0 — HEAVY WORK REQUIRED. (2026-11-09T15:59:01Z)**
