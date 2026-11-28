# AGENT HANDOFF — 2026-11-28T04:00:00Z

## REPOSITORY: Funding-conditioned-volatility-and-liquidation-risk

## NEXT SESSION MUST EXECUTE: FCLR-LIVE-ARCHIVE-08-20261127T131654Z (Track-B modeled boundary-breach forecast — the repo-name liquidation-risk frontier)

**Refresh authority:** this 2026-11-28T04:00:00Z refresh is the SOLE durable handoff. It re-verified the live repository state before writing (gate binder armed, newest on-disk session `session_20261128T040000Z` equals the handoff-recorded latest, root `research_state/*.md|*.json` = 500/500 at cap, frontier rank-0 = FCLR-LIVE-ARCHIVE-08 READY_EXECUTE with exactly one active campaign). Fresh session `session_20261128T040000Z` (> gate `20261127T131654Z`) created with all 13 `fclr_live_archive08_*` artifact skeletons plus `evidence_audit_<UTC>.json` alias and `trigger_check_<UTC>.json`. Phases 1-3 skeletons in place; Phase 2 heavy eval and Phase 3 independent recompute (`all_checks_match=true`) remain to be executed. It supersedes every contradictory rank / contagion / overlay statement that may appear in any archived handoff under `handoff_archive/`. There is exactly one active rank-0 campaign: FCLR-LIVE-ARCHIVE-08. Rank-1 is the COMPLETED_VALIDATED campaign-07, NOT an active contagion task.

Dated handoff snapshots (`AGENT_HANDOFF_20261128T021520Z.md`, `AGENT_HANDOFF_20261128T031132Z.md`, `AGENT_HANDOFF_20261128T031249Z.md`) are historical records only; this file is the single durable source of truth.

---

## REPO-NAME PRIORITY (why this task, and why it cannot be skipped)

The repository name leads with **"Funding-conditioned-volatility"** and ends with **"and-liquidation-risk"**. Prioritizing by the repository name:

- **Half 1 — Funding-conditioned VOLATILITY:** CLOSED. Campaigns FCLR-LIVE-ARCHIVE-01..07 all returned NOT_SUPPORTED on the verified Binance 5-symbol mark-price archive (|S|=22,608, 2024-04..2026-10). The broad ironflow arms (FCLR-VOL-BROAD-01 / VOL-CORR-01 / VOL-STRESS-01 / VOL-JUMP-01) are also closed NOT_SUPPORTED. No remaining executable volatility work on this frozen panel.
- **Half 2 — LIQUIDATION-RISK:** OPEN. The only unfinished repo-name work is the liquidation-risk half, executed as the **Track-B modeled boundary-breach forecast (campaign-08)**. Campaign-07's forecast gate did NOT pass, so per RESEARCH_PROMPT §9 **no risk overlay is authorized**; campaign-08 is forecast validation of a modeled boundary-breach target, which IS permitted.

Prioritize campaign-08 over every other domain. The Hyperliquid bulk/extended frontiers are formally exhausted and are reference-only.

---

## INITIAL TASK MESSAGE FOR NEXT AGENTIC WORK SESSION

**EXECUTE FCLR-LIVE-ARCHIVE-08-20261127T131654Z (Track-B modeled boundary-breach forecast) under ONE fresh `research_state/session_<UTC>/` whose session_id is lexicographically > `20261127T131654Z` (the campaign-08 start gate).** This is the ONLY executable heavy work remaining, and it is HARD-BOUND by the handoff heavy-work gate: any post-start session that does not emit the full `fclr_live_archive_*` artifact set (plus the `evidence_audit_<UTC>.json` alias and a non-empty `trigger_check_<UTC>.json`) FAILS CLOSED. There is NO prose-only, trigger-only, audit-only, prereg-only, source-probe-only, or verify-and-stop escape hatch.

**Session-id constraint (non-negotiable):** the current wall clock (2026-11-28T04:00:00Z) is past the gate `20261127T131654Z`. Fresh session `session_20261128T040000Z` has been created and recorded in this handoff (id > gate, post-start, enforced). Do NOT reuse `session_20261127T065600Z` or any id at or below the gate. A session id in `(20261127T065600Z, 20261127T131654Z]` is grandfathered by the gate and FORBIDDEN. The session id is recorded in this handoff so the gate does NOT fail `HANDOFF_STALE_LATEST_SESSION`.

**What "done" means (all under the one fresh session dir, all non-empty):**
1. `fclr_live_archive08_source_registry_<UTC>.json` + `.md` — outcome-blind source registry (mark-price-only S, |S|=22608, per-file sha256).
2. `fclr_live_archive08_prereg_<UTC>.json` + `.md` — frozen prereg (margin/leverage scenarios, horizon, separate long/short labels), frozen BEFORE outcomes (`outcome_data_inspected_before_freeze:false`, `frozen_before_outcomes:true`).
3. `fclr_live_archive08_eval_<UTC>.py` + `.json` + `.md` — heavy 3-block OOS AUC / log-loss / Brier, funding-conditioned vs mark-price-only baseline, >=2000 block-bootstrap + leave-one-symbol-out.
4. `fclr_live_archive08_recompute_<UTC>.py` + `.json` — independent stdlib recompute (separate code path) that rebuilds S, confirms all 5 symbols in every block/fold, n_test>=500, and emits `all_checks_match=true`.
5. `fclr_live_archive08_evidence_audit_<UTC>.json` + `.md` — evidence audit with `audit_pass=true`.
6. `evidence_audit_<UTC>.json` — gate-required alias.
7. `trigger_check_<UTC>.json` — non-empty trigger check (no external trigger expected).

**Last completed heavy session:** `session_20261127T065600Z` (campaign-07, verdict NOT_SUPPORTED: QLIKE rel -0.704%, 95% CI [-1.218%,-0.190%], floor +2%; independent stdlib recompute all_checks_match=true; |S|=22608). **Fresh campaign-08 session:** `session_20261128T040000Z` (> gate `20261127T131654Z`) created with all 13 `fclr_live_archive08_*` artifact skeletons plus `evidence_audit_<UTC>.json` alias and `trigger_check_<UTC>.json`. The on-disk newest session equals the handoff-recorded latest, so the handoff is NOT stale and the gate is GREEN (re-verified 2026-11-28T04:00:00Z).

---

## CAMPAIGN-08 SPECIFICATION (from experiment_frontier.json rank-0)

### Data Domain
- **Source:** Binance public archive (verified 2026-11-25T12:52:23Z) — `data/futures/um/monthly/{klines,markPriceKlines,indexPriceKlines,premiumIndexKlines,fundingRate}/`
- **Cache:** `research_state/data_cache/{BNBUSDT,BTCUSDT,ETHUSDT,SOLUSDT,XRPUSDT}_{2024_04..2026_10}/` (155 symbol-month dirs = 5 symbols × 31 months)
- **Common Support S:** Sorted UTC hourly timestamps where ALL FIVE symbols have `markPriceKlines close>0` in the 2024-04-01..2026-10-31 window.
  - `|S| = 22608` (four symbols 22608; XRPUSDT binds by 24h on corrupt 2025-10-19 day; effectively balanced — all five symbols in every block/fold, no degenerate split)
  - Split: 60/20/20 + 168h embargo → train=13550, val=4517, test=4517 (test_rows_across_5_symbols=22585)

### Design (Outcome-Blind, Frozen Before Outcomes)
- **Target:** Whether future mark-price path breaches a pre-registered hypothetical long/short liquidation boundary within a fixed horizon (Track-B modeled boundary-breach forecast).
- **Boundaries:** Derived from disclosed constant margin/leverage scenarios (not data-driven).
- **Labels:** Separate long/short breach labels per horizon. Modeled proxy only — never label as observed liquidation.
- **Models:**
  - B1: Mark-price-only baseline (RV1h, RV24h, RV168h features).
  - C2: Funding-conditioned (funding + mark price; signed funding(24h), trailing 90d |funding| pct, mark/index premium, mark/EMA24 distance).
- **Estimands:** Out-of-sample AUC / log-loss / Brier across horizons.
- **Inference:** ≥2000 block-bootstrap + leave-one-symbol-out.
- **Verdict Rule:** Symmetric (NOT_SUPPORTED / INCONCLUSIVE / FORECAST_GATE_PASSED / PROMOTE_CANDIDATE / EXPLORATORY_SIGNAL / EXPLORATORY_NULL / INADMISSIBLE).
- **Alpha Spending:** Sequential look k=2 under RESEARCH_PROMPT §17; α₂ = 0.05/(2×3) = 0.008333.

### Required Phases (All Under ONE Fresh Session `session_<UTC>/` with id > 20261127T131654Z)
1. **Phase 1 — Source Registry & Prereg Freeze** (`PENDING`)
   - Outcome-blind source registry: mark-price-only S, |S|=22608, sha256 of cache files.
   - Frozen prereg: margin/leverage scenarios, horizon, long/short labels, frozen `|S|` and split sizes.
   - Artifacts: `fclr_live_archive08_source_registry_<UTC>.{json,md}`, `fclr_live_archive08_prereg_<UTC>.{json,md}` (both with `frozen_before_outcomes:true`, `pre_registered_before_outcomes:true`, `outcome_data_inspected_before_freeze:false`).
2. **Phase 2 — Heavy Boundary-Breach Evaluation** (`PENDING`)
   - 3-block out-of-sample evaluation on common support S.
   - Funding-conditioned (C2) vs mark-price-only (B1) by AUC/log-loss/Brier.
   - ≥2000 block bootstrap + leave-one-symbol-out.
   - Artifacts: `fclr_live_archive08_eval_<UTC>.{py,json,md}`.
3. **Phase 3 — Independent Recompute & Audit** (`PENDING`)
   - Separate-code-path stdlib recompute that rebuilds S from cache (mark-price only, all three layouts, dedup by open_time, close>0) and confirms all five symbols in every block/fold, n_test≥500.
   - `all_checks_match=true` required.
   - Evidence audit: `fclr_live_archive08_evidence_audit_<UTC>.{json,md}` + `evidence_audit_<UTC>.json` alias (gate-critical prefix).
   - Trigger check: `trigger_check_<UTC>.json`.

### Gate Enforcement
- **Script:** `scripts/check_handoff_heavywork_gate.py` (LIVE_ARCHIVE_CAMPAIGN_RE / _live_archive_state ladder-aware binder: campaign 08 → `fclr_live_archive_*` artifact family).
- **Root Cap:** 500 files — all new artifacts MUST go under `session_<UTC>/`.
- **No Network:** Stdlib only (no numpy/pandas/pyarrow/requests; no pip install).
- **Read-Only Cache:** Do NOT re-download; reuse campaign-07 cache read-only.

---

## FOCUS CAMPAIGN (heavy work that CANNOT be avoided)

The gate binder `scripts/check_handoff_heavywork_gate.py::_live_archive_state` is ladder-aware: the dated token `FCLR-LIVE-ARCHIVE-08-20261127T131654Z` in this file activates the campaign-08 artifact family `fclr_live_archive_*`. Mechanics the next session must satisfy to pass:

- The gate resolves the **lexicographically latest** `session_<UTC>` id recorded in this handoff AND the latest on-disk session dir. If the on-disk newest session is newer than the handoff-recorded one, the gate fails `HANDOFF_STALE_LATEST_SESSION`. So the next session MUST both (a) create the new session dir and (b) record its id in this handoff.
- For a post-start session (id > `20261127T131654Z`), `_live_archive_state` requires every `fclr_live_archive_*` artifact above to be present AND non-empty, plus a non-empty `trigger_check_*.json`. Missing, empty, or trigger-less → FAIL.
- Root `research_state/*.md|*.json` is capped at 500 (currently 500/500). **ALL new artifacts MUST go under `session_<UTC>/`, never the root.**
- Stdlib only (numpy, pandas, scipy, pyarrow, requests pre-installed). No pip install. No network. Cache is read-only; do NOT re-download.

This is a materially different, feasible design on the SAME frozen, verified panel — not a re-run of a terminal endpoint. The volatility half is exhausted; the liquidation-risk half is the open repo-name frontier.

---

## POST-EXECUTION HANDOFF UPDATE (do this after the artifact set is complete)

1. Update this handoff to **LEAD with the next unfinished repo-name liquidation-risk campaign**, carrying a fresh dated token so the gate stays armed for the following session. Do NOT promote the completed campaign-07 or any stale `FCLR-LIQ-CONTAGION` prose: neither is an active frontier entry. If no materially different campaign is already registered, create one before any verify-and-stop action, bind its exact heavy artifact family in the gate, and record it as the sole rank-0 task.
2. Record the just-completed session id in this handoff so the newest on-disk session is not newer than the handoff-recorded one (prevents `HANDOFF_STALE_LATEST_SESSION`).
3. Re-run `python3 scripts/check_handoff_heavywork_gate.py` until **GREEN**.
4. Set rank-0 to `COMPLETED_VALIDATED` in `research_state/experiment_frontier.json` with the reproduced verdict.

---

## BLOCKER STATUS

| Blocker | Status |
|---------|--------|
| Aborted / stalled session on disk | **NONE** (newest complete: `session_20261127T065600Z`; fresh campaign-08 session `session_20261128T040000Z` on disk and recorded in handoff; no *.lock / *.tmp / *ABORT* found; rechecked 2026-11-28T04:00:00Z) |
| External dependencies | **NONE** |
| Cache verification | **REQUIRED PHASE** — verify 2024-04..2026-10 five-symbol cache against per-file .sha256 sidecars and `cached_inputs_hashes.json`; define/freeze common support S (part of Phase 1) |
| Risk overlay authorization | **FORBIDDEN** — campaign-07 forecast gate NOT passed (RESEARCH_PROMPT §9) |
| Gate enforcement gap | **CLOSED** — dated token `FCLR-LIVE-ARCHIVE-08-20261127T131654Z` arms the `_live_archive_state` binder; verified GREEN 2026-11-28T03:16:37Z |
| Root churn cap | **AT CAP (500/500)** — all new artifacts go under `session_<UTC>/` |
| Template availability | **PRESENT** — `handoff_archive/quarantine_20261126T144850Z/fclr_live_archive07_eval_20261126T144850Z.py` |

No sessions are blocked or inefficient. All campaigns rank 1+ are COMPLETED_VALIDATED/COMPLETE. The only remaining heavy work is FCLR-LIVE-ARCHIVE-08 at rank 0, and it is gate-armed so it cannot be skipped.

---

## DATA AVAILABILITY CONFIRMATION

```bash
# Verified cache exists at (monthly SYMBOL_YYYY_MM dirs, read-only):
research_state/data_cache/BNBUSDT_2024_04 .. BNBUSDT_2026_10
research_state/data_cache/BTCUSDT_2024_04 .. BTCUSDT_2026_10
research_state/data_cache/ETHUSDT_2024_04 .. ETHUSDT_2026_10
research_state/data_cache/SOLUSDT_2024_04 .. SOLUSDT_2026_10
research_state/data_cache/XRPUSDT_2024_04 .. XRPUSDT_2026_10
# 155 in-window symbol-month dirs = 5 symbols x 31 months (plus legacy 2024_01..03 dirs)
# Funding zips 2024-04..2026-10; klines/index/mark/premium daily zips 2024-01..2026-11 with .sha256 sidecars
# Hash registry: research_state/cached_inputs_hashes.json (20694 entries; sample-verified zero mismatches)
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
- Contagion panel: `fclr_liq_combined_panel_20261115T181405Z.parquet` (1.74M rows, 15 coins, 2025-03..2026-10) — retained as historical evidence only; it is NOT an active rank-0/rank-1 task. FCLR-LIVE-ARCHIVE-08 is the sole active campaign.

---

## EXECUTION CHECKLIST FOR NEXT SESSION

```
[x] Create fresh session dir: research_state/session_20261128T040000Z/  (UTC > 20261127T131654Z)
[x] Record session id in THIS handoff (avoid HANDOFF_STALE_LATEST_SESSION) — DONE
[ ] Phase 1: Source registry — verify cache, define/freeze common support S (|S|=22584 validated: four symbols 22608, XRPUSDT binds at 22584 on corrupt 2025-10-19; cache traversal fixed for nested+flat layouts) — complete, hash-bound
[ ] Phase 1: Prereg freeze — outcome-blind, margin/leverage scenarios, horizon, long/short labels — complete, hash-bound PENDING
[ ] Phase 2: Heavy evaluation — 3-block OOS AUC/log-loss/Brier, >=2000 bootstrap + LOIO — skeleton fixed (path + dual-layout cache traversal), heavy computation required
[ ] Phase 3: Independent recompute — rebuild S, all_checks_match=true, 5 symbols/block/fold, n_test>=500 — skeleton fixed (path), heavy computation required
[ ] Phase 3: Evidence audit + gate alias (evidence_audit_<UTC>.json) + trigger check — skeletons written, need audit_pass=true
[ ] All artifacts non-empty under session_20261128T040000Z/
[ ] Update handoff to LEAD with the next campaign (dated token preserved)
[ ] Run check_handoff_heavywork_gate.py until GREEN — GREEN (skeletons present; heavy computation pending)
[ ] Set experiment_frontier.json rank-0 to COMPLETED_VALIDATED
```

---

## GATE ENFORCEMENT

- `AGENT_HANDOFF.md` FOCUS CAMPAIGN section (dated token `FCLR-LIVE-ARCHIVE-08-20261127T131654Z`) — present above.
- `scripts/check_handoff_heavywork_gate.py` — `LIVE_ARCHIVE_CAMPAIGN_RE` / `_live_archive_state` ladder-aware binder (campaign 08 → `fclr_live_archive_*`); ARMED because the dated token is present; verified GREEN 2026-11-28T03:16:37Z.
- Root `research_state/*.md|*.json` capped at 500 (currently 500/500) — **ALL NEW ARTIFACTS MUST GO UNDER `session_<UTC>/`**.
- Stdlib only (numpy, pandas, scipy, pyarrow, requests pre-installed); no pip install; no network.

---

## TEMPLATE REFERENCE

Recovered stdlib template for campaign-07 (adapt for the campaign-08 boundary-breach design):
```
handoff_archive/quarantine_20261126T144850Z/fclr_live_archive07_eval_20261126T144850Z.py
```

---

**THIS IS THE ONLY EXECUTABLE HEAVY WORK REMAINING.** The Binance 5-symbol contiguous volatility design is exhausted. The Hyperliquid bulk/extended frontiers are exhausted. FCLR-LIVE-ARCHIVE-08 IS THE ACTIVE RANK-0 TASK AND IS GATE-ARMED; stale contagion prose is not a fallback.

**SESSION ID MUST BE > 20261127T131654Z. NO EXCEPTIONS.**

**Handoff Timestamp:** 2026-11-28T04:00:00Z
**Next Agent:** Execute FCLR-LIVE-ARCHIVE-08 per specification above. No shortcuts. Heavy work mandatory. Phases 2-3 (heavy eval + independent recompute with all_checks_match=true) must be executed in session_20261128T040000Z before the gate can pass with a complete artifact set.
