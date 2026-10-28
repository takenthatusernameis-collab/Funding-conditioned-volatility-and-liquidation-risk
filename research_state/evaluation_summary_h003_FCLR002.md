# Evaluation Summary (FCLR-H003)

Generated: 2026-10-28T22:53:27Z
Experiment: FCLR-002
Horizon: 24h | MMR: 0.005 | Leverages: [3.0, 5.0, 10.0, 20.0] | Sides: ['long', 'short'] (separate)
Panel: FCLR-002 test block 2024-07-23T00:00:00Z .. 2024-09-30T23:00:00Z

Notes: Labels are synthetic modeled boundary breaches (not observed liquidations). Long/short evaluated separately. Assumptions: maintenance margin rate 0.005, zero-cost boundary, mark close at decision time as entry, horizon 24h forward mark closes.

## lev3.0_long

- B0: n=8280, base_rate=0.0000, Brier=0.000020, log-loss=0.002557, AUPRC=0.000000
  best F1 @ thresh 0.00: prec=0.000 rec=0.000 (TP=0 FP=8280 TN=0 FN=0)
- C2: n=8274, base_rate=0.0000, Brier=0.000002, log-loss=0.000644, AUPRC=0.000000
  best F1 @ thresh 0.00: prec=0.000 rec=0.000 (TP=0 FP=8274 TN=0 FN=0)

## lev3.0_short

- B0: n=8280, base_rate=0.0000, Brier=0.000020, log-loss=0.002557, AUPRC=0.000000
  best F1 @ thresh 0.00: prec=0.000 rec=0.000 (TP=0 FP=8280 TN=0 FN=0)
- C2: n=8274, base_rate=0.0000, Brier=0.000002, log-loss=0.000644, AUPRC=0.000000
  best F1 @ thresh 0.00: prec=0.000 rec=0.000 (TP=0 FP=8274 TN=0 FN=0)

## lev5.0_long

- B0: n=8280, base_rate=0.0036, Brier=0.003625, log-loss=0.024065, AUPRC=0.008473
  best F1 @ thresh 0.01: prec=0.014 rec=0.167 (TP=5 FP=354 TN=7896 FN=25)
- C2: n=8274, base_rate=0.0036, Brier=0.003615, log-loss=0.024166, AUPRC=0.008949
  best F1 @ thresh 0.01: prec=0.015 rec=0.100 (TP=3 FP=202 TN=8042 FN=27)

## lev5.0_short

- B0: n=8280, base_rate=0.0033, Brier=0.003240, log-loss=0.020246, AUPRC=0.012571
  best F1 @ thresh 0.02: prec=0.031 rec=0.185 (TP=5 FP=155 TN=8098 FN=22)
- C2: n=8274, base_rate=0.0033, Brier=0.003244, log-loss=0.021994, AUPRC=0.040594
  best F1 @ thresh 0.02: prec=0.086 rec=0.111 (TP=3 FP=32 TN=8215 FN=24)

## lev10.0_long

- B0: n=8280, base_rate=0.0169, Brier=0.016589, log-loss=0.082749, AUPRC=0.029867
  best F1 @ thresh 0.03: prec=0.039 rec=0.321 (TP=45 FP=1116 TN=7024 FN=95)
- C2: n=8274, base_rate=0.0169, Brier=0.016517, log-loss=0.082601, AUPRC=0.037114
  best F1 @ thresh 0.04: prec=0.052 rec=0.200 (TP=28 FP=514 TN=7620 FN=112)

## lev10.0_short

- B0: n=8280, base_rate=0.0153, Brier=0.014434, log-loss=0.066644, AUPRC=0.152279
  best F1 @ thresh 0.04: prec=0.240 rec=0.441 (TP=56 FP=177 TN=7976 FN=71)
- C2: n=8274, base_rate=0.0153, Brier=0.014613, log-loss=0.069495, AUPRC=0.169984
  best F1 @ thresh 0.04: prec=0.241 rec=0.323 (TP=41 FP=129 TN=8018 FN=86)

## lev20.0_long

- B0: n=8280, base_rate=0.1249, Brier=0.108023, log-loss=0.371285, AUPRC=0.188117
  best F1 @ thresh 0.12: prec=0.213 rec=0.404 (TP=418 FP=1543 TN=5703 FN=616)
- C2: n=8274, base_rate=0.1250, Brier=0.107891, log-loss=0.370437, AUPRC=0.190336
  best F1 @ thresh 0.12: prec=0.207 rec=0.440 (TP=455 FP=1739 TN=5501 FN=579)

## lev20.0_short

- B0: n=8280, base_rate=0.1025, Brier=0.088904, log-loss=0.316916, AUPRC=0.242194
  best F1 @ thresh 0.15: prec=0.356 rec=0.211 (TP=179 FP=324 TN=7107 FN=670)
- C2: n=8274, base_rate=0.1026, Brier=0.089042, log-loss=0.317273, AUPRC=0.243350
  best F1 @ thresh 0.13: prec=0.257 rec=0.371 (TP=315 FP=912 TN=6513 FN=534)
