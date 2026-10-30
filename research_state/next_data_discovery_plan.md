# Next Data Discovery Plan — FCLR-NEXT-001

Updated: 2026-10-30T12:04:30Z
Priority: Find NEW admissible unauthenticated data source

## Targets (minimal for confirmatory)
- >=5 symbols: BTCUSDT, ETHUSDT, BNBUSDT, SOLUSDT, XRPUSDT (or equivalent)
- >=3 non-overlapping 30-day blocks (>=90 days contiguous or partitionable)
- Data type: mark/index prices (for H001-style) OR liquidation census (for H004) OR other relevant
- Unauthenticated, no credentials/signup, public
- Provenance/license documented
- No paid services

## Candidate sources to investigate
1. **Alternative Binance paths** - check other naming in data.binance.vision (liquidationHistory, forceLiquidation, etc.)
2. **Bybit** - check other archive locations, or see if trade data can be used differently (unlikely for census)
3. **OKX** - public data endpoints
4. **Deribit** - check historical data
5. **Academic repos** - Zenodo, OSF, arXiv supplements (check for datasets)
6. **GitHub** - search for CSV/Parquet files in public repos (raw content)
7. **Other HF datasets** - more specific search for 2024 perp liquidation/mark data
8. **CryptoDataDownload** - check all products
9. **CoinMetrics/Kaiko alternatives** - likely paid/gated, skip
10. **Blockchain data** - DeFi only, not relevant to CEX perps

## Validation checklist
- [ ] Unauthenticated download confirmed
- [ ] Schema inspected
- [ ] Coverage (symbols, dates) verified
- [ ] Completeness characterized (census vs sample)
- [ ] License/terms acceptable for research
- [ ] Can integrate with existing pipeline or needs new pipeline
- [ ] No sealed-hold reuse

## GO/NO-GO
**GO only if:** concrete download path + coverage >=5 symbols + >=3 blocks + documented completeness + license OK. Must pre-register experiment BEFORE inspecting outcomes.

**Default NO-GO:** If only partial/sample/undercounted, cannot infer zeros. If wrong window/venue/product, not applicable.

## Immediate actions
1. Probe alternative Binance paths more thoroughly
2. Check OKX public archives
3. Search GitHub raw for "liquidationSnapshot" or "forceOrders" CSV
4. Look for any cached 2024 liquidation data elsewhere in filesystem
5. Document all findings
