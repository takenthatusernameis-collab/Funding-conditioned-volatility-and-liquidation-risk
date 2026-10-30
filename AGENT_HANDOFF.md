# AGENT HANDOFF — Funding-Conditioned Volatility and Liquidation Risk

UPDATED: 2026-10-30T12:46:14Z
HEAD: 20671b69 (main) — clean working tree (ignore __pycache__)
REPO: Funding-conditioned-volatility-and-liquidation-risk
DURABLE_HANDOFF: SINGLE_SOURCE_OF_TRUTH
SESSION_GOAL: EXECUTE FCLR-006 ON UNSEALED 2026 DATA — NO SEAL VIOLATIONS

## INITIAL TASK MESSAGE (TIMESTAMPED) — MANDATORY FOR NEXT AGENTIC WORK SESSION

**PRIORITY: CAMPAIGN FCLR-006 — CONFIRMATORY VOLATILITY FORECAST ON UNSEALED 2026 DATA (NO SEAL VIOLATIONS)**

### GROUND TRUTH (DECISIVE)
- **FCLR-003 (2024-10-02..2024-12-31):** COMPLETE & NEGATIVE. C2 vs B1: +0.015205 QLIKE (worse), -3.78% rel, CI crosses 0. **FCLR-H001: NOT_SUPPORTED.** Risk-overlay INELIGIBLE.
- **FCLR-002 (2024-07-23..2024-09-30):** Underpowered (<3 blocks), SEALED, INCONCLUSIVE.
- **FCLR-001 (2024 Q1):** Coverage defect, BTCUSDT-only effectively, SEALED, INCONCLUSIVE.
- **H002:** PARTIAL_REPLICATION (SSRN 403). 88 events Jan-Mar 2024, median 8.0h. Full replication blocked by methodology access.
- **H003:** INCONCLUSIVE on both panels; no incremental skill.
- **Track A (liquidations):** BLOCKED after exhaustive probes (Binance/Bybit/OKX/Deribit/HF/GitHub). HF ochinimus/crypto-liquidation-ticks only 2026 ~30-day window (FCLR-005 exploratory, no skill, <3 blocks).

### BOTTLENECK REMOVAL (COMPLETED)
**Data exhaustion claims were FALSE.** Verified 2026-10-30T12:40:17Z in `research_state/data_cache/`:
- **2026 Apr-Jul:** ALL 5 symbols (BTCUSDT, ETHUSDT, BNBUSDT, SOLUSDT, XRPUSDT) have `markPriceKlines/`, `indexPriceKlines/`, `fundingRate/` coverage.
- **Common timestamps:** ~122 common UTC hourly days across all 5 symbols = **>=4 non-overlapping 30-day blocks** (> required >=3).
- **Unsealed:** Not used in FCLR-001/002/003 or FCLR-005.
- `hypothesis_registry.json` and `experiment_frontier.json` corrected to reflect unsealed 2026 window and FCLR-006 added.

### EXECUTION PLAN (DO IN THIS EXACT ORDER — NO SHORTCUTS)

#### STEP 1: COVERAGE-ONLY AUDIT (NO OUTCOME INSPECTION) — START HERE
- **Goal:** Audit coverage for BTCUSDT, ETHUSDT, BNBUSDT, SOLUSDT, XRPUSDT for 2026-04-01 through 2026-07-31.
- **Actions:**
  1. Inventory `markPriceKlines`, `indexPriceKlines`, `fundingRate` files per symbol-month.
  2. Compute common UTC hourly timestamps across all 5 symbols (require >=5 instruments, >=90 common days).
  3. Identify contiguous gaps, delisted/symbol-reuse, or schema anomalies. Quarantine suspicious rows with provenance. Do NOT guess repairs.
  4. Propose chronological splits (60/20/20) with 7-day purge/embargo boundaries based purely on coverage.
- **Output:** `research_state/fclr006_coverage_audit.md` with exact counts, common timestamp total, proposed frozen splits, file hashes.
- **Constraint:** Do NOT look at QLIKE, model performance, or any outcome metrics.

#### STEP 2: PRE-REGISTER FCLR-006 PROTOCOL (BEFORE OUTCOMES)
- **Goal:** Freeze protocol before computing any results.
- **Actions:**
  1. Create `research_state/research_protocol_fclr006.md` v1.0 copying FCLR-001 design.
  2. Specify: unit = contract x UTC hour; target = next-24h realized variance of mark-price log returns (sum of squared log returns t+1..t+24); predictors RV1h/RV24h/RV168h + signed funding + 90-day abs-funding percentile + mark/index premium + mark/EMA24 distance.
  3. Models: B0 (persistence), B1 (RV-only HAR), C1 (funding-augmented), C2 (combined). Primary contrast C2 vs B1 on QLIKE.
  4. Frozen: chronological splits, >=2% relative QLIKE materiality floor, Holm multiplicity, block bootstrap 2000 replicates, >=5 instruments, >=3 non-overlapping 30-day blocks.
  5. Record git SHA, config hash, source file hashes.
- **Output:** Frozen protocol file. No evaluation until this exists.

#### STEP 3: BUILD/RUN EVALUATION
- **Goal:** Execute evaluation on frozen splits.
- **Actions:**
  1. Use `scripts/run_evaluation.py` with `FCLR_EXPERIMENT=FCLR-006` (idempotent, checkpointed).
  2. Verify ingestion handles 2026 schema (same as 2024).
  3. Run full evaluation with 2000 bootstrap replicates.
- **Output:** `research_state/evaluation_summary_FCLR006.md`, gate assessment, updated manifest.

#### STEP 4: RECORD, VERIFY, REPRODUCE
- **Goal:** Seal results with verification.
- **Actions:**
  1. Update `research_state/hypothesis_registry.json` with FCLR-H001 status on FCLR-006 (seal after outcomes).
  2. Update `research_state/experiment_frontier.json`.
  3. Run `python -m unittest discover -s tests -v` (must pass all 14 tests).
  4. Reproduce: `FCLR_EXPERIMENT=FCLR-006 python scripts/run_evaluation.py` and confirm byte-identical numbers.
- **Output:** Updated handoff status below.

### SECONDARY WORK (ONLY AFTER FCLR-006 OR IF BLOCKED)
- **H002:** Attempt alternative SSRN mirrors (arXiv, author institutional pages). Document structural impossibility if all fail.
- **H003 extensions:** Require fresh pre-registration on unsealed 2026 data if pursued.
- **Track A:** Remain BLOCKED. No new admissible liquidation source exists.

### HARD CONSTRAINTS
- **NO SEAL VIOLATIONS:** Never tune on sealed FCLR-002/003/005 holds.
- **COVERAGE-ONLY FIRST:** Step 1 has zero outcome inspection.
- **PRE-REGISTER BEFORE OUTCOMES:** Protocol must be frozen before any QLIKE computed.
- **NO FABRICATION:** No invented liquidation labels; distinguish modeled (H003) vs observed (H004).
- **NO WORKFLOW CHANGES:** No `.github/workflows/*` changes without explicit authorization.
- **EVIDENCE-BASED:** Document blockers if unreachable; no guessing.

### VERIFICATION COMMANDS
```bash
python -m unittest discover -s tests -v
git log --oneline -2
ls research_state/data_cache/BTCUSDT_2026_04/markPriceKlines-* | wc -l  # expect 30
ls research_state/data_cache/ETHUSDT_2026_07/markPriceKlines-* | wc -l  # spot check
```

### NEXT AGENT DIRECTIVE
**START IMMEDIATELY WITH STEP 1.** Do not explore unrelated files, do not re-probe dead liquidation endpoints, do not rationalize data exhaustion. Run the coverage-only audit on 2026 Apr-Jul for all 5 symbols. Produce `research_state/fclr006_coverage_audit.md` with exact common-timestamp count and proposed frozen splits. If >=5 symbols and >=90 common days confirmed, proceed to Step 2. This is the only unblocked confirmatory path forward. Heavy execution required.
