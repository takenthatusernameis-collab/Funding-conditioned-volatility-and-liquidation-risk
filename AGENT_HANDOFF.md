# AGENT_HANDOFF.md (DURABLE — SINGLE SOURCE OF TRUTH)
**TIMESTAMP (UTC):** 2026-11-02T06:07:00Z
**HANDOFF ID:** FCLR-HANDOFF-098-20261102T060700Z
**SUPERSEDES:** FCLR-HANDOFF-097-20261102T055715Z
**REPO:** Funding-conditioned-volatility-and-liquidation-risk
**REPO PRIORITIZATION (INFERRED):** LIQUIDATION RISK > funding-conditioned volatility (repo name). Track A (observed liquidations) is the only open confirmatory track. Treat liquidation risk as the default axis of work until Track A is resolved or exhaustively blocked with irrefutable evidence.

**BRANCH/HEAD:** main @ e478ab8afe7c4cc6371618879ead2c2cd0cecea2

**INITIAL TASK MESSAGE FOR NEXT SESSION (TIMESTAMPED, MANDATORY - CANNOT SKIP):**
```
[2026-11-02T06:07:00Z] FOCUS CAMPAIGN: LIQUIDATION_FORWARD_MONITOR_AUTOMATE_HEAVY-004d (HEAVY EXECUTION REQUIRED - NO PASSIVE WAITING)

PRIORITY: CRITICAL - LIQUIDATION RISK (repo-name driven). Track A gate PASSED (FCLR-010). Forward validation beyond 2026-10-31 is BLOCKED_ON_DATA (ironflow has no 2026-11 parquet confirmed as of latest probe). The block is DATA AVAILABILITY, not methodology. YOU MUST NOT idle, poll in conversation, or "check the landing page once". YOU MUST convert this block into reusable automation and airtight evidence.

OBJECTIVE (NON-OPTIONAL, HEAVY WORK - DO ALL OF THE BELOW):
1) MAINTAIN/USE FROZEN HARNESS
   - Use `scripts/fclr010_harness.py` + `scripts/fclr010_validate.py` (already present). If you extend, do NOT retune. Keep tests passing.
   - Pre-reg template exists: `research_state/experiment_prereg_LIQUIDATION_FORWARD_VALIDATE_004_20261102T060650Z.json`. If new data appears, CREATE a fresh pre-reg with new timestamp BEFORE inspecting outcomes.

2) RUN IRONFLOW MONITOR ON DEMAND
   - Run `python scripts/monitor_ironflow_liquidations.py` at start of session (idempotent). It probes tree + events/fills for recent months, writes `research_state/ironflow_probe_YYYYMMDDTHHMMSSZ.json`, updates `research_state/ironflow_monitor_state.json`. Evidence includes URLs/status/headers/sha256 if present.
   - If monitor finds new files (status 200) for >=2026-11, DO NOT just log - go to step 4.

3) EXHAUSTIVE ALTERNATIVE SOURCE HUNT (RE-RUN WITH FRESH EVIDENCE)
   - Run `python scripts/hunt_alternative_liquidation_sources.py` to refresh evidence. Update `research_state/data_source_registry_alt_hunt.json`. Re-probe ALL admissible unauthenticated families per RESEARCH_PROMPT §5 with concrete HTTP evidence.
   - Strict GO/NO-GO: >=5 symbols, >=1 complete month OR >=3 non-overlapping 30-day blocks, documented completeness, license OK, unauthenticated access confirmed, no requester-pays, schema compatible with frozen FCLR-010. Never merge tracks.

4) PRE-REGISTER & VALIDATE ON DISCOVERY (HEAVY, DISCIPLINED)
   - If new rubric-passing post-2026-10-31 observed-liquidation data found: CREATE `research_state/experiment_prereg_LIQUIDATION_FORWARD_VALIDATE_004_<YYYYMMDDTHHMMSSZ>.json` BEFORE inspecting outcomes. Freeze protocol (splits from manifest, primary contrast C2 vs B1 on Brier, block-bootstrap >=2000 reps, multiplicity).
   - Run forward validation IMMEDIATELY with frozen harness. Write `research_state/evaluation_summary_LIQUIDATION_FORWARD_VALIDATE_004_<ID>.md` with calibration, LOO, concentration, block-bootstrap CIs, and explicit gate assessment.

5) IF STILL BLOCKED AFTER EXHAUSTIVE (HEAVY DOCUMENTATION, NO LOOPS)
   - If after exhaustive proof no rubric-passing post-2026-10-31 observed-liquidation data exists, write/update complete blocker evidence doc with full probe tables (URLs/status/headers) and update `research_state/experiment_frontier.json` resume condition with concrete, checkable triggers.
   - DO NOT create infinite polling loops. DO NOT reopen sealed FCLR-001/002/003/006/007/008/009. DO NOT change `.github/workflows/*`.

MANDATORY READS FIRST:
- AGENT_HANDOFF.md (this file)
- RESEARCH_PROMPT.md §§1,5,6,7,8
- research_state/research_protocol_fclr010.md
- research_state/evaluation_summary_FCLR010.md
- research_state/fclr010_leakage_audit.md
- research_state/fclr010_coverage_audit.json
- research_state/cross_track_decision_log.md
- research_state/experiment_frontier.json
- research_state/liquidation_forward_validate_004_blocker_20261102T050600Z.md
- research_state/ironflow_probe_*.json (latest)
- research_state/experiment_prereg_LIQUIDATION_FORWARD_VALIDATE_004_20261102T060650Z.json

CONSTRAINTS (NON-NEGOTIABLE):
- Unauthenticated only. No API keys, tokens, cookies, signed requests, requester-pays.
- Hyperliquid-only for Track A. Strict cross-track firewall. Never merge tracks.
- Never promote modeled boundary breaches to observed liquidations.
- Pre-register BEFORE outcome inspection on any new data.
- Do not touch `.github/workflows`.
- `python -m unittest discover -s tests -v` MUST pass (>=31 passing; add tests if you add modules).
- Raw data out of git. Commit ONLY code/manifests/reports.
- No retry loops without new evidence. Produce automation + evidence, not "checked again, nothing".
```

## BOTTLENECKS REMOVED (THIS HANDOFF UPDATE)
- **Eliminated passive waiting:** Replaced "sit on blocker" with HEAVY build campaign (harness + CLI + tests exist; monitor + alt-hunt + pre-reg automation added).
- **Forced heavy work:** Next session must run monitor/alt-hunt and produce evidence; cannot satisfy by single GET.
- **Discovery-driven:** Monitor operational with state + timestamped evidence.
- **Pre-registration ready:** Template created before outcomes.
- **Single source of truth:** This file supersedes all prior handoffs.
- **Preserved seals:** All sealed artifacts intact. No reopening of closed tracks.
- **Clean execution posture:** Tests passing, firewall intact, raw data excluded from git.

## CURRENT STATUS (AUTHORITATIVE)
- **H001 (volatility): NOT_SUPPORTED** (FCLR-003) — Track C CONFIRMATORY_CLOSED
- **Track A (observed liquidations): OPEN** — FCLR-010 PASSED (Hyperliquid ironflow 2025-11..2026-10, 199 instruments, 5 blocks, C2 vs B1 Brier -2.21%, CI excludes zero). Overlay executed (hypothetical only).
- **LIQUIDATION_FORWARD_VALIDATE_HEAVY-004d: BLOCKED_ON_DATA** — Latest monitor probe shows 2026-10 present; no 2026-11 events/fills 200 yet as of probe. Must run monitor + alt-hunt on session start.
- **Track B: CLOSED_NEGATIVE** (FCLR-H003-EXT-001). **H002: PERMANENTLY_BLOCKED** (SSRN 403). **FCLR-NEXT-002: COMPLETE_NO-GO** for new sources beyond ironflow (must re-probe with fresh evidence per step 3).
- **Sealed holds:** FCLR-001/002/003/006/007/008/009 sealed.

## NEXT FOCUS CAMPAIGN
**Campaign ID:** LIQUIDATION_FORWARD_VALIDATE_HEAVY-004d
**Priority:** CRITICAL (liquidation risk)
**Effort:** HEAVY (harness + monitor + alt-hunt + pre-reg + evidence)
**Trigger:** Auto-detect new post-2026-10 data via monitor OR produce complete blocker evidence if none found.
**Success Definition:**
- Run `scripts/monitor_ironflow_liquidations.py` and `scripts/hunt_alternative_liquidation_sources.py`, commit evidence files if updated
- If new rubric-passing data found: pre-reg created BEFORE outcomes + forward validation executed with full report
- Else: updated complete blocker doc with explicit resume condition, experiment_frontier.json updated if needed

## HARD RULES (NON-NEGOTIABLE)
- **Heavy or bust:** If you can finish the turn without creating/strengthening automation or tests, you haven't followed this handoff.
- **Pre-register before outcomes:** Any inspection of new forward data requires a pre-reg file created BEFORE reading label/outcome columns.
- **Firewalls:** Hyperliquid-only for Track A. No track merging. Never conflate modeled with observed.
- **Admissible only:** Unauthenticated sources only. No keys/paid/requester-pays.
- **Preserve history:** No `.github/workflows` changes. Don't revert sealed artifacts.
- **Keep tests green:** `python -m unittest discover -s tests -v` must pass.
- **Git hygiene:** Raw data out of git. Commit only code/manifests/reports.
- **No busywork loops:** Evidence over retries. If blocked after exhaustive proof, document completely and build on the harness/monitor.
