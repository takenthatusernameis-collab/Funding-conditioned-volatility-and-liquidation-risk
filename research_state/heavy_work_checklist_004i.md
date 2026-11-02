# HEAVY-WORK CHECKLIST — CAMPAIGN LIQUIDATION_FORWARD_VALIDATE_HEAVY-004i (NEXT CAMPAIGN)

**Purpose:** Make it impossible for any future agent session to avoid heavy work. This checklist is non-skippable. A session that produces no measurable automation, tests, or evidence FAILS.

**Repo:** Funding-conditioned-volatility-and-liquidation-risk (Track A liquidation risk PRIORITIZED)
**Campaign:** LIQUIDATION_FORWARD_VALIDATE_HEAVY-004i
**Generated:** 2026-11-02T12:48:00Z
**Data state:** blocked (ironflow data_through=2026-10, consecutive_absent=3, no post-2026-10 data)

---

## MANDATORY PER-SESSION HEAVY WORK (BLOCKED PATH)

Every session while data remains blocked MUST complete ALL of the following before ending:

### 1. CHECK FOR NEW EVIDENCE (Step 1 — never skip)
- [ ] Read `research_state/ironflow_monitor_state.json` — check `last_probe`, `new_files_found`, `data_through`, `consecutive_absent`
- [ ] If `new_files_found` is non-empty for any month >= 2026-11, OR any month >= 2026-11 shows status 200 → proceed to Step 2 (NEW DATA PATH)
- [ ] Otherwise → proceed to Step 4 (BLOCKED PATH — heavy work mandatory)

### 2. NEW DATA PATH (only if >=2026-11 data appeared)
- [ ] CREATE fresh pre-registration BEFORE inspecting outcomes (`scripts/create_forward_prereg.py` or manual per `research_state/research_protocol_fclr010.md`)
- [ ] Run frozen FCLR-010 harness immediately
- [ ] Write `research_state/evaluation_summary_LIQUIDATION_FORWARD_VALIDATE_004_<YYYYMMDDTHHMMSSZ>.md` with calibration, LOO, concentration, block-bootstrap CIs (>=2000 reps), multiplicity, gate assessment
- [ ] Update `research_state/experiment_frontier.json` and commit evidence

### 3. READ LATEST EVIDENCE (only after Step 2 if new data)
- [ ] `research_state/liquidation_forward_validate_004_blocker_<latest>.md`
- [ ] `research_state/ironflow_monitor_state.json`
- [ ] `research_state/experiment_frontier.json`

### 4. BLOCKED PATH — MANDATORY HEAVY WORK (expected case — no new data)
Complete ALL four sub-items. A session that skips any sub-item FAILS.

#### 4A. STRENGTHEN AUTOMATION (cannot skip)
- [ ] Improve `scripts/monitor_ironflow_liquidations.py` (e.g. skip re-listing when tree ETag unchanged, wider/faster lookahead, smarter failure classification) AND/OR `scripts/hunt_alternative_liquidation_sources.py`
- [ ] Add retry/backoff robustness, broader unauthenticated probes, or new detection logic
- [ ] Make it faster/smarter/more exhaustive
- [ ] Evidence: modified script file + fresh probe output

#### 4B. ADD TESTS (cannot skip)
- [ ] Extend `tests/test_monitor_ironflow.py` or add new tests covering state-diff, ETag caching, month-window, classification
- [ ] All must pass: `python -m unittest discover -s tests -v`
- [ ] Evidence: new test methods + green test run

#### 4C. UPDATE BLOCKER DOC (cannot skip)
- [ ] Write `research_state/liquidation_forward_validate_004_blocker_<new_timestamp>.md` with:
  - Complete probe tables (all URLs tried, status codes, headers, body previews)
  - Explicit checkable resume conditions (exact paths/patterns/URLs/months to watch)
  - Concrete timestamps
- [ ] Evidence: new blocker doc file

#### 4D. UPDATE FRONTIER (cannot skip)
- [ ] Update `research_state/experiment_frontier.json` with precise resume triggers and refreshed blocked-cell status
- [ ] Evidence: modified frontier JSON

---

## NON-SKIPPABLE HEAVY-WORK CHECKLIST (must complete before any session ends)

This checklist must be checked off in AGENT_HANDOFF.md at session end. Unchecked = session FAILED.

- [ ] New evidence checked (ironflow_monitor_state.json read, new_files_found evaluated)
- [ ] Automation strengthened (monitor and/or hunt script improved)
- [ ] Tests added/extended (all pass: `python -m unittest discover -s tests -v`)
- [ ] Blocker doc updated (fresh timestamp, complete probe tables, resume conditions)
- [ ] Frontier updated (precise resume triggers, refreshed blocked-cell status)
- [ ] AGENT_HANDOFF.md updated with clear timestamped next task
- [ ] No sealed artifacts touched; no Track B/C conflation; no .github/workflows changes
- [ ] Raw data out of git; only code/manifests/reports committed

---

## NEXT CAMPAIGN: FORWARD VALIDATION HOOKS

When data becomes unblocked (resume trigger met), the next session MUST:

1. **Pre-register BEFORE outcome inspection:** Create `research_state/experiment_prereg_LIQUIDATION_FORWARD_VALIDATE_004_<timestamp>.json` with `pre_registered_before_outcomes: true`, `frozen_before_outcomes: true`, protocol ref `research_state/research_protocol_fclr010.md v1.0`, harness `scripts/fclr010_harness.py`, primary contrast C2_vs_B1, primary metric brier, bootstrap_reps 2000, rubric GO criteria.

2. **Execute frozen harness:** Run `scripts/fclr010_harness.py` on the new post-2026-10-31 data. Do NOT inspect outcomes before pre-registration exists.

3. **Write evaluation summary:** `research_state/evaluation_summary_LIQUIDATION_FORWARD_VALIDATE_004_<timestamp>.md` with:
   - Calibration (Brier score, reliability)
   - LOO (leave-one-out) stability
   - Concentration (leave-one-instrument-out)
   - Block-bootstrap CIs (>=2000 reps)
   - Multiplicity correction (Holm across registered family)
   - Gate assessment (pass/fail vs FCLR-010 gate criteria)

4. **Update frontier:** `research_state/experiment_frontier.json` with result status.

5. **Commit evidence:** All artifacts committed to git (code, manifests, reports — NOT raw data).

---

## BOTTLENECKS REMOVED (do not re-introduce)
- Monitor hardened (state-aware diff, wider window, failure classification, ETag caching, data_through/consecutive_absent tracking)
- Alt-hunt exhaustive (12 source families, rubric-scored, retry/backoff)
- Retry-loop guard: monitor/alt-hunt already ran at 20261102T115745Z; re-running without new evidence is forbidden
- Complete blocker evidence exists
- All confirmatory tracks at stable closeout; no session should spin on closed gates

---

## RESUME CONDITION (concrete, checkable — THE ONLY WAY TO UNBLOCK)
Ironflow publishes `data/events/YYYY-MM.parquet` and/or `data/fills/YYYY-MM.parquet` for any month >= 2026-11 with HTTP 200 on unauthenticated GET (verify via `scripts/monitor_ironflow_liquidations.py` — state-aware; reports genuinely new files), OR a NEW admissible unauthenticated source passes strict GO rubric (>=5 symbols, >=1 complete month OR >=3 non-overlapping 30-day blocks, documented completeness/coverage, permissive license, unauthenticated access no keys/signed/requester-pays, schema compatible with frozen FCLR-010). Hyperliquid-only for Track A.

---

**Next agent:** Check `research_state/ironflow_monitor_state.json` for new evidence. If none (expected), execute MANDATORY HEAVY WORK in full (4A-4D) + non-skippable checklist. Never avoid heavy working.
