# FCLR-RISK-10 Evidence Audit (per RESEARCH_PROMPT.md §19)

Campaign: `FCLR-LIQ-RISK-ESCALATION-10-20261119T105200Z`
Session UTC: `20261119T110653Z`

## What the evidence supported, contradicted, or left unknown

- **Supported:** none. The power gate failed for all scored blocks (`mde_brier_80pct` 0.0028–0.0041 > `PLAUSIBLE_EFFECT_BRIER=0.001`), so no family member can be declared SUPPORT or honestly NOT_MET on power grounds.
- **Contradicted:** none. No family member demonstrated a block_3 Brier improvement over RV-only clearing `p_raw<0.05`, `p_holm<0.05`, and placebo-95th<improvement.
- **Unknown:** whether the true incremental Brier effect of funding-conditioned interactions over RV-only is exactly zero or merely below the ~0.0028–0.0041 MDE floor at this sample size.

## Strongest alternative explanation

The funding-conditioned interaction has negligible incremental out-of-sample forecast skill over realized-volatility-only at the detectable effect scale; any true effect is smaller than the plausible-effect threshold (0.001 Brier) and hence undetectable here.

## Dominating limitation

Statistical power (sample size × effect size), not data availability. The panel and labels are complete and admissible (113,880 coin-hours, 13 coins, 12 months; `n_discrepancies=0`).

## Concrete falsifying test

Advance to RISK-11 (per ladder rule) only if `MDE <= plausible effect` via the MDE-by-instrument-count redesign or a larger/deeper panel; otherwise preserve the null. No outcome mining.

## Highest information-gain task

Campaign RISK-10 power restoration design complete. Next: ladder-rule handoff bump to RISK-11; no further RISK-10 work without a materially different route.

## Exact artifact and verification command

Exact artifact: `research_state/session_20261119T110653Z/fclr_risk10_evaluation_20261119T110653Z.json`

Verification command: `python3 scripts/check_handoff_heavywork_gate.py --json` (must PASS) and `python3 research_state/session_20261119T110653Z/fclr_risk10_evaluation_20261119T110653Z.py` (regenerates evaluation/power/recompute JSONs)

## Artifacts

- `fclr_risk10_prereg_20261119T110653Z.{json,md}` — outcome-blind contract incl. MDE-by-instrument-count + smallest-defensible-effect decision rule
- `fclr_risk10_power_20261119T110653Z.{py,json,md}` — block MDE audit + MDE-by-instrument-count table; status UNDERPOWERED
- `fclr_risk10_recompute_20261119T110653Z.{py,json}` — panel integrity, `n_discrepancies=0`
- `fclr_risk10_evaluation_20261119T110653Z.{py,json,md}` — 6-member family vs RV-only, placebo (1000 perms), Holm, MDE-by-instrument-count table, verdict UNDERPOWERED
- `evidence_audit_20261119T110653Z.{json,md}` — this audit
- `trigger_check_20261119T110653Z.json` — all 4 registry triggers re-evaluated
