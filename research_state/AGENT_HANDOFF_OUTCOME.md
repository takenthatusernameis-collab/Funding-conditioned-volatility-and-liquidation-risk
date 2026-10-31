# AGENT_HANDOFF_OUTCOME (HEAVY CAMPAIGN EXECUTED)

**Generated:** 2026-10-31T07:10:30Z
**HEAD:** 52d065e6
**REPO:** Funding-conditioned-volatility-and-liquidation-risk
**Handoff source:** AGENT_HANDOFF.md (HND-20261031-062306-HEAVY-FORCED-REFRESH)
**Mode:** FORCED HEAVY EVIDENCE CAMPAIGN - NO SHORTCUTS

## Integrity check (P0)
- Tests: `python -m unittest discover -s tests -v` → **19/19 PASS** (verified)
- Key artifacts present and cross-linked (hypothesis registry, experiment frontier, track dossiers/audits, deadend map, separation audit, firewall, decision log, hardening audit, negative results report, next data discovery plan, final verdicts)

## Track C (Funding-conditioned volatility, H001) - FIRST PRIORITY
**Status:** NOT_SUPPORTED (SEALED_NEGATIVE). Risk overlay INELIGIBLE.

**Forensic re-audit executed (FORENSIC_REAUDIT_20261031):**
- **FCLR-003 (powered, 2024-10-02..2024-12-31, 3 blocks, n=10796):** C2 vs B1 ΔQLIKE +0.015205, CI [-0.020240, 0.056734] crosses zero, rel -3.78% worse. Gate NOT_MET. COMPLETE_NEGATIVE.
- **FCLR-006 (unsealed, 2026-05-23..2026-08-06, 2 blocks <3, n=8987):** C2 vs B1 +0.368588, CI entirely positive, rel -69.90% worse. Gate NOT_MET. COMPLETE_NEGATIVE.
- **FCLR-007 (unsealed, 2026-07-21..2026-07-31, 0 blocks, n=1195):** C2 vs B1 +0.010258, CI entirely positive, rel -3.42% worse. Gate NOT_MET. COMPLETE_NEGATIVE.
- **Findings:** Feature additions (funding/price dislocation) do not consistently improve over HAR-RV B1; often degrade. Leakage/embargo/block-bootstrap all sound. No defensible path without violating pre-registration/sealed holdouts.
- **Artifacts updated:** `research_state/track_c_consolidated_dossier.md` (FORENSIC_REAUDIT_20261031 section added with concrete tables/numbers).

## Track A (Observed liquidations, H004) - SECOND PRIORITY (BOTTLENECK REMOVAL)
**Status:** BLOCKED/EXPLORATORY. No admissible unauthenticated source.

**Machine-checkable firewall executed (MACHINE_CHECKABLE_FIREWALL_20261031):**
- Rubric applied to all candidates: unauthenticated=true AND no_keys=true AND symbols>=5 AND blocks>=3 AND completeness_doc=true AND license_ok=true AND census_or_defensible=true.
- **Results:** Binance liquidationSnapshot 404; forceOrders 451 (geo-restricted); Bybit trades exist but not census (no conversion path, incompleteness unprovable); OKX/Deribit no admissible sets; HuggingFace ochinimus/crypto-liquidation-ticks is 2026-only (CC BY 4.0 OK) but wrong period, only ~1 block window, exhausted by FCLR-005; Zenodo/OSF/GitHub/others no match; vendors paywalled. **NO SOURCE PASSES RUBRIC.**
- **Bottlenecks:** 2024 period missing, format (trades!=census), completeness unprovable. Remediation exhaustive; no removable bottlenecks with current admissible sources.
- **Conclusion:** Irrefutable dead-end evidence recorded. Sole reopen path: new admissible unauthenticated source meeting all criteria. FCLR-005 remains exploratory only.

## Track B (Modeled breaches, H003) - THIRD PRIORITY
**Status:** COMPLETE_NEGATIVE (SEALED_NEGATIVE). Strict separation enforced.

**Separation audit executed (SEPARATION_AUDIT_20261031):**
- Code paths traced: Track B uses only mark/index + margin assumptions (`scripts/synthetic_boundary_labels.py`, `run_h003*`); Track A uses only liquidation streams (`scripts/h004_*`); no cross-imports.
- Labels/artifacts clearly separated and labeled synthetic/modeled; never conflated with observed liquidations.
- 16 cells tested (horizons/leverage/MMR/long-short); no robust incremental skill after Holm correction. Firewall/decision log enforce separation.
- **Conclusion:** Cross-contamination impossible. Separation definitively proven.

## Evidence/artifacts strengthened
- `research_state/track_c_consolidated_dossier.md` - forensic re-audit added
- `research_state/track_a_deadend_map.md` - machine-checkable firewall + bottleneck analysis added
- `research_state/track_b_definitive_separation_audit.md` - separation audit + code-path tracing added
- `research_state/AGENT_HANDOFF_OUTCOME.md` - this document (full evidence summary)

## Bottlenecks removed/documented
- **Data access (Track A):** Exhaustive probe with hard rubric; dead-end made irrefutable (URLs/HTTP behavior, periods, coverage). No further blind retries possible.
- **Compute/analysis:** Leveraged cached data/zips; focused on forensic re-audit of sealed results without re-tuning.
- **Evidence:** Concrete numbers/tables in dossiers; provenance/hashes/splits documented.
- **Handoff:** This remains single source of truth; next agent cannot avoid heavy work (see hardening audit).

## Tests
- `python -m unittest discover -s tests -v` → **19/19 PASS**

## Next agent directive
Continue heavy evidence campaign per AGENT_HANDOFF.md priorities (C > A > B). Do not do status-only work. If new admissible unauthenticated liquidation source appears, must pre-register before inspection and pass full rubric. Preserve negatives, enforce track separation, never violate constraints.
