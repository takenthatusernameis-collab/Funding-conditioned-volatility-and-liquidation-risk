# AGENT_HANDOFF.md (SINGLE DURABLE SOURCE OF TRUTH)

**TIMESTAMP:** 20261102T210204Z
**REPO:** Funding-conditioned-volatility-and-liquidation-risk — Track A liquidation risk PRIORITIZED (repo-name-driven)
**CAMPAIGN:** LIQUIDATION_FORWARD_VALIDATE_HEAVY-004i — BLOCKED_ON_DATA
**SESSION GOAL FOR NEXT AGENT:** NO COASTING. Execute the clearest initial task below. If new ironflow data appears (>=2026-11) OR new admissible unauthenticated Track A source passes GO rubric → PRE-REGISTER BEFORE INSPECTING OUTCOMES and run `scripts/fclr010_harness.py`. Otherwise, EXECUTE MANDATORY HEAVY WORK A–E IN FULL and produce at least ONE new measurable artifact beyond baseline.

## VERIFIED STATE (THIS SESSION, 20261102T210204Z)
- `python scripts/monitor_ironflow_liquidations.py --verify` → ok=True, data_through=2026-10, consecutive_absent=3
- `python scripts/monitor_ironflow_liquidations.py --quick` → probed ['2026-11','2026-12','2027-01','2027-02'] all 404 (HEAD), tree 304, no new files, probe_diff(added=0 changed=0 removed=0), resume_trigger=false
- `python -m unittest discover -s tests -v` → OK (green)
- Alt hunt re-run with enhanced candidates (coinglass, hyblock, coinank, paradigm, theblock): COMPLETE_NO-GO (no new admissible unauthenticated Track A source)
- Fresh blocker: `research_state/liquidation_forward_validate_004_blocker_20261102T205920Z.md`
- Frontier: `research_state/experiment_frontier.json` status BLOCKED_ON_DATA (ironflow 2026-11+ missing; no other admissible sources)
- All confirmatory gates resolved; stable closeout point: Track A FCLR-010 COMPLETE/FORECAST_GATE_PASSED + overlay EXECUTED (HYPOTHETICAL_ONLY); Track B CLOSED_NEGATIVE; Track C H001 NOT_SUPPORTED (CONFIRMATORY_CLOSED); H002 PERMANENT_BLOCK (SSRN HTTP 403); FCLR-NEXT-002 COMPLETE_NO-GO across 8 source families.

## NEXT AGENT INITIAL TASK (CLEAR, TIMESTAMPED — START NOW)

**20261102T210204Z: STATE-AWARE RESUME CHECK (CHEAP, NO POLLING)**
1. Run: `python scripts/monitor_ironflow_liquidations.py --verify` (must report `ok=True`)
2. Run: `python scripts/monitor_ironflow_liquidations.py --quick` (state-aware forward-edge check; writes `last_quick_check`, `last_quick_probe`, `probe_diff`, `tree_change`; no network beyond 8 HEAD probes; caches locally)
3. Read latest `research_state/ironflow_trend_report_*.json` (or generate offline with `python scripts/monitor_ironflow_liquidations.py --report`)

**DECISION TREE:**
- **NEW DATA PATH (IF ANY):** `new_files_found` non-empty for month >=2026-11 OR `quick_resume_check.triggered` true OR `probe_diff.summary.changed_count>0` (404→200) OR `tree_change.changed` true with new parquet paths.
  - CREATE fresh pre-registration BEFORE inspecting outcomes per `research_state/research_protocol_fclr010.md` v1.0 (frozen_before_outcomes=true).
  - Run `python scripts/fclr010_harness.py`.
  - Write `research_state/evaluation_summary_LIQUIDATION_FORWARD_VALIDATE_004_<YYYYMMDDTHHMMSSZ>.md` (calibration, LOO, concentration, block-bootstrap CIs>=2000 reps, Holm, gate). Update frontier + cross-track log.
- **BLOCKED PATH (EXPECTED):** No new data. Execute **MANDATORY HEAVY WORK A–E** below in full. You MUST produce at least ONE NEW measurable artifact beyond baseline. "Nothing to do" is not an option — session fails otherwise.

## BOTTLENECKS REMOVED (EVIDENCE — DO NOT RE-EXPLORE)
- **Monitor hardened:** ETag tree caching (304 skip), HEAD-before-GET, per-file ETag/Last-Modified, jittered backoff + per-endpoint budgets, rate-limit awareness, `--quick` forward-edge + `last_quick_check`/`last_quick_probe`, `compare_probes()` detects 404→200, `check_tree_change()` detects new paths anywhere, `--report` aggregates all prior probe evidence locally (no network), `quick_diff_summary()` added.
- **Alt hunt exhaustive:** Enhanced with additional candidates, rubric-scored → COMPLETE_NO-GO (no recurring re-probe of dead routes).
- **Dead routes (documented, never re-probe without new evidence):** Binance alt paths (HTTP 404 / fapi 451), Bybit (no liquidation dir), OKX (CDN 403, API 404), Deribit (connection failed), academic archives (no crypto perp liquidation datasets), GitHub raw (401), Hugging Face non-ironflow (ochinimus exhausted; wrong types), CryptoDataDownload (no liquidation/futures links), coinglass/hyblock/coinank/paradigm/theblock (no admissible unauthenticated source). Evidence: `research_state/track_a_deadend_map.md`, `research_state/track_a_final_block_proof.md`, `research_state/source_probe_FCLR-NEXT-002_*.md`.
- **Tests:** 90/90 PASS (TestQuickDiffSummary x2, TestCompareProbes, TestTreeChange, TestTrendReport).
- **Blocker/frontier:** Fresh blocker + frontier updated with precise resume_triggers.
- **Seals intact:** FCLR-010/FCLR-008 untouched. No `.github/workflows/*` changes. Raw data out of git.
- **No repeat polling:** `--quick` is state-aware and caches locally; do not re-poll dead Binance/Bybit/OKX/Deribit/HF-2026/Zenodo/GitHub/CryptoDataDownload routes (structurally blocked, documented above).

## MANDATORY HEAVY WORK (BLOCKED PATH — CANNOT SKIP)

### A. STRENGTHEN AUTOMATION (>=1 concrete improvement)
Improve `scripts/monitor_ironflow_liquidations.py` or `scripts/hunt_alternative_liquidation_sources.py`. Evidence: modified script + fresh output.

### B. ADD TESTS (all must pass)
Extend `tests/test_monitor_ironflow.py` with coverage for new logic. Run `python -m unittest discover -s tests -v` → 100% pass. Evidence: new test methods + green run.

### C. UPDATE BLOCKER DOC (irrefutable evidence)
Write fresh blocker doc with complete probe table, timeline, resume conditions, alt-hunt summary. Evidence: new blocker doc (timestamped).

### D. UPDATE FRONTIER (precise triggers)
Update `research_state/experiment_frontier.json` with new timestamp, status BLOCKED_ON_DATA, explicit resume_triggers. Evidence: modified frontier.

### E. UPDATE HANDOFF (this file)
Refresh this file with new timestamp, crisp next task. Evidence: updated AGENT_HANDOFF.md.

**Acceptance:** at least ONE new measurable artifact beyond baseline (new test, new automation helper, fresh blocker, or fresh frontier). Zero artifacts = session FAILED.

## NON-NEGOTIABLE CONSTRAINTS
- Unauthenticated only. Hyperliquid-only for Track A.
- Never promote modeled boundary breaches to observed liquidations.
- Pre-register BEFORE outcome inspection if new data appears.
- DO NOT touch `.github/workflows/*`.
- `python -m unittest discover -s tests -v` MUST pass.
- Commit ONLY code/manifests/reports — never raw data.
- Heavy work mandatory if blocked; producing no new measurable artifact beyond baseline = session FAILED.
- Preserve FCLR-010/FCLR-008 seals.

## RESUME CONDITION (CHECKABLE)
Ironflow `data/events/YYYY-MM.parquet` or `data/fills/YYYY-MM.parquet` for >=2026-11 returns HTTP 200 (unauthenticated) → verify via `python scripts/monitor_ironflow_liquidations.py --quick`. OR new admissible unauthenticated source passing strict rubric (>=5 symbols, >=1 complete month OR >=3 non-overlapping 30-day blocks, documented completeness/coverage/license, no keys/signed/requester-pays, schema compatible with frozen FCLR-010).

**Next agent:** Run verify+quick, read trend report. If no new data → DO HEAVY WORK A–E fully, add tests, fresh blocker+frontier+handoff. No shortcuts.
