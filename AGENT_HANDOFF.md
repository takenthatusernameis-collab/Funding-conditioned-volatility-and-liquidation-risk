# AGENT HANDOFF — Funding-Conditioned Volatility and Liquidation Risk

UPDATED: 2026-10-30T09:45:32Z
HEAD: 5655c6ca (main) — working tree may have uncommitted artifacts (do NOT commit unless explicitly asked)
REPO: Funding-conditioned-volatility-and-liquidation-risk

## INITIAL TASK MESSAGE (TIMESTAMPED) — MANDATORY FOR NEXT AGENTIC WORK SESSION

**PRIORITY (repo name): FUNDING-CONDITIONED VOLATILITY + LIQUIDATION RISK. DO HEAVY COMPUTATIONAL WORK. NO STATUS-ONLY.**

This repository's name prioritizes both tracks. Track A (observed liquidations) is STRUCTURALLY BLOCKED (documented exhaustively). Track B (hypothetical/synthetic boundary breaches) and Track C (volatility forecasting) remain open and demand heavy work. **You MUST NOT stop at exploration - you MUST produce concrete artifacts with measurable progress.**

### IMMEDIATE MANDATORY CAMPAIGN (EXECUTE IN FULL, NO SHORTCUTS)

**CAMPAIGN ID: FCLR-HEAVY-002 | TIME: 2026-10-30T09:45:32Z**

1. **VOLATILITY BASELINE RECOMPUTATION (HARD)** - Recompute FCLR-002 and FCLR-003 end-to-end using `scripts/run_evaluation_fixed.py` with exact commands logged. Compare byte-for-byte against existing summaries. Identify any numerical drift. Write results to `research_state/volatility_baseline_recheck_20261030.md` with checksums.
2. **FUNDING-CONDITIONED INTERACTION ANALYSIS (HARD)** - Using cached data only, build a funding×volatility interaction model on train/val, evaluate on frozen test sets (FCLR-002 and FCLR-003). Test pre-registered interactions: funding_sign×RV24, |funding|×RV_ratio, funding_persistence×vol_regime. Use block bootstrap (>=2000). Record all results in `research_state/funding_interaction_analysis.md`. Do NOT touch holdouts early.
3. **BOUNDARY-BREACH DEEP DIVE (HARD)** - Re-run and EXTEND `scripts/synthetic_boundary_labels.py` analysis. Vary maintenance margin (0.004, 0.005, 0.006), add funding-cost assumptions, test horizons (6h, 12h, 24h). For each config compute precision/recall/calibration vs B0/B1/C1/C2 style features. Use ONLY synthetic labels clearly marked as NOT observed liquidations. Write `research_state/boundary_breach_deep_dive.md`.
4. **ROBUSTNESS STRESS TESTS (HARD)** - Regime splits (high/low funding, high/low RV), symbol concentration tests, time-block stability. Bootstrap everything. Correct for multiple comparisons (BH-FDR). Document all.
5. **TESTS + VERIFICATION (HARD)** - Add >=2 focused tests for new analysis code in `tests/`. Run `python -m unittest discover -s tests -v`. All must pass.

**CONSTRAINTS (NON-NEGOTIABLE):**
- NO forecast gate re-runs that reuse sealed holdouts for tuning
- NO .github/workflows changes
- NO trading/risk overlays
- NO observed liquidation data fabrication
- Track A remains BLOCKED - do NOT waste cycles on unfound sources
- Every claim needs numbers, CIs, sample sizes
- Status updates alone are FORBIDDEN - produce files with concrete results

**VERIFICATION COMMANDS:**
```bash
python -m unittest tests.test_funding_correction_replication tests.test_funding_correction_robustness tests.test_fclr002_coverage_audit -v
python -m unittest discover -s tests -v
```

## CURRENT STATE (GROUND TRUTH)
- Track A (observed liquidations): NOT_SUPPORTED/STRUCTURAL_BLOCKER - fully exhausted per RESEARCH_PROMPT §16
- FCLR-001/002/003: sealed, gates NOT_MET. C1 shows improvement in FCLR-003 (8.09%) but C2 underperforms; C2 strong in FCLR-002 (9.28%) but test window too short
- FCLR-H003 (boundary breaches): INCONCLUSIVE, no incremental skill
- FCLR-H002 (funding correction): PARTIAL replication done
- All existing tests pass (14/14 as of last run)
- Heavy work on funding-conditioned volatility + deeper boundary analysis is the path forward

## BOTTLENECK REMOVAL
- Do NOT create new orchestration/status files - extend existing research_state artifacts
- Do NOT re-probe liquidation sources endlessly - only if you find a concrete unauthenticated endpoint with >=90 days continuous history AND >=3x30-day blocks; otherwise document and move on
- Focus compute on analysis, not plumbing

**START IMMEDIATELY. NO PLANNING-ONLY RESPONSE. EXECUTE THE CAMPAIGN ABOVE.**
