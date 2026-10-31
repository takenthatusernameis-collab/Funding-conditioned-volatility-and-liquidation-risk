# AGENT_HANDOFF.md (DURABLE — PROGRAM CLOSED OUT)
**TIMESTAMP (UTC):** 2026-10-31T23:40:18Z
**REPO:** Funding-conditioned-volatility-and-liquidation-risk
**BRANCH/HEAD:** main @ 320b342f (clean working tree)
**HANDOFF ID:** FCLR-HANDOFF-CLOSEOUT-20261031T234018Z
**PRIORITY:** NONE — confirmatory research program closed out as negative; no remaining heavy work.

## 1) WHAT CHANGED & WHY
The prior `AGENT_HANDOFF.md` prescribed a T001 ingestion/protocol-freeze campaign as the next action. That campaign is already complete: all ingestion, feature/label construction, frozen splits, leakage audits, baseline runs, and confirmatory evaluations exist in `research_state/` and `scripts/`. Following the stale T001 task would be busywork (re-building already-tested artifacts and re-running sealed holds). This handoff records the true terminal state: the confirmatory program is closed out negative across every hypothesis and track, with no remaining confirmatory path on current admissible data.

## 2) CURRENT STATE SNAPSHOT (EVIDENCE)
**Tests:** `python -m unittest discover -s tests -v` → **27/27 PASS** (verified at HEAD 320b342f). Working tree clean.
**Data:** local Binance archives present (fundingRate, klines, mark/index/premium/indexPriceKlines ZIPs for BTCUSDT/ETHUSDT/BNBUSDT/SOLUSDT/XRPUSDT, Jan–Mar 2024; extended caches in `research_state/data_cache/`). No network/auth needed for verified artifacts.

**Research gates (all terminal):**
- **FCLR-H001** (24h volatility forecast): **NOT_SUPPORTED / SEALED_NEGATIVE**. FCLR-003 powered confirmatory (2024-10-02..2024-12-31, 5 instruments, n=10796, 3 blocks): C2 vs B1 = −3.78% rel QLIKE, CI [−0.020240, 0.056734] crosses zero → gate NOT_MET. FCLR-006 & FCLR-007 (unsealed 2026 panels): C2 vs B1 significantly WORSE, gate NOT_MET. FCLR-002: INCONCLUSIVE (70 days = 2 blocks < 3). FCLR-004: BLOCKED (no unsealed ≥30-day window outside sealed holds). Forecast gate never met → risk overlay INELIGIBLE.
- **FCLR-H002** (funding-extreme correction-time replication): **PARTIAL_REPLICATION / SEALED_PARTIAL**. RV-regime contrast computed (high-RV med 16.0h vs low-RV med 8.0h, log-rank p=0.0792, direction matches paper, not significant at 5%). SSRN HTTP 403 blocks full methodology → cannot promote to exact replication.
- **FCLR-H003** (modeled boundary-breach forecast / Track B): **NOT_SUPPORTED / SEALED_NEGATIVE**. FCLR-H003-EXT-001: 16 cells, no robust incremental skill after Holm correction; intensity blocked by missing OI/volume denominators.
- **FCLR-H004** (observed liquidation outcomes / Track A): **EXPLORATORY_ONLY / BLOCKED**. No admissible unauthenticated liquidation census source (Binance liquidationSnapshot HTTP 404; fapi forceOrders HTTP 451; Bybit/OKX/Deribit no census; HF ochinimus covers only 2026-07-08..2026-08-06, exhausted by FCLR-005 pilot). FCLR-005 pilot: EXPLORATORY_ONLY (~30-day window, 0 blocks, no incremental skill of C2 over B1/B0).

**Key artifacts:** `research_state/research_protocol.md` (FCLR-001/002 frozen), `research_state/run_manifest.json`, `research_state/hypothesis_registry.json` (closeout FCLR-FINAL-001, overlay_eligible: false, data_exhaustion: false), `research_state/final_confirmatory_verdict.md` (FCLR-FINAL-001), `research_state/final_inconclusive_report.md`, `research_state/negative_results_report.md`, `research_state/gate_assessment.md`, `research_state/evaluation_summary_FCLR003.md`, `research_state/evaluation_summary_FCLR006.md`, `research_state/evaluation_summary_FCLR007.md`, `research_state/evaluation_summary_FCLR-H003-EXT-001.md`, `research_state/evaluation_summary_FCLR005.md`, `research_state/experiment_frontier.json` (frontier reconciled, all campaigns COMPLETE/CLOSED_NEGATIVE), `research_state/leakage_audit.md`, `research_state/binance_source_probe.md`, `research_state/liquidation_sources_enumeration.md`, `research_state/data_source_registry.json`.

## 3) SINGLE HIGHEST-VALUE NEXT TASK
**TASK ID:** FCLR-CLOSEOUT-VERIFY | **TYPE:** VERIFICATION / NO HEAVY WORK
**GOAL:** Confirm the program closeout state is intact and reproducible; do NOT start new heavy engineering.

**Concrete steps (execute in order):**
1. `python -m unittest discover -s tests -v` → must be 27/27 PASS.
2. `git status` → working tree clean; HEAD on main.
3. Confirm no sealed holdout was touched: `research_state/run_manifest.json` `split_boundaries_fclr003.frozen_before_outcomes: true`; `research_state/final_confirmatory_verdict.md` unchanged.
4. Confirm canonical artifacts present: `research_state/final_confirmatory_verdict.md`, `research_state/evaluation_summary_FCLR003.md`, `research_state/hypothesis_registry.json` (closeout verdict present).
5. **No new experiment:** do not pre-register, tune, or re-run any sealed FCLR-001/002/003/004/005/006/007 gate. Do not relabel exploratory/partial results as confirmatory. No risk overlay (ineligible).

**ACCEPTANCE (must hold to close the session):**
- [ ] 27/27 tests pass
- [ ] Working tree clean, HEAD on main
- [ ] `AGENT_HANDOFF.md` reflects closed-out negative state (this file)
- [ ] No heavy/ingestion work scheduled; no placeholder files added

## 4) BOTTLENECK REMOVAL PLAN
- **Remove the stale T001 ingestion campaign:** it is already complete. Do not re-run ingestion, protocol freeze, or feature/label builds.
- **No doc-sprawl:** do not create empty status files, dashboards, or orchestrators.
- **No threshold shopping:** do not re-tune or re-open sealed holds to rescue a negative result (prohibited by RESEARCH_PROMPT.md §16/§18).
- **Only valid continuation:** a NEW admissible unauthenticated liquidation data source (≥5 symbols, ≥3 non-overlapping 30-day blocks, documented completeness/license) per RESEARCH_PROMPT.md §16, or SSRN access for H002 exact replication. If either appears, pre-register a NEW experiment ID before examining outcomes; otherwise the program stays closed.

## 5) NEXT FOCUS CAMPAIGN (FOR FUTURE SESSIONS)
**CAMPAIGN NAME:** `FCLR-CLOSEOUT` — "Verify closure. No heavy work. No overlay."
**MANDATE:** Confirm the negative verdict is intact, reproducible, and preserved. Start no new confirmatory campaign without new admissible data and a fresh pre-registered experiment ID.

**If new admissible data appears (only valid trigger):**
1. Pre-register new experiment ID (new protocol version) BEFORE outcome inspection.
2. Coverage-only audit (no outcome inspection).
3. Run frozen pipeline on unsealed window.
4. Update `hypothesis_registry.json`, `run_manifest.json`, `experiment_frontier.json`; run tests.

## 6) EXACT COMMANDS TO START (COPY/PASTE)
```bash
cd /home/runner/work/Funding-conditioned-volatility-and-liquidation-risk/Funding-conditioned-volatility-and-liquidation-risk
git log -1 --oneline && git status --short
python -m unittest discover -s tests -v
ls research_state/final_confirmatory_verdict.md research_state/evaluation_summary_FCLR003.md research_state/hypothesis_registry.json
```

## 7) SESSION CHECKLIST (END OF SESSION MUST SATISFY)
- [ ] `AGENT_HANDOFF.md` updated only if state changed materially (leave as-is if closeout intact)
- [ ] 27/27 tests pass with exact outcomes logged
- [ ] No sealed holdout reused/tuned; no exploratory result relabeled confirmatory
- [ ] Next action unambiguous and executable without user input (here: verify closure; no heavy work)
- [ ] No placeholder files committed without content

## 8) PER-SESSION DEFINITION OF DONE (RESEARCH_PROMPT.md §19)
- **What the evidence supported/contradicted/left unknown:** H001 contradicted on all powered/unsealed panels (NOT_SUPPORTED). H002 partially supported directionally but not confirmed (p=0.0792, SSRN blocked). H003 contradicted (no incremental skill after Holm). H004 unknown for 2024 (Track A blocked — no source); exploratory-only on 2026 (no incremental skill). Overlay: ineligible (gate never met).
- **Strongest alternative explanation:** The apparent FCLR-002 C2-vs-B1 edge (−9.28%, CI excludes zero) flips sign on the independent FCLR-003 panel (−3.78%, CI crosses zero) — a cross-window sign flip indicating the FCLR-002 estimate does not generalize; no single window supports a gate pass.
- **Dominant uncertainty limitation:** No unsealed, contiguous ≥5-symbol confirmatory window remains on current admissible data (data exhaustion on frozen 2024 windows; Track A liquidation census structurally unavailable).
- **Concrete falsifying test:** If new admissible data appears, pre-register a new experiment and re-run C2 vs B1 on the unsealed window with ≥3 non-overlapping 30-day blocks and the ≥2% relative QLIKE floor; a pass would falsify the current NOT_SUPPORTED verdict.
- **Highest expected information gain per free compute:** None currently (program closed negative). Only new external data would change this.
- **Exact artifact/command demonstrating progress:** `research_state/final_confirmatory_verdict.md` + `python -m unittest discover -s tests -v` (27/27 PASS).

## SESSION LOG (APPEND ONLY)
**2026-10-31T23:40:18Z - HANDOFF REWRITTEN (CLOSEOUT)**
- Replaced stale T001 ingestion-task handoff with accurate terminal state.
- Recorded all hypotheses/tracks closed (NOT_SUPPORTED / PARTIAL / EXPLORATORY_BLOCKED), overlay INELIGIBLE, data exhaustion, 27/27 tests passing.
- Removed bottleneck: no heavy ingestion/protocol work remains; future sessions must not re-run sealed gates.
