# FCLR-SHEK-SCALE Sensitivity Grid — 2026-11-15T16:24:23Z

**Prereg:** `FCLR-SHEK-SCALE-20261115T063600Z` (frozen `2026-11-15T06:36:00Z`)
**Class:** EXPLORATORY_ONLY · promotable=false · sealed_mutated=false · network=false

**Grid:** percentiles [1,99],[5,95],[10,90] x censor [168,336]h x rv_split [tercile,median] = 12 cells x 2 arms = 24 cells

**Headline cell:** [5,95]/168h/tercile (recomputed for reference, never used to select headline)

---

## Grid cells — Arm A (Binance, primary)

  [1.0,99.0]/168h/tercile: events=257 (corrected=257, censored=0) KM med high=8.000000277777778h low=8.0h chi2=6.878077483243179 p=0.008725937414944096 Holm p=0.052355624489664576 med_diff=2.7777777766857525e-07h material=False verdict=NULL
  CI: [0.0, 1.9444444436800268e-06]

  [1.0,99.0]/168h/median: events=257 (corrected=257, censored=0) KM med high=8.0h low=8.0h chi2=6.276166732784498 p=0.012237252213309624 Holm p=0.08566076549316737 med_diff=0.0h material=False verdict=NULL
  CI: [0.0, 5.555555553371505e-07]

  [1.0,99.0]/336h/tercile: events=257 (corrected=257, censored=0) KM med high=8.000000277777778h low=8.0h chi2=6.878077483243179 p=0.008725937414944096 Holm p=0.052355624489664576 med_diff=2.7777777766857525e-07h material=False verdict=NULL
  CI: [0.0, 1.9444444436800268e-06]

  [1.0,99.0]/336h/median: events=257 (corrected=257, censored=0) KM med high=8.0h low=8.0h chi2=6.276166732784498 p=0.012237252213309624 Holm p=0.08566076549316737 med_diff=0.0h material=False verdict=NULL
  CI: [0.0, 5.555555553371505e-07]

  [5.0,95.0]/168h/tercile: events=847 (corrected=845, censored=2) KM med high=8.000000277777778h low=8.0h chi2=18.8987926104695 p=1.3783988168647454e-05 Holm p=0.00011027190534917963 med_diff=2.7777777766857525e-07h material=False verdict=TAIL_SHAPE_EFFECT
  CI: [-2.7777777766857525e-07, 1.9444444436800268e-06]

  [5.0,95.0]/168h/median: events=847 (corrected=845, censored=2) KM med high=8.000000277777778h low=8.0h chi2=14.608031963952438 p=0.00013234925014615762 Holm p=0.001058794001169261 med_diff=2.7777777766857525e-07h material=False verdict=TAIL_SHAPE_EFFECT
  CI: [-2.7777777766857525e-07, 1.111111110674301e-06]

  [5.0,95.0]/336h/tercile: events=847 (corrected=846, censored=1) KM med high=8.000000277777778h low=8.0h chi2=20.126778635301875 p=7.247481326744243e-06 Holm p=5.797985061395394e-05 med_diff=2.7777777766857525e-07h material=False verdict=TAIL_SHAPE_EFFECT
  CI: [-2.7777777766857525e-07, 1.9444444436800268e-06]

  [5.0,95.0]/336h/median: events=847 (corrected=846, censored=1) KM med high=8.000000277777778h low=8.0h chi2=15.664820875764635 p=7.561765719665825e-05 Holm p=0.000604941257573266 med_diff=2.7777777766857525e-07h material=False verdict=TAIL_SHAPE_EFFECT
  CI: [-2.7777777766857525e-07, 1.111111110674301e-06]

  [10.0,90.0]/168h/tercile: events=1381 (corrected=1377, censored=4) KM med high=8.000000833333333h low=8.000000277777778h chi2=22.917347070706803 p=1.691187114571946e-06 Holm p=1.3529496916575567e-05 med_diff=5.555555553371505e-07h material=False verdict=TAIL_SHAPE_EFFECT
  CI: [-2.7777777766857525e-07, 1.9444444454563836e-06]

  [10.0,90.0]/168h/median: events=1381 (corrected=1377, censored=4) KM med high=8.000000833333333h low=8.000000277777778h chi2=26.35450832437203 p=2.84154865637376e-07 Holm p=2.273238925099008e-06 med_diff=5.555555553371505e-07h material=False verdict=TAIL_SHAPE_EFFECT
  CI: [0.0, 1.9444444436800268e-06]

  [10.0,90.0]/336h/tercile: events=1381 (corrected=1378, censored=3) KM med high=8.000000833333333h low=8.000000277777778h chi2=23.96963303304486 p=9.786718002668948e-07 Holm p=7.829374402135159e-06 med_diff=5.555555553371505e-07h material=False verdict=TAIL_SHAPE_EFFECT
  CI: [-2.7777777766857525e-07, 2.222222223124959e-06]

  [10.0,90.0]/336h/median: events=1381 (corrected=1378, censored=3) KM med high=8.000000833333333h low=8.000000277777778h chi2=27.363222906357972 p=1.686075498108508e-07 Holm p=1.3488603984868064e-06 med_diff=5.555555553371505e-07h material=False verdict=TAIL_SHAPE_EFFECT
  CI: [0.0, 1.9444444436800268e-06]


## Grid cells — Arm B (ironflow, secondary, never promotable)

  [1.0,99.0]/168h/tercile: events=13778 (corrected=13778, censored=0) KM med high=1.9999894444444444h low=1.0000133333333334h chi2=233.433694808798 p=0.0 Holm p=0.0 med_diff=0.999976111111111h material=True verdict=REPLICATES_DIRECTION
  CI: [0.9999677777777778, 0.9999822222222221]

  [1.0,99.0]/168h/median: events=13778 (corrected=13778, censored=0) KM med high=1.999978888888889h low=1.0000141666666666h chi2=177.78265812392226 p=0.0 Holm p=0.0 med_diff=0.9999647222222223h material=True verdict=REPLICATES_DIRECTION
  CI: [1.2777777777639443e-05, 0.9999741666666666]

  [1.0,99.0]/336h/tercile: events=13778 (corrected=13778, censored=0) KM med high=1.9999894444444444h low=1.0000133333333334h chi2=233.433694808798 p=0.0 Holm p=0.0 med_diff=0.999976111111111h material=True verdict=REPLICATES_DIRECTION
  CI: [0.9999677777777778, 0.9999822222222221]

  [1.0,99.0]/336h/median: events=13778 (corrected=13778, censored=0) KM med high=1.999978888888889h low=1.0000141666666666h chi2=177.78265812392226 p=0.0 Holm p=0.0 med_diff=0.9999647222222223h material=True verdict=REPLICATES_DIRECTION
  CI: [1.2777777777639443e-05, 0.9999741666666666]

  [5.0,95.0]/168h/tercile: events=39021 (corrected=39016, censored=5) KM med high=1.9999952777777779h low=1.000025h chi2=384.3648099401398 p=0.0 Holm p=0.0 med_diff=0.9999702777777779h material=True verdict=REPLICATES_DIRECTION
  CI: [2.4999999999941735e-05, 0.9999763888888891]

  [5.0,95.0]/168h/median: events=39021 (corrected=39016, censored=5) KM med high=1.9999922222222222h low=1.0000283333333333h chi2=310.44803017075367 p=0.0 Holm p=0.0 med_diff=0.9999638888888889h material=True verdict=REPLICATES_DIRECTION
  CI: [1.6388888888885234e-05, 0.9999702777777779]

  [5.0,95.0]/336h/tercile: events=39021 (corrected=39018, censored=3) KM med high=1.9999952777777779h low=1.000025h chi2=386.7268628540982 p=0.0 Holm p=0.0 med_diff=0.9999702777777779h material=True verdict=REPLICATES_DIRECTION
  CI: [2.4999999999941735e-05, 0.9999763888888891]

  [5.0,95.0]/336h/median: events=39021 (corrected=39018, censored=3) KM med high=1.9999922222222222h low=1.0000283333333333h chi2=312.3838360964968 p=0.0 Holm p=0.0 med_diff=0.9999638888888889h material=True verdict=REPLICATES_DIRECTION
  CI: [1.6388888888885234e-05, 0.9999702777777779]

  [10.0,90.0]/168h/tercile: events=57611 (corrected=57585, censored=26) KM med high=1.9999972222222222h low=1.9999875h chi2=294.2726874906542 p=0.0 Holm p=0.0 med_diff=9.722222222174892e-06h material=False verdict=TAIL_SHAPE_EFFECT
  CI: [5.555555555591951e-06, 1.7500000000003624e-05]

  [10.0,90.0]/168h/median: events=57611 (corrected=57585, censored=26) KM med high=1.999996111111111h low=1.9999880555555556h chi2=270.3460681828237 p=0.0 Holm p=0.0 med_diff=8.055555555497307e-06h material=False verdict=TAIL_SHAPE_EFFECT
  CI: [4.444444444473561e-06, 1.3055555555752107e-05]

  [10.0,90.0]/336h/tercile: events=57611 (corrected=57599, censored=12) KM med high=1.9999972222222222h low=1.9999875h chi2=303.3971941472267 p=0.0 Holm p=0.0 med_diff=9.722222222174892e-06h material=False verdict=TAIL_SHAPE_EFFECT
  CI: [5.555555555591951e-06, 1.7500000000003624e-05]

  [10.0,90.0]/336h/median: events=57611 (corrected=57599, censored=12) KM med high=1.999996111111111h low=1.9999880555555556h chi2=273.1869664121878 p=0.0 Holm p=0.0 med_diff=8.055555555497307e-06h material=False verdict=TAIL_SHAPE_EFFECT
  CI: [4.444444444473561e-06, 1.3055555555530063e-05]

## Consistency vs headline

- Arm A headline verdict: **TAIL_SHAPE_EFFECT** (sealed: TAIL_SHAPE_EFFECT)
- Arm B headline verdict: **REPLICATES_DIRECTION** (sealed: REPLICATES_DIRECTION)

All cells reported only; none used to select or tune the headline. EXPLORATORY_ONLY, promotable=false.
