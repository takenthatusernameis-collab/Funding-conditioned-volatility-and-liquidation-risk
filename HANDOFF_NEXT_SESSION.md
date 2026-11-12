# INITIAL TASK MESSAGE — NEXT AGENTIC WORK SESSION (SINGLE DURABLE HANDOFF)
**Repo:** `Funding-conditioned-volatility-and-liquidation-risk` (priority: funding-conditioned volatility AND liquidation risk — repo-name-prioritized)
**Handoff timestamp (UTC):** 2026-11-12T05:44:30Z (supersedes 2026-11-12T05:30:24Z; this file is the sole authoritative handoff)
**Status:** AUTHORITATIVE — execute this file only. `AGENT_HANDOFF.md`, `FOCUS_CAMPAIGN.md`, `NEXT_SESSION_TASK.md` are redirects. No competing root handoff files.

## Immediate task (heavy, in-session now)
Do not produce a status-only response. Execute the Focus Campaign below now. Every session must deliver concrete heavy work (prereg/build/eval/verdict/state updates) or, only if infeasible, a concrete timestamped evidence artifact — never a status-only memo.

### (A) Gate 4 Branch 1 — FIRST CHECK (deterministic, only if valid trigger exists)
- **Verified 2026-11-12T05:44:30Z:** `research_state/fclr016_local_audit/` contains **no** `fclr016_v5_terms_evidence_RESOLVED_*` with `status=RESOLVED_VERIFIED`, `fabricated=false`, and human/legal attestation. Highest local artifact remains unresolved (`fclr016_v5_terms_evidence_UNRESOLVED_20261108T204000Z.json`). **Do not wait/poll.**
- **If a valid RESOLVED trigger appears:** execute deterministic Branch 1 only — promotion + validators; on all-green run confirmatory Track C multi-split ablation + verdict + required state updates per Gate 4 protocol. Never guess, never set `fabricated=true`, never bypass.
- **If absent (current):** proceed immediately to (B)/(C).

### (B) Material unblock discovered (evidence; do not ignore)
Prior early-window claim `TRACKA-HL-EARLY-20261111T191958Z` was **INADMISSIBLE** only because 1h `candleSnapshot` returned empty historical rows (`research_state/evaluation_summary_TRACKA-HL-early-infeasible-20261111T193500Z.md`).
**New evidence (2026-11-12T05:40:21Z):** Hyperliquid `candleSnapshot` at **4h** interval returns complete historical candles for 2025-11-01..2026-04-30.
- Candles cached+provenanced: `research_state/data_cache/hyperliquid_candles_4h/<COIN>/2025-{11,12},2026-{01..04}.{json,accessed.json,sha256}` for BTC,ETH,BNB,SOL,XRP,AVAX,DOGE,LINK,SUI (9 coins, 1086 bars/coin, 180 bars/block in each prereg test block; full coverage). Fetch report: `research_state/tracka_hl_early_candle_fetch_4h_report_20261112T054104Z.json`. Script: `scripts/tracka_hl_fetch_candles_early_4h.py`.
- Observed liquidation labels (ironflow, CC BY 4.0, Hyperliquid-only): cached `research_state/data_cache/ironflow_events/2025-11..2026-04.parquet` present.
- Funding context: cached `research_state/data_cache/hyperliquid_funding/{9 coins}.json` covers ~2025-11-01..2026-10-30 (8668 rows/coin), window-covered.
=> **Early 2025-11..2026-04 observed-liquidation+funding panel is plausibly admissible on 4h cadence and is the highest-priority untested repo-relevant heavy path.** Treat 4h as a **new design/cadence** vs the frozen 1h early prereg; do not relitigate sealed 2026-05..2026-10 outcomes.

## FOCUS CAMPAIGN (EXECUTE IN ORDER, HEAVY WORK REQUIRED)
1. **Gate 4 trigger check:** absent (verified). Execute Branch 1 only on valid RESOLVED trigger.
2. **PRIMARY heavy task — early-window liquidation forecast (4h cadence), funding-conditioned:**
   - **Freeze a NEW prereg BEFORE any panel alignment, outcome computation, or evaluation** (new experiment_id/timestamp, e.g. `TRACKA-HL-EARLY-4H-<UTC>`): `research_state/tracka_prereg_hyperliquid_early_4h_<UTC>.{json,md}`. State explicitly: 4h candle design (supersedes 1h acquisition assumption of `TRACKA-HL-EARLY-20261111T191958Z` only for cadence/data-availability), Hyperliquid-only, observed ironflow labels only (not modeled/proxy), 9 symbols (or ex-ante subset with rule frozen pre-outcomes), window 2025-11-01..2026-04-30, target = next-24h observed liquidation intensity per symbol per 24h UTC bucket (notional_usd-weighted event count) aggregated from ironflow events, B1 (RV/context-only baseline, 4h-derived, pre-specified) vs C2 (adds pre-specified funding-conditioned features), QLIKE (lower better), ≥5 paired instruments, ≥3 non-overlapping 30-day OOS blocks with 7-day embargo (reuse/adapt feasible split logic but freeze exact boundaries pre-outcomes), materiality gate per protocol (e.g. ≥2% relative reduction, CI excludes zero) — all frozen pre-outcomes. Define RV/baseline/feature construction from 4h closes deterministically and ex-ante. Include infeasibility rule.
   - **Build deterministic panel** from cached 4h candles + cached funding + cached ironflow events (venue-consistent, provenance-backed). No redundant network polling; no new acquisition unless a bounded, evidenced gap remains.
   - **Evaluate pre-registered C2 vs B1** and emit verdict: `research_state/evaluation_summary_TRACKA-HL-EARLY-4H-<UTC>.md` (and result json) with exact metrics/CI/n/blocks/instruments and PASS/NOT_MET/INCONCLUSIVE/INADMISSIBLE per prereg. No threshold-shopping.
   - **Atomic state updates:** append/update `research_state/experiment_frontier.json` (set next task based on outcome), `research_state/hypothesis_registry.json` as applicable, `research_state/run_manifest.json`, and addendum/note in `research_state/final_confirmatory_verdict.md` if confirmatory-relevant; keep sealed records immutable. Preserve provenance.
3. **If (2) becomes infeasible after deterministic evidence:** emit a concrete timestamped infeasibility/admissibility artifact citing exact failing minima/evidence (no status-only), update state to the next highest-value admissible heavy task (e.g. full §16 audit of `metpie/hyperliquid-liquidation-events` 2025-03-22..2025-05-25 joined to HL funding/candles for that exact window, only if feasible/venue-consistent/non-sealed; or bounded reprobe when HL post-2026-10-31 ≥100d AND verifiable post-2026-10-31 observed labels exist). When reprobing/monitoring, record timestamped evidence (URLs/status/counts/schema/coverage), not a polling loop.
4. **State hygiene:** keep this file the single durable root handoff; keep redirects aligned. Preserve all sealed records/verdicts/manifests exactly as immutable.

## BOTTLENECKS — STATUS & REQUIRED ACTION (2026-11-12T05:44:30Z)
| Bottleneck | Status | Removal/action |
|---|---|---|
| Early 2025-11..2026-04 RV/candles missing at 1h (prior blocker) | **REMOVED** | 4h candles cached+provenanced for 9 coins, full window/blocks covered (`research_state/data_cache/hyperliquid_candles_4h/`, `tracka_hl_early_candle_fetch_4h_report_20261112T054104Z.json`). Execute prereg+build+eval now. |
| Stale handoff/frontier pointed to passive monitor | **REMOVED** | This handoff + frontier updated to require early-4h heavy execution as primary. |
| Gate 4 Branch 1 (external/legal Binance terms) | BLOCKED, not agent-removable | Execute Branch 1 only on valid RESOLVED trigger (`status=RESOLVED_VERIFIED`, `fabricated=false`, human/legal attestation). |
| Cached-data exhaustion on prior designs (1h/24h tested paths) | PARTIALLY RELIEVED | New admissible 4h early-window design available; do not reopen sealed designs. |
| Post-2026-10-31 HL window too short (~11d) / no verified post-2026-10-31 observed labels | OPEN (secondary) | Only after (2) completes/fails with evidence: bounded reprobe/monitor with evidence; no polling. |

## COMPLETED / SEALED — DO NOT REOPEN, RETUNE, OR RELITIGATE
- `TRACKA-HL-EARLY-20261111T191958Z` = **INADMISSIBLE** under 1h-candle assumption (sealed record). 4h redesign is a new preregistered claim, not a reopening.
- Track A liquidation expansion `TRACKA-HL-EXPANSION-20261111T195500Z` = **PASS** (robustness **FRAGILE**, `TRACKA-EXP-ROBUST-20261112T015119Z`). Sealed.
- Track A alternate volatility `TRACKA-ALT-VOL-20261112T020322Z` = **NOT_MET**. Sealed.
- Track A volatility primary 24h `TRACKA-VOL-20261111T234918Z` = **NOT_MET**; volatility family `TRACKA-VOL-FAMILY-20261112T005111Z` = **NOT_MET**. Sealed.
- Track A 9-symbol 2026-05..2026-10 liquidation = **NOT_MET** (closed). Track B/C 2024 and H1/FCLR-002/003 contexts sealed/closed negative; H1 primary NOT_SUPPORTED on tested panels. 2024 Binance confirmatory FCLR-003 = **NOT_SUPPORTED** (`research_state/final_confirmatory_verdict.md`). Immutable.

## HARD BANS (BINDING)
- **No outcome inspection before prereg freeze** for the new early-4h claim. No threshold-shopping. No sealed-holdout reuse.
- No Binance/2024 conflation; venue-consistent artifacts only. No modeled/proxy/synthetic liquidation labels as observed.
- No `.github/workflows` edits. No redundant network polling. No agent-set `RESOLVED_VERIFIED`/`fabricated=true`; no Gate 4 bypass.
- **No status-only output.** Every session must deliver: Gate 4 Branch 1 if triggered, OR early-4h prereg + (build+eval+verdict+state updates) or evidenced infeasibility + state updates, OR a concrete timestamped probe/admissibility audit with evidence.
- Do not relitigate or retune sealed verdicts; 4h early-window work is a distinct pre-specified design.

## KEY REFERENCES
- **This unblock (primary):** `research_state/tracka_hl_early_candle_fetch_4h_report_20261112T054104Z.json`, `research_state/data_cache/hyperliquid_candles_4h/`, `scripts/tracka_hl_fetch_candles_early_4h.py`, labels `research_state/data_cache/ironflow_events/2025-11..2026-04.parquet`, funding `research_state/data_cache/hyperliquid_funding/`
- Prior early record (sealed, 1h): `research_state/evaluation_summary_TRACKA-HL-early-infeasible-20261111T193500Z.md`, `research_state/tracka_prereg_hyperliquid_early_20261111T191958Z.{json,md}`, `research_state/tracka_hl_early_candle_fetch_report_20261111T193140Z.json`
- External probes: `research_state/new_data_external_probe_audit_20261112T044425Z.md`, `.json`, `research_state/external_probe_raw_20261112T044425Z.json`; local audit `research_state/new_data_admissibility_audit_20261112T042738Z.md`
- Handoff/state: `research_state/experiment_frontier.json`, `research_state/hypothesis_registry.json`, `research_state/final_confirmatory_verdict.md`, `research_state/fclr016_local_audit/`
- Protocol: `RESEARCH_PROMPT.md` (§16 admissible new data)

---
**Execute now:** Gate 4 check (absent) → **freeze new 4h early-window prereg (before outcomes)** → build deterministic panel from cached 4h candles/funding/ironflow → evaluate pre-registered C2 vs B1 liquidation-forecast claim → emit verdict + atomic state updates. If deterministically infeasible, emit timestamped evidence artifact and advance to next admissible heavy task. No status-only output.
