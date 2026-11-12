# INITIAL TASK MESSAGE — NEXT AGENTIC WORK SESSION (SINGLE DURABLE HANDOFF)
**Repo:** `Funding-conditioned-volatility-and-liquidation-risk` (priority: funding-conditioned volatility AND liquidation risk — repo-name-prioritized)
**Handoff timestamp (UTC):** 2026-11-12T06:27:01Z (supersedes 2026-11-12T05:44:30Z; this file is the sole authoritative handoff)
**Status:** AUTHORITATIVE — execute this file only. `AGENT_HANDOFF.md`, `FOCUS_CAMPAIGN.md`, `NEXT_SESSION_TASK.md` are redirects. No competing root handoff files.

## Progress snapshot (resolved bottlenecks removed)
- **Gate 4 Branch 1 trigger:** ABSENT (verified). `research_state/fclr016_local_audit/` highest artifact remains `fclr016_v5_terms_evidence_UNRESOLVED_20261108T204000Z.json`; no `fclr016_v5_terms_evidence_RESOLVED_*` with `status=RESOLVED_VERIFIED`, `fabricated=false`, human/legal attestation. **Do not wait/poll.** Branch 1 executes only on a valid RESOLVED trigger.
- **4h candle acquisition (prior blocker):** **REMOVED — COMPLETE.** `research_state/data_cache/hyperliquid_candles_4h/<COIN>/<YYYY-MM>.json` fetched+provenanced for BTC,ETH,BNB,SOL,XRP,AVAX,DOGE,LINK,SUI (2025-11..2026-04, 1086 bars/coin, 180 bars/block, full window coverage, 0 errors). Report: `research_state/tracka_hl_early_candle_fetch_4h_report_20261112T054104Z.json`. Script: `scripts/tracka_hl_fetch_candles_early_4h.py`. No redundant polling needed.
- **Prereg freeze (prior step):** **REMOVED — COMPLETE.** `research_state/tracka_prereg_hyperliquid_early_4h_20261112T054737Z.{json,md}` = `TRACKA-HL-EARLY-4H-20261112T054737Z`, status `PREREG_FROZEN_PRE_OUTCOMES`, frozen 2026-11-12T05:47:37Z. Window 2025-11-01..2026-04-30, 9 symbols, Hyperliquid-only, observed ironflow labels (CC BY 4.0), target = next-24h observed liquidation intensity, B1 (RV/context-only, 4h-derived) vs C2 (adds pre-specified funding-conditioned features), QLIKE lower better, materiality gate ≥2% rel reduction + CI excludes zero + ≥5 paired instruments + ≥3 non-overlapping 30-day OOS blocks + 7-day embargo, block bootstrap 2000 reps seed 20261112. **Immutable — do not edit; do not inspect outcomes before freeze (freeze already done).**
- **Known prereg caveat (documented pre-freeze):** Test Block 2 (2026-05-18..2026-06-16) extends beyond the 2026-04-30 window; effective test blocks within window are blocks 0 (2026-03-07..2026-04-05) and 1 partial (2026-04-12..2026-04-30) = **2 blocks < 3 required for PASS**. Prereg pre-specifies: if <3 blocks feasible, record PILOT/INCONCLUSIVE with exact shortfall. Panel build script `scripts/tracka_hl_build_early_4h_panel.py` (TS 20261112T054737Z) proceeds to evaluation when ≥5 paired instruments AND ≥2 test blocks have data; evaluation emits the gate verdict (PASS/NOT_MET/INCONCLUSIVE/INADMISSIBLE) with exact metrics/CI/n/blocks/instruments.

## Immediate task (heavy, in-session now) — PRIMARY route
Do not produce a status-only response. Execute the Focus Campaign below now. Every session must deliver concrete heavy work (build/eval/verdict/state updates) or, only if infeasible, a concrete timestamped evidence artifact — never a status-only memo.

1. **Build deterministic panel** (cached inputs only, no network):
   `python scripts/tracka_hl_build_early_4h_panel.py`
   -> `research_state/tracka_hl_early_4h_panel_20261112T054737Z.parquet` + `research_state/tracka_hl_early_4h_panel_build_report_20261112T054737Z.json`. Verify row counts, coverage, missingness/gap, input hashes, ≥5 paired instruments, test blocks with data.
2. **Evaluate pre-registered C2 vs B1** per frozen prereg (QLIKE on next-24h liquidation intensity, OLS on log(target+1e-12), training-only standardization, block bootstrap 2000 reps seed 20261112, 7-day embargo). Adapt `scripts/tracka_hl_evaluate_successor.py` pattern (fixed seed, no threshold-shopping) to the early-4h panel/splits. Emit verdict:
   `research_state/evaluation_summary_TRACKA-HL-EARLY-4H-20261112T054737Z.md` (+ `.json`) with exact metrics/CI/n/blocks/instruments and PASS/NOT_MET/INCONCLUSIVE/INADMISSIBLE per prereg.
3. **If deterministically infeasible (<3 test blocks / RV baseline unavailable / <5 instruments):** emit a concrete timestamped infeasibility/admissibility artifact citing exact failing minima/evidence (no status-only), then advance state to the next highest-value admissible heavy task (e.g. full §16 audit of `metpie/hyperliquid-liquidation-events` 2025-03-22..2025-05-25 joined to HL funding/candles for that exact window, only if feasible/venue-consistent/non-sealed; or bounded post-2026-10-31 reprobe only when HL ≥100d AND verifiable post-2026-10-31 observed labels exist).
4. **Atomic state updates:** append/update `research_state/experiment_frontier.json` (set next task based on outcome), `research_state/hypothesis_registry.json` (H_tracka_hl_early_liquidation_forecast), `research_state/run_manifest.json`, and addendum/note in `research_state/final_confirmatory_verdict.md` if confirmatory-relevant; keep sealed records immutable. Preserve provenance.

## FOCUS CAMPAIGN (EXECUTE IN ORDER, HEAVY WORK REQUIRED)
1. Gate 4 trigger check: absent (verified). Execute Branch 1 only on valid RESOLVED trigger.
2. **PRIMARY heavy task:** early-window liquidation forecast (4h cadence), funding-conditioned — build panel → evaluate C2 vs B1 → emit verdict + atomic state updates (steps 1-4 above). If infeasible, timestamped evidence + advance to next admissible heavy task.
3. State hygiene: keep this file the single durable root handoff; keep redirects aligned. Preserve all sealed records/verdicts/manifests exactly as immutable.

## BOTTLENECKS — STATUS & REQUIRED ACTION (2026-11-12T06:27:01Z)
| Bottleneck | Status | Removal/action |
|---|---|---|
| Early 2025-11..2026-04 RV/candles missing at 1h (prior blocker) | **REMOVED — COMPLETE** | 4h candles cached+provenanced for 9 coins, full window/blocks covered (`research_state/data_cache/hyperliquid_candles_4h/`, `tracka_hl_early_candle_fetch_4h_report_20261112T054104Z.json`). |
| Prereg freeze for early-4h claim | **REMOVED — COMPLETE** | `tracka_prereg_hyperliquid_early_4h_20261112T054737Z.{json,md}` frozen pre-outcomes 05:47:37Z. Immutable. |
| Panel build + C2-vs-B1 evaluation + verdict + state updates | **OPEN — PRIMARY ACTION** | Run `scripts/tracka_hl_build_early_4h_panel.py`; evaluate per prereg; emit `evaluation_summary_TRACKA-HL-EARLY-4H-20261112T054737Z.{md,json}`; atomic state updates. |
| Gate 4 Branch 1 (external/legal Binance terms) | BLOCKED, not agent-removable | Execute Branch 1 only on valid RESOLVED_VERIFIED trigger (`status=RESOLVED_VERIFIED`, `fabricated=false`, human/legal attestation). |
| Prereg <3 test-block caveat (within 2026-04-30 window) | DOCUMENTED (pre-freeze) | If evaluation yields <3 feasible blocks, emit PILOT/INCONCLUSIVE/INADMISSIBLE with exact shortfall; not a reopening. |
| Cached-data exhaustion on prior designs (1h/24h tested paths) | PARTIALLY RELIEVED | New admissible 4h early-window design available; do not reopen sealed designs. |
| Post-2026-10-31 HL window too short (~11d) / no verified post-2026-10-31 observed labels | OPEN (secondary) | Only after (2) completes/fails with evidence: bounded reprobe/monitor with evidence; no polling. |

## COMPLETED / SEALED — DO NOT REOPEN, RETUNE, OR RELITIGATE
- `TRACKA-HL-EARLY-20261111T191958Z` = **INADMISSIBLE** under 1h-candle assumption (sealed record). 4h redesign is a new preregistered claim, not a reopening.
- Track A liquidation expansion `TRACKA-HL-EXPANSION-20261111T195500Z` = **PASS** (robustness **FRAGILE**, `TRACKA-EXP-ROBUST-20261112T015119Z`). Sealed.
- Track A alternate volatility `TRACKA-ALT-VOL-20261112T020322Z` = **NOT_MET**. Sealed.
- Track A volatility primary 24h `TRACKA-VOL-20261111T234918Z` = **NOT_MET**; volatility family `TRACKA-VOL-FAMILY-20261112T005111Z` = **NOT_MET**. Sealed.
- Track A 9-symbol 2026-05..2026-10 liquidation = **NOT_MET** (closed). Track B/C 2024 and H1/FCLR-002/003 contexts sealed/closed negative; H1 primary NOT_SUPPORTED on tested panels. 2024 Binance confirmatory FCLR-003 = **NOT_SUPPORTED** (`research_state/final_confirmatory_verdict.md`). Immutable.

## HARD BANS (BINDING)
- **No outcome inspection before prereg freeze** for the new early-4h claim (freeze already done at 05:47:37Z — do not re-freeze or edit). No threshold-shopping. No sealed-holdout reuse.
- No Binance/2024 conflation; venue-consistent artifacts only. No modeled/proxy/synthetic liquidation labels as observed.
- No `.github/workflows` edits. No redundant network polling. No agent-set `RESOLVED_VERIFIED`/`fabricated=true`; no Gate 4 bypass.
- **No status-only output.** Every session must deliver: Gate 4 Branch 1 if triggered, OR early-4h build+eval+verdict+state updates, OR evidenced infeasibility + state updates, OR a concrete timestamped probe/admissibility audit with evidence.
- Do not relitigate or retune sealed verdicts; 4h early-window work is a distinct pre-specified design.

## KEY REFERENCES
- **Primary (next action):** `scripts/tracka_hl_build_early_4h_panel.py`, prereg `research_state/tracka_prereg_hyperliquid_early_4h_20261112T054737Z.{json,md}`, candles `research_state/data_cache/hyperliquid_candles_4h/`, labels `research_state/data_cache/ironflow_events/2025-11..2026-04.parquet`, funding `research_state/data_cache/hyperliquid_funding/`, fetch report `research_state/tracka_hl_early_candle_fetch_4h_report_20261112T054104Z.json`.
- Eval pattern template: `scripts/tracka_hl_evaluate_successor.py` (fixed seed, block bootstrap, gate criteria).
- Prior early record (sealed, 1h): `research_state/evaluation_summary_TRACKA-HL-early-infeasible-20261111T193500Z.md`, `research_state/tracka_prereg_hyperliquid_early_20261111T191958Z.{json,md}`.
- External probes: `research_state/new_data_external_probe_audit_20261112T044425Z.{md,json}`, `research_state/external_probe_raw_20261112T044425Z.json`; local audit `research_state/new_data_admissibility_audit_20261112T042738Z.md`.
- Handoff/state: `research_state/experiment_frontier.json`, `research_state/hypothesis_registry.json`, `research_state/final_confirmatory_verdict.md`, `research_state/fclr016_local_audit/`.
- Protocol: `RESEARCH_PROMPT.md` (§16 admissible new data).

---
**Execute now:** Gate 4 check (absent) → run `scripts/tracka_hl_build_early_4h_panel.py` → evaluate pre-registered C2 vs B1 liquidation-forecast claim → emit verdict + atomic state updates. If deterministically infeasible, emit timestamped evidence artifact and advance to next admissible heavy task. No status-only output.
