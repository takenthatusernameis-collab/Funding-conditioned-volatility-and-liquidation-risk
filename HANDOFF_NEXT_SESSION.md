# INITIAL TASK MESSAGE — NEXT AGENTIC WORK SESSION (SINGLE DURABLE HANDOFF)
**Repo:** `Funding-conditioned-volatility-and-liquidation-risk` (priority: funding-conditioned volatility AND liquidation risk — repo-name-prioritized)
**Handoff timestamp (UTC):** 2026-11-12T04:30:17Z (supersedes 2026-11-12T04:27:38Z; this file remains the sole authoritative handoff)
**Status:** AUTHORITATIVE — execute this file only. `AGENT_HANDOFF.md`, `FOCUS_CAMPAIGN.md`, `NEXT_SESSION_TASK.md` are redirects. No competing root handoff files.

## Immediate task (heavy, in-session now)
Do not produce a status-only response. Execute the Focus Campaign below now.

### (A) Gate 4 Branch 1 — FIRST CHECK (deterministic, only if valid trigger exists)
- **Verified this session (2026-11-12T04:30:17Z):** `research_state/fclr016_local_audit/` contains **no** `fclr016_v5_terms_evidence_RESOLVED_*` artifact with `status=RESOLVED_VERIFIED`, `fabricated=false`, and human/legal attestation. Highest local artifact is `fclr016_v5_terms_evidence_UNRESOLVED_20261108T204000Z.json` (`confirmatory_claim_go=NO_GO`, `status=UNRESOLVED`, reviewer_role=pending_human_legal_maintainer). Only `_BLOCKED`/`_UNRESOLVED`/`_partial`/probe artifacts present. **Do not wait/poll.**
- **If a valid RESOLVED trigger appears:** execute deterministic Branch 1 path only — promotion + validators; on all-green run confirmatory Track C multi-split ablation + verdict + required state updates per Gate 4 protocol. Never guess, never set `fabricated=true`, never bypass.
- **If absent (current state):** proceed immediately to (B). Program awaits Gate 4 or new data, but this session must still do heavy work (B).

### (B) REPO-PRIORITY: LOCAL NEW-DATA ADMISSIBILITY INVENTORY COMPLETE — NO LOCALLY-ADMISSIBLE UNTESTED CANDIDATE
The mandatory local new-data admissibility inventory (RESEARCH_PROMPT.md §16) was executed and finalized in prior session (2026-11-12T04:27:38Z). Findings are recorded in:
- `research_state/new_data_admissibility_audit_20261112T042738Z.md` (evidence-backed assessment)
- `research_state/new_data_admissibility_audit_20261112T042738Z.json` (machine summary)

**Conclusion:** **NO locally-admissible untested candidate exists.** All admissible cached-data volatility/liquidation designs on current Hyperliquid/Binance caches are EXHAUSTED/SEALED:
- `hyperliquid_funding/` (23 coins, 2025-11..2026-10): feature-only, window exhausted.
- `hyperliquid_candles/*/` (17 symbols): 2026-05..2026-10 exhausted (all volatility designs NOT_MET); 2025-11..2026-04 INADMISSIBLE (candles empty → RV uncomputable).
- `ironflow_events/*.parquet` (2025-05..2026-10): observed labels only, paired with exhausted candle window.
- `craftify_liq/` (2 months): coverage insufficient, provenance unverified → INADMISSIBLE.
- `data/raw/` + Binance monthly caches: SEALED/INADMISSIBLE (Track A Hyperliquid-only; Binance/2024 conflation forbidden; Track B/C 2024 NOT_SUPPORTED).

Per §(B) step 4: document exhausted-local state + specify the minimal external acquisition needed — **do not fabricate, download unverified data, or guess provenance.** Any network acquisition must follow repo policy and be unauthenticated, bounded, and fully evidenced.

## FOCUS CAMPAIGN (EXECUTE IN ORDER, HEAVY WORK REQUIRED)
1. **Gate 4 trigger check (done/verified):** absent → continue. Do not re-poll.
2. **Local new-data admissibility inventory (DONE prior session):** audit artifacts emitted above. Conclusion: no locally-admissible untested candidate.
3. **Mandatory next heavy work — EXTERNAL NEW-DATA ACQUISITION CAMPAIGN:** Acquire ONE new admissible source/window meeting ALL of RESEARCH_PROMPT.md §16 (see audit artifact § "Minimal external acquisition needed"):
   - unauthenticated/public, provenance + license/terms documented,
   - observed labels where required (no modeled/proxy/synthetic liquidation labels as observed),
   - ≥5 symbols/instruments, ≥3 non-overlapping 30-day test blocks, non-overlapping train/val/test + 7-day embargo,
   - venue-consistent, not conflated with sealed Binance 2024 verdicts,
   - NOT already sealed: e.g. Hyperliquid 2026-11 onward (post-panel) or a genuinely new venue/window.
   Run bounded network probe(s), fully evidenced (endpoint, status, schema sample, coverage, license/terms), saved to `research_state/` with timestamp.
4. **If any externally-admissible candidate is verified:** freeze a preregistration **BEFORE outcomes** (`research_state/track*_prereg_*_<UTC>.json` + `.md`) with hypothesis, exact data/feature/label definitions, splits/embargo/blocks, primary metric/gate, robustness/multiplicity plan, pass/fail criteria; then execute build+eval in-session if feasible and emit verdict + atomic state updates (`experiment_frontier.json`, manifests/registry). No threshold-shopping, no holdout reuse.
5. **If no admissible external source is verifiable:** document structural exhaustion with evidence in this handoff's next update context; name the next materially different free route; keep `program_status=ACTIVE_HEAVY_CAMPAIGN`, `next_unfinished_task=EXTERNAL_NEW_DATA_SOURCE`. Do not write another blocker memo and wait if a valid bounded free-data/diagnostic task exists.
6. **State hygiene (only as justified):** keep this file the single durable root handoff; keep redirects aligned. Preserve all sealed records/verdicts/manifests exactly as immutable.

## BOTTLENECKS — STATUS & REQUIRED ACTION (UPDATED)
| Bottleneck | Status | Removal/action (this session / next session) |
|---|---|---|
| Gate 4 Branch 1 (external/legal Binance terms) | BLOCKED, not agent-removable | Verified absent 2026-11-12T04:30:17Z. **Do not wait.** Execute Branch 1 only on valid RESOLVED trigger with `status=RESOLVED_VERIFIED`, `fabricated=false`, human/legal attestation. |
| No untested admissible cached-data experiment | EXHAUSTED | Inventory complete → audit artifacts emitted. Next: external new-data acquisition campaign (above). |
| Competing root handoff docs / session ambiguity | REMOVED | This file sole durable root handoff; redirects in place. |
| Prior campaign items (volatility family, expansion robustness, alternate volatility) | COMPLETED/SEALED | Do not reopen/retune/relitigate. |
| **No active external data probe in progress** | **NEW — MUST START NOW** | **This session MUST run bounded probe(s) of candidate new sources per RESEARCH_PROMPT.md §16. Probe results → evidence artifacts → prereg if admissible, else document exhaustion + next route.** |

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
- **No status-only output.** Every session must deliver: Gate 4 Branch 1 execution if triggered, OR prereg + (build+eval or documented infeasibility with evidence) + state updates, OR a concrete timestamped new-data admissibility audit (+ prereg/external-spec as applicable).
- **No new experiments on exhausted cached data.** Any new claim requires NEW admissible data/source with provenance/license/coverage per RESEARCH_PROMPT.md §16.

## KEY REFERENCES
- Handoff/state: `research_state/experiment_frontier.json`, `research_state/hypothesis_registry.json`, `research_state/run_manifest.json`, `research_state/final_confirmatory_verdict.md`, `research_state/fclr016_local_audit/`
- Protocol: `RESEARCH_PROMPT.md` (esp. §16 admissible new data)
- Caches: `research_state/data_cache/hyperliquid_candles/`, `research_state/data_cache/hyperliquid_funding/`, `research_state/data_cache/ironflow_events/`, `data/`, `data/raw/`
- Sealed results: `research_state/evaluation_summary_TRACKA-HL-expansion-20261111T202344Z.md`, `research_state/evaluation_summary_TRACKA-EXP-ROBUST-20261112T015119Z.md`, `research_state/evaluation_summary_TRACKA-ALT-VOL-20261112T020322Z.md`, `research_state/evaluation_summary_TRACKA-VOL-20261111T234918Z.md`, `research_state/evaluation_summary_TRACKA-VOL-FAMILY-20261112T005111Z.md`
- This session's audit baseline: `research_state/new_data_admissibility_audit_20261112T042738Z.md` + `.json`

---
**Execute Gate 4 check (verified absent) → external new-data acquisition campaign NOW. Run bounded probe(s) of candidate new source(s) per RESEARCH_PROMPT.md §16. If candidate verified: freeze prereg + build/eval + verdict + state updates. If none verifiable: document structural exhaustion + next materially different free route. No status-only output. No waiting.**