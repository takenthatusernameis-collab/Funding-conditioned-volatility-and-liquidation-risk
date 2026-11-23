# FCLR-POOLED-AUDIT-001 Evidence Audit

Session UTC: 20261122T165200Z
Campaign: FCLR-POOLED-AUDIT-001-20261122T120000Z
Evidence type: evidence_audit

## Data evidence
Source: research_state/data_cache/ironflow_bulk/{candles_1h,funding,open_interest,liquidations}
Months: 2025-05..2026-10 (18 months)

| dataset | rows | files | sha256 sidecars asserted |
|---|---|---|---|
| candles_1h | 3,643,742 | 18 | yes |
| funding | 4,104,648 | 18 | yes |
| open_interest | 3,977,432 | 18 | yes |
| liquidations | 2,849,452 | 18 | yes |

Per-month sha256 and row counts: fclr_pooled_audit001_evidence_audit_20261122T165200Z.json (datasets).

## Properties
- Caches mutated: no
- Network used: no
- New source required: no
- Nulls preserved as-is; no zero-fill/forward-fill
- Software: stdlib + pyarrow only; numpy/pandas/scipy not used

## Audit outputs
- fclr_pooled_audit001_audit_20261122T165200Z.py / .json / .md — ten adversarial audit domains + Track B modeled boundary-breach labels
- fclr_pooled_audit001_recompute_20261122T165200Z.py / .json — independent stdlib recompute (all material domains verified; strict exact-timestamp alignment not estimable — funding grid ≠ hourly grid — reported as a coverage null)
- fclr_pooled_audit001_prereg_20261122T165200Z.json / .md — outcome-blind prereg freeze
- trigger_check_20261122T165200Z.json — trigger check
- evidence_audit_20261122T165200Z.json — gate-critical alias to this package

## Key measured findings
- d1: zero within-file monotonicity violations; zero cross-file overlaps
- d2: train/test gap is 1 hour (adjacent distinct hours); purge+embargo of 48h NOT present in the raw panel — reported, not assumed
- d3: mean corr funding_t vs fwd return 0.00113 vs vs lag return 0.00060 — publication-timing reading
- d4: 6.8% of aligned rows above 1% mark/oracle tolerance; max premium 37x (STRAX-PERP)
- d5: zero nulls in candles/funding; open_interest mark_price nulls concentrated 2026-07..09 (up to 175k rows); liquidations block nulls pre-2025-09
- d6: 344 coins new in last month, 44 absent from last month; survivor share of last-month universe 38%
- d7: mean abs funding survivors 2.77e-5 vs non-survivors 3.20e-5 — no strong survivorship funding difference
- d8: top market share of stress hours 2.5% — not single-coin dominated
- d9: mean monthly p66 |funding| drift 1.1e-5
- d10: pairwise Jaccard 0.52..0.92 across horizons — forward liquidation-intensity outcomes not independent
- trackb: modeled breach rate 4.1% at 2.5% band; high funding tercile 4.7% vs low 2.9% (modeled proxy, not observed liquidation)
