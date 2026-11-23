# FCLR-TRACKA-SOURCE-AUDIT-01 — Viability Decision and Pivot

**Campaign:** FCLR-TRACKA-SOURCE-AUDIT-01-20261122T225107Z
**Session UTC:** 20261123T014600Z
**Phase:** VIABILITY_DECISION_AND_PIVOT
**Frozen before outcomes:** true — `outcome_data_inspected_before_freeze: false`.

## Viability decision: TRACK_A_STRUCTURALLY_BLOCKED

Track A (observed liquidation labels) is **NOT viable** and is formally closed. No free, unauthenticated source provides a complete observed-liquidation census with defensible provenance and adequate coverage.

## Evidence (all recorded in fclr_tracks01_source_registry_20261123T014600Z.{json,md})

| # | Source | Access result | Track A admissible? | Reason |
|---|---|---|---|---|
| 1 | Binance public archive (data.binance.vision) | HTTP 200 metrics/funding/klines zips; liquidationSnapshot HTTP 404 (daily + monthly) | No | No liquidationSnapshot dataset exists |
| 2 | Bybit public REST v5 | HTTP 403 on kline/funding/liquidation | No | Not unauthenticated in this environment; no credentials requested (§1) |
| 3 | OKX public REST v5 | HTTP 200 candles/funding; liquidation HTTP 404 | No | No public liquidation endpoint |
| 4 | Hyperliquid public API | HTTP 405 GET /info (POST required) | No | No verified unauthenticated deep historical liquidation endpoint |
| 5 | Ironflow / Hugging Face archive | HTTP 200 PAR1 parquet, CC BY 4.0, unauthenticated | No | Capped-sample feed, not a complete census (§15); absence ≠ zero |
| 6 | GitHub/Zenodo/HF institutional archives | No URL verified | No | No verified source |

**Structural-impossibility basis:** three distinct blocked routes spanning two+ source families — access terms (Bybit 403), absent endpoints (Binance liquidationSnapshot 404, OKX liquidation 404), method gating (Hyperliquid 405/POST-only), and incomplete coverage (Ironflow capped sample). Per RESEARCH_PROMPT.md §16 this justifies a new experiment rather than repeating blocked routes.

## Input integrity (sha256 asserted before any outcome)

- fclr_tracks01_source_registry_20261123T014600Z.json: fdcc492878b628d2d7c101735aa5ebf7d757729ee5815bd0c1c4888ae927ad30
- fclr_tracks01_probe_20261123T014600Z.json: d3baafa75f91fa7f5f2de93798206dfe2c8f9268f3f59f1c457c39bbfb84e040
- ironflow_bulk_liquidations_2025-05.parquet: 840bc18b1ec0df9c559e0bf2bff042c36642308f038268922c3dff6c8edb99f3 (on-disk cache consulted, not mutated)
- research_state/data_source_registry.json: consulted only; not rewritten (root cap 499/500)

## Pivot: Track B modeled boundary-breach

**Track B protocol experiment ID:** FCLR-TRACKB-MODELED-BREACH-01-20261123T014600Z

- **Label rule:** modeled hypothetical breach proxy only — never described or reported as observed liquidation. Long and short outcomes kept separate. Does not reconstruct account-specific liquidation mechanics, portfolio/cross margin, liquidation engine execution, or actual forced liquidations (RESEARCH_PROMPT.md §15).
- **Data sources:** Binance public archive markPriceKlines/indexPriceKlines/premiumIndexKlines + klines; Ironflow bulk candles_1h + funding + open_interest (mark_price/oracle_price/open_interest), 18 months 2025-05 .. 2026-10, on disk, sha256-verified.
- **Margin scenario:** pre-registered hypothetical leverage/maintenance margin, frozen before outcomes (see fclr_tracks01_pivot_prereg_20261123T014600Z).
- **Outcome construct:** whether the observed mark-price path crosses the precomputed hypothetical long/short liquidation boundary within a pre-specified horizon.

## Track A status carried forward

NOT_SUPPORTED (Track A observed-liquidation intensity forecast — terminal, FCLR-LIQ-RISK-ESCALATION-09 under session_20261122T224500Z, +0.149% rel QLIKE, fails -2% floor, CI95 includes zero, Holm p=0.6365). Track A source viability now TRACK_A_STRUCTURALLY_BLOCKED. Track B pivot PROTOCOL_FROZEN pending heavy evaluation in this same session.

## Next action (heavy, same session)

Execute fclr_tracks01_eval_20261123T014600Z.{py,json,md} (heavy Track B modeled-breach evaluation on the frozen bulk panel) and fclr_tracks01_recompute_20261123T014600Z.{py,json} (independent stdlib recompute) in THIS session, plus evidence_audit_20261123T014600Z.json and trigger_check_20261123T014600Z.json. The heavy evaluation cannot be deferred to a later session.

**Generated:** 2026-11-23T01:49:35Z
