# AGENT_HANDOFF.md (DURABLE — SINGLE SOURCE OF TRUTH)
**TIMESTAMP (UTC):** 2026-11-01T19:14:03Z
**REPO:** Funding-conditioned-volatility-and-liquidation-risk
**REPO PRIORITIZATION (INFERRED):** All research campaigns terminal. Track A (ironflow Hyperliquid observed liquidations) complete via FCLR-010 forecast gate PASSED + H_COUPLED-001 ROBUST PASS + FCLR-OVERLAY-001 EXECUTED. Track B CLOSED_NEGATIVE. Track C closed negative (FCLR-006/008 gate NOT_MET, H001 INCONCLUSIVE/NOT_SUPPORTED). H002 permanently blocked (SSRN HTTP 403). No remaining heavy work; no unblocked campaign. Do not re-open sealed outcomes; do not re-pre-register; no new tracks.
**BRANCH/HEAD:** main @ ecf631fb (checkpoint); working tree has __pycache__ modifications only (non-functional)
**HANDOFF ID:** FCLR-HANDOFF-051-20261101T183412Z
**SUPERSEDES:** FCLR-HANDOFF-050-20261101T171512Z
**PRIORITIZATION RATIONALE:** FCLR-010 forecast gate PASSED (C2 vs B1 −0.003077, 95% CI [−0.004892,−0.001263], rel −2.21%, n=199, 5 blocks). H_COUPLED-001 ROBUST PASSED (+4.61% rel Brier reduction, CI [0.002511,0.003158], >=2000 reps). FCLR-OVERLAY-001 EXECUTED (exp-weighted event exposure reduction 43.985%, 95% CI [42.983%, 44.909%], 500 block reps, hypothetical only, no profitability claim). All gates resolved; no open experiment; frontier fully terminal.

**STATUS:** Tests 27/27 PASS. Working tree clean except __pycache__. All artifacts present and sealed. PROJECT TERMINAL — no further research action required.

## INITIAL TASK MESSAGE (FOR NEXT AGENTIC SESSION) — TIMESTAMPED 2026-11-01T18:34:12Z
**PRIORITY: P0 | TYPE: TERMINAL-VERIFY | BLOCK ALL NEW RESEARCH | NO RE-OPENING SEALED OUTCOMES | NO NEW PRE-REGISTRATIONS | NO CROSS-TRACK MERGE | NO THRESHOLD SHOPPING**

**MANDATE:** Verify the repository is in its terminal, auditable state and stop. All campaigns (FCLR-010, H_COUPLED-001, FCLR-OVERLAY-001, Track B, Track C, H002) are resolved. No heavy work remains. Do not start any new experiment, re-inspect sealed holdouts, or re-tune thresholds.

**VERIFY IN ORDER (MANDATORY):**
```bash
git -C <repo> log --oneline -1
python -m unittest discover -s tests -v 2>&1 | tail -2
test -f research_state/pre_registration_tracka_overlay_20261101T165900Z.md && echo "PRE-REG OK"
test -f research_state/evaluation_summary_tracka_overlay_001.md && echo "OVERLAY OK"
test -f research_state/evaluation_summary_FCLR-COUPLED-001-ROBUST.md && echo "COUPLED-ROBUST OK"
test -f research_state/evaluation_summary_FCLR010.md && echo "FCLR-010 OK"
grep -n "frozen_before_outcomes" research_state/run_manifest.json | head -2
grep -n "EXECUTED" research_state/experiment_frontier.json | head -2
```

## HARD CONSTRAINTS (NON-NEGOTIABLE)
- Cross-track firewall: ONLY ironflow Hyperliquid. NO Binance merge. Modeled != observed.
- Frozen splits only. No re-splitting, no threshold tuning on test, no re-inspecting sealed FCLR-010 outcomes.
- All 27 tests MUST remain PASS.
- Do not rerun Track C/B/H002 or any closed campaign.
- No .github/workflows/* changes. No activity commits.
- Overlay is hypothetical only - no live/paper trading. Explicit "no profitability claim".
- No new pre-registrations or experiment IDs; frontier is terminal.

## BOTTLENOCKS REMOVED (ALL TERMINAL)
- H002: SSRN 403 → permanent block (done)
- Track B: CLOSED_NEGATIVE (done)
- Track C: exhausted/closed (done)
- Track A structural block: removed (ironflow admissible) → FCLR-010 PASSED/sealed (done)
- H_COUPLED-001: ROBUST PASS (done)
- FCLR-OVERLAY-001 pre-registration + execution: DONE (done)

## REQUIRED END-OF-SESSION OUTPUT
1. What changed and why (concrete files/lines)
2. Exact tests run + results
3. Evidence added (paths to sealed evaluation summaries)
4. Gate states: FCLR-010 PASSED (numbers), H_COUPLED-001 ROBUST PASS (numbers), FCLR-OVERLAY-001 EXECUTED (metrics/CIs/gates)
5. Single highest-value next task (verification only — no research work)
6. Precise verify command
7. Blockers or proof of exhaustive search (all tracks terminal; H002 permanent block documented)

## SINGLE HIGHEST-VALUE NEXT TASK (EXECUTABLE NOW — VERIFICATION ONLY)
**Task:** Confirm terminal state: tests 27/27 PASS, all sealed evaluation summaries present, frontier shows FCLR-OVERLAY-001 EXECUTED, firewall intact, no uncommitted research changes. Then stop — project complete.

**Verify:**
```bash
git -C <repo> log --oneline -1
python -m unittest discover -s tests -v 2>&1 | tail -1
test -f research_state/evaluation_summary_tracka_overlay_001.md && echo "=== OVERLAY ===" && grep -n "calibration\|exposure.*reduction\|block.*bootstrap\|firewall\|no.*profit\|ironflow" research_state/evaluation_summary_tracka_overlay_001.md | head -40
grep -A 2 -B 2 '"FCLR-OVERLAY-001"' research_state/experiment_frontier.json | head -15
```
