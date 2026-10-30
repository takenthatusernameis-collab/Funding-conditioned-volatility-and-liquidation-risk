# AGENT HANDOFF — Funding-Conditioned Volatility and Liquidation Risk

UPDATED: 2026-10-30T13:52:00Z
HEAD: 1f595d2a (main) — clean working tree (ignore __pycache__)
REPO: Funding-conditioned-volatility-and-liquidation-risk
DURABLE_HANDOFF: SINGLE_SOURCE_OF_TRUTH
SESSION_GOAL: CLOSE OUT CONFIRMATORY PROGRAM — FCLR-006 COMPLETE (NEGATIVE); RECONCILE STALE RECORDS; DOCUMENT STRUCTURAL BLOCKERS; FINAL VERIFICATION

## INITIAL TASK MESSAGE (TIMESTAMPED) — MANDATORY FOR NEXT AGENTIC WORK SESSION

**PRIORITY: PROGRAM CLOSEOUT AND FINAL VERIFICATION — NO FURTHER CONFIRMATORY WORK FEASIBLE ON EXISTING ADMISSIBLE DATA**

### GROUND TRUTH (DECISIVE)
- **FCLR-003 (2024-10-02..2024-12-31):** SEALED NEGATIVE. C2 vs B1: +0.015205 QLIKE (worse), -3.78% rel, CI [-0.020240, 0.056734] crosses 0. 91 days = 3 blocks, 5 instruments, n=10796. **FCLR-H001: NOT_SUPPORTED.** Risk-overlay INELIGIBLE. Canonical: research_state/evaluation_summary_FCLR003.md
- **FCLR-006 (unsealed 2026-05-23..2026-08-06):** COMPLETE NEGATIVE, byte-identical reproduction confirmed. C2 vs B1: +0.368588 QLIKE (significantly WORSE), CI [0.173748, 0.615614] entirely positive, -69.90% rel. n=8987 paired, 5 instruments. Test window 76 days = 2 blocks < 3 required -> block criterion NOT_MET. Gate NOT_MET. Canonical: research_state/evaluation_summary_FCLR006.md (Generated 2026-10-30T13:47:31Z); hypothesis_registry.json closeout FCLR-FINAL-001.
- **H002 (Funding-correction replication):** PARTIAL_REPLICATION; SSRN HTTP 403 blocks full methodology — structural impossibility. 88 events Jan-Mar 2024, median 8.0h. Do not promote.
- **H003 (Modeled boundary-breach):** INCONCLUSIVE on both panels; no incremental skill.
- **Track A (observed liquidations):** BLOCKED/exhausted after >=2 materially distinct source families (Binance fapi forceOrders 451, liquidationSnapshot 404; Bybit HF census single 30-day window used by FCLR-005; Zenodo/GitHub dead ends). No confirmatory-feasible window.
- All 14 tests pass (`python -m unittest discover -s tests -v`).

### STALE RECORDS TO RECONCILE (BOTTLENECK REMOVAL)
- **experiment_frontier.json rank 6 still shows FCLR-006 status NOT_STARTED** — it is COMPLETE (results in hypothesis_registry.json, evaluation_summary_FCLR006.md, reproduction verified). Fix: mark COMPLETE, record gate NOT_MET / H001 NOT_SUPPORTED (unsealed 2026 confirmation).
- **AGENT_HANDOFF.md previously instructed re-running FCLR-006 Step 1** — obsolete; Steps 1-4 complete (coverage audit 12:52:01Z, protocol frozen 13:45:00Z, evaluation run 13:47:31Z, byte-identical repro verified).
- **final_confirmatory_verdict.md (FCLR-FINAL-001, 10:46:44Z) claims data exhaustion** — retracted 2026-10-30T12:34:23Z per hypothesis_registry.json closeout (2026 Apr-Aug holds all 5 symbols unsealed; now exhausted by FCLR-006). Do not treat as current on data-exhaustion.

### EXECUTION PLAN (DO IN THIS EXACT ORDER)

#### STEP 1: MARK FCLR-006 COMPLETE
- experiment_frontier.json rank 6: status -> COMPLETE; result: "C2 vs B1 +0.368588 QLIKE (worse), CI [0.173748, 0.615614], -69.90% rel, gate NOT_MET, block criterion NOT_MET (2 blocks < 3); H001 NOT_SUPPORTED on unsealed 2026 data; byte-identical repro verified."
- Mark Steps 1-4 complete; note coverage audit + protocol + evaluation + reproduction all done.

#### STEP 2: DOCUMENT H002 STRUCTURAL IMPOSSIBILITY
- Create research_state/h002_replication_blocker.md: SSRN 7529458 HTTP 403 blocks full methodology/event definition/censoring rules; PARTIAL_REPLICATION final (88 events Jan-Mar 2024, median 8.0h); no promotion to confirmatory/forecast-skill/liquidation evidence; no RV-regime contrast possible (no Jan-Mar 2024 mark prices in cache; downloads not permitted).

#### STEP 3: FINAL TRACK A VERDICT
- Confirm BLOCKED: >=2 materially distinct source families exhausted (Binance/Bybit/OKX/Deribit/HF/GitHub/Zenodo). Evidence: research_state/binance_source_probe.md; research_state/liquidation_sources_enumeration.md §1-4, §84-92. No new admissible liquidation source with >=3 non-overlapping 30-day blocks. If a new source appears, register a new protocol before examining outcomes (RESEARCH_PROMPT.md §16).

#### STEP 4: FINAL VERIFICATION
- `python -m unittest discover -s tests -v` — must pass all 14 tests.
- Byte-identical repro: `FCLR_EXPERIMENT=FCLR-006 python scripts/run_evaluation.py`; diff against research_state/evaluation_summary_FCLR006.md (numbers identical; only Generated timestamp may differ).
- `git log --oneline -2` — confirm HEAD 1f595d2a, clean tree.
- Update this AGENT_HANDOFF.md with final closeout status once Steps 1-4 are done.

### SECONDARY WORK
- None on existing admissible data. Only new route: a new unauthenticated liquidation/price source with confirmatory-feasible coverage (>=5 symbols, >=3 non-overlapping 30-day blocks) -> pre-register a new experiment ID before examining outcomes. Do not re-run sealed FCLR-001/002/003/005/006 holds.

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
Execute Steps 1-4 in order. The confirmatory program is closed negative: H001 NOT_SUPPORTED on both the powered 2024-12 panel and unsealed 2026 data; overlay INELIGIBLE; Track A BLOCKED; H002 PARTIAL (structural); H003 INCONCLUSIVE. Produce: updated experiment_frontier.json, new h002_replication_blocker.md, final verification evidence, and this handoff updated with closeout status. If no new admissible data source appears, report the program as closed with H001 NOT_SUPPORTED and no further confirmatory path on current data. Do heavy working — close the records honestly; do not re-run completed experiments.
