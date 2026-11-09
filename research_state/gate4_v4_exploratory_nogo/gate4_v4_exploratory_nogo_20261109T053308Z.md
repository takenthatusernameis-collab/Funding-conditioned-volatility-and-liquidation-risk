# Gate 4 v4 EXPLORATORY NO-GO note — funding ablations on local 2024-04..09 slice

**20261109T053308Z — EXPLORATORY / NOT CONFIRMATORY / NOT PROMOTABLE**
- Git SHA: `d7a764b9e9411f58b8dca3abe8251f6780c5d6d4`
- Prereg: `research_state/pre_registration_gate4_funding_multisplit_v4_20261107T1845Z.json` — `FROZEN_BEFORE_OUTCOMES`, `confirmatory_claim_go=NO_GO`, `exploratory_smoke_authorized_after_freeze=true`
- Does NOT replace prereg A-E contrasts, does NOT change confirmatory estimands. No confirmatory GO, no economic-value claim, no promotion, no sealed-anchor (FCLR002/003/013 domain family) reuse.
- Scope: local 2024-04..09 cache (FCLR-015), 5 symbols (BTCUSDT, ETHUSDT, SOLUSDT, XRPUSDT, BNBUSDT), 4 chronological 30-day splits (prereg v3_30d), purge/embargo 7d.

## What was tested (EXPLORATORY stabilized variants, fixed rules)

Four principled, leakage-safe variants evaluated against RV-only baseline A (alt-base ΔQLIKE; negative better for alt), 95% block-bootstrap CI by UTC time blocks:

| Variant | Rule summary | E vs A ΔQLIKE (95% CI) | Verdict |
|---|---|---|---|
| V1_primary | ridge=1e-10*I, floor-at-zero | +0.488 CI [-0.042, 1.197] | inconclusive (CI spans 0) |
| V2_scale_ridge | ridge=1e-8*max(trace(X'X)/k,1)*I, floor-at-zero | +0.488 CI [-0.042, 1.197] | inconclusive |
| V3_scale_ridge_target_floor | V2 + train-only target-scale floor max(0,1e-4*train_target_median) | **+1096 CI [331, 2104]** | **significantly worse** |
| V4_winsor_train | V3 + train-only winsor q0.5/q99.5 (train bounds) | +1421 CI [414, 2995] | significantly worse |

Pooled over all contrasts (V1): B worse CI>0, C inconclusive, D inconclusive, E inconclusive. Under V3/V4 every funding ablation (B/C/D/E) is significantly worse or inconclusive; none improves vs A.

Split-3 diagnostic (EXPLORATORY): B QLIKE V1=45.00 → V3=1028.58 (blowup amplified). BTCUSDT dominates B/D blowups (raw negatives + large coef_l2). E has no single catastrophic blowup but many raw negatives (622) and is worse than A.

E vs A LOO (V3, EXPLORATORY): all=+1096 CI [331, 2104]; drop_XRP attenuates to +344 CI [-132, 814] (inconclusive); every other drop leaves CI entirely >0. **No LOO shows improvement.**

## Verdict (EXPLORATORY NO-GO — not confirmatory)

Principled leakage-safe stabilization (scale-aware ridge, train-only target-scale floor, train-only winsor, block bootstrap by UTC time blocks, chronological splits, train-only normalization) **does not improve out-of-sample QLIKE vs the RV-only baseline**; it catastrophically degrades it (V3 E vs A +1096, CI entirely >0; B vs A amplified 45→1029). No instrument drop yields improvement. **Funding ablations B/C/D/E show no credible incremental forecast skill on this local 2024-04..09 slice.**

Status: EXPLORATORY_ONLY, NO-GO signal confirmed. Not confirmatory. Not promotable. No sealed-anchor reuse. Original confirmatory estimands unchanged; Gate 4 v4 prereg remains FROZEN_BEFORE_OUTCOMES with confirmatory_claim_go=NO_GO.

Artifacts: `scripts/run_gate4_v4_exploratory_stab.py` (executed `20261109T045805Z`), `tests/test_gate4_v4_exploratory_stab.py` (6 tests), `research_state/gate4_v4_exploratory_stab/gate4_v4_exploratory_stab_20261109T045805Z.{json,md}`, `results/fclr_heavy001/gate4_v4_exploratory_stab_20261109T045805Z.md`.

Command: `python scripts/run_gate4_v4_exploratory_stab.py --out-suffix 20261109T045805Z`
