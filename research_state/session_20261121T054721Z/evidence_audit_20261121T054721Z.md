# FCLR-XSEC-008 Evidence Audit — Alternative Regime Conditioning (RV168/RV24 voV terciles)

**Session UTC:** 20261121T054721Z
**Experiment ID:** FCLR-XSEC-008-20261121T054721Z
**Audit scope:** Heavy artifact triad + recompute + evidence audit + trigger check for the FCLR-XSEC-008 campaign.

## 1. Artifacts present (all non-empty, no zero-byte placeholders)

| Artifact | Role |
|----------|------|
| fclr_xsec008_protocol_freeze_20261121T054721Z.json + .md | Preregistered protocol freeze, pre-outcomes |
| fclr_xsec008_evaluation_20261121T054721Z.py + .json + .md | Joint evaluation (Primary A voV->RV; Primary B voV->notional-weighted liq intensity; block bootstrap + Holm + 2% floor) |
| fclr_xsec008_recompute_20261121T054721Z.py + .json | Independent second-code-path recompute |
| evidence_audit_20261121T054721Z.json + .md | This evidence audit |
| trigger_check_20261121T054721Z.json | Non-empty trigger check enumerating PASS/FAIL acceptance checks |

Zero-byte placeholders: none. Empty artifacts: none.

## 2. Panel hash audit (both frozen panels, hash-verified)

- FCLR-001 panel `research_state/fclr011_recompute_panel_20261115T234700Z.parquet`: expected sha256 `41962f823e59de5989c7d854cb3180cad61a4cbc2f5f230133c41b321342c1f4`; asserted and verified at the top of both evaluation and recompute scripts.
- Combined liquidation panel `research_state/fclr_liq_combined_panel_20261115T181405Z.parquet`: expected sha256 `81a100d5d0625832bebabaabea13b786e15319577721cfe8507da5b779ec7f14`; asserted and verified at the top of both scripts.

No panel rebuild, no substitution, no new data, no network, no credentials.

## 3. Freeze-order audit

- `outcome_data_inspected_before_freeze` = false (recorded in protocol freeze, evaluation, and recompute).
- Protocol freeze precedes evaluation; no holdout outcomes inspected before freeze.

## 4. Recompute concurrence (independent code path)

- Independent implementation: numpy.random.Generator (PCG64) block bootstrap, manual hour-by-tercile grouping, independent Holm step-down.
- Recompute verdict: NOT_SUPPORTED; Evaluation verdict: NOT_SUPPORTED.
- Concurrence: TRUE — the verdict is not a single-implementation artifact.

## 5. Sealed-mutation audit

- `research_state/research_protocol.md` (sealed legacy FCLR-001 2024-01..03): NOT modified.
- `.github/workflows/`: NOT modified.

## 6. Root churn audit

- No root-level `research_state/*.md` or `research_state/*.json` added. All artifacts under `research_state/session_20261121T054721Z/`.
- Root churn cap 499/500 respected.

## 7. No re-run of terminal campaigns

FCLR-STARTER-001, FCLR-XSEC-001, FCLR-XSEC-002, FCLR-XSEC-003, FCLR-XSEC-004, FCLR-XSEC-005, FCLR-XSEC-006, FCLR-XSEC-007: none re-run. FCLR-XSEC-008 is a distinct estimand (voV ratio terciles vs RV tercile / UTC session bucket).

## 8. Network / paid data audit

- No network calls, no paid data, no credentials, no new data acquisition. Frozen panels only.

## 9. Track separation

- Observed liquidations (Track A) only; no conflation with modeled boundary breaches (Track B) or RV forecasts.

## 10. Cross-reference audit

Evaluation, recompute, and evidence audit explicitly cross-reference FCLR-XSEC-002, XSEC-004, XSEC-005, XSEC-006, XSEC-007.

## 11. Verdict integrity

- Verdict: NOT_SUPPORTED (honest null preserved).
- Primary A (voV HIGH tercile funding->RV): PASSED all three gates (CI [-0.000160, -0.000060] excludes zero, Holm adj_p=0.0, materiality 0.145 >= 0.02). Sign negative — a sign reversal versus FCLR-XSEC-002's positive contrast; sign is not a gate criterion and is reported honestly.
- Primary B (voV any-tercile funding->notional-weighted liq intensity): FAILED all three terciles (CI include zero; Holm adj_p 0.297–0.857).
- Joint gate: False (requires BOTH primaries).
- 2% materiality floor NOT relaxed after seeing outcomes; no threshold-shopping.

## 12. Distinct from

FCLR-STARTER-001, FCLR-XSEC-001, FCLR-XSEC-002 (RV tercile), FCLR-XSEC-003, FCLR-XSEC-004 (count-based RV tercile), FCLR-XSEC-005 (notional-weighted RV tercile), FCLR-XSEC-006 (UTC session bucket), FCLR-XSEC-007 (terminal NOT_SUPPORTED), FCLR-LIQ-XSEC-ORDERING, FCLR-LIQ-XSEC-QLIKE.

## 13. Conclusion

The FCLR-XSEC-008 heavy artifact triad is complete and internally consistent: protocol freeze (pre-outcomes), joint evaluation, independent recompute (concurs), evidence audit, and non-empty trigger check are all present under `research_state/session_20261121T054721Z/`. The joint verdict is NOT_SUPPORTED: the funding->RV effect replicates under voV conditioning (Primary A), but the funding->notional-weighted-liquidation-intensity effect does not (Primary B), so the joint claim fails. This is an honest, pre-registered, heavy result exercising both halves of the repository name (funding-conditioned volatility AND liquidation risk).
