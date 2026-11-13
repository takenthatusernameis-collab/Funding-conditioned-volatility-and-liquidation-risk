# Evaluation Summary — FCLR-EXP-ROBUST-REDO-20261113T063000Z

Generated: 2026-11-13T07:12:29Z
Verdict: **FRAGILE**

Panel: tracka_hl_expansion_panel_20261111T202344Z.parquet (sha256 39916a72dfc37d15...)

## Checks

- loio_ge_6_of_8: False (4/8)
- placebo_pass: False (null p95 21.88866185618114, true 19.03709721199804)
- bootstrap_settings_pass: True

## Placebo (funding permutation)

- true rel reduction: 19.04%
- null p95: 21.8887% (n=2000)
- p-value approx: 0.18

## LOIO

- ZEC: rel 9.67%, CI [-2.649513, 0.682221], mat=True, ci=False
- NEAR: rel 24.36%, CI [-7.132405, 0.000058], mat=True, ci=False
- UNI: rel 3.12%, CI [-1.921964, 0.752544], mat=True, ci=False
- AAVE: rel 18.78%, CI [-5.788025, -1.096023], mat=True, ci=True
- CRV: rel 19.37%, CI [-5.094251, -0.390990], mat=True, ci=True
- ADA: rel 17.58%, CI [-4.410308, -0.595051], mat=True, ci=True
- LTC: rel 29.71%, CI [-8.787484, -2.417754], mat=True, ci=True
- BCH: rel 10.39%, CI [-6.222642, 3.370433], mat=True, ci=False

## Note

The prior sealed 19.04% PASS (LOIO 4/8, placebo null p95 21.10%) is FRAGILE and is not re-scored here. This cell only tests whether the pre-registered design changes the verdict.
