# Evaluation Summary — TRACKA-VOL-FAMILY-20261112T005111Z
**Generated (UTC):** 2026-11-12T00:51:11.707328+00:00
**Prereg:** `research_state/tracka_prereg_volatility_20261111T234918Z.json` (frozen pre-outcomes)
**Panel:** `research_state/tracka_vol_panel_20261111T234918Z.parquet` (cached Hyperliquid, 2026-05..2026-10, 9 coins)
**Family:** Primary 24h + Secondary 6h/72h/168h × Contrasts {C2vsB1, C1vsB1, C2vsC1} = 12 comparisons
**Multiplicity Correction:** Holm (alpha=0.05)
**Verdict:** NOT_MET

## Per-Horizon Results
### 6h (6h)
- B0: QLIKE=1.100481, n=19233
- B1: QLIKE=8.195934, n=19233
- C1: QLIKE=8.199977, n=19233
- C2: QLIKE=8.198241, n=19233

- C2_vs_B1: improvement=-0.002307, rel reduction=-0.03%, 95% CI=[-0.006230, 0.011278], excludes zero favoring alt=False, n=19233
- C1_vs_B1: improvement=-0.004042, rel reduction=-0.05%, 95% CI=[0.002769, 0.005469], excludes zero favoring alt=False, n=19233
- C2_vs_C1: improvement=0.001735, rel reduction=0.02%, 95% CI=[-0.010092, 0.007090], excludes zero favoring alt=False, n=19233

### 24h (24h)
- B0: QLIKE=0.649391, n=19233
- B1: QLIKE=6.501093, n=19233
- C1: QLIKE=6.497413, n=19233
- C2: QLIKE=6.495250, n=19233

- C2_vs_B1: improvement=0.005843, rel reduction=0.09%, 95% CI=[-0.012758, 0.000982], excludes zero favoring alt=False, n=19233
- C1_vs_B1: improvement=0.003680, rel reduction=0.06%, 95% CI=[-0.004921, -0.002302], excludes zero favoring alt=True, n=19233
- C2_vs_C1: improvement=0.002163, rel reduction=0.03%, 95% CI=[-0.008864, 0.004727], excludes zero favoring alt=False, n=19233

### 72h (72h)
- B0: QLIKE=3.965287, n=18801
- B1: QLIKE=5.243301, n=18801
- C1: QLIKE=5.244755, n=18801
- C2: QLIKE=5.242314, n=18801

- C2_vs_B1: improvement=0.000987, rel reduction=0.02%, 95% CI=[-0.006749, 0.004919], excludes zero favoring alt=False, n=18801
- C1_vs_B1: improvement=-0.001454, rel reduction=-0.03%, 95% CI=[-0.000165, 0.003161], excludes zero favoring alt=False, n=18801
- C2_vs_C1: improvement=0.002441, rel reduction=0.05%, 95% CI=[-0.007955, 0.003141], excludes zero favoring alt=False, n=18801

### 168h (168h)
- B0: QLIKE=19.763544, n=17937
- B1: QLIKE=4.266645, n=17937
- C1: QLIKE=4.266249, n=17937
- C2: QLIKE=4.263771, n=17937

- C2_vs_B1: improvement=0.002875, rel reduction=0.07%, 95% CI=[-0.006904, 0.001136], excludes zero favoring alt=False, n=17937
- C1_vs_B1: improvement=0.000396, rel reduction=0.01%, 95% CI=[-0.001245, 0.000466], excludes zero favoring alt=False, n=17937
- C2_vs_C1: improvement=0.002478, rel reduction=0.06%, 95% CI=[-0.006347, 0.001570], excludes zero favoring alt=False, n=17937

## Family-Wise Results (Holm Correction)
| Horizon | Contrast | p-value | Rel Reduction % | 95% CI | Holm Rejected |
|---------|----------|---------|-----------------|--------|---------------|
| 6h | C2_vs_B1 | 0.605427 | -0.03% | [-0.006230, 0.011278] | False |
| 6h | C1_vs_B1 | 0.000000 | -0.05% | [0.002769, 0.005469] | True |
| 6h | C2_vs_C1 | 0.692183 | 0.02% | [-0.010092, 0.007090] | False |
| 24h | C2_vs_B1 | 0.095507 | 0.09% | [-0.012758, 0.000982] | False |
| 24h | C1_vs_B1 | 0.000000 | 0.06% | [-0.004921, -0.002302] | True |
| 24h | C2_vs_C1 | 0.532739 | 0.03% | [-0.008864, 0.004727] | False |
| 72h | C2_vs_B1 | 0.740218 | 0.02% | [-0.006749, 0.004919] | False |
| 72h | C1_vs_B1 | 0.086545 | -0.03% | [-0.000165, 0.003161] | False |
| 72h | C2_vs_C1 | 0.388457 | 0.05% | [-0.007955, 0.003141] | False |
| 168h | C2_vs_B1 | 0.161060 | 0.07% | [-0.006904, 0.001136] | False |
| 168h | C1_vs_B1 | 0.363689 | 0.01% | [-0.001245, 0.000466] | False |
| 168h | C2_vs_C1 | 0.219855 | 0.06% | [-0.006347, 0.001570] | False |

## Criteria Assessment
- min_paired_instruments>=5: True (9 instruments)
- min_test_blocks>=3: True (3 blocks)
- all_blocks_ge5_instruments: True
- Primary contrast C2vsB1 materiality>=2% + CI excludes zero after Holm: False

## Verdict
Family-wise primary gate NOT MET. C2 not confirmed over B1 under frozen thresholds with multiplicity correction.

## Provenance/Integrity
- Panel sha256: `bd6b9924e2f76dfa9ea5cecd9737e62f32c0a76b663695bd9fc161cc1257b837`
- Cached Hyperliquid data only; causal features; no outcome peeking before prereg freeze
- No threshold shopping; no sealed-holdout reuse; Hyperliquid-only venue