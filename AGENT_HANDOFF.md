# AGENT HANDOFF — 2026-11-16T11:47:50Z (sole durable handoff)

## INITIAL TASK MESSAGE FOR NEXT AGENTIC WORK SESSION

**Priority 0 — repository and rank-0 state.** Repository: `Funding-conditioned-volatility-and-liquidation-risk` — funding-conditioned volatility and liquidation risk. Program status: `CLOSED_TERMINAL` (final structural closure `research_state/fclr_final_structural_closure_20261116T114626.{md,json}`; terminal verdict `NO_CLAIM_WORTHY_RESULT_PROMOTABLE; ALL_P1_P2_P3_SEALED`; all P1/P2/P3 sealed; no feasible 3-block pre-registered design in any domain). Rank-0 campaign `FCLR-BOUNDED-TRIGGER-ONLY-20261115T220000Z` (`TRIGGER_ONLY` / `BOUNDED_TRIGGER_ONLY`, `all_terminal=true`, `next_action_heavy=null`). All cached-data confirmatory estimands are terminal. Sealed FCLR-011 PASS was not independently reproduced (clean recompute C2 vs B1 **-294.01%** vs sealed **+4.94%**); fragile/non-promotable. Track B `NOT_SUPPORTED`; Track C cached confirmatory designs terminal; H2 (Shek) `EXPLORATORY_ONLY`.

**Read these first, in order:**
1. `research_state/resume_trigger_registry.json`
2. `research_state/ironflow_monitor_state.json`
3. `research_state/FCLR_HEAVY_CAMPAIGN_NEXT.md`
4. `research_state/session_20261116T100533Z/trigger_readiness_power_calibration_20261116T100533Z.md`

**Mandatory next-session sequence — campaign `FCLR-READINESS-01` (trigger-readiness + reproducibility hardening).** This is the bounded heavy-work campaign that operates inside the `TRIGGER_ONLY` sentinel. Do all steps in order. A trigger check plus unit tests is **not** a heavy session and is **not** completion.

1. **Create a new evidence directory** `research_state/session_<UTC>/` using the actual session UTC. Do not add files to the `research_state/` root: it is at **500/500** md/json and the cap is fail-closed. All new artifacts go into the new session subdirectory only.
2. **Check triggers exactly once, without network access or polling.** Read the two trigger files above. Record timestamp, each trigger status, `data_through`, and the post-2026-10 month classifications in the new session directory. Current state: all four triggers `OPEN`; Ironflow `data_through=2026-10`; 2026-11, 2026-12, 2027-01 `CONFIRMED_ABSENT`. Do not re-probe HuggingFace, run a monitor, or repeat the trigger check later in the same session.
3. **Produce ONE new quantitative artifact (this is the non-skippable heavy work).** Choose the highest-value item that applies, in this order:
   - **(a) If a trigger fired** (its registry-defined evidence artifact now exists with required fields): instantiate `research_state/session_20261116T035833Z/prereg_template_trigger_gated_20261116T035833Z.json` as a **new** prereg in the new session directory, sized per `trigger_readiness_power_calibration_*` (paired_n at or above the anchor `n_required_for_2pct`, >=5 instruments, >=3 non-overlapping 30-day blocks, 7-day purge/embargo, prespecified Holm family, `outcome_data_inspected_before_freeze=false`), then execute and record an honest verdict.
   - **(b) If no trigger fired:** refresh and extend the trigger-readiness power ledger with any newly published primary contrast (new row + new source citation only; never overwrite a historical row), OR perform an independent numpy-only recomputation of a terminal headline from its stored panel/config and assert agreement within a declared tolerance.
   - Write the artifact (JSON + MD) into the new session directory. A prose-only restatement of prior findings does not satisfy this step.
4. **Audit the carried-forward heavy evidence bundle.** Confirm `research_state/session_20261116T100533Z/` still contains the five required artifact families (`rca011_feature_attribution_*`, `rca011_impl_crosscheck_*`, `rca011_sealed_bridge_*`, `prereg_template_trigger_gated_*`, `program_power_synthesis_*`) and that this session's copy in `session_20261116T035833Z/` is present and unmodified. Write a concise evidence-audit artifact in the new session directory recording the bundle path, families found, and the integrity conclusion (RCA complete; FCLR-011 not reproducible/promotable; attribution fit only 152 complete training rows; `next_action_heavy=null` on cached data). Do not rerun FCLR-RCA-011 merely because an old note calls it pending.
5. **Run and capture every required gate under the new session directory:**
   - `python3 scripts/check_handoff_heavywork_gate.py --json` — must PASS with the complete `session_20261116T100533Z` bundle and root count at most 500.
   - `python3 scripts/check_tracka_scope_registry_drift.py --json` — must PASS.
   - `python3 -m unittest tests.test_active_campaign_gate tests.test_tracka_hardening_117 tests.test_tracka_hardening_118 tests.test_tracka_hardening_143` — must pass all targeted tests.
   - `python3 -m unittest discover -q` — run to completion; record exact test count, skip count, and final process EXIT. Never treat a timeout or monitor cap as green. Revert any timestamp-only side effect the suite makes to tracked files (e.g. `research_state/ironflow_fastpath_cache.json`).
6. **Update only this handoff** after steps 3-5: replace the timestamp/verification section with the actual new timestamp and results. Keep this initial task message, the sole-handoff declaration, the carried-forward bundle reference, and the external blockers intact. Do not create another handoff file and do not execute any tombstoned instruction.

**Trigger-gated science is the only scientific advance — but it must be pre-powered.** If no trigger is satisfied, do not advance or re-run a confirmatory estimand. The required holding action is the new quantitative artifact (step 3b) plus the evidence audit, complete gate run, and accurate handoff update. If a trigger is satisfied, follow step 3a: §16 admissibility/source audit first, freeze the pre-sized prereg before inspecting outcomes, require a materially different estimand and the power ledger's sample floor, then execute, register any new scripts in both scope registries, run all gates, and update the frontier/hypothesis registries with an honest verdict.

**Heavy-work mandate (future agents cannot avoid this):** Completion of any session under this handoff requires a *new* `research_state/session_<UTC>/` containing a *new* quantitative artifact. Re-auditing the static bundle, re-running gates alone, or a trigger-check-only session is explicitly **not** completion. The gate is a floor; the new artifact is the requirement.

**Heavy-work evidence on disk (authoritative).** The current self-contained bundle is `research_state/session_20261116T100533Z/`:
- Carried forward unmodified from `session_20261116T035833Z/`: `rca011_feature_attribution_*` (funding increment **-342.67%**, EMA24 **+9.75%**, joint **-294.01%**), `rca011_impl_crosscheck_*` (OLS/lstsq agree ~1e-12–1e-17), `rca011_sealed_bridge_*` (sealed **+4.94%** vs clean recompute **-294.01%**; 120-row eligibility delta; sealed panel is an unavailable/LFS-pointer artifact), `prereg_template_trigger_gated_*`, `program_power_synthesis_*` (FCLR-011 fragile/non-promotable; `next_action_heavy=null`).
- New this session: `trigger_readiness_power_calibration_20261116T100533Z.{json,md}` and `trigger_readiness_power.py` — offline, stdlib-only design-power ledger. Finding: most historical windows were **underpowered** for the 2% materiality floor; only FCLR-009 (n=24,495, 6 blocks, MDE 1.95%) was adequately powered; the Track A liquidation recompute (n=593, MDE 8.88%) needs **~11,689 paired observations** for a 2% MDE. Per-trigger sample floors are now fixed before any outcome data exists.
- `trigger_check.json` — one-time trigger verdict (`NO_TRIGGER_FIRED`).

**Bottlenecks removed.**
- **Treadmill eliminated.** The prior handoff defined "heavy work" as re-auditing a static bundle and re-running gates, which any future session could repeat forever without new science. The gate is now a *floor*; completion requires a *new* `session_<UTC>/` with a *new* quantitative artifact (step 3).
- **Design-on-trigger delay removed.** Sample-size/power is now precomputed per trigger, so a firing trigger executes an already-sized prereg instead of improvising one.
- **Dependency bottleneck removed.** The readiness/reproducibility path is stdlib-only; it runs where `statsmodels` (not in `requirements.txt`) is absent. Do not add `statsmodels` to the core path.
- **Handoff ambiguity removed.** `NEXT_SESSION_HANDOFF.md`, `NEXT_SESSION_TASK.md`, and `AGENT_HANDOFF_20261115T073240Z.md` are tombstoned; this file is the only authority.
- **Root churn respected.** Root is 500/500; all new artifacts go to `research_state/session_<UTC>/`; no root-level additions.

**Bottlenecks and prohibitions.**
- Do not start or re-run any cached-data confirmatory estimand; all are terminal.
- Do not mutate sealed artifacts, the frontier, hypothesis registries, or `.github/workflows/*`.
- Do not poll, re-probe the HuggingFace tree, use paid/credentialed/manual outcome data, or add root-level `research_state/*.md|json`.
- Do not add `statsmodels` or other unpinned heavy dependencies to the core path; install only `requirements.txt` if a documented gate needs it.
- The discovery suite is long-running; let it finish and record its actual EXIT, not a partial result.
- The scientific blocker is external: no admissible post-2026-10 observed liquidation labels/source and no agent-settable Gate 4 attestation. The agent-removable requirement is the new quantitative artifact, evidence audit, complete verification, and accurate handoff update.

**Reopen triggers (machine-checkable — Act ONLY when satisfied).** All four are `OPEN`. Do not act until the predicate is satisfied by a concrete evidence artifact in `research_state/`: `GATE4_BRANCH_1` (`fclr016_v5_terms_evidence_RESOLVED_*.json` with `status: RESOLVED_VERIFIED`, `fabricated: false`), `NEW_OBSERVED_LIQUIDATION_SOURCE` (`<source>_admissibility_audit_<UTC>.json` with `status: ADMISSIBLE`, `observed_labels: true`), `HL_LABEL_EXTENSION` (`hl_label_extension_audit_<UTC>.{md,json}`), `EXPANSION_ROBUSTNESS_REDO` (`expansion_robustness_redo_prereg_<UTC>.json` + `evaluation_summary_*.json`).

**Verification record — 2026-11-16T11:47:50Z**

- Last completed heavy session: `session_20261116T100533Z` — new heavy artifact `trigger_readiness_power_calibration_20261116T100533Z.{json,md}` (offline design-power ledger); evidence audit `evidence_audit_20261116T100533Z.md` present; five RCA families carried forward unmodified from `session_20261116T035833Z/`.
- Most recent session (2026-11-16T10:50:28Z): **trigger-check-only, INCOMPLETE.** Trigger check at 2026-11-16T10:46:44Z: all four triggers `OPEN`; Ironflow `data_through=2026-10`; 2026-11/2026-12/2027-01 `CONFIRMED_ABSENT`; no trigger satisfied. One-time trigger-check output written at UTC 2026-11-16T10:53:41Z — contains only the trigger check (no new quantitative artifact, no evidence audit, no gate run). A trigger-check-only session is explicitly **not** completion under the heavy-work mandate (step 3 / mandate).
- `python3 scripts/check_handoff_heavywork_gate.py --json`: **PASS**, `heavy_session=session_20261116T100533Z`, `session_ok=True`, `missing=[]`, `root=500/500`, `reason=OK`, EXIT 0 (verified from `session_20261116T100533Z/heavywork_gate.json`).
- `python3 scripts/check_tracka_scope_registry_drift.py --json`: **PASS**, `scripts=196`, `registry=196`, `reason=OK`, EXIT 0 (verified from `session_20261116T100533Z/scope_drift.json`).
- `python3 -m unittest tests.test_active_campaign_gate tests.test_tracka_hardening_117 tests.test_tracka_hardening_118 tests.test_tracka_hardening_143`: **51 tests OK**, EXIT 0 (verified from `session_20261116T100533Z/targeted_tests.txt`).
- `python3 -m unittest discover -q`: **completed**, 1354 tests, `OK (skipped=1)`, 343.113s, final EXIT 0 (verified from `session_20261116T100533Z/unittest_discover.txt`).
- Root md/json count: **500/500** (at cap — all new artifacts must go to `research_state/session_<UTC>/`; no root-level additions).
- No network probe, no polling, no sealed-artifact/frontier/registry mutation, no new confirmatory estimand performed this session.
- Remaining external blocker: no admissible post-2026-10 observed liquidation labels/source and no agent-settable Gate 4 attestation; cannot be resolved by the agent.

## Tombstones (no authority)
- `NEXT_SESSION_HANDOFF.md`, `NEXT_SESSION_TASK.md`: tombstoned 2026-11-15T22:57:29Z.
- `AGENT_HANDOFF_20261115T073240Z.md`: SUPERSEDED — ignore.
