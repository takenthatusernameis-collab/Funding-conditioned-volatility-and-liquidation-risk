# FCLR-LIQ-RISK-PROGRAM-CLOSURE-02 — Evidence Audit (gate-critical alias)

**experiment_id:** FCLR-LIQ-RISK-PROGRAM-CLOSURE-02
**session_id:** session_20261125T060000Z
**session_utc:** 20261125T060000Z
**generated_utc:** 2026-11-25T06:00:00Z
**campaign_id:** FCLR-LIQ-RISK-PROGRAM-CLOSURE-02-20261125T054500Z
**audit_pass:** true

## Verdict

Program closed. All confirmatory verdicts NOT_SUPPORTED / NOT_STABLE / STRUCTURALLY_BLOCKED.

## Evidence inputs
- `research_state/data_cache/ironflow_bulk/{candles_1h,funding,open_interest}/` — 54 parquet files, sha256-asserted, read-only
- Closed campaign artifacts under `research_state/session_*/` (source registries, preregs, evals, recomputes, evidence audits)

## Summary

Gate-critical alias of the FCLR-LIQ-RISK-PROGRAM-CLOSURE-02 synthesis report. Half 1 (funding-conditioned volatility) closed NOT_SUPPORTED on all five estimands; Half 2 (liquidation risk) confirmatory-exhausted (Track A STRUCTURALLY_BLOCKED; Track B NOT_SUPPORTED; Track C NOT_SUPPORTED; cross-sectional SUPPORTED_GENERALIZATION but NOT_STABLE + materiality floor NOT MET). Frontier formally exhausted on frozen `ironflow_bulk` panel. No unresolved blockers.

`sha256_assertions: true` | `no_network: true` | `no_rerun_closed_arms: true` | `unresolved_blockers: []`
