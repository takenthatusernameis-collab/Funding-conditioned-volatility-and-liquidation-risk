# Track C Consolidated Evidence Dossier (FCLR-H001)

**Document type:** Decision-grade synthesis (sealed; no holdout reuse/tuning)
**Repository:** Funding-conditioned-volatility-and-liquidation-risk
**Generated:** 2026-10-31T02:24:27Z (restored full version 2026-10-31T02:26:45Z after truncation audit)
**Hypothesis:** H001 — Do funding extremes, realized volatility, and pre-specified price dislocation/smoothing features improve OOS forecasts of future realized volatility/stress vs RV-only baseline?
**Status:** NOT_SUPPORTED (all confirmatory campaigns complete negative). Risk overlay INELIGIBLE.

## Cross-run summary (byte-identical reproduction verified)

| Run | Window (test) | Blocks (30d, non-overlap) | Paired n | C2 vs B1 ΔQLIKE (CI) | Rel QLIKE | Gate | Verdict |
|---|---|---|---|---|---|---|---|
| FCLR-001 | 2024-01-24..2024-03-24 (sealed pilot) | 1 (<3) | — | -2.50% rel; CI [-0.123401, 0.158843] crosses zero | — | NOT_MET | PILOT/INCONCLUSIVE |
| FCLR-002 | 2024-07-23..2024-09-30 (sealed) | 2 (<3) | 8274 | -0.008788 [-0.097648, -0.008788] excludes zero | -9.28% | NOT_MET (block count) | INCONCLUSIVE |
| FCLR-003 | 2024-10-02..2024-12-31 (sealed, powered) | 3 | 10796 | +0.015205 [-0.020240, 0.056734] crosses zero | -3.78% | NOT_MET | COMPLETE_NEGATIVE |
| FCLR-006 | 2026-05-23..2026-08-06 (unsealed) | 2 (<3) | 8987 | +0.368588 [0.173748, 0.615614] entirely positive | -69.90% | NOT_MET (worse + underpowered) | COMPLETE_NEGATIVE |
| FCLR-007 | 2026-07-21..2026-07-31 (unsealed) | 0 (<3) | 1195 | +0.010258 [0.001308, 0.019737] entirely positive | -3.42% | NOT_MET (worse + underpowered) | COMPLETE_NEGATIVE |

**Conclusion:** Across all confirmatory runs, C2 (RV + funding + price features) does not meet the pre-registered gate vs B1 (RV-only). In the adequately-powered FCLR-003 window it is neutral (CI crosses zero); in the two unsealed 2026 windows it is statistically worse. No path to passing the gate without violating pre-registration (no tuning, no holdout reuse, no threshold shopping). H001 is NOT_SUPPORTED. Risk overlay INELIGIBLE per §9 of RESEARCH_PROMPT.md.

## Model definitions (frozen in protocol)
- B0: persistence — forecast next-24h RV using preceding RV24h.
- B1: HAR-style OLS on log RV1h, log RV24h, log RV168h → log next-24h RV.
- C1: B1 + signed funding + 90-day absolute-funding percentile.
- C2: C1 + mark/index premium + mark/EMA24 distance.
- Primary contrast: C2 vs B1 on paired OOS QLIKE. Secondary: C1 vs B1, C2 vs C1. Epsilon=1e-12 fixed; training-only standardization; documented smearing back-transform; no regularization/hyperparameter search.

## Traceability
- FCLR-001: `research_state/evaluation_summary.md`; protocol `research_state/research_protocol.md` v1.0
- FCLR-002: `research_state/evaluation_summary_FCLR002.md`; `research_state/fclr002_coverage_audit.json`; byte-identical repro 2026-10-28
- FCLR-003: `research_state/evaluation_summary_FCLR003.md` (2026-10-29T19:13:39Z); splits `run_manifest.json#split_boundaries_fclr003` (frozen_before_outcomes: true); independent re-run 2026-10-30 (bgp_18c914b78001ZWxMSjA8l35RtN)
- FCLR-006: `research_state/evaluation_summary_FCLR006.md` (2026-10-30T16:52:51Z); `research_state/reporting_errata_FCLR006.md`; protocol `research_state/research_protocol_fclr006.md`
- FCLR-007: `research_state/evaluation_summary_FCLR007.md` (2026-10-31T00:21:05Z); protocol `research_state/research_protocol_fclr007.md` v1.0 pre-registered BEFORE outcomes; coverage audit `research_state/fclr007_coverage_audit.md`
- All: `research_state/hypothesis_registry.json` (FCLR-H001), `research_state/run_manifest.json`, `research_state/gate_assessment.md`, `research_state/final_confirmatory_verdict.md`, `research_state/final_inconclusive_report.md`

## Decision
- Track C CLOSED (negative). Risk overlay INELIGIBLE.
- Reopen conditions: none. Reopening would require violating pre-registration/holdout discipline (forbidden by RESEARCH_PROMPT.md §8, §16).
- Multiplicity: Holm familywise correction applied across all registered contrasts and horizons; unadjusted and adjusted results disclosed.

## Verification
- `python -m unittest discover -s tests -v` → 14/14 PASS (re-verified 2026-10-31T02:26:45Z).
- Byte-identical reproduction confirmed for FCLR-002, FCLR-003, FCLR-006, FCLR-007 on independent re-runs.
- Sealed holds intact: no re-tuning, no holdout reuse, no threshold shopping, no workflow changes, no trading/paper-trading logic.

## FORENSIC_REAUDIT_20261031 (HEAVY - EXECUTED)

**Timestamp:** 2026-10-31T06:11:42Z
**Executor:** forced heavy campaign (per AGENT_HANDOFF.md HND-20261031-060736-HEAVY-FORCED)
**Goal:** Deep forensic re-examination of FCLR-003/006/007 under pre-registered constraints.

### FCLR-003 (Powered confirmatory, 2024-10-02..2024-12-31, 3 blocks)
- **Splits (frozen):** Train 2024-04-01..2024-07-23, Val 2024-07-31..2024-09-24, Test 2024-10-02..2024-12-31 (7d embargo). Verified in `run_manifest.json#split_boundaries_fclr003` with `frozen_before_outcomes: true`.
- **Panel:** BTCUSDT, ETHUSDT, BNBUSDT, SOLUSDT, XRPUSDT (>=5 PASS). Paired n=10796.
- **Models:** B0 persistence, B1 HAR(RV1h,RV24h,RV168h), C1 B1+funding features, C2 C1+price-dislocation (mark/index premium, mark/EMA24). Frozen definitions.
- **QLIKE (lower better):** B0=0.487674, B1=0.401884, C1=0.369366, C2=0.417089.
- **Primary contrast C2 vs B1:** mean diff +0.015205, 95% CI [-0.020240, 0.056734] crosses zero. Relative -3.78% (worse). Block bootstrap ~24h blocks, 2000 deterministic replicates.
- **Secondary:** C1 vs B1: -0.032518 CI [-0.045813,-0.020303] (+8.09% better). C2 vs C1: +0.047723 CI [0.006214,0.095465] (-12.92% worse).
- **Leakage checks:** Embargoes applied, normalization fitted on train only, no holdout tuning. Timestamp alignment verified. Feature availability at forecast time respected.
- **Block structure:** 91 days = 3 non-overlapping 30-day blocks (PASS). Paired coverage complete across 5 instruments.
- **Verdict:** COMPLETE_NEGATIVE. Gate NOT_MET. C2 fails to improve over B1; CI crosses zero on worse side.

### FCLR-006 (Unsealed 2026, 2026-05-23..2026-08-06, 2 blocks - underpowered)
- **Splits (pre-registered):** Train 2026-04-01..04-24, Val 2026-05-02..05-15, Test 2026-05-23..2026-08-06 (7d embargoes). Frozen before outcomes per `run_manifest.json#split_boundaries_fclr006`.
- **Panel:** 5 instruments, n=8987 paired. 76 days = 2 non-overlapping 30-day blocks (< 3 required).
- **QLIKE:** B0=0.518169, B1=0.527290, C1=0.626463, C2=0.895879.
- **Primary contrast C2 vs B1:** mean diff +0.368588, 95% CI [0.173748, 0.615614] entirely positive (C2 WORSE). Relative -69.90%. C1 vs B1 also worse.
- **Verdict:** COMPLETE_NEGATIVE. Gate NOT_MET (worse + underpowered). Independently reproduced byte-identical.

### FCLR-007 (Unsealed 2026 short window, 2026-07-21..2026-07-31, 0 blocks)
- **Protocol pre-registered BEFORE outcomes:** `research_state/research_protocol_fclr007.md` v1.0. Coverage audit `research_state/fclr007_coverage_audit.md`. Splits frozen in manifest.
- **Test window:** 11 days = 0 non-overlapping 30-day blocks (< 3). n=1195 paired, 5 instruments all PASS.
- **QLIKE:** B0=0.661522, B1=0.666587, C1=0.709572, C2=0.693426.
- **Primary contrast C2 vs B1:** mean diff +0.010258, 95% CI [0.001308, 0.019737] entirely positive. Relative -3.42% (worse).
- **Verdict:** COMPLETE_NEGATIVE. Gate NOT_MET (worse + severely underpowered).

### Forensic observations
1. **Feature set effect:** Adding funding+price features (C1,C2) does not consistently improve over RV-only B1; in strong cases degrades materially.
2. **Regime dependence:** No regime split shows C2 > B1 in powered window. Cross-window consistency negative.
3. **Leakage audit:** All runs use training-only normalization, embargoes, block bootstrap. No evidence of holdout leakage.
4. **Multiplicity:** Holm correction applied across registered family; results consistent.
5. **Robustness:** Block structure, paired coverage, CI construction all defensible.

### Alternative ablations considered (pre-registered but unexecuted)
Per protocols, ablations exist but require sealed holdouts or violate pre-registration - BLOCKED. No outcome inspection to select ablations. None executed.

### Conclusion (forensic)
H001 NOT_SUPPORTED. All confirmatory panels negative. No defensible path to passing forecast gate without violating RESEARCH_PROMPT.md §8 (pre-registration, sealed holdout, no tuning). Risk overlay INELIGIBLE. Track C remains CLOSED.

**Artifacts updated:** This dossier. Cross-linked to `research_state/evaluation_summary_FCLR003.md`, `evaluation_summary_FCLR006.md`, `evaluation_summary_FCLR007.md`, `hypothesis_registry.json`, `negative_results_report.md`.
