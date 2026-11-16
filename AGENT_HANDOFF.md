# AGENT HANDOFF — 2026-11-16T04:54:04Z (sole durable handoff)

## INITIAL TASK MESSAGE FOR NEXT AGENTIC WORK SESSION
**Priority (repo: Funding-conditioned-volatility-and-liquidation-risk):** All cached-data confirmatory estimands are terminal and the rank-0 sentinel `FCLR-BOUNDED-TRIGGER-ONLY-20261115T220000Z` (TRIGGER_ONLY / BOUNDED_TRIGGER_ONLY) is active. The heavy FCLR-RCA-011 reproducibility/integrity campaign is COMPLETE. This session I removed the **last structural bottleneck**: the mandated heavy work was prose-only, so a future session could "finish" by running only the trigger check + the unit suite. That is now impossible — a new deterministic, test-enforced gate (`scripts/check_handoff_heavywork_gate.py`, `tests/test_tracka_hardening_143.py`) fails the suite if the durable handoff is missing its task section, if the recorded heavy-session bundle lacks the Phase-B/C evidence, or if the root churn cap is breached.

**Your non-skippable job (do ALL of it, in order):**
1. **Trigger check ONCE, no re-poll.** Read `research_state/resume_trigger_registry.json` + `research_state/ironflow_monitor_state.json`. Confirm `data_through=2026-10` and 2026-11..2027-01 absent. Do NOT re-probe the HuggingFace tree (probes already == 2). If a trigger is satisfied with its required evidence artifact, jump to the campaign's Phase D.
2. **Run the new handoff gate and the deterministic gates — record exact output in this file:**
   ```bash
   python3 scripts/check_handoff_heavywork_gate.py
   python3 scripts/check_tracka_scope_registry_drift.py
   python3 -m unittest tests.test_active_campaign_gate tests.test_tracka_hardening_117 tests.test_tracka_hardening_118 tests.test_tracka_hardening_143
   python3 -m unittest discover -q
   ```
3. **Heavy work is gated, not optional.** `tests/test_tracka_hardening_143.py` is part of `discover -q`; it asserts the handoff points at a self-contained `session_<UTC>/` bundle with `rca011_feature_attribution_*`, `rca011_impl_crosscheck_*`, `rca011_sealed_bridge_*`, `prereg_template_trigger_gated_*`, and `program_power_synthesis_*`. If you write a NEW heavy session, write the same artifact set under `research_state/session_<newUTC>/` and update the `session_<UTC>` reference below. If you do NOT advance the science, you MUST still keep this gate green (it already is).

**Do NOT:** start a new confirmatory estimand on cached data; re-run concluded/sealed cells; mutate sealed artifacts; edit `.github/workflows/*`; add root-level `research_state/*.md|json` (root is 498/500 — write only into `research_state/session_<UTC>/`); fabricate data/outcomes; poll.

### Heavy-session evidence (authoritative, on disk)
Latest self-contained heavy bundle: `research_state/session_20261116T035833Z/` — contains the complete Phase-B/C set:
- `rca011_feature_attribution_20261116T035833Z.{json,md}` — B1_plus_funding vs B1 **-342.67%** (CI [-497.48,-221.27]); B1_plus_ema24 vs B1 **+9.75%**; joint vs B1 **-294.01%**. Funding augmentation drives recompute harm.
- `rca011_impl_crosscheck_20261116T035833Z.json` — statsmodels.OLS vs numpy.linalg.lstsq parity (~1e-12–1e-17); no solver/smearing artifact.
- `rca011_sealed_bridge_20261116T035833Z.md` (+ `rca011_sealed_bridge_ext_20261116T035833Z.md`) — sealed PASS (+4.94%) not reproduced by clean recompute (-294.01%); +120-row eligibility delta; sealed panel LFS pointer unauditable here.
- `prereg_template_trigger_gated_20261116T035833Z.json` — power-remediation prereg skeleton (>=3 non-overlapping 30d blocks, MDE < 2% floor, Holm family, `outcome_data_inspected_before_freeze=false`).
- `program_power_synthesis_20261116T035833Z.{json,md}` — FCLR-011 classification: **(c) feature/back-transform/artifact-driven integrity failure with underpowered/unstable training fit (152 complete train rows)**; sealed PASS not independently reproduced / not promotable. `next_action_heavy=null`.

(The Phase-B set was consolidated into `session_20261116T035833Z/` this session; originals remain in `session_20261116T023837Z/`.)

### This session's change (2026-11-16T04:54:04Z) — bottleneck removed
- **New gate:** `scripts/check_handoff_heavywork_gate.py` (class `resume_gate_infra`, read-only, no network, no writes). Fails closed with machine-readable reasons (`HANDOFF_MISSING`, `HANDOFF_MARKERS_MISSING`, `HEAVY_SESSION_ID_UNRECORDED`, `HEAVY_SESSION_DIR_MISSING`, `HEAVY_SESSION_ARTIFACTS_MISSING`, `ROOT_COUNT_EXCEEDS_CAP`).
- **New test:** `tests/test_tracka_hardening_143.py` (13 tests, OK) — pins the gate to pass on the real repo and to fail closed on every missing/incomplete condition (tmp-isolated).
- **Registry sync:** `check_handoff_heavywork_gate.py` added to `research_state/tracka_script_scope_registry.json` (196/196) and `tests/test_tracka_hardening_117.py::SCRIPT_REGISTRY`. Drift PASS, 118 sync OK.
- **Consolidation:** copied `prereg_template_trigger_gated_*` + `rca011_sealed_bridge_*` into `session_20261116T035833Z/` so the latest heavy bundle is self-contained (no root files added; root count still 498/500).
- **No** frontier/hypothesis/registry mutation, **no** sealed-artifact mutation, **no** `.github/workflows/*` edits, **no** commit.

### Current gate/program state (authoritative)
- **Frontier rank 0:** `FCLR-BOUNDED-TRIGGER-ONLY-20261115T220000Z`, TRIGGER_ONLY / BOUNDED_TRIGGER_ONLY, `all_terminal=true`, `next_action_heavy=null`.
- **FCLR-H001 / FCLR-009:** complete, **NOT_MET** (`research_state/evaluation_summary_FCLR-009.md`); do not rerun.
- **FCLR-011:** sealed PASS **not independently reproduced**; recompute harm attributable to funding augmentation; fragile/non-promotable.
- **Track A:** no new admissible observed-liquidation data (ironflow through 2026-10). **Track B:** sealed NOT_SUPPORTED. **Track C:** terminal on cached confirmatory designs. **H2:** EXPLORATORY_ONLY, not promotable.
- **Gate 4 Branch 1:** blocked on human/legal attestation (agent cannot set RESOLVED_VERIFIED).

### Blockers & commands/results (record exact output when you run)
- **No open blockers.** Structural: all 4 resume triggers OPEN; no agent-removable confirmatory estimand on cached data.
- **Verified this session:** `check_handoff_heavywork_gate.py` PASS (`root=498/500`, heavy_session=session_20261116T035833Z, session_ok=True); drift PASS (`scripts=196 registry=196`); guards+143 = 51 tests OK; root md+json = 498/500.
- Full `discover -q` was last recorded green in the prior session (**1341 OK, skipped=1**). Re-run and record the new count here.

### Next materially different free route
Hold TRIGGER_ONLY with the gate green. Advance ONLY on a satisfied external trigger with §16 admissibility audit + NEW pre-outcomes prereg (materially different estimand, >=3 non-overlapping 30d blocks, MDE below 2% floor, Holm family). On advance, write a fresh `session_<UTC>/` heavy bundle (same artifact set the gate enforces) and update the `session_<UTC>` reference in this file.

## Tombstones (no authority)
- `NEXT_SESSION_HANDOFF.md`, `NEXT_SESSION_TASK.md`: tombstoned 2026-11-15T22:57:29Z.
- `AGENT_HANDOFF_20261115T073240Z.md`: SUPERSEDED — ignore.