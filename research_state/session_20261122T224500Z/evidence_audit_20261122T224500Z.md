# FCLR-LIQ-RISK-ESCALATION-09 — Evidence Audit

**Experiment ID:** FCLR-LIQ-RISK-ESCALATION-09
**Campaign:** FCLR-LIQ-RISK-ESCALATION-09-20261122T193000Z
**Session UTC:** 20261122T224500Z

## Evidence type

Evidence/provenance audit of the Track A observed-liquidation-intensity campaign (FCLR-LIQ-RISK-ESCALATION-09), the first confirmatory use of the on-disk ironflow bulk observed-liquidation stream to test whether funding-conditioned features predict observed liquidation intensity.

## Inputs verified

| Item | Status |
|------|--------|
| Prereg present (frozen before outcomes) | true |
| Prereg outcome_data_inspected_before_freeze | false |
| Power result present | true |
| Recompute result present | true |
| Evaluation result present | true |
| Trigger check present | true |

## Provenance

| Item | Value |
|------|-------|
| Data source | research_state/data_cache/ironflow_bulk/{candles_1h,funding,open_interest,liquidations}, 18 months 2025-05..2026-10 |
| SHA-256 asserted before every read | true |
| SHA-256 files checked | 72 |
| SHA-256 files matched | 72 |
| SHA-256 files mismatched | 0 |
| Caches never mutated | true |
| No network | true |
| No new source | true |
| Software | stdlib + pyarrow only; numpy/pandas/scipy not used |
| Track | Track A (observed on-chain liquidations), NOT Track B modeled breach proxy |

## Design fidelity

| Remediation | Applied | Matches prereg |
|-------------|---------|----------------|
| d2 48h purge+embargo | true | true |
| d10 non-overlapping 168h forward blocks | true | true |
| d6 delisting-aware identity | true | true |
| d7 survivors-vs-exited arm | true | true |
| Outcome-blind prereg frozen before outcomes | true | true |
| Materiality floor frozen (2%) | true | true |
| Holm family declared | 4 contrasts | true |
| Alpha-spending k=2 | 0.008333 | true |

## Recompute agreement

| Item | Value |
|------|-------|
| Independent recompute pass | true |
| QLIKE B1 agree within tolerance | true |
| QLIKE C2 agree within tolerance | true |
| N test rows agree | true |
| Tolerance (rel) | 1e-06 |

## Decision integrity

| Item | Value |
|------|-------|
| Materiality floor | 2.0% |
| Materiality met | false |
| Holm primary adjusted p | 1.000000 |
| Alpha_k (k=2) | 0.008333 |
| Primary significant after Holm | false |
| Decision | NOT_SUPPORTED |
| Null preserved honestly | true |
| No threshold shopping | true |
| No relaxed materiality floor | true |
| No overlay built | true |

## Verdict

FCLR-LIQ-RISK-ESCALATION-09 Track A observed-liquidation-intensity evaluation executed under a leakage-hardened design (48h purge+embargo, non-overlapping 168h forward blocks, delisting-aware identity, survivors-vs-exited arm, per-coin block bootstrap, Holm, alpha-spending k=2). The funding-conditioned candidate adds no incremental skill over the RV-only baseline for observed liquidation intensity; verdict NOT_SUPPORTED. Null preserved honestly; never claim a complete observed-liquidation census from a capped feed. No risk overlay built (RESEARCH_PROMPT.md section 9).

## Evidence paths

All artifacts under `research_state/session_20261122T224500Z/`:
- fclr_risk09_prereg_20261122T224500Z.json + .md
- fclr_risk09_power_20261122T224500Z.py + .json + .md
- fclr_risk09_recompute_20261122T224500Z.py + .json
- fclr_risk09_evaluation_20261122T224500Z.py + .json + .md
- evidence_audit_20261122T224500Z.json + .md
- trigger_check_20261122T224500Z.json
