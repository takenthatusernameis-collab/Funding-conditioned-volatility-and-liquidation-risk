# AGENT HANDOFF — 2026-11-17T00:23:34Z (sole durable handoff)

## INITIAL TASK MESSAGE FOR NEXT AGENTIC WORK SESSION (do this first)

**Priority 0 — repository and rank-0 state.**
- Repository: `Funding-conditioned-volatility-and-liquidation-risk` (funding-conditioned volatility and liquidation risk). The primary Track C volatility campaign is COMPLETE and gated; the Track A observed-liquidation arm is the active unfinished arm.
- Program: `CLOSED_TERMINAL` — final structural closure `research_state/fclr_final_structural_closure_20261116T114626.{md,json}`; verdict `NO_CLAIM_WORTHY_RESULT_PROMOTABLE; ALL_P1_P2_P3_SEALED`; no feasible 3-block pre-registered design in any domain.
- Rank-0: `FCLR-BOUNDED-TRIGGER-ONLY-20261115T220000Z` (`TRIGGER_ONLY` / `BOUNDED_TRIGGER_ONLY`, `next_action_heavy=null`). All cached-data confirmatory estimands are terminal.
- Consequence: **do not start or re-run any cached-data confirmatory estimand.** The only agent-removable heavy work is the independent reproducibility audit below. "Keep the suite green" is a floor, not completion.

**MANDATORY HEAVY WORK (non-skippable): FCLR-013 independent recompute, then FCLR-014.**
A trigger-check-only session, tests/gates-only session, copied bundle, re-audit of static bundles, or "no trigger → stop cleanly" is **NOT** completion. Completion requires ALL of:
1. new `research_state/session_<UTC>/`;
2. `recompute_fclr013_<UTC>.{py,json,md}` with an independent 2026-Q3 Track C recompute (plus FCLR-014 if its local inputs are valid and time permits);
3. `evidence_audit_<UTC>.md`;
4. gate captures + full-suite capture under the session dir;
5. this handoff updated with actual results and the queue ticked.

**Read first (in order):**
1. `research_state/resume_trigger_registry.json`
2. `research_state/ironflow_monitor_state.json`
3. `research_state/FCLR_HEAVY_CAMPAIGN_NEXT.md`
4. `research_state/session_20261117T002014Z/evidence_audit_20261117T002014Z.md` + `recompute_fclr010_20261117T002014Z.md` (latest completed heavy evidence; CSV/JSON parquet-free method)
5. `research_state/evaluation_summary_FCLR-013.md` + `research_state/pre_registration_fclr013_20261107T094132Z.md` + `research_state/fclr013_coverage_audit_20261107T0936Z.json`

**Completed work — do not repeat:**
- **FCLR-010 — DONE (`session_20261117T002014Z`).** Independent parquet-free recompute from `results/liqmicro_v2/panel_liqmicro_v2.csv` + `hyperliquid_funding/{SYM}.json`. Verdict **NOT_REPLICATED**: C2-vs-B1 Brier relative reduction **0.50%** (CI `[-0.001106,-0.000316]`, excludes zero) vs sealed **2.21%**; below the 2% materiality floor; LOIO (`>=4/5`) and placebo both **fail**; 17 symbols, n=64,056 test rows, 157 days. Direction replicates, magnitude does not. Do not re-run FCLR-010.
- FCLR-002 — `session_20261117T000400Z`; exact values diverged beyond tolerance; C2-vs-B1 directionally positive (`8.60%`, CI `[-0.093389,-0.005759]`); 70-day/2-block gate **NOT_MET**.
- FCLR-003 — `session_20261117T000400Z`; B0/B1 match, C1/C2 diverge; C2 vs B1 worse (`-11.85%`); **NOT_MET** corroborated.
- FCLR-009 — `session_20261116T125624Z`; `all_within_tolerance=true`.
- FCLR-006 — `session_20261116T185811Z`; `all_within_tolerance=true`.
- FCLR-008 — `session_20261116T230140Z`; B0/B1 within tolerance, C1/C2 divergence documented; qualitative **NOT_MET** corroborated.
- FCLR-RCA-011 — complete bundle `session_20261116T100533Z`.

**Next target — FCLR-013 (2026 Q3 funding-conditioned volatility, Track C):**
- Universe: BTCUSDT, ETHUSDT, BNBUSDT, SOLUSDT, XRPUSDT (5).
- Window: 2026-07-01 .. 2026-09-30; frozen splits: train 2026-07-01..2026-08-05, val 2026-08-06..2026-08-25, test 2026-08-26..2026-09-30 (7d embargo).
- Primary contrast: C2 vs B1 on next-24h realized variance QLIKE (2000-rep 24h-block bootstrap); sealed result **NOT_MET** (rel -1.32%, 1 test block). Recompute independently and issue an honest CONFIRMED/NOT_REPLICATED/INCONCLUSIVE verdict; do not re-score the sealed summary.
- Inputs (local, no network): `research_state/data_cache/{BTCUSDT,ETHUSDT,BNBUSDT,SOLUSDT,XRPUSDT}_2026_07|08|09/` — **ZIP archives** (`<SYM>-1h-YYYY-MM-DD.zip`, `BTCUSDT-fundingRate-*.zip`, index/premium). Use the ZIP-aware reader pattern from `session_20261117T000400Z/recompute_fclr002_003_20261117T000400Z.py`; a CSV-only glob will silently drop days.
- Do **not** use `scripts/fclr_liq_010_confirm.py` — it is parquet-only and cannot run here (see blocked-path warning).

**Blocked-path warning (do not waste a session here):**
- **No parquet engine is installed** (`pyarrow`, `fastparquet`, `duckdb`, `polars` all absent; network installs prohibited). Any task whose only input is `.parquet` is blocked unless a CSV/JSON twin exists. FCLR-010 was solved this way; FCLR-013 uses ZIP/CSV caches.
- `research_state/research_protocol_fclr002.md` and `research_state/research_protocol_fclr003.md` **do not exist** — do not block on them.
- `research_state/run_manifest.json`, `run_manifest_FCLR002.json`, `data_cache/fclr002_panel*.json`, `data_cache/manifest_fclr002.json`, `data_cache/manifest_fclr003.json` are **unresolved Git-LFS pointers with no local object**. Do NOT run `git lfs pull` (network is prohibited). FCLR-002/003 are already computed; do not repeat them.
- **2024 cache format:** Apr-Jun 2024 mark/premium/index files are ZIPs; Jan-Mar and Jul-Nov are CSVs. (Relevant only to already-completed FCLR-002/003.)

**Execute in order (do not skip to "stop cleanly"):**
1. **Create `research_state/session_<UTC>/`** (actual UTC). `research_state/` root is **500/500** (fail-closed cap); put ALL new artifacts inside the session subdirectory only.
2. **Check triggers exactly once (no network, no polling).** Read files 1–2. Record timestamp, each trigger status, `data_through`, and post-2026-10 month classifications in the session dir. Current state: all four `OPEN`; Ironflow `data_through=2026-10`, `consecutive_absent=3`; 2026-11/2026-12/2027-01 `CONFIRMED_ABSENT`.
3. **FCLR-013 independent recompute (primary).** Read the 2026 Q3 ZIP cache for the 5 symbols, independently reconstruct the registered estimand(s) from `pre_registration_fclr013_20261107T094132Z.md`, and write `recompute_fclr013_<UTC>.{py,json,md}` under the session dir. Do not read `run_manifest.json`, do not use parquet, and never mutate sealed artifacts.
4. **FCLR-014 (only if FCLR-013 completes cleanly and local inputs are valid).** Same independence rule; write `recompute_fclr014_<UTC>.{py,json,md}`. If FCLR-014's registered panel is parquet-only with no CSV/JSON twin, record the exact blocker and emit the closest non-parquet artifact instead of fabricating values.
5. **Audit carried-forward evidence.** Confirm `session_20261116T100533Z/` (5 RCA-011 families), `session_20261116T125624Z/` (FCLR-009), `session_20261116T185811Z/` (FCLR-006), `session_20261116T230140Z/` (FCLR-008), `session_20261117T000400Z/` (FCLR-002/003), and `session_20261117T002014Z/` (FCLR-010) are present. Write a concise evidence-audit artifact in the session dir. Do not rerun any of them.
6. **Run and capture every required gate under the new session dir:**
   - `python3 scripts/check_handoff_heavywork_gate.py --json` — PASS (complete bundle + new session audit + fresh quant artifact, root <= 500).
   - `python3 scripts/check_tracka_scope_registry_drift.py --json` — PASS (register any new script in both scope registries; a session-local recompute script under `research_state/session_*/` is not scanned, but any `scripts/*.py` addition must be registered).
   - `python3 -m unittest tests.test_active_campaign_gate tests.test_tracka_hardening_117 tests.test_tracka_hardening_118 tests.test_tracka_hardening_143` — all pass (52 tests).
   - `python3 -m unittest discover -q` — run to completion; record exact test count, skip count, error list, and final EXIT. **Baseline:** 1340 tests, 4 pre-existing errors (all `tests.test_fclr_liq_combined_admissibility_audit`, caused by missing `pyarrow`; environmental, not agent-caused), 18 skipped, EXIT 1. Success = identical set with no new failures/errors. Never treat timeout/monitor cap as green. Revert any timestamp-only side effect to tracked files.
7. **Update only this handoff** after steps 3–6: replace timestamp/verification with actual results, tick FCLR-013 (and FCLR-014 if done), keep sole-handoff contract, bundle refs, blockers intact. Do not create another handoff file.

**Trigger-gated science is the only scientific advance — but must be pre-powered.** If no trigger is satisfied, do not advance or re-run a confirmatory estimand; required holding action is the FCLR-013 reproducibility artifact + evidence audit + complete verification + accurate handoff update. If a trigger is satisfied, follow `RESEARCH_PROMPT.md` §16 admissibility/source audit first, freeze a pre-sized prereg before inspecting outcomes (use `session_20261116T035833Z/prereg_template_trigger_gated_20261116T035833Z.json` and power floors in `session_20261116T100533Z/trigger_readiness_power_calibration_20261116T100533Z.md`: Gate4/TrackC `paired_n>=23224`, TrackA/expansion `paired_n>=11689`, >=3 blocks, 7d purge/embargo), require a materially different estimand, execute, register any new scripts in both scope registries, run all gates, and update frontier/hypothesis registries with an honest verdict.

## Reproducibility-audit queue (non-skippable; do in order)

1. ~~FCLR-009~~ — DONE (`session_20261116T125624Z`; `all_within_tolerance=true`).
2. ~~FCLR-006~~ — DONE (`session_20261116T185811Z`; `all_within_tolerance=true`; supersedes tolerance-failed `session_20261116T140001Z`).
3. ~~FCLR-008~~ — DONE (`session_20261116T230140Z`; B0/B1 within tolerance; C1/C2 divergence documented; qualitative NOT_MET corroborated). `session_20261116T221127Z` is an earlier divergent FCLR-008 attempt with no evidence audit — **superseded, do not count/resume**.
4. ~~FCLR-002~~ — DONE (`session_20261117T000400Z`; exact values diverged beyond tolerance; qualitative C2-vs-B1 improvement corroborated; gate NOT_MET).
5. ~~FCLR-003~~ — DONE (`session_20261117T000400Z`; B0/B1 matched; C1/C2 diverged; NOT_MET corroborated).
6. ~~FCLR-010~~ — **DONE (`session_20261117T002014Z`; CSV/JSON parquet-free recompute; verdict NOT_REPLICATED: 0.50% vs sealed 2.21%, LOIO/placebo fail).**
7. **FCLR-013 (2026 Q3 panels, 5 symbols, ZIP cache): independent recompute — CURRENT TARGET (PRIMARY).**
8. **FCLR-014 (confirmatory funding-vol panel): independent recompute — NEXT (only if local non-parquet inputs valid).**

A session that completes an item must (a) create `research_state/session_<UTC>/`, (b) emit a new quantitative artifact named per queue, (c) write evidence audit, (d) run all gates + full discovery suite to completion with recorded EXIT, (e) update this handoff and tick the queue item.

## Heavy-work evidence on disk (authoritative; do not redo)

- **FCLR-010 — `research_state/session_20261117T002014Z/`:** parquet-free recompute (`recompute_fclr010_20261117T002014Z.{py,json,md}`), evidence audit, trigger check. Verdict NOT_REPLICATED.
- FCLR-002/FCLR-003 — `research_state/session_20261117T000400Z/` (recomputes, evidence audit, gate/suite captures).
- FCLR-008 — `research_state/session_20261116T230140Z/` (B0/B1 QLIKE match <=3e-7; C1/C2 divergence ~1.4e-3/2.1e-3; evidence audit and full gate/suite capture complete).
- FCLR-006 — `research_state/session_20261116T185811Z/` (`all_within_tolerance=true`).
- FCLR-009 — `research_state/session_20261116T125624Z/` (`all_within_tolerance=true`).
- Self-contained bundle: `research_state/session_20261116T100533Z/` (5 RCA-011 families + `trigger_readiness_power_calibration_*`/`trigger_readiness_power.py`).
- `research_state/session_20261116T115028Z/`: third numpy-only FCLR-011 crosscheck confirming sealed PASS not reproducible.

**Incomplete / non-counting sessions (do not resume, copy, or count):** `session_20261116T104644Z/`, `session_20261116T105341Z/`, `session_20261116T134957Z/` (trigger-only). `session_20261116T140001Z/` superseded (tolerance-failed FCLR-006). `session_20261116T221127Z/` superseded (divergent FCLR-008). No empty session directories present.

## Bottlenecks removed / prevented

- **Parquet engine absent (the FCLR-010 blocker, now removed):** `pyarrow`/`fastparquet`/`duckdb`/`polars` are not installed and network installs are prohibited. The FCLR-010 recompute was moved to `results/liqmicro_v2/panel_liqmicro_v2.csv` + `hyperliquid_funding/{SYM}.json`, proving the CSV/JSON path. Future sessions must use the same rule: if a registered input is parquet-only, find a CSV/JSON/ZIP twin or record the exact blocker — never fabricate.
- **FCLR-013 target made actionable:** its 2026 Q3 inputs are present as ZIP caches for all 5 symbols; no parquet is required. This is the concrete next heavy artifact.
- **Nonexistent protocol paths:** `research_protocol_fclr002.md` / `research_protocol_fclr003.md` do not exist. The frozen splits and published values are embedded in the handoff and `evaluation_summary_FCLR002/003.md`; FCLR-002/003 are complete.
- **Unresolved LFS inputs:** `run_manifest.json`, `run_manifest_FCLR002.json`, `fclr002_panel*.json`, `manifest_fclr002.json`, `manifest_fclr003.json` are pointers with no local object. Do not attempt `git lfs pull`.
- **2024 ZIP/CSV bottleneck:** Apr-Jun 2024 files are ZIPs; CSV-only readers silently drop the training window. Use the ZIP-aware reader from `session_20261117T000400Z` (FCLR-002/003, complete).
- **Frontier loophole closed:** the rank-0 frontier defers the concrete unfinished task to `FCLR_HEAVY_CAMPAIGN_NEXT.md`; that note defines a new quantitative artifact as the completion floor, so "keep the suite green" alone cannot close a session.
- **Duplicate FCLR-008 attempt marked:** `session_20261116T221127Z` is explicitly non-counting; `session_20261116T230140Z` is authoritative.
- **Suite baseline documented:** 4 errors are pre-existing missing-`pyarrow` errors in `test_fclr_liq_combined_admissibility_audit`; they are not agent-caused and must not be "fixed" by adding heavy deps to the core path.
- **Maintenance-refresh treadmill blocked:** handoff-only refreshes with no new heavy artifact are not completion; next session must emit `recompute_fclr013_<UTC>.{json,md}`.
- **Reproducibility path:** stdlib/numpy-only; no `statsmodels`/unpinned heavy deps in core path.
- **Handoff authority:** this file only (`AGENT_HANDOFF.md`).
- **Root churn:** 500/500 — session-only writes required.

## Bottlenecks and prohibitions

- Do not start or re-run any cached-data confirmatory estimand; all terminal.
- Do not mutate sealed artifacts, frontier, hypothesis registries, or `.github/workflows/*`.
- Do not poll, re-probe HuggingFace tree, use paid/credentialed/manual outcome data, or add root-level `research_state/*.md|json`.
- Do not add `statsmodels` or unpinned heavy dependencies to core path.
- Do not run `git lfs pull` or otherwise fetch network data.
- Do not run `scripts/fclr_liq_010_confirm.py` (parquet-only; will fail on import).
- Discovery suite is long-running; let it finish and record actual EXIT, not partial/timeout.
- Scientific blocker is external (no admissible post-2026-10 observed liquidation labels/source; no agent-settable Gate 4 attestation). Agent-removable requirement: new quantitative artifact + evidence audit + complete verification + accurate handoff update.

## Reopen triggers (machine-checkable — Act ONLY when satisfied; all `OPEN`)

- `GATE4_BRANCH_1` — `research_state/fclr016_v5_terms_evidence_RESOLVED_*.json` (`status: RESOLVED_VERIFIED`, `fabricated: false`). Human/legal attestation only.
- `NEW_OBSERVED_LIQUIDATION_SOURCE` — `research_state/<source>_admissibility_audit_<UTC>.{md,json}` (`status: ADMISSIBLE`, `observed_labels: true`, >=5 instruments, >=3 blocks or >=1 complete month).
- `HL_LABEL_EXTENSION` — `research_state/hl_label_extension_audit_<UTC>.{md,json}`.
- `EXPANSION_ROBUSTNESS_REDO` — `research_state/expansion_robustness_redo_prereg_<UTC>.json` + `evaluation_summary_*.json`.

## Tombstones (no authority)

- `NEXT_SESSION_HANDOFF.md`, `NEXT_SESSION_TASK.md`: tombstoned 2026-11-15T22:57:29Z.
- `AGENT_HANDOFF_20261115T073240Z.md`: SUPERSEDED — ignore.
- `HANDOFF_NEXT_SESSION_20261116T114626Z.md`: tombstoned 2026-11-16T12:45:00Z — ignore.

## Verification record — 2026-11-17T00:23:34Z handoff refresh

- **Changed:** refreshed the sole durable handoff; FCLR-010 marked **DONE** (`session_20261117T002014Z`, parquet-free CSV/JSON recompute, verdict **NOT_REPLICATED**: 0.50% vs sealed 2.21%, LOIO/placebo fail); next target set to **FCLR-013** (2026 Q3, 5-symbol ZIP cache); recorded the removed parquet-engine bottleneck and the FCLR-013 actionable path; ticked the reproducibility queue.
- **New heavy artifact:** `research_state/session_20261117T002014Z/recompute_fclr010_20261117T002014Z.{py,json,md}` + `evidence_audit_20261117T002014Z.md` + `trigger_check_20261117T002014Z.json`.
- **Baseline gates:** `check_handoff_heavywork_gate.py --json` **PASS**; `check_tracka_scope_registry_drift.py --json` **PASS**.
- **Targeted suite:** `test_active_campaign_gate`, `test_tracka_hardening_117/118/143` — **52 tests OK, EXIT 0**.
- **Full `unittest discover -q`:** recorded under the session dir; baseline 1340 tests, 4 pre-existing pyarrow errors, 18 skipped, EXIT 1; success = no new failures/errors.
- **Queue:** FCLR-009/006/008/002/003/010 DONE; FCLR-013 CURRENT; FCLR-014 NEXT.
- **Git tree:** new session artifacts under `research_state/session_20261117T002014Z/` only; no tracked file modified.

(End of file)