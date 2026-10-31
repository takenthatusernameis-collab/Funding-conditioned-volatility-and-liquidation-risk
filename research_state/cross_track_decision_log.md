# Cross-Track Decision Log (Decision-Grade)

**Document type:** End-to-end decision trace from pre-registration to closure
**Generated:** 2026-10-31T02:24:27Z
**DURABLE_HANDOFF:** SINGLE_SOURCE_OF_TRUTH

## Hypothesis trace

| Hypothesis | Description | Status | Gates/Evidence | Decision |
|---|---|---|---|---|
| H001 (Track C) | Funding+RV+price features improve OOS RV forecast vs RV-only | NOT_SUPPORTED (SEALED_NEGATIVE) | FCLR-003 (NOT_MET), FCLR-006 (NOT_MET/worse), FCLR-007 (NOT_MET/worse). CI coverage, block requirements, byte-identical repro. | CLOSED. Risk overlay INELIGIBLE. No further confirmatory runs. |
| H002 (Track A) | Observed liquidation predictability | BLOCKED (NO-GO) | All candidates probed (Binance alt, OKX, Deribit, Zenodo/OSF/arXiv, GitHub, HF, CryptoDataDownload). No admissible unauth source with ≥5 symbols, ≥3 blocks, completeness/license. | BLOCKED. Reopen ONLY if new admissible unauthenticated liquidation data appears. |
| H003/H004 (Track B) | Modeled boundary breaches / related | COMPLETE_NEGATIVE | FCLR-H003-EXT-001: no robust incremental skill after Holm across 16 cells. Strict separation enforced. | CLOSED (negative). Never conflated with observed liquidations. |

## Conditions for reopening
- **Track A:** New admissible unauthenticated source providing historical forced-liquidation records with defensible provenance, ≥5 symbols, ≥3 non-overlapping 30-day blocks, documented completeness/gaps, license OK. Must pre-register before inspection of outcomes.
- **Track C/B:** None. Closed by evidence; reopening would require violating pre-registration/holdout discipline (forbidden).

## Principles enforced
- Chronological walk-forward, sealed holdouts, purging/embargo, training-only normalization
- Track separation (A observed / B modeled / C volatility)
- Negatives/inconclusives preserved, multiple-comparisons correction
- No credentials/paid data/manual inputs, no trading/paper-trading, no workflow changes without auth
- No threshold shopping/tuning on holdouts

## Final state
Structural closure confirmed. Future agents must produce heavy auditable evidence (synthesis/robustness/audits), not status checks.
