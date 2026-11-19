# Track A extension preregistration (outcome-blind, frozen)

- campaign: `FCLR-LIQ-TRACKA-EXTENSION-01-20261119T015256Z`
- session: `session_20261119T022824Z`
- artifact: `fclr_tracka_extension01_prereg_20261119T022824Z`
- frozen_before_outcomes: true
- outcome_target_inspected_before_freeze: false

## Source / licence / venue (identical to exploratory prereg)
- Source: ironflow/hyperliquid-liquidations (https://huggingface.co/datasets/ironflow/hyperliquid-liquidations)
- Licence: CC BY 4.0, unauthenticated
- Venue: hyperliquid_perpetuals (main dex)
- Observed labels: true; modeled_or_proxy: false
- Cache: research_state/data_cache/ironflow_bulk/{candles_1h,funding,open_interest,liquidations}/{month}.parquet
- Instrument filter: dex == "" AND market_class == "perp" (main-dex linear perpetual contracts)

## Universe
- 13 coins: BTC, ETH, BNB, SOL, XRP, AVAX, DOGE, LINK, SUI, ARB, OP, APT, ADA

## Window
- 2025-11 .. 2026-10 (12 complete months)
- First half: 2025-11 .. 2026-04 ; Second half: 2026-05 .. 2026-10

## Target (admissibility only; not a forecast test)
- Observed liquidation incidence per (coin, hour_utc)
- Fields: liq_count, liq_notional_usd, liq_long_count, liq_short_count, liq_fills
- Absence from feed is not evidence of no liquidation (missing/unknown, not zero)

## Gates (frozen, identical to exploratory + declared g7)
- g1 provenance hashed: PASS/FAIL
- g2 >= 5 instruments with observed events: PASS/FAIL
- g3 >= 3 complete months (max coin-month 1h gap <= 20%): PASS/FAIL
- g4 max coin-month 1h candle gap <= 20%: PASS/FAIL
- g5 observed-only labels (no modeled/proxy columns): PASS/FAIL
- g6 alignment yield >= 95%: PASS/FAIL
- g7 half-year stability (PRE-DECLARED): both halves independently satisfy g2/g3/g6; report per-half-year event prevalence ratio and per-coin event counts. PASS iff both halves satisfy g2/g3/g6.

## Verdict
- ADMISSIBLE: all gates g1..g7 PASS
- DATA_BLOCKED: any gate FAIL; record exact shortfall (month, coin, gate, observed vs threshold)

## Confirmatory condition
- Register FCLR-LIQ-TRACKA-CONFIRMATORY-01 only from an ADMISSIBLE verdict.
- Registration only; no confirmatory evaluation in this campaign.

## Prohibitions
- No sealed Binance months for outcomes.
- No confirmatory evaluation in this campaign (registration only).
- No re-run of RISK-05/06/07, ROBUST-05, Track C QLIKE.
- No writes to .github/workflows; no heavyweight stats packages; no frozen-session edits.
- pandas/pyarrow only for parquet reads in ingest/alignment; no statsmodels/numpy in core path.
