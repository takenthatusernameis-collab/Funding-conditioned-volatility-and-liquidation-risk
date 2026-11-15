# NEXT SESSION INITIAL TASK MESSAGE — 2026-11-15T15:25:27Z
# SOLE DURABLE HANDOFF POINTER

**Repository:** Funding-conditioned-volatility-and-liquidation-risk (funding rates, volatility, liquidation-risk in crypto perpetuals)
**Sole durable handoff:** `AGENT_HANDOFF.md` — execute its `INITIAL TASK MESSAGE FOR NEXT AGENTIC WORK SESSION — 2026-11-15T15:25:27Z`. `NEXT_SESSION_HANDOFF.md` = tombstone. `AGENT_HANDOFF_20261115T073240Z.md` = RETIRED/SUPERSEDED — ignore.

## IMMEDIATE TASK (default heavy path, NOT trigger-gated)
Execute **`FCLR-SHEK-SCALE-SENSITIVITY-GRID-20261115T073000Z`** now. No `evaluation_summary_FCLR-SHEK-SCALE-SENS-*` artifacts exist as of 2026-11-15T15:25:27Z. Run the START block in `AGENT_HANDOFF.md`; if green run `python3 scripts/fclr_shek_scale.py` (single instance) to emit timestamped SENS artifacts for the full frozen prereg grid (24 cells, both arms), then validate, run full verification, mark frontier `COMPLETED_VALIDATED` with evidence, append execution record in `AGENT_HANDOFF.md`, and install next truthful heavy cell at rank 0.

## Hard constraints
- Never reopen sealed/terminal families or mutate sealed artifacts; never edit `.github/workflows/*`
- No new prereg/threshold tuning/outcome-peeking; no network/paid/credentialed/manual data
- `H2_shek_replication` EXPLORATORY_ONLY, promotable=false; never relabel as forecast skill/boundary-breach/observed-liquidation prediction
- "No trigger → stop cleanly" is NOT completion; heavy work is the default path
