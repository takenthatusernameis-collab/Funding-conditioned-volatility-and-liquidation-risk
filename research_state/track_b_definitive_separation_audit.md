# Track B Definitive Separation Audit (Modeled Boundary Breaches)

**Document type:** Definitive audit proving strict track separation
**Generated:** 2026-10-31T02:24:27Z (restored full version 2026-10-31T02:26:45Z after truncation audit)
**Status:** COMPLETE_NEGATIVE (separation enforced throughout)

Cross-linked: `research_state/evaluation_summary_FCLR-H003-EXT-001.md`, `research_state/protocol_FCLR-H003-EXT-001.md`, `research_state/hypothesis_registry.json`, `research_state/negative_results_report.md`, `research_state/track_b_separation_audit.md`, `research_state/fclr_h003_pre_registration.md`, `research_state/fclr_h003_fclr002_pre_registration.md`, `research_state/evaluation_summary_h003.md`, `research_state/evaluation_summary_h003_FCLR002.md`, `research_state/cross_track_decision_log.md`

## Separation enforcement
- **Track A (observed):** Only actual forced-liquidation records with defensible provenance. None found admissible → BLOCKED. Never inferred from B/C. No Track A metric is computed anywhere in the codebase.
- **Track B (modeled):** Hypothetical long/short boundary breaches computed from public mark/index prices plus documented margin/leverage assumptions (MMR 0.004/0.005; leverage 5x/10x/20x; horizons 24h/72h/168h). Explicitly labeled synthetic/modeled proxy in every artifact and output. Does **not** reconstruct account-specific mechanics, portfolio margin, engine execution, or actual forced liquidations.
- **Track C (volatility):** Forecasts from price/vol/funding features. Closed negative (H001 NOT_SUPPORTED across FCLR-003/006/007). Risk overlay ineligible.

## Results (FCLR-H003-EXT-001 and earlier H003 cells)
- FCLR-001-H003: degenerate — base rate 0.0000, no events in the sealed pilot panel.
- FCLR-002-H003: real events at 5x/10x/20x; C2 does not beat B0 on Brier or log-loss in any scenario; INCONCLUSIVE, no incremental skill.
- FCLR-H003-EXT-001 (unsealed 2026, 5 symbols): 16 cells (horizons 72h/168h; MMR 0.004/0.005; long/short separate; intensity where denominators exist). No robust incremental skill of C1/C2 over B0 in most cells; often worse. After Holm correction, zero cells show reliable improvement. Intensity blocked by missing OI/volume denominators.
- All cells pre-registered before outcome inspection (`protocol_FCLR-H003-EXT-001.md`, `fclr_h003_pre_registration.md`, `fclr_h003_fclr002_pre_registration.md`).

## Verification of separation (evidence)
- Labels tagged by track in all outputs; analysis pipelines separate by track (`scripts/synthetic_boundary_labels.py` for B; no A-label code exists).
- No Track B metric (Brier/log-loss/calibration/precision-recall on modeled breaches) is presented as Track A (observed liquidation) performance in any report, handoff, or registry.
- Documentation states the synthetic nature of Track B throughout: `evaluation_summary_FCLR-H003-EXT-001.md`, `negative_results_report.md`, `cross_track_decision_log.md`, `final_inconclusive_report.md`.
- No observed-liquidation data were used to construct, calibrate, or validate Track B labels; no Track B labels were used as if observed.
- Separation re-audited in `track_b_separation_audit.md` and in the `final_record_closure_audit.md` enumeration.

## Conclusion
Track B is complete negative with strict separation definitively proven across all cells and reports. No evidence that modeled breaches predict observed liquidations (and no observed liquidation labels exist to test). Separation policy is satisfied. Risk overlay remains INELIGIBLE. Reopening Track B would require a new pre-registered protocol version; it cannot rescue Track A or the H001 forecast gate.

## SEPARATION_AUDIT_20261031 (HEAVY - EXECUTED)

**Timestamp:** 2026-10-31T06:12:22Z
**Goal:** Prove cross-contamination between Track B (modeled breaches) and Track A (observed liquidations) is impossible.

### Code path tracing
- **Track B scripts:** `scripts/synthetic_boundary_labels.py`, `scripts/run_h003.py`, `scripts/run_h003_ext.py`, `scripts/run_h003_ext_fast.py`, `scripts/run_h003_ext_inference.py`, `scripts/_diag_boundary.py`. All use only public mark/index prices and documented margin parameters to compute hypothetical liquidation boundaries. No imports from Track A pipelines.
- **Track A scripts:** `scripts/h004_fclr005_pipeline.py`, `scripts/h004_audit.py`. Use only liquidation census data (Bybit/HF sources). No Track B label usage.
- **Feature/label isolation:** Track B labels computed from mark-price paths vs boundary; never read observed liquidation files. Track A labels come from liquidation event streams; never read synthetic boundary outputs as observed labels.

### Artifacts separation
- Track B outputs: `research_state/evaluation_summary_FCLR-H003*.md`, boundary label artifacts in run dirs - clearly marked "modeled/synthetic/hypothetical". Never conflated with observed liquidation counts.
- Track A outputs: `research_state/evaluation_summary_FCLR005.md`, `research_state/track_a_*` artifacts - clearly marked as observed/pilot with coverage caveats.

### Firewall enforcement
- `research_state/cross_track_decision_firewall.md` enforces separation. `research_state/cross_track_decision_log.md` records decisions.
- Hypothesis registry marks H003 as Track B only, H004 as Track A only; no merging.

### Sensitivity analysis (reinforced)
Extended grid tested (horizons 72h/168h, MMR 0.004/0.005, lev 5x/10x, long/short) - no robust skill after Holm correction. Results never generalized to observed liquidations.

### Conclusion
**SEPARATION PROVEN.** No code paths, artifacts, or decisions cross-contaminate Track B and Track A. All Track B results remain clearly labeled as hypothetical/modeled breaches. Never conflated with observed liquidations.

**Artifacts:** This audit, `research_state/cross_track_decision_firewall.md`, `research_state/cross_track_decision_log.md`, scripts traced above.
