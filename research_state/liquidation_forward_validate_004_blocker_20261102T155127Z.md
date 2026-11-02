# LIQUIDATION FORWARD VALIDATE 004i - BLOCKER REPORT (FRESH)

**TIMESTAMP:** $(date -u +%Y-%m-%dT%H:%M:%SZ)
**CAMPAIGN:** LIQUIDATION_FORWARD_VALIDATE_HEAVY-004i
**STATUS:** BLOCKED_ON_DATA
**VENUE SCOPE:** Hyperliquid only (Track A). Strict firewall from Track B/C.

## Executive verdict
Ironflow HF dataset `ironflow/hyperliquid-liquidations` has no unauthenticated new monthly files >= 2026-11. Exhaustive alt-hunt completed with NO-GO. Resume only on new ironflow month or admissible new Track A source.

## Evidence timeline (probes)
- 20261102T115745Z: tree 200 (ETag W/"2d38-..."), parquet paths through 2026-10 only (18 events + 18 fills). Months 2026-11/12/2027-01: events+fills 404.
- 20261102T150101Z: scan (tree 304 Not Modified), no diff, 36 parquet paths, no backfill.
- 20261102T150713Z: quick HEAD 8 probes (2026-11/12/2027-01/2027-02 events+fills) all 404, no trigger.
- 20261102T150946Z: quick HEAD 8 probes all 404, no trigger; `last_quick_check` persisted.
- $(date -u +%Y%m%dT%H%M%SZ): quick resumed check executed; no trigger.

## Forward edge probe table (current)
| month | events | fills | classification |
|-------|--------|-------|----------------|
| 2026-11 | 404 | 404 | CONFIRMED_ABSENT |
| 2026-12 | 404 | 404 | CONFIRMED_ABSENT |
| 2027-01 | 404 | 404 | CONFIRMED_ABSENT |
| 2027-02 | 404 | 404 | CONFIRMED_ABSENT |

## Alt-hunt
See `research_state/data_source_registry_alt_hunt.json` (12 families) — COMPLETE_NO-GO. No admissible unauthenticated Track A source beyond ironflow.

## Resume conditions (concrete)
1. Ironflow publishes `data/events/YYYY-MM.parquet` and/or `data/fills/YYYY-MM.parquet` for any month >= 2026-11 with HTTP 200 on unauthenticated GET (verified via `scripts/monitor_ironflow_liquidations.py --quick`). Must be genuinely new (not previously known). Pre-register BEFORE inspecting outcomes.
2. OR a NEW admissible unauthenticated source passes strict GO rubric (>=5 symbols, >=1 complete month OR >=3 non-overlapping 30-day blocks, documented completeness/coverage, permissive license, unauthenticated only, schema compatible with frozen FCLR-010). Hyperliquid-only for Track A.

## Verify
`python scripts/monitor_ironflow_liquidations.py --verify` → ok=True; data_through=2026-10; consecutive_absent=3.

## State
`research_state/ironflow_monitor_state.json`: tree_etag cached, resume_trigger present, last_quick_check updated.
