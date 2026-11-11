# FOCUS_CAMPAIGN — 2026-11-11T18:51:48Z
**Single durable handoff (authoritative):** `HANDOFF_NEXT_SESSION.md` — execute it. `AGENT_HANDOFF.md` is a redirect.

## Active campaign (heavy, inescapable)
1. **Branch 1 (CONDITIONAL):** If valid `research_state/fclr016_local_audit/fclr016_v5_terms_evidence_RESOLVED_<UTC>.json` appears (`fabricated=false`, `status=RESOLVED_VERIFIED`, human/legal attestation, all 8 fields) → deterministic promotion/`--expect-go` validators → on all-green GO run confirmatory Track C multi-split ablation and emit verdict + atomic state updates. **Verified absent 2026-11-11T18:51:48Z → Gate 4 BLOCKED.**
2. **Branch 2 (DEFAULT, PRIORITY): `GAP-TRACKA-EARLY-OBSERVED-2025H2_2026Q1`** — freeze prereg BEFORE outcomes for new early Hyperliquid observed-liquidation claim (9 coins; ironflow labels + cached funding ~2025-11-01..2026-04 overlap; candles missing for that window), disjoint from NOT_MET 2026-05..2026-10; bounded first-time unauthenticated candleSnapshot acquisition with provenance for missing months only (no re-fetch 2026-05..2026-10); build deterministic RV panel; run pre-registered evaluation (C2 vs B1, embargo/blocks/bootstrap per prereg); emit verdict + atomic state updates. If infeasible, emit documented infeasibility and pivot to `GAP-TRACKA-SYMBOL-EXPANSION-2026M05M10`.

## Closed / do not relitigate
- Track A `TRACKA-HL-S-20261111T133430Z` (2026-05..2026-10): **NOT_MET**.
- Track B/C confirmatory (2024): closed negative. Sealed holds immutable.

## Hard bans
No outcome inspection before freeze; no Binance/2024 conflation; no modeled/proxy labels as observed; no threshold-shopping; no sealed-holdout reuse; no `.github/workflows` edits; no redundant polling (bounded first-time acquisition allowed); no agent-set `RESOLVED_VERIFIED`/`fabricated=true`; no status-only output.
