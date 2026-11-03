# AGENT_HANDOFF.md (SINGLE DURABLE HANDOFF)
Timestamp (UTC): 2026-11-03T13:12:49Z
Git SHA (HEAD): 7436addd
Branch: main
Repo: Funding-conditioned-volatility-and-liquidation-risk
Handoff ID: FCLR-HANDOFF-20261103T121155Z | Priority: HEAVY-WORK (do not do status-only) | Mode: EXECUTION-ONLY-IF-DATA-ELSE-BLOCKER

## 0) MANDATORY INITIAL MESSAGE FOR NEXT AGENT (copy/paste as first action)
```
TASK ID: FCLR-NEXT-012-EXEC
PRIORITY: P0 - EXECUTION PHASE (heavy work enforced)
CAMPAIGN: CONSOLIDATE-TRACKA-AND-FUNDING-INCREMENTAL
OBJECTIVE: Execute forward validation ONLY if new admissible data exists for Track A (Hyperliquid ironflow monthly parquet > 2026-10-31) or funding-conditioned volatility (new unsealed 2026 Binance panel beyond sealed FCLR-011 window 2026-05-08..2026-08-06).
HARD RULES: Pre-register BEFORE inspecting outcomes. Freeze splits/metrics/gates. Enforce embargoes (>=7d). Block-bootstrap (>=2000 reps). No tuning. Separate experiments. NEVER reuse sealed holdouts. IMMUTABLE cross-track firewall (no Binance<->Hyperliquid merge). Overlay HYPOTHETICAL_ONLY. Do not relax thresholds. No status-only files. No polling loops.
ACTION:
1) Run verification: tests/test_fclr010_harness.py (must be green), frontier contains FCLR-012, consolidated/synthesis files present, no NEXT_AGENT_HANDOFF_*.md duplicates exist.
2) Scan for new admissible unauthenticated data: new Hyperliquid ironflow monthly parquet > 2026-10-31 (Track A); new unsealed 2026 Binance 1h/funding/index/mark/premium panel beyond 2026-08-06 for BNBUSDT/BTCUSDT/ETHUSDT/SOLUSDT/XRPUSDT (Track V).
3) IF new data found: pre-register a FRESH experiment ID via scripts/fclr010_harness.py pre_register_forward_experiment() BEFORE any outcome inspection; run evaluate_forward() with frozen config only; write results to research_state/ with cross-links to manifest/frontier.
4) IF NO new data: write a concrete BLOCKER report (data gaps, exact paths checked, last timestamps, why insufficient, next unauthenticated discovery route) to research_state/blockers_FCLR-012_<YYYYMMDDTHHMMSSZ>.md. DO NOT re-run sealed panels, DO NOT relax gates, DO NOT tune, DO NOT merge tracks, DO NOT fabricate status files. Then STOP.
FAILURE CONDITION: any attempt to merge tracks, retune, re-backtest sealed data, or report status-only progress is a VIOLATION.
```

## 1) Bottleneck removal (ENFORCED - verified this session)
- Duplicate `NEXT_AGENT_HANDOFF_*.md` files: NONE remain (root or research_state). AGENT_HANDOFF.md is the ONLY durable handoff. Verified with glob; no competing "single durable handoffs".
- Stale `research_state/AGENT_HANDOFF.md`: retired (no longer present). No stale handoff contradicting gate state or directing re-execution of completed work.
- Blocker report `research_state/blockers_FCLR-012_20261103T120855Z.md` already written by prior session (no new admissible data found). Do not re-scan identical paths expecting different results unless a new trigger appears.
- __pycache__ files are modified in the working tree but are binary caches only; they carry no research meaning and must not be committed or treated as progress.

## 2) What was actually tested (exact outcomes)
- FCLR-010: test 2026-05-28..2026-10-31, 199 native perps, block-bootstrap ~24h blocks. C2 vs B1 Brier diff -0.003077, rel -2.21%, CI excludes 0. Gates all PASS.
- FCLR-011: test 2026-05-08..2026-08-06, 5 instruments, block-bootstrap 2000 reps. C2 vs B1 QLIKE diff -0.016458, rel -4.94%, CI [-0.032546,-0.001418]. Gates all PASS.
- tests/test_fclr010_harness.py: 4/4 PASS (green).

## 3) Evidence added / where
- research_state/track_a_fclr010_consolidated.md (FCLR-010 consolidation)
- research_state/funding_incremental_synthesis_20261103T115630Z.md (FCLR-011 synthesis)
- research_state/forward_campaign_fclr012_prereg.md (FCLR-012 pre-registration)
- research_state/run_manifest.json (experiments map FCLR-010/FCLR-011/OVERLAY-001 with cross-links)
- research_state/experiment_frontier.json (FCLR-012 entry, rank 0)
- scripts/fclr010_harness.py (hardened: pre_register_forward_experiment() writes locked prereg; evaluate_forward() BLOCKED without pre-reg, frozen config only)
- research_state/blockers_FCLR-012_20261103T120855Z.md (concrete blocker: no new admissible data)

## 4) Current state of each research gate
- Track A (FCLR-H004/FCLR-010): FORECAST_GATE_PASSED. Overlay: HYPOTHETICAL_ONLY. No live/paper trading.
- Funding-conditioned volatility (FCLR-H001/FCLR-011): FORECAST_GATE_PASSED (incremental value of funding+price features over RV-only).
- Track C (H001): NOT_SUPPORTED / CONFIRMATORY_CLOSED (all confirmatory panels exhausted: FCLR-003/006/007/008).
- Track B: CLOSED_NEGATIVE.
- H002 (funding-extreme correction replication): PERMANENT_BLOCK (SSRN HTTP 403).
- LIQMICRO-002/003: COMPLETE.
- FCLR-NEXT-012: PREREGISTERED; forward validation BLOCKED pending new admissible data.

## 5) SINGLE HIGHEST-VALUE NEXT TASK (must not avoid heavy work) — EXECUTION MANDATE
**CAMPAIGN: CONSOLIDATE-TRACKA-AND-FUNDING-INCREMENTAL (FCLR-NEXT-012) — EXECUTION PHASE.**

This agent MUST perform HEAVY WORK, not status reporting. The only admissible actions:
- FCLR-012-A (Track A liquidation risk): ONLY forward validate beyond 2026-10-31 if new monthly ironflow parquet appears (unauthenticated, admissible). Execute pre-registered forward test via scripts/fclr010_harness.py (pre-register fresh ID BEFORE inspecting outcomes, frozen config, no retuning, no overlay changes, firewall intact).
- FCLR-012-V (funding-conditioned volatility): ONLY forward test on new unsealed 2026 Binance panel beyond FCLR-011 test window (2026-05-08..2026-08-06). Only if new unsealed panel exists; otherwise NO run — do not relax thresholds, do not re-run sealed panels, do not extend sealed windows.
- IF NO NEW ADMISSIBLE DATA: MUST write concrete blocker report to research_state/blockers_FCLR-012_<YYYYMMDDTHHMMSSZ>.md documenting exact paths checked (ironflow/*, all zip/csv dirs, research_state/data_cache), last timestamps, why insufficient, and recommended next unauthenticated discovery. DO NOT create summary/status files. Preserve all gate states. DO NOT fabricate runs.

Concrete subtasks already DONE (do not repeat): consolidate, synthesize, unify handoff, harden harness, manifest hygiene, bottleneck removal (duplicate handoffs retired), heavy-work enforcement (prereg written). Remaining = execution or concrete blocker with evidence.

## 6) Precise command/check to verify
```bash
cd /home/runner/work/Funding-conditioned-volatility-and-liquidation-risk/Funding-conditioned-volatility-and-liquidation-risk
python -m pytest tests/test_fclr010_harness.py -v 2>&1 | tail -15
grep -n "FCLR-012" research_state/experiment_frontier.json 2>&1 | head -5
test -f research_state/track_a_fclr010_consolidated.md && echo "OK_consolidated"
test -f research_state/forward_campaign_fclr012_prereg.md && echo "OK_prereg"
test -f research_state/funding_incremental_synthesis_20261103T115630Z.md && echo "OK_synthesis"
ls NEXT_AGENT_HANDOFF_*.md research_state/NEXT_AGENT_HANDOFF_*.md 2>&1 | head -1  # must NOT exist (single durable handoff)
```
All must pass/be present. Do not claim success without running checks.

## 7) Blockers / next materially different free route
- No new admissible unauthenticated liquidation source beyond ironflow found (FCLR-NEXT-002 source discovery COMPLETE_NO-GO across 8 families). Track A forward only via ironflow monthly parquet > 2026-10-31.
- Overlay is hypothetical only; do not build live/paper trading.
- Cross-track firewall is IMMUTABLE - never merge Hyperliquid ironflow with Binance panels.
- Forward runs BLOCKED until new admissible data appears. Do NOT relax thresholds or re-run sealed panels.
- Bottlenecks removed: duplicate handoffs retired; consolidated bundle written; forward harness hardened; manifest cross-linked; pre-registration written.

## FORWARD CAMPAIGN (FROZEN RULES)
- Pre-register BEFORE inspecting outcomes
- Freeze splits/metrics/gates
- Enforce embargoes (>=7d)
- Block-bootstrap for uncertainty
- No tuning on holdout/test
- Separate experiments, never reuse sealed holdouts
- Firewall enforced
- No risk-overlay until/unless separate pre-registration passes gates
- Heavy work only - no status-only files

**NEXT AGENT: EXECUTE FCLR-NEXT-012 FORWARD VALIDATION ONLY IF NEW ADMISSIBLE DATA APPEARS. OTHERWISE LOG CONCRETE BLOCKER WITH EVIDENCE AND WAIT. DO NOT DEVIATE FROM FROZEN RULES.**
