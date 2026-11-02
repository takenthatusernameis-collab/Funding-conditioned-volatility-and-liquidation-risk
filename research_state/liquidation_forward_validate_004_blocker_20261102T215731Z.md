# LIQUIDATION_FORWARD_VALIDATE_HEAVY-004i BLOCKER (HEAVY WORK REFRESH)
**TIMESTAMP:** 20261102T215731Z
**CAMPAIGN:** LIQUIDATION_FORWARD_VALIDATE_HEAVY-004i
**STATUS:** BLOCKED_ON_DATA
**DATA_THROUGH:** 2026-10
**CONSECUTIVE_ABSENT:** 3
**NEXT AGENT:** NO COASTING — if no new admissible data appears, do heavy work A–E fully; produce >=1 new measurable artifact.

## VERIFIED STATE (THIS REFRESH)
- `python scripts/monitor_ironflow_liquidations.py --verify` → ok=True, data_through=2026-10, consecutive_absent=3, baseline_drift=False
- `python scripts/monitor_ironflow_liquidations.py --quick` → probed ['2026-11','2026-12','2027-01','2027-02'] all 404 (HEAD), tree 304, probe_diff no change, baseline_drift intact, resume_trigger false
- `python scripts/monitor_ironflow_liquidations.py --report` → total_runs aggregated; longest_stable_blocked_streak observed; no trigger
- `python -m unittest discover -s tests -v` → OK (94/94)
- Alt-hunt (FCLR-NEXT-002): COMPLETE_NO-GO across 8 source families; no admissible unauthenticated Track A source beyond ironflow/hyperliquid-liquidations (already used in FCLR-010)

## PROBE SUMMARY (FORWARD EDGE)
| Month | events | fills | classification |
|-------|--------|-------|----------------|
| 2026-11 | 404 | 404 | CONFIRMED_ABSENT |
| 2026-12 | 404 | 404 | CONFIRMED_ABSENT |
| 2027-01 | 404 | 404 | CONFIRMED_ABSENT |
| 2027-02 | 404 | 404 | CONFIRMED_ABSENT |

## HEAVY WORK COMPLETED THIS SESSION
- **A. Automation:** Added `resume_block_summary()` helper; enhanced `quick_diff_summary()` with detailed lists/files; hardened `check_baseline_drift()` to only consider tree-present pairs (all tests pass)
- **B. Tests:** Added `test_quick_diff_summary_with_changes()`; all 94 tests pass
- **C. Blocker doc:** This fresh blocker with probe table, timeline, resume conditions
- **D. Frontier:** Updated below
- **E. Handoff:** Updated below

## RESUME CONDITIONS (CHECKABLE)
1. Ironflow `data/events/YYYY-MM.parquet` OR `data/fills/YYYY-MM.parquet` for >=2026-11 returns HTTP 200 (unauthenticated). Verify via `python scripts/monitor_ironflow_liquidations.py --quick` (tree-change + probe-diff detect flips).
2. OR new admissible unauthenticated source passing strict rubric: >=5 symbols, >=1 complete month OR >=3 non-overlapping 30-day blocks, documented completeness/coverage/license, no keys/signed/requester-pays, schema compatible with frozen FCLR-010 (Hyperliquid-only for Track A).

**ON TRIGGER:** Pre-register BEFORE inspecting outcomes per `research_state/research_protocol_fclr010.md` v1.0; run `python scripts/fclr010_harness.py`; write `research_state/evaluation_summary_LIQUIDATION_FORWARD_VALIDATE_004_<YYYYMMDDTHHMMSSZ>.md` with calibration/LOO/concentration/block-bootstrap CIs>=2000 reps/Holm/gate. Update frontier + cross-track log.

## DEAD ROUTES (NEVER RE-PROBE WITHOUT NEW EVIDENCE)
Binance alt paths/fapi 451, Bybit no liquidation dir, OKX CDN 403/API 404, Deribit failed, academic archives none, GitHub raw 401, HF ochinimus exhausted/wrong types, CryptoDataDownload none, coinglass/hyblock/coinank/paradigm/theblock no admissible unauthenticated source. Evidence in `research_state/track_a_deadend_map.md`, `research_state/track_a_final_block_proof.md`.

**NO SHORTCUTS. HEAVY WORK MANDATORY IF BLOCKED.**
