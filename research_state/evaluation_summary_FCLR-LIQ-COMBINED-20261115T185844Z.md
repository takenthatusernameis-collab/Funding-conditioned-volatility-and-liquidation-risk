# FCLR-LIQ-COMBINED Evaluation — FCLR-LIQ-COMBINED-20261115T185844Z

**Generated (UTC):** 2026-11-15T18:58:45Z
**Experiment:** FCLR-LIQ-COMBINED-20261115T181449Z
**Prereg:** prereg_fclr_liq_combined_20261115T181449Z.json (frozen pre-outcomes)
**Panel:** fclr_liq_combined_panel_20261115T181405Z.parquet (sha256 81a100d5d0625832...)
**Verdict:** `NOT_MET` — pre-registered C2 vs B1 on 24h observed liquidation intensity

## 1. Determination

Expanding-window walk-forward QLIKE, contrast **C2 vs B1**, 3 non-overlapping 30-day test blocks, 7d purge/embargo, 2000 block-bootstrap reps (seed 20261115).
Forecast gate: **NOT_MET**.
Incremental forecast skill NOT demonstrated at the pre-registered materiality gate.

## 2. Per-block QLIKE (lower is better)

| block | window | n_train | n_test | B1 mean QLIKE | C2 mean QLIKE |
|---|---|---|---|---|---|
| 0 | 2025-10-01..2025-10-31 | 2405 | 412 | 119.099915 | 139.688884 |
| 1 | 2026-01-01..2026-01-31 | 3628 | 390 | 42.039463 | 53.129957 |
| 2 | 2026-09-01..2026-09-30 | 6615 | 419 | 18.472202 | 17.778288 |

## 3. Pooled test-set QLIKE

- B1 mean QLIKE: 59.954470 (n=1221)
- C2 mean QLIKE: 70.206066 (n=1221)

## 4. Primary contrast C2 vs B1 (block bootstrap)

- Paired n: 1221 across 3 test block(s)
- Mean diff (C2 - B1) QLIKE: 10.251596
- 95% CI: [-0.693914, 20.588970]
- Relative QLIKE reduction: -17.10%
- Bootstrap two-sided p: 0.0850 (Holm-adjusted, single-member family)

## 5. Gate assessment

- >= 2.0% relative QLIKE reduction: NOT_MET (-17.10%)
- 95% CI hi < 0 (excludes zero, C2 better): NOT_MET
- >= 5 paired instruments: PASS (15)
- >= 3 non-overlapping test blocks: PASS (3)
- **Forecast gate (all criteria): NOT_MET**

## 6. Compliance
- outcome_data_inspected_before_freeze: false (prereg frozen pre-outcomes)
- No threshold tuning after freeze: PASS
- No sealed-artifact mutation: PASS
- No network/paid/credentialed data for outcomes: PASS
- H2_shek_replication remains EXPLORATORY_ONLY (promotable=false)

## 7. Artifacts
- Panel: /home/runner/work/Funding-conditioned-volatility-and-liquidation-risk/Funding-conditioned-volatility-and-liquidation-risk/research_state/fclr_liq_combined_panel_20261115T181405Z.parquet
- Prereg: /home/runner/work/Funding-conditioned-volatility-and-liquidation-risk/Funding-conditioned-volatility-and-liquidation-risk/research_state/prereg_fclr_liq_combined_20261115T181449Z.json
- Eval JSON: /home/runner/work/Funding-conditioned-volatility-and-liquidation-risk/Funding-conditioned-volatility-and-liquidation-risk/research_state/evaluation_summary_FCLR-LIQ-COMBINED-20261115T185844Z.json

---
**End of verdict.** Evaluation ID: FCLR-LIQ-COMBINED-20261115T185844Z
