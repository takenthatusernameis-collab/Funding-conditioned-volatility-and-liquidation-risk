# Gate 4 v4 Exploratory Execution — Funding-Conditioned Volatility Ablation (NOT CONFIRMATORY)

**Timestamp (UTC):** 2026-11-09T00:40:03Z (run start) / 2026-11-09T00:40:39Z (artifacts)
**Git SHA:** 2f21b1dd40b26f3a4f0357457138643680a51e2d
**Status:** EXPLORATORY / NOT CONFIRMATORY / NOT PROMOTABLE
**Reason:** v4 prereg `confirmatory_claim_go=NO_GO` (sealed-anchor conflict with FCLR002/003/013 domain family); `exploratory_smoke_authorized_after_freeze=true`.

## Exact command
```bash
python scripts/run_funding_ablations.py \
  --symbols BTCUSDT,ETHUSDT,SOLUSDT,XRPUSDT,BNBUSDT \
  --start 2024-04-01 --end 2024-09-30 \
  --include-cache --split-design v3_30d \
  --out-suffix _v4_exploratory_exec_20261109T004003Z \
  --experiment-id GATE4-FUND-VOL-ABLATIONS-MSPLIT-V4-30D-EXPLORATORY-20261109T004003Z \
  --pre-registration research_state/pre_registration_gate4_funding_multisplit_v4_20261107T1845Z.json
```
**Exit:** 0. Log: `research_state/gate4_v4_exploratory_exec/gate4_v4_exploratory_exec_20261109T004003Z.log`

## Inputs / provenance
- **Pre-registration (frozen):** `research_state/pre_registration_gate4_funding_multisplit_v4_20261107T1845Z.json` — `FROZEN_BEFORE_OUTCOMES`, `confirmatory_claim_go:NO_GO`.
- **FCLR-015 input manifest:** `research_state/fclr015_local_audit/fclr015_input_manifest_2024_04_09_20261107T180626Z.json`
- **FCLR-015 manifest SHA256:** `3e6ac26ce645b8b2f0c2fb495288c4880aa74b5b7e457e1e7c88fb7eb3f5406c`
- **Local cache:** `research_state/data_cache/*_2024_04..09` (30 symbol-month dirs present for 5 symbols × 6 months). `--include-cache` used.
- **Design:** 4×30-day walk-forward (2024-04-01..2024-09-30), 7d purge/embargo, v3_30d; ablations A–E; primary QLIKE; contrast E vs A; 24h UTC block bootstrap joint across instruments (seed=12345, reps=2000, block_hours=24, α=0.05). Direct-variance OLS HAR, train-only normalization per split.

## Split / sample table (from run manifest)
| Split | Train | Test | Purge/Embargo | n_train | n_test | Test days |
|---|---|---|---|---:|---:|---:|
| 0 | 2024-04-01..2024-05-07 | 2024-05-15..2024-06-13 | 7d/7d | 4440 | 3600 | 30 |
| 1 | 2024-04-01..2024-06-06 | 2024-06-14..2024-07-13 | 7d/7d | 8040 | 3600 | 30 |
| 2 | 2024-04-01..2024-07-06 | 2024-07-14..2024-08-12 | 7d/7d | 11640 | 3600 | 30 |
| 3 | 2024-04-01..2024-08-05 | 2024-08-13..2024-09-11 | 7d/7d | 15240 | 3600 | 30 |
Data sufficiency: instruments=5, ok_splits=4, ok_30day_splits=4, `meets_claim_worthy_data_sufficiency=true`, no shortfalls reported. **Data-sufficient pilot under prereg design; still NOT confirmatory.**

## Aggregate metrics (mean across OK splits)
| Ablation | QLIKE | MAE | RMSE |
|---|---:|---:|---:|
| A_rv_only | 0.798319 | 0.00109255 | 0.00182047 |
| B_rv_signed | 12.183624 | 0.00106513 | 0.00185164 |
| C_rv_abs | 0.845962 | 0.00106290 | 0.00180975 |
| D_rv_signed_abs | 3.449289 | 0.00105037 | 0.00181522 |
| E_rv_funding_trails | 1.241702 | 0.00114139 | 0.00201428 |

## Primary contrast: E vs A (ΔQLIKE = alt − base; negative = better for QLIKE)
- **Point:** 0.487902 (worse for E vs A)
- **95% block bootstrap CI:** [-0.042161, 1.197338] (spans 0)
- **n_obs:** 12969, **n_blocks:** 120
- **Verdict (script):** DATA-SUFFICIENT PILOT / INCONCLUSIVE ON PRIMARY CONTRAST (pre-registered 30-day blocks met; E vs A CI spans 0; no improvement claim)

## Other contrasts vs A (exploratory context)
| Contrast | ΔQLIKE point | 95% CI | n_obs |
|---|---:|---:|---:|
| B_rv_signed vs A | 11.110523 | [0.480523, 32.312583] | 13620 |
| C_rv_abs vs A | -0.024710 | [-0.371595, 0.270799] | 13985 |
| D_rv_signed_abs vs A | 2.421918 | [-0.253960, 7.512203] | 13269 |

## Instability / shortfalls
- B/D show extreme split instability (e.g., split 3 ΔQLIKE B vs A = 44.69; D vs A = 10.33), indicating outlier/variance sensitivity in direct-variance OLS under some funding transforms. **No improvement claim.**
- E vs A CI spans 0 across block-size sensitivity (12/24/48h) — primary remains inconclusive.
- Exploratory sensitivity is labeled NOT confirmatory in manifest; do not promote if unstable.

## Versioned artifacts
- `research_state/gate4_v4_exploratory_exec/run_manifest_funding_v4_exploratory_exec_20261109T004003Z.json`
- `research_state/gate4_v4_exploratory_exec/evaluation_summary_funding_v4_exploratory_exec_20261109T004003Z.md`
- `research_state/gate4_v4_exploratory_exec/gate4_v4_exploratory_exec_20261109T004003Z.log`
- `results/fclr_heavy001/gate4_v4_exploratory_exec_20261109T004003Z.md` (this note)

## Explicit verdict
**EXPLORATORY ONLY. NOT CONFIRMATORY. NOT PROMOTABLE.** No confirmatory GO, no economic value claim, no overlay, no Track A linkage. Results are out-of-sample forecast evidence under a pre-registered design on a sealed-anchor-conflicted 2024 slice; instability must be reported honestly.
