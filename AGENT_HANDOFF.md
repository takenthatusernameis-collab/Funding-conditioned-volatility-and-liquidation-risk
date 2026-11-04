# AGENT_HANDOFF.md (SINGLE DURABLE HANDOFF)
Timestamp (UTC): 20261104T132758Z
Git SHA (HEAD): a98ec9b0
Branch: main
Repo: Funding-conditioned-volatility-and-liquidation-risk
Handoff ID: FCLR-HANDOFF-20261104T132758Z | Priority: P0 - HEAVY WORK ENFORCED | Mode: CAMPAIGN-DRIVEN

## MANDATORY INITIAL MESSAGE FOR NEXT AGENT (COPY/PASTE)
```text
TASK ID: FCLR-NEXT-056-FUNDING-FIRST-HEAVY
PRIORITY: P0 - HEAVY WORK ENFORCED (REPO-NAME PRIORITIZED)
CAMPAIGN: FUNDING-CONDITIONED VOLATILITY FIRST → LIQUIDATION RISK ON TRIGGER
TIMESTAMP (UTC): 20261104T132758Z
OBJECTIVE: Per repo name "Funding-conditioned-volatility-and-liquidation-risk", PRIORITIZE Track C (funding-conditioned volatility) as the primary campaign. Track C is currently SEALED/NOT_SUPPORTED (FCLR-003: C2 vs B1 +0.015205 QLIKE, CI crosses zero, gate NOT_MET). You MUST do HEAVY re-examination work - do NOT accept "sealed" as terminal without executing ALL 4 mandatory blocks below. Track A remains the only reopen path if NEW admissible unauthenticated liquidation data appears.
CONSTRAINTS: No credentials, no manual files, no .github/workflows changes, no polling loops/schedulers/status-only files, no data fabrication, chronological/leakage-safe, preregister before outcomes if new data appears.
MANDATORY EVERY SESSION (EXECUTE ALL, IN ORDER):
  1) STATE SWEEP (HEAVY): Read RESEARCH_PROMPT.md, AGENT_HANDOFF.md, research_state/*, tests/, scripts/, recent git log. Extract exact blockers, frozen gates, and what "sealed" means. Write findings to research_state/campaign_sweep_$(date -u +%Y%m%dT%H%M%SZ).md (>=150 lines of concrete evidence).
  2) TRACK C DEEP DIVE (HEAVY): Re-audit funding-conditioned volatility from scratch. Mine existing caches (research_state/data_cache, repo root zips/dirs) for unused funding/mark/index/premium features. Test alternative funding normalizations (z-score vs rank vs sign-split vs time-to-funding), lag structures, interaction terms, regime splits. Run smallest verifiable harness against frozen splits. Produce research_state/trackc_deepdive_$(date -u +%Y%m%dT%H%M%SZ).md with ablations + block-bootstrap >=2000 + Holm correction.
  3) TRACK A READINESS (HEAVY): Run scripts/monitor_ironflow_liquidations.py --quick AND scripts/deep_review_alt_sources.py (if exists) or equivalent. Record probe JSON, ETag/tree diffs, and concrete resume condition check. If ANY new files appear (events/fills YYYY-MM.parquet) for >=2026-11 with ironflow or other admissible source, PREREGISTER before inspecting outcomes in research_state/fclr010_prereg_*.json and ONLY THEN run frozen harness.
  4) BOTTLENECK ELIMINATION (HEAVY): Fix any inefficiency blocking progress (missing imports, broken paths, slow scripts). Clean __pycache__/pyc, ensure tests fast/reliable. Add NO new controllers/schedulers. Every action must produce a verifiable artifact.
STOP RULE: Do NOT stop after 1-2 blocks. Complete all 4. If truly stuck, write blocker_evidence with 3+ alternative routes tried and concrete next action.
```

## Current Verified State
- Tests: 164/164 OK (pytest, 16.41s)
- HEAD: a98ec9b0
- Track C: FCLR-003 SEALED/NOT_SUPPORTED (C2 vs B1 +0.015205 QLIKE, CI crosses zero) - BUT repo name prioritizes this; requires deep re-examination, not blind acceptance
- Track A (ironflow Hyperliquid): data_through 2026-10, last probe 2026-11-04T13:21:55Z - tree unchanged (304), no trigger. Resume only on new admissible unauthenticated liquidation data (>=2026-11 events/fills.parquet)
- Track B: CLOSED_NEGATIVE/PERMANENT_BLOCKED
- Bottlenecks: accepting "sealed" without exhaustive alternatives; underutilized caches; need to force heavy work every session

## Priority Order (by repo name)
1. **TRACK C - Funding-conditioned volatility** (HIGHEST - matches repo name). Exhaust all interpretable funding/price features, interactions, regimes. Do not skip just because previous run was negative.
2. **TRACK A - Liquidation risk** (ON TRIGGER). Only if new admissible unauthenticated data appears. Preregister before outcomes.
3. **INFRA/BOTTLENECKS** - Remove anything slowing progress, but only if it enables 1 or 2.

## Bottleneck Removal Plan
- **"Sealed" is not terminal**: Force mandatory deep dive every session until Track C is either re-gated to PASS with evidence, or exhaustively documented as negative with 5+ ablations tried.
- **Cache utilization**: Mine all existing data caches (Binance zips/dirs, ironflow cache, research_state/data_cache) before considering new downloads.
- **Efficient probing**: Use existing `monitor_ironflow_liquidations.py` with ETag caching (304) - no manual polling loops.
- **Heavy work enforcement**: All 4 mandatory blocks must complete. Artifacts required: campaign sweep, trackc deepdive, ironflow probe + alt-source scan evidence, bottleneck fixes.
- **No bloat**: No new schedulers/controllers/status-only files. Fix existing code paths.

## Next Action (EXACT)
1. Execute STATE SWEEP - write campaign_sweep_*.md
2. Execute TRACK C DEEP DIVE - mine caches, try funding normalizations/interactions/regimes, run frozen splits, block-bootstrap>=2000, Holm
3. Execute TRACK A READINESS - probe ironflow + scan alts, record evidence
4. Execute BOTTLENECK ELIMINATION - clean/fix as needed, ensure 164/164 tests still pass
5. Update this handoff with new timestamp, artifacts created, next concrete task
