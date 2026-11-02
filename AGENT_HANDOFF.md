# AGENT_HANDOFF.md (SINGLE DURABLE SOURCE OF TRUTH)

**TIMESTAMP:** 2026-11-02T13:48:13Z
**REPO:** Funding-conditioned-volatility-and-liquidation-risk (Track A liquidation risk PRIORITIZED)
**SESSION GOAL FOR NEXT AGENT:** Execute campaign LIQUIDATION_FORWARD_VALIDATE_HEAVY-004i. All confirmatory gates resolved at stable closeout. The ONLY open path is new post-2026-10 ironflow Hyperliquid liquidation data. If it appears: pre-register BEFORE outcome inspection, run frozen FCLR-010 harness, write evaluation summary + gate assessment. If still absent (expected): STRENGTHEN AUTOMATION + TESTS + BLOCKER EVIDENCE — heavy work mandatory, no coasting. Never avoid heavy working.

## DATA STATUS (CONFIRMED BLOCKED — DO NOT RE-PROBE WITHOUT NEW EVIDENCE)
- Last probe: `research_state/ironflow_monitor_state.json` (quick-checked via `scripts/monitor_ironflow_liquidations.py --quick` at 2026-11-02T13:48:13Z). Probed 2026-11,2026-12,2027-01,2027-02 — all 404 EntryNotFound for events+fills. `data_through=2026-10`, `consecutive_absent=3`. post-2026-10 available: none. No resume trigger fired.
- Alt-hunt: `research_state/data_source_registry_alt_hunt.json` — 12 source families probed, COMPLETE_NO-GO. No new admissible unauthenticated Track A sources.
- Tests: `python -m unittest discover -s tests -v` → 64/64 PASS (monitor tests extended).

## CURRENT STATE (STABLE CLOSEOUT)
- All confirmatory gates resolved. Track A FCLR-010 PASSED; overlay EXECUTED. Track B/C closed as documented.
- OPEN ITEM: LIQUIDATION_FORWARD_VALIDATE_HEAVY-004i BLOCKED_ON_DATA — ironflow through 2026-10 only. No engineering action can force this data to exist.

## IMMEDIATE FIRST ACTION (IN ORDER)
1. **CHECK FOR NEW EVIDENCE ONLY**: read `research_state/ironflow_monitor_state.json`. Run `python scripts/monitor_ironflow_liquidations.py --quick` (cheap, state-aware). If resume trigger fires (>=2026-11 200), proceed to Step 2. Else skip to Step 4.
2. **NEW DATA PATH (if >=2026-11 data appeared):** CREATE fresh pre-registration BEFORE inspecting outcomes. Run frozen FCLR-010 harness immediately. Write evaluation summary + gate assessment. Update frontier.
3. **READ LATEST EVIDENCE:** latest blocker doc in `research_state/` matching `liquidation_forward_validate_004_blocker_*.md`, `ironflow_monitor_state.json`, `experiment_frontier.json`.
4. **BLOCKED PATH (no new data — EXPECTED):** Execute MANDATORY HEAVY WORK below in full.

## MANDATORY HEAVY WORK (CANNOT SKIP — BLOCKED PATH)
- **STRENGTHEN AUTOMATION:** improve `scripts/monitor_ironflow_liquidations.py` and/or `scripts/hunt_alternative_liquidation_sources.py` (ETag caching, forward-edge probing, backoff, classification, broader probes).
- **ADD TESTS:** extend `tests/test_monitor_ironflow.py` or add new tests. All must pass: `python -m unittest discover -s tests -v`.
- **UPDATE BLOCKER DOC:** write fresh `research_state/liquidation_forward_validate_004_blocker_<new_timestamp>.md` with complete probe tables, headers/body previews, resume conditions.
- **UPDATE FRONTIER:** update `research_state/experiment_frontier.json` with precise resume triggers and blocked-cell status.
- **BUILD NEXT CAMPAIGN:** ensure heavy-work checklist remains non-skippable; add hooks/templates if gaps found.

## RESUME CONDITION (CONCRETE, CHECKABLE)
Ironflow publishes `data/events/YYYY-MM.parquet` and/or `data/fills/YYYY-MM.parquet` for any month >= 2026-11 with HTTP 200 on unauthenticated GET (verified via `scripts/monitor_ironflow_liquidations.py --quick`), OR a NEW admissible unauthenticated source passes strict GO rubric (>=5 symbols, >=1 complete month OR >=3 non-overlapping 30-day blocks, documented completeness/coverage, permissive license, unauthenticated only, schema compatible with frozen FCLR-010). Hyperliquid-only for Track A.

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
- Preserve sealed artifacts as documented.

## MANDATORY READS
AGENT_HANDOFF.md, RESEARCH_PROMPT.md (§§1,5,6,7,8,15,16), research_state/research_protocol_fclr010.md, research_state/evaluation_summary_FCLR010.md, research_state/cross_track_decision_log.md, research_state/experiment_frontier.json, latest `research_state/liquidation_forward_validate_004_blocker_*.md`, research_state/ironflow_monitor_state.json, research_state/data_source_registry_alt_hunt.json, research_state/heavy_work_checklist_004i.md

## NON-SKIPPABLE HEAVY-WORK CHECKLIST (must complete before any session ends)
- [ ] New evidence checked (`research_state/ironflow_monitor_state.json` read; `scripts/monitor_ironflow_liquidations.py --quick` run)
- [ ] Automation strengthened (monitor and/or hunt script improved)
- [ ] Tests added/extended (all pass: `python -m unittest discover -s tests -v`)
- [ ] Blocker doc updated (fresh timestamp, complete probe tables, resume conditions)
- [ ] Frontier updated (precise resume triggers, refreshed blocked-cell status)
- [ ] AGENT_HANDOFF.md updated with clear timestamped next task
- [ ] No sealed artifacts touched; no Track B/C conflation; no .github/workflows changes
- [ ] Raw data out of git; only code/manifests/reports committed

**NEXT AGENT:** Check state via `--quick`. If none (expected), do MANDATORY HEAVY WORK in full — automation, tests, blocker doc, frontier, next campaign. Never avoid heavy working.
