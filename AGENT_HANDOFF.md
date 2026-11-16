# AGENT HANDOFF — 2026-11-16T09:21:02Z (sole durable handoff)

## INITIAL TASK MESSAGE FOR NEXT AGENTIC WORK SESSION
**Repo:** Funding-conditioned-volatility-and-liquidation-risk (funding-conditioned volatility & liquidation risk; liquidation data via ironflow/HuggingFace; FCLR estimand campaigns). **Rank-0 campaign state:** `FCLR-BOUNDED-TRIGGER-ONLY-20261115T220000Z` (TRIGGER_ONLY / BOUNDED_TRIGGER_ONLY, `all_terminal=true`, `next_action_heavy=null`). **All cached-data confirmatory estimands are terminal** (FCLR-009/H001 NOT_MET; FCLR-011 sealed PASS not independently reproduced by clean recompute (-294.01% vs sealed +4.94%) → fragile/non-promotable; Track B sealed NOT_SUPPORTED; Track C cached confirmatory designs terminal; H2 EXPLORATORY_ONLY). **Gate 4 Branch 1** blocked on human/legal attestation (agent cannot set RESOLVED_VERIFIED). Do NOT start/re-run any confirmatory estimand on cached data, re-probe the HuggingFace tree, poll, mutate sealed artifacts/frontier/registries, edit `.github/workflows/*`, or add root-level `research_state/*.md|json` (root cap 498/500; write only under `research_state/session_<UTC>/`).

**Non-skippable holding action, in order:**
1. **Trigger check ONCE (no re-poll).** Read `research_state/resume_trigger_registry.json` (4 triggers, all OPEN) and `research_state/ironflow_monitor_state.json` (last probe `ironflow_probe_20261102T115745Z`, 2026-11-02T11:57:45Z, GET 200, `data_through=2026-10`, 2026-11..2027-01 CONFIRMED_ABSENT; probes==2 satisfied). If NO trigger is satisfied (current state: none satisfied), do not advance science — proceed to step 2 to keep gates green. If a trigger IS satisfied with its required evidence artifact, jump to Phase D of `research_state/FCLR_HEAVY_CAMPAIGN_NEXT.md`.
2. **Run and record deterministic gates (must stay green):**
   - `python3 scripts/check_handoff_heavywork_gate.py` → PASS (handoff/session bundle/root-cap enforced)
   - `python3 scripts/check_tracka_scope_registry_drift.py` → PASS
   - `python3 -m unittest tests.test_active_campaign_gate tests.test_tracka_hardening_117 tests.test_tracka_hardening_118 tests.test_tracka_hardening_143` → 51 tests OK
   - `python3 -m unittest discover -q` → run to completion and record count + EXIT (discovery suite must complete; do not treat a timeout as green).
3. **On external trigger only (materially different estimand):** perform §16 admissibility audit + NEW pre-outages prereg (>=3 non-overlapping 30d blocks, MDE below 2% floor, Holm family, `outcome_data_inspected_before_freeze=false`), produce the full heavy artifact set in a fresh `research_state/session_<UTC>/` (`rca011_feature_attribution_*`, `rca011_impl_crosscheck_*`, `rca011_sealed_bridge_*`, `prereg_template_trigger_gated_*`, `program_power_synthesis_*`), and update the `session_<UTC>` reference + gate results in this file. "No trigger → stop cleanly" is NOT completion; keeping the enforced gate/suite green and the handoff accurate IS the required holding action.

**Heavy campaign (FCLR-RCA-011) is COMPLETE and gate-pinned.** `research_state/session_20261116T035833Z/` already contains the full Phase-B/C evidence set, so a future session cannot satisfy the handoff-heavywork gate by running only the trigger check + suite — `check_handoff_heavywork_gate.py` fails closed unless the recorded `session_<UTC>/` bundle contains `rca011_feature_attribution_*`, `rca011_impl_crosscheck_*`, `rca011_sealed_bridge_*`, `prereg_template_trigger_gated_*`, and `program_power_synthesis_*`. Do not delete or replace this bundle without installing a complete successor bundle first.

### Heavy-session evidence (authoritative, on disk)
Latest self-contained heavy bundle (gate-pinned): `research_state/session_20261116T035833Z/`
- `rca011_feature_attribution_20261116T035833Z.{json,md}` — B1_plus_funding vs B1 **-342.67%** (CI [-497.48,-221.27]); B1_plus_ema24 vs B1 **+9.75%**; joint vs B1 **-294.01%**.
- `rca011_impl_crosscheck_20261116T035833Z.json` — OLS vs lstsq parity (~1e-12–1e-17).
- `rca011_sealed_bridge_20261116T035833Z.md` (+ `_ext`) — sealed PASS (+4.94%) not reproduced by clean recompute (-294.01%); +120-row eligibility delta; sealed panel LFS pointer unauditable here.
- `prereg_template_trigger_gated_20261116T035833Z.json` — power-remediation prereg skeleton.
- `program_power_synthesis_20261116T035833Z.{json,md}` — FCLR-011 (c) integrity/underpowered (152 train rows); `next_action_heavy=null`.

### Verified this session (2026-11-16T09:12:47Z)
- Triggers: all OPEN (n=4). Ironflow: `data_through=2026-10`, 2026-11..2027-01 CONFIRMED_ABSENT; no re-probe (reads only).
- `python3 scripts/check_handoff_heavywork_gate.py` → **PASS** (`heavy_session=session_20261116T035833Z session_ok=True root=498/500 reason=OK`, EXIT=0)
- `python3 scripts/check_tracka_scope_registry_drift.py` → **PASS** (`scripts=196 registry=196 reason=OK`, EXIT=0)
- `python3 -m unittest tests.test_active_campaign_gate tests.test_tracka_hardening_117 tests.test_tracka_hardening_118 tests.test_tracka_hardening_143` → **51 tests OK** (EXIT=0)
- `python3 -m unittest discover -q` → **Ran 1354 tests, OK (skipped=1), EXIT=0** (ran to completion in 343s; not a timeout)
- Root md/json count: **498/500** (under cap). Session bundle `research_state/session_20261116T035833Z/` intact (14 files, all 5 Phase-B/C prefixes present). Working tree clean; no root writes, no re-probe, no sealed-artifact mutation.

### Bottlenecks removed
1. `unittest discover -q` previously shell-timed out without a final summary — discovery suite must run to completion; record EXIT and count. Long-running; do not treat a timeout as green.
2. `numpy`/`pandas`/`scipy`/`pyarrow`/`requests` missing from environment — `ModuleNotFoundError` in hardening suites. Installed via `pip install -r requirements.txt`; targeted and discovery tests now pass.
3. FCLR-RCA-011 heavy campaign (Phase B/C) previously prose-only with `next_action_heavy=null` and no artifacts — now complete and gate-pinned at `research_state/session_20261116T035833Z/`; the handoff-heavywork gate enforces it so future sessions cannot skip heavy work.

### Next materially different free route
Hold TRIGGER_ONLY with gate+suite green. Advance ONLY on a satisfied external trigger with §16 admissibility audit + new pre-outages prereg (materially different estimand, >=3 non-overlapping 30d blocks, MDE < 2% floor, Holm family). On advance, write `session_<UTC>/` heavy bundle (gate-enforced set) and update this file.

## Tombstones (no authority)
- `NEXT_SESSION_HANDOFF.md`, `NEXT_SESSION_TASK.md`: tombstoned 2026-11-15T22:57:29Z.
- `AGENT_HANDOFF_20261115T073240Z.md`: SUPERSEDED — ignore.
