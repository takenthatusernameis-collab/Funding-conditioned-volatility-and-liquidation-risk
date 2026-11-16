# FCLR Focus Campaign — `FCLR-REPRO-AUDIT-02` — current as of 2026-11-16T13:45:00Z

**Frontier rank 0:** `FCLR-BOUNDED-TRIGGER-ONLY-20261115T220000Z` (`TRIGGER_ONLY` / `BOUNDED_TRIGGER_ONLY`, `all_terminal=true`, `next_action_heavy=null`).
**Sole handoff:** `AGENT_HANDOFF.md` (refreshed 2026-11-16T13:45:00Z). This file is the detailed campaign note referenced by the frontier and the handoff.
**Governing rules:** `RESEARCH_PROMPT.md`. Never re-run concluded estimands, re-score sealed results, fabricate data, edit `.github/workflows/*`, poll, re-probe the HuggingFace tree, or use paid/credentialed/manual outcome data.
**Artifact rule:** write every new artifact to a new `research_state/session_<UTC>/`. The `research_state/` root is at 500/500 md/json; adding root files breaks the enforced churn cap.

## Why this campaign exists (bottlenecks removed)

The previous `FCLR-READINESS-01` campaign was complete: it precomputed per-trigger design power and produced the FCLR-011 third independent recompute. Two sessions were left trigger-only (`session_20261116T104644Z/` and `session_20261116T105341Z/`); they are incomplete and must not be resumed or copied. `FCLR-REPRO-AUDIT-02` makes the heavy-work gate a **floor** and requires every session to emit a *new* quantitative artifact: an independent reproducibility audit of the terminal headlines, in queue order.

**2026-11-16T13:45:00Z refresh (stale-target bottleneck removed):** FCLR-009 reproducibility is DONE (`session_20261116T125624Z/`, `all_within_tolerance=true`; B0 0.367906, B1 0.340756, C1 0.339628, C2 0.342205; C2-vs-B1 mean diff 0.001449, rel -0.425%, CI [-0.003120, 0.006165], n_pairs 24,495). The handoff previously still named FCLR-009 as the mandatory step-3 target, which would have made the next session repeat completed work. The primary Phase-B target is now **FCLR-006** (queue item 2); FCLR-009 must not be repeated.

## Current classification

The former FCLR-RCA-011 heavy campaign is **COMPLETE**. Its evidence bundle is `research_state/session_20261116T035833Z/`, carried forward unmodified into `research_state/session_20261116T100533Z/` (the current self-contained bundle). It contains all required Phase-B/C artifacts:

- `rca011_feature_attribution_20261116T035833Z.{json,md}`
- `rca011_impl_crosscheck_20261116T035833Z.json`
- `rca011_sealed_bridge_20261116T035833Z.md` and `_ext`
- `prereg_template_trigger_gated_20261116T035833Z.json`
- `program_power_synthesis_20261116T035833Z.{json,md}`

The latest heavy session is `research_state/session_20261116T125624Z/` (exactly four files): `recompute_fclr009_20261116T125624Z.{py,json,md}` + `evidence_audit_20261116T125624Z.md`. It independently reproduced the FCLR-009 headline (the only adequately powered Track C null) with `all_within_tolerance=true`. Note: this session directory does **not** contain a discovery-suite capture (an earlier handoff claim to that effect was corrected at 2026-11-16T13:45:00Z); the next session must capture its own gate/suite outputs. Do not delete or replace the `session_20261116T100533Z/` bundle without first installing a complete successor bundle.

## Non-skippable execution contract

### Phase A — Check external triggers once

Read only these files at session start:

1. `research_state/resume_trigger_registry.json`
2. `research_state/ironflow_monitor_state.json`

Record timestamp and verdict in the new session directory. Do not poll, issue a network request, re-probe HuggingFace, or repeat this check later in the same session.

The four triggers are `GATE4_BRANCH_1`, `NEW_OBSERVED_LIQUIDATION_SOURCE`, `HL_LABEL_EXTENSION`, and `EXPANSION_ROBUSTNESS_REDO`. A trigger is satisfied only when its registry-defined evidence artifact exists with the required fields. The agent cannot create or mark `GATE4_BRANCH_1` as `RESOLVED_VERIFIED`.

Current state: all four are OPEN; Ironflow is `data_through=2026-10`; 2026-11, 2026-12, and 2027-01 are `CONFIRMED_ABSENT`.

### Phase B — Emit ONE new quantitative artifact (the heavy work)

The trigger check plus unit tests is **not** a heavy session and is not completion. Every session must do exactly one of the following and write the artifact (JSON + MD) into the new session directory:

1. **No trigger fired — FCLR-006 independent recompute (primary, non-skippable; queue item 2).** Recompute B0/B1/C1/C2 24-hour QLIKE on the frozen test window and the paired C2-vs-B1 contrast (secondary: C1-vs-B1, C2-vs-C1) from cached 2026 data. Use `research_state/research_protocol_fclr006.md` (frozen v1.0), `research_state/evaluation_summary_FCLR006.md` (published values), and `research_state/reporting_errata_FCLR006.md` (CI correction). Do not run the canonical `scripts/run_evaluation.py` against the tracked summary; use an independent path or a temporary copy. Write `recompute_fclr006_<UTC>.{json,md}` plus the recompute script.
   - Frozen splits: train `2026-04-01T00:00:00Z..2026-04-24T23:00:00Z`; 7d embargo `2026-04-25..2026-05-01`; val `2026-05-02T00:00:00Z..2026-05-15T23:00:00Z`; 7d embargo `2026-05-16..2026-05-22`; test `2026-05-23T00:00:00Z..2026-08-06T23:00:00Z` (76 days = 2 blocks; block criterion NOT_MET by design — do not relax).
   - Data: `research_state/data_cache/{BTCUSDT,ETHUSDT,BNBUSDT,SOLUSDT,XRPUSDT}_2026_0{4,5,6,7,8}/` (markPriceKlines 1h, indexPriceKlines, premiumIndexKlines, fundingRate). `run_manifest.json` is an LFS pointer; do not use it for splits.
   - Published values to reproduce: B0 `0.518169` (n=9000), B1 `0.527290` (n=8987), C1 `0.620158` (n=8987), C2 `0.882279` (n=8987); C2_vs_B1 mean diff `0.354989`, relative reduction `-67.32%`, paired n `8987`. Errata: summary CI display `[0.168263, 0.591948]` has a wrong "excludes zero: no" flag; corrected published interval `[0.173748, 0.615614]` (excludes zero). Gate remains NOT_MET; FCLR-H001 remains NOT_SUPPORTED. Tolerances: QLIKE abs <= 1e-6; mean diff abs <= 1e-6; relative reduction <= 0.01 pct-points.
2. **No trigger fired — documented fallback only if the FCLR-006 cache is incomplete.** Record the exact missing path/hash, then independently recompute `FCLR-LIQ-010-CONFIRM` from `research_state/fclr_liq_010_confirm_panel_20261113T065953Z.parquet`. The fallback is still heavy work; a trigger check, copied bundle, or prose-only note is not.
3. **Trigger fired:** perform the `RESEARCH_PROMPT.md` §16 admissibility/source audit, instantiate `research_state/session_20261116T035833Z/prereg_template_trigger_gated_20261116T035833Z.json` as a **new** prereg sized per `research_state/session_20261116T100533Z/trigger_readiness_power_calibration_20261116T100533Z.md` (paired_n at or above the anchor `n_required_for_2pct`, >=5 instruments, >=3 non-overlapping 30-day blocks, 7d purge/embargo, prespecified Holm family, `outcome_data_inspected_before_freeze=false`), then execute and record an honest verdict.

### Phase C — Verify and hand off

1. Create `research_state/session_<UTC>/` (never add root md/json).
2. Audit `research_state/session_20261116T100533Z/` and confirm the five required RCA prefixes are present and unmodified; confirm `session_20261116T125624Z/` still holds the FCLR-009 recompute + audit.
3. Write a concise evidence-audit artifact in the new session directory.
4. Run and capture under the new session directory:
   - `python3 scripts/check_handoff_heavywork_gate.py --json`
   - `python3 scripts/check_tracka_scope_registry_drift.py --json`
   - `python3 -m unittest tests.test_active_campaign_gate tests.test_tracka_hardening_117 tests.test_tracka_hardening_118 tests.test_tracka_hardening_143`
   - `python3 -m unittest discover -q` to completion; record final test count, skip count, and process exit status. Never call a timeout green. Revert any timestamp-only tracked-file side effect the suite makes.
5. Update only `AGENT_HANDOFF.md` after the checks, replacing its timestamp/verification section while preserving the sole-handoff contract and the current bundle reference.

A session that only rereads the trigger files, repeats prior prose, copies the old bundle without new analysis, redoes FCLR-009, or records a green suite without a new artifact is incomplete.

## Design-power summary (from `trigger_readiness_power_calibration_20261116T100533Z.md`)

- Only **FCLR-009** (n=24,495, 6 blocks, MDE **1.95%**) was powered for the 2% floor.
- FCLR-002/003/011/013/014 were underpowered (MDE 5.1%–16.4%).
- Track A liquidation recompute (n=593, MDE **8.88%**) needs **~11,689 paired observations** for a 2% MDE.
- Per-trigger sample floors: Gate 4 / Track C `paired_n >= 23,224`; Track A / expansion `paired_n >= 11,689`; all with >=3 blocks and 7d purge/embargo.

## Bottleneck policy

- **Stale instructions:** `NEXT_SESSION_HANDOFF.md`, `NEXT_SESSION_TASK.md`, `HANDOFF_NEXT_SESSION_20261116T114626Z.md`, and `AGENT_HANDOFF_20261115T073240Z.md` have no authority.
- **Incomplete sessions:** `session_20261116T104644Z/` and `session_20261116T105341Z/` are trigger-only; do not resume, copy, or count them as completion.
- **Completed-work confusion:** FCLR-RCA-011 and FCLR-009 are complete; do not rerun them merely because an old note calls them pending.
- **Gate false failure:** the gate accepts a latest new-style session with `evidence_audit_*` + a fresh quantitative artifact while still resolving the complete bundle. Do not weaken this check further.
- **Root churn:** root `research_state/*.md|json` count is 500/500. Keep new outputs in session subdirectories.
- **Dependencies:** the readiness/reproducibility path is stdlib-only; do not add `statsmodels` or other unpinned heavy deps to the core path. Install only missing `requirements.txt` deps when a documented gate needs them.
- **Suite duration:** allow the discovery suite to finish and record its actual exit status; do not substitute a partial run.
- **External science:** if no trigger fires, the required progress is the new FCLR-006 artifact (or documented LIQ-010 fallback), evidence audit, complete gate run, and accurate handoff update. Repeated polling and new confirmatory estimands on exhausted cached data are forbidden.

## Verification record — 2026-11-16T13:45:00Z

- Handoff maintenance: initial task message refreshed from completed FCLR-009 to FCLR-006 (queue item 2); `session_20261116T125624Z` record claim corrected (four files, no suite capture).
- `python3 scripts/check_handoff_heavywork_gate.py --json`: **PASS**; `heavy_session=session_20261116T100533Z`, `latest_session=session_20261116T125624Z`, `root=500/500`, `reason=OK`, EXIT 0.
- `python3 scripts/check_tracka_scope_registry_drift.py --json`: **PASS**; 196/196 scripts, EXIT 0.
- Targeted tests (`test_active_campaign_gate`, `test_tracka_hardening_117`, `test_tracka_hardening_118`, `test_tracka_hardening_143`): 52 tests OK, EXIT 0; `git status` clean afterwards.
- No new heavy research artifact was produced by this maintenance session; the next session must produce the FCLR-006 recompute (or documented LIQ-010 fallback) artifact and the full discovery-suite capture.

## Session closeout

- [ ] Trigger registry and monitor state checked once; verdict recorded.
- [ ] New `research_state/session_<UTC>/` created.
- [ ] One new quantitative artifact produced (FCLR-006 recompute or documented LIQ-010 fallback).
- [ ] Carried-forward `session_20261116T100533Z` bundle and `session_20261116T125624Z` FCLR-009 recompute verified.
- [ ] Gate JSON outputs and full-suite final result recorded under the new session directory.
- [ ] Root md/json count remains at most 500.
- [ ] `AGENT_HANDOFF.md` updated with the new timestamp, new-artifact result, gate results, and remaining external blockers.

Stop cleanly only when every box is checked. Never leave the suite red, never delete the rank-0 sentinel, and never claim completion from a trigger-only or copied-bundle-only check alone.