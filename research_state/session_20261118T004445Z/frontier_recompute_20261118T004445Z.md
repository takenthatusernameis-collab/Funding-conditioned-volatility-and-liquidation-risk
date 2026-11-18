# Frontier Recompute — 20261118T004445Z (verify, do not re-fix)

Campaign: `FCLR-LEDGER-INTEGRITY-02-20261118T000000Z`

Independently re-runs `scripts/next_campaign_status.py` `markfund_frontier()` + `disjoint_block_frontier()`. Read-only, outcome-blind.

## Observed vs expected closed verdict

| field | expected | observed | match |
|---|---|---|---|
| n_individually_feasible | `1` | `1` | True |
| individually_feasible_months | `['2025-01']` | `['2025-01']` | True |
| n_overlapping_pairs | `0` | `0` | True |
| max_mutually_non_overlapping | `1` | `1` | True |
| campaign_feasible_non_overlapping | `False` | `False` | True |

**PASS: True** (mismatches: none)

## Arithmetic that closes the frontier

- Only individually-feasible test month(s): ['2025-01'] (< MIN_MF_BLOCKS=3)
- Its 30-day train window 2024-11-25..2024-12-24 over ['2024-11', '2024-12'] is FCLR-003 test, allowed as pre-test history; the test month itself is untested.
- Contiguous untested complete mark+funding runs: [(['2024-04', '2024-05'], 61), (['2025-01'], 31)]; max span vs MIN_DESIGN_DAYS=127 -> feasible=False.
- Therefore `max_mutually_non_overlapping=1` `campaign_feasible_non_overlapping=False`. **Frontier closed.**
