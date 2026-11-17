# FCLR-014 Panel Coverage Audit + Blocker Resolution — 20261117T041333Z

Verdict: **FCLR-014 BLOCKED-ON-DESIGN (corrected; NOT blocked-on-data)**

Coverage-only. No outcomes inspected. No parquet engine used. No network.

## Per-month admissibility (5 symbols: BTCUSDT, ETHUSDT, BNBUSDT, SOLUSDT, XRPUSDT)

| month | days | mark_total | funding_syms | admissible | status |
|---|---|---|---|---|---|
| 2024-01 | 31 | 155 | 0/5 | False | INCOMPLETE_COVERAGE |
| 2024-02 | 29 | 145 | 0/5 | False | INCOMPLETE_COVERAGE |
| 2024-03 | 31 | 155 | 0/5 | False | INCOMPLETE_COVERAGE |
| 2024-04 | 30 | 150 | 5/5 | True | UNTESTED_COMPLETE_MARKFUND |
| 2024-05 | 31 | 155 | 5/5 | True | UNTESTED_COMPLETE_MARKFUND |
| 2024-06 | 30 | 150 | 5/5 | True | CONSUMED_BY_SEALED_CELL |
| 2024-07 | 31 | 155 | 5/5 | True | CONSUMED_BY_SEALED_CELL |
| 2024-08 | 31 | 155 | 5/5 | True | CONSUMED_BY_SEALED_CELL |
| 2024-09 | 30 | 150 | 5/5 | True | CONSUMED_BY_SEALED_CELL |
| 2024-10 | 31 | 155 | 5/5 | True | UNTESTED_COMPLETE_MARKFUND |
| 2024-11 | 30 | 150 | 5/5 | True | UNTESTED_COMPLETE_MARKFUND |
| 2024-12 | 31 | 155 | 5/5 | True | UNTESTED_COMPLETE_MARKFUND |
| 2025-01 | 31 | 155 | 5/5 | True | UNTESTED_COMPLETE_MARKFUND |
| 2025-02 | 28 | 140 | 5/5 | True | CONSUMED_BY_SEALED_CELL |
| 2025-03 | 31 | 155 | 5/5 | True | CONSUMED_BY_SEALED_CELL |
| 2025-04 | 30 | 150 | 5/5 | True | CONSUMED_BY_SEALED_CELL |
| 2025-05 | 31 | 155 | 5/5 | True | CONSUMED_BY_SEALED_CELL |
| 2025-06 | 30 | 150 | 5/5 | True | CONSUMED_BY_SEALED_CELL |
| 2025-07 | 31 | 155 | 5/5 | True | CONSUMED_BY_SEALED_CELL |
| 2025-08 | 31 | 155 | 5/5 | True | CONSUMED_BY_SEALED_CELL |
| 2025-09 | 30 | 150 | 5/5 | True | CONSUMED_BY_SEALED_CELL |
| 2025-10 | 31 | 155 | 5/5 | True | CONSUMED_BY_SEALED_CELL |
| 2025-11 | 30 | 150 | 5/5 | True | CONSUMED_BY_SEALED_CELL |
| 2025-12 | 31 | 155 | 5/5 | True | CONSUMED_BY_SEALED_CELL |
| 2026-01 | 31 | 155 | 5/5 | True | CONSUMED_BY_SEALED_CELL |
| 2026-02 | 28 | 140 | 5/5 | True | CONSUMED_BY_SEALED_CELL |
| 2026-03 | 31 | 155 | 5/5 | True | CONSUMED_BY_SEALED_CELL |
| 2026-04 | 30 | 150 | 5/5 | True | CONSUMED_BY_SEALED_CELL |
| 2026-05 | 31 | 155 | 5/5 | True | CONSUMED_BY_SEALED_CELL |
| 2026-06 | 30 | 150 | 5/5 | True | CONSUMED_BY_SEALED_CELL |
| 2026-07 | 31 | 185 | 5/5 | True | CONSUMED_BY_SEALED_CELL |
| 2026-08 | 31 | 155 | 5/5 | True | CONSUMED_BY_SEALED_CELL |
| 2026-09 | 30 | 150 | 5/5 | True | CONSUMED_BY_SEALED_CELL |
| 2026-10 | 31 | 145 | 5/5 | True | CONSUMED_BY_SEALED_CELL |
| 2026-11 | 30 | 40 | 0/5 | False | INCOMPLETE_COVERAGE |

## Candidate disjoint 30-day blocks — mark+funding-only estimand (B0/B1/C1)

available = 2 (['2024-12', '2025-01'])

- test 2024-04: **INCOMPLETE_TRAIN** (train 2024-02-24..2024-03-24; missing=['2024-02', '2024-03'])
- test 2024-05: **INCOMPLETE_TRAIN** (train 2024-03-25..2024-04-23; missing=['2024-03'])
- test 2024-10: **INCOMPLETE_TRAIN** (train 2024-08-25..2024-09-23; missing=['2024-08', '2024-09'])
- test 2024-11: **INCOMPLETE_TRAIN** (train 2024-09-25..2024-10-24; missing=['2024-09'])
- test 2024-12: **AVAILABLE** (train 2024-10-25..2024-11-23; missing=[])
- test 2025-01: **AVAILABLE** (train 2024-11-25..2024-12-24; missing=[])

## Candidate disjoint 30-day blocks — FULL C2 estimand (needs mark+index+premium+funding)

available = 0 ([])

- test 2024-04: **INCOMPLETE_TRAIN** (train 2024-02-24..2024-03-24; missing=['2024-02', '2024-03'])
- test 2024-05: **INCOMPLETE_TRAIN** (train 2024-03-25..2024-04-23; missing=['2024-03'])
- test 2025-01: **INCOMPLETE_TRAIN** (train 2024-11-25..2024-12-24; missing=['2024-11', '2024-12'])

## Contiguous rolling-design runs (need >= 127d)

mark+funding-only:
- 2024-04..2024-05 span=61d feasible=False
- 2024-10..2025-01 span=123d feasible=False

full-C2:
- 2024-04..2024-05 span=61d feasible=False
- 2025-01..2025-01 span=31d feasible=False

**AVAILABLE disjoint blocks (mark+funding): 2** (need >=3)
**AVAILABLE disjoint blocks (full-C2): 0** (need >=3)
**campaign_feasible_new_prereg: False**

## Tool cross-check (scripts/next_campaign_status.py)

- ready funding-backed untested months: ['2024-04', '2024-05', '2025-01']
- any contiguous feasible: False
- n feasible disjoint blocks: 0

## Corrected blocker

DESIGN_ADMISSIBILITY: full-C2 estimand has 0 available disjoint blocks and no contiguous untested run >= 127d; mark+funding-only (B0/B1/C1) has 2 available blocks (<3). A confirmatory >=3-block FCLR-014 design cannot be frozen from local data without consuming a sealed window. A 2-block mark+funding-only EXPLORATORY pilot is the only constructible local design, and it is NOT promotable.

FCLR-014 is BLOCKED-ON-DESIGN, not blocked-on-data. The cache DOES hold complete 5-symbol mark+funding months, but every untested complete month lacks a complete funded 30-day train window, and no contiguous untested run reaches MIN_DESIGN_DAYS. Under the FULL C2 rule (mark+index+premium+funding) there are 0 available disjoint blocks; under the mark+funding-only rule there are 2 (2024-12, 2025-01) - still <3. A confirmatory >=3-block FCLR-014 design cannot be frozen from local data without consuming a sealed window; do NOT re-score and do NOT relax the completeness rule.
