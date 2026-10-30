# AGENT HANDOFF — Funding-Conditioned Volatility and Liquidation Risk

UPDATED: 2026-10-30T17:05:23Z
HEAD: fb7b0da1 (main) — working tree clean
REPO: Funding-conditioned-volatility-and-liquidation-risk
DURABLE_HANDOFF: SINGLE_SOURCE_OF_TRUTH
SESSION_GOAL: MAINTENANCE_ONLY — VERIFY_CLOSURE_AND_STOP

## PRIORITIZED INITIAL TASK (2026-10-30T17:05:23Z) — MANDATORY

**TASK_ID:** `HND-20261030-170523-CLOSEOUT_VERIFY`
**PRIORITY:** P0
**MODE:** READ-ONLY VERIFICATION. NO EXPLORATORY RESEARCH.

The program is **CLOSED**. H001 (funding-conditioned volatility improvement) is **NOT_SUPPORTED** across all confirmatory paths. Do not re-open sealed experiments.

### IMMEDIATE STEPS (Execute in order, no deviation)

1. **[VERIFY TESTS]** Run `python -m unittest discover -s tests -v`
   - Expected: `14 tests OK`. If any test fails, fix the minimal breakage with evidence, or report the exact failure and stop. Do not proceed if tests are broken.
2. **[VERIFY REPRODUCIBILITY]** Run `FCLR_EXPERIMENT=FCLR-006 python scripts/run_evaluation.py`
   - Expected: Only the `Generated` timestamp differs from `research_state/evaluation_summary_FCLR006.md`. All metrics and intervals must be byte-identical otherwise.
3. **[VERIFY CLOSURE RECORD]** Read `research_state/final_record_closure_audit.md`
   - Confirm verdicts for FCLR-001/002/003/005/006, H001/H002/H003, and Track A are present and match the closeout.
4. **[VERIFY ERRATA]** Read `research_state/reporting_errata_FCLR006.md`
   - Confirm the CI flag erratum is recorded (interval entirely positive, flag reporting error only).
5. **[REPORT & STOP]** If all checks pass with no modifications needed, output exactly: `PROGRAM_CLOSED_VERIFIED_H001_NOT_SUPPORTED` and stop with no further tool calls.

### BOTTLENECK REMOVAL
- No new data acquisition needed (all admissible data exhausted)
- No training/tuning loops required
- No background processes to spin up
- Verification is O(seconds) and requires no network access

### ONLY POSSIBLE NEW WORK
A new route is **ONLY** admissible if concrete evidence of a **new unauthenticated admissible liquidation/price source** appears with:
- ≥ 5 symbols
- ≥ 3 non-overlapping 30-day blocks
- Verifiable coverage in `research_state/liquidation_sources_enumeration.md`

If such evidence exists, **pre-register a new experiment ID BEFORE examining outcomes** per `RESEARCH_PROMPT.md §16`. Otherwise, do **NOT** invent a new experiment.

### HARD CONSTRAINTS
- **NO SEAL VIOLATIONS:** Do not re-run FCLR-001/002/003/005/006 or tune on sealed holds.
- **NO THRESHOLD SHOPPING:** Do not optimize cutoffs post-hoc.
- **NO WORKFLOW CHANGES:** Do not modify `.github/workflows/*` without explicit maintainer authorization.
- **PRESERVE NEGATIVES:** H001_NOT_SUPPORTED is correct. Document nulls, not just positives.
- **DISTINGUISH OUTCOMES:** Keep modeled (H003) vs observed (H004) strictly separate.
- **NO FABRICATION:** Cite evidence paths for every claim.

**Do heavy verification first. Do not chase tangents. If closure is verified, stop cleanly.**