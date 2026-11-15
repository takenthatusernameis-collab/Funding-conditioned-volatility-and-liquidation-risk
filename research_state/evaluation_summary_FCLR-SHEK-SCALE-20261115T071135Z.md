# FCLR-SHEK-SCALE Evaluation Summary — 2026-11-15T07:21:47Z

**Prereg:** `FCLR-SHEK-SCALE-20261115T063600Z` (frozen `2026-11-15T06:36:00Z`)  
**Class:** EXPLORATORY_ONLY · promotable=false · sealed_mutated=false · network=false

## Arm A — Binance (primary, independent of 2024-Q1)

- Events: 847 (corrected 845, censored 2)
- Verdict: **TAIL_SHAPE_EFFECT**
- Pooled high vs low: KM median 8.000000277777778h vs 8.0h; corrected median 8.000000277777778h vs 8.0h; mean 17.02491106563859h vs 12.353356768747547h
- log-rank chi2=18.8987926104695, p=1.3783988168647454e-05, Holm p=0.00011027190534917963
- median diff (KM-anchored) = 2.7777777766857525e-07h; materiality threshold = 4.0h; material = False
- Median diff (high-low) 95% cluster+block CI: [-2.7777777766857525e-07, 1.9444444436800268e-06]

### Regime counts

| Regime | N | Corrected | Censored | KM median (h) | Corrected median (h) | Mean (h) |
|---|---|---|---|---|---|---|
| high | 283 | 281 | 2 | 8.000000277777778 | 8.000000277777778 | 17.02491106563859 |
| middle | 280 | 280 | 0 | 8.000000277777778 | 8.000000277777778 | 12.57142861904762 |
| low | 283 | 283 | 0 | 8.0 | 8.0 | 12.353356768747547 |
| missing | 1 | 1 | 0 | 24.0 | 24.0 | 24.0 |

### Primary comparison family (Holm-adjusted)

| Comparison | High N | Low N | KM hi | KM lo | Mean hi | Mean lo | p | Holm p | Material |
|---|---|---|---|---|---|---|---|---|---|
| pooled_high_vs_low | 281 | 283 | 8.000000277777778 | 8.0 | 17.02491106563859 | 12.353356768747547 | 1.3783988168647454e-05 | 0.00011027190534917963 | False |
| positive_high_vs_low | 71 | 108 | 15.999996944444444 | 8.000000277777778 | 21.971830974178403 | 14.296296093106996 | 0.0033519792376999202 | 0.02011187542619952 | True |
| negative_high_vs_low | 210 | 175 | 8.0 | 8.0 | 15.352381001322751 | 11.154285642857143 | 0.0001518420211773508 | 0.0010628941482414556 | False |
| symbol_BNBUSDT_high_vs_low | 57 | 58 | 8.000000277777778 | 8.000000277777778 | 16.00000009746589 | 11.034482691570883 | 0.007033644210683643 | 0.035168221053418214 | False |
| symbol_BTCUSDT_high_vs_low | 63 | 63 | 8.000002222222221 | 8.000000277777778 | 18.03174601410935 | 13.58730138888889 | 0.024181850631834534 | 0.09672740252733814 | False |
| symbol_ETHUSDT_high_vs_low | 55 | 56 | 8.000000277777778 | 8.0 | 20.79999984848485 | 12.14285699404762 | 0.05555235486679644 | 0.16665706460038932 | False |
| symbol_SOLUSDT_high_vs_low | 43 | 43 | 8.0 | 8.0 | 16.37209330103359 | 14.139534857881136 | 0.1659557511804889 | 0.18633215975328654 | False |
| symbol_XRPUSDT_high_vs_low | 63 | 63 | 8.0 | 8.0 | 14.095238117283952 | 11.301587164903 | 0.09316607987664327 | 0.18633215975328654 | False |

## Arm B — ironflow cross-coin (secondary, never promotable)

- Coins: 160; events: 39021 (corrected 39016, censored 5)
- Verdict: **REPLICATES_DIRECTION**
- Pooled high vs low: KM median 1.9999952777777779h vs 1.000025h; corrected median 1.9999952777777779h vs 1.000025h; mean 4.059230680023148h vs 2.678494265067992h
- log-rank chi2=384.3648099401398, p=0.0, Holm p=0.0
- median diff (KM-anchored) = 0.9999702777777779h; material = True


## Overall

- Arm A verdict: **TAIL_SHAPE_EFFECT**; Arm B verdict: **REPLICATES_DIRECTION**
- This is an EXPLORATORY_ONLY partial replication; it never promotes H2, and correction time is not forecast skill or observed-liquidation prediction.
