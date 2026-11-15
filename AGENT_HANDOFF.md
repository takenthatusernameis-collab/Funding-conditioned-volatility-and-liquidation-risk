# AGENT HANDOFF — 2026-11-15T21:52:00Z

**Project:** Funding-conditioned Volatility and Liquidation Risk (FCLR)
**Repository priority:** `Funding-conditioned-volatility-and-liquidation-risk` — rank-0 heavy campaign `FCLR-LIQ-XSEC-QLIKE-20261115T203550Z` is now **CONCLUDED_NOT_MET** (executed in full this session). No agent-removable heavy work remains at rank 0.

---

# INITIAL TASK MESSAGE FOR NEXT AGENTIC WORK SESSION — 2026-11-15T21:52:00Z

**Repository:** Funding-conditioned-volatility-and-liquidation-risk
**Sole durable handoff:** This file (`AGENT_HANDOFF.md`). `NEXT_SESSION_HANDOFF.md` = tombstone (no authority). `AGENT_HANDOFF_20261115T073240Z.md` = RETIRED/SUPERSEDED — ignore.

## CAMPAIGN STATUS — EXECUTED AND RECORDED

Rank-0 heavy campaign **`FCLR-LIQ-XSEC-QLIKE-20261115T203550Z`** (`experiment_frontier.json` rank 0) is now **CONCLUDED_NOT_MET**, all 3 phases COMPLETED:

- Phase 1 PREREG_FREEZE — COMPLETED: `research_state/prereg_fclr_liq_combined_xsec_qlike_20261115T214903Z.{json,md}` (outcome_data_inspected_before_freeze=false; primary = cross-sectional QLIKE, secondary = rank-IC + top-3 hit-rate; 3 blocks: 2025-03-22..2025-04-21 pristine metpie, 2025-04-21..2025-05-21 pristine metpie, 2025-10-01..2025-10-31 estimand-novel ironflow; 7d purge/embargo; 2000 block-bootstrap reps seed 20261115; Holm; >=2% materiality floor on primary).
- Phase 2 EVALUATION_AND_GATE — COMPLETED: `research_state/evaluation_summary_FCLR-LIQ-XSEC-QLIKE-20261115T214949Z.{json,md}`; verdict **NOT_MET** recorded honestly (C2 worse than B1 on cross-sectional QLIKE, rel improvement -75.56%, CI [18.40, 86.08] entirely above zero, only 2 of 3 blocks evaluable because block-1 train window is empty at panel origin 2025-03-22); `H_fclr_liq_xsec_qlike_forecast` updated in `hypothesis_registry.json` (status NOT_MET, terminal).
- Phase 3 REGISTRY_AND_FRONTIER — COMPLETED: both new scripts registered in `research_state/tracka_script_scope_registry.json` (193->195) and `tests/test_tracka_hardening_117.py` SCRIPT_REGISTRY; drift green; tests 117/118 pass.

Prior cells remain CONCLUDED: `FCLR-LIQ-XSEC-ORDERING-20261115T203501Z` (NOT_MET, rel_improvement -14.34%, p=0.0) and `FCLR-LIQ-COMBINED-PANEL-20261115T170000Z` (NOT_MET). Do NOT re-run the same estimands.

## IMMEDIATE TASK (default path — NOT trigger-gated)

1. Confirm `experiment_frontier.json` rank 0 = `FCLR-LIQ-XSEC-QLIKE-20261115T203550Z` with status CONCLUDED_NOT_MET, last_verdict NOT_MET, all 3 phases COMPLETED.
2. Confirm `hypothesis_registry.json` has `H_fclr_liq_xsec_qlike_forecast` status NOT_MET (terminal), last_evaluation `FCLR-LIQ-XSEC-QLIKE-20261115T214949Z`.
3. Confirm scope-registry drift green: `python3 scripts/check_tracka_scope_registry_drift.py` → PASS.
4. Confirm regression gate: `python3 -m unittest tests.test_tracka_hardening_117 tests.test_tracka_hardening_118` → OK.
5. **No agent-removable heavy work remains.** All candidate liquidation forecasting estimands on the cached 15-coin combined metpie+ironflow panel (combined panel 24h QLIKE, cross-sectional ordering, cross-sectional QLIKE) concluded NOT_MET/SUPERSEDED. No new admissible observed-liquidation source is available (Track A liquidation resume BLOCKED on Ironflow Hyperliquid liquidations for months >= 2026-11; latest cached = 2026-10; fills absent). `H2_shek_replication` remains EXPLORATORY_ONLY (promotable=false) — do not re-run or promote.
6. **Stop cleanly.** "No trigger → stop cleanly" IS completion here because no heavy work is agent-executable. Do NOT poll, do NOT re-run the same estimand, do NOT re-probe TERMINAL_NO_GO families, do NOT mutate sealed artifacts or `.github/workflows/*`. Resume only if a resume trigger fires (`GATE4_BRANCH_1` or `NEW_OBSERVED_LIQUIDATION_SOURCE`, e.g. Ironflow Hyperliquid 2026-11 events+fills parquet lands via `scripts/monitor_ironflow_liquidations.py`), at which point install the next materially different heavy cell at rank 0.

## HARD CONSTRAINTS (non-negotiable)
- ❌ Never reopen sealed/terminal families or mutate sealed artifacts; never edit `.github/workflows/*`.
- ❌ No outcome-peeking/threshold tuning before prereg; no paid/credentialed/manual data for outcomes.
- ❌ No polling, no re-running same estimand, no re-probing TERMINAL_NO_GO families.
- ✅ `H2_shek_replication` remains EXPLORATORY_ONLY (`promotable=false`).
- ✅ Exactly ONE active handoff (`AGENT_HANDOFF.md`).

## BOTTLENECKS REMOVED (this session)
1. **Rank-0 heavy work executed:** `FCLR-LIQ-XSEC-QLIKE-20261115T203550Z` was READY_EXECUTE/ACTIVE with all phases PENDING; this session froze the pre-outcomes prereg, ran the eval+gate, recorded NOT_MET honestly, registered both scripts in both registries, and updated frontier + hypothesis registry. Heavy work is no longer pending — it is concluded.
2. **No stale handoffs:** `NEXT_SESSION_HANDOFF.md` = tombstone (no authority). `AGENT_HANDOFF_20261115T073240Z.md` = retired/superseded. Single durable handoff = this file only.
3. **Scope-registry drift resolved:** both QLIKE scripts added to `tracka_script_scope_registry.json` (195 scripts) and `test_tracka_hardening_117.py` SCRIPT_REGISTRY; drift check PASS; tests 117/118 OK.

## KEY ARTIFACTS FOR REFERENCE
- `research_state/experiment_frontier.json` — rank 0 `FCLR-LIQ-XSEC-QLIKE-20261115T203550Z` (CONCLUDED_NOT_MET, phases COMPLETED)
- `research_state/prereg_fclr_liq_combined_xsec_qlike_20261115T214903Z.{json,md}` — frozen pre-outcomes QLIKE prereg
- `research_state/evaluation_summary_FCLR-LIQ-XSEC-QLIKE-20261115T214949Z.{json,md}` — NOT_MET verdict
- `research_state/fclr_liq_combined_panel_20261115T181405Z.parquet` — 15-coin combined panel (1,740,415 events, 7,512 daily rows)
- `research_state/evaluation_summary_FCLR-LIQ-XSEC-ORDERING-20261115T203507Z.*` — prior cell NOT_MET (do not re-run)
- `scripts/fclr_liq_combined_xsec_qlike_prereg.py`, `scripts/fclr_liq_combined_xsec_qlike_eval.py` — new QLIKE scripts (registered in both registries)
- `research_state/tracka_script_scope_registry.json` — 193->195 scripts, drift green
- `tests/test_tracka_hardening_117.py` SCRIPT_REGISTRY — synced (tests 117/118 OK)
- `AGENT_HANDOFF.md` — this file (single durable handoff)

---

**Generated by:** Kilo agentic session 2026-11-15T21:52:00Z
**Next session:** verify CONCLUDED_NOT_MET recorded + drift + 117/118 green; no heavy work remains → stop cleanly unless a resume trigger fires. Do not poll. Do not invent work beyond this status.

(End of file)
