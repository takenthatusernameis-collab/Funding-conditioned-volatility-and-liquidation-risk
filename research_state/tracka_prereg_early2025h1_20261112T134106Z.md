# Preregistration — TRACKA-HL-EARLY4H-2025H1

**Campaign:** FCLR-EARLY4H-2025H1-HEAVY v2
**Frozen (UTC):** 2026-11-12T13:41:06Z
**Status:** FROZEN BEFORE OUTCOMES
**SHA-256:** `db9d643df1c64323e07398de95942f059766ed3368e29d503303d231c082667a`

## Window and labels
- Observed liquidation labels: 2025-05-25T00:00:00+00:00 .. 2025-10-31T23:59:59+00:00
- Labels are observed ironflow events. No modeled, proxy, or synthetic labels.
- Universe: 9 named coins (AVAX, BNB, BTC, DOGE, ETH, LINK, SOL, SUI, XRP).

## Splits
- Train: 2025-05-25T00:00:00Z .. 2025-08-31T23:59:59Z
- Validation: 2025-09-01T00:00:00Z .. 2025-09-30T23:59:59Z
- Test blocks: 5 complete 30-day blocks, 1-day purge

## Models (frozen)
- B0 persistence; B1 HAR-RV (log RV4h/RV24h/RV168h);
- C1 = B1 + signed funding + trailing abs-funding percentile;
- C2 = C1 + mark/index premium + mark/EMA24 distance.

## Primary contrast and gate
- Primary: `C2_vs_B1`; metric QLIKE (lower better).
- PASS requires >= 2.0% relative QLIKE reduction AND 95% CI upper < 0
  AND >= 5 paired instruments AND >= 3 test blocks,
  with Holm correction across the declared family.

## Concentration hazard
BTC+ETH are ~63% of events and ~84% of notional. Per-coin and per-block reporting
is mandatory; a PASS driven by a single coin or block is rejected.
