# Cross-Track Decision Firewall (Immutable)

**Document type:** Decision-grade firewall preventing premature reopening/reuse
**Generated:** 2026-10-31T04:26:00Z
**HEAD:** 92d6e6ec4f0277078cdf362b0e022eb604b67e55
**Status:** IMMUTABLE — SEALED

## Decision matrix (H001-H004)
| Hypothesis | Track | Frozen protocol | Evidence | Gate | Outcome | Risk Overlay | Reopen Allowed? |
|---|---|---|---|---|---|---|---|
| H001 | C (Volatility) | `research_protocol*.md`, pre-registered before outcomes | FCLR-001-003,006,007; byte-identical repro; block structure; Holm | C2 vs B1 ΔQLIKE, ≥2 blocks, CI excludes zero, rel improvement | **NOT_SUPPORTED** | **INELIGIBLE** | **NO** — would violate pre-registration/holdout discipline |
| H002 | A (Observed liquidations) | `next_data_discovery_plan.md`, GO/NO-GO rubric | Exhaustive probe of all admissible families (Binance/OKX/Bybit/Deribit, Zenodo/OSF/arXiv, GitHub, HF 2026-only, CryptoDataDownload, Tardis paywalled) | ≥5 symbols, ≥3 non-overlapping 30d blocks, documented completeness, license OK, unauthenticated | **BLOCKED (NO-GO)** | **INELIGIBLE** | **ONLY** if NEW admissible unauthenticated data meets all criteria AND pre-registered BEFORE outcome inspection |
| H003 | B (Modeled boundary breaches) | `protocol_FCLR-H003-EXT-001.md`, pre-registered | FCLR-001-H003, FCLR-002-H003, FCLR-H003-EXT-001 (16 cells); Holm correction | Incremental skill over B0 on Brier/log-loss with separation | **COMPLETE_NEGATIVE** | **INELIGIBLE** | **NO** — closed negative; cannot rescue A or C |
| H004 | Correction-time replication (Shek) | As feasible from public data | 88 events Jan-Mar 2024; RV-regime contrast infeasible (no mark prices); SSRN 403 | Independent reconstruction | **PARTIAL_REPLICATION** | **INELIGIBLE** | **ONLY** if full methodology reconstructible from admissible public sources |

## Hard gates (enforced)
- **Chronological:** Walk-forward/expanding window; no random splits
- **Sealed holds:** Tune only in train/val; holdout sealed; no re-tuning/threshold shopping/holdout reuse
- **Purge/embargo:** ≥ max horizon between folds
- **Normalization:** Training-period only
- **Multiplicity:** Holm FWER across declared family
- **Separation:** A observed / B modeled / C volatility — never conflated
- **Data admissibility:** No credentials/paid/manual; verify unauthenticated path
- **Provenance:** Provenance, hashes, manifests required
- **No trading:** No live/paper trading, no order logic

## Firewall rules
1. **No re-execution of sealed confirms:** FCLR-003, FCLR-006, FCLR-007 are sealed. No recompute with different params.
2. **No grid expansion:** Feature sets frozen per protocol; no unregistered ablations on holdouts.
3. **No track conflation:** Modeled breaches ≠ observed liquidations. Volatility skill ≠ liquidation predictability.
4. **Reopen requires evidence:** Track A reopen requires machine-checkable evidence meeting all criteria + pre-registration.
5. **Workflow protected:** No `.github/workflows/*` changes without explicit maintainer auth.

## Conclusion
Risk overlay INELIGIBLE across all tracks. Structural closure confirmed. Firewall prevents bottlenecks from being reintroduced.
