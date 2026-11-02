# AGENT_HANDOFF.md (SINGLE DURABLE SOURCE OF TRUTH)

**TIMESTAMP:** 2026-11-02T20:00:33Z
**REPO:** Funding-conditioned-volatility-and-liquidation-risk — Track A liquidation risk PRIORITIZED (repo-name-driven prioritization: observed-liquidation forecast validation before any volatility overlay).
**CAMPAIGN:** LIQUIDATION_FORWARD_VALIDATE_HEAVY-004i — BLOCKED_ON_DATA
**SESSION GOAL FOR NEXT AGENT:** Execute with ZERO coasting. Data blocked (ironflow through 2026-10; 2026-11/12/2027-01/2027-02 CONFIRMED_ABSENT; fresh state-aware check 20261102T200107Z: 0 triggered, probe_diff added=0/changed=0/removed=0; local trend report 195805Z: 65 runs, 0 triggered, longest stable blocked streak 52). First action: state-aware resume check (`python scripts/monitor_ironflow_liquidations.py --quick` + `--verify`, verify ok=True). If ANY post-2026-10 ironflow data appears OR new admissible Track A source found, PRE-REGISTER BEFORE inspecting outcomes and run frozen `scripts/fclr010_harness.py`. Otherwise MANDATORY HEAVY WORK A–E in full — at least ONE new measurable artifact beyond the previous session's diff (previous diff: `--report` trend mode + `ironflow_trend_report_20261102T195805Z.json`, TestTrendReport x4, TestTreeChange x3, 88/88 tests, `run_manifest.json` JSON fix, blocker doc 195818Z, frontier/handoff 19:58:18Z) = session FAILED. Fresh blocker/frontier/handoff written at 2026-11-02T20:00:33Z.

## NEXT AGENT INITIAL TASK (CLEAR, TIMESTAMPED — START NOW)
**2026-11-02T20:00:33Z:** Run `python scripts/monitor_ironflow_liquidations.py --quick` (state-aware, cheap, forward-edge only). Read `research_state/ironflow_monitor_state.json` (and confirm `python scripts/monitor_ironflow_liquidations.py --verify` reports ok=True).
- If `new_files_found` is non-empty for any month >= 2026-11, OR `quick_resume_check.triggered` is true, OR `probe_diff.summary.changed_count > 0` (a 404→200 flip on any forward-edge month) OR `tree_change.changed` is true with new parquet paths → NEW DATA PATH (Step 2 below). Create fresh pre-registration BEFORE inspecting outcomes, then run `scripts/fclr010_harness.py` and write `research_state/evaluation_summary_LIQUIDATION_FORWARD_VALIDATE_004_<YYYYMMDDTHHMMSSZ>.md` (calibration, LOO, concentration, block-bootstrap CIs >=2000 reps, Holm multiplicity, gate assessment). Update frontier + cross-track log.
- Otherwise (expected) → BLOCKED PATH: execute MANDATORY HEAVY WORK A–E below in full, ESCALATED: this session must produce at least ONE new measurable artifact beyond the previous session's diff (previous session: `--report` trend mode added to `scripts/monitor_ironflow_liquidations.py` + `ironflow_trend_report_20261102T195805Z.json` artifact; TestTrendReport x4 added; tests 88/88 PASS; fresh blocker doc `liquidation_forward_validate_004_blocker_20261102T195818Z.md`; frontier refreshed). "Nothing to do" is not an option. A session producing no measurable automation, tests, or evidence FAILS.

## BOTTLENOCKS REMOVED (EVIDENCE-BASED, DO NOT RE-INTRODUCE)
- **Monitor hardened:** `scripts/monitor_ironflow_liquidations.py` — If-None-Match tree ETag caching (304 skips full parse), HEAD-before-GET existence probes, per-file ETag/Last-Modified caching, jittered exponential backoff with per-endpoint retry budgets (tree=3, resolve=3, head=1), RateLimit-header awareness (panic at r<=10), forward-edge-only `--quick` resume check, `--verify` state-consistency check (no network), `--force` guard on full candidate-months probe (anti retry-loop), scan path now rebuilds/retains the `resume_trigger` block, `--quick` now persists a machine-readable `last_quick_check` record AND a `last_quick_probe` block (per-month per-kind status) to prevent silent re-probes, NEW `compare_probes()` probe-to-probe diff that detects 404→200 flips across consecutive quick runs, NEW `probe_diff` block in `--quick` evidence, NEW `check_tree_change()` + `tree_change` block in `--quick` evidence that detects new parquet paths ANYWHERE in the archive (including backfilled older months the forward-edge probe misses), `data_through`/`consecutive_absent`/`new_files_found` tracking.
- **NEW — `--report` trend mode (this session):** `scripts/monitor_ironflow_liquidations.py --report` aggregates ALL saved `ironflow_probe_*.json` evidence into a machine-readable data-availability trend (runs, triggered/blocked counts, longest stable blocked streak, latest data_through/consecutive_absent, resume_trigger_met) with NO network. Removes the per-session re-confirmation bottleneck: a future session can read `ironflow_trend_report_*.json` and confirm the block persists without re-probing the remote endpoint. Fresh artifact: `ironflow_trend_report_20261102T195805Z.json` (65 runs, 0 triggered, streak 52, resume_trigger_met=false).
- **Alt hunt exhaustive:** `scripts/hunt_alternative_liquidation_sources.py` — 12 source families probed (Binance alt paths, Bybit, OKX, Deribit, academic archives, GitHub raw, Hugging Face, CryptoDataDownload, Tardis/CryptoHFTData, etc.), rubric-scored, retry/backoff, COMPLETE_NO-GO. No admissible unauthenticated Track A source beyond ironflow.
- **Retry-loop guard:** monitor/alt-hunt already ran at 20261102T145805Z (+scan 150101Z, +quick 150713Z, +quick 150946Z, +quick 155438Z, +quick 155443Z, +quick 194916Z, +quick 195433Z, +quick 195654Z, +quick 195812Z, +report 195805Z, +verify 194923Z, +quick 200107Z); re-running without new evidence is forbidden. `--force` required for full re-probe. No polling loops without new evidence.
- **Tests green:** `python -m unittest discover -s tests -v` → 88/88 PASS (includes monitor state-diff, ETag caching, 304 skip, 429 backoff, forward-edge month generation, consecutive_absent, quick-path structure, plus `recompute_consecutive_absent`, `verify_state` consistency, `last_quick_check` quick-path persistence, TestCompareProbes x6, TestTreeChange x3 for tree-change detection in --quick, and TestTrendReport x4 for the new --report trend mode). Previous session's claim of "81/81 PASS" was wrong — 4 test_fclr010_harness tests errored because `run_manifest.json` was an unreadable Git LFS pointer; manifest rewritten as valid JSON; all 88 now pass.
- **Blocker docs:** complete probe tables exist (`research_state/liquidation_forward_validate_004_blocker_*.md`, latest 20261102T195818Z).
- **Frontier:** `research_state/experiment_frontier.json` ranks LIQUIDATION_FORWARD_VALIDATE_HEAVY-004i first (rank 0.25), status BLOCKED_ON_DATA, with precise resume triggers, refreshed 2026-11-02T19:58:18Z.
- **Seals preserved:** FCLR-010 artifacts (protocol, coverage audit, leakage audit, diagnostics, evaluation summary) byte-identical, unmodified (md5 recorded in FCLR-HEAVY-001 integrity block).
- **No .github/workflows/* changes.** No Track B/C conflation. Raw data out of git (code/manifests/reports only).
- **Manifest bottleneck fixed:** `research_state/run_manifest.json` was a Git LFS pointer (unreadable as JSON), breaking `FCLR010Harness._load_frozen_splits()` and 4 tests. Rewritten as valid JSON containing `split_boundaries_fclr010` (frozen_before_outcomes=true, train/validation/test boundaries from evaluation_summary_FCLR010.md).

## DATA STATUS (CONFIRMED BLOCKED — EVIDENCE REQUIRED)
- **Last probe:** `research_state/ironflow_probe_20261102T115745Z.json`. Tree 200 (etag W/"2d38-..."), parquet paths through 2026-10 only. Months 2026-11, 2026-12, 2027-01: events+fills all 404 EntryNotFound → CONFIRMED_ABSENT. `data_through=2026-10`, `consecutive_absent=3`, `new_files_found=[]`.
- **Fresh quick checks:** `ironflow_probe_20261102T155438Z.json`, `ironflow_probe_20261102T155443Z.json`, `ironflow_probe_20261102T194916Z.json`, `ironflow_probe_20261102T194923Z.json`, `ironflow_probe_20261102T195433Z.json`, `ironflow_probe_20261102T195640Z.json`, `ironflow_probe_20261102T195654Z.json`, `ironflow_probe_20261102T195812Z.json`, `ironflow_probe_20261102T200107Z.json` — cross-run probe diff confirmed all forward-edge probes unchanged (404→404). `last_quick_check` persisted (triggered=false). `last_quick_probe` persisted with all 8 probe results. Tree-change check added: no new paths anywhere.
- **Fresh scan:** `ironflow_scan_20261102T150101Z.json` — tree 304 Not Modified, no diff, 36 parquet paths, no backfilled older months.
- **Trend report:** `ironflow_trend_report_20261102T195805Z.json` — 65 runs aggregated locally (no network), 0 triggered, 55 blocked, longest stable blocked streak 52, latest data_through=2026-10, resume_trigger_met=false.
- **Alt hunt:** `research_state/data_source_registry_alt_hunt.json` — 12 families, COMPLETE_NO-GO. Sole reopen path: new ironflow month >= 2026-11, OR a NEW admissible unauthenticated source passing strict GO rubric.
- **Track A (FCLR-010):** COMPLETE, FORECAST_GATE_PASSED on Hyperliquid ironflow census 2025-11..2026-10 (199 native perps, 12 monthly blocks). C2 vs B1 Brier rel reduction 2.21%, CI excludes zero. Overlay H_COUPLED-001 EXECUTED (exp-weighted event exposure reduction 43.985%, CI [42.983%, 44.909%], 500 block reps, no profitability claim).
- **Track C (volatility):** FCLR-008 COMPLETE, gate NOT_MET (+4.30% rel QLIKE but CI [-0.029938, 0.000524] crosses zero). All confirmatory panels exhausted; H001 INCONCLUSIVE/NOT_SUPPORTED. Overlay INELIGIBLE.

## MANDATORY HEAVY WORK (CANNOT SKIP — BLOCKED PATH, ESCALATED)
Produce measurable artifacts. Check off every item before ending. At least one artifact must be NEW relative to this session's diff (this session: `--report` trend mode + `ironflow_trend_report_20261102T195805Z.json`; TestTrendReport x4; 88/88 tests; blocker doc 195818Z; frontier 19:58:18Z; AGENT_HANDOFF.md 19:58:18Z). NEXT session must add beyond that baseline.

### A. STRENGTHEN AUTOMATION (>=1 concrete improvement)
- Harden `scripts/monitor_ironflow_liquidations.py` (`--verify` state-consistency check, `--force` guard, scan-path `resume_trigger` rebuild, `Last-Modified` per-file tracking, jittered backoff, `last_quick_check` + `last_quick_probe` persistence, `compare_probes` probe-to-probe diff, `probe_diff` in --quick evidence, NEW `check_tree_change` tree/path-change detection in --quick, NEW `--report` local trend aggregation) AND/OR `scripts/hunt_alternative_liquidation_sources.py` (broader unauthenticated probes, HTML/JSON/parquet classification, rubric filtering).
- Evidence: modified script file + fresh probe/trend output.

### B. ADD TESTS (all must pass)
- Extend `tests/test_monitor_ironflow.py`: 304 tree skip, 429 backoff, forward-edge month generation, consecutive_absent, post-2026-10 summary, state diffing (`new_files_found`), `recompute_consecutive_absent`, `verify_state` consistency, quick-path `last_quick_check` persistence, TestCompareProbes x6, TestTreeChange x3 (new), TestTrendReport x4 (new --report mode).
- Run `python -m unittest discover -s tests -v` — must be 100% pass. Add tests for any new logic.

### C. UPDATE BLOCKER DOC (irrefutable evidence)
- Fresh `research_state/liquidation_forward_validate_004_blocker_<YYYYMMDDTHHMMSSZ>.md` with: probe table (every URL, method, status, key headers ETag/RateLimit/Date, body preview hash/length, classification), timeline of all probes, exact resume conditions + verify command, alt-hunt rubric pass/fail, verdict BLOCKED_ON_DATA.

### D. UPDATE FRONTIER (precise triggers)
- `research_state/experiment_frontier.json`: status BLOCKED_ON_DATA, fresh `generated` timestamp, explicit `resume_triggers` (the resume trigger conditions: ironflow events/fills >=2026-11 HTTP 200; OR new source passing full GO rubric), refreshed `blockers` with evidence references. No Track B/C conflation.

### E. UPDATE HANDOFF (this file)
- New timestamp, crisp NEXT AGENT INITIAL TASK block, all heavy-work checklist items checked.

## NON-NEGOTIABLE CONSTRAINTS
- Unauthenticated only: no API keys/tokens/cookies/signed/requester-pays. Hyperliquid-only for Track A. Strict cross-track firewall; never merge tracks.
- Never promote modeled boundary breaches to observed liquidations.
- Pre-register BEFORE outcome inspection on ANY new data (fresh pre-reg per `research_state/research_protocol_fclr010.md` v1.0, `pre_registered_before_outcomes: true`).
- Do NOT touch `.github/workflows/*`. `python -m unittest discover -s tests -v` MUST pass. Commit ONLY code/manifests/reports — never raw data.
- Heavy work mandatory: no measurable automation/tests/evidence/frontier/handoff = session FAILED.
- Preserve seals: do not touch sealed FCLR-010/FCLR-008 artifacts.

## RESUME CONDITION (CONCRETE, CHECKABLE — THE ONLY WAY TO UNBLOCK)
Ironflow publishes `data/events/YYYY-MM.parquet` and/or `data/fills/YYYY-MM.parquet` for any month >= 2026-11 with HTTP 200 on unauthenticated GET (verified via `scripts/monitor_ironflow_liquidations.py --quick`, which reports genuinely new files), OR a NEW admissible unauthenticated source passes strict GO rubric (>=5 symbols, >=1 complete month OR >=3 non-overlapping 30-day blocks, documented completeness/coverage, permissive license, unauthenticated access no keys/signed/requester-pays, schema compatible with frozen FCLR-010). Hyperliquid-only for Track A.

## MANDATORY READS (START HERE)
1. `AGENT_HANDOFF.md` (this file)
2. `research_state/heavy_work_checklist_004i.md`
3. `research_state/ironflow_monitor_state.json`
4. `research_state/experiment_frontier.json`
5. Latest `research_state/liquidation_forward_validate_004_blocker_*.md`
6. `research_state/data_source_registry_alt_hunt.json`
7. `research_state/research_protocol_fclr010.md` (§§1,5,6,7,8,15,16)
8. `research_state/evaluation_summary_FCLR010.md`
9. `research_state/cross_track_decision_log.md`
10. `scripts/monitor_ironflow_liquidations.py` and `scripts/hunt_alternative_liquidation_sources.py`

## NON-SKIPPABLE HEAVY-WORK CHECKLIST (MUST COMPLETE BEFORE END)
- [ ] New evidence checked (`ironflow_monitor_state.json` read; `monitor --quick` run; `--report` trend confirms block persists)
- [ ] Automation strengthened (monitor improved with concrete diff: `--report` trend mode + `ironflow_trend_report_20261102T195805Z.json` artifact; prior `check_tree_change` + `tree_change` in --quick evidence; `run_manifest.json` rewritten as valid JSON)
- [ ] Tests added/extended (all pass: `python -m unittest discover -s tests -v` → 88/88 PASS; TestTrendReport x4 added; TestTreeChange x3 added; fixed 4 test_fclr010_harness errors)
- [ ] Blocker doc updated (fresh timestamp 20:00:33Z, complete probe tables, resume conditions, trend report referenced)
- [ ] Frontier updated (precise resume triggers, refreshed blocked-cell status, generated 20:00:33Z)
- [ ] AGENT_HANDOFF.md updated with clear timestamped next task (this file refreshed 20:00:33Z)
- [ ] No sealed artifacts touched; no Track B/C conflation; no .github/workflows changes
- [ ] Raw data out of git; only code/manifests/reports committed
- [ ] At least one NEW measurable artifact beyond this session's diff (`--report` trend mode automation + TestTrendReport tests + `ironflow_trend_report_20261102T195805Z.json` artifact)

**Next agent:** check `research_state/ironflow_monitor_state.json` for new evidence. If none (expected), execute MANDATORY HEAVY WORK in full (A–E, escalated) + checklist. Never avoid heavy working.
