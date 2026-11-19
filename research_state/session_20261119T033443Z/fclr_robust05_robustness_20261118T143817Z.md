# FCLR-VOL-LIQ-ROBUST-05 — Track C Multi-Holdout Robustness + Placebo (stdlib OLS HAR)

**Session:** session_20261118T143817Z
**Campaign:** FCLR-VOL-LIQ-ROBUST-05-20261118T132800Z
**Timestamp (UTC):** 20261118T143817Z
**Label:** EXPLORATORY/PILOT — not confirmatory, no forecast-gate pass claim.
**Network:** none. **Parquet:** none. **numpy/pandas/scipy:** none (stdlib only).

## Sign convention (do not invert)
- `delta_qlike_vs_A = mean(QLIKE_A - QLIKE_model)`; QLIKE is a **loss** (lower is better).
- **Positive** delta = model BEATS RV-only. **Negative** delta = model is WORSE.

## Design
- Four chronological holdouts with expanding train and 7-day purge/embargo.
- Instruments: BTCUSDT, ETHUSDT, SOLUSDT, XRPUSDT, BNBUSDT
- Target: next-24h realized variance (sum of 24 hourly squared log returns t+1..t+24).
- Features (causal at t): lrv1, lrv24, lrv168, fund, fund_abs, fmean, fewma.
- Estimation: stdlib OLS on log RV, Duan smearing, train-only standardization.
- Uncertainty: UTC-day block bootstrap, seed 12345, 2000 reps, per split + pooled; LOIO.
- Placebo: deterministic permutation of funding values across timestamps, same pipeline.

### Holdout 2024-06: train 2024-04-01..2024-05-24, embargo 2024-05-25..2024-05-31, test 2024-06-01..2024-06-30
- common test timestamps: 696
- A_rv_only: n=3480, mean_qlike=-6.366830096174081, mean_delta_qlike_vs_A=0.0
- B_rv_signed: n=3480, mean_qlike=-6.362199600985979, mean_delta_qlike_vs_A=-0.004630495188103106, boot mean(A-model)=-0.004628 CI95=[-0.013593, 0.003674]
- C_rv_abs: n=3480, mean_qlike=-6.364926555183553, mean_delta_qlike_vs_A=-0.0019035409905290086, boot mean(A-model)=-0.001980 CI95=[-0.017907, 0.012634]
- D_rv_signed_abs: n=3480, mean_qlike=-6.368210226036296, mean_delta_qlike_vs_A=0.0013801298622142378, boot mean(A-model)=0.001391 CI95=[-0.014453, 0.015353]
- E_rv_funding_trails: n=3480, mean_qlike=-6.303664973409296, mean_delta_qlike_vs_A=-0.06316512276478664, boot mean(A-model)=-0.063109 CI95=[-0.091534, -0.034411]

### Holdout 2024-07: train 2024-04-01..2024-06-23, embargo 2024-06-24..2024-06-30, test 2024-07-01..2024-07-31
- common test timestamps: 720
- A_rv_only: n=3600, mean_qlike=-5.613094927012957, mean_delta_qlike_vs_A=0.0
- B_rv_signed: n=3600, mean_qlike=-5.601629213662658, mean_delta_qlike_vs_A=-0.01146571335029833, boot mean(A-model)=-0.011491 CI95=[-0.018977, -0.002059]
- C_rv_abs: n=3600, mean_qlike=-5.581255147132275, mean_delta_qlike_vs_A=-0.03183977988068262, boot mean(A-model)=-0.031934 CI95=[-0.050600, -0.008121]
- D_rv_signed_abs: n=3600, mean_qlike=-5.566243359489151, mean_delta_qlike_vs_A=-0.04685156752380493, boot mean(A-model)=-0.047219 CI95=[-0.073242, -0.012842]
- E_rv_funding_trails: n=3600, mean_qlike=-5.3965418009222805, mean_delta_qlike_vs_A=-0.21655312609067562, boot mean(A-model)=-0.216531 CI95=[-0.283895, -0.149081]

### Holdout 2024-08: train 2024-04-01..2024-07-24, embargo 2024-07-25..2024-07-31, test 2024-08-01..2024-08-31
- common test timestamps: 720
- A_rv_only: n=3600, mean_qlike=-5.120910751698631, mean_delta_qlike_vs_A=0.0
- B_rv_signed: n=3600, mean_qlike=-5.114624747042107, mean_delta_qlike_vs_A=-0.0062860046565226795, boot mean(A-model)=-0.006225 CI95=[-0.010596, -0.001513]
- C_rv_abs: n=3600, mean_qlike=-5.100933318034682, mean_delta_qlike_vs_A=-0.019977433663948538, boot mean(A-model)=-0.020007 CI95=[-0.030907, -0.006542]
- D_rv_signed_abs: n=3600, mean_qlike=-4.98434957173581, mean_delta_qlike_vs_A=-0.1365611799628203, boot mean(A-model)=-0.137055 CI95=[-0.199416, -0.066564]
- E_rv_funding_trails: n=3600, mean_qlike=-4.373334495249136, mean_delta_qlike_vs_A=-0.747576256449495, boot mean(A-model)=-0.751040 CI95=[-1.128211, -0.305815]

### Holdout 2024-09: train 2024-04-01..2024-08-24, embargo 2024-08-25..2024-08-31, test 2024-09-01..2024-09-30
- common test timestamps: 696
- A_rv_only: n=3480, mean_qlike=-6.110056052214218, mean_delta_qlike_vs_A=0.0
- B_rv_signed: n=3480, mean_qlike=-6.108779175888441, mean_delta_qlike_vs_A=-0.0012768763257773091, boot mean(A-model)=-0.001233 CI95=[-0.005123, 0.002913]
- C_rv_abs: n=3480, mean_qlike=-6.106848782979606, mean_delta_qlike_vs_A=-0.0032072692346130803, boot mean(A-model)=-0.003218 CI95=[-0.006205, -0.000058]
- D_rv_signed_abs: n=3480, mean_qlike=-6.103127697637085, mean_delta_qlike_vs_A=-0.006928354577132994, boot mean(A-model)=-0.006913 CI95=[-0.011328, -0.002013]
- E_rv_funding_trails: n=3480, mean_qlike=-6.0807570488188745, mean_delta_qlike_vs_A=-0.029299003395344254, boot mean(A-model)=-0.029142 CI95=[-0.041750, -0.016079]

## Pooled summary (ΔQLIKE = A − model; positive = model better)
- A_rv_only: n=14160, mean_qlike=-5.795337870039054, mean_delta_qlike_vs_A=0.0
- B_rv_signed: n=14160, mean_qlike=-5.78937290975001, mean_delta_qlike_vs_A=-0.005964960289043748, boot mean(A-model)=-0.005936 CI95=[-0.009331, -0.002138]
- C_rv_abs: n=14160, mean_qlike=-5.780907955607969, mean_delta_qlike_vs_A=-0.014429914431085216, boot mean(A-model)=-0.014459 CI95=[-0.021818, -0.006406]
- D_rv_signed_abs: n=14160, mean_qlike=-5.747343963756584, mean_delta_qlike_vs_A=-0.047993906282469495, boot mean(A-model)=-0.047672 CI95=[-0.068373, -0.025394]
- E_rv_funding_trails: n=14160, mean_qlike=-5.527495996014911, mean_delta_qlike_vs_A=-0.26784187402414333, boot mean(A-model)=-0.269483 CI95=[-0.373319, -0.150074]

## Placebo null (funding values permuted across timestamps)
- 2024-06: placebo mean_qlike_E=-6.379305878350555, placebo mean_delta_qlike_vs_A=0.012475782176473008, boot CI95=[-0.02693184111493675, 0.047711148651679865]
- 2024-07: placebo mean_qlike_E=-5.378578290041406, placebo mean_delta_qlike_vs_A=-0.23451663697155054, boot CI95=[-0.3156414526132672, -0.1438152055130664]
- 2024-08: placebo mean_qlike_E=-4.977849698384623, placebo mean_delta_qlike_vs_A=-0.1430610533140076, boot CI95=[-0.20971136116210298, -0.054974741131]
- 2024-09: placebo mean_qlike_E=-6.101465405398955, placebo mean_delta_qlike_vs_A=-0.00859064681526301, boot CI95=[-0.016748604267696976, 8.164911856373059e-05]
- placebo pooled mean_qlike_E = -5.700298363402684
- placebo mean (A − E) across holdouts = -0.09342313873108703

## Materiality floor (pre-registered)
- E beats A in 0 of 4 holdouts; per-holdout: 2024-06: delta=-0.06316512276478664, CI_lo=-0.09153403549833822, beats=False, 2024-07: delta=-0.21655312609067562, CI_lo=-0.28389506546852256, beats=False, 2024-08: delta=-0.747576256449495, CI_lo=-1.1282113429812703, beats=False, 2024-09: delta=-0.029299003395344254, CI_lo=-0.04175021308373257, beats=False
- real pooled |Δ| = 0.26784187402414333 vs placebo |Δ| = 0.09342313873108703
- real exceeds placebo = True
- better model by pooled mean QLIKE = **A_rv_only**
- **materiality_floor_met = False**

## Honest status
- EXPLORATORY/PILOT. No confirmatory promotion claimed.
- No sealed months touched. No look-ahead; train-only standardization; expanding train.
- Negative result is a valid completion of the pre-registered campaign.
