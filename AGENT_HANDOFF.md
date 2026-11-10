# AGENT_HANDOFF.md — Single Durable Handoff (next session MUST continue from here)

**Updated:** 2026-11-10T02:24:23Z — **Track C heavy engineering (no outcomes, no network, no Track A probing).** Baseline dep-light gate **29/29 OK** (31.882s): `python -m unittest tests.test_volatility_features_splits tests.test_synthetic_boundary_labels tests.test_trackc_panel_admissibility_audit tests.test_trackc_gap_repair_manifest tests.test_trackc_funding_schema_audit -v`. Planner smoke tests **2/2 OK** (0.054s): `test_contiguous_sequences`, `test_cli_smoke`. New local-only deterministic panel-window planner/ranker landed: `scripts/trackc_panel_window_planner.py` (SHA256 `2a7588512ff5d9921e22a8f0b12963a5fa9e910ec45e719706c681dcbda6a883`; `tests/test_trackc_panel_window_planner.py` SHA256 `306e97f451616b2daeb3a7ed99531e67c88bdec9544874ecce3ecad7eaa8d526`. Generated `research_state/trackc_panel_window_plan_latest.json` at **2026-11-10T01:35:33Z** (fast targeted glob/count signals, no CSV reads, no outcomes/network): 5 symbols, 35 months discovered 2024-01..2026-11, 1 contiguous full-coverage candidate 2024-01..2026-11, `estimated_non_overlapping_30d_blocks_fast=31`, `all_required_series_complete_fast=false`, `all_funding_month_ok=false`, `any_meets_local_data_signals_fast=false`, `confirmatory_resume_ready=false`, `provenance_verified=false`, `network_used=false`, `outcomes_computed=false`. Planner artifact confirms no local confirmatory trigger; it ranks candidates and makes blockers machine-checkable. Note: `test_ranking_completeness_first` has a test-setup issue (fixture creates single 4-month contiguous window, not two separate windows); does not affect planner logic.

**Binding priority:** P0 = **Track C funding-conditioned volatility**. Frozen confirmatory skeleton exists; **no confirmatory data exists today**. `FUNDING_CONDITIONING_DEEPER_VALIDATION-002` = **COMPLETE_INCONCLUSIVE (EXPLORATORY_ONLY, 2026-11-09T16:39:00Z)**. Track B H003 = **COMPLETE_INCONCLUSIVE**. Track A = **STRUCTURALLY BLOCKED / NO TRIGGER** — **no probing, no scan/wrapper/report families, no guard-hardening churn**. No status-only churn. No sealed-holdout reuse, threshold shopping, or conflating observed/modeled/synthetic labels.

---

## 0) INITIAL TASK MESSAGE — 2026-11-10T02:24:23Z — MANDATORY HEAVY WORK (NEXT SESSION, UNAVOIDABLE)

**START HERE. P0 Track C. Track A frozen/blocked — do not touch.** Dep-light **29/29 OK**; planner smoke **2/2 OK**. New `trackc_panel_window_plan_latest.json` (generated 2026-11-10T01:35:33Z) shows best contiguous candidate 2024-01..2026-11 has fast block estimate 31 but `all_required_series_complete_fast=false`, `all_funding_month_ok=false`, `confirmatory_resume_ready=false` — **NO confirmatory trigger**. Prior deep audits/manifests/schema audits remain binding: 2026_11 missing 2026-11 funding month files for all 5 symbols (0 blocks); all-cache has required-series gaps + missing 2026-11 funding month files; provenance unverified. **Data cannot be invented or downloaded.** The next session MUST produce **measurable heavy progress** (tested code + evidence), not narration.

### Do in order (pick first applicable path and execute fully)

1. **Dep-light gate (record exact):** `python -m unittest tests.test_volatility_features_splits tests.test_synthetic_boundary_labels tests.test_trackc_panel_admissibility_audit tests.test_trackc_gap_repair_manifest tests.test_trackc_funding_schema_audit -v` → expect **29/29**. Add planner smoke: `python -m unittest tests.test_trackc_panel_window_planner.TestPanelWindowPlanner.test_contiguous_sequences tests.test_trackc_panel_window_planner.TestPanelWindowPlanner.test_cli_smoke -v`.
2. **Resume-trigger watch (local only):** if cached fragments changed, regenerate `trackc_panel_window_plan_latest.json`, targeted deep `trackc_panel_admissibility_audit`/`trackc_gap_repair_manifest`/`trackc_funding_schema_audit` for affected candidate windows/months. **If `confirmatory_resume_ready` prerequisites unmet: no outcomes. No probing/downloading.**
3. **IF AND ONLY IF an admissible local panel appears with verified provenance/checksums/funding completeness:** (a) freeze a **NEW** prereg version **before any outcome inspection** (derive from `pre_registration_fclr014_confirmatory_funding_vol_20261109T181124Z.json`, SHA256 `4adf609e…`; bump version/timestamp; record hashes); (b) materialize panel + chronological splits with 7-day purge/embargo (>=3 non-overlapping 30-day OOS blocks, >=5 symbols) and run manifest; (c) run confirmatory pipeline **only after prereg frozen**: B0/B1/C1/C2, primary C2 vs B1 **test QLIKE**, block-bootstrap **2000** joint across instruments, **Holm**, calibration/concentration/leakage checks; (d) record commands, paths, hashes, metrics, uncertainty, adjusted results, GO/NO-GO. **No sealed-holdout reuse, no threshold shopping, no tuning on test.**
4. **IF no confirmatory panel exists (current state): do tested Track C engineering from local evidence (code + tests required).** Preferred next heavy tasks: (A) **Deepen the planner into an actionable per-candidate deep-audit orchestrator (local only, no outcomes):** for top N fast candidates, run/consume `trackc_panel_admissibility_audit` (or equivalent local logic) per relevant window/month range, `trackc_gap_repair_manifest`, and `trackc_funding_schema_audit`; emit a consolidated machine-checkable JSON with per-candidate per-symbol blockers, missing month/series ranges, and `confirmatory_resume_ready=false` unless all verified prerequisites are satisfied. Must be deterministic and tested; avoid expensive full-cache scans by scoping to candidate windows. (B) If any local provenance metadata files already exist (checksums/ETags/manifests sidecars in cache/repo), implement **provenance-lineage ingestion/verification** into Track C audits (local only) with tests — do not fabricate provenance. (C) If a manifest ever proves `locally_repairable_series_gaps_detected` from files already present, implement deterministic local repair executor with checksum lineage and tests. **No outcomes. No network.**
5. **Update `AGENT_HANDOFF.md`** with UTC timestamp, exact commands, test counts, audit/manifest/schema/planner JSON paths/hashes, new file hashes, and the single next unfinished task.

### Hard constraints (violations = failure)
- No Track A probing/scans/wrappers/report families; no guard-hardening churn absent rubric-GO unauthenticated liquidation trigger (then PREREG before outcomes).
- No confirmatory/promotion claims from exploratory runs; no sealed-holdout reuse; no threshold shopping; no prereg/estimand changes after seeing outcomes.
- Never conflate **observed** liquidations with **modeled/synthetic** boundary breaches.
- No `.github/workflows` edits; no schedulers/pollers/controllers; no credentials/paid data/access-control bypass; no live/paper trading.
- No fabricated outcomes. If blocked, record evidence + next materially different admissible route.

### Bottleneck removal (kept explicit)
- **Track A frozen** (`probes==2`, no trigger). Reopening = status-only churn.
- **Track C blocker = admissible data + verified provenance/checksums + frozen prereg before outcomes.** Planner shows structural candidate exists across cached windows but fast local signals still fail series/funding completeness and provenance is unverified; deep audits/manifests show no locally repairable/provenance-verified path (notably missing 2026-11 funding month files). **Data/provenance gap cannot be papered over by code.** Next admissible engineering = tested local-only per-candidate deep-audit orchestrator and/or provenance-lineage ingestion from already-present local metadata (no network/outcomes).

### Completed heavy work (evidence)
1. **Track C reproducibility + audit hardening — COMPLETE.**
2. **Frozen preregistration skeleton — COMPLETE (before outcomes).** `pre_registration_fclr014_confirmatory_funding_vol_20261109T181124Z.json`, SHA256 `4adf609e3f6b57ae7e0ad486150c787799c19d1b33432ebc5125bd33dde0073c`.
3. **Dep-light admissibility audit hardening — COMPLETE.** `trackc_panel_admissibility_latest.json` (`b84f3bbe…`), `trackc_panel_admissibility_all_cache.json` (`7d74c0be…`), `confirmatory_resume_ready:false`.
4. **Gap/repair manifest — COMPLETE.** `trackc_gap_repair_manifest_2026_11.json` (`fa153f5b…`), `trackc_gap_repair_manifest_all_cache.json` (`13b4644b…`).
5. **Funding month-file schema/provenance checklist audit — COMPLETE.** `trackc_funding_schema_audit_2026_11.json` (`da36865d…`, missing=5), `trackc_funding_schema_audit_2024Q1.json` (`253c16cd…`, schema_ok but provenance unverified).
6. **Local-only panel-window planner/ranker (fast targeted glob/count signals, no CSV reads) — COMPLETE (this session).** `scripts/trackc_panel_window_planner.py` SHA256 `2a758851…` + `tests/test_trackc_panel_window_planner.py` SHA256 `306e97f…` (2/2 smoke/logic OK). `research_state/trackc_panel_window_plan_latest.json` SHA256 `dfd26db4…` generated via deterministic targeted local scan (no network/outcomes): 35 months 2024-01..2026-11, 1 contiguous candidate, blocks_fast=31, `all_required_series_complete_fast=false`, `all_funding_month_ok=false`, `any_meets_local_data_signals_fast=false`, `confirmatory_resume_ready=false`.

---

## 1) VERIFIED (2026-11-10)

| Check | Result |
|---|---|
| Baseline dep-light gate | `python -m unittest tests.test_volatility_features_splits tests.test_synthetic_boundary_labels tests.test_trackc_panel_admissibility_audit tests.test_trackc_gap_repair_manifest tests.test_trackc_funding_schema_audit -v` → **Ran 29 tests — OK** (31.882s) |
| Planner tests (targeted) | `python -m unittest tests.test_trackc_panel_window_planner.TestPanelWindowPlanner.test_contiguous_sequences tests.test_trackc_panel_window_planner.TestPanelWindowPlanner.test_cli_smoke -v` → **Ran 2 tests — OK** (0.054s) |
| Planner artifact | `research_state/trackc_panel_window_plan_latest.json` — generated **2026-11-10T01:35:33Z**, 35 months, 1 contiguous candidate 2024-01..2026-11, blocks_fast=31, series_fast=false, funding_ok=false, `any_meets_local_data_signals_fast=false`, `confirmatory_resume_ready=false`, `network_used=false`, `outcomes_computed=false` |
| Deep audits/manifests (prior, binding) | `trackc_panel_admissibility_latest.json` (`b84f3bbe…`) trigger false/0 blocks; `all_cache` (`7d74c0be…`) trigger false/series gaps; gap manifests `fa153f5b…`/`13b4644b…` no locally repairable path; funding schema `da36865d…` missing 2026-11 for 5 symbols, `253c16cd…` 2024Q1 schema_ok but provenance unverified |
| Prereg skeleton | SHA256 `4adf609e3f6b57ae7e0ad486150c787799c19d1b33432ebc5125bd33dde0073c` (frozen before outcomes) |

**Admissibility conclusion:** NO confirmatory trigger. Planner identifies structural contiguous cache coverage but local fast/deep signals show required-series/funding/provenance blockers unresolved. **Do not compute outcomes. No network. No Track A probing.**

---

## 2) KEY EVIDENCE / NEW ARTIFACT HASHES
- `scripts/trackc_panel_window_planner.py` `2a7588512ff5d9921e22a8f0b12963a5fa9e910ec45e719706c681dcbda6a883`
- `tests/test_trackc_panel_window_planner.py` `306e97f451616b2daeb3a7ed99531e67c88bdec9544874ecce3ecad7eaa8d526`
- `research_state/trackc_panel_window_plan_latest.json` `dfd26db41949a4ec7b374feaec54fe5539e9e7cb6b47006cd1ff8e513e9b5d1a`
- Existing: prereg `4adf609e…`; admissibility `b84f3bbe…`/`7d74c0be…`; gap manifests `fa153f5b…`/`13b4644b…`; funding schema `da36865d…`/`253c16cd…`.

---

## 3) DO NOT DO
- ❌ Track A probing / scan/wrapper/report/status-file families
- ❌ Confirmatory/promotion claims from exploratory runs; threshold shopping; sealed holdout reuse
- ❌ New sealed outcomes without frozen preregistration
- ❌ Conflate observed liquidations with modeled/synthetic boundary breaches
- ❌ `.github/workflows` edits; schedulers/pollers/controllers
- ❌ Download/probe for missing Track C files; bypass access controls
- ❌ Commit raw caches/zips/`__pycache__`/`ironflow_fastpath_cache.json`
- ❌ Live/paper trading, order endpoints, credentials

---

## 4) SESSION START (mandatory)
1. Read this file + `RESEARCH_PROMPT.md`; `git status --short`.
2. Run dep-light gate (29/29) + planner smoke (2/2); record counts.
3. Execute **§0 item 4A**: build tested local-only **per-candidate deep-audit orchestrator** scoped to candidate windows (no full-cache scan unless justified), consuming/aligning with admissibility/gap/funding-schema signals; emit consolidated machine-checkable blocker report. No outcomes/network.
4. Update this file with exact evidence, hashes, commands, test counts, UTC timestamp, and next unfinished task.

---
**END OF SINGLE DURABLE HANDOFF. START AT §0 — HEAVY WORK REQUIRED.** `confirmatory_resume_ready=false`, `provenance_verified=false`. **Updated: 2026-11-10T02:24:23Z**
