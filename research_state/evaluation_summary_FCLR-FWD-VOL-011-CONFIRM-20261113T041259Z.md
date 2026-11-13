# Evaluation Summary — FCLR-FWD-VOL-011-CONFIRM-20261113T041200Z

Generated: 2026-11-13T04:12:59Z
Verdict: **NOT_REPLICATED**

## Primary (C2 vs B1, 24h QLIKE, pooled 3 blocks)

- mean diff: 0.026841
- 95% CI: [0.000344, 0.064968]
- relative reduction: -5.57%
- n: 10200

## Checks

- materiality_ge_2pct: False
- ci_excludes_zero: False
- instruments_ge_5: True
- blocks_ge_3: True
- loio_ge_4_of_5: False
- placebo_pass: False
- sensitivity_pass: False
- repro_011_pass: False

## LOIO

- BTCUSDT: rel -1.0561093030078683%, CI [-0.012580237385733722, 0.01990785723254948]
- ETHUSDT: rel -0.5899409047850195%, CI [-0.003906533741206392, 0.01724050329420038]
- BNBUSDT: rel -6.386567949779717%, CI [0.0077405598459846965, 0.04354119095724696]
- SOLUSDT: rel -6.0349304039887635%, CI [0.0018501089340664035, 0.04276701427761578]
- XRPUSDT: rel -17.45318018805902%, CI [0.012646362194177413, 0.24010420946838734]

## Placebo

- null p95: -5.35% vs true -5.57% -> False

## Sensitivity (excluding previously inspected days)

- {'mean_diff': 0.04721424140489102, 'ci_lo': -0.00040440766698917024, 'ci_hi': 0.1100103673022755, 'n': 5995, 'n_days': 50, 'p_boot': 0.052, 'rel_reduction_pct': -7.834545952510681}

## FCLR-011 reproduction

- {'mean_diff': -0.01340280953640259, 'ci_lo': -0.023139360106869553, 'ci_hi': -0.004566994144131955, 'n': 10805, 'n_days': 91, 'p_boot': 0.008, 'rel_reduction_pct': 4.037272008532205}
