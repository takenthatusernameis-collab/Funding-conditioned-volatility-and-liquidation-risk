# LIQUIDATION_FORWARD_VALIDATE_004 BLOCKER EVIDENCE — SESSION 2026-11-02T12:48:00Z (HEAVY)

**Campaign:** LIQUIDATION_FORWARD_VALIDATE_HEAVY-004i (forward validation of frozen FCLR-010 model on post-2026-10-31 Hyperliquid ironflow liquidation data)
**Session timestamp:** 2026-11-02T12:48:00Z
**Repo HEAD:** ec848c9e (chore(kilo): checkpoint agent session)
**Verdict:** NO-GO for this session — no post-2026-10-31 (2026-11+) observed-liquidation data exists yet on the sole admissible source. Forward validation DEFERRED, not skipped. Resume condition stated below.

## Governing references (read first, authoritative)
- AGENT_HANDOFF.md (current) — single durable handoff; campaign LIQUIDATION_FORWARD_VALIDATE_HEAVY-004i
- RESEARCH_PROMPT.md §§1,5,6,7,8,15 — admissible sources, Track A firewall, freeze-before-outcomes, no fabricated data
- research_state/research_protocol_fclr010.md v1.0 — frozen FCLR-010 model (C2 vs B1 on Brier), splits frozen_before_outcomes=true
- research_state/evaluation_summary_FCLR010.md — gate PASSED (C2 vs B1 Brier rel −2.21%, CI excludes zero)
- research_state/cross_track_decision_log.md — Track A = Hyperliquid ironflow ONLY; no track merge; modeled != observed
- research_state/experiment_frontier.json — FCLR-NEXT-002 COMPLETE_NO-GO

## Step 1 — state read (authoritative, this session)
- AGENT_HANDOFF.md, RESEARCH_PROMPT.md §§1,5,6,7,8, experiment_frontier.json, cross_track_decision_log.md, research_protocol_fclr010.md, evaluation_summary_FCLR010.md: read.
- Monitor run (fresh): `python scripts/monitor_ironflow_liquidations.py` → wrote `research_state/ironflow_probe_<ts>.json`, updated `research_state/ironflow_monitor_state.json`. New files found: [] (genuinely new). data_through: 2026-10, consecutive_absent: 3. post-2026-10 available: None.
- Alt-hunt run (fresh): `python scripts/hunt_alternative_liquidation_sources.py` → updated `research_state/data_source_registry_alt_hunt.json`. No new admissible unauthenticated Track A sources found.
- Tests: `python -m unittest discover -s tests -v` → 49/49 PASS (7 new automation tests added this session).
- No sealed artifacts touched. No Track B/C conflation. No .github/workflows changes.

## Step 2 — data acquisition evidence (actual access attempted, unauthenticated, no keys)
Source: ironflow/hyperliquid-liquidations (Hugging Face, CC BY 4.0) — sole admissible unauthenticated liquidation census per FCLR-NEXT-002.

Tree listing: `https://huggingface.co/api/datasets/ironflow/hyperliquid-liquidations/tree/main?recursive/latest` → HTTP 200, parsed OK. Parquet paths span 2025-05..2026-10 for both `data/events/` and `data/fills/`. No path for any month >= 2026-11.

Month-by-month probe results (unauthenticated GET, resolve URLs):
- 2026-05 events/fills: HTTP 200 (NEW_AVAILABLE)
- 2026-06 events/fills: HTTP 200 (NEW_AVAILABLE)
- 2026-07 events/fills: HTTP 200 (NEW_AVAILABLE)
- 2026-08 events/fills: HTTP 200 (NEW_AVAILABLE)
- 2026-09 events/fills: HTTP 200 (NEW_AVAILABLE)
- 2026-10 events/fills: HTTP 200 (NEW_AVAILABLE)
- 2026-11 events: HTTP 404 EntryNotFound (CONFIRMED_ABSENT); fills: HTTP 404 EntryNotFound (CONFIRMED_ABSENT)
- 2026-12 events: HTTP 404 EntryNotFound (CONFIRMED_ABSENT); fills: HTTP 404 EntryNotFound (CONFIRMED_ABSENT)
- 2027-01 events: HTTP 404 EntryNotFound (CONFIRMED_ABSENT); fills: HTTP 404 EntryNotFound (CONFIRMED_ABSENT)

Full probe tables with headers and body previews: `research_state/ironflow_probe_20261102T115745Z.json` (last probe) and `research_state/ironflow_monitor_state.json` (current state).

Unauthenticated confirmed (no API key, no signed request, no requester-pays, no registration). No other admissible unauthenticated source found via fresh alt-hunt (12 candidate families probed, all NO-GO or REVIEW_REQUIRED-without-census).

## Step 3 — pre-registration status
Template exists: `research_state/experiment_prereg_LIQUIDATION_FORWARD_VALIDATE_004_20261102T060650Z.json` (frozen_before_outcomes=true). Fresh pre-reg with new timestamp MUST be created BEFORE inspecting outcomes on any rubric-passing post-2026-10-31 data.

## Step 4 — forward validation
NOT EXECUTED. Frozen FCLR-010 harness (`scripts/fclr010_harness.py`, `scripts/fclr010_validate.py`) ready; no new forward block available.

## Step 5 — blocker evidence (complete) + automation strengthened
- Monitor improved (ETag tree caching with If-None-Match conditional GET, wider lookahead 6 months, exponential backoff with retry budget, rate-limit awareness, state-aware diff, wider window, failure classification, data_through/consecutive_absent tracking). Tests added: `tests/test_monitor_ironflow.py` (ETag caching, month-window, state-diff, consecutive absent, classification). All tests pass: 49/49.
- Alt-hunt strengthened (12 source families, rubric scoring, retry/backoff, exhaustive unauthenticated probes).
- Full probe tables in `ironflow_probe_20261102T115745Z.json`. Alt-hunt evidence in `research_state/data_source_registry_alt_hunt.json`.

**Resume condition (concrete, checkable):**
1. Ironflow publishes `data/events/YYYY-MM.parquet` and/or `data/fills/YYYY-MM.parquet` for any month >= 2026-11 with HTTP 200 on unauthenticated GET to resolve URLs (verify via `scripts/monitor_ironflow_liquidations.py` — state-aware; reports genuinely new files), OR
2. Any NEW admissible unauthenticated source passes strict GO rubric: >=5 symbols, >=1 complete month OR >=3 non-overlapping 30-day blocks, documented completeness/coverage, permissive license, unauthenticated access confirmed (no signed request, no keys, no requester-pays), schema compatible with frozen FCLR-010 model (observed liquidation labels compatible with C2 vs B1 contrast on Brier). Hyperliquid-only for Track A.

On resume: run monitor + alt-hunt, create fresh pre-reg BEFORE outcome inspection if GO, execute frozen harness with block-bootstrap >=2000 reps, calibration, LOO, concentration, multiplicity handling, write full evaluation summary with gate assessment. If still NO-GO, re-document with fresh evidence and restate resume condition — no retry loops without new evidence.

## Step 6 — constraints honored
- Unauthenticated only. No keys/tokens/cookies/signed requests/requester-pays.
- Hyperliquid-only for Track A. Strict cross-track firewall. No track merging.
- Never promote modeled boundary breaches to observed liquidations.
- Pre-register BEFORE outcome inspection on new data.
- No .github/workflows changes.
- Tests green (49/49). Raw data out of git. Only evidence/code/manifests/reports committed.

## Heavy work completed this session (BLOCKED PATH, MANDATORY)
1. Strengthened `scripts/monitor_ironflow_liquidations.py`: ETag tree caching (If-None-Match, skip re-parse on 304), wider lookahead (6 months), exponential backoff + retry budget on 429/5xx, rate-limit awareness, tree_etag persisted in state.
2. Strengthened `scripts/hunt_alternative_liquidation_sources.py`: 12 source families (up from 8), rubric-scored GO/NO-GO assessment, retry/backoff, broader unauthenticated probes (broad HF liquidation search, GitHub code/repo search).
3. Added 7 tests to `tests/test_monitor_ironflow.py`: ETag caching (304 skip / 200 update), month-window coverage, state-diff edge cases, consecutive absent counting. Suite: 49/49 PASS.
4. This blocker doc (fresh timestamp, complete probe tables, explicit resume conditions).
5. Next campaign artifact: `research_state/heavy_work_checklist_004i.md` — non-skippable heavy-work checklist for all future sessions.
