# AGENT_HANDOFF.md (SINGLE DURABLE SOURCE OF TRUTH)

**TIMESTAMP:** 2026-11-02T11:53:15Z
**REPO:** Funding-conditioned-volatility-and-liquidation-risk (Track A liquidation risk PRIORITIZED)
**SESSION GOAL FOR NEXT AGENT:** Execute the heavy liquidation-forward campaign until new post-2026-10 data exists OR produce irrefutable blocker evidence with strengthened automation. Do NOT coast. Heavy work mandatory.

## IMMEDIATE FIRST ACTION (DO THIS FIRST, IN ORDER)
1. **RUN MONITOR**: `python scripts/monitor_ironflow_liquidations.py` - state-aware, wider window, failure classification. Read output.
2. **RUN ALT-HUNT**: `python scripts/hunt_alternative_liquidation_sources.py` - Hyperliquid-only admissible for Track A. Confirm no other unauthenticated sources.
3. **READ LATEST EVIDENCE**: `research_state/liquidation_forward_validate_004_blocker_20261102T104628Z.md`, `research_state/ironflow_monitor_state.json`, `research_state/experiment_frontier.json`

## CURRENT BLOCKER (AUTHORITATIVE)
- **Campaign:** LIQUIDATION_FORWARD_VALIDATE_HEAVY-004i (harmonized across all artifacts)
- **State:** BLOCKED_ON_DATA - ironflow/hyperliquid-liquidations
- **Latest monitor:** 20261102T114517Z shows 2026-10 present (events/fills both exist), 2026-11 events/fills HTTP 404. data_through=2026-10, consecutive_absent=3.
- **Alt-hunt:** Confirms no other admissible unauthenticated sources exist. Hyperliquid-only strictly enforced.
- **Track A status:** FCLR-010 PASSED (C2 vs B1 Brier -2.21%, CI excludes zero). Overlay is hypothetical only.

## MANDATORY HEAVY WORK (CANNOT SKIP)
**IF NEW DATA APPEARS (events/fills 200 for >=2026-11):**
- CREATE fresh pre-registration BEFORE inspecting outcomes (`scripts/create_forward_prereg.py` or manual per protocol). Follow `research_state/research_protocol_fclr010.md`.
- Run frozen FCLR-010 harness immediately. Write `research_state/evaluation_summary_LIQUIDATION_FORWARD_VALIDATE_004_<YYYYMMDDTHHMMSSZ>.md` with calibration, LOO, concentration, block-bootstrap CIs, multiplicity, gate assessment.
- Update `research_state/experiment_frontier.json` and commit evidence.

**IF STILL BLOCKED (no new rubric-passing data):**
- STRENGTHEN AUTOMATION: Improve `scripts/monitor_ironflow_liquidations.py`, `scripts/hunt_alternative_liquidation_sources.py`, or add detection logic. Make it faster/smarter/more exhaustive.
- ADD TESTS: Extend `tests/test_monitor_ironflow.py` or add new tests. All must pass.
- UPDATE BLOCKER DOC: `research_state/liquidation_forward_validate_004_blocker_<timestamp>.md` with complete probe tables (all URLs tried, status codes, headers, body previews), explicit checkable resume conditions (exact paths/patterns/URLs/months to watch), concrete timestamps.
- UPDATE FRONTIER: `research_state/experiment_frontier.json` with precise resume triggers.
- BUILD NEXT CAMPAIGN: Make future agents unable to avoid heavy work - add automation hooks, pre-reg templates, validation steps.

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
AGENT_HANDOFF.md, RESEARCH_PROMPT.md (§§1,5,6,7,8,15,16), research_state/research_protocol_fclr010.md, research_state/evaluation_summary_FCLR010.md, research_state/cross_track_decision_log.md, research_state/experiment_frontier.json, research_state/liquidation_forward_validate_004_blocker_20261102T104628Z.md, research_state/ironflow_probe_20261102T114517Z.json, research_state/ironflow_monitor_state.json, research_state/data_source_registry_alt_hunt.json

## BOTTLENECKS ALREADY REMOVED
- Monitor hardened (state-aware diff, wider window, failure classification, data_through/consecutive_absent tracking). Tests added. 42/42 passing.
- Campaign harmonized to 004i across all artifacts.
- Alt-hunt confirms no other admissible sources.
- Complete blocker evidence exists. Automation strengthened.

**NEXT AGENT:** Start with monitor+alt-hunt NOW. If blocked, produce stronger automation + irrefutable evidence. Never avoid heavy working.
