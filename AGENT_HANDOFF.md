# AGENT HANDOFF — 2026-11-17T00:04:00Z (sole durable handoff)

## INITIAL TASK MESSAGE FOR NEXT AGENTIC WORK SESSION (do this first)

**Priority 0 — repository and rank-0 state.**
- Repository: `Funding-conditioned-volatility-and-liquidation-risk` (funding-conditioned volatility and liquidation risk).
- Program: `CLOSED_TERMINAL` — final structural closure `research_state/fclr_final_structural_closure_20261116T114626.{md,json}`; verdict `NO_CLAIM_WORTHY_RESULT_PROMOTABLE; ALL_P1_P2_P3_SEALED`; no feasible 3-block pre-registered design in any domain.
- Rank-0: `FCLR-BOUNDED-TRIGGER-ONLY-20261115T220000Z` (`TRIGGER_ONLY` / `BOUNDED_TRIGGER_ONLY`, `next_action_heavy=null`). All cached-data confirmatory estimands are terminal.
- Consequence: **do not start or re-run any cached-data confirmatory estimand.** The only agent-removable heavy work is the independent reproducibility audit below. "Keep the suite green" is a floor, not completion.

**MANDATORY HEAVY WORK (non-skippable): FCLR-010 independent recompute, then FCLR-013/FCLR-014.**
A trigger-check-only session, tests/gates-only session, copied bundle, re-audit of static bundles, or "no trigger → stop cleanly" is **NOT** completion. Completion requires ALL of:
1. new `research_state/session_<UTC>/`;
2. `recompute_fclr010_<UTC>.{py,json,md}` with independent Track-A liquidation-confirm results (plus FCLR-013/FCLR-014 if inputs and time permit);
3. `evidence_audit_<UTC>.md`;
4. gate captures + full-suite capture under the session dir;
5. this handoff updated with actual results and the queue ticked.

**Read first (in order):**
1. `research_state/resume_trigger_registry.json`
2. `research_state/ironflow_monitor_state.json`
3. `research_state/FCLR_HEAVY_CAMPAIGN_NEXT.md`
4. `research_state/session_20261117T000400Z/evidence_audit_20261117T000400Z.md` + `recompute_fclr002_20261117T000400Z.md` + `recompute_fclr003_20261117T000400Z.md` (latest completed heavy evidence)
5. `research_state/evaluation_summary_FCLR010.md` if present, otherwise the FCLR-010 panel metadata and `RESEARCH_PROMPT.md` Track-A contract.

**Completed work — do not repeat:**
- FCLR-002 — `session_20261117T000400Z`; independent recompute completed. B0/B1/C1/C2 QLIKE diverged beyond the 1e-6 tolerance, but C2 vs B1 remains directionally positive (`8.60%` recomputed relative reduction, CI `[-0.093389,-0.005759]`), and the frozen 70-day / 2-block test still makes the overall gate **NOT_MET**.
- FCLR-003 — `session_20261117T000400Z`; independent recompute completed. B0/B1 match, C1/C2 diverge beyond tolerance; C2 vs B1 is worse (`-11.85%` relative change, CI `[0.004045,0.097614]`), corroborating **NOT_MET**.
- FCLR-009 — `session_20261116T125624Z`; `all_within_tolerance=true`.
- FCLR-006 — `session_20261116T185811Z`; `all_within_tolerance=true`.
- FCLR-008 — `session_20261116T230140Z`; B0/B1 within tolerance, C1/C2 divergence documented, qualitative **NOT_MET** corroborated.
- FCLR-RCA-011 — complete bundle `session_20261116T100533Z`.

**Next target — FCLR-010 (Track A liquidation confirm):**
- Primary input: `research_state/fclr_liq_010_confirm_panel_20261113T065953Z.parquet`.
- Recompute the terminal Track-A liquidation-confirm headline independently from the local panel. Do not mutate the sealed panel. If the parquet cannot be read because `pyarrow`/`fastparquet` is unavailable, record the exact local dependency/path blocker and use only a documented local fallback; do not fabricate values and do not add heavy dependencies to the core path.
- The Track-A design is underpowered for the 2% floor (published n=593, MDE about 8.88%; about 11,689 paired observations are needed for a 2% MDE). Preserve that limitation in the verdict.
- If FCLR-010 completes cleanly, proceed to FCLR-013/FCLR-014 only when their registered panels and coverage audits are locally present and not unresolved LFS pointers.

**Blocked-path warning (do not waste a session here):**
- `research_state/research_protocol_fclr002.md` and `research_state/research_protocol_fclr003.md` **do not exist** — do not block on them.
- `research_state/run_manifest.json`, `research_state/run_manifest_FCLR002.json`, `research_state/data_cache/fclr002_panel*.json`, `research_state/data_cache/manifest_fclr002.json`, and `research_state/data_cache/manifest_fclr003.json` are **unresolved Git-LFS pointers with no local object**. Do NOT run `git lfs pull` (network is prohibited). FCLR-002/003 have already been computed from local raw data; do not repeat them.
- **2024 cache format warning:** Apr-Jun 2024 mark/premium/index files under `research_state/data_cache/<SYM>_2024_04..06/` are ZIP archives; Jan-Mar and Jul-Nov are CSVs. A CSV-only glob silently drops the Apr-Jun training window and produces false zero-row/`None` results. Use the ZIP-aware reader in `session_20261117T000400Z/recompute_fclr002_003_20261117T000400Z.py`.
- `scripts/build_fclr002_panel_local.py` reads `run_manifest.json` and defaults to the tracked LFS pointer `research_state/data_cache/fclr002_panel_local.json` — do not run it as-is.
- Raw 2024 CSVs/ZIPs are present for all five symbols under `research_state/data_cache/<SYM>_2024_01..12/` (markPriceKlines, fundingRate, indexPriceKlines). No network is needed.

**Execute in order (do not skip to "stop cleanly"):**
1. **Create `research_state/session_<UTC>/`** (actual UTC). `research_state/` root is **500/500** (fail-closed cap); put ALL new artifacts inside the session subdirectory only.
2. **Check triggers exactly once (no network, no polling).** Read files 1–2. Record timestamp, each trigger status, `data_through`, and post-2026-10 month classifications in the session dir. Current state: all four `OPEN`; Ironflow `data_through=2026-10`; 2026-11/2026-12/2027-01 `CONFIRMED_ABSENT`. Do not re-probe HuggingFace or repeat later.
3. **FCLR-010 independent recompute (primary).** Read the local Track-A panel directly, independently reconstruct the registered estimand(s), and write `recompute_fclr010_<UTC>.{py,json,md}` under the session dir. Do not run the canonical evaluator against a sealed summary, do not read `run_manifest.json`, and never mutate sealed artifacts.
4. **FCLR-013/FCLR-014 (only if FCLR-010 completes cleanly and local inputs are valid).** Same independence rule; write `recompute_fclr013_<UTC>.{py,json,md}` and/or `recompute_fclr014_<UTC>.{py,json,md}`. Do not repeat FCLR-002/003/006/008/009.
5. **Audit carried-forward evidence.** Confirm `session_20261116T100533Z/` (5 RCA-011 families), `session_20261116T125624Z/` (FCLR-009), `session_20261116T185811Z/` (FCLR-006), `session_20261116T230140Z/` (FCLR-008), and `session_20261117T000400Z/` (FCLR-002/003) are present. Write a concise evidence-audit artifact in the session dir. Do not rerun FCLR-RCA-011/FCLR-009/FCLR-006/FCLR-008/FCLR-002/FCLR-003.
6. **Run and capture every required gate under the new session dir:**
   - `python3 scripts/check_handoff_heavywork_gate.py --json` — PASS (complete bundle + new session audit + fresh quant artifact, root <= 500).
   - `python3 scripts/check_tracka_scope_registry_drift.py --json` — PASS (register any new script in both scope registries).
   - `python3 -m unittest tests.test_active_campaign_gate tests.test_tracka_hardening_117 tests.test_tracka_hardening_118 tests.test_tracka_hardening_143` — all pass (52 tests).
   - `python3 -m unittest discover -q` — run to completion; record exact test count, skip count, error list, and final EXIT. **Baseline:** 1340 tests, 4 pre-existing errors (all `tests.test_fclr_liq_combined_admissibility_audit`, caused by missing `pyarrow`; environmental, not agent-caused), 18 skipped, EXIT 1. Success = identical set with no new failures/errors. Never treat timeout/monitor cap as green. Revert any timestamp-only side effect to tracked files.
7. **Update only this handoff** after steps 3–6: replace timestamp/verification with actual results, tick FCLR-010 (and FCLR-013/014 if done), keep sole-handoff contract, bundle refs, blockers intact. Do not create another handoff file.

**Trigger-gated science is the only scientific advance — but must be pre-powered.** If no trigger is satisfied, do not advance or re-run a confirmatory estimand; required holding action is the FCLR-010 reproducibility artifact + evidence audit + complete verification + accurate handoff update. If a trigger is satisfied, follow `RESEARCH_PROMPT.md` §16 admissibility/source audit first, freeze a pre-sized prereg before inspecting outcomes (use `session_20261116T035833Z/prereg_template_trigger_gated_20261116T035833Z.json` and power floors in `session_20261116T100533Z/trigger_readiness_power_calibration_20261116T100533Z.md`: Gate4/TrackC `paired_n>=23224`, TrackA/expansion `paired_n>=11689`, >=3 blocks, 7d purge/embargo), require a materially different estimand, execute, register any new scripts in both scope registries, run all gates, and update frontier/hypothesis registries with an honest verdict.

## Reproducibility-audit queue (non-skippable; do in order)

1. ~~FCLR-009~~ — DONE (`session_20261116T125624Z`; `all_within_tolerance=true`).
2. ~~FCLR-006~~ — DONE (`session_20261116T185811Z`; `all_within_tolerance=true`; supersedes tolerance-failed `session_20261116T140001Z`).
3. ~~FCLR-008~~ — DONE (`session_20261116T230140Z`; B0/B1 within tolerance; C1/C2 divergence documented; qualitative NOT_MET corroborated). `session_20261116T221127Z` is an earlier divergent FCLR-008 attempt with no evidence audit — **superseded, do not count/resume**.
4. ~~FCLR-002~~ — DONE (`session_20261117T000400Z`; exact values diverged beyond tolerance; qualitative C2-vs-B1 improvement corroborated; gate NOT_MET).
5. ~~FCLR-003~~ — DONE (`session_20261117T000400Z`; B0/B1 matched; C1/C2 diverged; NOT_MET corroborated).
6. **FCLR-010 (Track A liquidation confirm): independent recompute from `fclr_liq_010_confirm_panel_20261113T065953Z.parquet`, `recompute_fclr010_<UTC>.{json,md}` — CURRENT TARGET (PRIMARY).**
7. **FCLR-013 / FCLR-014 (2026 Q3 / 2025 H1 panels): independent recompute — NEXT.**

A session that completes an item must (a) create `research_state/session_<UTC>/`, (b) emit a new quantitative artifact named per queue, (c) write evidence audit, (d) run all gates + full discovery suite to completion with recorded EXIT, (e) update this handoff and tick the queue item.

## Heavy-work evidence on disk (authoritative; do not redo)

- Self-contained bundle: `research_state/session_20261116T100533Z/` (carried forward from `session_20261116T035833Z/`): 5 RCA-011 families + `trigger_readiness_power_calibration_*`/`trigger_readiness_power.py`.
- `research_state/session_20261116T125624Z/`: FCLR-009 reproduced `all_within_tolerance=true`.
- `research_state/session_20261116T185811Z/`: FCLR-006 reproduced `all_within_tolerance=true`.
- `research_state/session_20261116T115028Z/`: third numpy-only FCLR-011 crosscheck confirming sealed PASS not reproducible.
- `research_state/session_20261116T230140Z/`: FCLR-008 independent recompute (B0/B1 QLIKE match <=3e-7; C1/C2 divergence ~1.4e-3/2.1e-3; evidence audit and full gate/suite capture complete).
- `research_state/session_20261116T221127Z/`: **superseded** earlier FCLR-008 attempt (no evidence audit; divergent C1/C2) — evidence only, not a completed queue item.
- `research_state/session_20261117T000400Z/`: FCLR-002 and FCLR-003 independent recomputes, evidence audit, trigger check, gate/suite captures. Exact values diverge beyond tolerance for C1/C2; qualitative NOT_MET verdicts are corroborated.

**Incomplete / non-counting sessions (do not resume, copy, or count):** `session_20261116T104644Z/`, `session_20261116T105341Z/`, `session_20261116T134957Z/` (trigger-only). `session_20261116T140001Z/` superseded (tolerance-failed FCLR-006). No empty session directories present.

## Bottlenecks removed / prevented

- **Nonexistent protocol paths removed:** the old handoff pointed at `research_protocol_fclr002.md` / `research_protocol_fclr003.md`, which do not exist. This handoff embeds the frozen splits and published values; FCLR-002/003 are now complete.
- **Unresolved LFS inputs documented:** `run_manifest.json`, `run_manifest_FCLR002.json`, `fclr002_panel*.json`, `manifest_fclr002.json`, `manifest_fclr003.json` are pointers with no local object. Do not attempt `git lfs pull`.
- **2024 ZIP/CSV bottleneck documented:** Apr-Jun files are ZIP archives; CSV-only readers silently drop the training window. Use the ZIP-aware reader from `session_20261117T000400Z`.
- **Stale campaign/handoff mismatch removed:** `research_state/FCLR_HEAVY_CAMPAIGN_NEXT.md` now names FCLR-010 as the current target (FCLR-002/003/008/006/009 done), matching this handoff.
- **Frontier loophole closed:** the rank-0 frontier defers the concrete unfinished task to `FCLR_HEAVY_CAMPAIGN_NEXT.md`; that note defines a new quantitative artifact as the completion floor, so "keep the suite green" alone cannot close a session.
- **Duplicate FCLR-008 attempt marked:** `session_20261116T221127Z` is explicitly non-counting; `session_20261116T230140Z` is authoritative.
- **Suite baseline documented:** 4 errors are pre-existing missing-`pyarrow` errors in `test_fclr_liq_combined_admissibility_audit`; they are not agent-caused and must not be "fixed" by adding heavy deps to the core path.
- **Empty/stale session clutter removed:** none present; incomplete trigger-only sessions must not be resumed.
- **Maintenance-refresh treadmill blocked:** handoff-only refreshes with no new heavy artifact are not completion; next session must emit `recompute_fclr010_<UTC>.{json,md}`.
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

## Verification record — 2026-11-17T00:04:00Z handoff refresh

- **Changed:** refreshed the sole durable handoff; aligned `research_state/FCLR_HEAVY_CAMPAIGN_NEXT.md` (FCLR-010 current, FCLR-002/003 done); recorded the new FCLR-002/003 quantitative artifacts; documented the Apr-Jun ZIP/CSV cache bottleneck and exact divergences; ticked the reproducibility queue.
- **Baseline gates:** `check_handoff_heavywork_gate.py --json` **PASS** (`latest_session=session_20261116T230140Z` at capture, `heavy_session=session_20261116T100533Z`, root 500/500). `check_tracka_scope_registry_drift.py --json` **PASS** (196/196 scripts).
- **Targeted suite:** `test_active_campaign_gate`, `test_tracka_hardening_117/118/143` — **52 tests OK, EXIT 0**.
- **Full `unittest discover -q`:** **1340 tests, 4 pre-existing pyarrow errors, 18 skipped, EXIT 1** — recorded per mandate; no new failures introduced.
- **Queue:** FCLR-009/006/008/002/003 DONE; FCLR-010 CURRENT; FCLR-013/014 NEXT.
- **Git tree:** new session artifacts under `research_state/session_20261117T000400Z/`; timestamp-only `research_state/ironflow_fastpath_cache.json` change reverted.

(End of file)