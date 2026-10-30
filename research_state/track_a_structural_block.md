# Track A (observed liquidations) — Irrefutable Structural Block (2026-10-30)

## Scope
Track A requires observed liquidation/force-order labels for confirmatory evaluation against frozen holdouts. Priority per repo name is liquidation risk, but observed liquidation labels are not available from admissible unauthenticated public sources.

## Exhaustive probes (evidence)
- Binance data.binance.vision: `futures/um/daily/liquidationSnapshot/`, `futures/um/monthly/liquidationSnapshot/`, CM variants — HTTP 404 (confirmed).
- Binance API: `fapi.binance.com/fapi/v1/forceOrders` returns HTTP 451 restricted location in this environment (confirmed). Authenticated historical liquidation archives not publicly accessible without credentials/terms in accessible unauthenticated form.
- Bybit: public APIs/archives probed; no unauthenticated bulk liquidation census matching temporal coverage/completeness for required windows.
- OKX/Deribit: no obvious unauthenticated bulk liquidationSnapshot archives suitable for confirmatory windows.
- HF/Zenodo/GitHub: general dataset repos searched; any found samples insufficient for frozen 2024 confirmatory windows or lack defensible coverage/completeness. 2026 pilot (FCLR-005) showed no incremental skill on <3 blocks.

Sources cited: `research_state/binance_source_probe.md`, `research_state/liquidation_sources_enumeration.md`, `research_state/liquidation_source_campaign.md`, `research_state/fclr_h004_tracka_viable.json`, `research_state/research_protocol_fclr005.md`, `research_state/final_confirmatory_verdict.md`.

## Conclusion
Track A is **STRUCTURALLY BLOCKED** for admissible 2024 confirmatory windows and not viable for decision-grade evidence under current constraints (unauthenticated, no credentials, no paid/signup). FCLR-005 2026 pilot was exploratory_only with no incremental skill.

## Single materially different free route to unblock (concrete/executable)
1. **Venue-native public liquidation exports with full history**: Find a venue that publishes complete historical liquidation/force-order data as unauthenticated bulk downloads (daily/monthly) with stable paths, machine-readable format, and documented coverage for >=5 instruments across >=3 non-overlapping 30-day blocks. Must be license-compatible for research use without authentication.
2. **Verified academic/third-party archive with provenance**: A citable archive (e.g., Zenodo/HF) containing raw liquidation events with timestamps/symbol/side/price/qty/notional and coverage metadata for required windows, downloadable without credentials.
3. **On-chain/DEX liquidation data**: If perp liquidations map to on-chain events with public indexers and complete coverage for the target venues/symbols, with timestamps alignable to mark prices.

None of the above have been found after exhaustive search. Any future unblock requires discovering such a source and pre-registering a tiny pilot before inspection.
