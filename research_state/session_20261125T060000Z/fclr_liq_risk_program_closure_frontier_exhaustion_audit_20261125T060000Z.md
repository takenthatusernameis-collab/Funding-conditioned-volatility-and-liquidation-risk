# FCLR-LIQ-RISK-PROGRAM-CLOSURE-02 — Frontier Exhaustion Audit

**experiment_id:** FCLR-LIQ-RISK-PROGRAM-CLOSURE-02
**session_id:** session_20261125T060000Z
**session_utc:** 20261125T060000Z
**generated_utc:** 2026-11-25T06:00:00Z
**campaign_id:** FCLR-LIQ-RISK-PROGRAM-CLOSURE-02-20261125T054500Z
**audit_rule:** RESEARCH_PROMPT.md section 16 three-blocked-routes rule; two or more independent source families/methods

## Blocked routes

1. **Track A — observed liquidation labels:** STRUCTURALLY_BLOCKED. `ironflow` liquidations are a capped-sample feed (not a complete census); absence != zero liquidations; no complete observed-liquidation source available on frozen data; `NEW_OBSERVED_LIQUIDATION_SOURCE` cannot fire on frozen data.

2. **Track B — modeled hypothetical boundary-breach labels:** NOT_SUPPORTED. Modeled breach labels do not reconstruct account-specific liquidation mechanics, portfolio margin, liquidation engine execution, or actual forced liquidations; cannot serve as a confirmatory liquidation-risk outcome.

3. **Track C — volatility/stress outcomes from mark-price history:** NOT_SUPPORTED. All Half-2 arms below the frozen materiality floor; cross-sectional finding NOT_STABLE (section 17 condition #4).

4. **Half 1 — funding-conditioned volatility (all five estimands):** NOT_SUPPORTED (closed). Mean QLIKE 1.93%, correction-time, stress 1.51%, jump magnitude 0.0922%/0.1510%/0.3025%, jump direction/sign 0.0474% — all below the 2% floor.

## Source families tested
- `ironflow_bulk` parquet (`candles_1h`, `funding`, `open_interest`) — 18 months, sha256-asserted
- Closed campaign artifacts under `research_state/session_*/`

## Independent methods applied
- Walk-forward OLS/logit evaluation
- Cluster bootstrap + Driscoll-Kraay block inference
- Holm familywise-error correction
- Independent stdlib hash + sufficient-statistic recompute

## Conclusion

`no_feasible_confirmatory_design_remains: true`
The frontier is formally exhausted on admissible frozen data. Reopen requires a new observed-liquidation source (`NEW_OBSERVED_LIQUIDATION_SOURCE`, cannot fire on frozen data).
Honest endpoint: closure + negative-results preservation.
`audit_pass: true` | `unresolved_blockers: []`
