# Source Probe: FCLR-NEXT-002 — Family #7 — Hugging Face Datasets

**Probe date:** 2026-11-02T01:00:00Z
**Source family:** Hugging Face unauthenticated API search + download for liquidation/perp datasets
**Campaign:** FCLR-NEXT-002
**Rubric:** unauthenticated==true AND no_keys==true AND symbols>=5 AND blocks>=3 (non-overlapping 30-day blocks) AND completeness_doc==true AND license_ok==true AND census_or_defensible==true

## Endpoints tested

| Endpoint | HTTP status | Result |
|---|---|---|
| https://huggingface.co/api/datasets?search=liquidation&limit=30 | 200 | 11 datasets surfaced |
| https://huggingface.co/api/datasets?search=funding%20rate&limit=20 | 200 | No funding-rate datasets surfaced |
| https://huggingface.co/api/datasets?search=perpetual&limit=20 | 200 | linxy/USDT-M_Perpetual_Futures (price data, not liquidation labels) |

## Datasets evaluated

| Dataset | License | Size | Format | Coverage | Assessment |
|---|---|---|---|---|---|
| ironflow/hyperliquid-liquidations | CC BY 4.0 | 10M<n<100M | parquet | 2025-11-01..2026-10-31, 185-199 symbols, 12 monthly blocks | **ALREADY ADMISSIBLE** — passes ALL rubric items. Census of every Hyperliquid perpetual liquidation. Used in FCLR-010 (gate PASSED). Not a NEW source for FCLR-NEXT-002; already the Track A reopen path. |
| ochinimus/crypto-liquidation-ticks | CC BY 4.0 | 1M<n<10M | csv | 2026-07-08..2026-08-06 (~1 block), 800 symbols | NO-GO — single ~30-day window, 0 non-overlapping 30-day blocks, exhausted by FCLR-005. Does not cover 2024 frozen windows. |
| nick128373/crypto-liquidation-ticks | CC BY 4.0 | 1M<n<10M | csv | Similar to ochinimus | NO-GO — same limitations as ochinimus. |
| Chainticks/defi-liquidations | CC BY 4.0 | 1K<n<10K | parquet | DeFi lending (Aave, Compound) | NO-GO — DeFi lending liquidations, NOT perpetual futures liquidations. Wrong outcome type. |
| carrierone/verilex-defi-liquidations | MIT | — | — | DeFi lending (Aave, Compound, x402) | NO-GO — DeFi lending liquidations, not perp futures. |
| PhysiAI/Bitcoin-Liquidation-Heatmapping | Apache 2.0 | — | — | Bitcoin-only | NO-GO — 1 symbol only (<5), empty data files (.gitattributes + 28-byte README only). |
| PhysiAI/Bitcoin-Liquidation-Heatmapping-1h | Apache 2.0 | — | — | Bitcoin-only | NO-GO — 1 symbol only (<5). |
| craftify2221/hyperliquid-builder-liquidation-panel | ODC-BY | 1M<n<10M | parquet/csv | Hyperliquid builder liquidations | NO-GO — builder-specific subset, overlaps with ironflow (same venue), not a complete census distinct from ironflow. |
| linxy/USDT-M_Perpetual_Futures | MIT | 10M<n<100M | — | Binance USDT-M perp price data | NO-GO for Track A — price/klines data, NOT liquidation labels. Useful for Track C only (already available via data.binance.vision). |
| pCwOrM/werracle-oev-liquidation-dataset-2026 | CC BY 4.0 | 1K<n<10K | csv | DeFi MEV (Morpho Blue, Aave v3) | NO-GO — DeFi MEV liquidations, not perp futures. |
| Gopher-Lab/bankless_Hasu__Hart... | — | n<1K | parquet | DeFi liquidations analysis | NO-GO — DeFi, not perp futures; n<1K symbols coverage insufficient. |
| french-open-data/caracteristiques-des-retraites-* | — | — | — | French retirement data | NO-GO — unrelated domain. |

## Coverage (best admissible candidate: ironflow/hyperliquid-liquidations)
- Symbols: 185 native perpetual markets (199 total incl. HIP-3 builder markets) — PASS (>=5)
- Blocks: 12 monthly blocks (2025-11..2026-10) — PASS (>=3 non-overlapping 30-day blocks)
- Completeness doc: TRUE — dataset card states "Every liquidation on Hyperliquid perpetuals from 1 November 2025 to 30 October 2026: 2,167,823 liquidated positions across 460 markets and 422,181 wallets, $29.9 billion in liquidated notional"
- License OK: TRUE — CC BY 4.0
- Census/defensible: TRUE — each row is a fill Hyperliquid marked as a liquidation
- Unauthenticated: TRUE — HuggingFace resolve/main download, no keys
- no_keys: TRUE

## GO/NO-GO verdict
**ironflow/hyperliquid-liquidations: GO** — passes ALL rubric items. ALREADY USED in FCLR-010 (gate PASSED).
**All other HF datasets: NO-GO** — none meet ALL rubric items. No NEW admissible liquidation source beyond ironflow found on Hugging Face.

## Bottleneck / removal
The only admissible unauthenticated liquidation census on Hugging Face is ironflow/hyperliquid-liquidations, already exploited via FCLR-010. No additional distinct source family found. This bottleneck (no second independent liquidation census) cannot be removed within current admissible sources.

## Next materially different route
Track A is already open via ironflow (FCLR-010 COMPLETE, gate PASSED, overlay EXECUTED). No further source discovery needed for Track A reopen. FCLR-NEXT-002 confirms no additional independent liquidation census exists beyond ironflow.
