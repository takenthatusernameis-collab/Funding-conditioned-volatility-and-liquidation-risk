# AGENT_HANDOFF.md — Single Durable Handoff (next session MUST continue from here)

**Updated:** 2026-11-10T03:33:55Z — **P0 = Track C funding-conditioned volatility heavy engineering (no outcomes, no network, no Track A probing).** Repository name `Funding-conditioned-volatility-and-liquidation-risk` resolves priority in favor of **Track C P0**. Track A (liquidation risk) is **STRUCTURALLY BLOCKED / NO TRIGGER** — frozen unless a rubric-GO unauthenticated liquidation trigger appears (then PREREG before outcomes). Dep-light gate **39/39 OK** (core 29 + planner smoke 2 + orchestrator 8, 53.542s). `confirmatory_resume_ready=false`, `provenance_verified=false` for all audited windows. **Data/provenance gap cannot be fabricated.**

## 0) INITIAL TASK MESSAGE — 2026-11-10T03:33:55Z — MANDATORY HEAVY WORK (NEXT SESSION, UNAVOIDABLE)

**START HERE. P0 Track C. Track A frozen/blocked — do not touch.** No confirmatory trigger: scoped deep audits show `confirmatory_resume_ready=false` for `2024-10,2024-11,2024-12` (`symbols_ok=0/5`, `panel_blocks=0`, blockers: REQUIRED_SERIES_GAPS_OR_MISSING, MISSING_FUNDING_MONTH_FILE, PROVENANCE_NOT_MACHINE_VERIFIED, INSUFFICIENT_SYMBOLS/30D_BLOCKS_FOR_CONFIRMATORY, CONFIRMATORY_REQUIRES_FROZEN_PREREG_BEFORE_OUTCOMES, CONFIRMATORY_REQUIRES_VERIFIED_PROVENANCE_CHECKSUMS; `trackc_deep_audit_orchestrator_latest.json` SHA256 `90d228b9…`) and for `2026-11` (`symbols_ok=5/5`, `panel_blocks=0`, blockers: MISSING_FUNDING_MONTH_FILE, PROVENANCE_NOT_MACHINE_VERIFIED, INSUFFICIENT_30D_BLOCKS_FOR_CONFIRMATORY, CONFIRMATORY_REQUIRES_FROZEN_PREREG_BEFORE_OUTCOMES, CONFIRMATORY_REQUIRES_VERIFIED_PROVENANCE_CHECKSUMS; `trackc_deep_audit_orchestrator_2026_11.json`). `trackc_panel_window_plan_latest.json` (SHA256 `3c2bae46…`, 2026-11-10T02:40:56Z) fast signals: contiguous 2024-01..2026-11, blocks_fast=31 but `series_fast=false`, `funding_ok=false`, `confirmatory_resume_ready=false`. Prior audits/manifests/schema audits remain binding (missing 2026-11 funding month files for 5 symbols; series gaps 2024-10/11/12; provenance unverified). **No network. No outcomes. No invented data/provenance.**

**Single next unfinished task (measurable heavy engineering):** implement **Gate G3 — provenance-lineage ingestion from local metadata sidecars** into Track C audits/orchestrator with tests, so machine-verified provenance can be established from already-present local evidence (or explicitly proven absent) without network/outcomes.

### Do in order

1. **Dep-light gate (record exact):**
   `python -m unittest tests.test_volatility_features_splits tests.test_synthetic_boundary_labels tests.test_trackc_panel_admissibility_audit tests.test_trackc_gap_repair_manifest tests.test_trackc_funding_schema_audit tests.test_trackc_panel_window_planner.TestPanelWindowPlanner.test_contiguous_sequences tests.test_trackc_panel_window_planner.TestPanelWindowPlanner.test_cli_smoke tests.test_trackc_panel_deep_audit_orchestrator -v` → expect **39/39 OK**.

2. **G3 — provenance-lineage ingestion (code + tests, local-only):**
   - Inventory local provenance/manifest sidecars: `research_state/data_cache/manifest_extended.json` (1835 records, has `path/url/sha256/size_bytes`, types incl funding_rate_monthly/klines/mark/index/premium; paths exist), `manifest_extract.json` (3819 zip records with `zip/zip_sha256/dest/members/status`), `manifest_fclr002.json`, `manifest_fclr003.json`, `fclr002_panel.json`, `fclr002_panel_local.json`, `fclr011_panel.json`, etc. **Observation (2026-11-10T03:33:55Z):** no adjacent `*.sha256` sidecar files found under `research_state/data_cache/` (glob count 0), so current adjacent-sidecar provenance checks correctly report unverified.
   - Extend Track C provenance verification to deterministically ingest applicable local manifest metadata (map cache-resident files ↔ manifest sha256/lineage; verify content hash where mapping is unambiguous) and emit machine-checkable fields: `provenance_verified`, `provenance_source` (adjacent_sidecar|manifest_record|none), `provenance_checked/ok/mismatch/unmapped` counts, blockers unchanged unless truly verified. Do **not** fabricate provenance, do **not** treat URL/manifest presence alone as verified without hash match, do **not** use network.
   - Add/extend tests (e.g. `tests/test_trackc_provenance_lineage.py` or extend existing Track C tests) covering: manifest-backed hash match -> verified signal; mismatch/unmapped -> not verified + blocker; deterministic/no-network/no-outcomes; compatibility with existing orchestrator/admissibility behavior.
   - Run scoped deep audits for `2024-10,2024-11,2024-12` and `2026-11` after changes and record whether any blockers are removed by verified lineage (expected: series/funding-month structural blockers may remain).

3. **If `confirmatory_resume_ready` becomes true from verified local prerequisites (unlikely):** freeze a **NEW** prereg version **before any outcome inspection** (derive/bump from `pre_registration_fclr014_confirmatory_funding_vol_20261109T181124Z.json`, SHA256 `4adf609e…`; record hashes), materialize panel + chronological splits with 7-day purge/embargo (>=3 non-overlapping 30-day OOS blocks, >=5 symbols) and run manifest, then run confirmatory pipeline only after prereg frozen (B0/B1/C1/C2, primary C2 vs B1 test QLIKE, block-bootstrap 2000 joint, Holm, calibration/concentration/leakage checks). No sealed-holdout reuse, no threshold shopping, no tuning on test.

4. **If not ready (expected):** machine-demonstrate remaining blockers per candidate with updated evidence JSONs/hashes and stop cleanly. Do not compute outcomes.

5. **Update `AGENT_HANDOFF.md`** with UTC timestamp, exact commands, test counts, changed file hashes, audit/planner/manifest JSON paths+hashes, and the single next unfinished task.

### Hard constraints
- No Track A probing/scans/wrappers/report families; no guard-hardening churn absent rubric-GO unauthenticated liquidation trigger (then PREREG before outcomes).
- No confirmatory/promotion claims from exploratory runs; no sealed-holdout reuse; no threshold shopping; no prereg/estimand changes after seeing outcomes.
- Never conflate **observed** liquidations with **modeled/synthetic** boundary breaches.
- No `.github/workflows` edits; no schedulers/pollers/controllers; no credentials/paid data/access-control bypass; no network/downloads; no live/paper trading.
- No fabricated outcomes/provenance. No full-cache planner scans (use `--window-hint` scoping).

### Bottleneck status
- **B1 (full-cache scan timeout >120s): REMOVED** — scoped orchestrator (`--window-hint`) in place and verified.
- **B2 (2026-11 funding month missing, all 5 symbols): STRUCTURAL local blocker** — not repairable without admissible external data (no network). Record evidence.
- **B3 (required-series gaps 2024-10/11/12): STRUCTURAL for those windows** unless deterministically repairable from already-present local files with checksum lineage (G3/provenance work may clarify; deep audit shows gaps remain).
- **B4 (provenance unverified): G3 TARGET** — adjacent `*.sha256` sidecars absent in `research_state/data_cache/`; local manifests with sha256/url exist (`manifest_extended.json`, `manifest_extract.json`, etc.) and are the admissible lineage-ingestion source to evaluate.

### Completed heavy work (evidence)
1. **Track C reproducibility + audit hardening — COMPLETE.**
2. **Frozen prereg skeleton — COMPLETE (before outcomes).** `research_state/pre_registration_fclr014_confirmatory_funding_vol_20261109T181124Z.json` SHA256 `4adf609e…`.
3. **Dep-light admissibility audit hardening — COMPLETE.** `trackc_panel_admissibility_latest.json` (`b84f3bbe…`), `trackc_panel_admissibility_all_cache.json` (`7d74c0be…`), `confirmatory_resume_ready:false`.
4. **Gap/repair manifest — COMPLETE.** `trackc_gap_repair_manifest_2026_11.json` (`fa153f5b…`), `trackc_gap_repair_manifest_all_cache.json` (`13b4644b…`).
5. **Funding month-file schema/provenance checklist audit — COMPLETE.** `trackc_funding_schema_audit_2026_11.json` (`da36865d…`), `trackc_funding_schema_audit_2024Q1.json` (`253c16cd…`).
6. **Local-only panel-window planner/ranker — COMPLETE.** `scripts/trackc_panel_window_planner.py` (`895b7abc…`) + `tests/test_trackc_panel_window_planner.py` (`e4fe0502…`), artifact `research_state/trackc_panel_window_plan_latest.json` (`3c2bae46…`).
7. **Per-candidate deep-audit orchestrator — COMPLETE (G1/G2).** `scripts/trackc_panel_deep_audit_orchestrator.py` (`0499f41c…`) + `tests/test_trackc_panel_deep_audit_orchestrator.py` (`ae45a716…`, 8/8). Scoped audits: `trackc_deep_audit_orchestrator_latest.json` (`90d228b9…`, 2024-10..12) and `trackc_deep_audit_orchestrator_2026_11.json` (2026-11) — both `confirmatory_resume_ready=false`, `network_used=false`, `outcomes_computed=false`.

### Next focus campaign
**Campaign: Track C provenance-lineage ingestion (G3) + blocker reclassification (local-only, no outcomes/network).** Execute §0 until verified provenance allows confirmatory resume from local prerequisites (then freeze NEW prereg before outcomes) OR until blockers are machine-demonstrated as structural/unrepairable locally with evidence.
- **G1 (entry): GREEN** — dep-light 39/39, planner/orchestrator artifacts present, scoped execution.
- **G2 (orchestrator): COMPLETE** — scoped deep audits emitted for key windows.
- **G3 (provenance lineage): NEXT** — ingest/verify from local manifest metadata with tests; no fabricated provenance.
- **Exit:** confirmatory prereqs met → prereg+outcomes path; else structural stop recorded with evidence.

## 1) VERIFIED (2026-11-10T03:33:55Z)

| Check | Result |
|---|---|
| Dep-light gate | `python -m unittest tests.test_volatility_features_splits tests.test_synthetic_boundary_labels tests.test_trackc_panel_admissibility_audit tests.test_trackc_gap_repair_manifest tests.test_trackc_funding_schema_audit tests.test_trackc_panel_window_planner.TestPanelWindowPlanner.test_contiguous_sequences tests.test_trackc_panel_window_planner.TestPanelWindowPlanner.test_cli_smoke tests.test_trackc_panel_deep_audit_orchestrator -v` → **Ran 39 tests — OK** (53.542s) |
| Planner artifact | `research_state/trackc_panel_window_plan_latest.json` SHA256 `3c2bae46…` (2026-11-10T02:40:56Z): 35 months 2024-01..2026-11, contiguous 2024-01..2026-11, blocks_fast=31, `series_fast=false`, `funding_ok=false`, `any_meets_local_data_signals_fast=false`, `confirmatory_resume_ready=false` |
| Deep audit 2024-10..12 | `research_state/trackc_deep_audit_orchestrator_latest.json` SHA256 `90d228b9…` (2026-11-10T03:15:27Z): `symbols_ok=0/5`, `panel_blocks_estimate=0`, `confirmatory_resume_ready=false`, `provenance_verified=false` |
| Deep audit 2026-11 | `research_state/trackc_deep_audit_orchestrator_2026_11.json` (2026-11-10T03:27:11Z): `symbols_ok=5/5`, `panel_blocks_estimate=0`, `confirmatory_resume_ready=false`, `provenance_verified=false`, missing 2026-11 funding month files for all 5 symbols |
| Local provenance sidecars | Adjacent `*.sha256` under `research_state/data_cache/`: **0**. Manifest metadata present: `manifest_extended.json` (1835 records, sha256/url/path), `manifest_extract.json` (3819 zip records, zip_sha256/dest/status), plus fclr002/fclr003/fclr011 manifests |
| Binding prereg skeleton | `research_state/pre_registration_fclr014_confirmatory_funding_vol_20261109T181124Z.json` SHA256 `4adf609e…` (before outcomes) |

**Admissibility conclusion:** NO confirmatory trigger. `confirmatory_resume_ready=false`, `provenance_verified=false`. Do not compute outcomes. No network. No Track A probing.

## 2) KEY ARTIFACTS (paths/hashes as recorded)
- `scripts/trackc_panel_window_planner.py` `895b7abc…`, `tests/test_trackc_panel_window_planner.py` `e4fe0502…`, `research_state/trackc_panel_window_plan_latest.json` `3c2bae46…`
- `scripts/trackc_panel_deep_audit_orchestrator.py` `0499f41c…`, `tests/test_trackc_panel_deep_audit_orchestrator.py` `ae45a716…`
- `research_state/trackc_deep_audit_orchestrator_latest.json` `90d228b9…`, `research_state/trackc_deep_audit_orchestrator_2026_11.json`
- `scripts/trackc_panel_admissibility_audit.py` `966ce2cf…`, `scripts/trackc_gap_repair_manifest.py` `51fd6b72…`, `scripts/trackc_funding_schema_audit.py` `78cbcd00…`
- Prior: `trackc_panel_admissibility_latest.json` `b84f3bbe…`, `trackc_panel_admissibility_all_cache.json` `7d74c0be…`, `trackc_gap_repair_manifest_2026_11.json` `fa153f5b…`, `trackc_gap_repair_manifest_all_cache.json` `13b4644b…`, `trackc_funding_schema_audit_2026_11.json` `da36865d…`, `trackc_funding_schema_audit_2024Q1.json` `253c16cd…`

## 3) DO NOT DO
- ❌ Track A probing/scans/wrappers/report/status-file families
- ❌ Confirmatory/promotion claims from exploratory runs; threshold shopping; sealed holdout reuse
- ❌ New sealed outcomes without frozen preregistration
- ❌ Conflate observed liquidations with modeled/synthetic boundary breaches
- ❌ `.github/workflows` edits; schedulers/pollers/controllers
- ❌ Download/probe/network for missing Track C files; bypass access controls
- ❌ Fabricate provenance/outcomes; commit raw caches/zips/`__pycache__`/`ironflow_fastpath_cache.json`
- ❌ Live/paper trading, order endpoints, credentials
- ❌ Full-cache planner scans (scope to candidate windows)

## 4) SESSION START (mandatory)
1. Read this file + `RESEARCH_PROMPT.md`; `git status --short`.
2. Run dep-light gate (39/39) and record counts.
3. Execute **§0 G3** (provenance-lineage ingestion + tests + re-audit), then §0 item 3/4 as applicable.
4. Update this file with exact evidence, hashes, commands, test counts, UTC timestamp, and next unfinished task.

---
**END OF SINGLE DURABLE HANDOFF. START AT §0 — HEAVY WORK REQUIRED.** `confirmatory_resume_ready=false`, `provenance_verified=false`. **Updated: 2026-11-10T03:33:55Z**
