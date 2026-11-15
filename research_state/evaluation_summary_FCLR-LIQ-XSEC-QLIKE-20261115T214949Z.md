# FCLR-LIQ-XSEC-QLIKE Evaluation — FCLR-LIQ-XSEC-QLIKE-20261115T214949Z

**Generated (UTC):** 2026-11-15T21:49:50Z
**Experiment:** FCLR-LIQ-XSEC-QLIKE-20261115T214903Z
**Prereg:** prereg_fclr_liq_combined_xsec_qlike_20261115T214903Z.json (frozen pre-outcomes)
**Panel:** fclr_liq_combined_panel_20261115T181405Z.parquet (sha256 81a100d5d0625832...)
**Verdict:** `NOT_MET` — pre-registered C2 vs B1 on daily cross-sectional QLIKE

## 1. Determination

Expanding-window walk-forward, contrast **C2 vs B1**, 3 non-overlapping 30-day test blocks, 7d purge/embargo, 2000 block-bootstrap reps (seed 20261115).
Primary metric: **mean daily cross-sectional QLIKE** (lower is better; materiality floor 2.0% relative QLIKE reduction).
Forecast gate: **NOT_MET**.
Incremental forecast skill NOT demonstrated at the pre-registered materiality gate on cross-sectional QLIKE.

## 2. Per-metric results (C2 vs B1 paired differences)

| metric | mean diff | 95% CI | p-value | Holm reject |
|---|---|---|---|---|
| cross_sectional_qlike | 52.243893 | [18.403847, 86.083938] | 0.0000 | True |
| spearman_ic | -0.114208 | [-0.121896, -0.106520] | 0.0000 | True |
| top3_hit_rate | -0.005376 | [-0.021505, 0.010753] | 0.4780 | False |

## 3. Primary metric (cross-sectional QLIKE) gate assessment

- >= 2.0% relative QLIKE reduction (C2 lower loss): NOT_MET (-75.56%)
- 95% CI hi < 0 (excludes zero, C2 lower loss): NOT_MET
- >= 5 paired instruments: PASS (15)
- >= 3 non-overlapping test blocks: NOT_MET (2)
- **Forecast gate (all criteria): NOT_MET**

## 4. Compliance
- outcome_data_inspected_before_freeze: false (prereg frozen pre-outcomes)
- No threshold tuning after freeze: PASS
- No sealed-artifact mutation: PASS
- No network/paid/credentialed data for outcomes: PASS
- H2_shek_replication remains EXPLORATORY_ONLY (promotable=false)

## 5. Artifacts
- Panel: /home/runner/work/Funding-conditioned-volatility-and-liquidation-risk/Funding-conditioned-volatility-and-liquidation-risk/research_state/fclr_liq_combined_panel_20261115T181405Z.parquet
- Prereg: /home/runner/work/Funding-conditioned-volatility-and-liquidation-risk/Funding-conditioned-volatility-and-liquidation-risk/research_state/prereg_fclr_liq_combined_xsec_qlike_20261115T214903Z.json
- Eval JSON: /home/runner/work/Funding-conditioned-volatility-and-liquidation-risk/Funding-conditioned-volatility-and-liquidation-risk/research_state/evaluation_summary_FCLR-LIQ-XSEC-QLIKE-20261115T214949Z.json

---
**End of verdict.** Evaluation ID: FCLR-LIQ-XSEC-QLIKE-20261115T214949Z
