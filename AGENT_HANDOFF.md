# AGENT HANDOFF — Funding-Conditioned Volatility and Liquidation Risk

UPDATED: 2026-10-29T22:48:55Z
HEAD: c3236af1 (main)
REPO: Funding-conditioned-volatility-and-liquidation-risk

## SINGLE INITIAL TASK FOR NEXT AGENT (MANDATORY)

Repo name centers on funding-conditioned behavior; the only live, unblocked track is **FCLR-H002 (funding-extreme correction-time partial replication)**. Campaign: **H002-PARTIAL-REPLICA-v1** — independently assess Shek (SSRN 7529458) funding-extreme correction pattern from cached public data only.

### This session (2026-10-29T22:48:55Z) completed
- `research_state/h002_pre_registration.md` written and FROZEN: extreme definition (trailing 90-day 5th/95th percentile, min 30 history, same-side dedupe), correction definition (first funding back inside band, 168h max follow-up, censoring), RV regime split (trailing 24h RV terciles per symbol), exclusions, eligibility; cites paper claim (1,696 events / 18 contracts; median 27h high-RV vs 3h low-RV; lower hazard with higher RV).
- `scripts/funding_correction_replication.py` extended: hazard-by-RV-regime table, censoring summary, per-symbol counts, load errors, frozen config block.
- `tests/test_funding_correction_replication.py` rewritten (unittest): 10 tests, all pass via `python -m unittest tests.test_funding_correction_replication -v`.
- Pipeline executed on cached Jan–Mar 2024 funding (BTCUSDT/ETHUSDT/BNBUSDT/SOLUSDT/XRPUSDT), no downloads: **88 events, 84 corrected, 4 censored, median correction 8.0h; all RV regimes "missing"** — mark-price cache under `research_state/data_cache/` starts 2024-04, so the RV-regime hazard contrast is infeasible for Jan–Mar 2024. Record as a pre-registered limitation, NOT a blocker: report overall correction statistics and state the RV-regime contrast could not be computed.

### Next session — one task, heavy work
**Write `research_state/h002_replication_report.md` (PARTIAL replication report) and consolidate state.**

Steps (complete in this order):
1. Report: reconstructed event counts, censoring counts, median/mean correction time by symbol and overall; hazard-by-RV-regime table with the "all-missing" regime and explicit statement that the RV-regime contrast could not be computed (no Jan–Mar 2024 mark prices in cache; no new downloads permitted). Compare to paper claim (27h vs 3h; lower hazard with higher RV). Explicit PARTIAL statement: full Shek methodology not independently reconstructible (SSRN HTTP 403 — see research_state/shek_methodology_availability.md). Explicitly separate correction time from volatility forecast/liquidation; no forecast-skill or liquidation claims.
2. Update `research_state/hypothesis_registry.json` (FCLR-H002 evidence + status transition), append an H002 run record to `research_state/run_manifest.json` (preserve existing top-level keys; git SHA c3236af1, data = cached Jan–Mar 2024 funding), update `research_state/negative_results_report.md` only if null/inconclusive findings arise.
3. Verify: `python -m unittest tests.test_funding_correction_replication -v` passes.

### DO NOT DEVIATE
- Do NOT re-attempt FCLR-001/FCLR-002/FCLR-003/FCLR-004 or any forecast gate (sealed partitions exhausted; FCLR-004 blocked). Forecast gate status: NOT_MET (FCLR-002 CI crosses zero / <3 blocks; FCLR-004 structurally blocked).
- Do NOT touch `.github/workflows`. Do NOT do risk-overlay/trading/simulation. Do NOT merge Track A/B/C.
- No new downloads, no credentials, no sealed holdouts. Preserve negative/inconclusive results. No threshold-shopping after seeing numbers.

### BOTTLENECKS (REMOVED)
- FCLR-004: structurally blocked (no unused >=30-day window outside sealed partitions); re-attempts forbidden. H002 is the only viable heavy campaign — do not revisit FCLR-004.
- pytest unavailable in this environment: acceptance test command is `python -m unittest tests.test_funding_correction_replication -v` (10 tests pass).
- RV-regime contrast infeasible for Jan–Mar 2024 (mark-price cache starts 2024-04): documented as a limitation in the report; does not block the PARTIAL report.

### ACCEPTANCE
- `research_state/h002_pre_registration.md` exists and is frozen (done this session).
- `research_state/h002_replication_report.md` exists with hazard/censoring table by symbol, comparison to paper claim, PARTIAL statement, RV-regime infeasibility note, and correction-time/vs-forecast separation.
- `python -m unittest tests.test_funding_correction_replication -v` passes.
- No sealed holdouts reused. No forecast-gate runs.

### EVIDENCE
- H002 current: 88 events (Jan–Mar 2024, 5 symbols), 84 corrected, 4 censored, median 8.0h. RV-regime contrast: not computable (no Jan–Mar mark prices cached). Paper claim: 1,696 events / 18 contracts; median 27h high-RV vs 3h low-RV.

### CONTEXT SNAPSHOT
- Forecast gate: NOT_MET / BLOCKED across FCLR-001-004. Risk-overlay: INELIGIBLE.
- H003: INCONCLUSIVE (no incremental skill). H004: BLOCKED (no direct liquidation labels).
