# AGENT HANDOFF — 2026-11-28T00:04:07Z
## REPOSITORY: Funding-conditioned-volatility-and-liquidation-risk
## NEXT SESSION MUST EXECUTE: FCLR-LIVE-ARCHIVE-08 (Track-B modeled boundary-breach forecast)

---

## INITIAL TASK MESSAGE FOR NEXT AGENTIC WORK SESSION

**EXECUTE FCLR-LIVE-ARCHIVE-08 (Track-B modeled boundary-breach forecast) under one fresh `research_state/session_<UTC>/` with session_id lexicographically > 20261127T131654Z (the campaign-08 start gate). This is the ONLY executable heavy work remaining.**

- Repository name priority: "Funding-conditioned-volatility" → the Binance 5-symbol archive (|S|=22,608, 2024-04..2026-10, five symbols) is the live data frontier for funding-conditioned volatility.
- All prior funding-conditioned volatility arms (LIVE-ARCHIVE-01 through -07) are CLOSED NOT_SUPPORTED on verified cache.
- Hyperliquid bulk/extended frontiers are exhausted (no untouched region ≥127 days for 3-block design).
- Contagion campaign (FCLR-LIQ-CONTAGION-001) is rank-1; rank-0 is FCLR-LIVE-ARCHIVE-08.
- Forecast gate (campaign-07) did NOT pass → NO risk overlay authorized (RESEARCH_PROMPT §9); Track-B modeled boundary-breach forecast IS permitted.
- Data: Frozen balanced mark-price common support S (|S|=22,608) — cache read-only, already on disk, do NOT re-download.
- Target: Whether future mark-price path breaches pre-registered hypothetical long/short liquidation boundary within fixed horizon (margin/leverage scenarios disclosed).
- Models: Baseline (RV1h, RV24h, RV168h) vs Funding-conditioned (Baseline + signed funding(24h) + trailing 90d |funding| pct + mark/index premium + mark/EMA24 distance).
- Metrics: OOS AUC/log-loss/Brier with ≥2000 block-bootstrap + leave-one-symbol-out.
- Validation: Independent stdlib recompute with `all_checks_match=true`.

**Last completed heavy session**: `session_20261127T065600Z` (campaign-07, verdict NOT_SUPPORTED: QLIKE rel -0.704%, 95% CI [-1.218%,-0.190%], floor +2%; independent stdlib recompute all_checks_match=true; |S|=22608).

**CRITICAL**: Next session ID MUST BE > 20261127T131654Z. Session IDs in (20261127T065600Z, 20261127T131654Z] are GRANDFATHERED BY THE GATE AND FORBIDDEN.

---

## CURRENT CAMPAIGN STATE (from `experiment_frontier.json` rank-0)

| Field | Value |
|-------|-------|
| **Rank-0 Task** | `FCLR-LIVE-ARCHIVE-08` |
| **Status** | `READY_EXECUTE` |
| **Program Status** | `ACTIVE` |
| **Generated** | `20261127T080708Z` |
| **Campaign-08 Start Gate** | `20261127T131654Z` |
| **Last Completed Session** | `20261127T065600Z` (campaign-07, verdict NOT_SUPPORTED) |

**CRITICAL SESSION ID CONSTRAINT**: Next fresh session ID **MUST BE > 20261127T131654Z** (the campaign-08 start gate). A session ID in `(20261127T065600Z, 20261127T131654Z]` is **GRANDFATHERED BY THE GATE AND FORBIDDEN**.

---

## EXPERIMENT SPECIFICATION (FCLR-LIVE-ARCHIVE-08)

**Domain**: Track-B modeled boundary-breach forecast (NOT an overlay) — permitted because campaign-07 forecast gate did NOT pass (per RESEARCH_PROMPT §9, NO risk overlay authorized; forecast validation of modeled boundary-breach target IS permitted).

**Data**: Frozen balanced mark-price common support **S** (|S| = 22,608 timestamps, 2024-04..2026-10, five symbols: BNBUSDT, BTCUSDT, ETHUSDT, SOLUSDT, XRPUSDT). Cache is read-only, verified, already on disk at `research_state/data_cache/{SYMBOL}_{2024_04..2026_10}/`. **Do NOT re-download.**

**Split**: 60/20/20 by unique UTC ts + 168h purge/embargo → test split into 3 blocks.

**Target**: Whether the future mark-price path breaches a pre-registered hypothetical long/short liquidation boundary within a fixed horizon.
- Boundaries derived from disclosed constant margin/leverage scenarios
- Separate long/short labels
- Track-B: modeled boundary-breach forecast (not an overlay)

**Models**:
- **Baseline (mark-price-only)**: RV1h, RV24h, RV168h features
- **Funding-conditioned**: Baseline + signed funding(24h) + trailing 90d \|funding\| pct + mark/index premium + mark/EMA24 distance

**Metrics**: Out-of-sample AUC / log-loss / Brier with **≥2000 block-bootstrap** and **leave-one-symbol-out**.

**Validation**: Independent stdlib recompute with `all_checks_match=true`.

---

## REQUIRED ARTIFACTS (all under ONE fresh `research_state/session_<UTC>/` with session_id > 20261127T131654Z)

| Artifact | Description |
|----------|-------------|
| `fclr_live_archive08_source_registry_<UTC>.json/.md` | Outcome-blind source registry (mark-price-only S, \|S\|=22608, sha256) |
| `fclr_live_archive08_prereg_<UTC>.json/.md` | Frozen prereg (margin/leverage scenarios, horizon, long/short labels) |
| `fclr_live_archive08_eval_<UTC>.py/.json/.md` | Heavy 3-block evaluation |
| `fclr_live_archive08_recompute_<UTC>.py/.json` | Independent stdlib recompute (rebuilds S, confirms all 5 symbols in every block/fold, n_test≥500) |
| `fclr_live_archive08_evidence_audit_<UTC>.json/.md` | Evidence audit with `audit_pass=true` |
| `evidence_audit_<UTC>.json` | Alias (gate requirement) |
| `trigger_check_<UTC>.json` | Trigger check |

**All artifacts non-empty. `all_checks_match=true` from independent recompute.**

---

## POST-EXECUTION HANDOFF UPDATE

After producing the complete artifact set with `all_checks_match=true`:
1. Update this handoff to **LEAD with FCLR-LIVE-ARCHIVE-08**
2. Re-run the handoff heavy-work gate (`scripts/check_handoff_heavywork_gate.py`) until **GREEN**
3. Set rank-0 to `COMPLETED_VALIDATED` in `experiment_frontier.json`

---

## BLOCKER STATUS

| Blocker | Status |
|---------|--------|
| Aborted session on disk | **NONE** (newest complete: 20261127T065600Z) |
| External dependencies | **NONE** |
| Cache verification | **REQUIRED PHASE** — verify 2024-04..2026-10 five-symbol cache against per-file .sha256 sidecars and `cached_inputs_hashes.json`; define/freeze common support S |
| Risk overlay authorization | **FORBIDDEN** — campaign-07 forecast gate NOT passed (RESEARCH_PROMPT §9) |

No sessions are blocked or inefficient. All campaigns rank 1+ are COMPLETED_VALIDATED/COMPLETE. The only remaining heavy work is FCLR-LIVE-ARCHIVE-08 at rank 0.

---

## DATA AVAILABILITY CONFIRMATION

```bash
# Verified cache exists at:
research_state/data_cache/BNBUSDT_2024_04..2026_10/
research_state/data_cache/BTCUSDT_2024_04..2026_10/
research_state/data_cache/ETHUSDT_2024_04..2026_10/
research_state/data_cache/SOLUSDT_2024_04..2026_10/
research_state/data_cache/XRPUSDT_2024_04..2026_10/

# 155 symbol-month dirs = 5 symbols × 31 months
# Funding zips: 2024-04..2026-10
# Klines/index/mark/premium daily zips: 2024-01..2026-11 with .sha256 sidecars
```

---

## CAMPAIGN HISTORY (for context — DO NOT RE-RUN)

| Campaign | Verdict | Session | Key Result |
|----------|---------|---------|------------|
| FCLR-LIVE-ARCHIVE-01 | NOT_SUPPORTED | 20261126T042519Z | QLIKE rel 0.840% < 2% floor |
| FCLR-LIVE-ARCHIVE-03 | NOT_SUPPORTED | 20261126T051548Z | Brier rel 0.458% < 2% floor |
| FCLR-LIVE-ARCHIVE-04 | NOT_SUPPORTED | 20261126T061929Z | Pinball rel -1.102% |
| FCLR-LIVE-ARCHIVE-05 | NOT_SUPPORTED | 20261126T082429Z | MSE rel 0.141% < 2% floor |
| FCLR-LIVE-ARCHIVE-06 | NOT_SUPPORTED | 20261126T133828Z | MSE rel 0.716%, CI [0.419%,1.020%] < 2% |
| FCLR-LIVE-ARCHIVE-07 | NOT_SUPPORTED | 20261127T065600Z | QLIKE rel -0.704%, CI [-1.218%,-0.190%] |

**All funding-conditioned volatility estimands CLOSED NOT_SUPPORTED on verified 5-symbol archive.**

---

## SECOND DATA DOMAIN: IRONFLOW HYPERLIQUID BULK (for reference)

- **Path**: `research_state/data_cache/ironflow_bulk/` (candles_1h, funding, open_interest, liquidations)
- **Months**: 2025-05..2026-10 (18 months)
- **Status**: Program formally exhausted (FCLR-LIQ-RISK-PROGRAM-CLOSURE-02 completed 2026-11-25T06:00:00Z)
- **Contagion panel**: `fclr_liq_combined_panel_20261115T181405Z.parquet` (1.74M rows, 15 coins, 2025-03..2026-10) — rank-1 campaign `FCLR-LIQ-CONTAGION-001` is ACTIVE/READY_EXECUTE but **rank-0 is FCLR-LIVE-ARCHIVE-08**

---

## EXECUTION CHECKLIST FOR NEXT SESSION

```
[ ] Create fresh session directory: research_state/session_<UTC>/  (UTC > 20261127T131654Z)
[ ] Phase 1: Source registry — verify cache, define/freeze common support S (|S|=22608)
[ ] Phase 2: Prereg freeze — outcome-blind, margin/leverage scenarios, horizon, long/short labels
[ ] Phase 3: Heavy evaluation — 3-block OOS AUC/log-loss/Brier, ≥2000 bootstrap + LOSO
[ ] Phase 4: Independent recompute — rebuild S, all_checks_match=true, 5 symbols/block/fold, n_test≥500
[ ] Phase 5: Evidence audit + gate alias + trigger check
[ ] All artifacts non-empty under session_<UTC>/
[ ] Update handoff to LEAD with FCLR-LIVE-ARCHIVE-08
[ ] Run check_handoff_heavywork_gate.py until GREEN
[ ] Set experiment_frontier.json rank-0 to COMPLETED_VALIDATED
```

---

## GATE ENFORCEMENT

- `AGENT_HANDOFF.md` FOCUS CAMPAIGN section
- `scripts/check_handoff_heavywork_gate.py` — `LIVE_ARCHIVE_CAMPAIGN_RE` / `_live_archive_state` ladder-aware binder (campaign 08 → `fclr_live_archive08_*`)
- Root `research_state/*.md|*.json` capped at 500 — **ALL NEW ARTIFACTS MUST GO UNDER `session_<UTC>/`**
- Stdlib only (numpy, pandas, pyarrow, requests pre-installed); no pip install; no network

---

## TEMPLATE REFERENCE

Recovered stdlib template for campaign-07 (adapt for campaign-08 boundary-breach design):
```
handoff_archive/quarantine_20261126T144850Z/fclr_live_archive07_eval_20261126T144850Z.py
```

---

**THIS IS THE ONLY EXECUTABLE HEAVY WORK REMAINING. The Binance 5-symbol contiguous design is exhausted. The Hyperliquid bulk/extended frontiers are exhausted. The contagion campaign is rank-1. FCLR-LIVE-ARCHIVE-08 IS THE ACTIVE RANK-0 TASK.**

**SESSION ID MUST BE > 20261127T131654Z. NO EXCEPTIONS.**
