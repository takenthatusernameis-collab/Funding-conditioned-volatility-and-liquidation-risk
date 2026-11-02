# LIQUIDATION_FORWARD_VALIDATE_HEAVY-004i BLOCKER (FRESH)

**TIMESTAMP:** 20261102T160400Z
**CAMPAIGN:** LIQUIDATION_FORWARD_VALIDATE_HEAVY-004i
**STATUS:** BLOCKED_ON_DATA
**PRIORITY:** Track A (liquidation risk) — repo-name-driven

## Evidence (fresh)
- Monitor quick: `ironflow_probe_20261102T160229Z.json` — forward-edge 2026-11/12/2027-01/2027-02 all 404 (events+fills). Tree 200 with ETag cached; no new files.
- Monitor quick: `ironflow_probe_20261102T160238Z.json` — probe_diff added=0 changed=0 removed=0 (confirmed identical)
- Verify: `--verify` ok=True, data_through=2026-10, consecutive_absent=3
- Scan: `ironflow_scan_20261102T150101Z.json` tree 304, no backfill
- Alt hunt: COMPLETE_NO-GO (12 families). Only ironflow >=2026-11 or new admissible unauthenticated source can reopen.

## Probe table (key)
| URL pattern | Method | Status | Notes |
|-------------|--------|--------|-------|
| tree/main?recursive=true | GET (ETag cached) | 200/304 | paths through 2026-10 only |
| data/events/2026-11.parquet | GET/HEAD | 404 | absent |
| data/fills/2026-11.parquet | GET/HEAD | 404 | absent |
| data/events/2026-12.parquet | GET/HEAD | 404 | absent |
| data/fills/2026-12.parquet | GET/HEAD | 404 | absent |
| data/events/2027-01.parquet | GET/HEAD | 404 | absent |
| data/fills/2027-01.parquet | GET/HEAD | 404 | absent |
| data/events/2027-02.parquet | GET/HEAD | 404 | absent |
| data/fills/2027-02.parquet | GET/HEAD | 404 | absent |

## Resume conditions (checkable)
1. Ironflow `data/events/YYYY-MM.parquet` OR `data/fills/YYYY-MM.parquet` for >=2026-11 returns HTTP 200 (unauthenticated). Verify via `python scripts/monitor_ironflow_liquidations.py --quick` (reports genuinely new files).
2. OR new admissible unauthenticated source: >=5 symbols, >=1 complete month OR >=3 non-overlapping 30-day blocks, documented completeness/coverage/license, no keys/signed/requester-pays, schema compatible with frozen FCLR-010 (Hyperliquid-only for Track A).

## Verdict
BLOCKED_ON_DATA. Heavy work mandatory (A-E). No Track B/C conflation. Preserve FCLR-010/FCLR-008 seals.
