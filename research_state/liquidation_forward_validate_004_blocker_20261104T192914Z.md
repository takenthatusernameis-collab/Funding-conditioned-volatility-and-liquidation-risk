# Track A Liquidation Forward Validation - Blocker Report (004i)
Timestamp (UTC): 20261104T192914Z
Git SHA: 478cdf49
Campaign: LIQUIDATION_FORWARD_VALIDATE_HEAVY-004i
Priority: P0 - HEAVY WORK ENFORCED

## Status
BLOCKED - NO NEW DATA. On trigger only. Track A (FCLR-010) is sealed/passed; cannot execute forward validation without admissible new data.

## Evidence (complete probe tables)

### Ironflow (Hyperliquid liquidations) - primary Track A source
- Dataset: ironflow/hyperliquid-liquidations (unauthenticated HF)
- Tree URL: https://huggingface.co/api/datasets/ironflow/hyperliquid-liquidations/tree/main?recursive=true
- Last probe (monitor): 2026-11-02T11:57:45.019472+00:00 (probe_id ironflow_probe_20261102T115745Z)
- Latest quick probe (this session): 20261104T192914Z -> wrote research_state/ironflow_probe_20261104T192914Z.json
- Tree status: 200 (ETag W/"2d38-1SMR0rg9CO86I0iH/hn97Xzs5v8")
- Available months (both data/events/*.parquet and data/fills/*.parquet present):
  - 2025-05 through 2026-10 (18 months each). No 2026-11, 2026-12, 2027-01, 2027-02.
- data_through: 2026-10
- consecutive_absent (forward edge): >=3 (2026-11,12,... probed)
- Head probes (2026-11,12,2027-01,2027-02): no resume trigger
- Baseline drift: intact=True, regressions=0, content_replaced=0, pairs_checked=36
- Kaggle mirror: last updated 2026-11-01T06:18:48.21Z, triggered=False

### Alternative sources (deep review)
Reviewed in prior sessions: research_state/alt_source_deep_review_*.md (20261104T153327Z, 154741Z, 173256Z, 182957Z, 183735Z). Summary:
- Binance public archives: coverage audited; liquidation labels not available in standard public klines/funding; liquidation snapshots not present in unauthenticated archives reviewed.
- Bybit public: checked; no clear unauthenticated historical liquidation event parquet with >=5 symbols and >=1 complete month meeting strict rubric.
- OKX public: checked; no admissible liquidation history found.
- CoinAPI, Tardis, Kaiko, Glassnode: require keys/payment/auth or not dataset hosts - NO-GO.
- Coinglass: web pages, likely require signup/API - NO-GO per strict rubric.
- Other venues: no admissible unauthenticated sources found meeting all rubric criteria.

All alternatives either require auth/payment, lack documented coverage/completeness, lack schema compatibility with frozen FCLR-010, or don't provide >=5 symbols with >=1 complete month / >=3 blocks.

## Strict GO rubric (Track A)
Must ALL hold:
1. Unauthenticated access only (no keys/signed/requester-pays)
2. Observed liquidation labels (not synthetic) with provenance
3. >=5 symbols
4. >=1 complete month OR >=3 non-overlapping 30-day blocks
5. Documented completeness/coverage, permissible license/terms
6. Schema compatible with frozen FCLR-010 (Hyperliquid-only for Track A)
7. Adequate coverage for forward validation (non-overlapping blocks sufficient)

## Resume conditions (concrete, checkable)
**PRIMARY (Ironflow):**
- Ironflow publishes data/events/YYYY-MM.parquet and/or data/fills/YYYY-MM.parquet for any month >= 2026-11
- HTTP 200 on unauthenticated GET to https://huggingface.co/datasets/ironflow/hyperliquid-liquidations/resolve/main/data/events/YYYY-MM.parquet and/or fills
- Verify via: `python scripts/monitor_ironflow_liquidations.py --quick` (should show NEW_AVAILABLE/resume trigger)

**ALTERNATIVE (rubric-GO):**
- New admissible unauthenticated source passes strict GO rubric above
- Evidence: source URL, access date, no-auth test, license/terms, fields/schema, coverage (symbols/months/blocks), completeness docs, hashes/ETags
- Preregister in research_state/fclr010_prereg_$(date -u +%Y%m%dT%H%M%SZ).json BEFORE inspecting outcomes with frozen splits/hypothesis/metrics/stop rule
- Run ONLY frozen FCLR-010 harness (scripts/fclr010_execute.py or scripts/fclr010_harness.py) on existing sealed configuration. No merging sources, no widening scope, no re-tuning.

## Automation improvements (this session)
- Enhanced scripts/monitor_ironflow_liquidations.py with tree_get_cached (ETag caching + TTL fast path), improved HTTPError handling
- Enhanced scripts/hunt_alternative_liquidation_sources.py with EXTENDED_CANDIDATES and improved probing
- Added tests in tests/test_monitor_ironflow.py for fast-path enhancements (all pass)

## Next actions (heavy, non-skippable)
1. Continue monitoring on every session (run monitor quick + deep_review_alt_sources as needed)
2. If new data appears: HALT inspection, preregister FIRST, run only frozen harness
3. If no new data: strengthen automation further, add tests, update blocker doc/frontier
4. Track C remains LOCKED - no re-tuning

## Artifacts
- research_state/ironflow_probe_20261104T192914Z.json
- research_state/ironflow_monitor_state.json (last_check 2026-11-02T05:59:46Z)
- research_state/campaign_sweep_tracka_20261104T192914Z.md
- tests/test_monitor_ironflow.py (82 tests passing)
