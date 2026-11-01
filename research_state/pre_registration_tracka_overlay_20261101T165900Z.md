# Pre-registration: Track A Liquidation-Risk Overlay / Position-Sizing (FCLR-OVERLAY-001)
**TIMESTAMP (UTC):** 2026-11-01T16:59:00Z
**EXPERIMENT_ID:** FCLR-OVERLAY-001
**HYPOTHESIS_ID:** FCLR-H004 (Track A observed liquidations) + H_COUPLED-001 (coupled funding×vol×lagged observed flow)
**PRIORITY:** P0 — PRE-REGISTER BEFORE OUTCOME INSPECTION
**STATUS:** PRE-REGISTERED (not executed)

## Objective
Use the sealed FCLR-010 framework with the ROBUSTLY PASSED coupled model H_COUPLED-001 to evaluate a purely hypothetical liquidation-risk overlay / position-sizing approach on observed Hyperliquid liquidations. This is a hypothetical historical overlay only; no live/paper trading.

## Scope / Firewall
- **Data source:** ONLY ironflow Hyperliquid liquidation census (admissible per registry v1.2). 199 native perps, 12 monthly blocks 2025-11..2026-10.
- **Cross-track firewall:** IMMUTABLE. No Binance merge. Track B/C closed/blocked. Modeled ≠ observed.
- **Test window:** FROZEN from `research_state/run_manifest.json#split_boundaries_fclr010` (frozen_before_outcomes=true, frozen_at 2026-11-01T05:39:07Z). Test window 2026-05-28 .. 2026-10-31 SEALED.
- **Splits:** Use existing frozen splits only; no re-splitting, no threshold tuning on test.

## Inputs
- FCLR-010 base: logistic model for next-window observed liquidation events (per pre-registered protocol).
- H_COUPLED-001: coupled features (funding×vol regime×lagged observed flow). ROBUST PASS established: +4.61% rel Brier reduction, 95% CI [0.002511, 0.003158] excludes zero, >=2000 reps.
- Features computed only with information available at forecast time t; embargo/purge respected as in FCLR-010.

## Overlay Specification (PRE-REGISTERED)
We map predicted liquidation-risk p_t (from coupled model) to a hypothetical overlay decision rule, applied post-hoc on frozen test set only. All parameters fixed below BEFORE any overlay outcomes computed:

**Risk bands (fixed):**
- p_t in [0, p_low) → Risk Low: no de-risking / full hypothetical exposure (reference)
- p_t in [p_low, p_mid) → Risk Mid: hypothetical size multiplier s_mid (fixed)
- p_t in [p_mid, p_high) → Risk High: hypothetical size multiplier s_high (fixed)
- p_t >= p_high → Risk Very High: hypothetical size multiplier s_very_high (fixed, can be < 1)

**Fixed parameters (no tuning):**
- p_low = 0.33 quantile of in-sample calibration distribution from development period only (computed once from frozen dev set, stored before overlay eval)
- p_mid = 0.67 quantile (dev-only)
- p_high = 0.90 quantile (dev-only)
- s_mid = 0.8, s_high = 0.6, s_very_high = 0.4 (fixed multipliers; conservative de-risking)
- Exposure cap: max hypothetical exposure multiplier = 1.0; min = 0.0 (no leverage increase)
- No dynamic stop rules based on test-period outcomes

**Costs/assumptions (explicit):**
- Transaction/slippage costs: include conservative estimate (e.g. 5-10bps roundtrip) if computing PnL proxy; document assumption
- Funding costs/fees: note if modeled, else explicitly state omission and direction of bias
- Liquidation mechanics: overlay is hypothetical boundary/size adjustment only; does NOT reconstruct engine execution/cross-margin/account-specific effects
- Model != reality: PnL proxy is for risk-reduction assessment only, not profitability claim

## Primary Metrics (pre-registered)
1. **Calibration** by risk bucket (reliability diagram bins) — must remain acceptable
2. **Event capture / false alarm** in high-risk buckets (precision/recall) relative to baseline
3. **Hypothetical risk reduction proxy:** reduction in exposure-weighted event exposure in high-risk periods vs no-overlay baseline, with block-bootstrap CIs
4. **Turnover/stability:** frequency of band changes, max drawdown proxy if PnL computed
5. **Robustness:** by instrument concentration (leave-one-instrument-out), by time block, by regime

**Gates (must all pass to claim any benefit):**
- Calibration acceptable in all buckets (slope/intercept reasonable, no severe miscalibration)
- No leakage detected (frozen splits respected, features causal)
- Firewall intact (only ironflow, no cross-track merge)
- Block-bootstrap CIs computed; improvement not driven by single coin/block/crisis
- Multiplicity controlled if multiple overlay variants tested (Holm) — but only these fixed params specified
- Results reproducible from stored hashes

## Constraints
- **NO outcome inspection before pre-registration** — this document IS the pre-registration
- **NO threshold shopping** — parameters fixed above
- **NO tuning on test set** — dev-period quantiles only
- **NO relabeling** — observed liquidations only from ironflow
- **NO overlay code execution for outcome calculation in this session** — pre-registration only
- **NO .github/workflows changes**
- **NO fabricating metrics**

## Artifacts
- This pre-registration: `research_state/pre_registration_tracka_overlay_20261101T165900Z.md`
- Will produce (if executed later): `research_state/evaluation_summary_tracka_overlay_001.md`, updates to `experiment_frontier.json`, `cross_track_decision_log.md`, `run_manifest.json` if needed

## Verification
Next agent must verify this file exists with all sections above and confirms no outcome computation performed.
