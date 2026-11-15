# NEXT SESSION INITIAL TASK MESSAGE — 2026-11-15T17:54:17Z
# SOLE DURABLE HANDOFF POINTER

**Repository:** Funding-conditioned-volatility-and-liquidation-risk (funding rates, volatility, liquidation risk in crypto perpetuals)
**Sole durable handoff:** `AGENT_HANDOFF.md` — execute its `INITIAL TASK MESSAGE FOR NEXT AGENTIC WORK SESSION — 2026-11-15T17:54:17Z`. `NEXT_SESSION_HANDOFF.md` = tombstone. `AGENT_HANDOFF_20261115T073240Z.md` = RETIRED/SUPERSEDED — ignore.

## IMMEDIATE HEAVY TASK (default path — NOT trigger-gated, NOT status-only)

Rank-0 heavy campaign: **`FCLR-LIQ-COMBINED-PANEL-20261115T170000Z`** (`READY_EXECUTE` / `ACTIVE`).

Prior work exhausted the 5-symbol Binance volatility 3-block frontier and ironflow-only liquidation designs, but admissible heavy work remains. `metpie` (new observed-liquidation source family, never used for outcomes) abuts cached `ironflow` on the same Hyperliquid coin universe, forming a continuous **588.5-day Hyperliquid observed-liquidation window (2025-03-22..2026-10-31)** with 19×30-day blocks and 15 funded coins ≥5,000 events. §16 audit = **ADMISSIBLE_PENDING_BOUNDED_ACQUISITION** (`research_state/audits/admissibility_audit_liq_combined_metpie_ironflow_20261115T170000Z.{json,md}`).

## EXECUTE IN ORDER (do not stop at status; do not skip to verdict)
1. Run baseline/start block in `AGENT_HANDOFF.md`; confirm campaign gate 19/19, fwd-vol PASS, scope drift green, targeted suite green, `next_campaign_status.py` honest, rank-0 = `FCLR-LIQ-COMBINED-PANEL-20261115T170000Z`.
2. Bounded unauthenticated Hyperliquid candle+funding acquisition for the 15 funded coins over 2025-03-22..2025-10-31 (cache is 2025-11+ only), with idempotent provenance (`.accessed.json`/`.sha256`).
3. Build unified metpie+ironflow observed-liquidation panel (normalize schema, dedup on coin/timestamp/notional_usd/tx-hash, causal features) → `fclr_liq_combined_panel_<UTC>.parquet` + build report.
4. Freeze NEW pre-outcomes prereg (24h observed-liquidation-intensity QLIKE, C2 vs B1, expanding-window walk-forward, ≥3 blocks incl. 2 pristine metpie, 7d purge/embargo, block bootstrap ≥2000, Holm, 2% materiality).
5. Evaluate + gate + emit `research_state/evaluation_summary_FCLR-LIQ-COMBINED-<UTC>.{json,md}`; update frontier + `H_fclr_liq_combined_panel_forecast`. If NOT_MET, record honestly and install next materially different heavy cell at rank 0.

## HARD CONSTRAINTS
- Never reopen sealed/terminal families or mutate sealed artifacts; never edit `.github/workflows/*`.
- No outcome-peeking/threshold tuning before prereg freeze; no paid/credentialed/manual data for outcomes (bounded free unauthenticated context acquisition allowed).
- `H2_shek_replication` remains EXPLORATORY_ONLY (`promotable=false`). Do not relabel exploratory as confirmatory.
- Do not poll, do not re-run tested windows for same estimand, do not re-probe TERMINAL_NO_GO families.
- Exactly ONE active handoff (`AGENT_HANDOFF.md`). "No trigger → stop cleanly" is NOT completion.
