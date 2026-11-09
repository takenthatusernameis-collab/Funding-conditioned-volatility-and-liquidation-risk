# Gate 4 v4 EXPLORATORY NO-GO note — funding ablations on local 2024-04..09 slice (audit copy)

**20261109T053308Z — EXPLORATORY / NOT CONFIRMATORY / NOT PROMOTABLE**
- Git SHA: `d7a764b9e9411f58b8dca3abe8251f6780c5d6d4`
- Prereg: `research_state/pre_registration_gate4_funding_multisplit_v4_20261107T1845Z.json` — `FROZEN_BEFORE_OUTCOMES`, `confirmatory_claim_go=NO_GO`, `exploratory_smoke_authorized_after_freeze=true`
- Canonical note: `research_state/gate4_v4_exploratory_nogo/gate4_v4_exploratory_nogo_20261109T053308Z.md`

**Verdict (EXPLORATORY NO-GO — not confirmatory):** Principled leakage-safe stabilization (scale-aware ridge, train-only target-scale floor, train-only winsor, block bootstrap by UTC time blocks, chronological splits, train-only normalization) does NOT improve out-of-sample QLIKE vs the RV-only baseline A; it catastrophically degrades it (V3 E vs A ΔQLIKE +1096 CI [331, 2104], significantly worse; V4 +1421 CI [414, 2995]; B vs A amplified split-3 QLIKE 45→1029). No variant and no leave-one-instrument-out drop shows improvement. Funding ablations B/C/D/E show no credible incremental forecast skill on this local 2024-04..09 slice. Status: EXPLORATORY_ONLY, NO-GO. Not confirmatory. Not promotable. No sealed-anchor reuse.
