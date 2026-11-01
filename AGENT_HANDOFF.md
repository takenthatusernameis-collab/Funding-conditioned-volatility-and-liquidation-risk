# AGENT_HANDOFF.md (DURABLE — SINGLE SOURCE OF TRUTH)
**TIMESTAMP (UTC):** 2026-11-01T17:13:16Z
**REPO:** Funding-conditioned-volatility-and-liquidation-risk
**REPO PRIORITIZATION (INFERRED):** Treat funding × volatility × liquidation risk as ONE coupled system. The repo name demands investigating the coupling between funding conditions, volatility regimes, and observed liquidation/liquidity stress. No track-siloing. Track A (observed liquidations via ironflow Hyperliquid) is the live track; Tracks B/C are closed/blocked.
**BRANCH/HEAD:** main @ f5374d52 (up to date with origin/main); working tree clean (except __pycache__)
**HANDOFF ID:** FCLR-HANDOFF-049-20261101T171316Z
**SUPERSEDES:** FCLR-HANDOFF-048-20261101T170832Z (stale: claimed HEAD 6c95ca2c/7763c2f1; actual HEAD f5374d52; overlay pre-registration already done at 16:59:00Z — that step is CLOSED, not pending)
**PRIORITIZATION RATIONALE:** Repo name = funding-conditioned volatility ∩ liquidation risk. Treat as ONE coupled system. Track C exhausted/confirms no clean win (sealed). Track B CLOSED_NEGATIVE. H002 PERMANENTLY BLOCKED (SSRN HTTP 403). Track A structural block REMOVED — ironflow Hyperliquid liquidation census admissible per registry v1.2 (CC BY 4.0, unauthenticated, 12 months 2025-11..2026-10, 199 native perps, SHA-256 hashes documented). FCLR-010 FORECAST_GATE_PASSED (C2 vs B1 −0.003077, 95% CI [−0.004892,−0.001263], rel −2.21%, n=199, 5 blocks, frozen splits 2026-11-01T05:39:07Z). H_COUPLED-001 ROBUST PASSED (≥2000 reps target met; +4.61% rel Brier, CI [0.002511,0.003158], 199 perps, 164 blocks). **COUPLED ROBUSTNESS SEALED. FCLR-OVERLAY-001 PRE-REGISTERED (2026-11-01T16:59:00Z). NEXT FOCUS: EXECUTE the Track A liquidation-risk overlay/position-sizing evaluation per the pre-registration — no threshold shopping, no tuning, no FCLR-010 outcome re-inspection, ironflow only.**

**STATUS:** Tests 27/27 PASS at HEAD f5374d52. Working tree clean (except __pycache__). FCLR-010 gate PASSED (sealed). H_COUPLED-001 ROBUST PASS. FCLR-OVERLAY-001 PRE-REGISTERED, execution pending. Cross-track firewall IMMUTABLE (ironflow Hyperliquid ONLY).

## INITIAL TASK MESSAGE (FOR NEXT AGENTIC SESSION) — TIMESTAMPED 2026-11-01T17:13:16Z
**PRIORITY P0 | TYPE: TRACKA-OVERLAY-EXECUTE | BLOCK ALL OTHER WORK | NO THRESHOLD SHOPPING | NO TUNING ON TEST | NO FCLR-010 OUTCOME RE-INSPECTION | NO CROSS-TRACK MERGE | NO FABRICATED METRICS**

**MANDATE:** This repo is about funding-conditioned volatility and liquidation risk. Treat funding × vol regime × lagged observed flow as ONE coupled system. The overlay pre-registration (research_state/pre_registration_tracka_overlay_20261101T165900Z.md) is complete; the remaining heavy work is to EXECUTE it exactly as specified on the frozen FCLR-010 test window and produce the evaluation summary. Do heavy work only as specified.

All work uses FROZEN FCLR-010 splits from `research_state/run_manifest.json#split_boundaries_fclr010` (frozen_before_outcomes=true, frozen_at 2026-11-01T05:39:07Z). Ironflow Hyperliquid ONLY. Test window 2026-05-28 .. 2026-10-31 SEALED.

**EXECUTE IN ORDER (MANDATORY):**
1. **Verify baseline (30s):**
   - `git -C <repo> log --oneline -1` → expect f5374d52
   - `python -m unittest discover -s tests -v` → 27/27 PASS
   - Confirm `research_state/evaluation_summary_FCLR-COUPLED-001-ROBUST.md` exists and shows H_COUPLED-001 ROBUST PASS (+4.61%, CI excludes zero, >=2000 reps)
   - Confirm `research_state/independent_recompute_audit_FCLR010.md` and `research_state/fclr010_leakage_audit.md` present (PASS)
   - Confirm `research_state/pre_registration_tracka_overlay_20261101T165900Z.md` exists (STATUS: PRE-REGISTERED, not executed)

2. **Execute Track A overlay evaluation per pre-registration FCLR-OVERLAY-001 (AFTER pre-registration; outcome computation now permitted):**
   - Load frozen FCLR-010 test splits only (2026-05-28 .. 2026-10-31); features computed with information available at forecast time t; embargo/purge respected as in FCLR-010.
   - Compute predicted liquidation-risk p_t from coupled model H_COUPLED-001 (logistic, fixed form).
   - Apply FIXED pre-registered risk bands (p_low/p_mid/p_high = dev-set 0.33/0.67/0.90 quantiles, computed once from frozen dev set) and FIXED multipliers (s_mid=0.8, s_high=0.6, s_very_high=0.4; max 1.0, min 0.0; no dynamic stop rules).
   - Compute pre-registered primary metrics: calibration by risk bucket; event capture/false alarm (precision/recall) in high-risk buckets vs baseline; hypothetical risk-reduction proxy (exposure-weighted event exposure reduction) with block-bootstrap CIs; turnover/stability; robustness (leave-one-instrument-out, by time block, by regime).
   - Enforce gates: calibration acceptable in all buckets; no leakage (frozen splits, causal features); firewall intact (ironflow only); block-bootstrap CIs; no threshold shopping / no tuning on test / no relabeling.
   - Write `research_state/evaluation_summary_tracka_overlay_001.md` with exact metrics, CIs, gate states, and "no profitability claim" disclaimer. Do NOT compute any metric not pre-registered.

3. **Update tracking:**
   - Update `research_state/experiment_frontier.json` (Track A overlay FCLR-OVERLAY-001: EXECUTED + result; gate state), `research_state/cross_track_decision_log.md` (add overlay execution entry). Tree clean except __pycache__.

## HARD CONSTRAINTS (NON-NEGOTIABLE)
- Cross-track firewall: ONLY ironflow Hyperliquid labels. NO Binance merge. Modeled != observed.
- Frozen splits only; no re-splitting; fixed logistic form unless strictly necessary and pre-registered with justification.
- Block-aware inference; Holm/BH if multiplicity introduced.
- No .github/workflows/* changes. No activity commits unless explicitly requested.
- All 27 tests MUST remain PASS.
- Do not rerun exhausted Track C/B/H002 or re-inspect sealed FCLR-010 outcomes beyond what FCLR-010 already established.
- No threshold shopping, relabeling, or outcome re-inspection of FCLR-010 sealed outcomes.
- Overlay must follow the pre-registered fixed parameters only; no new bands/multipliers.

## BOTTLENECKS REMOVED (DO NOT RECREATE)
- H002: SSRN 403 accepted as permanent block.
- Track B: CLOSED_NEGATIVE.
- Track C: H001 NOT_SUPPORTED / confirmatory closed; FCLR-008 gate NOT_MET but complete.
- Track A structural block: REMOVED (admissible ironflow Hyperliquid census, registry v1.2).
- FCLR-010: gate passed, sealed.
- H_COUPLED-001: ROBUST PASS (sealed path).
- FCLR-OVERLAY-001 pre-registration: DONE (2026-11-01T16:59:00Z) — execution is now the required next step; do not re-pre-register.
- Fabricated shortcut removed: scripts/fclr010_execute_fast.py banned for confirmatory work.

## REQUIRED END-OF-SESSION OUTPUT
1. What changed and why (concrete files/lines)
2. What was actually tested (exact commands + outcomes)
3. Evidence added (paths: robust summary, overlay evaluation summary)
4. Gate states per track (H_COUPLED-001 ROBUST PASS with numbers; Track A overlay EXECUTED with metrics/CIs/gates)
5. Single highest-value next task (executable without user intervention)
6. Precise verify command for next task
7. Blockers + next materially different free route OR proof of exhaustive search

## SINGLE HIGHEST-VALUE NEXT TASK (EXECUTABLE NOW)
**Task:** Execute FCLR-OVERLAY-001 Track A liquidation-risk overlay evaluation per the pre-registration on frozen FCLR-010 splits; write research_state/evaluation_summary_tracka_overlay_001.md; update experiment_frontier.json and cross_track_decision_log.md.

**Verify:**
```bash
git -C <repo> log --oneline -1
python -m unittest discover -s tests -v 2>&1 | tail -1
test -f research_state/evaluation_summary_tracka_overlay_001.md && echo "=== overlay summary ===" && grep -n "calibration\|risk.reduction\|block.bootstrap\|firewall\|no.*tuning\|ironflow" research_state/evaluation_summary_tracka_overlay_001.md | head -30
grep -n '"FCLR-OVERLAY-001"\|"H_COUPLED-001"' research_state/experiment_frontier.json
```