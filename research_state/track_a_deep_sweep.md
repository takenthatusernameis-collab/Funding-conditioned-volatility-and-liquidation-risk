# Track A Deep Source Sweep (Heavy Evidence)
AUDIT_ID: FCLR-TRA-SWEEP-001
TIMESTAMP: 2026-10-31T01:26:50Z
SCOPE: Exhaustive probe of observed liquidation sources (unauthenticated)

## Candidates probed (per next_data_discovery_plan.md)
- Binance data.vision: liquidationSnapshot archives (HTTP 404), fapi forceOrders (HTTP 451 restricted)
- Bybit: public liquidation data/archives — no unauthenticated bulk census found suitable for ≥5 symbols/≥3 blocks/2024
- OKX: no suitable unauthenticated bulk liquidation census
- Deribit: no
- HuggingFace ochinimus/crypto-liquidation-ticks: covers 2026-07-08..08-06 only (exhausted by FCLR-005, exploratory only, insufficient)
- Zenodo/OSF/arXiv/GitHub raw: searched; no admissible 2024 multi-symbol bulk sets
- CryptoDataDownload: NO-GO

## Evidence
Documented in liquidation_source_campaign.md, track_a_structural_block.md, negative_results_report.md. FCLR-005 treated as exploratory only.

## Conclusion
No admissible unauthenticated source meeting GO criteria (≥5 symbols, ≥3 non-overlapping 30-day blocks, completeness, license OK) found for 2024 confirmatory windows. Structural block confirmed. Sole reopen path: new admissible source passing GO checklist.
