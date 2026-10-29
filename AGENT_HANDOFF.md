# AGENT HANDOFF — Funding-Conditioned Volatility and Liquidation Risk

UPDATED: 2026-10-29T22:54:25Z
HEAD: c3236af1 (main)
REPO: Funding-conditioned-volatility-and-liquidation-risk

## SINGLE INITIAL TASK FOR NEXT AGENT (MANDATORY)

Repo name centers on funding-conditioned behavior; the forecast gate remains NOT_MET / BLOCKED across FCLR-001-004; H002 partial replication is now COMPLETE. The only live, unblocked heavy campaign is **Track A source discovery for FCLR-H004 (observed liquidation labels)** — enumerate and test additional admissible public liquidation sources before concluding Track A unviable. Campaign: **H004-SOURCE-DISCOVERY-v1**. Do NOT re-attempt FCLR-001-004, do NOT do risk overlay, do NOT touch .github/workflows.

### This session (2026-10-29T22:54:25Z) completed
- `research_state/h002_replication_report.md` written: 88 events (Jan–Mar 2024, 5 symbols), 84 corrected, 4 censored, median 8.0 h, mean 12.6 h; hazard-by-RV-regime table with all-`missing` regime; explicit PARTIAL statement (SSRN HTTP 403); RV-regime contrast infeasible (no Jan–Mar 2024 mark prices in cache; no downloads permitted); correction time separated from volatility forecast/liquidation.
- `research_state/hypothesis_registry.json` updated: FCLR-H002 evidence + status transition to PARTIAL_REPLICATION with full run record, per-symbol stats, artifacts, limitations; fixed mislabeled trailing FCLR-H001 entry (was actually FCLR-004).
- `research_state/run_manifest.json` appended: `h002_partial_replica_v1` run record (git SHA c3236af1, cached Jan–Mar 2024 funding, 88 events, PARTIAL_REPLICATION_COMPLETE).
- `tests/test_funding_correction_replication.py`: 10/10 pass via `python -m unittest tests.test_funding_correction_replication -v`.
- `negative_results_report.md`: NOT updated (H002 is PARTIAL, not null/inconclusive; existing section 3 already records H002 PARTIAL).

### Next session — one task, heavy work
**H004-SOURCE-DISCOVERY-v1: enumerate and test additional admissible public liquidation sources for FCLR-H004.**

Steps (complete in this order):
1. Read `research_state/binance_source_probe.md` (existing evidence: liquidationSnapshot archive HTTP 404; Binance fapi forceOrders HTTP 451 restricted).
2. Enumerate additional admissible public liquidation sources per RESEARCH_PROMPT.md section 5: public GitHub, Zenodo, Hugging Face, institutional or academic archives providing downloadable historical liquidation/event records without signups, API keys, payment, or manually supplied files; other venue-native historical archives with lawful unauthenticated downloads.
3. For each candidate source, run a small unauthenticated request (bounded, with retries/backoff) and record: exact URL/endpoint, access date, test method, no-auth result, license/terms, fields, earliest/latest timestamp, observed cadence, symbol/venue coverage, known gaps, file hashes/ETags where feasible, rejection reason if inadmissible.
4. Write/extend `research_state/liquidation_sources_enumeration.md` with a ranked source table and acceptance status per source.
5. Decision: if any source passes the direct-label quality gate (temporal coverage, meaning of observed records, not a capped sample), mark FCLR-H004 Track A viable and proceed to label construction. If none pass, record structural blocker with evidence and keep Track A BLOCKED; Track B (modeled boundary breaches) and Track C (volatility/stress) proceed independently.
6. Verify: no new downloads beyond small bounded probes; no credentials; no sealed holdouts.

### DO NOT DEVIATE
- Do NOT re-attempt FCLR-001/FCLR-002/FCLR-003/FCLR-004 or any forecast gate (sealed partitions exhausted; FCLR-004 blocked). Forecast gate status: NOT_MET (FCLR-002 CI crosses zero / <3 blocks; FCLR-004 structurally blocked).
- Do NOT touch `.github/workflows`. Do NOT do risk-overlay/trading/simulation. Do NOT merge Track A/B/C.
- No new downloads beyond small bounded source probes; no credentials; no sealed holdouts. Preserve negative/inconclusive results. No threshold-shopping after seeing numbers.

### BOTTLENECKS (REMOVED)
- FCLR-004: structurally blocked (no unused >=30-day window outside sealed partitions); re-attempts forbidden. H004 source discovery is the only viable heavy campaign — do not revisit FCLR-004.
- pytest unavailable in this environment: acceptance test command is `python -m unittest tests.test_funding_correction_replication -v` (10 tests pass).
- RV-regime contrast infeasible for Jan–Mar 2024 (mark-price cache starts 2024-04): documented as limitation in h002_replication_report.md; does not block H002 report.
- SSRN 7529458 HTTP 403: full Shek methodology not recoverable; H002 remains PARTIAL_REPLICATION.

### ACCEPTANCE
- `research_state/h002_replication_report.md` exists with hazard/censoring table by symbol, comparison to paper claim, PARTIAL statement, RV-regime infeasibility note, correction-time/vs-forecast separation. (done this session)
- `research_state/hypothesis_registry.json` FCLR-H002 evidence updated with run record and artifacts. (done this session)
- `research_state/run_manifest.json` `h002_partial_replica_v1` record appended. (done this session)
- `python -m unittest tests.test_funding_correction_replication -v` passes. (verified this session)
- Next session: `research_state/liquidation_sources_enumeration.md` exists with ranked source table and Track A viability decision for FCLR-H004.

### EVIDENCE
- H002 current: 88 events (Jan–Mar 2024, 5 symbols), 84 corrected, 4 censored, median 8.0 h. RV-regime contrast: not computable (no Jan–Mar mark prices cached). Paper claim: 1,696 events / 18 contracts; median 27 h high-RV vs 3 h low-RV.
- FCLR-H004: BLOCKED — no liquidationSnapshot archive (HTTP 404); Binance fapi forceOrders HTTP 451 restricted.

### CONTEXT SNAPSHOT
- Forecast gate: NOT_MET / BLOCKED across FCLR-001-004. Risk-overlay: INELIGIBLE.
- H001: INCONCLUSIVE. H002: PARTIAL_REPLICATION (complete this session). H003: INCONCLUSIVE (no incremental skill). H004: BLOCKED (no direct liquidation labels).
