# INITIAL TASK MESSAGE — NEXT AGENTIC WORK SESSION (SINGLE DURABLE HANDOFF)
**Repo:** `Funding-conditioned-volatility-and-liquidation-risk` (priority: funding-conditioned volatility AND liquidation risk — repo-name-prioritized)
**Handoff timestamp (UTC):** 2026-11-12T02:07:25Z (supersedes 2026-11-12T01:42:43Z; this file remains the sole authoritative handoff)
**Status:** AUTHORITATIVE — execute this file only. `AGENT_HANDOFF.md`, `FOCUS_CAMPAIGN.md`, `NEXT_SESSION_TASK.md` are redirects. No competing root handoff files.

## Immediate task (heavy, in-session now)
Do not produce a status-only response. Execute the Focus Campaign below now.

### (A) REPO-PRIORITY: ALL CACHED-DATA VOLATILITY DESIGNS EXHAUSTED — AWAIT GATE 4 OR NEW DATA
The robustness/falsification campaign for sealed Track A liquidation expansion PASS (`TRACKA-HL-EXPANSION-20261111T195500Z`) completed **FRAGILE** (`TRACKA-EXP-ROBUST-20261112T015119Z`): LOIO FAIL (4/8 pass, need ≥6), Placebo/Permutation FAIL (true rel 19.04% ≤ 95th pctl 21.10%), Bootstrap Settings PASS (3/3). State updated; sealed PASS preserved.

Per protocol fallback, preregistered and executed alternate volatility design `TRACKA-ALT-VOL-20261112T015546Z` on cached HL 2026-05..2026-10 panel: 6h horizon, C2_ALT (adds rv72h), 5 test blocks. Verdict: **NOT_MET** (`TRACKA-ALT-VOL-20261112T020322Z`) — materiality PASSED (5.77% ≥ 2%) but CI crosses zero.

**All admissible cached-data volatility designs on Hyperliquid 2026-05..2026-10 are now EXHAUSTED:**
- Primary 24h (TRACKA-VOL-20261111T234918Z): NOT_MET (-1.37%, CI crosses zero)
- Family multiplicity 6h/24h/72h/168h (TRACKA-VOL-FAMILY-20261112T005111Z): NOT_MET (Holm, no horizon passes)
- Alternate 6h + rv72h (TRACKA-ALT-VOL-20261112T020322Z): NOT_MET (materiality PASS, CI FAIL)

### (B) Gate 4 Branch 1 (ONLY if valid trigger appears)
If `research_state/fclr016_local_audit/fclr016_v5_terms_evidence_RESOLVED_<UTC>.json` exists with `status=RESOLVED_VERIFIED`, `fabricated=false`, and human/legal attestation → deterministic promotion+validators → on all-green confirmatory Track C multi-split ablation + verdict + state updates. **Verified absent; do not wait/poll.**

## BOTTLENECK CHECK (THIS SESSION)
- **Gate 4 Branch 1 trigger:** NOT PRESENT — `research_state/fclr016_local_audit/` contains no `fclr016_v5_terms_evidence_RESOLVED_*` with required RESOLVED_VERIFIED/legal attestation/fabricated=false; only `_BLOCKED`/`_UNRESOLVED`/`_partial`/probe artifacts exist. **Do not wait/poll; program awaits Gate 4 or new data.** Never guess, never set `fabricated=true`, never bypass.
- **Stale/competing handoff surfaces:** REMOVED — root `AGENT_HANDOFF.md`, `FOCUS_CAMPAIGN.md`, `NEXT_SESSION_TASK.md` redirect to this file. Single durable handoff only.
- **Volatility multiplicity family:** COMPLETED NOT_MET — `research_state/evaluation_summary_TRACKA-VOL-FAMILY-20261112T005111Z.md` (12 comparisons, Holm correction, no horizon passes primary gate). Immutable.
- **Liquidation expansion PASS:** SEALED — `TRACKA-HL-EXPANSION-20261111T195500Z` PASS (C2 vs B1 rel QLIKE -19.04%, 95% CI [-5.088,-0.478], n=593, 8 instruments, 3 blocks, 2026-05..2026-10). Immutable, do not relitigate.
- **Liquidation expansion robustness:** FRAGILE — `TRACKA-EXP-ROBUST-20261112T015119Z` (LOIO FAIL, Placebo/Permutation FAIL, Bootstrap PASS). Immutable, documented with exact failure modes.
- **Alternate volatility design:** NOT_MET — `TRACKA-ALT-VOL-20261112T020322Z` (materiality PASS 5.77%, CI crosses zero). Immutable.
- **Volatility primary 24h:** NOT_MET — `TRACKA-VOL-20261111T234918Z` (C2 vs B1 rel QLIKE -1.37%, CI crosses zero, n=19233, 9 instruments, 3 blocks). Immutable.
- **All other Track A/B/C contexts:** SEALED/CLOSED negative (NOT_MET, NOT_SUPPORTED, INADMISSIBLE). Immutable.

## FOCUS CAMPAIGN (REPO-NAME-PRIORITIZED)
**Objective (inferred from repo name + protocol):** No further claim-worthy experiments can be executed on current cached admissible data. All Track A volatility designs exhausted. Track A liquidation expansion PASS is sealed but FRAGILE on robustness. Gate 4 Branch 1 remains EXTERNAL_BLOCKED. **Next session must either:** (1) detect valid Gate 4 Branch 1 trigger and execute deterministic Branch 1 path, OR (2) await/acquire new admissible data source per RESEARCH_PROMPT.md §16 (unauthenticated, provenance/license, ≥5 symbols, ≥3 non-overlapping 30-day blocks) and pre-register new claim BEFORE outcomes.

**Execute in this exact order:**
1. **Check Gate 4 trigger:** Verify `research_state/fclr016_local_audit/fclr016_v5_terms_evidence_RESOLVED_<UTC>.json` exists with ALL required fields (`status=RESOLVED_VERIFIED`, `fabricated=false`, human/legal attestation). If present → execute Branch 1 deterministically (Track C multi-split ablation + verdict + state updates). If absent → proceed to step 2.
2. **No status-only output.** Document current exhausted state in handoff; do not fabricate new experiments on exhausted cached data. Any new experiment requires NEW admissible data source with provenance.
3. **Preserve all sealed/closed records.** Never mutate `TRACKA-HL-EXPANSION-20261111T195500Z`, `TRACKA-EXP-ROBUST-20261112T015119Z`, `TRACKA-VOL-FAMILY-20261112T005111Z`, `TRACKA-ALT-VOL-20261112T020322Z`, FCLR-003, Track B/C verdicts.

## BOTTLENECKS — STATUS & REMOVAL
| Bottleneck | Status | Removal/action |
|---|---|---|
| Gate 4 Branch 1 (external/legal Binance terms) | BLOCKED, not agent-removable | **Do not wait.** Run Branch 1 ONLY if valid `fclr016_v5_terms_evidence_RESOLVED_<UTC>.json` exists with all required fields, `fabricated=false`, `status=RESOLVED_VERIFIED`, and human/legal attestation → deterministic promotion+validators → on all-green confirmatory Track C multi-split ablation + verdict + state. Verified absent now. |
| Volatility multiplicity family incomplete | **REMOVED** | Completed: `research_state/evaluation_summary_TRACKA-VOL-FAMILY-20261112T005111Z.md` (NOT_MET). |
| Liquidation expansion robustness | **COMPLETED FRAGILE** | `TRACKA-EXP-ROBUST-20261112T015119Z` (LOIO FAIL, Placebo FAIL, Bootstrap PASS). Documented exact failure modes; sealed PASS preserved. |
| Alternate volatility design | **COMPLETED NOT_MET** | `TRACKA-ALT-VOL-20261112T020322Z` (materiality PASS, CI FAIL). All cached-data volatility designs exhausted. |
| No further claim-worthy cached-data experiments | **EXHAUSTED** | No admissible cached-data volatility/liquidation designs remain. Requires Gate 4 trigger OR new admissible data source (per RESEARCH_PROMPT.md §16). |
| Competing root handoff docs / session ambiguity | REMOVED | This file is sole durable root handoff; redirect files in place. |

## COMPLETED / SEALED — DO NOT REOPEN, RETUNE, OR RELITIGATE
- Track A liquidation expansion `TRACKA-HL-EXPANSION-20261111T195500Z` = **PASS** (C2 vs B1 rel QLIKE -19.04%, 95% CI [-5.088,-0.478], n=593, 8 instruments, 3 blocks, 2026-05..2026-10). Sealed.
- Track A liquidation expansion robustness `TRACKA-EXP-ROBUST-20261112T015119Z` = **FRAGILE** (LOIO: 4/8 FAIL, Placebo: p≈0.07 FAIL, Bootstrap: 3/3 PASS). Sealed.
- Track A alternate volatility `TRACKA-ALT-VOL-20261112T020322Z` = **NOT_MET** (6h horizon, C2_ALT+rv72h, rel 5.77%, CI crosses zero, 5 test blocks). Sealed.
- Track A volatility primary 24h `TRACKA-VOL-20261111T234918Z` = **NOT_MET** (C2 vs B1 rel QLIKE -1.37%, CI crosses zero, n=19233, 9 instruments, 3 blocks). Sealed.
- Track A volatility family `TRACKA-VOL-FAMILY-20261112T005111Z` = **NOT_MET** (Holm across 12 comparisons; no horizon passes primary gate). Sealed.
- Track A 9-symbol 2026-05..2026-10 liquidation = **NOT_MET** (closed). Track A early 2025-11..2026-04 = **INADMISSIBLE** (closed).
- Track B/C 2024 and H1/FCLR-002/003 contexts sealed/closed negative; H1 primary NOT_SUPPORTED on tested panels. Immutable.
- 2024 Binance confirmatory FCLR-003 = **NOT_SUPPORTED** (final_confirmatory_verdict.md executive verdict). Immutable.

## HARD BANS (BINDING)
- No outcome inspection before prereg freeze. No threshold-shopping. No sealed-holdout reuse.
- No Binance/2024 conflation; Hyperliquid-only venue for cached-data campaigns with matching artifacts.
- No modeled/proxy/synthetic liquidation labels as observed.
- No `.github/workflows` edits. No redundant network polling. No agent-set `RESOLVED_VERIFIED`/`fabricated=true`; no Gate 4 bypass.
- **No status-only output.** Every session must deliver prereg + (build+eval or documented infeasibility+next-attempt) + state updates, OR detect valid Gate 4 trigger and execute Branch 1, OR document exhausted state and await new data.
- **No new experiments on exhausted cached data.** Any new claim requires NEW admissible data source with provenance/license/coverage per RESEARCH_PROMPT.md §16.

## KEY REFERENCES
- Handoff/state: `research_state/experiment_frontier.json`, `research_state/hypothesis_registry.json`, `research_state/run_manifest.json`, `research_state/final_confirmatory_verdict.md`, `research_state/fclr016_local_audit/`
- Caches: `research_state/data_cache/hyperliquid_candles/` (9 coins, 2026-05..2026-10), `research_state/data_cache/hyperliquid_funding/` (9 coins, ~2025-11..2026-10), `research_state/data_cache/ironflow_events/` (2025-05..2026-10, 432 markets)
- Liquidation expansion panel: `research_state/tracka_hl_expansion_panel_20261111T202344Z.parquet`, `research_state/tracka_hl_expansion_panel_build_report_20261111T202344Z.json`
- Liquidation expansion robustness: `research_state/tracka_prereg_expansion_robust_20261112T014515Z.json`, `research_state/evaluation_summary_TRACKA-EXP-ROBUST-20261112T015119Z.md`
- Alternate volatility: `research_state/tracka_prereg_alt_volatility_20261112T015546Z.json`, `research_state/evaluation_summary_TRACKA-ALT-VOL-20261112T020322Z.md`
- Volatility panel: `research_state/tracka_vol_panel_20261111T234918Z.parquet`, `research_state/tracka_vol_panel_build_report_20261111T234918Z.json`
- Evaluation scripts: `scripts/run_expansion_robustness.py`, `scripts/run_alt_volatility.py`, `scripts/tracka_hl_evaluate_successor.py`, `src/volatility/eval.py`, `src/volatility/block_bootstrap.py`, `src/volatility/features_ext.py`

---

**Execute Gate 4 check first. If trigger absent: document exhausted state and await new admissible data source. No status-only output.**

(End of file - total lines)