# FCLR-LIVE-ARCHIVE-06 Preregistration (20261126T133828Z)
**Experiment:** FCLR-LIVE-ARCHIVE-06
**Outcome-data inspected before freeze:** False
**Target:** next-24h downside realized-semivariance level log(RV_minus+1e-09).
**Models:** B1 = OLS signed-component HAR (7 feats); C2 = B1 + funding + price features (11 feats).
**Primary contrast:** C2 vs B1 paired test-set out-of-sample MSE. Materiality floor: 2% relative reduction.
**Decision rule:** PROMOTED iff relative MSE reduction >=2% and bootstrap 95% CI lower bound > 0; else NOT_SUPPORTED; INCONCLUSIVE if insufficient data.
**Source registry sha256:** 5222b9b68f09a8176e2aee715bb1164ad6b4181be1568dcedc1153d5b78eff47
