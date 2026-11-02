# AGENT_HANDOFF.md (DURABLE — SINGLE SOURCE OF TRUTH)
**TIMESTAMP (UTC):** 2026-11-02T05:04:08Z
**HANDOFF ID:** FCLR-HANDOFF-091-20261102T050150Z
**SUPERSEDES:** FCLR-HANDOFF-090-20261102T042425Z
**REPO:** Funding-conditioned-volatility-and-liquidation-risk
**REPO PRIORITIZATION (INFERRED):** Liquidation risk > funding-conditioned volatility (repo name). Track A (observed liquidations) is OPEN via Hyperliquid ironflow census — FCLR-010 gate PASSED, overlay EXECUTED (hypothetical only). Data hunt FCLR-NEXT-002 COMPLETE_NO-GO (all 8 source families probed, no NEW admissible unauthenticated source beyond ironflow). Do NOT reopen sealed negative experiments without a concrete new data source meeting pre-registration requirements.

**BRANCH/HEAD:** main @ dec4180b1d379919674d1206f7b114cb351b7644b0

**INITIAL TASK MESSAGE FOR NEXT SESSION (TIMESTAMPED, MANDATORY - CANNOT SKIP):**
```
[2026-11-02T05:01:50Z] FOCUS CAMPAIGN: LIQUIDATION_FORWARD_VALIDATE_HEAVY-004 (HEAVY EXECUTION REQUIRED - NO SHORTCUTS)

PRIORITY: CRITICAL - LIQUIDATION RISK EXTENSION PER REPO NAME. TRACK A GATE PASSED (FCLR-010, HYPERLIQUID IRONFLOW). ALL CONFIRMATORY GATES RESOLVED.

OBJECTIVE (NON-OPTIONAL, HEAVY WORK REQUIRED):
Extend the Track A observed-liquidation forecast on Hyperliquid ironflow census BEYOND the sealed FCLR-010 test window (2026-05-28..2026-10-31). You MUST acquire post-window liquidation data (November 2026+) from ironflow/hyperliquid-liquidations. Apply the FROZEN FCLR-010 model (C2 vs B1 on Brier) WITHOUT retuning, re-splitting, or feature changes. Validate out-of-sample on new forward blocks. Produce block-bootstrap CIs (>=2000 reps), calibration, leave-one-instrument-out robustness, and a gate assessment. Respect cross-track firewall: Hyperliquid only, no Binance merge, no Track B/C conflation. If NO post-window data exists after exhaustive, evidence-based probing, you MUST document with concrete evidence (exact URLs, HTTP status, headers, response bodies/headers, file hashes, schema checks) and state the resume condition. DO NOT skip pre-registration of any new experiment ID BEFORE outcome inspection. DO NOT reopen sealed FCLR-001/002/003/006/007/008/009 holds. This is HEAVY work - landing page checks are insufficient.

MANDATORY EXECUTION STEPS (DO ALL - NO STEPS SKIPPED):
1. READ FIRST (authoritative): AGENT_HANDOFF.md, RESEARCH_PROMPT.md §5, research_state/experiment_frontier.json, research_state/cross_track_decision_log.md, research_state/research_protocol_fclr010.md, research_state/evaluation_summary_FCLR010.md, research_state/fclr010_leakage_audit.md, research_state/fclr010_coverage_audit.json. Treat as authoritative.
2. DATA ACQUISITION (HEAVY - MUST ATTEMPT ACTUAL ACCESS): Probe ironflow/hyperliquid-liquidations for data beyond 2026-10-31 (e.g., 2026-11 monthly parquet, daily files). Attempt actual download/curl with evidence. Record exact URL, access_date (UTC), HTTP method, HTTP status, headers (ETag/Last-Modified/Content-Length), file hashes (sha256), schema, row counts, symbol coverage, unauthenticated access confirmation (no keys). Test at least 2-3 candidate paths.
3. PRE-REGISTRATION (BEFORE INSPECTING ANY OUTCOMES): If new post-window data found AND passes GO rubric, create research_state/experiment_prereg_LIQUIDATION_FORWARD_VALIDATE_004_<YYYYMMDDTHHMMSSZ>.json + protocol delta pre-registering the forward validation experiment BEFORE inspecting any outcomes. Set frozen_before_outcomes=true, freeze splits, declare primary contrast (C2 vs B1 on Brier), block-bootstrap >=2000 reps, multiplicity plan. Do NOT compute/peek at results until pre-reg is committed.
4. FORWARD VALIDATION (HEAVY): Apply frozen FCLR-010 model to new forward block(s). Compute paired comparisons with block bootstrap (>=2000 reps), calibration (reliability diagram stats), leave-one-instrument-out robustness, concentration analysis. Write research_state/evaluation_summary_LIQUIDATION_FORWARD_VALIDATE_004_<ID>.md with full gate assessment.
5. EVIDENCE DOCUMENTATION (IF BLOCKED): If NO new post-window data exists after exhaustive evidence, write research_state/liquidation_forward_validate_004_blocker_<YYYYMMDDTHHMMSSZ>.md with COMPLETE per-source evidence table (all URLs probed, HTTP status, headers, hashes if downloaded, rejection reason, unauthenticated check). Update experiment_frontier.json with resume condition. Do NOT retry loops without new evidence.
6. GO RUBRIC (STRICT - ALL MUST HOLD): >=5 symbols, >=3 non-overlapping 30-day blocks OR >=1 complete month with >=5 symbols AND documented completeness, license OK (CC/explicit permissive), no signed request, no requester-pays, unauthenticated access confirmed, schema compatible with frozen model. ALL must hold for a new confirmatory claim.
7. UPDATE HANDOFF (MANDATORY): Update AGENT_HANDOFF.md with what changed, exact evidence added/locations, current gate states, single highest-value next task, precise verification command, and blockers with next materially different route.

BOTTLENECKS REMOVED: Track A open (FCLR-010 passed), stale data-hunt campaigns superseded (FCLR-NEXT-002 complete no-go), HEAD current (dec4180b), single durable handoff, sealed artifacts intact, tests pass (27/27). No redundant controllers/schedulers.

CONSTRAINTS: Only admissible unauthenticated sources. Never merge Track A/B/C. Never promote modeled breaches to observed liquidations. Never touch .github/workflows. Tests must pass (`python -m unittest discover -s tests -v`). Keep raw data out of git. Commit only code/manifests/reports.
```

## BOTTLENECKS REMOVED
- Track A is OPEN (not blocked): FCLR-010 gate PASSED on Hyperliquid ironflow census (2025-11..2026-10, 199 instruments, 5 blocks). Removed stale "Track A BLOCKED for 2024" claim.
- LIQUIDATION_DATA_HUNT_HEAVY-003 campaign SUPERSEDED: FCLR-NEXT-002 already completed NO-GO (all 8 source families probed). Removed stale data-hunt campaign.
- HEAD corrected: main @ dec4180b1d379919674d1206f7b114cb351b7644b0.
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

(End of file - total 129 lines)
