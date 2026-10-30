# H003 Extension Feasibility — Hypothetical Boundary-Breach Forecast

Updated: 2026-10-30T12:04:15Z
Status: INCONCLUSIVE (SEALED_INCONCLUSIVE)
Extensions: UNTESTED (would require pre-registration)

## Completed evaluations
- FCLR-001-H003: 8 scenarios, n=70 each, base_rate=0.0000 everywhere (degenerate, no events)
- FCLR-002-H003: 8 scenarios on FCLR-002 test block, real events at 5x/10x/20x. C2 vs B0: worse or negligible on Brier/log-loss; AUPRC small gains but precision at best-F1 low. No incremental skill.

## Untested extensions
- Longer horizons (48h/72h/168h)
- Lower MMR tiers
- Different leverage ranges
- Event-intensity target (count of breaches) vs binary
- Alternative boundary definitions

## Feasibility assessment
- Need pre-registration BEFORE outcome inspection (fresh protocol version or amendment)
- Must not threshold-shop existing results
- Event rates depend on scenario/horizon - need to check if any scenario has sufficient events
- Current panels (FCLR-001/FCLR-002) are sealed; cannot reuse for tuning
- No unsealed >=5-symbol panel with sufficient history obvious

## Recommendation
Only pursue if: (1) new admissible data provides unsealed window, (2) pre-registered scenarios with event-rate feasibility check, (3) clear separation from sealed holds. Do not re-run on sealed sets.
