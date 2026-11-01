# AGENT_HANDOFF.md (DURABLE — SINGLE SOURCE OF TRUTH)
**TIMESTAMP (UTC):** 2026-11-01T22:28:55Z
**REPO:** Funding-conditioned-volatility-and-liquidation-risk
**REPO PRIORITIZATION (INFERRED):** Funding-conditioned volatility → liquidation risk. The repo name is the directive. Funding-conditioned analysis is #1.
**BRANCH/HEAD:** main @ 9b7a7161
**HANDOFF ID:** FCLR-HANDOFF-066-20261101T222855Z
**SUPERSEDES:** FCLR-HANDOFF-065-20261101T222652Z

**STATUS:** Tests 27/27 PASS. Sealed artifacts intact (H001/FCLR-003/FCLR-001..010, Track B/C closed, Track A PASSED). Working tree has only `__pycache__` modifications (harmless). **BOTTLENECK REMOVED:** Hyperliquid `fundingHistory` API confirmed accessible unauthenticated at `https://api.hyperliquid.xyz/info` with `{"type":"fundingHistory","coin":<COIN>,"startTime":<ms>,"endTime":<ms>}`. Covers ironflow range (2025-11-01..2026-10-30), 500 records/call, 235 coins. No keys required.

## IMMEDIATE BLOCKER TO FIX (THE ONLY REASON TO NOT PROGRESS)
**FCLR-LIQMICRO-001 is DEGENERATE.** `src/analysis/liqmicro/features.py::add_funding_features` never consumes `funding_df` - it zeroes `funding_rate`, `funding_sign`, `funding_abs`, `funding_zscore`. D2 has `funding_abs=0.0` with NaN p-values. D3 clustering_by_decile is empty. This violates the repo's priority and invalidates D2/D3. Must be fixed now.

## INITIAL TASK MESSAGE (FOR NEXT AGENTIC SESSION) — TIMESTAMPED 2026-11-01T22:28:55Z
**PRIORITY: P0 | TYPE: HEAVY FUNDING-CONDITIONED RESEARCH | CAMPAIGN: FCLR-LIQMICRO-002 | FIREWALLS ENFORCED**

**MANDATE:** Integrate REAL Hyperliquid funding data and re-run D1-D3 with actual funding variation. Do NOT reopen H001/FCLR-003/FCLR-010. Do NOT merge Binance. Only use ironflow liquidations + Hyperliquid fundingHistory API. Every action must produce concrete artifacts with file:line, provenance, computed values, and acceptance checks. Do heavy verification work - do not shortcut.

### EXECUTE IN STRICT ORDER

#### Step 1: Sanity (2-5 min)
- [ ] `git log --oneline -1 && git status --short && python -m unittest discover -s tests -v` → must remain 27/27 PASS at HEAD 9b7a7161
- [ ] Working tree clean except `__pycache__`

#### Step 2: Fetch real funding data (HEAVY - removes bottleneck)
- [ ] Create `scripts/hyperliquid_funding_fetch.py`. Call `api.hyperliquid.xyz/info` with `{"type":"fundingHistory","coin":<COIN>,"startTime":<ms>,"endTime":<ms>}` for >= symbols overlapping ironflow (prioritize BTC-PERP, ETH-PERP, SOL-PERP, BNB-PERP, XRP-PERP + all ironflow native perps).
- [ ] Paginate in ~21-day chunks across 2025-11-01T00:00:00Z to 2026-10-30T23:59:59Z. Exponential backoff + retry budget. Cache valid responses.
- [ ] Map Hyperliquid coins: strip `-PERP` suffix (BTC-PERP → BTC). Write each to `research_state/data_cache/hyperliquid_funding/<COIN>.parquet` with columns `coin, fundingRate, premium, time` (ms converted to UTC).
- [ ] Write `research_state/liqmicro_funding_audit_002.md` with: coins fetched, records/coin, date range, % overlap with ironflow, `fundingRate.std() > 0` confirmation, SHA-256 of each parquet.
- [ ] **GATE:** >=5 overlapping symbols, `fundingRate.std() > 0` for fetched set, no fabricated values.

#### Step 3: Wire funding into pipeline (IMPLEMENT - fix the zeroing)
- [ ] Extend `src/analysis/liqmicro/ingest.py` to load Hyperliquid funding (`research_state/data_cache/hyperliquid_funding/*.parquet`), normalize symbol mapping (PERP stripped), align to hourly UTC.
- [ ] **FIX** `src/analysis/liqmicro/features.py::add_funding_features`: merge panel with funding on `symbol`+`hour` (UTC). Compute `funding_rate`, `funding_sign = sign(rate)`, `funding_abs = abs(rate)`, `funding_zscore = rolling zscore` by symbol (window reasonable, no look-ahead). If funding missing for symbol-hour, do NOT zero silently - either drop with explicit flag or forward-fill only with justification logged.
- [ ] Verify alignment with a spot check (document file:line and values).
- [ ] **GATE:** `panel['funding_rate'].std() > 0` across non-NaN rows. No column is all zeros.

#### Step 4: Re-run with real funding (HEAVY COMPUTATION)
- [ ] Create/update script to run v2 (e.g. `scripts/run_liqmicro_v2.py` or extend existing). Output to `results/liqmicro_v2/` (never overwrite sealed `results/liqmicro/`).
- [ ] Pre-register: write `research_state/pre_registration_FCLR-LIQMICRO-002.md` noting it's a funding-integration fix to FCLR-LIQMICRO-001, same D1-D3, pre-registered before seeing outcomes.
- [ ] Run D1-D3 with real funding. Save panel, stats, and all tables to `results/liqmicro_v2/`.
- [ ] Write `research_state/evaluation_summary_FCLR-LIQMICRO-002.md` with D1-D3 results, BH FDR, verdict, and explicit statement: **NO reversal of H001, no confirmatory re-test of H001 opened.**
- [ ] **GATE:** Funding features show variation. All tests remain 27/27.

#### Step 5: Validate, integrate, report
- [ ] Confirm funding variation in panel (log std/min/max/counts with file:line).
- [ ] Update `research_state/experiment_frontier.json` with `FCLR-LIQMICRO-002` (status, artifacts, timestamps, HEAD).
- [ ] Update `research_state/cross_track_decision_log.md` documenting funding integration decision and firewall compliance.
- [ ] If funding cannot be obtained for any overlapping symbol despite trying, document concrete blocker with evidence - do NOT fabricate data.

## HARD CONSTRAINTS
- NO Binance merge
- NO reopening H001/FCLR-003/FCLR-010
- All 27 tests must PASS
- No changes to `.github/workflows/`
- Only admissible data: ironflow liquidations (Hyperliquid) + Hyperliquid fundingHistory API
- Never silently zero missing funding - drop/flag with justification
- Sealed artifacts unchanged; write only new `*_002*` artifacts and `results/liqmicro_v2/`
- Hyperliquid-only cross-track firewall

## REQUIRED END-OF-SESSION OUTPUT
1. `git log --oneline -1 && git status --short && python -m unittest discover -s tests -v` (must be 27/27)
2. `research_state/liqmicro_funding_audit_002.md` path + coverage (% overlap, funding std confirmation)
3. Code changes (files + key diffs/line refs) for funding ingestion/wiring
4. `results/liqmicro_v2/` contents + confirmation of funding variation (std>0)
5. `research_state/evaluation_summary_FCLR-LIQMICRO-002.md` with D1-D3 + BH FDR + verdict
6. Explicit statement re: H001 (no reversal, no re-test opened)

## SINGLE HIGHEST-VALUE NEXT TASK
**FCLR-LIQMICRO-002:** Integrate real Hyperliquid funding (unauthenticated `fundingHistory`) and re-analyze funding-conditioned liquidations. This directly matches repo name, fixes the degenerate zeroed-funding bug, and is the only remaining path to meaningful progress without violating any sealed results.
