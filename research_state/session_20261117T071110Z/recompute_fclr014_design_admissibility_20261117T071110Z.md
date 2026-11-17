# FCLR-014 Design-Admissibility Adjudication — 2026-11-17T07:12:03Z

**Verdict: `BLOCKED_ON_DESIGN`**

## Question
Can a >=3-block confirmatory FCLR-014 design be frozen from local cached data before outcome inspection?

## Canonical tool (full-C2: mark+index+premium+funding)
- `design_feasibility.any_feasible`: False
  - run ['2024-04', '2024-05'] span=61d feasible=False
  - run ['2025-01'] span=31d feasible=False
- `disjoint_block_frontier.n_feasible`: 0 (need >= 3)
- `disjoint_block_frontier.campaign_feasible`: False
  - 2024-04: feasible=False reason=2024-02:missing_or_unfunded; 2024-03:missing_or_unfunded
  - 2024-05: feasible=False reason=2024-03:missing_or_unfunded
  - 2025-01: feasible=False reason=2024-11:missing_or_unfunded; 2024-12:missing_or_unfunded

## Mark+funding-only rule (B0/B1/C1, materially different estimand)
- candidate untested mark+fund months: ['2024-04', '2024-05', '2024-10', '2024-11', '2024-12', '2025-01']
- individually feasible: 4 -> ['2024-10', '2024-11', '2024-12', '2025-01']
- **mutually non-overlapping maximum: 2 -> ['2024-10', '2025-01'] (need >= 3)**
- overlapping pairs among individually-feasible blocks: 5
  - 2024-10 vs 2024-11 overlap ['2024-09-25', '2024-10-31']
  - 2024-10 vs 2024-12 overlap ['2024-10-25', '2024-10-31']
  - 2024-11 vs 2024-12 overlap ['2024-10-25', '2024-11-30']
  - 2024-11 vs 2025-01 overlap ['2024-11-25', '2024-11-30']
  - 2024-12 vs 2025-01 overlap ['2024-11-25', '2024-12-31']

## Conflict resolution
- discrepancy: 041333Z (corrected JSON) and 051045Z count 4 mark+funding-only blocks and claim a prereg is freezable; the canonical full-C2 tool reports 0 feasible blocks / no >=127d run.
- root cause: The 4-block count treats each month independently and omits the mutual non-overlap constraint across blocks.  A 30d train + 7d embargo + 30d test window spans ~2.2 months, so consecutive candidate months (2024-10/11/12, 2025-01) have train windows that overlap a neighbouring block's test month, i.e. cross-block leakage.  Enforcing non-overlap leaves at most 2 blocks.
- retraction: RETRACTED: the claim 'campaign_feasible_new_prereg=true / freeze a NEW mark+funding-only prereg using 2024-10, 2024-11, 2024-12' (session_20261117T051045Z and the corrected 041333Z JSON) is UNSAFE for a confirmatory claim: it uses mutually overlapping blocks.  It is valid only as an EXPLORATORY / NOT-CONFIRMATORY / NOT-PROMOTABLE 2-block pilot.

## Verdict detail
FCLR-014 is BLOCKED-ON-DESIGN.  Under the registered full-C2 rule (mark+index+premium+funding) the canonical tool finds 0 feasible disjoint blocks and no contiguous untested run >=127d.  Under a mark+funding-only rule (a materially different estimand requiring a new prereg) only 2 mutually non-overlapping blocks exist (<3).  Therefore no >=3-block confirmatory design can be frozen from local data without consuming a sealed window.  Do NOT freeze a prereg on the retracted 4-block claim; do NOT re-score sealed results.

## Prior-session claims (recorded, adjudicated)
- session_20261117T041333Z: campaign_feasible_new_prereg=True n_blocks=4
- session_20261117T051045Z: overall_verdict={'full_c2_design_feasible': False, 'mark_funding_only_design_feasible': True, 'recommended_path': 'mark_funding_only'}
