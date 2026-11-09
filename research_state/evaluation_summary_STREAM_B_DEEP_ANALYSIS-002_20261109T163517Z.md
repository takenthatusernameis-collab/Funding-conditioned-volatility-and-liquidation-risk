# STREAM_B_DEEP_ANALYSIS-002 - 20261109T163522Z

## Context
- Panel: /home/runner/work/Funding-conditioned-volatility-and-liquidation-risk/Funding-conditioned-volatility-and-liquidation-risk/research_state/data_cache/fclr002_panel.json (FCLR-002, frozen)
- Symbols: ['BNBUSDT', 'BTCUSDT', 'ETHUSDT', 'SOLUSDT', 'XRPUSDT'] (n=5)
- Splits: {'train': ['2024-04-01T00:00:00Z', '2024-06-08T23:00:00Z'], 'val': ['2024-06-16T00:00:00Z', '2024-07-15T23:00:00Z'], 'test': ['2024-07-23T00:00:00Z', '2024-09-30T23:00:00Z']}
- Train/Test: 7608/8280
- Constraint: leakage-resistant (train-only funding quartile thresholds + normalization, trailing-only features, chronological splits). No sealed panel re-runs.
- Block count: FCLR-002 test = 2 non-overlapping 30-day blocks (< 3) -> regime-stratified results are EXPLORATORY only, not confirmatory.

## 1) Funding |.| quartile thresholds (TRAIN only, no look-ahead)
- Train n=7608 |fund| quartiles: Q1 boundary=5.114e-05, Q2 (median)=0.0001, Q3 boundary=0.0001
- Regime rule (per symbol, train thresholds applied to test): Q1 = most negative signed funding .. Q4 = most positive signed funding, using abs(|fund|) quartile bins on signed funding sign.

## 2) Regime-stratified QLIKE per symbol per funding regime (TEST)
| Symbol | Regime | n | B1 QLIKE | C2_all QLIKE | rel_imp_vs_B1 | diff(C2-B1) | 95% CI (diff) | CI_excludes0 |
|--------|--------|---|----------|--------------|---------------|--------------|---------------|--------------|
| BNBUSDT | Q1_low_abs_neg | 49 | 0.097936 | 0.100263 | -2.376% | 0.002327 | [-0.009040,0.012746] | NO |
| BNBUSDT | Q1_low_abs_pos | 1440 | 0.588247 | 0.558356 | +5.081% | -0.029891 | [-0.061359,-0.006366] | YES |
| BNBUSDT | Q2_neg | 34 | 0.260563 | 0.261527 | -0.370% | 0.000964 | [-0.034085,0.035673] | NO |
| BNBUSDT | Q2_pos | 22 | 0.442049 | 0.482699 | -9.196% | 0.040650 | [0.040650,0.040650] | NO |
| BNBUSDT | Q4_high_abs_neg | 111 | 0.239632 | 0.254609 | -6.250% | 0.014977 | [-0.025744,0.053660] | NO |
| BTCUSDT | Q1_low_abs_neg | 374 | 0.652235 | 0.634653 | +2.696% | -0.017581 | [-0.071961,0.018251] | NO |
| BTCUSDT | Q1_low_abs_pos | 656 | 0.801553 | 0.766491 | +4.374% | -0.035062 | [-0.067655,-0.008086] | YES |
| BTCUSDT | Q2_neg | 151 | 0.368099 | 0.345984 | +6.008% | -0.022115 | [-0.070669,0.016052] | NO |
| BTCUSDT | Q2_pos | 467 | 0.898212 | 0.860093 | +4.244% | -0.038119 | [-0.100127,-0.000064] | YES |
| BTCUSDT | Q4_high_abs_neg | 8 | 0.234558 | 0.310498 | -32.375% | 0.075939 | [0.075939,0.075939] | NO |
| ETHUSDT | Q1_low_abs_neg | 306 | 0.495473 | 0.496619 | -0.231% | 0.001147 | [-0.035905,0.038624] | NO |
| ETHUSDT | Q1_low_abs_pos | 729 | 1.065445 | 1.003482 | +5.816% | -0.061962 | [-0.134497,-0.013016] | YES |
| ETHUSDT | Q2_neg | 31 | 0.230709 | 0.291191 | -26.215% | 0.060481 | [0.026449,0.095218] | NO |
| ETHUSDT | Q2_pos | 582 | 0.657506 | 0.620213 | +5.672% | -0.037292 | [-0.073519,-0.008381] | YES |
| ETHUSDT | Q4_high_abs_neg | 8 | 0.721194 | 0.855057 | -18.561% | 0.133864 | [0.133864,0.133864] | NO |
| SOLUSDT | Q1_low_abs_neg | 340 | 0.430979 | 0.419781 | +2.598% | -0.011197 | [-0.056987,0.023107] | NO |
| SOLUSDT | Q1_low_abs_pos | 554 | 0.410669 | 0.382238 | +6.923% | -0.028430 | [-0.049364,-0.009897] | YES |
| SOLUSDT | Q2_neg | 103 | 0.401943 | 0.407674 | -1.426% | 0.005731 | [-0.039244,0.051253] | NO |
| SOLUSDT | Q2_pos | 651 | 0.277063 | 0.265178 | +4.289% | -0.011884 | [-0.031231,0.004036] | NO |
| SOLUSDT | Q4_high_abs_neg | 8 | 0.046660 | 0.048415 | -3.761% | 0.001755 | [0.001755,0.001755] | NO |
| XRPUSDT | Q1_low_abs_neg | 189 | 2.068948 | 1.878771 | +9.192% | -0.190177 | [-0.418925,-0.040327] | YES |
| XRPUSDT | Q1_low_abs_pos | 509 | 0.907574 | 0.858839 | +5.370% | -0.048735 | [-0.091247,-0.016444] | YES |
| XRPUSDT | Q2_neg | 66 | 0.381811 | 0.441003 | -15.503% | 0.059192 | [0.025684,0.088393] | NO |
| XRPUSDT | Q2_pos | 859 | 0.603740 | 0.587891 | +2.625% | -0.015849 | [-0.032380,-0.000709] | YES |
| XRPUSDT | Q4_high_abs_neg | 33 | 0.766571 | 0.750175 | +2.139% | -0.016395 | [-0.114899,0.082188] | NO |

## 3) Interaction/ablation per regime (TEST, incremental contribution)
| Symbol | Regime | Model | QLIKE | rel_imp_vs_B1 | diff_vs_C2_all | 95% CI vs B1 | CI_excludes0 |
|--------|--------|-------|-------|---------------|----------------|--------------|--------------|
| BNBUSDT | Q1_low_abs_neg | A1_fundpctz | 0.095911 | +2.067% | -0.421431 | [-0.008468,0.003859] | NO |
| BNBUSDT | Q1_low_abs_neg | A3_pricedisloc | 0.098208 | -0.278% | -0.419134 | [-0.006111,0.006372] | NO |
| BNBUSDT | Q1_low_abs_neg | C1 | 0.097315 | +0.634% | -0.420027 | [-0.002388,0.001103] | NO |
| BNBUSDT | Q1_low_abs_neg | I1_fund_x_rvregime | 0.096163 | +1.810% | -0.421179 | [-0.008386,0.004239] | NO |
| BNBUSDT | Q1_low_abs_neg | I2_fund_x_disloc | 0.096433 | +1.535% | -0.420909 | [-0.008776,0.005145] | NO |
| BNBUSDT | Q1_low_abs_pos | A1_fundpctz | 0.564982 | +3.955% | +0.047641 | [-0.037503,-0.011289] | YES |
| BNBUSDT | Q1_low_abs_pos | A3_pricedisloc | 0.571576 | +2.834% | +0.054234 | [-0.037047,-0.003140] | YES |
| BNBUSDT | Q1_low_abs_pos | C1 | 0.580211 | +1.366% | +0.062869 | [-0.013016,-0.003897] | YES |
| BNBUSDT | Q1_low_abs_pos | I1_fund_x_rvregime | 0.565095 | +3.936% | +0.047753 | [-0.037675,-0.010934] | YES |
| BNBUSDT | Q1_low_abs_pos | I2_fund_x_disloc | 0.563291 | +4.242% | +0.045949 | [-0.040983,-0.011675] | YES |
| BNBUSDT | Q2_neg | A1_fundpctz | 0.258340 | +0.853% | -0.259002 | [-0.029212,0.024248] | NO |
| BNBUSDT | Q2_neg | A3_pricedisloc | 0.261391 | -0.318% | -0.255951 | [-0.008583,0.010235] | NO |
| BNBUSDT | Q2_neg | C1 | 0.259285 | +0.490% | -0.258057 | [-0.014370,0.011567] | NO |
| BNBUSDT | Q2_neg | I1_fund_x_rvregime | 0.258749 | +0.696% | -0.258593 | [-0.028979,0.024990] | NO |
| BNBUSDT | Q2_neg | I2_fund_x_disloc | 0.259004 | +0.598% | -0.258338 | [-0.030543,0.026797] | NO |
| BNBUSDT | Q2_pos | A1_fundpctz | 0.464870 | -5.163% | -0.052472 | [0.022821,0.022821] | NO |
| BNBUSDT | Q2_pos | A3_pricedisloc | 0.457419 | -3.477% | -0.059923 | [0.015370,0.015370] | NO |
| BNBUSDT | Q2_pos | C1 | 0.444150 | -0.475% | -0.073192 | [0.002101,0.002101] | NO |
| BNBUSDT | Q2_pos | I1_fund_x_rvregime | 0.464899 | -5.169% | -0.052443 | [0.022850,0.022850] | NO |
| BNBUSDT | Q2_pos | I2_fund_x_disloc | 0.465202 | -5.238% | -0.052139 | [0.023154,0.023154] | NO |
| BNBUSDT | Q4_high_abs_neg | A1_fundpctz | 0.246493 | -2.863% | -0.270849 | [-0.027650,0.039092] | NO |
| BNBUSDT | Q4_high_abs_neg | A3_pricedisloc | 0.241662 | -0.847% | -0.275680 | [-0.006000,0.009270] | NO |
| BNBUSDT | Q4_high_abs_neg | C1 | 0.242079 | -1.021% | -0.275263 | [-0.020246,0.023090] | NO |
| BNBUSDT | Q4_high_abs_neg | I1_fund_x_rvregime | 0.248297 | -3.616% | -0.269045 | [-0.026726,0.041953] | NO |
| BNBUSDT | Q4_high_abs_neg | I2_fund_x_disloc | 0.248021 | -3.501% | -0.269321 | [-0.030141,0.043948] | NO |
| BTCUSDT | Q1_low_abs_neg | A1_fundpctz | 0.626507 | +3.945% | -0.096059 | [-0.074650,0.005976] | NO |
| BTCUSDT | Q1_low_abs_neg | A3_pricedisloc | 0.648947 | +0.504% | -0.073619 | [-0.019406,0.007489] | NO |
| BTCUSDT | Q1_low_abs_neg | C1 | 0.645727 | +0.998% | -0.076838 | [-0.018224,0.001182] | NO |
| BTCUSDT | Q1_low_abs_neg | I1_fund_x_rvregime | 0.627003 | +3.868% | -0.095563 | [-0.074155,0.006484] | NO |
| BTCUSDT | Q1_low_abs_neg | I2_fund_x_disloc | 0.626389 | +3.963% | -0.096177 | [-0.076603,0.007151] | NO |
| BTCUSDT | Q1_low_abs_pos | A1_fundpctz | 0.764437 | +4.631% | +0.041871 | [-0.063643,-0.015263] | YES |
| BTCUSDT | Q1_low_abs_pos | A3_pricedisloc | 0.787740 | +1.723% | +0.065174 | [-0.029132,-0.001305] | YES |
| BTCUSDT | Q1_low_abs_pos | C1 | 0.796208 | +0.667% | +0.073642 | [-0.009949,-0.001720] | YES |
| BTCUSDT | Q1_low_abs_pos | I1_fund_x_rvregime | 0.764572 | +4.614% | +0.042006 | [-0.063535,-0.015119] | YES |
| BTCUSDT | Q1_low_abs_pos | I2_fund_x_disloc | 0.763744 | +4.717% | +0.041178 | [-0.065108,-0.015250] | YES |
| BTCUSDT | Q2_neg | A1_fundpctz | 0.342678 | +6.906% | -0.379888 | [-0.062726,0.006923] | NO |
| BTCUSDT | Q2_neg | A3_pricedisloc | 0.362402 | +1.548% | -0.360164 | [-0.013938,0.002369] | NO |
| BTCUSDT | Q2_neg | C1 | 0.358355 | +2.647% | -0.364211 | [-0.022541,0.001491] | NO |
| BTCUSDT | Q2_neg | I1_fund_x_rvregime | 0.343350 | +6.724% | -0.379216 | [-0.062260,0.007767] | NO |
| BTCUSDT | Q2_neg | I2_fund_x_disloc | 0.341939 | +7.107% | -0.380627 | [-0.065326,0.007923] | NO |
| BTCUSDT | Q2_pos | A1_fundpctz | 0.869508 | +3.196% | +0.146942 | [-0.063341,-0.004875] | YES |
| BTCUSDT | Q2_pos | A3_pricedisloc | 0.873164 | +2.789% | +0.150598 | [-0.059822,-0.002304] | YES |
| BTCUSDT | Q2_pos | C1 | 0.888604 | +1.070% | +0.166038 | [-0.018636,-0.002508] | YES |
| BTCUSDT | Q2_pos | I1_fund_x_rvregime | 0.869461 | +3.201% | +0.146895 | [-0.063638,-0.004741] | YES |
| BTCUSDT | Q2_pos | I2_fund_x_disloc | 0.867119 | +3.462% | +0.144553 | [-0.069080,-0.005084] | YES |
| BTCUSDT | Q4_high_abs_neg | A1_fundpctz | 0.298772 | -27.376% | -0.423794 | [0.064213,0.064213] | NO |
| BTCUSDT | Q4_high_abs_neg | A3_pricedisloc | 0.242228 | -3.270% | -0.480338 | [0.007670,0.007670] | NO |
| BTCUSDT | Q4_high_abs_neg | C1 | 0.258744 | -10.311% | -0.463822 | [0.024185,0.024185] | NO |
| BTCUSDT | Q4_high_abs_neg | I1_fund_x_rvregime | 0.300205 | -27.987% | -0.422361 | [0.065647,0.065647] | NO |
| BTCUSDT | Q4_high_abs_neg | I2_fund_x_disloc | 0.301614 | -28.588% | -0.420951 | [0.067056,0.067056] | NO |
| ETHUSDT | Q1_low_abs_neg | A1_fundpctz | 0.483455 | +2.426% | -0.277617 | [-0.041429,0.014686] | NO |
| ETHUSDT | Q1_low_abs_neg | A3_pricedisloc | 0.496252 | -0.157% | -0.264820 | [-0.013213,0.014556] | NO |
| ETHUSDT | Q1_low_abs_neg | C1 | 0.492095 | +0.682% | -0.268978 | [-0.010750,0.003151] | NO |
| ETHUSDT | Q1_low_abs_neg | I1_fund_x_rvregime | 0.484204 | +2.274% | -0.276869 | [-0.040638,0.016057] | NO |
| ETHUSDT | Q1_low_abs_neg | I2_fund_x_disloc | 0.483687 | +2.379% | -0.277385 | [-0.042207,0.016453] | NO |
| ETHUSDT | Q1_low_abs_pos | A1_fundpctz | 1.013086 | +4.914% | +0.252014 | [-0.103981,-0.014188] | YES |
| ETHUSDT | Q1_low_abs_pos | A3_pricedisloc | 1.039990 | +2.389% | +0.278918 | [-0.053198,-0.004498] | YES |
| ETHUSDT | Q1_low_abs_pos | C1 | 1.059644 | +0.544% | +0.298572 | [-0.011421,-0.001488] | YES |
| ETHUSDT | Q1_low_abs_pos | I1_fund_x_rvregime | 1.013226 | +4.901% | +0.252153 | [-0.103902,-0.014083] | YES |
| ETHUSDT | Q1_low_abs_pos | I2_fund_x_disloc | 1.012279 | +4.990% | +0.251207 | [-0.105672,-0.014381] | YES |
| ETHUSDT | Q2_neg | A1_fundpctz | 0.262146 | -13.626% | -0.498926 | [0.012651,0.050778] | NO |
| ETHUSDT | Q2_neg | A3_pricedisloc | 0.238945 | -3.570% | -0.522127 | [0.001955,0.014467] | NO |
| ETHUSDT | Q2_neg | C1 | 0.239232 | -3.694% | -0.521841 | [0.002847,0.014312] | NO |
| ETHUSDT | Q2_neg | I1_fund_x_rvregime | 0.267587 | -15.984% | -0.493485 | [0.014537,0.059218] | NO |
| ETHUSDT | Q2_neg | I2_fund_x_disloc | 0.264605 | -14.692% | -0.496467 | [0.014056,0.054008] | NO |
| ETHUSDT | Q2_pos | A1_fundpctz | 0.636505 | +3.194% | -0.124567 | [-0.033454,-0.009222] | YES |
| ETHUSDT | Q2_pos | A3_pricedisloc | 0.631120 | +4.013% | -0.129953 | [-0.056113,-0.005613] | YES |
| ETHUSDT | Q2_pos | C1 | 0.650814 | +1.018% | -0.110258 | [-0.011357,-0.002465] | YES |
| ETHUSDT | Q2_pos | I1_fund_x_rvregime | 0.636535 | +3.189% | -0.124538 | [-0.033745,-0.009035] | YES |
| ETHUSDT | Q2_pos | I2_fund_x_disloc | 0.634952 | +3.430% | -0.126120 | [-0.036506,-0.009461] | YES |
| ETHUSDT | Q4_high_abs_neg | A1_fundpctz | 0.818117 | -13.439% | +0.057045 | [0.096923,0.096923] | NO |
| ETHUSDT | Q4_high_abs_neg | A3_pricedisloc | 0.745905 | -3.426% | -0.015168 | [0.024711,0.024711] | NO |
| ETHUSDT | Q4_high_abs_neg | C1 | 0.755051 | -4.695% | -0.006021 | [0.033857,0.033857] | NO |
| ETHUSDT | Q4_high_abs_neg | I1_fund_x_rvregime | 0.824567 | -14.334% | +0.063495 | [0.103374,0.103374] | NO |
| ETHUSDT | Q4_high_abs_neg | I2_fund_x_disloc | 0.826277 | -14.571% | +0.065205 | [0.105084,0.105084] | NO |
| SOLUSDT | Q1_low_abs_neg | A1_fundpctz | 0.419227 | +2.727% | +0.075330 | [-0.039224,0.013165] | NO |
| SOLUSDT | Q1_low_abs_neg | A3_pricedisloc | 0.423013 | +1.848% | +0.079115 | [-0.026747,0.008622] | NO |
| SOLUSDT | Q1_low_abs_neg | C1 | 0.427537 | +0.799% | +0.083639 | [-0.010902,0.003218] | NO |
| SOLUSDT | Q1_low_abs_neg | I1_fund_x_rvregime | 0.419519 | +2.659% | +0.075622 | [-0.039095,0.013553] | NO |
| SOLUSDT | Q1_low_abs_neg | I2_fund_x_disloc | 0.418516 | +2.892% | +0.074618 | [-0.042084,0.014536] | NO |
| SOLUSDT | Q1_low_abs_pos | A1_fundpctz | 0.391699 | +4.619% | +0.047801 | [-0.031072,-0.007675] | YES |
| SOLUSDT | Q1_low_abs_pos | A3_pricedisloc | 0.393580 | +4.161% | +0.049682 | [-0.030483,-0.005151] | YES |
| SOLUSDT | Q1_low_abs_pos | C1 | 0.408068 | +0.633% | +0.064171 | [-0.005065,-0.000745] | YES |
| SOLUSDT | Q1_low_abs_pos | I1_fund_x_rvregime | 0.391832 | +4.587% | +0.047935 | [-0.030916,-0.007540] | YES |
| SOLUSDT | Q1_low_abs_pos | I2_fund_x_disloc | 0.391178 | +4.746% | +0.047281 | [-0.032092,-0.007657] | YES |
| SOLUSDT | Q2_neg | A1_fundpctz | 0.395444 | +1.617% | +0.051546 | [-0.044249,0.030298] | NO |
| SOLUSDT | Q2_neg | A3_pricedisloc | 0.405757 | -0.949% | +0.061859 | [-0.005226,0.012520] | NO |
| SOLUSDT | Q2_neg | C1 | 0.397741 | +1.045% | +0.053844 | [-0.017460,0.008711] | NO |
| SOLUSDT | Q2_neg | I1_fund_x_rvregime | 0.396711 | +1.302% | +0.052813 | [-0.043706,0.032292] | NO |
| SOLUSDT | Q2_neg | I2_fund_x_disloc | 0.396584 | +1.333% | +0.052686 | [-0.045103,0.033155] | NO |
| SOLUSDT | Q2_pos | A1_fundpctz | 0.269771 | +2.632% | -0.074127 | [-0.015428,0.000099] | NO |
| SOLUSDT | Q2_pos | A3_pricedisloc | 0.267005 | +3.630% | -0.076893 | [-0.025046,0.000899] | NO |
| SOLUSDT | Q2_pos | C1 | 0.274071 | +1.080% | -0.069827 | [-0.006016,-0.000276] | YES |
| SOLUSDT | Q2_pos | I1_fund_x_rvregime | 0.269888 | +2.589% | -0.074009 | [-0.015535,0.000318] | NO |
| SOLUSDT | Q2_pos | I2_fund_x_disloc | 0.269002 | +2.909% | -0.074896 | [-0.017132,0.000024] | NO |
| SOLUSDT | Q4_high_abs_neg | A1_fundpctz | 0.048888 | -4.775% | -0.295010 | [0.002228,0.002228] | NO |
| SOLUSDT | Q4_high_abs_neg | A3_pricedisloc | 0.043144 | +7.533% | -0.300753 | [-0.003515,-0.003515] | YES |
| SOLUSDT | Q4_high_abs_neg | C1 | 0.046097 | +1.206% | -0.297801 | [-0.000563,-0.000563] | YES |
| SOLUSDT | Q4_high_abs_neg | I1_fund_x_rvregime | 0.048888 | -4.775% | -0.295010 | [0.002228,0.002228] | NO |
| SOLUSDT | Q4_high_abs_neg | I2_fund_x_disloc | 0.049012 | -5.041% | -0.294886 | [0.002352,0.002352] | NO |
| XRPUSDT | Q1_low_abs_neg | A1_fundpctz | 1.907006 | +7.827% | +1.091126 | [-0.323890,-0.046301] | YES |
| XRPUSDT | Q1_low_abs_neg | A3_pricedisloc | 2.003790 | +3.149% | +1.187911 | [-0.154387,-0.003597] | YES |
| XRPUSDT | Q1_low_abs_neg | C1 | 2.024551 | +2.146% | +1.208671 | [-0.087803,-0.013215] | YES |
| XRPUSDT | Q1_low_abs_neg | I1_fund_x_rvregime | 1.908413 | +7.759% | +1.092533 | [-0.321495,-0.045506] | YES |
| XRPUSDT | Q1_low_abs_neg | I2_fund_x_disloc | 1.897465 | +8.288% | +1.081585 | [-0.347452,-0.047944] | YES |
| XRPUSDT | Q1_low_abs_pos | A1_fundpctz | 0.865254 | +4.663% | +0.049375 | [-0.072672,-0.017848] | YES |
| XRPUSDT | Q1_low_abs_pos | A3_pricedisloc | 0.887257 | +2.239% | +0.071377 | [-0.037142,-0.006673] | YES |
| XRPUSDT | Q1_low_abs_pos | C1 | 0.902516 | +0.557% | +0.086636 | [-0.010088,-0.001402] | YES |
| XRPUSDT | Q1_low_abs_pos | I1_fund_x_rvregime | 0.865588 | +4.626% | +0.049709 | [-0.072294,-0.017416] | YES |
| XRPUSDT | Q1_low_abs_pos | I2_fund_x_disloc | 0.864713 | +4.723% | +0.048833 | [-0.073546,-0.018052] | YES |
| XRPUSDT | Q2_neg | A1_fundpctz | 0.424640 | -11.217% | -0.391240 | [0.015483,0.067459] | NO |
| XRPUSDT | Q2_neg | A3_pricedisloc | 0.392403 | -2.774% | -0.423476 | [0.003980,0.016779] | NO |
| XRPUSDT | Q2_neg | C1 | 0.395988 | -3.713% | -0.419892 | [0.004436,0.022989] | NO |
| XRPUSDT | Q2_neg | I1_fund_x_rvregime | 0.426428 | -11.686% | -0.389452 | [0.016874,0.069830] | NO |
| XRPUSDT | Q2_neg | I2_fund_x_disloc | 0.427701 | -12.019% | -0.388178 | [0.017125,0.071898] | NO |
| XRPUSDT | Q2_pos | A1_fundpctz | 0.584461 | +3.193% | -0.231418 | [-0.032949,-0.007973] | YES |
| XRPUSDT | Q2_pos | A3_pricedisloc | 0.599171 | +0.757% | -0.216709 | [-0.011378,0.002021] | NO |
| XRPUSDT | Q2_pos | C1 | 0.596638 | +1.176% | -0.219241 | [-0.012207,-0.002915] | YES |
| XRPUSDT | Q2_pos | I1_fund_x_rvregime | 0.584679 | +3.157% | -0.231200 | [-0.032707,-0.007768] | YES |
| XRPUSDT | Q2_pos | I2_fund_x_disloc | 0.583966 | +3.275% | -0.231914 | [-0.034038,-0.008163] | YES |
| XRPUSDT | Q4_high_abs_neg | A1_fundpctz | 0.734925 | +4.128% | -0.080955 | [-0.113046,0.049823] | NO |
| XRPUSDT | Q4_high_abs_neg | A3_pricedisloc | 0.764352 | +0.289% | -0.051528 | [-0.016472,0.012182] | NO |
| XRPUSDT | Q4_high_abs_neg | C1 | 0.750209 | +2.134% | -0.065671 | [-0.052939,0.020114] | NO |
| XRPUSDT | Q4_high_abs_neg | I1_fund_x_rvregime | 0.741970 | +3.209% | -0.073910 | [-0.110738,0.061601] | NO |
| XRPUSDT | Q4_high_abs_neg | I2_fund_x_disloc | 0.735123 | +4.102% | -0.080757 | [-0.117461,0.054697] | NO |

## 4) Aggregate regime summary (all symbols pooled, TEST)
| Regime | n | B1 QLIKE | C2_all QLIKE | rel_imp_vs_B1 | diff(C2-B1) | 95% CI | CI_excludes0 |
|--------|---|----------|--------------|---------------|--------------|--------|--------------|
| Q1_low_abs_neg | 1258 | 0.745559 | 0.709103 | +4.890% | -0.036456 | [-0.080391,-0.003577] | YES |
| Q1_low_abs_pos | 3888 | 0.730213 | 0.691177 | +5.346% | -0.039036 | [-0.057688,-0.023675] | YES |
| Q2_neg | 385 | 0.358945 | 0.366907 | -2.218% | 0.007962 | [-0.021898,0.034220] | NO |
| Q2_pos | 2581 | 0.585369 | 0.562137 | +3.969% | -0.023232 | [-0.037703,-0.009791] | YES |
| Q4_high_abs_neg | 168 | 0.356639 | 0.373388 | -4.696% | 0.016749 | [-0.029563,0.062385] | NO |

## 5) Per-regime observation counts and block-bootstrap validity (TEST)
| Symbol | Regime | n | unique_regime_rows | min_block_24h_feasible |
|--------|--------|---|----------------------|------------------------|
| BNBUSDT | Q1_low_abs_neg | 49 | 49 | YES |
| BNBUSDT | Q1_low_abs_pos | 1440 | 1440 | YES |
| BNBUSDT | Q2_neg | 34 | 34 | YES |
| BNBUSDT | Q2_pos | 22 | 22 | NO |
| BNBUSDT | Q3_neg | 0 | 0 | NO |
| BNBUSDT | Q3_pos | 0 | 0 | NO |
| BNBUSDT | Q4_high_abs_neg | 111 | 111 | YES |
| BNBUSDT | Q4_high_abs_pos | 0 | 0 | NO |
| BTCUSDT | Q1_low_abs_neg | 374 | 374 | YES |
| BTCUSDT | Q1_low_abs_pos | 656 | 656 | YES |
| BTCUSDT | Q2_neg | 151 | 151 | YES |
| BTCUSDT | Q2_pos | 467 | 467 | YES |
| BTCUSDT | Q3_neg | 0 | 0 | NO |
| BTCUSDT | Q3_pos | 0 | 0 | NO |
| BTCUSDT | Q4_high_abs_neg | 8 | 8 | NO |
| BTCUSDT | Q4_high_abs_pos | 0 | 0 | NO |
| ETHUSDT | Q1_low_abs_neg | 306 | 306 | YES |
| ETHUSDT | Q1_low_abs_pos | 729 | 729 | YES |
| ETHUSDT | Q2_neg | 31 | 31 | YES |
| ETHUSDT | Q2_pos | 582 | 582 | YES |
| ETHUSDT | Q3_neg | 0 | 0 | NO |
| ETHUSDT | Q3_pos | 0 | 0 | NO |
| ETHUSDT | Q4_high_abs_neg | 8 | 8 | NO |
| ETHUSDT | Q4_high_abs_pos | 0 | 0 | NO |
| SOLUSDT | Q1_low_abs_neg | 340 | 340 | YES |
| SOLUSDT | Q1_low_abs_pos | 554 | 554 | YES |
| SOLUSDT | Q2_neg | 103 | 103 | YES |
| SOLUSDT | Q2_pos | 651 | 651 | YES |
| SOLUSDT | Q3_neg | 0 | 0 | NO |
| SOLUSDT | Q3_pos | 0 | 0 | NO |
| SOLUSDT | Q4_high_abs_neg | 8 | 8 | NO |
| SOLUSDT | Q4_high_abs_pos | 0 | 0 | NO |
| XRPUSDT | Q1_low_abs_neg | 189 | 189 | YES |
| XRPUSDT | Q1_low_abs_pos | 509 | 509 | YES |
| XRPUSDT | Q2_neg | 66 | 66 | YES |
| XRPUSDT | Q2_pos | 859 | 859 | YES |
| XRPUSDT | Q3_neg | 0 | 0 | NO |
| XRPUSDT | Q3_pos | 0 | 0 | NO |
| XRPUSDT | Q4_high_abs_neg | 33 | 33 | YES |
| XRPUSDT | Q4_high_abs_pos | 0 | 0 | NO |

## 6) Status decision (FUNDING_CONDITIONING_DEEPER_VALIDATION-002)
- Gate: confirmatory requires >=3 non-overlapping 30-day blocks; FCLR-002 test has 2 blocks -> confirmatory NOT met, EXPLORATORY only.
- Aggregate C2 vs B1 on full TEST: +4.588% rel QLIKE, CI excludes 0 (STREAM_B_DEEP_ANALYSIS-001).
- Regime-stratified results above: inspect per-regime CI_excludes0 and rel_imp. If NO regime shows robust skill (CI excludes 0 AND rel_imp >= 0 consistently), record null in negative_results_report.md Track C section and set experiment_frontier.json FUNDING_CONDITIONING_DEEPER_VALIDATION-002 to COMPLETE_INCONCLUSIVE. If a regime shows robust skill, keep EXPLORATORY_ONLY — do NOT promote to confirmatory (2 blocks < 3).
