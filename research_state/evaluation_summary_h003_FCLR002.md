# Evaluation Summary (FCLR-H003)

Generated: 2026-11-09T15:27:50Z
Experiment: FCLR-002
Horizon: 24h | MMR: 0.005 | Leverages: [3.0, 5.0, 10.0, 20.0] | Sides: ['long', 'short'] (separate)
Panel: FCLR-002 test block 2024-07-23T00:00:00Z .. 2024-09-30T23:00:00Z

Notes: Labels are synthetic modeled boundary breaches (not observed liquidations). Long/short evaluated separately. Assumptions: maintenance margin rate 0.005, zero-cost boundary, mark close at decision time as entry, horizon 24h forward mark closes.

## lev3.0_long

- B0: n=8280, base_rate=0.0000, Brier=0.000020, log-loss=0.002550, AUPRC=0.000000
  best F1 @ thresh 0.00: prec=0.000 rec=0.000 (TP=0 FP=8280 TN=0 FN=0)
- C2: n=8274, base_rate=0.0000, Brier=0.000002, log-loss=0.000641, AUPRC=0.000000
  best F1 @ thresh 0.00: prec=0.000 rec=0.000 (TP=0 FP=8274 TN=0 FN=0)

## lev3.0_short

- B0: n=8280, base_rate=0.0000, Brier=0.000020, log-loss=0.002550, AUPRC=0.000000
  best F1 @ thresh 0.00: prec=0.000 rec=0.000 (TP=0 FP=8280 TN=0 FN=0)
- C2: n=8274, base_rate=0.0000, Brier=0.000002, log-loss=0.000641, AUPRC=0.000000
  best F1 @ thresh 0.00: prec=0.000 rec=0.000 (TP=0 FP=8274 TN=0 FN=0)

## lev5.0_long

- B0: n=8280, base_rate=0.0036, Brier=0.003625, log-loss=0.024076, AUPRC=0.008798
  best F1 @ thresh 0.01: prec=0.015 rec=0.167 (TP=5 FP=338 TN=7912 FN=25)
- C2: n=8274, base_rate=0.0036, Brier=0.003615, log-loss=0.024281, AUPRC=0.009965
  best F1 @ thresh 0.01: prec=0.017 rec=0.100 (TP=3 FP=177 TN=8067 FN=27)

## lev5.0_short

- B0: n=8280, base_rate=0.0033, Brier=0.003239, log-loss=0.020226, AUPRC=0.011412
  best F1 @ thresh 0.02: prec=0.032 rec=0.185 (TP=5 FP=149 TN=8104 FN=22)
- C2: n=8274, base_rate=0.0033, Brier=0.003244, log-loss=0.022088, AUPRC=0.015339
  best F1 @ thresh 0.02: prec=0.071 rec=0.074 (TP=2 FP=26 TN=8221 FN=25)

## lev10.0_long

- B0: n=8280, base_rate=0.0169, Brier=0.016577, log-loss=0.082507, AUPRC=0.032137
  best F1 @ thresh 0.03: prec=0.044 rec=0.300 (TP=42 FP=908 TN=7232 FN=98)
- C2: n=8274, base_rate=0.0169, Brier=0.016504, log-loss=0.082259, AUPRC=0.037993
  best F1 @ thresh 0.03: prec=0.049 rec=0.414 (TP=58 FP=1115 TN=7019 FN=82)

## lev10.0_short

- B0: n=8280, base_rate=0.0153, Brier=0.014464, log-loss=0.066615, AUPRC=0.152351
  best F1 @ thresh 0.04: prec=0.276 rec=0.433 (TP=55 FP=144 TN=8009 FN=72)
- C2: n=8274, base_rate=0.0153, Brier=0.014639, log-loss=0.069548, AUPRC=0.170915
  best F1 @ thresh 0.04: prec=0.280 rec=0.291 (TP=37 FP=95 TN=8052 FN=90)

## lev20.0_long

- B0: n=8280, base_rate=0.1249, Brier=0.107878, log-loss=0.370613, AUPRC=0.184587
  best F1 @ thresh 0.13: prec=0.223 rec=0.352 (TP=364 FP=1271 TN=5975 FN=670)
- C2: n=8274, base_rate=0.1250, Brier=0.107764, log-loss=0.369912, AUPRC=0.190695
  best F1 @ thresh 0.13: prec=0.223 rec=0.378 (TP=391 FP=1365 TN=5875 FN=643)

## lev20.0_short

- B0: n=8280, base_rate=0.1025, Brier=0.088912, log-loss=0.316933, AUPRC=0.241277
  best F1 @ thresh 0.14: prec=0.268 rec=0.257 (TP=218 FP=595 TN=6836 FN=631)
- C2: n=8274, base_rate=0.1026, Brier=0.089074, log-loss=0.317375, AUPRC=0.245475
  best F1 @ thresh 0.13: prec=0.256 rec=0.365 (TP=310 FP=899 TN=6526 FN=539)
