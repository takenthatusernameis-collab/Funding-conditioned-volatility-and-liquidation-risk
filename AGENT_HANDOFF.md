# AGENT_HANDOFF.md — Single Durable Handoff (next session MUST continue from here)

**Updated:** 2026-11-10T03:15:27Z — **P0 = Track C funding-conditioned volatility heavy engineering (no outcomes, no network, no Track A probing).** Repository name `Funding-conditioned-volatility-and-liquidation-risk` resolves the Track A vs Track C conflict in favor of **Track C P0**. Track A (liquidation risk) is STRUCTURALLY BLOCKED / NO TRIGGER — frozen unless a rubric-GO unauthenticated liquidation trigger appears (then PREREG before outcomes). Dep-light gate **29/29 OK** + planner smoke **2/2 OK** + new scoped deep-audit orchestrator **8/8 OK**. New local-only deterministic per-candidate deep-audit orchestrator: `scripts/trackc_panel_deep_audit_orchestrator.py` (SHA256 `0499f41c0d0ee77cb2ca827b3aa21c08090417fc04d9310cc9d1a17d93303b8f`) + `tests/test_trackc_panel_deep_audit_orchestrator.py` (SHA256 `ae45a716f6c99f9a490ef9d10d2324038d6c70b4359175c236b99d27623bf2df`) — addresses bottleneck B1 by scoping to candidate windows (`--window-hint`), no full-cache scan, no network, no outcomes. Scoped real-cache deep audit on the B3 gap window `2024-10,2024-11,2024-12` emitted to `research_state/trackc_deep_audit_orchestrator_latest.json` (SHA256 `90d228b9b9b73fcee22ec687c7d0da23b4f9686673782f7f1b78dbcc5e55dfb1`): `confirmatory_resume_ready=false`, `symbols_ok=0/5`, `panel_blocks_estimate=0`, blockers = REQUIRED_SERIES_GAPS_OR_MISSING, MISSING_FUNDING_MONTH_FILE, PROVENANCE_NOT_MACHINE_VERIFIED, INSUFFICIENT_SYMBOLS/30D_BLOCKS_FOR_CONFIRMATORY, CONFIRMATORY_REQUIRES_FROZEN_PREREG_BEFORE_OUTCOMES, CONFIRMATORY_REQUIRES_VERIFIED_PROVENANCE_CHECKSUMS; `network_used=false`, `outcomes_computed=false`.

## BLOCKER / BOTTLENECK REMOVAL (executed this session)

- **Bottleneck B1 — full-cache planner scan is slow/non-deterministic:** `python scripts/trackc_panel_window_planner.py` (default cache `research_state/data_cache`, 202 symbol-month dirs) **timed out at 120s** (full recursive globs for funding month files across the whole tree). Fix: next session MUST scope the planner/orchestrator to candidate windows only (`--window-hint` per candidate month range), no full-cache scan unless justified. Do not retry full-cache scans as progress.
- **Bottleneck B2 — missing 2026-11 funding month files for all 5 symbols:** `MISSING_FUNDING_MONTH_FILE` for BTC/ETH/BNB/SOL/XRP in 2026-11 (0 blocks). **Data cannot be invented or downloaded.** Record as structural blocker; no local workaround from present files. Next admissible route = per-candidate deep audit to confirm no locally repairable path, then stop cleanly with evidence.
- **Bottleneck B3 — required-series gaps in 2024-10, 2024-11, 2024-12:** `REQUIRED_SERIES_GAPS_OR_MISSING` for symbol-months (2024-10 BNB/SOL/XRP; 2024-11 BNB/ETH/SOL/XRP; 2024-12 all 5). Breaks `all_required_series_complete_fast` for the 2024-01..2026-11 candidate. Deep audit per candidate window must confirm whether gaps are locally repairable from files already present (checksum lineage) or structural.
- **Bottleneck B4 — provenance unverified everywhere:** `PROVENANCE_NOT_MACHINE_VERIFIED` + `SCHEMA_NOT_VERIFIED_IN_FAST_MODE` on every symbol-month. Existing local manifest sidecars present in `research_state/data_cache/` (`manifest_extended.json`, `fclr011_panel.json`, `fclr002_panel_local.json`, `manifest_extract.json`, `manifest_fclr002.json`, `manifest_fclr003.json`, `fclr002_panel.json`) are candidate provenance sources — ingest/verify only, do not fabricate.

**Binding priority (resolves Track A vs Track C conflict):** P0 = **Track C funding-conditioned volatility**. `FUNDING_CONDITIONING_DEEPER_VALIDATION-002` = **COMPLETE_INCONCLUSIVE (EXPLORATORY_ONLY, 2026-11-09T16:39:00Z)**. Track B H003 = **COMPLETE_INCONCLUSIVE**. Track A = **STRUCTURALLY BLOCKED / NO TRIGGER** — **no probing, no scan/wrapper/report families, no guard-hardening churn**. `experiment_frontier.json` line "Repo-name priority: liquidation risk (Track A) only active; Track C sealed/locked" is **STALE / SUPERSEDED** by this file (root durable handoff, declared authoritative in `research_state/FCLR_CAMPAIGN_NEXT.md`). FCLR-NEXT-132/139 ambiguity resolved: Track C is P0 heavy work; FCLR-NEXT-139 retained only as a blocked Track-A campaign marker, no new Track A work absent trigger. No status-only churn. No sealed-holdout reuse, threshold shopping, or conflating observed/modeled/synthetic labels.

---

## 0) INITIAL TASK MESSAGE — 2026-11-10T03:15:27Z — MANDATORY HEAVY WORK (NEXT SESSION, UNAVOIDABLE)

**START HERE. P0 Track C. Track A frozen/blocked — do not touch.** Dep-light **29/29 OK**; planner smoke **2/2 OK**; scoped deep-audit orchestrator **8/8 OK**. `trackc_panel_window_plan_latest.json` (generated 2026-11-10T02:40:56Z) shows best contiguous candidate 2024-01..2026-11 fast block estimate 31 but `all_required_series_complete_fast=false`, `all_funding_month_ok=false`, `confirmatory_resume_ready=false` — **NO confirmatory trigger**. Scoped real-cache deep audit on the B3 gap window `2024-10,2024-11,2024-12` (`trackc_deep_audit_orchestrator_latest.json`) confirms `confirmatory_resume_ready=false`, `symbols_ok=0/5`, `panel_blocks=0`, required-series + funding + provenance blockers unresolved. Prior deep audits/manifests/schema audits remain binding: 2026-11 missing funding month files for all 5 symbols (0 blocks); required-series gaps 2024-10/11/12; provenance unverified. **Data cannot be invented or downloaded.** Bottleneck B1 (full-cache planner scan timeout >120s) is removed: the orchestrator is scoped to candidate windows via `--window-hint` and ran the real-cache audit in well under the cap.

The next session MUST produce **measurable heavy progress** (tested code + evidence), not narration. **Single next unfinished task:** execute the Track C per-candidate deep-audit orchestrator campaign (G2/G3) — run `trackc_panel_deep_audit_orchestrator.py` scoped to each remaining candidate window (notably `2026_11` for the missing funding months, plus any other fast candidates), implement provenance-lineage ingestion from local metadata sidecars (B4) with tests if sidecars exist, and either reach `confirmatory_resume_ready=true` (then freeze a NEW prereg before outcomes) or machine-demonstrate no locally repairable/provenance-verified path exists and record evidence + stop cleanly. **No outcomes. No network. No Track A probing.**

### Do in order (pick first applicable path and execute fully)

1. **Dep-light gate (record exact):** `python -m unittest tests.test_volatility_features_splits tests.test_synthetic_boundary_labels tests.test_trackc_panel_admissibility_audit tests.test_trackc_gap_repair_manifest tests.test_trackc_funding_schema_audit -v` → expect **29/29**. Add planner smoke: `python -m unittest tests.test_trackc_panel_window_planner.TestPanelWindowPlanner.test_contiguous_sequences tests.test_trackc_panel_window_planner.TestPanelWindowPlanner.test_cli_smoke -v` → expect **2/2**. Add orchestrator: `python -m unittest tests.test_trackc_panel_deep_audit_orchestrator -v` → expect **8/8**.

2. **Resume-trigger watch / scoped deep-audit execution (local only, no full-cache scan):** run `python scripts/trackc_panel_deep_audit_orchestrator.py --cache research_state/data_cache --repo-root . --symbols BTCUSDT,ETHUSDT,BNBUSDT,SOLUSDT,XRPUSDT --window-hint <candidate months> --min-symbols 5 --min-blocks 3 --out research_state/trackc_deep_audit_orchestrator_<window>.json` scoped to each candidate window (notably `2026_11` for missing funding months; `2024_10,2024_11,2024_12` already done → `confirmatory_resume_ready=false`, `symbols_ok=0/5`). Do NOT full-cache scan unless justified. Regenerate `trackc_panel_window_plan_latest.json` scoped to candidate windows if cached fragments changed. **If `confirmatory_resume_ready` prerequisites unmet: no outcomes. No probing/downloading.**

3. **IF AND ONLY IF an admissible local panel appears with verified provenance/checksums/funding completeness:** (a) freeze a **NEW** prereg version **before any outcome inspection** (derive from `pre_registration_fclr014_confirmatory_funding_vol_20261109T181124Z.json`, SHA256 `4adf609e3f6b57ae7e0ad486150c787799c19d1b33432ebc5125bd33dde0073c`; bump version/timestamp; record hashes); (b) materialize panel + chronological splits with 7-day purge/embargo (>=3 non-overlapping 30-day OOS blocks, >=5 symbols) and run manifest; (c) run confirmatory pipeline **only after prereg frozen**: B0/B1/C1/C2, primary C2 vs B1 **test QLIKE**, block-bootstrap **2000** joint across instruments, **Holm**, calibration/concentration/leakage checks; (d) record commands, paths, hashes, metrics, uncertainty, adjusted results, GO/NO-GO. **No sealed-holdout reuse, no threshold shopping, no tuning on test.**

4. **IF no confirmatory panel exists (current state): execute tested Track C engineering from local evidence (code + tests required).** (A) **Per-candidate deep-audit orchestrator — COMPLETE:** `scripts/trackc_panel_deep_audit_orchestrator.py` + `tests/test_trackc_panel_deep_audit_orchestrator.py` (8/8); run it scoped to each candidate window via `--window-hint`, emit consolidated machine-checkable blocker JSON, `confirmatory_resume_ready=false` unless all verified prereqs satisfied; avoids full-cache scan (bottleneck B1 removed). (B) **Provenance-lineage ingestion (G3, next):** if local metadata sidecars exist (checksums/ETags/manifests in cache/repo — see B4 list), ingest/verify provenance into Track C audits (local only) with tests — do not fabricate provenance. (C) If a manifest ever proves `locally_repairable_series_gaps_detected` from files already present, implement deterministic local repair executor with checksum lineage and tests. **No outcomes. No network.**

5. **Update `AGENT_HANDOFF.md`** with UTC timestamp, exact commands, test counts, audit/manifest/schema/planner JSON paths/hashes, new file hashes, and the single next unfinished task.

### Hard constraints (violations = failure)
- No Track A probing/scans/wrappers/report families; no guard-hardening churn absent rubric-GO unauthenticated liquidation trigger (then PREREG before outcomes).
- No confirmatory/promotion claims from exploratory runs; no sealed-holdout reuse; no threshold shopping; no prereg/estimand changes after seeing outcomes.
- Never conflate **observed** liquidations with **modeled/synthetic** boundary breaches.
- No `.github/workflows` edits; no schedulers/pollers/controllers; no credentials/paid data/access-control bypass; no live/paper trading.
- No fabricated outcomes. If blocked, record evidence + next materially different admissible route.

### Bottleneck removal (kept explicit)
- **Track A frozen** (`probes==2`, no trigger). Reopening = status-only churn. Priority conflict with `experiment_frontier.json` resolved in favor of this file (Track C P0, Track A frozen); `experiment_frontier.json` stale priority line superseded; FCLR-NEXT-132/139 ambiguity closed.
- **Track C blocker = admissible data + verified provenance/checksums + frozen prereg before outcomes.** Planner shows structural candidate exists across cached windows but fast local signals still fail series/funding completeness and provenance is unverified; deep audits/manifests show no locally repairable/provenance-verified path (notably missing 2026-11 funding month files; series gaps 2024-10/11/12). **Bottleneck B1 removed:** full-cache planner scan previously timed out >120s; replaced by the scoped deep-audit orchestrator (`--window-hint` per candidate window), which ran the real-cache B3 gap-window audit well under the cap. **Data/provenance gap cannot be papered over by code.** Remaining admissible engineering = provenance-lineage ingestion from already-present local metadata sidecars (G3) with tests, then either confirmatory resume or a recorded structural stop (no network/outcomes).

### Completed heavy work (evidence)
1. **Track C reproducibility + audit hardening — COMPLETE.**
2. **Frozen preregistration skeleton — COMPLETE (before outcomes).** `pre_registration_fclr014_confirmatory_funding_vol_20261109T181124Z.json`, SHA256 `4adf609e3f6b57ae7e0ad486150c787799c19d1b33432ebc5125bd33dde0073c`.
3. **Dep-light admissibility audit hardening — COMPLETE.** `trackc_panel_admissibility_latest.json` (`b84f3bbe2cb1568e98176f237eed99199916f9190cde6dea0ee6b23129d72c03`), `trackc_panel_admissibility_all_cache.json` (`7d74c0be…`), `confirmatory_resume_ready:false`.
4. **Gap/repair manifest — COMPLETE.** `trackc_gap_repair_manifest_2026_11.json` (`fa153f5b6f38e94c0243f28125a88417cbd8c60c18ca96a966067ffddf544605`), `trackc_gap_repair_manifest_all_cache.json` (`13b4644b…`).
5. **Funding month-file schema/provenance checklist audit — COMPLETE.** `trackc_funding_schema_audit_2026_11.json` (`da36865dacea7004fb132940ba86d56cae8f89e80ab7b2d15dffb20a3eeb4218`, missing=5), `trackc_funding_schema_audit_2024Q1.json` (`253c16cd…`, schema_ok but provenance unverified).
6. **Local-only panel-window planner/ranker (fast targeted glob/count signals, no CSV reads) — COMPLETE.** `scripts/trackc_panel_window_planner.py` SHA256 `895b7abc3574730cff53f8a739bed507f6417506a44d13d53079618864eadbef` + `tests/test_trackc_panel_window_planner.py` SHA256 `e4fe0502ca1a4fe66ee9b9976bd02194a252ed3ef276fc096204cecfeba7b0bc` (2/2 smoke/logic OK). `research_state/trackc_panel_window_plan_latest.json` SHA256 `3c2bae467d33678e298a0b77f8630cc6c9123c248885438e5a9ce6a34821b65d` generated via deterministic targeted local scan (no network/outcomes): 35 months 2024-01..2026-11, 1 contiguous candidate, blocks_fast=31, series_fast=false, funding_ok=false, `any_meets_local_data_signals_fast=false`, `confirmatory_resume_ready=false`. **Bottleneck B1 removed:** full-cache invocation previously timed out >120s; the scoped deep-audit orchestrator (item 7) replaces full-cache scans with `--window-hint`-scoped candidate windows.
7. **Per-candidate deep-audit orchestrator — COMPLETE.** `scripts/trackc_panel_deep_audit_orchestrator.py` SHA256 `0499f41c0d0ee77cb2ca827b3aa21c08090417fc04d9310cc9d1a17d93303b8f` + `tests/test_trackc_panel_deep_audit_orchestrator.py` SHA256 `ae45a716f6c99f9a490ef9d10d2324038d6c70b4359175c236b99d27623bf2df` (8/8 OK). Scoped real-cache deep audit on B3 gap window `2024-10,2024-11,2024-12` → `research_state/trackc_deep_audit_orchestrator_latest.json` SHA256 `90d228b9b9b73fcee22ec687c7d0da23b4f9686673782f7f1b78dbcc5e55dfb1`: `confirmatory_resume_ready=false`, `symbols_ok=0/5`, `panel_blocks_estimate=0`, `network_used=false`, `outcomes_computed=false`.

### Next focus campaign (future agents cannot avoid heavy work)
**Campaign: Track C per-candidate deep-audit orchestrator (local-only, no outcomes/network).** Execute §0 item 4 until `confirmatory_resume_ready` becomes true from verified local prerequisites, OR until it is machine-demonstrated that no locally repairable/provenance-verified path exists (then record evidence and stop cleanly; do not fabricate).
- **Gate G1 (entry):** dep-light 29/29 + planner smoke 2/2 + orchestrator 8/8 green; `trackc_panel_window_plan_latest.json` machine-readable; full-cache scan bottleneck (B1) scoped to candidate windows. **G1 GREEN.**
- **Gate G2 (orchestrator):** deterministic script + tests consuming admissibility/gap/funding-schema signals scoped to candidate windows; emits consolidated blocker JSON with per-candidate per-symbol blockers + missing month/series ranges; `confirmatory_resume_ready=false` unless all verified prereqs satisfied; no network; no outcomes. **G2 COMPLETE** (`trackc_panel_deep_audit_orchestrator.py` + tests 8/8; scoped real-cache audit on `2024-10,2024-11,2024-12` emitted with blockers).
- **Gate G3 (provenance lineage):** if local metadata sidecars exist (B4 list), ingest/verify provenance into Track C audits with tests; no fabricated provenance. **G3 IN PROGRESS (next).**
- **Exit:** either confirmatory prerequisites met (freeze NEW prereg → outcomes) or structural blocker recorded with evidence; then update this file.

---

## 1) VERIFIED (2026-11-10)

| Check | Result |
|---|---|
| Baseline dep-light gate | `python -m unittest tests.test_volatility_features_splits tests.test_synthetic_boundary_labels tests.test_trackc_panel_admissibility_audit tests.test_trackc_gap_repair_manifest tests.test_trackc_funding_schema_audit -v` → **Ran 29 tests — OK** (31.645s) |
| Planner tests (targeted) | `python -m unittest tests.test_trackc_panel_window_planner.TestPanelWindowPlanner.test_contiguous_sequences tests.test_trackc_panel_window_planner.TestPanelWindowPlanner.test_cli_smoke -v` → **Ran 2 tests — OK** (0.050s) |
| Orchestrator tests | `python -m unittest tests.test_trackc_panel_deep_audit_orchestrator -v` → **Ran 8 tests — OK** (~22s) |
| Planner artifact | `research_state/trackc_panel_window_plan_latest.json` — generated **2026-11-10T02:40:56Z**, 35 months, 1 contiguous candidate 2024-01..2026-11, blocks_fast=31, series_fast=false, funding_ok=false, `any_meets_local_data_signals_fast=false`, `confirmatory_resume_ready=false`, `network_used=false`, `outcomes_computed=false` |
| Scoped deep-audit (real cache, B3 gap window) | `research_state/trackc_deep_audit_orchestrator_latest.json` — generated **2026-11-10T03:15:27Z**, candidate `2024-10,2024-11,2024-12` contiguous, `symbols_ok=0/5`, `panel_blocks_estimate=0`, `confirmatory_resume_ready=false`, `provenance_verified=false`, `network_used=false`, `outcomes_computed=false`; blockers = REQUIRED_SERIES_GAPS_OR_MISSING, MISSING_FUNDING_MONTH_FILE, PROVENANCE_NOT_MACHINE_VERIFIED, INSUFFICIENT_SYMBOLS/30D_BLOCKS_FOR_CONFIRMATORY, CONFIRMATORY_REQUIRES_FROZEN_PREREG_BEFORE_OUTCOMES, CONFIRMATORY_REQUIRES_VERIFIED_PROVENANCE_CHECKSUMS |
| Deep audits/manifests (prior, binding) | `trackc_panel_admissibility_latest.json` (`b84f3bbe…`) trigger false/0 blocks; `all_cache` (`7d74c0be…`) trigger false/series gaps; gap manifests `fa153f5b…`/`13b4644b…` no locally repairable path; funding schema `da36865d…` missing 2026-11 for 5 symbols, `253c16cd…` 2024Q1 schema_ok but provenance unverified |
| Prereg skeleton | SHA256 `4adf609e…` (frozen before outcomes) |

**Admissibility conclusion:** NO confirmatory trigger. Planner identifies structural contiguous cache coverage but local fast/deep signals show required-series/funding/provenance blockers unresolved. **Do not compute outcomes. No network. No Track A probing.**

---

## 2) KEY EVIDENCE / NEW ARTIFACT HASHES
- `scripts/trackc_panel_window_planner.py` `895b7abc3574730cff53f8a739bed507f6417506a44d13d53079618864eadbef`
- `tests/test_trackc_panel_window_planner.py` `e4fe0502ca1a4fe66ee9b9976bd02194a252ed3ef276fc096204cecfeba7b0bc`
- `research_state/trackc_panel_window_plan_latest.json` `3c2bae467d33678e298a0b77f8630cc6c9123c248885438e5a9ce6a34821b65d` (generated 2026-11-10T02:40:56Z)
- `scripts/trackc_panel_deep_audit_orchestrator.py` `0499f41c0d0ee77cb2ca827b3aa21c08090417fc04d9310cc9d1a17d93303b8f`
- `tests/test_trackc_panel_deep_audit_orchestrator.py` `ae45a716f6c99f9a490ef9d10d2324038d6c70b4359175c236b99d27623bf2df`
- `research_state/trackc_deep_audit_orchestrator_latest.json` `90d228b9b9b73fcee22ec687c7d0da23b4f9686673782f7f1b78dbcc5e55dfb1` (generated 2026-11-10T03:15:27Z)
- `scripts/trackc_panel_admissibility_audit.py` `966ce2cfe72484646ff8c5a078bd8c8ab68755827f78e3d68aa87947ac09f8ff`
- `scripts/trackc_gap_repair_manifest.py` `51fd6b72e584749efa17d9b74203d807654bc19ea0a2ed4414ca21c53d316ee8`
- `scripts/trackc_funding_schema_audit.py` `78cbcd00e9620ea153e8399670c25d7c1b2aead5567e9b94f4daa8e321365667`
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
- ❌ Full-cache planner scans that time out (bottleneck B1 — scope to candidate windows)

---

## 4) SESSION START (mandatory)
1. Read this file + `RESEARCH_PROMPT.md`; `git status --short`.
2. Run dep-light gate (29/29) + planner smoke (2/2) + orchestrator (8/8); record counts: `python -m unittest tests.test_volatility_features_splits tests.test_synthetic_boundary_labels tests.test_trackc_panel_admissibility_audit tests.test_trackc_gap_repair_manifest tests.test_trackc_funding_schema_audit tests.test_trackc_panel_window_planner.TestPanelWindowPlanner.test_contiguous_sequences tests.test_trackc_panel_window_planner.TestPanelWindowPlanner.test_cli_smoke tests.test_trackc_panel_deep_audit_orchestrator -v`.
3. Execute **§0 item 4**: run the scoped deep-audit orchestrator (`trackc_panel_deep_audit_orchestrator.py --window-hint <candidate months>`) over each remaining candidate window (notably `2026_11` for missing funding months), implement provenance-lineage ingestion from local metadata sidecars (G3) with tests if sidecars exist, and either reach `confirmatory_resume_ready=true` (then freeze a NEW prereg before outcomes) or record a structural stop with evidence. No outcomes/network.
4. Update this file with exact evidence, hashes, commands, test counts, UTC timestamp, and next unfinished task.

---
**END OF SINGLE DURABLE HANDOFF. START AT §0 — HEAVY WORK REQUIRED.** `confirmatory_resume_ready=false`, `provenance_verified=false`. **Updated: 2026-11-10T03:15:27Z**
