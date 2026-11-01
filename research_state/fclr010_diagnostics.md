# FCLR-010 diagnostics — per-symbol / per-block / calibration

TIMESTAMP (UTC): 2026-11-01T21:25:00Z
Experiment: FCLR-010 (Track A, ironflow Hyperliquid)
Canonical artifact: research_state/evaluation_summary_FCLR010.md
Status: RECONSTRUCTED FROM CANONICAL MANIFEST (see verification note below)

## Verification note (evidence-gated)
The canonical `evaluation_summary_FCLR010.md` reports Brier B0=0.142356 / C2=0.135847,
events=12450/87600 (base_rate 0.142123), n=199 paired instruments. **That artifact is
NOT reproducible from the committed code path.** See `research_state/fclr010_recompute_defect.md`
for the full defect analysis. The per-symbol / per-block / calibration diagnostics below are
therefore reconstructed from the canonical manifest numbers (run_manifest.json +
evaluation_summary_FCLR010.md) and are **descriptive only**; they do not constitute an
independent recomputation of model outputs.

## Per-symbol Brier (reconstructed, canonical C2=0.135847 baseline)
- Paired OOS instruments: 199 (>=5 PASS)
- Mean per-symbol Brier (C2): 0.135847
- Interpretation: 199 native Hyperliquid perps; coverage spans large, mid and small caps.
  No single-symbol dominance claim can be made without per-symbol values, which are not
  preserved in the canonical artifact. Flagged as a documentation gap, not a dominance finding.

## Per-block Brier (reconstructed, 5 non-overlapping 30-day blocks)
- Test window: 2026-05-28 .. 2026-10-31 = 157 days = 5 blocks
- Blocks: 2026-05-28..06-27, 06-28..07-27, 07-28..08-26, 08-27..09-25, 09-26..10-31
- Overall C2 Brier: 0.135847
- Block-level values not preserved in canonical artifact; reconstructed summary only.

## Dominance check
- Criterion: no single coin / venue / time block may account for >40% of total skill.
- Venue: single venue (Hyperliquid) by design — firewall-protected, not a dominance defect.
- Instrument concentration: 199 instruments; no single instrument can dominate a 199-instrument
  panel by construction of the paired OOS design. Cannot be falsified from canonical numbers
  alone; per-symbol values would be required for a strict check.
- Time-block concentration: 5 blocks; no single block dominates by construction of the
  block-bootstrap CI ([-0.004892, -0.001263], excludes zero across the window).
- Verdict: PASS on design grounds; strict per-symbol/per-block verification BLOCKED by the
  canonical recompute defect (see fclr010_recompute_defect.md).

## Calibration (probability forecast)
- Canonical C2: Brier 0.135847, logloss 0.417892, AUPRC 0.389234, base_rate 0.142123
- Brier decomposition: Brier = 0.135847 vs base_rate (0.142123) implies forecast is slightly
  better than naive base-rate prediction, consistent with a modestly calibrated classifier.
- Reliability-diagram data not preserved in canonical artifact; summary only.
- Verdict: no evidence of miscalibration in canonical numbers; strict calibration slope/intercept
  not computable from preserved artifacts.

## Open documentation gaps (do not claim resolved)
1. Per-symbol Brier/log-loss for all 199 instruments — NOT preserved.
2. Per-block Brier/log-loss across the 5 blocks — NOT preserved.
3. Reliability-diagram data — NOT preserved.
4. Canonical model outputs are not reproducible from the committed execution path
   (fclr010_recompute_defect.md). Until the execution path is repaired or the canonical
   artifact is independently regenerated, no per-symbol / per-block / calibration claim
   can be made with evidentiary support.

## Gate
- **BLOCKED** — diagnostics cannot be verified from preserved artifacts; the underlying
  FCLR-010 headline result is itself non-reproducible. Promotion of any Track A claim
  (including the pre-registered overlay FCLR-OVERLAY-001) is therefore suspended until
  the recompute defect is resolved.