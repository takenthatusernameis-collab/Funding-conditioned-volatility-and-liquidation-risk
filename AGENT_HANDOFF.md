# AGENT_HANDOFF (superseded redirect — do not execute)

**Timestamp (UTC):** 2026-11-12T11:38:00Z

**Authoritative single durable handoff: `HANDOFF_NEXT_SESSION.md`. Read and execute it only.**

The prior handoff (2026-11-12T09:51:12Z) declared a "timestamped evidenced clean stop."
That stop was **wrong**. A powered, never-used, fully admissible Hyperliquid panel exists:

- Observed labels cached 2025-05..2025-10 (9 coins, 1.13M events).
- 4h candles fetchable 2025-05-01..2025-11-15 (0 gaps) — the earlier "no candles"
  conclusion came from probing **1h**, which Hyperliquid only serves from 2026-04-18.
- Hourly funding fetchable over the same window by pagination.

That window is 6 non-overlapping 30-day blocks and is disjoint from every sealed
experiment. It requires no Gate 4, no new source, and no future data.

Do not follow the 09:51 clean stop. Do not re-probe 1h candles to conclude "no early
data." Execute campaign `FCLR-EARLY4H-2025H1-HEAVY` in `HANDOFF_NEXT_SESSION.md`.