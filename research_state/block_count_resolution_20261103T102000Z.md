# BLOCK_COUNT_RESOLUTION_20261103T102000Z

## Goal
Find any cached/unsealed panel/config with >=5 symbols and >=3 non-overlapping 30-day blocks for Track B (volatility forecasting) without peeking at outcomes to create a new confirmatory cell. Follow protocol: do not relax thresholds after seeing outcomes. Analysis-only.

## Audited sources
- research_state/data_cache/fclr002_panel.json (FCLR-002) - sealed/frozen context
- research_state/.cache/fclr005_panel.json (structure-only, Track A related)
- Root daily zips: markPriceKlines-1h-2024-*, klines-1h-2024-*, indexPriceKlines-1h-2024-*, premiumIndexKlines-1h-2024-* (Jan-Mar 2024 present)
- research_state/fclr008_coverage_audit.json (2026 Jan-Aug, coverage-only)
- research_state/data_cache/* funding/mark dirs

## FCLR-002 (frozen)
- Symbols: BTCUSDT, ETHUSDT, BNBUSDT, SOLUSDT, XRPUSDT (5)
- Test window: 2024-07-23 .. 2024-09-29 (69 days) -> floor(69/30)=2 non-overlapping 30-day blocks
- Result: C2 vs B1 -4.588% rel QLIKE, CI excludes zero but < 3 blocks (underpowered per protocol). NOT_MET.

## FCLR-008 (coverage audit only - no constructed panel JSON found with splits)
- Window: 2026-01-01 .. 2026-08-06 (218 days)
- Symbols: 5 (all present)
- common_timestamps 5232 per symbol
- block_counts.non_overlapping_30d: 7 (remainder 8)
- Split info from protocol: train 2026-01-01..2026-03-17, val 2026-03-25..2026-04-30, test 2026-05-08..2026-08-06 (91-day test) -> >=3 blocks PASS
- However: no cached panel JSON (like fclr002_panel.json) found with rows/splits for FCLR-008 in repo. Building a full leakage-resistant panel from root daily zips requires careful alignment (mark/index/funding, purge/embargo, train-only normalization) - large engineering task. Protocol/handoff states FCLR-008 was run as confirmatory on unsealed data (CI crossed zero). Creating a new cell would require constructing a fresh panel + preregistration before outcome inspection - possible in principle but is heavy engineering.

## Root 2024 data availability
- Jan-Mar 2024 daily markPriceKlines present for all 5 symbols (many days)
- Apr-Sep 2024 also present (FCLR-002 covered Apr-Sep). Jan-Mar exists but not obviously in current frozen FCLR-002 splits.

## Conclusion
- **NO existing cached panel JSON with >=5 symbols and >=3 non-overlapping 30-day blocks is readily loadable** in the same format as fclr002_panel.json except possibly none found.
- FCLR-008 has >=3 blocks by coverage audit, but constructing a leakage-resistant panel from raw archives is non-trivial and would require preregistration before any outcome peek - this is a substantial engineering effort (ingestion/alignment/normalization/splits). Not a "quick scan" - it's a multi-step build.
- The bottleneck remains real. Cannot trivially run new confirmatory on cached structured panel without building it first.

## Recommendation (do NOT violate rules)
1. **Do NOT re-run sealed panels** (FCLR-001..008).
2. **Heavy work continues on FCLR-002 frozen splits** - mechanism deep dive, ablations (done partially), interactions, regime conditioning. This is valuable regardless of block count.
3. **If want to pursue FCLR-008 path**: treat as new experiment ID (e.g. FCLR-011) with full preregistration BEFORE building panel/outcomes. Must meet all criteria. This is heavy but valid if done correctly.
4. **Track A** remains monitor-only.

**Block count resolution:** INSUFFICIENT cached structured panel found. FCLR-008 is promising structurally (>=3 blocks) but requires panel construction + preregistration - high effort, must be done carefully without peeking.
