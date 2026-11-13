# Evaluation Summary — FCLR-FWD-VOL-011-CONFIRM-20261113T041200Z

Generated: 2026-11-13T04:15:43Z
Verdict: **INCONCLUSIVE**

## Primary (C2 vs B1, 24h QLIKE, pooled 3 blocks)

- mean diff: 0.026760
- 95% CI: [0.000343, 0.064822]
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

- BTCUSDT: rel -1.0630289335176746%, CI [-0.01223762977110065, 0.01980549188061072]
- ETHUSDT: rel -0.5998552098382518%, CI [-0.0038451073651465553, 0.01735071198888085]
- BNBUSDT: rel -6.393880456072219%, CI [0.007745040099008486, 0.04361068013249452]
- SOLUSDT: rel -5.92043796780371%, CI [0.0018284571546801473, 0.04198236850445892]
- XRPUSDT: rel -17.441890446503233%, CI [0.012659560371555348, 0.2396928905962122]

## Placebo

- null p95: -5.35% vs true -5.55% -> False

## Sensitivity (excluding previously inspected days)

- {'mean_diff': 0.047141621223313515, 'ci_lo': -0.000410986006965161, 'ci_hi': 0.10987026917409534, 'n': 5995, 'n_days': 50, 'p_boot': 0.052, 'rel_reduction_pct': -7.822495644537508}

## FCLR-011 reproduction

- {'mean_diff': -0.014711330252252306, 'ci_lo': -0.03083862387968236, 'ci_hi': 6.527733375376297e-06, 'rel_reduction_pct': 4.423125379203187, 'n': 10805, 'n_days': 91, 'sealed_mean_diff': -0.016458, 'sealed_rel_reduction_pct': 4.94, 'abs_diff_vs_sealed_pp': 0.5168746207968136, 'pass': False}
