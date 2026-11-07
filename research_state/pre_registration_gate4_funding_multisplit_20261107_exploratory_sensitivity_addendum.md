# Exploratory Sensitivity Addendum — Gate 4 Funding Multi-Split Pilot

**parent:** `research_state/pre_registration_gate4_funding_multisplit_20261107.md` (GATE4-FUNDING-MULTISPLIT-PILOT-20261107, frozen 2026-11-07T01:36:11Z)
**addendum_id:** GATE4-FUNDING-MULTISPLIT-PILOT-20261107-EXPL-SENS-001
**frozen_before_outcomes:** true (written 2026-11-07T03:20:00Z before computing/reporting sensitivity outputs from updated script)
**status:** EXPLORATORY — not confirmatory, not claim-bearing, not a gate pass

## Scope (fixed before running)
- **Primary contrast unchanged:** E vs A (ΔQLIKE, alt-base). All primary metrics/splits/ablations unchanged.
- **Exploratory only:** block-bootstrap block size sensitivity {12h, 24h, 48h} for paired ΔQLIKE vs A (B/C/D/E vs A) using the same pooled paired observations, same seed=12345, same reps=2000, same alpha=0.05, two-sided percentile CI, circular block bootstrap resampling whole UTC time blocks jointly across instruments.
- **Exploratory reporting:** per-split paired ΔQLIKE(E vs A and secondaries) table for instability visibility (derived from the same pre-registered splits/predictions; no new contrast).

## Interpretation rules
- Primary remains block=24h per parent prereg.
- If sign/CI stability changes materially across block sizes, record instability; **do not promote**.
- Sensitivity does not relax data-sufficiency/claim-worthy criteria and does not create a confirmatory claim.
