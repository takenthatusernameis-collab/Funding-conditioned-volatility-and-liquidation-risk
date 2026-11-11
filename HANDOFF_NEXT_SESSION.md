# HANDOFF: Next Agentic Work Session — SINGLE DURABLE HANDOFF
**Repo:** `Funding-conditioned-volatility-and-liquidation-risk`
**Timestamp (UTC, authoritative):** 2026-11-11T13:26:16Z
**Status:** AUTHORITATIVE. This is the only task message to execute. `FOCUS_CAMPAIGN.md` and `NEXT_SESSION_TASK.md` must point here. `AGENT_HANDOFF.md` is a redirect only. Any other doc claiming “closeout complete”, “no work remains”, or conflicting Track A status is stale for Track A unless reconciled by artifacts produced under this handoff. Read this entire file before any action. **No status-only output.**

## INITIAL TASK MESSAGE (EXECUTE NOW) — 2026-11-11T13:26:16Z

**Mission (repo-prioritized, heavy):** The repo name `Funding-conditioned-volatility-and-liquidation-risk` makes **liquidation-risk forecasting co-equal with volatility forecasting**. **Track A (observed Hyperliquid liquidations, ironflow CC BY 4.0, unauthenticated)** is the only computable path not externally blocked and is the **mandatory heavy campaign this session**. **You must terminalize Track A this session** via path (b) or (c) below. Do not stop at analysis/probing/status.

**Gate 4 / Track C (Binance 2025+ volatility extension): EXPLICIT_BLOCKER_UNRESOLVED (human/legal terms evidence).** Cannot be automated or fabricated. **Deprioritize entirely this session** (no polling/spin) except the conditional branch in “Gate 4 rule” below.

---

### Verified state (do not relitigate)
- **Track A path (a) audit COMPLETE:** `research_state/tracka_alignment_patha_audit_20261111T125022Z.md`. Frozen prereg window `2025-06..2026-10` **NOT buildable** from admissible cached evidence.
  - Labels (ironflow, observed only): complete `2025-06..2026-10` (`research_state/data_cache/ironflow_events/`).
  - Funding (HL `fundingHistory`, cached): `2025-11-01T00:00:00Z..2026-10-30T23:00:00Z` (`research_state/data_cache/hyperliquid_funding/*.json`, 9 coins).
  - Mark/OHLCV (`candleSnapshot` 1h probe): usable `~2026-05..2026-10` (2026-04 partial; minor gaps/errors noted in `research_state/hl_pathb_probe_20261111T122801Z.json`). No separate historical index/premium series cached.
  - **Maximal aligned overlap:** `2026-05-01..2026-10-31` (6 months). Path (a) CLOSED with evidence.
- **Frozen prereg (UNEXECUTED, do not compute outcomes under it):** `research_state/tracka_prereg_hyperliquid_2026.json` (`TRACKA-HL-20261111T073000Z`, `PREREGISTERED_FROZEN_PRE_OUTCOMES`).
- **No successor prereg / no Track A evaluation summary exists yet** in `research_state/` (must be produced this session as part of terminalization).
- **Track B/C confirmatory (2024):** closed negative / sealed immutable (`H001 NOT_SUPPORTED`, `final_confirmatory_verdict.md` is historical for 2024 program). **Do not relitigate or reuse sealed holds.**
- **Gate 4 terms blocker:** `research_state/fclr016_local_audit/fclr016_v5_terms_evidence_BLOCKED_20261108T014835Z.json` (`EXPLICIT_BLOCKER_UNRESOLVED`, `fabricated=false`, `confirmatory_claim_go=NO_GO`). Agents must NOT set `RESOLVED_VERIFIED` or fabricate.

---

### Required heavy work — TERMINALIZE TRACK A THIS SESSION (choose path b or c, record choice with evidence)

#### Path (b) — SUCCESSOR PREREG + EVALUATION (preferred if claim-worthy on admissible overlap)
Execute in order; **freeze prereg BEFORE any outcome computation**:
1. **Design & freeze** `research_state/tracka_prereg_hyperliquid_successor_<UTC>.json` (e.g. `TRACKA-HL-S-<UTC>`):
   - Scope strictly Hyperliquid/ironflow observed labels only; no Binance/2024 conflation; no modeled/proxy/synthetic labels.
   - Window: `2026-05-01..2026-10-31` (or tighter justified subset) with exact UTC bounds.
   - Symbols: from funded/available overlap (candidate 9: BTC,ETH,BNB,SOL,XRP,AVAX,DOGE,LINK,SUI as `*-PERP` in ironflow) with explicit inclusion/exclusion rules.
   - Label definition: observed ironflow `notional_usd`-weighted liquidation event count per symbol per 24h UTC bucket (document aggregation).
   - Required context/features & provenance (funding, candle/mark/OHLCV as available from cached admissible sources); record SHA256/checksums and source paths of every input artifact used.
   - Chronological splits with **≥7d embargo**; specify feasibility/justification for **≥3 non-overlapping test blocks** and **min paired instruments** (or explicitly mark **not claim-worthy** → take path c). No threshold-shopping.
   - Primary contrast/metric (e.g. QLIKE C2 vs B1 or justified) and materiality/decision rules. Status must indicate frozen pre-outcomes.
2. **Build aligned panel** from cached admissible inputs only (no redundant network polling). Save deterministic build artifacts (panel path/hash, row/coverage counts, missingness/gap report) under `research_state/` with provenance.
3. **Run pre-registered evaluation** per successor prereg. Perform leakage/embargo checks. Emit `research_state/evaluation_summary_TRACKA-HL-<successor_id>.md` with full results, uncertainty/diagnostics as pre-registered, and explicit verdict.
4. **Update state atomically** to reflect terminal outcome: `research_state/experiment_frontier.json`, `research_state/hypothesis_registry.json`, `research_state/run_manifest.json`, and `research_state/final_confirmatory_verdict.md` (add Track A addendum/verdict dated now; do not erase historical 2024 H001 record).

#### Path (c) — TERMINAL CLOSURE (if overlap cannot satisfy minimum prereg/test requirements)
1. Emit `research_state/evaluation_summary_TRACKA-HL-terminal-<UTC>.md` closing Track A as `NOT_SUPPORTED` or `BLOCKED` (as evidenced) citing `tracka_alignment_patha_audit_20261111T125022Z.md`, `hl_pathb_probe_20261111T122801Z.json`, funding/candle ranges, and the specific unmet minima (test blocks/instruments/context completeness) on `2026-05-01..2026-10-31`.
2. **Update state atomically** (frontier/registry/manifest/final verdict addendum) to terminal state with pointers to evidence.

**Acceptance for “done this session”:** a new `evaluation_summary_TRACKA-HL-*` verdict artifact + consistent state updates exist (path b or c). Anything less is incomplete.

---

### Gate 4 rule (conditional, only if unblocked by valid evidence)
Keep BLOCKED; no bypass/fabrication/`RESOLVED_VERIFIED` by agents. **If and only if** a valid `research_state/fclr016_local_audit/fclr016_v5_terms_evidence_RESOLVED_<UTC>.json` appears with all 8 verifiable fields, `fabricated=false`, `status=RESOLVED_VERIFIED`, and human/legal reviewer: run deterministic promotion then `--expect-go` validators; only on all-green GO execute confirmatory Track C multi-split ablation (≥7d purge/embargo, train-only normalization, block bootstrap ΔQLIKE CIs) with frozen evaluation artifacts. Otherwise do **not** touch Gate 4 work.

---

### Hard bans
- No outcome inspection before successor prereg freeze.
- No Binance/2024 conflation (Hyperliquid only, admissible overlap).
- No modeled/proxy/synthetic liquidation labels (observed ironflow events only).
- No threshold-shopping; no sealed-holdout reuse; no `.github/workflows` edits.
- No redundant network polling (use cached provenance/artifacts).
- No agent-set `RESOLVED_VERIFIED` / `fabricated=true`.
- No status-only output without a Track A verdict artifact (or a newly valid resolved terms artifact + executed promotion chain).

### Bottleneck removal (applied/confirmed)
- `AGENT_HANDOFF.md` retired to redirect → single durable handoff is this file.
- `FOCUS_CAMPAIGN.md` / `NEXT_SESSION_TASK.md` aligned to this handoff.
- Track A path (a) ambiguity removed (audit complete, overlap fixed to `2026-05-01..2026-10-31`); path (b)/(c) is the only forward route.
- Gate 4 external blocker isolated/deprioritized to prevent spin.
- Track B/C 2024 closed & sealed; do not reopen.

### Key refs
- Track A: `research_state/tracka_prereg_hyperliquid_2026.json`, `research_state/tracka_alignment_patha_audit_20261111T125022Z.md`, `research_state/tracka_hl_alignment_blocker.md`, `research_state/hl_pathb_probe_20261111T122801Z.json`, `research_state/data_cache/ironflow_events/`, `research_state/data_cache/hyperliquid_funding/`, `src/analysis/tracka_admissible.py`, `scripts/hyperliquid_funding_fetch.py`, `scripts/tracka_hl_pathb_probe.py`
- Gate 4: `research_state/fclr016_local_audit/fclr016_v5_*`, `scripts/fclr016_v5_preflight_summary.py`, `scripts/fclr016_validate_v5_admissibility.py`
- Baseline checks (as relevant): `python -m unittest discover -s tests -v`

**End of Handoff — Execute the INITIAL TASK MESSAGE now. Terminalize Track A this session.**
