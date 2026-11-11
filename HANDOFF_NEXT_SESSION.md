# HANDOFF: Next Agentic Work Session — SINGLE DURABLE HANDOFF
**Repo:** `Funding-conditioned-volatility-and-liquidation-risk`
**Timestamp (UTC, this update):** 2026-11-11T12:58:01Z
**Authoritative:** This file is the only task message to execute. `FOCUS_CAMPAIGN.md` and `NEXT_SESSION_TASK.md` must point here. Read this entire file before any action. No status-only output.

## INITIAL TASK MESSAGE (execute now) — 2026-11-11T12:58:01Z

**Mission (repo-prioritized):** advance funding-conditioned **volatility** forecasting and **liquidation-risk** forecasting. The repo name makes liquidation-risk forecasting co-equal with volatility forecasting; Track A (observed Hyperliquid liquidations, ironflow CC BY 4.0) is the only path that is not externally blocked and is the heavy mandatory campaign this session. Terminalize Track A this session; do not stall.

---

### Verified state (inferred from research_state; do not relitigate closed items)

- **Track A path (a) audit COMPLETE:** `research_state/tracka_alignment_patha_audit_20261111T125022Z.md`. Full frozen prereg window `2025-06..2026-10` is **NOT buildable**. Labels complete `2025-06..2026-10`; funding admissible only `2025-11-01T00:00:00Z..2026-10-30T23:00:00Z`; mark/OHLCV candles admissible only `~2026-05..2026-10` (2026-04 partial, AVAX 2026-09 HTTP 429, BNB 2026-06 in probe); no separate historical index/premium series cached. **Maximal aligned overlap: `2026-05-01..2026-10-31` (6 months).** Path (a) CLOSED with evidence. Do not execute frozen prereg `TRACKA-HL-20261111T073000Z`.
- **Frozen prereg** `research_state/tracka_prereg_hyperliquid_2026.json` remains `PREREGISTERED_FROZEN_PRE_OUTCOMES` and **UNEXECUTED**.
- **Gate 4 / Track C volatility extension (2025+ Binance):** `EXPLICIT_BLOCKER_UNRESOLVED`. `research_state/fclr016_local_audit/fclr016_v5_terms_evidence_BLOCKED_20261108T014835Z.json` (status `EXPLICIT_BLOCKER_UNRESOLVED`, `fabricated=false`, `confirmatory_claim_go=NO_GO`) and the `UNRESOLVED` draft both require human/legal terms review with all 8 verifiable fields. Agents must NOT set `RESOLVED_VERIFIED`, `fabricated=true`, or bypass. Remain explicitly BLOCKED this session.
- **Track B/C confirmatory (2024):** closed negative (`H001 NOT_SUPPORTED`, sealed holds immutable). Do not relitigate.

---

### Required action — TERMINALIZE TRACK A THIS SESSION via path (b) or (c). Pick one and record it.

**Path (b) — preferred if claim-worthy (successor prereg then evaluate):**
1. Freeze `research_state/tracka_prereg_hyperliquid_successor_<UTC>.json` **BEFORE any outcome computation** on overlap `2026-05-01..2026-10-31` (9 symbols `*-PERP`: BTC/ETH/BNB/SOL/XRP/AVAX/DOGE/LINK/SUI), documenting: exact window; label definition (observed ironflow `notional_usd`-weighted per symbol per 24h UTC); required context fields & provenance; 7d embargo; chronological splits; feasibility of ≥3 non-overlapping test blocks / min paired instruments (or explicitly mark not claim-worthy); primary contrast/metric (QLIKE C2 vs B1 or justified); SHA256/checksums of all input artifacts used.
2. Build aligned panel from cached admissible inputs only; record panel hash/row counts.
3. Run pre-registered evaluation; emit `research_state/evaluation_summary_TRACKA-HL-<successor_id>.md` with results, leakage/embargo checks, and verdict.
4. Update `research_state/experiment_frontier.json`, `research_state/hypothesis_registry.json`, `research_state/run_manifest.json`, and `research_state/final_confirmatory_verdict.md` **atomically** to reflect terminal outcome.

**Path (c) — if overlap cannot satisfy minimum prereg/test requirements:**
1. Emit terminal verdict artifact `research_state/evaluation_summary_TRACKA-HL-terminal-<UTC>.md` closing Track A panel as `NOT_SUPPORTED`/`BLOCKED` with evidence (cite path-a audit + probe/funding ranges) and explicit reason (insufficient aligned test blocks/context).
2. Update frontier/registry/manifest/final verdict atomically.

---

### Gate 4 this session
Keep explicitly BLOCKED; no bypass/fabrication/`RESOLVED_VERIFIED` by agents. If and only if a valid `research_state/fclr016_local_audit/fclr016_v5_terms_evidence_RESOLVED_<UTC>.json` appears (all 8 fields, `fabricated=false`, `status=RESOLVED_VERIFIED`, human/legal reviewer), run deterministic promotion then `--expect-go` validators, and only on all-green GO execute confirmatory Track C multi-split ablation (≥7d purge/embargo, train-only normalization, block bootstrap ΔQLIKE CIs) with frozen evaluation artifacts. Otherwise proceed to Track A as the computable campaign.

---

### Constraints / hard bans (apply to all work)
- No outcome inspection before successor prereg freeze.
- No Binance/2024 conflation (Hyperliquid only, admissible overlap).
- No modeled/proxy/synthetic labels (observed ironflow events only).
- No threshold-shopping; no sealed-holdout reuse; no `.github/workflows` edits.
- No redundant network polling (use cached provenance).
- No agent-set `RESOLVED_VERIFIED` / `fabricated=true` on terms evidence.
- No status-only output without a verdict artifact or resolved terms artifact.

---

### Bottleneck removal
- Track C/Gate 4 is externally blocked (human/legal terms; cannot be automated or fabricated). **Deprioritize it entirely this session** so the agent does not spin; proceed to Track A as the computable campaign.
- Track A path (a) ambiguity is removed by the audit; the next agent must execute path (b) or (c) to a terminal state this session.

---

### Key refs
- Track A: `research_state/tracka_prereg_hyperliquid_2026.json`, `research_state/tracka_alignment_patha_audit_20261111T125022Z.md`, `research_state/tracka_hl_alignment_blocker.md`, `research_state/hl_pathb_probe_20261111T122801Z.json`, `research_state/data_cache/ironflow_events/`, `research_state/data_cache/hyperliquid_funding/`, `src/analysis/tracka_admissible.py`, `scripts/hyperliquid_funding_fetch.py`, `scripts/tracka_hl_pathb_probe.py`
- Gate 4: `research_state/fclr016_local_audit/fclr016_v5_*`, `scripts/fclr016_v5_preflight_summary.py`, `scripts/fclr016_validate_v5_admissibility.py`
- Baseline checks: `python -m unittest discover -s tests -v`

**End of Handoff — Next Agent Must Read This Entire File Before Any Action**
