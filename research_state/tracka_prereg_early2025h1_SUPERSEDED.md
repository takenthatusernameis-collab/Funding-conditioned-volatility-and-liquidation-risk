# SUPERSEDED PREREG — audit note

**Supersedes:** `research_state/tracka_prereg_early2025h1_20261112T134106Z.json`
(sha256 `db9d643df1c64323e07398de95942f059766ed3368e29d503303d231c082667a`)
**Superseded at (UTC):** 2026-11-12T13:44:00Z
**Reason:** the frozen split layout was **provably invalid**, not merely suboptimal.

## Defect (evidence)

The first freeze declared:

- `train` = 2025-05-25 .. 2025-08-31
- `test_blocks` = 2025-06-01 .. 2025-10-30

The programmatic leakage guard in
`research_state/tracka_hl_early2025h1_panel_build_report_20261112T134352Z.json`
returned `verdict: FAIL`:

```
train_test_day_overlap: 0
val_test_day_overlap:   30
test_days_with_feature_row_in_train: 91
```

i.e. **30 days of validation and 91 days of test fell inside the training span**. Fitting on
that layout would have leaked ~3 months of test information into the training fit and made
every downstream QLIKE contrast meaningless. The defect was in the *split definition*, so it
was corrected before any model was fit and before any outcome was read.

## Corrected layout (this is the freeze now in force)

The label support is 2025-05-25..2025-10-31 (160 days). That ceiling, not convenience,
determines the layout.

| Split | Span | Days |
|---|---|---|
| train | 2025-05-25 .. 2025-06-30 | 37 |
| validation (tail of train span) | 2025-06-24 .. 2025-06-30 | 7 |
| test block 0 | 2025-07-01 .. 2025-07-30 | 30 |
| test block 1 | 2025-07-31 .. 2025-08-29 | 30 |
| test block 2 | 2025-08-30 .. 2025-09-28 | 30 |
| test block 3 | 2025-09-29 .. 2025-10-28 | 30 |

Guarantees, verified programmatically by the build report's `leakage_guards`:

- `train_test_day_overlap = 0`, `val_test_day_overlap = 0`
- both purge directions checked (`test+1 ∩ train` and `train+1 ∩ test`), so no test feature
  row can be sourced from a training day and vice versa
- >= 1 day purge at every split boundary; the last block ends 2025-10-28, leaving 3 days of
  margin before the 2025-10-31 label ceiling

## What is unchanged from the superseded freeze

Everything that controls the inference is identical: the 9-coin universe, the coin × 24h UTC
unit, both targets (T1 observed liquidation notional, T2 next-24h realized variance), the
frozen B0/B1/C1/C2 model forms, the primary contrast `C2_vs_B1`, QLIKE, block bootstrap
(2000 reps, seed 20261112), Holm correction across the declared family, the ≥2% relative
materiality floor, and the ≥5-instrument / ≥3-block minima. No threshold, feature, or model
was changed to obtain this layout; only the split boundaries were repaired.

## Artifacts

- Superseded freeze (preserved, unmodified): `tracka_prereg_early2025h1_20261112T134106Z.{json,md}`
- Corrected freeze: the newest `tracka_prereg_early2025h1_<UTC>.{json,md}`
- Evidence: `tracka_hl_early2025h1_panel_build_report_20261112T134352Z.json` (`leakage_guards`)