# FCLR Focus Campaign — `FCLR-REPRO-AUDIT-02` — current as of 2026-11-16T12:45:00Z

**Frontier rank 0:** `FCLR-BOUNDED-TRIGGER-ONLY-20261115T220000Z` (`TRIGGER_ONLY` / `BOUNDED_TRIGGER_ONLY`, `all_terminal=true`, `next_action_heavy=null`).
**Sole handoff:** `AGENT_HANDOFF.md`. This file is the detailed campaign note referenced by the frontier and the handoff.
**Governing rules:** `RESEARCH_PROMPT.md`. Never re-run concluded estimands, re-score sealed results, fabricate data, edit `.github/workflows/*`, poll, re-probe the HuggingFace tree, or use paid/credentialed/manual outcome data.
**Artifact rule:** write every new artifact to a new `research_state/session_<UTC>/`. The `research_state/` root is at 500/500 md/json; adding root files breaks the enforced churn cap.

## Why this campaign exists (bottlenecks removed)

The previous `FCLR-READINESS-01` campaign was complete: it precomputed per-trigger design power and produced the FCLR-011 third independent recompute. Two sessions were left trigger-only (`session_20261116T104644Z/` and `session_20261116T105341Z/`); they are incomplete and must not be resumed or copied. The remaining agent-removable work is not more static audits: it is an independent reproducibility audit of the terminal headlines, starting with FCLR-009, the only adequately powered Track C null.

`FCLR-REPRO-AUDIT-02` makes the heavy-work gate a **floor** and requires every session to emit a *new* quantitative artifact. It also removes the false gate failure caused by the old gate demanding the static Phase-B bundle inside the latest audit session.

## Current classification

The former FCLR-RCA-011 heavy campaign is **COMPLETE**. Its evidence bundle is `research_state/session_20261116T035833Z/`, carried forward unmodified into `research_state/session_20261116T100533Z/` (the current self-contained bundle). It contains all required Phase-B/C artifacts:

- `rca011_feature_attribution_20261116T035833Z.{json,md}`
- `rca011_impl_crosscheck_20261116T035833Z.json`
- `rca011_sealed_bridge_20261116T035833Z.md` and `_ext`
- `prereg_template_trigger_gated_20261116T035833Z.json`
- `program_power_synthesis_20261116T035833Z.{json,md}`

The latest heavy session is `research_state/session_20261116T115028Z/`: `independent_recompute_fclr011_20261116T115028Z.{json,md}` + `independent_recompute_fclr011.py` + `evidence_audit_20261116T115028Z.md`. It triple-confirmed the sealed FCLR-011 PASS is not reproducible (clean recompute **-294.01%** vs sealed **+4.94%**), with funding increment **-342.67%**, EMA24 **+9.75%**, joint **-294.01%**; only 152 complete training rows. Do not delete or replace this bundle without first installing a complete successor bundle.

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

1. **No trigger fired — FCLR-009 independent recompute (primary, non-skippable).** Recompute B1/C1/C2 24-hour QLIKE on the frozen test window and the paired C2-vs-B1 contrast from cached 2025 data. Use `research_state/research_protocol_fclr009.md` and `research_state/evaluation_summary_FCLR-009.md` for frozen splits and published values; `research_state/run_manifest.json` is an LFS pointer and must not be used as the split source. Do not run the canonical `scripts/run_evaluation.py` against the tracked summary; use an independent path or a temporary copy. Write `recompute_fclr009_<UTC>.{json,md}` plus the recompute script.
   - Frozen splits: train `2025-01-01..2025-04-05`, val `2025-04-13..2025-05-31`, test `2025-06-08..2025-12-31`; 7-day purge/embargo.
   - Data: `research_state/data_cache/{BTCUSDT,ETHUSDT,BNBUSDT,SOLUSDT,XRPUSDT}_2025_*/`.
   - Published values to reproduce: B0 `0.367906` (n=24,648), B1 `0.340756` (n=24,495), C1 `0.339628`, C2 `0.342205`; C2-vs-B1 mean diff `0.001449`, relative `-0.43%`, 95% CI `[-0.003120, 0.006165]`. Tolerance: QLIKE abs <= 1e-6; rel% <= 0.01 pct-points.
2. **No trigger fired — documented fallback only if the FCLR-009 cache is incomplete.** Record the exact missing path/hash, then independently recompute `FCLR-LIQ-010-CONFIRM` from `research_state/fclr_liq_010_confirm_panel_20261113T065953Z.parquet`. The fallback is still heavy work; a trigger check, copied bundle, or prose-only note is not.
3. **Trigger fired:** perform the `RESEARCH_PROMPT.md` §16 admissibility/source audit, instantiate `research_state/session_20261116T035833Z/prereg_template_trigger_gated_20261116T035833Z.json` as a **new** prereg sized per `research_state/session_20261116T100533Z/trigger_readiness_power_calibration_20261116T100533Z.md` (paired_n at or above the anchor `n_required_for_2pct`, >=5 instruments, >=3 non-overlapping 30-day blocks, 7d purge/embargo, prespecified Holm family, `outcome_data_inspected_before_freeze=false`), then execute and record an honest verdict.

### Phase C — Verify and hand off

1. Create `research_state/session_<UTC>/` (never add root md/json).
2. Audit `research_state/session_20261116T100533Z/` and confirm the five required RCA prefixes are present and unmodified.
3. Write a concise evidence-audit artifact in the new session directory.
4. Run and capture under the new session directory:
   - `python3 scripts/check_handoff_heavywork_gate.py --json`
   - `python3 scripts/check_tracka_scope_registry_drift.py --json`
   - `python3 -m unittest tests.test_active_campaign_gate tests.test_tracka_hardening_117 tests.test_tracka_hardening_118 tests.test_tracka_hardening_143`
   - `python3 -m unittest discover -q` to completion; record final test count, skip count, and process exit status. Never call a timeout green. Revert any timestamp-only tracked-file side effect the suite makes.
5. Update only `AGENT_HANDOFF.md` after the checks, replacing its timestamp/verification section while preserving the sole-handoff contract and the current bundle reference.

A session that only rereads the trigger files, repeats prior prose, copies the old bundle without new analysis, or records a green suite without a new artifact is incomplete.

## Design-power summary (from `trigger_readiness_power_calibration_20261116T100533Z.md`)

- Only **FCLR-009** (n=24,495, 6 blocks, MDE **1.95%**) was powered for the 2% floor.
- FCLR-002/003/011/013/014 were underpowered (MDE 5.1%–16.4%).
- Track A liquidation recompute (n=593, MDE **8.88%**) needs **~11,689 paired observations** for a 2% MDE.
- Per-trigger sample floors: Gate 4 / Track C `paired_n >= 23,224`; Track A / expansion `paired_n >= 11,689`; all with >=3 blocks and 7d purge/embargo.

## Bottleneck policy

- **Stale instructions:** `NEXT_SESSION_HANDOFF.md`, `NEXT_SESSION_TASK.md`, `HANDOFF_NEXT_SESSION_20261116T114626Z.md`, and `AGENT_HANDOFF_20261115T073240Z.md` have no authority.
- **Incomplete sessions:** `session_20261116T104644Z/` and `session_20261116T105341Z/` are trigger-only; do not resume, copy, or count them as completion.
- **Completed-work confusion:** FCLR-RCA-011 is complete; do not rerun it merely because an old note calls it pending.
- **Gate false failure:** the gate now accepts a latest new-style session with `evidence_audit_*` + a fresh quantitative artifact while still resolving the complete bundle. Do not weaken this check further.
- **Root churn:** root `research_state/*.md|json` count is 500/500. Keep new outputs in session subdirectories.
- **Dependencies:** the readiness/reproducibility path is stdlib-only; do not add `statsmodels` or other unpinned heavy deps to the core path. Install only missing `requirements.txt` deps when a documented gate needs them.
- **Suite duration:** allow the discovery suite to finish and record its actual exit status; do not substitute a partial run.
- **External science:** if no trigger fires, the required progress is the new FCLR-009 artifact (or documented LIQ-010 fallback), evidence audit, complete gate run, and accurate handoff update. Repeated polling and new confirmatory estimands on exhausted cached data are forbidden.

## Verification record — 2026-11-16T12:45:00Z

- Handoff gate fixed and verified: `python3 scripts/check_handoff_heavywork_gate.py --json` PASS; `heavy_session=session_20261116T100533Z`, `latest_session=session_20261116T115028Z`, `root=500/500`, `reason=OK`, EXIT 0.
- `python3 -m unittest tests.test_tracka_hardening_143`: 14 tests OK, EXIT 0.
- No new heavy research artifact was produced by this maintenance session; the next session must produce the FCLR-009 recompute (or documented fallback) artifact.

## Session closeout

- [ ] Trigger registry and monitor state checked once; verdict recorded.
- [ ] New `research_state/session_<UTC>/` created.
- [ ] One new quantitative artifact produced (FCLR-009 recompute or documented LIQ-010 fallback).
- [ ] Carried-forward `session_20261116T100533Z` bundle and all five artifact families verified.
- [ ] Gate JSON outputs and full-suite final result recorded under the new session directory.
- [ ] Root md/json count remains at most 500.
- [ ] `AGENT_HANDOFF.md` updated with the new timestamp, new-artifact result, gate results, and remaining external blockers.

Stop cleanly only when every box is checked. Never leave the suite red, never delete the rank-0 sentinel, and never claim completion from a trigger-only or copied-bundle-only check alone.