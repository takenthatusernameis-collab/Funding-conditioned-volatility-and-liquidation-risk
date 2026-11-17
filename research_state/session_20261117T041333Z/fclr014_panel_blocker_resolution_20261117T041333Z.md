# FCLR-014 Blocker Resolution — 20261117T041333Z

**corrected_blocker:** DESIGN_ADMISSIBILITY: full-C2 estimand has 0 available disjoint blocks and no contiguous untested run >= 127d; mark+funding-only (B0/B1/C1) has 2 available blocks (<3). A confirmatory >=3-block FCLR-014 design cannot be frozen from local data without consuming a sealed window. A 2-block mark+funding-only EXPLORATORY pilot is the only constructible local design, and it is NOT promotable.

- campaign_feasible_new_prereg: False
- available disjoint blocks (mark+funding-only, B0/B1/C1): 2 (need >=3) -> ['2024-12', '2025-01']
- available disjoint blocks (full-C2): 0 (need >=3) -> []
- min_design_days: 127

## Month classification

| month | mark+fund adm | full-C2 adm | status | reason |
|---|---|---|---|---|
| 2024-01 | False | False | INCOMPLETE_COVERAGE | missing_dir=[] unfunded=['BTCUSDT', 'ETHUSDT', 'BNBUSDT', 'SOLUSDT', 'XRPUSDT'] mark_lt_25=[] |
| 2024-02 | False | False | INCOMPLETE_COVERAGE | missing_dir=[] unfunded=['BTCUSDT', 'ETHUSDT', 'BNBUSDT', 'SOLUSDT', 'XRPUSDT'] mark_lt_25=[] |
| 2024-03 | False | False | INCOMPLETE_COVERAGE | missing_dir=[] unfunded=['BTCUSDT', 'ETHUSDT', 'BNBUSDT', 'SOLUSDT', 'XRPUSDT'] mark_lt_25=[] |
| 2024-04 | True | True | UNTESTED_COMPLETE_MARKFUND | outside every TESTED_WINDOW; mark+funding complete for 5 symbols |
| 2024-05 | True | True | UNTESTED_COMPLETE_MARKFUND | outside every TESTED_WINDOW; mark+funding complete for 5 symbols |
| 2024-06 | True | True | CONSUMED_BY_SEALED_CELL | month overlaps tested window(s): ['FCLR-FWD-VOL-2024-DISJOINT-2024-06 (EXPLAINED_BY_ESTIMATOR; singleton)'] |
| 2024-07 | True | True | CONSUMED_BY_SEALED_CELL | month overlaps tested window(s): ['FCLR-FWD-VOL-2024Q4-CROSS (NOT_REPLICATED)'] |
| 2024-08 | True | True | CONSUMED_BY_SEALED_CELL | month overlaps tested window(s): ['FCLR-FWD-VOL-2024Q4-CROSS (NOT_REPLICATED)'] |
| 2024-09 | True | True | CONSUMED_BY_SEALED_CELL | month overlaps tested window(s): ['FCLR-FWD-VOL-2024Q4-CROSS (NOT_REPLICATED)'] |
| 2024-10 | True | False | UNTESTED_COMPLETE_MARKFUND | outside every TESTED_WINDOW; mark+funding complete for 5 symbols; index/premium INCOMPLETE -> full-C2 NOT admissible |
| 2024-11 | True | False | UNTESTED_COMPLETE_MARKFUND | outside every TESTED_WINDOW; mark+funding complete for 5 symbols; index/premium INCOMPLETE -> full-C2 NOT admissible |
| 2024-12 | True | False | UNTESTED_COMPLETE_MARKFUND | outside every TESTED_WINDOW; mark+funding complete for 5 symbols; index/premium INCOMPLETE -> full-C2 NOT admissible |
| 2025-01 | True | True | UNTESTED_COMPLETE_MARKFUND | outside every TESTED_WINDOW; mark+funding complete for 5 symbols |
| 2025-02 | True | True | CONSUMED_BY_SEALED_CELL | month overlaps tested window(s): ['FCLR-FWD-VOL-2025-CROSS (NOT_REPLICATED)'] |
| 2025-03 | True | True | CONSUMED_BY_SEALED_CELL | month overlaps tested window(s): ['FCLR-FWD-VOL-2025-CROSS (NOT_REPLICATED)'] |
| 2025-04 | True | True | CONSUMED_BY_SEALED_CELL | month overlaps tested window(s): ['FCLR-FWD-VOL-2025-CROSS (NOT_REPLICATED)'] |
| 2025-05 | True | True | CONSUMED_BY_SEALED_CELL | month overlaps tested window(s): ['FCLR-FWD-VOL-2025-CROSS (NOT_REPLICATED)'] |
| 2025-06 | True | True | CONSUMED_BY_SEALED_CELL | month overlaps tested window(s): ['FCLR-FWD-VOL-2025-DISJOINT-CROSS (EXPLORATORY_NULL)'] |
| 2025-07 | True | True | CONSUMED_BY_SEALED_CELL | month overlaps tested window(s): ['FCLR-FWD-VOL-2025H2-CROSS (NOT_REPLICATED)'] |
| 2025-08 | True | True | CONSUMED_BY_SEALED_CELL | month overlaps tested window(s): ['FCLR-FWD-VOL-2025H2-CROSS (NOT_REPLICATED)'] |
| 2025-09 | True | True | CONSUMED_BY_SEALED_CELL | month overlaps tested window(s): ['FCLR-FWD-VOL-2025H2-CROSS (NOT_REPLICATED)'] |
| 2025-10 | True | True | CONSUMED_BY_SEALED_CELL | month overlaps tested window(s): ['FCLR-FWD-VOL-2025H2-CROSS (NOT_REPLICATED)'] |
| 2025-11 | True | True | CONSUMED_BY_SEALED_CELL | month overlaps tested window(s): ['FCLR-FWD-VOL-2025-DISJOINT-CROSS (EXPLORATORY_NULL)'] |
| 2025-12 | True | True | CONSUMED_BY_SEALED_CELL | month overlaps tested window(s): ['FCLR-FWD-VOL-2025-DISJOINT-CROSS (EXPLORATORY_NULL)'] |
| 2026-01 | True | True | CONSUMED_BY_SEALED_CELL | month overlaps tested window(s): ['FCLR-FWD-VOL-2025Q1Q2-CROSS (NOT_REPLICATED)'] |
| 2026-02 | True | True | CONSUMED_BY_SEALED_CELL | month overlaps tested window(s): ['FCLR-FWD-VOL-2025Q1Q2-CROSS (NOT_REPLICATED)'] |
| 2026-03 | True | True | CONSUMED_BY_SEALED_CELL | month overlaps tested window(s): ['FCLR-FWD-VOL-2025Q1Q2-CROSS (NOT_REPLICATED)'] |
| 2026-04 | True | True | CONSUMED_BY_SEALED_CELL | month overlaps tested window(s): ['FCLR-FWD-VOL-2025Q1Q2-CROSS (NOT_REPLICATED)'] |
| 2026-05 | True | True | CONSUMED_BY_SEALED_CELL | month overlaps tested window(s): ['FCLR-011 sealed PASS + FCLR-FWD-VOL-011-CONFIRM'] |
| 2026-06 | True | True | CONSUMED_BY_SEALED_CELL | month overlaps tested window(s): ['FCLR-011 sealed PASS + FCLR-FWD-VOL-011-CONFIRM'] |
| 2026-07 | True | True | CONSUMED_BY_SEALED_CELL | month overlaps tested window(s): ['FCLR-011 sealed PASS + FCLR-FWD-VOL-011-CONFIRM'] |
| 2026-08 | True | True | CONSUMED_BY_SEALED_CELL | month overlaps tested window(s): ['FCLR-011 sealed PASS + FCLR-FWD-VOL-011-CONFIRM', 'FCLR-FWD-VOL-011-CONFIRM forward walk'] |
| 2026-09 | True | True | CONSUMED_BY_SEALED_CELL | month overlaps tested window(s): ['FCLR-FWD-VOL-011-CONFIRM forward walk'] |
| 2026-10 | True | True | CONSUMED_BY_SEALED_CELL | month overlaps tested window(s): ['FCLR-FWD-VOL-011-CONFIRM forward walk'] |
| 2026-11 | False | False | INCOMPLETE_COVERAGE | missing_dir=[] unfunded=['BTCUSDT', 'ETHUSDT', 'BNBUSDT', 'SOLUSDT', 'XRPUSDT'] mark_lt_25=['BTCUSDT', 'ETHUSDT', 'BNBUSDT', 'SOLUSDT', 'XRPUSDT'] |

FCLR-014 is BLOCKED-ON-DESIGN, not blocked-on-data. The cache DOES hold complete 5-symbol mark+funding months, but every untested complete month lacks a complete funded 30-day train window, and no contiguous untested run reaches MIN_DESIGN_DAYS. Under the FULL C2 rule (mark+index+premium+funding) there are 0 available disjoint blocks; under the mark+funding-only rule there are 2 (2024-12, 2025-01) - still <3. A confirmatory >=3-block FCLR-014 design cannot be frozen from local data without consuming a sealed window; do NOT re-score and do NOT relax the completeness rule.
