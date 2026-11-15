# FCLR Heavy Campaign (Trigger-Only) — 2026-11-15T22:39Z

**Frontier rank 0:** `FCLR-BOUNDED-TRIGGER-ONLY-20261115T220000Z` (TRIGGER_ONLY / BOUNDED_TRIGGER_ONLY, `next_action_heavy=null`, `all_terminal=true`).
**Sole handoff:** `AGENT_HANDOFF.md`. This file is the durable bounded campaign note referenced by the frontier; it is non-skippable while trigger-only.

## Current conclusion
All cached-data liquidation forecasting estimands are concluded NOT_MET/SUPERSEDED (do not re-run): `FCLR-LIQ-XSEC-QLIKE-20261115T214949Z`, `FCLR-LIQ-XSEC-ORDERING-20261115T203507Z`, `FCLR-LIQ-COMBINED-20261115T185844Z`. Hypotheses terminal: `H_fclr_liq_xsec_qlike_forecast`, `H_fclr_liq_xsec_ordering_forecast`, `H_fclr_liq_combined_panel_forecast` = NOT_MET. `H2_shek_replication` EXPLORATORY_ONLY (`promotable=false`).

## Resume triggers (all OPEN unless evidenced otherwise)
Check once per session start via `research_state/resume_trigger_registry.json` and `research_state/ironflow_monitor_state.json` (no polling, no re-probe): `GATE4_BRANCH_1` (human/legal), `NEW_OBSERVED_LIQUIDATION_SOURCE` (ironflow `data_through=2026-10`, 2026-11+ absent), `HL_LABEL_EXTENSION`, `EXPANSION_ROBUSTNESS_REDO` (only a NEW prereg design meeting stated conditions; never re-run/re-score sealed designs).

## Mandatory bounded hardening (heavy default while trigger-only)
1. **Trigger check (once):** confirm trigger states and ironflow coverage unchanged. If a trigger is satisfied with required artifacts/fields, go to “Trigger-gated advance”.
2. **Full regression gate:** `python3 -m unittest discover -q` → 0 failures (fix root causes only; never touch sealed artifacts or `.github/workflows/*`).
3. **Invariants:** `python3 scripts/check_tracka_scope_registry_drift.py` PASS; `python3 -m unittest tests.test_active_campaign_gate tests.test_tracka_hardening_117 tests.test_tracka_hardening_118` PASS. Keep rank-0 TRIGGER_ONLY sentinel active.
4. **Reproducibility/consistency:** keep `AGENT_HANDOFF.md`, frontier, and this file aligned with ground truth; record commands/results. Commit checkpoint if changed.

## Trigger-gated advance (only on evidenced trigger)
- Pre-outcomes prereg first (`outcome_data_inspected_before_freeze=false`), admissibility audit per `RESEARCH_PROMPT.md`, materially different estimand only.
- Execute eval+gates; register new scripts in both scope registries; update `experiment_frontier.json`/`hypothesis_registry.json`; install as rank-0 active heavy cell with honest verdict.
- Forbidden: re-run concluded estimands, re-probe TERMINAL_NO_GO families, mutate sealed artifacts, edit `.github/workflows/*`, paid/credentialed/manual outcome data, polling.

## Session closeout
Stop cleanly only after: trigger checked once, full suite/guards green, and handoff/campaign consistent with external blockers documented.
