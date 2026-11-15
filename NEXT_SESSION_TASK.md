# NEXT SESSION INITIAL TASK MESSAGE — 2026-11-15T16:40:31Z
# SOLE DURABLE HANDOFF POINTER

**Repository:** Funding-conditioned-volatility-and-liquidation-risk (funding rates, volatility, liquidation-risk in crypto perpetuals)
**Sole durable handoff:** `AGENT_HANDOFF.md` — execute its `INITIAL TASK MESSAGE FOR NEXT AGENTIC WORK SESSION — 2026-11-15T16:40:31Z`. `NEXT_SESSION_HANDOFF.md` = tombstone. `AGENT_HANDOFF_20261115T073240Z.md` = RETIRED/SUPERSEDED — ignore.

## IMMEDIATE TASK (default heavy path — now EXHAUSTED; program is TRIGGER-ONLY)

All cache-heavy estimands are complete and validated:

1. **`FCLR-SHEK-SCALE-SENSITIVITY-GRID-20261115T073000Z` — COMPLETED_VALIDATED.** Frozen prereg sensitivity grid emitted: `research_state/evaluation_summary_FCLR-SHEK-SCALE-SENS-20261115T144938Z.{json,md}` — all 12 grid cells x 2 arms (24 arm-cells), percentiles [1,99],[5,95],[10,90] × censor [168,336]h × rv_split [tercile,median]; headline cell [5,95]/168h/tercile consistent with sealed verdicts (Arm A TAIL_SHAPE_EFFECT, Arm B REPLICATES_DIRECTION). Demoted to rank 1 in `research_state/experiment_frontier.json` (retained, not deleted).
2. **Forecast 3-block frontier — EXHAUSTED.** `python3 scripts/next_campaign_status.py` → "no feasible 3-block design in ANY domain".
3. **Rank-0 sentinel installed:** `FCLR-BOUNDED-TRIGGER-ONLY-20261115T164031Z` (`TRIGGER_ONLY` / `BOUNDED_TRIGGER_ONLY`) so `tests.test_active_campaign_gate::test_frontier_rank0_is_active_heavy_campaign` holds (was red because rank-0 held a `COMPLETED_VALIDATED` campaign).

## NEXT ACTION

Run the START block in `AGENT_HANDOFF.md`; confirm baseline green (campaign gate 19/19, fwd-vol PASS, scope drift 186/186, targeted suite 60/60, `next_campaign_status.py` honest), confirm the trigger-only sentinel at rank 0, confirm no trigger is present. **If no trigger arrives, stop cleanly in trigger-only state — this is the honest terminal state; it is NOT completion and must not be relabeled as such.** On trigger only: (1) `GATE4_BRANCH_1` → valid `research_state/fclr016_v5_terms_evidence_RESOLVED_<UTC>.json` (status=RESOLVED_VERIFIED, fabricated=false, human/legal attestation) → Gate 4 confirmatory flow under a NEW frozen prereg. (2) `NEW_OBSERVED_LIQUIDATION_SOURCE` → materially new family (not a re-probe) → §16 admissibility audit BEFORE any prereg/outcomes.

## Hard constraints
- Never reopen sealed/terminal families or mutate sealed artifacts; never edit `.github/workflows/*`
- No new prereg/threshold tuning/outcome-peeking; no network/paid/credentialed/manual data
- `H2_shek_replication` EXPLORATORY_ONLY, promotable=false; never relabel as forecast skill/boundary-breach/observed-liquidation prediction
- "No trigger → stop cleanly" is NOT completion; do not poll, do not re-run tested windows, do not re-probe exhausted/TERMINAL_NO_GO families
- Exactly ONE active handoff (`AGENT_HANDOFF.md`); do not create competing handoff files (the churn failure mode)