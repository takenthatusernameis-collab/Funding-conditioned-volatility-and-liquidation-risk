# Track A GO Rubric - Maximally Strict (Hardened 091)
TIMESTAMP (UTC): 20261105T081715Z
SCOPE: Hyperliquid-only for Track A observed liquidation risk (repo priority). No Binance merge. No modeled!=observed conflation.

## Frozen GO Criteria (ALL required)
| Criterion | Requirement | Enforcement |
|---|---|---|
| Authentication | `unauthenticated_only=true`, no keys/tokens/signed requests | `hunt.RUBRIC`, `deep_review.RUBRIC`, probe code paths; adversarial test |
| Cost/access | `no_requester_pays=true` | rubric + classification |
| Coverage | `min_symbols>=5` | rubric |
| Completeness | `>=1 complete month` OR `>=3 non-overlapping 30-day blocks` + `completeness_doc_required=true` | rubric text + pre-reg gate |
| License | `license_ok=true` (permissive/documented for research use) | rubric |
| Schema | `schema_compatible_fclr010=true` (timestamp,symbol,mark_price,funding_rate/liquidation fields per harness contract) | rubric; FCLR-010 harness validates |
| Venue/scope | Hyperliquid-only observed liquidation labels for Track A resume | AGENT_HANDOFF + monitor target |
| Temporal trigger | ironflow `data/events/YYYY-MM.parquet` or `data/fills/YYYY-MM.parquet` for month>=2026-11 HTTP 200 unauthenticated | `monitor_ironflow_liquidations.py --quick` |

## NO-GO / Disqualifiers (immediate)
- Any auth/key/signed header/cookie/wallet requirement.
- Requester-pays or paid tiers required for the needed history.
- Modeled/synthetic liquidation boundaries presented as observed labels.
- Binance/other-venue merge into Track A observed labels.
- Incomplete month without >=3 non-overlapping 30-day blocks.
- Schema incompatible with frozen FCLR-010 without a NEW pre-registered protocol.

## Operational Controls
- Caching: shared URL probe cache + HF search cache with TTL; ETag/conditional reuse where supported. Fast-fail on cache hits.
- Preregister BEFORE outcome inspection: `FCLR010Harness.pre_register_forward_experiment()` must produce a frozen record; `evaluate_forward()` blocks without prereg.
- No threshold-shopping, no holdout reuse, no overlay changes, no retuning.
- Monitor is CLI-invoked (no scheduler/poller loops). Tests enforce absence of scheduler patterns.

## Evidence This Session
- Probes: quick/alt/deep_review all NO-GO/NO TRIGGER (cached, unauthenticated). No rubric-GO source found.
- Tests: `tests/test_tracka_hardening_091.py` enforces rubric alignment/strictness and prereg gate.
