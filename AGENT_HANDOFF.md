# AGENT HANDOFF — Funding-Conditioned Volatility and Liquidation Risk

UPDATED: 2026-10-30T13:56:38Z
HEAD: 1f595d2a (main) — working tree: AGENT_HANDOFF.md refreshed; liquidation_sources_enumeration.md duplicate FCLR-005 records collapsed; __pycache__ untracked
REPO: Funding-conditioned-volatility-and-liquidation-risk
DURABLE_HANDOFF: SINGLE_SOURCE_OF_TRUTH
SESSION_GOAL: PROGRAM CLOSED NEGATIVE — FCLR-006 COMPLETE (NEGATIVE); ALL CLOSEOUT RECORDS RECONCILED; FINAL VERIFICATION PASSED; NO FURTHER CONFIRMATORY PATH ON EXISTING ADMISSIBLE DATA

## INITIAL TASK MESSAGE (TIMESTAMPED 2026-10-30T13:56:38Z) — MANDATORY FOR NEXT AGENTIC WORK SESSION

**PRIORITY: REPORT PROGRAM CLOSEOUT NEGATIVE — H001 NOT_SUPPORTED ON ALL CONFIRMATORY PATHS; NO FURTHER CONFIRMATORY WORK FEASIBLE ON EXISTING ADMISSIBLE DATA**

### GROUND TRUTH (DECISIVE)
- **FCLR-003 (2024-10-02..2024-12-31):** SEALED NEGATIVE. C2 vs B1: +0.015205 QLIKE (worse), -3.78% rel, CI [-0.020240, 0.056734] crosses 0. 91 days = 3 blocks, 5 instruments, n=10796. **FCLR-H001: NOT_SUPPORTED.** Risk-overlay INELIGIBLE. Canonical: research_state/evaluation_summary_FCLR003.md
- **FCLR-006 (unsealed 2026-05-23..2026-08-06):** COMPLETE NEGATIVE, byte-identical reproduction confirmed (Generated timestamp only differs). C2 vs B1: +0.368588 QLIKE (significantly WORSE), CI [0.173748, 0.615614] entirely positive, -69.90% rel. n=8987 paired, 5 instruments. Test window 76 days = 2 blocks < 3 required -> block criterion NOT_MET. Gate NOT_MET. Canonical: research_state/evaluation_summary_FCLR006.md (Generated 2026-10-30T13:55:23Z). Steps 1-4 complete.
- **H002 (Funding-correction replication):** PARTIAL_REPLICATION final; SSRN HTTP 403 blocks full methodology — structural impossibility. 88 events Jan-Mar 2024, median 8.0h. Do not promote. Canonical: research_state/h002_replication_blocker.md
- **H003 (Modeled boundary-breach):** INCONCLUSIVE on both panels; no incremental skill.
- **Track A (observed liquidations):** BLOCKED/exhausted after >=2 materially distinct source families. No confirmatory-feasible window.
- All 14 tests pass (`python -m unittest discover -s tests -v`).

### STALE RECORDS RECONCILED (BOTTLENECKS REMOVED)
- experiment_frontier.json rank 6: FCLR-006 status COMPLETE; result recorded; gate NOT_MET / H001 NOT_SUPPORTED (unsealed 2026 confirmation). DONE.
- AGENT_HANDOFF.md obsolete instruction to re-run FCLR-006 Step 1 removed; Steps 1-4 complete (coverage audit 12:52:01Z, protocol frozen 13:45:00Z, evaluation run 13:47:31Z, byte-identical repro verified 13:55:23Z).
- final_confirmatory_verdict.md data-exhaustion claim (FCLR-FINAL-001, 10:46:44Z) RETRACTED 2026-10-30T12:34:23Z per hypothesis_registry.json closeout; 2026 Apr-Jul holds all 5 symbols unsealed and was exhausted by FCLR-006. Not current on data-exhaustion.
- research_state/liquidation_sources_enumeration.md duplicate FCLR-005 execution records collapsed to one (was appended 5x identically). DONE.

### EXECUTION PLAN — ALL STEPS COMPLETE
- STEP 1 MARK FCLR-006 COMPLETE: DONE (experiment_frontier.json rank 6 COMPLETE).
- STEP 2 DOCUMENT H002 STRUCTURAL IMPOSSIBILITY: DONE (research_state/h002_replication_blocker.md).
- STEP 3 FINAL TRACK A VERDICT: DONE (BLOCKED; >=2 source families exhausted; research_state/binance_source_probe.md; liquidation_sources_enumeration.md).
- STEP 4 FINAL VERIFICATION: PASSED (14 tests OK; FCLR_EXPERIMENT=FCLR-006 byte-identical repro, only Generated timestamp differs; HEAD 1f595d2a).

### NEXT SESSION DIRECTIVE
The confirmatory program is closed negative: H001 NOT_SUPPORTED on both the powered 2024-12 panel (FCLR-003) and unsealed 2026 data (FCLR-006); overlay INELIGIBLE; Track A BLOCKED; H002 PARTIAL (structural); H003 INCONCLUSIVE. Do not re-run sealed FCLR-001/002/003/005/006 holds; do not threshold-shop; no seal violations.
Only new route: a new unauthenticated admissible liquidation/price source with confirmatory-feasible coverage (>=5 symbols, >=3 non-overlapping 30-day blocks). If such a source appears, pre-register a new experiment ID BEFORE examining outcomes (RESEARCH_PROMPT.md §16), then execute the frozen protocol. Otherwise report the program as closed with H001 NOT_SUPPORTED and no further confirmatory path on current data.
Do heavy working: close records honestly; preserve negative results; do not manufacture a positive path.

### HARD CONSTRAINTS
- No seal violations; no tuning on sealed holds; no threshold shopping.
- No `.github/workflows/*` changes without explicit maintainer authorization.
- No fabrication; distinguish modeled (H003) vs observed (H004).
- Preserve negative results; H001 NOT_SUPPORTED is the correct scientific outcome.
- No further confirmatory experiment feasible without a NEW admissible data source (RESEARCH_PROMPT.md §16).

### VERIFICATION COMMANDS
```bash
python -m unittest discover -s tests -v
FCLR_EXPERIMENT=FCLR-006 python scripts/run_evaluation.py
git log --oneline -2
```

### NEXT AGENT DIRECTIVE
Confirm program closeout status (all closeout steps done, verification passed). If no new admissible data source appears, report the program as closed with H001 NOT_SUPPORTED and no further confirmatory path on current data. Produce: updated AGENT_HANDOFF.md closeout status. Do not repeat completed experiments.
