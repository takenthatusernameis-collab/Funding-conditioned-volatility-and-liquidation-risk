# FCLR-014 Panel Blocker Resolution — 2026-11-17T05:10:45Z

**Artifact ID:** FCLR-014-BLOCKER-RESOLUTION-20261117T051045Z
**Corrected Blocker:** Design admissibility under TESTED_WINDOWS, NOT data absence. Cache holds 31 months mark+funding (2024-04..2026-10) and 22 months full mark+index+premium+funding (2025-01..2026-10).

## Cache Coverage Summary

- **Mark+funding complete (all 5 symbols):** 31 months (2024-04..2026-10)
- **Full features (mark+index+premium+funding, all 5 symbols):** 28 months (2024-04..2026-10)
- **Note:** 2024-04..2024-09: complete mark+funding+premium+index for all 5; 2024-10..2024-12: mark+funding only (premium/index missing for 4/5 symbols); 2025-01..2026-10: complete full features for all 5

## Tested Windows (from `scripts/next_campaign_status.py`)

| Window | Label |
|--------|-------
| 2024-07-23..2024-09-30 | FCLR-FWD-VOL-2024Q4-CROSS (NOT_REPLICATED) |
| 2025-02-01..2025-05-31 | FCLR-FWD-VOL-2025-CROSS (NOT_REPLICATED) |
| 2026-05-01..2026-08-31 | FCLR-011 sealed PASS + FCLR-FWD-VOL-011-CONFIRM |
| 2026-08-03..2026-10-31 | FCLR-FWD-VOL-011-CONFIRM forward walk |
| 2025-07-23..2025-10-15 | FCLR-FWD-VOL-2025H2-CROSS (NOT_REPLICATED) |
| 2026-01-01..2026-04-01 | FCLR-FWD-VOL-2025Q1Q2-CROSS (NOT_REPLICATED) |
| 2024-06-01..2024-06-30 | FCLR-FWD-VOL-2024-DISJOINT-2024-06 (EXPLAINED_BY_ESTIMATOR; singleton) |
| 2025-06-01..2025-06-30 | FCLR-FWD-VOL-2025-DISJOINT-CROSS (EXPLORATORY_NULL) |
| 2025-11-01..2025-11-30 | FCLR-FWD-VOL-2025-DISJOINT-CROSS (EXPLORATORY_NULL) |
| 2025-12-01..2025-12-31 | FCLR-FWD-VOL-2025-DISJOINT-CROSS (EXPLORATORY_NULL) |

## Design Option Analysis

### Option A: Full C2 Design (mark+index+premium+funding)
**Requires:** mark, index, premium, funding for all 5 symbols in test AND train months
**Admissible months:** 2024-04, 2024-05, 2024-06, 2024-07, 2024-08, 2024-09, 2025-01, 2025-02, 2025-03, 2025-04, 2025-05, 2025-06, 2025-07, 2025-08, 2025-09, 2025-10, 2025-11, 2025-12, 2026-01, 2026-02, 2026-03, 2026-04, 2026-05, 2026-06, 2026-07, 2026-08, 2026-09, 2026-10
**Feasible disjoint blocks:** 0 (need >=3)
**Feasible contiguous runs (>=127d):** 0
**Can freeze new prereg:** False

All 2025-01..2026-10 full-feature months are consumed by sealed test windows. **NO valid untested blocks remain for Full C2 design.**

### Option B: Mark+Funding-Only Design (B0/B1/C1 — no premium features)
**Requires:** mark+funding for all 5 symbols in test AND train months
**Admissible months:** 31 months (2024-04..2026-10)
**Feasible disjoint blocks:** 4 (need >=3) ✓
**Feasible contiguous runs (>=127d):** 0
**Can freeze new prereg:** True

#### Available Disjoint Test Blocks (Mark+Funding Only)

| Test Month | Train Months | Classification |
|------------|--------------|----------------|
| 2024-10 | 2024-08, 2024-09 | AVAILABLE |
| 2024-11 | 2024-09, 2024-10 | AVAILABLE |
| 2024-12 | 2024-10, 2024-11 | AVAILABLE |
| 2025-01 | 2024-11, 2024-12 | AVAILABLE |


#### Consumed/Infeasible Blocks

| Test Month | Classification | Reason |
|------------|----------------|--------|
| 2024-04 | INCOMPLETE_TRAIN | Train months incomplete: 2024-02:incomplete_mark_or_funding, 2024-03:incomplete_... |
| 2024-05 | INCOMPLETE_TRAIN | Train months incomplete: 2024-03:incomplete_mark_or_funding |
| 2024-06 | CONSUMED_BY_SEALED_CELL | Inside tested window: FCLR-FWD-VOL-2024-DISJOINT-2024-06 (EXPLAINED_BY_ESTIMATOR... |
| 2024-07 | CONSUMED_BY_SEALED_CELL | Inside tested window: FCLR-FWD-VOL-2024Q4-CROSS (NOT_REPLICATED) |
| 2024-08 | CONSUMED_BY_SEALED_CELL | Inside tested window: FCLR-FWD-VOL-2024Q4-CROSS (NOT_REPLICATED) |
| 2024-09 | CONSUMED_BY_SEALED_CELL | Inside tested window: FCLR-FWD-VOL-2024Q4-CROSS (NOT_REPLICATED) |
| 2025-02 | CONSUMED_BY_SEALED_CELL | Inside tested window: FCLR-FWD-VOL-2025-CROSS (NOT_REPLICATED) |
| 2025-03 | CONSUMED_BY_SEALED_CELL | Inside tested window: FCLR-FWD-VOL-2025-CROSS (NOT_REPLICATED) |
| 2025-04 | CONSUMED_BY_SEALED_CELL | Inside tested window: FCLR-FWD-VOL-2025-CROSS (NOT_REPLICATED) |
| 2025-05 | CONSUMED_BY_SEALED_CELL | Inside tested window: FCLR-FWD-VOL-2025-CROSS (NOT_REPLICATED) |
| 2025-06 | CONSUMED_BY_SEALED_CELL | Inside tested window: FCLR-FWD-VOL-2025-DISJOINT-CROSS (EXPLORATORY_NULL) |
| 2025-07 | CONSUMED_BY_SEALED_CELL | Inside tested window: FCLR-FWD-VOL-2025H2-CROSS (NOT_REPLICATED) |
| 2025-08 | CONSUMED_BY_SEALED_CELL | Inside tested window: FCLR-FWD-VOL-2025H2-CROSS (NOT_REPLICATED) |
| 2025-09 | CONSUMED_BY_SEALED_CELL | Inside tested window: FCLR-FWD-VOL-2025H2-CROSS (NOT_REPLICATED) |
| 2025-10 | CONSUMED_BY_SEALED_CELL | Inside tested window: FCLR-FWD-VOL-2025H2-CROSS (NOT_REPLICATED) |
| 2025-11 | CONSUMED_BY_SEALED_CELL | Inside tested window: FCLR-FWD-VOL-2025-DISJOINT-CROSS (EXPLORATORY_NULL) |
| 2025-12 | CONSUMED_BY_SEALED_CELL | Inside tested window: FCLR-FWD-VOL-2025-DISJOINT-CROSS (EXPLORATORY_NULL) |
| 2026-01 | CONSUMED_BY_SEALED_CELL | Inside tested window: FCLR-FWD-VOL-2025Q1Q2-CROSS (NOT_REPLICATED) |
| 2026-02 | CONSUMED_BY_SEALED_CELL | Inside tested window: FCLR-FWD-VOL-2025Q1Q2-CROSS (NOT_REPLICATED) |
| 2026-03 | CONSUMED_BY_SEALED_CELL | Inside tested window: FCLR-FWD-VOL-2025Q1Q2-CROSS (NOT_REPLICATED) |
| 2026-04 | CONSUMED_BY_SEALED_CELL | Inside tested window: FCLR-FWD-VOL-2025Q1Q2-CROSS (NOT_REPLICATED) |
| 2026-05 | CONSUMED_BY_SEALED_CELL | Inside tested window: FCLR-011 sealed PASS + FCLR-FWD-VOL-011-CONFIRM |
| 2026-06 | CONSUMED_BY_SEALED_CELL | Inside tested window: FCLR-011 sealed PASS + FCLR-FWD-VOL-011-CONFIRM |
| 2026-07 | CONSUMED_BY_SEALED_CELL | Inside tested window: FCLR-011 sealed PASS + FCLR-FWD-VOL-011-CONFIRM |
| 2026-08 | CONSUMED_BY_SEALED_CELL | Inside tested window: FCLR-011 sealed PASS + FCLR-FWD-VOL-011-CONFIRM |
| 2026-09 | CONSUMED_BY_SEALED_CELL | Inside tested window: FCLR-FWD-VOL-011-CONFIRM forward walk |
| 2026-10 | CONSUMED_BY_SEALED_CELL | Inside tested window: FCLR-FWD-VOL-011-CONFIRM forward walk |


## Overall Verdict

- **Full C2 design (current FCLR-014 pre-registration):** NOT FEASIBLE — all full-feature months consumed by tested windows
- **Mark+funding-only B0/B1/C1 design:** **FEASIBLE** — 4 disjoint test blocks available (2024-10, 2024-11, 2024-12, 2025-01), meets >=3 block requirement

## Recommended Next Action

**Freeze a NEW mark+funding-only B0/B1/C1 pre-registration** (copy `session_20261116T035833Z/prereg_template_trigger_gated_20261116T035833Z.json`, set `outcome_data_inspected_before_freeze=false`) using:
- Test blocks: 2024-10, 2024-11, 2024-12 (3 non-overlapping 30-day blocks)
- Train history: 2024-08..2024-11 (mark+funding complete for all 5 symbols)
- **STOP before outcomes** — this is a pre-registration freeze, not an execution

The existing FCLR-014 pre-registration (`pre_registration_fclr014_confirmatory_funding_vol_20261109T181124Z.json`) remains frozen `NO_GO` with FCLR-002-copied 2-block splits. A new prereg with a materially different estimand (mark+funding-only, no premium features) can be frozen before outcome inspection.
