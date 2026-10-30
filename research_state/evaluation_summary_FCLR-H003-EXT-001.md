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