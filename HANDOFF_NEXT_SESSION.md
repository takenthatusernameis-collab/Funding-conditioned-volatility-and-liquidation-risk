# INITIAL TASK MESSAGE — NEXT AGENTIC WORK SESSION (SINGLE DURABLE HANDOFF)
**Repo:** `Funding-conditioned-volatility-and-liquidation-risk` (priority: funding-conditioned volatility AND liquidation risk — repo-name-prioritized)
**Handoff timestamp (UTC):** 2026-11-12T04:26:20Z (supersedes 2026-11-12T02:07:25Z; this file remains the sole authoritative handoff)
**Status:** AUTHORITATIVE — execute this file only. `AGENT_HANDOFF.md`, `FOCUS_CAMPAIGN.md`, `NEXT_SESSION_TASK.md` are redirects. No competing root handoff files.

## Immediate task (heavy, in-session now)
Do not produce a status-only response. Execute the Focus Campaign below now.

### (A) Gate 4 Branch 1 — FIRST CHECK (deterministic, only if valid trigger exists)
- **Verified this session (2026-11-12T04:26:20Z):** `research_state/fclr016_local_audit/` contains **no** `fclr016_v5_terms_evidence_RESOLVED_*` artifact with `status=RESOLVED_VERIFIED`, `fabricated=false`, and human/legal attestation. Only `_BLOCKED`/`_UNRESOLVED`/`_partial`/probe artifacts present. **Do not wait/poll.**
- **If a valid RESOLVED trigger appears:** execute deterministic Branch 1 path only — promotion + validators; on all-green run confirmatory Track C multi-split ablation + verdict + required state updates per Gate 4 protocol. Never guess, never set `fabricated=true`, never bypass.
- **If absent (current state):** proceed immediately to (B). Program awaits Gate 4 or new data, but this session must still do heavy work (B).

### (B) REPO-PRIORITY: ALL CACHED-DATA CLAIMS EXHAUSTED — NEW ADMISSIBLE DATA CAMPAIGN (MANDATORY)
All admissible cached-data volatility/liquidation designs on current Hyperliquid/Binance caches are **EXHAUSTED/SEALED** (see “Sealed — do not reopen”). No new claim-worthy experiment may be run on exhausted cached data. The next repo-priority work is to **find and qualify a NEW admissible data source/window** (or prove none exists locally) per `RESEARCH_PROMPT.md` §16 and move it to a frozen preregistration.

**New admissible data (hard requirements):** unauthenticated/public, provenance + license/terms documented, sufficient for the claim (observed labels where required; no modeled/proxy/synthetic liquidation labels as observed), coverage meeting design minimums (typically ≥5 symbols/instruments and ≥3 non-overlapping 30-day test blocks, with non-overlapping train/val/test and embargo as applicable), venue-consistent with artifacts, and not conflated with sealed Binance 2024 verdicts.

## FOCUS CAMPAIGN (EXECUTE IN ORDER, HEAVY WORK REQUIRED)
1. **Gate 4 trigger check (done/verified):** absent → continue. Do not re-poll.
2. **Local new-data admissibility inventory (concrete, this session):**
   - Inventory potential untested sources in-repo: `data/raw/`, `data/`, `research_state/data_cache/` (including non-HL/Binance-month dirs such as `hyperliquid_candles`, `hyperliquid_funding`, `ironflow_events`, `craftify_liq`, any BTCUSDT subdirs, manifests), and any scripts under `scripts/`/`src/` that define admissible acquisition/build paths.
   - For each candidate, produce an evidence-backed assessment against §16: venue, symbols, time coverage, continuity/gaps, label type (observed vs proxy), provenance/license evidence available locally, and whether it enables an **untested** funding-conditioned volatility or liquidation-risk claim not already sealed.
   - Write findings to a timestamped artifact: `research_state/new_data_admissibility_audit_<UTC>.md` (+ `.json` summary) listing `ADMISSIBLE_CANDIDATE` / `INADMISSIBLE` / `NEEDS_EXTERNAL_PROVENANCE` with reasons.
3. **If any locally-admissible untested candidate exists:** freeze a preregistration **BEFORE outcomes** (`research_state/track*_prereg_*_<UTC>.json` + `.md`) with hypothesis, exact data/feature/label definitions, splits/embargo/blocks, primary metric/gate, robustness/multiplicity plan, and pass/fail criteria; then execute build+eval in-session if feasible and emit verdict + atomic state updates (`experiment_frontier.json`, manifests/registry as applicable). No threshold-shopping, no holdout reuse.
4. **If no locally-admissible candidate exists (likely, given exhausted caches):** document exhausted-local state in the audit artifacts and in this handoff’s next update context; specify the minimal external acquisition needed (exact venue/product, symbols, date range, fields, license/provenance proof required) to unblock a new claim — but **do not fabricate, download unverified data, or guess provenance**. Any network acquisition must follow repo policy and be unauthenticated, bounded, and fully evidenced.
5. **State hygiene (only as justified):** keep this file the single durable root handoff; keep redirects aligned. Preserve all sealed records/verdicts/manifests exactly as immutable.

## BOTTLENECKS — STATUS & REQUIRED ACTION
| Bottleneck | Status | Removal/action (this session) |
|---|---|---|
| Gate 4 Branch 1 (external/legal Binance terms) | BLOCKED, not agent-removable | Verified absent 2026-11-12T04:26:20Z. **Do not wait.** Execute Branch 1 only on valid RESOLVED trigger with `status=RESOLVED_VERIFIED`, `fabricated=false`, human/legal attestation. |
| No untested admissible cached-data experiment remains | **EXHAUSTED** | Mandatory local new-data admissibility inventory + timestamped audit artifacts (§16). Prereg+run if candidate found; else evidence-backed exhaustion/external-spec. |
| Competing root handoff docs / session ambiguity | REMOVED | This file sole durable root handoff; redirects in place. |
| Prior campaign items (volatility family, expansion robustness, alternate volatility) | COMPLETED/SEALED | Do not reopen/retune/relitigate. |

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

---
**Execute Gate 4 check (verified absent) → run local new-data admissibility inventory and emit `research_state/new_data_admissibility_audit_<UTC>.md/.json` now. If candidate found: freeze prereg and run. No status-only output.**
