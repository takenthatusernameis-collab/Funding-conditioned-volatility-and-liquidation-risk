# AGENT_HANDOFF.md — Single Durable Handoff (next session MUST continue from here)

**Updated:** 2026-11-10T05:24:39Z — **P0 = Track C funding-conditioned volatility heavy engineering (no outcomes, no network, no Track A probing).** Repository name `Funding-conditioned-volatility-and-liquidation-risk` resolves priority in favor of **Track C P0**. Track A (liquidation risk) is **STRUCTURALLY BLOCKED / NO TRIGGER** — frozen unless a rubric-GO unauthenticated liquidation trigger appears (then PREREG before outcomes). Dep-light gate **48/48 OK** (core 39 + provenance lineage 9) re-confirmed 2026-11-10T05:24:39Z. `confirmatory_resume_ready=false`, `provenance_verified=false` for all audited windows. **Data/provenance gap cannot be fabricated.**

## 0) INITIAL TASK MESSAGE — 2026-11-10T05:24:39Z — MANDATORY HEAVY WORK (NEXT SESSION, UNAVOIDABLE)

**START HERE. P0 Track C. Track A frozen/blocked — do not touch.** No confirmatory trigger: scoped deep audits show `confirmatory_resume_ready=false` for `2024-10,2024-11,2024-12` (`symbols_ok=0/5`, `panel_blocks=0`, blockers: REQUIRED_SERIES_GAPS_OR_MISSING, MISSING_FUNDING_MONTH_FILE, PROVENANCE_NOT_MACHINE_VERIFIED, INSUFFICIENT_SYMBOLS/30D_BLOCKS_FOR_CONFIRMATORY, CONFIRMATORY_REQUIRES_FROZEN_PREREG_BEFORE_OUTCOMES, CONFIRMATORY_REQUIRES_VERIFIED_PROVENANCE_CHECKSUMS; `trackc_deep_audit_orchestrator_latest.json` SHA256 `90d228b9…`) and for `2026-11` (`symbols_ok=5/5`, `panel_blocks=0`, blockers: MISSING_FUNDING_MONTH_FILE, PROVENANCE_NOT_MACHINE_VERIFIED, INSUFFICIENT_30D_BLOCKS_FOR_CONFIRMATORY, CONFIRMATORY_REQUIRES_FROZEN_PREREG_BEFORE_OUTCOMES, CONFIRMATORY_REQUIRES_VERIFIED_PROVENANCE_CHECKSUMS; `trackc_deep_audit_orchestrator_2026_11.json`). `trackc_panel_window_plan_latest.json` (SHA256 `3c2bae46…`, 2026-11-10T02:40:56Z) fast signals: contiguous 2024-01..2026-11, blocks_fast=31 but `series_fast=false`, `funding_ok=false`, `confirmatory_resume_ready=false`. Prior audits/manifests/schema audits remain binding (missing 2026-11 funding month files for 5 symbols; series gaps 2024-10/11/12; provenance unverified). **No network. No outcomes. No invented data/provenance.**

**Single next unfinished task (measurable heavy engineering):** **G3 COMPLETE** — provenance-lineage ingestion integrated into Track C audits/orchestrator with tests (`scripts/trackc_panel_deep_audit_orchestrator.py`, `scripts/trackc_panel_admissibility_audit.py`, `tests/test_trackc_provenance_lineage.py`); scoped deep audits re-run for `2024-10,2024-11,2024-12` and `2026-11`. Result: `confirmatory_resume_ready=false`, `provenance_verified=false`; no blockers removed by verified lineage (manifest loaded, 0 adjacent `*.sha256` sidecars, files unmapped → no fabricated provenance). Structural blockers B2 (2026-11 funding month missing all 5 symbols) and B3 (2024-10/11/12 series gaps) remain unrepaired locally; no network permitted. Track C confirmatory campaign at **structural stop** — no further confirmatory work possible without admissible external data (network prohibited).

### Do in order

1. **Dep-light gate (record exact):**
   `python -m unittest tests.test_volatility_features_splits tests.test_synthetic_boundary_labels tests.test_trackc_panel_admissibility_audit tests.test_trackc_gap_repair_manifest tests.test_trackc_funding_schema_audit tests.test_trackc_panel_window_planner.TestPanelWindowPlanner.test_contiguous_sequences tests.test_trackc_panel_window_planner.TestPanelWindowPlanner.test_cli_smoke tests.test_trackc_panel_deep_audit_orchestrator tests.test_trackc_provenance_lineage -v` → expect **48/48 OK** (core 39 + provenance lineage 9).

2. **Confirm structural stop evidence (re-audit):**
   Re-run scoped deep audits (no network, no outcomes, `--window-hint` scoping only, no full-cache scan):
   - `python scripts/trackc_panel_deep_audit_orchestrator.py --cache research_state/data_cache --repo-root . --symbols BTCUSDT,ETHUSDT,BNBUSDT,SOLUSDT,XRPUSDT --window-hint 2024_10,2024_11,2024_12 --min-symbols 5 --min-blocks 3 --out research_state/trackc_deep_audit_orchestrator_latest.json`
   - `python scripts/trackc_panel_deep_audit_orchestrator.py --cache research_state/data_cache --repo-root . --symbols BTCUSDT,ETHUSDT,BNBUSDT,SOLUSDT,XRPUSDT --window-hint 2026_11 --min-symbols 5 --min-blocks 3 --out research_state/trackc_deep_audit_orchestrator_2026_11.json`
   Confirm both emit `confirmatory_resume_ready=false`, `provenance_verified=false`, `network_used=false`, `outcomes_computed=false`, and per-symbol `provenance_source=none`, `provenance_checked=0`, `provenance_ok=0`, `provenance_unmapped>0`; blockers contain `PROVENANCE_NOT_MACHINE_VERIFIED` plus structural `MISSING_FUNDING_MONTH_FILE` (2026-11) / `REQUIRED_SERIES_GAPS_OR_MISSING` (2024-10..12).

3. **If `confirmatory_resume_ready` becomes true from verified local prerequisites (not the case here; do not force):** freeze a **NEW** prereg version **before any outcome inspection** (derive/bump from `pre_registration_fclr014_confirmatory_funding_vol_20261109T181124Z.json`, SHA256 `4adf609e…`; record hashes), materialize panel + chronological splits with 7-day purge/embargo (>=3 non-overlapping 30-day OOS blocks, >=5 symbols) and run manifest, then run confirmatory pipeline only after prereg frozen (B0/B1/C1/C2, primary C2 vs B1 test QLIKE, block-bootstrap 2000 joint, Holm, calibration/concentration/leakage checks). No sealed-holdout reuse, no threshold shopping, no tuning on test.

4. **Not ready (current state):** machine-demonstrate remaining blockers per candidate with updated evidence JSONs/hashes (done via §0 item 2) and stop cleanly. Do not compute outcomes.

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
- **B4 (provenance): NOT machine-verifiable locally (G3 complete).** Adjacent `*.sha256` sidecars = 0 under `research_state/data_cache/`; `manifest_extended.json` (1835 records) + `manifest_extract.json` (3819 zip records) loaded but cache files unmapped (no unambiguous path+sha256 match) → `provenance_verified=false`, `provenance_source=none`, `provenance_unmapped>0`; no fabricated provenance. Blocker remains; local evidence insufficient to verify lineage.

### Completed heavy work (evidence)
1. **Track C reproducibility + audit hardening — COMPLETE.**
2. **Frozen prereg skeleton — COMPLETE (before outcomes).** `research_state/pre_registration_fclr014_confirmatory_funding_vol_20261109T181124Z.json` SHA256 `4adf609e…`.
3. **Dep-light admissibility audit hardening — COMPLETE.** `trackc_panel_admissibility_latest.json` (`b84f3bbe…`), `trackc_panel_admissibility_all_cache.json` (`7d74c0be…`), `confirmatory_resume_ready:false`.
4. **Gap/repair manifest — COMPLETE.** `trackc_gap_repair_manifest_2026_11.json` (`fa153f5b…`), `trackc_gap_repair_manifest_all_cache.json` (`13b4644b…`).
5. **Funding month-file schema/provenance checklist audit — COMPLETE.** `trackc_funding_schema_audit_2026_11.json` (`da36865d…`), `trackc_funding_schema_audit_2024Q1.json` (`253c16cd…`).
6. **Local-only panel-window planner/ranker — COMPLETE.** `scripts/trackc_panel_window_planner.py` (`895b7abc…`) + `tests/test_trackc_panel_window_planner.py` (`e4fe0502…`), artifact `research_state/trackc_panel_window_plan_latest.json` (`3c2bae46…`).
7. **Per-candidate deep-audit orchestrator — COMPLETE (G1/G2).** `scripts/trackc_panel_deep_audit_orchestrator.py` (`0499f41c…`) + `tests/test_trackc_panel_deep_audit_orchestrator.py` (`ae45a716…`, 8/8). Scoped audits: `trackc_deep_audit_orchestrator_latest.json` (`90d228b9…`, 2024-10..12) and `trackc_deep_audit_orchestrator_2026_11.json` (2026-11) — both `confirmatory_resume_ready=false`, `network_used=false`, `outcomes_computed=false`.
8. **Provenance-lineage ingestion (G3) — COMPLETE.** `scripts/trackc_provenance_lineage.py` (`7236 bytes`, deterministic stdlib-only, NO NETWORK/NO OUTCOMES) integrated into `scripts/trackc_panel_deep_audit_orchestrator.py` (`8500a773…`) and `scripts/trackc_panel_admissibility_audit.py` (`45e2982c…`); consumes `verify_paths_with_manifests()` and emits `provenance_verified`, `provenance_source` (adjacent_sidecar|manifest_record|none), `provenance_checked/ok/mismatch/unmapped` counts. Tests added: `tests/test_trackc_provenance_lineage.py` (`fca4453b…`, 9 tests). Scoped deep audits re-run: `trackc_deep_audit_orchestrator_latest.json` (`a28f952a…`, 2024-10..12) and `trackc_deep_audit_orchestrator_2026_11.json` (`40b4c3ae…`, 2026-11) — both `confirmatory_resume_ready=false`, `provenance_verified=false`, `network_used=false`, `outcomes_computed=false`. **No blockers removed by verified lineage** (0 adjacent sidecars; manifest loaded but files unmapped → no fabricated provenance). B2/B3 structural; B4 evaluated = not machine-verifiable from local evidence.
9. **Track C confirmatory campaign at structural stop.** `confirmatory_resume_ready=false`; no further confirmatory work possible without admissible external data (network prohibited). Prereg skeleton frozen (before outcomes): `pre_registration_fclr014_confirmatory_funding_vol_20261109T181124Z.json` SHA256 `4adf609e…`.

### Next focus campaign
**Campaign: Track C provenance-lineage ingestion (G3) + structural stop (local-only, no outcomes/network) — COMPLETE.** G3 executed per §0: `trackc_provenance_lineage.py` integrated into both Track C audits/orchestrator; `tests/test_trackc_provenance_lineage.py` added (9 tests); scoped deep audits re-run for `2024-10,2024-11,2024-12` and `2026-11`. `confirmatory_resume_ready=false`, `provenance_verified=false`; no blockers removed by verified lineage. **Exit reached: structural stop recorded with evidence.** No further Track C confirmatory work possible without admissible external data (network prohibited).
- **G1 (entry): GREEN** — dep-light 48/48, planner/orchestrator artifacts present, scoped execution.
- **G2 (orchestrator): COMPLETE** — scoped deep audits emitted for key windows.
- **G3 (provenance lineage): COMPLETE** — integrated + tested; provenance evaluated = not machine-verifiable locally; no fabricated provenance.
- **Exit:** confirmatory prereqs NOT met (structural B2/B3/B4) → structural stop recorded with evidence; stop cleanly, no outcomes.

## 1) VERIFIED (2026-11-10T04:15:00Z)

| Check | Result |
|---|---|
| Dep-light gate | `python -m unittest tests.test_volatility_features_splits tests.test_synthetic_boundary_labels tests.test_trackc_panel_admissibility_audit tests.test_trackc_gap_repair_manifest tests.test_trackc_funding_schema_audit tests.test_trackc_panel_window_planner.TestPanelWindowPlanner.test_contiguous_sequences tests.test_trackc_panel_window_planner.TestPanelWindowPlanner.test_cli_smoke tests.test_trackc_panel_deep_audit_orchestrator tests.test_trackc_provenance_lineage -v` → **Ran 48 tests — OK** (60.012s, re-confirmed 2026-11-10T05:24:39Z) |
| Planner artifact | `research_state/trackc_panel_window_plan_latest.json` SHA256 `3c2bae46…` (2026-11-10T02:40:56Z): 35 months 2024-01..2026-11, contiguous 2024-01..2026-11, blocks_fast=31, `series_fast=false`, `funding_ok=false`, `any_meets_local_data_signals_fast=false`, `confirmatory_resume_ready=false` |
| Deep audit 2024-10..12 | `research_state/trackc_deep_audit_orchestrator_latest.json` SHA256 `a28f952a…` (2026-11-10T05:21:41Z): `symbols_ok=0/5`, `panel_blocks_estimate=0`, `confirmatory_resume_ready=false`, `provenance_verified=false`, blockers: `REQUIRED_SERIES_GAPS_OR_MISSING`, `MISSING_FUNDING_MONTH_FILE`, `INSUFFICIENT_SYMBOLS_FOR_CONFIRMATORY`, `INSUFFICIENT_30D_BLOCKS_FOR_CONFIRMATORY`, `PROVENANCE_NOT_MACHINE_VERIFIED`, `CONFIRMATORY_REQUIRES_FROZEN_PREREG_BEFORE_OUTCOMES`, `CONFIRMATORY_REQUIRES_VERIFIED_PROVENANCE_CHECKSUMS` |
| Deep audit 2026-11 | `research_state/trackc_deep_audit_orchestrator_2026_11.json` SHA256 `40b4c3ae…` (2026-11-10T05:21:41Z): `symbols_ok=5/5`, `panel_blocks_estimate=0`, `confirmatory_resume_ready=false`, `provenance_verified=false`, blockers: `MISSING_FUNDING_MONTH_FILE`, `INSUFFICIENT_30D_BLOCKS_FOR_CONFIRMATORY`, `PROVENANCE_NOT_MACHINE_VERIFIED`, `CONFIRMATORY_REQUIRES_FROZEN_PREREG_BEFORE_OUTCOMES`, `CONFIRMATORY_REQUIRES_VERIFIED_PROVENANCE_CHECKSUMS`; missing 2026-11 funding month files for all 5 symbols |
| Local provenance sidecars | Adjacent `*.sha256` under `research_state/data_cache/`: **0**. Manifest metadata present: `manifest_extended.json` (1835 records, sha256/url/path), `manifest_extract.json` (3819 zip records, zip_sha256/dest/status), plus fclr002/fclr003/fclr011 manifests. `verify_paths_with_manifests` loads manifests; cache files unmapped → no unambiguous lineage match. |
| Provenance script | `scripts/trackc_provenance_lineage.py` — deterministic, stdlib-only, loads manifests, verifies content hashes. **Tests added (`tests/test_trackc_provenance_lineage.py`, 9 tests); integrated into `trackc_panel_deep_audit_orchestrator.py` + `trackc_panel_admissibility_audit.py`.** Emits `provenance_verified`, `provenance_source`, `provenance_checked/ok/mismatch/unmapped`. Result: not machine-verifiable locally; no fabricated provenance. |
| Binding prereg skeleton | `research_state/pre_registration_fclr014_confirmatory_funding_vol_20261109T181124Z.json` SHA256 `4adf609e…` (before outcomes) |

**Admissibility conclusion:** NO confirmatory trigger. `confirmatory_resume_ready=false`, `provenance_verified=false`. Do not compute outcomes. No network. No Track A probing. Track C confirmatory campaign at structural stop.

## 2) KEY ARTIFACTS (paths/hashes as recorded)
- `scripts/trackc_panel_window_planner.py` `895b7abc…`, `tests/test_trackc_panel_window_planner.py` `e4fe0502…`, `research_state/trackc_panel_window_plan_latest.json` `3c2bae46…`
- `scripts/trackc_panel_deep_audit_orchestrator.py` `8500a773…`, `tests/test_trackc_panel_deep_audit_orchestrator.py` `ae45a716…`
- `scripts/trackc_provenance_lineage.py` `7236 bytes`, integrated; `tests/test_trackc_provenance_lineage.py` `fca4453b…` (9 tests)
- `scripts/trackc_panel_admissibility_audit.py` `45e2982c…` (provenance counts fields added)
- `research_state/trackc_deep_audit_orchestrator_latest.json` `a28f952a…` (2024-10..12), `research_state/trackc_deep_audit_orchestrator_2026_11.json` `40b4c3ae…` (2026-11) — both `confirmatory_resume_ready=false`, `provenance_verified=false`
- `scripts/trackc_panel_admissibility_audit.py` (was `966ce2cf…`), `scripts/trackc_gap_repair_manifest.py` `51fd6b72…`, `scripts/trackc_funding_schema_audit.py` `78cbcd00…`
- Prior: `trackc_panel_admissibility_latest.json` `b84f3bbe…`, `trackc_panel_admissibility_all_cache.json` `7d74c0be…`, `trackc_gap_repair_manifest_2026_11.json` `fa153f5b…`, `trackc_gap_repair_manifest_all_cache.json` `13b4644b…`, `trackc_funding_schema_audit_2026_11.json` `da36865d…`, `trackc_funding_schema_audit_2024Q1.json` `253c16cd…`
- Binding prereg skeleton: `research_state/pre_registration_fclr014_confirmatory_funding_vol_20261109T181124Z.json` `4adf609e…` (before outcomes)

## 3) DO NOT DO
- ❌ Track A probing/scans/wrappers/report/status-file families
- ❌ Confirmatory/promotion claims from exploratory runs; threshold shopping; sealed holdout reuse
- ❌ New sealed outcomes without frozen preregistration
- ❌ Conflate observed liquidations with modeled/synthetic boundary breaches
- ❌ `.github/workflows` edits; schedulers/pollers/controllers
- ❌ Download/probe/network for missing Track C files; bypass access controls
- ❌ Fabricate provenance/outcomes. No full-cache planner scans (scope to candidate windows)
- ❌ Live/paper trading, order endpoints, credentials

## 4) SESSION START (mandatory)
1. Read this file + `RESEARCH_PROMPT.md`; `git status --short`.
2. Run dep-light gate (48/48) and record counts (§0 item 1).
3. Confirm structural stop evidence is current (§0 item 2): re-run both scoped deep audits; confirm `confirmatory_resume_ready=false`, `provenance_verified=false`, `network_used=false`, `outcomes_computed=false`; record any hash changes.
4. G3 is complete — do not re-integrate provenance. If a rubric-GO unauthenticated liquidation trigger appears, PREREG before outcomes (Track A); otherwise Track C remains at structural stop: no outcomes, no network, no Track A probing.
5. Update this file with exact evidence, hashes, commands, test counts, UTC timestamp, and next unfinished task only if state changes.

---
**END OF SINGLE DURABLE HANDOFF. START AT §0 — HEAVY WORK REQUIRED.** `confirmatory_resume_ready=false`, `provenance_verified=false`. Track C confirmatory campaign at structural stop (no further confirmatory work possible without admissible external data; network prohibited). **Updated: 2026-11-10T05:24:39Z**
