# AGENT_HANDOFF.md — Single Durable Handoff (next session MUST continue from here)

**Updated:** 2026-11-09T18:16:48Z — refreshed initial task message + bottleneck removal confirmation.
**Repo:** `Funding-conditioned-volatility-and-liquidation-risk` — repo-name priority: **funding-conditioned volatility (Track C) first**; Track A liquidation risk is structurally blocked (no admissible unauthenticated liquidation labels; ironflow `data_through=2026-10`; forward edge 2026-11..2027-02 absent; probes==2 exhausted). `git status --short`: clean. Do **not** commit large raw caches/data zips, `__pycache__`, `ironflow_fastpath_cache.json`, or workflow changes.
**Binding priority:** P0 = **Track C funding-conditioned volatility — frozen confirmatory-readiness skeleton created; no confirmatory data exists today (2 blocks < 3); no confirmatory claims**. `FUNDING_CONDITIONING_DEEPER_VALIDATION-002` = **COMPLETE_INCONCLUSIVE (EXPLORATORY_ONLY, 2026-11-09T16:39:00Z)**. Track B H003 = **COMPLETE_INCONCLUSIVE (2026-11-09T15:35:43Z)**. Track A = **STRUCTURALLY BLOCKED / NO TRIGGER** — **no probing, no scan/wrapper/report families**. **No status-only churn. No `.github/workflows` edits. No confirmatory promotion from exploratory results. No sealed-holdout reuse, threshold shopping, or conflating observed/modeled/synthetic labels. Every session must produce versioned, auditable artifacts and/or tested code.**

---

## 0) INITIAL TASK MESSAGE — 2026-11-09T18:16:48Z — MANDATORY HEAVY WORK (DO NOT AVOID)

**Repo-name priority:** `Funding-conditioned-volatility-and-liquidation-risk` → **Track C funding-conditioned volatility first**. Track A (liquidation risk) is structurally blocked (no admissible unauthenticated liquidation labels; ironflow `data_through=2026-10`; forward edge 2026-11..2027-02 absent; probes==2 exhausted) — **no probing, no scan/wrapper/report families, no guard-hardening churn absent a trigger**. Track B H003 = COMPLETE_INCONCLUSIVE — do not merge tracks.

**Execute measurable research/engineering progress this session.** Forbidden: status-only churn; Track A probing/re-probe; Track A guard-hardening substitution on legacy entrypoints (FCLR-NEXT-131 guard hardening COMPLETE — frozen, no further Track A code churn absent an admissible trigger); Track C/B new sealed outcomes without frozen prereg; conflating observed/modeled/synthetic labels; workflow/controller/scheduler/poller/wrapper creation; `.github/workflows` edits; confirmatory claims from exploratory runs; sealed-anchor reuse; prereg/estimand changes; threshold-shopping/holdout reuse; weakening `root_md_json_bounded` or Track A invariants; fabricating outcomes; live/paper trading; credentials; access-control bypass.

### Bottleneck removal (sessions blocked/inefficient → unblock significant progress)
- **Track A guard-hardening bottleneck REMOVED:** `FCLR-NEXT-131` (G1-G3 harness/operator/guard snapshot hardening) is COMPLETE; `root_md_json_bounded<=163`, `probes==2`, no trigger. Track A remains structurally blocked with no admissible trigger. Continuing Track A hardening is status-only churn and is stopped. No further Track A entrypoint/script/registry work unless a rubric-GO unauthenticated liquidation source appears (then PREREG before outcomes).
- **Track C confirmatory bottleneck = data, not code:** FCLR-002 test = 2 non-overlapping 30-day blocks (< 3 required); Binance archive ends 2026-11-02; no cached >=3-block unsealed panel. No code change removes this. Admissible heavy work = resume-trigger watch + dep-light gate only, until a >=5-symbol/>=3-block panel appears.

### Completed heavy work (evidence recorded)
1. **Track C reproducibility + audit hardening — COMPLETE.** `research_state/trackc_reproducibility_audit_20261109T175518Z.md` covers: (a) SHA256/size/mtime for `evaluation_summary_STREAM_B_DEEP_ANALYSIS-001_20261109T162703Z.md`, `-002_20261109T163517Z.md`, `data_cache/fclr002_panel.json`, `run_manifest.json`, `experiment_frontier.json`, `negative_results_report.md`, `block_count_resolution_20261103T102000Z.md`, `AGENT_HANDOFF.md`; (b) exact rerun commands (`PYTHONPATH=$PWD python scripts/run_stream_b_deep_analysis_001.py`, `..._002.py`) + environment deps (numpy/pandas/scipy OK; pyarrow/sklearn/matplotlib MISSING); (c) 2-block confirmatory blocker evidence (FCLR-002 test `2024-07-23..2024-09-30` = 70 days = **2** non-overlapping 30-day blocks < 3 required; Binance archive ends **2026-11-02**; no cached >=3-block unsealed panel ready); (d) single next confirmatory path with concrete prereg skeleton filename `research_state/pre_registration_fclr014_confirmatory_funding_vol_<UTC>.json` to create **before any outcome inspection** if/when a >=3-block admissible panel appears.
2. **Frozen preregistration skeleton created — COMPLETE (before outcomes).** `research_state/pre_registration_fclr014_confirmatory_funding_vol_20261109T181124Z.json` written, frozen `FROZEN_BEFORE_OUTCOMES`, `frozen_before_outcomes: true`, `outcome_metrics_present: false`, `outcome_values_inspected: false`, `confirmatory_claim_go: NO_GO`, git SHA `6b1944866785eb08de1149f7a8b57fa12d3fc056`, frozen at `2026-11-09T18:11:24Z`, SHA256 `4adf609e3f6b57ae7e0ad486150c787799c19d1b33432ebc5125bd33dde0073c`. Contents: FCLR-H001/FCLR-H002 hypotheses, universe (>=5 symbols BTC/ETH/BNB/SOL/XRP, binance_um_perp, unauthenticated archive), admissibility source rules (no auth/payment/manual key/bypass; provenance URLs/ETags/checksums), unit/timing, primary target next-24h realized variance of mark-price returns (secondary 6h/72h/168h), causal features (RV1h/24h/168h, signed+abs funding, 90-day trailing percentile >=30 obs rule, mark/index premium, mark/EMA24 distance; train-only normalization, no fill), chronological train/val/test splits with 7-day purge/embargo (FCLR-002 illustrative windows copied; NOT frozen for FCLR-014 until a >=3-block panel is verified), baselines B0/B1/C1/C2 (OLS log-linear, no tuning), primary contrast C2 vs B1 test QLIKE, block-bootstrap 2000 reps joint across instruments, Holm multiplicity, decision gates (>=3-block rule, >=2% relative QLIKE, CI supports improvement, concentration/calibration/leakage conditions), resume trigger (>=5 symbols, >=3 non-overlapping 30-day OOS admissible panel), do-not list. **Zero outcome values inspected.**
3. **Dep-light test gate — GREEN.** `python -m unittest tests.test_synthetic_boundary_labels` → **Ran 8 tests — OK** (8/8, verified 2026-11-09T18:14:52Z). Full `discover` blocked if heavy-dep import errors; record counts only, never fabricate.
4. **Resume-trigger watchlist — documented** in audit artifact §5: new unauthenticated, provenance-auditable Binance (or equivalently admissible public) panel with **>=5 symbols** and **>=3 non-overlapping 30-day OOS blocks** (or equivalent pre-registered design), plus full preregistration frozen before outcomes. Track A trigger rules unchanged. Default: **no network probing**.

### Next focus campaign — mandatory, measurable, unavoidable (next session, do in order)

**Campaign: Track C confirmatory-readiness (repo P0 — funding-conditioned volatility first).** Confirmatory data does NOT exist today (2 blocks < 3; archive ends 2026-11-02), so the admissible heavy work this session was the frozen preregistration skeleton; going forward the only admissible heavy work is the resume-trigger watch and keeping the dep-light gate green until a >=3-block admissible panel appears.

1. **Create `research_state/pre_registration_fclr014_confirmatory_funding_vol_<UTC>.json`** — **DONE** (2026-11-09T18:11:24Z): `research_state/pre_registration_fclr014_confirmatory_funding_vol_20261109T181124Z.json`, SHA256 `4adf609e3f6b57ae7e0ad486150c787799c19d1b33432ebc5125bd33dde0073c`, frozen before outcomes, zero outcome values inspected. Do not build/peek the panel yet; do not compute outcomes against this skeleton.
2. **Verify dep-light tests green each session:** `python -m unittest tests.test_synthetic_boundary_labels` → **DONE** (Ran 8 tests — OK, 8/8, verified 2026-11-09T18:14:52Z). Record exact count every session. If actionable, add/extend one small stdlib-only unit test around real `src/volatility/*` code paths (no placeholder tests). Record exact test counts.
3. **Resume-trigger watch — THE NEXT UNFINISHED TASK (do not skip):** re-confirm resume-trigger evidence in this file (>=5 symbols, >=3 non-overlapping 30-day blocks, prereg before outcomes); no network probing unless a single bounded admissible check with provenance logged. Current evidence: FCLR-002 test = 2 blocks (< 3); Binance archive ends 2026-11-02; FCLR-012-V forward (2026-10-29..2026-11-02 = 5 days = 0 blocks) INCONCLUSIVE; no cached >=3-block unsealed panel. **Await a new admissible panel meeting the >=5-symbol/>=3-block rule; do not probe by default.** When a panel appears, freeze a new preregistration version before any outcome inspection, then build/evaluate.
4. **Update this file** every session with exact evidence, file hashes, commands, test counts, timestamps, and the next unfinished task — **DONE this session (2026-11-09T18:16:48Z)**.

**Acceptance (mandatory):** (A) frozen prereg skeleton `pre_registration_fclr014_confirmatory_funding_vol_20261109T181124Z.json` present + zero outcome values inspected + dep-light 8/8 recorded + `AGENT_HANDOFF.md` updated, **or** (B) a materially different tested engineering/research task with the same evidence discipline. **Anything less is failure.** Track A Track-guard hardening is frozen and must not be reopened absent a trigger — future agents may not substitute it for Track C heavy work.

---

## 1) VERIFIED (2026-11-09T18:16:48Z)

| Check | Result |
|---|---|
| `git status --short` | clean |
| `python -m unittest tests.test_synthetic_boundary_labels` | **Ran 8 tests — OK** |
| Reproducibility audit artifact | `research_state/trackc_reproducibility_audit_20261109T175518Z.md` present; hashes/size/mtime/env recorded (sub-items a–d complete) |
| Prereg skeleton `pre_registration_fclr014_confirmatory_funding_vol_*` | **PRESENT** `research_state/pre_registration_fclr014_confirmatory_funding_vol_20261109T181124Z.json` (SHA256 `4adf609e...`); status FROZEN_BEFORE_OUTCOMES; zero outcome values inspected; frozen 2026-11-09T18:11:24Z; git SHA `6b194486...` |
| STREAM_B artifacts | both summaries present (001 `162703Z`, 002 `163517Z`) |
| Frontier/negative report | `FUNDING_CONDITIONING_DEEPER_VALIDATION-002` COMPLETE_INCONCLUSIVE (exploratory); Track C negative section present |
| Track A | no trigger; no re-probe performed |

---

## 2) DONE (carry forward)

- Volatility gate H001 closed NOT_SUPPORTED on claim-worthy panels (FCLR-001/002/003/008/v3/FCLR-013). Risk overlay INELIGIBLE.
- Track A structurally blocked; no admissible unauthenticated liquidation labels; ironflow probes==2 exhausted.
- Track B H003 **COMPLETE_INCONCLUSIVE** (2026-11-09T15:35:43Z).
- Track C `FUNDING_CONDITIONING_DEEPER_VALIDATION-002` **COMPLETE_INCONCLUSIVE (EXPLORATORY_ONLY)** (2026-11-09T16:39:00Z) — robust Q1 regime skill but 2 blocks < 3; not confirmatory.
- `test_synthetic_boundary_labels` dep-light: 8/8 OK.
- `trackc_reproducibility_audit_20261109T175518Z.md` written (hashes, commands, blocker evidence, prereg resume path).

---

## 3) GATE STATE (binding)

| Gate | Status |
|---|---|
| Gate 1 | Track A BLOCKED; Track C cache/manifests present (frozen FCLR-002 splits) |
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
| Confirmatory Track C impossible on current data (2 blocks, archive ends 2026-11-02) | structural/data | Record reproducibly; freeze prereg skeleton before outcomes; define resume path; no fake confirmatory run |
| `pre_registration_fclr014_confirmatory_funding_vol_<UTC>.json` not yet created | actionable | **DONE** 2026-11-09T18:11:24Z — `research_state/pre_registration_fclr014_confirmatory_funding_vol_20261109T181124Z.json` (SHA256 `4adf609e...`), frozen before outcomes, 0 outcomes inspected. Next: resume-trigger watch only (>=5 symbols, >=3 non-overlapping 30-day blocks); no default probing. |
| numpy/pandas/scipy missing in some runners | env | Use stdlib/deplight tests + existing analysis artifacts; tmp-isolate heavy-dep tests |
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
- `research_state/trackc_reproducibility_audit_20261109T175518Z.md`
- `research_state/block_count_resolution_20261103T102000Z.md`
- `research_state/fclr_h003_pre_registration.md`, `research_state/evaluation_summary_h003_FCLR002.md`
- `research_state/pre_registration_fclr014_confirmatory_funding_vol_20261109T181124Z.json` (frozen prereg skeleton, zero outcomes inspected)
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
3. Run dep-light verification: `python -m unittest tests.test_synthetic_boundary_labels` (record count; expected 8/8). Do not fabricate full-suite results if heavy deps missing.
4. Execute **§0 Next focus campaign items 3–4** (resume-trigger watch: await new admissible >=5-symbol/>=3-block panel, no default probing; keep this file updated). Item 1 (prereg skeleton `research_state/pre_registration_fclr014_confirmatory_funding_vol_20261109T181124Z.json`) and item 2 (dep-light 8/8) already complete this session.
5. Update **this file** with exact evidence and next unfinished task.

---

**END OF SINGLE DURABLE HANDOFF. FUTURE AGENTS: START AT §0 — HEAVY WORK REQUIRED. (2026-11-09T18:16:48Z)**
