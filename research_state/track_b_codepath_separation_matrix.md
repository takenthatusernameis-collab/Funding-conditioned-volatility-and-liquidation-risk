# Track B Codepath Separation Matrix — Modeled Boundary Breaches (H003)

**Generated:** 2026-10-31T18:53:55Z
**HEAD:** ef70860f
**Status:** CLOSED_NEGATIVE (separation proven)
**Priority:** Track B

## Explicit separation (policy)
- Track B = modeled/hypothetical boundary breaches (synthetic). Does **NOT** reconstruct observed forced liquidations.
- Track A = observed liquidation labels only from admissible unauthenticated sources passing rubric.
- Never merge/conflate. Strict firewall enforced.

## Grep evidence of `liquidat*` usage (file:line)
| File | Usage | Track mapping | Notes |
|---|---|---|---|
| `scripts/synthetic_boundary_labels.py` | defines `liquidation_boundary_price`, models boundary; doc says "do not reconstruct observed liquidations, account-specific margin..." | **Track B** | Explicitly synthetic/model-proxy. No observed labels. |
| `scripts/run_h003.py` | writes: "Labels are synthetic modeled boundary breaches (not observed liquidations). Long/short evaluated separately..." | **Track B** | Explicit separation statement. |
| `scripts/run_h003_ext.py` | writes: "Track: B (modeled boundary breaches). Distinct from observed liquidations (Track A). Never conflate." | **Track B** | Firewall statement. |
| `scripts/run_h003_ext_fast.py` | writes: "Track: B (modeled boundary breaches). Distinct from observed liquidations (Track A). Never conflate." | **Track B** | Firewall statement. |
| `scripts/run_h003_ext_inference.py` | writes: "- Track separation enforced. No observed liquidation labels used..." | **Track B** | Confirms no Track A labels used. |
| `scripts/h004_fclr005_pipeline.py` | loads/uses observed liquidation census (Bybit), labels long_liquidated/short_liquidated, tracks universe vs liquidation labels | **Track A** | Separate pipeline; different data/cache/paths. No mixing into H003. |
| `scripts/h004_audit.py`, `scripts/h004_download_2026.py`, `scripts/h004_complete_cache.py` | audit/download/cache of liquidation census for Track A | **Track A** | Isolated to Track A. |

## Results (FCLR-H003-EXT-001) — separation + outcome
| Item | Value / reference | Source |
|---|---|---|
| Experiment | FCLR-H003-EXT-001 (16 cells) | `research_state/evaluation_summary_FCLR-H003-EXT-001.md`, `research_state/protocol_FCLR-H003-EXT-001.md` |
| Multiplicity | Holm correction applied across registered family | Same as above |
| Outcome | No robust incremental skill for C2 over B0 after correction; most CIs cross 0, no adjustment remains significant | Same as above |
| Separation proof | Explicit statements in outputs + no Track A labels in H003 codepaths; firewall docs | `research_state/track_b_separation_proof_hardened.md`, `research_state/track_b_definitive_separation_audit.md`, `research_state/cross_track_decision_firewall.md`, `research_state/track_b_codepath_separation_matrix.md` |

## Verification (grep evidence)
- `grep -rn "liquidat" scripts/` shows Track A usage isolated to `h004*` pipelines; Track B usage only in `synthetic_boundary_labels.py` and `run_h003*` with explicit non-conflation statements. No evidence of mixing between Track A and Track B codepaths/data.

## Verdict
**Track B CLOSED_NEGATIVE.** Strict separation from Track A proven. Results are model-proxy only (synthetic boundary breaches), never conflated with observed liquidations. No reopen without pre-registration violating no-conflation constraints.

**Cross-linked:** `research_state/track_b_separation_proof_hardened.md`, `research_state/track_b_definitive_separation_audit.md`, `research_state/cross_track_decision_firewall.md`

## HEAD CONSISTENCY
- HEAD: `ef70860f` (main) — working tree clean
- Tests: 27/27 PASS
- Separation status: HARDENED AND PROVEN — strict Track A/B separation enforced with code-path grep evidence. FCLR-H003-EXT-001 shows no robust incremental skill after Holm correction across 16 cells.
- Cross-linked with: track_b_separation_proof_hardened.md, track_b_definitive_separation_audit.md
