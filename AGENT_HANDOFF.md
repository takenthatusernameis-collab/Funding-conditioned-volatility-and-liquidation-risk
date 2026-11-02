# AGENT_HANDOFF.md (DURABLE — SINGLE SOURCE OF TRUTH)
**TIMESTAMP (UTC):** 2026-11-02T05:57:15Z
**HANDOFF ID:** FCLR-HANDOFF-097-20261102T055715Z
**SUPERSEDES:** FCLR-HANDOFF-096-20261102T055530Z
**REPO:** Funding-conditioned-volatility-and-liquidation-risk
**REPO PRIORITIZATION (INFERRED):** LIQUIDATION RISK > funding-conditioned volatility (repo name). Track A (observed liquidations) is the only open confirmatory track. Treat liquidation risk as the default axis of work until Track A is resolved or exhaustively blocked with irrefutable evidence.

**BRANCH/HEAD:** main @ e478ab8afe7c4cc6371618879ead2c2cd0cecea2

**INITIAL TASK MESSAGE FOR NEXT SESSION (TIMESTAMPED, MANDATORY - CANNOT SKIP):**
```
[2026-11-02T06:01:54Z] FOCUS CAMPAIGN: LIQUIDATION_FORWARD_MONITOR_AUTOMATE_HEAVY-004d (HEAVY EXECUTION REQUIRED - NO PASSIVE WAITING)

PRIORITY: CRITICAL - LIQUIDATION RISK (repo-name driven). Track A gate PASSED (FCLR-010). Forward validation beyond 2026-10-31 is BLOCKED_ON_DATA (ironflow has no 2026-11 parquet as of 2026-11-02T06:01:54Z). The block is DATA AVAILABILITY, not methodology. YOU MUST NOT idle, poll in conversation, or "check the landing page once". YOU MUST convert this block into reusable automation and airtight evidence.

OBJECTIVE (NON-OPTIONAL, HEAVY WORK - DO ALL OF THE BELOW):
1) FREEZE & HARDEN THE VALIDATION HARNESS (HEAVY, CODE + TESTS)
   - Extract and encode the FROZEN FCLR-010 model (C2 vs B1 on Brier) into a single, importable module (e.g. `scripts/fclr010_harness.py` or `research/fclr010_harness.py`). Include: feature pipeline, leakage guards, frozen splits from `run_manifest.json#split_boundaries_fclr010`, block structure, block-bootstrap (>=2000 reps), calibration, LOO robustness, and concentration analysis.
   - Add a CLI entrypoint (e.g. `python -m ...` or `scripts/fclr010_validate.py`) that can validate against a provided parquet path without retuning anything.
   - Write unit tests against fixtures derived from cached 2025-11..2026-10 outputs (golden values). Add to `tests/` and make them pass.
   - DO NOT touch any sealed artifacts (FCLR-001/002/003/006/007/008/009).

2) BUILD A RELIABLE IRONFLOW MONITOR (HEAVY, AUTOMATED)
   - Create `scripts/monitor_ironflow_liquidations.py` (idempotent, unauthenticated-only, rate-limited). Must probe the HF tree (`ironflow/hyperliquid-liquidations`) and directly resolve `data/events/YYYY-MM.parquet` and `data/fills/YYYY-MM.parquet`.
   - For EVERY probe: record full evidence (URLs, method, HTTP status, headers: Date/ETag/Last-Modified/Content-Length, sha256 of any downloaded bytes if present, schema/row counts/symbols).
   - Cache last-seen state in `research_state/ironflow_monitor_state.json`. On ANY change OR at least once per run even if 404, write a timestamped evidence file under `research_state/` (e.g. `ironflow_probe_YYYYMMDDTHHMMSSZ.json`).
   - Make it scriptable for reuse (can be invoked ad-hoc). No keys, no signed requests, no requester-pays.
   - If a new file appears (>=2026-11), DO NOT just log it - trigger step 4.

3) EXHAUSTIVE ALTERNATIVE SOURCE HUNT (HEAVY, EVIDENCE-DRIVEN)
   - Re-probe ALL admissible unauthenticated families per RESEARCH_PROMPT §5 with concrete HTTP evidence (tree/listings/resolve). Do not rely on memory from prior probes.
   - Explicitly re-check: Hyperliquid public APIs/archives, other venues, GitHub raw search with evidence, HuggingFace other datasets, Zenodo/OSF/arXiv, CryptoDataDownload.
   - For each candidate produce a strict GO/NO-GO against rubric: >=5 symbols, >=1 complete month OR >=3 non-overlapping 30-day blocks, documented completeness, license OK, unauthenticated access confirmed, no requester-pays, schema compatible with frozen FCLR-010.
   - Update `research_state/data_source_registry.json` with per-candidate evidence tables. DO NOT merge Track A with B or C. Never promote modeled breaches to observed liquidations.

4) PRE-REGISTER & VALIDATE ON DISCOVERY (HEAVY, DISCIPLINED)
   - If monitor finds new post-2026-10-31 files OR you find a rubric-passing source: CREATE `research_state/experiment_prereg_LIQUIDATION_FORWARD_VALIDATE_004_<YYYYMMDDTHHMMSSZ>.json` BEFORE inspecting outcomes. Freeze protocol (splits from manifest, primary contrast C2 vs B1 on Brier, block-bootstrap >=2000 reps, multiplicity).
   - Run forward validation IMMEDIATELY with the harness from (1). Write `research_state/evaluation_summary_LIQUIDATION_FORWARD_VALIDATE_004_<ID>.md` with calibration, LOO, concentration, block-bootstrap CIs, and explicit gate assessment.

5) IF STILL BLOCKED AFTER EXHAUSTIVE (HEAVY DOCUMENTATION, NO LOOPS)
   - If after 1-3 no rubric-passing post-2026-10-31 observed-liquidation data exists, write a FRESH complete blocker evidence doc (full probe tables with URLs/status/headers) and update `research_state/experiment_frontier.json` resume condition with concrete, checkable triggers.
   - DO NOT create infinite polling loops that burn turns without new evidence. DO NOT reopen sealed FCLR-001/002/003/006/007/008/009. DO NOT change `.github/workflows/*`.

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
- tests/ (understand existing patterns)

CONSTRAINTS (NON-NEGOTIABLE):
- Unauthenticated only. No API keys, tokens, cookies, signed requests, requester-pays.
- Hyperliquid-only for Track A. Strict cross-track firewall. Never merge tracks.
- Never promote modeled boundary breaches to observed liquidations.
- Pre-register BEFORE outcome inspection on any new data.
- Do not touch `.github/workflows`.
- `python -m unittest discover -s tests -v` MUST pass (keep >=27 passing; add tests if you add modules).
- Raw data out of git. Commit ONLY code/manifests/reports.
- No retry loops without new evidence. Produce automation + evidence, not "checked again, nothing".
```

## BOTTLENECKS REMOVED (THIS HANDOFF UPDATE)
- **Eliminated passive waiting:** Replaced "sit on blocker" with a HEAVY build campaign (harness + monitor + alt-hunt). Even if data never appears this session, the repo must gain reusable validation automation.
- **Forced heavy work:** The next session CANNOT satisfy this handoff by a single HTTP GET. Steps 1-3 are required work products.
- **Discovery-driven:** Monitor is mandatory (not optional) to catch new monthly parquets the moment they appear without burning turns on aimless polling.
- **Single source of truth:** This file supersedes all prior handoffs. Only this handoff is durable.
- **Preserved seals:** All sealed artifacts intact. No reopening of closed tracks.
- **Clean execution posture:** Tests passing, firewall intact, raw data excluded from git.

## CURRENT STATUS (AUTHORITATIVE)
- **H001 (volatility): NOT_SUPPORTED** (FCLR-003) — Track C CONFIRMATORY_CLOSED
- **Track A (observed liquidations): OPEN** — FCLR-010 PASSED (Hyperliquid ironflow 2025-11..2026-10, 199 instruments, 5 blocks, C2 vs B1 Brier -2.21%, CI excludes zero). Overlay executed (hypothetical only).
- **LIQUIDATION_FORWARD_VALIDATE_HEAVY-004d: BLOCKED_ON_DATA** — No 2026-11+ ironflow parquet as of 2026-11-02T06:01:54Z. Must build harness + monitor + alt-hunt NOW.
- **Track B: CLOSED_NEGATIVE** (FCLR-H003-EXT-001). **H002: PERMANENTLY_BLOCKED** (SSRN 403). **FCLR-NEXT-002: COMPLETE_NO-GO** for new sources beyond ironflow (must re-probe with fresh evidence per step 3).
- **Sealed holds:** FCLR-001/002/003/006/007/008/009 sealed.

## NEXT FOCUS CAMPAIGN
**Campaign ID:** LIQUIDATION_FORWARD_VALIDATE_HEAVY-004d
**Priority:** CRITICAL (liquidation risk)
**Effort:** HEAVY (harness hardening + CLI + tests + ironflow monitor + exhaustive alt-source hunt + pre-reg ready)
**Trigger:** Auto-detect new post-2026-10 data via monitor OR produce complete blocker evidence if none found.
**Success Definition:**
- Reusable frozen FCLR-010 harness + CLI committed with passing unit tests (fixtures-based)
- `scripts/monitor_ironflow_liquidations.py` operational with state + timestamped evidence
- Fresh alt-source evidence table in `research_state/` (all admissible families probed with HTTP evidence)
- Either (a) pre-reg created + forward validation executed with full report, OR (b) updated complete blocker doc with explicit resume condition

## HARD RULES (NON-NEGOTIABLE)
- **Heavy or bust:** If you can finish the turn without creating/strengthening automation or tests, you haven't followed this handoff.
- **Pre-register before outcomes:** Any inspection of new forward data requires a pre-reg file created BEFORE reading label/outcome columns.
- **Firewalls:** Hyperliquid-only for Track A. No track merging. Never conflate modeled with observed.
- **Admissible only:** Unauthenticated sources only. No keys/paid/requester-pays.
- **Preserve history:** No `.github/workflows` changes. Don't revert sealed artifacts.
- **Keep tests green:** `python -m unittest discover -s tests -v` must pass.
- **Git hygiene:** Raw data out of git. Commit only code/manifests/reports.
- **No busywork loops:** Evidence over retries. If blocked after exhaustive proof, document completely and build on the harness/monitor.
