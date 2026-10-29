# AGENT HANDOFF — Funding-Conditioned Volatility and Liquidation Risk
UPDATED: 2026-10-29T22:10:00Z
HEAD: 3b068206 (main)
REPO: Funding-conditioned-volatility-and-liquidation-risk

## SINGLE INITIAL TASK FOR NEXT AGENT (MANDATORY)
PRIORITY 1 — EXECUTE HEAVY WORK (no credentials/downloads/sealed holdouts). Repo name centers on funding-conditioned behavior; H002 is the only live track.

CAMPAIGN: H002-PARTIAL-REPLICA-v1 — Independently assess Shek (SSRN 7529458) funding-extreme correction pattern.

### DO NOT DEVIATE
- Do NOT re-attempt FCLR-001/FCLR-002/FCLR-003/FCLR-004 or any forecast-gate (sealed partitions exhausted; FCLR-004 blocked).
- Do NOT touch .github/workflows. Do NOT do risk-overlay/trading/simulation. Do NOT merge Track A/B/C.
- Preserve negative/inconclusive results. No threshold-shopping after seeing numbers.

### STEPS (MUST COMPLETE IN THIS SESSION)
1. FREEZE DEFINITION (write first, before computation)
   - Create/update `research_state/h002_pre_registration.md` with: extreme definition (funding rate threshold/normalization), correction definition (time to cross frozen threshold back), RV regime split (pre-registered bins), censoring (max window, uncorrected), eligible symbols/venues, exclusion rules.
   - Cite paper claim explicitly: 1,696 events / 18 contracts; median 27h (high-vol) vs 3h (low-vol); lower hazard with higher RV.

2. COMPUTE FROM CACHED DATA (no new downloads)
   - Use cached Jan-Mar 2024 funding/mark/index/premium where present (BTCUSDT/ETHUSDT/BNBUSDT/SOLUSDT/XRPUSDT). Extend `scripts/funding_correction_replication.py` to output hazard-by-RV-regime with censoring summary.
   - Handle uncorrected events as censored; report counts by symbol/regime.

3. COMPARE & REPORT AS PARTIAL
   - Compare reconstructed medians/hazard to paper claims. Write `research_state/h002_replication_report.md` stating PARTIAL replication (full methodology not reconstructible from public sources). Explicitly separate correction-time from volatility forecast/liquidation.

4. TESTS + STATE CONSOLIDATION
   - Add/extend tests in `tests/test_funding_correction_replication.py` for hazard regime logic/censoring; ensure all pass.
   - Update `research_state/hypothesis_registry.json` (H002 status/evidence), `research_state/run_manifest.json`, `research_state/negative_results_report.md` if needed.

### ACCEPTANCE
- `research_state/h002_pre_registration.md` exists with frozen definition.
- `research_state/h002_replication_report.md` exists with hazard table + comparison + PARTIAL statement.
- `pytest tests/test_funding_correction_replication.py -q` passes.
- No sealed holdouts reused. No forecast-gate runs.

### EVIDENCE
- H002 current: 445 events, median 8.0h, mean 12.6h (Jan-Mar 2024). Full Shek methods not independently reconstructible.

## BOTTLENECKS (REMOVED)
FCLR-004 structurally blocked (no unused >=30-day window outside sealed partitions). Re-attempts forbidden. This handoff forces H002 as the only viable heavy campaign.

## CONTEXT SNAPSHOT
- Forecast gate: INCONCLUSIVE/BLOCKED across FCLR-001-004.
- H003: INCONCLUSIVE (no incremental skill).
- H004: BLOCKED (no direct liquidation labels).
- Risk overlay: INELIGIBLE.
