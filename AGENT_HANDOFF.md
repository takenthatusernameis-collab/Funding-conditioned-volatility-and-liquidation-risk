# AGENT_HANDOFF.md (DURABLE — SINGLE SOURCE OF TRUTH)
**TIMESTAMP (UTC):** 2026-11-02T04:20:39Z
**HANDOFF ID:** FCLR-HANDOFF-088-20261102T042039Z
**SUPERSEDES:** FCLR-HANDOFF-087-20261102T041815Z
**REPO:** Funding-conditioned-volatility-and-liquidation-risk
**REPO PRIORITIZATION (INFERRED):** Liquidation risk > funding-conditioned volatility (repo name). Track A (observed liquidations) is OPEN via Hyperliquid ironflow census — FCLR-010 gate PASSED, overlay EXECUTED (hypothetical only). Data hunt FCLR-NEXT-002 COMPLETE_NO-GO (all 8 source families probed, no NEW admissible unauthenticated source beyond ironflow). Do NOT reopen sealed negative experiments without a concrete new data source meeting pre-registration requirements.

**BRANCH/HEAD:** main @ 0d1398f0766686bf6ef2e5df5e15e70f608979cd

**INITIAL TASK MESSAGE FOR NEXT SESSION (TIMESTAMPED, MANDATORY - CANNOT SKIP):**
```
[2026-11-02T04:20:39Z] FOCUS CAMPAIGN: LIQUIDATION_FORWARD_VALIDATE_HEAVY-004 (HEAVY EXECUTION REQUIRED)

PRIORITY: CRITICAL - LIQUIDATION RISK EXTENSION PER REPO NAME. TRACK A GATE PASSED (FCLR-010, HYPERLIQUID IRONFLOW).

OBJECTIVE (NON-OPTIONAL, HEAVY WORK REQUIRED):
Extend the Track A observed-liquidation forecast on Hyperliquid ironflow census beyond the sealed FCLR-010 test window (2026-05-28..2026-10-31). Acquire post-window liquidation data (November 2026+) from ironflow/hyperliquid-liquidations. Apply the frozen FCLR-010 model WITHOUT retuning or re-splitting. Validate out-of-sample on new forward blocks. Produce block-bootstrap CIs (>=2000 reps), calibration, leave-one-instrument-out robustness, and a gate assessment. Respect cross-track firewall: Hyperliquid only, no Binance merge, no Track B/C conflation. If no post-window data exists, document with concrete evidence (HTTP status, headers, file hashes) and state the resume condition. Do NOT skip pre-registration of any new experiment ID before outcome inspection. Do NOT reopen sealed FCLR-001/002/003/006/007/008/009 holds.

MANDATORY EXECUTION STEPS (DO ALL):
1. READ FIRST: AGENT_HANDOFF.md, RESEARCH_PROMPT.md §5, research_state/experiment_frontier.json, research_state/cross_track_decision_log.md, research_state/research_protocol_fclr010.md, research_state/evaluation_summary_FCLR010.md. Treat as authoritative.
2. DATA ACQUISITION (heavy): Query ironflow/hyperliquid-liquidations for data beyond 2026-10-31 (e.g., 2026-11 monthly parquet). Attempt actual download. Record exact URL, access_date (UTC), HTTP status, headers, file hashes, schema, row counts, symbol coverage. Verify unauthenticated access (no keys).
3. PRE-REGISTRATION (BEFORE OUTCOMES): If new data found, create research_state/experiment_prereg_<ID>.json + protocol delta pre-registering the forward validation experiment BEFORE inspecting any outcomes. Freeze splits with frozen_before_outcomes=true.
4. FORWARD VALIDATION (heavy): Apply frozen FCLR-010 model (C2 vs B1 on Brier) to new forward block(s). Compute paired comparisons with block bootstrap (>=2000 reps), calibration, leave-one-instrument-out. Write research_state/evaluation_summary_<ID>.md + gate assessment.
5. EVIDENCE DOCUMENTATION: If NO new data exists, write research_state/liquidation_forward_validate_004_blocker_YYYYMMDDTHHMMSSZ.md with full per-source evidence table (URL, status, headers, hashes, rejection reason). Update experiment_frontier.json resume condition.
6. GO RUBRIC (STRICT): >=5 symbols, >=3 non-overlapping 30-day blocks, documented completeness, license OK, no signed request, no requester-pays. ALL must hold for a new confirmatory claim.
7. UPDATE HANDOFF: Update AGENT_HANDOFF.md with results, next action, and verification command.

CONSTRAINTS: Only admissible unauthenticated sources. Never merge Track A/B/C. Never promote modeled breaches to observed liquidations. Never touch .github/workflows. Tests must pass (`python -m unittest discover -s tests -v`). Keep raw data out of git. Commit only code/manifests/reports.
```

## BOTTLENECKS REMOVED
- Track A is OPEN (not blocked): FCLR-010 gate PASSED on Hyperliquid ironflow census (2025-11..2026-10, 199 instruments, 5 blocks). Removed stale "Track A BLOCKED for 2024" claim.
- LIQUIDATION_DATA_HUNT_HEAVY-003 campaign SUPERSEDED: FCLR-NEXT-002 already completed NO-GO (all 8 source families probed). Removed stale data-hunt campaign.
- HEAD corrected: main @ 0d1398f0 (was stale a03d9a63).
- Consolidated to single durable handoff (this file). No duplicate handoff files.
- All sealed artifacts verified intact (FCLR-HEAVY-001 integrity OK). No reopening of closed negative tracks.
- Tests: `python -m unittest discover -s tests -v` passes (27/27).
- No workflow modifications. No redundant controllers/schedulers added.

## CURRENT STATUS (AUTHORITATIVE)
- **H001 (volatility forecasting): NOT_SUPPORTED** (FCLR-003) — forecast gate failed. Track C CONFIRMATORY_CLOSED. No risk overlay eligible on Track C.
- **Track A (observed liquidations): OPEN** — FCLR-010 gate PASSED (Hyperliquid ironflow, 2025-11..2026-10, 199 instruments, 5 blocks, C2 vs B1 Brier -2.21%, CI excludes zero). Overlay EXECUTED (hypothetical only, no profitability claim). FCLR-HEAVY-001 complete (all 6 steps).
- **Track B (hypothetical boundary breach): CLOSED_NEGATIVE** (FCLR-H003-EXT-001). No incremental skill.
- **H002 (paper replication): PERMANENTLY BLOCKED** (SSRN HTTP 403). No further work without SSRN access.
- **Data hunt: COMPLETE_NO-GO** (FCLR-NEXT-002) — all 8 source families probed, no NEW admissible unauthenticated source beyond ironflow.
- **Sealed holds:** FCLR-001/002/003/006/007/008/009 sealed. Do not reopen.

## NEXT FOCUS CAMPAIGN (HEAVY WORK - CANNOT AVOID)
**Campaign ID:** LIQUIDATION_FORWARD_VALIDATE_HEAVY-004
**Priority:** CRITICAL (liquidation risk per repo name)
**Effort:** Heavy (data acquisition + frozen model forward validation + block-bootstrap + robustness)
**Success Criterion:** Either (a) forward validation on new post-FCLR-010 block with full evidence + gate assessment, or (b) complete evidence-based blocker documenting no post-window data exists + resume condition stated.

**HARD RULES:**
- Heavy work only. Landing page checks insufficient — must attempt actual access/downloads with evidence (HTTP status, headers, file listing, hashes).
- Pre-register new experiment ID BEFORE inspecting any outcomes on new data.
- Cross-track firewall: Hyperliquid only, no Binance merge, no Track B/C conflation.
- Never fabricate data/sources.
- If blocked, document with headers/status and move on — no retry loops without new evidence.
- If no post-window data exists after exhaustive evidence, write complete blocker and state resume condition. No blocking/waiting loops.
- Every candidate/source tested must appear in evidence with rejection reason if not GO.
