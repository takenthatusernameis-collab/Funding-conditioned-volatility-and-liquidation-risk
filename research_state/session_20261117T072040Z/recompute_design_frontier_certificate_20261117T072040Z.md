# Design Frontier Certificate — FCLR-REPRO-SYNTH-05 (2026-11-17T07:20:40Z)

- **Overall verdict:** `BLOCKED_ON_DESIGN`
- **Promotable:** `False`
- **FCLR-014 closed verdict reproduced:** `True`

## Per-estimand certificate

### Full-C2 (mark+index+premium+funding)
- Disjoint feasible blocks (canonical tool): **0** (campaign_feasible=False)
- Contiguous run feasible (>= 127d): **False**
- With/without explicit mutual non-overlap: no feasible blocks/runs (unchanged).
- Verdict: **BLOCKED_ON_DESIGN**

### Mark+funding-only (B0/B1/C1; materially different estimand, new prereg required)
- Individually feasible test months (outside TESTED_WINDOWS, without mutual non-overlap): **4** — 2024-10, 2024-11, 2024-12, 2025-01
- Mutually non-overlapping feasible blocks (enforced on [train_start,test_end]): **2** — 2024-10, 2025-01
- Overlapping pairs: **5**
- Campaign feasible (>=3 non-overlapping): **False**
- Contiguous untested complete mark+funding months run >= 127d: **False**

## FCLR-014 reproduction
- Full-C2: 0 feasible blocks / no >=127d contiguous run. ✓
- Mark+funding-only: 4 individually feasible (2024-10/11/12, 2025-01), 2 mutually non-overlapping (2024-10, 2025-01). ✓
- Retracted claim: 4-block confirmatory prereg freeze (041333Z corrected / 051045Z) due to cross-block train/test overlap leakage.

## Verdict detail
Full-C2: 0 feasible disjoint blocks and no contiguous untested run >=127d. Mark+funding-only: 4 individually feasible test months but only 2 mutually non-overlapping blocks (<3) after enforcing non-overlap in [train_start, test_end] and excluding TESTED_WINDOWS; consecutive candidates leak across blocks. No >=3-block confirmatory design can be frozen from local cached data. FCLR-014 BLOCKED_ON_DESIGN; the 4-block 'freeze a prereg' claim is retracted.
