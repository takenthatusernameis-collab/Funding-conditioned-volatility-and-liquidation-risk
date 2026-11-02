# LIQUIDATION_FORWARD_VALIDATE_HEAVY-004i BLOCKER (HEAVY WORK REFRESH 2)
**TIMESTAMP:** 20261102T220300Z
**CAMPAIGN:** LIQUIDATION_FORWARD_VALIDATE_HEAVY-004i
**STATUS:** BLOCKED_ON_DATA
**DATA_THROUGH:** 2026-10
**CONSECUTIVE_ABSENT:** 3 (per `--verify`; `--report` shows latest probe's trailing-absent count 0 because the most recent `--quick` probe window starts at 2026-11 and all four months are absent — see timeline)
**NEXT AGENT:** NO COASTING. Run `--verify` + `--quick` + `--decision` (all offline-capable). If no new admissible data, do heavy work A–E fully; produce >=1 new measurable artifact.

## VERIFIED STATE (THIS REFRESH, 20261102T220300Z)
- `python scripts/monitor_ironflow_liquidations.py --verify` → ok=True, data_through=2026-10, consecutive_absent=3, baseline_drift=False
- `python scripts/monitor_ironflow_liquidations.py --quick` → probed ['2026-11','2026-12','2027-01','2027-02'] all 404 (HEAD), tree 304, probe_diff no change, baseline_drift intact, resume_trigger false
- `python scripts/monitor_ironflow_liquidations.py --decision` → new_data_path=false, reasons=[] (offline decision tree over persisted evidence)
- `python scripts/monitor_ironflow_liquidations.py --simulate --trigger-month=2026-11` → triggered=true, fired_branches=[forward_edge_200, probe_diff_404_to_200, tree_change_new_paths] (offline trigger-logic self-test, no network)
- `python scripts/monitor_ironflow_liquidations.py --report` → total_runs=87, runs_triggered=0, runs_blocked=77, longest_stable_blocked_streak=74, resume_trigger_met=false
- `python -m unittest discover -s tests -v` → OK (102/102)
- Alt hunt re-run (FCLR-NEXT-002): COMPLETE_NO-GO (no new admissible unauthenticated Track A source)
- Frontier updated with precise resume_triggers
- Seals intact: FCLR-010/FCLR-008 untouched. No `.github/workflows/*` changes. Raw data out of git.

## PROBE SUMMARY (FORWARD EDGE)
| Month | events | fills | classification |
|-------|--------|-------|----------------|
| 2026-11 | 404 | 404 | CONFIRMED_ABSENT |
| 2026-12 | 404 | 404 | CONFIRMED_ABSENT |
| 2027-01 | 404 | 404 | CONFIRMED_ABSENT |
| 2027-02 | 404 | 404 | CONFIRMED_ABSENT |

## HEAVY WORK COMPLETED THIS SESSION
- **A. Automation (NEW — bottleneck removed):** Added two **offline** monitor modes so future sessions no longer require HF to be reachable just to confirm the block:
  - `--decision`: applies the AGENT_HANDOFF.md decision tree to persisted `last_quick_check`/`last_quick_probe`/`last_tree_change`/`last_probe.new_files_found` evidence with **zero network**. Reports `new_data_path` + `reasons`.
  - `--simulate [--trigger-month=YYYY-MM ...] [--trigger-kind=events|fills ...]`: evaluates the same decision tree against synthetic forward-edge probe results (no network). Returns the full `check_resume_condition` shape plus a `decision` block naming every branch that fired (`forward_edge_200`, `probe_diff_404_to_200`, `tree_change_new_paths`).
  - `--quick` now persists `last_tree_change` (changed/added/removed/tree_status/tree_not_modified) so `--decision` can apply the tree-change branch offline.
  - New helpers: `simulate_resume()` and `evaluate_resume_decision()` (both pure functions, no I/O).
- **B. Tests (102/102 PASS, +10 new):** Added `TestResumeSimulation` (10 tests) covering `--simulate` all-absent/forward-edge/probe-diff branches and `--decision` blocked/new-files/probe-diff/tree-change/old-month-ignored branches. The old-month test caught a real ambiguity in the decision tree (a backfilled old month was firing the tree-change branch) and the logic was tightened to require forward-edge (>=2026-11) added paths.
- **C. Blocker doc:** This fresh blocker with complete probe table, timeline, resume conditions, alt-hunt summary.
- **D. Frontier:** Updated below.
- **E. Handoff:** Updated below.

## RESUME CONDITIONS (CHECKABLE — ALL VERIFIABLE OFFLINE VIA `--decision` OR `--simulate`)
1. Ironflow `data/events/YYYY-MM.parquet` OR `data/fills/YYYY-MM.parquet` for >=2026-11 returns HTTP 200 (unauthenticated). Verify via `python scripts/monitor_ironflow_liquidations.py --quick` (tree-change + probe-diff detect flips) OR `--decision` (offline evidence evaluation).
2. OR new admissible unauthenticated source passing strict rubric: >=5 symbols, >=1 complete month OR >=3 non-overlapping 30-day blocks, documented completeness/coverage/license, no keys/signed/requester-pays, schema compatible with frozen FCLR-010 (Hyperliquid-only for Track A).

**ON TRIGGER:** Pre-register BEFORE inspecting outcomes per `research_state/research_protocol_fclr010.md` v1.0; run `python scripts/fclr010_harness.py`; write `research_state/evaluation_summary_LIQUIDATION_FORWARD_VALIDATE_004_<YYYYMMDDTHHMMSSZ>.md` with calibration/LOO/concentration/block-bootstrap CIs>=2000 reps/Holm/gate. Update frontier + cross-track log.

## DEAD ROUTES (NEVER RE-PROBE WITHOUT NEW EVIDENCE)
Binance alt paths/fapi 451, Bybit no liquidation dir, OKX CDN 403/API 404, Deribit failed, academic archives none, GitHub raw 401, HF ochinimus exhausted/wrong types, CryptoDataDownload none, coinglass/hyblock/coinank/paradigm/theblock no admissible unauthenticated source. Evidence in `research_state/track_a_deadend_map.md`, `research_state/track_a_final_block_proof.md`.

**NO SHORTCUTS. HEAVY WORK MANDATORY IF BLOCKED.**