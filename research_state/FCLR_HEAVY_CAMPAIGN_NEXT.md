# FCLR Focus Campaign — `FCLR-REPRO-AUDIT-02` — current as of 2026-11-16T20:14:30Z

**Frontier rank 0:** `FCLR-BOUNDED-TRIGGER-ONLY-20261115T220000Z` (`TRIGGER_ONLY` / `BOUNDED_TRIGGER_ONLY`, `all_terminal=true`, `next_action_heavy=null`).
**Sole handoff:** `AGENT_HANDOFF.md` (refreshed 2026-11-16T20:14:30Z). This file is the detailed campaign note referenced by the frontier and the handoff.
**Governing rules:** `RESEARCH_PROMPT.md`. Never re-run concluded estimands, re-score sealed results, fabricate data, edit `.github/workflows/*`, poll, re-probe the HuggingFace tree, or use paid/credentialed/manual outcome data.
**Artifact rule:** write every new artifact to a new `research_state/session_<UTC>/`. The `research_state/` root is at 500/500 md/json; adding root files breaks the enforced churn cap.

## Why this campaign exists (bottlenecks removed)

The previous `FCLR-READINESS-01` campaign was complete: it precomputed per-trigger design power and produced the FCLR-011 third independent recompute. Incomplete sessions `session_20261116T104644Z/`, `session_20261116T105341Z/`, `session_20261116T134957Z/` (trigger-only) must not be resumed/copied/counted; an empty incomplete session dir was removed in this refresh. `FCLR-REPRO-AUDIT-02` makes the heavy-work gate a **floor** and requires every session to emit a *new* quantitative artifact: an independent reproducibility audit of the terminal headlines, in queue order.

**2026-11-16T20:06:45Z refresh (stale-target bottleneck removed):** FCLR-009 DONE (`session_20261116T125624Z/`, `all_within_tolerance=true`). FCLR-006 DONE (`session_20261116T185811Z/`, `all_within_tolerance=true`; supersedes tolerance-failed `session_20261116T140001Z/`). The primary Phase-B target is now **FCLR-008** (queue item 3) with explicit published values recorded in `AGENT_HANDOFF.md`; FCLR-006/FCLR-009 must not be repeated. This alignment removes the prior campaign/handoff mismatch that could send agents to already-complete work.

## Current classification

The former FCLR-RCA-011 heavy campaign is **COMPLETE**. Its evidence bundle is `research_state/session_20261116T035833Z/`, carried forward unmodified into `research_state/session_20261116T100533Z/` (current self-contained bundle). It contains all required Phase-B/C artifacts:

- `rca011_feature_attribution_20261116T035833Z.{json,md}`
- `rca011_impl_crosscheck_20261116T035833Z.json`
- `rca011_sealed_bridge_20261116T035833Z.md` and `_ext`
- `prereg_template_trigger_gated_20261116T035833Z.json`
- `program_power_synthesis_20261116T035833Z.{json,md}`

Latest completed heavy sessions:
- `session_20261116T125624Z/` (4 files): `recompute_fclr009_20261116T125624Z.{py,json,md}` + `evidence_audit_20261116T125624Z.md` — FCLR-009 reproduced `all_within_tolerance=true` (queue item 1 DONE). No discovery-suite capture saved there.
- `session_20261116T185811Z/`: `recompute_fclr006_20261116T185811Z.{py,json,md}` + `evidence_audit_20261116T185811Z.md` + `trigger_check.json` + `unittest_discover.txt` + gate outputs — FCLR-006 reproduced `all_within_tolerance=true` (queue item 2 DONE).

Do not delete or replace `session_20261116T100533Z/` without first installing a complete successor bundle. `session_20261116T140001Z/` is a superseded tolerance-failed FCLR-006 attempt (do not count as completion). Incomplete trigger-only sessions: `session_20261116T104644Z/`, `session_20261116T105341Z/`, `session_20261116T134957Z/`.

## Non-skippable execution contract

### Phase A — Check external triggers once

Read only `research_state/resume_trigger_registry.json` and `research_state/ironflow_monitor_state.json`. Record timestamp and verdict in the new session directory. Do not poll, issue network requests, re-probe HuggingFace, or repeat later. Triggers: `GATE4_BRANCH_1`, `NEW_OBSERVED_LIQUIDATION_SOURCE`, `HL_LABEL_EXTENSION`, `EXPANSION_ROBUSTNESS_REDO` — satisfied only by registry-defined evidence artifacts. Agent cannot mark `GATE4_BRANCH_1` RESOLVED_VERIFIED. Current state: all OPEN; Ironflow `data_through=2026-10`; 2026-11/12/2027-01 `CONFIRMED_ABSENT`.

### Phase B — Emit ONE new quantitative artifact (the heavy work)

Every session must do exactly one of the following and write artifact (JSON+MD) + script into the new session directory:

1. **No trigger fired — FCLR-008 independent recompute (primary, non-skippable; queue item 3).** Recompute B0/B1/C1/C2 24h QLIKE and paired contrasts on the frozen test window from cached 2026 data. Use `research_state/research_protocol_fclr008.md` (frozen) and `research_state/evaluation_summary_FCLR-008.md` (published). Do not run canonical `scripts/run_evaluation.py` against tracked summary; use independent path; never mutate sealed artifacts. Write `recompute_fclr008_<UTC>.{json,md}` plus script.
   - Frozen splits: train `2026-01-01T00:00:00Z..2026-03-17T23:00:00Z`; 7d embargo `2026-03-18..2026-03-24`; val `2026-03-25T00:00:00Z..2026-04-30T23:00:00Z`; 7d embargo `2026-05-01..2026-05-07`; test `2026-05-08T00:00:00Z..2026-08-06T23:00:00Z` (91 days, 3 blocks).
   - Data: `research_state/data_cache/{BTCUSDT,ETHUSDT,BNBUSDT,SOLUSDT,XRPUSDT}_2026_0{1..8}/` (markPriceKlines 1h, indexPriceKlines, premiumIndexKlines, fundingRate).
   - Published values (from eval summary): B0 `0.330127` (n=10800), B1 `0.333314` (n=10785), C1 `0.330164` (n=10785), C2 `0.318996` (n=10785). C2_vs_B1 diff `-0.014318` CI `[-0.029938,0.000524]` rel `4.30%` n=10785; C1_vs_B1 diff `-0.003150` CI `[-0.010051,0.003832]` rel `0.94%`; C2_vs_C1 diff `-0.011168` CI `[-0.026088,0.002175]` rel `3.38%`. Gate NOT_MET (CI excludes zero: no). Tolerances: QLIKE abs <= 1e-6; mean diff abs <= 1e-6; relative reduction <= 0.01 pct-points.
2. **Fallback only if FCLR-008 cache incomplete:** record exact missing path/hash, then independently recompute `FCLR-LIQ-010-CONFIRM` from `research_state/fclr_liq_010_confirm_panel_20261113T065953Z.parquet`. Still heavy work; trigger check/copy/prose-only is not.
3. **Trigger fired:** perform `RESEARCH_PROMPT.md` §16 admissibility/source audit, instantiate a **new** prereg from `session_20261116T035833Z/prereg_template_trigger_gated_20261116T035833Z.json` sized per `session_20261116T100533Z/trigger_readiness_power_calibration_20261116T100533Z.md` (paired_n >= anchor `n_required_for_2pct`, >=5 instruments, >=3 non-overlapping 30-day blocks, 7d purge/embargo, prespecified Holm family, `outcome_data_inspected_before_freeze=false`), then execute and record honest verdict.

### Phase C — Verify and hand off

1. Create `research_state/session_<UTC>/`.
2. Audit `session_20261116T100533Z/` (5 RCA families) and confirm `session_20261116T125624Z/` (FCLR-009) + `session_20261116T185811Z/` (FCLR-006) present.
3. Write concise evidence-audit artifact in new session dir.
4. Run and capture under new session dir: `check_handoff_heavywork_gate.py --json`, `check_tracka_scope_registry_drift.py --json`, targeted unittests, and `python3 -m unittest discover -q` to completion (record count/skip/EXIT; never call timeout green). Revert timestamp-only tracked-file side effects.
5. Update only `AGENT_HANDOFF.md` (timestamp/verification/queue), preserve sole-handoff contract and blockers.

A session that only rereads triggers, repeats prior prose, copies old bundle without new analysis, redoes FCLR-006/FCLR-009, or records green checks without a new artifact is incomplete.

## Design-power summary (from `trigger_readiness_power_calibration_20261116T100533Z.md`)

- Only **FCLR-009** (n=24,495, 6 blocks, MDE **1.95%**) was powered for the 2% floor.
- FCLR-002/003/011/013/014 were underpowered (MDE 5.1%–16.4%).
- Track A liquidation recompute (n=593, MDE **8.88%**) needs **~11,689 paired observations** for a 2% MDE.
- Per-trigger sample floors: Gate 4 / Track C `paired_n >= 23,224`; Track A / expansion `paired_n >= 11,689`; all with >=3 blocks and 7d purge/embargo.

## Bottleneck policy

- **Stale instructions:** `NEXT_SESSION_HANDOFF.md`, `NEXT_SESSION_TASK.md`, `HANDOFF_NEXT_SESSION_20261116T114626Z.md`, and `AGENT_HANDOFF_20261115T073240Z.md` have no authority. `AGENT_HANDOFF.md` is sole handoff.
- **Incomplete sessions:** `session_20261116T104644Z/`, `session_20261116T105341Z/`, `session_20261116T134957Z/` (trigger-only) — do not resume, copy, or count. `session_20261116T140001Z/` is a superseded tolerance-failed FCLR-006 attempt. An empty incomplete session dir was removed in this refresh.
- **Completed-work confusion:** FCLR-RCA-011, FCLR-009, and FCLR-006 are complete; do not rerun merely because an old note calls them pending. Next is **FCLR-008**.
- **Gate false failure:** gate accepts latest new-style session with `evidence_audit_*` + fresh quantitative artifact while resolving complete bundle. Do not weaken.
- **Root churn:** root `research_state/*.md|json` count is 500/500. Keep new outputs in session subdirectories.
- **Dependencies:** readiness/reproducibility path is stdlib/numpy-only; do not add `statsmodels` or unpinned heavy deps to core path.
- **Suite duration:** allow discovery suite to finish and record actual exit status; do not substitute partial run.
- **External science:** if no trigger fires, required progress is the new FCLR-008 artifact (or documented LIQ-010 fallback), evidence audit, complete gate run, and accurate handoff update. Repeated polling and new confirmatory estimands on exhausted cached data are forbidden.

## Verification record — 2026-11-16T20:14:30Z

- Handoff/campaign reaffirmed: **FCLR-008** is mandatory next heavy artifact (`recompute_fclr008_<UTC>.{json,md}`), FCLR-006/FCLR-009 done/not to repeat, trigger-only/superseded sessions not resumable.
- `python3 scripts/check_handoff_heavywork_gate.py --json`: **PASS**; `heavy_session=session_20261116T100533Z`, `latest_session=session_20261116T185811Z`, root 500/500, EXIT 0.
- `python3 scripts/check_tracka_scope_registry_drift.py --json`: **PASS**; 196/196 scripts, EXIT 0.
- No new heavy research artifact produced by this maintenance refresh; next session must produce `recompute_fclr008_<UTC>.{json,md}` (+ script) or documented LIQ-010 fallback, with evidence audit and full gate/suite capture.

## Session closeout

- [ ] Trigger registry and monitor state checked once; verdict recorded.
- [ ] New `research_state/session_<UTC>/` created.
- [ ] One new quantitative artifact produced (FCLR-008 recompute or documented LIQ-010 fallback).
- [ ] Carried-forward `session_20261116T100533Z` bundle and `session_20261116T125624Z`/`session_20261116T185811Z` recomputes verified.
- [ ] Gate JSON outputs and full-suite final result recorded under the new session directory.
- [ ] Root md/json count remains at most 500.
- [ ] `AGENT_HANDOFF.md` updated with the new timestamp, new-artifact result, gate results, and remaining external blockers.

Stop cleanly only when every box is checked. Never leave the suite red, never delete the rank-0 sentinel, and never claim completion from a trigger-only or copied-bundle-only check alone.