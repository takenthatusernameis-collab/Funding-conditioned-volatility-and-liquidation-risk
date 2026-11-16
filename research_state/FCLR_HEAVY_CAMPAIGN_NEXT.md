# FCLR Focus Campaign — Trigger-Only — current as of 2026-11-16T09:54:52Z

**Frontier rank 0:** `FCLR-BOUNDED-TRIGGER-ONLY-20261115T220000Z` (`TRIGGER_ONLY` / `BOUNDED_TRIGGER_ONLY`, `all_terminal=true`, `next_action_heavy=null`).
**Sole handoff:** `AGENT_HANDOFF.md`. This file is the detailed campaign note referenced by the frontier and the handoff.
**Governing rules:** `RESEARCH_PROMPT.md`. Never re-run concluded estimands, re-score sealed results, fabricate data, edit `.github/workflows/*`, poll, re-probe the HuggingFace tree, or use paid/credentialed/manual outcome data.
**Artifact rule:** write every new artifact to a new `research_state/session_<UTC>/`. The `research_state/` root is at 498/500 md/json; adding root files breaks the enforced churn cap.

## Current classification

The former FCLR-RCA-011 heavy campaign is **COMPLETE**, not pending. Its self-contained evidence bundle is `research_state/session_20261116T035833Z/` and contains all required Phase-B/C artifacts:

- `rca011_feature_attribution_20261116T035833Z.{json,md}`
- `rca011_impl_crosscheck_20261116T035833Z.json`
- `rca011_sealed_bridge_20261116T035833Z.md` and `_ext`
- `prereg_template_trigger_gated_20261116T035833Z.json`
- `program_power_synthesis_20261116T035833Z.{json,md}`

The RCA found that the sealed FCLR-011 PASS is not independently reproduced. The clean recompute gives C2 versus B1 at **-294.01%**, versus the sealed **+4.94%**. Funding attribution is **-342.67%**; EMA24 attribution is **+9.75%**; the joint result is **-294.01%**. Independent OLS and `lstsq` paths agree to numerical precision, so this is not a solver artifact. The fit has only 152 complete training rows after purge/dropna, making the result fragile and non-promotable. Do not delete or replace this bundle without first installing a complete successor bundle.

## Non-skippable execution contract

### Phase A — Check external triggers once

Read only these files at session start:

1. `research_state/resume_trigger_registry.json`
2. `research_state/ironflow_monitor_state.json`

Record the timestamp and verdict in the new session directory. Do not poll, issue a network request, re-probe HuggingFace, or repeat this check later in the same session.

The four triggers are `GATE4_BRANCH_1`, `NEW_OBSERVED_LIQUIDATION_SOURCE`, `HL_LABEL_EXTENSION`, and `EXPANSION_ROBUSTNESS_REDO`. A trigger is satisfied only when its registry-defined evidence artifact exists with the required fields. The agent cannot create or mark `GATE4_BRANCH_1` as `RESOLVED_VERIFIED`.

Current state: all four are OPEN; Ironflow is `data_through=2026-10`; 2026-11, 2026-12, and 2027-01 are `CONFIRMED_ABSENT`.

### Phase B — Preserve and verify the completed heavy evidence

The trigger check plus unit tests is **not** a heavy session and is not completion. Every session must do all of the following:

1. Create `research_state/session_<UTC>/`.
2. Verify `research_state/session_20261116T035833Z/` exists and contains every required RCA prefix above.
3. Record a concise evidence audit in the new session directory, including the bundle path, the five required artifact families, and the observed result that the RCA is complete.
4. Run:
   - `python3 scripts/check_handoff_heavywork_gate.py --json`
   - `python3 scripts/check_tracka_scope_registry_drift.py --json`
   - `python3 -m unittest tests.test_active_campaign_gate tests.test_tracka_hardening_117 tests.test_tracka_hardening_118 tests.test_tracka_hardening_143`
   - `python3 -m unittest discover -q` to completion; record the final test count, skip count, and process exit status. Never call a timeout green.
5. Save the command outputs under the new session directory, not in the `research_state/` root.
6. Update only `AGENT_HANDOFF.md` after the checks, replacing its timestamp/verification section while preserving the sole-handoff contract and the latest complete heavy-session reference.

A session that only rereads the trigger files, repeats prior prose, or records a green suite without the evidence audit and new-session outputs is incomplete. Do not claim completion from prose alone.

### Phase C — Trigger-gated advance

Advance scientifically only when a trigger is satisfied with its required evidence artifact. Before any outcome inspection:

1. Perform the `RESEARCH_PROMPT.md` §16 admissibility/source audit.
2. Instantiate `research_state/session_20261116T035833Z/prereg_template_trigger_gated_20261116T035833Z.json` as a new prereg with a unique experiment id and UTC timestamp.
3. Require a materially different estimand, at least five paired OOS instruments, at least three non-overlapping 30-day test blocks, a prespecified Holm family, seven-day purge/embargo, and a target MDE below the 2% materiality floor.
4. Set `outcome_data_inspected_before_freeze=false`.
5. Write the prereg and admissibility artifacts under a fresh `research_state/session_<UTC>/` before evaluating outcomes.
6. Execute the frozen design, run all gates, register any new scripts in both scope registries, and update the frontier/hypothesis registries with an honest verdict.
7. Write a new complete heavy bundle in the same session directory and update the handoff reference only after that bundle is complete.

Never promote a result that fails any preregistered criterion. Preserve null, negative, and inconclusive verdicts.

## Bottleneck policy

- **Stale instructions:** `NEXT_SESSION_HANDOFF.md`, `NEXT_SESSION_TASK.md`, and `AGENT_HANDOFF_20261115T073240Z.md` have no authority. Do not execute their historical campaigns.
- **Completed-work confusion:** FCLR-RCA-011 is complete; do not rerun it merely because an old note calls it pending.
- **Root churn:** root `research_state/*.md|json` count is 498/500. Keep new outputs in session subdirectories.
- **Dependencies:** install only missing dependencies from `requirements.txt` when required to run the documented gates.
- **Suite duration:** allow the discovery suite to finish and record its actual exit status; do not substitute a partial run.
- **External science:** if no trigger fires, the required progress is the evidence audit, complete gate run, and an accurate handoff update. Repeated polling and new confirmatory estimands on exhausted cached data are forbidden.

## Verification record — 2026-11-16T09:54:52Z

- Trigger check: all four triggers OPEN; Ironflow `data_through=2026-10`; 2026-11/2026-12/2027-01 CONFIRMED_ABSENT.
- Heavy-work gate: PASS for `session_20261116T035833Z`; root count 498/500.
- Scope drift: PASS (196 scripts, 196 registry entries).
- Targeted tests: 51 OK.
- Full discovery suite: completed, 1354 tests, OK (skipped=1), final EXIT 0.
- No network probe, polling, sealed mutation, or new confirmatory estimand.

## Session closeout

- [ ] Trigger registry and monitor state checked once; verdict recorded.
- [ ] New `research_state/session_<UTC>/` created.
- [ ] Completed `session_20261116T035833Z` bundle and all five artifact families verified.
- [ ] Gate JSON outputs and full-suite final result recorded under the new session directory.
- [ ] Root md/json count remains at most 500.
- [ ] `AGENT_HANDOFF.md` updated with the new timestamp, evidence-audit result, gate results, and remaining external blockers.

Stop cleanly only when every box is checked. Never leave the suite red, never delete the rank-0 sentinel, and never claim completion from a trigger-only check alone.