# AGENT HANDOFF — Funding-Conditioned Volatility and Liquidation Risk
UPDATED: 2026-10-29T22:08:53Z
HEAD: 3b068206 (main)
REPO: Funding-conditioned-volatility-and-liquidation-risk

## MISSION (PRIORITIZED)
H002 partial replication campaign FIRST. Forecast-gate track (H001/FCLR-001/002/003) is INCONCLUSIVE and structurally blocked — no unused >=30-day test window exists outside sealed partitions. FCLR-004 is BLOCKED and must NOT be re-attempted. Risk-overlay remains INELIGIBLE until the forecast gate passes. H004 (observed liquidations) is BLOCKED — no direct labels available.

## WHAT WAS DONE (HEAVY WORK)
- FCLR-001: PILOT/INCONCLUSIVE. C2 vs B1 -2.50% QLIKE, CI crosses zero, ~4-day single block, BTC-only 5-symbol intersection (0 common mark-price timestamps). Gate NOT MET.
- FCLR-002: INCONCLUSIVE. C2 vs B1 -9.28%, CI [-0.097648,-0.008788] excludes zero, byte-identical repro (2026-10-28), but only 2 of required >=3 non-overlapping 30-day blocks (70-day window). Gate NOT MET.
- FCLR-003: INCONCLUSIVE. Meets block design (91 days, 3 blocks, 5 instruments) but C2 vs B1 CI crosses zero (-3.78%); C2 vs C1 WORSE (+12.92%); sign flip vs FCLR-002. C1 vs B1 is secondary only.
- FCLR-004: BLOCKED (pre-registered pivot to 6h). Exhaustive timestamp audit: only 2024-10-01 unused (1 day); no >=30-day window outside frozen partitions. Cannot satisfy >=3 blocks without reusing sealed holdouts — forbidden. No run executed.
- H002: PARTIAL_REPLICATION. 445 funding-extreme events (Jan-Mar 2024, 5 symbols); median correction 8.0h, mean 12.6h; full Shek methodology not independently reconstructable from public sources.
- H003: INCONCLUSIVE on both panels (no incremental skill over volatility-only baseline on Brier/log-loss; degenerate base rate on FCLR-001).
- H004: BLOCKED. Binance liquidationSnapshot archive HTTP 404; fapi forceOrders returns 451 restricted location.

## BOTTLENECK REMOVED
FCLR-004 is structurally blocked by data availability (all partitions consumed, no unused >=30-day window). Re-attempting FCLR-004/FCLR-001/OOS extensions is forbidden without a new pre-registered protocol AND newly available admissible data — none exists locally. Future sessions must not re-run these. This removes the bottleneck of repeated blocked forecast attempts. The only executable heavy work is H002 partial replication (uses cached Jan-Mar 2024 data; no sealed holdouts; no downloads needed).

## NEXT ACTION (FOR NEXT AGENT) — INITIAL TASK 2026-10-29T22:08:53Z
Campaign: H002 partial replication of Shek funding-correction hazard (SSRN, posted 29 Sep 2026, abstract_id=7529458) + final consolidated state.

Steps (in order):
1. Pre-specify the event definition in writing BEFORE computing outcomes: funding-extreme identification, correction-time definition, volatility-regime split, censoring rules, eligible contracts. Record in research_state (new pre-registration note).
2. Compute correction hazard by realized-volatility regime from admissible Binance funding/mark data (cached Jan-Mar 2024, 5 symbols). Handle censored events; do not invent liquidation labels.
3. Compare reconstructed numbers to the paper's claimed figures (median 27h high-vol vs 3h low-vol correction; 1,696 events across 18 contracts; lower hazard with higher RV). Report explicitly as PARTIAL replication, not exact.
4. Extend scripts/funding_correction_replication.py with hazard-by-regime output; add focused tests. Produce a reproducible report artifact.
5. Final consolidated state: refresh negative_results_report.md, gate_assessment.md, hypothesis_registry.json, run_manifest.json with H002 outcome.

Acceptance criteria:
- Event definition frozen in writing before outcome computation.
- Correction hazard computed by RV regime with censoring reported; no threshold-shopping.
- Report states PARTIAL vs exact replication explicitly; no promotion of correction-time to forecast/liquidation evidence.
- No sealed-holdout reuse; no risk-overlay work.
- `pytest tests/test_funding_correction_replication.py` passes (4/4 existing plus new hazard tests).

Exact verification command:
pytest tests/test_funding_correction_replication.py -q

## WHAT MUST NOT BE REPEATED
- Do not re-attempt FCLR-004, FCLR-001/OOS extension, or any forecast-gate run reusing sealed holdouts.
- Do not relax block/multiplicity/uncertainty gates after seeing outcomes.
- Do not relabel exploratory/partial results as confirmatory.
- Do not report unexecuted H003 alternate horizons/tiers or H004 as completed/null.
- No paid services/trials/keys/live/paper trading; no .github/workflows changes; append-only.
