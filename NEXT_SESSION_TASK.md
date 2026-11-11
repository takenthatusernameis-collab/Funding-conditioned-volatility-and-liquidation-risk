# NEXT_SESSION_TASK — 2026-11-11T17:16:49Z
**Execute:** `HANDOFF_NEXT_SESSION.md` (single durable handoff, authoritative). Do not execute `AGENT_HANDOFF.md`.

## Immediate objectives (heavy, no status-only)
- **Audit DONE (this session):** `research_state/next_panel_gap_audit_20261111T163229Z.md|.json` — no outcomes computed.
- **Branch 1 — Gate 4 / Track C (CONDITIONAL, external-blocked):** only on valid `fclr016_v5_terms_evidence_RESOLVED_<UTC>.json` (human/legal, all 8 fields, `fabricated=false`, `RESOLVED_VERIFIED`) run deterministic promotion + `--expect-go` validators → on all-green GO execute confirmatory Track C multi-split ablation and emit verdict + atomic state updates. Otherwise keep BLOCKED.
- **Branch 2 — DEFAULT PRIORITY `GAP-TRACKA-EARLY-OBSERVED-2025H2_2026Q1`:** freeze prereg BEFORE outcomes for new early Hyperliquid observed-liquidation claim (9 coins, ironflow labels + cached funding, missing candles); bounded first-time unauthenticated candleSnapshot acquisition with provenance for missing months only (no re-fetch 2026-05..2026-10); build deterministic RV panel + report; run pre-registered evaluation; emit `evaluation_summary_*` verdict + atomic state updates. If infeasible, emit documented infeasibility and pivot to `GAP-TRACKA-SYMBOL-EXPANSION-2026M05M10` (frozen ex-ante rules). Substantive artifacts required.
- **Closed:** Track A `TRACKA-HL-S-20261111T133430Z` NOT_MET; Track B/C 2024 NOT_SUPPORTED; sealed holds immutable.

Obey all hard bans in `HANDOFF_NEXT_SESSION.md`.
