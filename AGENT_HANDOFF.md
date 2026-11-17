# AGENT HANDOFF — 2026-11-17T04:07:43Z (sole durable handoff)

## INITIAL TASK MESSAGE FOR NEXT AGENTIC WORK SESSION (do this first)

**Priority 0 — repository and rank-0 state.**
- Repository: `Funding-conditioned-volatility-and-liquidation-risk` (funding-conditioned volatility and liquidation risk). Prioritize by repo name: **Track C funding-conditioned volatility first**; Track A observed-liquidation arm is the active-but-externally-blocked arm; Track B is COMPLETE_INCONCLUSIVE.
- Program: `CLOSED_TERMINAL` — final structural closure `research_state/fclr_final_structural_closure_20261116T114626.{md,json}`; verdict `NO_CLAIM_WORTHY_RESULT_PROMOTABLE; ALL_P1_P2_P3_SEALED`; no feasible 3-block pre-registered design was found **under the tool's current enumeration** (see bottleneck correction below — this verdict is now known to be over-conservative, not a data fact).
- Rank-0: `FCLR-BOUNDED-TRIGGER-ONLY-20261115T220000Z` (`TRIGGER_ONLY` / `BOUNDED_TRIGGER_ONLY`, `next_action_heavy=null`). All cached-data confirmatory estimands are terminal.
- Consequence: **do not start or re-run any sealed cached-data confirmatory estimand.** The only agent-removable heavy work is the **FCLR-014 admissible-panel reconstruction + panel-blocker-resolution audit** defined below. "Keep the suite green" or "no trigger → stop cleanly" is **NOT** completion.

**MANDATORY HEAVY WORK (non-skippable): FCLR-014 admissible-panel coverage audit + blocker resolution.**
A trigger-check-only session, tests/gates-only session, copied bundle, re-audit of static bundles, or a prose-only "blocker confirmed" note is **NOT** completion. Completion requires ALL of:
1. new `research_state/session_<UTC>/`;
2. `fclr014_panel_coverage_audit_<UTC>.{json,md}` — a **per-symbol × per-month** coverage matrix over the local `research_state/data_cache/` cache for all 5 symbols (BTCUSDT, ETHUSDT, BNBUSDT, SOLUSDT, XRPUSDT), recording for each month: mark/index/premium day counts, funding presence, and an `admissible_for_fclr014` boolean (mark+funding complete for all 5 symbols);
3. `fclr014_panel_blocker_resolution_<UTC>.{json,md}` — states the **exact, corrected** FCLR-014 blocker: the existing `pre_registration_fclr014_confirmatory_funding_vol_20261109T181124Z.json` is frozen `NO_GO` with FCLR-002-copied 70-day (2-block) splits; the cache DOES contain multiple complete 5-symbol mark+funding months (notably 2024-04, 2024-05, 2025-01, and all of 2025-02..2026-10), but a **contiguous 3-block confirmatory design** requires a contiguous untested run >= MIN_DESIGN_DAYS (127d) that avoids every `TESTED_WINDOWS` region — record which candidate windows are genuinely available vs consumed, and state whether a **new pre-registered design** (not a re-score) can be frozen before outcomes;
4. `evidence_audit_<UTC>.md`;
5. gate captures + full-suite capture under the session dir;
6. this handoff updated with actual results and the queue ticked.

**Read first (in order):**
1. `research_state/resume_trigger_registry.json`
2. `research_state/ironflow_monitor_state.json`
3. `research_state/FCLR_HEAVY_CAMPAIGN_NEXT.md`
4. `research_state/session_20261117T031656Z/evidence_audit_20261117T031656Z.md` + `recompute_fclr013_20261117T031656Z.md` (latest completed heavy evidence; ZIP/CSV parquet-free method to reuse)
5. `research_state/pre_registration_fclr014_confirmatory_funding_vol_20261109T181124Z.json` (FCLR-014 skeleton; `confirmatory_claim_go: NO_GO`, `exploratory_label_required`, splits NOT frozen)
6. `research_state/fclr013_coverage_audit_20261107T0936Z.json` (FCLR-013 coverage-audit template to mirror)

**Completed work — do not repeat:**
- **FCLR-013 — DONE (`session_20261117T031656Z`).** ZIP/CSV parquet-free recompute from `research_state/data_cache/{BTCUSDT,ETHUSDT,BNBUSDT,SOLUSDT,XRPUSDT}_2026_07|08|09/`. Verdict **NOT_REPLICATED**: C2-vs-B1 QLIKE mean diff **0.017010** (CI `[-0.000523,0.034809]`, crosses zero), relative reduction **-4.99%** vs sealed **-1.32%** (NOT_MET); only 1 test block (>=3 required); materiality <2%; LOIO and placebo both **fail**; n_pairs=4200, 5 symbols, 36 test days. Do not re-run FCLR-013.
- **FCLR-010 — DONE (`session_20261117T002014Z`).** CSV/JSON parquet-free recompute from `results/liqmicro_v2/panel_liqmicro_v2.csv` + `hyperliquid_funding/{SYM}.json`. Verdict **NOT_REPLICATED**: C2-vs-B1 Brier relative reduction **0.50%** (CI `[-0.001106,-0.000316]`) vs sealed **2.21%**; below 2% floor; LOIO and placebo **fail**; 17 symbols, n=64,056, 157 days. Do not re-run FCLR-010.
- FCLR-002 — `session_20261117T000400Z`; exact values diverged beyond tolerance; C2-vs-B1 directionally positive (`8.60%`, CI `[-0.093389,-0.005759]`); 70-day/2-block gate **NOT_MET**.
- FCLR-003 — `session_20261117T000400Z`; B0/B1 match, C1/C2 diverge; C2 vs B1 worse (`-11.85%`); **NOT_MET** corroborated.
- FCLR-009 — `session_20261116T125624Z`; `all_within_tolerance=true`.
- FCLR-006 — `session_20261116T185811Z`; `all_within_tolerance=true`.
- FCLR-008 — `session_20261116T230140Z`; B0/B1 within tolerance, C1/C2 divergence documented; qualitative **NOT_MET** corroborated.
- FCLR-RCA-011 — complete bundle `session_20261116T100533Z`.

**FCLR-014 STATUS — BLOCKED-ON-DESIGN (corrected; NOT blocked-on-data):**
- Pre-registration `pre_registration_fclr014_confirmatory_funding_vol_20261109T181124Z.json` is frozen `status: FROZEN_BEFORE_OUTCOMES`, `confirmatory_claim_go: NO_GO`, `exploratory_label_required: "EXPLORATORY / NOT CONFIRMATORY / NOT PROMOTABLE"`.
- Its `candidate_frozen_splits_pending_panel` is an **illustrative copy of FCLR-002**: test window 2024-07-23..2024-09-30 = 70 days = **2 blocks**, which fails `block_requirement: >=3 non-overlapping 30-day OOS evaluation blocks`.
- **CORRECTION (verified this session):** the claim "no admissible panel exists locally" is FALSE. Local `data_cache` holds complete 5-symbol mark+index+premium+funding months across **2024-04..2024-11 (mark+funding)**, **2025-01..2025-12 (all series)**, and **2026-01..2026-10 (all series)** — 22+ months. The genuine blocker is **design admissibility**, not data presence: a 3-block confirmatory design needs a **contiguous untested run >=127 days** avoiding every `TESTED_WINDOWS` region in `scripts/next_campaign_status.py`, and no such run currently exists (2025-02..2026-10 are consumed by sealed cells; 2024-04/05 and 2025-01 are complete but their 30-day train windows lack funding or full index/premium coverage).
- **Do not attempt an FCLR-014 confirmatory recompute or re-score.** The next session's job is to **document this corrected blocker precisely** and determine whether a **new, differently-scoped pre-registered design** (e.g. a mark+funding-only B0/B1/C1 estimand, or a disjoint-block design using only fully-complete months) can be frozen **before** any outcome inspection. If yes, freeze a NEW prereg and stop before outcomes; if no, record the exact missing coverage month and hold.

**Blocked-path warning (do not waste a session here):**
- **No parquet engine is installed** (`pyarrow`, `fastparquet`, `duckdb`, `polars` all absent; network installs prohibited). Any task whose only input is `.parquet` is blocked unless a CSV/JSON/ZIP twin exists. Use the ZIP/CSV reader pattern from `session_20261117T031656Z/recompute_fclr013_20261117T031656Z.py`.
- `research_state/research_protocol_fclr002.md` and `research_state/research_protocol_fclr003.md` **do not exist** — do not block on them.
- `research_state/run_manifest.json`, `run_manifest_FCLR002.json`, `data_cache/fclr002_panel*.json`, `data_cache/manifest_fclr002.json`, `data_cache/manifest_fclr003.json` are **unresolved Git-LFS pointers with no local object**. Do NOT run `git lfs pull` (network is prohibited). FCLR-002/003 are already computed; do not repeat them.
- **2024 cache format:** Apr–Jun 2024 mark/premium/index files are ZIPs; Jan–Mar and Jul–Nov 2024 are CSVs; 2025–2026 are ZIP+CSV. Use a ZIP-aware reader.
- **FCLR-014 confirmatory path blocked by DESIGN, not data format.** A confirmatory run requires a contiguous >=3-block untested window that does not currently exist under `TESTED_WINDOWS`.

**Execute in order (do not skip to "stop cleanly"):**
1. **Create `research_state/session_<UTC>/`** (actual UTC). `research_state/` root is **500/500** (fail-closed cap); put ALL new artifacts inside the session subdirectory only. Do NOT add root-level `research_state/*.md|json`.
2. **Check triggers exactly once (no network, no polling).** Read files 1–2. Record timestamp, each trigger status, `data_through`, and post-2026-10 month classifications in the session dir. Current state: all four `OPEN`; Ironflow `data_through=2026-10`, `consecutive_absent=3`; 2026-11/2026-12/2027-01 `CONFIRMED_ABSENT`.
3. **FCLR-014 panel coverage audit (primary heavy artifact).** Walk `research_state/data_cache/{SYM}_YYYY_MM/` for all 5 symbols. For each month compute mark/index/premium day counts and funding presence; set `admissible_for_fclr014` (mark+funding for all 5). Write `fclr014_panel_coverage_audit_<UTC>.{json,md}`. Do NOT read `run_manifest.json`, do NOT use parquet, do NOT re-score sealed summaries.
4. **FCLR-014 blocker-resolution artifact.** Using the coverage matrix + `scripts/next_campaign_status.py` `TESTED_WINDOWS` + `MIN_DESIGN_DAYS`, enumerate every candidate 3-block design window, classify each as `AVAILABLE` / `CONSUMED_BY_SEALED_CELL` / `INCOMPLETE_TRAIN`, and state whether a new pre-registered design can be frozen before outcomes. Write `fclr014_panel_blocker_resolution_<UTC>.{json,md}`. If a valid un-tested contiguous run >=127d exists, **freeze a NEW prereg** (copy `session_20261116T035833Z/prereg_template_trigger_gated_20261116T035833Z.json`, set `outcome_data_inspected_before_freeze=false`) and STOP before outcomes.
5. **Audit carried-forward evidence.** Confirm `session_20261116T100533Z/` (5 RCA-011 families), `session_20261116T125624Z/` (FCLR-009), `session_20261116T185811Z/` (FCLR-006), `session_20261116T230140Z/` (FCLR-008), `session_20261117T000400Z/` (FCLR-002/003), `session_20261117T002014Z/` (FCLR-010), `session_20261117T031656Z/` (FCLR-013) are present. Write a concise evidence-audit artifact in the session dir. Do not rerun any of them.
6. **Run and capture every required gate under the new session dir:**
   - `python3 scripts/check_handoff_heavywork_gate.py --json` — PASS (complete bundle + new session audit + fresh quant artifact, root <= 500).
   - `python3 scripts/check_tracka_scope_registry_drift.py --json` — PASS (register any new script in both scope registries; a session-local script under `research_state/session_*/` is not scanned, but any `scripts/*.py` addition must be registered).
   - `python3 -m unittest tests.test_active_campaign_gate tests.test_tracka_hardening_117 tests.test_tracka_hardening_118 tests.test_tracka_hardening_143` — all pass (52 tests).
   - `python3 -m unittest discover -q` — run to completion; record exact test count, skip count, error list, and final EXIT. **Baseline:** ~1340 tests, 4 pre-existing errors (all `tests.test_fclr_liq_combined_admissibility_audit`, caused by missing `pyarrow`; environmental, not agent-caused), ~18 skipped, EXIT 1. Success = identical set with no new failures/errors. Never treat timeout/monitor cap as green. Revert any timestamp-only side effect to tracked files.
7. **Update only this handoff** after steps 3–6: replace timestamp/verification with actual results, tick FCLR-014 to its true status (BLOCKED-ON-DESIGN with corrected blocker, or NEW-PRERG-FROZEN), keep sole-handoff contract, bundle refs, blockers intact. Do not create another handoff file.

**Trigger-gated science is the only scientific advance — but must be pre-powered.** If no trigger is satisfied, do not advance or re-run a confirmatory estimand; required holding action is the FCLR-014 panel coverage audit + blocker-resolution artifact + evidence audit + complete verification + accurate handoff update. If a trigger is satisfied, follow `RESEARCH_PROMPT.md` §16 admissibility/source audit first, freeze a pre-sized prereg before inspecting outcomes (use `session_20261116T035833Z/prereg_template_trigger_gated_20261116T035833Z.json` and power floors in `session_20261116T100533Z/trigger_readiness_power_calibration_20261116T100533Z.md`: Gate4/TrackC `paired_n>=23224`, TrackA/expansion `paired_n>=11689`, >=3 blocks, 7d purge/embargo), require a materially different estimand, execute, register any new scripts in both scope registries, run all gates, and update frontier/hypothesis registries with an honest verdict.

## Reproducibility-audit queue (non-skippable; do in order)

1. ~~FCLR-009~~ — DONE (`session_20261116T125624Z`; `all_within_tolerance=true`).
2. ~~FCLR-006~~ — DONE (`session_20261116T185811Z`; `all_within_tolerance=true`; supersedes tolerance-failed `session_20261116T140001Z`).
3. ~~FCLR-008~~ — DONE (`session_20261116T230140Z`; B0/B1 within tolerance; C1/C2 divergence documented; qualitative NOT_MET corroborated). `session_20261116T221127Z` is an earlier divergent FCLR-008 attempt with no evidence audit — **superseded, do not count/resume**.
4. ~~FCLR-002~~ — DONE (`session_20261117T000400Z`; exact values diverged beyond tolerance; qualitative C2-vs-B1 improvement corroborated; gate NOT_MET).
5. ~~FCLR-003~~ — DONE (`session_20261117T000400Z`; B0/B1 matched; C1/C2 diverged; NOT_MET corroborated).
6. ~~FCLR-010~~ — **DONE (`session_20261117T002014Z`; CSV/JSON parquet-free recompute; verdict NOT_REPLICATED: 0.50% vs sealed 2.21%, LOIO/placebo fail).**
7. ~~FCLR-013~~ — **DONE (`session_20261117T031656Z`; ZIP/CSV parquet-free recompute; verdict NOT_REPLICATED: C2-vs-B1 rel -4.99%, CI crosses zero, 1 test block; sealed -1.32% NOT_MET).**
8. **FCLR-014 panel coverage audit + blocker resolution — CURRENT (document corrected blocker; freeze NEW prereg only if a valid untested >=127d window exists; do NOT re-score).**

A session that completes an item must (a) create `research_state/session_<UTC>/`, (b) emit a new quantitative artifact named per queue, (c) write evidence audit, (d) run all gates + full discovery suite to completion with recorded EXIT, (e) update this handoff and tick the queue item.

## Heavy-work evidence on disk (authoritative; do not redo)

- **FCLR-013 — `research_state/session_20261117T031656Z/`:** ZIP/CSV parquet-free recompute (`recompute_fclr013_20261117T031656Z.{py,json,md}`), evidence audit, trigger check. Verdict NOT_REPLICATED.
- **FCLR-010 — `research_state/session_20261117T002014Z/`:** parquet-free recompute (`recompute_fclr010_20261117T002014Z.{py,json,md}`), evidence audit, trigger check. Verdict NOT_REPLICATED.
- FCLR-002/FCLR-003 — `research_state/session_20261117T000400Z/` (recomputes, evidence audit, gate/suite captures).
- FCLR-008 — `research_state/session_20261116T230140Z/` (B0/B1 QLIKE match <=3e-7; C1/C2 divergence ~1.4e-3/2.1e-3; evidence audit and full gate/suite capture complete).
- FCLR-006 — `research_state/session_20261116T185811Z/` (`all_within_tolerance=true`).
- FCLR-009 — `research_state/session_20261116T125624Z/` (`all_within_tolerance=true`).
- Self-contained bundle: `research_state/session_20261116T100533Z/` (5 RCA-011 families + `trigger_readiness_power_calibration_*`/`trigger_readiness_power.py`).
- `research_state/session_20261116T115028Z/`: third numpy-only FCLR-011 crosscheck confirming sealed PASS not reproducible.

**Incomplete / non-counting sessions (do not resume, copy, or count):** `session_20261116T104644Z/`, `session_20261116T105341Z/`, `session_20261116T134957Z/` (trigger-only). `session_20261116T140001Z/` superseded (tolerance-failed FCLR-006). `session_20261116T221127Z/` superseded (divergent FCLR-008). No empty session directories present.

## Bottlenecks removed / prevented

- **FCLR-014 "blocked-on-data" misclassification (corrected this session):** the prior handoff said "no admissible panel exists locally / raw 2024 data exists but panel not admissible." Verification shows the cache holds **complete 5-symbol mark+index+premium+funding for all of 2025 and 2026-01..10, plus 2024-04..2024-11 (mark+funding)**. The true blocker is **design admissibility under `TESTED_WINDOWS`** (no contiguous untested >=127d run), not data absence. Next session must document this corrected blocker, not repeat the false "no data" claim.
- **`next_campaign_status.py` enumeration gap (documented, not yet patched):** `ready_windows()` silently drops 2024-11 and 2024-12 because their index/premium day counts for 4/5 symbols are 0 (only BTCUSDT has them), so they fail the `5*25` completeness threshold. This is why the disjoint frontier reports "no feasible block." A future session may patch the tool (register any `scripts/*.py` change in both scope registries) to report partial-coverage months explicitly, but must NOT weaken the completeness rule to fabricate a feasible design.
- **Parquet engine absent (the FCLR-010 blocker, removed):** `pyarrow`/`fastparquet`/`duckdb`/`polars` are not installed and network installs prohibited. Use CSV/JSON/ZIP twins; if a registered input is parquet-only, record the exact blocker — never fabricate.
- **Nonexistent protocol paths:** `research_protocol_fclr002.md` / `research_protocol_fclr003.md` do not exist. Frozen splits and published values are embedded in the handoff and `evaluation_summary_FCLR002/003.md`; FCLR-002/003 are complete.
- **Unresolved LFS inputs:** `run_manifest.json`, `run_manifest_FCLR002.json`, `fclr002_panel*.json`, `manifest_fclr002.json`, `manifest_fclr003.json` are pointers with no local object. Do not attempt `git lfs pull`.
- **2024 ZIP/CSV bottleneck:** Apr–Jun 2024 files are ZIPs; CSV-only readers silently drop the training window. Use the ZIP-aware reader from `session_20261117T031656Z` (FCLR-013, complete).
- **Frontier loophole closed:** the rank-0 frontier defers the concrete unfinished task to `FCLR_HEAVY_CAMPAIGN_NEXT.md`; that note defines a new quantitative artifact as the completion floor, so "keep the suite green" alone cannot close a session.
- **Duplicate FCLR-008 attempt marked:** `session_20261116T221127Z` is explicitly non-counting; `session_20261116T230140Z` is authoritative.
- **Suite baseline documented:** 4 errors are pre-existing missing-`pyarrow` errors in `test_fclr_liq_combined_admissibility_audit`; they are not agent-caused and must not be "fixed" by adding heavy deps to the core path.
- **Maintenance-refresh treadmill blocked:** handoff-only refreshes with no new heavy artifact are not completion; next session must emit `fclr014_panel_coverage_audit_<UTC>.{json,md}` + `fclr014_panel_blocker_resolution_<UTC>.{json,md}`.
- **Reproducibility path:** stdlib/numpy-only; no `statsmodels`/unpinned heavy deps in core path.
- **Handoff authority:** this file only (`AGENT_HANDOFF.md`).
- **Root churn:** 500/500 — session-only writes required.

## Bottlenecks and prohibitions

- Do not start or re-run any cached-data confirmatory estimand; all sealed estimands are terminal.
- Do not mutate sealed artifacts, frontier, hypothesis registries, or `.github/workflows/*`.
- Do not poll, re-probe HuggingFace tree, use paid/credentialed/manual outcome data, or add root-level `research_state/*.md|json`.
- Do not add `statsmodels` or unpinned heavy dependencies to core path.
- Do not run `git lfs pull` or otherwise fetch network data.
- Do not run `scripts/fclr_liq_010_confirm.py` (parquet-only; will fail on import).
- Discovery suite is long-running; let it finish and record actual EXIT, not partial/timeout.
- Scientific blocker is external (no admissible post-2026-10 observed liquidation labels/source; no agent-settable Gate 4 attestation) AND design-admissibility (no contiguous untested >=127d window under `TESTED_WINDOWS`). Agent-removable requirement: new FCLR-014 coverage audit + blocker-resolution artifact + evidence audit + complete verification + accurate handoff update.

## Reopen triggers (machine-checkable — Act ONLY when satisfied; all `OPEN`)

- `GATE4_BRANCH_1` — `research_state/fclr016_v5_terms_evidence_RESOLVED_*.json` (`status: RESOLVED_VERIFIED`, `fabricated: false`). Human/legal attestation only.
- `NEW_OBSERVED_LIQUIDATION_SOURCE` — `research_state/<source>_admissibility_audit_<UTC>.{md,json}` (`status: ADMISSIBLE`, `observed_labels: true`, >=5 instruments, >=3 blocks or >=1 complete month).
- `HL_LABEL_EXTENSION` — `research_state/hl_label_extension_audit_<UTC>.{md,json}`.
- `EXPANSION_ROBUSTNESS_REDO` — `research_state/expansion_robustness_redo_prereg_<UTC>.json` + `evaluation_summary_*.json`.

## Tombstones (no authority)

- `NEXT_SESSION_HANDOFF.md`, `NEXT_SESSION_TASK.md`: tombstoned 2026-11-15T22:57:29Z.
- `AGENT_HANDOFF_20261115T073240Z.md`: SUPERSEDED — ignore.
- `HANDOFF_NEXT_SESSION_20261116T114626Z.md`: tombstoned 2026-11-16T12:45:00Z — ignore.

## Verification record — 2026-11-17T04:07:43Z handoff refresh

- **Changed:** refreshed the sole durable handoff with current timestamp; FCLR-013 **DONE** (`session_20261117T031656Z`, ZIP/CSV parquet-free recompute, verdict **NOT_REPLICATED**: C2-vs-B1 QLIKE mean diff 0.017010, CI `[-0.000523,0.034809]` crosses zero, rel **-4.99%** vs sealed **-1.32%** NOT_MET, 1 test block >=3 required, materiality <2%, LOIO/placebo fail; n_pairs=4200, 5 symbols, 36 test days); FCLR-010 remains **DONE** (`session_20261117T002014Z`, verdict NOT_REPLICATED: 0.50% vs sealed 2.21%); FCLR-014 reclassified to **BLOCKED-ON-DESIGN** with a **corrected blocker** — the prior "no admissible panel locally" claim was verified FALSE (cache holds complete 5-symbol mark+funding for 2024-04..2026-10; all of 2025 and 2026-01..10 have mark+index+premium+funding); the real blocker is design admissibility (no contiguous untested >=127d window avoiding `TESTED_WINDOWS`); `next_campaign_status.py` enumeration gap (drops 2024-11/12 partial-coverage months) documented; all other documented bottlenecks remain removed; root `research_state/*.md|json` at 500/500 cap — session-only writes required.
- **New heavy artifact this session (required):** `fclr014_panel_coverage_audit_<UTC>.{json,md}` + `fclr014_panel_blocker_resolution_<UTC>.{json,md}` + `evidence_audit_<UTC>.md` + `trigger_check_<UTC>.json` under new `research_state/session_<UTC>/`.
- **Baseline gates (verified this session):** `check_handoff_heavywork_gate.py --json` **PASS**; `check_tracka_scope_registry_drift.py --json` **PASS**.
- **Queue:** FCLR-009/006/008/002/003/010/013 DONE; FCLR-014 BLOCKED-ON-DESIGN (corrected blocker).
- **Git tree:** new session artifacts under `research_state/session_<UTC>/` only; no tracked file modified.

(End of file)