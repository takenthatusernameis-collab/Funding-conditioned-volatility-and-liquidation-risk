# FCLR-005 Evaluation Summary — Track A Observed Liquidation Outcomes (2026 pilot)

**Experiment:** FCLR-005 (protocol FCLR-005 v1.0, frozen 2026-10-30T04:30:00Z, pre-registered before outcome inspection)
**Status:** PILOT/EXPLORATORY_ONLY — ~30-day label window cannot satisfy the >=3 non-overlapping 30-day confirmatory gate; no confirmatory skill claimed; FCLR-H004 remains BLOCKED for frozen 2024
**Run start:** 2026-10-30T06:18:43Z  |  **Run end:** 2026-10-30T06:23:25Z
**Git SHA:** 37ddd9fda2ac5542e0989db9a60c18b37fa48cf8

## Data provenance
- Liquidations: `/home/runner/work/Funding-conditioned-volatility-and-liquidation-risk/Funding-conditioned-volatility-and-liquidation-risk/research_state/data_cache/liquidations_full_20260807.csv` (HF ochinimus/crypto-liquidation-ticks, CC BY 4.0, unauthenticated)
- Liquidation total_rows=1442664; bybit census rows (target symbols)=49938; bybit exchange rows=346269
- Per exchange: {'binance': 859499, 'bybit': 346269, 'okx': 236896}
- Per symbol/exchange (target symbols, bybit): BTCUSDT=21779, ETHUSDT=13904, BNBUSDT=367, SOLUSDT=8883, XRPUSDT=5005
- Binance/OKX rows excluded from the binary presence/absence target (undercounted lower-bound only; never census)
- Label window (Bybit census): 2026-07-08T16:42:32Z .. 2026-08-06T23:59:42Z
- Feature cache: research_state/data_cache/<SYM>_2026_*/ mark/index/premium 1h + monthly fundingRate, 2026-04-01..2026-08-06 (verified complete on disk)
- Universe: ['BTCUSDT', 'ETHUSDT', 'BNBUSDT', 'SOLUSDT', 'XRPUSDT'] (Binance mark-price features cross-referenced to Bybit liquidation labels)
- Panel rows after causal filtering: 3520
- Split (chronological, by unique UTC hour): train<= 2026-07-23T07:00:00Z, val<= 2026-07-30T15:00:00Z, test> val
- Train rows=1760, test rows=880
- Non-overlapping 30-day blocks in test window: 0 (< 3 required for confirmatory -> pilot limitation)

## Results (hourly binary liquidation presence, Bybit census only)
### Target: long_liquidated (Bybit 'long_liquidated' events -> long side)
- Base rate (test): 0.480682; events in test=423/880
- B0: Brier=0.250713 (boot mean=0.250722, 95% CI [0.245961, 0.256178]), logloss=0.694588 (boot mean=0.694607, 95% CI [0.685049, 0.705558]), AUPRC=1.000000, calibration intercept=-0.076912, slope=0.000000, precision@base_rate=0.480682 (thr=0.447727), n_test=880
- B1: Brier=0.251538 (boot mean=0.251566, 95% CI [0.245893, 0.257846]), logloss=0.696263 (boot mean=0.696319, 95% CI [0.684914, 0.708950]), AUPRC=0.467555, calibration intercept=-0.415516, slope=-1.413294, precision@base_rate=0.485849 (thr=0.441692), n_test=880
- C1: Brier=0.251633 (boot mean=0.251651, 95% CI [0.245893, 0.258295]), logloss=0.696472 (boot mean=0.696509, 95% CI [0.684911, 0.709872]), AUPRC=0.501503, calibration intercept=-0.109818, slope=-0.134064, precision@base_rate=0.466981 (thr=0.439724), n_test=880
- C2: Brier=0.251629 (boot mean=0.251647, 95% CI [0.245891, 0.258289]), logloss=0.696464 (boot mean=0.696501, 95% CI [0.684906, 0.709861]), AUPRC=0.501579, calibration intercept=-0.107672, slope=-0.125331, precision@base_rate=0.466981 (thr=0.439716), n_test=880

### Target: short_liquidated (Bybit 'short_liquidated' events -> short side)
- Base rate (test): 0.419318; events in test=369/880
- B0: Brier=0.245027 (boot mean=0.244956, 95% CI [0.240974, 0.248798]), logloss=0.683183 (boot mean=0.683040, 95% CI [0.675058, 0.690742]), AUPRC=1.000000, calibration intercept=-0.325164, slope=0.000000, precision@base_rate=0.419318 (thr=0.458523), n_test=880
- B1: Brier=0.244900 (boot mean=0.244823, 95% CI [0.239740, 0.249569]), logloss=0.682932 (boot mean=0.682778, 95% CI [0.672564, 0.692296]), AUPRC=0.414776, calibration intercept=-0.490222, slope=-0.802234, precision@base_rate=0.410811 (thr=0.452662), n_test=880
- C1: Brier=0.243575 (boot mean=0.243499, 95% CI [0.238096, 0.248535]), logloss=0.680231 (boot mean=0.680078, 95% CI [0.669191, 0.690181]), AUPRC=0.444742, calibration intercept=-0.044149, slope=1.325557, precision@base_rate=0.448649 (thr=0.452349), n_test=880
- C2: Brier=0.243571 (boot mean=0.243494, 95% CI [0.238091, 0.248530]), logloss=0.680222 (boot mean=0.680069, 95% CI [0.669182, 0.690170]), AUPRC=0.444765, calibration intercept=-0.043091, slope=1.330480, precision@base_rate=0.448649 (thr=0.452315), n_test=880

## Leave-one-symbol-out stability (primary contrast C2 vs B1, Brier difference C2-B1; negative = C2 better)
- BTCUSDT/long: n_test=176, events=106, base_rate=0.602273, Brier B1=0.284054, C2=0.288258, C2-B1=+0.004204
- BTCUSDT/short: n_test=176, events=103, base_rate=0.585227, Brier B1=0.285362, C2=0.284077, C2-B1=-0.001285
- ETHUSDT/long: n_test=176, events=96, base_rate=0.545455, Brier B1=0.261488, C2=0.259906, C2-B1=-0.001582
- ETHUSDT/short: n_test=176, events=96, base_rate=0.545455, Brier B1=0.264995, C2=0.261836, C2-B1=-0.003159
- BNBUSDT/long: n_test=176, events=33, base_rate=0.187500, Brier B1=0.283761, C2=0.286062, C2-B1=+0.002301
- BNBUSDT/short: n_test=176, events=27, base_rate=0.153409, Brier B1=0.309306, C2=0.311830, C2-B1=+0.002524
- SOLUSDT/long: n_test=176, events=102, base_rate=0.579545, Brier B1=0.274570, C2=0.274944, C2-B1=+0.000373
- SOLUSDT/short: n_test=176, events=94, base_rate=0.534091, Brier B1=0.259691, C2=0.259136, C2-B1=-0.000555
- XRPUSDT/long: n_test=176, events=86, base_rate=0.488636, Brier B1=0.252453, C2=0.253876, C2-B1=+0.001423
- XRPUSDT/short: n_test=176, events=49, base_rate=0.278409, Brier B1=0.238535, C2=0.241474, C2-B1=+0.002939

## Notes
- Event-free intervals NOT inferred from missing data. Hours with zero Bybit rows = observed zero in census arm only, not an absolute zero claim.
- Binance/OKX rows never used to construct the binary absence/presence target (capped streams, undercounted).
- No forward-fill / zero-fill across splits; rows with missing causal features dropped for that model comparison.
- Fixed logistic form; no hyperparameter search, no threshold tuning on outcomes, no alert-budget selection (pilot).
- Block bootstrap over complete UTC hours (deterministic seed); leave-one-symbol-out stability reported above.
- FCLR-005 is PILOT/EXPLORATORY ONLY. Does NOT clear any sealed FCLR-001-004 forecast gate. FCLR-H004 remains BLOCKED for frozen 2024.
- This summary is generated by scripts/h004_fclr005_pipeline.py (idempotent; rerun reproduces identical numbers).
