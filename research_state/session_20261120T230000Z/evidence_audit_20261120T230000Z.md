# Evidence Audit — FCLR-XSEC-004 (session_20261120T230000Z)

- **Campaign:** FCLR-XSEC-004-20261120T225115Z
- **Estimand:** regime-conditioned cross-sectional funding effect on **next-hour observed liquidation intensity** (distinct from the FCLR-XSEC-002 RV estimand)
- **Panel:** `research_state/fclr_liq_combined_panel_20261115T181405Z.parquet` (1,740,415 rows, 15 coins, 10,052 hourly buckets, zero-null features)
- **Panel sha256 (verified on disk):** `81a100d5d0625832bebabaabea13b786e15319577721cfe8507da5b779ec7f14`
- **Outcome data inspected before freeze:** `false` (protocol frozen before any liquidation outcome was examined)
- **Verdict:** **SUPPORTED**

## Verdict basis

1. **Low-RV regime funding contrast** — high-minus-low funding next-hour liquidation intensity: mean diff `+643,509.56`, 95% block-bootstrap CI `[448,605.26, 841,155.73]` (excludes zero), p = 0.0, Holm adj_p = 0.0 (passes), materiality effect `0.80 ≥ 0.02` floor (passes).
2. **High-RV regime funding contrast** — mean diff `+141,973.81`, CI `[-125,531.60, 393,874.14]` (includes zero), p = 0.263, Holm adj_p = 0.263 (fails). Preserved as an **honest null** within the 4-test family.
3. **Both within-regime RV-persistence baselines** — CI excludes zero, p = 0.0, Holm passes; confirms the contrast family is not degenerate.
4. **Independent recompute** — `recompute_fclr_xsec004_20261120T230000Z.py` (separate code path) reproduces all four tests and the SUPPORTED verdict exactly (`reproduces_fclr_xsec004 = true`).

## Regime note

The liquidation-intensity funding signal is concentrated in the **LOW** market-wide-RV regime, the mirror image of the FCLR-XSEC-002 RV finding (signal in the **HIGH** regime). Both halves of the repository mandate are now SUPPORTED but are **regime-distinct**, strengthening rather than duplicating the result. The high-RV liquidation contrast is an honest null and is not threshold-shopped.

## Artifacts (all under `research_state/session_20261120T230000Z/`)

- `fclr_xsec004_protocol_freeze_20261120T230000Z.{json,md}`
- `fclr_xsec004_evaluation_20261120T230000Z.{py,json}`
- `recompute_fclr_xsec004_20261120T230000Z.{py,json}`
- `trigger_check_20261120T230000Z.json`
- `evidence_audit_20261120T230000Z.{json,md}`

## Constraints honored

- No root-level `research_state/*.md|json` added (root count stays 499/500).
- No overwrite of sealed `research_state/research_protocol.md`.
- No re-run of FCLR-STARTER-001 / FCLR-XSEC-001 / FCLR-XSEC-002 / FCLR-XSEC-003.
- No modification of `.github/workflows`.
- No network, no paid or credentialed data.
- Liquidation outcomes not inspected before the protocol freeze.