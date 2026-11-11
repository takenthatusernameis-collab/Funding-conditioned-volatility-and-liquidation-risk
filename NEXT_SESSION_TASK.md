# NEXT_SESSION_TASK — 2026-11-11T18:51:48Z
**Execute:** `HANDOFF_NEXT_SESSION.md` (single durable handoff, authoritative). Do not execute `AGENT_HANDOFF.md`.

## Immediate objectives (heavy, no status-only)
- **Branch 1 (CONDITIONAL):** only on valid Gate 4 `RESOLVED` terms artifact (all 8 fields, `fabricated=false`, human/legal verified) run deterministic promotion + `--expect-go` validators → on all-green GO execute confirmatory Track C multi-split ablation and emit verdict + atomic state updates. **Currently absent → BLOCKED.**
- **Branch 2 (DEFAULT, PRIORITY): `GAP-TRACKA-EARLY-OBSERVED-2025H2_2026Q1`** — freeze prereg BEFORE outcomes (new early HL observed-liquidation claim, 9 coins, ironflow + cached funding ~2025-11-01..2026-04, candles missing) disjoint from NOT_MET 2026-05..2026-10; bounded first-time unauthenticated candleSnapshot acquisition with provenance for missing months only (no re-fetch 2026-05..2026-10); build deterministic RV panel; run pre-registered evaluation; emit verdict + atomic state updates. If infeasible, document and pivot to `GAP-TRACKA-SYMBOL-EXPANSION-2026M05M10`.

## Known facts (verified 2026-11-11T18:51:48Z)
- Gate 4 unresolved (no RESOLVED artifact). HL candles cached only 2026-05..2026-10; funding ~2025-11-01..2026-10-30 (9 coins); ironflow 2025-05..2026-10.
- Track A 2026-05..2026-10 NOT_MET (closed).

Obey all hard bans in `HANDOFF_NEXT_SESSION.md`.
