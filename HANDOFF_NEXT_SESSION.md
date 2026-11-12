# INITIAL TASK MESSAGE — NEXT AGENTIC WORK SESSION (SINGLE DURABLE HANDOFF)
**Repo:** `Funding-conditioned-volatility-and-liquidation-risk` (priority: funding-conditioned volatility AND liquidation risk — repo-name-prioritized)
**Handoff timestamp (UTC):** 2026-11-12T05:26:23Z (supersedes 2026-11-12T04:44:25Z; this file is the sole authoritative handoff)
**Status:** AUTHORITATIVE — execute this file only. `AGENT_HANDOFF.md`, `FOCUS_CAMPAIGN.md`, `NEXT_SESSION_TASK.md` are redirects. No competing root handoff files.

## Immediate task (heavy, in-session now)
Do not produce a status-only response. Execute the Focus Campaign below now.

### (A) Gate 4 Branch 1 — FIRST CHECK (deterministic, only if valid trigger exists)
- **Verified 2026-11-12T05:26:23Z:** `research_state/fclr016_local_audit/` contains **no** `fclr016_v5_terms_evidence_RESOLVED_*` with `status=RESOLVED_VERIFIED`, `fabricated=false`, and human/legal attestation. Highest local artifact remains unresolved (`fclr016_v5_terms_evidence_UNRESOLVED_20261108T204000Z.json`). **Do not wait/poll.**
- **If a valid RESOLVED trigger appears:** execute deterministic Branch 1 only — promotion + validators; on all-green run confirmatory Track C multi-split ablation + verdict + required state updates per Gate 4 protocol. Never guess, never set `fabricated=true`, never bypass.
- **If absent (current):** proceed immediately to (B)/(C).

### (B) Local + external new-data admissibility (RE-PROBED this session, evidenced)
- **Local inventory (complete):** `research_state/new_data_admissibility_audit_20261112T042738Z.md/.json` — **NO locally-admissible untested candidate.** All admissible cached-data volatility/liquidation designs on current HL/Binance caches EXHAUSTED/SEALED.
- **External probes (EXECUTED 2026-11-12T04:44:25Z):** evidence `research_state/new_data_external_probe_audit_20261112T044425Z.md/.json` (+ raw `external_probe_raw_20261112T044425Z.json`).
  - **HL public API `api.hyperliquid.xyz/info` (unauthenticated), 2026-11-01T00:00Z..now:** `candleSnapshot` 1h = **269 candles/coin** and `fundingHistory` = **269 records/coin** for 9 coins, covering ~2026-11-01..2026-11-12T04:00Z (~11.2 days). Feature-side feasible but **INSUFFICIENT for §16** (needs ≥3 non-overlapping 30-day test blocks with splits+embargo).
  - **Observed liquidation labels post-2026-10-31:** NONE verified. `ironflow/hyperliquid-liquidations` (HF, CC BY 4.0, `lastModified` 2026-11-07T10:18:25Z) event files still `2025-05..2026-10` only — no post-2026-10-31 labels. No other verifiable liquidation dataset found.
  - **`metpie/hyperliquid-liquidation-events`** (GitHub): 346,130 trades, 179 markets, **2025-03-22..2025-05-25** (node-trade reconstruction, CC BY 4.0) — historical, not post-sealed; not verifiably admissible now for a new multi-block claim without full §16 audit/alignment to HL funding/candles for that exact window.
- **Determination:** **NO verifiably admissible external source now.** Structural exhaustion documented with evidence. No prereg created.

## FOCUS CAMPAIGN (EXECUTE IN ORDER, HEAVY WORK REQUIRED)
1. **Gate 4 trigger check:** absent (verified). Do not re-poll. Execute Branch 1 only on valid RESOLVED trigger.
2. **Local + external admissibility:** DONE with evidence (above). Do not redo unchanged probes without a new signal (ironflow HF `lastModified`/file list change, or sufficient time for ≥100d HL window).
3. **Mandatory next heavy work — materially different free route (choose highest-value executable):**
   - **(Preferred when eligible)** When HL 2026-11+ has accumulated **≥100 contiguous days** of candles+funding for ≥5 ex-ante symbols **AND** a verifiable observed liquidation-label source covers the same post-2026-10-31 window with provenance/license/completeness per §16: run bounded acquisition (evidenced), freeze prereg **BEFORE outcomes**, then build+eval in-session if feasible; emit verdict + atomic state updates. (As of 2026-11-12T05:26:23Z: ~11 days available — not eligible.)
   - **Monitor/re-probe (bounded, evidence-backed):** Re-check `ironflow/humoring-hyperliquid-liquidations` HF metadata/file coverage for extension beyond 2026-10-31 and re-probe HL API coverage for the target window. Record timestamped evidence artifacts in `research_state/`. Perform as a bounded task when plausibly available, not a polling loop.
   - **Secondary audit (heavy, if feasible):** Full §16 admissibility audit of `metpie/hyperliquid-liquidation-events` (2025-03-22..2025-05-25) joined to HL funding/candles for that exact window — only if venue-consistent, ≥5 symbols, ≥3 non-overlapping 30d blocks, observed-label meaning/completeness acceptable, license/provenance documented, and not conflated with sealed verdicts. If admissible: prereg BEFORE outcomes → build/eval → verdict. If not: document with evidence.
4. **If no admissible path is verifiable in-session:** append/update timestamped probe/admissibility evidence in `research_state/` and keep `program_status=ACTIVE_HEAVY_CAMPAIGN`, `next_unfinished_task=EXTERNAL_NEW_DATA_SOURCE_MONITOR_AND_REPROBE`. Do not write a status-only memo; include probe outputs/URLs/status/schema/counts.
5. **State hygiene:** keep this file the single durable root handoff; keep redirects aligned. Preserve all sealed records/verdicts/manifests exactly as immutable.

## BOTTLENOCKS — STATUS & REQUIRED ACTION (2026-11-12T05:26:23Z)
| Bottleneck | Status | Removal/action |
|---|---|---|
| Gate 4 Branch 1 (external/legal Binance terms) | BLOCKED, not agent-removable | Execute Branch 1 only on valid RESOLVED trigger (`status=RESOLVED_VERIFIED`, `fabricated=false`, human/legal attestation). Not agent-actionable. |
| No untested admissible cached-data experiment | EXHAUSTED | Local + external probes complete; no new cached claim possible. |
| Post-2026-10-31 HL feature window too short (~11d as of 2026-11-12T05:26:23Z) | OPEN (time-dependent) | Re-probe HL API when ≥100d accumulated; evidence required. |
| Post-2026-10-31 observed liquidation labels unavailable (ironflow HF ends 2026-10-31) | OPEN (external dependency) | Monitor ironflow HF for extension; search for verifiable alternate observed-label sources. |
| Competing root handoff docs / session ambiguity | REMOVED | This file sole durable root handoff; redirects in place. |
| Multiple blocked/inefficient sessions | CLEARED | Single root handoff enforced; no parallel competing sessions; every session must deliver heavy work or evidence, never status-only. |
| Prior campaign items (volatility family, expansion/robustness, alternate volatility) | COMPLETED/SEALED | Do not reopen/retune/relitigate. |

## COMPLETED / SEALED — DO NOT REOPEN, RETUNE, OR RELITIGATE
- Track A liquidation expansion `TRACKA-HL-EXPANSION-20261111T195500Z` = **PASS** (C2 vs B1 rel QLIKE -19.04%, 95% CI [-5.088,-0.478], n=593, 8 instruments, 3 blocks, 2026-05..2026-10). Sealed.
- Track A liquidation expansion robustness `TRACKA-EXP-ROBUST-20261112T015119Z` = **FRAGILE** (LOIO FAIL 4/8, Placebo FAIL p≈0.07, Bootstrap PASS 3/3). Sealed.
- Track A alternate volatility `TRACKA-ALT-VOL-20261112T020322Z` = **NOT_MET** (6h, C2_ALT+rv72h, rel 5.77%, CI crosses zero). Sealed.
- Track A volatility primary 24h `TRACKA-VOL-20261111T234918Z` = **NOT_MET** (rel -1.37%, CI crosses zero). Sealed.
- Track A volatility family `TRACKA-VOL-FAMILY-20261112T005111Z` = **NOT_MET** (Holm, 12 comparisons). Sealed.
- Track A 9-symbol 2026-05..2026-10 liquidation = **NOT_MET** (closed). Track A early 2025-11..2026-04 = **INADMISSIBLE** (closed).
- Track B/C 2024 and H1/FCLR-002/003 contexts sealed/closed negative; H1 primary NOT_SUPPORTED on tested panels. Immutable.
- 2024 Binance confirmatory FCLR-003 = **NOT_SUPPORTED** (`research_state/final_confirmatory_verdict.md`). Immutable.

## HARD BANS (BINDING)
- No outcome inspection before prereg freeze. No threshold-shopping. No sealed-holdout reuse.
- No Binance/2024 conflation; venue-consistent artifacts only.
- No modeled/proxy/synthetic liquidation labels as observed.
- No `.github/workflows` edits. No redundant network polling. No agent-set `RESOLVED_VERIFIED`/`fabricated=true`; no Gate 4 bypass.
- **No status-only output.** Every session must deliver: Gate 4 Branch 1 if triggered, OR prereg + (build+eval or evidenced infeasibility) + state updates, OR a concrete timestamped new-data probe/admissibility audit with evidence.
- **No new experiments on exhausted cached data.** Any new claim requires NEW admissible data/source with provenance/license/coverage per RESEARCH_PROMPT.md §16.

## KEY REFERENCES
- This session probe: `research_state/new_data_external_probe_audit_20261112T044425Z.md`, `.json`, `research_state/external_probe_raw_20261112T044425Z.json`
- Prior probes: `research_state/new_data_external_probe_audit_20261112T043530Z.md`, `research_state/new_data_admissibility_audit_20261112T042738Z.md`
- Handoff/state: `research_state/experiment_frontier.json`, `research_state/hypothesis_registry.json`, `research_state/final_confirmatory_verdict.md`, `research_state/fclr016_local_audit/`
- Protocol: `RESEARCH_PROMPT.md` (§16 admissible new data)
- Sealed results: `research_state/evaluation_summary_TRACKA-HL-expansion-20261111T202344Z.md`, `research_state/evaluation_summary_TRACKA-EXP-ROBUST-20261112T015119Z.md`, `research_state/evaluation_summary_TRACKA-ALT-VOL-20261112T020322Z.md`, `research_state/evaluation_summary_TRACKA-VOL-20261111T234918Z.md`, `research_state/evaluation_summary_TRACKA-VOL-FAMILY-20261112T005111Z.md`

---
**Execute now:** Gate 4 check (absent) → run highest-value materially different free heavy task: bounded evidence-backed probe/reprobe for HL 2026-11+ coverage and ironflow HF label extension (when plausibly available) and/or full §16 audit of `metpie` for a feasible non-sealed design. If any candidate becomes verifiably admissible, freeze prereg + build/eval + verdict + state updates. Otherwise emit timestamped probe/audit evidence and keep `ACTIVE_HEAVY_CAMPAIGN` / `EXTERNAL_NEW_DATA_SOURCE_MONITOR_AND_REPROBE`. No status-only output.
