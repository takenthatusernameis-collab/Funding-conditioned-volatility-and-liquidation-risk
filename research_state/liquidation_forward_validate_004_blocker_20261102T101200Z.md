# LIQUIDATION_FORWARD_VALIDATE_004 BLOCKER EVIDENCE — SESSION 2026-11-02T10:12:00Z (HEAVY)

**Campaign:** LIQUIDATION_FORWARD_VALIDATE_HEAVY-004g (forward validation of frozen FCLR-010 model on post-2026-10-31 Hyperliquid ironflow liquidation data)
**Session timestamp:** 2026-11-02T10:12:00Z
**Repo HEAD:** a60a5afdb669b795cc2ab10b4bcd1eaa7df4118c
**Verdict:** NO-GO for this session — no post-2026-10-31 (2026-11+) observed-liquidation data exists yet on the sole admissible source. Forward validation DEFERRED, not skipped. Resume condition stated below.

## Governing references (read first, authoritative)
- AGENT_HANDOFF.md (FCLR-HANDOFF-109, current) — single durable handoff; campaign LIQUIDATION_FORWARD_VALIDATE_HEAVY-004g
- RESEARCH_PROMPT.md §§1,5,6,7,8,15 — admissible sources, Track A firewall, freeze-before-outcomes, no fabricated data
- research_state/research_protocol_fclr010.md v1.0 — frozen FCLR-010 model (C2 vs B1 on Brier), splits frozen_before_outcomes=true
- research_state/evaluation_summary_FCLR010.md — gate PASSED (C2 vs B1 Brier rel −2.21%, CI excludes zero)
- research_state/cross_track_decision_log.md — Track A = Hyperliquid ironflow ONLY; no track merge; modeled != observed
- research_state/experiment_frontier.json — FCLR-NEXT-002 COMPLETE_NO-GO (all 8 source families probed)

## Step 1 — state read (authoritative, this session)
- AGENT_HANDOFF.md, RESEARCH_PROMPT.md §§1,5,6,7,8, experiment_frontier.json, cross_track_decision_log.md, research_protocol_fclr010.md, evaluation_summary_FCLR010.md: read.
- Monitor run (fresh): `python scripts/monitor_ironflow_liquidations.py` → wrote `research_state/ironflow_probe_20261102T101024Z.json`, updated `research_state/ironflow_monitor_state.json`. New files found: none (genuinely new). data_through: 2026-10, consecutive_absent: 3. post-2026-10 available: False.
- Alt-hunt run (fresh): `python scripts/hunt_alternative_liquidation_sources.py` → updated `research_state/data_source_registry_alt_hunt.json`. No new admissible unauthenticated Track A sources found.
- Tests: `python -m unittest discover -s tests -v` → 42/42 PASS.
- No sealed artifacts touched. No Track B/C conflation. No .github/workflows changes.

## Step 2 — data acquisition evidence (actual access attempted, unauthenticated, no keys)
Source: ironflow/hyperliquid-liquidations (Hugging Face, CC BY 4.0) — sole admissible unauthenticated liquidation census per FCLR-NEXT-002.

Latest probe (20261102T101024Z): tree parsed OK (parquet_paths include 2025-05..2026-10 for events and fills). Probed months include 2026-10, 2026-11, 2026-12, 2027-01:
- 2026-10 events/fills: HTTP 200 (confirmed present)
- 2026-11 events/fills: HTTP 404 (EntryNotFound)
- 2026-12 events/fills: HTTP 404
- 2027-01 events/fills: HTTP 404

Unauthenticated confirmed (no API key, no signed request, no requester-pays, no registration). Repo-name prioritization applied (liquidation risk > volatility). No other admissible unauthenticated source found via fresh alt-hunt.

## Step 3 — pre-registration status
Template exists: `research_state/experiment_prereg_LIQUIDATION_FORWARD_VALIDATE_004_20261102T060650Z.json` (frozen_before_outcomes=true). Fresh pre-reg with new timestamp MUST be created BEFORE inspecting outcomes on any rubric-passing post-2026-10-31 data.

## Step 4 — forward validation
NOT EXECUTED. Frozen FCLR-010 harness (`scripts/fclr010_harness.py`, `scripts/fclr010_validate.py`) ready; no new forward block available.

## Step 5 — blocker evidence (complete) + automation strengthened
- Monitor improved (state-aware diff, wider window, failure classification, data_through/consecutive_absent). Tests added: `tests/test_monitor_ironflow.py` (5 tests). All tests pass.
- Full probe tables in `research_state/ironflow_probe_20261102T101024Z.json`. Alt-hunt evidence in `research_state/data_source_registry_alt_hunt.json`.

**Resume condition (concrete, checkable):**
1. Ironflow publishes `data/events/YYYY-MM.parquet` and/or `data/fills/YYYY-MM.parquet` for any month >= 2026-11 with HTTP 200 on unauthenticated GET to resolve URLs (verify via `scripts/monitor_ironflow_liquidations.py` — it is now state-aware and will report genuinely new files), OR
2. Any NEW admissible unauthenticated source passes strict GO rubric: >=5 symbols, >=1 complete month OR >=3 non-overlapping 30-day blocks, documented completeness/coverage, permissive license, unauthenticated access confirmed (no signed request, no keys, no requester-pays), schema compatible with frozen FCLR-010 model (observed liquidation labels compatible with C2 vs B1 contrast on Brier). Hyperliquid-only for Track A.

On resume: run monitor + alt-hunt, create fresh pre-reg BEFORE outcome inspection if GO, execute frozen harness with block-bootstrap >=2000 reps, calibration, LOO, concentration, multiplicity handling, write full evaluation summary with gate assessment. If still NO-GO, re-document with fresh evidence and restate resume condition — no retry loops without new evidence.

## Step 6 — constraints honored
- Unauthenticated only. No keys/tokens/cookies/signed requests/requester-pays.
- Hyperliquid-only for Track A. Strict cross-track firewall. No track merging.
- Never promote modeled boundary breaches to observed liquidations.
- Pre-register BEFORE outcome inspection on new data.
- No .github/workflows changes.
- Tests green (42/42). Raw data out of git. Only evidence/code/manifests/reports committed.
