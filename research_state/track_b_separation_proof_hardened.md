# Track B Separation Proof Hardened — Modeled Boundary Breaches vs Observed Liquidations

**Report ID:** FCLR-TRACKB-SEP-002
**Date (UTC):** 2026-10-31T09:10:42Z
**HEAD:** 52506b1a
**Priority:** Track B (THIRD) per repo name inference
**Status:** CLOSED_NEGATIVE
**Rule:** NEVER conflate Track B (synthetic/model proxy) with Track A (observed). Strict separation enforced.

## Evidence sources
- `research_state/track_b_separation_audit.md`
- `research_state/track_b_definitive_separation_audit.md`
- `research_state/cross_track_decision_firewall.md`
- `research_state/cross_track_decision_log.md`
- `research_state/evaluation_summary_FCLR-H003-EXT-001.md`
- `research_state/protocol_FCLR-H003-EXT-001.md`
- `research_state/research_protocol_fclr004.md`

## Code-path separation (trace)
**Separation enforced by design:**
- Track B uses public mark/index prices + documented margin/leverage assumptions to compute hypothetical liquidation boundaries (modeled breach proxy)
- Track A requires observed liquidation records/census
- Decision firewall prevents cross-contamination: `research_state/cross_track_decision_firewall.md` codifies separation rules
- Decision log tracks track boundaries: `research_state/cross_track_decision_log.md`
- Definitive separation audit documents no Track A liquidation labels consumed by Track B: `research_state/track_b_definitive_separation_audit.md`

**Verification:** Grep-based trace confirms Track B logic does not ingest observed liquidation datasets; labels are computed from price paths under disclosed assumptions. All Track B artifacts explicitly label as "synthetic" or "modeled breach proxy".

## FCLR-H003-EXT-001 results (summary)
- 16 cells tested across pre-registered dimensions
- Holm familywise-error correction applied
- No robust incremental skill demonstrated
- Results labeled as hypothetical/model proxy only
- Never conflated with observed liquidations

## Sensitivity (documented)
Margin/leverage/funding assumptions varied within pre-registered/sensible ranges; sensitivity documented. All results remain synthetic proxies with no evidence of mapping to observed liquidation events.

## Final determination
**Track B CLOSED_NEGATIVE.** Separation from Track A is proven and enforced. Track B results are synthetic/model proxies only — they do not constitute evidence of observed liquidation predictability.
