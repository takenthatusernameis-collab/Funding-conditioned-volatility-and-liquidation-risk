# FCLR Focus Campaign — `FCLR-REPRO-AUDIT-03` — current as of 2026-11-17T00:04:00Z

**Frontier rank 0:** `FCLR-BOUNDED-TRIGGER-ONLY-20261115T220000Z` (`TRIGGER_ONLY` / `BOUNDED_TRIGGER_ONLY`, `all_terminal=true`, `next_action_heavy=null`).
**Sole handoff:** `AGENT_HANDOFF.md` (refreshed 2026-11-17T00:04:00Z). This file is the detailed campaign note referenced by the frontier and the handoff.
**Governing rules:** `RESEARCH_PROMPT.md`. Never re-run concluded estimands, re-score sealed results, fabricate data, edit `.github/workflows/*`, poll, re-probe the HuggingFace tree, use paid/credentialed/manual outcome data, or run `git lfs pull`.
**Artifact rule:** write every new artifact to a new `research_state/session_<UTC>/`. The `research_state/` root is at 500/500 md/json; adding root files breaks the enforced churn cap.

## Current target (updated 2026-11-17T00:04:00Z)

**Primary heavy artifact: FCLR-010 independent recompute** from `research_state/fclr_liq_010_confirm_panel_20261113T065953Z.parquet`, then **FCLR-013/FCLR-014** independent recomputes if their cached panels are available.

Completed and NOT to be repeated:
- FCLR-002 — `session_20261117T000400Z` (`recompute_fclr002_20261117T000400Z.{json,md}`; exact values diverged beyond tolerance, qualitative C2-vs-B1 improvement corroborated; gate remains NOT_MET).
- FCLR-003 — `session_20261117T000400Z` (`recompute_fclr003_20261117T000400Z.{json,md}`; B0/B1 matched, C1/C2 diverged beyond tolerance; NOT_MET corroborated).
- FCLR-009 — `session_20261116T125624Z` (`all_within_tolerance=true`).
- FCLR-006 — `session_20261116T185811Z` (`all_within_tolerance=true`; supersedes `session_20261116T140001Z`).
- FCLR-008 — `session_20261116T230140Z` (B0/B1 within tolerance; C1/C2 divergence documented; qualitative NOT_MET corroborated). `session_20261116T221127Z` is a superseded earlier FCLR-008 attempt — do not count/resume.
- FCLR-RCA-011 — complete bundle `session_20261116T100533Z/`.

Incomplete trigger-only sessions (do not resume/copy/count): `session_20261116T104644Z/`, `session_20261116T105341Z/`, `session_20261116T134957Z/`.

## Why this campaign exists (bottlenecks removed)

The former `FCLR-READINESS-01` campaign was complete. FCLR-002 and FCLR-003 have now been independently recomputed, so they must not be repeated. The next agent-removable bottleneck is the remaining reproducibility queue: FCLR-010, then FCLR-013/FCLR-014. The previous handoff understated a major data-path issue: Apr-Jun 2024 mark/premium/index files are ZIP archives, while Jan-Mar and Jul-Nov are CSVs. A CSV-only reader silently drops the entire Apr-Jun training window and produces false `None`/zero-row results. Future sessions must use a ZIP-aware reader or the existing session-local `recompute_fclr002_003_20261117T000400Z.py`.

The rank-0 frontier's `next_unfinished_task` defers the concrete task to this note. This note makes a **new quantitative artifact** the completion floor: trigger checks, tests/gates, copied bundles, static re-audits, and "no trigger → stop cleanly" are not completion. The maintenance-refresh treadmill (handoff-only refreshes with no heavy artifact) must not repeat.

## Non-skippable execution contract

### Phase A — Check external triggers once

Read only `research_state/resume_trigger_registry.json` and `research_state/ironflow_monitor_state.json`. Record timestamp and verdict in the new session directory. Do not poll, issue network requests, re-probe HuggingFace, or repeat later. Triggers: `GATE4_BRANCH_1`, `NEW_OBSERVED_LIQUIDATION_SOURCE`, `HL_LABEL_EXTENSION`, `EXPANSION_ROBUSTNESS_REDO` — satisfied only by registry-defined evidence artifacts. Agent cannot mark `GATE4_BRANCH_1` RESOLVED_VERIFIED. Current state: all OPEN; Ironflow `data_through=2026-10`; 2026-11/12 and 2027-01 `CONFIRMED_ABSENT`.

### Phase B — Emit ONE new quantitative artifact (the heavy work)

Every session must write artifact (JSON+MD) + script into the new session directory.

1. **No trigger fired — FCLR-010 independent recompute (primary, non-skippable).** Recompute the terminal Track-A liquidation-confirm headline from `research_state/fclr_liq_010_confirm_panel_20261113T065953Z.parquet` without mutating the sealed panel. If `pyarrow` is unavailable, use an available parquet-capable local reader; if no local reader exists, record the exact dependency blocker and use the documented fallback in `AGENT_HANDOFF.md` rather than fabricating values. Write `recompute_fclr010_<UTC>.{json,md}`.
2. **FCLR-013/FCLR-014 (do if FCLR-010 completes cleanly and their cached panels/coverage audits are present).** Independent recompute from the registered 2026 Q3 / 2025 H1 panels; write `recompute_fclr013_<UTC>.{json,md}` and/or `recompute_fclr014_<UTC>.{json,md}`. Do not rerun FCLR-002/003/006/008/009.
3. **Fallback only if FCLR-010 inputs are unavailable:** record the exact missing path/hash and independently recompute the `fclr_liq_010_confirm_panel` fallback named in the handoff. A trigger check/copy/prose-only result is not completion.
4. **Trigger fired:** perform `RESEARCH_PROMPT.md` §16 admissibility/source audit, instantiate a **new** prereg from `session_20261116T035833Z/prereg_template_trigger_gated_20261116T035833Z.json` sized per `session_20261116T100533Z/trigger_readiness_power_calibration_20261116T100533Z.md` (paired_n >= anchor `n_required_for_2pct`, >=5 instruments, >=3 non-overlapping 30-day blocks, 7d purge/embargo, prespecified Holm family, `outcome_data_inspected_before_freeze=false`), then execute and record honest verdict.

### Phase C — Verify and hand off

1. Create `research_state/session_<UTC>/`.
2. Audit `session_20261116T100533Z/` (5 RCA families), `session_20261116T125624Z/` (FCLR-009), `session_20261116T185811Z/` (FCLR-006), `session_20261116T230140Z/` (FCLR-008), and `session_20261117T000400Z/` (FCLR-002/003) present.
3. Write a concise evidence-audit artifact in the new session dir.
4. Run and capture under new session dir: `check_handoff_heavywork_gate.py --json`, `check_tracka_scope_registry_drift.py --json`, targeted unittests, and `python3 -m unittest discover -q` to completion (record count/skip/error/EXIT; never call timeout green). Baseline: 1340 tests, 4 pre-existing pyarrow errors (`tests.test_fclr_liq_combined_admissibility_audit`), 18 skipped, EXIT 1; success = same set with no new failures/errors. Revert timestamp-only tracked-file side effects.
5. Update only `AGENT_HANDOFF.md` (timestamp/verification/queue), preserve sole-handoff contract and blockers.

A session that only rereads triggers, repeats prior prose, copies old bundle without new analysis, redoes FCLR-002/003/006/008/009, or records green checks without a new artifact is incomplete.

## Design-power summary (from `trigger_readiness_power_calibration_20261116T100533Z.md`)

- Only **FCLR-009** (n=24,495, 6 blocks, MDE **1.95%**) was powered for the 2% floor.
- FCLR-002/003/011/013/014 were underpowered (MDE 5.1%–16.4%).
- Track A liquidation recompute (n=593, MDE **8.88%**) needs **~11,689 paired observations** for a 2% MDE.
- Per-trigger sample floors: Gate 4 / Track C `paired_n >= 23,224`; Track A / expansion `paired_n >= 11,689`; all with >=3 blocks and 7d purge/embargo.

## Bottleneck policy

- **Stale instructions:** `NEXT_SESSION_HANDOFF.md`, `NEXT_SESSION_TASK.md`, `HANDOFF_NEXT_SESSION_20261116T114626Z.md`, and `AGENT_HANDOFF_20261115T073240Z.md` have no authority. `AGENT_HANDOFF.md` is sole handoff.
- **Incomplete sessions:** `session_20261116T104644Z/`, `session_20261116T105341Z/`, `session_20261116T134957Z/` (trigger-only) — do not resume, copy, or count. `session_20261116T140001Z/` is a superseded tolerance-failed FCLR-006 attempt. `session_20261116T221127Z/` is a superseded divergent FCLR-008 attempt. Do not recreate empty shells.
- **Maintenance treadmill:** handoff-only refreshes with no new heavy artifact are not completion and must not repeat; the next session must emit `recompute_fclr010_<UTC>.{json,md}` (FCLR-013/014 next).
- **Completed-work confusion:** FCLR-002/003/006/008/009 and FCLR-RCA-011 are complete; do not rerun them merely because an old note calls them pending. Next is **FCLR-010**.
- **Missing inputs:** `research_protocol_fclr002.md` / `research_protocol_fclr003.md` do not exist; `run_manifest.json` and panel/manifest JSONs are unresolved LFS pointers. FCLR-002/003 have now been computed with hardcoded splits; do not repeat. For FCLR-010, verify the parquet is a real local file and not an LFS pointer before analysis.
- **ZIP/CSV bottleneck:** the 2024 cache is mixed-format; Apr-Jun mark/premium/index data are ZIP archives. CSV-only globbing silently produces false zero-row results. Use the ZIP-aware reader pattern in `session_20261117T000400Z/recompute_fclr002_003_20261117T000400Z.py`.
- **Gate false failure:** gate accepts latest new-style session with `evidence_audit_*` + fresh quantitative artifact while resolving complete bundle. Do not weaken.
- **Root churn:** root `research_state/*.md|json` count is 500/500. Keep new outputs in session subdirectories.
- **Dependencies:** readiness/reproducibility path is stdlib/numpy-only; do not add `statsmodels` or unpinned heavy deps to core path.
- **Suite duration:** allow discovery suite to finish and record actual exit status; do not substitute partial run. The 4 pyarrow errors are environmental, not a new regression.
- **External science:** if no trigger fires, required progress is the new FCLR-010 artifact (FCLR-013/014 next), evidence audit, complete gate run, and accurate handoff update. Repeated polling and new confirmatory estimands on exhausted cached data are forbidden.

## Verification record — 2026-11-17T00:04:00Z

- Handoff/campaign aligned: **FCLR-010** is mandatory next heavy artifact; FCLR-002 and FCLR-003 are DONE in `session_20261117T000400Z` and must not be repeated.
- Inputs verified present: `research_state/evaluation_summary_FCLR002.md`, `evaluation_summary_FCLR003.md`, `data_cache/{SYM}_2024_01..12/` for all 5 symbols, fallback parquet `fclr_liq_010_confirm_panel_20261113T065953Z.parquet`.
- New bottleneck documented: Apr-Jun 2024 mark/premium/index files are ZIP archives; future readers must handle them.
- Blocked inputs documented: `research_protocol_fclr002.md` / `research_protocol_fclr003.md` absent; `run_manifest.json` / `run_manifest_FCLR002.json` / `fclr002_panel*.json` / `manifest_fclr002.json` / `manifest_fclr003.json` are unresolved LFS pointers.
- `python3 scripts/check_handoff_heavywork_gate.py --json`: **PASS** (`latest_session=session_20261116T230140Z` at capture; root 500/500, EXIT 0).
- `python3 scripts/check_tracka_scope_registry_drift.py --json`: **PASS**; 196/196 scripts, EXIT 0.
- Targeted suite (`test_active_campaign_gate`, `test_tracka_hardening_117/118/143`): **52 tests OK, EXIT 0**.
- Full `unittest discover -q`: **1340 tests, 4 pre-existing pyarrow errors, 18 skipped, EXIT 1** — recorded per mandate; no new failures introduced.

## Session closeout

- [x] Trigger registry and monitor state checked once; verdict recorded.
- [x] New `research_state/session_20261117T000400Z/` created.
- [x] Two new quantitative artifacts produced (FCLR-002 and FCLR-003).
- [x] Carried-forward bundles verified.
- [x] Gate JSON outputs and full-suite final result recorded under the new session directory.
- [x] Root md/json count remains at most 500.
- [ ] `AGENT_HANDOFF.md` updated with the new timestamp, new-artifact result, gate results, and remaining external blockers.

Stop cleanly only when every box is checked. Never leave the suite with new failures, never delete the rank-0 sentinel, and never claim completion from a trigger-only or copied-bundle-only check alone.