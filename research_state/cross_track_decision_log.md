# Cross-Track Decision Log (Decision-Grade)

**Document type:** End-to-end decision trace from pre-registration to closure
**Generated:** 2026-10-31T02:24:27Z (restored full version 2026-10-31T02:26:45Z after truncation audit)
**DURABLE_HANDOFF:** SINGLE_SOURCE_OF_TRUTH
**HEAD:** 5121e509

## Hypothesis trace

| Hypothesis | Description | Status | Gates/Evidence | Decision |
|---|---|---|---|---|
| H001 (Track C) | Funding+RV+price features improve OOS RV forecast vs RV-only | NOT_SUPPORTED (SEALED_NEGATIVE) | FCLR-001 PILOT/INCONCLUSIVE; FCLR-002 INCONCLUSIVE (2 blocks); FCLR-003 COMPLETE_NEGATIVE (3 blocks, n=10796, CI crosses zero, -3.78% rel); FCLR-006 COMPLETE_NEGATIVE (2 blocks, +0.3686 QLIKE, worse); FCLR-007 COMPLETE_NEGATIVE (0 blocks, +0.0103 QLIKE, worse). CI coverage, block requirements, byte-identical repro, Holm multiplicity. | CLOSED. Risk overlay INELIGIBLE. No further confirmatory runs. |
| H002 (Track A proxy) | Observed liquidation predictability | BLOCKED (NO-GO) | All candidates probed (Binance alt/data.vision 404, fapi forceOrders 451, OKX, Bybit trades non-census, Deribit, Zenodo/OSF/arXiv, GitHub raw 401, HF 2026-only exhausted by FCLR-005, CryptoDataDownload, Tardis/CryptoHFTData paywalled). No admissible unauth source with ≥5 symbols, ≥3 blocks, completeness/license. | BLOCKED. Reopen ONLY if new admissible unauthenticated liquidation data appears. |
| H003 (Track B) | Modeled boundary-breach forecast | COMPLETE_NEGATIVE | FCLR-001-H003 degenerate (base rate 0); FCLR-002-H003 INCONCLUSIVE (no Brier/log-loss win for C2 vs B0 at 5x/10x/20x); FCLR-H003-EXT-001 16 cells no robust incremental skill after Holm. Strict separation enforced. | CLOSED (negative). Never conflated with observed liquidations. |
| H002-correction (secondary) | Shek (SSRN, 29 Sep 2026) funding-extreme correction-time replication | PARTIAL_REPLICATION | 88 events Jan-Mar 2024, 84 corrected, 4 censored, median 8.0h; RV-regime contrast infeasible (no Jan-Mar 2024 mark prices in cache); SSRN HTTP 403 blocks full methodology. | PARTIAL only. Do not promote correction-time association as evidence on volatility skill, boundary breaches, or observed liquidations. |

## Conditions for reopening
- **Track A:** New admissible unauthenticated source providing historical forced-liquidation records with defensible provenance, ≥5 symbols, ≥3 non-overlapping 30-day blocks, documented completeness/gaps, license OK. Must pre-register a new experiment ID BEFORE inspecting any outcomes (RESEARCH_PROMPT.md §16).
- **Track C/B:** None. Closed by evidence; reopening would require violating pre-registration/holdout discipline (forbidden).
- **H002-correction:** Full paper methodology independently reconstructible from admissible public sources (currently blocked by SSRN 403).

## Principles enforced
- Chronological walk-forward, sealed holdouts, 7-day purge/embargo, training-only normalization
- Track separation (A observed / B modeled / C volatility) — proven in `track_b_definitive_separation_audit.md`
- Negatives/inconclusives preserved; Holm familywise correction across the whole declared family
- No credentials/paid data/manual inputs; no trading/paper-trading; no `.github/workflows/*` changes without maintainer auth
- No threshold shopping/tuning on holdouts; no unregistered feature/grid expansion

## Final state
Structural closure confirmed. All confirmatory campaigns complete negative. Forecast gate NOT_MET on every tested panel. Risk overlay INELIGIBLE. Future agents must produce heavy auditable evidence (synthesis/robustness/audits/reproducibility), not status checks — and must not re-open sealed holds, re-run completed experiments, or relax the ≥3-block/≥2%-relative-QLIKE gate.