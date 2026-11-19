# evidence_audit_20261119T095800Z

Campaign: `FCLR-LIQ-RISK-ESCALATION-09-20261119T095305Z`
Session UTC: `20261119T095800Z`
Per RESEARCH_PROMPT.md §19.

## Verdict

`UNDERPOWERED`. The RISK-09 specification scan (joint funding × RV × open-interest interaction family, 6 members) was executed against the RV-only baseline on the frozen Track A panel. The power gate failed for every scored block (block_2 mde 0.00409, block_3 mde 0.00389, pooled mde 0.00282 vs plausible effect 0.001 Brier), so `models_run=false`. Honest evaluation artifacts are still written; all six members return `NOT_MET` on block_3 (primary) and the scored blocks. No member can be declared SUPPORT or honestly NOT_MET on power grounds.

## What the evidence supported / contradicted / left unknown

- Supported: nothing positive; no family member showed a block_3 Brier improvement over RV-only clearing p_raw<0.05, p_holm<0.05, and placebo-95th<improvement.
- Contradicted: nothing; the test was underpowered, so no negative is claimed.
- Unknown: whether the true incremental Brier effect of funding-conditioned interactions over RV-only is exactly zero or merely below the ~0.0028-0.0041 MDE floor at this sample size.

## Strongest alternative explanation

The funding-conditioned interaction has negligible incremental out-of-sample forecast skill over realized-volatility-only at the detectable effect scale; any true effect is smaller than the plausible-effect threshold (0.001 Brier) and hence undetectable here.

## Dominating limitation

Statistical power (sample size × effect size), not data availability. The panel and labels are complete and admissible (113,880 coin-hours, 13 coins, 12 months; funding 113,880/113,880; OI 113,035/113,880; n_discrepancies=0).

## Concrete falsifying test

RISK-10 power restoration: pooled-block MDE audit + minimum-detectable-effect table by instrument count + a preregistered decision on the smallest defensible effect; re-run only if MDE <= plausible effect. No outcome mining.

## Highest expected information-gain task

Campaign `RISK-10` power restoration design (per the RISK-09 → UNDERPOWERED contingency in AGENT_HANDOFF.md).

## Exact artifact and command demonstrating progress

- Artifact: `research_state/session_20261119T095800Z/fclr_risk09_evaluation_20261119T095800Z.json`
- Command: `python3 scripts/check_handoff_heavywork_gate.py --json` (must PASS); regenerate with `python3 research_state/session_20261119T095800Z/fclr_risk09_evaluation_20261119T095800Z.py`

## Artifacts produced this session

fclr_risk09_prereg_20261119T095800Z.{json,md},
fclr_risk09_power_20261119T095800Z.{py,json,md},
fclr_risk09_recompute_20261119T095800Z.{py,json},
fclr_risk09_evaluation_20261119T095800Z.{py,json,md},
evidence_audit_20261119T095800Z.{json,md},
trigger_check_20261119T095800Z.json
