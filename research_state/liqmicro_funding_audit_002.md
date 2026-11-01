# LIQMICRO FUNDING AUDIT 002 (Hyperliquid fundingHistory)
**TIMESTAMP (UTC):** 2026-11-01T23:16:02Z
**API:** https://api.hyperliquid.xyz/info (unauthenticated, type=fundingHistory)
**Range:** 2025-11-01T00:00:00Z to 2026-10-30T23:59:59Z

## Coins fetched
- AVAX: 8668 records, fundingRate.std()=1.4954177866e-05, sha256=d420bc4efe8b284eb4b974babba1e650fa043dd470440d3ce95d475dec3e48f4
- BNB: 8668 records, fundingRate.std()=1.2583753563e-05, sha256=92c9c9221eb331e2450253d423be2cf37a70a0118961d998a931bed35c11321a
- BTC: 8668 records, fundingRate.std()=8.6671243720e-06, sha256=1c7d2b5d8c40c7b9e3ba84264bce214bb0f694f78aa8623d0b04b336c6a7e430
- DOGE: 8668 records, fundingRate.std()=1.0945539924e-05, sha256=91d3882a699796c354f6aa8159f4a4fa3b61ea05b857f04ae6b10b9c40e42e3b
- ETH: 8668 records, fundingRate.std()=8.8751749644e-06, sha256=2e3851fa6c541fecf3bbf399e8b8b87ad483c876a8010fa66a0f15b628815c5c
- LINK: 8668 records, fundingRate.std()=9.8636912635e-06, sha256=0dec3eaf2667caa7aa9ac277836f22ade3b909ee1623aff3fe441d3973fc8ac2
- SOL: 8668 records, fundingRate.std()=1.5356497768e-05, sha256=5aba146a9a587e4770884b5cfc7a1212d06e161049ed20c33512bb4c5f6e0ee3
- SUI: 8668 records, fundingRate.std()=1.2474588119e-05, sha256=78bd52963727f5a71f36c5eead5ab31a9b2f41deca2aa2d19c61a486c2251fef
- XRP: 8668 records, fundingRate.std()=1.3571629235e-05, sha256=95d980a1688ab5f98764fe9f46683c37f418f546d91b809dde147b5465cf4781

**OVERLAP CHECK:** Ironflow contains native perp symbols (e.g. BTC-PERP). Hyperl perps mapped by stripping `-PERP` -> base coin.
**fundingRate.std() > 0 for all fetched:** YES