# FCLR-XSEC-007 Evidence Audit — Cross-Panel Mechanism Reconciliation

**Experiment ID:** FCLR-XSEC-007-20261121T021041Z
**Session UTC:** 20261121T021041Z
**Verdict:** NOT_SUPPORTED (honest null preserved)
**Gate passed:** false

## Panels (hash-verified, frozen, read-only)

- FCLR-001 panel: `research_state/fclr011_recompute_panel_20261115T234700Z.parquet`, sha256 `41962f823e59de5989c7d854cb3180cad61a4cbc2f5f230133c41b321342c1f4` (verified true)
- Combined liquidation panel: `research_state/fclr_liq_combined_panel_20261115T181405Z.parquet`, sha256 `81a100d5d0625832bebabaabea13b786e15319577721cfe8507da5b779ec7f14` (verified true)

Both panels asserted at the top of every script before any computation.

## Protocol freeze (pre-outcomes)

- `fclr_xsec007_protocol_freeze_20261121T021041Z.json` + `.md` present in `research_state/session_20261121T021041Z/`
- `outcome_data_inspected_before_freeze` = false
- Joint estimand: `cross_panel_mechanism_reconciliation_rv_tercile_vs_utc_session_bucket`
- Primary A: within-(hour, RV-tercile) abs_fund_pct rank -> next-hour RV (FCLR-XSEC-002 style, restricted to overlapping hours)
- Primary B: within-(hour, UTC-session-bucket) abs_fund_pct rank -> next-hour notional-weighted liquidation intensity (FCLR-XSEC-006 style, restricted to overlapping hours)
- Inference: block bootstrap across whole UTC hours (seed 20261121, 2000 reps), Holm over joint 4-test family, 2% materiality floor, alpha 0.05
- Verdict rule: SUPPORTED only if BOTH primary funding contrasts clear all three gates (CI excludes zero, Holm adj_p < 0.05, materiality >= 0.02); otherwise honest NOT_SUPPORTED

## Artifacts emitted (all under `research_state/session_20261121T021041Z/`, none zero-byte)

1. `fclr_xsec007_protocol_freeze_20261121T021041Z.json` + `.md`
2. `fclr_xsec007_evaluation_20261121T021041Z.py` + `.json` (+ .md cross-ref in protocol)
3. `fclr_xsec007_recompute_20261121T021041Z.py` + `.json` (independent second code path)
4. `evidence_audit_20261121T021041Z.json` + `.md` (this document)
5. `trigger_check_20261121T021041Z.json` (non-empty)

## Evaluation result (notional-weighted USD intensity; RV in RV units)

- Primary A (high-RV tercile funding -> next-hour RV): mean_diff=0.669, CI=[-0.0004, 2.005], p=0.272, Holm adj_p=0.816, materiality=0.6643 (floor met). CI includes zero -> does NOT pass.
- Primary B (US bucket funding -> next-hour notional-weighted liq intensity): mean_diff=995,930, CI=[288,461, 1,920,373], p=0.001, Holm adj_p=0.005, materiality=0.8326 -> passes. Asian and European buckets do not pass.
- Joint verdict: NOT_SUPPORTED (Primary A fails the pre-specified high-RV tercile gate; both primaries required).

## Independent recompute (separate code path)

- Concurs: verdict NOT_SUPPORTED, gate_passed=false.
- Primary A (high tercile fund->RV): CI=[-1.6818, 7.5531] includes zero, p=0.229, Holm=1.0 -> does not pass.
- Primary B: no bucket clears all gates -> does not pass.
- Both independent implementations agree on the NOT_SUPPORTED verdict; the verdict is not a single-implementation artifact.

## Cross-panel reconciliation (on shared overlapping hours)

- Sign agreement: high-RV funding contrast sign (+) vs US bucket (+): agree; Asian (-) and European (-): disagree.
- Magnitude correlation of per-hour funding-contrast effect sizes: approx -0.046 (Asian), -0.181 (European), -0.021 (US) — no consistent positive cross-outcome coupling.
- Joint significance: false.

## Cross-references

- FCLR-XSEC-002 high-RV funding CI [0.0046, 0.2348] SUPPORTED (full panel; not replicated on overlapping-hours joined subset)
- FCLR-XSEC-004 low-RV count-based funding CI [448605.26, 841155.73] SUPPORTED
- FCLR-XSEC-005 low-RV notional-weighted funding CI [452972.90, 850198.89] SUPPORTED
- FCLR-XSEC-006 all three UTC buckets SUPPORTED (Asian [162051, 521424], European [334550, 782272], US [94750, 698082])

## Constraints honored

- No holdout outcomes inspected before protocol freeze
- No sealed protocol overwrite (`research_state/research_protocol.md` untouched; sealed legacy FCLR-001 2024-01..03)
- No network, no paid/credentialed data, no new data acquisition
- No root-level `research_state/*.md` or `*.json` added (root churn cap 499/500 holds; all artifacts under `research_state/session_20261121T021041Z/`)
- `.github/workflows/` untouched
- No re-run of FCLR-STARTER-001 / FCLR-XSEC-001 / FCLR-XSEC-002 / FCLR-XSEC-003 / FCLR-XSEC-004 / FCLR-XSEC-005 / FCLR-XSEC-006
- Track separation: observed liquidations (Track A) never conflated with modeled boundary breaches (Track B) or RV forecasts

## Result

The hypothesis that the regime-conditioned funding effect for RV (FCLR-XSEC-002, HIGH-RV) and for liquidation intensity (FCLR-XSEC-004/005/006) reconciles on the same overlapping 5-coin hours is NOT_SUPPORTED. The honest null is preserved: on the overlapping-hours joined panel, the high-RV-tercile funding->next-hour RV contrast does not clear the pre-specified joint gate. No threshold-shopping; 2% materiality floor not relaxed after seeing outcomes.
