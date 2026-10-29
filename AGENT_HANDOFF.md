# AGENT HANDOFF — Funding-Conditioned Volatility and Liquidation Risk
UPDATED: 2026-10-29T21:11:19Z
HEAD: 358a8bac (main)
REPO: Funding-conditioned-volatility-and-liquidation-risk

## PRIORITY
1) VOLATILITY FORECASTING GATES FIRST - all FCLR-001/002/003 INCONCLUSIVE. Risk-overlay INELIGIBLE until gate passes.
2) FCLR-004 IN PROGRESS - pre-registered, features fixed, split-audit needed

## FCLR-004 STATUS (PRE-REGISTERED)
- Protocol: research_state/research_protocol_fclr004.md (v1.0, frozen)
- Hypothesis: FCLR-H001, PRIMARY CONTRAST: C1' vs B1 (pivoted from C2 vs B1 due to C2 degradation in FCLR-003)
- Rationale: C1 beats B1 in FCLR-003 (-8.09%), C2 worse than C1; funding signal stronger than broken price features
- Fixed: EMA computation (proper recursive) and premium/index loading added to scripts/run_evaluation.py
- Registries updated: hypothesis_registry.json, leakage_audit.md, run_manifest.json

## BOTTLENECKS
- Split reuse: FCLR-003 test (Oct-Dec 2024, 91 days, 3 blocks) is only window meeting block count; all windows overlap frozen test sets. Need timestamp-level audit.
- If no unused >=3-block window exists for 24h: must pivot to alternative horizon (6h) with justification OR document exhaustively.

## NEXT ACTION (HEAVY WORK)
1. Do timestamp-level audit: enumerate all timestamps used in FCLR-001/002/003 train/val/test; find unused window in common 5-symbol panel with >=3 blocks for 24h
2. If found: add split_boundaries_fclr004 to run_manifest, run FCLR-004
3. If not: pre-register 6h as primary with new splits not overlapping, justify, run
4. Write full evaluation_summary_FCLR004.md regardless
5. Update gate_assessment.md, negative_results_report.md

CONSTRAINTS: no paid services/trials/keys/live/paper trading; no .github/workflows changes; no reuse of sealed holdouts; append-only; every action produces artifact.
