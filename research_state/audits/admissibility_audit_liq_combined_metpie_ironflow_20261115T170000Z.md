# §16 Admissibility Audit — combined metpie + ironflow Hyperliquid observed-liquidation panel

**Audit ID:** `admissibility_audit_liq_combined_metpie_ironflow`
**Campaign:** `FCLR-LIQ-COMBINED-PANEL`
**Timestamp (UTC):** 20261115T170000Z
**Protocol:** RESEARCH_PROMPT.md §16
**Network used:** False · **Outcomes inspected:** False · **Canonical state mutated:** False

## Sources

| Source | Rows | Coins | Start | End | Span (d) | License |
|---|---:|---:|---|---|---:|---|
| metpie | 346130 | 179 | 2025-03-22T10:56:26Z | 2025-05-25T14:23:20Z | 64.1437 | CC BY 4.0 |
| ironflow | 2848413 | 468 | 2025-05-25T14:36:58Z | 2026-10-31T23:30:10Z | 524.3703 | CC BY 4.0 |

**Seam:** metpie ends 2025-05-25T14:23:20Z, ironflow starts 2025-05-25T14:36:58Z (gap 0.2273h). Near-seamless abutment (~13 min) consistent with two releases of the same Hyperliquid node-trade liquidation archive; treat as one continuous observed-liquidation series after dedup on (coin, timestamp, notional_usd, tx-hash).

## Schema mapping

- `timestamp`: metpie.time(ms)->UTC ; ironflow.timestamp->UTC
- `coin`: metpie.coin ; ironflow.market with '-PERP' suffix stripped
- `notional_usd`: metpie.notional_usd ; ironflow.notional_usd
- `side`: metpie.side ; ironflow.position_side

## Combined window

- Rows: 3194543 · Coins: 478 · Span: 2025-03-22T10:56:26Z .. 2026-10-31T23:30:10Z (588.5234d)
- 30-day non-overlapping blocks: 19 (2 PRISTINE vs sealed windows)
- Coins >= 5000 events: 63
- Funded coins (cached HL funding): ['AAVE', 'ADA', 'AVAX', 'BCH', 'BNB', 'BTC', 'CRV', 'DOGE', 'ETH', 'LINK', 'LTC', 'NEAR', 'SOL', 'SUI', 'UNI', 'XRP']
- Funded coins >= 5000 events: ['AAVE', 'ADA', 'AVAX', 'BNB', 'BTC', 'CRV', 'DOGE', 'ETH', 'LINK', 'LTC', 'NEAR', 'SOL', 'SUI', 'UNI', 'XRP']
- Funded coins with cached HL candles: ['AAVE', 'ADA', 'AVAX', 'BCH', 'BNB', 'BTC', 'CRV', 'DOGE', 'ETH', 'LINK', 'LTC', 'NEAR', 'SOL', 'SUI', 'UNI', 'XRP']

## Block classification (30-day)

| # | Start | End | Class | Overlap |
|---:|---|---|---|---|
| 0 | 2025-03-22T10:56:26Z | 2025-04-21T10:56:25Z | PRISTINE |  |
| 1 | 2025-04-21T10:56:26Z | 2025-05-21T10:56:25Z | PRISTINE |  |
| 2 | 2025-05-21T10:56:26Z | 2025-06-20T10:56:25Z | ESTIMAND_OVERLAP | TRACKA-VOL-FULLHIST + TRACKA-LIQ-XSEC (NOT_MET/EXPLORATORY_NULL) |
| 3 | 2025-06-20T10:56:26Z | 2025-07-20T10:56:25Z | ESTIMAND_OVERLAP | TRACKA-VOL-FULLHIST + TRACKA-LIQ-XSEC (NOT_MET/EXPLORATORY_NULL) |
| 4 | 2025-07-20T10:56:26Z | 2025-08-19T10:56:25Z | ESTIMAND_OVERLAP | TRACKA-VOL-FULLHIST + TRACKA-LIQ-XSEC (NOT_MET/EXPLORATORY_NULL) |
| 5 | 2025-08-19T10:56:26Z | 2025-09-18T10:56:25Z | ESTIMAND_OVERLAP | TRACKA-VOL-FULLHIST + TRACKA-LIQ-XSEC (NOT_MET/EXPLORATORY_NULL) |
| 6 | 2025-09-18T10:56:26Z | 2025-10-18T10:56:25Z | ESTIMAND_OVERLAP | TRACKA-VOL-FULLHIST + TRACKA-LIQ-XSEC (NOT_MET/EXPLORATORY_NULL) |
| 7 | 2025-10-18T10:56:26Z | 2025-11-17T10:56:25Z | ESTIMAND_OVERLAP | TRACKA-VOL-FULLHIST + TRACKA-LIQ-XSEC (NOT_MET/EXPLORATORY_NULL) |
| 8 | 2025-11-17T10:56:26Z | 2025-12-17T10:56:25Z | ESTIMAND_OVERLAP | TRACKA-VOL-FULLHIST + TRACKA-LIQ-XSEC (NOT_MET/EXPLORATORY_NULL) |
| 9 | 2025-12-17T10:56:26Z | 2026-01-16T10:56:25Z | ESTIMAND_OVERLAP | TRACKA-VOL-FULLHIST + TRACKA-LIQ-XSEC (NOT_MET/EXPLORATORY_NULL) |
| 10 | 2026-01-16T10:56:26Z | 2026-02-15T10:56:25Z | ESTIMAND_OVERLAP | TRACKA-VOL-FULLHIST + TRACKA-LIQ-XSEC (NOT_MET/EXPLORATORY_NULL) |
| 11 | 2026-02-15T10:56:26Z | 2026-03-17T10:56:25Z | ESTIMAND_OVERLAP | TRACKA-LIQ-XSEC-FORWARD + TRACKA-VOL-FORWARD (EXPLORATORY_NULL; region exhausted) |
| 12 | 2026-03-17T10:56:26Z | 2026-04-16T10:56:25Z | ESTIMAND_OVERLAP | TRACKA-LIQ-XSEC-FORWARD + TRACKA-VOL-FORWARD (EXPLORATORY_NULL; region exhausted) |
| 13 | 2026-04-16T10:56:26Z | 2026-05-16T10:56:25Z | ESTIMAND_OVERLAP | TRACKA-LIQ-XSEC-FORWARD + TRACKA-VOL-FORWARD (EXPLORATORY_NULL; region exhausted) |
| 14 | 2026-05-16T10:56:26Z | 2026-06-15T10:56:25Z | ESTIMAND_OVERLAP | FCLR-011 sealed PASS test window (2026-05-08..2026-08-06; EXPLORATORY_ONLY) |
| 15 | 2026-06-15T10:56:26Z | 2026-07-15T10:56:25Z | ESTIMAND_OVERLAP | FCLR-011 sealed PASS test window (2026-05-08..2026-08-06; EXPLORATORY_ONLY) |
| 16 | 2026-07-15T10:56:26Z | 2026-08-14T10:56:25Z | ESTIMAND_OVERLAP | FCLR-011 sealed PASS test window (2026-05-08..2026-08-06; EXPLORATORY_ONLY) |
| 17 | 2026-08-14T10:56:26Z | 2026-09-13T10:56:25Z | ESTIMAND_OVERLAP | FCLR-FWD-VOL-011-CONFIRM forward walk (2026-08-03..2026-10-31; NOT_REPLICATED) |
| 18 | 2026-09-13T10:56:26Z | 2026-10-13T10:56:25Z | ESTIMAND_OVERLAP | FCLR-FWD-VOL-011-CONFIRM forward walk (2026-08-03..2026-10-31; NOT_REPLICATED) |

## §16 criteria

| Criterion | Status | Evidence |
|---|---|---|
| unauthenticated_public_access | PASS | metpie GitHub CC BY 4.0 + ironflow HF; both cached, no auth/keys/signature/requester-pays. |
| provenance_license_documented | PASS | metpie/hyperliquid-liquidation-events CC BY 4.0; ironflow/hyperliquid-liquidations CC BY 4.0; both Hyperliquid node-trade 'LiquidatedMarket' archives. |
| observed_labels_not_modeled | PASS | Both provide observed liquidation events (px/sz/side/notional_usd/tx hash), not synthetic/modeled/proxy. |
| venue_consistency_hyperliquid | PASS | metpie coin == ironflow market(-PERP) on identical universe; seam gap 0.2273h at 2025-05-25; same venue (Hyperliquid perps). |
| ge_5_instruments_with_label_coverage | PASS | 15 coins with >= 5000 events AND cached HL funding: ['AAVE', 'ADA', 'AVAX', 'BNB', 'BTC', 'CRV', 'DOGE', 'ETH', 'LINK', 'LTC', 'NEAR', 'SOL', 'SUI', 'UNI', 'XRP']. |
| ge_3_nonoverlapping_30d_blocks | PASS | combined span 588.5234d -> 19 non-overlapping 30d blocks (>= 3 required); 2 pristine of 19. |
| aligned_market_context_available | PARTIAL | cached HL candles cover 2025-11..2026-10; cached HL funding 2025-11-01 00:00:00.078000+00:00..2026-10-31 23:00:00.044000+00:00; combined window starts 2025-03-22 10:56:26.556000+00:00. Cache does NOT reach the combined window start -> bounded first-time HL candle/funding acquisition for the funded coins is required before panel build. 16 funded coins have a cached candle directory. |

## Determination: **ADMISSIBLE_PENDING_BOUNDED_ACQUISITION**

**Next step.** If ADMISSIBLE(_PENDING_BOUNDED_ACQUISITION): (1) bounded first-time Hyperliquid candle/funding acquisition for the funded coins lacking cache; (2) freeze a NEW prereg (pre-outcomes) for a 24h observed-liquidation-intensity C2-vs-B1 expanding-window walk-forward on the combined 2025-03-22..2025-10-31 window, placing >=3 test blocks in the pristine early segment and/or the estimand-novel 2025-05..2025-10 range; (3) build panel; (4) evaluate; (5) gate + frontier update. No sealed verdict is reopened; no threshold tuning.

**Compliance:** no outcome inspection before prereg freeze; no threshold-shopping; no sealed-holdout reuse; no Binance/2024 conflation; no modeled/proxy/synthetic labels; no `.github/workflows` edits; no network/paid/credentialed/manual data.
