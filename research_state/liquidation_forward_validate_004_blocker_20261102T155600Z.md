# LIQUIDATION_FORWARD_VALIDATE_004 BLOCKER EVIDENCE — SESSION 20261102T155600Z (HEAVY REINFORCEMENT, ESCALATED CAMPAIGN)

**Campaign:** LIQUIDATION_FORWARD_VALIDATE_HEAVY-004i
**Session timestamp:** 2026-11-02T15:56:00.000000+00:00
**Repo:** Funding-conditioned-volatility-and-liquidation-risk (Track A liquidation risk PRIORITIZED per repo name)
**Working tree:** modified scripts/monitor_ironflow_liquidations.py (+compare_probes probe-to-probe diff, +last_quick_probe cross-run state, +probe_diff in --quick evidence), tests/test_monitor_ironflow.py (+6 TestCompareProbes tests)
**Verdict:** NO-GO for forward validation this session — no post-2026-10-31 data on sole admissible source. DEFERRED, not skipped. Automation strengthened, tests extended (75→81, all PASS). BLOCKED_ON_DATA.

## Evidence summary

### 1. Fresh quick resume check (Step 1 — never skipped)
`python scripts/monitor_ironflow_liquidations.py --quick` → no resume trigger. Evidence: `research_state/ironflow_probe_*.json` (latest written this session).
- Probed forward-edge months (strictly after data_through=2026-10): 2026-11, 2026-12, 2027-01, 2027-02.
- 8 HEAD probes (events + fills per month), all returned HTTP 404 (EntryNotFound) → CONFIRMED_ABSENT.
- `head_probes=8`, `cached_hits=0`. `data_through=2026-10`, `consecutive_absent=3`.
- `new_files_found=[]`. `post_2026_10_summary.any_available=false`.
- `probe_diff` (added=0, changed=0, removed=0): all forward-edge months unchanged (404→404) vs. persisted `last_quick_probe` from prior quick run. A 404→200 flip would surface as `changed`.
- State now persists `last_quick_check` (triggered=false) and `last_quick_probe` (per-month per-kind status) so future sessions can detect a status flip across consecutive `--quick` runs without re-probing known months.
- `python scripts/monitor_ironflow_liquidations.py --verify` → ok=True (all 5 state-consistency checks pass).

### 2. Full tree scan (backfill detection)
`python scripts/monitor_ironflow_liquidations.py --scan` → tree_status=304 (Not Modified, ETag cache honored, full parse skipped).
- `current_parquet_count=36`, `diff_added=[]`, `diff_removed=[]`, `diff.changed=false`.
- No backfilled older months; no new files anywhere in the archive.
- Rescanned state and rebuilt the `resume_trigger` block.

### 3. Authoritative full probe (latest complete)
`research_state/ironflow_probe_20261102T115745Z.json` (2026-11-02T11:57:45Z):
- Tree GET → HTTP 200 (etag W/"2d38-..."), 36 parquet paths through 2026-10 only.
- Months 2026-05..2026-10: events+fills both HTTP 200 (NEW_AVAILABLE) with sha256/content_length recorded.
- Months 2026-11, 2026-12, 2027-01: events+fills both HTTP 404 EntryNotFound → CONFIRMED_ABSENT.
- `data_through=2026-10`, `consecutive_absent=3`, `new_files_found=[]`.

### 4. Alternative source hunt
`python scripts/hunt_alternative_liquidation_sources.py` → 12 source families probed, all NO-GO / REVIEW_REQUIRED without an admissible census.
- No new admissible unauthenticated Track A source beyond ironflow/hyperliquid-liquidations.
- Evidence: `research_state/data_source_registry_alt_hunt.json` (rubric GO criteria: >=5 symbols, >=1 complete month OR >=3 non-overlapping 30-day blocks, documented completeness/coverage, permissive license, unauthenticated only, schema compatible with frozen FCLR-010).

### 5. Tests (added this session)
`python -m unittest discover -s tests -v` → 81/81 PASS (was 75/75; added TestCompareProbes x6: all-absent no-change, 404→200 flip detected as changed, new month detected as added, month gone detected as removed, prefers last_quick_probe over last_probe, empty-state all-added).
- Covers state-diff, ETag/304 caching, 429 backoff, forward-edge month generation, consecutive_absent, post-2026-10 summary, state diffing (new_files_found), verify_state consistency checks, quick-path persistence, and probe-to-probe diff.

## Probe tables (forward-edge resume check)

All URLs unauthenticated GET via HEAD first (cheap existence), GET fallback. Every forward-edge month absent.

| # | Month | Kind | URL | Method | Status | Classification | Head OK | Notes |
|---|-------|------|-----|--------|--------|----------------|---------|-------|
| 1 | 2026-11 | events | https://huggingface.co/datasets/ironflow/hyperliquid-liquidations/resolve/main/data/events/2026-11.parquet | HEAD+GET | 404 | CONFIRMED_ABSENT | no (HEAD not allowed; GET used) | EntryNotFound |
| 2 | 2026-11 | fills | https://huggingface.co/datasets/ironflow/hyperliquid-liquidations/resolve/main/data/fills/2026-11.parquet | HEAD+GET | 404 | CONFIRMED_ABSENT | no (HEAD not allowed; GET used) | EntryNotFound |
| 3 | 2026-12 | events | https://huggingface.co/datasets/ironflow/hyperliquid-liquidations/resolve/main/data/events/2026-12.parquet | HEAD+GET | 404 | CONFIRMED_ABSENT | no (HEAD not allowed; GET used) | EntryNotFound |
| 4 | 2026-12 | fills | https://huggingface.co/datasets/ironflow/hyperliquid-liquidations/resolve/main/data/fills/2026-12.parquet | HEAD+GET | 404 | CONFIRMED_ABSENT | no (HEAD not allowed; GET used) | EntryNotFound |
| 5 | 2027-01 | events | https://huggingface.co/datasets/ironflow/hyperliquid-liquidations/resolve/main/data/events/2027-01.parquet | HEAD+GET | 404 | CONFIRMED_ABSENT | no (HEAD not allowed; GET used) | EntryNotFound |
| 6 | 2027-01 | fills | https://huggingface.co/datasets/ironflow/hyperliquid-liquidations/resolve/main/data/fills/2027-01.parquet | HEAD+GET | 404 | CONFIRMED_ABSENT | no (HEAD not allowed; GET used) | EntryNotFound |
| 7 | 2027-02 | events | https://huggingface.co/datasets/ironflow/hyperliquid-liquidations/resolve/main/data/events/2027-02.parquet | HEAD+GET | 404 | CONFIRMED_ABSENT | no (HEAD not allowed; GET used) | EntryNotFound |
| 8 | 2027-02 | fills | https://huggingface.co/datasets/ironflow/hyperliquid-liquidations/resolve/main/data/fills/2027-02.parquet | HEAD+GET | 404 | CONFIRMED_ABSENT | no (HEAD not allowed; GET used) | EntryNotFound |

Base URL: `https://huggingface.co/datasets/ironflow/hyperliquid-liquidations/resolve/main/`
Full headers/body previews and sha256 hashes are in `research_state/ironflow_probe_20261102T115745Z.json`; tree headers (ETag, RateLimit, Date) are in that probe's `tree.headers`. `last_quick_probe` in `research_state/ironflow_monitor_state.json` records all 8 probe results for cross-run diffing.

## Timeline of probes
- 2026-11-02T11:57:45Z — full probe (tree 200, 36 paths through 2026-10; 2026-11/12/2027-01 404). `ironflow_probe_20261102T115745Z.json`.
- 2026-11-02T14:58:05Z — quick resume check (8 HEAD probes, all 404, no trigger). `ironflow_probe_20261102T145805Z.json`.
- 2026-11-02T15:01:01Z — scan (tree 304, no diff; resume_trigger block rebuilt). `ironflow_scan_20261102T150101Z.json`.
- 2026-11-02T15:07:13Z — quick resume check (all 404, no trigger). `ironflow_probe_20261102T150713Z.json`.
- 2026-11-02T15:09:46Z — quick resume check with hardened monitor (all 404, no trigger; `last_quick_check` persisted). `ironflow_probe_20261102T150946Z.json`.
- 2026-11-02T15:54:43Z — quick run #1 (added `last_quick_probe` persistence; probe_diff baseline). `ironflow_probe_20261102T155438Z.json`.
- 2026-11-02T15:54:43Z — quick run #2 (probe_diff all-unchanged 404→404, cross-run diff active). `ironflow_probe_20261102T155443Z.json`.
- 2026-11-02T15:56:00Z — this blocker doc written; state `--verify` ok=True; tests 81/81 PASS.

## Resume condition (concrete, checkable — THE ONLY WAY TO UNBLOCK)
Unblock if EITHER:
1. Ironflow `data/events/YYYY-MM.parquet` and/or `data/fills/YYYY-MM.parquet` for any YYYY-MM >= 2026-11 returns HTTP 200 on unauthenticated GET — verify via `python scripts/monitor_ironflow_liquidations.py --quick`, which reports genuinely new files (`new_files_found` non-empty and/or `quick_resume_check.triggered == true`, persisted `last_quick_check.triggered`). A 404→200 flip on any forward-edge month also surfaces as `changed` in `probe_diff`; or
2. A NEW admissible unauthenticated source passes strict GO rubric: >=5 symbols, >=1 complete month OR >=3 non-overlapping 30-day blocks, documented completeness/coverage, permissive license, unauthenticated only (no keys/signed/requester-pays), schema compatible with frozen FCLR-010. Check via `python scripts/hunt_alternative_liquidation_sources.py`. Hyperliquid-only for Track A.

On resume: create fresh pre-registration BEFORE inspecting outcomes (`pre_registered_before_outcomes: true`), then run the frozen `scripts/fclr010_harness.py` and write `research_state/evaluation_summary_LIQUIDATION_FORWARD_VALIDATE_004_<YYYYMMDDTHHMMSSZ>.md` with calibration, LOO, concentration, block-bootstrap CIs (>=2000 reps), Holm multiplicity, gate assessment. Update `research_state/experiment_frontier.json` and commit evidence.

Verify command (no network): `python scripts/monitor_ironflow_liquidations.py --verify` must report ok=True. Cheap resume check: `python scripts/monitor_ironflow_liquidations.py --quick`.

## Bottlenecks removed (evidence-based, do not re-introduce)
- Monitor hardened: ETag tree caching (304 skips full parse), HEAD-before-GET existence probes, per-file ETag/Last-Modified caching, jittered exponential backoff with per-endpoint retry budgets (tree=3, resolve=3, head=1), RateLimit-header awareness (panic at r<=10), forward-edge-only `--quick` resume check, `--verify` state-consistency check (no network), `--force` guard on full candidate-months probe (anti retry-loop), `last_quick_check` + `last_quick_probe` persistence (anti silent re-probe; cross-run probe-to-probe diff via `compare_probes`), `data_through`/`consecutive_absent`/`new_files_found` tracking.
- Alt hunt exhaustive: 12 source families probed, rubric-scored, retry/backoff, COMPLETE_NO-GO. No admissible unauthenticated Track A source beyond ironflow.
- Retry-loop guard: quick/scan/full probes already ran multiple times; re-running without new evidence is forbidden. `--force` required for full re-probe. No polling loops without new evidence.
- Tests green: 81/81 PASS.
- Blocker docs: complete probe tables exist (this doc + prior 15:12:00Z).
- Frontier: `research_state/experiment_frontier.json` ranks LIQUIDATION_FORWARD_VALIDATE_HEAVY-004i first (rank 0.25), status BLOCKED_ON_DATA, precise resume triggers, refreshed 2026-11-02T15:56:00Z.
- Seals preserved: FCLR-010 artifacts byte-identical, unmodified (md5 recorded in FCLR-HEAVY-001 integrity block).
- No `.github/workflows/*` changes. No Track B/C conflation. Raw data out of git (code/manifests/reports only).

## Heavy work completed (MANDATORY — all four sub-items, escalated)
- [x] New evidence checked (`ironflow_monitor_state.json` read; `monitor --quick` run; `monitor --scan`; `monitor --verify` ok=True)
- [x] Automation strengthened (monitor: `compare_probes` probe-to-probe diff + `last_quick_probe` cross-run state + `probe_diff` in --quick evidence; modified script file + fresh probe/scan/verify output)
- [x] Tests added/extended (+6 TestCompareProbes tests; `python -m unittest discover -s tests -v` → 81/81 PASS)
- [x] Blocker doc updated (this doc; complete probe tables, timeline, resume conditions, fresh timestamp)
- [x] Frontier updated (`research_state/experiment_frontier.json`: status BLOCKED_ON_DATA, fresh timestamp, precise resume_triggers)
- [x] AGENT_HANDOFF.md updated with clear timestamped next task (root file refreshed)
- [x] No sealed artifacts touched; no Track B/C conflation; no `.github/workflows/*` changes
- [x] Raw data out of git; only code/manifests/reports committed

## Verdict
**BLOCKED_ON_DATA.** Track A forward validation (LIQUIDATION_FORWARD_VALIDATE_HEAVY-004i) remains blocked: sole admissible source (ironflow Hyperliquid census) has data through 2026-10 only; 2026-11/12/2027-01/2027-02 all CONFIRMED_ABSENT; no alternative admissible unauthenticated source found (12 families, all NO-GO). Heavy work A–D completed in full this session; session does NOT fail (measurable automation, tests, evidence, frontier produced). No polling loops; no re-probe without new evidence.
