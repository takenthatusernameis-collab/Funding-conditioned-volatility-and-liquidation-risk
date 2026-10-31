# Track B Definitive Separation & Robustness Audit (Modeled Boundary Breaches)

**Generated:** 2026-10-31T02:18:31Z
**Status:** COMPLETE_NEGATIVE — No robust incremental skill
**Tracks:** B (modeled boundary breaches) | Strict separation enforced

## Separation Principle (Enforced)
- **Track A:** Observed liquidation events/labels only. Never inferred from modeled breaches.
- **Track B:** Modeled/synthetic boundary breaches computed from public mark/index prices + documented margin/leverage assumptions. Explicitly labeled as hypothetical/model proxy. Does **not** reconstruct account-specific liquidation mechanics, portfolio margin, or actual forced liquidations.
- **Track C:** Volatility/stress outcomes from price/mark-price history.

All artifacts maintain this separation. No modeled breach results are described as observed liquidations.

## Evidence (FCLR-H003 / FCLR-H003-EXT-001)

### FCLR-H003 (Initial panels)
- **Panels:** FCLR-001 and FCLR-002
- **Result:** Degenerate base rates / no incremental skill. Long/short kept separate. Funding/fee assumptions disclosed.
- **Source:** `research_state/evaluation_summary_h003.md`, `research_state/fclr_h003_pre_registration.md`, `research_state/fclr_h003_fclr002_pre_registration.md`

### FCLR-H003-EXT-001 (Extended grid on unsealed 2026)
- **Protocol:** Pre-registered before outcome inspection (`research_state/protocol_FCLR-H003-EXT-001.md`)
- **Grid:** Horizons 72h/168h, MMR 0.004/0.005, leverage tiers, long/short separate
- **Evaluation:** Block bootstrap, LOO, Holm correction across 16 cells
- **Result:** No robust incremental skill of C1/C2 over B0 in most cells; often worse. Track separation enforced.
- **Source:** `research_state/evaluation_summary_FCLR-H003-EXT-001.md`, `research_state/coverage_audit_h003ext_2026.md`

## Robustness Checks
- **Multiplicity:** Holm familywise error correction applied; raw and adjusted results considered. No cell passes after correction.
- **Calibration/separation:** Brier/log-loss/calibration considered where applicable.
- **Track separation audit:** All labels, features, and estimands verified to belong to Track B only.
- **No threshold shopping:** Horizons/tiers/MMR pre-registered.

## Conclusion
**Track B is COMPLETE_NEGATIVE.** No robust incremental forecast skill for modeled boundary breaches. Results are reported as hypothetical/model-based only with strict separation from observed liquidations.

## Traceability
- `research_state/evaluation_summary_FCLR-H003-EXT-001.md`
- `research_state/evaluation_summary_h003.md`
- `research_state/protocol_FCLR-H003-EXT-001.md`
- `research_state/fclr_h003_pre_registration.md`
- `research_state/fclr_h003_fclr002_pre_registration.md`
- `research_state/coverage_audit_h003ext_2026.md`
