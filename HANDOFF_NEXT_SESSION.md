# HANDOFF: Next Agentic Work Session — SINGLE DURABLE HANDOFF
**Repo:** `Funding-conditioned-volatility-and-liquidation-risk`
**Timestamp (UTC, this update):** 2026-11-11T12:50:22Z
**Authoritative:** This file is the only task message to execute. `FOCUS_CAMPAIGN.md` and `NEXT_SESSION_TASK.md` must point here. Read this entire file before any action. No status-only output.

## INITIAL TASK MESSAGE (execute now)
**Mission (repo-prioritized):** advance (1) funding-conditioned **volatility** forecasting and (2) **liquidation-risk** forecasting. Do heavy, terminalizing work; do not stall.

### 1) Gate 4 / Track C volatility extension (2025+ Binance) — EXTERNALLY BLOCKED
- **Status:** `EXPLICIT_BLOCKER_UNRESOLVED` (license/terms). Deterministic artifacts green except human/legal terms: needs `research_state/fclr016_local_audit/fclr016_v5_terms_evidence_RESOLVED_<UTC>.json` (all 8 fields, `fabricated=false`, `status=RESOLVED_VERIFIED`, human/legal reviewer). Fail-closed guards block confirmatory 2025+ outcomes.
- **This session:** keep explicitly BLOCKED; **no bypass/fabrication/`RESOLVED_VERIFIED`**. If and only if a valid resolved terms artifact appears, run deterministic promotion then `--expect-go` validators, and only on all-green GO execute confirmatory Track C multi-split ablation (≥7d purge/embargo, train-only normalization, block bootstrap ΔQLIKE CIs) with frozen evaluation artifacts. Otherwise proceed to Track A.

### 2) Track A liquidation-risk (observed Hyperliquid, ironflow CC BY 4.0) — PRIMARY COMPUTABLE CAMPAIGN (heavy, mandatory)
- **Frozen prereg (do not execute):** `research_state/tracka_prereg_hyperliquid_2026.json` (`TRACKA-HL-20261111T073000Z`, 2025-06..2026-10, C2 vs B1, QLIKE). Full window **NOT buildable**.
- **Path (a) CLOSED with evidence (2026-11-11T12:50:22Z):** `research_state/tracka_alignment_patha_audit_20261111T125022Z.md`.
  - Labels (ironflow, cached): complete 2025-06..2026-10, 9 funded symbols.
  - Funding (HL `fundingHistory`, cached): **2025-11-01T00:00:00Z..2026-10-30T23:00:00Z** only.
  - Candles (HL `candleSnapshot` probe `hl_pathb_probe_20261111T122801Z.json`): **~2026-05..2026-10** usable (2026-04 partial), 2025-06..2026-03 absent; no separate admissible historical index/premium series cached.
  - **Maximal admissible overlap (labels+funding+candles): 2026-05-01..2026-10-31 (6 months).** No additional admissible local HL-native historical context found.

**You must terminalize Track A this session via path (b) or (c):**

**Path (b) — preferred if claim-worthy (successor prereg then evaluate):**
1. Freeze `research_state/tracka_prereg_hyperliquid_successor_<UTC>.json` **BEFORE any outcome computation** on overlap (e.g. 2026-05-01..2026-10-31, 9 symbols BTC/ETH/BNB/SOL/XRP/AVAX/DOGE/LINK/SUI as `*-PERP`), documenting: exact window, label definition (observed ironflow notional_usd-weighted per symbol per 24h UTC), required context fields & provenance, 7d embargo, chronological splits, feasibility of ≥3 non-overlapping test blocks / min paired instruments (or explicitly mark not claim-worthy), primary contrast/metric (QLIKE C2 vs B1 or justified), and SHA256/checksums of all input artifacts used.
2. Build aligned panel from cached admissible inputs only; record panel hash/row counts.
3. Run pre-registered evaluation; emit `research_state/evaluation_summary_TRACKA-HL-<successor_id>.md` with results, leakage/embargo checks, and verdict.
4. Update `research_state/experiment_frontier.json`, `research_state/hypothesis_registry.json`, `research_state/run_manifest.json`, and `research_state/final_confirmatory_verdict.md` (or final verdict artifact as appropriate) **atomically** to reflect terminal outcome.

**Path (c) — if overlap cannot satisfy minimum prereg/test requirements:**
1. Emit terminal verdict artifact `research_state/evaluation_summary_TRACKA-HL-terminal-<UTC>.md` closing Track A panel as `NOT_SUPPORTED`/`BLOCKED` with evidence (cite path-a audit + probe/funding ranges) and explicit reason (insufficient aligned test blocks/context).
2. Update frontier/registry/manifest/final verdict atomically.

**Constraints:** no outcome inspection before successor prereg freeze; no Binance/2024 conflation; no modeled/proxy/synthetic labels; no threshold-shopping; no sealed-holdout reuse; no `.github/workflows` edits; no redundant network polling (use cached provenance).

## Hard state / do-not-relitigate
- Track B/C confirmatory (2024 Binance): closed/negative — `research_state/final_confirmatory_verdict.md` (H001 NOT_SUPPORTED). Sealed holds immutable.
- Gate 4 confirmatory 2025+: blocked on human/legal terms only (external).
- Track A frozen prereg infeasible on full window; path (a) complete.

## Key refs
- Track A: `research_state/tracka_prereg_hyperliquid_2026.json`, `research_state/tracka_alignment_patha_audit_20261111T125022Z.md`, `research_state/tracka_hl_alignment_blocker.md`, `research_state/hl_pathb_probe_20261111T122801Z.json`, `research_state/data_cache/ironflow_events/`, `research_state/data_cache/hyperliquid_funding/`, `src/analysis/tracka_admissible.py`, `scripts/hyperliquid_funding_fetch.py`, `scripts/tracka_hl_pathb_probe.py`
- Gate 4: `research_state/fclr016_local_audit/fclr016_v5_*`, `scripts/fclr016_v5_preflight_summary.py`, `scripts/fclr016_validate_v5_admissibility.py`
- Baseline checks: `python -m unittest discover -s tests -v`

**End of Handoff — Next Agent Must Read This Entire File Before Any Action**
