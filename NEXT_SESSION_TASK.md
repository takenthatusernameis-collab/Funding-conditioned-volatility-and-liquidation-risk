# NEXT SESSION INITIAL TASK MESSAGE — 2026-11-15T19:01:23Z
# SOLE DURABLE HANDOFF POINTER

**Repository:** Funding-conditioned-volatility-and-liquidation-risk (funding rates, volatility, liquidation risk in crypto perpetuals)
**Sole durable handoff:** `AGENT_HANDOFF.md` — execute its `INITIAL TASK MESSAGE FOR NEXT AGENTIC WORK SESSION — 2026-11-15T19:01:23Z`. `NEXT_SESSION_HANDOFF.md` = tombstone. `AGENT_HANDOFF_20261115T073240Z.md` = RETIRED/SUPERSEDED — ignore.

## IMMEDIATE HEAVY TASK (default path — NOT trigger-gated, NOT status-only)

Rank-0 heavy campaign: **`FCLR-LIQ-XSEC-ORDERING-20261115T185957Z`** (`READY_EXECUTE` / `ACTIVE`).

The prior combined-panel time-series cell (`FCLR-LIQ-COMBINED-PANEL-20261115T170000Z`) is **CONCLUDED `NOT_MET`** — executed to a frozen prereg + timestamped eval (`research_state/evaluation_summary_FCLR-LIQ-COMBINED-20261115T185844Z.{json,md}`; C2 vs B1 on 24h observed liquidation intensity, C2 worse by 17.1%, CI spans zero). It is demoted (rank 1, SUPERSEDED) and must not be re-run.

The open heavy cell is a **materially different, cache-backed estimand**: cross-sectional liquidation ordering on the SAME already-built 15-coin combined panel (`research_state/fclr_liq_combined_panel_20261115T181405Z.parquet`, 1.74M events, all causal features present). **No new acquisition needed.**

## EXECUTE IN ORDER (do not stop at status; do not skip to verdict)
1. Run the baseline/start block in `AGENT_HANDOFF.md`; confirm campaign gate 19/19, fwd-vol PASS, scope drift 191/191 green, targeted suite 82/82 green, `next_campaign_status.py` honest, rank-0 = `FCLR-LIQ-XSEC-ORDERING-20261115T185957Z`.
2. Freeze a NEW pre-outcomes prereg (`scripts/fclr_liq_combined_xsec_prereg.py` → `research_state/prereg_fclr_liq_combined_xsec_<UTC>.{json,md}`): daily cross-sectional ordering of next-day liquidation intensity, C2 vs B1, mean rank-IC + top-3 hit-rate + cross-sectional QLIKE, expanding-window walk-forward over the same 3 test blocks (2025-10, 2026-01, 2026-09), 7d purge/embargo, ≥2000 block-bootstrap reps (seed 20261115), Holm, ≥2% materiality floor.
3. Evaluate + gate (`scripts/fclr_liq_combined_xsec_eval.py`) → `research_state/evaluation_summary_FCLR-LIQ-XSEC-ORDERING-<UTC>.{json,md}`; update frontier + `H_fclr_liq_xsec_ordering_forecast`. If NOT_MET, record honestly and install the next materially different heavy cell at rank 0.
4. Register BOTH new scripts in BOTH scope registries (`research_state/tracka_script_scope_registry.json` + `tests/test_tracka_hardening_117.py` SCRIPT_REGISTRY); keep drift + `test_tracka_hardening_117/118` green.

## HARD CONSTRAINTS
- Never reopen sealed/terminal families or mutate sealed artifacts; never edit `.github/workflows/*`.
- No outcome-peeking/threshold tuning before prereg freeze; no paid/credentialed/manual data for outcomes.
- `H2_shek_replication` remains EXPLORATORY_ONLY (`promotable=false`). Do not relabel exploratory as confirmatory.
- Do not poll, do not re-run tested windows for the same estimand, do not re-probe TERMINAL_NO_GO families.
- Exactly ONE active handoff (`AGENT_HANDOFF.md`). "No trigger → stop cleanly" is NOT completion.

## NOTE
`scripts/tracka_resume_check.py` `root_md_json_bounded` fails closed on untracked root `research_state/*.{md,json}`; the 2 new `evaluation_summary_FCLR-LIQ-COMBINED-*` files become tracked at the standard end-of-session checkpoint commit (HEAD already contains the prior session's prereg/scripts). If still red at start, stage the deliverables listed in `AGENT_HANDOFF.md` and proceed — bookkeeping, not a research blocker.