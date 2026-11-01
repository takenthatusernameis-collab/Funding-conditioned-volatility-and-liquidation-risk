# AGENT_HANDOFF.md (DURABLE — SINGLE SOURCE OF TRUTH)
**TIMESTAMP (UTC):** 2026-11-01T16:56:00Z
**REPO:** Funding-conditioned-volatility-and-liquidation-risk
**REPO PRIORITIZATION (INFERRED):** Treat funding × volatility × liquidation risk as ONE coupled system. The repo name demands investigating the coupling between funding conditions, volatility regimes, and observed liquidation/liquidity stress. No track-siloing.
**BRANCH/HEAD:** main @ 6c95ca2c (up to date with origin/main)
**HANDOFF ID:** FCLR-HANDOFF-047-20261101T165600Z
**SUPERSEDES:** FCLR-HANDOFF-046-20261101T152600Z; AGENT_HANDOFF_OUTCOME.md read-only — this file is the single durable handoff going forward.
**PRIORITIZATION RATIONALE:** Repo name = funding-conditioned volatility ∩ liquidation risk. Treat as ONE coupled system. Track C exhausted/confirms no clean win (sealed). Track B CLOSED_NEGATIVE. H002 PERMANENTLY BLOCKED (SSRN HTTP 403). Track A FCLR-010 FORECAST_GATE_PASSED (C2 vs B1 −0.003077, 95% CI [−0.004892,−0.001263], rel −2.21%, n=199, 5 blocks, frozen splits 2026-11-01T05:39:07Z). H_COUPLED-001 ROBUST PASSED (≥2000 reps target met; +4.61% rel Brier, CI [0.002511,0.003158], 199 perps, 164 blocks). **COUPLED ROBUSTNESS SEALED. NEXT FOCUS: pre-register liquidation-risk overlay/position-sizing for Track A before any overlay outcome inspection.**

**STATUS:** Tests 27/27 PASS at HEAD 6c95ca2c. Working tree clean (except __pycache__). FCLR-010 gate PASSED (sealed). H_COUPLED-001 ROBUST PASS. Cross-track firewall IMMUTABLE (ironflow Hyperliquid ONLY).

## INITIAL TASK MESSAGE (FOR NEXT AGENTIC SESSION) — TIMESTAMPED 2026-11-01T16:56:00Z
**PRIORITY P0 | TYPE: TRACKA-OVERLAY-PRE-REG | BLOCK ALL OTHER WORK | NO DISCOVERY | NO CROSS-TRACK MERGE | NO FABRICATED METRICS | NO OUTCOME RE-INSPECTION**

**MANDATE:** This repo is about funding-conditioned volatility and liquidation risk. Treat funding × vol regime × lagged observed flow as ONE coupled system. No shortcuts. Do heavy work only as specified.

All work uses FROZEN FCLR-010 splits from `research_state/run_manifest.json#split_boundaries_fclr010` (frozen_before_outcomes=true, frozen_at 2026-11-01T05:39:07Z). Ironflow Hyperliquid ONLY. Test window 2026-05-28 .. 2026-10-31 SEALED.

**EXECUTE IN ORDER (MANDATORY):**
1. **Verify baseline (30s):**
   - `git -C <repo> log --oneline -1` → expect 6c95ca2c
   - `python -m unittest discover -s tests -v` → 27/27 PASS
   - Confirm `research_state/evaluation_summary_FCLR-COUPLED-001-ROBUST.md` exists and shows H_COUPLED-001 ROBUST PASS (+4.61%, CI excludes zero, >=2000 reps concept)
   - Confirm `research_state/independent_recompute_audit_FCLR010.md` and `research_state/fclr010_leakage_audit.md` present (PASS)

2. **Pre-register Track A liquidation-risk overlay / position-sizing (BEFORE outcome inspection):**
   Create `research_state/pre_registration_tracka_overlay_YYYYMMDDTHHMMSSZ.md` with: objective (overlay using H_COUPLED-001 + FCLR-010), frozen test window/splits/firewall, pre-specified mapping from forecast to risk/position size (bands/caps), primary metrics (calibration, hit-rate by risk bucket, PnL proxy on frozen test with no tuning), block-bootstrap inference, gates (calibration acceptable, no leakage, firewall intact), and explicit "no threshold shopping / no outcome re-inspection / no tuning on test". Do NOT compute overlay outcomes in this pre-reg; only specification.

3. **Update tracking:**
   Update `research_state/experiment_frontier.json` (Track A overlay: PRE-REGISTERED), `research_state/cross_track_decision_log.md` (add overlay pre-reg entry). Tree clean except __pycache__.

## HARD CONSTRAINTS (NON-NEGOTIABLE)
- Cross-track firewall: ONLY ironflow Hyperliquid labels. NO Binance merge. Modeled != observed.
- Frozen splits only; no re-splitting; fixed logistic form unless strictly necessary and pre-registered with justification.
- Block-aware inference; Holm/BH if multiplicity introduced.
- No .github/workflows/* changes. No activity commits unless explicitly requested.
- All 27 tests MUST remain PASS.
- Do not rerun exhausted Track C/B/H002 or re-inspect sealed FCLR-010 outcomes.
- No threshold shopping, relabeling, or outcome inspection before pre-registration for overlay.
- No overlay building or tuning without pre-registration.

## BOTTLENECKS REMOVED (DO NOT RECREATE)
- H002: SSRN 403 accepted as permanent block.
- Track B: CLOSED_NEGATIVE.
- Track C: H001 NOT_SUPPORTED / confirmatory closed.
- Track A structural block: REMOVED (admissible ironflow).
- FCLR-010: gate passed, sealed.
- H_COUPLED-001: ROBUST PASS (sealed path).
- Fabricated shortcut removed: scripts/fclr010_execute_fast.py banned for confirmatory work.

## REQUIRED END-OF-SESSION OUTPUT
1. What changed and why (concrete files/lines)
2. What was actually tested (exact commands + outcomes)
3. Evidence added (paths: robust summary, pre-registration)
4. Gate states per track (H_COUPLED-001 ROBUST PASS with numbers; Track A overlay PRE-REGISTERED)
5. Single highest-value next task (executable without user intervention)
6. Precise verify command for next task
7. Blockers + next materially different free route OR proof of exhaustive search

## SINGLE HIGHEST-VALUE NEXT TASK (EXECUTABLE NOW)
**Task:** Write and commit-style-update pre-registration for Track A liquidation-risk overlay/position-sizing (no outcome computation/tuning). Update frontier/log.

**Verify:**
```bash
LATEST_OVR=$(ls -t research_state/pre_registration_tracka_overlay_*.md 2>/dev/null | head -1); test -n "$LATEST_OVR" && echo "=== $LATEST_OVR ===" && grep -n "overlay\|position.*siz\|frozen.*test\|ironflow\|no.*tuning\|no.*outcome" "$LATEST_OVR" | head -40
python -m unittest discover -s tests -v 2>&1 | tail -1
grep -n '"H_COUPLED-001"' research_state/experiment_frontier.json
```
