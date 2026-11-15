# NEXT SESSION INITIAL TASK MESSAGE — 2026-11-15T170000Z
# SOLE DURABLE HANDOFF POINTER

**Repository:** Funding-conditioned-volatility-and-liquidation-risk (funding rates, volatility, liquidation risk in crypto perpetuals)
**Sole durable handoff:** `AGENT_HANDOFF.md` — execute its `INITIAL TASK MESSAGE FOR NEXT AGENTIC WORK SESSION — 2026-11-15T170000Z`. `NEXT_SESSION_HANDOFF.md` = tombstone. `AGENT_HANDOFF_20261115T073240Z.md` = RETIRED/SUPERSEDED — ignore.

## IMMEDIATE TASK (heavy work is the DEFAULT path — NOT trigger-gated)

Rank-0 heavy campaign: **`FCLR-LIQ-COMBINED-PANEL-20261115T170000Z`** (`READY_EXECUTE` / `ACTIVE`).

The prior program exhausted the 5-symbol Binance volatility 3-block frontier and ironflow-only liquidation designs, but that is NOT "no heavy work". A materially new observed-liquidation source family (`metpie`, never used for outcomes) abuts the cached `ironflow` archive on the same Hyperliquid coin universe, forming a continuous **588.5-day Hyperliquid observed-liquidation window (2025-03-22..2026-10-31)** with 19×30-day blocks (2 pristine metpie) and 15 funded coins ≥5,000 events. §16 audit = **ADMISSIBLE_PENDING_BOUNDED_ACQUISITION** (`research_state/audits/admissibility_audit_liq_combined_metpie_ironflow_20261115T170000Z.{json,md}`).

## NEXT ACTION (do these in order; do not skip to a verdict)

Run the START block in `AGENT_HANDOFF.md`, confirm baseline green (campaign gate 19/19, fwd-vol PASS, scope drift 187/187, targeted 64/64, `next_campaign_status.py` honest), confirm rank-0 = `FCLR-LIQ-COMBINED-PANEL-20261115T170000Z`, then:
1. Bounded unauthenticated Hyperliquid candle+funding acquisition for the 15 funded coins over 2025-03-22..2025-10-31 (cache is 2025-11+ only).
2. Build the unified metpie+ironflow observed-liquidation panel (dedup + causal features).
3. Freeze a NEW pre-outcomes prereg (24h observed-liquidation-intensity QLIKE, C2 vs B1, expanding-window walk-forward, ≥3 blocks incl. 2 pristine metpie).
4. Execute, gate, emit `research_state/evaluation_summary_FCLR-LIQ-COMBINED-<UTC>.{json,md}`, update frontier + `H_fclr_liq_combined_panel_forecast`.

## Hard constraints
- Never reopen sealed/terminal families or mutate sealed artifacts; never edit `.github/workflows/*`
- No outcome-peeking/threshold tuning before the prereg freeze; bounded free unauthenticated acquisition only (no paid/credentialed/manual data for outcomes)
- `H2_shek_replication` stays EXPLORATORY_ONLY, promotable=false; never relabel exploratory as confirmatory
- Do not poll, do not re-run tested windows for the SAME estimand, do not re-probe exhausted/TERMINAL_NO_GO families
- Exactly ONE active handoff (`AGENT_HANDOFF.md`); do not create competing handoff files (the churn failure mode)
- "No trigger → stop cleanly" is NOT completion