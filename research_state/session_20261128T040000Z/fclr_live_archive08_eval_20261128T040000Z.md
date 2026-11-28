# FCLR-LIVE-ARCHIVE-08 Evaluation — 20261128T040000Z

Campaign: FCLR-LIVE-ARCHIVE-08-20261128T040000Z
Design: Track-B modeled boundary-breach forecast (NOT a risk overlay).
Target: mark-price path breaches +/-4% hypothetical liquidation boundary within 24h (25x leverage).
Common support S: 22584 timestamps ({'BNBUSDT': 22608, 'BTCUSDT': 22608, 'ETHUSDT': 22608, 'SOLUSDT': 22608, 'XRPUSDT': 22584}); window 2024-04-01..2026-10-31 UTC.
Split: 60/20/20 + 168h embargo -> train=13349, val=4450, test=4449 timestamps.

## Out-of-sample results (test set)
B1 mark-price-only:  AUC=0.7086 logloss=0.4332 brier=0.1315
C2 funding-conditioned: AUC=0.6706 logloss=0.4349 brier=0.1324
Relative Brier improvement C2 vs B1: -0.705% (floor 2.0%, met=False)
Block-bootstrap (N=2000, block=24) 95% CI for rel Brier improvement: [-1.426%, 0.073%], supports_improvement=False
Verdict: NOT_SUPPORTED

## Leave-one-symbol-out (held-out symbol test AUC / logloss / brier)
- BNBUSDT: B1 auc=0.6601 brier=0.1098 | C2 auc=0.5934 brier=0.1047
- BTCUSDT: B1 auc=0.6191 brier=0.0934 | C2 auc=0.6561 brier=0.0992
- ETHUSDT: B1 auc=0.6287 brier=0.1327 | C2 auc=0.5986 brier=0.1343
- SOLUSDT: B1 auc=0.6974 brier=0.1680 | C2 auc=0.6581 brier=0.1703
- XRPUSDT: B1 auc=0.6984 brier=0.1655 | C2 auc=0.6580 brier=0.1699

Controls: outcome-blind prereg frozen before outcomes; train-only fit/scaling; 168h purge/embargo; stdlib-only; read-only cache; no network.