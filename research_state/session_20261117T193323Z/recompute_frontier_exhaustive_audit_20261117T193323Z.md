# Independent Exhaustive Frontier Audit — FCLR-FRONTIER-VERIFY-06 (20261117T193323Z)

- **Generated UTC:** 2026-11-17T19:37:03Z
- **Campaign:** FCLR-FRONTIER-VERIFY-06-20261117T130551Z
- **Track priority:** Track C funding-conditioned volatility
- **Repository:** Funding-conditioned-volatility-and-liquidation-risk
- **Overall verdict:** `BLOCKED_ON_DESIGN`
- **Promotable:** `False`
- **FCLR-014 closed verdict reproduced:** `True`
- **Frontier verification mismatch:** `False`

## Method
Independent stdlib-only ZIP/CSV-aware reconstruction of `research_state/data_cache/` for the five Binance symbols. Tested-window boundaries read from `scripts/next_campaign_status.py` source (exclusion only); candidate feasibility recomputed independently. The canonical tool was run only as a comparison target (`--json`). No network, no parquet, no outcome data inspected. No sealed artifact modified.

## Cache reconstruction
- Months inventoried: 35
- Complete full-C2 months (all 3 kline kinds >= 125 CSVs + funding, all 5 symbols): 28 -> ['2024-04', '2024-05', '2024-06', '2024-07', '2024-08', '2024-09', '2025-01', '2025-02', '2025-03', '2025-04', '2025-05', '2025-06', '2025-07', '2025-08', '2025-09', '2025-10', '2025-11', '2025-12', '2026-01', '2026-02', '2026-03', '2026-04', '2026-05', '2026-06', '2026-07', '2026-08', '2026-09', '2026-10']
- Complete mark+funding-only months (mark >= 125 CSVs + funding): 31 -> ['2024-04', '2024-05', '2024-06', '2024-07', '2024-08', '2024-09', '2024-10', '2024-11', '2024-12', '2025-01', '2025-02', '2025-03', '2025-04', '2025-05', '2025-06', '2025-07', '2025-08', '2025-09', '2025-10', '2025-11', '2025-12', '2026-01', '2026-02', '2026-03', '2026-04', '2026-05', '2026-06', '2026-07', '2026-08', '2026-09', '2026-10']

## Full-C2 (mark+index+premium+funding)
- Individually feasible test blocks: 0
- Max mutually non-overlapping: 0
- Overlapping pairs: 0
- Contiguous run >= 127d: False (longest 61d)
- Campaign feasible: False

## Mark+funding-only (B0/B1/C1; no premium/index C2 terms)
- Individually feasible test months: 4 -> ['2024-10', '2024-11', '2024-12', '2025-01']
- Mutually non-overlapping selection: 2 -> [['2024-10', '2025-01']]
- Overlapping pairs: 5
- Contiguous run >= 127d: False (longest 123d)
- Campaign feasible (>=3 non-overlapping): False

## Expected closed-world result (reproduced)
- Full-C2: 0 disjoint feasible blocks; no contiguous run >=127d; campaign_feasible=False. ✓
- Mark+funding-only: 4 individually feasible (2024-10/11/12, 2025-01); 2 mutually non-overlapping (2024-10, 2025-01); 5 overlapping pairs; campaign_feasible_non_overlapping=False; no contiguous run >=127d. ✓
- Overall: BLOCKED_ON_DESIGN; promotable=False; fclr014_closed_verdict_reproduced=True.

## Comparison to canonical tool and sealed certificate (exact_match per field)
- design_feasibility.any_feasible: True
- disjoint_block_frontier.campaign_feasible: True
- disjoint_block_frontier.individual_feasible_count_matches_canonical: True
- disjoint_block_frontier.n_feasible: True
- markfund_frontier.any_contiguous_run_ge_min_design_days: True
- markfund_frontier.campaign_feasible_non_overlapping: True
- markfund_frontier.individually_feasible_months: True
- markfund_frontier.max_mutually_non_overlapping: True
- markfund_frontier.n_individually_feasible: True
- markfund_frontier.n_overlapping_pairs: True
- markfund_frontier.non_overlapping_selection: True
- all_exact_match: True

## Sensitivity grid (EXPLORATORY_DESIGN_ONLY / NOT_A_PREREG / NOT_PROMOTABLE)
- full_c2 train=30d embargo=7d test=14d: n_individually_feasible=0 months=[] max_non_overlap=0 n_overlapping_pairs=0 campaign_feasible=False any_run_ge_min=False longest=61d
- mark_funding_only train=30d embargo=7d test=14d: n_individually_feasible=4 months=['2024-10', '2024-11', '2024-12', '2025-01'] max_non_overlap=2 n_overlapping_pairs=5 campaign_feasible=False any_run_ge_min=False longest=123d
- full_c2 train=30d embargo=7d test=30d: n_individually_feasible=0 months=[] max_non_overlap=0 n_overlapping_pairs=0 campaign_feasible=False any_run_ge_min=False longest=61d
- mark_funding_only train=30d embargo=7d test=30d: n_individually_feasible=4 months=['2024-10', '2024-11', '2024-12', '2025-01'] max_non_overlap=2 n_overlapping_pairs=5 campaign_feasible=False any_run_ge_min=False longest=123d

## Integrity
- No confirmatory estimand run or re-scored.
- No sealed artifact modified.
- No outcome data inspected.
- All triggers OPEN; trigger-satisfied §16 path not taken.
