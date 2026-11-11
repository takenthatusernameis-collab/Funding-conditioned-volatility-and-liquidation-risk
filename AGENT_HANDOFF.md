# AGENT_HANDOFF — Funding-conditioned-volatility-and-liquidation-risk
**Single durable handoff for agentic continuity**
**Timestamp (UTC):** 2026-11-11T09:23:05Z
**Authoritative source:** `HANDOFF_NEXT_SESSION.md` (this file mirrors its intent)

## Current state
- **Active track:** Track A only (observed Hyperliquid liquidations via ironflow/hyperliquid-liquidations, CC BY 4.0).
- **Status:** Prereg frozen (`TRACKA-HL-20261111T073000Z`) but **blocked** — full 2025-06..2026-10 aligned panel not buildable from admissible HL-native sources.
- **Blocker evidence:** `research_state/tracka_hl_alignment_blocker.md` — HL fundingHistory covers 2025-11..2026-10 only; candleSnapshot (mark 1h) covers ~2026-05..2026-10 only; no admissible index/premium endpoint.
- **Tracks B/C:** Closed, NOT_SUPPORTED.

## Next session must do (in order)
1. **Verify prereg freeze** — confirm `research_state/tracka_prereg_hyperliquid_2026.json` has `frozen_before_outcomes: true`, no outcome inspection.
2. **Exhaust path (a)** — search local cache/repo for any overlooked admissible HL-native source covering 2025-06..2026-10; probe `scripts/hl_coverage_probe.py`, `scripts/hyperliquid_funding_fetch.py`; if none found, declare path (a) exhausted with evidence.
3. **Choose and execute terminal path**:
   - **(b) Scope-down + re-prereg** if viable overlap exists (~2026-05..2026-10): write successor prereg `tracka_prereg_hyperliquid_2026_scoped.json` (frozen pre-outcomes) → build aligned panel → run pre-reg evaluation → write verdict artifact.
   - **(c) Terminal closure** if (a) exhausted and (b) infeasible: write `evaluation_summary_TRACKA-HL-20261111T073000Z.md` with NOT_SUPPORTED/INCONCLUSIVE_CLOSED_DUE_TO_ALIGNMENT_DATA_INADMISSIBILITY, update frontier/registry/manifest/final verdict atomically.
4. **Update canonical state** — experiment_frontier.json, hypothesis_registry.json, run_manifest.json, final_confirmatory_verdict.md.

## What was tested/evidenced
- Ironflow labels: 2,848,413 rows, 2025-05..2026-10, 468 markets, 9 funded symbols as *-PERP — **GO**.
- HL fundingHistory: 8,668 rows/symbol, 2025-11..2026-10 — **gap 2025-06..2025-10**.
- HL candleSnapshot (mark 1h): ~169 rows/month from 2026-05 onward — **gap 2025-06..2026-04**.
- No admissible HL index/premium historical endpoint found.
- Frozen prereg splits (train/val/test with 7d embargo) **not executable** on full panel.

## Next actionable verification
- `python scripts/check_tracka_scope_registry_drift.py --json`
- `python -m unittest tests.test_volatility_features_splits tests.test_synthetic_boundary_labels tests.test_trackc_panel_admissibility_audit tests.test_trackc_funding_schema_audit tests.test_trackc_provenance_lineage -v`

## Blocker + next free route
- **Blocker:** No admissible HL-native mark/index/premium/funding covering 2025-06..2026-10.
- **Route:** Exhaust local probe (path a); if no new source, scope-down to maximal overlap (path b) with full re-prereg, or close (path c). No Binance conflation, no modeled labels, no holdout reuse.