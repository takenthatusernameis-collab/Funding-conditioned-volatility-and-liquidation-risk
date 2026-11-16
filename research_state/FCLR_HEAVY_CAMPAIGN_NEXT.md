# FCLR Focus Campaign — `FCLR-READINESS-01` — current as of 2026-11-16T10:05:33Z

**Frontier rank 0:** `FCLR-BOUNDED-TRIGGER-ONLY-20261115T220000Z` (`TRIGGER_ONLY` / `BOUNDED_TRIGGER_ONLY`, `all_terminal=true`, `next_action_heavy=null`).
**Sole handoff:** `AGENT_HANDOFF.md`. This file is the detailed campaign note referenced by the frontier and the handoff.
**Governing rules:** `RESEARCH_PROMPT.md`. Never re-run concluded estimands, re-score sealed results, fabricate data, edit `.github/workflows/*`, poll, re-probe the HuggingFace tree, or use paid/credentialed/manual outcome data.
**Artifact rule:** write every new artifact to a new `research_state/session_<UTC>/`. The `research_state/` root is at 498/500 md/json; adding root files breaks the enforced churn cap.

## Why this campaign exists (bottleneck removed)

The previous campaign defined "heavy work" as re-auditing a static bundle and re-running gates. That is repeatable forever with no new science, so a future session could "complete" without doing heavy work. `FCLR-READINESS-01` makes the heavy-work gate a **floor** and requires every session to emit a **new quantitative artifact**. It also pre-computes design power per trigger so a firing trigger executes an already-sized prereg instead of improvising one.

## Current classification

The former FCLR-RCA-011 heavy campaign is **COMPLETE**. Its evidence bundle is `research_state/session_20261116T035833Z/` and is carried forward unmodified into `research_state/session_20261116T100533Z/` (the current self-contained bundle). It contains all required Phase-B/C artifacts:

- `rca011_feature_attribution_20261116T035833Z.{json,md}`
- `rca011_impl_crosscheck_20261116T035833Z.json`
- `rca011_sealed_bridge_20261116T035833Z.md` and `_ext`
- `prereg_template_trigger_gated_20261116T035833Z.json`
- `program_power_synthesis_20261116T035833Z.{json,md}`

The RCA found the sealed FCLR-011 PASS is not independently reproduced (clean recompute **-294.01%** vs sealed **+4.94%**); funding attribution **-342.67%**, EMA24 **+9.75%**, joint **-294.01%**; independent OLS/`lstsq` paths agree to numerical precision; the fit has only **152** complete training rows, so the result is fragile/non-promotable. Do not delete or replace this bundle without first installing a complete successor bundle.

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

1. **Trigger fired:** perform the `RESEARCH_PROMPT.md` §16 admissibility/source audit, instantiate `research_state/session_20261116T035833Z/prereg_template_trigger_gated_20261116T035833Z.json` as a **new** prereg sized per `research_state/session_20261116T100533Z/trigger_readiness_power_calibration_20261116T100533Z.md` (paired_n at or above the anchor `n_required_for_2pct`, >=5 instruments, >=3 non-overlapping 30-day blocks, 7d purge/embargo, prespecified Holm family, `outcome_data_inspected_before_freeze=false`), then execute and record an honest verdict.
2. **No trigger fired — power-ledger refresh:** extend `trigger_readiness_power_calibration_*` with any newly published primary contrast (new row + new source citation only; never overwrite a historical row) and recompute MDE / n_required.
3. **No trigger fired — independent recomputation:** re-derive a terminal headline from its stored panel/config using an independent path (e.g. numpy-only OLS) and assert agreement within a declared tolerance; record the comparison.

A prose-only restatement of prior findings, a copied-bundle-only session, or a trigger-check-only session does **not** satisfy Phase B.

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

- **Stale instructions:** `NEXT_SESSION_HANDOFF.md`, `NEXT_SESSION_TASK.md`, and `AGENT_HANDOFF_20261115T073240Z.md` have no authority.
- **Completed-work confusion:** FCLR-RCA-011 is complete; do not rerun it merely because an old note calls it pending.
- **Root churn:** root `research_state/*.md|json` count is 498/500. Keep new outputs in session subdirectories.
- **Dependencies:** the readiness/reproducibility path is stdlib-only; do not add `statsmodels` or other unpinned heavy deps to the core path. Install only missing `requirements.txt` deps when a documented gate needs them.
- **Suite duration:** allow the discovery suite to finish and record its actual exit status; do not substitute a partial run.
- **External science:** if no trigger fires, the required progress is the new quantitative artifact, evidence audit, complete gate run, and accurate handoff update. Repeated polling and new confirmatory estimands on exhausted cached data are forbidden.

## Verification record — 2026-11-16T10:05:33Z

- Trigger check: all four triggers OPEN; Ironflow `data_through=2026-10`; 2026-11/2026-12/2027-01 CONFIRMED_ABSENT.
- New heavy artifact: `session_20261116T100533Z/trigger_readiness_power_calibration_20261116T100533Z.{json,md}` (offline design-power ledger).
- Heavy-work gate: PASS for `session_20261116T100533Z`; root count 498/500.
- Scope drift: PASS (196 scripts, 196 registry entries).
- Targeted tests: 51 OK.
- Full discovery suite: completed, 1354 tests, OK (skipped=1), 343.113s, final EXIT 0.
- No network probe, polling, sealed mutation, or new confirmatory estimand.

## Session closeout

- [ ] Trigger registry and monitor state checked once; verdict recorded.
- [ ] New `research_state/session_<UTC>/` created.
- [ ] One new quantitative artifact produced (power-ledger refresh / trigger execution / independent recomputation).
- [ ] Carried-forward `session_20261116T100533Z` bundle and all five artifact families verified.
- [ ] Gate JSON outputs and full-suite final result recorded under the new session directory.
- [ ] Root md/json count remains at most 500.
- [ ] `AGENT_HANDOFF.md` updated with the new timestamp, new-artifact result, gate results, and remaining external blockers.

Stop cleanly only when every box is checked. Never leave the suite red, never delete the rank-0 sentinel, and never claim completion from a trigger-only or copied-bundle-only check alone.