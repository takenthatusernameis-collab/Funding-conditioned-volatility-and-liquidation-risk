# Track B Separation Proof Hardened — Modeled Boundary Breaches vs Observed Liquidations

**Report ID:** FCLR-TRACKB-SEP-002
**Date (UTC):** 2026-10-31T09:13:52Z
**HEAD:** 52506b1a
**Priority:** Track B (THIRD)
**Status:** CLOSED_NEGATIVE (H003). Strict separation ENFORCED from Track A.

## Core principle (non-negotiable)
Track B uses **modeled/synthetic** hypothetical liquidation boundaries computed from public mark/index prices + documented margin/leverage assumptions. Track A requires **observed** forced-liquidation records. These are fundamentally different outcomes. **NEVER conflate them.**

## Code-path trace (separation verification)
- Track B logic isolated to modeled boundary computation using mark-price paths and pre-specified leverage/margin assumptions. No observed liquidation label ingestion in Track B evaluation paths.
- Firewall artifacts enforce separation: `research_state/cross_track_decision_firewall.md`, `research_state/cross_track_decision_log.md`, `research_state/track_b_definitive_separation_audit.md`, `research_state/track_b_separation_audit.md`.
- Track A blocked by source availability; no merge of tracks occurred.

## H003 results (traceable)
- **Experiment:** FCLR-H003-EXT-001 (pre-registered extension)
- **Protocol:** `research_state/protocol_FCLR-H003-EXT-001.md`, pre-registration `research_state/fclr_h003_pre_registration.md`/`fclr_h003_fclr002_pre_registration.md`
- **Evaluations:** `research_state/evaluation_summary_h003.md`, `research_state/evaluation_summary_FCLR-H003-EXT-001.md`
- **Coverage:** `research_state/coverage_audit_h003ext_2026.md`
- **Finding:** No robust incremental skill after Holm correction across 16 cells. Sensitivity to margin/leverage/funding assumptions tested; effects labeled as synthetic/model proxy only.
- **Conclusion:** Track B CLOSED_NEGATIVE. Performance of modeled breach proxy cannot be interpreted as proof of observed liquidation prediction.

## Separation enforcement evidence
- `research_state/track_b_definitive_separation_audit.md` documents boundary between tracks
- Decision logs explicitly forbid conflation; firewall codifies separation
- All Track B reports label outcomes as "hypothetical/model boundary breach" or "synthetic proxy"

## Final determination
**Track B CLOSED_NEGATIVE. Strict separation from Track A maintained. Modeled boundary breaches do NOT constitute observed liquidation evidence. No risk-overlay eligibility from Track B.**

## Artifacts (traceability)
- `research_state/protocol_FCLR-H003-EXT-001.md`, `research_state/evaluation_summary_FCLR-H003-EXT-001.md`
- `research_state/cross_track_decision_firewall.md`, `research_state/cross_track_decision_log.md`
- `research_state/track_b_definitive_separation_audit.md`, `research_state/track_b_separation_audit.md`
- `research_state/hypothesis_registry.json` (H003)
