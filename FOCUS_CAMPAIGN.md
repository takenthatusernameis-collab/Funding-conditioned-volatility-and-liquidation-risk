# FOCUS_CAMPAIGN — 2026-11-11T13:45:00Z
**Single durable handoff (authoritative):** `HANDOFF_NEXT_SESSION.md` — execute it. `AGENT_HANDOFF.md` is a redirect.

## Active campaign (heavy, inescapable)
1. **Track A liquidation-risk (PRIMARY, TERMINALLY CLOSED PATH (c) — re-open only via bottleneck removal):** Observed Hyperliquid liquidations (ironflow). **This session terminalized Track A as NOT_SUPPORTED** (verdict `evaluation_summary_TRACKA-HL-terminal-20261111T133430Z.md`).
   - **Binding bottleneck (REMOVE IT):** mark-price/RV context for `2026-05-01..2026-10-31` not cached; live unauthenticated Hyperliquid `candleSnapshot` confirmed available (~720-744 rows/month, 9 coins). **First-time acquisition (not redundant polling) → cache candles → rebuild aligned panel → execute pre-registered successor C2 vs B1 evaluation → emit `evaluation_summary_TRACKA-HL-*` verdict + atomic state updates.** This is the heavy, inescapable work. Future agents must not skip it.
   - If RV fetch attempted and minima still unmet → emit documented Path (c) terminal closure `evaluation_summary_TRACKA-HL-terminal-<UTC>.md` + atomic closure.

2. **Gate 4 / Track C volatility (EXTERNAL-BLOCKED):** Human/legal Binance terms evidence required; keep BLOCKED, no bypass/fabrication. Act only on valid resolved terms artifact → deterministic reconcile + `--expect-go` validators → confirmatory multi-split ablation.

## Closed / do not relitigate
- Track B/C confirmatory (2024): closed negative (H001 NOT_SUPPORTED). Sealed holds immutable.
- Track A original frozen prereg `TRACKA-HL-20261111T073000Z`: superseded by successor prereg; Path (a) closed (full 2025-06..2026-10 panel not buildable).

## Hard bans
No outcome inspection before freeze; no Binance/2024 conflation; no modeled/proxy labels; no threshold-shopping; no sealed-holdout reuse; no `.github/workflows` edits; no redundant network polling (bounded first-time candle acquisition excepted); no agent-set `RESOLVED_VERIFIED`/`fabricated=true`; no status-only output without a Track A verdict artifact (or valid resolved terms + executed promotion chain).

## Bottleneck removal (current)
- Single durable handoff enforced (`HANDOFF_NEXT_SESSION.md`); `AGENT_HANDOFF.md` redirect; campaign/task pointers aligned.
- Track A path (a) ambiguity removed; overlap fixed `2026-05-01..2026-10-31`; Path (b)/(c) forward.
- **Binding bottleneck removed-pending-execution:** acquire cached mark-price/RV context for `2026-05-01..2026-10-31` via bounded unauthenticated `candleSnapshot` fetch, then complete Track A evaluation. Gate 4 isolated to prevent spin. Track B/C 2024 closed & sealed.
