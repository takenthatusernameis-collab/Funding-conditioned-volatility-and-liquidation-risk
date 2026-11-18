# FCLR-LIQ-RISK-CALIBRATION-06 — Out-of-Sample Breach-Risk Calibration

**Session:** `session_20261118T182813Z`
**Campaign:** `FCLR-LIQ-RISK-CALIBRATION-06-20261118T182600Z`
**Label:** EXPLORATORY/PILOT — **not confirmatory**.
**Outcome:** `synthetic_modeled_boundary_breach`, `observed_liquidation_labels=false`.
**Stdlib only**; no network; no parquet; no sealed months.

**Verdict:** `HONEST_NEGATIVE_OR_INCONCLUSIVE`

## Dataset
- Rows: 262080 (unique origins 21840); overall breach rate 0.023813339438339437
- Rows without features: 0

## Primary scenario `L10|long|H24` — ΔBrier vs B0 (positive = funding better)

| Holdout | Model | ΔBrier | CI95 | Δlogloss | CI95 |
|---|---|---|---|---|---|
| 2024-07 | B1_funding_conditioned | -0.0000 | [-0.0003565426011164354, 0.0004624693728082956] | -0.0003 | [-0.00591337325122959, 0.010888569541203739] |
| 2024-07 | B2_funding_shock | -0.0002 | [-0.0004966721137418147, -6.8006499076298e-05] | 0.0043 | [-0.010162288318593768, -0.0005376219990587394] |
| 2024-08 | B1_funding_conditioned | 0.0005 | [-0.00012414288981169166, 0.0013744046295527624] | -0.0058 | [-0.0013063482098031962, 0.018127670165085936] |
| 2024-08 | B2_funding_shock | -0.0003 | [-0.0011411288907093194, 0.0002489853123276644] | 0.0018 | [-0.005570634792390026, 0.002914119760659315] |
| 2024-09 | B1_funding_conditioned | 0.0002 | [0.0001102764483828145, 0.00021529876518996697] | -0.0069 | [0.005705932568447937, 0.007838669861322287] |
| 2024-09 | B2_funding_shock | -0.0001 | [-9.119551636430502e-05, -1.692807011744015e-05] | 0.0008 | [-0.0016243065882994973, -0.00012185132780926749] |

## Pooled equal-weight ΔBrier over 12 scenarios

| Holdout | Model | mean ΔBrier | CI95 | placebo mean ΔBrier |
|---|---|---|---|---|
| 2024-07 | B1_funding_conditioned | -0.0000 | [-8.34074637427607e-05, 2.2697125114120178e-05] | -0.0002061295961564854 |
| 2024-07 | B2_funding_shock | -0.0008 | [-0.001978223431481317, -0.00013675806422432018] | -0.00024612572909208703 |
| 2024-08 | B1_funding_conditioned | 0.0002 | [-0.00019249185721635035, 0.0006398702207253676] | -0.000862649237961358 |
| 2024-08 | B2_funding_shock | -0.0006 | [-0.001594729844959268, 5.704894032193007e-06] | -0.0008861717453361346 |
| 2024-09 | B1_funding_conditioned | 0.0001 | [-0.00027495180251501896, 0.0004937416225796024] | -0.00024774378666985944 |
| 2024-09 | B2_funding_shock | -0.0001 | [-0.0001162922498155345, 1.232190627148009e-05] | -0.00026552655199962735 |

## Materiality floor
- Holdouts where B1 beats B0 (Δ>0, CI lo>0): **1/3**
- Holdouts where B2 beats B0 (Δ>0, CI lo>0): **0/3**
- Real mean ΔBrier: B1 0.0002, B2 -0.0002
- Placebo mean ΔBrier: B1 -0.00043884087359590093, B2 -0.00046594134214261626
- **floor_met = False**

## Calibration deciles (best model, primary scenario, per holdout)

### 2024-07 — best model `B0_rv_only`

| decile | n | mean_predicted | observed_rate |
|---|---|---|---|
| 1 | 372 | 0.01405 | 0.00000 |
| 2 | 372 | 0.01426 | 0.00000 |
| 3 | 372 | 0.01444 | 0.00000 |
| 4 | 372 | 0.01464 | 0.00000 |
| 5 | 372 | 0.01489 | 0.00000 |
| 6 | 372 | 0.01521 | 0.00269 |
| 7 | 372 | 0.01571 | 0.01613 |
| 8 | 372 | 0.01651 | 0.09677 |
| 9 | 372 | 0.01803 | 0.06183 |
| 10 | 372 | 0.02527 | 0.03226 |

### 2024-08 — best model `B1_funding_conditioned`

| decile | n | mean_predicted | observed_rate |
|---|---|---|---|
| 1 | 372 | 0.00606 | 0.00000 |
| 2 | 372 | 0.00799 | 0.00269 |
| 3 | 372 | 0.00963 | 0.00000 |
| 4 | 372 | 0.01112 | 0.01882 |
| 5 | 372 | 0.01273 | 0.02151 |
| 6 | 372 | 0.01448 | 0.02957 |
| 7 | 372 | 0.01727 | 0.04839 |
| 8 | 372 | 0.02043 | 0.07796 |
| 9 | 372 | 0.02816 | 0.11022 |
| 10 | 372 | 0.08364 | 0.03763 |

### 2024-09 — best model `B1_funding_conditioned`

| decile | n | mean_predicted | observed_rate |
|---|---|---|---|
| 1 | 348 | 0.00626 | 0.00000 |
| 2 | 348 | 0.00759 | 0.00000 |
| 3 | 348 | 0.00866 | 0.00000 |
| 4 | 348 | 0.00954 | 0.00287 |
| 5 | 348 | 0.01051 | 0.00287 |
| 6 | 348 | 0.01163 | 0.00000 |
| 7 | 348 | 0.01322 | 0.00000 |
| 8 | 348 | 0.01637 | 0.00000 |
| 9 | 348 | 0.02270 | 0.00000 |
| 10 | 348 | 0.03051 | 0.00000 |

## LOIO (primary scenario)

- 2024-07: B1_funding_conditioned={BTCUSDT:-0.0001, ETHUSDT:0.0000, SOLUSDT:-0.0002, XRPUSDT:0.0000, BNBUSDT:0.0000}, B2_funding_shock={BTCUSDT:-0.0004, ETHUSDT:-0.0002, SOLUSDT:-0.0022, XRPUSDT:-0.0001, BNBUSDT:-0.0003}
- 2024-08: B1_funding_conditioned={BTCUSDT:0.0006, ETHUSDT:0.0006, SOLUSDT:-0.0007, XRPUSDT:0.0014, BNBUSDT:0.0007}, B2_funding_shock={BTCUSDT:-0.0006, ETHUSDT:0.0000, SOLUSDT:-0.0022, XRPUSDT:-0.0001, BNBUSDT:0.0000}
- 2024-09: B1_funding_conditioned={BTCUSDT:0.0002, ETHUSDT:0.0002, SOLUSDT:0.0001, XRPUSDT:0.0001, BNBUSDT:0.0004}, B2_funding_shock={BTCUSDT:-0.0002, ETHUSDT:-0.0000, SOLUSDT:-0.0002, XRPUSDT:0.0000, BNBUSDT:-0.0000}

## Honest status
- EXPLORATORY/PILOT. Modeled boundary breaches only; never observed liquidations.
- Positive/negative result is reported as-is; the floor is pre-registered and applied mechanically.
- No sealed months, no network, no confirmatory promotion.
