# AGENT_HANDOFF.md — Single Durable Handoff (next session MUST continue from here)

**Updated:** 2026-11-09T21:10:15Z — **Track C heavy engineering (no outcomes, no network, no Track A probing).** Dep-light gate **25/25 OK** (28.296s): `python -m unittest tests.test_volatility_features_splits tests.test_synthetic_boundary_labels tests.test_trackc_panel_admissibility_audit tests.test_trackc_gap_repair_manifest -v`. Added `scripts/trackc_gap_repair_manifest.py` (SHA256 `51fd6b72e584749efa17d9b74203d807654bc19ea0a2ed4414ca21c53d316ee8`) + `tests/test_trackc_gap_repair_manifest.py` (`9e250e1720aa44de33fc204c6f7479c3d0ee19bd3646c15260d790f78ca370de`): consumes `trackc_panel_admissibility_*.json`, emits deterministic per-symbol/per-series missing-day ranges, missing funding month files, local file/sidecar presence samples, checksum/provenance expectations, and evidence-backed blockers — **no download, no outcomes**. Generated manifests (`outcomes_computed:false, network_used:false, confirmatory_resume_ready:false`): `research_state/trackc_gap_repair_manifest_2026_11.json` (SHA256 `fa153f5b6f38e94c0243f28125a88417cbd8c60c18ca96a966067ffddf544605`, source audit `b84f3bbe…`) → `any_required_series_gaps=false`, `funding_months_missing_union=["2026-11"]`, `locally_repairable_series_gaps_detected=false` (2026_11 mark/index/premium complete for 5 symbols/8 days but **no 2026-11 funding month files in cache**; 0 blocks). `research_state/trackc_gap_repair_manifest_all_cache.json` (SHA256 `13b4644bf71cb48962d1d11e4d1c2ed87baeeae16cf56c3ab849029b3ac42c0e`, source audit `7d74c0be…`) → `any_required_series_gaps=true` (BTC 31 index/premium day gaps; ETH/SOL/BNB/XRP 92 each), `funding_months_missing_union=["2026-11"]`, `locally_repairable_series_gaps_detected=false`. FCLR-014 prereg re-verified SHA256 `4adf609e3f6b57ae7e0ad486150c787799c19d1b33432ebc5125bd33dde0073c` (frozen before outcomes). **No `.github/workflows` edits. No confirmatory outcomes. No Track A probing.**

**Binding priority:** P0 = **Track C funding-conditioned volatility** (repo name). Frozen confirmatory skeleton exists; **no confirmatory data exists today** (no >=5-symbol/>=3-block admissible panel with verified funding+provenance+checksums). `FUNDING_CONDITIONING_DEEPER_VALIDATION-002` = **COMPLETE_INCONCLUSIVE (EXPLORATORY_ONLY, 2026-11-09T16:39:00Z)**. Track B H003 = **COMPLETE_INCONCLUSIVE (2026-11-09T15:35:43Z)**. Track A = **STRUCTURALLY BLOCKED / NO TRIGGER** — **no probing, no scan/wrapper/report families, no guard-hardening churn**. No status-only churn. No sealed-holdout reuse, threshold shopping, or conflating observed/modeled/synthetic labels.

---

## 0) INITIAL TASK MESSAGE — 2026-11-09T21:10:15Z — MANDATORY HEAVY WORK (NEXT SESSION, UNAVOIDABLE)

**START HERE. Repo P0 = Track C funding-conditioned volatility. Track A frozen/blocked — do not touch.** Latest dep-light gate is green (**25/25 OK**) and audits/manifests show **NO confirmatory trigger** (`confirmatory_resume_ready=false`). The next session MUST produce **measurable heavy progress**, not status narration.

### Do in order (pick the first applicable path and execute fully)
1. **Dep-light gate (record exact count):** `python -m unittest tests.test_volatility_features_splits tests.test_synthetic_boundary_labels tests.test_trackc_panel_admissibility_audit tests.test_trackc_gap_repair_manifest -v` → expect **25/25 OK**. Never fabricate full-suite if heavy deps missing.
2. **Resume-trigger watch (no network by default):** run `python scripts/trackc_panel_admissibility_audit.py [--window-hint <candidate>]` and `python scripts/trackc_gap_repair_manifest.py --audit <audit.json> --repo-root . --out <manifest.json>` on any **new/changed** cached panel fragments. Current evidence (2026-11-09T21:10:15Z): `2026_11` = 5 symbols × 8 days, 0 blocks, required series complete, **all 5 symbols missing 2026-11 funding month files** (`NO_MONTH_FILES_FOR_RANGE`); all-cache has BTC 31 + ETH/SOL/BNB/XRP 92 index/premium day gaps and missing 2026-11 funding month files. **No locally repairable series gaps detected by manifests. If `resume_trigger_met=false` / blockers remain: do not compute outcomes.**
3. **IF AND ONLY IF `resume_trigger_met=true` AND funding completeness + provenance (URLs/ETags/checksums) are verified for the panel:** (a) create/freeze a **new** preregistration version **before any outcome inspection** (derive from `pre_registration_fclr014_confirmatory_funding_vol_20261109T181124Z.json`, SHA256 `4adf609e…`, preserve its discipline; bump version/timestamp; record hashes); (b) materialize the panel + chronological splits with 7-day purge/embargo (>=3 non-overlapping 30-day OOS blocks, >=5 symbols) and write a run manifest; (c) run the confirmatory pipeline **only after prereg is frozen**: B0/B1/C1/C2, primary C2 vs B1 **test QLIKE**, block-bootstrap **2000** joint across instruments, **Holm** multiplicity, calibration/concentration/leakage checks per frozen prereg; (d) record all commands, artifact paths, hashes, metrics, uncertainty, and GO/NO-GO with adjusted results. **No sealed-holdout reuse, no threshold shopping, no tuning on test.**
4. **IF no confirmatory panel exists (current state):** do **tested Track C engineering that directly unblocks confirmatory readiness** (must land code + tests, not prose): extend the gap-repair workflow with a deterministic **local-only repair executor** for cases the manifest *can* prove locally repairable (e.g., assemble missing day CSVs from already-present admissible local zip/CSV sources with checksum lineage and explicit provenance fields) — **no network, no outcomes**. If no locally repairable path exists (current manifests show `locally_repairable_series_gaps_detected=false` and missing 2026-11 funding month files absent locally), build the next tested engineering artifact that is still useful: e.g. a **funding/provenance checklist validator** or **month-file/schema verifier** over already-present local funding files + a machine-checkable blocker register, or a deterministic panel-window planner that ranks cached windows by distance-to-admissibility (blocks/series/funding/provenance) — all stdlib, tested, no outcomes/network. **Do not download or probe. Do not run confirmatory outcomes** unless `confirmatory_resume_ready` prerequisites are satisfied by verified data + a newly frozen prereg version before outcomes.
5. **Update `AGENT_HANDOFF.md`** with UTC timestamp, exact commands, test counts, audit/manifest JSON paths/hashes, any new file hashes, and the single next unfinished task.

### Hard constraints (violations = failure)
- No Track A probing/scans/wrappers/report families; no guard-hardening churn absent a rubric-GO unauthenticated liquidation trigger (then PREREG before outcomes).
- No confirmatory/promotion claims from exploratory runs; no sealed-holdout reuse; no threshold shopping; no prereg/estimand changes after seeing outcomes.
- Never conflate **observed** liquidations with **modeled/synthetic** boundary breaches (Track separation immutable).
- No `.github/workflows` edits; no schedulers/pollers/controllers; no credentials/paid data/access-control bypass; no live/paper trading.
- No fabricated outcomes. If blocked, record evidence + the next materially different admissible route.

### Bottleneck removal (kept explicit)
- **Track A guard-hardening bottleneck REMOVED:** `FCLR-NEXT-131` COMPLETE; `probes==2`, no trigger — **frozen**. Reopening = status-only churn.
- **Track C confirmatory blocker = admissible data:** requires >=5 symbols, >=3 non-overlapping 30-day OOS blocks, verified unauthenticated provenance/funding/checksums. 2026_11 is 8 days (0 blocks) and missing 2026-11 funding month files locally; all-cache has series/funding gaps. **Data gap cannot be papered over by code** — gap/repair manifests make blockers machine-checkable. Next admissible engineering = local-only repair executor for provable local repairs, or tested readiness/planner/checklist tooling (no network/outcomes).

### Completed heavy work (evidence recorded)
1. **Track C reproducibility + audit hardening — COMPLETE.** `research_state/trackc_reproducibility_audit_20251109T175518Z.md`/`20261109T175518Z.md` context preserved in prior sessions; STREAM_B summaries `001 20261109T162703Z`, `002 20261109T163517Z`.
2. **Frozen preregistration skeleton — COMPLETE (before outcomes).** `research_state/pre_registration_fclr014_confirmatory_funding_vol_20261109T181124Z.json`, SHA256 `4adf609e3f6b57ae7e0ad486150c787799c19d1b33432ebc5125bd33dde0073c`, `FROZEN_BEFORE_OUTCOMES`, zero outcome values inspected.
3. **Dep-light admissibility audit hardening — COMPLETE.** `scripts/trackc_panel_admissibility_audit.py` (SHA256 `269a37fdd82181ba8019ee5148aa64e9b79f221c45a42a3d3c396671443442f4`) + `tests/test_trackc_panel_admissibility_audit.py` (`bb010ff07830677695f3544b1f79ebbbd710786826cf9aad69780941f1a9b88c`), 6 tests. Artifacts: `research_state/trackc_panel_admissibility_latest.json` (`b84f3bbe…`, 2026-11-09T20:15:20Z), `research_state/trackc_panel_admissibility_all_cache.json` (`7d74c0be…`, 2026-11-09T20:15:44Z), both `outcomes_computed:false, network_used:false, confirmatory_resume_ready:false`.
4. **Gap/repair manifest (this session, 2026-11-09T21:10:15Z) — COMPLETE.** `scripts/trackc_gap_repair_manifest.py` (`51fd6b72…`) + `tests/test_trackc_gap_repair_manifest.py` (`9e250e17…`), 3 tests. Generated: `research_state/trackc_gap_repair_manifest_2026_11.json` (`fa153f5b…`, source `b84f3bbe…`) — 2026_11 no series gaps but missing 2026-11 funding month files for all 5 symbols, not locally repairable; `research_state/trackc_gap_repair_manifest_all_cache.json` (`13b4644b…`, source `7d74c0be…`) — all-cache has series gaps + missing 2026-11 funding month files, not locally repairable. Gate: **25/25 OK** (28.296s).

---

## 1) VERIFIED (2026-11-09T21:10:15Z)

| Check | Result |
|---|---|
| `git status --short` (before final handoff write) | worktree contains Track C code/test/artifact additions/updates (record exact status at session end) |
| `python -m unittest tests.test_volatility_features_splits tests.test_synthetic_boundary_labels tests.test_trackc_panel_admissibility_audit tests.test_trackc_gap_repair_manifest -v` | **Ran 25 tests — OK** (28.296s) |
| `trackc_panel_admissibility_audit --window-hint 2026_11` | `b84f3bbe…` — `resume_trigger_met=false, confirmatory_resume_ready=false, symbols_ok=5, panel_blocks=0`; required series complete; **all 5 symbols funding `NO_MONTH_FILES_FOR_RANGE` for 2026-11** |
| `trackc_panel_admissibility_audit` all-cache | `7d74c0be…` — `resume_trigger_met=false, confirmatory_resume_ready=false, symbols_ok=0, panel_blocks=0`; BTC 31 + ETH/SOL/BNB/XRP 92 index/premium day gaps; funding `PARTIAL_MONTH_FILES` 34/35, missing 2026-11 |
| `trackc_gap_repair_manifest` 2026_11/all_cache | `fa153f5b…` / `13b4644b…` — `network_used:false, outcomes_computed:false, locally_repairable_series_gaps_detected:false`; funding months missing union `["2026-11"]` |
| Prereg skeleton (frozen) | `research_state/pre_registration_fclr014_confirmatory_funding_vol_20261109T181124Z.json`, SHA256 `4adf609e3f6b57ae7e0ad486150c787799c19d1b33432ebc5125bd33dde0073c` (re-verified) |

**Admissibility conclusion (actionable):** neither 2026_11 nor all-cache is confirmatory-admissible. 2026_11 lacks funding month files and blocks; all-cache lacks required-series completeness and full funding coverage. Current gap-repair manifests show **no locally repairable path** from already-present admissible files. **Do not compute outcomes. Do not download/probe.**

---

## 2) DONE (carry forward)

- Volatility gate H001 closed NOT_SUPPORTED on claim-worthy panels (FCLR-001/002/003/008/v3/FCLR-013). Risk overlay INELIGIBLE.
- Track A structurally blocked; no admissible unauthenticated liquidation labels; ironflow probes==2 exhausted. Guard hardening frozen.
- Track B H003 **COMPLETE_INCONCLUSIVE** (2026-11-09T15:35:43Z).
- Track C `FUNDING_CONDITIONING_DEEPER_VALIDATION-002` **COMPLETE_INCONCLUSIVE (EXPLORATORY_ONLY)** (2026-11-09T16:39:00Z).
- FCLR-014 prereg skeleton frozen before outcomes (SHA256 `4adf609e…`).
- Admissibility audit + gap-repair manifest tooling/tests complete; artifacts show no confirmatory trigger and no locally repairable path.

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
| Confirmatory Track C blocked by data admissibility | structural/data | 2026_11 missing 2026-11 funding month files for all 5 symbols and has 0 blocks; all-cache has series gaps + missing 2026-11 funding month files. Gap-repair manifests show no locally repairable path. Next: tested local-only readiness/planner/checklist tooling (no network/outcomes), or deterministic repair executor only if future manifest proves local repairability. |
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
- `research_state/trackc_panel_admissibility_latest.json` (`b84f3bbe…`, 2026-11-09T20:15:20Z)
- `research_state/trackc_panel_admissibility_all_cache.json` (`7d74c0be…`, 2026-11-09T20:15:44Z)
- `research_state/trackc_gap_repair_manifest_2026_11.json` (`fa153f5b…`)
- `research_state/trackc_gap_repair_manifest_all_cache.json` (`13b4644b…`)
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
2. Run dep-light verification: `python -m unittest tests.test_volatility_features_splits tests.test_synthetic_boundary_labels tests.test_trackc_panel_admissibility_audit tests.test_trackc_gap_repair_manifest -v` (record count; expected **25/25**). Do not fabricate full-suite results if heavy deps missing.
3. Execute **§0 item 4**: if cached fragments changed, regenerate audits/manifests (no network/outcomes). Build tested local-only readiness/planner/checklist or repair-executor engineering only where manifests prove local repairability (current: none). **Do not compute confirmatory outcomes.**
4. Update **this file** with exact evidence, hashes, commands, test counts, timestamps, and the next unfinished task.

---

**END OF SINGLE DURABLE HANDOFF. FUTURE AGENTS: START AT §0 — HEAVY WORK REQUIRED (2026-11-09T21:10:15Z).** Dep-light **25/25 OK**. `confirmatory_resume_ready=false`. 2026_11/all_cache gap-repair manifests show **no locally repairable path** (missing 2026-11 funding month files; all-cache series gaps). Do not compute outcomes; no network; no Track A probing.
