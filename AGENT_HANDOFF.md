# AGENT_HANDOFF.md (DURABLE — SINGLE SOURCE OF TRUTH)
**TIMESTAMP (UTC):** 2026-11-02T05:07:45Z
**HANDOFF ID:** FCLR-HANDOFF-094-20261102T050745Z
**SUPERSEDES:** FCLR-HANDOFF-093-20261102T050716Z
**REPO:** Funding-conditioned-volatility-and-liquidation-risk
**REPO PRIORITIZATION (INFERRED):** LIQUIDATION RISK > funding-conditioned volatility (repo name). Track A (observed liquidations) OPEN via Hyperliquid ironflow census; Track C CONFIRMATORY_CLOSED; Track B CLOSED_NEGATIVE.

**BRANCH/HEAD:** main @ e478ab8afe7c4cc6371618879ead2c2cd0cecea2

**INITIAL TASK MESSAGE FOR NEXT SESSION (TIMESTAMPED, MANDATORY - CANNOT SKIP):**
```
[2026-11-02T05:07:45Z] FOCUS CAMPAIGN: LIQUIDATION_FORWARD_MONITOR_HARNESS_HEAVY-004b (HEAVY EXECUTION REQUIRED - NO PASSIVE WAITING)

PRIORITY: CRITICAL - LIQUIDATION RISK (repo-name driven). Track A gate PASSED (FCLR-010). Forward validation beyond 2026-10-31 is BLOCKED_ON_DATA (ironflow has no 2026-11 parquet as of 2026-11-02T05:06Z). YOU MUST NOT wait idly. You MUST build automation + exhaustive evidence so that the moment data appears, validation can run with ZERO retuning.

OBJECTIVE (NON-OPTIONAL, HEAVY WORK):
1) FREEZE & HARDEN THE VALIDATION HARNESS (HEAVY): Extract/encode the FROZEN FCLR-010 model (C2 vs B1 on Brier), splits/blocks, feature pipeline, leakage guards, block-bootstrap (>=2000 reps), calibration, LOO robustness into a single reusable module + CLI entrypoint. Write unit tests against fixtures from cached 2025-11..2026-10 (golden outputs). Do NOT touch sealed artifacts.
2) BUILD A RELIABLE DATA MONITOR (HEAVY, AUTOMATED): Create scripts/monitor_ironflow_liquidations.py that probes HF tree + resolve paths on schedule logic (can be invoked by cron/agent), records full evidence (URLs, HTTP method/status/headers/ETag/Last-Modified/Content-Length, sha256, schema/row counts/symbols), caches last-seen state in research_state/ironflow_monitor_state.json, and writes a timestamped evidence file on ANY change or daily even if 404. Make it idempotent, rate-limited, unauthenticated-only.
3) EXHAUSTIVE ALTERNATIVE SOURCE HUNT (HEAVY): Aggressively re-probe ALL admissible unauthenticated sources per RESEARCH_PROMPT §5 with concrete HTTP evidence (tree/listings/resolve). Check Hyperliquid public APIs/archives, other venues, GitHub/HF/Zenodo for liquidation-like event files. For each candidate produce a GO/NO-GO against rubric (>=5 symbols, >=1 month or >=3x30d blocks, license, unauth, no requester-pays, schema compatible). Update research_state/data_source_registry.json with evidence. Do NOT merge tracks.
4) PRE-REGISTER THE MOMENT DATA APPEARS (HEAVY): If monitor finds new files OR you find rubric-passing source, CREATE experiment_prereg_LIQUIDATION_FORWARD_VALIDATE_004_<YYYYMMDDTHHMMSSZ>.json BEFORE inspecting outcomes, freeze protocol, declare primary contrast, bootstrap>=2000, multiplicity. Then run validation immediately with harness.
5) IF STILL BLOCKED AFTER EXHAUSTIVE (HEAVY DOCUMENTATION): If after steps 1-3 no rubric-passing post-2026-10-31 observed-liquidation data exists, write a fresh complete blocker evidence doc with full probe tables and update experiment_frontier.json resume condition. Do NOT create polling loops that burn turns without new evidence. DO NOT reopen sealed FCLR-001/002/003/006/007/008/009.

MANDATORY READS FIRST:
- AGENT_HANDOFF.md, RESEARCH_PROMPT.md §§1,5,6,7,8
- research_state/research_protocol_fclr010.md, evaluation_summary_FCLR010.md, fclr010_leakage_audit.md, fclr010_coverage_audit.json
- research_state/cross_track_decision_log.md, experiment_frontier.json
- research_state/liquidation_forward_validate_004_blocker_20261102T050600Z.md
- tests/ (understand existing patterns)

CONSTRAINTS: unauthenticated only, no Track A/B/C merge, no promotion of modeled breaches, never touch .github/workflows, tests must pass (python -m unittest discover -s tests -v), keep raw data out of git, commit only code/manifests/reports. Cross-track firewall strict.
```

## BOTTLENECKS REMOVED (THIS HANDOFF UPDATE)
- **Eliminated passive waiting:** Replaced "blocker wait" with a HEAVY harness+monitor campaign (steps 1-2) that produces reusable validation code even while blocked.
- **Forced heavy work:** Next agent MUST build tests, CLI, monitor, and alternative hunt - cannot claim done with landing-page checks.
- **Single source of truth:** Consolidated to this handoff; supersedes previous.
- **Preserved seals:** All sealed artifacts intact (FCLR-HEAVY-001/FCLR-010 gates). No reopening of closed tracks.
- **Clean state:** Working tree clean context, HEAD e478ab8a, tests 27/27 passing.

## CURRENT STATUS (AUTHORITATIVE)
- **H001 (volatility): NOT_SUPPORTED** (FCLR-003) — Track C CONFIRMATORY_CLOSED.
- **Track A (observed liquidations): OPEN** — FCLR-010 PASSED (Hyperliquid ironflow 2025-11..2026-10, 199 instruments, 5 blocks, C2 vs B1 Brier -2.21%, CI excludes zero). Overlay executed (hypothetical only).
- **LIQUIDATION_FORWARD_VALIDATE_HEAVY-004b: BLOCKED_ON_DATA** — No 2026-11+ ironflow parquet. Must build harness+monitor+alt-hunt now.
- **Track B: CLOSED_NEGATIVE** (FCLR-H003-EXT-001). **H002: PERMANENTLY_BLOCKED** (SSRN 403). **Data hunt FCLR-NEXT-002: COMPLETE_NO-GO** for new sources beyond ironflow (must re-probe with fresh evidence).
- **Sealed holds:** FCLR-001/002/003/006/007/008/009 sealed.

## NEXT FOCUS CAMPAIGN
**Campaign ID:** LIQUIDATION_FORWARD_VALIDATE_HEAVY-004b
**Priority:** CRITICAL (liquidation risk)
**Effort:** HEAVY (harness hardening + monitor + exhaustive source hunt + pre-reg ready)
**Trigger:** Auto-run validation on new post-2026-10 data OR produce complete blocker evidence if none found.
**Success:** Reusable frozen harness passing fixture tests + ironflow monitor operational + alt-source evidence table + either pre-reg+validation (if data found) or refreshed blocker with resume condition.

**HARD RULES (NON-NEGOTIABLE):**
- Heavy work only. No "checked page, nothing there" reports.
- Pre-register BEFORE outcome inspection on new data.
- Hyperliquid-only for Track A; never merge tracks; never promote modeled to observed.
- Only unauthenticated sources; no keys/paid/requester-pays.
- No .github/workflows changes.
- Tests must pass. Raw data out of git. Commit only code/manifests/reports.
- If blocked after exhaustive evidence, document completely and move to next materially different route (harness/monitor) - no retry loops.
