# INITIAL TASK MESSAGE — NEXT AGENTIC WORK SESSION (SINGLE DURABLE HANDOFF)
**Repo:** `Funding-conditioned-volatility-and-liquidation-risk` (priority: funding-conditioned volatility AND liquidation risk — repo-name-prioritized)
**Handoff timestamp (UTC):** 2026-11-12T04:35:30Z (supersedes 2026-11-12T04:30:17Z; this file remains the sole authoritative handoff)
**Status:** AUTHORITATIVE — execute this file only. `AGENT_HANDOFF.md`, `FOCUS_CAMPAIGN.md`, `NEXT_SESSION_TASK.md` are redirects. No competing root handoff files.

## Immediate task (heavy, in-session now)
Do not produce a status-only response. Execute the Focus Campaign below now.

### (A) Gate 4 Branch 1 — FIRST CHECK (deterministic, only if valid trigger exists)
- **Verified 2026-11-12T04:32:39Z:** `research_state/fclr016_local_audit/` contains **no** `fclr016_v5_terms_evidence_RESOLVED_*` with `status=RESOLVED_VERIFIED`, `fabricated=false`, and human/legal attestation. Highest local artifact is `fclr016_v5_terms_evidence_UNRESOLVED_20261108T204000Z.json` (`confirmatory_claim_go=NO_GO`, `status=UNRESOLVED`, reviewer_role=pending_human_legal_maintainer). **Do not wait/poll.**
- **If a valid RESOLVED trigger appears:** execute deterministic Branch 1 only — promotion + validators; on all-green run confirmatory Track C multi-split ablation + verdict + required state updates per Gate 4 protocol. Never guess, never set `fabricated=true`, never bypass.
- **If absent (current):** proceed immediately to (B)/(C).

### (B) Local + external new-data admissibility (EXECUTED this session, evidenced)
- **Local inventory (complete, prior):** `research_state/new_data_admissibility_audit_20261112T042738Z.md/.json` — **NO locally-admissible untested candidate.** All admissible cached-data volatility/liquidation designs on current HL/Binance caches EXHAUSTED/SEALED (HL funding 2025-11..2026-10 feature-only exhausted; HL candles 2026-05..2026-10 exhausted, 2025-11..2026-04 inadmissible/empty; ironflow labels 2025-05..2026-10 paired with exhausted window; craftify insufficient/provenance-unverified; Binance sealed/inadmissible for Track A).
- **External acquisition probes (EXECUTED 2026-11-12T04:35:30Z):** `research_state/new_data_external_probe_audit_20261112T043530Z.md/.json` (+ raw: `external_new_data_probe_20261112T043403Z.json`, `hyperliquid_nov2026_coverage_probe_20261112T043403Z.json`, `external_new_data_probe_followup_20261112T043437Z.json`).
  - **HL public API (unauthenticated, `api.hyperliquid.xyz/info`) 2026-11-01..2026-11-11:** `candleSnapshot` 1h = **241 candles/coin** and `fundingHistory` = **240 records/coin** for 9 coins (BTC,ETH,BNB,SOL,XRP,AVAX,DOGE,LINK,SUI). Feature-side feasible but **window ~10 days — INSUFFICIENT for §16** (needs ≥3 non-overlapping 30-day test blocks with splits+embargo).
  - **Observed liquidation labels post-2026-10-31:** NONE verified. `ironflow/hyperliquid-liquidations` (HF, CC BY 4.0, lastModified 2026-11-07T10:18:25Z) still covers **2025-05-25..2026-10-31** only (same as sealed cache). ironflow GitHub repo/contents/releases = 404. HF search surfaced no other liquidation dataset.
  - **`metpie/hyperliquid-liquidation-events`** (GitHub): 346k trades, 179 markets, **2025-03-22..2025-05-25** (node-trade reconstruction) — historical, not post-sealed; **not verifiably admissible now** for a new multi-block claim without full §16 audit/alignment (deferred, evidence captured).
- **Determination:** **NO verifiably admissible external source now** for a new claim (features too-short window and/or no post-2026-10-31 observed liquidation labels). Structural exhaustion of currently verifiable new data documented with evidence. No prereg created (no outcomes/threshold-shopping).

## FOCUS CAMPAIGN (EXECUTE IN ORDER, HEAVY WORK REQUIRED)
1. **Gate 4 trigger check:** absent (verified). Do not re-poll. Execute Branch 1 only on valid RESOLVED trigger.
2. **Local + external admissibility:** DONE with evidence (above). Do not redo unchanged probes without a new signal (e.g. ironflow HF `lastModified`/coverage change, or sufficient time for ≥100d HL window).
3. **Mandatory next heavy work — materially different free route (choose highest-value executable):**
   - **(Preferred when eligible)** If HL 2026-11+ has accumulated **≥100 contiguous days** of candles+funding for ≥5 ex-ante symbols **AND** a verifiable observed liquidation-label source covers the same post-2026-10-31 window with provenance/license/completeness per §16: run bounded acquisition probes (evidenced), freeze prereg **BEFORE outcomes**, then build+eval in-session if feasible; emit verdict + atomic state updates. (As of 2026-11-12 only ~10 days available — not yet eligible.)
   - **Monitor/re-probe (bounded, evidence-backed):** Re-check `ironflow/hyperliquid-liquidations` HF metadata/coverage for extension beyond 2026-10-31 and re-probe HL API coverage for the target window. Record evidence artifacts in `research_state/` with UTC timestamp. Do this as a bounded task when new data is plausibly available, not as a polling loop.
   - **Secondary audit (heavy, if feasible):** Full §16 admissibility audit of `metpie/hyperliquid-liquidation-events` (2025-03-22..2025-05-25) joined to HL funding/candles for that exact window — only if venue-consistent, ≥5 symbols, ≥3 non-overlapping 30d blocks, observed-label meaning/completeness acceptable, license/provenance documented, and not conflated with sealed verdicts. If admissible: prereg BEFORE outcomes → build/eval → verdict. If not: document with evidence.
4. **If no admissible path is verifiable in-session:** extend `research_state/new_data_external_probe_audit_*.md/.json` (or new timestamped audit) with concrete probe evidence and keep `program_status=ACTIVE_HEAVY_CAMPAIGN`, `next_unfinished_task=EXTERNAL_NEW_DATA_SOURCE_MONITOR_AND_REPROBE`. Do not write a status-only memo; include probe outputs/URLs/status/schema/counts.
5. **State hygiene:** keep this file the single durable root handoff; keep redirects aligned. Preserve all sealed records/verdicts/manifests exactly as immutable.

## BOTTLENECKS — STATUS & REQUIRED ACTION (2026-11-12T04:35:30Z)
| Bottleneck | Status | Removal/action |
|---|---|---|
| Gate 4 Branch 1 (external/legal Binance terms) | BLOCKED, not agent-removable | Execute Branch 1 only on valid RESOLVED trigger (`status=RESOLVED_VERIFIED`, `fabricated=false`, human/legal attestation). |
| No untested admissible cached-data experiment | EXHAUSTED | Local + external probes done; no new cached claim possible. |
| Post-2026-10-31 HL feature window too short (~10d as of 2026-11-11) | OPEN (time-dependent) | Re-probe when ≥100d accumulated; evidence required. |
| Post-2026-10-31 observed liquidation labels unavailable (ironflow HF ends 2026-10-31) | OPEN (external dependency) | Monitor ironflow HF for extension; search for verifiable alternate observed-label sources. |
| Competing root handoff docs / session ambiguity | REMOVED | This file sole durable root handoff; redirects in place. |
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
- This session audit: `research_state/new_data_external_probe_audit_20261112T043530Z.md`, `.json`
- Prior local audit: `research_state/new_data_admissibility_audit_20261112T042738Z.md`, `.json`
- Handoff/state: `research_state/experiment_frontier.json`, `research_state/hypothesis_registry.json`, `research_state/final_confirmatory_verdict.md`, `research_state/fclr016_local_audit/`
- Protocol: `RESEARCH_PROMPT.md` (§16 admissible new data)
- Sealed results: `research_state/evaluation_summary_TRACKA-HL-expansion-20261111T202344Z.md`, `research_state/evaluation_summary_TRACKA-EXP-ROBUST-20261112T015119Z.md`, `research_state/evaluation_summary_TRACKA-ALT-VOL-20261112T020322Z.md`, `research_state/evaluation_summary_TRACKA-VOL-20261111T234918Z.md`, `research_state/evaluation_summary_TRACKA-VOL-FAMILY-20261112T005111Z.md`

---
**Execute now:** Gate 4 check (absent) → run highest-value materially different free heavy task: bounded evidence-backed probe/reprobe for HL 2026-11+ coverage and ironflow HF label extension (when plausibly available) and/or full §16 audit of `metpie` for a feasible non-sealed design. If any candidate becomes verifiably admissible, freeze prereg + build/eval + verdict + state updates. Otherwise emit timestamped probe/audit evidence and keep `ACTIVE_HEAVY_CAMPAIGN` / `EXTERNAL_NEW_DATA_SOURCE_MONITOR_AND_REPROBE`. No status-only output.
