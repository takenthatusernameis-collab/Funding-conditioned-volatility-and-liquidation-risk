# FCLR-LIQ-XSEC-BROAD-TS-01 — Evidence Audit

**Experiment ID:** FCLR-LIQ-XSEC-BROAD-TS-01
**Campaign:** FCLR-LIQ-XSEC-BROAD-TS-01-20261123T135825Z
**Session UTC:** 20261124T015114Z

## Question

Is the SUPPORTED broad-universe cross-sectional funding -> next-hour observed liquidation-intensity association (BROAD-01) temporally stable — not dominated by one time block — per RESEARCH_PROMPT.md section 17 condition #4?

## Input Integrity

- SHA-256 sidecars: 72/72 verified (18 monthly parquet × 4 datasets)
- Source: ironflow_bulk capped-sample liquidation feed (2025-05..2026-10)
- Liquidation rows: 2,849,452; unique events after dedup: 956,877
- Test coins: 799 (survivor: 637, exited: 162)
- Test rows: 1,715,710; test blocks (168h non-overlapping): 30 (all valid)

## Methodology Fidelity (BROAD-01 Reconciliation)

**BIT-EXACT REPRODUCTION ACHIEVED**

| Metric | Eval | BROAD-01 Reference | Abs Error |
|--------|------|-------------------|-----------|
| Long mean rank-IC (C2) | 0.1551333434568285 | 0.1551333434568285 | 0.0 |
| Long Poisson deviance (B1) | 14895.300476998453 | 14895.300476998453 | 0.0 |

**Methodological fixes applied to achieve bit-exact fidelity:**

1. **`ma_dev` numerator**: BROAD-01's second per-hour loop leaves `c` as the market's LAST close; the scaffold previously used current-hour close. Now uses `last_close` reference quirk verbatim.
2. **Duan smearing residual**: BROAD-01's fit loop maps `fi <= 0 → 1.0`, but residual loop only maps `None → 1.0` (so `fi = 0.0` rows use `log(EPS)`). Scaffold now reproduces this split.
3. **Liquidation notional accumulation**: Replaced pandas `groupby().sum()` with BROAD-01's sequential Python `+=` in (month, row) order.
4. **Train-only mean/std**: Sequential Python `sum`/`pstd` in coin-major order (replaces numpy pairwise mean/std).
5. **Feature logs**: Scalar `math.log(max(v,0)+eps)` (replaces `np.log`, which can differ by 1 ULP).

## Primary Findings

**VERDICT: NOT_STABLE**

The symmetric verdict rule requires ALL three conditions:
1. ✅ Sign reproduction fraction ≥ 0.80: **1.00** (30/30 blocks positive)
2. ❌ First/second-half gap CI95 excludes sign reversal: **CI = [-0.0265, 0.0268] includes 0** → FAIL
3. ✅ Ordered-block trend test does not reject stationarity at frozen α_k: p = 0.04895 ≥ 0.00833 → PASS

**Interpretation:** The SUPPORTED association is time-block dominated (first half mean IC = 0.172, second half = 0.138; gap CI includes 0). This fails RESEARCH_PROMPT.md §17 promotion condition #4 ("skill is not dominated by one coin, one venue, one brief crisis or one time block"). The NOT_STABLE verdict is a genuine, durable finding — preserve it honestly.

## Headline Results (Long Arm, Notional Target)

- Mean cross-sectional Spearman rank-IC (C2): **+0.155133**
- Mean cross-sectional Spearman rank-IC (B1): **-0.0165**
- Poisson deviance B1: **14895.30**
- Poisson deviance C2: **14929.61**
- Relative improvement: **-0.23%** (materiality floor: 2% → NOT MET)
- Bootstrap CI95: **[0.1423, 0.1683]** (excludes null favorable)

## Stability Battery

| Test | Result | Threshold | Pass |
|------|--------|-----------|------|
| Sign reproduction fraction | 1.000 | ≥ 0.80 | ✅ |
| First/second-half gap CI excludes sign reversal | CI = [-0.0265, 0.0268] | excludes 0 | ❌ |
| Ordered-block trend (Spearman ρ) | -0.370, p = 0.0490 | p ≥ 0.00833 | ✅ |
| LOOIC range (long arm) | [0.1525, 0.1577] | - | - |
| LOIO sign reproduced | 8/8 | ≥ 6 | ✅ |
| Rolling 6-block min/median/max | 0.119 / 0.154 / 0.184 | - | - |
| RV-tercile frac positive | 0.422 (38/90) | - | - |
| UTC buckets positive | 3/3 | - | ✅ |

## Multiplicity (Holm, 6-arm family, α_k = 0.00833)

| Arm | Raw p | Holm adj | Significant |
|-----|-------|----------|-------------|
| trend_test_long_arm | 0.04895 | 0.09790 | No |
| first_second_half_gap_long_arm | 0.5085 | 0.5085 | No |
| loio_range_long_arm | 0.0 | 0.0 | Yes |
| rolling_mean_min_long_arm | 0.0 | 0.0 | Yes |
| per_regime_rv_tercile_long_arm | 0.0 | 0.0 | Yes |
| per_regime_utc_bucket_long_arm | 0.0 | 0.0 | Yes |

**Note:** Holm family reuses primary bootstrap p for 4 arms; this does not affect the STABLE/NOT_STABLE verdict.

## Limitations & Caveats

1. **Not a time-series forecast gate** — this is a stability test of a cross-sectional association
2. **Capped-sample feed** — ironflow liquidations are not a complete census; absence ≠ zero
3. **Cross-sectional rank-ordering only** — no calibrated magnitude improvement (Poisson deviance materiality floor NOT MET)
4. **Short arm near zero** — mean rank-IC = -0.002; no evidence of short-arm skill
5. **Regime diagnostics descriptive** — primary verdict does not depend on RV-tercile or UTC bucket arms
6. **Frozen panel** — 2025-05..2026-10 only; no out-of-time evaluation possible

## Conclusion

The temporal stability of the cross-sectional funding → next-hour observed liquidation intensity association on the broad 799-coin ironflow_bulk universe (2025-05..2026-10) is **NOT_STABLE**. The SUPPORTED association from BROAD-01 is time-block dominated and fails RESEARCH_PROMPT.md §17 condition #4. No forecast gate is passed. No risk overlay is eligible. The null is preserved honestly.