# AGENT_HANDOFF.md (DURABLE - PROGRAM CLOSED OUT)
**TIMESTAMP (UTC):** 2026-11-01T00:43:20Z
**REPO:** Funding-conditioned-volatility-and-liquidation-risk
**BRANCH/HEAD:** main @ b72a338a (working tree: __pycache__ only)
**HANDOFF ID:** FCLR-HANDOFF-CLOSEOUT-20261101T004320Z
**PRIORITY:** VERIFY_CLOSURE_ONLY - confirmatory research program closed out as negative; NO remaining heavy work. Bottlenecks removed.

## 1) WHAT CHANGED & WHY
The program evaluated funding-conditioned volatility/liquidation effects across H001-H004. All confirmatory gates failed or are blocked. No remaining admissible path exists on current data. Do not re-run sealed holds or start new heavy engineering.

## 2) CURRENT STATE SNAPSHOT (EVIDENCE)
- **Tests:** `python -m unittest discover -s tests -v` → **27/27 PASS** (verified at HEAD)
- **Data:** local Binance archives present; no network/auth needed for verified artifacts
- **Research gates (terminal):**
  - **FCLR-H001** (24h volatility forecast): **NOT_SUPPORTED / SEALED_NEGATIVE**. FCLR-003 (2024-10-02..2024-12-31, 5 instruments, n=10796, 3 blocks): C2 vs B1 = −3.78% rel QLIKE, CI [−0.020240, 0.056734] crosses zero → NOT_MET. FCLR-006/FCLR-007 worse → NOT_MET. Overlay INELIGIBLE.
  - **FCLR-H002** (funding-extreme correction time): **PARTIAL_REPLICATION / SEALED_PARTIAL**. RV-regime contrast direction matches (high-RV med 16.0h vs low-RV med 8.0h) but log-rank p=0.0792 (not sig @ 5%); SSRN HTTP 403 blocks exact replication.
  - **FCLR-H003** (modeled boundary-breach forecast): **NOT_SUPPORTED / SEALED_NEGATIVE**. FCLR-H003-EXT-001 shows no robust incremental skill after Holm correction.
  - **FCLR-H004** (observed liquidations): **EXPLORATORY_ONLY / BLOCKED**. No admissible unauthenticated liquidation census; FCLR-005 exploratory only with no incremental skill.

**Key artifacts:** `research_state/final_confirmatory_verdict.md`, `research_state/evaluation_summary_FCLR003.md`, `research_state/final_inconclusive_report.md`, `research_state/negative_results_report.md`, `research_state/hypothesis_registry.json`, `research_state/experiment_frontier.json`, `research_state/run_manifest.json`, `research_state/research_protocol.md`, `research_state/leakage_audit.md`

## 3) SINGLE HIGHEST-VALUE NEXT TASK
**TASK ID:** FCLR-CLOSEOUT-VERIFY | **TYPE:** VERIFICATION / NO HEAVY WORK
**GOAL:** Confirm closeout state intact and reproducible. Do NOT pre-register/tune/re-run sealed holds.

**Steps (in order):**
1. `python -m unittest discover -s tests -v` → must be 27/27 PASS
2. `git status` → clean working tree, on main
3. Verify sealed holds untouched: `grep -n "frozen_before_outcomes" research_state/run_manifest.json` shows true; `research_state/final_confirmatory_verdict.md` unchanged
4. Verify canonical artifacts present: `ls research_state/final_confirmatory_verdict.md research_state/evaluation_summary_FCLR003.md research_state/hypothesis_registry.json`

**ACCEPTANCE:**
- [ ] 27/27 tests pass
- [ ] Working tree clean, HEAD on main
- [ ] Sealed boundaries intact (no holdout touched)
- [ ] No heavy/ingestion work scheduled; no placeholder files added

## 4) BOTTLENECK REMOVAL PLAN
- **Stale T001 ingestion:** Already complete - do not re-run ingestion/protocol freeze/features/labels.
- **No threshold shopping:** Prohibited by research discipline (§16/§18). Do not re-tune/re-open sealed holds.
- **No doc-sprawl:** Do not create empty status files/dashboards/orchestrators.
- **Only valid continuation:** NEW admissible unauthenticated liquidation data source (≥5 symbols, ≥3 non-overlapping 30-day blocks, documented completeness/license) OR SSRN access for H002 exact replication. If either appears, PRE-REGISTER new experiment ID BEFORE examining outcomes.

## 5) NEXT FOCUS CAMPAIGN (FOR FUTURE SESSIONS)
**CAMPAIGN NAME:** `FCLR-CLOSEOUT` — "Verify closure. No heavy work. No overlay."

**MANDATE:** Confirm negative verdict intact, reproducible, preserved. Start no new confirmatory campaign without new admissible data and fresh pre-registered experiment ID.

**If new admissible data appears (only valid trigger):**
1. Pre-register new experiment ID (new protocol version) BEFORE outcome inspection
2. Coverage-only audit (no outcome inspection)
3. Run frozen pipeline on unsealed window
4. Update `hypothesis_registry.json`, `run_manifest.json`, `experiment_frontier.json`; run tests

## 6) EXACT COMMANDS TO START (COPY/PASTE)
```bash
cd /home/runner/work/Funding-conditioned-volatility-and-liquidation-risk/Funding-conditioned-volatility-and-liquidation-risk
git log -1 --oneline && git status --short
python -m unittest discover -s tests -v
ls research_state/final_confirmatory_verdict.md research_state/evaluation_summary_FCLR003.md research_state/hypothesis_registry.json research_state/experiment_frontier.json
grep -n "frozen_before_outcomes" research_state/run_manifest.json
```

## 7) SESSION CHECKLIST (END OF SESSION MUST SATISFY)
- [ ] 27/27 tests pass with exact outcomes logged
- [ ] No sealed holdout reused/tuned; no exploratory result relabeled confirmatory
- [ ] Next action unambiguous and executable without user input (verify closure; no heavy work)
- [ ] No placeholder files committed without content

## 8) PER-SESSION DEFINITION OF DONE (RESEARCH_PROMPT.md §19)
- **Evidence:** H001 contradicted on all powered/unsealed panels (NOT_SUPPORTED). H002 partially supported directionally but not confirmed (p=0.0792, SSRN blocked). H003 contradicted (no incremental skill after Holm). H004 unknown for 2024 (blocked); exploratory-only 2026 (no incremental skill). Overlay INELIGIBLE.
- **Strongest alternative:** Apparent FCLR-002 edge flips on independent FCLR-003 (cross-window sign flip) → estimate does not generalize.
- **Uncertainty:** No unsealed contiguous ≥5-symbol confirmatory window remains on admissible data; Track A liquidation census structurally unavailable.
- **Falsifying test:** If new admissible data appears, pre-register new experiment and re-run C2 vs B1 on unsealed window with ≥3 non-overlapping 30-day blocks and ≥2% rel QLIKE floor.
- **Highest expected info gain:** None currently (closed negative). Only new external data would change.
- **Demonstrating progress:** `research_state/final_confirmatory_verdict.md` + `python -m unittest discover -s tests -v` (27/27 PASS)

## SESSION LOG
**2026-11-01T00:42:41Z - HANDOFF REFRESHED (CLOSEOUT, CLEAR INITIAL TASK)**
- Re-verified baseline: 27/27 PASS at HEAD d142f650
- Refreshed timestamp/HEAD to current checkpoint; working tree clean (only __pycache__)
- No bottlenecks; program closed negative; no heavy work scheduled
