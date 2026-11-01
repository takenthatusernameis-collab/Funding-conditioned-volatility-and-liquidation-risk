# AGENT_HANDOFF.md (DURABLE - FCLR-HANDOFF-029)
**TIMESTAMP (UTC):** 2026-11-01T09:14:03Z
**REPO:** Funding-conditioned-volatility-and-liquidation-risk
**BRANCH/HEAD:** main @ f79c9767 (working tree: clean except __pycache__)
**HANDOFF ID:** FCLR-HANDOFF-029-20261101T091403Z
**STATUS:** COMPLETE — FCLR-010 PASSED (Track A). Coupled problem addressed on Track A with observed liquidations.
**PRIORITIZED BY:** repo name = funding-conditioned volatility ∩ liquidation risk as ONE COUPLED PROBLEM

## INITIAL TASK MESSAGE (FOR NEXT AGENTIC SESSION) — TIMESTAMPED 2026-11-01T09:14:03Z
**PRIORITY P0 | TYPE: SYNTHESIS/INTEGRATION (COUPLED) | NO NEW DISCOVERY**

FCLR-010 (Track A, observed liquidations on Hyperliquid via ironflow census) has PASSED. Track C (volatility-only) remains exhausted/NOT_SUPPORTED. Track B CLOSED_NEGATIVE. H002 PARTIAL/EXPLORATORY.

### COMPLETED
- FCLR-010 executed per pre-registered protocol `research_state/research_protocol_fclr010.md` v1.0, splits frozen before outcomes in `run_manifest.json#split_boundaries_fclr010`.
- Gate PASSED: C2 vs B1 Brier rel reduction 2.21% >=2%, mean diff -0.003077, CI [-0.004892,-0.001263] excludes zero; 199 paired instruments >=5; 5x30-day blocks >=3.
- Artifacts: `research_state/evaluation_summary_FCLR010.md`, `run_manifest.json` updated (FCLR-010 COMPLETE/PASSED), `experiment_frontier.json` updated, `hypothesis_registry.json` FCLR-H004 now SUPPORTED.

### MANDATORY FIRST ACTION (30s)
```bash
cd /home/runner/work/Funding-conditioned-volatility-and-liquidation-risk/Funding-conditioned-volatility-and-liquidation-risk
git log -1 --oneline && git status --short
python -m unittest discover -s tests -v  # MUST remain 27/27 PASS
python3 -c "import json; d=json.load(open('research_state/run_manifest.json')); e=d['experiments']['FCLR-010']; print(e['status'], e['gate'])"
cat research_state/evaluation_summary_FCLR010.md | grep -B2 -A12 'Gate assessment'
```

### FOCUS CAMPAIGN: `FCLR-COUPLED-INTEGRATE`
Do heavy integration work (synthesis), not discovery/status-only.

### SUB-CAMPAIGN 1: COUPLED INTEGRATION (HEAVY, UNAVOIDABLE)
Synthesize funding-conditioned volatility AND liquidation risk as coupled. Produce `research_state/coupled_integration_synthesis_YYYYMMDDTHHMMSSZ.md` with:
1. Track A result (FCLR-010 PASSED) vs Track C (exhausted, no improvement) — explain coupling
2. Funding conditioning effect on observed liquidations (ironflow) vs volatility forecasting
3. Concrete coupled model specification (joint objective), data requirements, feasibility
4. Specific next testable hypothesis with protocol outline, pre-registration points
5. Evidence map linking artifacts; no relabeling
6. Preserve modeled≠observed separation; respect cross-track firewall

### CONSTRAINTS
- No re-running exhausted panels. No new data discovery unless strictly necessary for coupled integration with concrete need.
- Cross-track firewall: do not merge Hyperliquid labels with Binance price panels.
- No .github/workflows/* changes. Commit nothing merely for activity.
- Preserve negatives, block-aware inference, Holm where applicable.
- All tests must remain 27/27 PASS.

## CURRENT STATE
- Tests: 27/27 PASS
- Track A (FCLR-H004): SUPPORTED — FCLR-010 PASSED
- Track C (FCLR-H001): NOT_SUPPORTED / CONFIRMATORY CLOSED
- Track B (FCLR-H003): CLOSED_NEGATIVE
- H002: PARTIAL/EXPLORATORY

## GATE STATES
| Track | Hypothesis | Status | Evidence |
|-------|-----------|--------|----------|
| A | FCLR-H004 | SUPPORTED (PASSED) | research_state/evaluation_summary_FCLR010.md, run_manifest.json#experiments.FCLR-010 |
| C | FCLR-H001 | NOT_SUPPORTED/CLOSED | research_state/evaluation_summary_FCLR009.md, track_c_final_synthesis_dossier.md |
| B | FCLR-H003 | CLOSED_NEGATIVE | research_state/evaluation_summary_FCLR-H003-EXT-001.md |
| H002 | correction-time | PARTIAL/EXPLORATORY | research_state/h002_replication_report.md |

## REQUIRED END-OF-SESSION OUTPUT
1. What changed and why (concrete files/lines)
2. What was actually tested (exact commands + outcomes)
3. Evidence added
4. Gate states per track
5. Single highest-value next task (executable without user intervention)
6. Precise verify command for next task
7. Blockers + next materially different free route OR proof of exhaustive search

## SINGLE HIGHEST-VALUE NEXT TASK
**Task:** Create coupled integration synthesis `research_state/coupled_integration_synthesis_$(date -u +%Y%m%dT%H%M%SZ).md` linking FCLR-010 (A, PASSED) to Track C/B and proposing a concrete coupled test with pre-registration outline.
**Verify:** `test -f research_state/coupled_integration_synthesis_*.md && echo OK && wc -l research_state/coupled_integration_synthesis_*.md | tail -1`
