# Evidence Audit — session_20261118T182813Z

- **Timestamp (UTC):** 20261118T182813Z
- **Campaign:** `FCLR-LIQ-RISK-CALIBRATION-06-20261118T182600Z` (Track B breach-risk calibration)
- **Network used:** none. No installs, no `git lfs pull`, no HF probes.
- **Writes:** session dir only + `AGENT_HANDOFF.md` (sole durable handoff). No root `research_state/*.md|json` added.
- **Outcome inspected before prereg freeze:** false (prereg written first).

## Artifacts (all non-empty)
- Prereg: `fclr_risk06_prereg_20261118T182813Z.json/.md` — frozen before evaluation.
- Labels: `fclr_risk06_labels_20261118T182813Z.py/.json/.md` — multi-month modeled breach labels, 262080 rows, 6241 breached (rate 0.023813339438339437).
- Calibration: `fclr_risk06_calibration_20261118T182813Z.py/.json/.md` — verdict `HONEST_NEGATIVE_OR_INCONCLUSIVE`.
- Trigger check: `trigger_check_20261118T182813Z.json` — all four triggers OPEN, none fired.
- Recompute: `recompute_fclr_risk06_calibration_20261118T182813Z.json` — RECONCILED_ZERO_DISCREPANCIES, 0 discrepancies.

## Result
- Primary scenario `L10|long|H24`; floor_met = **False**.
- Beat-B0 holdouts: B1 1/3, B2 0/3.
- Real mean ΔBrier (B1) 0.000209; placebo mean -0.000439.
- Effect sizes are ~1e-4 Brier units against a baseline of ~2e-2; both signs occur across holdouts.

## Prohibitions respected
- No sealed re-score, no sealed-month read, no network, no root `research_state/*.md|json`, no sealed-artifact/workflow mutation, no Track C QLIKE rerun, no zero-byte artifacts.

## Honest status
- EXPLORATORY/PILOT. Modeled boundary breaches only; not observed liquidations. No confirmatory promotion claimed.
