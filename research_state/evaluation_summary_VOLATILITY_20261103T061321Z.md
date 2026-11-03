# Volatility Evaluation (Funding-Conditioned) - 2026-11-03T06:13:21.397730+00:00

## Data
- Panel: /home/runner/work/Funding-conditioned-volatility-and-liquidation-risk/Funding-conditioned-volatility-and-liquidation-risk/research_state/data_cache/fclr002_panel.json
- Total rows: 19488
- Symbols: ['BNBUSDT', 'BTCUSDT', 'ETHUSDT', 'SOLUSDT', 'XRPUSDT']
- Splits (frozen): {'train': ['2024-04-01T00:00:00Z', '2024-06-08T23:00:00Z'], 'val': ['2024-06-16T00:00:00Z', '2024-07-15T23:00:00Z'], 'test': ['2024-07-23T00:00:00Z', '2024-09-30T23:00:00Z']}

## TRAIN
- n: 7608
- B1 (RV-only/persist): QLIKE=0.7647201826786748, MSE=8.067097106606452e-06, MAE=0.0010608017152179381
- C1 (RV+funding): QLIKE=0.7647111511711404, MSE=8.067175834301149e-06, MAE=0.001060807413486924
- C2 (RV+funding+price): QLIKE=0.7645398635051808, MSE=8.08157259426839e-06, MAE=0.0010615431981561283

## VAL
- n: 3600
- B1 (RV-only/persist): QLIKE=0.8387172362247259, MSE=2.9966966309703507e-06, MAE=0.000997063579867619
- C1 (RV+funding): QLIKE=0.8387113919559926, MSE=2.9967155745795044e-06, MAE=0.0009970662217584146
- C2 (RV+funding+price): QLIKE=0.8383289122633886, MSE=2.999010949442745e-06, MAE=0.0009973797613503472

## TEST
- n: 8280
- B1 (RV-only/persist): QLIKE=0.6625517972776758, MSE=8.916021619809523e-06, MAE=0.0011670718044717076
- C1 (RV+funding): QLIKE=0.6625493274702909, MSE=8.916055279322992e-06, MAE=0.0011670739923972263
- C2 (RV+funding+price): QLIKE=0.662271163716895, MSE=8.933259186415876e-06, MAE=0.0011677633625634468

## Notes
- Using existing frozen panel splits; leakage-resistant by construction (chronological).
- All features trailing-only as encoded in panel.
- No tuning on test set.
- This is a working evaluation; extend with proper train-only normalization and block bootstrap.