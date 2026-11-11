# NEXT_SESSION_TASK — 2026-11-11T18:46:47Z
**Execute:** `HANDOFF_NEXT_SESSION.md` (single durable handoff, authoritative). Do not execute `AGENT_HANDOFF.md`.

## Immediate objectives (heavy, no status-only)
- **Branch 1 — Gate 4 / Track C (CONDITIONAL):** only on valid `fclr016_v5_terms_evidence_RESOLVED_<UTC>.json` (human/legal, all 8 fields, `fabricated=false`, `RESOLVED_VERIFIED`) run deterministic promotion + `--expect-go` validators → on all-green GO execute confirmatory Track C multi-split ablation and emit verdict + atomic state updates. **Currently absent → Gate 4 BLOCKED.**
- **Branch 2 — DEFAULT PRIORITY `GAP-TRACKA-EARLY-OBSERVED-2025H2_2026Q1`:** freeze prereg BEFORE outcomes for new early Hyperliquid observed-liquidation claim (9 coins, ironflow labels + cached funding ~2025-11-01..2026-04, candles missing for that window); bounded first-time unauthenticated candleSnapshot acquisition with provenance for missing months only (no re-fetch 2026-05..2026-10); build deterministic RV panel + report; run pre-registered evaluation; emit verdict + atomic state updates. If infeasible, emit documented infeasibility and pivot to `GAP-TRACKA-SYMBOL-EXPANSION-2026M05M10`. Substantive artifacts required.

## Known facts (verified 2026-11-11T18:46:47Z)
- HL funding cached 9 coins ~2025-11-01T00:00Z..2026-10-30T23:00Z; candles cached only 2026-05..2026-10; ironflow 2025-05..2026-10.
- Track A 2026-05..2026-10 NOT_MET (closed). Gate 4 BLOCKED (no RESOLVED artifact; fabricated=false).
- Root raw 2024 clutter consolidated to `data/raw_legacy_2024q1_scattered/`.

Obey all hard bans in `HANDOFF_NEXT_SESSION.md`.
