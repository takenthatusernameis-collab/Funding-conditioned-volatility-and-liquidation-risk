# Evidence Audit — FCLR-XSEC-002 (session_20261120T210000Z)

**Campaign:** FCLR-XSEC-002-20261120T180707Z — UTC-hour / market-wide-RV conditioning of the funding effect.
**Estimand:** utc_hour_market_wide_rv_conditioning_rv1h (distinct from FCLR-STARTER-001 time-series 24h forward RV and FCLR-XSEC-001 pooled within-hour funding contrast; both NOT_SUPPORTED).
**Panel:** research_state/fclr011_recompute_panel_20261115T234700Z.parquet (sha256 41962f823e59de5989c7d854cb3180cad61a4cbc2f5f230133c41b321342c1f4, verified).
**Outcome data inspected before freeze:** false.

## Verdict
SUPPORTED. The regime-conditioned funding contrast is significant in the high market-wide-RV regime: CI [0.0046, 0.2348] excludes zero (p=0.019), materiality effect 1.09 >= 2% floor. The high-RV RV persistence baseline is also significant (CI [0.0489, 0.6187], p=0.0, Holm passes), serving as a specificity control. Gate: ci_supports_improvement=true, holm_passes_any=true, materiality_met_any=true, gate_passed=true.

## Artifacts on disk (all under research_state/session_20261120T210000Z/)
- fclr_xsec002_protocol_freeze_20261120T210000Z.{json,md}
- fclr_xsec002_baselines_20261120T210000Z.{py,json,md}
- fclr_xsec002_evaluation_20261120T210000Z.{py,json,md}
- trigger_check_20261120T210000Z.json
- recompute_fclr_xsec002_20261120T210000Z.{py,json} (independent reproducibility recompute; reproduces SUPPORTED)
- evidence_audit_20261120T210000Z.{json,md} (this audit)

## Specificity reading
The funding signal is concentrated in the high-RV regime; the pooled FCLR-XSEC-001 test was null (NOT_SUPPORTED), consistent with a regime-masked effect only visible after conditioning on market-wide RV.

## Constraints honored
- No root-level research_state/*.md or *.json added (root count stays 499/500).
- Sealed research_state/research_protocol.md not overwritten.
- FCLR-STARTER-001 and FCLR-XSEC-001 not re-run (terminal NOT_SUPPORTED).
- No network; no paid or credentialed data.
- No holdout outcomes inspected before protocol freeze.

## State synchronization required
- experiment_frontier.json: rank 0 FCLR-XSEC-002 -> COMPLETE, last_verdict SUPPORTED, session_20261120T210000Z; FCLR-XSEC-001 SUPERSEDED.
- hypothesis_registry.json: H_fclr_xsec_002 -> terminal SUPPORTED, last_experiment session_20261120T210000Z.
- AGENT_HANDOFF.md Section 1: next-session initial task message (see Section 1).

Generated: 2026-11-20T21:00:00Z
