# AGENT_HANDOFF.md — Single Durable Handoff (next session MUST continue from here)

**Updated:** 2026-11-10T01:09:13Z — **Track C heavy engineering (no outcomes, no network, no Track A probing).** Dep-light gate **28/28 OK** (31.504s): `python -m unittest tests.test_volatility_features_splits tests.test_synthetic_boundary_labels tests.test_trackc_panel_admissibility_audit tests.test_trackc_gap_repair_manifest tests.test_trackc_funding_schema_audit -v`. Added local-only funding month-file schema/provenance checklist audit `scripts/trackc_funding_schema_audit.py` (SHA256 `78cbcd00e9620ea153e8399670c25d7c1b2aead5567e9b94f4daa8e321365667`) + `tests/test_trackc_funding_schema_audit.py` (`062430e62f105c28ab20c0ae2cc990d87b65fb8ac5596c84b70a5ba4cbe3c0bd`): stdlib-only, machine-checkable blocker register for required symbols/months (schema/time/rate sanity, adjacent sidecar presence, SHA256), emits `confirmatory_resume_ready:false, provenance_verified:false, network_used:false, outcomes_computed:false`. Generated: `research_state/trackc_funding_schema_audit_2026_11.json` (SHA256 `da36865dacea7004fb132940ba86d56cae8f89e80ab7b2d15dffb20a3eeb4218`, months `2026-11`, 5 symbols) → `missing=5, schema_bad=0, all_ok=false` (all 5 symbols missing local 2026-11 funding month files; blockers `MISSING_LOCAL_FUNDING_MONTH_FILES`, `CONFIRMATORY_REQUIRES_VERIFIED_PROVENANCE_CHECKSUMS`, `CONFIRMATORY_REQUIRES_FROZEN_PREREG_BEFORE_OUTCOMES`). `research_state/trackc_funding_schema_audit_2024Q1.json` (SHA256 `253c16cd65a9d9878a7ebe907ca4ce8d31cceb9852dfbee4255e33e6912e732b`, months `2024-01..03`, 5 symbols) → `missing=0, schema_bad=0, all_ok=true` locally/schema-wise but `provenance_verified:false, confirmatory_resume_ready:false`. Re-verified manifests/audits unchanged: `research_state/trackc_gap_repair_manifest_2026_11.json` (`fa153f5b…`, `confirmatory_resume_ready:false`, `locally_repairable_series_gaps_detected:false`, funding months missing union `["2026-11"]`...

**Binding priority:** P0 = **Track C funding-conditioned volatility** (repo name). Frozen confirmatory skeleton exists; **no confirmatory data exists today** (no >=5-symbol/>=3-block admissible panel with verified funding+provenance+checksums). `FUNDING_CONDITIONING_DEEPER_VALIDATION-002` = **COMPLETE_INCONCLUSIVE (EXPLORATORY_ONLY, 2026-11-09T16:39:00Z)**. Track B H003 = **COMPLETE_INCONCLUSIVE (2026-11-09T15:35:43Z)**. Track A = **STRUCTURALLY BLOCKED / NO TRIGGER** — **no probing, no scan/wrapper/report families, no guard-hardening churn**. No status-only churn. No sealed-holdout reuse, threshold shopping, or conflating observed/modeled/synthetic labels.

---

## 0) INITIAL TASK MESSAGE — 2026-11-10T01:09:13Z — MANDATORY HEAVY WORK (NEXT SESSION, UNAVOIDABLE)

**START HERE. Repo P0 = Track C funding-conditioned volatility. Track A frozen/blocked — do not touch.** Latest dep-light gate is green (**28/28 OK**) and audits/manifests show **NO confirmatory trigger** (`confirmatory_resume_ready=false`, `provenance_verified=false`). 2026_11 cache (5 symbols, 8 days, 0 blocks) has required mark/index/premium series but **no local 2026-11 funding month files** for all 5 symbols; all-cache has required-series gaps and missing 2026-11 funding month files. Gap-repair manifests report **no locally repairable path**; funding-schema audits confirm the same blockers. **Data cannot be invented or downloaded in this pass.** The next session MUST produce **measurable heavy progress** (tested code + evidence), not status narration.

### Do in order (pick the first applicable path and execute fully)

1. **Dep-light gate (record exact count):** `python -m unittest tests.test_volatility_features_splits tests.test_synthetic_boundary_labels tests.test_trackc_panel_admissibility_audit tests.test_trackc_gap_repair_manifest tests.test_trackc_funding_schema_audit -v` → expect **28/28 OK**. Never fabricate full-suite if heavy deps missing.
2. **Resume-trigger watch (no network by default):** if any cached panel fragments changed, run `trackc_panel_admissibility_audit`, `trackc_gap_repair_manifest`, and `trackc_funding_schema_audit` for affected windows/months (local only). **If `confirmatory_resume_ready` prerequisites are still unmet: do not compute outcomes.** Do not probe/download.
3. **IF AND ONLY IF an admissible local panel appears with verified provenance/checksums/funding completeness:** (a) freeze a **new** preregistration version **before any outcome inspection** (derive from `pre_registration_fclr014_confirmatory_funding_vol_20261109T181124Z.json`, SHA256 `4adf609e…`, preserve discipline; bump version/timestamp; record hashes); (b) materialize panel + chronological splits with 7-day purge/embargo (>=3 non-overlapping 30-day OOS blocks, >=5 symbols) and write a run manifest; (c) run confirmatory pipeline **only after prereg is frozen**: B0/B1/C1/C2, primary C2 vs B1 **test QLIKE**, block-bootstrap **2000** joint across instruments, **Holm** multiplicity, calibration/concentration/leakage checks per frozen prereg; (d) record commands, artifact paths, hashes, metrics, uncertainty, adjusted results, GO/NO-GO. **No sealed-holdout reuse, no threshold shopping, no tuning on test.**
4. **IF no confirmatory panel exists (current state):** do **tested Track C engineering that directly advances confirmatory readiness from local evidence** (must land code + tests, not prose). Preferred next heavy tasks: (A) **Build a deterministic local-only panel-window planner/ranker** over all cached `SYMBOL_YYYY_MM` windows — using admissibility audit + funding schema signals — that emits a machine-checkable ranked table of candidate contiguous multi-window panels (coverage days, required-series completeness, funding month presence/schema, provenance-sidecar presence, estimated non-overlapping 30-day blocks) and explicit blockers per candidate; stdlib, no network/outcomes. (B) Alternatively, if a manifest ever proves `locally_repairable_series_gaps_detected` for a real case, implement a deterministic **local-only repair executor** with checksum lineage/provenance fields and tests (current evidence shows no such case). (C) Extend `trackc_funding_schema_audit` with month-file checksum/ETag/provenance **lineage fields ingestion** only when local metadata files already exist (no network). **Do not compute confirmatory outcomes. Do not download/probe.**
5. **Update `AGENT_HANDOFF.md`** with UTC timestamp, exact commands, test counts, audit/manifest/schema-audit JSON paths/hashes, new file hashes, and the single next unfinished task.

### Hard constraints (violations = failure)

- No Track A probing/scans/wrappers/report families; no guard-hardening churn absent a rubric-GO unauthenticated liquidation trigger (then PREREG before outcomes).
- No confirmatory/promotion claims from exploratory runs; no sealed-holdout reuse; no threshold shopping; no prereg/estimand changes after seeing outcomes.
- Never conflate **observed** liquidations with **modeled/synthetic** boundary breaches (Track separation immutable).
- No `.github/workflows` edits; no schedulers/pollers/controllers; no credentials/paid data/access-control bypass; no live/paper trading.
- No fabricated outcomes. If blocked, record evidence + the next materially different admissible route.

### Bottleneck removal (kept explicit)

- **Track A guard-hardening bottleneck REMOVED:** `FCLR-NEXT-131` COMPLETE; `probes==2`, no trigger — **frozen**. Reopening = status-only churn.
- **Track C confirmatory blocker = admissible data + verified provenance:** 2026_11 missing 2026-11 funding month files for all 5 symbols and has 0 blocks; all-cache has series gaps + missing 2026-11 funding month files. Manifests/schema audits show no locally repairable/provenance-verified path. **Data/provenance gap cannot be papered over by code.** Next admissible engineering = tested local-only panel-window planner/ranker or provenance-lineage ingestion from already-present local metadata (no network/outcomes).

### Completed heavy work (evidence recorded)

1. **Track C reproducibility + audit hardening — COMPLETE.** STREAM_B summaries `001 20261109T162703Z`, `002 20261109T163517Z`.
2. **Frozen preregistration skeleton — COMPLETE (before outcomes).** `research_state/pre_registration_fclr014_confirmatory_funding_vol_20261109T181124Z.json`, SHA256 `4adf609e3f6b57ae7e0ad486150c787799c19d1b33432ebc5125bd33dde0073c`, `FROZEN_BEFORE_OUTCOMES`.
3. **Dep-light admissibility audit hardening — COMPLETE.** `scripts/trackc_panel_admissibility_audit.py` (`269a37fdd82181ba8019ee5148aa64e9b79f221c45a42a3d3c396671443442f4`) + `tests/test_trackc_panel_admissibility_audit.py` (`bb010ff07830677695f3544b1f79ebbbd710786826cf9aad69780941f1a9b88c`). Artifacts: `trackc_panel_admissibility_latest.json` (`b84f3bbe…`), `trackc_panel_admissibility_all_cache.json` (`7d74c0be…`), `confirmatory_resume_ready:false`.
4. **Gap/repair manifest — COMPLETE.** `scripts/trackc_gap_repair_manifest.py` (`51fd6b72e584749efa17d9b74203d807654bc19ea0a2ed4414ca21c53d316ee8`) + `tests/test_trackc_gap_repair_manifest.py` (`9e250e1720aa44de33fc204c6f7479c3d0ee19bd3646c15260d790f78ca370de`). `trackc_gap_repair_manifest_2026_11.json` (`fa153f5b…`), `trackc_gap_repair_manifest_all_cache.json` (`13b4644b…`) — no locally repairable path.
5. **Funding month-file schema/provenance checklist audit (2026-11-09T21:15:42Z, re-verified 2026-11-10T01:09:13Z) — COMPLETE.** `scripts/trackc_funding_schema_audit.py` (`78cbcd00e9620ea153e8399670c25d7c1b2aead5567e9b94f4daa8e321365667`) + `tests/test_trackc_funding_schema_audit.py` (`062430e62f105c28ab20c0ae2cc990d87b65fb8ac5596c84b70a5ba4cbe3c0bd`). `trackc_funding_schema_audit_2026_11.json` (`da36865dacea7004fb132940ba86d56cae8f89e80ab7b2d15dffb20a3eeb4218`) missing=5; `trackc_funding_schema_audit_2024Q1.json` (`253c16cd65a9d9878a7ebe907ca4ce8d31cceb9852dfbee4255e33e6912e732b`) missing=0/schema_ok but provenance unverified. Dep-light gate **28/28 OK**.

---

## 1) VERIFIED (2026-11-10T01:09:13Z)

| Check | Result |
|---|---|
| `git status --short` (before final handoff write) | `?? research_state/trackc_funding_schema_audit_2024Q1.json`, `?? research_state/trackc_funding_schema_audit_2026_11.json`, `?? scripts/trackc_funding_schema_audit.py`, `?? tests/test_trackc_funding_schema_audit.py` |
| `python -m unittest tests.test_volatility_features_splits tests.test_synthetic_boundary_labels tests.test_trackc_panel_admissibility_audit tests.test_trackc_gap_repair_manifest tests.test_trackc_funding_schema_audit -v` | **Ran 28 tests — OK** (31.504s) |
| `trackc_panel_admissibility_audit --window-hint 2026_11` (prior, re-verified artifact) | `b84f3bbe…` — `resume_trigger_met=false, confirmatory_resume_ready=false, symbols_ok=5, panel_blocks=0`; required series complete; **all 5 symbols funding `NO_MONTH_FILES_FOR_RANGE` for 2026-11** |
| `trackc_panel_admissibility_audit` all-cache (prior) | `7d74c0be…` — `resume_trigger_met=false, confirmatory_resume_ready=false`; BTC 31 + ETH/SOL/BNB/XRP 92 index/premium day gaps; funding missing 2026-11 |
| `trackc_gap_repair_manifest` 2026_11/all_cache (re-verified) | `fa153f5b…` / `13b4644b…` — `network_used:false, outcomes_computed:false, locally_repairable_series_gaps_detected:false`; funding months missing union `["2026-11"]` |
| `trackc_funding_schema_audit --months 2026-11` | `da36865d…` — `missing=5, schema_bad=0, all_ok=false, confirmatory_resume_ready:false, provenance_verified:false, network_used:false` |
| `trackc_funding_schema_audit --months 2024-01,2024-02,2024-03` | `253c16cd…` — `missing=0, schema_bad=0, all_ok=true` (local/schema), `confirmatory_resume_ready:false, provenance_verified:false` |
| Prereg skeleton (frozen) | `research_state/pre_registration_fclr014_confirmatory_funding_vol_20261109T181124Z.json`, SHA256 `4adf609e3f6b57ae7e0ad486150c787799c19d1b33432ebc5125bd33dde0073c` (re-verified) |

**Admissibility conclusion (actionable):** neither 2026_11 nor all-cache is confirmatory-admissible. 2026_11 lacks local 2026-11 funding month files and has 0 blocks; all-cache lacks required-series completeness and full funding coverage. Funding schema audit confirms 2026-11 month files missing locally for all 5 symbols and global provenance unverified. **No locally repairable path detected. Do not compute outcomes. Do not download/probe.**

---

## 2) DONE (carry forward)

- Volatility gate H001 closed NOT_SUPPORTED on claim-worthy panels (FCLR-001/002/003/008/v3/FCLR-013). Risk overlay INELIGIBLE.
- Track A structurally blocked; no admissible unauthenticated liquidation labels; ironflow probes==2 exhausted. Guard hardening frozen.
- Track B H003 **COMPLETE_INCONCLUSIVE** (2026-11-09T15:35:43Z).
- Track C `FUNDING_CONDITIONING_DEEPER_VALIDATION-002` **COMPLETE_INCONCLUSIVE (EXPLORATORY_ONLY)** (2026-11-09T16:39:00Z).
- FCLR-014 prereg skeleton frozen before outcomes (SHA256 `4adf609e…`).
- Admissibility audit + gap-repair manifest + funding schema checklist tooling/tests complete; artifacts show no confirmatory trigger and no locally repairable/provenance-verified path.

---

## 3) GATE STATE (binding)

| Gate | Status |
|---|---|
| Gate 1 | Track A BLOCKED; Track C cache/manifests present but not confirmatory-admissible |
| Gate 2 | Gate 4 v4 frozen-before-outcomes context preserved; no confirmatory claim |
| Gate 3 | Track C forward INCONCLUSIVE / data not confirmatory-admissible |
| Gate 4 | EXPLORATORY evidence only; NOT CONFIRMATORY/NOT PROMOTABLE |
| Forecast Gate | NOT ELIGIBLE |
| Track B H003 | COMPLETE_INCONCLUSIVE |
| Track C deeper validation | COMPLETE_INCONCLUSIVE (EXPLORATORY_ONLY) |

---

## 4) BOTTLENECKS

| Bottleneck | Status | Action |
|---|---|---|
| Confirmatory Track C blocked by data admissibility + provenance | structural/data | 2026_11 missing 2026-11 funding month files for all 5 symbols and has 0 blocks; all-cache has series gaps + missing 2026-11 funding month files. Manifests/schema audits show no locally repairable/provenance-verified path. Next: tested local-only panel-window planner/ranker over cached windows and/or provenance-lineage ingestion from already-present local metadata (no network/outcomes). |
| Prereg skeleton exists but panel not ready | actionable when panel ready | Freeze a **new** prereg version before any outcome inspection if/when admissible panel appears. Do not reuse prereg after outcome inspection. |
| Heavy deps may be missing in some runners | env | Use stdlib/dep-light tests + existing artifacts; tmp-isolate heavy-dep tests; never fabricate full-suite. |
| Track A no admissible labels | structural | No re-probe; trigger-only with prereg before outcomes. |

---

## 5) KEY EVIDENCE PATHS

- `AGENT_HANDOFF.md` (this file, single durable)
- `RESEARCH_PROMPT.md`
- `research_state/pre_registration_fclr014_confirmatory_funding_vol_20261109T181124Z.json` (frozen prereg skeleton, zero outcomes inspected)
- `scripts/trackc_panel_admissibility_audit.py` (`269a37f…`), `tests/test_trackc_panel_admissibility_audit.py` (`bb010ff…`)
- `scripts/trackc_gap_repair_manifest.py` (`51fd6b7…`), `tests/test_trackc_gap_repair_manifest.py` (`9e250e1…`)
- `scripts/trackc_funding_schema_audit.py` (`78cbcd0…`), `tests/test_trackc_funding_schema_audit.py` (`062430e…`)
- `research_state/trackc_panel_admissibility_latest.json` (`b84f3bbe…`)
- `research_state/trackc_panel_admissibility_all_cache.json` (`7d74c0be…`)
- `research_state/trackc_gap_repair_manifest_2026_11.json` (`fa153f5b…`)
- `research_state/trackc_gap_repair_manifest_all_cache.json` (`13b4644b…`)
- `research_state/trackc_funding_schema_audit_2026_11.json` (`da36865d…`)
- `research_state/trackc_funding_schema_audit_2024Q1.json` (`253c16cd…`)
- `research_state/experiment_frontier.json`, `research_state/negative_results_report.md`, `research_state/run_manifest.json` (LFS)

---

## 6) DO NOT DO

- ❌ Track A probing / scan/wrapper/report/status-file families
- ❌ Confirmatory/promotion claims from exploratory runs; threshold shopping; sealed holdout reuse
- ❌ New sealed outcomes without frozen preregistration
- ❌ Conflate observed liquidations with modeled/synthetic boundary breaches
- ❌ `.github/workflows` edits; schedulers/pollers/controllers
- ❌ Download/probe for missing Track C files in this engineering pass; do not bypass access controls
- ❌ Commit raw caches/zips/`__pycache__`/`ironflow_fastpath_cache.json`
- ❌ Live/paper trading, order endpoints, credentials, access-control bypass

---

## 7) SESSION START (mandatory)

1. Read **this file** + `RESEARCH_PROMPT.md`; `git status --short`.
2. Run dep-light verification: `python -m unittest tests.test_volatility_features_splits tests.test_synthetic_boundary_labels tests.test_trackc_panel_admissibility_audit tests.test_trackc_gap_repair_manifest tests.test_trackc_funding_schema_audit -v` (record count; expected **28/28**). Do not fabricate full-suite results if heavy deps missing.
3. Execute **§0 item 4**: if cached fragments changed, regenerate local audits/manifests (no network/outcomes). Build tested local-only **panel-window planner/ranker** (or deterministic local repair/provenance-lineage tooling only where evidence supports it). **Do not compute confirmatory outcomes.**
4. Update **this file** with exact evidence, hashes, commands, test counts, timestamps, and the next unfinished task.

---

**END OF SINGLE DURABLE HANDOFF. FUTURE AGENTS: START AT §0 — HEAVY WORK REQUIRED (2026-11-10T01:09:13Z).** Dep-light **28/28 OK**. `confirmatory_resume_ready=false`, `provenance_verified=false`. 2026_11/all_cache audits + gap-repair manifests + funding schema audits show **no locally repairable/provenance-verified path** (missing 2026-11 funding month files; all-cache series gaps). Do not compute outcomes; no network; no Track A probing.