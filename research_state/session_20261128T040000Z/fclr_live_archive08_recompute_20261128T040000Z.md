# FCLR-LIVE-ARCHIVE-08 Recompute — session_20261128T040000Z

**Campaign:** FCLR-LIVE-ARCHIVE-08-20261127T131654Z (Track-B modeled boundary-breach forecast)
**Session:** session_20261128T040000Z
**Generated:** 2026-11-28T04:00:00Z
**Experiment ID:** FCLR-LIVE-ARCHIVE-08

## Status

PENDING_HEAVY_COMPUTATION — Phase 3 independent recompute not yet executed.

## Required action

Run independent stdlib recompute (separate code path from eval) that:
- Rebuilds common support S from cache (mark-price only, all three layouts, dedup by open_time, close>0)
- Confirms all five symbols in every block/fold
- Confirms n_test >= 500
- Reports all_checks_match=true

## Note

Skeleton artifact. The independent recompute must report all_checks_match=true before the gate can pass.
