# Track B Code-Path Separation Matrix — Modeled vs Observed (H003)

**Document type:** Decision-grade code-path separation matrix (heavy evidence artifact)
**Repository:** Funding-conditioned-volatility-and-liquidation-risk
**Generated:** 2026-10-31T14:16:58Z
**HEAD:** a915cd38 (main). Working tree clean except untracked `scripts/__pycache__/`, `tests/__pycache__/`.
**Tracks:** Track B (modeled/synthetic boundary breaches) vs Track A (observed liquidations).
**Status:** SEPARATION ENFORCED; Track B CLOSED_NEGATIVE / NOT_SUPPORTED.
**Priority:** Track B is P2 per repo-name inference (Track C > Track A > Track B).

## Code-path trace (Track A label usage in Track B code paths)
| Check | Finding | Evidence location |
|---|---|---|
| Track B experiments use modeled boundary-breach definitions only | confirmed — documented margin parameters + mark prices; synthetic/model proxy only | `research_state/track_b_separation_proof_hardened.md:18-19, 54-58` |
| Imports/usages of Track A observed-liquidation label loaders in Track B pipelines | none found | `research_state/track_b_separation_proof_hardened.md:19, 43` |
| Observed liquidation label usage confined to Track A paths | confirmed | `research_state/track_b_separation_proof_hardened.md:43` |
| Cross-track boundary enforced by firewall | `research_state/cross_track_decision_firewall.md` defines hard separation rules | `research_state/track_b_separation_proof_hardened.md:23-26` |
| Separation logged | `research_state/cross_track_decision_log.md` records decisions enforcing separation | `research_state/cross_track_decision_log.md` |
| Separation structural (different sources, labels, hypotheses) | confirmed | `research_state/track_b_separation_proof_hardened.md:21` |

Key files/scripts checked: `scripts/*` related to Track B/H003 (`synthetic_boundary_labels.py`, `run_h003*`, `run_h003_ext*`); `research_state/*` decision logs/firewalls; tests related to separation (`tests/test_synthetic_boundary_labels.py`, `tests/test_funding_correction_replication.py`).

## Firewall enforcement
- `research_state/cross_track_decision_firewall.md`: hard separation rules (observed vs modeled never conflated)
- `research_state/cross_track_decision_log.md`: decision trace enforcing separation (C→A→B synthesis)
- `research_state/track_b_definitive_separation_audit.md` (SEPARATION_AUDIT_20261031): confirms no conflation

## Track B confirmatory result (sealed)
**FCLR-H003-EXT-001** (extended grid): symbols BTCUSDT/ETHUSDT/BNBUSDT/SOLUSDT/XRPUSDT; horizons 72h/168h; MMR 0.004/0.005; leverage 5x/10x; long/short separate → 16 cells. C2 vs B0 across 16 cells: no robust incremental skill after Holm correction (m=16). Most CIs cross 0. Intensity target blocked by missing OI/volume denominators. Labeled synthetic/model proxy only. Status: CLOSED_NEGATIVE / NOT_SUPPORTED.

Source: `research_state/track_b_separation_proof_hardened.md:29, 60-64`; `research_state/evaluation_summary_FCLR-H003-EXT-001.md`.

## Explicit separation statement (enforced)
**Track B (modeled boundary breaches) is NEVER conflated with Track A (observed liquidations).** All Track B results are model-proxy only and provide no evidence for observed liquidation outcomes. Separation enforced by policy, code paths, and audit artifacts. Source: `research_state/track_b_separation_proof_hardened.md:31-32, 66-68`.

## Grep/code-path evidence summary
- Searched Track B paths for Track A observed liquidation label usage: none found.
- Track B paths reference model-based breach definitions only.
- Firewall enforcement documented; separation proven structurally and by audit.

## Artifacts (traceability)
- `research_state/track_b_separation_proof_hardened.md`
- `research_state/track_b_definitive_separation_audit.md`
- `research_state/track_b_separation_audit.md`
- `research_state/cross_track_decision_firewall.md`
- `research_state/cross_track_decision_log.md`
- `research_state/evaluation_summary_FCLR-H003-EXT-001.md`

## Tests
`python -m unittest discover -s tests -v` → 27/27 PASS at HEAD a915cd38 (must remain green; Track B separation is structural, not a test failure).
