# Evaluation Summary — FCLR-FWD-VOL-2024-DISJOINT-2024-06-20261114T231100Z

- Generated: 2026-11-14T23:15:53Z
- Verdict: **EXPLAINED_BY_ESTIMATOR**
- Promotable: false | Max status: EXPLORATORY_ONLY | Singleton: true
- Prereg: `prereg_fclr_fwd_vol_2024_disjoint_2024_06_20261114T231100Z.json` (sha256 `0f44033ae2023b1b2d478d76c7c709adb8a621bd55a92637e52c85c757cdf350`)
- Panel: `research_state/tracka_fwd_vol_2024_disjoint_2024_06_panel_20261114T231545Z.parquet` (sha256 `ec1827f0200d9e2ae8d7a381c0a4b2f3e3b467dd554aa07e083d5cd025cd3ff4`)

## Lineage & Leakage
- lineage pass: True | leakage pass: True
- rows=8880 keys=8880 dup_keys=0 symbols=['BNBUSDT', 'BTCUSDT', 'ETHUSDT', 'SOLUSDT', 'XRPUSDT']
- span: 2024-04-25 00:00:00+00:00 .. 2024-07-07 23:00:00+00:00

## Estimator Arms (primary C2 vs B1, 24h QLIKE)
- sealed: mean_diff=-0.004960772911304939, rel_reduction_pct=0.9708873339874656, ci=[-0.04050992922517061, 0.023778366086377067], p_boot=0.853, n=3600, days=30
- corrected: mean_diff=0.014951052553487902, rel_reduction_pct=-3.5119072297689584, ci=[-0.009033194596158797, 0.03468207610350498], p_boot=0.193, n=3600, days=30
- swing (corrected-sealed rel pct): -4.482794563756424

## Verdict
- EXPLAINED_BY_ESTIMATOR (EXPLORATORY_ONLY, promotable=false, singleton diagnostic)
