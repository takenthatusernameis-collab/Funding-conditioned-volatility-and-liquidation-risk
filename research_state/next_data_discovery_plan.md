# Next Data Discovery Plan — FCLR-NEXT-001

Updated: 2026-10-30T13:56:38Z
Priority: Find NEW admissible unauthenticated data source — EXECUTE, do not merely plan
Context: H001 NOT_SUPPORTED on all confirmatory paths; Track A BLOCKED; this is the ONLY remaining path to reopen the confirmatory program.

## Targets (minimal for confirmatory)
- >=5 symbols: BTCUSDT, ETHUSDT, BNBUSDT, SOLUSDT, XRPUSDT (or equivalent)
- >=3 non-overlapping 30-day blocks (>=90 days contiguous or partitionable)
- Data type: mark/index prices (for H001-style) OR liquidation census (for H004) OR other relevant
- Unauthenticated, no credentials/signup, public
- Provenance/license documented
- No paid services

## Candidate sources to investigate (execute in order; each must be a materially distinct source family/method per RESEARCH_PROMPT §16)
1. **Alternative Binance paths** - check other naming in data.binance.vision (liquidationHistory, forceLiquidation, liquidations/, monthly/)
2. **Bybit** - check other archive locations (linear/liquidation/, trading/liquidation/)
3. **OKX** - public data endpoints, static.okx.com CDN
4. **Deribit** - check historical data (historical.deribit.com/)
5. **Academic repos** - Zenodo, OSF, arXiv supplements (check for datasets)
6. **GitHub** - search for CSV/Parquet files in public repos (raw content)
7. **Other HF datasets** - more specific search for 2024 perp liquidation/mark data
8. **CryptoDataDownload** - check all products

## Validation checklist (all required before GO)
- [ ] Unauthenticated download confirmed (HTTP 200, no key/account)
- [ ] Schema inspected
- [ ] Coverage (symbols, dates) verified
- [ ] Completeness characterized (census vs sample)
- [ ] License/terms acceptable for research
- [ ] Can integrate with existing pipeline or needs new pipeline
- [ ] No sealed-hold reuse

## GO/NO-GO
**GO only if:** concrete download path + coverage >=5 symbols + >=3 blocks + documented completeness + license OK. Must pre-register experiment BEFORE inspecting outcomes.

**Default NO-GO:** If only partial/sample/undercounted, cannot infer zeros. If wrong window/venue/product, not applicable.

## Immediate actions (execute this session)
1. Probe alternative Binance paths more thoroughly (liquidations/, liquidationHistory/, forceLiquidation/)
2. Check OKX public archives
3. Search GitHub raw for "liquidationSnapshot" or "forceOrders" CSV
4. Look for any cached 2024 liquidation data elsewhere in filesystem
5. HuggingFace API search for liquidation datasets (unauthenticated GET)
6. Document all findings in research_state/liquidation_source_campaign.md
7. If a source meets GO criteria: pre-register new experiment ID BEFORE examining outcomes, then execute frozen protocol
8. If all routes exhausted: update AGENT_HANDOFF.md with structural blocker + evidence and stop cleanly

## Completion criteria (do not mark complete without)
- >=1 documented probe outcome per candidate source family (#1-#8), OR
- A documented structural blocker with evidence for each route exhausted, OR
- A new GO source found with pre-registered experiment ID
