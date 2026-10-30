# AGENT HANDOFF — Funding-Conditioned Volatility and Liquidation Risk

UPDATED: 2026-10-30T12:50:00Z
HEAD: 20671b69 (main) — clean working tree (ignore __pycache__)
REPO: Funding-conditioned-volatility-and-liquidation-risk
DURABLE_HANDOFF: SINGLE_SOURCE_OF_TRUTH
SESSION_GOAL: EXECUTE FCLR-006 ON UNSEALED 2026 DATA — NO SEAL VIOLATIONS

## INITIAL TASK MESSAGE (TIMESTAMPED) — MANDATORY FOR NEXT AGENTIC WORK SESSION

**PRIORITY: CAMPAIGN FCLR-006 — CONFIRMATORY VOLATILITY FORECAST ON UNSEALED 2026 DATA (HEAVY EXECUTION REQUIRED)**

### GROUND TRUTH (DECISIVE)
- **FCLR-003 (2024-10-02..2024-12-31):** COMPLETE & NEGATIVE. C2 vs B1: +0.015205 QLIKE (worse), -3.78% rel, CI crosses 0. **FCLR-H001: NOT_SUPPORTED.** Risk-overlay INELIGIBLE.
- **FCLR-002 (2024-07-23..2024-09-30):** Underpowered (<3 blocks), SEALED, INCONCLUSIVE.
- **FCLR-001 (2024 Q1):** Coverage defect, BTCUSDT-only effectively, SEALED, INCONCLUSIVE.
- **H002 (Funding-correction replication):** PARTIAL_REPLICATION (SSRN 7529458). 88 events Jan-Mar 2024, median 8.0h. Full replication blocked by methodology access — document structural impossibility if no alternative source found.
- **H003 (Modeled boundary-breach):** INCONCLUSIVE on both panels; no incremental skill. Never conflate with observed liquidations.
- **Track A (observed liquidations):** BLOCKED after exhaustive probes (Binance/Bybit/OKX/Deribit/HF/GitHub). No admissible unauthenticated liquidation labels found. Remain BLOCKED — do not fabricate.

### BOTTLENECK REMOVAL (COMPLETED)
**"Data exhaustion" is FALSE.** Verified 2026-10-30T12:40:17Z in `research_state/data_cache/`:
- **2026 Apr–Jul:** ALL 5 symbols (BTCUSDT, ETHUSDT, BNBUSDT, SOLUSDT, XRPUSDT) have `markPriceKlines/`, `indexPriceKlines/`, `fundingRate/` coverage.
- **Unsealed:** Not used in FCLR-001/002/003 or FCLR-005. This is the only unblocked confirmatory window.
- **Sufficient size:** ~122 common UTC hourly days across all 5 symbols = **>=4 non-overlapping 30-day blocks** (> required >=3).
- `hypothesis_registry.json` and `experiment_frontier.json` already reflect FCLR-006 on unsealed data.

### EXECUTION PLAN (DO IN THIS EXACT ORDER — NO SHORTCUTS)

#### STEP 1: COVERAGE-ONLY AUDIT (NO OUTCOME INSPECTION) — START HERE
- **Goal:** Audit coverage for BTCUSDT, ETHUSDT, BNBUSDT, SOLUSDT, XRPUSDT for 2026-04-01 through 2026-07-31 with ZERO look at QLIKE/model performance.
- **Actions:**
  1. Inventory `markPriceKlines`, `indexPriceKlines`, `fundingRate` files per symbol-month.
  2. Compute common UTC hourly timestamps across all 5 symbols (require >=5 instruments, >=90 common days).
  3. Identify contiguous gaps, delisted/symbol-reuse, or schema anomalies. Quarantine suspicious rows with provenance. Do NOT guess repairs.
  4. Propose chronological splits (60/20/20) with 7-day purge/embargo boundaries based purely on coverage.
- **Output:** `research_state/fclr006_coverage_audit.md` with exact counts, common timestamp total, proposed frozen splits, file hashes per source set.
- **Constraint:** COVERAGE-ONLY. No evaluation metrics.

#### STEP 2: PRE-REGISTER FCLR-006 PROTOCOL (BEFORE OUTCOMES)
- **Goal:** Freeze protocol before computing any results.
- **Actions:**
  1. Create `research_state/research_protocol_fclr006.md` v1.0 copying the FCLR-001 design.
  2. Specify: unit = contract x UTC hour; target = next-24h realized variance of mark-price log returns (sum of squared log returns t+1..t+24); predictors RV1h/RV24h/RV168h + signed funding + 90-day abs-funding percentile + mark/index premium + mark/EMA24 distance.
  3. Models: B0 (persistence), B1 (RV-only HAR), C1 (funding-augmented), C2 (combined). Primary contrast C2 vs B1 on QLIKE.
  4. Freeze: chronological splits, >=2% relative QLIKE materiality floor, Holm multiplicity, block bootstrap 2000 replicates, >=5 instruments, >=3 non-overlapping 30-day blocks.
  5. Record git SHA, config hash, and source file hashes.
- **Output:** Frozen protocol. Do NOT run evaluation until this file exists.

#### STEP 3: BUILD/RUN EVALUATION
- **Goal:** Execute evaluation on frozen splits.
- **Actions:**
  1. Use `scripts/run_evaluation.py` with `FCLR_EXPERIMENT=FCLR-006` (idempotent, checkpointed).
  2. Verify ingestion handles 2026 schema (same as 2024). If schema differs, adapt minimally with provenance notes.
  3. Run full evaluation with 2000 bootstrap replicates.
- **Output:** `research_state/evaluation_summary_FCLR006.md`, gate assessment, updated `research_state/run_manifest.json`.

#### STEP 4: RECORD, VERIFY, REPRODUCE
- **Goal:** Seal results with verification.
- **Actions:**
  1. Update `research_state/hypothesis_registry.json` with FCLR-H001 status on FCLR-006 (seal after outcomes).
  2. Update `research_state/experiment_frontier.json`.
  3. Run `python -m unittest discover -s tests -v` (must pass all tests).
  4. Reproduce: `FCLR_EXPERIMENT=FCLR-006 python scripts/run_evaluation.py` and confirm byte-identical numbers.
- **Output:** Update this handoff with final status and next action.

### SECONDARY WORK (ONLY AFTER FCLR-006 OR IF BLOCKED)
- **H002:** Attempt alternative SSRN mirrors (arXiv, author institutional pages). If all fail, write `research_state/h002_replication_blocker.md` stating structural impossibility with evidence.
- **H003:** Only consider if FCLR-006 passes AND new unsealed data becomes available with pre-registration.
- **Track A:** Remain BLOCKED. No new admissible liquidation source exists. Do not hunt dead endpoints endlessly.

### HARD CONSTRAINTS
- **NO SEAL VIOLATIONS:** Never tune on sealed FCLR-002/003/005 holds.
- **COVERAGE-ONLY FIRST:** Step 1 has zero outcome inspection.
- **PRE-REGISTER BEFORE OUTCOMES:** Protocol must be frozen before any QLIKE computed.
- **NO FABRICATION:** No invented liquidation labels; distinguish modeled (H003) vs observed (H004).
- **NO WORKFLOW CHANGES:** No `.github/workflows/*` changes without explicit maintainer authorization.
- **EVIDENCE-BASED:** If blocked, document evidence and next materially different route. No guessing.
- **HEAVY WORK:** This campaign must produce measurable research output. Avoid status-only files, wrappers, or polling loops.

### VERIFICATION COMMANDS
```bash
python -m unittest discover -s tests -v
git log --oneline -2
ls research_state/data_cache/BTCUSDT_2026_04/markPriceKlines-* | wc -l  # expect ~30
ls research_state/data_cache/ETHUSDT_2026_07/markPriceKlines-* | wc -l  # spot check
ls research_state/data_cache/BNBUSDT_2026_05/fundingRate-* | wc -l
```

### NEXT AGENT DIRECTIVE
**START IMMEDIATELY WITH STEP 1.** Do not explore unrelated files, do not re-probe dead liquidation endpoints, do not rationalize data exhaustion. Run the coverage-only audit on 2026-04-01..2026-07-31 for all 5 symbols. Produce `research_state/fclr006_coverage_audit.md` with exact common-timestamp count and proposed frozen splits. If >=5 symbols and >=90 common days confirmed, proceed to Step 2. If coverage is sufficient, execute all steps through reproduction. This is the only unblocked confirmatory path forward — do heavy working.
