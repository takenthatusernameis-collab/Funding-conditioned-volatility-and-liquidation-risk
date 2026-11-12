# NEXT_SESSION_TASK (redirect)
**Timestamp (UTC):** 2026-11-12T06:27:01Z

Execute **`HANDOFF_NEXT_SESSION.md`** (single durable handoff, authoritative). Gate 4 Branch 1 only if valid RESOLVED trigger present (verified absent 2026-11-12T06:27:01Z). PRIMARY: 4h candles 2025-11..2026-04 cached+complete (`research_state/data_cache/hyperliquid_candles_4h/`) and prereg frozen (`tracka_prereg_hyperliquid_early_4h_20261112T054737Z`) — run `scripts/tracka_hl_build_early_4h_panel.py`, then evaluate pre-registered C2 vs B1 liquidation forecast + verdict + atomic state updates. If infeasible, emit timestamped evidence and advance. No status-only output.
