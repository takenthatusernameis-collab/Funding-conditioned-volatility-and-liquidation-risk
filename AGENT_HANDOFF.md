# AGENT_HANDOFF.md (SINGLE DURABLE SOURCE OF TRUTH)

**TIMESTAMP:** 2026-11-02T15:51:49Z
**REPO:** Funding-conditioned-volatility-and-liquidation-risk — Track A liquidation risk PRIORITIZED (repo-name-driven prioritization: observed-liquidation forecast validation before any volatility overlay).
**CAMPAIGN:** LIQUIDATION_FORWARD_VALIDATE_HEAVY-004i — BLOCKED_ON_DATA
**SESSION GOAL FOR NEXT AGENT:** Execute with ZERO coasting. Data blocked (ironflow through 2026-10; 2026-11/12/2027-01/2027-02 CONFIRMED_ABSENT). First action: state-aware resume check (`python scripts/monitor_ironflow_liquidations.py --quick` + `--verify`). If ANY post-2026-10 ironflow data appears OR new admissible Track A source found, PRE-REGISTER BEFORE inspecting outcomes and run frozen `scripts/fclr010_harness.py`. Otherwise MANDATORY HEAVY WORK A–E in full — no measurable artifact beyond previous diff = session FAILED. Fresh blocker/frontier/handoff written at 2026-11-02T15:51:49Z.

## NEXT AGENT INITIAL TASK (CLEAR, TIMESTAMPED — START NOW)
**2026-11-02T15:49:13Z:** Run `python scripts/monitor_ironflow_liquidations.py --quick` (state-aware, cheap, forward-edge only). Read `research_state/ironflow_monitor_state.json` (and confirm `python scripts/monitor_ironflow_liquidations.py --verify` reports ok=True).
- If `new_files_found` is non-empty for any month >= 2026-11, OR any month >= 2026-11 returns HTTP 200 for events OR fills → NEW DATA PATH (Step 2 below). Create fresh pre-registration BEFORE inspecting outcomes, then run `scripts/fclr010_harness.py` and write `research_state/evaluation_summary_LIQUIDATION_FORWARD_VALIDATE_004_<YYYYMMDDTHHMMSSZ>.md` (calibration, LOO, concentration, block-bootstrap CIs >=2000 reps, Holm multiplicity, gate assessment). Update frontier + cross-track log.
- Otherwise (expected) → BLOCKED PATH: execute MANDATORY HEAVY WORK A–E below in full, ESCALATED: this session must produce at least ONE new measurable artifact beyond the previous session's diff (previous session: monitor now persists `last_quick_check` on `--quick`; tests 73→75 PASS; blocker doc 15:12:00Z; frontier refreshed). "Nothing to do" is not an option. A session producing no measurable automation, tests, or evidence FAILS.

## BOTTLENOCKS REMOVED (EVIDENCE-BASED, DO NOT RE-INTRODUCE)
- **Monitor hardened:** `scripts/monitor_ironflow_liquidations.py` — If-None-Match tree ETag caching (304 skips full parse), HEAD-before-GET existence probes, per-file ETag/Last-Modified caching, jittered exponential backoff with per-endpoint retry budgets (tree=3, resolve=3, head=1), RateLimit-header awareness (panic at r<=10), forward-edge-only `--quick` resume check, `--verify` state-consistency check (no network), `--force` guard on full candidate-months probe (anti retry-loop), scan path now rebuilds/retains the `resume_trigger` block, `--quick` now persists a machine-readable `last_quick_check` record (anti silent re-probe), `data_through`/`consecutive_absent`/`new_files_found` tracking.
- **Alt hunt exhaustive:** `scripts/hunt_alternative_liquidation_sources.py` — 12 source families probed (Binance alt paths, Bybit, OKX, Deribit, academic archives, GitHub raw, Hugging Face, CryptoDataDownload, Tardis/CryptoHFTData, etc.), rubric-scored, retry/backoff, COMPLETE_NO-GO. No admissible unauthenticated Track A source beyond ironflow.
- **Retry-loop guard:** monitor/alt-hunt already ran at 20261102T145805Z (+scan 150101Z, +quick 150713Z, +quick 150946Z); re-running without new evidence is forbidden. `--force` required for full re-probe. No polling loops without new evidence.
- **Tests green:** `python -m unittest discover -s tests -v` → 75/75 PASS (includes monitor state-diff, ETag caching, 304 skip, 429 backoff, forward-edge month generation, consecutive_absent, quick-path structure, plus `recompute_consecutive_absent`, `verify_state` consistency, and `last_quick_check` quick-path persistence).
- **Blocker docs:** complete probe tables exist (`research_state/liquidation_forward_validate_004_blocker_*.md`, latest 20261102T151200Z).
- **Frontier:** `research_state/experiment_frontier.json` ranks LIQUIDATION_FORWARD_VALIDATE_HEAVY-004i first (rank 0.25), status BLOCKED_ON_DATA, with precise resume triggers, refreshed 2026-11-02T15:12:00Z.
- **Seals preserved:** FCLR-010 artifacts (protocol, coverage audit, leakage audit, diagnostics, evaluation summary) byte-identical, unmodified (md5 recorded in FCLR-HEAVY-001 integrity block).
- **No .github/workflows/* changes.** No Track B/C conflation. Raw data out of git (code/manifests/reports only).

## DATA STATUS (CONFIRMED BLOCKED — EVIDENCE REQUIRED)
- **Last probe:** `research_state/ironflow_probe_20261102T115745Z.json`. Tree 200 (etag W/"2d38-..."), parquet paths through 2026-10 only. Months 2026-11, 2026-12, 2027-01: events+fills all 404 EntryNotFound → CONFIRMED_ABSENT. `data_through=2026-10`, `consecutive_absent=3`, `new_files_found=[]`.
- **Fresh quick checks:** `ironflow_probe_20261102T150713Z.json` and `ironflow_probe_20261102T150946Z.json` — 8 HEAD probes each (2026-11/12/2027-01/2027-02 events+fills), all 404, no resume trigger, `head_probes=8`, `cached_hits=0`. `last_quick_check` persisted (triggered=false, ts 2026-11-02T15:09:46Z).
- **Fresh scan:** `ironflow_scan_20261102T150101Z.json` — tree 304 Not Modified, no diff, 36 parquet paths, no backfilled older months.
- **Alt hunt:** `research_state/data_source_registry_alt_hunt.json` — 12 families, COMPLETE_NO-GO. Sole reopen path: new ironflow month >= 2026-11, OR a NEW admissible unauthenticated source passing strict GO rubric.
- **Track A (FCLR-010):** COMPLETE, FORECAST_GATE_PASSED on Hyperliquid ironflow census 2025-11..2026-10 (199 native perps, 12 monthly blocks). C2 vs B1 Brier rel reduction 2.21%, CI excludes zero. Overlay H_COUPLED-001 EXECUTED (exp-weighted event exposure reduction 43.985%, CI [42.983%, 44.909%], 500 block reps, no profitability claim).
- **Track C (volatility):** FCLR-008 COMPLETE, gate NOT_MET (+4.30% rel QLIKE but CI [-0.029938, 0.000524] crosses zero). All confirmatory panels exhausted; H001 INCONCLUSIVE/NOT_SUPPORTED. Overlay INELIGIBLE.

## MANDATORY HEAVY WORK (CANNOT SKIP — BLOCKED PATH, ESCALATED)
Produce measurable artifacts. Check off every item before ending. At least one artifact must be NEW relative to this session's diff (monitor `last_quick_check` persistence + 2 tests already delivered; next session adds its own).

### A. STRENGTHEN AUTOMATION (>=1 concrete improvement)
- Harden `scripts/monitor_ironflow_liquidations.py` (`--verify` state-consistency check, `--force` guard, scan-path `resume_trigger` rebuild, `Last-Modified` per-file tracking, jittered backoff, `last_quick_check` persistence) AND/OR `scripts/hunt_alternative_liquidation_sources.py` (broader unauthenticated probes, HTML/JSON/parquet classification, rubric filtering).
- Evidence: modified script file + fresh probe output.

### B. ADD TESTS (all must pass)
- Extend `tests/test_monitor_ironflow.py`: 304 tree skip, 429 backoff, forward-edge month generation, consecutive_absent, post-2026-10 summary, state diffing (`new_files_found`), `recompute_consecutive_absent`, `verify_state` consistency, quick-path `last_quick_check` persistence.
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
Ironflow publishes `data/events/YYYY-MM.parquet` and/or `data/fills/YYYY-MM.parquet` for any month >= 2026-11 with HTTP 200 on unauthenticated GET (verified via `scripts/monitor_ironflow_liquidations.py --quick`, which reports genuinely new files), OR a NEW admissible unauthenticated source passes strict GO rubric (>=5 symbols, >=1 complete month OR >=3 non-overlapping 30-day blocks, documented completeness/coverage, permissive license, unauthenticated only, schema compatible with frozen FCLR-010). Hyperliquid-only for Track A.

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
- [ ] New evidence checked (`ironflow_monitor_state.json` read; `monitor --quick` run)
- [ ] Automation strengthened (monitor and/or hunt script improved with concrete diff)
- [ ] Tests added/extended (all pass: `python -m unittest discover -s tests -v`)
- [ ] Blocker doc updated (fresh timestamp, complete probe tables, resume conditions)
- [ ] Frontier updated (precise resume triggers, refreshed blocked-cell status)
- [ ] AGENT_HANDOFF.md updated with clear timestamped next task (this file refreshed)
- [ ] No sealed artifacts touched; no Track B/C conflation; no .github/workflows changes
- [ ] Raw data out of git; only code/manifests/reports committed
- [ ] At least one NEW measurable artifact beyond this session's diff (new test or new automation)

**Next agent:** check `research_state/ironflow_monitor_state.json` for new evidence. If none (expected), execute MANDATORY HEAVY WORK in full (A–E, escalated) + checklist. Never avoid heavy working.
