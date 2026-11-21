# FCLR-SESSION-SYNTHESIS-01 — Frontier Exhaustion Audit

- **Experiment ID:** FCLR-SESSION-SYNTHESIS-01-20261121T080000Z
- **Tool:** `scripts/next_campaign_status.py` (exit 0)
- **Overall status:** `NO_FEASIBLE_3_BLOCK_DESIGN_IN_ANY_DOMAIN`

## 1. Per-domain blockage

| Domain | Status | Detail |
|--------|--------|--------|
| Binance 5-symbol mark+funding contiguous | EXHAUSTED | No contiguous run ≥127d. 2024-04..2024-05 span 61d TOO SHORT; 2025-01 span 31d TOO SHORT. |
| Binance disjoint 30-day block | INFEASIBLE | All candidate test months (2024-04, 2024-05, 2025-01) have training windows containing missing/unfunded months. |
| Mark+funding-only B0/B1/C1 | BLOCKED_ON_DESIGN | Individually feasible test months = 1 ['2025-01']; need ≥3 mutually non-overlapping. |
| Hyperliquid bulk frontier | EXHAUSTED | 18 months of candles/funding/OI/liq; no untouched region long enough (2025-05 span 24d TOO SHORT). |
| Hyperliquid extended frontier | EXHAUSTED | 17 coins, 18 event months; usable 2025-11..2026-10 but no untouched contiguous region. |
| Months with klines but no funding | BASELINE_ONLY | 2024-01/02/03 have klines but funding starts 2024-04; baseline-only. |

Frozen preregs without an evaluation artifact: **NONE** (every frozen prereg has an evaluation).

## 2. Bottleneck assessment

**Primary bottleneck:** The prior rank-0 campaign
`FCLR-BOUNDED-TRIGGER-ONLY-LIQUIDATION-SOURCE-20261121T071500Z` was TRIGGER_ONLY, gated on an
external `NEW_OBSERVED_LIQUIDATION_SOURCE` trigger that cannot fire on frozen data. That caused
future agents to idle.

**Resolution:** This synthesis campaign executes a heavy, non-deferrable evidence-consolidation +
quantitative meta-analysis **now**, removing the trigger-only idle bottleneck. The frontier is
genuinely exhausted for *new 3-block confirmatory designs* on frozen data, but consolidation /
meta-analysis of the existing terminal record is heavy, admissible, and non-duplicative work.

**Reopen requires:** `NEW_OBSERVED_LIQUIDATION_SOURCE` (a new observed-liquidation data source
beyond the frozen panels).

**Verdict:** `FRONTIER_EXHAUSTED_FOR_NEW_CONFIRMATORY_DESIGNS_CONSOLIDATION_CONTINUES`