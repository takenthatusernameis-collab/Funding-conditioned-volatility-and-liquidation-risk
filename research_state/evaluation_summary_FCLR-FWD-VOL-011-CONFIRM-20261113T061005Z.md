# Evaluation Summary — FCLR-FWD-VOL-011-CONFIRM-20261113T041200Z

Generated: 2026-11-13T06:10:05Z
Verdict: **INCONCLUSIVE**

## Primary (C2 vs B1, 24h QLIKE, pooled 3 blocks)

- mean diff (C2 - B1): 0.026760 (positive = C2 worse)
- 95% CI: [0.000343, 0.064822]
- relative reduction: -5.55%
- n: 10200
- days: 85

## Checks

- materiality_ge_2pct: False
- ci_excludes_zero: False
- instruments_ge_5: True
- blocks_ge_3: True
- loio_ge_4_of_5: False
- placebo_pass: False
- sensitivity_pass: False
- repro_011_pass: False

## Interpretation

Forward evidence contradicts the FCLR-011 PASS: pooled C2 vs B1 mean diff is 0.026760 (positive = C2 worse), 95% CI [0.000343, 0.064822], relative reduction -5.55%. 5/5 LOIO subsets are negative. However the pipeline reproduces the sealed FCLR-011 result at 4.39% vs 4.94% (delta 0.552pp), outside the pre-registered +/-0.5pp tolerance, so the frozen verdict rule requires INCONCLUSIVE pending exact panel reconstruction.

## LOIO (C2 vs B1, held-out symbol)

- BTCUSDT: rel -1.06%, CI [-0.012238, 0.019805]
- ETHUSDT: rel -0.60%, CI [-0.003845, 0.017351]
- BNBUSDT: rel -6.39%, CI [0.007745, 0.043611]
- SOLUSDT: rel -5.92%, CI [0.001828, 0.041982]
- XRPUSDT: rel -17.44%, CI [0.012660, 0.239693]

## Placebo (funding permutation)

- null p95: -5.35% vs true -5.55% -> pass=False

## Sensitivity (excluding previously inspected days)

- rel -7.82%, CI [-0.000411, 0.109870], n=5995

## FCLR-011 reproduction (legacy conventions)

- rel 4.39% vs sealed 4.94% (delta 0.552pp)
- mean diff -0.014571 vs sealed -0.016458; CI [-0.030726, 0.000099]
- pass=False

## Next action

1. Materialize `research_state/data_cache/fclr011_panel.json` (LFS) or reconstruct the exact sealed FCLR-011 panel.
2. Re-run `scripts/fclr_fwd_vol_confirm.py` and confirm the repro delta <= 0.5pp.
3. Issue the final verdict: NOT_REPLICATED if the forward C2-vs-B1 CI remains in favor of B1; otherwise CONFIRMED.
