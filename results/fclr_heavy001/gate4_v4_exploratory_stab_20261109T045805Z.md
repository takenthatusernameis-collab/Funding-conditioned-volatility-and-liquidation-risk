# Gate 4 v4 EXPLORATORY stabilized comparison — 20261109T045805Z

**EXPLORATORY / NOT CONFIRMATORY / NOT PROMOTABLE**
- Git SHA: `d7a764b9e9411f58b8dca3abe8251f6780c5d6d4`
- Prereg: `research_state/pre_registration_gate4_funding_multisplit_v4_20261107T1845Z.json` — `FROZEN_BEFORE_OUTCOMES`, `confirmatory_claim_go=NO_GO`, `exploratory_smoke_authorized_after_freeze=true`
- Does NOT replace prereg A-E contrasts or change confirmatory estimands. No confirmatory GO / economic value / promotion.
- Leakage controls preserved: chronological multi-split, purge/embargo as prereg v3_30d, train-only normalization (`wf.apply_train_only_normalization`), train-only ridge scale/winsor/floor parameters, block bootstrap by UTC time blocks.

## Variants (EXPLORATORY, fixed rules)
- V1_primary: ridge=1e-10*I, floor 0 (matches primary fit).
- V2_scale_ridge: ridge=1e-8*max(trace(X'X)/k,1)*I, floor 0.
- V3_scale_ridge_target_floor: V2 + train-only floor max(0,1e-4*train_target_median) per instrument/split.
- V4_winsor_train: V3 + train-only standardized-feature winsor q0.5/q99.5 (train bounds applied to train/test).

## Pooled ΔQLIKE vs A (alt-base; negative better for alt), 95% block bootstrap CI
| Variant | Contrast | Point | CI low | CI high | n_obs | n_blocks | Verdict (EXPLORATORY) |
|---|---|---:|---:|---:|---:|---:|---|
| V1_primary | B_rv_signed | 11.110522836791604 | 0.48052288989834724 | 32.31258287470994 | 13620 | 120 | alt worse (CI>0) |
| V1_primary | C_rv_abs | -0.024710146016296737 | -0.37159501419659596 | 0.2707987870777838 | 13985 | 120 | inconclusive (CI spans 0) |
| V1_primary | D_rv_signed_abs | 2.421918112567877 | -0.2539600556711275 | 7.512202570277498 | 13269 | 120 | inconclusive (CI spans 0) |
| V1_primary | E_rv_funding_trails | 0.4879023125557301 | -0.04216077732548571 | 1.1973379300275868 | 12969 | 120 | inconclusive (CI spans 0) |
| V2_scale_ridge | B_rv_signed | 11.067703657521898 | 0.48051701921883 | 32.18292126455609 | 13620 | 120 | alt worse (CI>0) |
| V2_scale_ridge | C_rv_abs | -0.02470957499162285 | -0.3715910651166797 | 0.27079736999232146 | 13985 | 120 | inconclusive (CI spans 0) |
| V2_scale_ridge | D_rv_signed_abs | 2.393068548013342 | -0.2539575108344221 | 7.425151210308135 | 13269 | 120 | inconclusive (CI spans 0) |
| V2_scale_ridge | E_rv_funding_trails | 0.48785883377919703 | -0.04217381127818388 | 1.197250470465031 | 12969 | 120 | inconclusive (CI spans 0) |
| V3_scale_ridge_target_floor | B_rv_signed | 319.54341011288415 | 157.0627730378603 | 501.87895230619074 | 14400 | 120 | alt worse (CI>0) |
| V3_scale_ridge_target_floor | C_rv_abs | -59.59570823984368 | -147.9408125763792 | -1.6109173431837522 | 14400 | 120 | alt better (CI<0) |
| V3_scale_ridge_target_floor | D_rv_signed_abs | 517.9000824804125 | 79.15123340084074 | 976.4031459125539 | 14400 | 120 | alt worse (CI>0) |
| V3_scale_ridge_target_floor | E_rv_funding_trails | 1096.4323968982128 | 330.8633563340269 | 2103.866327919272 | 14400 | 120 | alt worse (CI>0) |
| V4_winsor_train | B_rv_signed | 514.0855424810592 | 368.8462036087277 | 665.2487776650739 | 14400 | 120 | alt worse (CI>0) |
| V4_winsor_train | C_rv_abs | -61.05685478872567 | -171.67747935604504 | 33.66368825482879 | 14400 | 120 | inconclusive (CI spans 0) |
| V4_winsor_train | D_rv_signed_abs | 386.20595356655224 | 14.997418094786958 | 761.2598958999341 | 14400 | 120 | alt worse (CI>0) |
| V4_winsor_train | E_rv_funding_trails | 1421.4959744699004 | 414.2215207833895 | 2994.9173799203486 | 14400 | 120 | alt worse (CI>0) |

## E vs A instrument LOO (V3, EXPLORATORY)
| LOO | Point | CI low | CI high | n_obs |
|---|---:|---:|---:|---:|
| all | 1096.4323968982128 | 330.8633563340269 | 2103.866327919272 | 14400 |
| drop_BTCUSDT | 1050.1403337194006 | 166.76094884314833 | 2255.2460936330053 | 11520 |
| drop_ETHUSDT | 1174.322082008321 | 254.44746705753317 | 2376.0695373494864 | 11520 |
| drop_SOLUSDT | 1272.0512066823098 | 435.53886888215186 | 2476.2219036782094 | 11520 |
| drop_XRPUSDT | 343.8127618423249 | -131.78461150663372 | 813.7731751336344 | 11520 |
| drop_BNBUSDT | 2024.7789450151156 | 813.6580273697282 | 3946.136352587911 | 11520 |

## Split-3 B/D/E diagnostics (V1 vs V3, selected)

### V1_primary split 3
- A_rv_only: qlike=0.9746929691197167 valid_n=3579 n=3600
  - BNBUSDT: ql=0.17754525966604837 raw_neg=0/720 coef_max=0.000988237612494518 floor=max(p,0)
  - BTCUSDT: ql=3.8911191975277926 raw_neg=21/720 coef_max=0.00145020875742801 floor=max(p,0)
  - ETHUSDT: ql=0.2771222580615486 raw_neg=0/720 coef_max=0.0007191613769537409 floor=max(p,0)
  - SOLUSDT: ql=0.21153131228623934 raw_neg=0/720 coef_max=0.0011235896905505394 floor=max(p,0)
  - XRPUSDT: ql=0.4012092497188567 raw_neg=0/720 coef_max=0.000769540837911244 floor=max(p,0)
- B_rv_signed: qlike=45.0003731898787 valid_n=3288 n=3600
  - BNBUSDT: ql=0.1734991789632053 raw_neg=0/720 coef_max=0.0009239804100740898 floor=max(p,0)
  - BTCUSDT: ql=225.80010799533534 raw_neg=89/720 coef_max=0.0012681007236079224 floor=max(p,0)
  - ETHUSDT: ql=2.719843282194781 raw_neg=53/720 coef_max=0.0011598953557048419 floor=max(p,0)
  - SOLUSDT: ql=5.233353623859102 raw_neg=125/720 coef_max=0.0016136816440517961 floor=max(p,0)
  - XRPUSDT: ql=0.6347535096162674 raw_neg=45/720 coef_max=0.0010134819548684808 floor=max(p,0)
- D_rv_signed_abs: qlike=11.285365689575759 valid_n=3024 n=3600
  - BNBUSDT: ql=0.20287734788146045 raw_neg=0/720 coef_max=0.0008919884290264835 floor=max(p,0)
  - BTCUSDT: ql=1.6846908618062455 raw_neg=275/720 coef_max=0.0031501395720951223 floor=max(p,0)
  - ETHUSDT: ql=0.5250572929543632 raw_neg=90/720 coef_max=0.004091345140969719 floor=max(p,0)
  - SOLUSDT: ql=56.342413198111075 raw_neg=142/720 coef_max=0.0043096305677196925 floor=max(p,0)
  - XRPUSDT: ql=0.5138030694765162 raw_neg=69/720 coef_max=0.0029992586412832855 floor=max(p,0)
- E_rv_funding_trails: qlike=1.5020435559282244 valid_n=2978 n=3600
  - BNBUSDT: ql=0.28866627824062807 raw_neg=19/720 coef_max=0.0008997746574056509 floor=max(p,0)
  - BTCUSDT: ql=3.856614148900415 raw_neg=279/720 coef_max=0.003208545077931594 floor=max(p,0)
  - ETHUSDT: ql=0.8614548946497643 raw_neg=88/720 coef_max=0.003953904522795021 floor=max(p,0)
  - SOLUSDT: ql=2.456600121728104 raw_neg=137/720 coef_max=0.005113118402193317 floor=max(p,0)
  - XRPUSDT: ql=0.9554371086253677 raw_neg=99/720 coef_max=0.0037392380363616305 floor=max(p,0)
### V3_scale_ridge_target_floor split 3
- A_rv_only: qlike=112.99356151442291 valid_n=3600 n=3600
  - BNBUSDT: ql=0.17754525939464152 raw_neg=0/720 coef_max=0.0009882375929855692 floor=max(p,1e-4*train_target_median=5.59152e-08) (train-only)
  - BTCUSDT: ql=563.900399495224 raw_neg=21/720 coef_max=0.0014502087287511514 floor=max(p,1e-4*train_target_median=4.81847e-08) (train-only)
  - ETHUSDT: ql=0.2771222559420358 raw_neg=0/720 coef_max=0.0007191613545780111 floor=max(p,1e-4*train_target_median=6.46763e-08) (train-only)
  - SOLUSDT: ql=0.21153131123064106 raw_neg=0/720 coef_max=0.0011235896733676031 floor=max(p,1e-4*train_target_median=1.47154e-07) (train-only)
  - XRPUSDT: ql=0.4012092503232095 raw_neg=0/720 coef_max=0.0007695408268338738 floor=max(p,1e-4*train_target_median=6.11191e-08) (train-only)
- B_rv_signed: qlike=1028.5751046076339 valid_n=3600 n=3600
  - BNBUSDT: ql=0.17349917742784843 raw_neg=0/720 coef_max=0.0009239803782507928 floor=max(p,1e-4*train_target_median=5.59152e-08) (train-only)
  - BTCUSDT: ql=1944.1579382505345 raw_neg=89/720 coef_max=0.001268100698078742 floor=max(p,1e-4*train_target_median=4.81847e-08) (train-only)
  - ETHUSDT: ql=891.8287044651507 raw_neg=53/720 coef_max=0.001159895328157822 floor=max(p,1e-4*train_target_median=6.46763e-08) (train-only)
  - SOLUSDT: ql=1611.7966721145278 raw_neg=125/720 coef_max=0.0016136815711105758 floor=max(p,1e-4*train_target_median=1.47154e-07) (train-only)
  - XRPUSDT: ql=694.9187090305289 raw_neg=45/720 coef_max=0.0010134819105404335 floor=max(p,1e-4*train_target_median=6.11191e-08) (train-only)
- D_rv_signed_abs: qlike=1996.8258496657752 valid_n=3600 n=3600
  - BNBUSDT: ql=0.20287734628164683 raw_neg=0/720 coef_max=0.0008919883920358403 floor=max(p,1e-4*train_target_median=5.59152e-08) (train-only)
  - BTCUSDT: ql=5497.587538785964 raw_neg=275/720 coef_max=0.003150139222247732 floor=max(p,1e-4*train_target_median=4.81847e-08) (train-only)
  - ETHUSDT: ql=1602.9063160938256 raw_neg=90/720 coef_max=0.004091344777981078 floor=max(p,1e-4*train_target_median=6.46763e-08) (train-only)
  - SOLUSDT: ql=1869.0853014743916 raw_neg=142/720 coef_max=0.004309629587749614 floor=max(p,1e-4*train_target_median=1.47154e-07) (train-only)
  - XRPUSDT: ql=1014.3472146284134 raw_neg=69/720 coef_max=0.0029992580748255697 floor=max(p,1e-4*train_target_median=6.11191e-08) (train-only)
- E_rv_funding_trails: qlike=2113.906925022571 valid_n=3600 n=3600
  - BNBUSDT: ql=314.61355734818096 raw_neg=19/720 coef_max=0.0008997746334339 floor=max(p,1e-4*train_target_median=5.59152e-08) (train-only)
  - BTCUSDT: ql=5603.956403062011 raw_neg=279/720 coef_max=0.003208544100149672 floor=max(p,1e-4*train_target_median=4.81847e-08) (train-only)
  - ETHUSDT: ql=1567.3211056150408 raw_neg=88/720 coef_max=0.0039539039174746144 floor=max(p,1e-4*train_target_median=6.46763e-08) (train-only)
  - SOLUSDT: ql=1808.7260965951698 raw_neg=137/720 coef_max=0.005113117299052905 floor=max(p,1e-4*train_target_median=1.47154e-07) (train-only)
  - XRPUSDT: ql=1274.9174624924524 raw_neg=99/720 coef_max=0.0037392374299145357 floor=max(p,1e-4*train_target_median=6.11191e-08) (train-only)

## Interpretation (EXPLORATORY ONLY — NOT CONFIRMATORY)
V1 E vs A point=0.4879023125557301 CI=[-0.04216077732548571,1.1973379300275868] (inconclusive). V3 (scale-aware ridge + train-only target-scale floor) E vs A point=1096.4323968982128 CI=[330.8633563340269,2103.866327919272] (not spanning 0). V3 E vs A LOO (EXPLORATORY): all=1096.4323968982128; no LOO shows a CI entirely below 0=True. V3 B vs A point=319.54341011288415 CI=[157.0627730378603,501.87895230619074]. Split 3 B QLIKE V1=45.0003731898787 -> V3=1028.5751046076339 (EXPLORATORY diagnostic).

Artifacts: `research_state/gate4_v4_exploratory_stab/gate4_v4_exploratory_stab_20261109T045805Z.json`, `/home/runner/work/Funding-conditioned-volatility-and-liquidation-risk/Funding-conditioned-volatility-and-liquidation-risk/results/fclr_heavy001/gate4_v4_exploratory_stab_20261109T045805Z.md`
