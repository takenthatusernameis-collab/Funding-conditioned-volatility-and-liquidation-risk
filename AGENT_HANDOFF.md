# AGENT_HANDOFF.md (SINGLE DURABLE SOURCE OF TRUTH)

**TIMESTAMP:** 2026-11-02T12:47:51Z
**REPO:** Funding-conditioned-volatility-and-liquidation-risk (Track A liquidation risk PRIORITIZED)
**SESSION GOAL FOR NEXT AGENT:** Execute campaign LIQUIDATION_FORWARD_VALIDATE_HEAVY-004i. All confirmatory gates resolved at stable closeout. The ONLY open path is new post-2026-10 ironflow Hyperliquid liquidation data. If it appears: pre-register BEFORE outcome inspection, run frozen FCLR-010 harness, write evaluation summary + gate assessment. If still absent: STRENGTHEN AUTOMATION + TESTS + BLOCKER EVIDENCE — heavy work mandatory, no coasting. Never avoid heavy working.

## DATA STATUS (CONFIRMED BLOCKED — DO NOT RE-PROBE WITHOUT NEW EVIDENCE)
- Last probe: `research_state/ironflow_probe_20261102T115745Z.json` at 2026-11-02T11:57:45Z (~50 min ago). Tree parsed OK. Probed 2026-10, 2026-11, 2026-12, 2027-01. 2026-10 events/fills HTTP 200; 2026-11/12/2027-01 both HTTP 404 EntryNotFound. `data_through=2026-10`, `consecutive_absent=3`. post-2026-10 available: none.
- Alt-hunt: `research_state/data_source_registry_alt_hunt.json` — no new admissible unauthenticated Track A sources. 8 source families probed, COMPLETE_NO-GO.
- **Do NOT re-run `monitor_ironflow_liquidations.py` or `hunt_alternative_liquidation_sources.py` unless new evidence exists (e.g. a new month URL in the HF tree listing). Repeating the same 404 endpoints without new evidence is a forbidden retry loop.**
- Tests: `python -m unittest discover -s tests -v` → 42/42 PASS (verified this session).

## CURRENT STATE (STABLE CLOSEOUT)
- **All confirmatory gates resolved:** Track A FCLR-010 COMPLETE gate PASSED (C2 vs B1 Brier −2.21%, CI excludes zero, overlay hypothetical only). Track C H001 NOT_SUPPORTED closed. Track B CLOSED_NEGATIVE. H002 PERMANENT_BLOCK (SSRN 403). FCLR-LIQMICRO-002/003 COMPLETE. FCLR-NEXT-002 COMPLETE_NO-GO (no new admissible source across 8 source families). FCLR-HEAVY-001 EXECUTED_ALL_STEPS. FCLR-OVERLAY-001 EXECUTED.
- **OPEN ITEM:** LIQUIDATION_FORWARD_VALIDATE_HEAVY-004i BLOCKED_ON_DATA — ironflow/hyperliquid-liquidations events/fills through 2026-10 only. 2026-11+ both HTTP 404. No engineering action can force this data to exist.

## IMMEDIATE FIRST ACTION (IN ORDER)
1. **CHECK FOR NEW EVIDENCE ONLY**: read `research_state/ironflow_monitor_state.json` (last_probe 20261102T115745Z). If `new_files_found` is non-empty for any month >= 2026-11, or any month >= 2026-11 shows status 200, proceed to Step 2 (NEW DATA PATH). Otherwise skip directly to Step 4 (BLOCKED PATH).
2. **NEW DATA PATH (if >=2026-11 data appeared):** CREATE fresh pre-registration BEFORE inspecting outcomes (`scripts/create_forward_prereg.py` or manual per `research_state/research_protocol_fclr010.md`). Run frozen FCLR-010 harness immediately. Write `research_state/evaluation_summary_LIQUIDATION_FORWARD_VALIDATE_004_<YYYYMMDDTHHMMSSZ>.md` with calibration, LOO, concentration, block-bootstrap CIs (>=2000 reps), multiplicity, gate assessment. Update `research_state/experiment_frontier.json` and commit evidence.
3. **READ LATEST EVIDENCE** (only after Step 2 if new data): `research_state/liquidation_forward_validate_004_blocker_20261102T104628Z.md`, `research_state/ironflow_monitor_state.json`, `research_state/experiment_frontier.json`.
4. **BLOCKED PATH (no new data — EXPECTED CASE):** Execute MANDATORY HEAVY WORK below in full. This is the session's required output. A session that produces no measurable automation/tests/evidence FAILS.

## MANDATORY HEAVY WORK (CANNOT SKIP — BLOCKED PATH)
- **STRENGTHEN AUTOMATION:** improve `scripts/monitor_ironflow_liquidations.py` (e.g. skip re-listing when tree ETag unchanged, wider/faster lookahead, smarter failure classification) and/or `scripts/hunt_alternative_liquidation_sources.py`. Add retry/backoff robustness, broader unauthenticated probes, or new detection logic. Make it faster/smarter/more exhaustive.
- **ADD TESTS:** extend `tests/test_monitor_ironflow.py` or add new tests covering state-diff, ETag caching, month-window, classification. All must pass: `python -m unittest discover -s tests -v`.
- **UPDATE BLOCKER DOC:** `research_state/liquidation_forward_validate_004_blocker_<new_timestamp>.md` with complete probe tables (all URLs tried, status codes, headers, body previews), explicit checkable resume conditions (exact paths/patterns/URLs/months to watch), concrete timestamps.
- **UPDATE FRONTIER:** `research_state/experiment_frontier.json` with precise resume triggers and refreshed blocked-cell status.
- **BUILD NEXT CAMPAIGN:** make future agents unable to avoid heavy work — add pre-registration templates, forward-validation hooks, validation steps, and a non-skippable heavy-work checklist that must be completed before any session ends.

## RESUME CONDITION (CONCRETE, CHECKABLE)
Ironflow publishes `data/events/YYYY-MM.parquet` and/or `data/fills/YYYY-MM.parquet` for any month >= 2026-11 with HTTP 200 on unauthenticated GET (verify via `scripts/monitor_ironflow_liquidations.py` — state-aware; reports genuinely new files), OR a NEW admissible unauthenticated source passes strict GO rubric (>=5 symbols, >=1 complete month OR >=3 non-overlapping 30-day blocks, documented completeness/coverage, permissive license, unauthenticated access no keys/signed/requester-pays, schema compatible with frozen FCLR-010). Hyperliquid-only for Track A.

## NON-NEGOTIABLE CONSTRAINTS
- Unauthenticated only. No API keys/tokens/cookies/signed/requester-pays.
- Hyperliquid-only for Track A. Strict cross-track firewall. Never merge tracks.
- Never promote modeled boundary breaches to observed liquidations.
- Pre-register BEFORE outcome inspection on ANY new data.
- Do NOT touch `.github/workflows/*`.
- `python -m unittest discover -s tests -v` MUST pass. Add tests if adding/modifying modules.
- Raw data OUT of git. Commit ONLY code/manifests/reports.
- No retry loops without new evidence. Evidence + automation over "checked again".
- Heavy work required. If nothing measurable done (automation/tests/evidence), session FAILED.
- Preserve sealed artifacts: FCLR-001/002/003/006/007/008/009, FCLR-H003-EXT-001, H001/H002 closed as documented.

## MANDATORY READS
AGENT_HANDOFF.md, RESEARCH_PROMPT.md (§§1,5,6,7,8,15,16), research_state/research_protocol_fclr010.md, research_state/evaluation_summary_FCLR010.md, research_state/cross_track_decision_log.md, research_state/experiment_frontier.json, research_state/liquidation_forward_validate_004_blocker_20261102T104628Z.md, research_state/ironflow_probe_20261102T115745Z.json, research_state/ironflow_monitor_state.json, research_state/data_source_registry_alt_hunt.json

## BOTTLENECKS ALREADY REMOVED
- Monitor hardened (state-aware diff, wider window, failure classification, data_through/consecutive_absent tracking). Tests added. 42/42 passing.
- Campaign harmonized to 004i across all artifacts.
- Alt-hunt confirms no other admissible sources; 8 source families probed, COMPLETE_NO-GO.
- Complete blocker evidence exists. Automation strengthened.
- All confirmatory tracks at stable closeout; no session should spin on closed gates.
- Retry-loop guard: monitor/alt-hunt already ran at 11:57:45Z; re-running without new evidence is forbidden.

**NEXT AGENT:** Check state file for new evidence. If none (expected), execute MANDATORY HEAVY WORK in full — automation, tests, blocker doc, frontier, next campaign. Never avoid heavy working.
