# AGENT_HANDOFF.md (SINGLE DURABLE HANDOFF)
Timestamp (UTC): 20261104T133800Z
Git SHA (HEAD): f128b157
Branch: main
Repo: Funding-conditioned-volatility-and-liquidation-risk
Handoff ID: FCLR-HANDOFF-20261104T133800Z | Priority: P0 - HEAVY WORK ENFORCED | Mode: CAMPAIGN-DRIVEN | Enforcement: NO-SKIP

## STATE CONTRADICTION RESOLVED (read first)
AGENT_HANDOFF previously claimed Track C "NOT_SUPPORTED" citing only FCLR-003 (sealed). This is STALE and superseded by `run_manifest.json` and `evaluation_summary_FCLR-011_20261103T111743Z.md`:

- **FCLR-011 (Track C, funding-conditioned volatility): COMPLETE, FORECAST_GATE_PASSED.** C2 vs B1 mean diff -0.016458 QLIKE, 95% CI [-0.032546, -0.001418] EXCLUDES ZERO, relative reduction 4.94% (>= 2% floor met), 5 instruments, test window 2026-05-08..2026-08-06 = 91 days = 3 non-overlapping 30-day blocks. Splits frozen before outcomes (`pre_registration_fclr011_20261103T111501Z.md`). Forecast gate PASSED.
- **FCLR-012-V (Track C forward replication): INCONCLUSIVE.** Binance archive ends 2026-11-02 (live probe 2026-11-04T00:45Z -> 404 for 2026-11-03/04 and 2026-10-28/29). Test window 2026-10-29..2026-11-02 = 5 days = 0 non-overlapping 30-day blocks, CI spans zero. No new admissible Binance data exists. Blocked on data, NOT on methodology.
- **Track A (FCLR-010): COMPLETE_SEALED, FORECAST_GATE_PASSED** (Brier rel reduction 2.21%, CI excludes zero, 199 instruments, 5 blocks). Blocked on new ironflow parquet >= 2026-11 (data_through 2026-10).
- **Track B (modeled boundary breach): NOT_SUPPORTED.**
- Tests: 164/164 pass (pytest, ~18s). HEAD f128b157.

Per repo name `Funding-conditioned-volatility-and-liquidation-risk`, Track C is the highest-priority campaign. The confirmatory gate PASSED on FCLR-011; forward confirmation is blocked on new data. Available heavy work NOW: deeper funding-conditioned validation on FROZEN splits without touching sealed outcomes.

## MANDATORY INITIAL MESSAGE FOR NEXT AGENT (COPY/PASTE - DO NOT EDIT)
```text
TASK ID: FCLR-NEXT-058-FUNDING-CONDITIONED-DEEPER-VALIDATION
PRIORITY: P0 - HEAVY WORK ENFORCED (REPO-NAME PRIORITIZED = TRACK C)
CAMPAIGN: FUNDING-CONDITIONED VOLATILITY DEEPER VALIDATION (FROZEN SPLITS) -> FORWARD READINESS
TIMESTAMP (UTC): 20261104T133800Z
OBJECTIVE: Track C gate PASSED on FCLR-011 (C2 vs B1 -4.94% rel QLIKE, CI [-0.032546,-0.001418] excl zero, 5 instruments, 3 blocks). Forward replication FCLR-012-V is INCONCLUSIVE, blocked on data (Binance archive ends 2026-11-02; ironflow ends 2026-10). Execute deeper funding-conditioned validation on FROZEN FCLR-011/FCLR-002 splits ONLY. Produce regime-stratified QLIKE by funding quartiles per symbol/time, funding x RV interaction refinements, mark/index premium and mark/EMA24 sensitivity ablations. Output research_state/fclr011_deeper_validation_$(date -u +%Y%m%dT%H%M%SZ).md with ablations + block-bootstrap >=2000 (deterministic) + Holm correction. Do NOT re-run sealed FCLR-001/002/003/006/007/008/010/011. Do NOT threshold-shop. Do NOT merge Binance and Hyperliquid. Track C overlay remains HYPOTHETICAL_ONLY (gate pass does not authorize overlay changes).
CONSTRAINTS: No credentials, no manual files, no .github/workflows changes, no polling loops/schedulers/status-only files, no data fabrication, chronological/leakage-safe, preregister before outcomes if new data appears.
MANDATORY EVERY SESSION (EXECUTE ALL, IN ORDER - NO SKIPPING):
  1) STATE SWEEP (HEAVY): Read RESEARCH_PROMPT.md, AGENT_HANDOFF.md, run_manifest.json, research_state/*, tests/, scripts/, recent git log. Extract exact blockers, frozen gates, sealed sets, and "sealed" definition. Reconcile AGENT_HANDOFF.md vs run_manifest.json contradictions explicitly. Write findings to research_state/campaign_sweep_$(date -u +%Y%m%dT%H%M%SZ).md (>=150 lines of concrete evidence with file paths/lines).
  2) TRACK C DEEPER VALIDATION (HEAVY): On frozen FCLR-011/FCLR-002 splits only, run regime-stratified QLIKE by funding quartiles per symbol/time, funding x RV interaction terms, mark/index premium and mark/EMA24 sensitivity ablations. Block-bootstrap >=2000 deterministic replicates, Holm correction. Produce research_state/trackc_deeper_validation_$(date -u +%Y%m%dT%H%M%SZ).md with ablations table (base/C2, each ablation, delta QLIKE, 95% CI, p/Holm, blocks). Every ablation must report CI and Holm-adjusted result.
  3) TRACK A READINESS (HEAVY): Run scripts/monitor_ironflow_liquidations.py --quick AND scripts/deep_review_alt_sources.py (if exists) or equivalent admissible-source scan. Record probe JSON/ETag/tree diffs. Define concrete resume condition (e.g. new ironflow YYYY-MM.parquet >=2026-11 or other admissible unauthenticated source with events/fills). If ANY new files appear for >=2026-11 with ironflow or other admissible source, PREREGISTER before inspecting outcomes in research_state/fclr010_prereg_$(date -u +%Y%m%dT%H%M%SZ).json and ONLY THEN run frozen harness.
  4) BOTTLENECK ELIMINATION (HEAVY): Fix any inefficiency blocking progress (missing imports, broken paths, slow scripts, cache misses). Clean __pycache__/pyc. Ensure tests remain fast/reliable (164/164 must stay green). Add NO new controllers/schedulers/status-only files. Every action must produce a verifiable artifact (diffs, before/after timings, or test outputs).
STOP RULE: Do NOT stop after 1-2 blocks. Complete all 4. If truly stuck, write blocker_evidence_$(date -u +%Y%m%dT%H%M%SZ).md with >=3 alternative routes tried, concrete files/commands, and a single concrete next action. Never report "blocked" due to lack of new data without first completing 1,2,4.
```

## Current Verified State
- Tests: 164/164 OK (pytest, ~18s)
- HEAD: f128b157 (branch main)
- Track C FCLR-H001: FCLR-011 FORECAST_GATE_PASSED (C2 vs B1 -4.94% rel QLIKE, CI [-0.032546,-0.001418] excl zero, 5 instruments, 3 blocks, test 2026-05-08..2026-08-06). FCLR-012-V forward INCONCLUSIVE (data blocked: Binance ends 2026-11-02, 0 test blocks).
- Track A FCLR-H004: FCLR-010 COMPLETE_SEALED FORECAST_GATE_PASSED (Brier -2.21% rel, CI excl zero, 199 instruments, 5 blocks). Blocked on new ironflow parquet >= 2026-11 (last probe 2026-11-04T13:21:55Z, tree unchanged 304).
- Track B: NOT_SUPPORTED.
- Bottlenecks: stale AGENT_HANDOFF claiming Track C NOT_SUPPORTED (superseded by FCLR-011 PASS); forward data blocked (Binance/ironflow); must not let "sealed" status block deeper validation on frozen splits.

## Priority Order (by repo name)
1. **TRACK C - Funding-conditioned volatility** (HIGHEST - matches repo name). Gate PASSED on FCLR-011; execute deeper validation on frozen splits (regime-stratified QLIKE, funding-quartile interactions, mark/index + EMA24 ablations). Forward confirmation blocked on new data.
2. **TRACK A - Liquidation risk** (ON TRIGGER). Only if new admissible unauthenticated liquidation data (>=2026-11 events/fills.parquet) appears. Preregister before outcomes.
3. **INFRA/BOTTLENECKS** - Remove anything slowing progress, but only if it enables 1 or 2. Keep 164/164 green. Never create schedulers/controllers/status-only files.

## Bottleneck Removal Plan
- **Stale handoff eliminated**: AGENT_HANDOFF.md now reflects FCLR-011 PASS; Track C is not closed-negative.
- **Data blocked, work redirected**: Binance archive ends 2026-11-02; ironflow ends 2026-10. Do NOT fabricate, do NOT relax thresholds, do NOT re-run sealed panels. Deeper validation on frozen splits is the required heavy work.
- **Cache utilization**: Mine existing caches (Binance zips/dirs, research_state/data_cache) before any new downloads.
- **Efficient probing**: Use `scripts/monitor_ironflow_liquidations.py --quick` with ETag caching (304) - no manual polling loops.
- **Heavy work enforcement**: All 4 mandatory blocks must complete with concrete artifacts.
- **No bloat**: No new schedulers/controllers/status-only files. Fix existing code paths and keep tests green.

## Next Action (EXACT)
1. Execute STATE SWEEP - write `research_state/campaign_sweep_$(date -u +%Y%m%dT%H%M%SZ).md` (>=150 lines, reconcile AGENT_HANDOFF vs run_manifest contradiction)
2. Execute TRACK C DEEPER VALIDATION - on frozen FCLR-011/FCLR-002 splits only, regime-stratified QLIKE by funding quartiles, funding x RV interactions, mark/index + EMA24 ablations; block-bootstrap>=2000, Holm; write `research_state/trackc_deeper_validation_$(date -u +%Y%m%dT%H%M%SZ).md`
3. Execute TRACK A READINESS - probe ironflow + scan alts, record evidence (probe JSON/ETag/tree diffs). If new >=2026-11 files appear, preregister before outcomes.
4. Execute BOTTLENECK ELIMINATION - clean/fix as needed, ensure 164/164 tests still pass
5. Append a short "SESSION SUMMARY" to this handoff (new timestamp, artifacts created, next concrete task) before ending.

## Verification commands
- `python -m pytest tests/ -q` (expect 164 passed)
- `python scripts/monitor_ironflow_liquidations.py --quick` (Track A probe, expect 304/no new data)
- `git status` (working tree clean except pyc caches)
