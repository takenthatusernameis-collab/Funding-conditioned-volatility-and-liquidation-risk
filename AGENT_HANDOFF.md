# AGENT HANDOFF — Funding-Conditioned Volatility and Liquidation Risk

UPDATED: 2026-10-30T12:30:00Z
HEAD: c151dfad (main) — clean working tree (ignore __pycache__)
REPO: Funding-conditioned-volatility-and-liquidation-risk
DURABLE_HANDOFF: SINGLE_SOURCE_OF_TRUTH

## INITIAL TASK MESSAGE (TIMESTAMPED) — MANDATORY FOR NEXT AGENTIC WORK SESSION

**PRIORITY: CAMPAIGN FCLR-006 — CONFIRMATORY VOLATILITY FORECAST ON UNSEALED 2026 DATA (NO SEAL VIOLATIONS)**

### CURRENT GROUND TRUTH (DECISIVE)

- **FCLR-003 (confirmatory, 2024-10-02..2024-12-31):** COMPLETE & NEGATIVE. C2 vs B1: mean diff +0.015205 QLIKE, rel -3.78% (worse), 95% CI [-0.020240, 0.056734] crosses zero. **FCLR-H001: NOT_SUPPORTED.** Risk-overlay INELIGIBLE. Independently reproduced byte-identical 2026-10-28; final re-verify log /tmp/fclr003_repro.log.
- **FCLR-002 (2024-07-23..2024-09-30):** Underpowered (2 blocks < 3 required), SEALED, INCONCLUSIVE.
- **FCLR-001 (2024 Q1):** Coverage defect, BTCUSDT-only effectively, PILOT/INCONCLUSIVE, SEALED.
- **H002 (correction-time replication):** PARTIAL_REPLICATION (SSRN HTTP 403 blocks full methodology). 88 events Jan-Mar 2024, median 8.0h. RV-regime contrast impossible without Jan-Mar 2024 mark prices.
- **H003 (boundary breach):** INCONCLUSIVE on both panels; no incremental skill. Extensions untested, need pre-registration + unsealed data.
- **H004 / Track A (observed liquidations):** BLOCKED for 2024. Binance liquidationSnapshot HTTP 404, forceOrders HTTP 451. HF ochinimus/crypto-liquidation-ticks (2026 only, ~30-day window, used in FCLR-005 pilot). No admissible census with >=3 blocks found. FCLR-005 (2026 pilot): no incremental skill of C2 over B1/B0, <3 blocks, EXPLORATORY_ONLY.

### BOTTLENECK REMOVED — DATA EXHAUSTION CLAIM WAS WRONG

The hypothesis_registry and final_confirmatory_verdict claim "no unsealed >=5-symbol, >=3-block confirmatory window remains" and "2026 has no mark-price data at all." **Both claims are false.** Verified against research_state/data_cache/:

- **2026 Apr-Aug: ALL 5 symbols (BTCUSDT, ETHUSDT, BNBUSDT, SOLUSDT, XRPUSDT) have markPriceKlines (~89-141 daily files/month), indexPriceKlines (same count, for premium feature), and fundingRate zips (4-8/month).**
- BTCUSDT 2026-04: 30 markPrice days, 30 klines days, 119 indexPrice days, 4 funding zips.
- ETHUSDT/BNBUSDT/SOLUSDT/XRPUSDT 2026-04: 30 markPrice days, 89 indexPrice days, 4 funding zips each.
- BTCUSDT 2026-08: 98 markPrice days (partial Aug). Others: 17 markPrice days in Aug (partial).
- Combined Apr-Jul 2026 = ~122 days across all 5 symbols = **4 non-overlapping 30-day blocks available.** Exceeds the >=3-block minimum.
- This data is UNSEALED: not used in FCLR-001/002/003 (2024 only) or FCLR-005 (HF liquidation 2026-07-08..2026-08-06, Track A only).

**Conclusion:** A new confirmatory experiment FCLR-006 on 2026 Apr-Jul data IS feasible without any new source. The "data exhaustion" blocker is removed. Per RESEARCH_PROMPT.md §16, Track A is blocked after >=3 distinct routes; continue Track C (volatility) on available unsealed data.

### HEAVY EXECUTION PLAN — FCLR-006 (EXECUTE IN ORDER)

#### STEP 1: COVERAGE-ONLY AUDIT OF 2026 DATA (NO OUTCOME INSPECTION)
- Verify markPriceKlines, indexPriceKlines, fundingRate coverage for all 5 symbols, 2026-04..2026-07.
- Compute common UTC hourly timestamp count across all 5 symbols (target: >=5 instruments, >=90 days).
- Document any gaps/delisted/symbol-reuse issues. Quarantine suspicious rows with provenance; do not repair by guessing.
- Output: research_state/fclr006_coverage_audit.md with exact symbol-month coverage, common timestamp count, split boundaries proposed (train/val/test chronological), source file hashes.
- Constraint: Do NOT inspect QLIKE, model results, or any outcome during this audit. Coverage only.

#### STEP 2: PRE-REGISTER FCLR-006 PROTOCOL (BEFORE ANY OUTCOME INSPECTION)
- Create research_state/research_protocol_fclr006.md v1.0, frozen before outcomes.
- Copy FCLR-001 design: unit = contract x UTC hour; primary target = next-24h realized variance of mark-price returns (sum of squared log returns t+1..t+24); predictors RV1h/RV24h/RV168h + signed funding + 90-day abs-funding percentile + mark/index premium + mark/EMA24 distance; OLS log-linear; B0 persistence, B1 RV-only HAR, C1 funding-augmented, C2 combined; primary contrast C2 vs B1 on QLIKE.
- Freeze splits (chronological 60/20/20 with 7-day purge/embargo), >=2% relative QLIKE materiality floor, Holm multiplicity, block bootstrap 2000 replicates, >=5 instruments, >=3 non-overlapping 30-day blocks.
- Record source hashes, git SHA, config hash before outcome computation.

#### STEP 3: BUILD/RUN FCLR-006 EVALUATION
- Use existing scripts/run_evaluation.py with FCLR_EXPERIMENT=FCLR-006 (idempotent, checkpointed).
- Verify ingestion pipeline handles 2026 data format (same schema as 2024; confirm column/units).
- Run evaluation on frozen splits. Expected runtime: bounded (~24h blocks, 2000 bootstrap replicates).
- Output: research_state/evaluation_summary_FCLR006.md, gate assessment, manifest update.

#### STEP 4: RECORD & VERIFY
- Update hypothesis_registry.json with FCLR-H001 status on FCLR-006 (sealed after outcome).
- Update experiment_frontier.json.
- Run: `python -m unittest discover -s tests -v` (must pass, 14 tests).
- Verify reproducibility: re-run `FCLR_EXPERIMENT=FCLR-006 python scripts/run_evaluation.py` and compare byte-identical numbers.
- Update this AGENT_HANDOFF.md with campaign status and next action.

### SECONDARY WORK (AFTER FCLR-006 COMPLETE OR IF BLOCKED)
- **H002 completion:** Try alternative SSRN access routes (arXiv, author institutional page, alternative mirrors) to document full methodology. SSRN HTTP 403 remains the blocker; document structural impossibility if all routes fail.
- **H003 extensions on 2026 data:** Longer horizons (72h/168h), lower MMR tiers, event-intensity target — require fresh pre-registration before outcome inspection on unsealed 2026 data.
- **Track A:** Remains BLOCKED. No new liquidation source found after Binance/Bybit/OKX/Deribit/HF/GitHub/raw probes. Do not re-probe same dead ends.

### VERIFICATION
```bash
python -m unittest discover -s tests -v
git log --oneline -2
ls research_state/data_cache/BTCUSDT_2026_04/markPriceKlines-* | wc -l   # expect 30
```

### HARD CONSTRAINTS
- **NO SEAL VIOLATIONS:** No tuning/threshold-shopping on FCLR-002/003/005 sealed holds. FCLR-006 uses unsealed 2026 data only; pre-register BEFORE outcome inspection.
- **NO FABRICATION:** No invented liquidation labels; don't conflate modeled breaches (H003) with observed liquidations (H004).
- **NO WORKFLOW CHANGES:** No `.github/workflows/*` changes without explicit authorization.
- **PRE-REGISTER FIRST:** New experiment on unsealed data must be pre-registered before outcome inspection. FCLR-006 protocol frozen in research_state/research_protocol_fclr006.md before any QLIKE computed.
- **EVIDENCE-BASED:** If methodology unreachable (SSRN), document blockers. No guessing.
- **COVERAGE-ONLY FIRST:** Step 1 audits coverage without looking at outcomes. Split boundaries set from data coverage alone, before model results.

### NEXT AGENT DIRECTIVE
**START WITH STEP 1.** Run the coverage-only audit on 2026 Apr-Jul data for all 5 symbols. Produce research_state/fclr006_coverage_audit.md with exact common-timestamp count and proposed frozen splits. If >=5 symbols and >=90 common days confirmed, proceed to Step 2 (pre-register FCLR-006). No busywork — this is the unsealed confirmatory path that the previous session incorrectly declared exhausted.