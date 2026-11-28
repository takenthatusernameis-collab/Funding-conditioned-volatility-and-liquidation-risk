# AGENT HANDOFF — 2026-11-28T06:52:14Z

## REPOSITORY: Funding-conditioned-volatility-and-liquidation-risk

## NEXT SESSION: FCLR-LIVE-ARCHIVE-08 COMPLETE — Phase 3 independent stdlib recompute + evidence audit finished; verdict NOT_SUPPORTED; no further heavy work (verification-only posture)

**Refresh authority:** this 2026-11-28T06:52:14Z refresh is the SOLE durable handoff. It re-verified the live repository state before writing (gate binder armed, newest on-disk session `session_20261128T040000Z` equals the handoff-recorded latest, root `research_state/*.md|*.json` = 500/500 at cap, frontier rank-0 = FCLR-LIVE-ARCHIVE-08 COMPLETED_VALIDATED with no active campaign). Fresh session `session_20261128T040000Z` (> gate `20261127T131654Z`) exists with Phases 1-3 COMPLETE: source registry/prereg frozen, heavy boundary-breach evaluation EXECUTED (verdict NOT_SUPPORTED, C2 worse than B1 on all metrics: AUC -5.36%, logloss -0.38%, Brier -0.71%), independent stdlib recompute `all_checks_match=true`, evidence audit `audit_pass=true`. All Phase 3 work complete; `all_checks_match=true` and `audit_pass=true` reproduced under session_20261128T040000Z. It supersedes every contradictory rank / contagion / overlay statement that may appear in any archived handoff under `handoff_archive/`. No active rank-0 campaign remains; Rank-1 is the COMPLETED_VALIDATED campaign-07.

Dated handoff snapshots (`AGENT_HANDOFF_20261128T021520Z.md`, `AGENT_HANDOFF_20261128T031132Z.md`, `AGENT_HANDOFF_20261128T031249Z.md`, `AGENT_HANDOFF_20261128T040000Z.md`) are historical records only; this file is the single durable source of truth.

---

## REPO-NAME PRIORITY (why this task, and why it cannot be skipped)

The repository name leads with **"Funding-conditioned-volatility"** and ends with **"and-liquidation-risk"**. Prioritizing by the repository name:

- **Half 1 — Funding-conditioned VOLATILITY:** CLOSED. Campaigns FCLR-LIVE-ARCHIVE-01..07 all returned NOT_SUPPORTED on the verified Binance 5-symbol mark-price archive (|S|=22,584, 2024-04..2026-10). The broad ironflow arms (FCLR-VOL-BROAD-01 / VOL-CORR-01 / VOL-STRESS-01 / VOL-JUMP-01/02/03/04) are also closed NOT_SUPPORTED. No remaining executable volatility work on this frozen panel.
- **Half 2 — LIQUIDATION-RISK:** CLOSED NOT_SUPPORTED. Campaign-08 (Track-B modeled boundary-breach forecast) completed under session_20261128T040000Z: independent stdlib recompute `all_checks_match=true`, evidence audit `audit_pass=true`, verdict NOT_SUPPORTED (C2 worse than B1 on all metrics: AUC -5.36%, logloss -0.38%, Brier -0.71%). Campaign-07's forecast gate did NOT pass, so per RESEARCH_PROMPT §9 **no risk overlay is authorized**; campaign-08 was forecast validation of a modeled boundary-breach target, which was permitted.

All repo-name work complete: Half 1 (funding-conditioned volatility) CLOSED NOT_SUPPORTED on the verified 5-symbol archive; Half 2 (liquidation-risk) CLOSED NOT_SUPPORTED. No remaining executable heavy work on this frozen panel.

---

## INITIAL TASK MESSAGE FOR NEXT AGENTIC WORK SESSION — VERIFICATION ONLY (no heavy work remaining)

FCLR-LIVE-ARCHIVE-08 is COMPLETE. All Phase 3 work finished under `research_state/session_20261128T040000Z/`:
- `fclr_live_archive08_recompute_20261128T040000Z.py` — independent stdlib recompute executed, `all_checks_match=true`
- `fclr_live_archive08_recompute_20261128T040000Z.json` — complete recompute results, `all_checks_match=true`
- `fclr_live_archive08_evidence_audit_20261128T040000Z.json` + `.md` — `audit_pass=true`, verdict NOT_SUPPORTED reproduced
- `evidence_audit_20261128T040000Z.json` — gate alias updated, `audit_pass=true`
- `trigger_check_20261128T040000Z.json` — present (non-empty)

Verdict: NOT_SUPPORTED (C2 worse than B1 on all metrics: AUC -5.36%, logloss -0.38%, Brier -0.71%).
Common support: |S|=22584; split train=13349/val=4450/test=4449.
Bootstrap: 2000 reps, block=24, seed=20261126.

**Next session: run `python3 scripts/check_handoff_heavywork_gate.py` to confirm GREEN.** No further heavy work, no new session, no re-runs. All repo-name work (Half 1 volatility + Half 2 liquidation-risk) is CLOSED NOT_SUPPORTED on the verified Binance 5-symbol archive.

**Phase 2 Results (already executed, for reference):**
- Verdict: NOT_SUPPORTED
- B1 (mark-price-only): AUC=0.7086, logloss=0.4332, Brier=0.1315
- C2 (funding-conditioned): AUC=0.6706, logloss=0.4349, Brier=0.1324
- Relative Brier improvement C2 vs B1: **-0.71%** (worse; floor +2% not met; CI [-1.43%, +0.07%] does not support improvement)
- Bootstrap: 2000 reps, block=24, seed=20261126
- LOIO: all 5 symbols tested, n_test=4449 each
- Common support: |S|=22584 (XRPUSDT binds at 22584 on corrupt 2025-10-19; other four 22608)
- Split: train=13349, val=4450, test=4449 timestamps (test_rows_across_5_symbols=22245)

**Current gate status:** `python3 scripts/check_handoff_heavywork_gate.py` → PASS (complete artifact set; Phase 3 done). Verify GREEN on next session.

---

## CAMPAIGN-08 PHASE 3 SPECIFICATION (from experiment_frontier.json rank-0) — COMPLETE

All requirements verified satisfied under `session_20261128T040000Z/`:

- **Separate code path** from Phase 2 eval: `fclr_live_archive08_recompute_20261128T040000Z.py` uses a distinct stdlib implementation (csv.DictReader + os.walk + distinct feature/bootstrap/AUC paths) vs the Phase 2 eval (`fclr_live_archive08_eval_20261128T040000Z.py`).
- **Rebuilt common support S** from read-only cache: mark-price only, traversed all three layouts, dedup by `open_time`, filter `close>0`, intersected all 5 symbols → |S|=22584.
- **Confirmed**: all 5 symbols present in every block/fold; `n_test >= 500` (actual: 22245 across 5 symbols).
- **Reproduced**: same split (60/20/20 + 168h embargo: train=13349/val=4450/test=4449), same models (B1/C2), same metrics (AUC/logloss/Brier), same bootstrap (2000 reps, block=24, seed=20261126), same LOIO.
- **Emitted**: `all_checks_match=true` in recompute JSON.
- **Evidence audit**: `audit_pass: true`, `verdict: "NOT_SUPPORTED"` reproduced, `all_checks_match: true`, relative improvements and CI match Phase 2 results.
- **Gate**: `python3 scripts/check_handoff_heavywork_gate.py` → PASS. Root cap 500 satisfied (all artifacts under `session_<UTC>/`). No network; stdlib only; read-only cache.

## FOCUS CAMPAIGN (heavy work — COMPLETE, no further heavy work)

FCLR-LIVE-ARCHIVE-08 (dated token `FCLR-LIVE-ARCHIVE-08-20261127T131654Z`) is COMPLETE. The campaign-08 artifact family `fclr_live_archive_*` is fully produced and non-empty under `session_20261128T040000Z/`, plus a non-empty `trigger_check_20261128T040000Z.json`.

- Gate resolves latest `session_<UTC>` id recorded here vs latest on-disk: both `session_20261128T040000Z` — consistent, no `HANDOFF_STALE_LATEST_SESSION`.
- Root `research_state/*.md|*.json` capped at 500 (currently 500/500). **ALL artifacts under `session_<UTC>/`, never the root.**
- Stdlib only; no pip install; no network; cache read-only.

No remaining heavy work. The volatility half is exhausted; the liquidation-risk half is CLOSED NOT_SUPPORTED. This was a materially different, feasible design on the SAME frozen, verified panel — not a re-run of a terminal endpoint.

---

## POST-EXECUTION HANDOFF UPDATE (complete — no further action required)

All post-execution steps done:
1. Handoff updated to reflect campaign-08 COMPLETE; dated token preserved so the gate stays armed.
2. Session id `session_20261128T040000Z` recorded (newest on-disk session not newer than handoff-recorded).
3. `python3 scripts/check_handoff_heavywork_gate.py` → GREEN (verified 2026-11-28).
4. Rank-0 set to `COMPLETED_VALIDATED` in `research_state/experiment_frontier.json` with reproduced verdict NOT_SUPPORTED.
5. No further campaign to promote; no remaining heavy work; verification-only posture going forward.

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

No sessions are blocked or inefficient. All campaigns are COMPLETED_VALIDATED/COMPLETE. No remaining heavy work; FCLR-LIVE-ARCHIVE-08 Phase 3 completed under session_20261128T040000Z (gate-armed, verified GREEN). Verification-only posture going forward.

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
[x] Phase 3: Independent recompute — rebuild S, all_checks_match=true, 5 symbols/block/fold, n_test>=500 — COMPLETE (fclr_live_archive08_recompute_20261128T040000Z.py, separate code path; all_checks_match=true)
[x] Phase 3: Evidence audit + gate alias + trigger check — COMPLETE (audit_pass=true, all_checks_match=true, verdict reproduced NOT_SUPPORTED)
[x] All artifacts non-empty under session_20261128T040000Z/ — VERIFIED
[x] Update handoff to reflect campaign COMPLETE (dated token preserved) — DONE
[x] Run check_handoff_heavywork_gate.py until GREEN — GREEN
[x] Set experiment_frontier.json rank-0 to COMPLETED_VALIDATED — DONE
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

**ALL EXECUTABLE HEAVY WORK COMPLETE.** The Binance 5-symbol contiguous volatility design is exhausted (Half 1 CLOSED NOT_SUPPORTED). The Hyperliquid bulk/extended frontiers are exhausted. FCLR-LIVE-ARCHIVE-08 Phase 3 completed under session_20261128T040000Z (Half 2 CLOSED NOT_SUPPORTED); the gate is verified GREEN. Stale contagion prose is not a fallback; there is no remaining rank-0 heavy task.

**SESSION ID:** `session_20261128T040000Z` (> `20261127T131654Z`, gate-compliant, already on disk).

**Handoff Timestamp:** 2026-11-28T08:03:59Z
**Next Agent:** Verification-only — run `python3 scripts/check_handoff_heavywork_gate.py` to confirm GREEN. No further heavy work, no new session, no re-runs. All repo-name work (Half 1 volatility + Half 2 liquidation-risk) is CLOSED NOT_SUPPORTED on the verified Binance 5-symbol archive.
