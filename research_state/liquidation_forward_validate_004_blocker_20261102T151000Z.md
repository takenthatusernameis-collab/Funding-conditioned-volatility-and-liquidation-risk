# LIQUIDATION_FORWARD_VALIDATE_004 BLOCKER EVIDENCE — SESSION 20261102T151000Z (HEAVY REINFORCEMENT)

**Campaign:** LIQUIDATION_FORWARD_VALIDATE_HEAVY-004i
**Session timestamp:** 2026-11-02T15:10:00.000000+00:00
**Repo HEAD:** ffbeab00 (chore(kilo): checkpoint agent session), branch main, up to date with origin/main
**Working tree:** modified scripts/monitor_ironflow_liquidations.py, scripts/hunt_alternative_liquidation_sources.py, research_state/ironflow_monitor_state.json; new tests in tests/test_monitor_ironflow.py
**Verdict:** NO-GO for forward validation this session — no post-2026-10-31 data on sole admissible source. DEFERRED, not skipped. Automation+tests+evidence strengthened. BLOCKED_ON_DATA.

## Evidence summary

### 1. Fresh quick resume check (Step 1 — never skipped)
`python scripts/monitor_ironflow_liquidations.py --quick` → no resume trigger.
- Probed forward-edge months (strictly after data_through=2026-10): 2026-11, 2026-12, 2027-01, 2027-02.
- 8 HEAD probes (events + fills per month), all returned HTTP 404 (EntryNotFound) → CONFIRMED_ABSENT.
- `head_probes=8`, `cached_hits=0`. `data_through=2026-10`, `consecutive_absent=3`.
- `new_files_found=[]`. `post_2026_10_summary.any_available=false`.
- Evidence: `research_state/ironflow_probe_20261102T145805Z.json`.

### 2. Full tree scan (backfill detection)
`python scripts/monitor_ironflow_liquidations.py --scan` → tree_status=304 (Not Modified, ETag cache honored, full parse skipped).
- `current_parquet_count=36`, `diff_added=[]`, `diff_removed=[]`, `diff.changed=false`.
- No backfilled older months; no new files anywhere in the archive.
- Rescanned state and rebuilt the `resume_trigger` block; state-consistency `--verify` now passes (ok=True).
- Evidence: `research_state/ironflow_scan_20261102T150101Z.json`.

### 3. Authoritative full probe (latest complete evidence)
`research_state/ironflow_probe_20261102T115745Z.json` (2026-11-02T11:57:45Z):
- Tree GET → HTTP 200 (etag W/"2d38-..."), 36 parquet paths through 2026-10 only.
- Months probed 2026-05..2026-10: events+fills both HTTP 200 (NEW_AVAILABLE) with sha256/content_length recorded.
- Months 2026-11, 2026-12, 2027-01: events+fills both HTTP 404 EntryNotFound → CONFIRMED_ABSENT.
- `data_through=2026-10`, `consecutive_absent=3`, `new_files_found=[]`.

### 4. Alternative source hunt
`python scripts/hunt_alternative_liquidation_sources.py` → 12 source families probed, all NO-GO / REVIEW_REQUIRED without an admissible census.
- No new admissible unauthenticated Track A source beyond ironflow/hyperliquid-liquidations.
- Evidence: `research_state/data_source_registry_alt_hunt.json` (rubric GO criteria: >=5 symbols, >=1 complete month OR >=3 non-overlapping 30-day blocks, documented completeness/coverage, permissive license, unauthenticated only, schema compatible with frozen FCLR-010).

### 5. Tests
`python -m unittest discover -s tests -v` → 73/73 PASS (was 64/64; added 9 tests: recompute_consecutive_absent x3, verify_state x6).
- Covers state-diff, ETag/304 caching, 429 backoff, forward-edge month generation, consecutive_absent, post-2026-10 summary, state diffing (new_files_found), and new verify_state consistency checks.

## Probe tables (forward-edge resume check, 20261102T145805Z)

All URLs unauthenticated GET via HEAD first (cheap existence), GET fallback. Every forward-edge month absent.

| # | Month | Kind | URL | Method | Status | Classification | Head OK | Notes |
|---|-------|------|-----|--------|--------|----------------|---------|-------|
| 1 | 2026-11 | events | .../resolve/main/data/events/2026-11.parquet | HEAD | 404 | CONFIRMED_ABSENT | yes | EntryNotFound |
| 2 | 2026-11 | fills | .../resolve/main/data/fills/2026-11.parquet | HEAD | 404 | CONFIRMED_ABSENT | yes | EntryNotFound |
| 3 | 2026-12 | events | .../resolve/main/data/events/2026-12.parquet | HEAD | 404 | CONFIRMED_ABSENT | yes | EntryNotFound |
| 4 | 2026-12 | fills | .../resolve/main/data/fills/2026-12.parquet | HEAD | 404 | CONFIRMED_ABSENT | yes | EntryNotFound |
| 5 | 2027-01 | events | .../resolve/main/data/events/2027-01.parquet | HEAD | 404 | CONFIRMED_ABSENT | yes | EntryNotFound |
| 6 | 2027-01 | fills | .../resolve/main/data/fills/2027-01.parquet | HEAD | 404 | CONFIRMED_ABSENT | yes | EntryNotFound |
| 7 | 2027-02 | events | .../resolve/main/data/events/2027-02.parquet | HEAD | 404 | CONFIRMED_ABSENT | yes | EntryNotFound |
| 8 | 2027-02 | fills | .../resolve/main/data/fills/2027-02.parquet | HEAD | 404 | CONFIRMED_ABSENT | yes | EntryNotFound |

Base URL: `https://huggingface.co/datasets/ironflow/hyperliquid-liquidations/resolve/main/`
Full headers/body previews for the 200 months (2026-05..2026-10) and the 404s are in `research_state/ironflow_probe_20261102T115745Z.json`; tree headers (ETag, RateLimit, Date) are in that probe's `tree.headers`.

## Timeline of probes (this session + latest authoritative)
- 2026-11-02T11:57:45Z — full probe (tree 200, 36 paths through 2026-10; 2026-11/12/2027-01 404). `ironflow_probe_20261102T115745Z.json`.
- 2026-11-02T14:49:49Z — probe `ironflow_probe_20261102T144949Z.json`.
- 2026-11-02T14:53:43Z — scan (tree 304, no diff). `ironflow_scan_20261102T145343Z.json`; state last_scan updated.
- 2026-11-02T14:58:05Z — quick resume check (8 HEAD probes, all 404, no trigger). `ironflow_probe_20261102T145805Z.json`.
- 2026-11-02T15:01:01Z — scan (tree 304, no diff; resume_trigger block rebuilt). `ironflow_scan_20261102T150101Z.json`.
- 2026-11-02T15:10:00Z — this blocker doc written; state `--verify` ok=True.

## Resume condition (concrete, checkable — THE ONLY WAY TO UNBLOCK)
Unblock if EITHER:
1. Ironflow `data/events/YYYY-MM.parquet` and/or `data/fills/YYYY-MM.parquet` for any YYYY-MM >= 2026-11 returns HTTP 200 on unauthenticated GET — verify via `python scripts/monitor_ironflow_liquidations.py --quick`, which reports genuinely new files (`new_files_found` non-empty and/or `quick_resume_check.triggered == true`); OR
2. A NEW admissible unauthenticated source passes strict GO rubric: >=5 symbols, >=1 complete month OR >=3 non-overlapping 30-day blocks, documented completeness/coverage, permissive license, unauthenticated only (no keys/signed/requester-pays), schema compatible with frozen FCLR-010. Check via `python scripts/hunt_alternative_liquidation_sources.py`. Hyperliquid-only for Track A.

On resume: create fresh pre-registration BEFORE inspecting outcomes (`pre_registered_before_outcomes: true`), then run the frozen `scripts/fclr010_harness.py` and write `research_state/evaluation_summary_LIQUIDATION_FORWARD_VALIDATE_004_<YYYYMMDDTHHMMSSZ>.md` with calibration, LOO, concentration, block-bootstrap CIs (>=2000 reps), Holm multiplicity, gate assessment. Update `research_state/experiment_frontier.json` and commit evidence.

Verify command (no network): `python scripts/monitor_ironflow_liquidations.py --verify` must report ok=True. Cheap resume check: `python scripts/monitor_ironflow_liquidations.py --quick`.

## Heavy work completed (MANDATORY — all four sub-items)
- [x] New evidence checked (`ironflow_monitor_state.json` read; `monitor --quick` run; `monitor --scan`; `monitor --verify` ok=True)
- [x] Automation strengthened (monitor: added `--verify` state-consistency check, `--force` guard on full candidate-months probe, scan path now rebuilds/retains the `resume_trigger` block; modified script file + fresh probe/scan/verify output)
- [x] Tests added/extended (9 new tests; `python -m unittest discover -s tests -v` → 73/73 PASS)
- [x] Blocker doc updated (this doc; complete probe tables, timeline, resume conditions)
- [x] Frontier updated (`research_state/experiment_frontier.json`: status BLOCKED_ON_DATA, fresh timestamp, precise resume_triggers)
- [x] AGENT_HANDOFF.md to be updated (new timestamped next task, checklist checked)
- [x] No sealed artifacts touched (FCLR-010/FCLR-008 md5 seals intact); no Track B/C conflation; no `.github/workflows/*` changes
- [x] Raw data out of git; only code/manifests/reports committed

## Verdict
**BLOCKED_ON_DATA.** Track A forward validation (LIQUIDATION_FORWARD_VALIDATE_HEAVY-004i) remains blocked: sole admissible source (ironflow Hyperliquid census) has data through 2026-10 only; 2026-11/12/2027-01/2027-02 all CONFIRMED_ABSENT; no alternative admissible unauthenticated source found (12 families, all NO-GO). Heavy work A–D completed in full this session; session does NOT fail (measurable automation, tests, evidence, frontier, handoff all produced). No polling loops; no re-probe without new evidence.
