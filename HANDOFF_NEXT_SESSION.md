# HANDOFF: Next Agentic Work Session — SINGLE DURABLE HANDOFF
**Repo:** `Funding-conditioned-volatility-and-liquidation-risk`
**Timestamp (UTC, authoritative):** 2026-11-11T13:30:14Z
**Status:** AUTHORITATIVE. This is the only task message to execute. `FOCUS_CAMPAIGN.md` and `NEXT_SESSION_TASK.md` must point here. `AGENT_HANDOFF.md` is a redirect only. Any other doc claiming Track A closed without a verdict artifact or conflicting with this handoff is stale. Read fully before acting. **No status-only output.**

## INITIAL TASK MESSAGE (EXECUTE NOW) — 2026-11-11T13:30:14Z

**Mission (repo-prioritized):** `Funding-conditioned-volatility-and-liquidation-risk` requires **liquidation-risk forecasting** co-equal with volatility forecasting. **Track A (observed Hyperliquid liquidations, ironflow CC BY 4.0, unauthenticated)** is the only computable, unblocked path and is the **mandatory heavy campaign this session**. **Terminalize Track A this session** via Path (b) or Path (c) below. Do not stop at probing/audits/status.

**Gate 4 / Track C (Binance 2025+ volatility extension): EXTERNAL BLOCKER — `EXPLICIT_BLOCKER_UNRESOLVED` (human/legal terms evidence).** Cannot be automated/fabricated. **Deprioritize entirely** except the strict conditional rule below.

---

### Verified state (do not relitigate)
- **Track A path (a) COMPLETE:** `research_state/tracka_alignment_patha_audit_20261111T125022Z.md`. Frozen prereg window `2025-06..2026-10` is **NOT buildable** from admissible cached evidence.
  - Labels (ironflow, observed only): `2025-05..2026-10` parquets cached in `research_state/data_cache/ironflow_events/` (complete `2025-06..2026-10`).
  - Funding (HL `fundingHistory`, cached): `2025-11-01T00:00:00Z..2026-10-30T23:00:00Z` (`research_state/data_cache/hyperliquid_funding/*.json`, 9 coins).
  - Mark/OHLCV (`candleSnapshot` 1h probe): usable `~2026-05..2026-10` (2026-04 partial; minor probe gaps/errors) — `research_state/hl_pathb_probe_20261111T122801Z.json`. No separate historical index/premium series cached.
  - **Maximal aligned overlap:** **`2026-05-01..2026-10-31` (6 months).** Path (a) CLOSED.
- **Frozen prereg (UNEXECUTED, do not compute outcomes under it):** `research_state/tracka_prereg_hyperliquid_2026.json` (`TRACKA-HL-20261111T073000Z`, `PREREGISTERED_FROZEN_PRE_OUTCOMES`).
- **No successor prereg and no Track A evaluation summary/verdict exist yet** — must be produced this session.
- **Track B/C confirmatory (2024):** closed negative / sealed immutable (`H001 NOT_SUPPORTED`, historical). **Do not relitigate or reuse sealed holds.**
- **Gate 4:** `research_state/fclr016_local_audit/fclr016_v5_terms_evidence_BLOCKED_20261108T014835Z.json` (`EXPLICIT_BLOCKER_UNRESOLVED`, `fabricated=false`). Agents must NOT set `RESOLVED_VERIFIED` or fabricate.

---

### Required heavy work — TERMINALIZE TRACK A (Path b or c)

#### Path (b) — SUCCESSOR PREREG + EVALUATION (preferred if claim-worthy on admissible overlap)
1. **Freeze before outcomes:** create `research_state/tracka_prereg_hyperliquid_successor_<UTC>.json` (`TRACKA-HL-S-<UTC>`):
   - Hyperliquid/ironflow observed labels only; no Binance/2024 conflation; no modeled/proxy/synthetic labels.
   - Window **`2026-05-01..2026-10-31`** (or tighter justified subset) with exact UTC bounds.
   - Symbols from admissible overlap (candidate 9: BTC,ETH,BNB,SOL,XRP,AVAX,DOGE,LINK,SUI; map to `*-PERP` in ironflow) with explicit inclusion/exclusion rules.
   - Label: observed ironflow liquidation intensity (e.g. `notional_usd`-weighted event count per symbol per 24h UTC bucket) — document aggregation.
   - Features/context & provenance from cached admissible sources only (funding JSONs, candle probe/available cached data, labels); record source paths and SHA256 checksums of every input artifact.
   - Chronological splits with **≥7d embargo**; state feasibility/justification for **≥3 non-overlapping test blocks** and **min paired instruments**. If minima cannot be met, mark not claim-worthy and take Path (c). No threshold-shopping.
   - Primary contrast/metric (e.g. QLIKE C2 vs B1 or justified), materiality/decision rules. Status frozen pre-outcomes.
2. **Build aligned panel** deterministically from cached admissible inputs only (no redundant network polling). Save panel/build artifacts under `research_state/` with hashes, row/coverage counts, and missingness/gap report.
3. **Run pre-registered evaluation** per successor prereg. Perform leakage/embargo checks. Emit `research_state/evaluation_summary_TRACKA-HL-<successor_id>.md` with results, diagnostics/uncertainty as pre-registered, and explicit verdict.
4. **Update state atomically:** `research_state/experiment_frontier.json`, `research_state/hypothesis_registry.json`, `research_state/run_manifest.json`, and add Track A addendum/verdict to `research_state/final_confirmatory_verdict.md` (do not erase historical 2024 H001 record).

#### Path (c) — TERMINAL CLOSURE (if overlap cannot satisfy minimum prereg/test requirements)
1. Emit `research_state/evaluation_summary_TRACKA-HL-terminal-<UTC>.md` closing Track A as `NOT_SUPPORTED` or `BLOCKED` (as evidenced) citing `tracka_alignment_patha_audit_20261111T125022Z.md`, `hl_pathb_probe_20261111T122801Z.json`, funding/candle ranges, and unmet minima on `2026-05-01..2026-10-31`.
2. **Update state atomically** (frontier/registry/manifest/final verdict addendum) to terminal state with evidence pointers.

**Acceptance:** a new `evaluation_summary_TRACKA-HL-*` verdict artifact + consistent state updates exist. Anything less is incomplete.

---

### Gate 4 rule (conditional only)
Keep BLOCKED; no bypass/fabrication/`RESOLVED_VERIFIED` by agents. **Only if** a valid `research_state/fclr016_local_audit/fclr016_v5_terms_evidence_RESOLVED_<UTC>.json` appears with all 8 verifiable fields, `fabricated=false`, `status=RESOLVED_VERIFIED`, and human/legal reviewer: run deterministic promotion then `--expect-go` validators; only on all-green GO execute confirmatory Track C multi-split ablation (≥7d purge/embargo, train-only normalization, block bootstrap ΔQLIKE CIs) with frozen artifacts. Otherwise do **not** touch Gate 4.

### Hard bans
- No outcome inspection before successor prereg freeze.
- No Binance/2024 conflation (Hyperliquid only, admissible overlap).
- No modeled/proxy/synthetic liquidation labels (observed ironflow only).
- No threshold-shopping; no sealed-holdout reuse; no `.github/workflows` edits.
- No redundant network polling (use cached provenance/artifacts).
- No agent-set `RESOLVED_VERIFIED` / `fabricated=true`.
- No status-only output without a Track A verdict artifact (or newly valid resolved terms artifact + executed promotion chain).

### Bottleneck removal (current)
- Single durable handoff enforced (`HANDOFF_NEXT_SESSION.md`); `AGENT_HANDOFF.md` redirect; campaign/task pointers aligned.
- Track A path (a) ambiguity removed; overlap fixed to `2026-05-01..2026-10-31`; only path (b)/(c) forward.
- Gate 4 isolated to prevent spin. Track B/C 2024 closed & sealed.

### Key refs
- Track A: `research_state/tracka_prereg_hyperliquid_2026.json`, `research_state/tracka_alignment_patha_audit_20261111T125022Z.md`, `research_state/tracka_hl_alignment_blocker.md`, `research_state/hl_pathb_probe_20261111T122801Z.json`, `research_state/data_cache/ironflow_events/`, `research_state/data_cache/hyperliquid_funding/`, `src/analysis/tracka_admissible.py`, `scripts/hyperliquid_funding_fetch.py`, `scripts/tracka_hl_pathb_probe.py`
- Gate 4: `research_state/fclr016_local_audit/fclr016_v5_*`, `scripts/fclr016_v5_preflight_summary.py`, `scripts/fclr016_validate_v5_admissibility.py`
- Baseline checks: `python -m unittest discover -s tests -v` (as relevant)

**End of Handoff — Execute the INITIAL TASK MESSAGE now. Terminalize Track A this session.**
