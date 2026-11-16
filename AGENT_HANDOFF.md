# AGENT HANDOFF — 2026-11-16T23:39:00Z (sole durable handoff)

## INITIAL TASK MESSAGE FOR NEXT AGENTIC WORK SESSION (do this first)

**Priority 0 — repository and rank-0 state.**
- Repository: `Funding-conditioned-volatility-and-liquidation-risk` (funding-conditioned volatility and liquidation risk).
- Program: `CLOSED_TERMINAL` — final structural closure `research_state/fclr_final_structural_closure_20261116T114626.{md,json}`; verdict `NO_CLAIM_WORTHY_RESULT_PROMOTABLE; ALL_P1_P2_P3_SEALED`; no feasible 3-block pre-registered design in any domain.
- Rank-0: `FCLR-BOUNDED-TRIGGER-ONLY-20261115T220000Z` (`TRIGGER_ONLY` / `BOUNDED_TRIGGER_ONLY`, `next_action_heavy=null`). All cached-data confirmatory estimands are terminal.
- Consequence: **do not start or re-run any cached-data confirmatory estimand.** The only agent-removable heavy work is the independent reproducibility audit below. "Keep the suite green" is a floor, not completion.

**MANDATORY HEAVY WORK (non-skippable): FCLR-002 independent recompute, then FCLR-003.**
A trigger-check-only session, tests/gates-only session, copied bundle, re-audit of static bundles, or "no trigger → stop cleanly" is **NOT** completion. Completion requires ALL of:
1. new `research_state/session_<UTC>/`;
2. `recompute_fclr002_<UTC>.{py,json,md}` with independent QLIKE/OLS results (plus `recompute_fclr003_<UTC>.{py,json,md}` if time);
3. `evidence_audit_<UTC>.md`;
4. gate captures + full-suite capture under the session dir;
5. this handoff updated with actual results and the queue ticked.

**Read first (in order):**
1. `research_state/resume_trigger_registry.json`
2. `research_state/ironflow_monitor_state.json`
3. `research_state/FCLR_HEAVY_CAMPAIGN_NEXT.md`
4. `research_state/session_20261116T230140Z/evidence_audit_20261116T230140Z.md` + `recompute_fclr008_20261116T230140Z.md` (latest completed heavy evidence)
5. `research_state/evaluation_summary_FCLR002.md`, `research_state/evaluation_summary_FCLR003.md`, `research_state/evaluation_summary_FCLR002_REPRO.md`

**Blocked-path warning (do not waste a session here):**
- `research_state/research_protocol_fclr002.md` and `research_state/research_protocol_fclr003.md` **do not exist** — do not block on them.
- `research_state/run_manifest.json`, `research_state/run_manifest_FCLR002.json`, `research_state/data_cache/fclr002_panel*.json`, `research_state/data_cache/manifest_fclr002.json`, and `research_state/data_cache/manifest_fclr003.json` are **unresolved Git-LFS pointers with no local object**. Do NOT run `git lfs pull` (network is prohibited). Hardcode the frozen splits below and rebuild from raw CSVs.
- `scripts/build_fclr002_panel_local.py` reads `run_manifest.json` for splits and defaults its output to the tracked LFS pointer `research_state/data_cache/fclr002_panel_local.json` — do not run it as-is. Use a session-local copy with hardcoded splits and `--out research_state/session_<UTC>/...`, or implement the feature construction directly.
- Raw 2024 CSVs are present for all five symbols under `research_state/data_cache/<SYM>_2024_01..12/` (markPriceKlines, fundingRate, indexPriceKlines). No network needed.

### FCLR-002 — frozen spec and published values (audit target)

- Universe: BTCUSDT, ETHUSDT, BNBUSDT, SOLUSDT, XRPUSDT. Data: 2024-01..2024-09.
- Frozen splits (7d embargo):
  - train `2024-04-01T00:00:00Z..2024-06-08T23:00:00Z`
  - val `2024-06-16T00:00:00Z..2024-07-15T23:00:00Z`
  - test `2024-07-23T00:00:00Z..2024-09-30T23:00:00Z`
- Models: B0 persistence; B1 HAR-style on log RV1h/RV24h/RV168h; C1 = B1 + signed funding + past-only 90d |funding| percentile; C2 = C1 + premium + EMA24 distance. OLS on log(RV+1e-12), intercept + 1e-12 ridge. QLIKE = y/yhat - log(y/yhat) - 1.
- Published test QLIKE: B0 `0.543471` (n=8280); B1 `0.487438` (n=8274); C1 `0.487455` (n=8274); C2 `0.442223` (n=8274).
- Published contrasts: C2_vs_B1 `-0.045215` CI `[-0.097648,-0.008788]` rel `9.28%` n=8274; C1_vs_B1 `0.000017` CI `[-0.005982,0.006047]` rel `-0.00%`; C2_vs_C1 `-0.045232` CI `[-0.098089,-0.009173]` rel `9.28%`.
- Gate: C2 vs B1 >=2% PASS; test = 70 days = 2 blocks -> >=3 NOT_MET; overall **NOT_MET**.

### FCLR-003 — frozen spec and published values (next audit target)

- Data: 2024-01..2024-12.
- Frozen splits (7d embargo):
  - train `2024-04-01T00:00:00Z..2024-07-23T23:00:00Z`
  - val `2024-07-31T00:00:00Z..2024-09-24T23:00:00Z`
  - test `2024-10-02T00:00:00Z..2024-12-31T23:00:00Z`
- Published test QLIKE: B0 `0.486931` (n=10800); B1 `0.400689` (n=10796); C1 `0.389589` (n=10796); C2 `0.444702` (n=10796).
- Published contrasts: C2_vs_B1 `0.044013` CI `[0.001487,0.093225]` rel `-10.98%`; C1_vs_B1 `-0.011100` CI `[-0.016972,-0.005925]` rel `2.77%`; C2_vs_C1 `0.055113` CI `[0.009734,0.107156]` rel `-14.15%`.
- Gate: C2 vs B1 NOT_MET; 3 blocks PASS; overall **NOT_MET**.

**Tolerances:** QLIKE abs <= `1e-6`; mean diff abs <= `1e-6`; relative reduction <= `0.01` percentage points; n must match where deterministic. A tolerance failure is a valid finding — document the divergence, do not tune to match.

**Execute in order (do not skip to "stop cleanly"):**
1. **Create `research_state/session_<UTC>/`** (actual UTC). `research_state/` root is **500/500** (fail-closed cap); put ALL new artifacts inside the session subdirectory only.
2. **Check triggers exactly once (no network, no polling).** Read files 1–2. Record timestamp, each trigger status, `data_through`, and post-2026-10 month classifications in the session dir. Current state: all four `OPEN`; Ironflow `data_through=2026-10`; 2026-11/2026-12/2027-01 `CONFIRMED_ABSENT`. Do not re-probe HuggingFace or repeat later.
3. **FCLR-002 independent recompute (primary).** Hardcode the frozen splits above; do not read `run_manifest.json` or run canonical `scripts/run_evaluation.py` against the tracked summary. You may import pure feature helpers from `scripts/run_evaluation.py` (mark/funding loaders, feature construction) but implement split assignment, OLS, QLIKE, and block bootstrap independently and write every output under the session dir. Never mutate sealed artifacts. Emit `recompute_fclr002_<UTC>.{py,json,md}`.
4. **FCLR-003 (do if FCLR-002 completes cleanly and time remains).** Same method with the FCLR-003 splits/values. Emit `recompute_fclr003_<UTC>.{py,json,md}`.
5. **Audit carried-forward evidence.** Confirm `session_20261116T100533Z/` (5 RCA-011 families), `session_20261116T125624Z/` (FCLR-009), `session_20261116T185811Z/` (FCLR-006), and `session_20261116T230140Z/` (FCLR-008) are present. Write a concise evidence-audit artifact in the session dir. Do not rerun FCLR-RCA-011/FCLR-009/FCLR-006/FCLR-008.
6. **Run and capture every required gate under the new session dir:**
   - `python3 scripts/check_handoff_heavywork_gate.py --json` — PASS (complete bundle + new session audit + fresh quant artifact, root <= 500).
   - `python3 scripts/check_tracka_scope_registry_drift.py --json` — PASS (register any new script in both scope registries).
   - `python3 -m unittest tests.test_active_campaign_gate tests.test_tracka_hardening_117 tests.test_tracka_hardening_118 tests.test_tracka_hardening_143` — all pass (52 tests).
   - `python3 -m unittest discover -q` — run to completion; record exact test count, skip count, error list, and final EXIT. **Baseline:** 1340 tests, 4 pre-existing errors (all `tests.test_fclr_liq_combined_admissibility_audit`, caused by missing `pyarrow`; environmental, not agent-caused), 18 skipped, EXIT 1. Success = identical set with no new failures/errors. Never treat timeout/monitor cap as green. Revert any timestamp-only side effect to tracked files.
7. **Update only this handoff** after steps 3–6: replace timestamp/verification with actual results, tick FCLR-002 (and FCLR-003 if done), keep sole-handoff contract, bundle refs, blockers intact. Do not create another handoff file.

**Trigger-gated science is the only scientific advance — but must be pre-powered.** If no trigger is satisfied, do not advance or re-run a confirmatory estimand; required holding action is the FCLR-002/003 reproducibility artifact + evidence audit + complete verification + accurate handoff update. If a trigger is satisfied, follow `RESEARCH_PROMPT.md` §16 admissibility/source audit first, freeze a pre-sized prereg before inspecting outcomes (use `session_20261116T035833Z/prereg_template_trigger_gated_20261116T035833Z.json` and power floors in `session_20261116T100533Z/trigger_readiness_power_calibration_20261116T100533Z.md`: Gate4/TrackC `paired_n>=23224`, TrackA/expansion `paired_n>=11689`, >=3 blocks, 7d purge/embargo), require a materially different estimand, execute, register any new scripts in both scope registries, run all gates, and update frontier/hypothesis registries with an honest verdict.

## Reproducibility-audit queue (non-skippable; do in order)

1. ~~FCLR-009~~ — DONE (`session_20261116T125624Z`; `all_within_tolerance=true`).
2. ~~FCLR-006~~ — DONE (`session_20261116T185811Z`; `all_within_tolerance=true`; supersedes tolerance-failed `session_20261116T140001Z`).
3. ~~FCLR-008~~ — DONE (`session_20261116T230140Z`; B0/B1 within tolerance; C1/C2 divergence ~1.4e-3/2.1e-3 QLIKE documented; qualitative NOT_MET corroborated). `session_20261116T221127Z` is an earlier divergent FCLR-008 attempt with no evidence audit — **superseded, do not count/resume**.
4. **FCLR-002 (frozen 2024 panel): independent recompute, `recompute_fclr002_<UTC>.{json,md}` — CURRENT TARGET (PRIMARY).**
5. **FCLR-003 (frozen 2024 panel): independent recompute, `recompute_fclr003_<UTC>.{json,md}` — NEXT.**
6. FCLR-010 (Track A liquidation confirm): independent recompute from `fclr_liq_010_confirm_panel_20261113T065953Z.parquet`, `recompute_fclr010_<UTC>.{json,md}`.
7. FCLR-013 / FCLR-014 (2026 Q3 / 2025 H1 panels): independent recompute.

A session that completes an item must (a) create `research_state/session_<UTC>/`, (b) emit a new quantitative artifact named per queue, (c) write evidence audit, (d) run all gates + full discovery suite to completion with recorded EXIT, (e) update this handoff and tick the queue item.

## Heavy-work evidence on disk (authoritative; do not redo)

- Self-contained bundle: `research_state/session_20261116T100533Z/` (carried forward from `session_20261116T035833Z/`): 5 RCA-011 families + `trigger_readiness_power_calibration_*`/`trigger_readiness_power.py`.
- `research_state/session_20261116T125624Z/`: FCLR-009 reproduced `all_within_tolerance=true`.
- `research_state/session_20261116T185811Z/`: FCLR-006 reproduced `all_within_tolerance=true`.
- `research_state/session_20261116T115028Z/`: third numpy-only FCLR-011 crosscheck confirming sealed PASS not reproducible.
- `research_state/session_20261116T230140Z/`: FCLR-008 independent recompute (B0/B1 QLIKE match <=3e-7; C1/C2 divergence ~1.4e-3/2.1e-3; evidence audit and full gate/suite capture complete).
- `research_state/session_20261116T221127Z/`: **superseded** earlier FCLR-008 attempt (no evidence audit; divergent C1/C2) — evidence only, not a completed queue item.

**Incomplete / non-counting sessions (do not resume, copy, or count):** `session_20261116T104644Z/`, `session_20261116T105341Z/`, `session_20261116T134957Z/` (trigger-only). `session_20261116T140001Z/` superseded (tolerance-failed FCLR-006). No empty session directories present.

## Bottlenecks removed / prevented

- **Nonexistent protocol paths removed:** the old handoff pointed at `research_protocol_fclr002.md` / `research_protocol_fclr003.md`, which do not exist. This handoff embeds the frozen splits and published values from `evaluation_summary_FCLR002.md` / `evaluation_summary_FCLR003.md`.
- **Unresolved LFS inputs documented:** `run_manifest.json`, `run_manifest_FCLR002.json`, `fclr002_panel*.json`, `manifest_fclr002.json`, `manifest_fclr003.json` are pointers with no local object; the next session must hardcode splits and rebuild from raw 2024 CSVs. Do not attempt `git lfs pull`.
- **Stale campaign/handoff mismatch removed:** `research_state/FCLR_HEAVY_CAMPAIGN_NEXT.md` now names FCLR-002 as the current target (FCLR-008/006/009 done), matching this handoff.
- **Frontier loophole closed:** the rank-0 frontier defers the concrete unfinished task to `FCLR_HEAVY_CAMPAIGN_NEXT.md`; that note now defines a new quantitative artifact as the completion floor, so "keep the suite green" alone cannot close a session.
- **Duplicate FCLR-008 attempt marked:** `session_20261116T221127Z` is explicitly non-counting; `session_20261116T230140Z` is authoritative.
- **Suite baseline documented:** 4 errors are pre-existing missing-`pyarrow` errors in `test_fclr_liq_combined_admissibility_audit`; they are not agent-caused and must not be "fixed" by adding heavy deps to the core path.
- **Empty/stale session clutter removed:** none present; incomplete trigger-only sessions must not be resumed.
- **Maintenance-refresh treadmill blocked:** handoff-only refreshes with no new heavy artifact are not completion; next session must emit `recompute_fclr002_<UTC>.{json,md}`.
- **Reproducibility path:** stdlib/numpy-only; no `statsmodels`/unpinned heavy deps in core path.
- **Handoff authority:** this file only (`AGENT_HANDOFF.md`).
- **Root churn:** 500/500 — session-only writes required.

## Bottlenecks and prohibitions

- Do not start or re-run any cached-data confirmatory estimand; all terminal.
- Do not mutate sealed artifacts, frontier, hypothesis registries, or `.github/workflows/*`.
- Do not poll, re-probe HuggingFace tree, use paid/credentialed/manual outcome data, or add root-level `research_state/*.md|json`.
- Do not add `statsmodels` or unpinned heavy dependencies to core path.
- Do not run `git lfs pull` or otherwise fetch network data.
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

## Verification record — 2026-11-16T23:39:00Z handoff refresh (no heavy artifact produced by this refresh)

- **Changed:** refreshed the sole durable handoff; aligned `research_state/FCLR_HEAVY_CAMPAIGN_NEXT.md` (FCLR-002 current, FCLR-008/006/009 done); embedded FCLR-002/003 frozen splits, published values, tolerances, and exact data paths; documented unresolved LFS pointers and the missing `research_protocol_fclr002/003.md`; marked `session_20261116T221127Z` superseded.
- **Baseline gates:** `check_handoff_heavywork_gate.py --json` **PASS** (`latest_session=session_20261116T230140Z`, `heavy_session=session_20261116T100533Z`, root 500/500). `check_tracka_scope_registry_drift.py --json` **PASS** (196/196 scripts).
- **Data-path smoke test:** `scripts/run_evaluation.py` imports under `FCLR_EXPERIMENT=FCLR-002` and `FCLR-003`. FCLR-002 `load_mark_series('BTCUSDT', 2024-04-01..2024-09-30)` returns 4392 rows and funding returns 642; FCLR-003 full-2024 mark returns 8784 rows and funding returns 918 — both raw caches are usable without any LFS fetch.
- **Targeted suite:** `test_active_campaign_gate`, `test_tracka_hardening_117/118/143` — **52 tests OK, EXIT 0**.
- **Full `unittest discover -q`:** **1340 tests, 4 pre-existing pyarrow errors, 18 skipped, EXIT 1** — recorded per mandate; no new failures introduced by this refresh.
- **Queue:** FCLR-009/006/008 DONE; FCLR-002 CURRENT; FCLR-003 NEXT.
- **Git tree:** only this handoff and `research_state/FCLR_HEAVY_CAMPAIGN_NEXT.md` are modified by this refresh; no other uncommitted changes.

(End of file)