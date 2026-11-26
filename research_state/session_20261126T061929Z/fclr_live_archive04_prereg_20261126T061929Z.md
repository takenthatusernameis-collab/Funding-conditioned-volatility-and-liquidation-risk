# FCLR-LIVE-ARCHIVE-04 Preregistration (20261126T061929Z)
**Experiment:** FCLR-LIVE-ARCHIVE-04
**Outcome-data inspected before freeze:** False
**Target:** next-24h RV (continuous) as a predictive distribution at quantiles [0.1, 0.25, 0.5, 0.75, 0.9].
**Models:** B1 = linear quantile HAR (log RV1h/24h/168h); C2 = B1 + funding + price features.
**Primary contrast:** C2 vs B1 paired test-set average pinball loss. Materiality floor: 2% relative reduction.
**Decision rule:** PROMOTED iff relative avg-pinball reduction >=2% and bootstrap 95% CI lower bound > 0; else NOT_SUPPORTED; INCONCLUSIVE if insufficient data.
**Source registry sha256:** aeaa5aa6833ebad0034fd527b3c19631a7f095b593623a37fe6681091d4cb1a0
