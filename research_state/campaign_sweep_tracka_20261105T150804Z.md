# Campaign Sweep Track A — FCLR-NEXT-100 (HEAVY-099 ROOT-CAUSE FIX)
**Timestamp (UTC):** 20261105T150804Z
**Track:** A (liquidation risk) — BLOCKED / NO RESUME. Volatility (Track C) SEALED/LOCKED. Track B NOT_SUPPORTED.
**Mode:** NO-COAST MANDATORY. Measurable delta required. Zero churn.

## Root cause found and fixed (the actual blocker)
The 098 invariant "ironflow probes == 2" was **not** being maintained by the monitor itself. Two defects in `scripts/monitor_ironflow_liquidations.py`:

1. **`_consolidate_ironflow_probes` dedup skipped the unlink.** The dedup `if pid in seen: continue` was meant to prevent *double-archiving* a probe already in the canonical digest, but it also skipped `old.unlink()`. A probe archived in a prior session (e.g. `ironflow_probe_20261105T130449Z`, already present in `ironflow_probe_digest_latest.json` from the 098 run) was therefore re-archived on every later `--quick` run while its file was never deleted. Verified 20261105T1505Z: **3** `ironflow_probe_*` files (2 live + 1 digest), churn reported `3 -> 3`, `removed 0`. Invariant is **==2**.
2. **Churn was measured and written AFTER consolidation.** The evidence file was written, then consolidated (which can delete it when an older-but-newer-mtime file exists), then re-written with the churn record — re-creating the file consolidation had just removed.

Both fixed. Split dedup into two concerns (skip the entry append, always unlink non-latest) and moved the churn measurement to a single write before a single consolidation pass.

## Measurable delta (before/after)
| Area | Before (099 entry, broken) | After (100, fixed) | Proof |
|---|---|---|---|
| `ironflow_probe_*` files | **3** (2 live + 1 digest) | **2** (1 live + 1 digest) | `ls research_state/ironflow_probe_*.json` |
| Consolidation `removed` | 0 (dedup skipped unlink) | **1** (unlinked the stale live probe) | `ironflow_probe_20261105T150753Z.json` churn `3 -> 2` |
| Idempotency | re-archived every run | second pass `removed=0`, count stays 2 | `test_conolidation_idempotent_probe_count_stays_two` |
| Tests | 274 OK | **276 OK** (+2) | `python -m unittest discover tests` |
| Root `research_state` md+json | 161 | **161** (`<=163`) | unchanged (no new recurring families) |
| Canonical alt outputs | 2 | 2 | `alt_source_deep_review_latest.md`, `alt_source_scan_latest.json` |
| `tracka_resume_check.py` | pass | pass (`pass:true`, `<5s`, `network:false`, `writes_real_research_state:false`) | unchanged |
| Trigger | NO DATA (data_through=2026-10) | NO DATA (data_through=2026-10) | `monitor --quick` |

## Evidence run (all deterministic, no real `research_state` writes except the required sweep/blocker/handoff)
- `python -m unittest discover tests` → **276 OK**
- `python scripts/tracka_resume_check.py` → `pass: true`, `network: false`, `writes_real_research_state: false`
- `python scripts/monitor_ironflow_liquidations.py --quick` → `No resume trigger. data_through=2026-10 probed=['2026-11','2026-12','2027-01','2027-02'] head_probes=8 cached_hits=0 probe_diff(added=0 changed=0 removed=0) baseline_drift(intact=True regressions=0 content_replaced=0 pairs_checked=18 method=state_only_tree_unchanged) kaggle_mirror(updated=False last=2026-11-01T06:18:48.21Z triggered=False)`
- `python scripts/deep_review_alt_sources.py` → canonical latest only, `cache_hits=13 cache_misses=1`
- `python scripts/hunt_alternative_liquidation_sources.py` → canonical latest only, `candidates=11, source=cache`
- `python scripts/fclr010_harness.py` → frozen config, offline, no outcome inspection

## New tests (deterministic, tmp-only, no network)
- `tests/test_monitor_ironflow.py::TestConsolidation::test_consolidation_deletes_previously_archived_live_probe` — a live probe whose entry is already in the canonical digest must still be physically removed; asserts `len(live)==1`, `stale` not exists, exactly one digest, no duplicate entries, `removed==1`.
- `tests/test_monitor_ironflow.py::TestConsolidation::test_conolidation_idempotent_probe_count_stays_two` — second consolidation pass removes nothing; count stays 2.

## Resume condition (only, unchanged)
`ironflow data/events/YYYY-MM.parquet` or `data/fills/YYYY-MM.parquet` for month>=2026-11 HTTP 200 unauthenticated **OR** admissible unauthenticated Hyperliquid observed-liquidation source passes the strict full-manifest GO gate. **Hyperliquid-only. PREREGISTER BEFORE INSPECTING OUTCOMES.**

## Next task
FCLR-NEXT-101: keep the probe-count invariant machine-checked in the resume/monitor path and re-verify on every session entry; Track A remains monitor-only until admissible Hyperliquid data appears.