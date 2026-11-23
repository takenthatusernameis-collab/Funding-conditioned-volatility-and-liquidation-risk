# FCLR-TRACKA-SOURCE-AUDIT-01 — Source Probe Report (human readable)

## Campaign
FCLR-TRACKA-SOURCE-AUDIT-01-20261122T225107Z

## Session UTC
20261123T014600Z (live probes at 2026-11-23T01:49:26Z .. 01:49:35Z)

## Method
Bounded unauthenticated GET/HEAD probes; stdlib urllib; no auth; no payment; no signup; no manual download; bounded retry budget with exponential backoff.

## Summary
| Metric | Value |
|--------|-------|
| Candidates enumerated | 6 |
| Track A admissible (complete census) | 0 |
| Track A reachable but structurally insufficient | 6 |
| Frozen viability decision | TRACK_A_STRUCTURALLY_BLOCKED |

## Per-source access table

| # | Source | Access result (live) | Track A admissible? | Reason |
|---|--------|----------------------|---------------------|--------|
| 1 | Binance public archive (data.binance.vision) | HTTP 200 on real zips (metrics `BTCUSDT-metrics-2026-01-01.zip` 11,114 B; fundingRate `BTCUSDT-fundingRate-2026-01.zip` 965 B); `liquidationSnapshot` daily+monthly = S3 NoSuchKey (HTTP 404) | No | No `liquidationSnapshot` dataset exists in the public archive |
| 2 | Bybit public REST v5 (api.bybit.com) | kline / funding / liquidation all HTTP 403 | No | Not unauthenticated in this environment; no credentials requested (§1) |
| 3 | OKX public REST v5 (www.okx.com) | candles HTTP 200, funding HTTP 200, `/api/v5/public/liquidation` HTTP 404 | No | No public liquidation endpoint |
| 4 | Hyperliquid public API (api.hyperliquid.xyz) | GET `/info` HTTP 405 (POST-only); no deep historical liquidation endpoint found | No | No verified unauthenticated deep-history liquidation endpoint |
| 5 | Ironflow / Hugging Face liquidations archive | HTTP 200 PAR1 parquet, CC BY 4.0, unauthenticated | No | Capped-sample feed, NOT a complete census (§15); absence ≠ "no liquidation" |
| 6 | Public GitHub / Zenodo / HF institutional archives | No specific URL verified admissible | No | No verified unauthenticated historical observed-liquidation path |

## Frozen viability decision

Decision: `TRACK_A_STRUCTURALLY_BLOCKED` — Track A (observed liquidation labels) is formally closed.
- `outcome_data_inspected_before_freeze: false`
- Structural-impossibility basis: three+ distinct blocked routes spanning ≥2 source families — absent endpoints (Binance liquidationSnapshot 404, OKX liquidation 404), access terms (Bybit 403), method gating (Hyperliquid 405/POST-only), and incomplete coverage (Ironflow capped sample).
- Pivot: Track B modeled boundary-breach protocol `FCLR-TRACKB-MODELED-BREACH-01` (modeled proxy only, §15).

## Source files
- `fclr_tracks01_source_registry_20261123T014600Z.json` — full registry (recovered from git commit `26d28372d`).
- `fclr_tracks01_probe_20261123T014600Z.json` — machine-readable probe results (recovered from git commit `26d28372d`).
- `fclr_tracks01_probe_20261123T014600Z.py` — probe script (recovered from git commit `26d28372d`).
- `fclr_tracks01_viability_decision_20261123T014600Z.{json,md}` — frozen viability decision (recovered from git commit `26d28372d`).

## Notes
No endpoint re-probe performed in this session; artifacts recovered verbatim from git. The audit is frozen; do not redo it. The heavy Track B modeled-breach evaluation (`fclr_tracks01_eval_*`) and independent stdlib recompute (`fclr_tracks01_recompute_*`) MUST run in the same session as this pivot prereg — no prereg-only / audit-only / verify-and-stop escape hatch.
