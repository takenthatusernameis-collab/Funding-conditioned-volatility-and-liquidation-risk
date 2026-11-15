# FCLR-LIQ-XSEC-ORDERING Evaluation — FCLR-LIQ-XSEC-ORDERING-20261115T203507Z

**Generated (UTC):** 2026-11-15T20:35:10Z
**Experiment:** FCLR-LIQ-XSEC-ORDERING-20261115T203501Z
**Prereg:** prereg_fclr_liq_combined_xsec_20261115T203501Z.json (frozen pre-outcomes)
**Panel:** fclr_liq_combined_panel_20261115T181405Z.parquet (sha256 81a100d5d0625832...)
**Verdict:** `NOT_MET` — pre-registered C2 vs B1 on daily cross-sectional liquidation ordering

## 1. Determination

Expanding-window walk-forward, contrast **C2 vs B1**, 3 non-overlapping 30-day test blocks, 7d purge/embargo, 2000 block-bootstrap reps (seed 20261115).
Primary metric: **mean daily Spearman rank-IC** (materiality floor 2.0%).
Forecast gate: **NOT_MET**.
Incremental forecast skill NOT demonstrated at the pre-registered materiality gate.

## 2. Per-metric results (C2 vs B1 paired differences)

| metric | mean diff | 95% CI | p-value | Holm reject |
|---|---|---|---|---|
| spearman_ic | -0.060749 | [-0.106520, -0.013295] | 0.0000 | True |
| top3_hit_rate | -0.010989 | [-0.044444, 0.010753] | 0.5890 | False |
| cross_sectional_qlike | 9.392914 | [-0.620184, 18.403847] | 0.0850 | False |

## 3. Primary metric (Spearman rank-IC) gate assessment

- >= 2.0% relative improvement: NOT_MET (-14.34%)
- 95% CI hi < 0 (excludes zero, C2 better): PASS
- >= 5 paired instruments: PASS (15)
- >= 3 non-overlapping test blocks: PASS (3)
- **Forecast gate (all criteria): NOT_MET**

## 4. Compliance
- outcome_data_inspected_before_freeze: false (prereg frozen pre-outcomes)
- No threshold tuning after freeze: PASS
- No sealed-artifact mutation: PASS
- No network/paid/credentialed data for outcomes: PASS
- H2_shek_replication remains EXPLORATORY_ONLY (promotable=false)

## 5. Artifacts
- Panel: /home/runner/work/Funding-conditioned-volatility-and-liquidation-risk/Funding-conditioned-volatility-and-liquidation-risk/research_state/fclr_liq_combined_panel_20261115T181405Z.parquet
- Prereg: /home/runner/work/Funding-conditioned-volatility-and-liquidation-risk/Funding-conditioned-volatility-and-liquidation-risk/research_state/prereg_fclr_liq_combined_xsec_20261115T203501Z.json
- Eval JSON: /home/runner/work/Funding-conditioned-volatility-and-liquidation-risk/Funding-conditioned-volatility-and-liquidation-risk/research_state/evaluation_summary_FCLR-LIQ-XSEC-ORDERING-20261115T203507Z.json

---
**End of verdict.** Evaluation ID: FCLR-LIQ-XSEC-ORDERING-20261115T203507Z
