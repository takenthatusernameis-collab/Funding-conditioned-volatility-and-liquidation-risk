# Evaluation Summary — FCLR-FWD-VOL-011-CONFIRM-20261113T041200Z

Generated: 2026-11-13T04:14:59Z
Verdict: **INCONCLUSIVE**

## Primary (C2 vs B1, 24h QLIKE, pooled 3 blocks)

- mean diff: 0.026762
- 95% CI: [0.000343, 0.064823]
- relative reduction: -5.55%
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

- BTCUSDT: rel -1.0643877082105644%, CI [-0.012233483591868223, 0.01981112837836984]
- ETHUSDT: rel -0.5987082559165243%, CI [-0.0038465601172774358, 0.01733310037449582]
- BNBUSDT: rel -6.395299662056581%, CI [0.007742003739256015, 0.04362522552813711]
- SOLUSDT: rel -5.923437708991682%, CI [0.0018257907069710662, 0.04200573645389203]
- XRPUSDT: rel -17.43653823297184%, CI [0.012665327367029492, 0.23963873522274787]

## Placebo

- null p95: -5.35% vs true -5.55% -> False

## Sensitivity (excluding previously inspected days)

- {'mean_diff': 0.04713926311360983, 'ci_lo': -0.0004118179670357802, 'ci_hi': 0.1098658378050256, 'n': 5995, 'n_days': 50, 'p_boot': 0.052, 'rel_reduction_pct': -7.822104349066379}

## FCLR-011 reproduction

- {'mean_diff': -0.014716181175293655, 'ci_lo': -0.030838985979033652, 'ci_hi': 4.424266591947451e-06, 'rel_reduction_pct': 4.42458386327287, 'n': 10805, 'n_days': 91, 'sealed_mean_diff': -0.016458, 'sealed_rel_reduction_pct': 4.94, 'abs_diff_vs_sealed_pp': 0.5154161367271302, 'pass': False}
