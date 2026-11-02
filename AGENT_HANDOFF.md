# AGENT_HANDOFF.md (SINGLE DURABLE SOURCE OF TRUTH)

**TIMESTAMP:** 2026-11-02T13:56:06Z
**REPO:** Funding-conditioned-volatility-and-liquidation-risk (Track A liquidation risk PRIORITIZED)
**CAMPAIGN:** LIQUIDATION_FORWARD_VALIDATE_HEAVY-004i (CONTINUATION - FORCE HEAVY WORK)
**SESSION GOAL FOR NEXT AGENT:** Execute with ZERO coasting. Data is blocked (ironflow through 2026-10 only). Your first action is to eliminate bottlenecks in detection/automation, harden tests, and produce irrefutable evidence. If ANY post-2026-10 ironflow data appears at any point, you MUST pre-register BEFORE inspecting outcomes and run the frozen FCLR-010 harness immediately.

## BOTTLENECKS REMOVED (THIS SESSION)
- **ETag caching hardened:** `scripts/monitor_ironflow_liquidations.py` uses If-None-Match on tree listing and skips re-parsing on 304; reads RateLimit headers and backs off when budget low.
- **Wider probe window:** lookback+lookahead expanded (forward edge explicitly probed for 2026-11+).
- **Failure classification:** every probe tagged (NEW_AVAILABLE/CONFIRMED_ABSENT/304/429/TRANSIENT_ERROR) with headers/body previews.
- **State machine:** `research_state/ironflow_monitor_state.json` tracks `data_through`, `consecutive_absent`, `post_2026_10_summary`, and `new_files_found`.
- **Heavy-work enforced:** `research_state/heavy_work_checklist_004i.md` is non-skippable; this handoff requires all items checked before ending.
- **Tests extended:** Monitor tests hardened (64/64 PASS as of last run).

## DATA STATUS (CONFIRMED BLOCKED — EVIDENCE REQUIRED)
- **Last probe:** `research_state/ironflow_probe_20261102T115745Z.json` (2026-11-02T11:57:45Z). 2026-11+ months return 404 EntryNotFound (confirmed). `data_through=2026-10`, `consecutive_absent>=3`. No resume trigger fired.
- **Alt hunt:** `research_state/data_source_registry_alt_hunt.json` — 12 source families probed, COMPLETE_NO-GO. No admissible unauthenticated Track A sources found.
- **Tests:** `python -m unittest discover -s tests -v` → 64/64 PASS (as of last recorded run).

## IMMEDIATE FIRST ACTION (IN ORDER, NO SKIPPING)
1. **CHECK FOR NEW EVIDENCE (MANDATORY):** Read `research_state/ironflow_monitor_state.json`. Run `python scripts/monitor_ironflow_liquidations.py --quick` (state-aware, cheap). If resume trigger fires (>=2026-11 returns 200 for events OR fills, or `new_files_found` non-empty for >=2026-11) → go to Step 2. Otherwise → go to Step 4.
2. **NEW DATA PATH (if triggered):** CREATE fresh pre-registration BEFORE inspecting outcomes (per `research_state/research_protocol_fclr010.md` v1.0). Freeze splits in `run_manifest.json` if not already frozen. Run frozen `scripts/fclr010_harness.py`. Write `research_state/evaluation_summary_LIQUIDATION_FORWARD_VALIDATE_004_<YYYYMMDDTHHMMSSZ>.md` with calibration, LOO, concentration, block-bootstrap CIs (>=2000 reps), multiplicity, and explicit gate assessment. Update frontier + cross-track log. Commit only code/manifests/reports.
3. **READ LATEST EVIDENCE:** Read latest `research_state/liquidation_forward_validate_004_blocker_*.md`, `research_state/ironflow_monitor_state.json`, `research_state/experiment_frontier.json`, and `research_state/heavy_work_checklist_004i.md`.
4. **BLOCKED PATH (EXPECTED):** EXECUTE MANDATORY HEAVY WORK BELOW IN FULL. No "checked again" loops without measurable changes.

## MANDATORY HEAVY WORK (CANNOT SKIP — BLOCKED PATH)
You MUST produce measurable artifacts. "Nothing to do" is not an option.

### A. STRENGTHEN AUTOMATION (≥1 concrete improvement)
- **Harden `scripts/monitor_ironflow_liquidations.py`:** Add ETag change detection for tree (already present) but also track `Last-Modified` per file, add `--force` guard, emit a machine-readable `resume_trigger` block in evidence JSON, and add jittered exponential backoff with per-endpoint retry budgets. Consider HEAD probes before GET to save bandwidth.
- **Strengthen `scripts/hunt_alternative_liquidation_sources.py`:** Broaden unauthenticated probes (more HF repos, common CDN paths), add response classification (HTML vs JSON vs parquet), detect pagination/range, and write structured probe matrices. Enforce strict GO rubric filtering.
- **Make detection proactive:** Ensure both scripts log exact resume conditions and write evidence atomically.

### B. ADD TESTS (all must pass)
- Extend `tests/test_monitor_ironflow.py` with cases: 304 tree skip, 429 backoff, forward-edge month generation, consecutive_absent calculation, post-2026-10 summary, and state diffing (`new_files_found`).
- If you touch hunt script, add/extend tests for classification and rubric.
- Run `python -m unittest discover -s tests -v` and ensure 100% pass. Add tests for any new logic.

### C. UPDATE BLOCKER DOC (irrefutable evidence)
Create fresh `research_state/liquidation_forward_validate_004_blocker_<YYYYMMDDTHHMMSSZ>.md` containing:
- **Probe table:** Every URL tried (tree + events/fills for 2026-11,2026-12,2027-01,2027-02 and any new candidates), method, status, key headers (ETag/RateLimit/Date), body preview hash/length, classification.
- **Timeline:** Timestamps of all probes in this session + prior.
- **Resume conditions:** Exact checkable strings/paths/months and the exact command to verify (`python scripts/monitor_ironflow_liquidations.py --quick`).
- **Alt-hunt summary:** Results of any new probes with rubric pass/fail per source.
- **Verdict:** BLOCKED_ON_DATA with zero admissible unauthenticated sources found.

### D. UPDATE FRONTIER (precise triggers)
Update `research_state/experiment_frontier.json` for campaign `LIQUIDATION_FORWARD_VALIDATE_HEAVY-004i`:
- Set `status` to `BLOCKED_ON_DATA` with fresh `generated` timestamp.
- Write explicit `resume_triggers` (ironflow events/fills >=2026-11 returning 200, OR new source passing full GO rubric).
- Refresh `blockers` with evidence references.
- Ensure no Track B/C conflation.

### E. UPDATE HANDOFF (this file)
Update this `AGENT_HANDOFF.md` with a new timestamp and a crisp "NEXT AGENT INITIAL TASK" block (see below). Check off all items in the heavy-work checklist.

## NON-NEGOTIABLE CONSTRAINTS
- **Unauthenticated only.** No API keys/tokens/cookies/signed/requester-pays.
- **Hyperliquid-only for Track A.** Strict cross-track firewall. Never merge tracks.
- **No label promotion:** Never promote modeled boundary breaches to observed liquidations.
- **Pre-register BEFORE outcome inspection:** On ANY new data, fresh pre-reg before looking at outcomes.
- **No workflow changes:** Do NOT touch `.github/workflows/*`.
- **Tests required:** `python -m unittest discover -s tests -v` MUST pass. Add tests if modifying modules.
- **Raw data out of git:** Commit ONLY code/manifests/reports.
- **Evidence over polling:** No retry loops without new evidence. Automation + tests + evidence required.
- **Heavy work mandatory:** If nothing measurable done (automation/tests/evidence/frontier/handoff), session FAILED.
- **Preserve seals:** Do not touch sealed artifacts as documented.

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

## NEXT AGENT INITIAL TASK (CLEAR, TIMESTAMPED)
**START NOW (2026-11-02T13:54:12Z):** Check evidence via `scripts/monitor_ironflow_liquidations.py --quick`. If none (expected per latest probe), execute A-E above with full rigor. Your deliverables at session end: (1) improved monitor/hunt automation, (2) new/extended tests all passing, (3) fresh blocker doc with complete probe tables, (4) updated frontier with precise resume triggers, (5) updated AGENT_HANDOFF.md with new timestamp and checked heavy-work list, (6) summary of measurable changes. Do not end until all checked. If new data appears, drop everything and run the new-data path.

**RESUME CONDITION (CONCRETE):** Ironflow publishes `data/events/YYYY-MM.parquet` and/or `data/fills/YYYY-MM.parquet` for any month >= 2026-11 with HTTP 200 on unauthenticated GET (verified via `scripts/monitor_ironflow_liquidations.py --quick`), OR a NEW admissible unauthenticated source passes strict GO rubric (>=5 symbols, >=1 complete month OR >=3 non-overlapping 30-day blocks, documented completeness/coverage, permissive license, unauthenticated only, schema compatible with frozen FCLR-010). Hyperliquid-only for Track A.

**HEAVY-WORK CHECKLIST (MUST COMPLETE BEFORE END)**
- [ ] New evidence checked (ironflow_monitor_state.json read; monitor --quick run)
- [ ] Automation strengthened (monitor and/or hunt script improved with concrete diff)
- [ ] Tests added/extended (all pass: `python -m unittest discover -s tests -v`)
- [ ] Blocker doc updated (fresh timestamp, complete probe tables, resume conditions)
- [ ] Frontier updated (precise resume triggers, refreshed blocked-cell status)
- [ ] AGENT_HANDOFF.md updated with clear timestamped next task (this file refreshed)
- [ ] No sealed artifacts touched; no Track B/C conflation; no .github/workflows changes
- [ ] Raw data out of git; only code/manifests/reports committed
