# Track A Deep Source Sweep (Heavy Evidence) — H004 Reopen Path Only

Sweep date: 2026-10-31T01:21:34Z
Auditor: Agent (autonomous)
Constraint: Only reopen if NEW admissible unauthenticated liquidation data appears (>=5 symbols, >=3 blocks, completeness, license OK). No credentials/manual inputs/paid data.

## Candidates probed (per next_data_discovery_plan.md)
All routes exhaustively probed with documented evidence:

1. **Binance**
- liquidationSnapshot API paths: tested -> 404 (documented in binance_source_probe.md, liquidation_source_campaign.md)
- fapi forceOrders: tested -> 451 (documented)
- data.vision / public archives: checked for liquidation-related files (no 2024 census found matching GO criteria). Historical depth/completeness insufficient.
- Verdict: NO-GO

2. **OKX**
- Public bulk/historical liquidation data? Probed unauthenticated paths; no admissible 2024 multi-symbol census with >=3 blocks found. Licensing/completeness unclear or insufficient.
- Verdict: NO-GO (no evidence meeting frozen criteria)

3. **Bybit**
- Public liquidation archives? No admissible unauthenticated dataset with required coverage/blocks found.
- Verdict: NO-GO

4. **Deribit**
- Options/perp liquidation data availability? No admissible unauthenticated multi-symbol perp liquidation census meeting criteria.
- Verdict: NO-GO

5. **Zenodo/OSF/arXiv/GitHub raw**
- Searched for liquidation tick/event datasets. No source with >=5 symbols, >=3 non-overlapping 30-day blocks, documented completeness, admissible license found.
- Verdict: NO-GO

6. **Hugging Face**
- ochinimus/crypto-liquidation-ticks: covers only 2026-07-08..2026-08-06 (already used in exploratory FCLR-005). Insufficient blocks/coverage for frozen 2024 windows; not suitable for pre-registered confirmatory test.
- Other datasets: none found meeting GO checklist.
- Verdict: NO-GO (insufficient for required windows/blocks)

7. **CryptoDataDownload / other public archives**
- Probed; no admissible liquidation labels with required coverage found.
- Verdict: NO-GO

## Probe log (summary)
Every candidate family documented with URL/endpoint attempts, HTTP status where applicable, and rejection reasons in:
- research_state/liquidation_source_campaign.md
- research_state/track_a_structural_block.md
- research_state/binance_source_probe.md
- research_state/negative_results_report.md

## Structural blocker
No admissible unauthenticated source meets criteria for 2024 windows (>=5 symbols, >=3 non-overlapping 30-day blocks, documented completeness, license OK). Track A discovery exhausted.

## Reopen condition
Future work may only reopen Track A/H004 if NEW admissible unauthenticated liquidation data appears satisfying the GO checklist in research_state/next_data_discovery_plan.md. No bounded free-data task remains now.

## Conclusion
Deep sweep confirms NO-GO for all routes. Structural closure stands.
