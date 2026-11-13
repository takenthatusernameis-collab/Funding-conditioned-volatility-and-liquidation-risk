# Coverage Audit / Feasibility — FCLR-FWD-VOL-2024Q1-RV-DIAGNOSTIC
Generated: 2026-11-13T11:12:44Z
Status: **NOT_EXECUTABLE_DESIGN_SHORTFALL**

## Window & data
- Window: 2024-01-01T00:00:00Z .. 2024-03-31T23:00:00Z (~91.0 days)
- Cached months 2024-01/02/03: mark/premium/index klines COMPLETE for 5 symbols (per `scripts/next_campaign_status.py`).
- Funding: **ABSENT** (funding starts 2024-04). Design is volatility-only B0/B1; funding-conditioned hypotheses out of scope.

## Pre-registered blocks (as specified) — train feasibility
| block | test_start | test_end | test_days | train_end (7d embargo) | train_days (from 2024-01-01) |
|---:|---|---|---:|---|---:|
| 0 | 2024-01-03T00:00:00Z | 2024-02-01T23:00:00Z | 29.958 | 2023-12-26 23:00:00+00:00 | 0.0 |
| 1 | 2024-01-31T00:00:00Z | 2024-03-01T23:00:00Z | 30.958 | 2024-01-23 23:00:00+00:00 | 22.958 |
| 2 | 2024-02-28T00:00:00Z | 2024-03-30T23:00:00Z | 31.958 | 2024-02-20 23:00:00+00:00 | 50.958 |

## Shortfall
- Block 0 train = **0.0 days** (< 30 days) — insufficient for model fitting.
- A minimal design requiring 3×30-day non-overlapping test blocks + 7-day embargo + ≥30-day train needs ≥141 days; available window is 91.0 days (deficit 50.0 days).
- No alternative partition of 2024-01..2024-03 can satisfy ≥3 non-overlapping 30-day test blocks with a meaningful train period.

## Decision
**NOT_EXECUTABLE_DESIGN_SHORTFALL.** Do not freeze a prereg, do not execute, do not force a funding-conditioned reading on a window without funding. Evidence recorded; Cell 7 closed by design shortfall.
