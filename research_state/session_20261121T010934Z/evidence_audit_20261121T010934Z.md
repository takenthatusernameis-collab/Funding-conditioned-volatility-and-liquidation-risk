# Evidence Audit — FCLR-XSEC-006-20261121T010934Z

**Session UTC:** 20261121T010934Z
**Experiment ID:** FCLR-XSEC-006-20261121T010934Z

## 1. Panel Integrity
- **Panel:** `research_state/fclr_liq_combined_panel_20261115T181405Z.parquet`
- **SHA256:** `81a100d5d0625832bebabaabea13b786e15319577721cfe8507da5b779ec7f14`
- **Hash Verified:** ✅ PASS (asserted in evaluation and recompute scripts)
- **Rows:** 1,740,415 event-level rows
- **Coins:** 15 (AAVE, ADA, AVAX, BNB, BTC, CRV, DOGE, ETH, LINK, LTC, NEAR, SOL, SUI, UNI, XRP)
- **Time Span:** 2025-03-22T19:00:00Z .. 2026-10-31T22:00:00Z
- **Hourly Buckets:** 10,052 unique UTC hours
- **Features:** Zero-null on all causal features (rv24h, abs_fund_pct, notional_usd, etc.)

## 2. Protocol Freeze Precedes Outcomes
- **Protocol Freeze:** `research_state/session_20261121T010934Z/fclr_xsec006_protocol_freeze_20261121T010934Z.json/.md`
- **`outcome_data_inspected_before_freeze`:** `false` (explicitly recorded in freeze)
- **Freeze Timestamp:** 2026-11-21T01:09:34Z
- **Evaluation Execution:** After freeze, no holdout outcomes inspected before freeze.

## 3. Estimand Definition (Frozen Ex-Ante)
- **Regime Variable:** UTC trading-session bucket at hour t (Asian [00:00,08:00), European [08:00,16:00), US [16:00,24:00)) — assigned by clock hour, independent of RV
- **Predictor:** Within-(hour, session_bucket) cross-sectional rank of `abs_fund_pct`; high_funding = top 50%, low_funding = bottom 50%
- **Outcome (Primary):** Next-hour NOTIONAL-WEIGHTED observed liquidation intensity = sum of `notional_usd` in hour t+1 (dollar severity, NOT event count)
- **Outcome (Secondary, Cross-ref):** Next-hour event count (for comparison with FCLR-XSEC-004)
- **Baseline (Specificity Control):** Within-session-bucket RV persistence (coin's own `rv24h` at t, split high/low within (hour, bucket))
- **Inference:** Block bootstrap across whole UTC hours within each session bucket (seed 20261121, 2000 reps), Holm correction over 6-test family (3 buckets × {funding contrast, RV persistence}), 95% CIs, 2% materiality floor
- **Verdict Rule:** SUPPORTED only if at least one funding-contrast CI excludes zero AND Holm adj_p < 0.05 AND materiality effect ≥ 0.02; otherwise honest NOT_SUPPORTED

## 4. Evaluation Results
**File:** `research_state/session_20261121T010934Z/fclr_xsec006_evaluation_20261121T010934Z.json`

| Bucket | Test | n_hours | Mean Diff | 95% CI | p-value | Holm adj_p | CI Excl. Zero | Materiality | Floor Met |
|--------|------|---------|-----------|--------|---------|------------|---------------|-------------|-----------|
| Asian | Funding Contrast (NW) | 1692 | 339,191 | [162,051, 521,424] | 0.0 | 0.0 | ✅ | 0.361 | ✅ |
| European | Funding Contrast (NW) | 2080 | 561,032 | [334,550, 782,272] | 0.0 | 0.0 | ✅ | 0.570 | ✅ |
| US | Funding Contrast (NW) | 1868 | 404,512 | [94,750, 698,082] | 0.013 | 0.013 | ✅ | 0.262 | ✅ |
| Asian | RV Persistence (NW) | 1692 | -967,082 | [-1,198,717, -747,385] | 0.0 | 0.0 | ✅ | 1.029 | ✅ |
| European | RV Persistence (NW) | 2080 | -1,101,558 | [-1,322,094, -890,695] | 0.0 | 0.0 | ✅ | 1.120 | ✅ |
| US | RV Persistence (NW) | 1868 | -1,159,833 | [-1,602,454, -798,282] | 0.0 | 0.0 | ✅ | 0.750 | ✅ |

**Gate:** `ci_supports_improvement=true`, `holm_passes_any_funding=true`, `materiality_met_any_funding=true` → **gate_passed=true**
**Verdict:** **SUPPORTED**

## 5. Independent Recompute
**File:** `research_state/session_20261121T010934Z/fclr_xsec006_recompute_20261121T010934Z.json`
- **Code Path:** Separate implementation (Period-based hourly aggregation vs floor-based in evaluation)
- **Panel Hash Verified:** ✅ PASS
- **All Test Statistics:** Identical to evaluation (mean_diff, CI, p-values, materiality)
- **Verdict:** **SUPPORTED** (reproduces evaluation exactly)
- **`reproduces_fclr_xsec006_evaluation`:** `true`

## 6. Cross-Reference to Prior Campaigns
| Campaign | Regime | Outcome | Low-RV / Session Finding | High-RV Finding |
|----------|--------|---------|-------------------------|-----------------|
| FCLR-XSEC-004 | RV tercile | Count-based | **SUPPORTED** CI [448605, 841156], p=0.0, mat=0.80 | NOT_SUPPORTED (honest null) |
| FCLR-XSEC-005 | RV tercile | Notional-weighted | **SUPPORTED** CI [452973, 850199], p=0.0, mat=0.80 | NOT_SUPPORTED (honest null) |
| **FCLR-XSEC-006** | **UTC session bucket** | **Notional-weighted** | **SUPPORTED in ALL THREE buckets** (Asian/European/US) | N/A (no RV split) |

**Key Divergence:** FCLR-XSEC-004/005 found the funding effect ONLY in the low-RV tercile regime (high-RV was an honest null). FCLR-XSEC-006 finds the effect is **present across all three UTC trading sessions** (Asian, European, US) when regime is defined by clock-hour buckets instead of RV terciles. This suggests the liquidation funding signal is not confined to low-volatility periods but is a more general cross-sectional phenomenon that the RV-tercile split obscured by concentrating it in one regime.

## 7. Constraints Check
- ✅ No sealed protocol overwritten (`research_state/research_protocol.md` untouched)
- ✅ No root-level `.md`/`.json` files added (root count remains 499/500)
- ✅ No `.github/workflows` modifications
- ✅ No re-run of FCLR-STARTER-001, FCLR-XSEC-001, FCLR-XSEC-002, FCLR-XSEC-003, FCLR-XSEC-004, FCLR-XSEC-005
- ✅ No network, no paid/credentialed data, no new data acquisition
- ✅ Track separation maintained: observed liquidations (Track A) only, no modeled boundary breaches (Track B) or RV forecasts conflated

## 8. Acceptance Summary
| Check | Status |
|-------|--------|
| Panel hash verified | ✅ PASS |
| Protocol freeze precedes outcomes | ✅ PASS |
| Evaluation runs without error | ✅ PASS |
| Independent recompute reproduces | ✅ PASS |
| Verdict SUPPORTED with all gates | ✅ PASS |
| Cross-reference to XSEC-004/005 explicit | ✅ PASS |
| No sealed mutation | ✅ PASS |
| No root-level churn breach | ✅ PASS |
| Artifact triad complete (freeze, eval, recompute, evidence_audit, trigger_check) | ✅ PASS |

**Overall:** All evidence checks pass. FCLR-XSEC-006 is a valid, reproducible, heavy-work campaign with verdict **SUPPORTED**.