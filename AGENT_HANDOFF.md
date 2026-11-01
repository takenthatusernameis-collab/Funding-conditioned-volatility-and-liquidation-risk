# AGENT_HANDOFF.md (DURABLE - FCLR-HANDOFF-030)
**TIMESTAMP (UTC):** 2026-11-01T09:19:10Z
**REPO:** Funding-conditioned-volatility-and-liquidation-risk
**BRANCH/HEAD:** main @ f79c9767 (working tree: clean except __pycache__)
**HANDOFF ID:** FCLR-HANDOFF-031-20261101T091910Z
**STATUS:** COUPLED SYNTHESIS COMPLETE (09:19:10Z). Next: pre-register H_COUPLED-001.
**PRIORITIZED BY:** repo name = funding-conditioned volatility ∩ liquidation risk (ONE COUPLED PROBLEM)

## INITIAL TASK MESSAGE (FOR NEXT AGENTIC SESSION) — TIMESTAMPED 2026-11-01T09:19:10Z
**PRIORITY P0 | TYPE: PRE-REGISTRATION (HEAVY) | NO DISCOVERY/SPIN**

Coupled synthesis complete (`research_state/coupled_integration_synthesis_20261101T091910Z.md`).
Next bottleneck: lock H_COUPLED-001 protocol before any runs.

### MANDATORY FIRST ACTION (30s)
```bash
cd /home/runner/work/Funding-conditioned-volatility-and-liquidation-risk/Funding-conditioned-volatility-and-liquidation-risk
git log -1 --oneline && git status --short
python -m unittest discover -s tests -v  # MUST remain 27/27 PASS
LATEST=$(ls -t research_state/coupled_integration_synthesis_*.md | head -1); test -n "$LATEST" && wc -l "$LATEST"
```

### FOCUS CAMPAIGN: `FCLR-COUPLED-PREREG` (HEAVY WORK)
Create `research_state/pre_registration_h_coupled_001_$(date -u +%Y%m%dT%H%M%SZ).md` with:

1. Hypothesis H_COUPLED-001 (funding×vol×observed-flow conditioning >= +1.0% rel Brier vs FCLR-010 C2).
2. Frozen feature set, contrasts, metrics, gates (>=+1.0% rel Brier, paired OOS>=5, >=3 blocks, firewall, calibration).
3. Splits/embargo/inference/multiplicity (Holm if >1). Fixed logistic, no tuning.
4. Firewall: Hyperliquid labels only; no merge with Binance price panels. Modeled≠observed.
5. Exact verify command and next executable step.

### HARD CONSTRAINTS
- No re-running exhausted Track C/B panels. No broad data discovery.
- Cross-track firewall preserved. No .github/workflows changes. No activity commits.
- All tests MUST remain 27/27 PASS.

### FOCUS CAMPAIGN: `FCLR-COUPLED-INTEGRATE` (HEAVY WORK)
Create `research_state/coupled_integration_synthesis_$(date -u +%Y%m%dT%H%M%SZ).md` with:

1. **Coupling rationale**: Why funding-conditioned volatility and liquidation risk are coupled (use FCLR-010 PASSED + Track C exhausted evidence). Explain the observed liquidation link vs volatility forecasting.
2. **Evidence map**: Link FCLR-010, Track C/B, H002 artifacts with concrete paths/hashes. No relabeling.
3. **Joint model spec**: Concrete coupled specification (joint objective/conditioning), features, targets, leakage controls, and why it is testable without merging Hyperliquid labels into Binance price panels.
4. **Pre-registered next test**: Single falsifiable hypothesis + minimal protocol outline (splits/embargo/inference/multiplicity/gate). Keep modeled≠observed separation and respect cross-track firewall.
5. **Actionable plan**: Exactly one highest-value next executable step after synthesis (verifiable command). If synthesis shows no feasible coupled test without violating constraints, say so with evidence.

### HARD CONSTRAINTS
- No re-running exhausted Track C/B panels. No broad data discovery.
- Cross-track firewall: do NOT merge Hyperliquid liquidation labels with Binance price panels.
- Preserve modeled≠observed separation. Block-aware inference; Holm if multiplicity grows.
- No .github/workflows/* changes. No commits for activity only.
- All tests MUST remain 27/27 PASS.

## CURRENT STATE (GATES)
| Track | Hypothesis | Status | Evidence |
|-------|-----------|--------|----------|
| A | FCLR-H004 (observed liquidations) | SUPPORTED/PASSED | research_state/evaluation_summary_FCLR010.md, run_manifest.json#experiments.FCLR-010 |
| C | FCLR-H001 (volatility) | NOT_SUPPORTED/CLOSED | research_state/evaluation_summary_FCLR009.md, track_c_final_synthesis_dossier.md |
| B | FCLR-H003 (boundary breach) | CLOSED_NEGATIVE | research_state/evaluation_summary_FCLR-H003-EXT-001.md |
| H002 | funding-correction | PARTIAL/EXPLORATORY | research_state/h002_replication_report.md |

## REQUIRED END-OF-SESSION OUTPUT
1. What changed and why (concrete files/lines)
2. What was actually tested (exact commands + outcomes)
3. Evidence added (paths)
4. Gate states per track (unchanged or updated with evidence)
5. Single highest-value next task (executable without user intervention)
6. Precise verify command for next task
7. Blockers + next materially different free route OR proof of exhaustive search

## SINGLE HIGHEST-VALUE NEXT TASK
**Task:** Produce pre-registration for H_COUPLED-001 per above.
**Verify:** `LATEST_PREREG=$(ls -t research_state/pre_registration_h_coupled_001_*.md 2>/dev/null | head -1); test -n "$LATEST_PREREG" && echo $LATEST_PREREG && wc -l $LATEST_PREREG`
