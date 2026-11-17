# FCLR Focus Campaign — `FCLR-REPRO-AUDIT-04` — current as of 2026-11-17T04:07:43Z

**Frontier rank 0:** `FCLR-BOUNDED-TRIGGER-ONLY-20261115T220000Z` (`TRIGGER_ONLY` / `BOUNDED_TRIGGER_ONLY`, `all_terminal=true`, `next_action_heavy=null`).
**Sole handoff:** `AGENT_HANDOFF.md` (refreshed 2026-11-17T04:07:43Z). This file is the detailed campaign note referenced by the frontier and the handoff.
**Governing rules:** `RESEARCH_PROMPT.md`. Never re-run concluded estimands, re-score sealed results, fabricate data, edit `.github/workflows/*`, poll, re-probe the HuggingFace tree, use paid/credentialed/manual outcome data, or run `git lfs pull`.
**Artifact rule:** write every new artifact to a new `research_state/session_<UTC>/`. The `research_state/` root is at 500/500 md/json; adding root files breaks the enforced churn cap.

## Current target (updated 2026-11-17T04:07:43Z)

**Primary heavy artifact: FCLR-014 panel coverage audit + blocker resolution** (5-symbol local `data_cache` coverage matrix + corrected blocker statement). FCLR-013 and FCLR-010 are DONE (both NOT_REPLICATED) and must not be repeated.

**CORRECTED FCLR-014 FRAMING (verified this session):** the prior "no admissible panel exists locally" claim is FALSE. The local `data_cache` holds complete 5-symbol mark+index+premium+funding for **all of 2025 (12 mo) and 2026-01..10 (10 mo)**, plus **2024-04..2024-11 mark+funding** (2024-11 has index/premium for BTCUSDT only; 2024-12 index/premium incomplete for all). The genuine blocker is **design admissibility under `TESTED_WINDOWS`** in `scripts/next_campaign_status.py`: a contiguous 3-block confirmatory design needs an untested run >= `MIN_DESIGN_DAYS` (127d), and every such run is consumed by a sealed cell (2025-02..2026-10). Complete-but-untested months 2024-04/2024-05 and 2025-01 have 30-day train windows that lack funding or full index/premium. The next session must document this corrected blocker and either freeze a NEW pre-registered design (mark+funding-only B0/B1/C1, or a disjoint-block design on fully-complete months) before outcomes, or record the exact missing coverage month and hold. Do NOT re-score sealed summaries.

Completed and NOT to be repeated:
- **FCLR-010 — DONE (`session_20261117T002014Z`).** Independent **parquet-free** recompute (CSV `results/liqmicro_v2/panel_liqmicro_v2.csv` + `hyperliquid_funding/{SYM}.json`). Verdict **NOT_REPLICATED**: C2-vs-B1 Brier relative reduction **0.50%** (CI `[-0.001106,-0.000316]`) vs sealed **2.21%**; below 2% materiality floor; LOIO and placebo **fail**; 17 symbols, n=64,056, 157 days. Direction replicates; magnitude does not.
- FCLR-002 — `session_20261117T000400Z` (exact values diverged beyond tolerance; C2-vs-B1 directionally positive; gate NOT_MET).
- FCLR-003 — `session_20261117T000400Z` (B0/B1 matched; C1/C2 diverged; NOT_MET corroborated).
- FCLR-009 — `session_20261116T125624Z` (`all_within_tolerance=true`).
- FCLR-006 — `session_20261116T185811Z` (`all_within_tolerance=true`; supersedes `session_20261116T140001Z`).
- FCLR-008 — `session_20261116T230140Z` (B0/B1 within tolerance; C1/C2 divergence documented; NOT_MET corroborated). `session_20261116T221127Z` is a superseded earlier FCLR-008 attempt — do not count/resume.
- FCLR-RCA-011 — complete bundle `session_20261116T100533Z/`.

Incomplete trigger-only sessions (do not resume/copy/count): `session_20261116T104644Z/`, `session_20261116T105341Z/`, `session_20261116T134957Z/`.

## Why this campaign exists (bottlenecks removed)

The reproducibility queue is the only agent-removable heavy work on exhausted cached data. FCLR-010 was the last parquet-blocked item and is now complete via a CSV/JSON path: **no parquet engine is installed** (`pyarrow`/`fastparquet`/`duckdb`/`polars` absent; network installs prohibited), so any task whose only input is `.parquet` must find a CSV/JSON/ZIP twin or record the exact blocker. FCLR-013 is genuinely actionable because its 2026 Q3 inputs are present as **ZIP archives** for all five symbols (`research_state/data_cache/{BTCUSDT,ETHUSDT,BNBUSDT,SOLUSDT,XRPUSDT}_2026_07|08|09/`). A CSV-only glob silently drops days.

The rank-0 frontier's `next_unfinished_task` defers the concrete task to this note. This note makes a **new quantitative artifact** the completion floor: trigger checks, tests/gates, copied bundles, static re-audits, and "no trigger → stop cleanly" are not completion.

## Non-skippable execution contract

### Phase A — Check external triggers once

Read only `research_state/resume_trigger_registry.json` and `research_state/ironflow_monitor_state.json`. Record timestamp and verdict in the new session directory. Do not poll, issue network requests, re-probe HuggingFace, or repeat later. Triggers: `GATE4_BRANCH_1`, `NEW_OBSERVED_LIQUIDATION_SOURCE`, `HL_LABEL_EXTENSION`, `EXPANSION_ROBUSTNESS_REDO` — satisfied only by registry-defined evidence artifacts. Agent cannot mark `GATE4_BRANCH_1` RESOLVED_VERIFIED. Current state: all OPEN; Ironflow `data_through=2026-10`, `consecutive_absent=3`; 2026-11/12 and 2027-01 `CONFIRMED_ABSENT`.

### Phase B — Emit ONE new quantitative artifact (the heavy work)

Every session must write artifact (JSON+MD) + script into the new session directory.

1. **No trigger fired — FCLR-013 independent recompute (primary, non-skippable).** From the 2026 Q3 ZIP cache for BTCUSDT/ETHUSDT/BNBUSDT/SOLUSDT/XRPUSDT, reconstruct the frozen FCLR-013 estimand (C2 vs B1 next-24h RV QLIKE; splits 2026-07-01..09-30, 7d embargo) using the ZIP-aware reader pattern in `session_20261117T000400Z/recompute_fclr002_003_20261117T000400Z.py`. Do not read `run_manifest.json`, do not use parquet, do not re-score the sealed summary. Write `recompute_fclr013_<UTC>.{py,json,md}`.
2. **FCLR-014 (only if FCLR-013 completes cleanly and its registered panel/coverage audit are present and non-parquet).** Same independence rule; write `recompute_fclr014_<UTC>.{py,json,md}`. If FCLR-014 is parquet-only with no twin, record the exact blocker and emit the closest non-parquet artifact.
3. **Fallback only if FCLR-013 inputs are unavailable:** record the exact missing path/hash and independently recompute the closest local cached estimand. A trigger check/copy/prose-only result is not completion.
4. **Trigger fired:** perform `RESEARCH_PROMPT.md` §16 admissibility/source audit, instantiate a **new** prereg from `session_20261116T035833Z/prereg_template_trigger_gated_20261116T035833Z.json` sized per `session_20261116T100533Z/trigger_readiness_power_calibration_20261116T100533Z.md` (paired_n >= anchor `n_required_for_2pct`, >=5 instruments, >=3 non-overlapping 30-day blocks, 7d purge/embargo, prespecified Holm family, `outcome_data_inspected_before_freeze=false`), then execute and record honest verdict.

### Phase C — Verify and hand off

1. Create `research_state/session_<UTC>/`.
2. Audit `session_20261116T100533Z/` (5 RCA families), `session_20261116T125624Z/` (FCLR-009), `session_20261116T185811Z/` (FCLR-006), `session_20261116T230140Z/` (FCLR-008), `session_20261117T000400Z/` (FCLR-002/003), `session_20261117T002014Z/` (FCLR-010) present.
3. Write a concise evidence-audit artifact in the new session dir.
4. Run and capture under new session dir: `check_handoff_heavywork_gate.py --json`, `check_tracka_scope_registry_drift.py --json`, targeted unittests, and `python3 -m unittest discover -q` to completion (record count/skip/error/EXIT; never call timeout green). Baseline: 1340 tests, 4 pre-existing pyarrow errors (`tests.test_fclr_liq_combined_admissibility_audit`), 18 skipped, EXIT 1; success = same set with no new failures/errors. Revert timestamp-only tracked-file side effects.
5. Update only `AGENT_HANDOFF.md` (timestamp/verification/queue), preserve sole-handoff contract and blockers.

A session that only rereads triggers, repeats prior prose, copies old bundle without new analysis, redoes FCLR-002/003/006/008/009/010, or records green checks without a new artifact is incomplete.

## Design-power summary (from `trigger_readiness_power_calibration_20261116T100533Z.md`)

- Only **FCLR-009** (n=24,495, 6 blocks, MDE **1.95%**) was powered for the 2% floor.
- FCLR-002/003/011/013/014 were underpowered (MDE 5.1%–16.4%).
- Track A liquidation recompute (n=593, MDE **8.88%**) needs **~11,689 paired observations** for a 2% MDE.
- Per-trigger sample floors: Gate 4 / Track C `paired_n >= 23,224`; Track A / expansion `paired_n >= 11,689`; all with >=3 blocks and 7d purge/embargo.

## Bottleneck policy

- **Parquet engine absent:** no `pyarrow`/`fastparquet`/`duckdb`/`polars`; network installs prohibited. Never run `scripts/fclr_liq_010_confirm.py` (parquet-only). Prefer CSV/JSON/ZIP twins; if none exists, record the exact blocker rather than fabricating.
- **Stale instructions:** `NEXT_SESSION_HANDOFF.md`, `NEXT_SESSION_TASK.md`, `HANDOFF_NEXT_SESSION_20261116T114626Z.md`, and `AGENT_HANDOFF_20261115T073240Z.md` have no authority. `AGENT_HANDOFF.md` is sole handoff.
- **Incomplete sessions:** `session_20261116T104644Z/`, `session_20261116T105341Z/`, `session_20261116T134957Z/` (trigger-only) — do not resume, copy, or count. `session_20261116T140001Z/` is a superseded tolerance-failed FCLR-006 attempt. `session_20261116T221127Z/` is a superseded divergent FCLR-008 attempt. Do not recreate empty shells.
- **Maintenance treadmill:** handoff-only refreshes with no new heavy artifact are not completion and must not repeat; the next session must emit `recompute_fclr013_<UTC>.{json,md}` (FCLR-014 next).
- **Completed-work confusion:** FCLR-002/003/006/008/009/010 and FCLR-RCA-011 are complete; do not rerun them merely because an old note calls them pending. Next is **FCLR-013**.
- **Missing inputs:** `research_protocol_fclr002.md` / `research_protocol_fclr003.md` do not exist; `run_manifest.json` and panel/manifest JSONs are unresolved LFS pointers. For FCLR-010 the CSV/JSON path is proven; for FCLR-013 verify the 2026 Q3 ZIP caches are real local files.
- **ZIP/CSV bottleneck:** 2024 and 2026 caches are ZIP archives (mixed with CSVs); CSV-only globbing silently produces false zero-row results. Use the ZIP-aware reader pattern.
- **Gate false failure:** gate accepts the latest new-style session with `evidence_audit_*` + fresh quantitative artifact while resolving the complete bundle. Do not weaken.
- **Root churn:** root `research_state/*.md|json` count is 500/500. Keep new outputs in session subdirectories.
- **Dependencies:** readiness/reproducibility path is stdlib/numpy-only; do not add `statsmodels` or unpinned heavy deps to core path.
- **Suite duration:** allow discovery suite to finish and record actual exit status; do not substitute partial run. The 4 pyarrow errors are environmental, not a new regression.
- **External science:** if no trigger fires, required progress is the new FCLR-013 artifact (FCLR-014 next), evidence audit, complete gate run, and accurate handoff update. Repeated polling and new confirmatory estimands on exhausted cached data are forbidden.

## Verification record — 2026-11-17T00:23:34Z

- Handoff/campaign aligned: **FCLR-013** is the mandatory next heavy artifact; FCLR-010 is **DONE** in `session_20261117T002014Z` (verdict NOT_REPLICATED) and must not be repeated.
- Parquet-engine bottleneck removed for FCLR-010 via `results/liqmicro_v2/panel_liqmicro_v2.csv` + `hyperliquid_funding/{SYM}.json`; FCLR-013 is actionable from 2026 Q3 ZIP caches for all 5 symbols.
- New artifacts: `session_20261117T002014Z/recompute_fclr010_20261117T002014Z.{py,json,md}`, `evidence_audit_20261117T002014Z.md`, `trigger_check_20261117T002014Z.json`.
- `python3 scripts/check_handoff_heavywork_gate.py --json`: **PASS**; `python3 scripts/check_tracka_scope_registry_drift.py --json`: **PASS**.
- Targeted suite (`test_active_campaign_gate`, `test_tracka_hardening_117/118/143`): **52 tests OK, EXIT 0**.
- Full `unittest discover -q`: captured under the session dir; baseline 1340 tests, 4 pre-existing pyarrow errors, 18 skipped, EXIT 1 — recorded per mandate; no new failures introduced.

## Session closeout

- [x] Trigger registry and monitor state checked once; verdict recorded (`session_20261117T002014Z/trigger_check_20261117T002014Z.json`).
- [x] New `research_state/session_20261117T002014Z/` created.
- [x] New quantitative artifact produced (FCLR-010 independent recompute; verdict NOT_REPLICATED).
- [x] Evidence audit written.
- [x] Carried-forward bundles verified.
- [x] Root md/json count remains at most 500.
- [x] `AGENT_HANDOFF.md` updated with the new timestamp, new-artifact result, gate results, and remaining external blockers.

Stop cleanly only when every box is checked. Never leave the suite with new failures, never delete the rank-0 sentinel, and never claim completion from a trigger-only or copied-bundle-only check alone.