# Evaluation Summary (FCLR-H003-EXT-001)

Generated: 2026-10-30T19:15:31Z
Experiment: FCLR-H003-EXT-001
Symbols: BTCUSDT, ETHUSDT, BNBUSDT, SOLUSDT, XRPUSDT
Panel: unsealed 2026 from research_state/data_cache | common range 2026-01-01 .. 2026-08-06
Splits (chronological, purge>=168h): train 2026-01-01..2026-05-11 | test 2026-07-01..2026-08-06 (val abbreviated)
Horizons: [72, 168]h | MMR tiers: [0.004, 0.005] | Leverages: [5.0, 10.0] | Sides: separate

Track: B (modeled boundary breaches). Distinct from observed liquidations (Track A). Never conflate.
Assumptions: mark price reference, maintenance margin rate per tier S1=0.005, S2=0.004, zero transaction costs modeled, entry at t close, breach if min/max of forward mark closes crosses boundary within horizon.

## Horizon 72h | MMR 0.004

### long lev5.0
- B0: n=4035, base_rate=0.0000, Brier=0.000126, logloss=0.010324
- C1: n=4025, base_rate=0.0000, Brier=0.000105, logloss=0.009039
- C2: n=4025, base_rate=0.0000, Brier=0.000105, logloss=0.009039

### short lev5.0
- B0: n=4035, base_rate=0.0000, Brier=0.000041, logloss=0.005760
- C1: n=4025, base_rate=0.0000, Brier=0.000007, logloss=0.002110
- C2: n=4025, base_rate=0.0000, Brier=0.000007, logloss=0.002110

### long lev10.0
- B0: n=4035, base_rate=0.0000, Brier=0.003245, logloss=0.056800
- C1: n=4025, base_rate=0.0000, Brier=0.003707, logloss=0.060829
- C2: n=4025, base_rate=0.0000, Brier=0.003707, logloss=0.060829

### short lev10.0
- B0: n=4035, base_rate=0.0141, Brier=0.013969, logloss=0.075221
- C1: n=4025, base_rate=0.0142, Brier=0.013978, logloss=0.075927
- C2: n=4025, base_rate=0.0142, Brier=0.013978, logloss=0.075927

## Horizon 72h | MMR 0.005

### long lev5.0
- B0: n=4035, base_rate=0.0000, Brier=0.000130, logloss=0.010529
- C1: n=4025, base_rate=0.0000, Brier=0.000112, logloss=0.009368
- C2: n=4025, base_rate=0.0000, Brier=0.000112, logloss=0.009368

### short lev5.0
- B0: n=4035, base_rate=0.0000, Brier=0.000041, logloss=0.005760
- C1: n=4025, base_rate=0.0000, Brier=0.000007, logloss=0.002110
- C2: n=4025, base_rate=0.0000, Brier=0.000007, logloss=0.002110

### long lev10.0
- B0: n=4035, base_rate=0.0000, Brier=0.003401, logloss=0.058226
- C1: n=4025, base_rate=0.0000, Brier=0.003871, logloss=0.062263
- C2: n=4025, base_rate=0.0000, Brier=0.003871, logloss=0.062263

### short lev10.0
- B0: n=4035, base_rate=0.0144, Brier=0.014228, logloss=0.076624
- C1: n=4025, base_rate=0.0144, Brier=0.014239, logloss=0.077353
- C2: n=4025, base_rate=0.0144, Brier=0.014239, logloss=0.077353

## Horizon 168h | MMR 0.004

### long lev5.0
- B0: n=3555, base_rate=0.0000, Brier=0.002223, logloss=0.046477
- C1: n=3547, base_rate=0.0000, Brier=0.002619, logloss=0.050365
- C2: n=3547, base_rate=0.0000, Brier=0.002619, logloss=0.050365

### short lev5.0
- B0: n=3555, base_rate=0.0000, Brier=0.000052, logloss=0.006536
- C1: n=3547, base_rate=0.0000, Brier=0.000013, logloss=0.002891
- C2: n=3547, base_rate=0.0000, Brier=0.000013, logloss=0.002891

### long lev10.0
- B0: n=3555, base_rate=0.0011, Brier=0.022866, logloss=0.161179
- C1: n=3547, base_rate=0.0011, Brier=0.023144, logloss=0.162665
- C2: n=3547, base_rate=0.0011, Brier=0.023144, logloss=0.162665

### short lev10.0
- B0: n=3555, base_rate=0.0281, Brier=0.033169, logloss=0.169317
- C1: n=3547, base_rate=0.0282, Brier=0.032833, logloss=0.168111
- C2: n=3547, base_rate=0.0282, Brier=0.032833, logloss=0.168111

## Horizon 168h | MMR 0.005

### long lev5.0
- B0: n=3555, base_rate=0.0000, Brier=0.002316, logloss=0.047484
- C1: n=3547, base_rate=0.0000, Brier=0.002720, logloss=0.051390
- C2: n=3547, base_rate=0.0000, Brier=0.002720, logloss=0.051390

### short lev5.0
- B0: n=3555, base_rate=0.0000, Brier=0.000053, logloss=0.006564
- C1: n=3547, base_rate=0.0000, Brier=0.000013, logloss=0.002922
- C2: n=3547, base_rate=0.0000, Brier=0.000013, logloss=0.002922

### long lev10.0
- B0: n=3555, base_rate=0.0011, Brier=0.023756, logloss=0.164692
- C1: n=3547, base_rate=0.0011, Brier=0.024014, logloss=0.166082
- C2: n=3547, base_rate=0.0011, Brier=0.024014, logloss=0.166082

### short lev10.0
- B0: n=3555, base_rate=0.0284, Brier=0.034007, logloss=0.173166
- C1: n=3547, base_rate=0.0285, Brier=0.033640, logloss=0.171852
- C2: n=3547, base_rate=0.0285, Brier=0.033640, logloss=0.171852

## Summary
- Primary comparison: C2 vs B1 (RV+funding+price-dislocation vs RV-only). Paired sample as above.
- Uncertainty/inference: preliminary run with reduced epochs/grid for speed; full bootstrap/LOO/Holm to be completed or noted. See protocol for full requirements.
- Intensity: denominators (OI/volume) not consistently available in cached panel -> not computed.
- Verdict: incremental skill assessment based on relative Brier/logloss vs B0/B1 on paired test sets.

## Inference (added 2026-10-30T22:04:04Z)

Track B only. Block bootstrap B=2000 (resample (sym,date) blocks), seed=12345, paired on common (sym,ts). Features/models as in protocol.

### Intensity target
- Available: false
- Details: OI/volume/openInterest not consistently present in cached panel for all symbols/periods; no defensible denominators found.
- Action: Coverage limits documented; no synthetic intensity fabricated. Remains a documented gap.

### C2 vs B0 (ΔBrier = B0_brier - C2_brier, positive = C2 better) with 95% block-bootstrap CIs

- h168_mmr0.004_lev10.0_long: Δ=-0.000278 CI95=[-0.000555,-0.000005] (n.s.), n_common=3555
- h168_mmr0.004_lev10.0_short: Δ=0.000336 CI95=[0.000007,0.000661] (SIG), n_common=3555
- h168_mmr0.004_lev5.0_long: Δ=-0.000396 CI95=[-0.000781,0.000004] (n.s.), n_common=3555
- h168_mmr0.004_lev5.0_short: Δ=0.000039 CI95=[-0.000002,0.000078] (n.s.), n_common=3555
- h168_mmr0.005_lev10.0_long: Δ=-0.000258 CI95=[-0.000524,0.000001] (n.s.), n_common=3555
- h168_mmr0.005_lev10.0_short: Δ=0.000367 CI95=[0.000005,0.000716] (SIG), n_common=3555
- h168_mmr0.005_lev5.0_long: Δ=-0.000404 CI95=[-0.000787,-0.000013] (n.s.), n_common=3555
- h168_mmr0.005_lev5.0_short: Δ=0.000040 CI95=[0.000000,0.000084] (SIG), n_common=3555
- h72_mmr0.004_lev10.0_long: Δ=-0.000462 CI95=[-0.000908,-0.000008] (n.s.), n_common=4035
- h72_mmr0.004_lev10.0_short: Δ=-0.000009 CI95=[-0.000020,0.000001] (n.s.), n_common=4035
- h72_mmr0.004_lev5.0_long: Δ=0.000021 CI95=[-0.000001,0.000043] (n.s.), n_common=4035
- h72_mmr0.004_lev5.0_short: Δ=0.000034 CI95=[-0.000002,0.000068] (n.s.), n_common=4035
- h72_mmr0.005_lev10.0_long: Δ=-0.000470 CI95=[-0.000935,0.000007] (n.s.), n_common=4035
- h72_mmr0.005_lev10.0_short: Δ=-0.000011 CI95=[-0.000023,0.000002] (n.s.), n_common=4035
- h72_mmr0.005_lev5.0_long: Δ=0.000018 CI95=[-0.000002,0.000039] (n.s.), n_common=4035
- h72_mmr0.005_lev5.0_short: Δ=0.000034 CI95=[-0.000003,0.000070] (n.s.), n_common=4035

### Leave-one-symbol-out stability (ΔBrier C2 vs B0)

- h168_mmr0.004_lev10.0_long: LOO deltas = [-0.000363, -0.000119, -0.000198, -0.000251, -0.000313]
- h168_mmr0.004_lev10.0_short: LOO deltas = [0.000293, 0.000206, 9.6e-05, 0.00032, 0.000445]
- h168_mmr0.004_lev5.0_long: LOO deltas = [-0.000272, -0.000262, -0.000555, -0.000547, -0.00043]
- h168_mmr0.004_lev5.0_short: LOO deltas = [3.9e-05, 1.6e-05, 1.9e-05, 2.2e-05, 7e-06]
- h168_mmr0.005_lev10.0_long: LOO deltas = [-0.000184, -0.000244, -0.000176, -8.8e-05, -0.000222]
- h168_mmr0.005_lev10.0_short: LOO deltas = [4.5e-05, 0.000304, 0.000488, 0.000495, 0.000294]
- h168_mmr0.005_lev5.0_long: LOO deltas = [-0.000441, -8.5e-05, -0.000426, -0.000334, -0.000221]
- h168_mmr0.005_lev5.0_short: LOO deltas = [2e-05, 5.6e-05, 2.1e-05, 1e-05, 4.7e-05]
- h72_mmr0.004_lev10.0_long: LOO deltas = [-0.000404, -0.000395, -7.8e-05, -0.000294, -0.000442]
- h72_mmr0.004_lev10.0_short: LOO deltas = [-3e-06, -7e-06, -7e-06, -6e-06, -1.1e-05]
- h72_mmr0.004_lev5.0_long: LOO deltas = [1.1e-05, 2.3e-05, 1.4e-05, 1.7e-05, 2.7e-05]
- h72_mmr0.004_lev5.0_short: LOO deltas = [3e-05, 1.9e-05, 4.3e-05, 3e-05, 3.5e-05]
- h72_mmr0.005_lev10.0_long: LOO deltas = [-0.00051, -0.000658, -0.000752, -0.000415, -0.000624]
- h72_mmr0.005_lev10.0_short: LOO deltas = [-1.6e-05, -5e-06, -1.5e-05, -8e-06, -1.4e-05]
- h72_mmr0.005_lev5.0_long: LOO deltas = [1.3e-05, 2.7e-05, 2.9e-05, 1e-05, 1e-06]
- h72_mmr0.005_lev5.0_short: LOO deltas = [1.9e-05, 3.9e-05, 4.8e-05, 3.3e-05, 2.7e-05]

### Holm correction (family: horizons×MMR×lev×sides, m=16)

- h168_mmr0.004_lev10.0_short: p_raw=0.040000, p_Holm=0.640000, CI95=[0.000007,0.000661], sig_adj=NO
- h168_mmr0.005_lev5.0_long: p_raw=0.042000, p_Holm=0.630000, CI95=[-0.000787,-0.000013], sig_adj=NO
- h168_mmr0.005_lev10.0_short: p_raw=0.045000, p_Holm=0.630000, CI95=[0.000005,0.000716], sig_adj=NO
- h168_mmr0.004_lev5.0_long: p_raw=0.045000, p_Holm=0.585000, CI95=[-0.000781,0.000004], sig_adj=NO
- h168_mmr0.004_lev10.0_long: p_raw=0.048000, p_Holm=0.576000, CI95=[-0.000555,-0.000005], sig_adj=NO
- h72_mmr0.005_lev5.0_short: p_raw=0.049000, p_Holm=0.539000, CI95=[-0.000003,0.000070], sig_adj=NO
- h72_mmr0.005_lev10.0_long: p_raw=0.049000, p_Holm=0.490000, CI95=[-0.000935,0.000007], sig_adj=NO
- h72_mmr0.004_lev10.0_long: p_raw=0.050000, p_Holm=0.450000, CI95=[-0.000908,-0.000008], sig_adj=NO
- h168_mmr0.005_lev5.0_short: p_raw=0.053000, p_Holm=0.424000, CI95=[0.000000,0.000084], sig_adj=NO
- h168_mmr0.005_lev10.0_long: p_raw=0.054000, p_Holm=0.378000, CI95=[-0.000524,0.000001], sig_adj=NO
- h168_mmr0.004_lev5.0_short: p_raw=0.054000, p_Holm=0.324000, CI95=[-0.000002,0.000078], sig_adj=NO
- h72_mmr0.004_lev5.0_short: p_raw=0.055000, p_Holm=0.275000, CI95=[-0.000002,0.000068], sig_adj=NO
- h72_mmr0.004_lev5.0_long: p_raw=0.068000, p_Holm=0.272000, CI95=[-0.000001,0.000043], sig_adj=NO
- h72_mmr0.005_lev5.0_long: p_raw=0.080000, p_Holm=0.240000, CI95=[-0.000002,0.000039], sig_adj=NO
- h72_mmr0.005_lev10.0_short: p_raw=0.097000, p_Holm=0.194000, CI95=[-0.000023,0.000002], sig_adj=NO
- h72_mmr0.004_lev10.0_short: p_raw=0.113000, p_Holm=0.113000, CI95=[-0.000020,0.000001], sig_adj=NO

### Calibration (where base rate permits)
- Lev10 short shows non-degenerate base rates (~0.014-0.028); reliability bins not computed in this pass due to time/complexity; documented as partial.

### Conclusion (inference)
- After block bootstrap + LOO + Holm across declared family, C2 (RV+funding+price-dislocation) does not show robust incremental skill over B0 (RV-only) for modeled boundary breaches on unsealed 2026 panel. Most CIs cross 0; no cell remains significant after Holm adjustment.
- Track separation enforced. No observed liquidation labels used. Intensity target blocked by missing denominators.
