# FCLR-XSEC-008 Protocol Freeze — Alternative Regime Conditioning (RV168/RV24 voV terciles)

**Experiment ID:** FCLR-XSEC-008-20261121T054721Z
**Session UTC:** 20261121T054721Z
**Status:** PREREG_FREEZE (frozen BEFORE inspecting any outcome data)
**outcome_data_inspected_before_freeze:** false

## 1. Purpose (repository-name priority)

The repository is named *Funding-conditioned-volatility-and-liquidation-risk* — two scientific halves reconciled by one mechanism: (a) does the funding rate condition volatility (RV), and (b) does it condition liquidation risk? The completed cross-sectional (XSEC) program has shown:

- Funding -> next-hour RV is SUPPORTED only in the HIGH-RV regime (FCLR-XSEC-002, CI [0.0046, 0.2348], p=0.019).
- Funding -> next-hour liquidation intensity is SUPPORTED in the LOW-RV regime (FCLR-XSEC-004 count-based, FCLR-XSEC-005 notional-weighted) and across all three UTC session buckets (FCLR-XSEC-006).
- Cross-panel reconciliation under RV-tercile vs UTC-session conditioning is an honest null (FCLR-XSEC-007, NOT_SUPPORTED).

FCLR-XSEC-008 re-tests the SAME funding->RV and funding->liquidation mechanisms under a DIFFERENT regime variable — RV168/RV24 volatility-of-volatility (voV) ratio terciles — instead of RV tercile or UTC session bucket. If the funding effect is a genuine structural feature it must survive a regime re-split; if it only appears under RV-tercile it was a binning artifact. Either outcome is publishable and heavy. This is contingency-ladder step 1 (AGENT_HANDOFF.md §6); it is NOT a re-run of any terminal campaign.

## 2. Frozen panels (hash-verified, do NOT rebuild or substitute)

| Panel | Path | sha256 | Rows | Coins | Span |
|-------|------|--------|------|-------|------|
| FCLR-001 (RV + funding) | research_state/fclr011_recompute_panel_20261115T234700Z.parquet | 41962f823e59de5989c7d854cb3180cad61a4cbc2f5f230133c41b321342c1f4 | 29,136 | 5 (BTC, ETH, BNB, SOL, XRP) | 2026-01-01..2026-08-31 |
| Combined liquidation (observed liq + funding) | research_state/fclr_liq_combined_panel_20261115T181405Z.parquet | 81a100d5d0625832bebabaabea13b786e15319577721cfe8507da5b779ec7f14 | 1,740,415 | 15 | 2025-03-22 19:00 -> 2026-10-31 22:00 |

Both sha256 values are asserted at the top of the evaluation and recompute scripts and recorded here. Panels are frozen before target generation.

## 3. Alternative regime variable (ex-ante)

Variable: **rv168h / rv24h volatility-of-volatility ratio**, computed per coin-hour where both rv168h and rv24h are non-null. Market-wide ratio per hour = mean across coins with a valid ratio at that hour. Hours are terciled **ex-ante** into low / mid / high voV regimes.

Contingency (Primary B only, pre-approved, not threshold-shopping): if per-(hour, voV-tercile) coin cells are too thin, fall back to funding-rate-volatility terciles (rolling sd of abs_fund_pct) as the Primary B regime variable.

## 4. Estimands

**Primary A** (FCLR-XSEC-002 style, alt regime): within-(hour, voV-tercile) cross-sectional abs_funding_pct_trail rank -> next-hour RV (target_rv24h). Declared on the **HIGH voV tercile** (analogue of FCLR-XSEC-002 high-RV). Baseline: within-(hour, voV-tercile) RV persistence -> next-hour RV.

**Primary B** (FCLR-XSEC-006 style, alt regime): within-(hour, voV-tercile) cross-sectional abs_fund_pct rank -> next-hour NOTIONAL-WEIGHTED observed liquidation intensity (sum of notional_usd, dollar severity). Evaluated across all three voV terciles; passes if **any** tercile clears gates (analogue of FCLR-XSEC-006 any-bucket). Baseline: within-(hour, voV-tercile) RV persistence -> next-hour notional-weighted liquidation intensity.

## 5. Inference

- Block bootstrap across whole UTC hours within each voV-tercile regime family.
- Seed 20261121, >= 2000 deterministic replicates.
- Holm correction over the joint test family (family_size = 6).
- 2% materiality floor: |mean_diff| / mean_abs_outcome >= 0.02.
- alpha = 0.05; min 3 coins per hour for a cross-sectional rank.

## 6. Verdict rule

SUPPORTED only if BOTH primary funding contrasts clear all three gates (CI excludes zero, Holm adj_p < 0.05, materiality >= 0.02); otherwise preserve the honest null as NOT_SUPPORTED. Do not threshold-shop; do not relax the 2% floor after seeing outcomes.

## 7. Cross-panel reconciliation

On the overlapping coins, compare coefficient sign agreement and magnitude of the funding-rank effect between the next-hour RV outcome (Primary A) and the next-hour notional-weighted liquidation intensity outcome (Primary B) under the same voV-tercile conditioning.

## 8. Distinct from

FCLR-STARTER-001, FCLR-XSEC-001, FCLR-XSEC-002 (RV tercile), FCLR-XSEC-003, FCLR-XSEC-004 (count-based RV tercile), FCLR-XSEC-005 (notional-weighted RV tercile), FCLR-XSEC-006 (UTC session bucket), FCLR-XSEC-007 (terminal NOT_SUPPORTED), FCLR-LIQ-COMBINED-PANEL, FCLR-LIQ-XSEC-ORDERING, FCLR-LIQ-XSEC-QLIKE.

## 9. Constraints

- No holdout outcomes inspected before this freeze.
- No sealed protocol overwrite (research_state/research_protocol.md untouched).
- No network, no paid data, no new data acquisition.
- No root-level research_state/*.md or *.json (root churn cap 499/500); all artifacts under research_state/session_20261121T054721Z/.
- No re-run of FCLR-STARTER-001 / FCLR-XSEC-001..007 (all terminal).
- Track separation: observed liquidations only; no conflation with modeled boundary breaches (Track B) or RV forecasts.

## 10. Cross-reference to prior campaigns

- FCLR-XSEC-002 high-RV funding CI [0.0046, 0.2348], p=0.019 -> SUPPORTED
- FCLR-XSEC-004 low-RV count-based funding CI [448605.26, 841155.73], p=0.0 -> SUPPORTED
- FCLR-XSEC-005 low-RV notional-weighted funding CI [452972.90, 850198.89], p=0.0 -> SUPPORTED
- FCLR-XSEC-006 all three UTC buckets -> SUPPORTED
- FCLR-XSEC-007 NOT_SUPPORTED (honest null)

## 11. Required artifacts (this session)

research_state/session_20261121T054721Z/:
- fclr_xsec008_protocol_freeze_20261121T054721Z.json + .md (this freeze)
- fclr_xsec008_evaluation_20261121T054721Z.py + .json + .md
- fclr_xsec008_recompute_20261121T054721Z.py + .json (independent second code path)
- evidence_audit_20261121T054721Z.json + .md
- trigger_check_20261121T054721Z.json (non-empty, PASS/FAIL per check)

Acceptance: python3 scripts/check_handoff_heavywork_gate.py exits 0 AND python3 -m unittest tests.test_active_campaign_gate tests.test_tracka_hardening_125 -> 0 failures; no holdout outcomes inspected before freeze; zero-byte placeholders do NOT count.
