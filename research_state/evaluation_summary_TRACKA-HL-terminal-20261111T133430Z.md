# Track A Terminal Verdict — evaluation_summary_TRACKA-HL-terminal-20261111T133430Z.md

**Report ID:** TRACKA-HL-terminal-20261111T133430Z
**Timestamp (UTC):** 2026-11-11T13:34:30Z
**Experiment:** TRACKA-HL-S-20261111T133430Z (successor prereg)
**Prereg document:** `research_state/tracka_prereg_hyperliquid_successor_20261111T133430Z.json` (frozen pre-outcomes)
**Superseded prereg:** `research_state/tracka_prereg_hyperliquid_2026.json` (TRACKA-HL-20261111T073000Z)
**Verdict:** `NOT_SUPPORTED` — Track A panel terminal closure (context insufficient / claim-worthy minima unmet on cached admissible inputs)
**Path taken:** Path (c) — terminal closure. Path (b) panel build executed; pre-registered evaluation infeasible.

---

## 1. Determination

Track A (observed Hyperliquid perpetual liquidation-risk forecasting) is **terminally closed as NOT_SUPPORTED** for this session.

The successor prereg was frozen **before any outcome computation** (no outcome inspection before prereg freeze). The aligned panel was built deterministically from cached admissible inputs only (no redundant network polling, per the single durable handoff). The pre-registered primary contrast **C2 vs B1** requires a realized-volatility-only baseline (B1), which requires mark-price / 1h-candle / RV context. That context is **not present in the cached admissible inputs** (only `ironflow_events/*.parquet` labels and `hyperliquid_funding/*.json` funding are cached; no mark-price/klines/index/premium cache exists). Per the handoff rule "Build aligned panel deterministically from cached admissible inputs only (no redundant network polling)", B1 and C2 cannot be computed, so the pre-registered evaluation cannot execute.

Consequently the minimum claim-worthy test requirements are **unmet** (RV baseline not computable on cached inputs). No threshold-shopping, no sealed-holdout reuse, no Binance/2024 conflation, no modeled/proxy/synthetic labels. No outcome was computed.

## 2. Evidence chain (all pre-outcome, frozen)

| Artifact | Role | Key content |
|---|---|---|
| `research_state/tracka_prereg_hyperliquid_2026.json` | Original frozen prereg (superseded) | TRACKA-HL-20261111T073000Z; window 2025-06..2026-10; C2 vs B1 QLIKE; min 5 instruments, min 3 test blocks, 7d embargo |
| `research_state/tracka_alignment_patha_audit_20261111T125022Z.md` | Path (a) audit | Full 2025-06..2026-10 panel NOT buildable; maximal admissible overlap `2026-05-01..2026-10-31`; funding only 2025-11-01..2026-10-30; candles only ~2026-05..2026-10; no index/premium historical endpoint |
| `research_state/tracka_hl_alignment_blocker.md` | Alignment blocker | Mark price missing 2025-06..2026-04; funding missing 2025-06..2025-10; no admissible unauthenticated index/premium endpoint; full prereg splits not executable |
| `research_state/hl_pathb_probe_20261111T122801Z.json` | Path (b) probe | Candle/funding overlap confirmed ~2026-05..2026-10; 9 funded coins present; minor probe gaps (AVAX 2026-09 429, BNB 2026-06 429, SUI funding 2026-07 429) |
| `research_state/tracka_prereg_hyperliquid_successor_20261111T133430Z.json` | Successor prereg (this session) | Window 2026-05-01..2026-10-31; 9 *-PERP symbols; input SHA256 checksums recorded; splits frozen pre-outcomes; feasibility assessed pre-outcomes |
| `research_state/tracka_hl_aligned_panel_20261111T133430Z.parquet` | Aligned panel (built this session) | sha256 `7a7c431bfd9fc66d34e4a9306e06d5f4847249950c0496a768f7d0c987197eda`; 1656 buckets (9 symbols × 184 days) |
| `research_state/tracka_hl_panel_build_report_20261111T133430Z.json` | Panel build report | 1434/1656 buckets with label (86.6%), 1656/1656 with funding (100%), all 9 symbols with label, 222 buckets missing label, 0 missing funding |
| `research_state/fclr016_local_audit/fclr016_v5_terms_evidence_BLOCKED_20261108T014835Z.json` | Gate 4 | EXPLICIT_BLOCKER_UNRESOLVED, fabricated=false (unchanged; not acted on) |

### Panel metrics (cached-input build)
- Total symbol×24h buckets: 1656
- Buckets with liquidation label: 1434 (86.6%)
- Buckets with funding context: 1656 (100%)
- Buckets complete (label + funding): 1434
- Symbols with any label: 9/9 (BTC, ETH, BNB, SOL, XRP, AVAX, DOGE, LINK, SUI) — min paired instruments (5) MET
- Min test blocks (3) temporally feasible within 6-month overlap — MET temporally
- RV/mark-price baseline (B1) computable: **NOT MET** (context not cached)
- Claim-worthy on cached inputs: **FALSE**

## 3. Why pre-registered evaluation could not run

- Primary contrast C2 vs B1 requires QLIKE on next-24h liquidation intensity vs RV-only baseline.
- B1 needs realized variance from mark-price 1h returns; mark-price/klines not in cached admissible inputs.
- Handoff prohibits redundant network polling; no mark-price cache exists to build from.
- Therefore the frozen pre-registered evaluation is infeasible; no model contrast, no QLIKE, no bootstrap CI, no materiality gate result was computed. This is **not** a negative result from a run — it is a determination that the claim-worthy test cannot be constituted from admissible cached inputs.

## 4. Compliance checks (all honored)

- No outcome inspection before successor prereg freeze: PASS (prereg frozen pre-outcomes; no outcomes computed)
- No Binance/2024 conflation: PASS (Hyperliquid only; ironflow + Hyperliquid-native funding)
- No modeled/proxy/synthetic liquidation labels: PASS (observed ironflow events only; notional_usd-weighted intensity)
- No threshold-shopping: PASS (no test-set tuning; no evaluation run)
- No sealed-holdout reuse: PASS (FCLR-002/FCLR-003/Track B/C test sets untouched)
- No `.github/workflows` edits: PASS
- No redundant network polling: PASS (panel built from cache only)
- No agent-set RESOLVED_VERIFIED / fabricated=true: PASS (Gate 4 untouched, remains BLOCKED)
- No status-only output: PASS (verdict artifact + state updates produced)

## 5. Atomic state updates (this session)

- `research_state/experiment_frontier.json` — Track A moved to terminal NOT_SUPPORTED; next_action points to RV-context acquisition then Path (b) retry, OR Gate 4 conditional.
- `research_state/hypothesis_registry.json` — `H_tracka_hl_liquidation_forecast` status → NOT_SUPPORTED, with evidence pointer to this verdict.
- `research_state/run_manifest.json` — TRACKA-HL terminal run recorded (git SHA, UTC, config, artifact hashes, status NOT_SUPPORTED).
- `research_state/final_confirmatory_verdict.md` — Track A addendum appended (historical 2024 H001 record preserved, not erased).

## 6. Bottleneck removed / next unblocking step

The binding bottleneck is the **absence of cached mark-price/RV context for 2026-05..2026-10**. It is available via the live unauthenticated Hyperliquid `candleSnapshot` endpoint (probe confirmed ~720-744 hourly rows/month for 2026-05..2026-10 across the 9 coins) but was not cached and fetching it is disallowed as "redundant network polling" in this session's handoff.

**Next session (bottleneck removal + heavy work):** Acquire mark-price 1h candleSnapshot for 2026-05..2026-10 for the 9 symbols (bounded, unauthenticated, first-time acquisition — not redundant polling), rebuild the aligned panel with RV, then execute the pre-registered successor C2 vs B1 evaluation and emit the Track A verdict artifact. Only after that succeeds (or fails on minima) should Track A be considered finally resolved. Gate 4 / Track C remains EXPLICIT_BLOCKER_UNRESOLVED and is not acted on unless a valid resolved terms artifact appears.

---

**End of verdict.** Anything short of this verdict artifact + consistent state updates is incomplete per the handoff acceptance criterion.
