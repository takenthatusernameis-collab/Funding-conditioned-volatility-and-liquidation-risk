# NEXT SESSION INITIAL TASK MESSAGE — 2026-11-15T08:48:14Z
# SOLE DURABLE HANDOFF POINTER — DO NOT RE-EDIT HANDOFF PROSE BEFORE PRODUCING DELIVERABLES

**Repository:** Funding-conditioned-volatility-and-liquidation-risk (funding rates, volatility, liquidation-risk in crypto perpetuals)
**Sole durable handoff:** `AGENT_HANDOFF.md` (execute its INITIAL TASK MESSAGE). `NEXT_SESSION_HANDOFF.md` = tombstone. `AGENT_HANDOFF_20261115T073240Z.md` = RETIRED/SUPERSEDED — ignore.

## IMMEDIATE TASK (default heavy path, NOT trigger-gated)
Execute **`FCLR-SHEK-SCALE-SENSITIVITY-GRID-20261115T073000Z`** now. Compute the frozen prereg sensitivity grid for both arms and emit timestamped artifacts `research_state/evaluation_summary_FCLR-SHEK-SCALE-SENS-<UTC>.{json,md}`. Required cache-only robustness on frozen Shek samples (not a re-probe, no headline/threshold tuning). Forecast 3-block frontier is exhausted per `next_campaign_status.py`.

## Baseline re-verified (2026-11-15T08:48:14Z)
- `fclr_campaign_gate.py` 19/19 PASS (env lacked `pyarrow`; installed in user site-packages)
- `fclr_fwd_vol_2025_disjoint_cross_gate.py` PASS
- `check_tracka_scope_registry_drift.py` 186/186 OK
- Targeted suites PASS: `tests.test_fclr_shek_scale`, `test_active_campaign_gate`, `test_next_campaign_status`, `test_funding_correction_replication`, `test_tracka_hardening_117`
- `next_campaign_status.py`: "no feasible 3-block design in ANY domain"
- `research_state/*SENS*`: none (grid not emitted)
- Frontier rank-0: `FCLR-SHEK-SCALE-SENSITIVITY-GRID-20261115T073000Z` `READY_EXECUTE`

## Mandatory start block
```bash
git status --short && git log -1 --oneline
python3 scripts/fclr_campaign_gate.py
python3 scripts/fclr_fwd_vol_2025_disjoint_cross_gate.py
python3 scripts/check_tracka_scope_registry_drift.py
python3 -m unittest tests.test_fclr_shek_scale tests.test_active_campaign_gate tests.test_next_campaign_status tests.test_funding_correction_replication tests.test_tracka_hardening_117 -v
python3 scripts/next_campaign_status.py
```
If green, proceed immediately to heavy execution — do not re-summarise baseline.

## Heavy execution requirements (in order)
1. **No new prereg:** use frozen `research_state/prereg_fclr_shek_scale_20261115T063600Z.json` and headline `evaluation_summary_FCLR-SHEK-SCALE-20261115T071135Z.{json,md}`. Do not tune thresholds, change headline, or peek/select by outcomes.
2. **Full frozen grid for BOTH arms** (Arm A Binance independent; Arm B ironflow secondary never-promotable): percentiles `[1,99],[5,95],[10,90]` × censor `168,336` × rv_split `tercile,median` (12 cells/arm, 24 total). Headline cell `[5,95]/168h/tercile` reported only.
3. **Emit** `research_state/evaluation_summary_FCLR-SHEK-SCALE-SENS-<UTC>.{json,md}` with per-cell event/regime counts, KM/log-rank/CI/Holm (or consistent contrast), verdict/materiality, and consistency vs headline (Arm A `TAIL_SHAPE_EFFECT`, Arm B `REPLICATES_DIRECTION`).
4. **Code:** extend `scripts/fclr_shek_scale.py` or add clearly-scoped companion script registered in BOTH `research_state/tracka_script_scope_registry.json` and `tests/test_tracka_hardening_117.py` `SCRIPT_REGISTRY`; keep scope drift green.
5. **Tests:** add/extend deterministic, fixture-based, tmp-isolated, no-network tests for grid computation and verdict-consistency. Keep `H2_shek_replication` `EXPLORATORY_ONLY`, `promotable=false`, never terminal-promote.
6. **Frontier:** mark `FCLR-SHEK-SCALE-SENSITIVITY-GRID-20261115T073000Z` `COMPLETED_VALIDATED` with evidence and install next heavy cell at rank 0 (truthful trigger-only sentinel only after grid completed).
7. **Verify & commit:** run full verification set (gates, scope drift, tests, `next_campaign_status.py` honest); commit only meaningful work.

## Hard constraints
- Never reopen sealed/terminal families or mutate sealed artifacts
- Never edit `.github/workflows/*`; never use paid/credentialed/manual data
- Never relabel as forecast skill / boundary-breach / observed-liquidation prediction
- "No trigger → stop cleanly" is NOT completion

**Heavy work is the default path. Do not write status-only notes. Do not re-probe exhausted families.**
