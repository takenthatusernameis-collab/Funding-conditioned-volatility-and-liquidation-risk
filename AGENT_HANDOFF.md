# AGENT HANDOFF — 2026-11-16T09:54:52Z (sole durable handoff)

## INITIAL TASK MESSAGE FOR NEXT AGENTIC WORK SESSION

**Priority 0 — repository and rank-0 state.** Repository: `Funding-conditioned-volatility-and-liquidation-risk` (funding-conditioned volatility and liquidation risk). The sole rank-0 campaign is `FCLR-BOUNDED-TRIGGER-ONLY-20261115T220000Z` (`TRIGGER_ONLY` / `BOUNDED_TRIGGER_ONLY`, `all_terminal=true`, `next_action_heavy=null`). All cached-data confirmatory estimands are terminal. The sealed FCLR-011 PASS was not independently reproduced (clean recompute C2 versus B1 **-294.01%**, versus sealed **+4.94%**) and is fragile/non-promotable. Track B is sealed `NOT_SUPPORTED`; Track C cached confirmatory designs are terminal; H2 is `EXPLORATORY_ONLY`.

**Read these first, in order:**
1. `research_state/resume_trigger_registry.json`
2. `research_state/ironflow_monitor_state.json`
3. `research_state/FCLR_HEAVY_CAMPAIGN_NEXT.md`
4. `research_state/session_20261116T035833Z/program_power_synthesis_20261116T035833Z.md`

**Mandatory next-session sequence.** Do all steps in order. A trigger check plus unit tests is not a heavy session and is not completion.

1. **Create a new evidence directory:** `research_state/session_<UTC>/` using the actual session UTC. Do not add files to the `research_state/` root: it is at **498/500** md/json and the cap is fail-closed.
2. **Check triggers exactly once, without network access or polling.** Read the two trigger files above. Record the timestamp, each trigger status, `data_through`, and the post-2026-10 month classifications in the new session directory. Current state: all four triggers are `OPEN`; Ironflow is `data_through=2026-10`; 2026-11, 2026-12, and 2027-01 are `CONFIRMED_ABSENT`. Do not re-probe HuggingFace, run a monitor, or repeat the trigger check later in the same session.
3. **Audit the completed heavy evidence bundle.** Verify that `research_state/session_20261116T035833Z/` still contains all required artifact families:
   - `rca011_feature_attribution_*`
   - `rca011_impl_crosscheck_*`
   - `rca011_sealed_bridge_*`
   - `prereg_template_trigger_gated_*`
   - `program_power_synthesis_*`
   Write a concise evidence-audit artifact in the new session directory that records the bundle path, the artifact families found, and the integrity conclusion: the RCA is complete; FCLR-011 is not reproducible/promotable; the attribution fit has only 152 complete training rows after purge/dropna; and `next_action_heavy=null` on cached data. Do not rerun FCLR-RCA-011 merely because an old note calls it pending.
4. **Run and capture every required gate.** Save the commands and outputs under the new session directory:
   - `python3 scripts/check_handoff_heavywork_gate.py --json` — must PASS with the complete `session_20261116T035833Z` bundle and root count at most 500.
   - `python3 scripts/check_tracka_scope_registry_drift.py --json` — must PASS.
   - `python3 -m unittest tests.test_active_campaign_gate tests.test_tracka_hardening_117 tests.test_tracka_hardening_118 tests.test_tracka_hardening_143` — must pass all 51 tests.
   - `python3 -m unittest discover -q` — run to completion; record the exact test count, skip count, wall time if available, and final process EXIT. Never treat a timeout or monitor cap as green.
5. **Update only this handoff after the evidence audit and gates.** Replace the timestamp/verification section with the actual new timestamp and results. Keep this initial task message, the sole-handoff declaration, the completed bundle reference, and the external blockers intact. Do not create another handoff file and do not execute any tombstoned instructions.

**Trigger-gated science is the only scientific advance.** If no trigger is satisfied, do not advance or re-run a confirmatory estimand. The required holding action is the new-session evidence audit plus complete gate run plus an accurate handoff update. If a trigger is satisfied with its registry-defined evidence artifact, then before inspecting outcomes:
- perform the `RESEARCH_PROMPT.md` §16 admissibility/source audit;
- instantiate `research_state/session_20261116T035833Z/prereg_template_trigger_gated_20261116T035833Z.json` as a new prereg in the new session directory;
- require a materially different estimand, at least five paired OOS instruments, at least three non-overlapping 30-day test blocks, a prespecified Holm family, seven-day purge/embargo, and target MDE below the 2% materiality floor;
- set `outcome_data_inspected_before_freeze=false`; and
- only then execute, register any new scripts in both scope registries, run all gates, and update the frontier/hypothesis registries with an honest verdict.

**Heavy-work evidence on disk (authoritative).** The completed gate-pinned bundle is `research_state/session_20261116T035833Z/`:
- `rca011_feature_attribution_20261116T035833Z.{json,md}`: funding increment **-342.67%** (CI [-497.48, -221.27]); EMA24 increment **+9.75%**; joint increment **-294.01%**.
- `rca011_impl_crosscheck_20261116T035833Z.json`: independent OLS and `lstsq` paths agree to approximately 1e-12–1e-17.
- `rca011_sealed_bridge_20261116T035833Z.md` and `_ext`: sealed **+4.94%** versus clean recompute **-294.01%**; 120-row eligibility delta; sealed panel is an unavailable/LFS-pointer artifact here.
- `prereg_template_trigger_gated_20261116T035833Z.json`: trigger-gated power-remediation skeleton.
- `program_power_synthesis_20261116T035833Z.{json,md}`: integrity/instability finding; FCLR-011 is fragile and non-promotable; `next_action_heavy=null`.

**Bottlenecks and prohibitions.**
- Do not start or re-run any cached-data confirmatory estimand; all are terminal.
- Do not mutate sealed artifacts, the frontier, hypothesis registries, or `.github/workflows/*`.
- Do not poll, re-probe the HuggingFace tree, use paid/credentialed/manual outcome data, or add root-level `research_state/*.md|json`.
- If dependencies are missing, install `pip install -r requirements.txt` before the documented gates.
- The discovery suite is long-running; let it finish and record its actual EXIT, not a partial result.
- The scientific blocker is external: no admissible post-2026-10 observed liquidation labels/source and no agent-settable Gate 4 attestation. The agent-removable requirement is the audit, complete verification, and accurate handoff update described above.

**Completion standard.** Completion requires a new `session_<UTC>/` evidence-audit artifact, all four command outputs captured there, a green heavy-work gate, a green scope-drift check, all targeted tests passing, the full discovery suite completed with its final EXIT recorded, root count at most 500, and this handoff updated with the new timestamp/results. A status-only session, a prose-only summary, or a timeout is not completion.

### Verification record — 2026-11-16T09:54:52Z
- Trigger files read once: all four triggers `OPEN`; Ironflow `data_through=2026-10`; 2026-11/2026-12/2027-01 `CONFIRMED_ABSENT`; no trigger satisfied.
- `python3 scripts/check_handoff_heavywork_gate.py --json`: **PASS**, `heavy_session=session_20261116T035833Z`, `session_ok=True`, `root=498/500`, `reason=OK`, EXIT 0.
- `python3 scripts/check_tracka_scope_registry_drift.py --json`: **PASS**, `scripts=196`, `registry=196`, `reason=OK`, EXIT 0.
- `python3 -m unittest tests.test_active_campaign_gate tests.test_tracka_hardening_117 tests.test_tracka_hardening_118 tests.test_tracka_hardening_143`: **51 tests OK**, EXIT 0.
- `python3 -m unittest discover -q`: **completed**, 1354 tests, `OK (skipped=1)`, approximately 343.820s, final EXIT 0.
- The full suite touched `research_state/ironflow_fastpath_cache.json`; that generated timestamp-only side effect was reverted. Final modified files are the three documentation files only.
- No network probe, no polling, no sealed-artifact/frontier/registry mutation, and no new confirmatory estimand were performed.

## Tombstones (no authority)
- `NEXT_SESSION_HANDOFF.md`, `NEXT_SESSION_TASK.md`: tombstoned 2026-11-15T22:57:29Z.
- `AGENT_HANDOFF_20261115T073240Z.md`: SUPERSEDED — ignore.