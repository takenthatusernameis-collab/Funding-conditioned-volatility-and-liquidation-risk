# Terminal Structural Stop — `liq` (TRACKA-HL-EARLY4H-2025H1-LIQ-GLM-ROBUST)

**Timestamp (UTC):** 2026-11-12T17:04:57Z
**Experiment ID:** TRACKA-HL-EARLY4H-2025H1-LIQ-GLM-ROBUST
**Campaign:** FCLR-EARLY4H-2025H1-LIQ-GLM-ROBUST v1
**Prereg:** research_state/tracka_prereg_early2025h1_liq_glm_robust_20261112T165234Z.json (sha256 f06060c7…)
**Panel:** research_state/tracka_hl_early2025h1_panel_20261112T145529Z.parquet (sha256 08c60803…)
**Evaluator:** scripts/early4h_liq_glm_robust.py

---

## Verdict

**NOT_MET** — The bounded-feature Poisson/quasi-Poisson GLM (log link, IRLS) is numerically stable but does **not** pass the forecast gate on the primary contrast `C2_vs_B1` (funding + premium features vs. RV-only baseline) for observed liquidation intensity.

---

## Evidence Summary

| Model | Mean QLIKE | Converged | Iters | Max row QLIKE |
|---|---|---|---|---|
| B1 (RV-only) | 4.15 | true | 7 | 212.8 |
| C1 (+ funding) | 4.19 | true | 9 | 243.4 |
| C2 (+ funding + premium) | 4.05 | true | 7 | 319.1 |

**Numerical stability:** All max row QLIKE ≤ 319 ≪ 1e6 threshold. The bounded-feature transformation (clip to train [min, max], standardize by train mean/std) **successfully eliminated** the extrapolation instability that caused the parent campaign's `INCONCLUSIVE_NUMERICAL_INSTABILITY` (where C2 max row QLIKE reached 3.5e9).

---

## Gate Assessment (primary contrast `C2_vs_B1`)

| Criterion | Required | Observed | Pass |
|---|---|---|---|
| Materiality ≥ 2% rel QLIKE reduction | ≥ 2% | **+2.42%** | ✅ |
| 95% CI upper bound < 0 | < 0 | **+0.85** | ❌ |
| Min test blocks ≥ 3 | ≥ 3 | **4** | ✅ |
| Min paired instruments ≥ 5 | ≥ 5 | **9** | ✅ |
| Holm rejection (FWER 0.05) | true | **false** | ❌ |
| Not single-coin driven | false | **false** | ✅ |

**Gate result:** FAILS (CI upper > 0; Holm not rejected)

- Mean diff: **−0.100** (negative favors C2)
- 95% CI: **[−1.23, +0.85]** (includes 0, upper > 0)
- Rel reduction: **+2.42%**
- p-value: **0.85** (approx., from bootstrap CI)
- Holm: **not rejected**

---

## Per-Coin / Per-Block Breakdown (C2 − B1 mean QLIKE diff)

| Coin | Mean diff |
|---|---|
| AVAX | +0.733 |
| BNB | +0.578 |
| BTC | +0.931 |
| DOGE | −0.149 |
| ETH | **−2.969** |
| LINK | +0.335 |
| SOL | −0.312 |
| SUI | +0.187 |
| XRP | +0.036 |

| Block | Period | Mean diff |
|---|---|---|
| 0 | 2025-07-01 .. 2025-07-30 | −0.043 |
| 1 | 2025-07-31 .. 2025-08-29 | **−1.697** |
| 2 | 2025-08-30 .. 2025-09-28 | +0.188 |
| 3 | 2025-09-29 .. 2025-10-28 | **+1.132** |

- Block 3 (Oct-2025 funding spike) shows **positive diff** (C2 worse than B1), consistent with the original extrapolation concern.
- Block 1 shows the strongest negative diff (C2 better).
- No single coin dominates; BTC+ETH ≈ 63.6% of events / 83.6% of notional.

---

## Structural Assessment

**The `liq` hypothesis (funding/premium features improve observed liquidation intensity forecasts over RV-only) is NOT SUPPORTED by the admissible data and the frozen protocol.**

- The parent `INCONCLUSIVE_NUMERICAL_INSTABILITY` was a **bounded-feature problem**, not a sample-size or label problem. The robust estimator fixed it.
- The fixed estimator yields a **stable, interpretable null**: mean QLIKE reduction of 2.4% but with wide uncertainty (CI [−1.23, +0.85]) that includes 0 and fails both the CI and Holm gates.
- **Label ceiling is hard:** Ironflow observed liquidation labels exist only 2025-05-25 .. 2026-10-31. No labels before 2025-05-25 exist. The 2024-08..2025-04 period is structurally unavailable for observed-label tests.
- **Concentration is documented:** BTC+ETH ≈ 63.6% events / 83.6% notional. Per-coin reporting is satisfied; no single coin drives the result.
- **Power is adequate:** 246–261 positive-label days per test block (1,016 total paired test rows across 4 blocks, 9 instruments).
- **No unresolved leakage, source, timestamp, or pipeline defects** in this campaign.

---

## Why No Further Estimator Iteration on This Source/Design

Per `RESEARCH_PROMPT.md` §16 (adaptive feasibility) and the frozen prereg's `numerical_stability.verdict_on_exceed`:

> "If this fires again, emit a timestamped evidenced structural-blocker document with the exact failing minima and stop; do not iterate estimator forms without a materially new source or a new preregistered design."

The robust estimator **did not** fire the instability clause — it is numerically clean. The gate fails on **statistical evidence**, not numerical pathology. The protocol was frozen before outcomes; the test was executed as registered; the result is a valid null.

Further estimator-form iteration (e.g., different link, regularization, feature interactions, survival models) on the **same panel, same splits, same labels, same target** would constitute threshold-shopping / post-hoc model search, which the protocol forbids. The confirmatory track for `liq` on this source/design is **closed**.

---

## Next Admissible Path (if any)

Per `RESEARCH_PROMPT.md` §16, a new campaign requires **a genuinely new admissible source** (Track A observed labels with earlier coverage, or a different venue with independent liquidation records) **or** a **new preregistered design** with a materially different estimand (e.g., Track B modeled boundary breaches, Track C volatility stress outcomes — both already covered by other tracks/experiments).

No such source is currently available without payment, credentials, or manual intervention. The Ironflow/Hyperliquid observed-label source is exhausted for the 2025H1 window.

---

## Artifacts Produced

- `scripts/early4h_liq_glm_robust.py` — bounded-feature GLM implementation
- `research_state/evaluation_summary_EARLY4H-2025H1-LIQ-GLM-ROBUST-20261112T170457Z.json` — full machine-readable result
- `research_state/evaluation_summary_EARLY4H-2025H1-LIQ-GLM-ROBUST-20261112T170457Z.md` — human-readable report

---

## Compliance

- No outcome inspection before prereg freeze ✅
- No threshold-shopping ✅
- No sealed holdout reuse ✅
- No Binance/2024 conflation with Hyperliquid windows ✅
- No modeled/proxy labels presented as observed ✅
- Venue consistent: Hyperliquid-only ✅
- Raw data/caches not committed ✅