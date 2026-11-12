# Track A Expansion Robustness/Falsification — TRACKA-EXP-ROBUST-20261112T014744Z
**Timestamp (UTC):** 2026-11-12T01:48:38Z
**Experiment:** TRACKA-EXP-ROBUST-20261112T014515Z (prereg frozen pre-outcomes)
**Prereg Document:** tracka_prereg_expansion_robust_20261112T014515Z.json
**Verdict:** `FRAGILE` — Robustness/falsification of sealed PASS TRACKA-HL-EXPANSION-20261111T195500Z
**Panel:** tracka_hl_expansion_panel_20261111T202344Z.parquet (sha256 39916a72dfc37d15...)

## Original Sealed PASS (Reference)
- Rel QLIKE reduction (C2 vs B1): 19.04%
- 95% CI: [-5.088, -0.478]
- Paired n: 593, Test blocks: 3, Instruments: 8

## Check 1: LOIO (Leave-One-Instrument-Out) Sensitivity
- **Result:** FAIL (0/8 passed, need >= 6)

- ZEC: rel=2.66% (mat:✓), CI=[-3.564368,2.976733] (ci:✗)
- NEAR: rel=-30.12% (mat:✗), CI=[-0.468691,19.993543] (ci:✗)
- UNI: rel=-15.30% (mat:✗), CI=[-1.643223,10.354457] (ci:✗)
- AAVE: rel=-19.97% (mat:✗), CI=[-0.867382,12.969754] (ci:✗)
- CRV: rel=-32.98% (mat:✗), CI=[-0.378228,14.970899] (ci:✗)
- ADA: rel=-34.37% (mat:✗), CI=[-0.709533,15.651113] (ci:✗)
- LTC: rel=-11.21% (mat:✗), CI=[-2.891786,9.836619] (ci:✗)
- BCH: rel=-35.15% (mat:✗), CI=[-0.583192,16.132531] (ci:✗)

## Check 2: Placebo/Permutation on Funding Features
- **Result:** FAIL
- True rel reduction: -24.39%
- Null distribution: n=1000, 95th pctl=0.4490%
- Approx p-value: 0.8180

## Check 3: Alternative Block/Bootstrap Settings
- **Result:** FAIL
- Setting a: rel=-24.39% (mat:✗), CI=[-0.672102,13.202670] (ci:✗)
- Setting b: rel=-24.39% (mat:✗), CI=[-1.229090,13.269653] (ci:✗)
- Setting c: rel=-24.39% (mat:✗), CI=[-0.672102,13.202670] (ci:✗)

## Overall Verdict
**FRAGILE**
At least one check failed. Exact failure modes documented above.

## Compliance
- Prereg frozen pre-outcomes: PASS
- No threshold-shopping: PASS
- No sealed-holdout reuse: PASS
- Hyperliquid only, observed ironflow labels: PASS
- Bounded compute (fixed seeds, pre-specified reps): PASS
- No agent-set RESOLVED_VERIFIED/fabricated=true: PASS

---
**End of verdict.** Verdict ID: TRACKA-EXP-ROBUST-20261112T014744Z
