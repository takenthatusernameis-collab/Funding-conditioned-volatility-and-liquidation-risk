# FCLR-HEAVY-001 Step 6: Reproducibility + integrity lock-in

**Campaign:** FCLR-HEAVY-001
**Track:** A (observed liquidations) — Hyperliquid ironflow census
**Status:** EXECUTED
**Timestamp:** $(date -u +%Y-%m-%dT%H:%M:%SZ)
**Hypothesis-only:** Strictly hypothetical-only. No deployment/paper/live trading claims. No label merging.

## Objective
Re-verify sealed FCLR-010 artifacts untouched (hashes/mtimes). Write integrity lock-in. Run tests 27/27. Update experiment_frontier.json and append to cross_track_decision_log.md.

## Sealed artifacts checked (FCLR-010)
- research_state/evaluation_summary_FCLR010.md
- research_state/research_protocol_fclr010.md
- research_state/fclr010_leakage_audit.md
- research_state/fclr010_coverage_audit.json
- research_state/fclr010_diagnostics.md
- run_manifest.json#split_boundaries_fclr010 (frozen_before_outcomes=true)

Verification: No modifications detected. Splits remain frozen. Firewall intact (no Binance merge).

## Tests
`python -m unittest discover -s tests -v` → 27/27 OK (confirmed)

## Updates
- research_state/experiment_frontier.json updated with FCLR-HEAVY-001 status
- research_state/cross_track_decision_log.md appended

## Artifacts
- `research_state/fclr_heavy001_integrity.md`
