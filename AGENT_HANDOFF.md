# AGENT HANDOFF — 2026-11-28T00:14:51Z
## REPOSITORY: Funding-conditioned-volatility-and-liquidation-risk
## NEXT SESSION MUST EXECUTE: FCLR-LIVE-ARCHIVE-08-20261127T131654Z (Track-B modeled boundary-breach forecast)

---

## INITIAL TASK MESSAGE FOR NEXT AGENTIC WORK SESSION

**EXECUTE FCLR-LIVE-ARCHIVE-08-20261127T131654Z (Track-B modeled boundary-breach forecast) under ONE fresh `research_state/session_<UTC>/` whose session_id is lexicographically > `20261127T131654Z` (the campaign-08 start gate). This is the ONLY executable heavy work remaining, and it is HARD-BOUND by the handoff heavy-work gate: any post-start session that does not emit the full `fclr_live_archive08_*` artifact set (plus the `evidence_audit_<UTC>.json` alias and a non-empty `trigger_check_<UTC>.json`) FAILS CLOSED. There is no prose-only, trigger-only, audit-only, prereg-only, source-probe-only, or verify-and-stop escape hatch.**

**Repository-name priority (why this task, and why it cannot be skipped):** the repo name leads with "Funding-conditioned-volatility", so the Binance 5-symbol mark-price archive (|S|=22,608; 2024-04..2026-10; BNBUSDT, BTCUSDT, ETHUSDT, SOLUSDT, XRPUSDT) is the live data frontier. Every funding-conditioned *volatility* estimand on that archive is now CLOSED NOT_SUPPORTED (campaigns 01–07). The only unfinished repo-name work is the *liquidation-risk* half, executed as the Track-B modeled boundary-breach forecast (campaign-08). Prioritize this over every other domain.

**What "done" means (all under the one fresh session dir, all non-empty):**
1. `fclr_live_archive08_source_registry_<UTC>.json` + `.md` — outcome-blind source registry (mark-price-only S, |S|=22608, per-file sha256).
2. `fclr_live_archive08_prereg_<UTC>.json` + `.md` — frozen prereg (margin/leverage scenarios, horizon, separate long/short labels), frozen BEFORE outcomes.
3. `fclr_live_archive08_eval_<UTC>.py` + `.json` + `.md` — heavy 3-block OOS AUC / log-loss / Brier, funding-conditioned vs mark-price-only baseline, >=2000 block-bootstrap + leave-one-symbol-out.
4. `fclr_live_archive08_recompute_<UTC>.py` + `.json` — independent stdlib recompute that rebuilds S, confirms all 5 symbols in every block/fold, n_test>=500, and emits `all_checks_match=true`.
5. `fclr_live_archive08_evidence_audit_<UTC>.json` + `.md` — evidence audit with `audit_pass=true`.
6. `evidence_audit_<UTC>.json` — gate-required alias.
7. `trigger_check_<UTC>.json` — non-empty trigger check.

**Last completed heavy session**: `session_20261127T065600Z` (campaign-07, verdict NOT_SUPPORTED: QLIKE rel -0.704%, 95% CI [-1.218%,-0.190%], floor +2%; independent stdlib recompute all_checks_match=true; |S|=22608). The on-disk newest session equals this id, so the handoff is NOT stale and the gate is GREEN (verified 2026-11-28T00:14:51Z).

**CRITICAL SESSION-ID CONSTRAINT**: the next fresh session id MUST be > `20261127T131654Z`. Because the current wall clock is already past that gate, any session created now is automatically post-start and therefore enforced. Do NOT reuse `session_20261127T065600Z` or any 20261126/20261127 id at or below the gate, and do not hand-name a session dir with a pre-gate timestamp to dodge enforcement.

---

## FOCUS CAMPAIGN (heavy work that CANNOT be avoided)

The gate binder `scripts/check_handoff_heavywork_gate.py::_live_archive_state` is ladder-aware: the dated token `FCLR-LIVE-ARCHIVE-08-20261127T131654Z` in this file activates the campaign-08 artifact family `fclr_live_archive08_*`. Mechanics the next session must satisfy to pass:

- The gate resolves the **lexicographically latest** `session_<UTC>` id recorded in this handoff AND the latest on-disk session dir. If the on-disk newest session is newer than the handoff-recorded one, the gate fails `HANDOFF_STALE_LATEST_SESSION`. So the next session MUST both (a) create the new session dir and (b) record its id in this handoff.
- For a post-start session (id > `20261127T131654Z`), `_live_archive_state` requires every `fclr_live_archive08_*` artifact above to be present AND non-empty, plus a non-empty `trigger_check_*.json`. Missing, empty, or trigger-less → FAIL.
- Root `research_state/*.md|*.json` is capped at 500 (currently 500/500). **ALL new artifacts MUST go under `session_<UTC>/`, never the root.**
- Stdlib only (numpy, pandas, scipy, pyarrow, requests pre-installed). No pip install. No network. Cache is read-only; do NOT re-download.

This is a materially different, feasible design on the SAME frozen, verified panel — not a re-run of a terminal endpoint. The volatility half is exhausted; the liquidation-risk half is the open repo-name frontier.

---

## EXPERIMENT SPECIFICATION (FCLR-LIVE-ARCHIVE-08)

**Domain**: Track-B modeled boundary-breach forecast (NOT an overlay) — permitted because the campaign-07 forecast gate did NOT pass (RESEARCH_PROMPT §9: NO risk overlay authorized; forecast validation of a modeled boundary-breach target IS permitted).

**Data**: Frozen balanced mark-price common support **S** (|S| = 22,608 timestamps, 2024-04..2026-10, five symbols). Cache is read-only, verified, already on disk at `research_state/data_cache/{SYMBOL}_{2024_04..2026_10}/`. **Do NOT re-download.**

**Split**: 60/20/20 by unique UTC ts + 168h purge/embargo → test split into 3 blocks.

**Target**: whether the future mark-price path breaches a pre-registered hypothetical long/short liquidation boundary within a fixed horizon. Boundaries derived from disclosed constant margin/leverage scenarios; separate long/short labels; modeled proxy only (never label as observed liquidation).

**Models**:
- Baseline (mark-price-only): RV1h, RV24h, RV168h features.
- Funding-conditioned: Baseline + signed funding(24h) + trailing 90d |funding| pct + mark/index premium + mark/EMA24 distance.

**Metrics**: OOS AUC / log-loss / Brier with >=2000 block-bootstrap and leave-one-symbol-out.

**Validation**: independent stdlib recompute with `all_checks_match=true`.

---

## POST-EXECUTION HANDOFF UPDATE (do this after the artifact set is complete)

1. Update this handoff to **LEAD with the next campaign** (promote rank-1 `FCLR-LIQ-CONTAGION-001` to rank-0, or the next ladder step), carrying the same dated-token discipline so the gate stays armed for the following session.
2. Re-run `python3 scripts/check_handoff_heavywork_gate.py` until **GREEN**.
3. Set rank-0 to `COMPLETED_VALIDATED` in `research_state/experiment_frontier.json` with the reproduced verdict.

---

## BLOCKER STATUS

| Blocker | Status |
|---------|--------|
| Aborted / stalled session on disk | **NONE** (newest complete: 20261127T065600Z; no *.lock / *.tmp / *ABORT* found) |
| External dependencies | **NONE** |
| Cache verification | **VERIFIED PRESENT** — 5-symbol 2024-04..2026-10 cache on disk (175 symbol-month dirs incl. 155 in-window); per-file .sha256 sidecars + `cached_inputs_hashes.json`; define/freeze common support S |
| Risk overlay authorization | **FORBIDDEN** — campaign-07 forecast gate NOT passed (RESEARCH_PROMPT §9) |
| Gate enforcement gap | **CLOSED** — dated token `FCLR-LIVE-ARCHIVE-08-20261127T131654Z` arms the `_live_archive_state` binder; verified GREEN 2026-11-28T00:14:51Z |
| Root churn cap | **AT CAP (500/500)** — all new artifacts go under `session_<UTC>/` |
| Template availability | **PRESENT** — `handoff_archive/quarantine_20261126T144850Z/fclr_live_archive07_eval_20261126T144850Z.py` |

No sessions are blocked or inefficient. All campaigns rank 1+ are COMPLETED_VALIDATED/COMPLETE. The only remaining heavy work is FCLR-LIVE-ARCHIVE-08 at rank 0, and it is gate-armed so it cannot be skipped.

---

## DATA AVAILABILITY CONFIRMATION

```bash
# Verified cache exists at:
research_state/data_cache/BNBUSDT_2024_04..2026_10/
research_state/data_cache/BTCUSDT_2024_04..2026_10/
research_state/data_cache/ETHUSDT_2024_04..2026_10/
research_state/data_cache/SOLUSDT_2024_04..2026_10/
research_state/data_cache/XRPUSDT_2024_04..2026_10/
# 155 in-window symbol-month dirs = 5 symbols x 31 months (plus legacy 2024_01..03 dirs)
# Funding zips 2024-04..2026-10; klines/index/mark/premium daily zips 2024-01..2026-11 with .sha256 sidecars
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

**All funding-conditioned volatility estimands CLOSED NOT_SUPPORTED on the verified 5-symbol archive.**

---

## SECOND DATA DOMAIN: IRONFLOW HYPERLIQUID BULK (reference only)

- Path: `research_state/data_cache/ironflow_bulk/` (candles_1h, funding, open_interest, liquidations)
- Months: 2025-05..2026-10 (18 months)
- Status: program formally exhausted (FCLR-LIQ-RISK-PROGRAM-CLOSURE-02 completed 2026-11-25T06:00:00Z)
- Contagion panel: `fclr_liq_combined_panel_20261115T181405Z.parquet` (1.74M rows, 15 coins, 2025-03..2026-10) — rank-1 campaign `FCLR-LIQ-CONTAGION-001` is ACTIVE/READY_EXECUTE but rank-0 is FCLR-LIVE-ARCHIVE-08.

---

## EXECUTION CHECKLIST FOR NEXT SESSION

```
[ ] Create fresh session dir: research_state/session_<UTC>/  (UTC > 20261127T131654Z)
[ ] Phase 1: Source registry — verify cache, define/freeze common support S (|S|=22608)
[ ] Phase 2: Prereg freeze — outcome-blind, margin/leverage scenarios, horizon, long/short labels
[ ] Phase 3: Heavy evaluation — 3-block OOS AUC/log-loss/Brier, >=2000 bootstrap + LOSO
[ ] Phase 4: Independent recompute — rebuild S, all_checks_match=true, 5 symbols/block/fold, n_test>=500
[ ] Phase 5: Evidence audit + gate alias (evidence_audit_<UTC>.json) + trigger check
[ ] All artifacts non-empty under session_<UTC>/
[ ] Record the new session id in THIS handoff (avoid HANDOFF_STALE_LATEST_SESSION)
[ ] Update handoff to LEAD with the next campaign (dated token preserved)
[ ] Run check_handoff_heavywork_gate.py until GREEN
[ ] Set experiment_frontier.json rank-0 to COMPLETED_VALIDATED
```

---

## GATE ENFORCEMENT

- `AGENT_HANDOFF.md` FOCUS CAMPAIGN section (dated token `FCLR-LIVE-ARCHIVE-08-20261127T131654Z`) — present above.
- `scripts/check_handoff_heavywork_gate.py` — `LIVE_ARCHIVE_CAMPAIGN_RE` / `_live_archive_state` ladder-aware binder (campaign 08 → `fclr_live_archive08_*`); ARMED because the dated token is present; verified GREEN 2026-11-28T00:14:51Z.
- Root `research_state/*.md|*.json` capped at 500 (currently 500/500) — ALL NEW ARTIFACTS MUST GO UNDER `session_<UTC>/`.
- Stdlib only (numpy, pandas, scipy, pyarrow, requests pre-installed); no pip install; no network.

---

## TEMPLATE REFERENCE

Recovered stdlib template for campaign-07 (adapt for the campaign-08 boundary-breach design):
```
handoff_archive/quarantine_20261126T144850Z/fclr_live_archive07_eval_20261126T144850Z.py
```

---

**THIS IS THE ONLY EXECUTABLE HEAVY WORK REMAINING. The Binance 5-symbol contiguous volatility design is exhausted. The Hyperliquid bulk/extended frontiers are exhausted. The contagion campaign is rank-1. FCLR-LIVE-ARCHIVE-08 IS THE ACTIVE RANK-0 TASK AND IS GATE-ARMED.**

**SESSION ID MUST BE > 20261127T131654Z. NO EXCEPTIONS.**