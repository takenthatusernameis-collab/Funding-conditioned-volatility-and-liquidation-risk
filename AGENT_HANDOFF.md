# AGENT_HANDOFF.md (DURABLE — SINGLE SOURCE OF TRUTH)
**TIMESTAMP (UTC):** 2026-11-01T18:33:23Z
**REPO:** Funding-conditioned-volatility-and-liquidation-risk
**REPO PRIORITIZATION (INFERRED):** Treat funding × volatility × liquidation risk as ONE coupled system. Repo name demands investigating the coupling between funding conditions, volatility regimes, and observed liquidation/liquidity stress. No track-siloing. Track A (observed liquidations via ironflow Hyperliquid) is the ONLY eligible track. Tracks B/C closed/blocked. H002 blocked.
**BRANCH/HEAD:** main @ 06989c49 (checkpoint); working tree has __pycache__ modifications only (non-functional)
**HANDOFF ID:** FCLR-HANDOFF-050-20261101T171512Z
**SUPERSEDES:** FCLR-HANDOFF-049-20261101T171316Z
**PRIORITIZATION RATIONALE:** FCLR-010 forecast gate PASSED (C2 vs B1 −0.003077, 95% CI [−0.004892,−0.001263], rel −2.21%, n=199, 5 blocks). H_COUPLED-001 ROBUST PASSED (+4.61% rel Brier reduction, CI [0.002511,0.003158], >=2000 reps). FCLR-OVERLAY-001 PRE-REGISTERED at 2026-11-01T16:59:00Z with FIXED bands/multipliers. **EXECUTION IS THE ONLY REMAINING HEAVY WORK. DO NOT RE-PRE-REGISTER. DO NOT RE-INSPECT SEALED FCLR-010 OUTCOMES.**

**STATUS:** Tests 27/27 PASS. Working tree clean except __pycache__. FCLR-010 sealed. H_COUPLED-001 ROBUST sealed. FCLR-OVERLAY-001 PRE-REGISTERED → EXECUTE NOW. Cross-track firewall IMMUTABLE (ironflow Hyperliquid ONLY).

## INITIAL TASK MESSAGE (FOR NEXT AGENTIC SESSION) — TIMESTAMPED 2026-11-01T18:33:23Z
**PRIORITY P0 | TYPE: TRACKA-OVERLAY-EXECUTE | BLOCK ALL OTHER WORK | NO THRESHOLD SHOPPING | NO TUNING ON TEST | NO FCLR-010 RE-INSPECTION | NO CROSS-TRACK MERGE | NO FABRICATED METRICS**

**MANDATE:** This repo = funding-conditioned volatility × liquidation risk. The overlay pre-registration is DONE. Your job is HEAVY EXECUTION: compute overlay metrics exactly as specified on frozen splits and write the evaluation summary. No exploration, no refactors, no new features.

**EXECUTE IN ORDER (MANDATORY):**
1. **Verify baseline (fast):**
   ```bash
   git -C <repo> log --oneline -1
   python -m unittest discover -s tests -v 2>&1 | tail -2
   test -f research_state/pre_registration_tracka_overlay_20261101T165900Z.md && echo "PRE-REG OK"
   test -f research_state/evaluation_summary_FCLR-COUPLED-001-ROBUST.md && echo "COUPLED-ROBUST OK"
   grep -n "frozen_before_outcomes" research_state/run_manifest.json | head -2
   ```

2. **Execute FCLR-OVERLAY-001 per pre-registration (ONLY allowed outcome computation):**
   - Load frozen FCLR-010 test splits from `run_manifest.json#split_boundaries_fclr010` (test 2026-05-28 .. 2026-10-31). Dev set for quantiles only.
   - Use coupled model H_COUPLED-001 predictions on frozen test window (ironflow Hyperliquid native perps only).
   - Compute dev-only quantiles: p_low = 0.33, p_mid = 0.67, p_high = 0.90 from frozen dev calibration distribution.
   - Apply FIXED multipliers: s_mid=0.8, s_high=0.6, s_very_high=0.4 (max 1.0, min 0.0). No dynamic rules.
   - Compute pre-registered metrics: calibration by bucket, event capture/precision-recall in high-risk buckets vs baseline, exposure-weighted event exposure reduction with block-bootstrap CIs (~24h blocks), turnover/stability, robustness (LOSO, by time block, by regime).
   - Enforce: causal features only, embargo/purge respected, firewall intact, no threshold shopping/tuning, no relabeling.

3. **Write artifacts & update tracking:**
   - Write `research_state/evaluation_summary_tracka_overlay_001.md` with exact numbers, CIs, gate states, "no profitability claim" disclaimer, and hash/config provenance.
   - Update `research_state/experiment_frontier.json` (FCLR-OVERLAY-001: EXECUTED + result + gate state)
   - Update `research_state/cross_track_decision_log.md` (add execution entry with timestamp)
   - Keep tree clean except `__pycache__`. Do not commit.

## HARD CONSTRAINTS (NON-NEGOTIABLE)
- Cross-track firewall: ONLY ironflow Hyperliquid. NO Binance merge. Modeled != observed.
- Frozen splits only. Fixed logistic form. Dev-only quantiles. Fixed multipliers.
- Block-aware inference (block-bootstrap). Control multiplicity only if variants introduced (but only fixed params specified).
- No .github/workflows/* changes. No activity commits.
- All 27 tests MUST remain PASS.
- Do not rerun Track C/B/H002 or re-inspect sealed FCLR-010 outcomes.
- No threshold shopping, relabeling, or outcome re-inspection.
- Overlay is hypothetical only - no live/paper trading. Explicit "no profitability claim".

## BOTTLENECKS REMOVED
- H002: SSRN 403 → permanent block (done)
- Track B: CLOSED_NEGATIVE (done)
- Track C: exhausted/closed (done)
- Track A structural block: removed (ironflow admissible)
- FCLR-010: passed/sealed (done)
- H_COUPLED-001: ROBUST PASS (done)
- FCLR-OVERLAY-001 pre-registration: DONE (done) → execution now unblocked

## REQUIRED END-OF-SESSION OUTPUT
1. What changed and why (concrete files/lines)
2. Exact tests run + results
3. Evidence added (path to `evaluation_summary_tracka_overlay_001.md`)
4. Gate states: H_COUPLED-001 ROBUST PASS (numbers), FCLR-OVERLAY-001 EXECUTED (metrics/CIs/gates)
5. Single highest-value next task (executable without user intervention)
6. Precise verify command
7. Blockers or proof of exhaustive search

## SINGLE HIGHEST-VALUE NEXT TASK (EXECUTABLE NOW)
**Task:** Execute FCLR-OVERLAY-001 Track A liquidation-risk overlay evaluation per pre-registration on frozen FCLR-010 splits; write `research_state/evaluation_summary_tracka_overlay_001.md`; update `experiment_frontier.json` and `cross_track_decision_log.md`.

**Verify:**
```bash
git -C <repo> log --oneline -1
python -m unittest discover -s tests -v 2>&1 | tail -1
test -f research_state/evaluation_summary_tracka_overlay_001.md && echo "=== OVERLAY ===" && grep -n "calibration\|exposure.*reduction\|block.*bootstrap\|firewall\|no.*profit\|ironflow" research_state/evaluation_summary_tracka_overlay_001.md | head -40
grep -A 2 -B 2 '"FCLR-OVERLAY-001"' research_state/experiment_frontier.json | head -15
```
