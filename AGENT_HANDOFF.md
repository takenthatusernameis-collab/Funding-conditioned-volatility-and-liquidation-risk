# AGENT_HANDOFF.md (DURABLE — SINGLE SOURCE OF TRUTH)
**TIMESTAMP (UTC):** 2026-11-01T22:26:52Z
**REPO:** Funding-conditioned-volatility-and-liquidation-risk
**REPO PRIORITIZATION (INFERRED):** Funding-conditioned volatility → liquidation risk. Repo name prioritizes "funding-conditioned" work first. Primary volatility hypothesis H001 NOT_SUPPORTED (FCLR-003 gate NOT_MET). Track A liquidation forecast (FCLR-010) PASSED on Hyperliquid ironflow data; overlay executed hypothetically. Current liqmicro campaign (FCLR-LIQMICRO-001) COMPLETE but DEGENERATE: funding features are ZEROED (funding_rate/sign/abs/zscore all 0.0) because `src/analysis/liqmicro/features.py::add_funding_features` does not consume funding_df. D2 shows funding_abs=0.0 with NaN p-values; D3 clustering_by_decile empty. Repo-name priority demands real funding-conditioned analysis.
**BRANCH/HEAD:** main @ dfab9d7f
**HANDOFF ID:** FCLR-HANDOFF-065-20261101T222652Z
**SUPERSEDES:** FCLR-HANDOFF-064-20261101T222500Z

**STATUS:** Tests 27/27 PASS. Sealed artifacts intact (FCLR-003/H001/FCLR-001..010, Track B/C closed, Track A REOPENED/gate PASSED, overlay ELIGIBLE but not computed). Working tree has modified __pycache__ only (harmless). **CRITICAL BOTTLENOW REMOVED:** Hyperliquid public funding API confirmed accessible UNAUTHENTICATED at `https://api.hyperliquid.xyz/info` via `{"type":"fundingHistory","coin":"<COIN>","startTime":<ms>,"endTime":<ms>}`. Returns 500 hourly records/call (~21 days), paginatable, covers 2024-11-01 onwards (includes full ironflow range 2025-11-01..2026-10-30). 235 coins including BTC, ETH, SOL, XRP. No keys, no signup, no payment. This removes the "funding data missing for Hyperliquid" blocker.

## BOTTLENECKS REMOVED (do not recreate)
- **Funding data missing for Hyperliquid**: REMOVED. Hyperliquid fundingHistory endpoint verified live and unauthenticated. Paginate by coin across 2025-11-01..2026-10-30, cache at `research_state/data_cache/hyperliquid_funding/<COIN>.parquet`.
- Track A structural block: already removed (ironflow passes rubric). Do not re-run exhausted source discovery.
- H002: SSRN 403 permanent block; stop scheduling.

## INITIAL TASK MESSAGE (FOR NEXT AGENTIC SESSION) — TIMESTAMPED 2026-11-01T22:26:52Z
**PRIORITY: P0 | TYPE: HEAVY FUNDING-CONDITIONED RESEARCH | CAMPAIGN: FCLR-LIQMICRO-002 | FIREWALLS ENFORCED**

**MANDATE:** Integrate real Hyperliquid funding data and re-run funding-conditioned liquidation microstructure (D1-D3) with REAL funding variation. Do NOT re-open sealed H001/FCLR-003/FCLR-010. Do NOT merge Binance. Use ONLY admissible data (ironflow liquidations + Hyperliquid fundingHistory API). Every step requires concrete artifacts with file:line/provenance, computed values, and explicit acceptance checks. Heavy verification work first.

### CAMPAIGN FCLR-LIQMICRO-002 — EXECUTE IN STRICT ORDER

**Step 1: Sanity (5 min)**
- [ ] `git log --oneline -1 && git status --short && python -m unittest discover -s tests -v` → must stay 27/27 PASS at HEAD dfab9d7f
- [ ] Working tree clean except `__pycache__/`.

**Step 2: Hyperliquid funding data fetch (HEAVY, removes the core bottleneck)**
- [ ] Write `scripts/hyperliquid_funding_fetch.py` to call `api.hyperliquid.xyz/info` with `{"type":"fundingHistory","coin":<COIN>,"startTime":<ms>,"endTime":<ms>}` for each of the 235 coins (or at least the 199 native perps in ironflow), paginating in 21-day chunks across 2025-11-01..2026-10-30.
- [ ] Add exponential backoff with max retry budget, honor rate limits, cache valid responses.
- [ ] Save each coin's funding history to `research_state/data_cache/hyperliquid_funding/<COIN>.parquet` with columns: coin, fundingRate, premium, time (ms → UTC).
- [ ] Write audit to `research_state/liqmicro_funding_audit_002.md`: coins fetched, records per coin, date range coverage, % overlap with ironflow symbols (BTC-PERP → BTC mapping), funding rate variation (std > 0 confirmed), SHA-256 hashes.
- [ ] **Gate:** >=5 Hyperliquid symbols with funding data overlapping ironflow panel; funding rate std > 0; no fabricated values.

**Step 3: Wire funding into pipeline (IMPLEMENT)**
- [ ] Extend `src/analysis/liqmicro/ingest.py` (or add `funding_ingest.py`) to load Hyperliquid funding aligned to symbol/hour. Map Hyperliquid symbol `BTC-PERP` → coin `BTC`, `ETH-PERP` → `ETH`, etc. (strip `-PERP` suffix, no colon).
- [ ] Fix `src/analysis/liqmicro/features.py::add_funding_features` to actually use `funding_df`: merge panel with funding on symbol+hour, compute `funding_rate`, `funding_sign` = sign(rate), `funding_abs` = abs(rate), `funding_zscore` = rolling z-score. NO look-ahead (use only funding known at prediction time), proper UTC timezone handling.
- [ ] If funding_df missing for a symbol, drop that symbol-hour or forward-fill with explicit flag — do NOT silently zero.
- [ ] **Gate:** Panel has funding_rate with std > 0 across symbols; no all-zero funding columns; alignment verified by spot check (file:line).

**Step 4: Re-run with real funding (HEAVY COMPUTATION)**
- [ ] Rebuild panel with real funding features via `scripts/run_liqmicro.py` (or new `run_liqmicro_v2.py`).
- [ ] Re-test D1-D3 with proper funding variation. Regenerate results in `results/liqmicro_v2/` (versioned, do not overwrite sealed v1).
- [ ] Create `research_state/pre_registration_FCLR-LIQMICRO-002.md` noting this is a funding-integration fix to FCLR-LIQMICRO-001, same hypotheses D1-D3, pre-registered before re-run outcomes.
- [ ] Write `research_state/evaluation_summary_FCLR-LIQMICRO-002.md` with D1-D3 results, BH FDR, verdict, explicit statement re: H001 (no reversal, no re-test).
- [ ] **Gate:** funding features have variation (std > 0); D1-D3 results computed with real funding; all tests still 27/27.

**Step 5: Validate & report**
- [ ] Confirm funding features variation (std > 0) in the panel. If still zero after trying all routes, document blocker with evidence.
- [ ] Explicitly state relation to H001: no reversal, no confirmatory re-test opened.
- [ ] Update `experiment_frontier.json` with FCLR-LIQMICRO-002 status/artifacts/timestamps/HEAD.
- [ ] Update `cross_track_decision_log.md` with funding integration decision.

### MANDATORY VERIFY COMMANDS
```bash
git log --oneline -1 && git status --short && python -m unittest discover -s tests -v 2>&1 | tail -2
```

## HARD CONSTRAINTS
- NO Binance merge, NO FCLR-003/H001/FCLR-010 re-opening
- All 27 tests must PASS
- No .github/workflows changes
- Use only admissible free data (ironflow liquidations + Hyperliquid fundingHistory API)
- Do not fabricate data; if funding unavailable for a symbol, drop/flag — never zero silently
- Sealed artifacts unchanged except new v2 ones
- Cross-track firewall: Hyperliquid funding + Hyperliquid liquidations only; no Binance price panels

## REQUIRED END-OF-SESSION OUTPUT
1. Tests + tree status
2. Funding audit path + coverage (symbols with funding, % overlap with ironflow)
3. Code changes to wire funding (features.py, ingest.py)
4. New results with funding variation confirmed (results/liqmicro_v2/)
5. Updated evaluation summary with D1-D3 verdict
6. Explicit statement re: H001

## SINGLE HIGHEST-VALUE NEXT TASK
**Task:** FCLR-LIQMICRO-002 - Integrate real Hyperliquid funding data (api.hyperliquid.xyz/info fundingHistory, unauthenticated) and re-analyze funding-conditioned liquidations. This is heavy, directly matches repo name "Funding-conditioned-volatility-and-liquidation-risk", and fixes the critical zeroed-funding bottleneck that invalidated FCLR-LIQMICRO-001's D2/D3 results.