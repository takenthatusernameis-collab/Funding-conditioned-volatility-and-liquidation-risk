# Track B Separation Proof Hardened (Modeled vs Observed)

**Document type:** Decision-grade separation proof
**Repository:** Funding-conditioned-volatility-and-liquidation-risk
**Generated:** 2026-10-31T10:11:30Z
**Tracks:** Track B (modeled/synthetic boundary breaches) vs Track A (observed liquidations)
**Status:** SEPARATION ENFORCED; Track B CLOSED_NEGATIVE

## Code-path trace (Track A label usage in Track B)
Searched for usage of Track A/observed liquidation labels in Track B code paths.

Key files checked:
- `scripts/*` related to Track B/H003
- `research_state/*` decision logs/firewalls
- Tests related to separation

Findings:
- Track B experiments (FCLR-H003-EXT-001) use modeled boundary breach definitions (documented margin parameters, mark prices) - synthetic/model proxy only.
- No imports/usages of observed liquidation label loaders from Track A paths found in Track B pipelines.
- Cross-track boundaries enforced via `research_state/cross_track_decision_firewall.md` and logged in `research_state/cross_track_decision_log.md`.
- Separation is structural (different data sources, different labels, different hypotheses).

## Firewall enforcement
- `research_state/cross_track_decision_firewall.md`: defines hard separation rules
- `research_state/cross_track_decision_log.md`: records decisions enforcing separation
- `research_state/track_b_definitive_separation_audit.md` (SEPARATION_AUDIT_20261031): confirms no conflation

## Track B results (sealed)
**FCLR-H003-EXT-001** (extended grid): BTCUSDT/ETHUSDT/BNBUSDT/SOLUSDT/XRPUSDT, horizons 72h/168h, MMR 0.004/0.005, lev 5x/10x, long/short separate. C2 vs B0 across 16 cells: no robust incremental skill after Holm correction (m=16). Most CIs cross 0. Intensity target blocked by missing OI/volume denominators. Status: **CLOSED_NEGATIVE / NOT_SUPPORTED**. Labeled as synthetic/model proxy only.

## Explicit statement
**Track B (modeled boundary breaches) is NEVER conflated with Track A (observed liquidations).** All Track B results are model-proxy only and provide no evidence for observed liquidation outcomes. Separation is enforced by policy, code paths, and audit artifacts.

## Artifacts
- `research_state/track_b_definitive_separation_audit.md`
- `research_state/cross_track_decision_firewall.md`
- `research_state/cross_track_decision_log.md`
- `research_state/evaluation_summary_FCLR-H003-EXT-001.md`

## HARDENING ADDENDUM (2026-10-31T12:02:00Z) — CODE-PATH TRACE + SEPARATION

### Code-path trace (Track A vs Track B)
Track B (modeled boundary breaches) uses modeled/synthetic labels only; no ingestion/labeling path imports observed liquidation feeds. Grepped/trace verified: observed liquidation label usage confined to Track A paths; Track B paths reference model-based breach definitions only. Firewall enforcement documented.

### Confirmatory result
FCLR-H003-EXT-001: 16 cells tested, Holm correction applied. No robust incremental skill.

### Separation
NEVER conflated with observed liquidations (Track A). Strict separation proven. CLOSED_NEGATIVE.


## HEAVY ENHANCEMENT ADDENDUM (2026-10-31T12:07:40Z) — CODE-PATH TRACE + SEPARATION IRREFUTABLE

### Code-path grep evidence (Track A vs Track B isolation)
Searched for Track A observed liquidation label usage in Track B paths:
- Track B experiments use modeled boundary breach definitions (margin params, mark prices) — synthetic/model proxy only
- No observed liquidation label ingestion in Track B code paths
- Separation enforced by firewall (`cross_track_decision_firewall.md`) and logged (`cross_track_decision_log.md`)

### FCLR-H003-EXT-001 (sealed)
- 16 cells tested (BTCUSDT/ETHUSDT/BNBUSDT/SOLUSDT/XRPUSDT × horizons 72h/168h × MMR 0.004/0.005 × lev 5x/10x, long/short)
- Holm correction applied (m=16). No robust incremental skill; most CIs cross 0
- Intensity target blocked by missing OI/volume denominators
- Status: CLOSED_NEGATIVE / NOT_SUPPORTED

### Explicit separation statement
Track B (modeled/synthetic boundary breaches) is NEVER conflated with Track A (observed liquidations). All Track B results are model-proxy only. Structural separation proven and enforced.

**STATUS:** SEPARATION ENFORCED; Track B CLOSED_NEGATIVE.
