# Replication Robustness — FCLR-REPRO-SYNTH-05 (2026-11-17T07:20:40Z)

Based on: `research_state/session_20261117T071110Z/replication_synthesis_20261117T071110Z.json` (no re-run). Studies: FCLR-002, FCLR-003, FCLR-006, FCLR-008, FCLR-009, FCLR-010, FCLR-013.

## Qualitative corroboration (leave-one-out)
- Overall: **7/7** (rate 1.000), Wilson95 [0.6456611570247934, 1.0]
- LOO rate range: **1.000–1.000**; all-unity: **True**

| Left out | Kept n | Corroborated | Rate | Wilson95 |
|---|---:|---:|---:|---|
| FCLR-002 | 6 | 6 | 1.000 | [0.6096569663469354, 0.9999999999999999] |
| FCLR-003 | 6 | 6 | 1.000 | [0.6096569663469354, 0.9999999999999999] |
| FCLR-006 | 6 | 6 | 1.000 | [0.6096569663469354, 0.9999999999999999] |
| FCLR-008 | 6 | 6 | 1.000 | [0.6096569663469354, 0.9999999999999999] |
| FCLR-009 | 6 | 6 | 1.000 | [0.6096569663469354, 0.9999999999999999] |
| FCLR-010 | 6 | 6 | 1.000 | [0.6096569663469354, 0.9999999999999999] |
| FCLR-013 | 6 | 6 | 1.000 | [0.6096569663469354, 0.9999999999999999] |

## Sign consistency (C2 vs B1 relative reduction)
- Positive (C2 better): **3**, Negative (C2 worse): **4**, consistent in sign: **False**

| Study | Metric | rel_reduction_pct | Sign |
|---|---|---:|---|
| FCLR-002 | QLIKE | 8.599046454748262 | positive(C2_better) |
| FCLR-003 | QLIKE | -11.846371528231844 | negative(C2_worse) |
| FCLR-006 | QLIKE | -67.32320689374508 | negative(C2_worse) |
| FCLR-008 | QLIKE | 0.6862427547811324 | positive(C2_better) |
| FCLR-009 | QLIKE | -0.42525774214540507 | negative(C2_worse) |
| FCLR-010 | Brier | 0.5010692983825399 | positive(C2_better) |
| FCLR-013 | QLIKE | -4.988898715596898 | negative(C2_worse) |

## Estimand heterogeneity caveat
- Metrics: QLIKE (FCLR-002/003/006/008/009/013) vs Brier (FCLR-010); designs/windows/blocks differ.
- LOO/sign aggregation is programme-level over heterogeneous estimands, not a single estimand's sampling distribution. Stricter like-for-like within-tolerance reproduction: **2/7**.

## Boundary certificate (minimal change to flip to promotable)
- Programme: **CLOSED_TERMINAL / NO_CLAIM_WORTHY_RESULT_PROMOTABLE**. Promotable = materiality>=2% favorable with passing gates AND >=3 blocks (per study gates) under prereg; none currently.
- Global minimal change: one promotable positive result on a trigger-satisfied, pre-powered (paired_n floors), >=3-block, 7d-purge/embargo, pre-registered design with admissible data; or a new design-feasible (>=3 mutually non-overlapping blocks) cached-data estimand that passes confirmatory gates. Neither exists in current local frontier.
- Concrete flips: FCLR-014 needs >=1 more mutually non-overlapping feasible block (total>=3) + frozen prereg + passing run; FCLR-013 needs >=3-block preregistered panel with favorable >=2% CI-excluding-0 and passing LOIO/placebo; FCLR-010 needs >=2% favorable effect with passing robustness (not re-scoring).
