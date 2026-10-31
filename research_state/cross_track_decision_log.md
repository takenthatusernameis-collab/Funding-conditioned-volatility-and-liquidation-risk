# Cross-Track Decision Log (Decision-Grade)

**Generated:** 2026-10-31T02:18:31Z
**Repo:** Funding-conditioned-volatility-and-liquidation-risk
**Priority:** Track C > Track A > Track B

## Hypothesis Registry
- **H001 (Primary):** Funding extremes + RV + price features improve OOS forecasts of future RV/volatility stress vs RV-only baseline.
  - **Status:** NOT_SUPPORTED (sealed negative). FCLR-003/006/007 all fail gate; two show significant degradation.
- **H002 (Secondary replication):** Shek (SSRN 29 Sep 2026) funding-correction pattern replication.
  - **Status:** PARTIAL / blocked on full methodology; cannot do exact replication from public sources alone.
- **H003 (Boundary breaches):** Modeled hypothetical liquidation-boundary breaches.
  - **Status:** COMPLETE_NEGATIVE. No robust incremental skill after Holm; strict Track B separation enforced.
- **H004 (Observed liquidations):** Actual forced-liquidation events.
  - **Status:** BLOCKED / NO-GO. No admissible unauthenticated source found for 2024 windows.

## Gates & Decisions
| Track | Experiment(s) | Gate/Result | Decision |
|-------|---------------|-------------|----------|
| C | FCLR-003 | CI crosses zero, -3.78% rel | NOT_MET → NOT_SUPPORTED |
| C | FCLR-006 | CI entirely positive (worse), -69.90% rel, 2 blocks | NOT_MET → NOT_SUPPORTED |
| C | FCLR-007 | CI entirely positive (worse), -3.42% rel, 0 blocks | NOT_MET → NOT_SUPPORTED |
| B | FCLR-H003, H003-EXT-001 | No robust skill after Holm across cells | COMPLETE_NEGATIVE |
| A | Discovery campaign | All candidates NO-GO | BLOCKED; structural blocker |

## Risk Overlay
**INELIGIBLE.** Forecast gate not passed on Track C; Track B/A cannot support risk overlay. No trading/paper-trading logic exists or planned.

## Conditions for Reopening
- **Track A:** Only if NEW admissible unauthenticated liquidation data appears with ≥5 symbols, ≥3 non-overlapping 30-day blocks, documented completeness, license OK. Must pre-register before outcome inspection.
- **Track C/B:** No planned reopen (sealed negative). Would require new pre-registered hypothesis with strong justification and admissible data.
- **Workflows:** No .github/workflows changes without explicit maintainer auth.

## Traceability
- `research_state/hypothesis_registry.json`
- `research_state/experiment_frontier.json`
- `research_state/track_c_consolidated_dossier.md`
- `research_state/track_a_deadend_map.md`
- `research_state/track_b_definitive_separation_audit.md`
- `research_state/final_confirmatory_verdict.md`
