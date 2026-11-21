# FCLR-XSEC-008 Evaluation — Alternative Regime Conditioning (RV168/RV24 voV terciles)

**Experiment ID:** FCLR-XSEC-008-20261121T054721Z
**Session UTC:** 20261121T054721Z
**Phase:** EVALUATION_AND_GATE (COMPLETE)
**outcome_data_inspected_before_freeze:** false (protocol frozen first)

## 1. Result summary (verdict first)

**Joint verdict: NOT_SUPPORTED** (gate_passed = False).

The joint gate requires BOTH primary funding contrasts to clear all three gates (CI excludes zero, Holm adj_p < 0.05, materiality >= 0.02). Primary A clears; Primary B does not. Therefore the joint claim — that the regime-conditioned funding effect replicates under RV168/RV24 volatility-of-volatility terciles for BOTH next-hour RV and next-hour notional-weighted liquidation intensity — is NOT_SUPPORTED. This is an honest, pre-registered null on the joint claim; the 2% materiality floor was not relaxed after seeing outcomes.

## 2. Panels (hash-verified)

| Panel | Path | sha256 |
|-------|------|--------|
| FCLR-001 (RV + funding) | research_state/fclr011_recompute_panel_20261115T234700Z.parquet | 41962f823e59de5989c7d854cb3180cad61a4cbc2f5f230133c41b321342c1f4 |
| Combined liquidation (observed liq + funding) | research_state/fclr_liq_combined_panel_20261115T181405Z.parquet | 81a100d5d0625832bebabaabea13b786e15319577721cfe8507da5b779ec7f14 |

Both sha256 values asserted in the script and verified against disk. No panel rebuild, no new data, no network.

## 3. Alternative regime variable

**RV168/RV24 volatility-of-volatility ratio** = rv168h / rv24h per coin-hour (where both non-null); market-wide ratio per hour = mean across the 5 overlapping coins with a valid ratio; hours terciled ex-ante into low / mid / high voV regimes.

- Eval-eligible coin-hours: 3,338 (unique shared hours: 890)
- Hours per voV tercile: low=298, mid=293, high=299 (well-populated; >= 3 coins per hour satisfied)
- voV ratio coverage on FCLR-001: ~61% of rows (rv168h non-null), consistent with handoff de-risk; ample after hourly market-wide aggregation.

## 4. Primary A — within-(hour, voV-tercile) funding rank -> next-hour RV (FCLR-XSEC-002 style)

Declared on the HIGH voV tercile (analogue of FCLR-XSEC-002 high-RV). Predictor: cross-sectional abs_funding_pct_trail rank (high vs low funding within hour). Outcome: next-hour RV (target_rv24h shift -1).

| Metric | Value |
|--------|-------|
| n_hours | 299 |
| mean_diff (high - low funding) | -0.000110 |
| 95% CI (block bootstrap, seed 20261121, 2000 reps) | [-0.000160, -0.000060] |
| p_value | 0.000 |
| Holm adj_p (joint family) | 0.000 |
| CI excludes zero | True |
| Holm passes | True |
| Materiality effect | 0.145 (floor 0.02 met) |
| Positive diffs | 108 / 299 |

**Primary A: PASSES all three gates.** The funding->RV effect replicates under voV conditioning, with the HIGH-voV tercile contrast statistically significant and material. Notably the sign is NEGATIVE (high funding -> lower next-hour RV), a sign reversal versus FCLR-XSEC-002's positive high-RV contrast (CI [0.0046, 0.2348]); this sign flip is reported honestly and does not affect the gate (which requires CI excludes zero, not a directed sign).

Baseline (RV persistence) also passes in high tercile: CI [0.000339, 0.000431], materiality 0.50 — specificity control consistent.

## 5. Primary B — within-(hour, voV-tercile) funding rank -> next-hour notional-weighted liquidation intensity (FCLR-XSEC-006 style)

Evaluated across all three voV terciles; pass rule = any tercile clears gates (analogue of FCLR-XSEC-006 any-bucket). Predictor: cross-sectional abs_fund_pct rank. Outcome: next-hour notional-weighted observed liquidation intensity (sum of notional_usd, dollar severity).

| Tercile | n_hours | mean_diff | 95% CI | p_value | Holm adj_p | CI excl. 0 | Holm | Materiality | Pass? |
|---------|---------|-----------|--------|---------|------------|------------|------|-------------|-------|
| low | 298 | -262,137 | [-2,080,750, 1,169,420] | 0.857 | 0.857 | False | False | 0.127 (met) | No |
| mid | 293 | 223,066 | [-281,197, 736,665] | 0.401 | 0.802 | False | False | 0.193 (met) | No |
| high | 299 | 248,642 | [-56,259, 502,704] | 0.099 | 0.297 | False | False | 0.352 (met) | No |

**Primary B: FAILS all three terciles.** None clears the CI-excludes-zero gate (Holm adj_p ranges 0.297–0.857). The funding->notional-weighted-liquidation-intensity effect does NOT replicate under voV conditioning. This contrasts with FCLR-XSEC-004/005 (low-RV tercile, SUPPORTED) and FCLR-XSEC-006 (all UTC buckets, SUPPORTED), indicating the liquidation-intensity funding effect is specific to the RV-tercile/UTC-session conditioning and does not survive re-splitting by voV.

Baseline (RV persistence) passes in mid/high terciles — specificity control consistent; the failure is specific to the funding contrast, not a power problem.

## 6. Cross-panel reconciliation

| Check | Result |
|-------|--------|
| Shared hours | 890 |
| Primary A passed | True |
| Primary B passed | False |
| Joint significance | False |
| Sign agreement (high-voV RV sign vs each tercile liq sign) | low: agree; mid: disagree; high: disagree |
| Effect-size magnitude correlation (high-voV RV vs each tercile liq) | high tercile: -0.250; low/mid: no shared hours (None) |

No coherent cross-panel sign agreement; consistent with the joint null.

## 7. Inference

- Block bootstrap across whole UTC hours within each voV-tercile regime family (seed 20261121, >= 2000 deterministic replicates).
- Holm correction over the joint 6-test family (3 terciles x funding contrast, reported; baselines included in family).
- 2% materiality floor (|mean_diff| / mean_abs_outcome >= 0.02).
- alpha = 0.05; min 3 coins per hour for a cross-sectional rank.

## 8. Cross-reference to prior campaigns

- FCLR-XSEC-002 high-RV funding CI [0.0046, 0.2348], p=0.019, materiality 1.09 -> SUPPORTED (RV tercile)
- FCLR-XSEC-004 low-RV count-based funding CI [448605.26, 841155.73], p=0.0, materiality 0.80 -> SUPPORTED (RV tercile)
- FCLR-XSEC-005 low-RV notional-weighted funding CI [452972.90, 850198.89], p=0.0, materiality 0.80 -> SUPPORTED (RV tercile)
- FCLR-XSEC-006 all three UTC buckets -> SUPPORTED (UTC session bucket)
- FCLR-XSEC-007 cross-panel RV tercile vs UTC bucket -> NOT_SUPPORTED (honest null)
- FCLR-XSEC-008 voV ratio terciles -> Primary A passes (RV), Primary B fails (liq intensity) -> Joint NOT_SUPPORTED

## 9. Distinct from

FCLR-STARTER-001, FCLR-XSEC-001, FCLR-XSEC-002 (RV tercile), FCLR-XSEC-003, FCLR-XSEC-004 (count-based RV tercile), FCLR-XSEC-005 (notional-weighted RV tercile), FCLR-XSEC-006 (UTC session bucket), FCLR-XSEC-007 (terminal NOT_SUPPORTED), FCLR-LIQ-COMBINED-PANEL, FCLR-LIQ-XSEC-ORDERING, FCLR-LIQ-XSEC-QLIKE. Not a re-run of any terminal campaign.

## 10. Constraints honored

- No holdout outcomes inspected before protocol freeze (outcome_data_inspected_before_freeze=false).
- No sealed protocol overwrite (research_state/research_protocol.md untouched).
- No network, no paid data, no new data acquisition.
- No root-level research_state/*.md or *.json (root churn cap 499/500); all artifacts under research_state/session_20261121T054721Z/.
- No re-run of FCLR-STARTER-001 / FCLR-XSEC-001..007 (all terminal).
- Track separation: observed liquidations only; no conflation with modeled boundary breaches (Track B) or RV forecasts.

## 11. Artifacts (this session)

- fclr_xsec008_protocol_freeze_20261121T054721Z.json + .md
- fclr_xsec008_evaluation_20261121T054721Z.py + .json + .md (this document)
- fclr_xsec008_recompute_20261121T054721Z.py + .json (independent second code path)
- evidence_audit_20261121T054721Z.json + .md
- trigger_check_20261121T054721Z.json (non-empty, PASS/FAIL per check)

Acceptance: python3 scripts/check_handoff_heavywork_gate.py exits 0 AND python3 -m unittest tests.test_active_campaign_gate tests.test_tracka_hardening_125 -> 0 failures; zero-byte placeholders do NOT count.
