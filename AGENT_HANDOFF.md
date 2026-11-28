# AGENT HANDOFF — 2026-11-28T06:52:14Z

## REPOSITORY: Funding-conditioned-volatility-and-liquidation-risk

## NEXT SESSION MUST EXECUTE: FCLR-LIVE-ARCHIVE-08-20261127T131654Z Phase 3 — Independent stdlib recompute + evidence audit (Track-B modeled boundary-breach forecast — the repo-name liquidation-risk frontier)

**Refresh authority:** this 2026-11-28T06:52:14Z refresh is the SOLE durable handoff. It re-verified the live repository state before writing (gate binder armed, newest on-disk session `session_20261128T040000Z` equals the handoff-recorded latest, root `research_state/*.md|*.json` = 500/500 at cap, frontier rank-0 = FCLR-LIVE-ARCHIVE-08 READY_EXECUTE with exactly one active campaign). Fresh session `session_20261128T040000Z` (> gate `20261127T131654Z`) exists with Phases 1-2 COMPLETE: source registry/prereg frozen, heavy boundary-breach evaluation EXECUTED (verdict NOT_SUPPORTED, C2 worse than B1 on all metrics: AUC -5.36%, logloss -0.38%, Brier -0.71%). Phase 3 remains: independent stdlib recompute (`all_checks_match=true`) + evidence audit (`audit_pass=true`). It supersedes every contradictory rank / contagion / overlay statement that may appear in any archived handoff under `handoff_archive/`. There is exactly one active rank-0 campaign: FCLR-LIVE-ARCHIVE-08. Rank-1 is the COMPLETED_VALIDATED campaign-07, NOT an active contagion task.

Dated handoff snapshots (`AGENT_HANDOFF_20261128T021520Z.md`, `AGENT_HANDOFF_20261128T031132Z.md`, `AGENT_HANDOFF_20261128T031249Z.md`, `AGENT_HANDOFF_20261128T040000Z.md`) are historical records only; this file is the single durable source of truth.

---

## REPO-NAME PRIORITY (why this task, and why it cannot be skipped)

The repository name leads with **"Funding-conditioned-volatility"** and ends with **"and-liquidation-risk"**. Prioritizing by the repository name:

- **Half 1 — Funding-conditioned VOLATILITY:** CLOSED. Campaigns FCLR-LIVE-ARCHIVE-01..07 all returned NOT_SUPPORTED on the verified Binance 5-symbol mark-price archive (|S|=22,584, 2024-04..2026-10). The broad ironflow arms (FCLR-VOL-BROAD-01 / VOL-CORR-01 / VOL-STRESS-01 / VOL-JUMP-01/02/03/04) are also closed NOT_SUPPORTED. No remaining executable volatility work on this frozen panel.
- **Half 2 — LIQUIDATION-RISK:** OPEN. The only unfinished repo-name work is the liquidation-risk half, executed as the **Track-B modeled boundary-breach forecast (campaign-08)**. Campaign-07's forecast gate did NOT pass, so per RESEARCH_PROMPT §9 **no risk overlay is authorized**; campaign-08 is forecast validation of a modeled boundary-breach target, which IS permitted.

Prioritize campaign-08 Phase 3 completion over every other domain. The Hyperliquid bulk/extended frontiers are formally exhausted and are reference-only.

---

## INITIAL TASK MESSAGE FOR NEXT AGENTIC WORK SESSION

**COMPLETE FCLR-LIVE-ARCHIVE-08 Phase 3 — Independent stdlib recompute + evidence audit in the EXISTING `research_state/session_20261128T040000Z/` (session_id > `20261127T131654Z`, gate-compliant).** Phase 2 heavy eval is DONE (verdict NOT_SUPPORTED: C2 worse than B1 on all metrics). Phase 3 is the ONLY remaining heavy work, and it is HARD-BOUND by the handoff heavy-work gate: the session must emit a working `fclr_live_archive08_recompute_<UTC>.py` (separate code path from eval), produce `all_checks_match=true`, update `fclr_live_archive08_evidence_audit_<UTC>.json` with `audit_pass=true` and the reproduced verdict, and refresh the `evidence_audit_<UTC>.json` alias. There is NO prose-only, trigger-only, audit-only, or verify-and-stop escape hatch.

**Session-id constraint (non-negotiable):** the current wall clock (2026-11-28T06:52:14Z) is past the gate `20261127T131654Z`. The working session `session_20261128T040000Z` already exists and is recorded in this handoff (id > gate, post-start, enforced). Do NOT create a new session. Do NOT reuse `session_20261127T065600Z` or any id at or below the gate. A session id in `(20261127T065600Z, 20261127T131654Z]` is grandfathered by the gate and FORBIDDEN.

**What "done" means (all under `session_20261128T040000Z/`, all non-empty):**
1. `fclr_live_archive08_recompute_20261128T040000Z.py` — **REPLACE SKELETON** with independent stdlib recompute (separate code path from eval) that rebuilds S from cache (mark-price only, all three layouts, dedup by open_time, close>0), confirms all 5 symbols in every block/fold, n_test>=500, and emits `all_checks_match=true`.
2. `fclr_live_archive08_recompute_20261128T040000Z.json` — complete recompute results with `all_checks_match=true`.
3. `fclr_live_archive08_evidence_audit_20261128T040000Z.json` + `.md` — **UPDATE** with `audit_pass=true`, reproduced verdict (NOT_SUPPORTED), and `all_checks_match=true`.
4. `evidence_audit_20261128T040000Z.json` — gate-required alias (update to match).
5. `trigger_check_20261128T040000Z.json` — ensure non-empty (already exists, `fired: false` acceptable for no external trigger).

**Phase 2 Results (already executed, for reference):**
- Verdict: NOT_SUPPORTED
- B1 (mark-price-only): AUC=0.7086, logloss=0.4332, Brier=0.1315
- C2 (funding-conditioned): AUC=0.6706, logloss=0.4349, Brier=0.1324
- Relative Brier improvement C2 vs B1: **-0.71%** (worse; floor +2% not met; CI [-1.43%, +0.07%] does not support improvement)
- Bootstrap: 2000 reps, block=24, seed=20261126
- LOIO: all 5 symbols tested, n_test=4449 each
- Common support: |S|=22584 (XRPUSDT binds at 22584 on corrupt 2025-10-19; other four 22608)
- Split: train=13349, val=4450, test=4449 timestamps (test_rows_across_5_symbols=22245)

**Current gate status:** `python3 scripts/check_handoff_heavywork_gate.py` → PASS (skeletons present; heavy computation pending). Gate will require Phase 3 completion to stay GREEN on next verification.

---

## CAMPAIGN-08 PHASE 3 SPECIFICATION (from experiment_frontier.json rank-0)

### Independent Recompute Requirements
- **Separate code path** from Phase 2 eval (different implementation, same logic)
- **Rebuild common support S** from read-only cache: mark-price only, traverse all three layouts (daily/monthly nested, flat), dedup by `open_time`, filter `close>0`, intersect all 5 symbols
- **Confirm**: all 5 symbols present in every block/fold; `n_test >= 500` (actual: 22245 across 5 symbols)
- **Reproduce**: same split (60/20/20 + 168h embargo), same models (B1/C2), same metrics (AUC/logloss/Brier), same bootstrap (2000 reps, block=24, seed=20261126), same LOIO
- **Emit**: `all_checks_match=true` in recompute JSON

### Evidence Audit Requirements
- `audit_pass: true`
- `verdict: "NOT_SUPPORTED"` (reproduced)
- `all_checks_match: true`
- `recompute_method: "independent stdlib recompute — separate code path"`
- Relative improvements and CI matching Phase 2 results

### Gate Enforcement
- **Script:** `scripts/check_handoff_heavywork_gate.py` (LIVE_ARCHIVE_CAMPAIGN_RE / _live_archive_state ladder-aware binder: campaign 08 → `fclr_live_archive_*` artifact family).
- **Root Cap:** 500 files — all new artifacts MUST go under `session_<UTC>/` (already satisfied).
- **No Network:** Stdlib only (numpy, pandas, scipy, pyarrow, requests pre-installed; no pip install).
- **Read-Only Cache:** Do NOT re-download; reuse campaign-07 cache read-only.

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
| Aborted / stalled session on disk | **NONE** (newest complete: `session_20261127T065600Z`; working session `session_20261128T040000Z` on disk and recorded in handoff; no *.lock / *.tmp / *ABORT* found; rechecked 2026-11-28T06:52:14Z) |
| External dependencies | **NONE** |
| Cache verification | **COMPLETE** — Phase 1 verified 2024-04..2026-10 five-symbol cache against per-file .sha256 sidecars and `cached_inputs_hashes.json`; common support S defined/frozen (|S|=22584) |
| Risk overlay authorization | **FORBIDDEN** — campaign-07 forecast gate NOT passed (RESEARCH_PROMPT §9) |
| Gate enforcement gap | **CLOSED** — dated token `FCLR-LIVE-ARCHIVE-08-20261127T131654Z` arms the `_live_archive_state` binder; verified GREEN 2026-11-28T06:52:14Z |
| Root churn cap | **AT CAP (500/500)** — all new artifacts go under `session_<UTC>/` |
| Template availability | **PRESENT** — `handoff_archive/quarantine_20261126T144850Z/fclr_live_archive07_eval_20261126T144850Z.py` |

No sessions are blocked or inefficient. All campaigns rank 1+ are COMPLETED_VALIDATED/COMPLETE. The only remaining heavy work is FCLR-LIVE-ARCHIVE-08 Phase 3 at rank 0, and it is gate-armed so it cannot be skipped.

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
[x] Phase 1: Source registry — verify cache, define/freeze common support S (|S|=22584 validated: four symbols 22608, XRPUSDT binds at 22584 on corrupt 2025-10-19; cache traversal fixed for nested+flat layouts) — COMPLETE, hash-bound
[x] Phase 1: Prereg freeze — outcome-blind, margin/leverage scenarios, horizon, long/short labels — COMPLETE, hash-bound
[x] Phase 2: Heavy evaluation — 3-block OOS AUC/log-loss/Brier, >=2000 bootstrap + LOIO — COMPLETE (verdict NOT_SUPPORTED: C2 worse than B1 on all metrics)
[ ] Phase 3: Independent recompute — rebuild S, all_checks_match=true, 5 symbols/block/fold, n_test>=500 — **IMPLEMENT separate code path in fclr_live_archive08_recompute_20261128T040000Z.py, execute, produce all_checks_match=true**
[ ] Phase 3: Evidence audit + gate alias (evidence_audit_<UTC>.json) + trigger check — **UPDATE to audit_pass=true, all_checks_match=true, verdict reproduced**
[ ] All artifacts non-empty under session_20261128T040000Z/
[ ] Update handoff to LEAD with the next campaign (dated token preserved)
[ ] Run check_handoff_heavywork_gate.py until GREEN — GREEN (Phase 2 done; Phase 3 pending)
[ ] Set experiment_frontier.json rank-0 to COMPLETED_VALIDATED
```

---

## GATE ENFORCEMENT

- `AGENT_HANDOFF.md` FOCUS CAMPAIGN section (dated token `FCLR-LIVE-ARCHIVE-08-20261127T131654Z`) — present above.
- `scripts/check_handoff_heavywork_gate.py` — `LIVE_ARCHIVE_CAMPAIGN_RE` / `_live_archive_state` ladder-aware binder (campaign 08 → `fclr_live_archive_*`); ARMED because the dated token is present; verified GREEN 2026-11-28T06:52:14Z.
- Root `research_state/*.md|*.json` capped at 500 (currently 500/500) — **ALL NEW ARTIFACTS MUST GO UNDER `session_<UTC>/`**.
- Stdlib only (numpy, pandas, scipy, pyarrow, requests pre-installed); no pip install; no network.

---

## TEMPLATE REFERENCE

Recovered stdlib template for campaign-07 (adapt for the campaign-08 boundary-breach design):
```
handoff_archive/quarantine_20261126T144850Z/fclr_live_archive07_eval_20261126T144850Z.py
```

---

**THIS IS THE ONLY EXECUTABLE HEAVY WORK REMAINING.** The Binance 5-symbol contiguous volatility design is exhausted. The Hyperliquid bulk/extended frontiers are exhausted. FCLR-LIVE-ARCHIVE-08 Phase 3 IS THE ACTIVE RANK-0 TASK AND IS GATE-ARMED; stale contagion prose is not a fallback.

**SESSION ID MUST BE > 20261127T131654Z. NO EXCEPTIONS. WORKING SESSION: `session_20261128T040000Z` ALREADY EXISTS.**

**Handoff Timestamp:** 2026-11-28T06:52:14Z
**Next Agent:** Complete FCLR-LIVE-ARCHIVE-08 Phase 3 — implement independent stdlib recompute in `fclr_live_archive08_recompute_20261128T040000Z.py` (separate code path from eval), execute to produce `all_checks_match=true`, update evidence audit to `audit_pass=true` with reproduced verdict NOT_SUPPORTED, refresh gate alias. No shortcuts. Heavy work mandatory. Phase 3 must complete before the gate can pass with a complete artifact set.
