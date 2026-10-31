# Track C Final Synthesis Dossier — Funding-Conditioned Volatility Forecasting

**Report ID:** FCLR-TRACKC-SYNTH-001
**Date (UTC):** 2026-10-31T09:10:42Z
**HEAD:** 52506b1a
**Priority:** Track C (FIRST) per repo name inference
**Status:** CLOSED_NEGATIVE / NOT_SUPPORTED
**Decision:** No risk overlay eligible. No valid reopen under current constraints.

## Traceability
- Protocols: `research_state/research_protocol.md`, `research_state/research_protocol_fclr006.md`, `research_state/research_protocol_fclr007.md`
- Manifests: `research_state/run_manifest.json`, `research_state/run_manifest_FCLR002.json`
- Evaluations: `research_state/evaluation_summary.md`, `research_state/evaluation_summary_FCLR003.md`, `research_state/evaluation_summary_FCLR006.md`, `research_state/evaluation_summary_FCLR007.md`, `research_state/evaluation_summary_FCLR002.md`
- Consolidated: `research_state/track_c_consolidated_dossier.md` (FORENSIC_REAUDIT_20261031), `research_state/track_c_residual_audit.md`
- Verdicts: `research_state/final_confirmatory_verdict.md`, `research_state/structural_closure_verdict_heavy.md`

## Frozen splits / embargoes / blocks (verbatim)
**FCLR-003 (canonical confirmatory, powered)**
- Train: 2024-04-01T00:00:00Z .. 2024-07-23T23:00:00Z
- Val:   2024-07-31T00:00:00Z .. 2024-09-24T23:00:00Z
- Test:  2024-10-02T00:00:00Z .. 2024-12-31T23:00:00Z (7d embargo)
- Paired instruments: BTCUSDT, ETHUSDT, BNBUSDT, SOLUSDT, XRPUSDT
- Paired OOS n: 10796
- Blocks: >=3 non-overlapping 30-day blocks (confirmed)

**FCLR-006 (unsealed)**
- Window: 2026-05-23T00:00:00Z .. 2026-08-06T23:00:00Z (2 blocks < 3)
- Paired n: 8987
- Status: UNDERPOWERED, COMPLETE_NEGATIVE

**FCLR-007 (unsealed)**
- Window: 2026-07-21T00:00:00Z .. 2026-07-31T23:00:00Z (0 blocks < 3)
- Paired n: 1195
- Status: UNDERPOWERED, COMPLETE_NEGATIVE

## QLIKE decomposition (lower better)
**FCLR-003 (test set)**
| Model | mean_QLIKE | n |
|-------|------------|---|
| B0    | 0.487674   | 10800 |
| B1    | 0.401884   | 10796 |
| C1    | 0.369366   | 10796 |
| C2    | 0.417089   | 10796 |

**Paired comparisons (block bootstrap, ~24h blocks, 2000 reps)**
| Contrast | Mean diff (A-B), QLIKE | 95% CI | Relative reduction | Verdict |
|----------|--------------------------|--------|-------------------|---------|
| C2 vs B1 (PRIMARY) | +0.015205 | [-0.020240, 0.056734] | -3.78% (worse) | **FAIL** (CI crosses zero) |
| C1 vs B1 (secondary) | -0.032518 | [-0.045813, -0.020303] | +8.09% (better) | Better alone, not primary claim |
| C2 vs C1 | +0.047723 | [0.006214, 0.095465] | -12.92% (worse) | Adding price features hurts when added to C1 |

**FCLR-006**: C2 vs B1 +0.368588 QLIKE, CI entirely positive → WORSE, -69.90% rel (NOT_MET)
**FCLR-007**: C2 vs B1 +0.010258 QLIKE, CI [0.001308, 0.019737] entirely positive → WORSE, -3.42% rel (NOT_MET)

## Leakage / integrity checks (cross-checked)
- Normalization fit only on training period (protocol enforced)
- Purge/embargo applied (7d embargo in FCLR-003)
- Chronological walk-forward / frozen splits; no random split
- Features computed with information available at forecast timestamp
- No holdout inspection before freezing; sealed holdouts preserved
- Block structure verified for bootstrap

## Gate assessment (pre-registered)
- >=2% relative QLIKE reduction (C2 vs B1): **NOT_MET**
- 95% CI excludes zero: **NO**
- >=5 paired OOS instruments: **PASS**
- >=3 non-overlapping 30-day blocks: **PASS (FCLR-003 only)**
- **FORECAST GATE: NOT_MET → Risk overlay INELIGIBLE**

## Final conclusion (Track C)
**H001 (FCLR-H001): NOT_SUPPORTED.** Adding funding extremes plus pre-specified price-dislocation/smoothing features does not improve OOS 24h realized-variance forecasts over RV-only HAR on frozen confirmatory panel. All tested panels fail gate; risk overlay ineligible. No reopen path without violating pre-registration/holdout discipline.
