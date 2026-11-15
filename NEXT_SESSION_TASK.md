# NEXT SESSION INITIAL TASK MESSAGE — 2026-11-15T20:35:50Z
# SOLE DURABLE HANDOFF POINTER

**Repository:** Funding-conditioned-volatility-and-liquidation-risk
**Sole durable handoff:** `AGENT_HANDOFF.md` — execute its `INITIAL TASK MESSAGE FOR NEXT AGENTIC WORK SESSION — 2026-11-15T20:35:50Z`. `NEXT_SESSION_HANDOFF.md` = tombstone. `AGENT_HANDOFF_20261115T073240Z.md` = RETIRED/SUPERSEDED — ignore.

## IMMEDIATE HEAVY TASK (default path — NOT trigger-gated)
Rank-0 heavy campaign: **`FCLR-LIQ-XSEC-QLIKE-20261115T203550Z`** (`READY_EXECUTE` / `ACTIVE`).

Prior cell `FCLR-LIQ-XSEC-ORDERING-20261115T185957Z` is **CONCLUDED `NOT_MET`** (do not re-run same estimand; eval `research_state/evaluation_summary_FCLR-LIQ-XSEC-ORDERING-20261115T203507Z.*`). Prior cell `FCLR-LIQ-COMBINED-PANEL-20261115T170000Z` is **CONCLUDED `NOT_MET`**. Execute the materially different cross-sectional QLIKE estimand on the existing 15-coin panel `research_state/fclr_liq_combined_panel_20261115T181405Z.parquet` (no new acquisition), using the 2 pristine metpie blocks + 1 estimand-novel ironflow block.

## EXECUTE IN ORDER
1. Run baseline block in `AGENT_HANDOFF.md`; confirm rank-0 = `FCLR-LIQ-XSEC-QLIKE-20261115T203550Z`. If `tracka_resume_check.py` is red only on untracked eval summaries, treat as bookkeeping and proceed.
2. Freeze NEW pre-outcomes prereg: create `scripts/fclr_liq_combined_xsec_qlike_prereg.py` → `research_state/prereg_fclr_liq_combined_xsec_qlike_<UTC>.{json,md}` (daily cross-sectional QLIKE of next-day liquidation intensity, B1 vs C2, primary metric = cross-sectional QLIKE, secondary = rank-IC + top-3 hit-rate, expanding-window walk-forward over 3 non-overlapping 30d test blocks: 2 pristine metpie blocks 2025-03-22..2025-04-21 & 2025-04-21..2025-05-21 + 1 estimand-novel ironflow block 2025-10-01..2025-10-31, 7d purge/embargo, ≥2000 block-bootstrap reps seed 20261115, Holm, ≥2% materiality; `outcome_data_inspected_before_freeze=false`).
3. Create `scripts/fclr_liq_combined_xsec_qlike_eval.py` → `research_state/evaluation_summary_FCLR-LIQ-XSEC-QLIKE-<UTC>.{json,md}`; update frontier + `H_fclr_liq_xsec_qlike_forecast`. If NOT_MET, record honestly and install next materially different heavy cell at rank 0.
4. Register BOTH new scripts in BOTH `research_state/tracka_script_scope_registry.json` and `tests/test_tracka_hardening_117.py` `SCRIPT_REGISTRY`; keep drift + 117/118 green. Checkpoint-commit deliverables (include untracked combined eval summaries if still untracked).

## HARD CONSTRAINTS
- Never reopen sealed/terminal families or mutate sealed artifacts; never edit `.github/workflows/*`.
- No outcome-peeking/threshold tuning before prereg; no paid/credentialed/manual data for outcomes.
- `H2_shek_replication` remains EXPLORATORY_ONLY (`promotable=false`).
- No polling, no re-running same estimand, no re-probing TERMINAL_NO_GO families. Exactly ONE active handoff (`AGENT_HANDOFF.md`). "No trigger → stop cleanly" is NOT completion.