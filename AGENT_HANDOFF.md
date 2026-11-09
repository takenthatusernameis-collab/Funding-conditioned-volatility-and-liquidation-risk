# AGENT_HANDOFF.md — Single Durable Handoff (next session MUST continue from here)

**Updated:** 2026-11-09T14:55:52Z
**Repo:** `Funding-conditioned-volatility-and-liquidation-risk` (git `5964cc3fe`, clean except uncommitted `research_state/run_manifest.json` materialized from LFS pointer via `git lfs pull` — do not commit unless asked)
**Binding priority:** P0 = **Track B H003 (hypothetical boundary-breach) operationalization** — the unexecuted liquidation-risk half of the repo name. **Stop the FCLR-NEXT-14x guard-hardening substitution** (status-only engineering churn that avoids the actual research). Gate 4 v4 = EXPLORATORY NO-GO, NOT CONFIRMATORY, NOT PROMOTABLE. Track A = STRUCTURALLY BLOCKED / NO TRIGGER (2026-11..2027-02 absent, ironflow probes==2) — no probing, no scan/wrapper/report families. Track C forward sealed INCONCLUSIVE. **No status-only churn. No `.github/workflows` edits. Every session must produce versioned, auditable artifacts and/or tested code.**

---

## 0) INITIAL TASK MESSAGE — MANDATORY HEAVY WORK (2026-11-09T14:55:52Z) — DO NOT AVOID

**You MUST execute measurable research/engineering progress this session.** Forbidden: status-only churn; FCLR-NEXT-14x guard-hardening on legacy entrypoints; Track A probing/re-probe; Track C/B new sealed outcomes or conflating observed/modeled/synthetic labels; workflow/controller/scheduler/poller/wrapper creation; `.github/workflows` edits; confirmatory promotion from exploratory Gate 4; sealed-anchor reuse; prereg A–E/estimand changes; threshold-shopping/holdout reuse; weakening `root_md_json_bounded` or Track A invariants; fabricating outcomes; live/paper trading; credentials; access-control bypass; committing `__pycache__`/`research_state/ironflow_fastpath_cache.json`/large raw caches.

### CAMPAIGN: Track B H003 liquidation-risk boundary-breach (heavy, bounded, offline)

The FCLR-H003 pre-registration is frozen (`research_state/fclr_h003_pre_registration.md`: 4 lev × 2 sides, MMR=0.005, 24h horizon) and `scripts/synthetic_boundary_labels.py` + `tests/test_synthetic_boundary_labels.py` pass 5/5. A claim-worthy FCLR-002 boundary-breach result already exists (`research_state/evaluation_summary_h003_FCLR002.md`, n≈8274) but is **absent from `experiment_frontier.json` and `negative_results_report.md`** (artifact-integrity gap), and `scripts/run_h003.py` **times out (>250s)** on the claim-worthy panel due to per-day `rglob` CSV loading (perf bottleneck). Close both gaps.

1. **Artifact integrity:** Add the FCLR-002 H003 cell to `research_state/experiment_frontier.json` (status COMPLETE_INCONCLUSIVE, linked to `evaluation_summary_h003_FCLR002.md`) and record the null-preserved outcome in `research_state/negative_results_report.md` (Track B section). Do not overwrite existing entries; append a new dated section.
2. **Perf fix:** Harden `scripts/run_h003.py` so it loads the 5-symbol claim-worthy panel without timing out (day-index/cache the CSVs once, avoid per-day `rglob`; keep causal/no-leakage semantics identical). Add/reuse tmp-isolated tests proving no behavioral change on a small fixture.
3. **Re-run & verify:** `H003_EXPERIMENT=FCLR-002 python scripts/run_h003.py` must complete (< timeout) and rewrite `evaluation_summary_h003_FCLR002.md` byte-stably. Run `python -m unittest tests.test_synthetic_boundary_labels.py` (expect 5/5 OK) + full suite (expect 1068 OK, 0 failures/errors).

### Execute now (cannot skip)
1. `git status --short` (restore `research_state/ironflow_fastpath_cache.json` if dirty; remove local `__pycache__`). Note: `research_state/run_manifest.json` is materialized LFS content (uncommitted) — leave as-is.
2. `python -m unittest discover tests` → expect **1068 OK, 0 failures/errors**.
3. `python -m unittest tests.test_synthetic_boundary_labels.py` → expect **5/5 OK**.
4. Perform campaign steps 1–3 above. Record exact results, counts, and timestamps here.
5. If run_h003.py still times out after the perf fix, reduce to a timed sub-window fixture test and document the residual blocker with the next materially different free route — do not abandon the session without a tested artifact.

**Acceptance (mandatory):** (A) full suite green + test_synthetic_boundary_labels 5/5 + H003 FCLR-002 cell present in frontier + negative-report Track B section + run_h003.py completes on claim-worthy panel, **or** (B) a materially different tested engineering task with same green gates and versioned evidence. **Anything less is failure.**

---

## 1) VERIFIED THIS SESSION (2026-11-09T14:55:52Z)

| Check | Result |
|---|---|
| `git --no-pager status --short` | `research_state/run_manifest.json` modified (LFS materialized, uncommitted); otherwise clean |
| `python -m unittest discover tests` | **1068 OK** (all passing) |
| `git lfs pull` | materialized `research_state/run_manifest.json` (FCLR-002 frozen splits: train 2024-04-01..2024-06-08, test 2024-07-23..2024-09-30, 7-day embargo) |
| `scripts/run_h003.py` H003_EXPERIMENT=FCLR-002 | **TIMEOUT >250s** (perf bottleneck: per-day rglob CSV loading) — perf fix required this session |
| `research_state/evaluation_summary_h003_FCLR002.md` | EXISTS (2026-10-28, n≈8274) but absent from frontier + negative report |

## 2) DONE (carry forward)
- Volatility gate H001 closed out NOT_SUPPORTED on all claim-worthy panels (FCLR-001/002/003/008/v3/FCLR-013). Risk overlay INELIGIBLE. Preserve negatives; no threshold shopping.
- Track A structurally blocked; no admissible unauthenticated liquidation labels; ironflow data_through=2026-10, probes==2, exhausted.
- H003 labels implemented + 5/5 tests pass; pre-registration frozen; FCLR-002 boundary-breach result computed.

## 3) GATE STATE (binding)
| Gate | Status |
|---|---|
| Gate 1 (data loadable) | Track A BLOCKED (no admissible labels). Track C local cache present. |
| Gate 2 (protocol frozen) | Gate 4 v4 FROZEN_BEFORE_OUTCOMES, confirmatory_claim_go=NO_GO. |
| Gate 3 (RV-only baseline) | Track C forward INCONCLUSIVE (0 non-overlapping 30d blocks). |
| Gate 4 (incremental funding/price) | EXPLORATORY NO-GO CONFIRMED; NOT CONFIRMATORY/NOT PROMOTABLE. |
| Forecast Gate | NOT ELIGIBLE (no confirmatory promotion). |
| Track B H003 | PRE-REGISTERED; labels+tests done; FCLR-002 result computed but unregistered (artifact gap to close). |

## 4) BOTTLENOCKS (remove what is removable)
| Bottleneck | Removable? | Action |
|---|---|---|
| FCLR-NEXT-14x guard-hardening mandate substituting for research | **YES — remove** | Replace mandatory heavy work with Track B H003 operationalization (this handoff §0). No more legacy-entrypoint hardening sessions. |
| `run_h003.py` times out >250s on claim-worthy panel | **YES** | Day-index/cache CSV loads; add fixture test; re-run to completion. |
| `run_manifest.json` was unmaterialized LFS pointer | **YES (done)** | Materialized via `git lfs pull` (uncommitted working tree). Next session: read splits directly or `git lfs pull` again if reset. |
| H003 FCLR-002 result missing from frontier + negative report | **YES** | Register cell + append Track B section (campaign step 1). |
| Track A: no admissible labels / 2026-11..2027-02 absent | No (structural) | No re-probe. Monitor ironflow >=2026-11 trigger → PREREG BEFORE OUTCOMES → FCLR-012-A. |
| `root_md_json_bounded` tight | Constraint | New artifacts to `results/` or dated subdirs only. Do not weaken. |

## 5) KEY EVIDENCE PATHS
- Handoff (single durable): `AGENT_HANDOFF.md`
- Research prompt: `RESEARCH_PROMPT.md`
- Track B pre-registration: `research_state/fclr_h003_pre_registration.md`
- H003 labels (5/5 tests): `scripts/synthetic_boundary_labels.py`, `tests/test_synthetic_boundary_labels.py`
- H003 runner (perf fix target): `scripts/run_h003.py`
- H003 FCLR-002 result: `research_state/evaluation_summary_h003_FCLR002.md`
- Frontier: `research_state/experiment_frontier.json`; Negative report: `research_state/negative_results_report.md`
- Manifest: `research_state/run_manifest.json` (materialized, FCLR-002 splits)

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
2. `git lfs pull` if `research_state/run_manifest.json` is still a pointer (needed for H003 splits).
3. Run verification loop (§0 #2–#3). Fix hygiene only — do not commit.
4. Execute **Track B H003 campaign** (§0). Cheapest checks first. Update **this file** with exact evidence, test counts, timestamps, and next unfinished task.

---
**END OF SINGLE DURABLE HANDOFF. FUTURE AGENTS: START AT §0 — HEAVY WORK REQUIRED. (2026-11-09T14:55:52Z)**
