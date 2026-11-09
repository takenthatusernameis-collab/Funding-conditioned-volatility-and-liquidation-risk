# AGENT_HANDOFF.md — Single Durable Handoff (next session MUST continue from here)

**Updated:** 2026-11-09T20:11:56Z — **Track C heavy engineering (no outcomes, no network, no Track A probing).** Dep-light gate **22/22 OK** (22.332s): `python -m unittest tests.test_volatility_features_splits tests.test_synthetic_boundary_labels tests.test_trackc_panel_admissibility_audit -v`. Hardened `scripts/trackc_panel_admissibility_audit.py` (SHA256 `269a37fdd82181ba8019ee5148aa64e9b79f221c45a42a3d3c396671443442f4`) + `tests/test_trackc_panel_admissibility_audit.py` (`bb010ff07830677695f3544b1f79ebbbd710786826cf9aad69780941f1a9b88c`): machine-checkable per-series gap manifests (missing day ranges vs mark-union), funding month-file range coverage + explicit `NO_MONTH_FILES_FOR_RANGE`, heuristic 8h funding-slot diagnostic (gap-planning only, not completeness proof), deterministic local adjacent-`*.sha256` verification sample, and explicit `confirmatory_resume_ready=false` / `confirmatory_ready_symbol=false` blockers (funding/provenance/checksums + frozen prereg-before-outcomes still required). Regenerated audits (**all `outcomes_computed:false, network_used:false`**): `--window-hint 2026_11` → `resume_trigger_met=false, symbols_ok=5, panel_blocks=0`, required mark/index/premium complete, **BTC funding `NO_MONTH_FILES_FOR_RANGE` for 2026-11** (no `BTCUSDT-fundingRate-2026-11` month file in cache; 0 heuristic slots in 8-day range) — `research_state/trackc_panel_admissibility_2026_11.json`/`latest` (`b5d456f2ce2dcdea63c5d28343c53553a738d26fa5ee49bb9603358ab16a78e6`); all-cache → `resume_trigger_met=false, symbols_ok=0, panel_blocks=0`, BTC example has 31/32 index/premium day gaps vs mark (1041 mark days) and `PARTIAL_MONTH_FILES` (34/35 months) — `research_state/trackc_panel_admissibility_all_cache.json` (`33fe971990c83f450f930d0ea2da7e9c2f5dfe76d98ce5f2238f9865595e468f`). FCLR-014 prereg SHA256 re-verified `4adf609e3f6b57ae7e0ad486150c787799c19d1b33432ebc5125bd33dde0073c` (frozen before outcomes). **No `.github/workflows` edits. No confirmatory claims. No sealed-holdout reuse/threshold shopping.**
**Binding priority:** P0 = **Track C funding-conditioned volatility** (repo name). Frozen confirmatory skeleton exists; **no confirmatory data exists today** (no >=5-symbol/>=3-block admissible panel with verified funding+provenance+checksums). `FUNDING_CONDITIONING_DEEPER_VALIDATION-002` = **COMPLETE_INCONCLUSIVE (EXPLORATORY_ONLY, 2026-11-09T16:39:00Z)**. Track B H003 = **COMPLETE_INCONCLUSIVE (2026-11-09T15:35:43Z)**. Track A = **STRUCTURALLY BLOCKED / NO TRIGGER** — **no probing, no scan/wrapper/report families, no guard-hardening churn**. No status-only churn. No sealed-holdout reuse, threshold shopping, or conflating observed/modeled/synthetic labels.

---

## 0) INITIAL TASK MESSAGE — 2026-11-09T20:11:56Z — MANDATORY HEAVY WORK (NEXT SESSION, UNAVOIDABLE)

**START HERE. Repo P0 = Track C funding-conditioned volatility. Track A frozen/blocked — do not touch.** Latest dep-light gate is green (**22/22 OK**) and audits show **NO confirmatory trigger** (`confirmatory_resume_ready=false`). The next session MUST produce **measurable heavy progress**, not status narration.

### Do in order (pick the first applicable path and execute fully)
1. **Dep-light gate (record exact count):** `python -m unittest tests.test_volatility_features_splits tests.test_synthetic_boundary_labels tests.test_trackc_panel_admissibility_audit -v` → expect **18/18 OK**. Never fabricate full-suite if heavy deps missing.
2. **Resume-trigger watch (no network by default):** run `python scripts/trackc_panel_admissibility_audit.py [--window-hint <candidate>]` on any **new/changed** cached panel fragments. Current evidence (2026-11-09T19:50:22Z): `2026_11` window = 5 symbols × 8 days, 0 blocks (NOT MET); all-cache has funding/index/premium gaps making `required_series_complete=false` (NOT MET). **If `resume_trigger_met=false`: do not compute outcomes.**
3. **IF AND ONLY IF `resume_trigger_met=true` AND funding completeness + provenance (URLs/ETags/checksums) are verified for the panel:** (a) create/freeze a **new** preregistration version **before any outcome inspection** (derive from `pre_registration_fclr014_confirmatory_funding_vol_20261109T181124Z.json`, SHA256 `4adf609e…`, preserve its discipline; bump version/timestamp; record hashes); (b) materialize the panel + chronological splits with 7-day purge/embargo (>=3 non-overlapping 30-day OOS blocks, >=5 symbols) and write a run manifest; (c) run the confirmatory pipeline **only after prereg is frozen**: B0/B1/C1/C2, primary C2 vs B1 **test QLIKE**, block-bootstrap **2000** joint across instruments, **Holm** multiplicity, calibration/concentration/leakage checks per frozen prereg; (d) record all commands, artifact paths, hashes, metrics, uncertainty, and GO/NO-GO with adjusted results. **No sealed-holdout reuse, no threshold shopping, no tuning on test.**
4. **IF no confirmatory panel exists (current state):** do **tested Track C engineering that directly unblocks confirmatory readiness** (must land code + tests, not prose): e.g. extend `scripts/trackc_panel_admissibility_audit.py` to (i) detect/validate funding file completeness vs mark days, (ii) emit a machine-checkable gap manifest per symbol/series/day range for unauthenticated **local** archive repair planning, (iii) add deterministic provenance/checksum fields when sidecar metadata exists — **all stdlib, no network, no outcome computation**; or add dep-light coverage for the confirmatory feature/pipeline interfaces used by FCLR-014 (train-only normalization, embargo, OLS log-linear spec) with fixture tests. **Do not add Track A probing, wrappers, schedulers, or workflow edits.**
5. **Update `AGENT_HANDOFF.md`** with UTC timestamp, exact commands, test counts, audit JSON paths/hashes, any new file hashes, and the single next unfinished task.

### Hard constraints (violations = failure)
- No Track A probing/scans/wrappers/report families; no guard-hardening churn absent a rubric-GO unauthenticated liquidation trigger (then PREREG before outcomes).
- No confirmatory/promotion claims from exploratory runs; no sealed-holdout reuse; no threshold shopping; no prereg/estimand changes after seeing outcomes.
- Never conflate **observed** liquidations with **modeled/synthetic** boundary breaches (Track separation immutable).
- No `.github/workflows` edits; no schedulers/pollers/controllers; no credentials/paid data/access-control bypass; no live/paper trading.
- No fabricated outcomes. If blocked, record evidence + the next materially different admissible route.

### Bottleneck removal (kept explicit)
- **Track A guard-hardening bottleneck REMOVED:** `FCLR-NEXT-131` COMPLETE; `probes==2`, no trigger — **frozen**. Reopening = status-only churn.
- **Track C confirmatory blocker = admissible data:** requires >=5 symbols, >=3 non-overlapping 30-day OOS blocks, verified unauthenticated provenance/funding/checksums. 2026_11 cache fragment is 8 days (0 blocks); all-cache has series/funding gaps. **Data gap cannot be papered over by code** — but engineering that makes gaps/provenance machine-checkable is admissible heavy work.

### Completed heavy work (evidence recorded)
1. **Track C reproducibility + audit hardening — COMPLETE.** `research_state/trackc_reproducibility_audit_20261109T175518Z.md` covers: (a) SHA256/size/mtime for `evaluation_summary_STREAM_B_DEEP_ANALYSIS-001_20261109T162703Z.md`, `-002_20261109T163517Z.md`, `data_cache/fclr002_panel.json`, `run_manifest.json`, `experiment_frontier.json`, `negative_results_report.md`, `block_count_resolution_20261103T102000Z.md`, `AGENT_HANDOFF.md`; (b) exact rerun commands (`PYTHONPATH=$PWD python scripts/run_stream_b_deep_analysis_001.py`, `..._002.py`) + environment deps (numpy/pandas/scipy OK; pyarrow/sklearn/matplotlib MISSING); (c) 2-block confirmatory blocker evidence (FCLR-002 test `2024-07-23..2024-09-30` = 70 days = **2** non-overlapping 30-day blocks < 3 required; Binance archive ends **2026-11-02**; no cached >=3-block unsealed panel ready); (d) single next confirmatory path with concrete prereg skeleton filename `research_state/pre_registration_fclr014_confirmatory_funding_vol_<UTC>.json` to create **before any outcome inspection** if/when a >=3-block admissible panel appears.
2. **Frozen preregistration skeleton created — COMPLETE (before outcomes).** `research_state/pre_registration_fclr014_confirmatory_funding_vol_20261109T181124Z.json` written, frozen `FROZEN_BEFORE_OUTCOMES`, `frozen_before_outcomes: true`, `outcome_metrics_present: false`, `outcome_values_inspected: false`, `confirmatory_claim_go: NO_GO`, git SHA `6b1944866785eb08de1149f7a8b57fa12d3fc056`, frozen at `2026-11-09T18:11:24Z`, SHA256 `4adf609e3f6b57ae7e0ad486150c787799c19d1b33432ebc5125bd33dde0073c`. Contents: FCLR-H001/FCLR-H002 hypotheses, universe (>=5 symbols BTC/ETH/BNB/SOL/XRP, binance_um_perp, unauthenticated archive), admissibility source rules (no auth/payment/manual key/bypass; provenance URLs/ETags/checksums), unit/timing, primary target next-24h realized variance of mark-price returns (secondary 6h/72h/168h), causal features (RV1h/24h/168h, signed+abs funding, 90-day trailing percentile >=30 obs rule, mark/index premium, mark/EMA24 distance; train-only normalization, no fill), chronological train/val/test splits with 7-day purge/embargo (FCLR-002 illustrative windows copied; NOT frozen for FCLR-014 until a >=3-block panel is verified), baselines B0/B1/C1/C2 (OLS log-linear, no tuning), primary contrast C2 vs B1 test QLIKE, block-bootstrap 2000 reps joint across instruments, Holm multiplicity, decision gates (>=3-block rule, >=2% relative QLIKE, CI supports improvement, concentration/calibration/leakage conditions), resume trigger (>=5 symbols, >=3 non-overlapping 30-day OOS admissible panel), do-not list. **Zero outcome values inspected.**
3. **Dep-light test gate — GREEN.** `python -m unittest tests.test_synthetic_boundary_labels` → **Ran 8 tests — OK** (8/8, verified 2026-11-09T18:14:52Z). Full `discover` blocked if heavy-dep import errors; record counts only, never fabricate.
4. **Resume-trigger watchlist — documented** in audit artifact §5: new unauthenticated, provenance-auditable Binance (or equivalently admissible public) panel with **>=5 symbols** and **>=3 non-overlapping 30-day OOS blocks** (or equivalent pre-registered design), plus full preregistration frozen before outcomes. Track A trigger rules unchanged. Default: **no network probing**.
5. **Dep-light engineering hardening (this session, 2026-11-09T19:37:03Z) — COMPLETE.** Added `tests/test_volatility_features_splits.py` (8 tests, stdlib-only, no network, no outcome inspection): covers `src.volatility.features.log_returns/realized_variance/trailing_rv/forward_rv` and `src.volatility.splits.parse_iso/in_split` (frozen-split semantics used by evaluation pipeline). Command: `python -m unittest tests.test_volatility_features_splits tests.test_synthetic_boundary_labels -v` → **Ran 16 tests — OK** (8 + 8, 1.570s). `test_synthetic_boundary_labels` alone: **Ran 8 tests — OK** (1.549s). Full `discover` not claimed (heavy deps/env variance); dep-light gate green. No confirmatory outcomes computed; no sealed holdout touched.

---

## Next focus campaign — mandatory, measurable, unavoidable (next session, do in order)

**Campaign: Track C confirmatory-readiness (repo P0 — funding-conditioned volatility first).** Confirmatory data does NOT exist today (2 blocks < 3; archive ends 2026-11-02), so the admissible heavy work this session was the frozen preregistration skeleton; going forward the only admissible heavy work is the resume-trigger watch and keeping the dep-light gate green until a >=3-block admissible panel appears.

1. **Create `research_state/pre_registration_fclr014_confirmatory_funding_vol_<UTC>.json`** — **DONE** (2026-11-09T18:11:24Z): `research_state/pre_registration_fclr014_confirmatory_funding_vol_20261109T181124Z.json`, SHA256 `4adf609e3f6b57ae7e0ad486150c787799c19d1b33432ebc5125bd33dde0073c`, frozen before outcomes, zero outcome values inspected. Do not build/peek the panel yet; do not compute outcomes against this skeleton.
2. **Dep-light panel admissibility audit (this session, 2026-11-09T19:42:53Z) — COMPLETE (tested engineering, no outcomes).** Added `scripts/trackc_panel_admissibility_audit.py` (stdlib, no network, no target/feature/model computation) + `tests/test_trackc_panel_admissibility_audit.py` (2 tests). Gate: `python -m unittest tests.test_volatility_features_splits tests.test_synthetic_boundary_labels tests.test_trackc_panel_admissibility_audit -v` → **Ran 22 tests — OK** (22.332s, 2026-11-09T20:11:56Z; includes gap/funding/provenance fixture checks). Deterministic cached audit: `--window-hint 2026_11` → `resume_trigger_met=false, symbols_ok=5 (BTC/ETH/BNB/SOL/XRP, 8 days 2026-11-01..08, required mark/index/premium complete), panel_blocks=0`; all-cache → `resume_trigger_met=false, symbols_ok=0, panel_blocks=0`. Artifacts: `research_state/trackc_panel_admissibility_2026_11.json`, `research_state/trackc_panel_admissibility_all_cache.json` (`outcomes_computed:false, network_used:false`). Script does **not** satisfy prereg resume alone (funding completeness/provenance/checksums + frozen prereg-before-outcomes still required).
3. **Verify dep-light tests green each session:** **DONE (2026-11-09T19:42:53Z).** `python -m unittest tests.test_volatility_features_splits tests.test_synthetic_boundary_labels tests.test_trackc_panel_admissibility_audit -v` → **Ran 22 tests — OK** (22.332s, 2026-11-09T20:11:56Z; includes gap/funding/provenance fixture checks). Record exact count every session; do not fabricate full `discover` under heavy-dep variance.
4. **NEXT UNFINISHED TASK (mandatory, heavy): local deterministic gap/repair manifest for an existing cached candidate window — no outcomes, no network.** Use the new gap/provenance audit to produce a **tested, machine-checkable repair plan artifact** (stdlib, no network) for the highest-value local candidate: e.g. add `scripts/trackc_gap_repair_manifest.py` + tests that consumes `trackc_panel_admissibility_*.json` and local cache metadata to emit per-symbol/per-day missing-series ranges, missing funding month files (e.g. BTC 2026-11), and required local source/provenance actions/checksum expectations **without downloading** and **without computing outcomes**. Run it on `2026_11` and `all_cache`; record artifact hashes and exact commands. Only if a repair manifest shows a locally repairable path using already-present admissible files, perform the deterministic local repair with checksums/lineage; otherwise record the evidence-backed blocker. **Do not run confirmatory outcomes** unless `confirmatory_resume_ready` prerequisites are satisfied by verified data + a newly frozen prereg version before outcomes.
5. **Update this file** every session with exact evidence, file hashes, commands, test counts, timestamps, and the next unfinished task — **DONE this session (2026-11-09T20:11:56Z)**.


**Acceptance (mandatory):** (A) frozen prereg skeleton present + zero outcome values inspected + dep-light **22/22** recorded + admissibility/gap audit JSONs with `outcomes_computed:false, network_used:false, confirmatory_resume_ready:false` when blocked + `AGENT_HANDOFF.md` updated, **or** (B) a materially different tested engineering/research task with the same evidence discipline (code + tests + artifact hashes). **Anything less is failure.** Track A guard hardening is frozen and must not be reopened absent a trigger.

---

## 1) VERIFIED (2026-11-09T20:11:56Z)

| Check | Result |
|---|---|
| `git status --short` | `M research_state/trackc_panel_admissibility_all_cache.json`, `M research_state/trackc_panel_admissibility_latest.json` (audit outputs regenerated; handoff updated) |
| `python -m unittest tests.test_volatility_features_splits tests.test_synthetic_boundary_labels tests.test_trackc_panel_admissibility_audit -v` | **Ran 22 tests — OK** (22.332s, 2026-11-09T20:11:56Z) |
| `trackc_panel_admissibility_audit --window-hint 2026_11` (no network/outcomes) | `trackc_panel_admissibility_2026_11.json`/`latest` SHA256 `b5d456…`: **resume_trigger_met=false, confirmatory_resume_ready=false, symbols_ok=5, panel_blocks=0** (BTC/ETH/BNB/SOL/XRP 8 days 2026-11-01..08, required mark/index/premium complete; **BTC funding `NO_MONTH_FILES_FOR_RANGE` for 2026-11**, 0 heuristic 8h slots in range, no BTC 2026-11 funding month file in cache) |
| `trackc_panel_admissibility_audit` all-cache (no network/outcomes) | `trackc_panel_admissibility_all_cache.json` SHA256 `33fe97…`: **resume_trigger_met=false, confirmatory_resume_ready=false, symbols_ok=0, panel_blocks=0** (1041-day span; BTC 31/32 index/premium day gaps vs 1041 mark days; funding `PARTIAL_MONTH_FILES` 34/35 months; NOT confirmatory-admissible) |
| Prereg skeleton (frozen) | `research_state/pre_registration_fclr014_confirmatory_funding_vol_20261109T181124Z.json`, SHA256 `4adf609e3f6b57ae7e0ad486150c787799c19d1b33432ebc5125bd33dde0073c` (re-verified) — `FROZEN_BEFORE_OUTCOMES`, zero outcome values inspected |
| Track A guard state | `tracka_resume_check` `pass:false` only `root_md_json_bounded` (149>163 due RS audit artifacts); probes==2, ironflow trigger exhausted, **no re-probe/no trigger side effects** |
| STREAM_B / reproducibility | summaries `001 20261109T162703Z`, `002 20261109T163517Z`; `trackc_reproducibility_audit_20261109T175518Z.md` present |

**Admissibility note (actionable):** all-cache audit shows `index/premium` day counts < mark over 2024-01-01..2026-11-08 for all 5 symbols, so a full-span confirmatory panel is **not** admissible without deterministic gap repair/manifesting and provenance. Any repair must be local, unauthenticated, auditable, tested — and **no outcomes before a new frozen prereg**.

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
| Confirmatory Track C impossible on current audited data | structural/data | 2026_11 window lacks BTC 2026-11 funding month file in cache (`NO_MONTH_FILES_FOR_RANGE`) and is 0 blocks; all-cache has index/premium day gaps + partial funding months. **Next heavy work:** deterministic local `trackc_gap_repair_manifest` (tested, no network, no outcomes) to plan/verify any locally repairable gaps from already-present admissible files; if not locally repairable, record evidence-backed blocker (no download/probing). |
| `pre_registration_fclr014_confirmatory_funding_vol_<UTC>.json` not yet created | actionable | **DONE** 2026-11-09T18:11:24Z — `research_state/pre_registration_fclr014_confirmatory_funding_vol_20261109T181124Z.json` (SHA256 `4adf609e...`), frozen before outcomes, 0 outcomes inspected. Next: resume-trigger watch only (>=5 symbols, >=3 non-overlapping 30-day blocks); no default probing. |
| numpy/pandas/scipy missing in some runners | env | Use stdlib/deplight tests + existing analysis artifacts; tmp-isolate heavy-dep tests |
| Track A no admissible labels | structural | No re-probe; trigger-only with prereg before outcomes |
| Track A guard-hardening repetition (status-only churn) | removed | FCLR-NEXT-131 COMPLETE; frozen; no further Track A code churn absent admissible trigger |

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
- `scripts/trackc_panel_admissibility_audit.py` (SHA256 `269a37f…`, 2026-11-09T20:11:56Z hardened: gap manifests, funding range/month+slot heuristic, adjacent sha256 verify sample, `confirmatory_resume_ready=false`), `tests/test_trackc_panel_admissibility_audit.py` (`bb010f…`, 6 tests)
- `research_state/trackc_panel_admissibility_2026_11.json`, `research_state/trackc_panel_admissibility_all_cache.json`


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
3. Run dep-light verification: `python -m unittest tests.test_volatility_features_splits tests.test_synthetic_boundary_labels tests.test_trackc_panel_admissibility_audit -v` (record count; expected 22/22). Do not fabricate full-suite results if heavy deps missing.
4. Execute **§0 Next focus campaign item 4** (resume-trigger watch): run `python scripts/trackc_panel_admissibility_audit.py [--window-hint <candidate>]` on any new cached fragments; no default network probing. Items 1–3 complete (prereg frozen, dep-light 22/22, hardened gap/provenance audit). **Next:** §0 item 4 — build/run tested local gap-repair manifest (no network/outcomes); do not compute confirmatory outcomes. If trigger met with verified funding/provenance: freeze new prereg version before any outcome inspection, materialize splits/manifest, run confirmatory pipeline with block-bootstrap/Holm per protocol, record evidence.

5. Update **this file** with exact evidence and next unfinished task.

---

**END OF SINGLE DURABLE HANDOFF. FUTURE AGENTS: START AT §0 — HEAVY WORK REQUIRED: build/run tested local `trackc_gap_repair_manifest` (no network, no outcomes) for 2026_11/all_cache; `confirmatory_resume_ready=false`. (2026-11-09T20:11:56Z)**
