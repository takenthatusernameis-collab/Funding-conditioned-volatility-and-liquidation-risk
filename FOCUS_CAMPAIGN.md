# FOCUS_CAMPAIGN (superseded redirect — do not execute)

**Timestamp (UTC):** 2026-11-12T11:38:00Z

**Authoritative single durable handoff: `HANDOFF_NEXT_SESSION.md`.**

Campaign **`FCLR-EARLY4H-2025H1-HEAVY`** (repo priority: funding-conditioned volatility > observed liquidation risk > modeled boundary breaches).

The prior campaign (`FCLR-NEXT-HEAVY-OR-CHECKPOINT`) resolved to a clean stop on
2026-11-12T09:51:12Z. That stop was based on a false premise: it probed **1h** candles,
which Hyperliquid serves only from 2026-04-18, and concluded no pre-2026-04 candle data
exists. The **4h** interval serves back to 2024-08-01.

Consequently a powered, unclaimed, admissible panel exists for **2025-05-01..2025-10-31**:
- observed ironflow labels cached (9 coins, 1.13M events, $32.3B notional);
- 4h candles fetchable with 0 gaps (1105 bars/coin);
- hourly funding fetchable by pagination (4776 rows/coin).

6 non-overlapping 30-day blocks, 9 instruments, disjoint from every sealed window.

Execute, in strict order:
1. Bounded 4h + funding acquisition with full provenance (no outcomes).
2. Freeze prereg BEFORE any outcome computation (`C2_vs_B1`, QLIKE, ≥3 blocks, ≥5 instruments, 7-d embargo, block bootstrap ≥2000, Holm across the declared family).
3. Deterministic panel build with hashes, coverage, missingness, reason-coded exclusions.
4. Pre-registered evaluation + explicit PASS/NOT_MET verdict; atomic state updates under a NEW experiment ID.
5. If negative, continue to power/coverage audit and the 2024-08..2025-04 extension feasibility question — do not stop.

Gate 4 Branch 1 only on a valid `fclr016_v5_terms_evidence_RESOLVED_<UTC>.json`
(`status=RESOLVED_VERIFIED`, `fabricated=false`, human/legal attestation). Absent now;
do not poll. The `RESOLVED_VERIFIED` string inside the fclr020 readiness matrix is **not** a trigger.