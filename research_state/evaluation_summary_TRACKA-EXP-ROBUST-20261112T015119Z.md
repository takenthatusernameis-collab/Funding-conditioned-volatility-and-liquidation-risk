# Track A Expansion Robustness/Falsification — TRACKA-EXP-ROBUST-20261112T015119Z
**Timestamp (UTC):** 2026-11-12T01:52:17Z
**Experiment:** TRACKA-EXP-ROBUST-20261112T014515Z (prereg frozen pre-outcomes)
**Prereg Document:** tracka_prereg_expansion_robust_20261112T014515Z.json
**Verdict:** `FRAGILE` — Robustness/falsification of sealed PASS TRACKA-HL-EXPANSION-20261111T195500Z
**Panel:** tracka_hl_expansion_panel_20261111T202344Z.parquet (sha256 39916a72dfc37d15...)

## Original Sealed PASS (Reference)
- Rel QLIKE reduction (C2 vs B1): 19.04%
- 95% CI: [-5.088, -0.478]
- Paired n: 593, Test blocks: 3, Instruments: 8

## Check 1: LOIO (Leave-One-Instrument-Out) Sensitivity
- **Result:** FAIL (4/8 passed, need >= 6)

- ZEC: rel=9.67% (mat:PASS), CI=[-2.649513,0.682221] (ci:FAIL)
- NEAR: rel=24.36% (mat:PASS), CI=[-7.132405,0.000058] (ci:FAIL)
- UNI: rel=3.12% (mat:PASS), CI=[-1.921964,0.752544] (ci:FAIL)
- AAVE: rel=18.78% (mat:PASS), CI=[-5.788025,-1.096023] (ci:PASS)
- CRV: rel=19.37% (mat:PASS), CI=[-5.094251,-0.390990] (ci:PASS)
- ADA: rel=17.58% (mat:PASS), CI=[-4.410308,-0.595051] (ci:PASS)
- LTC: rel=29.71% (mat:PASS), CI=[-8.787484,-2.417754] (ci:PASS)
- BCH: rel=10.39% (mat:PASS), CI=[-6.222642,3.370433] (ci:FAIL)

## Check 2: Placebo/Permutation on Funding Features
- **Result:** FAIL
- True rel reduction: 19.04%
- Null distribution: n=1000, 95th pctl=21.1022%
- Approx p-value: 0.1420

## Check 3: Alternative Block/Bootstrap Settings
- **Result:** PASS
- Setting a: rel=19.04% (mat:PASS), CI=[-5.088102,-0.477660] (ci:PASS)
- Setting b: rel=19.04% (mat:PASS), CI=[-4.556723,-1.017593] (ci:PASS)
- Setting c: rel=19.04% (mat:PASS), CI=[-5.088102,-0.477660] (ci:PASS)

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
**End of verdict.** Verdict ID: TRACKA-EXP-ROBUST-20261112T015119Z
