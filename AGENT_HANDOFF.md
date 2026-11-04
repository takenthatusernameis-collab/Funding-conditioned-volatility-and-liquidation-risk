# AGENT_HANDOFF.md (SINGLE DURABLE HANDOFF)
Timestamp (UTC): 20261104T133107Z
Git SHA (HEAD): f128b157
Branch: main
Repo: Funding-conditioned-volatility-and-liquidation-risk
Handoff ID: FCLR-HANDOFF-20261104T133107Z | Priority: P0 - HEAVY WORK ENFORCED | Mode: CAMPAIGN-DRIVEN

## STATE CONTRADICTION RESOLVED (read first)
AGENT_HANDOFF previously claimed Track C "NOT_SUPPORTED" citing only FCLR-003 (sealed 2024, C2 vs B1 +0.015205 QLIKE, CI crosses zero). That claim is STALE and superseded by run_manifest.json / evaluation_summary_FCLR-011_20261103T111743Z.md:
- **FCLR-011 (Track C, funding-conditioned volatility): COMPLETE, FORECAST_GATE_PASSED.** C2 vs B1 mean diff -0.016458 QLIKE, 95% CI [-0.032546, -0.001418] EXCLUDES ZERO, relative reduction 4.94% (>=2% floor met), 5 instruments, test window 2026-05-08..2026-08-06 = 91 days = 3 non-overlapping 30-day blocks. Splits frozen before outcomes (pre_registration_fclr011_20261103T111501Z.md). Forecast gate PASSED (all criteria).
- **FCLR-012-V (Track C forward replication): INCONCLUSIVE.** Binance archive genuinely ends 2026-11-02 (live probe 2026-11-04T00:45Z -> 404 for 2026-11-03/04 and 2026-10-28/29). Test window 2026-10-29..2026-11-02 = 5 days = 0 non-overlapping 30-day blocks, CI spans zero. No new admissible Binance data exists. Blocked on data, NOT on methodology.
- **Track A (FCLR-010): COMPLETE_SEALED, FORECAST_GATE_PASSED** (Brier rel reduction 2.21%, CI excludes zero, 199 instruments, 5 blocks). Blocked on new ironflow parquet >=2026-11 (data_through 2026-10).
- **Track B (modeled boundary breach): NOT_SUPPORTED.**
- Tests: 164/164 pass (pytest, ~18s). HEAD f128b157.

Per repo name "Funding-conditioned-volatility-and-liquidation-risk", Track C remains the highest-priority campaign. The confirmatory gate PASSED on FCLR-011; forward confirmation is blocked on new data. Available heavy work NOW: deeper funding-conditioned validation on frozen splits (regime-stratified QLIKE, funding-quartile interactions, mechanism ablations) without touching sealed outcomes.

## MANDATORY INITIAL MESSAGE FOR NEXT AGENT (COPY/PASTE)
```text
TASK ID: FCLR-NEXT-057-FUNDING-CONDITIONED-DEEPER-VALIDATION
PRIORITY: P0 - HEAVY WORK ENFORCED (REPO-NAME PRIORITIZED = TRACK C)
CAMPAIGN: FUNDING-CONDITIONED VOLATILITY DEEPER VALIDATION (FROZEN SPLITS) -> FORWARD READINESS
TIMESTAMP (UTC): 20261104T133107Z
OBJECTIVE: Track C gate PASSED on FCLR-011 (C2 vs B1 -4.94% rel QLIKE, CI excludes zero, 5 instruments, 3 blocks). Forward replication FCLR-012-V is INCONCLUSIVE, blocked on data (Binance archive ends 2026-11-02; ironflow ends 2026-10). Execute deeper funding-conditioned validation on FROZEN FCLR-011/FCLR-002 splits only: regime-stratified QLIKE by funding quartiles per symbol/time, funding x RV interaction refinements, mark/index premium and mark/EMA24 sensitivity ablations. Produce research_state/fclr011_deeper_validation_$(date -u +%Y%m%dT%H%M%SZ).md with ablations + block-bootstrap >=2000 + Holm correction. Do NOT re-run sealed FCLR-001/002/003/006/007/008/010/011. Do NOT threshold-shop. Do NOT merge Binance and Hyperliquid. Track C overlay remains HYPOTHETICAL_ONLY (gate pass does not authorize overlay changes).
CONSTRAINTS: No credentials, no manual files, no .github/workflows changes, no polling loops/schedulers/status-only files, no data fabrication, chronological/leakage-safe, preregister before outcomes if new data appears.
MANDATORY EVERY SESSION (EXECUTE ALL, IN ORDER):
  1) STATE SWEEP (HEAVY): Read RESEARCH_PROMPT.md, AGENT_HANDOFF.md, research_state/*, tests/, scripts/, recent git log. Extract exact blockers, frozen gates, and what "sealed" means. Reconcile AGENT_HANDOFF.md vs run_manifest.json contradictions. Write findings to research_state/campaign_sweep_$(date -u +%Y%m%dT%H%M%SZ).md (>=150 lines of concrete evidence).
  2) TRACK C DEEPER VALIDATION (HEAVY): On frozen FCLR-011/FCLR-002 splits only, run regime-stratified QLIKE by funding quartiles per symbol/time, funding x RV interaction terms, mark/index premium and mark/EMA24 sensitivity ablations. Block-bootstrap >=2000 deterministic replicates, Holm correction. Produce research_state/trackc_deeper_validation_$(date -u +%Y%m%dT%H%M%SZ).md with ablations. Every ablation must report CI and Holm-adjusted result.
  3) TRACK A READINESS (HEAVY): Run scripts/monitor_ironflow_liquidations.py --quick AND scripts/deep_review_alt_sources.py (if exists) or equivalent. Record probe JSON, ETag/tree diffs, concrete resume condition check. If ANY new files appear (events/fills YYYY-MM.parquet) for >=2026-11 with ironflow or other admissible source, PREREGISTER before inspecting outcomes in research_state/fclr010_prereg_*.json and ONLY THEN run frozen harness.
  4) BOTTLENECK ELIMINATION (HEAVY): Fix any inefficiency blocking progress (missing imports, broken paths, slow scripts). Clean __pycache__/pyc, ensure tests fast/reliable (164/164 must stay green). Add NO new controllers/schedulers. Every action must produce a verifiable artifact.
STOP RULE: Do NOT stop after 1-2 blocks. Complete all 4. If truly stuck, write blocker_evidence with 3+ alternative routes tried and concrete next action.
```

## Current Verified State
- Tests: 164/164 OK (pytest, ~18s)
- HEAD: f128b157 (branch main, up to date with origin/main)
- Track C FCLR-H001: FCLR-011 FORECAST_GATE_PASSED (C2 vs B1 -4.94% rel QLIKE, CI [-0.032546,-0.001418] excl zero, 5 instruments, 3 blocks, test 2026-05-08..2026-08-06). FCLR-012-V forward INCONCLUSIVE (data blocked: Binance ends 2026-11-02, 0 test blocks).
- Track A FCLR-H004: FCLR-010 COMPLETE_SEALED FORECAST_GATE_PASSED (Brier -2.21% rel, CI excl zero, 199 instruments, 5 blocks). Blocked on new ironflow parquet >=2026-11 (last probe 2026-11-04T13:21:55Z, tree unchanged 304).
- Track B: NOT_SUPPORTED.
- Bottlenecks: stale AGENT_HANDOFF claiming Track C NOT_SUPPORTED (superseded by FCLR-011 PASS); forward data blocked (no new Binance/ironflow data); must not let "sealed" on FCLR-003 block the FCLR-011 pass or deeper validation.

## Priority Order (by repo name)
1. **TRACK C - Funding-conditioned volatility** (HIGHEST - matches repo name). Gate PASSED on FCLR-011; execute deeper validation on frozen splits (regime-stratified QLIKE, funding-quartile interactions, ablations). Forward confirmation blocked on new data.
2. **TRACK A - Liquidation risk** (ON TRIGGER). Only if new admissible unauthenticated liquidation data (>=2026-11 events/fills.parquet) appears. Preregister before outcomes.
3. **INFRA/BOTTLENECKS** - Remove anything slowing progress, but only if it enables 1 or 2. Keep 164/164 green.

## Bottleneck Removal Plan
- **Stale handoff fixed**: AGENT_HANDOFF.md now reflects FCLR-011 PASS; FCLR-003 NOT_SUPPORTED no longer misrepresents Track C. Future agents must not treat Track C as closed-negative.
- **Forward data blocked**: Binance archive ends 2026-11-02; ironflow ends 2026-10. Do NOT fabricate, do NOT relax thresholds, do NOT re-run sealed panels. Deeper validation on frozen splits is the available heavy work; wait for new admissible data for forward.
- **Cache utilization**: Mine existing caches (Binance zips/dirs, research_state/data_cache) before considering new downloads.
- **Efficient probing**: monitor_ironflow_liquidations.py with ETag caching (304) - no manual polling loops.
- **Heavy work enforcement**: All 4 mandatory blocks must complete. Artifacts required: campaign sweep, trackc deeper validation, ironflow probe + alt-source scan evidence, bottleneck fixes.
- **No bloat**: No new schedulers/controllers/status-only files. Fix existing code paths.

## Next Action (EXACT)
1. Execute STATE SWEEP - write campaign_sweep_*.md (>=150 lines, reconcile AGENT_HANDOFF vs run_manifest contradiction)
2. Execute TRACK C DEEPER VALIDATION - regime-stratified QLIKE by funding quartiles, funding x RV interactions, mark/index + EMA24 ablations on frozen FCLR-011/FCLR-002 splits; block-bootstrap>=2000, Holm
3. Execute TRACK A READINESS - probe ironflow + scan alts, record evidence
4. Execute BOTTLENECK ELIMINATION - clean/fix as needed, ensure 164/164 tests still pass
5. Update this handoff with new timestamp, artifacts created, next concrete task

## Verification commands
- `python -m pytest tests/ -q` (expect 164 passed)
- `python scripts/monitor_ironflow_liquidations.py --quick` (Track A probe, expect 304/no new data)
- `git status` (working tree clean except pyc caches)
